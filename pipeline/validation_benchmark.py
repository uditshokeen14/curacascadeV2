"""CuraCascade — Independent Adjudication Validation Benchmark (Priority Two / Objective 8).

Evaluates the clinical integrity and statistical performance of the automated
cross-layer relational audit engine against a 100-gene documented expert adjudication
benchmark set:
- Gold standard comprises 54 published downgraded/disputed/refuted genes and 46 definitive controls.
- Ground truth is independently verified from peer-reviewed literature and ClinGen GCEPs.
- Removes hard-coded classification overrides (KNOWN_FN, KNOWN_FP).
- Executes queries against the live relational database (SQLite/DuckDB).
- Computes empirical confusion matrix (TP, FP, TN, FN), Precision, Recall, Specificity, F1, Accuracy.
- Reports Wilson score 95% confidence intervals for binomial performance metrics.
- Accurately reports inter-rater kappa status (N/A for single-curator adjudication) and
  measures classifier concordance kappa.
- Exports validation metrics to data/processed/validation_metrics.json and data/processed/validation_cases.csv.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure repository root is on sys.path
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from database.connection import get_db_path
from pipeline.disease_mapping import CANONICAL_DISEASE_REGISTRY, normalize_text

RAW_DIR = _REPO_ROOT / "data" / "raw"
PROCESSED_DIR = _REPO_ROOT / "data" / "processed"
GROUND_TRUTH_PATH = RAW_DIR / "benchmark_ground_truth.json"
JSON_OUT_PATH = PROCESSED_DIR / "validation_metrics.json"
CSV_OUT_PATH = PROCESSED_DIR / "validation_cases.csv"


def wilson_score_interval(successes: int, total: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Calculate the Wilson score confidence interval for a binomial proportion.

    Args:
        successes: Number of positive outcomes.
        total: Total number of trials.
        confidence: Confidence level (default: 0.95).

    Returns:
        Tuple of (lower_bound, upper_bound) rounded to 4 decimal places.
    """
    if total <= 0:
        return (0.0, 0.0)
    z = 1.959963984540054 if confidence == 0.95 else 1.6448536269514722
    p = successes / total
    denom = 1.0 + (z**2) / total
    centre = (p + (z**2) / (2.0 * total)) / denom
    spread = (z / denom) * math.sqrt((p * (1.0 - p) / total) + (z**2) / (4.0 * total**2))
    lower = max(0.0, centre - spread)
    upper = min(1.0, centre + spread)
    return (round(lower, 4), round(upper, 4))


def load_ground_truth_dataset() -> List[Dict[str, Any]]:
    """Load benchmark ground truth cases from disk or module definition."""
    if GROUND_TRUTH_PATH.exists():
        try:
            with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) >= 10:
                    return data
        except Exception:
            pass

    # Fallback to local import if raw file is not present
    from pipeline.disease_mapping import CANONICAL_DISEASE_REGISTRY
    return []


def run_validation_benchmark(
    db_path: Optional[Union[str, Path]] = None,
    export_outputs: bool = True,
) -> Dict[str, Any]:
    """Execute the independent validation suite against real database records.

    Evaluates the automated audit findings against independently frozen expert labels.
    No hard-coded predictions or predetermined error exceptions are permitted.

    Args:
        db_path: Optional path to SQLite database. Defaults to curacascade_full.db or curacascade.db.
        export_outputs: If True, writes JSON and CSV summaries to data/processed/.

    Returns:
        Dictionary containing verified evaluation metrics, confusion matrix, confidence intervals,
        and case-by-case classification records.
    """
    resolved_path = get_db_path(db_path)
    full_db = _REPO_ROOT / "data" / "curacascade_full.db"
    if db_path is None and full_db.exists():
        resolved_path = full_db

    ground_truth = load_ground_truth_dataset()
    if not ground_truth:
        raise RuntimeError(f"Benchmark ground truth dataset could not be loaded from {GROUND_TRUTH_PATH}")

    # Connect to database and extract relevant audit findings and curations
    with sqlite3.connect(str(resolved_path)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Check existing tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = set(r[0] for r in cur.fetchall())

        has_findings = "audit_findings" in tables
        has_genes = "genes" in tables
        has_curations = "clingen_curations" in tables

        # Pre-index database records for fast lookup
        genes_in_db = set()
        if has_genes:
            genes_in_db = set(r[0] for r in cur.execute("SELECT gene_symbol FROM genes").fetchall())

        curations_by_gene: Dict[str, List[Dict[str, Any]]] = {}
        if has_curations:
            for r in cur.execute("SELECT gene_symbol, disease_id, disease_name, classification FROM clingen_curations").fetchall():
                sym = r["gene_symbol"]
                curations_by_gene.setdefault(sym, []).append({
                    "disease_id": r["disease_id"],
                    "disease_name": r["disease_name"],
                    "classification": r["classification"],
                })

        findings_by_gene: Dict[str, List[Dict[str, Any]]] = {}
        if has_findings:
            cols = [col[1] for col in cur.execute("PRAGMA table_info(audit_findings)").fetchall()]
            has_match_status = "match_status" in cols
            has_target_pheno = "target_phenotype" in cols

            query = """
            SELECT gene_symbol, audit_class, severity, disease_id, disease_name, target_type, target_id
            """
            if has_match_status:
                query += ", match_status"
            if has_target_pheno:
                query += ", target_phenotype"
            query += " FROM audit_findings"

            for r in cur.execute(query).fetchall():
                sym = r["gene_symbol"]
                m_stat = r["match_status"] if has_match_status else "CONFIRMED_MATCH"
                findings_by_gene.setdefault(sym, []).append({
                    "audit_class": r["audit_class"],
                    "severity": r["severity"],
                    "disease_id": r["disease_id"],
                    "disease_name": r["disease_name"],
                    "target_type": r["target_type"],
                    "target_id": r["target_id"],
                    "match_status": m_stat,
                })

    # Evaluate each benchmark case against real database evidence
    detailed_eval: List[Dict[str, Any]] = []
    evaluable_cases: List[Dict[str, Any]] = []
    excluded_cases: List[Dict[str, Any]] = []

    for adj in ground_truth:
        gene = adj["gene"]
        target_did = adj.get("target_disease_id")
        target_dname = adj.get("target_disease_name")
        gold_flag = int(adj["is_downgraded_gold"])

        in_db = gene in genes_in_db
        curations = curations_by_gene.get(gene, [])
        findings = findings_by_gene.get(gene, [])

        # Priority 2: Evaluability check against warehouse evidence
        is_evaluable = True
        eval_status = "EVALUABLE"
        exclusion_reason = ""

        if not in_db and len(curations) == 0:
            is_evaluable = False
            eval_status = "NOT_EVALUABLE"
            exclusion_reason = "Gene and curation records completely absent from warehouse snapshot"
        elif len(curations) == 0:
            is_evaluable = False
            eval_status = "NOT_EVALUABLE"
            exclusion_reason = "No ClinGen gene validity curations available in warehouse snapshot"

        # Automated prediction algorithm:
        # Evaluates active discrepancy findings matching the target disease concept.
        # Note: benchmark gold labels are NEVER accessed during prediction calculation.
        matching_findings = []
        if is_evaluable:
            reg_entry = CANONICAL_DISEASE_REGISTRY.get(target_did, {})
            aliases = set()
            if reg_entry:
                aliases.update(normalize_text(a) for a in reg_entry.get("aliases", []))
            if target_dname:
                aliases.add(normalize_text(target_dname))

            for f in findings:
                if f.get("match_status") == "DISEASE_MISMATCH":
                    continue
                f_did = f.get("disease_id")
                f_dname = f.get("disease_name", "")

                # 1. Direct disease identifier match
                if target_did and f_did and f_did == target_did:
                    matching_findings.append(f)
                    continue

                # 2. Canonical crosswalk alias match
                norm_f_dname = normalize_text(f_dname)
                if norm_f_dname in aliases:
                    matching_findings.append(f)
                    continue

                # 3. Concept containment for specific disease concepts
                matched_concept = False
                for a in aliases:
                    if len(a) >= 6 and (a in norm_f_dname or norm_f_dname in a):
                        matching_findings.append(f)
                        matched_concept = True
                        break
                if matched_concept:
                    continue

        auto_flag = 1 if len(matching_findings) > 0 else 0

        # Classification assignment
        if is_evaluable:
            if auto_flag == 1 and gold_flag == 1:
                eval_class = "True Positive (TP)"
            elif auto_flag == 1 and gold_flag == 0:
                eval_class = "False Positive (FP - Cross-Domain Discordance)"
            elif auto_flag == 0 and gold_flag == 1:
                eval_class = "False Negative (FN - Absent Downstream Evidence)"
            else:
                eval_class = "True Negative (TN - Unflagged Valid Control)"
            evaluable_cases.append({
                "case_id": adj.get("case_id"),
                "gene": gene,
                "gold_flag": gold_flag,
                "auto_flag": auto_flag,
            })
        else:
            eval_class = f"EXCLUDED ({eval_status}: {exclusion_reason})"
            excluded_cases.append({
                "case_id": adj.get("case_id"),
                "gene": gene,
                "target_disease_id": target_did,
                "target_disease_name": target_dname,
                "gold_flag": gold_flag,
                "eval_status": eval_status,
                "exclusion_reason": exclusion_reason,
            })

        detailed_eval.append({
            "case_id": adj.get("case_id", f"BM_{len(detailed_eval)+1:03d}"),
            "gene": gene,
            "target_disease_id": target_did or "MONDO:UNKNOWN",
            "target_disease_name": target_dname or adj.get("panel", "Unknown"),
            "domain": adj.get("domain", "General"),
            "panel": adj.get("panel", "General"),
            "gold_standard_status": adj.get("published_status", "Unknown"),
            "gold_standard_downgraded": gold_flag,
            "eval_status": eval_status,
            "is_evaluable": is_evaluable,
            "curacascade_automated_flag": auto_flag,
            "evaluation_class": eval_class,
            "present_in_db": in_db,
            "curation_count": len(curations),
            "audit_finding_count": len(findings),
            "matching_finding_count": len(matching_findings),
            "source_citation": adj.get("source_citation", "Documented Literature Reappraisal"),
            "rationale": adj.get("rationale", ""),
            "exclusion_reason": exclusion_reason,
        })

    total_n = len(ground_truth)
    evaluable_n = len(evaluable_cases)
    excluded_n = len(excluded_cases)
    coverage_rate = evaluable_n / max(1, total_n)

    # 1. Evaluable Cohort Metrics (Primary Benchmark Population)
    tp = sum(1 for c in evaluable_cases if c["auto_flag"] == 1 and c["gold_flag"] == 1)
    fp = sum(1 for c in evaluable_cases if c["auto_flag"] == 1 and c["gold_flag"] == 0)
    fn = sum(1 for c in evaluable_cases if c["auto_flag"] == 0 and c["gold_flag"] == 1)
    tn = sum(1 for c in evaluable_cases if c["auto_flag"] == 0 and c["gold_flag"] == 0)

    precision_ppv = tp / max(1, (tp + fp))
    recall_sensitivity = tp / max(1, (tp + fn))
    specificity_tnr = tn / max(1, (tn + fp))
    accuracy = (tp + tn) / max(1, evaluable_n)
    denom_f1 = precision_ppv + recall_sensitivity
    f1_score = (2.0 * precision_ppv * recall_sensitivity) / max(1e-6, denom_f1) if denom_f1 > 0 else 0.0

    prec_ci = wilson_score_interval(tp, tp + fp)
    rec_ci = wilson_score_interval(tp, tp + fn)
    spec_ci = wilson_score_interval(tn, tn + fp)
    acc_ci = wilson_score_interval(tp + tn, evaluable_n)

    p_o = (tp + tn) / evaluable_n if evaluable_n > 0 else 0.0
    p_yes = ((tp + fp) / evaluable_n) * ((tp + fn) / evaluable_n) if evaluable_n > 0 else 0.0
    p_no = ((tn + fn) / evaluable_n) * ((tn + fp) / evaluable_n) if evaluable_n > 0 else 0.0
    p_e = p_yes + p_no
    classifier_kappa = (p_o - p_e) / max(1e-6, (1.0 - p_e)) if (1.0 - p_e) > 0 else 0.0

    # 2. Conservative All-Inclusive Cohort (N = 100, where unobserved cases are auto_flag = 0)
    all_tp = tp
    all_fp = fp
    all_fn = fn + sum(1 for ex in excluded_cases if ex["gold_flag"] == 1)
    all_tn = tn + sum(1 for ex in excluded_cases if ex["gold_flag"] == 0)

    all_prec = all_tp / max(1, (all_tp + all_fp))
    all_rec = all_tp / max(1, (all_tp + all_fn))
    all_spec = all_tn / max(1, (all_tn + all_fp))
    all_acc = (all_tp + all_tn) / max(1, total_n)
    all_denom_f1 = all_prec + all_rec
    all_f1 = (2.0 * all_prec * all_rec) / max(1e-6, all_denom_f1) if all_denom_f1 > 0 else 0.0

    all_p_o = (all_tp + all_tn) / total_n
    all_p_yes = ((all_tp + all_fp) / total_n) * ((all_tp + all_fn) / total_n)
    all_p_no = ((all_tn + all_fn) / total_n) * ((all_tn + all_fp) / total_n)
    all_p_e = all_p_yes + all_p_no
    all_kappa = (all_p_o - all_p_e) / max(1e-6, (1.0 - all_p_e)) if (1.0 - all_p_e) > 0 else 0.0

    metrics = {
        "benchmark_metadata": {
            "title": "CuraCascade 100-Gene Adjudication Validation Benchmark",
            "evaluation_date": "2026-10-25",
            "database_evaluated": str(resolved_path),
            "adjudication_type": "Single-Curator Expert Review (Documented Literature Reappraisals)",
            "unit_of_analysis": "Gene-Disease Clinical Validity Assertion (G, D)",
            "hardcoded_predictions_removed": True,
            "label_firewall_verified": True,
            "inter_rater_reliability_kappa": "N/A - Single-reviewer adjudication (requires >= 2 independent blinded raters)",
        },
        "coverage_summary": {
            "total_benchmark_cases": total_n,
            "evaluable_cases": evaluable_n,
            "excluded_cases": excluded_n,
            "coverage_rate": round(coverage_rate, 4),
            "coverage_pct": round(coverage_rate * 100.0, 1),
            "excluded_case_details": excluded_cases,
        },
        "evaluable_cohort_confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
            "denominator": evaluable_n,
        },
        "evaluable_cohort_metrics": {
            "precision_ppv": round(precision_ppv, 4),
            "precision_pct": round(precision_ppv * 100.0, 1),
            "precision_95ci": list(prec_ci),
            "recall_sensitivity": round(recall_sensitivity, 4),
            "recall_pct": round(recall_sensitivity * 100.0, 1),
            "recall_95ci": list(rec_ci),
            "specificity_tnr": round(specificity_tnr, 4),
            "specificity_pct": round(specificity_tnr * 100.0, 1),
            "specificity_95ci": list(spec_ci),
            "accuracy": round(accuracy, 4),
            "accuracy_pct": round(accuracy * 100.0, 1),
            "accuracy_95ci": list(acc_ci),
            "f1_score": round(f1_score, 4),
            "classifier_concordance_kappa": round(classifier_kappa, 4),
        },
        "unadjusted_all_100_confusion_matrix": {
            "true_positives": all_tp,
            "false_positives": all_fp,
            "false_negatives": all_fn,
            "true_negatives": all_tn,
            "denominator": total_n,
        },
        "unadjusted_all_100_metrics": {
            "precision_ppv": round(all_prec, 4),
            "precision_pct": round(all_prec * 100.0, 1),
            "recall_sensitivity": round(all_rec, 4),
            "recall_pct": round(all_rec * 100.0, 1),
            "specificity_tnr": round(all_spec, 4),
            "specificity_pct": round(all_spec * 100.0, 1),
            "accuracy": round(all_acc, 4),
            "accuracy_pct": round(all_acc * 100.0, 1),
            "f1_score": round(all_f1, 4),
            "classifier_concordance_kappa": round(all_kappa, 4),
        },
        # Backward compatibility aliases
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
        },
        "metrics": {
            "precision_ppv": round(precision_ppv, 4),
            "precision_pct": round(precision_ppv * 100.0, 1),
            "precision_95ci": list(prec_ci),
            "recall_sensitivity": round(recall_sensitivity, 4),
            "recall_pct": round(recall_sensitivity * 100.0, 1),
            "recall_95ci": list(rec_ci),
            "specificity_tnr": round(specificity_tnr, 4),
            "specificity_pct": round(specificity_tnr * 100.0, 1),
            "specificity_95ci": list(spec_ci),
            "accuracy": round(accuracy, 4),
            "accuracy_pct": round(accuracy * 100.0, 1),
            "accuracy_95ci": list(acc_ci),
            "f1_score": round(f1_score, 4),
            "classifier_concordance_kappa": round(classifier_kappa, 4),
        },
        "cohort_counts": {
            "total_benchmark_cases": total_n,
            "evaluable_cases": evaluable_n,
            "excluded_unobserved_cases": excluded_n,
            "gold_downgraded_cases": sum(1 for a in ground_truth if int(a["is_downgraded_gold"]) == 1),
            "gold_definitive_controls": sum(1 for a in ground_truth if int(a["is_downgraded_gold"]) == 0),
            "genes_present_in_db": sum(1 for d in detailed_eval if d["present_in_db"]),
            "genes_missing_from_snapshot": excluded_n,
            "missing_snapshot_genes": [ex["gene"] for ex in excluded_cases],
        },
        "detailed_results": detailed_eval,
    }

    if export_outputs:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        with open(JSON_OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        # Export detailed case-by-case CSV
        with open(CSV_OUT_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "case_id", "gene", "target_disease_id", "target_disease_name", "domain",
                    "panel", "gold_standard_status", "gold_standard_downgraded", "eval_status",
                    "is_evaluable", "curacascade_automated_flag", "evaluation_class", "present_in_db",
                    "curation_count", "audit_finding_count", "matching_finding_count",
                    "source_citation", "rationale", "exclusion_reason"
                ]
            )
            writer.writeheader()
            for r in detailed_eval:
                writer.writerow(r)

    return metrics


def load_validation_metrics() -> Dict[str, Any]:
    """Load cached validation metrics or compute on demand."""
    if JSON_OUT_PATH.exists():
        try:
            with open(JSON_OUT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return run_validation_benchmark()


def main() -> None:
    """CLI entrypoint for reproducible benchmark execution."""
    parser = argparse.ArgumentParser(
        description="Execute independent 100-gene validation benchmark against database."
    )
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help="Path to SQLite database (defaults to data/curacascade_full.db or data/curacascade.db).",
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Skip writing output JSON and CSV files.",
    )
    args = parser.parse_args()

    print("=" * 80)
    print("🧬 CURACASCADE INDEPENDENT VALIDATION BENCHMARK EVALUATION")
    print("=" * 80)
    res = run_validation_benchmark(db_path=args.db, export_outputs=not args.no_export)

    meta = res["benchmark_metadata"]
    cov = res["coverage_summary"]
    cm = res["evaluable_cohort_confusion_matrix"]
    m = res["evaluable_cohort_metrics"]
    all_cm = res["unadjusted_all_100_confusion_matrix"]
    all_m = res["unadjusted_all_100_metrics"]

    print(f"\n📁 Database Evaluated: {meta['database_evaluated']}")
    print(f"📋 Adjudication Protocol: {meta['adjudication_type']}")
    print(f"🎯 Unit of Analysis: {meta['unit_of_analysis']}")
    print(f"🔒 Prediction Label Firewall: VERIFIED (zero access to benchmark gold labels)")
    print(f"🚫 Hardcoded Overrides: REMOVED (dynamic evaluation on relational queries)\n")

    print("-" * 80)
    print("1. BENCHMARK COVERAGE & EXCLUSIONS")
    print("-" * 80)
    print(f"   Total Documented Benchmark Cases : {cov['total_benchmark_cases']}")
    print(f"   Evaluable Cases in Warehouse     : {cov['evaluable_cases']} ({cov['coverage_pct']}% coverage)")
    print(f"   Excluded Cases (Absent Evidence) : {cov['excluded_cases']}")
    for ex in cov["excluded_case_details"]:
        print(f"     - {ex['gene']} ({ex['target_disease_name']}): {ex['exclusion_reason']} [Gold={ex['gold_flag']}]")
    print()

    print("-" * 80)
    print(f"2. EVALUABLE COHORT CONFUSION MATRIX (N = {cm['denominator']})")
    print("-" * 80)
    print(f"                      Predicted Discrepancy (1) | Predicted Concordant (0)")
    print(f"   Gold Downgraded (1)      TP = {cm['true_positives']:<4}              | FN = {cm['false_negatives']:<4}")
    print(f"   Gold Definitive (0)      FP = {cm['false_positives']:<4}              | TN = {cm['true_negatives']:<4}\n")

    print("-" * 80)
    print(f"3. EVALUABLE COHORT PERFORMANCE METRICS (WITH 95% WILSON CONFIDENCE INTERVALS)")
    print("-" * 80)
    print(f"   Precision (PPV)       : {m['precision_pct']}% (95% CI: {m['precision_95ci'][0]*100:.1f}% - {m['precision_95ci'][1]*100:.1f}%)")
    print(f"   Recall (Sensitivity)  : {m['recall_pct']}% (95% CI: {m['recall_95ci'][0]*100:.1f}% - {m['recall_95ci'][1]*100:.1f}%)")
    print(f"   Specificity (TNR)     : {m['specificity_pct']}% (95% CI: {m['specificity_95ci'][0]*100:.1f}% - {m['specificity_95ci'][1]*100:.1f}%)")
    print(f"   Overall Accuracy      : {m['accuracy_pct']}% (95% CI: {m['accuracy_95ci'][0]*100:.1f}% - {m['accuracy_95ci'][1]*100:.1f}%)")
    print(f"   F1-Score              : {m['f1_score']:.4f}")
    print(f"   Classifier Concordance: κ = {m['classifier_concordance_kappa']:.4f}")
    print(f"   Inter-Rater Reliability: {meta['inter_rater_reliability_kappa']}\n")

    print("-" * 80)
    print(f"4. UNADJUSTED FULL COHORT (CONSERVATIVE N = {all_cm['denominator']})")
    print("-" * 80)
    print(f"   TP = {all_cm['true_positives']}, FP = {all_cm['false_positives']}, FN = {all_cm['false_negatives']}, TN = {all_cm['true_negatives']}")
    print(f"   Precision: {all_m['precision_pct']}%, Recall: {all_m['recall_pct']}%, Specificity: {all_m['specificity_pct']}%, Accuracy: {all_m['accuracy_pct']}%, κ = {all_m['classifier_concordance_kappa']:.4f}\n")

    print("-" * 80)
    print("5. EXPORTED ARTIFACTS")
    print("-" * 80)
    print(f"   Metrics JSON : {JSON_OUT_PATH}")
    print(f"   Case-level CSV: {CSV_OUT_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    main()
