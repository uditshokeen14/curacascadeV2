# CuraCascade: Downstream Clinical Evidence Downgrade Auditor

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Database](https://img.shields.io/badge/Database-SQLite3%20%7C%20DuckDB-green.svg)](https://sqlite.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Dashboard](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-46%20Passed-brightgreen.svg)]()

---

## 1. Biological Motivation & Problem Statement

In modern clinical genomics, accurate molecular diagnoses rely on the scientific validity of reported gene–disease relationships. When **ClinGen** (*Clinical Genome Resource*) Gene Curation Expert Panels (GCEPs) reappraise and downgrade a gene from *Definitive* or *Moderate* clinical validity to **Disputed**, **Refuted**, or **Limited**, downstream clinical repositories do not automatically synchronize:
- **NCBI ClinVar** variant archives frequently retain active **Pathogenic (P)** or **Likely Pathogenic (LP)** classifications in discredited genes.
- **Genomics England PanelApp** diagnostic panel lists often continue designating refuted genes as **"Green"** (diagnostic-grade), mandating routine clinical exome reporting.

This asynchronous "knowledge cascade lag" creates acute clinical risks:
1. **False-Positive Molecular Diagnoses:** Reporting variants as pathogenic in refuted genes misleads clinicians into diagnosing monogenic conditions.
2. **Iatrogenic Patient Harm:** Misdiagnoses in cardiovascular genetics (e.g., *SCN1B* in Brugada syndrome, *MYLK2* in hypertrophic cardiomyopathy) have led to unnecessary implantable cardioverter-defibrillator (ICD) implantations and sports restrictions.
3. **Inappropriate Cascade Family Screening:** Families are subjected to genetic counseling and anxiety based on invalid associations.

**CuraCascade** is an open-source clinical genomics data warehousing and automated discrepancy auditing framework. It models multi-source assertions, implements disease-aware entity joins, computes empirical cross-sectional latency, and provides laboratory governance dossiers to assist clinical laboratory directors and bioinformatics researchers.

> **Research and Audit Firewall Disclaimer:** CuraCascade is a research auditing and quality-control framework. It is **not** an autonomous clinical diagnostic decision-support system. It does not automatically reclassify variants or issue definitive medical orders; all flagged discrepancies require qualified clinical molecular geneticist evaluation.

---

## 2. Biological Data Sources & Roles

| Data Source | Entity Level | Role in CuraCascade | Primary Identifiers & Snapshots |
| :--- | :--- | :--- | :--- |
| **ClinGen** (*Clinical Genome Resource*) | Upstream Gene–Disease Validity | Ground-truth consensus appraisals establishing qualitative validity tiers (*Definitive*, *Strong*, *Moderate*, *Limited*, *Disputed*, *Refuted*). | HGNC Symbol, MONDO Disease ID, GCEP Name, Appraisal Timestamp. |
| **NCBI ClinVar** | Downstream Variant Interpretation | Clinical variant interpretations submitted by diagnostic laboratories and research consortia. | Variation ID, HGVS Protein/cDNA, Clinical Significance, Review Stars (0–4). |
| **Genomics England PanelApp** | Downstream Diagnostic Panels | Consensus clinical panel lists utilized by healthcare systems (e.g., UK NHS GMS) for diagnostic exome filtering. | Panel ID, Panel Name, Confidence Status (*Green*, *Amber*, *Red*). |
| **gnomAD v4** (*Genome Aggregation Database*) | Population Genetics Reference | Multi-ancestry continental population allele frequencies and Maximum Credible Allele Frequency (MCAF) ceilings. | Global AF, Popmax AF, Disease-specific MCAF Thresholds. |
| **Monarch / MONDO Ontology** | Disease Ontology Crosswalk | Standardized hierarchical disease concept cross-references unifying OMIM, MedGen, Orphanet, and MONDO. | MONDO ID, OMIM ID, MedGen Concept ID. |

---

## 3. Discrepancy Classification Taxonomy

CuraCascade stratifies discrepancies into three deterministic, clinically actionable classes:

| Class | Upstream ClinGen Curation | Downstream Target Record | Severity | Clinical Hazard Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Class A** | *Disputed* or *Refuted* | ClinVar Variant: Pathogenic / Likely Pathogenic | `CRITICAL` | Candidate false-positive molecular diagnosis in a discredited gene. |
| **Class B** | *Limited* Evidence | ClinVar Variant: Pathogenic / Likely Pathogenic | `HIGH` | Violates ACMG VUS ceiling; premature diagnostic closure. |
| **Class C** | *Disputed* or *Refuted* | PanelApp Panel: "Green" (Diagnostic-Grade) | `CRITICAL` | Routine automated clinical exome screening and reporting of invalid genes. |

---

## 4. Relational Database Architecture (Third Normal Form)

CuraCascade enforces strict **Third Normal Form (3NF)** relational normalization across SQLite and DuckDB.

```
       +-----------------------------+               +-----------------------------+
       |            GENES            |               |          DISEASES           |
       +-----------------------------+               +-----------------------------+
       | * gene_symbol (PK, TEXT)    |               | * disease_id (PK, TEXT)     |
       |   hgnc_id (TEXT)            |               |   disease_name (TEXT)       |
       |   entrez_id (TEXT)          |               |   mondo_id (TEXT)           |
       |   chromosome (TEXT)         |               |   omim_id (TEXT)            |
       |   is_downgraded (INTEGER)   |               |   inheritance_mode (TEXT)   |
       |   highest_severity (TEXT)   |               |   prevalence_per_million    |
       +--------------+--------------+               +--------------+--------------+
                      | 1                                           | 1
                      |                                             |
       +--------------+-----------------------+                     |
       | 1                                    | 1                   |
       |                                      |                     |
       | N                                    | N                   | N
+------v-----------------------+       +------v---------------------v-+
|      CLINGEN_CURATIONS       |       |       CLINVAR_VARIANTS       |
+------------------------------+       +------------------------------+
| * curation_id (PK, AUTOINT)  |       | * variation_id (PK, INTEGER) |
|   gene_symbol (FK -> genes)  |       |   gene_symbol (FK -> genes)  |
|   disease_id (FK -> diseases)|       |   disease_id (FK -> diseases)|
|   moi (TEXT)                 |       |   variant_name (TEXT)        |
|   classification (TEXT)      |       |   clinical_significance(TEXT)|
|   classification_date (TEXT) |       |   is_plp (INTEGER)           |
|   gcep (TEXT)                |       |   review_status (TEXT)       |
|   report_url (TEXT)          |       |   stars (INTEGER [0-4])      |
+--------------+---------------+       |   num_submitters (INTEGER)   |
               |                       |   gnomad_af_global (REAL)    |
               | 1                     |   gnomad_af_popmax (REAL)    |
               |                       |   mcaf_threshold (REAL)      |
               |                       |   population_refuted (INT)   |
               |                       +--------------+---------------+
               |                                      |
               | N                                    | N
+--------------v--------------------------------------v---------------+
|                               AUDIT_FINDINGS                         |
+---------------------------------------------------------------------+
| * finding_id (PK, AUTOINCREMENT)                                    |
|   audit_class (TEXT: 'Class A' | 'Class B' | 'Class C')             |
|   severity (TEXT: 'CRITICAL' | 'HIGH' | 'WARNING')                  |
|   gene_symbol (FK -> genes)                                         |
|   disease_id (FK -> diseases)                                       |
|   curation_id (FK -> clingen_curations)                             |
|   rule_id (TEXT: e.g. 'RULE_CANONICAL_SYNONYM_MATCH')               |
|   match_status (TEXT: 'CONFIRMED_MATCH' | 'REVIEW' | 'UNRESOLVED')  |
|   target_type (TEXT: 'ClinVar Variant' | 'PanelApp Panel')          |
|   target_id (TEXT: variation_id | panel_id)                         |
|   target_status (TEXT: e.g. 'Pathogenic (2 stars)')                 |
|   target_phenotype (TEXT: Associated disease label)                 |
|   disease_match_confidence (TEXT: 'EXACT' | 'HIGH' | 'MODERATE')   |
|   days_unresolved (INTEGER: Elapsed Latency)                        |
|   gnomad_af (REAL) | mcaf_threshold (REAL)                          |
+---------------------------------------------------------------------+
```

### Functional Dependencies & 3NF Proof:
- **`genes`**: Primary Key `gene_symbol`. Dependency: $\text{gene\_symbol} \to \{\text{hgnc\_id}, \text{entrez\_id}, \text{chromosome}, \text{is\_downgraded}, \dots\}$.
- **`diseases`**: Primary Key `disease_id`. Dependency: $\text{disease\_id} \to \{\text{disease\_name}, \text{mondo\_id}, \text{omim\_id}, \text{inheritance\_mode}, \text{prevalence\_per\_million}\}$.
- **`clingen_curations`**: Primary Key `curation_id`. Transitive dependencies eliminated by referencing `gene_symbol` and `disease_id`.
- **`clinvar_variants`**: Primary Key `variation_id`. Variant-level population frequencies are non-transitively dependent on `variation_id`.
- **`panelapp_entries`**: Primary Key `entry_id`.
- **`disease_mappings`**: Primary Key `mapping_id`. Tracks source ontology terms, canonical targets, mapping confidence, and mapping version.
- **`provenance`**: Primary Key `provenance_id`. Cryptographic audit logs recording source URLs, snapshot timestamps, record counts, and SHA-256 checksums.

Dual-engine integration:
- **SQLite 3NF Core:** Enforces ACID transactions, referential foreign keys (`PRAGMA foreign_keys = ON`), and fast B-Tree lookups.
- **DuckDB Analytical Engine:** Attached via zero-copy scanner (`ATTACH 'data/curacascade.db' AS db (TYPE SQLITE);`) for vectorized columnar analytics.

---

## 5. Disease-Aware Biological Matching Engine

A common defect in naive biological databases is treating gene symbols as sufficient join keys. Genes frequently exhibit pleiotropy, causing false discrepancy flags across distinct allelic disorders.

CuraCascade's matching engine (`pipeline/disease_mapping.py`) enforces:
1. **Stable Identifier Matches:** Prioritizes exact MONDO, OMIM, and MedGen identifier equality.
2. **Canonical Concept Dictionary:** Uses curated alias lists for standardized disease concepts.
3. **Distinct Disorder Exclusions:** 
   - *SCN1B*: Brugada syndrome (refuted) vs. Dravet syndrome / GEFS+ (definitive).
   - *KCNE2*: Long QT syndrome / Brugada (refuted) vs. hypokalemic periodic paralysis (distinct).
   - *ACTN2*: Hypertrophic cardiomyopathy (limited/disputed) vs. distal myopathy (definitive).
4. **Pleiotropic Review Routing:** Variants with multiple reported phenotypes spanning target and non-target conditions are assigned `POTENTIAL_DISCREPANCY_REVIEW` (`RULE_PLEIOTROPIC_MATCH`).
5. **Data Quality Handling:** Incomplete or placeholder terms ("not provided", "not specified", "allHighlyPenetrant") are assigned `DATA_QUALITY_ISSUE` rather than false discrepancy flags.

---

## 6. Example SQL Queries for Biological Database Coursework

These SQL queries demonstrate key relational database and biological curation principles:

### Query 1: Genes with Multiple Gene–Disease Curations (Pleiotropy)
*Biological Lesson:* One gene can have multiple distinct validity classifications for different clinical phenotypes.
```sql
SELECT 
    cc.gene_symbol,
    COUNT(DISTINCT cc.disease_id) AS distinct_diseases_count,
    GROUP_CONCAT(DISTINCT d.disease_name || ' [' || cc.classification || ']') AS curations_summary
FROM clingen_curations cc
JOIN diseases d ON cc.disease_id = d.disease_id
GROUP BY cc.gene_symbol
HAVING COUNT(DISTINCT cc.disease_id) > 1
ORDER BY distinct_diseases_count DESC
LIMIT 10;
```

### Query 2: Pathogenic Variant Assertions Associated with a Specific Disease
*Biological Lesson:* Shows how variant assertions link to specific disease ontologies rather than just gene symbols.
```sql
SELECT 
    cv.variation_id,
    cv.gene_symbol,
    cv.variant_name,
    cv.clinical_significance,
    cv.review_status,
    cv.stars,
    d.disease_name
FROM clinvar_variants cv
JOIN diseases d ON cv.disease_id = d.disease_id
WHERE cv.is_plp = 1
  AND d.disease_name LIKE '%Hypertrophic cardiomyopathy%'
ORDER BY cv.stars DESC, cv.variation_id ASC
LIMIT 10;
```

### Query 3: PanelApp Diagnostic Panel Membership by Disease Indication
*Biological Lesson:* Demonstrates how national diagnostic exome services assign diagnostic confidence tiers (*Green*, *Amber*, *Red*) per disease.
```sql
SELECT 
    pe.gene_symbol,
    pe.panel_name,
    pe.confidence,
    d.disease_name
FROM panelapp_entries pe
JOIN diseases d ON pe.disease_id = d.disease_id
WHERE pe.confidence = 'green'
ORDER BY pe.gene_symbol ASC, pe.panel_name ASC
LIMIT 10;
```

### Query 4: Traceable Audit Discrepancies with Source Provenance
*Biological Lesson:* Demonstrates traceability: each finding links back to the ClinGen curation, ClinVar variant, and matching rule.
```sql
SELECT 
    af.finding_id,
    af.audit_class,
    af.severity,
    af.gene_symbol,
    d.disease_name,
    af.clingen_classification,
    af.target_type,
    af.target_id,
    af.target_status,
    af.rule_id,
    af.match_status,
    af.days_unresolved
FROM audit_findings af
JOIN diseases d ON af.disease_id = d.disease_id
WHERE af.audit_class = 'Class A'
ORDER BY af.days_unresolved DESC
LIMIT 10;
```

### Query 5: Unresolved, Review, and Ambiguous Biological Mappings
*Biological Lesson:* Highlights biological uncertainty: not all clinical assertions cleanly map to a single ontology term without manual review.
```sql
SELECT 
    af.finding_id,
    af.gene_symbol,
    af.target_phenotype,
    af.match_status,
    af.rule_id,
    af.disease_match_confidence,
    af.match_rationale
FROM audit_findings af
WHERE af.match_status IN ('POTENTIAL_DISCREPANCY_REVIEW', 'DATA_QUALITY_ISSUE', 'AMBIGUOUS_RELATIONSHIP')
LIMIT 10;
```

### Query 6: Audit Findings Grouped by Discrepancy Class and Severity
*Biological Lesson:* Aggregates multi-source database discordance to quantify the magnitude of the knowledge cascade lag.
```sql
SELECT 
    af.audit_class,
    af.severity,
    af.target_type,
    COUNT(*) AS total_findings,
    COUNT(DISTINCT af.gene_symbol) AS affected_genes_count,
    ROUND(AVG(af.days_unresolved), 1) AS avg_days_unresolved
FROM audit_findings af
GROUP BY af.audit_class, af.severity, af.target_type
ORDER BY af.audit_class ASC;
```

### Query 7: Variant Records with Missing or Incomplete Phenotype Identifiers
*Biological Lesson:* Data quality in biological repositories: ClinVar records often lack standardized disease ontology IDs.
```sql
SELECT 
    cv.variation_id,
    cv.gene_symbol,
    cv.variant_name,
    cv.clinical_significance,
    cv.disease_id
FROM clinvar_variants cv
WHERE cv.disease_id IS NULL OR cv.disease_id = '' OR cv.disease_id = 'not provided'
LIMIT 10;
```

---

## 7. Installation & Quickstart (Windows, Linux, macOS)

### Prerequisites:
- Python 3.11, 3.12, or 3.13
- Git
- (Optional) Docker

### 1. Clone & Set Up Virtual Environment:
```bash
git clone https://github.com/uditshokeen14/curacascade.git
cd curacascade
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Verify Database Integrity:
```bash
python run.py verify
```

### 3. Run Discrepancy Audits via CLI:
```bash
# Audit specific genes:
python run.py audit --genes SCN1B,MYLK2,KCNE2 --class all --format table

# Export Class A findings to CSV or JSON:
python run.py audit --class A --format csv --output class_a_findings.csv
python run.py audit --class A --format json --output class_a_findings.json
```

### 4. Run the Full Test Suite:
```bash
pytest -v
```

### 5. Launch Interactive Web Dashboard:
```bash
streamlit run app.py
```
*Accessible in your browser at `http://localhost:8501`.*

### 6. (Optional) Run with Docker:
```bash
docker build -t curacascade:latest .
docker run -p 8501:8501 curacascade:latest
```

---

## 8. Independent Validation Benchmark Methodology & Results

The validation benchmark (`pipeline/validation_benchmark.py`) evaluates the deterministic audit rules against an independently curated benchmark dataset (`data/raw/benchmark_ground_truth.json`) containing **100 gene–disease validity assertions** (54 downgrades, 46 definitive disease controls) across cardiovascular, cancer, neurodevelopmental, and metabolic domains.

- **Decoupled Architecture:** Prediction outcomes and error assignments are computed directly from the live database, with zero hardcoded outcome overrides.
- **Adjudication Metadata:** Every record includes HGNC symbols, MONDO IDs, source citations, snapshot dates, and clinical rationale.
- **Reviewer Status:** Curated via single-curator expert review. Multi-rater consensus kappa is marked as N/A pending independent secondary review.

### Reproducible Benchmark Execution:
```bash
python -m pipeline.validation_benchmark
```

### Actual Live-Database Benchmark Metrics:

| Cohort Parameter / Metric | Primary Evaluable Cohort ($N = 94$) | Unadjusted Full Cohort ($N = 100$) | 95% Wilson Confidence Interval (Evaluable) |
| :--- | :---: | :---: | :---: |
| **Total Benchmark Assertions** | **94** | **100** | — |
| **Cohort Coverage Rate** | **94.0%** (94 / 100) | **100.0%** | — |
| **Excluded Cases (`NOT_EVALUABLE`)** | **6** | **0** | — |
| **True Positives (TP)** | **18** | **18** | — |
| **False Positives (FP)** | **0** | **0** | — |
| **True Negatives (TN)** | **42** | **46** | — |
| **False Negatives (FN)** | **34** | **36** | — |
| **Precision (PPV)** | **100.0%** | **100.0%** | **82.4% – 100.0%** |
| **Recall (Sensitivity)** | **34.6%** | **33.3%** | **23.2% – 48.2%** |
| **Specificity (TNR)** | **100.0%** | **100.0%** | **91.6% – 100.0%** |
| **Overall Accuracy** | **63.8%** | **64.0%** | **53.8% – 72.8%** |
| **F1-Score** | **0.5143** | **0.5000** | — |
| **Concordance Kappa ($\kappa$)** | **0.3212** | **0.3151** | — |

- **False Positive Elimination ($12 \to 0$):** In naive matching, broad keyword overlap caused distinct disorders in multi-disease genes (*MLH1, MSH2, MSH6, PMS2, FBN1, MYH11, RYR2, KCNQ1, KCNH2, SCN5A, MYH7, MYBPC3*) to be flagged against unrelated curations (e.g. Lynch syndrome vs breast cancer). Enforcing ontology crosswalk matches and routing broad keyword overlap to `is_match=False` (`POTENTIAL_DISCREPANCY_REVIEW`) eliminated all 12 false positives. Importantly, valid discrepancy alerts (e.g., 1,954 *MLH1* breast cancer findings) remain active in the warehouse and were simply not conflated with negative control diseases.
- **18 True Positives Verified:** All 18 TPs (*MYLK2, TCAP, MYOZ2, NEXN, VCL, KCNE2, SCN1B, GPD1L, KCNJ8, HCN4, TRPM4, BRIP1, NBN, RAD50, XRCC2, SLX4, A2ML1, AKAP9*) have confirmed upstream ClinGen downgrades and matching downstream ClinVar P/LP or PanelApp Green alerts.
- **Investigation of 34 False Negatives:** Exhaustive case-level analysis shows that FNs partition into 3 distinct biological mechanisms:
  1. *Absent downstream assertions (15 cases)*: ClinVar contains 0 P/LP variants and PanelApp contains 0 Green panels for the target gene in the snapshot. A clinical discrepancy cannot trigger when laboratories assert zero pathogenicity.
  2. *Target curation absent from ClinGen snapshot (3 cases: ACTN2, MECP2, SHANK3)*: Target downgraded curation missing from snapshot while Definitive curations exist for other phenotypes.
  3. *Cross-disease finding mismatch (16 cases: ANK2, BARD1, CHEK2, etc.)*: Active findings exist in the warehouse for other diseases (e.g., CPVT or ovarian cancer), but none for the benchmark target disease. Conflating distinct diseases to inflate recall would violate biological specificity.
- **Coverage & Absent Evidence:** 6 cases (*XRCC3, DFNB59, TSC1, TSC2, SMAD3, SMN1*) lack gene/curation records in the local warehouse snapshot. They are classified as `NOT_EVALUABLE` to avoid manufacturing false negative or false positive counts.
- **Database Rebuild & Ingestion Idempotency:** The database rebuild test (`init_db(drop_existing=True)`) and repeated ingestion test enforce composite unique constraints (`uq_clingen_curation`, `uq_panelapp_entry`), maintain 0 foreign-key defects (`PRAGMA foreign_key_check`), and preserve cryptographic provenance logging.
- **Prediction Algorithm Integrity:** The automated prediction algorithm queries live discrepancy join records without accessing benchmark gold labels.

---

## 9. Latency Modeling & Machine Learning Integrity

### Empirical Latency Analysis (`pipeline/survival_analysis.py`):
- **Cross-Sectional Cohort:** Evaluates 51,007 active ClinVar assertions across 536 curated genes.
- **Median Elapsed Latency:** **2.82 years** (1,030 days; IQR: 2.98 years).
- **Domain Breakdown:** Cardiovascular median = 1.39 years; Neurology median = 4.85 years ($p < 0.001$).
- **Review Confidence:** $\ge 2$ stars median = 1.84 years vs. 0–1 stars median = 3.15 years ($p < 0.001$).
- **No Synthetic Fallback by Default:** Analysis fails cleanly or reports observed data. Synthetic simulation mode (`--simulate`) requires an explicit CLI flag and outputs an unmistakable `SYNTHETIC_DEMONSTRATION` provenance warning.

```bash
# Empirical cross-sectional analysis:
python -m pipeline.survival_analysis

# Optional course demonstration simulation:
python -m pipeline.survival_analysis --simulate
```

### Machine Learning Downgrade Vulnerability (`pipeline/forecasting.py`):
- **Model Status:** `EXPLORATORY_RETROSPECTIVE_EVALUATION`
- **Methodology & Temporal Leakage Advisory:** Features reflect cross-sectional warehouse snapshots; prospective predictive performance cannot be claimed until features are reconstructed from longitudinal pre-appraisal snapshots.
- **Score Calibration:** Raw Random Forest scores are designated as **uncalibrated risk priority indices** (Brier score: **0.1508**; Logistic Regression baseline: **0.1348**).
- **Performance:** AUROC = 0.857; PR-AUC = 0.814; Precision@Top-20% = 75.8%.
- **Top Feature Drivers:** Low ClinVar star ratio (70.2%) and non-green PanelApp indications (26.0%).
- **Calibrated Probabilities:** Output represents direct model probabilities without arbitrary manual additive boosts. Rule-based risk triggers (e.g. MCAF ceiling violations) are exposed as independent heuristic flags.

```bash
python -m pipeline.forecasting
```

---

## 10. Repository Structure

```
curacascade/
├── run.py                                # Unified CLI entrypoint (audit, verify, serve)
├── config.py                             # Configuration paths, thresholds, and mappings
├── requirements.txt                      # Pinned Python dependencies
├── pytest.ini                            # Pytest test suite configuration
├── Dockerfile                            # Production container specification
├── app.py                                # Streamlit clinical audit web dashboard
├── database/
│   ├── __init__.py                       # Database package exports
│   ├── connection.py                     # Thread-safe SQLite/DuckDB connection manager
│   ├── duckdb_engine.py                  # Columnar analytical scanning engine
│   └── schema.py                         # 3NF DDL schema, migrations, and views
├── pipeline/
│   ├── __init__.py                       # Pipeline package exports
│   ├── disease_mapping.py                # Disease-aware concept matching and exclusions
│   ├── audit.py                          # Cross-layer audit engine and finding materialization
│   ├── validation_benchmark.py           # Independent validation benchmark pipeline
│   ├── survival_analysis.py              # Empirical cross-sectional latency analyzer
│   ├── forecasting.py                    # Cross-sectional ML vulnerability forecaster
│   ├── remediation.py                    # Clinical governance dossier generator
│   ├── allele_frequency.py               # gnomAD MCAF ceiling and frequency calculator
│   ├── build_full_warehouse.py           # Full 51k-variant warehouse ETL builder
│   ├── fetch_data.py                     # Real data fetchers (ClinGen, ClinVar, PanelApp)
│   ├── seed_sample_data.py               # 35+ showcase genes database generator
│   └── verify_integrity.py               # Foreign-key and cryptographic integrity auditor
├── tests/
│   ├── test_biological_matching.py       # Entity matching, exclusions, and pleiotropy tests
│   ├── test_database_integrity.py        # PK uniqueness, FK enforcement, and 3NF tests
│   └── test_scientific_statistical_integrity.py # Benchmark, survival, and ML integrity tests
├── test_cli.py                           # CLI exit codes and output formatting tests
├── test_dossier.py                       # Clinical governance dossier tests
├── docs/
│   └── MANUSCRIPT.md                     # Academic manuscript and technical documentation
└── data/
    ├── raw/
    │   └── benchmark_ground_truth.json   # 100-gene independently curated benchmark
    ├── processed/                        # Exported audit reports
    ├── curacascade.db                    # Showcase 36-gene SQLite database
    └── curacascade_full.db               # Full warehouse (3,833 genes, 51,025 variants)
```

---

## 11. Known Limitations & Future Work

1. **Static Snapshot Censoring:** A single database snapshot cannot capture historical retraction timestamps for variants modified in past years. Future iterations will integrate monthly historical ClinVar release snapshots to reconstruct dynamic assertion lifespans.
2. **Benchmark Single-Reviewer Status:** The 100-gene ground-truth dataset was curated by a single clinical genomics reviewer. Dual-reviewer consensus curation is planned to calculate formal inter-rater agreement ($\kappa$).
3. **Ontology Crosswalk Coverage:** While canonical mappings cover major disease concepts, rare or legacy phenotype strings may remain unmapped or default to broad clinical domain categories.
4. **Prospective Model Evaluation:** Current ML models evaluate cross-sectional vulnerability rather than prospective prediction. Longitudinal pre-appraisal feature tracking is required before models can be utilized prospectively.

---

## 12. License & Attribution

- **License:** CuraCascade is released under the permissive [MIT License](LICENSE).
- **ClinGen Data:** Public domain (U.S. Government work, NHGRI/ClinGen).
- **ClinVar Data:** Public domain (NCBI, National Library of Medicine).
- **Genomics England PanelApp:** Open Government Licence v3.0 / Creative Commons.
- **gnomAD Data:** Open access under the terms of the gnomAD consortium.

---

## 13. Author Information

**Udit Shokeen**  
School of Computer Science and Engineering,  
Vellore Institute of Technology, Vellore, Tamil Nadu, India.  
Contact: `uditshokeen14@gmail.com` | GitHub: [@uditshokeen14](https://github.com/uditshokeen14)
