# CuraCascade: Scientific Claims & Quantitative Verification Audit

**Document:** Comprehensive Evidence Audit & Source Verification Matrix  
**Target Manuscript:** IEEE Project Report & Presentation Deck  
**Lead Author:** Udit Shokeen (Reg. No: 23BCB0001)  
**Destination File:** [`CuraCascade_Claims_Verification.md`](file:///h:/Projects/curacascade/CuraCascade_Claims_Verification.md)  

---

## 1. Executive Verification Standard

Every quantitative metric, statistical denominator, and clinical claim in the redesigned presentation has been audited against active repository artifacts, frozen benchmark JSON files, and reproducible execution logs.

No synthetic, uncalibrated, or hardcoded predictions are presented as empirical fact. All performance metrics reflect the revised evaluation rules implemented in [`pipeline/validation_benchmark.py`](file:///h:/Projects/curacascade/pipeline/validation_benchmark.py) and verified in [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json).

---

## 2. Quantitative Claims Verification Matrix

| Claim / Metric | Value in Deck | Verified Source Artifact | Calculation / Verification Rule | Audit Verdict |
| :--- | :---: | :--- | :--- | :---: |
| **Total Benchmark Cohort** | **100 Genes** | [`data/raw/benchmark_ground_truth.json`](file:///h:/Projects/curacascade/data/raw/benchmark_ground_truth.json) | 54 published downgraded genes + 46 definitive ACMG controls. | **VERIFIED** |
| **Evaluable Benchmark Cohort** | **94 Cases** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L14) | Evaluated cases with both gene and curation records in warehouse snapshot. | **VERIFIED** |
| **Excluded Benchmark Cases** | **6 Cases** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L15) | Designated `NOT_EVALUABLE`: *XRCC3*, *DFNB59*, *TSC1*, *TSC2*, *SMAD3*, *SMN1*. | **VERIFIED** |
| **True Positives (TP)** | **18** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L76) | Verified downstream discrepancies correctly detected by automated join. | **VERIFIED** |
| **False Positives (FP)** | **0** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L77) | Zero definitive clinical controls flagged as invalid. | **VERIFIED** |
| **False Negatives (FN)** | **34** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L78) | Undetected benchmark positives (15 absent data, 3 missing curation, 16 cross-disease). | **VERIFIED** |
| **True Negatives (TN)** | **42** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L79) | Non-downgraded controls correctly confirmed concordant. | **VERIFIED** |
| **Join Precision (PPV)** | **100.0%** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L84) | $TP / (TP + FP) = 18 / (18 + 0) = 1.000$ (Wilson 95% CI: [0.8241, 1.0000]). | **VERIFIED** |
| **Gold-Standard Recall** | **34.6%** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L90) | $TP / (TP + FN) = 18 / (18 + 34) = 0.3462$ (Wilson 95% CI: [0.2315, 0.4820]). | **VERIFIED** |
| **Classifier Specificity** | **100.0%** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L96) | $TN / (TN + FP) = 42 / (42 + 0) = 1.000$ (Wilson 95% CI: [0.9162, 1.0000]). | **VERIFIED** |
| **Overall Accuracy** | **63.8%** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L102) | $(TP + TN) / N_{\text{eval}} = (18 + 42) / 94 = 0.6383$ (Wilson 95% CI: [0.5375, 0.7282]). | **VERIFIED** |
| **Classifier Concordance Kappa** | **0.3212** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L108) | Cohen's kappa evaluated against frozen gold-standard ground truth. | **VERIFIED** |
| **Unadjusted Sensitivity ($N=100$)**| **33.3%** | [`data/processed/validation_metrics.json`](file:///h:/Projects/curacascade/data/processed/validation_metrics.json#L121) | Sensitivity analysis including 6 unobserved cases as FN ($18 / 54 = 33.33\%$). | **VERIFIED** |
| **Empirical Latency Cohort** | **51,007 Vars** | [`data/processed/empirical_latency_summary.json`](file:///h:/Projects/curacascade/data/processed/empirical_latency_summary.json#L9) | Cross-sectional ClinVar P/LP assertions evaluated across 536 unique genes. | **VERIFIED** |
| **Median Evidence Latency** | **2.82 Years** | [`data/processed/empirical_latency_summary.json`](file:///h:/Projects/curacascade/data/processed/empirical_latency_summary.json#L15) | 1,030.0 days elapsed from ClinGen appraisal date to snapshot date (IQR: 684–1,771 d). | **VERIFIED** |
| **Commercial vs Academic Latency** | **2.80 vs 2.84 Yrs** | [`data/processed/empirical_latency_summary.json`](file:///h:/Projects/curacascade/data/processed/empirical_latency_summary.json#L42-L46) | Mann-Whitney U test statistic = $300,922,517.5, p = 0.00025$ ($p < 0.001$). | **VERIFIED** |
| **Class A vs Class B Latency** | **2.80 vs 3.77 Yrs** | [`data/processed/empirical_latency_summary.json`](file:///h:/Projects/curacascade/data/processed/empirical_latency_summary.json#L55-L58) | Refuted/Disputed median 1,021 d vs Limited evidence median 1,377 d ($p < 0.001$). | **VERIFIED** |
| **Exploratory ML AUROC** | **0.857** | [`pipeline/forecasting.py`](file:///h:/Projects/curacascade/pipeline/forecasting.py#L364) | Test set AUROC for Balanced Random Forest predicting downgrade risk. | **VERIFIED (Exploratory)** |
| **Exploratory ML Brier Score** | **0.1508** | [`pipeline/forecasting.py`](file:///h:/Projects/curacascade/pipeline/forecasting.py#L368) | Mean squared probability error evaluated on held-out test split. | **VERIFIED (Exploratory)** |
| **Automated Pytest Suite** | **47 Passed** | Pytest execution log (`pytest`) | 47 passing tests across 5 test modules in 48.9s (100% pass rate). | **VERIFIED** |

---

## 3. Scientific Categorization & Governance Boundaries

To ensure complete transparency during the viva examination, the presentation explicitly stratifies system claims into four formal categories:

### A. Fully Implemented & Empirically Verified
- 3NF Normalized relational schema in SQLite (`curacascade.db` and `curacascade_full.db`) with cascading foreign keys and compound indexes.
- 3-tier deterministic disease-aware concept crosswalk with MONDO, OMIM, and MedGen aliases.
- Automated discrepancy materialization into Class A, Class B, and Class C inconsistency findings.
- 47/47 passing automated tests covering biological matching, database integrity, and statistical metrics.
- High-throughput Streamlit clinical decision support portal (`curacascadev2.streamlit.app`).

### B. Exploratory & Retrospective Analyses
- Supervised Machine Learning downgrade forecasting (Random Forest, AUROC = 0.857): Disclosed as an exploratory triage tool evaluated on static cross-sectional snapshots; not claimed as prospectively validated clinical prediction.
- Evidence Latency Analysis (Median 2.82 years): Disclosed as cross-sectional elapsed duration in a static warehouse snapshot, not longitudinal follow-up of time-to-resolution.

### C. Technical Limitations
- Benchmark Recall (34.6%): Moderate sensitivity resulting from conservative disease matching rules and absent assertions in static database releases.
- Single-Reviewer Ground Truth: Gold-standard labels compiled from documented literature reappraisals rather than multi-center blinded independent human curators.

### D. Proposed Future Work
- Prospective longitudinal event tracking with automated monthly change delta capture.
- SMART-on-FHIR clinical exome pipeline integration for real-time electronic health record alerts.
- Consortium expansion of the 100-gene adjudication benchmark.
