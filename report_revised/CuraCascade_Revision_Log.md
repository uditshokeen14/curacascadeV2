# CuraCascade IEEE Project Report — Substantive Revision Log

**Document:** CuraCascade IEEE Project Report Revision  
**Author:** Udit Shokeen (Reg. No: 23BCB0001)  
**Date:** October 25, 2026  
**Destination Folder:** `h:\Projects\curacascade\report_revised/`

---

## 1. Overview of Substantive Edits

This revision log details the section-by-section improvements, terminology corrections, and architectural clarifications applied to create the revised, defense-ready IEEE conference report for **CuraCascade**.

All edits were executed with a strict focus on:
1. **Technical Precision:** Explaining the exact mechanism implemented in the code (e.g. 3-tier disease crosswalk, SQLite/DuckDB dual engine, SHA-256 provenance).
2. **Defensible Scholarship:** Framing evaluation metrics transparently, avoiding overstated precision or prospective ML claims, and clarifying sample size constraints.
3. **Student Defence Alignment:** Ensuring every statement can be defended during a university project viva by Udit Shokeen.

---

## 2. Section-by-Section Revision Detail

### Title & Author Block
- **Original:** Generic author block with placeholder email.
- **Revised:** Formatted with student name, university registration number, department, and institutional email:
  ```latex
  \author{\IEEEauthorblockN{Udit Shokeen (Reg. No: 23BCB0001)}
  \IEEEauthorblockA{\textit{School of Computer Science and Engineering} \\
  \textit{Vellore Institute of Technology}\\
  Vellore, Tamil Nadu 632014, India \\
  Email: udit.shokeen2023@vitstudent.ac.in}
  }
  ```

### Abstract & Index Terms
- **Substantive Edits:**
  - Clearly articulated the three distinct ClinGen tiers: *Limited* (insufficient evidence), *Disputed* (conflicting evidence), and *Refuted* (evidence against validity).
  - Explicitly stated that downstream variants are not globally invalid across all conditions, but represent *potential disease-specific discrepancies requiring expert review*.
  - Clarified cohort sizes: 94 of 100 cases evaluable; 6 unobserved cases designated `NOT_EVALUABLE`.
  - Stated sensitivity analysis results ($N = 100$, Recall = 33.3%, Accuracy = 64.0%) alongside the evaluable cohort results ($N = 94$, Precision = 100.0%, Recall = 34.6%, Specificity = 100.0%, Accuracy = 63.8%).
  - Clarified that the 2.82-year latency measures active cross-sectional elapsed duration in a static snapshot.
  - Toned down system claims from "preventing clinical harm" to "providing an automated research audit framework to prioritize potential discrepancies."

### Section I: Introduction
- **Substantive Edits:**
  - Expanded on the historical genesis of spurious gene–disease associations (small kindreds, candidate-gene testing without population control sequencing).
  - Defined the operational roles of ClinGen, ClinVar, and PanelApp.
  - Highlighted the clinical dangers of unpropagated gene refutations in cardiology (e.g., *MYLK2*, *TCAP*, *ANK2* causing inappropriate implantable cardioverter-defibrillator [ICD] procedures and unwarranted familial testing).
  - Emphasized that CuraCascade is a research auditing platform designed to support diagnostic laboratories in re-curation triage.

### Section II: Background and Related Work
- **Substantive Edits:**
  - Contrasted existing variant-centric discordance tools with CuraCascade's focus on the *gene-to-variant semantic gap*.
  - Cited foundational literature: ACMG/AMP variant interpretation guidelines (Richards et al. 2015), ClinGen clinical validity framework (Strande et al. 2017; Rehm et al. 2015), ClinVar (Landrum et al. 2020), and PanelApp (Martin et al. 2019).
  - Corrected the conceptual explanation: downgrading a gene does not automatically make all constituent variants benign; rather, it questions the diagnostic attribution of pathogenicity under that specific disease entity.

### Section III: Problem Statement and Objectives
- **Substantive Edits:**
  - Formulated the mathematical tuple representation of ClinGen validity ($A_{\text{CG}}$) and downstream variant/panel assertions ($A_{\text{CV}}, A_{\text{PA}}$).
  - Defined the latency equation $\Delta t = t_{\text{obs}} - t_{\text{CG}}$ explicitly as cross-sectional elapsed discordance duration.
  - Enumerated four concrete engineering objectives: Relational Evidence Harmonization, Deterministic Biological Audit Engine, Empirical Latency Characterization, and Transparent Independent Benchmarking.

### Section IV: System Architecture and Methodology
- **Substantive Edits:**
  - Described the four-layer decoupled system architecture (Ingestion, 3NF Storage, Audit Engine, Interfaces).
  - Integrated redesigned Figure 1 (`fig1_architecture.png`) with clean vector boxes, balanced column widths, and non-overlapping text labels.

### Section V: Data Sources and Data Processing (Table I)
- **Substantive Edits:**
  - Explicitly separated **Primary Biological Evidence Sources** (ClinGen, ClinVar, PanelApp, gnomAD) from the **Reference Disease Ontology** (Mondo Disease Ontology).
  - Added specific versions and snapshot dates (ClinGen Q1 2024, ClinVar Oct 2024, PanelApp API v1 2024, gnomAD v4.0, Mondo v2024-03).
  - Designated as **Table I** and verified in-text reference.

### Section VI: Database Design and Evidence Integration (Table II)
- **Substantive Edits:**
  - Detailed Third Normal Form (3NF) relational design across all 8 core entities.
  - Designated as **Table II** and verified in-text reference.
  - Documented SQLite referential integrity mechanisms (`PRAGMA foreign_keys = ON`), composite idempotency constraints (`uq_clingen_curation`, `uq_panelapp_entry`), and SHA-256 cryptographic provenance logging.

### Section VII: Disease-Matching and Validation Methodology
- **Substantive Edits:**
  - Detailed the three-tier concept matching hierarchy: Exact Ontology Matching (MONDO/OMIM IDs), Canonical Synonym Crosswalk, and Distinct Disorder Exclusions.
  - Detailed the pleiotropic safeguard in multi-disease genes (*MLH1*, *MSH2* Lynch syndrome vs. breast cancer) to explain why naive keyword overlap fails.
  - Detailed discrepancy classes: Class A (Direct Clinical Discrepancy), Class B (Indication Mismatch), Class C (Ambiguous / Data Quality).

### Section VIII: Implementation Details
- **Substantive Edits:**
  - Detailed core Python modules: `database/connection.py`, `database/duckdb_engine.py`, `run.py`, and `app.py`.
  - Documented CLI commands (`run.py audit`, `run.py verify`) and automated verification suite.

### Section IX: Experimental Setup and Results (Tables III & IV, Figures 3 & 4)
- **Substantive Edits:**
  - Detailed the 100-case curated benchmark: 54 published downgrades (28 Limited, 14 Disputed, 12 Refuted) and 46 negative controls.
  - **Table III:** Reconciled 94 evaluable cases vs. 100-case sensitivity cohort. Removed misleading 100% evidence coverage entry. Reported 95% Wilson confidence intervals for all metrics.
  - **Cohort Reconciliation:** Documented the 6 unobserved cases (`XRCC3`, `DFNB59`, `TSC1`, `TSC2`, `SMAD3`, `SMN1`) and explained why they are designated `NOT_EVALUABLE`.
  - **Table IV:** Detailed biological failure-mode taxonomy of the 34 false negatives (15 absent downstream assertions, 3 target curations absent from snapshot, 16 cross-disease mismatches).
  - **True Positives & Zero False Positives:** Documented all 18 True Positive genes. Confirmed that zero false positives was achieved by concept gating, with thousands of findings remaining active in `audit_findings` under other phenotypes.
  - **Figure 3 & Figure 4:** High-resolution 300 DPI figures embedded with descriptive captions.
  - **Empirical Latency Analysis:** Reported median of 2.82 years (1,030 days; IQR 2.98 years / 1,087 days). Reported verified Mann–Whitney $U$ test ($p < 0.001$) and Kruskal–Wallis specialty tests ($p < 0.001$). Clarified cross-sectional right-censoring constraint.
  - **Exploratory Machine Learning:** Documented Random Forest screening (AUROC = 0.857, Brier = 0.1508). Disclosed look-ahead temporal leakage; classified outputs as uncalibrated risk priority indices.

### Section X: Discussion and Limitations (Table V)
- **Substantive Edits:**
  - **Table V:** Detailed system limitations, operational boundaries, and research governance constraints.
  - Discussed the recall–precision trade-off in clinical auditing: why prioritizing 100% precision over recall is appropriate for diagnostic safety.

### Section XI: Ethical Considerations and Intended Use
- **Substantive Edits:**
  - Toned down clinical safety claims; stated that CuraCascade is a research auditing and curation prioritization tool, not an autonomous clinical diagnostic system.
  - Stated that the tool does not establish biological causality and does not replace professional clinical geneticist evaluation.

### Section XII: Conclusion and Future Work
- **Substantive Edits:**
  - Summarized core contributions: 3NF warehouse, disease-aware concept matching, empirical latency quantification, and reproducible CLI audit tooling.
  - Outlined future work: historical longitudinal XML archive ingestion, multi-rater blinded consensus adjudication, and HL7 FHIR Genomics integration.

### Reproducibility & References
- **Substantive Edits:**
  - Documented exact commands: `pytest -v`, `python run.py verify`, `python -m pipeline.validation_benchmark`.
  - Verified all 19 citations against peer-reviewed journals with authentic DOIs.
