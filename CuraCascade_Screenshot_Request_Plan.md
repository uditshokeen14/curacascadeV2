# CuraCascade: Screenshot Integration Plan & Evidentiary Audit

**Document:** CuraCascade Live Interface Visual Verification Plan  
**Lead Author:** Udit Shokeen (Reg. No: 23BCB0001)  
**Deployment URL:** [https://curacascadev2.streamlit.app/](https://curacascadev2.streamlit.app/)  
**Destination Folder:** [`docs/figures/screenshots/`](file:///h:/Projects/curacascade/docs/figures/screenshots)  

---

## 1. Executive Screenshot Verification Summary

In strict accordance with the project's **Mandatory Screenshot Policy (Section 5)**, no interface views, tables, or metrics have been fabricated or synthesized. All visual application evidence was captured directly from the live deployed instance of CuraCascade running on Streamlit Cloud (`curacascadev2.streamlit.app`).

Each capture was processed through a standardized forensic workflow:
1. **Inspection**: Verifying authentic database records and real-time telemetry.
2. **Cropping**: Removing operating system chrome (browser tab strip, URL address bar, taskbar) to maximize legible interface area.
3. **Data Integrity Check**: Zero alteration of table values, variant HGVS expressions, review stars, or statistical percentages.
4. **Slide Assignment**: Positioning high-resolution captures in Slides 07 and 08 with targeted analytical callouts.

---

## 2. Detailed Screenshot Manifest & Evaluation Matrix

| ID | File Source | Dimension | Destination Slide | Evaluation Verdict | Key Evidentiary Elements |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **S1** | `s1_dashboard_hero.png` | $1024 \times 544$<br>*(Cropped: $1024 \times 431$)* | **Slide 07 (Live UI Walkthrough)** | **USE (Top Frame)** | • Sidebar brand card: `CURACASCADE AUDIT ENGINE // V2.4`<br>• Real-time HUD: `curacascade.db`, 36 Curated Genes, 46 Variants, 34 Inconsistencies<br>• Hero header: *"Three databases. One truth."*<br>• 5 Top KPI Cards: Curated Genes (36), Discrepancies (34), Class A (20), Class B (8), Patient-Years at Risk (202.5 Yrs). |
| **S2** | `s2_audit_table_full.png` | $1024 \times 544$<br>*(Cropped: $1024 \times 431$)* | **Slide 07 (Live UI Walkthrough)** | **USE (Bottom Frame)** | • Materialized Audit Table: 13 active findings visible (*GJB6*, *MYLK2*, *TCAP*, *DFNB59*, *CACNA2D1*, *MYOZ2*, *ANK2*, *GPD1L*, *CAV3*)<br>• Severity badges: `CRITICAL` Class A and Class C findings<br>• Concrete prescriptive directives: `Apply ACMG BA1/BS1 Benign`, `Demote Panel to Red`<br>• Taxonomy Reference guide at bottom. |
| **S3** | `s3_custom_gene_evaluator.png` | $1024 \times 544$<br>*(Cropped: $1024 \times 431$)* | **Slide 08 (Clinical Case Studies)** | **USE (Bottom Frame)** | • Custom Gene Evaluator input: `ANK2, MYLK2, TCAP, TTN, MYH7`<br>• Live audit verdicts: *ANK2* Flagged (Class A), *MYLK2* Flagged (Class A, C), *TCAP* Flagged (Class A), *TTN* Uncurated Gene, *MYH7* Validated Benchmark (Definitive)<br>• Review star ratings: 1 to 3 stars ClinVar confidence glyphs. |
| **S4** | `s4_gene_detail_actn2.png` | $1024 \times 544$<br>*(Cropped: $1024 \times 431$)* | **Slide 08 (Clinical Case Studies)** | **USE (Top Frame)** | • Gene-Centric Cascade Deep Dive: *ACTN2* [Definitive Benchmark]<br>• Gene metadata: HGNC:164, Locus 1q43<br>• ClinGen validity status: `DEFINITIVE BENCHMARK` (Clinically validated relationship)<br>• Biological Specificity Banner: `Consistent Status for ACTN2: No downstream discrepancies detected. Downstream assertions adhere to ClinGen validity ratings.` |
| **S5** | `s2_audit_explorer_overview.png` | $1024 \times 544$<br>*(Cropped: $1024 \times 431$)* | *Archived Reference* | **EXCLUDE (Redundant)** | Excluded from the final slide deck because `s2_audit_table_full.png` displays more table rows and richer clinical directives in the same spatial footprint. |

---

## 3. Privacy, Security & Compliance Audit

- **PHI / PII Audit**: All gene symbols (*ACTN2*, *SCN1B*, *MYLK2*, *ANK2*), variants (e.g. `c.101C>T`), and panel IDs are derived from public reference archives (ClinGen, ClinVar, PanelApp). Zero identifiable patient health information is displayed.
- **Credential & Token Audit**: No API keys, database connection strings, or cloud environment secrets are visible in any capture.
- **Image Cropping Integrity**: Cropping applied strictly to outer browser chrome (Y = 78px to Y = 509px). Zero modification or blurring of internal table contents or metric values.
