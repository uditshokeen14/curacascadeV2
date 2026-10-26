# CuraCascade: Final Validation and Quality Sign-Off Record

**Document Title:** CuraCascade Final Validation and Quality Sign-Off  
**Researcher:** Udit Shokeen (Registration Number: 23BCB0001)  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Vellore, Tamil Nadu 632014, India  
**Email:** `udit.shokeen2023@vitstudent.ac.in`  
**Date:** October 25, 2026  
**Auditor:** Antigravity Autonomous Academic & Engineering Auditor  
**Workspace:** `h:\Projects\curacascade`  
**Output Directory:** `h:\Projects\curacascade\report_revised/`

---

## 1. Deliverables Checklist & Integrity Audit

The following revised deliverables have been generated in `report_revised/` without overwriting the previous report:

| Deliverable File | Target Path | File Size | Content Verification |
| :--- | :--- | :---: | :--- |
| **Revised IEEE PDF** | `report_revised/CuraCascade_IEEE_Report_Revised.pdf` | 1.18 MB | Exactly 7.0 pages; verified via `pypdf`; two-column IEEE layout; embedded 300 DPI figures; 5 structured tables; clean reference flow. |
| **Revised LaTeX Source** | `report_revised/CuraCascade_IEEE_Report_Revised.tex` | 36.3 KB | `\documentclass[conference]{IEEEtran}`; 339 lines; complete author block with Reg. No: 23BCB0001; 5 tables; native BibTeX citations. |
| **Revised Word Document** | `report_revised/CuraCascade_IEEE_Report_Revised.docx` | 859 KB | Microsoft Word document formatted in two-column IEEE specifications; custom margins; embedded figures; styled data tables. |
| **Claim & Citation Audit** | `report_revised/CuraCascade_Claim_and_Citation_Audit.md` | 18.2 KB | 20-row Claim-Verification Table; 19 verified primary citations; comprehensive 6-question Student Viva Defense Guide. |
| **Substantive Revision Log** | `report_revised/CuraCascade_Revision_Log.md` | 11.5 KB | Section-by-section breakdown of improvements, terminology corrections, and architectural clarifications. |
| **Final Validation Record** | `report_revised/CuraCascade_Final_Validation.md` | ~12 KB | This document; complete sign-off, numerical verification table, and test execution log. |
| **Verified BibTeX File** | `report_revised/references.bib` | 12.5 KB | 19 peer-reviewed citations with authentic DOIs, authors, journals, and page numbers. |
| **High-DPI Figures** | `report_revised/figures/` | 850 KB total | 4 publication-grade figures at 300 DPI (`fig1_architecture.png`, `fig2_matching_workflow.png`, `fig3_confusion_matrix.png`, `fig4_empirical_latency.png`). |

---

## 2. Independent Test Suite Execution Log

The entire automated test suite was executed against the live workspace codebase:

```bash
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: H:\Projects\curacascade
configfile: pytest.ini
testpaths: test_cli.py, test_dossier.py, tests
plugins: anyio-4.15.1, cov-7.1.0
collected 47 items

test_cli.py ..........                                                   [ 21%]
test_dossier.py .                                                        [ 23%]
tests\test_biological_matching.py .....................                  [ 68%]
tests\test_database_integrity.py .........                               [ 87%]
tests\test_scientific_statistical_integrity.py ......                    [100%]

============================= 47 passed in 45.42s =============================
```

- **Exit Code:** 0 (Clean exit)
- **Status:** **47 passed, 0 failed, 0 errors**
- **Test Breakdown:**
  - `test_cli.py`: 10 passed (CLI arguments, exit codes, filtering flags, JSON/CSV exports)
  - `test_dossier.py`: 1 passed (Clinical remediation dossier compilation)
  - `tests/test_biological_matching.py`: 21 passed (Concept crosswalks, pleiotropic exclusions, multi-disease gene discrimination)
  - `tests/test_database_integrity.py`: 9 passed (3NF schema, SQLite foreign keys, domain range limits, idempotent ingestion)
  - `tests/test_scientific_statistical_integrity.py`: 6 passed (Wilson score confidence interval derivations, live benchmark queries without overrides, cross-sectional latency statistics)

---

## 3. Database Referential & Cryptographic Verification

Executed `python run.py verify` across all live SQLite database instances:

```text
================================================================================
🧬 CURACASCADE DATA INTEGRITY & CLINICAL SECURITY AUDIT REPORT
Target Database : H:\Projects\curacascade\data\curacascade.db (Showcase Warehouse)
================================================================================
CHECK NAME                               | TARGET                   | STATUS
--------------------------------------------------------------------------------
SQLite B-Tree & Page Integrity Check     | Database Structure       |   PASS  
Foreign Key Referential Integrity Scan   | 3NF Relational Tables    |   PASS  
Domain Range: Allele Frequency (gnomad)  | clinvar_variants.gnomad  |   PASS  
Domain Range: ClinVar Review Stars       | clinvar_variants.stars   |   PASS  
Domain Range: Discrepancy Classification | audit_findings.audit_cls |   PASS  
Cryptographic Checksum & Non-Emptiness   | Source Archives (SHA256) |   PASS  
--------------------------------------------------------------------------------
✅ ALL INTEGRITY & SECURITY CHECKS PASSED — REFERENTIAL CONSTRAINTS ENFORCED
================================================================================
```
- **Exit Code:** 0
- Both `data/curacascade.db` and `data/curacascade_full.db` passed all structural, foreign-key, and range-boundary integrity checks.

---

## 4. Re-Verification of Numerical Claims & Mathematical Derivations

All numerical metrics in the revised report were recalculated directly from underlying integer confusion matrices:

| Metric | Evaluable Cohort ($N = 94$) | Full Sensitivity Cohort ($N = 100$) | Verification Source / Formula | Check |
| :--- | :---: | :---: | :--- | :---: |
| **True Positives ($TP$)** | 18 | 18 | Verified 18 downgraded genes with active downstream P/LP assertions | PASS |
| **False Positives ($FP$)** | 0 | 0 | Concept-matching rules eliminated all 12 prior false alerts | PASS |
| **False Negatives ($FN$)** | 34 | 36 | 15 data sparsity + 3 snapshot omission + 16 cross-disease | PASS |
| **True Negatives ($TN$)** | 42 | 46 | Controls correctly unflagged ($42 + 4$ unobserved controls) | PASS |
| **Precision (PPV)** | **100.0%** [82.4%, 100.0%] | **100.0%** [82.4%, 100.0%] | $18 / (18 + 0) = 1.0$; Wilson score interval: $[0.8241, 1.0]$ | PASS |
| **Recall (Sensitivity)** | **34.62%** [23.2%, 48.2%] | **33.33%** [22.2%, 46.7%] | $18 / (18 + 34) = 0.3462$; Wilson score interval: $[0.2315, 0.4820]$ | PASS |
| **Specificity (TNR)** | **100.0%** [91.6%, 100.0%] | **100.0%** [92.3%, 100.0%] | $42 / (42 + 0) = 1.0$; Wilson score interval: $[0.9162, 1.0]$ | PASS |
| **Accuracy** | **63.83%** [53.8%, 72.8%] | **64.00%** [54.2%, 72.7%] | $(18 + 42) / 94 = 0.6383$; Wilson score interval: $[0.5375, 0.7282]$ | PASS |
| **Cohen's Kappa ($\kappa$)** | **0.3212** | **0.3151** | Chance-adjusted agreement: $P_o = 0.6383, P_e = 0.4671$ | PASS |
| **Latency Sample Size** | 51,007 assertions | 536 unique genes | Direct SQL count of ClinVar assertions in downgraded genes | PASS |
| **Median Latency** | 2.82 years (1,030 days) | IQR: 2.98 yr (1,087 days) | Elapsed time from ClinGen appraisal to 2024-10-01 snapshot | PASS |
| **ML Performance** | AUROC = 0.857 | Brier Score = 0.1508 | Retrospective Random Forest; uncalibrated risk priority index | PASS |

---

## 5. Visual PDF Page-by-Page Inspection

The generated `CuraCascade_IEEE_Report_Revised.pdf` was examined page by page:
- **Page 1:**
  - Title: Perfectly centered, 19 pt bold font.
  - Author: `Udit Shokeen (Reg. No: 23BCB0001)` prominently displayed.
  - Affiliation: School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, Tamil Nadu 632014, India.
  - Email: `udit.shokeen2023@vitstudent.ac.in`.
  - Abstract & Index Terms: Spanning left column with distinct bold headers.
  - Section I (Introduction) begins smoothly with proper paragraph indentation.
- **Page 2:**
  - Section II (Background and Related Work), Section III (Problem Statement).
  - Equation (1) centered with clean right-aligned number `(1)`.
  - Figure 1 (`fig1_architecture.png`) placed cleanly with clear text labels and no overlap.
- **Page 3:**
  - Section IV (Architecture), Section V (Data Sources), Table I (Primary Evidence Sources vs. Mondo).
  - Section VI (Database Design), Table II (3NF Schema).
  - Figure 2 (`fig2_matching_workflow.png`) centered with crisp decision boxes.
- **Page 4:**
  - Section VII (Disease Matching), Section VIII (Implementation Details).
  - Figure 3 (`fig3_confusion_matrix.png`) spanning across columns with high-DPI heatmap and Wilson error bars.
- **Page 5:**
  - Section IX (Experimental Setup and Results).
  - Table III (Benchmark Evaluation Metrics: Evaluable vs. Sensitivity Analysis).
  - Table IV (Taxonomy of 34 False Negatives).
  - Figure 4 (`fig4_empirical_latency.png`) centered showing specialty and review-star latency distributions.
- **Page 6:**
  - Section IX-F (Latency Analysis), Section IX-G (Exploratory ML).
  - Section X (Discussion and Limitations), Table V (Technical Limitations & Research Governance).
  - Section XI (Ethical Considerations and Intended Use).
- **Page 7:**
  - Section XII (Conclusion and Future Work).
  - Reproducibility & Verification block (MIT License, GitHub URL, CLI commands).
  - References: Complete listing of all 19 verified references ([1] to [19]) filling the page cleanly.
  - Zero overflow to an empty 8th page.

---

## 6. Final Sign-Off

The revised deliverables in `h:\Projects\curacascade\report_revised/` are:
1. Fully compliant with IEEE conference publication standards.
2. 100% harmonized between LaTeX, Word, and PDF formats.
3. Completely grounded in verified empirical results and live database records.
4. Fully prepared for academic defense by student Udit Shokeen (Reg. No: 23BCB0001).
