"""CuraCascade — Cross-Database Inconsistency Audit Engine.

Executes relational SQL joins and classification logic across ClinGen, ClinVar,
and Genomics England PanelApp to identify downstream evidence cascades:
- Class A: Pathogenic/Likely Pathogenic ClinVar assertions in Disputed or Refuted genes.
- Class B: Pathogenic/Likely Pathogenic ClinVar assertions in Limited-evidence genes.
- Class C: Green (diagnostic-grade) PanelApp gene entries in Disputed or Refuted genes.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure repository root is on sys.path
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pandas as pd

import config as C
from database.connection import (
    ensure_database_ready,
    execute_many,
    execute_write,
    query_df,
)
from pipeline.disease_mapping import (
    match_panel_to_curation_disease,
    match_variant_to_curation_disease,
)


def run_audit(
    db_path: Optional[Union[str, Path]] = None,
    export_csv: bool = True,
) -> Dict[str, Any]:
    """Execute the full disease-aware cross-layer inconsistency audit.

    Enforces biological entity distinction:
    - Gene, disease concept, gene-disease validity assertion, variant, panel.
    - Prevents variants in multi-disease genes from being flagged for unrelated downgrades.
    - Assigns match_status, confidence, and provenance to every finding.

    Args:
        db_path: Target SQLite database file path.
        export_csv: If True, writes results to data/processed/audit_findings.csv.

    Returns:
        Dictionary containing summary metrics and audit DataFrames.
    """
    ensure_database_ready(db_path=db_path)

    # Clean out previous audit results to ensure idempotency
    execute_write("DELETE FROM audit_findings;", db_path=db_path)

    # 1. Retrieve all downgraded ClinGen curations (Disputed, Refuted, Limited)
    curations_sql = """
    SELECT 
        cc.curation_id,
        cc.gene_symbol,
        cc.disease_id,
        d.disease_name,
        cc.classification AS clingen_classification,
        cc.classification_date AS clingen_date,
        cc.gcep AS clingen_gcep,
        cc.report_url AS clingen_report_url
    FROM clingen_curations cc
    JOIN genes g ON cc.gene_symbol = g.gene_symbol
    JOIN diseases d ON cc.disease_id = d.disease_id
    WHERE cc.classification IN ('Disputed', 'Refuted', 'Limited')
    ORDER BY 
        CASE cc.classification 
            WHEN 'Refuted' THEN 1 
            WHEN 'Disputed' THEN 2 
            WHEN 'Limited' THEN 3 
            ELSE 4 
        END,
        g.gene_symbol ASC;
    """
    downgraded_curations = query_df(curations_sql, db_path=db_path)

    # 2. Retrieve ClinVar P/LP variants for target genes
    clinvar_sql = """
    SELECT 
        cv.variation_id,
        cv.gene_symbol,
        cv.disease_id,
        cv.variant_name,
        cv.clinical_significance,
        cv.stars,
        cv.review_status,
        cv.num_submitters,
        cv.submitter_names,
        cv.last_evaluated,
        cv.phenotype_list,
        COALESCE(cv.gnomad_af_global, 0.0) AS gnomad_af,
        COALESCE(cv.mcaf_threshold, 0.0001) AS mcaf_threshold,
        COALESCE(cv.population_refuted_flag, 0) AS population_refuted_flag
    FROM clinvar_variants cv
    WHERE cv.is_plp = 1;
    """
    clinvar_df = query_df(clinvar_sql, db_path=db_path)

    # 3. Retrieve PanelApp green panels
    panelapp_sql = """
    SELECT 
        pa.entry_id,
        pa.gene_symbol,
        pa.disease_id,
        pa.panel_id,
        pa.panel_name,
        pa.panel_version,
        pa.confidence,
        pa.mode_of_inheritance,
        pa.phenotypes
    FROM panelapp_entries pa
    WHERE LOWER(pa.confidence) = 'green';
    """
    panelapp_df = query_df(panelapp_sql, db_path=db_path)

    findings_to_insert: List[Tuple[Any, ...]] = []
    seen_findings: Set[Tuple[str, int, str, str]] = set()
    today = datetime.now().date()

    # Pre-index variants and panels by gene_symbol
    variants_by_gene: Dict[str, List[Dict[str, Any]]] = {}
    if not clinvar_df.empty:
        for _, v in clinvar_df.iterrows():
            sym = str(v["gene_symbol"]).strip().upper()
            variants_by_gene.setdefault(sym, []).append(v.to_dict())

    panels_by_gene: Dict[str, List[Dict[str, Any]]] = {}
    if not panelapp_df.empty:
        for _, p in panelapp_df.iterrows():
            sym = str(p["gene_symbol"]).strip().upper()
            panels_by_gene.setdefault(sym, []).append(p.to_dict())

    # Evaluate each curation
    for _, crow in downgraded_curations.iterrows():
        sym = str(crow["gene_symbol"]).strip().upper()
        cur_id = int(crow["curation_id"])
        cg_did = str(crow["disease_id"]).strip()
        cg_dname = str(crow["disease_name"]).strip()
        classification = str(crow["clingen_classification"]).strip()
        clingen_date_str = str(crow["clingen_date"]) if pd.notna(crow["clingen_date"]) else ""

        days_unresolved = 0
        if clingen_date_str:
            try:
                c_date = datetime.strptime(clingen_date_str.split()[0], "%Y-%m-%d").date()
                days_unresolved = max(0, (today - c_date).days)
            except ValueError:
                pass

        # Evaluate ClinVar Variants for this curation
        for v in variants_by_gene.get(sym, []):
            match_res = match_variant_to_curation_disease(
                gene_symbol=sym,
                variant_disease_id=v.get("disease_id"),
                variant_phenotypes=v.get("phenotype_list"),
                clingen_disease_id=cg_did,
                clingen_disease_name=cg_dname,
            )

            # Skip if variant condition does not match downgraded disease
            if not match_res.is_match:
                continue

            var_id_str = str(v["variation_id"])
            finding_key = (sym, cur_id, "ClinVar Variant", var_id_str)
            if finding_key in seen_findings:
                continue
            seen_findings.add(finding_key)

            stars = int(v["stars"]) if pd.notna(v.get("stars")) else 0
            star_str = f"{stars} star{'s' if stars != 1 else ''}"
            target_status = f"{v['clinical_significance']} ({star_str})"

            sub_names = v.get("submitter_names")
            n_sub = v.get("num_submitters", 1)
            submitter_info = (
                f"{sub_names} ({n_sub} submitter{'s' if n_sub != 1 else ''})"
                if pd.notna(sub_names) and sub_names
                else f"{n_sub} submitter(s)"
            )

            if classification in ("Disputed", "Refuted"):
                audit_class = C.AUDIT_CLASS_A
                severity = "CRITICAL" if match_res.match_status == "CONFIRMED_MATCH" else "HIGH"
                evidence_summary = (
                    f"ClinGen GCEP ({crow['clingen_gcep'] or 'Consortium'}) classified gene-disease causality as "
                    f"'{classification}' on {clingen_date_str}. Downstream ClinVar asserts this variant as "
                    f"{v['clinical_significance']} ({star_str}). Match: {match_res.rationale}"
                )
            else:  # Limited
                audit_class = C.AUDIT_CLASS_B
                severity = "HIGH" if match_res.match_status == "CONFIRMED_MATCH" else "MEDIUM"
                evidence_summary = (
                    f"ClinGen GCEP ({crow['clingen_gcep'] or 'Consortium'}) appraised evidence as 'Limited'. "
                    f"Variants in limited-evidence genes should not exceed VUS, yet ClinVar asserts "
                    f"{v['clinical_significance']}. Match: {match_res.rationale}"
                )

            findings_to_insert.append((
                audit_class,
                severity,
                sym,
                cg_did,
                cg_dname,
                classification,
                clingen_date_str,
                crow["clingen_gcep"],
                crow["clingen_report_url"],
                "ClinVar Variant",
                var_id_str,
                str(v["variant_name"]),
                target_status,
                evidence_summary,
                submitter_info,
                str(v["last_evaluated"]) if pd.notna(v.get("last_evaluated")) else "",
                days_unresolved,
                float(v.get("gnomad_af", 0.0)),
                float(v.get("mcaf_threshold", 0.0001)),
                int(v.get("population_refuted_flag", 0)),
                cur_id,
                match_res.match_status,
                match_res.rationale,
                match_res.rule_id,
                match_res.target_phenotype,
                match_res.confidence,
            ))

        # Evaluate PanelApp entries for this curation (Class C applies to Disputed/Refuted)
        if classification in ("Disputed", "Refuted"):
            for p in panels_by_gene.get(sym, []):
                match_res = match_panel_to_curation_disease(
                    gene_symbol=sym,
                    panel_id=int(p["panel_id"]),
                    panel_name=str(p["panel_name"]),
                    panel_phenotypes=p.get("phenotypes"),
                    clingen_disease_id=cg_did,
                    clingen_disease_name=cg_dname,
                )

                if not match_res.is_match:
                    continue

                panel_id_str = str(p["panel_id"])
                finding_key = (sym, cur_id, "PanelApp Panel", panel_id_str)
                if finding_key in seen_findings:
                    continue
                seen_findings.add(finding_key)

                target_status = f"Green (Diagnostic-Grade, v{p.get('panel_version') or '1.0'})"
                panel_info = f"PanelApp ID {p['panel_id']} ({p.get('mode_of_inheritance') or 'Unknown MOI'})"
                evidence_summary = (
                    f"Genomics England PanelApp lists this gene as diagnostic-grade 'Green' in '{p['panel_name']}', "
                    f"conflicting with ClinGen's '{classification}' determination for '{cg_dname}' on {clingen_date_str}. "
                    f"Match: {match_res.rationale}"
                )

                findings_to_insert.append((
                    C.AUDIT_CLASS_C,
                    "CRITICAL" if match_res.match_status == "CONFIRMED_MATCH" else "HIGH",
                    sym,
                    cg_did,
                    cg_dname,
                    classification,
                    clingen_date_str,
                    crow["clingen_gcep"],
                    crow["clingen_report_url"],
                    "PanelApp Panel",
                    panel_id_str,
                    str(p["panel_name"]),
                    target_status,
                    evidence_summary,
                    panel_info,
                    "",
                    days_unresolved,
                    0.0,
                    0.0001,
                    0,
                    cur_id,
                    match_res.match_status,
                    match_res.rationale,
                    match_res.rule_id,
                    match_res.target_phenotype,
                    match_res.confidence,
                ))

    # 4. Insert findings into audit_findings table
    insert_sql = """
    INSERT INTO audit_findings (
        audit_class, severity, gene_symbol, disease_id, disease_name,
        clingen_classification, clingen_date, clingen_gcep, clingen_report_url,
        target_type, target_id, target_name, target_status, evidence_summary,
        submitters_or_panel_info, last_evaluated_date, days_unresolved,
        gnomad_af, mcaf_threshold, population_refuted_flag,
        curation_id, match_status, match_rationale, rule_id,
        target_phenotype, disease_match_confidence
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    if findings_to_insert:
        execute_many(insert_sql, findings_to_insert, db_path=db_path)

    # 5. Log execution in provenance table
    class_a_n = sum(1 for f in findings_to_insert if f[0] == C.AUDIT_CLASS_A)
    class_b_n = sum(1 for f in findings_to_insert if f[0] == C.AUDIT_CLASS_B)
    class_c_n = sum(1 for f in findings_to_insert if f[0] == C.AUDIT_CLASS_C)
    prov_sql = """
    INSERT INTO provenance (source_name, source_url, snapshot_date, record_count, transformation_version, details)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        execute_write(
            prov_sql,
            (
                "CuraCascade Disease-Aware Audit Engine",
                "internal",
                datetime.now().strftime("%Y-%m-%d"),
                len(findings_to_insert),
                "2.0.0-disease-aware",
                f"Materialized {len(findings_to_insert)} findings ({class_a_n} Class A, {class_b_n} Class B, {class_c_n} Class C).",
            ),
            db_path=db_path,
        )
    except Exception:
        pass

    # 6. Compute Summary Metrics
    metrics = get_audit_metrics(db_path=db_path)
    findings_df = get_all_findings(db_path=db_path)

    if export_csv and not findings_df.empty:
        csv_path = C.PROCESSED_DATA_DIR / "audit_findings.csv"
        findings_df.to_csv(csv_path, index=False)

    return {
        "metrics": metrics,
        "findings_df": findings_df,
    }


def get_audit_metrics(db_path: Optional[Union[str, Path]] = None) -> Dict[str, int]:
    """Retrieve key numerical indicators of corpus integrity and audit findings.

    Args:
        db_path: Target database path.

    Returns:
        Dictionary of aggregated metrics.
    """
    counts_sql = """
    SELECT
        (SELECT COUNT(*) FROM genes) AS total_genes,
        (SELECT COUNT(*) FROM genes WHERE is_downgraded = 1) AS downgraded_genes,
        (SELECT COUNT(*) FROM clingen_curations) AS total_curations,
        (SELECT COUNT(*) FROM clinvar_variants) AS total_variants,
        (SELECT COUNT(*) FROM clinvar_variants WHERE is_plp = 1) AS total_plp_variants,
        (SELECT COUNT(*) FROM panelapp_entries) AS total_panel_entries,
        (SELECT COUNT(*) FROM audit_findings WHERE audit_class = 'Class A') AS class_a_count,
        (SELECT COUNT(*) FROM audit_findings WHERE audit_class = 'Class B') AS class_b_count,
        (SELECT COUNT(*) FROM audit_findings WHERE audit_class = 'Class C') AS class_c_count,
        (SELECT COUNT(DISTINCT gene_symbol) FROM audit_findings WHERE audit_class = 'Class A') AS class_a_genes,
        (SELECT COUNT(DISTINCT gene_symbol) FROM audit_findings WHERE audit_class = 'Class B') AS class_b_genes,
        (SELECT COUNT(DISTINCT gene_symbol) FROM audit_findings WHERE audit_class = 'Class C') AS class_c_genes,
        (SELECT COUNT(*) FROM audit_findings) AS total_findings
    """
    df = query_df(counts_sql, db_path=db_path)
    if df.empty:
        return {}
    return {k: int(v) for k, v in df.iloc[0].to_dict().items()}


def _build_audit_where_clause(
    audit_class: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    target_types: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    prescriptive_action: Optional[str] = None,
) -> Tuple[str, List[Any]]:
    """Construct SQL WHERE clause and parameters for audit findings filtering."""
    conditions = []
    params: List[Any] = []

    if audit_class and audit_class != "All":
        conditions.append("audit_class = ?")
        params.append(audit_class)

    if gene_symbol and gene_symbol.strip():
        conditions.append("UPPER(gene_symbol) LIKE ?")
        params.append(f"%{gene_symbol.strip().upper()}%")

    if target_types:
        if isinstance(target_types, str) and target_types not in ("All", "All Layers"):
            conditions.append("target_type = ?")
            params.append(target_types)
        elif isinstance(target_types, (list, tuple)) and target_types:
            filtered_targets = [t for t in target_types if t not in ("All", "All Layers")]
            if filtered_targets:
                placeholders = ",".join("?" for _ in filtered_targets)
                conditions.append(f"target_type IN ({placeholders})")
                params.extend(filtered_targets)

    if prescriptive_action and prescriptive_action not in ("All", "All Actions"):
        act_str = str(prescriptive_action)
        if "Benign" in act_str or "BA1" in act_str:
            conditions.append("population_refuted_flag = 1")
        elif "Demote Panel" in act_str:
            conditions.append("(COALESCE(population_refuted_flag, 0) = 0) AND (target_type LIKE '%Panel%' OR audit_class = 'Class C') AND (clingen_classification IN ('Refuted', 'Disputed') OR audit_class = 'Class C')")
        elif "Amber Tier" in act_str:
            conditions.append("(COALESCE(population_refuted_flag, 0) = 0) AND (target_type LIKE '%Panel%' OR audit_class = 'Class C') AND (clingen_classification = 'Limited' OR audit_class = 'Class B')")
        elif "Retract P/LP" in act_str or "Reclassify to VUS" in act_str:
            conditions.append("(COALESCE(population_refuted_flag, 0) = 0) AND NOT (target_type LIKE '%Panel%' OR audit_class = 'Class C') AND (clingen_classification IN ('Refuted', 'Disputed') OR audit_class = 'Class A')")
        elif "Cap at VUS" in act_str:
            conditions.append("(COALESCE(population_refuted_flag, 0) = 0) AND NOT (target_type LIKE '%Panel%' OR audit_class = 'Class C') AND (clingen_classification = 'Limited' OR audit_class = 'Class B')")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    return where_clause, params


def _build_audit_order_clause(sort_by: Optional[str] = None) -> str:
    """Build SQL ORDER BY clause based on sort directive."""
    if not sort_by:
        return """
        ORDER BY 
            CASE audit_class 
                WHEN 'Class A' THEN 1 
                WHEN 'Class B' THEN 2 
                WHEN 'Class C' THEN 3 
                ELSE 4 
            END,
            days_unresolved DESC,
            gene_symbol ASC
        """
    s = str(sort_by).lower()
    if "longest" in s or ("latency" in s and "desc" in s) or "days ↓" in s:
        return "ORDER BY days_unresolved DESC, CASE audit_class WHEN 'Class A' THEN 1 WHEN 'Class B' THEN 2 WHEN 'Class C' THEN 3 ELSE 4 END, gene_symbol ASC"
    elif "shortest" in s or ("latency" in s and "asc" in s) or "days ↑" in s:
        return "ORDER BY days_unresolved ASC, CASE audit_class WHEN 'Class A' THEN 1 WHEN 'Class B' THEN 2 WHEN 'Class C' THEN 3 ELSE 4 END, gene_symbol ASC"
    elif "priority" in s or "class a" in s:
        return "ORDER BY CASE audit_class WHEN 'Class A' THEN 1 WHEN 'Class B' THEN 2 WHEN 'Class C' THEN 3 ELSE 4 END, days_unresolved DESC, gene_symbol ASC"
    elif "gene symbol (a" in s or ("gene" in s and "a → z" in s):
        return "ORDER BY gene_symbol ASC, days_unresolved DESC"
    elif "gene symbol (z" in s or ("gene" in s and "z → a" in s):
        return "ORDER BY gene_symbol DESC, days_unresolved DESC"
    elif "date" in s and ("newest" in s or "desc" in s):
        return "ORDER BY clingen_date DESC, days_unresolved DESC"
    elif "date" in s and ("oldest" in s or "asc" in s):
        return "ORDER BY clingen_date ASC, days_unresolved DESC"
    else:
        return """
        ORDER BY 
            CASE audit_class 
                WHEN 'Class A' THEN 1 
                WHEN 'Class B' THEN 2 
                WHEN 'Class C' THEN 3 
                ELSE 4 
            END,
            days_unresolved DESC,
            gene_symbol ASC
        """


def get_findings_count(
    db_path: Optional[Union[str, Path]] = None,
    audit_class: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    target_types: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    prescriptive_action: Optional[str] = None,
) -> int:
    """Retrieve total count of matching audit findings for pagination."""
    where_clause, params = _build_audit_where_clause(
        audit_class=audit_class,
        gene_symbol=gene_symbol,
        target_types=target_types,
        prescriptive_action=prescriptive_action,
    )
    sql = f"SELECT COUNT(*) FROM audit_findings {where_clause};"
    df = query_df(sql, params=params if params else None, db_path=db_path)
    if not df.empty:
        return int(df.iloc[0, 0])
    return 0


def get_all_findings(
    db_path: Optional[Union[str, Path]] = None,
    audit_class: Optional[str] = None,
    gene_symbol: Optional[str] = None,
    target_types: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
    prescriptive_action: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> pd.DataFrame:
    """Retrieve audit findings with optional filtering, sorting, and server-side pagination.

    Args:
        db_path: Target database path.
        audit_class: Optional class filter ('Class A', 'Class B', 'Class C').
        gene_symbol: Optional gene symbol filter (case-insensitive substring match).
        target_types: Optional database layer filter ('ClinVar Variant', 'PanelApp Panel', or collection).
        prescriptive_action: Optional prescriptive action filter.
        sort_by: Optional sort order directive.
        limit: Optional maximum number of rows to retrieve (page size).
        offset: Optional row offset for server-side pagination.

    Returns:
        Pandas DataFrame of matching audit records.
    """
    where_clause, params = _build_audit_where_clause(
        audit_class=audit_class,
        gene_symbol=gene_symbol,
        target_types=target_types,
        prescriptive_action=prescriptive_action,
    )
    order_clause = _build_audit_order_clause(sort_by=sort_by)

    pagination_clause = ""
    if limit is not None and int(limit) > 0:
        pagination_clause = f"LIMIT {int(limit)}"
        if offset is not None and int(offset) > 0:
            pagination_clause += f" OFFSET {int(offset)}"

    sql = f"""
    SELECT 
        finding_id,
        audit_class,
        severity,
        gene_symbol,
        disease_id,
        disease_name,
        clingen_classification,
        clingen_date,
        clingen_gcep,
        target_type,
        target_id,
        target_name,
        target_status,
        submitters_or_panel_info,
        last_evaluated_date,
        days_unresolved,
        evidence_summary,
        clingen_report_url,
        gnomad_af,
        mcaf_threshold,
        population_refuted_flag,
        curation_id,
        match_status,
        match_rationale,
        rule_id,
        target_phenotype,
        disease_match_confidence
    FROM audit_findings
    {where_clause}
    {order_clause}
    {pagination_clause};
    """
    return query_df(sql, params=params if params else None, db_path=db_path)


def get_gene_history(
    gene_symbol: str,
    db_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Retrieve full cross-database timeline and linked records for a specific gene.

    Args:
        gene_symbol: Gene symbol (e.g. 'MYLK2', 'MYH7').
        db_path: Target database path.

    Returns:
        Dictionary containing gene metadata, curations, variants, panel memberships, and findings.
    """
    symbol = gene_symbol.strip().upper()

    gene_df = query_df(
        "SELECT * FROM genes WHERE UPPER(gene_symbol) = ?",
        params=(symbol,),
        db_path=db_path,
    )
    if gene_df.empty:
        return {}

    curations_df = query_df(
        """
        SELECT cc.*, d.disease_name 
        FROM clingen_curations cc
        JOIN diseases d ON cc.disease_id = d.disease_id
        WHERE UPPER(cc.gene_symbol) = ?
        ORDER BY cc.classification_date DESC
        """,
        params=(symbol,),
        db_path=db_path,
    )

    variants_df = query_df(
        """
        SELECT cv.*, d.disease_name 
        FROM clinvar_variants cv
        LEFT JOIN diseases d ON cv.disease_id = d.disease_id
        WHERE UPPER(cv.gene_symbol) = ?
        ORDER BY cv.is_plp DESC, cv.stars DESC, cv.last_evaluated DESC
        """,
        params=(symbol,),
        db_path=db_path,
    )

    panels_df = query_df(
        """
        SELECT * FROM panelapp_entries 
        WHERE UPPER(gene_symbol) = ?
        ORDER BY 
            CASE LOWER(confidence) 
                WHEN 'green' THEN 1 
                WHEN 'amber' THEN 2 
                ELSE 3 
            END,
            panel_name ASC
        """,
        params=(symbol,),
        db_path=db_path,
    )

    findings_df = query_df(
        """
        SELECT * FROM audit_findings 
        WHERE UPPER(gene_symbol) = ?
        ORDER BY audit_class ASC
        """,
        params=(symbol,),
        db_path=db_path,
    )

    return {
        "gene": gene_df.iloc[0].to_dict(),
        "curations": curations_df,
        "variants": variants_df,
        "panels": panels_df,
        "findings": findings_df,
    }


def main():
    """CLI Entry point for running the audit pipeline."""
    parser = argparse.ArgumentParser(description="Run the CuraCascade cross-database audit.")
    parser.add_argument("--db", type=str, default=str(C.DB_PATH), help="Path to SQLite database.")
    args = parser.parse_args()

    print(f"Running CuraCascade Audit against: {args.db}")
    results = run_audit(db_path=args.db)
    metrics = results["metrics"]

    print("\n" + "=" * 60)
    print("  CURACASCADE AUDIT SUMMARY REPORT")
    print("=" * 60)
    print(f"  Total Genes Curated:           {metrics.get('total_genes', 0):>6,}")
    print(f"  Downgraded Genes (Exposure):   {metrics.get('downgraded_genes', 0):>6,}")
    print(f"  Total ClinVar Variants:        {metrics.get('total_variants', 0):>6,}")
    print(f"  Pathogenic/Likely Pathogenic:  {metrics.get('total_plp_variants', 0):>6,}")
    print(f"  Genomics England Panel Genes:  {metrics.get('total_panel_entries', 0):>6,}")
    print("-" * 60)
    print(f"  [CRITICAL] Class A Inconsistencies: {metrics.get('class_a_count', 0):>6,} ({metrics.get('class_a_genes', 0)} genes)")
    print(f"             (P/LP in Disputed/Refuted)")
    print(f"  [HIGH]     Class B Inconsistencies: {metrics.get('class_b_count', 0):>6,} ({metrics.get('class_b_genes', 0)} genes)")
    print(f"             (P/LP in Limited-Evidence)")
    print(f"  [CRITICAL] Class C Inconsistencies: {metrics.get('class_c_count', 0):>6,} ({metrics.get('class_c_genes', 0)} genes)")
    print(f"             (Diagnostic Green in Disputed/Refuted)")
    print("=" * 60)
    print(f"  Total Audit Findings Flagged:       {metrics.get('total_findings', 0):>6,}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
