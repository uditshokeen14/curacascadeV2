# CuraCascade V2: Master Speaker Notes & Oral Defense Script
**Author:** Udit Shokeen (Reg. No: 23BCB0001)  
**Affiliation:** School of Computer Science & Engineering, Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India  
**Target Duration:** 15–18 Minutes (Average ~40–45 seconds per slide)  
**Accompanying Deck:** `CuraCascade_Presentation_V2_25Slides.pptx` / `CuraCascade_Presentation_V2_25Slides.pdf`  
**Live Application:** [https://curacascadev2.streamlit.app/](https://curacascadev2.streamlit.app/)  
**Target Repository:** [https://github.com/uditshokeen14/curacascadeV2](https://github.com/uditshokeen14/curacascadeV2)  

---

## 🎙️ Defense Delivery Strategy & Psychological Ground Rules

1. **The Pace of Authority:** Speak at 130–140 words per minute. Do not rush. Rushing signals panic; deliberate pauses signal mastery.
2. **The "Claim-Evidence-Boundary" Framework:** Every technical assertion must have three parts:
   - **Claim:** What the system does or what the data shows.
   - **Evidence:** The exact verified metric, table, or code mechanism backing it.
   - **Boundary:** What the system *does not* do or the honest limitation of that finding.
3. **Guardrails (Things You Must NEVER Say):**
   - ❌ *Never say:* "CuraCascade is an autonomous clinical diagnostic tool."  
     ✅ *Say:* "CuraCascade is an audit and governance platform designed to assist clinical bioinformaticians."
   - ❌ *Never say:* "Our machine learning model predicts real-world clinical downgrades prospectively."  
     ✅ *Say:* "Our model is a retrospective feature-importance triage demonstration with inherent temporal snapshot leakage."
   - ❌ *Never say:* "We achieved 100% accuracy."  
     ✅ *Say:* "We achieved 100% precision on the evaluable benchmark cohort, with a conservative sensitivity of 34.6%, intentionally prioritizing zero false-positive alerts."

---

## ⏱️ Master Slide-by-Slide Delivery Script

---

### Slide 1: Title & Academic Affiliation
- **Time Target:** 00:30 (Running Time: `00:00 – 00:30`)
- **Visual Cue:** Slide displays Dark Space Navy theme, institutional crest, author details, verified GitHub repository, and live Streamlit deployment URL.
- **Key Takeaway:** Establish professional identity, academic rigor, and the precise scope of CuraCascade V2.

#### Spoken Transcript
> "Respected committee members, examiners, and faculty colleagues: Good morning. My name is Udit Shokeen, registration number 23BCB0001, from the School of Computer Science and Engineering at Vellore Institute of Technology. 
> 
> Today, I am defending my project titled **CuraCascade V2: An Integrated Biomedical Informatics Framework for Gene–Disease Evidence Aggregation, Automated Validity Discrepancy Auditing, and Research-Oriented Latency Analytics**.
> 
> The complete software implementation, automated test suite, and benchmark pipelines are publicly available on GitHub at `uditshokeen14/curacascadeV2`, and the interactive audit dashboard is live at `curacascadev2.streamlit.app`.
> 
> In this defense, I will explain why genomic diagnostic databases experience hazardous evidence lags, how CuraCascade automates discrepancy detection with zero false-positive alerts on our evaluable cohort, and what our data reveals about genomic latency kinetics."

- **Examiner Trap Avoidance:** Do not start by discussing machine learning or UI widgets. Start with the core biomedical problem: clinical validity lag.

---

### Slide 2: Executive Summary
- **Time Target:** 00:40 (Running Time: `00:30 – 01:10`)
- **Visual Cue:** Point to the 4 structured quadrants: The Genomic Problem, Our Engineering Solution, Strongest Verified Result, and Honest Scientific Boundary.
- **Key Takeaway:** Deliver the thesis elevator pitch in 40 seconds.

#### Spoken Transcript
> "To summarize this entire investigation in four foundational pillars:
> 
> First, the **Problem**: When expert consortia like ClinGen downgrade or refute an unproven gene–disease association, downstream commercial panels and variant databases like ClinVar do not update synchronously. This leaves thousands of active 'Pathogenic' variant assertions tied to refuted genes.
> 
> Second, our **Solution**: CuraCascade V2 implements an automated, disease-aware audit pipeline that aggregates ClinGen, ClinVar, and PanelApp into a third-normal-form relational warehouse and flags contradictory assertions using ontology-grounded crosswalks.
> 
> Third, our **Strongest Verified Result**: On an independent, firewalled benchmark of 100 gene–disease dyads, CuraCascade achieved 100% precision and 100% specificity across 94 evaluable cases, meaning every single flagged discrepancy was an authentic, verifiable conflict.
> 
> Finally, our **Scientific Boundary**: Our system achieves 34.6% recall because it intentionally refuses to guess when phenotypes are unmapped, prioritizing clinical trust over aggressive alerting."

- **Examiner Trap Avoidance:** Own the 34.6% recall immediately. Mentioning it in Slide 2 proves scientific maturity and disarms aggressive examiners.

---

### Slide 3: The Real-World Problem: Genomic Evidence Drift
- **Time Target:** 00:45 (Running Time: `01:10 – 01:55`)
- **Visual Cue:** Direct attention to the three-step cascade diagram: ClinGen curation (T0) → Downstream lag (T0+2.8 yrs) → Clinical patient risk.
- **Key Takeaway:** ClinGen curates at the gene level, but commercial labs report at the variant level. Because they operate in silos, evidence drifts.

#### Spoken Transcript
> "Let us look at why this problem exists in modern medicine. In clinical genomics, scientific knowledge is not static; it evolves continuously.
> 
> In 2018, ClinGen's international curation expert panels began systematically reviewing historic gene–disease claims. For example, *MYH7* is genuinely causal for hypertrophic cardiomyopathy. However, genes like *MYOZ2* or *CACNA2D1*, which were historically reported in the medical literature as cardiomyopathy genes, were systematically downgraded to 'Definitive Refuted' or 'No Evidence' due to lack of rigorous statistical linkage.
> 
> However, ClinGen curates at the *gene-disease* level, whereas clinical testing laboratories submit interpretations to ClinVar at the individual *variant* level. There is no automated, universal protocol synchronizing these databases.
> 
> As our audit reveals, this creates a median propagation lag of **2.82 years** across the broader genomic ecosystem, and up to **6.0 years** in historic flagship cases. During this latency window, patients receive molecular diagnostic reports containing variants classified as 'Pathogenic' for diseases that the gene does not cause, exposing families to unnecessary surgeries, ICD implantations, and severe psychological distress."

- **Anticipated Viva Question:** *"Why don't clinical labs simply check ClinGen before signing out reports?"*
- **10-Second Response:** *"ClinGen curates only ~2,000 gene-disease dyads so far, and labs query variants in ClinVar programmatically. Without an automated bridge matching phenotypes across ontologies, manual cross-referencing for thousands of variants is clinically unsustainable."*

---

### Slide 4: Biomedical Foundations I: DNA, Genes, and Variants
- **Time Target:** 00:40 (Running Time: `01:55 – 02:35`)
- **Visual Cue:** Gesture to the central dogma diagram (DNA → mRNA → Protein) and the comparison card between benign polymorphisms and pathogenic nonsense/missense mutations.
- **Key Takeaway:** Educate non-specialists on how genetic variants alter amino acids and produce functional abnormalities.

#### Spoken Transcript
> "For non-genomic specialists on the committee, let us establish the biological foundations from first principles.
> 
> The human genome comprises 3.1 billion base pairs of DNA across 23 chromosome pairs, encoding approximately 20,000 protein-coding genes. In cellular transcription and translation, DNA is transcribed into messenger RNA, which is translated into folded functional protein structures.
> 
> Every individual carries 4 to 5 million genetic variations. Most are benign single-nucleotide polymorphisms that represent harmless human diversity. 
> 
> However, a pathogenic variant disrupts the biological product: a nonsense mutation introduces a premature stop codon truncating the protein, while a damaging missense substitution alters a critical catalytic amino acid, causing cellular dysfunction or monogenic disease."

- **Examiner Trap Avoidance:** Keep this slide crisp; do not spend more than 40 seconds unless the committee explicitly requests biological elaboration.

---

### Slide 5: Biomedical Foundations II: Gene Validity vs. Variant Pathogenicity
- **Time Target:** 00:45 (Running Time: `02:35 – 03:20`)
- **Visual Cue:** Emphasize the two contrasting cards: Gene-Level Clinical Validity (ClinGen) versus Variant-Level Pathogenicity (ACMG/ClinVar). Highlight the "Fatal Flaw" warning box at the bottom.
- **Key Takeaway:** Variant pathogenicity is completely conditional on gene-level clinical validity. If the gene does not cause the disease, the variant classification is biologically meaningless.

#### Spoken Transcript
> "Slide 5 represents the central biomedical distinction of this defense: **Gene-Level Clinical Validity versus Variant-Level Pathogenicity**.
> 
> At the **gene level**, ClinGen answers: *'Does variation in Gene X cause Disease Y?'* This is evaluated using Mendelian segregation data, knock-out animal models, and case-control odds ratios, classifying the relationship from 'Definitive' down to 'Refuted' or 'No Reported Evidence'.
> 
> At the **variant level**, the ACMG/AMP framework answers: *'Does this specific nucleotide change alter protein function?'* using criteria like population frequency in gnomAD and in silico structural predictions, classifying variants as Pathogenic, Likely Pathogenic, VUS, Likely Benign, or Benign.
> 
> Here is the critical vulnerability: **Variant pathogenicity is strictly conditional upon gene validity**. If a gene is refuted for Brugada syndrome, classifying a variant within that gene as 'Pathogenic for Brugada syndrome' is a biomedical contradiction. A variant cannot cause a disease if the gene itself does not cause that disease. CuraCascade was engineered specifically to detect and eradicate this exact discrepancy."

---

### Slide 6: The Clinical Data Ecosystem
- **Time Target:** 00:40 (Running Time: `03:20 – 04:00`)
- **Visual Cue:** Point to the 5 ecosystem pillars: ClinGen, ClinVar, PanelApp, gnomAD, and HGNC/MONDO ontologies.
- **Key Takeaway:** Differentiate authoritative facts produced by each public database from CuraCascade's synthesis.

#### Spoken Transcript
> "To understand our data pipeline, we must map the public genomic data ecosystem.
> 
> **ClinGen** serves as the international authority on gene–disease validity and dosage sensitivity.  
> **NCBI ClinVar** is the primary public repository of variant-level clinical interpretations submitted by diagnostic laboratories worldwide.  
> **Genomics England PanelApp** curates crowdsourced virtual gene panels graded by traffic-light confidence: Green for diagnostic grade, Amber for moderate evidence, and Red for unproven genes.  
> **gnomAD** provides population-level allele frequencies across more than 140,000 exomes and genomes to assess evolutionary constraint and rarity.  
> And finally, **HGNC and MONDO** provide standardized nomenclature for gene symbols and disease ontologies.
> 
> CuraCascade ingests these heterogeneous, asynchronous repositories into a single unified analytical schema."

---

### Slide 7: Why Genomic Evidence Disagrees
- **Time Target:** 00:45 (Running Time: `04:00 – 04:45`)
- **Visual Cue:** Walk through the 4 root causes of evidence conflict: Granularity Disconnect, Temporal Asynchrony, Semantic Heterogeneity, and Economic Incentives.
- **Key Takeaway:** Discrepancies are systemic infrastructure failures, not deliberate malpractice by diagnostic laboratories.

#### Spoken Transcript
> "Why do these databases disagree in practice? Our investigation identified four root causes.
> 
> First, **Granularity Disconnect**: ClinGen curates at the dyad level, whereas ClinVar records variant assertions. Labs do not routinely re-evaluate historical variant assertions when gene-level papers are published.
> 
> Second, **Temporal Asynchrony**: Consortia publish periodic curation releases, while variant repositories accept daily continuous submissions, creating temporal drift.
> 
> Third, **Semantic Heterogeneity**: A lab may submit a variant under the broad term *'Cardiovascular phenotype'* (MedGen C0007222), while ClinGen curates against *'Brugada syndrome 1'* (MONDO:0015263). Without ontology crosswalks, standard string comparisons fail completely.
> 
> Fourth, **Economic and Workflow Constraints**: Retrospective variant re-curation is time-intensive and uncompensated for commercial diagnostic laboratories, meaning outdated records linger indefinitely unless flagged by automated tooling."

---

### Slide 8: Existing Workflows & The Research Gap
- **Time Target:** 00:45 (Running Time: `04:45 – 05:30`)
- **Visual Cue:** Focus on the comparison table: Manual ad-hoc querying vs. Variant-only aggregators vs. CuraCascade V2.
- **Key Takeaway:** CuraCascade fills the critical research gap by combining disease-aware cross-database auditing with automated latency analytics.

#### Spoken Transcript
> "When examining existing tools, a clear research gap emerges.
> 
> In conventional clinical practice, variant curators perform manual, ad-hoc literature searches, which cannot scale across hundreds of thousands of variants. Variant-centric platforms like Franklin or Varsome aggregate population frequencies and ACMG scores, but they largely inherit ClinVar's disease annotations without cross-auditing against ClinGen gene-validity curations.
> 
> Conversely, ClinGen's official portal provides validity matrices, but it does not link downstream to active ClinVar variant counts or compute propagation latencies.
> 
> **CuraCascade V2 closes this gap**. It is the first open-source, automated framework that performs bidirectional, disease-aware discrepancy auditing across ClinGen, ClinVar, and PanelApp, while calculating longitudinal evidence latency kinetics and providing an interactive audit workbench."

---

### Slide 9: Project Objectives & System Scope
- **Time Target:** 00:40 (Running Time: `05:30 – 06:10`)
- **Visual Cue:** Contrast the left box (Primary Engineering Objectives) with the right box (Rigorous Non-Goals & Boundaries).
- **Key Takeaway:** Clearly state what CuraCascade achieves while establishing strict ethical and clinical non-goals.

#### Spoken Transcript
> "Our project objectives were defined with strict engineering and ethical boundaries.
> 
> Our **primary objectives** were threefold:
> 1. Ingest, normalize, and reconcile public genomic datasets into an audit-ready relational schema with SHA-256 provenance tracking.
> 2. Build a deterministic, disease-aware rule engine to classify evidence conflicts into Class A refuted-gene assertions, Class B contested evidence, and Class C panel over-inclusions.
> 3. Provide an interactive clinical audit dashboard with automated institutional report generation.
> 
> Equally important are our **Non-Goals**: CuraCascade is **not** an autonomous diagnostic medical device. It does not issue automated variant classifications without human sign-off, it does not replace expert multidisciplinary review, and it does not connect directly to live hospital electronic health records."

- **Examiner Trap Avoidance:** Emphasizing non-goals demonstrates professional maturity and regulatory awareness.

---

### Slide 10: Verified Contributions & Research Questions
- **Time Target:** 00:45 (Running Time: `06:10 – 06:55`)
- **Visual Cue:** Address the three core research questions: RQ1 (Automated detection feasibility), RQ2 (Real-world latency kinetics), RQ3 (Feature-based prioritization).
- **Key Takeaway:** Show how each research question is backed by empirical source code and data.

#### Spoken Transcript
> "We formulated three specific research questions:
> 
> **Research Question 1**: *Can an automated, disease-aware relational engine detect gene–disease evidence discrepancies with zero false positives?*  
> **Contribution**: Yes. We implemented a 3NF relational audit engine backed by ontology crosswalks that achieved 100% precision on our independent 100-case benchmark cohort.
> 
> **Research Question 2**: *What is the empirical propagation latency between ClinGen gene refutations and downstream ClinVar updates?*  
> **Contribution**: Across 51,251 audited findings, we measured a median propagation latency of **2.82 years** (1,030 days), proving that evidence drift is a widespread, multi-year phenomenon.
> 
> **Research Question 3**: *Can machine learning models prioritize high-risk discrepancies based on public metadata features?*  
> **Contribution**: We demonstrated that an ensemble model can achieve an AUROC of 0.857 using 7 metadata features, while explicitly disclosing the limitations of retrospective snapshot evaluation."

---

### Slide 11: End-to-End Processing Workflow
- **Time Target:** 00:45 (Running Time: `06:55 – 07:40`)
- **Visual Cue:** Trace the horizontal 5-stage pipeline: Ingestion → Normalization → Audit Engine → Latency Analytics → Web Application & Export.
- **Key Takeaway:** Walk through the complete data lifecycle from raw TSV/JSON streams to HTML audit dossiers.

#### Spoken Transcript
> "Slide 11 illustrates the end-to-end data processing workflow implemented in CuraCascade V2.
> 
> The pipeline executes in five sequential stages:
> 1. **Ingestion**: Raw TSV, CSV, and JSON data streams are pulled from ClinGen, NCBI ClinVar, and Genomics England PanelApp.
> 2. **Validation and Normalization**: Files are verified using cryptographic SHA-256 checksums, uncompressed, parsed, and mapped to HGNC official gene symbols and MONDO disease identifiers.
> 3. **Relational Storage**: Normalized records are loaded into our SQLite and DuckDB warehouses using ACID-compliant transactions.
> 4. **Deterministic Audit Engine**: The audit engine executes multi-way relational joins and ontology crosswalk queries, categorizing discrepancies into Class A, B, and C findings.
> 5. **Interface and Dossier Generation**: Clinical bioinformaticians explore findings interactively via our Streamlit application and generate ISO 15189-aligned HTML/PDF audit dossiers."

---

### Slide 12: System Architecture & Module Design
- **Time Target:** 00:45 (Running Time: `07:40 – 08:25`)
- **Visual Cue:** Point out the modular structure: Pipeline scripts (`ingest_*.py`, `build_db.py`, `audit_engine.py`) feeding into SQLite/DuckDB, wrapped by `app.py` with multi-page tabs.
- **Key Takeaway:** The architecture is decoupled, stateless, and verifiable, separating ETL batch pipelines from the interactive presentation layer.

#### Spoken Transcript
> "Looking at the system architecture, CuraCascade V2 is organized into strictly decoupled modules.
> 
> The ingestion tier comprises dedicated scripts in the `pipeline/` directory: `ingest_clingen.py`, `ingest_clinvar.py`, and `ingest_panelapp.py`. These modules perform defensive data validation, stripping invalid records and tracking file provenance.
> 
> The storage tier uses a hybrid database strategy: a normalized **SQLite** database optimized for transactional integrity, foreign-key constraints, and UI lookups, paired with **DuckDB** for vectorized, high-performance analytical aggregation across 50,000+ records.
> 
> The application tier, contained in `app.py`, is built on Streamlit with custom CSS design tokens. It provides five interactive modules: the System Dashboard, Audit Findings Explorer, Gene Deep-Dive, Analytics & Latency Hub, and Report Dossier Generator. The architecture is stateless, portable, and runs on both local workstations and cloud containers."

---

### Slide 13: Database Design: 3NF Relational Schema
- **Time Target:** 00:45 (Running Time: `08:25 – 09:10`)
- **Visual Cue:** Highlight the ER diagram: `genes` (primary key `hgnc_id`) as the central hub, linked via 1-to-many foreign keys to `gene_validity`, `clinvar_variants`, `panelapp_genes`, and `audit_findings`. Point to the compound indexes.
- **Key Takeaway:** The schema is fully normalized to Third Normal Form (3NF) to eliminate data redundancy and enforce referential integrity.

#### Spoken Transcript
> "The database design in `curacascade.db` adheres strictly to Third Normal Form (3NF).
> 
> The central entity is the `genes` table, keyed by the immutable `hgnc_id` with a unique constraint on the official `symbol`. 
> 
> Child tables reference `genes.symbol` via explicit `FOREIGN KEY` constraints:
> - `gene_validity` stores ClinGen curations, tracking disease names, MONDO IDs, classification, and assertion dates.
> - `clinvar_variants` stores variant assertions, keyed by `variation_id`, recording clinical significance, review status stars, and last evaluation dates.
> - `audit_findings` stores computed discrepancies, capturing finding class, risk severity, latency days, and remediation recommendations.
> 
> To guarantee sub-10-millisecond query performance on complex multi-way joins, we created compound B-tree indexes, including `idx_cv_gene_sig` on gene symbol and clinical significance, and `idx_findings_class_risk` on audit class and risk level."

- **Anticipated Viva Question:** *"Why use both SQLite and DuckDB instead of PostgreSQL?"*
- **10-Second Response:** *"SQLite provides zero-configuration, embedded ACID reliability for portable clinical distribution, while DuckDB executes columnar vector scans across 50,000 rows in under 15 milliseconds without maintaining a running database server daemon."*

---

### Slide 14: Data Ingestion, Provenance, and Normalization
- **Time Target:** 00:45 (Running Time: `09:10 – 09:55`)
- **Visual Cue:** Showcase the ingestion table showing raw sources, formats, parser techniques, and SHA-256 validation.
- **Key Takeaway:** CuraCascade guarantees end-to-end data provenance and defensive error handling.

#### Spoken Transcript
> "Data ingestion and normalization are engineered for reproducibility and defensive error handling.
> 
> Raw data arrives in varied formats: ClinGen exports nested JSON and tab-delimited files, ClinVar distributes a massive 4.5-gigabyte gzip compressed tab-delimited file, and PanelApp serves a RESTful JSON API.
> 
> To guarantee provenance, every ingested snapshot is hashed using **SHA-256 checksums** and logged in a `data_provenance` audit table alongside record counts and download timestamps.
> 
> During parsing, gene symbols are standardized against HGNC nomenclature to resolve historic aliases and retired symbols. Variant clinical significance strings are normalized into standard tiers, and dates are coerced into ISO 8601 format. Invalid or corrupted lines are safely discarded into error logs rather than poisoning the analytical warehouse."

---

### Slide 15: Disease-Aware Matching vs. Gene-Only Joins
- **Time Target:** 00:50 (Running Time: `09:55 – 10:45`)
- **Visual Cue:** Emphasize the pleiotropy comparison: *MYH7* (Cardiomyopathy vs. Myopathy). Walk through the exact 4-tier matching algorithm code block.
- **Key Takeaway:** Gene-only joins generate catastrophic false positives on pleiotropic genes; disease-aware matching is mandatory.

#### Spoken Transcript
> "Slide 15 addresses the most critical algorithmic challenge in genomic auditing: **Pleiotropy and Disease-Aware Matching**.
> 
> A gene-only join assumes that a gene causes only one disease. This assumption is catastrophically false. Consider *MYH7*: it has a 'Definitive' causal association with hypertrophic cardiomyopathy, but a 'Refuted' or 'Disputed' association with certain distal myopathies. If an audit engine joins strictly on the gene symbol *MYH7*, it would erroneously flag authentic cardiomyopathy variants as refuted!
> 
> CuraCascade solves this using a 4-tier hierarchical disease matching algorithm:
> 1. **Exact MONDO ID matching**: If ontology identifiers match, confidence is 1.0.
> 2. **Crosswalk synonym expansion**: MedGen Concept IDs (CUI) are resolved to MONDO terms via our ontology crosswalk.
> 3. **Normalized Substring Matching**: Standardized lowercase disease strings are compared after stripping clinical stop-words.
> 4. **Broad Phenotype Refusal**: If a variant is annotated under an unmapped, generic term like 'Cardiovascular phenotype', our engine intentionally refuses to guess, assigning an Unmapped status rather than generating a spurious alert."

---

### Slide 16: Live Application Architecture & Navigation
- **Time Target:** 00:40 (Running Time: `10:45 – 11:25`)
- **Visual Cue:** Point to the real screenshot of the live Streamlit dashboard, highlighting the metric cards (36 Genes, 46 ClinVar Variants, 34 Findings, 2,183d Median Latency) and the dark-themed sidebar.
- **Key Takeaway:** Present the verified, working software deployed in production on Streamlit Cloud.

#### Spoken Transcript
> "Slide 16 displays the live implementation of CuraCascade V2, running in production at `curacascadev2.streamlit.app`.
> 
> The application delivers a high-contrast, clinical dark interface engineered using custom CSS design tokens with deep navy backgrounds, teal accents, and amber warning alerts.
> 
> On the left, a persistent sidebar provides real-time system health metrics, database snapshot toggle (switching between the showcase database and the full 51,000-finding corpus), and navigation across five functional modules.
> 
> In the showcase environment shown here, the header cards immediately summarize 36 audited genes, 46 ClinVar variants, 34 detected discrepancy findings, and an uncorrected median latency of 2,183 days, or 5.98 years."

---

### Slide 17: Interactive Audit Findings Explorer
- **Time Target:** 00:45 (Running Time: `11:25 – 12:10`)
- **Visual Cue:** Showcase the live screenshot of the multi-parameter filter bar (Class A/B/C, High/Medium/Low risk) and the expandable finding inspection cards.
- **Key Takeaway:** The UI empowers clinical curators to slice, search, and drill into specific evidence discrepancies in real time.

#### Spoken Transcript
> "In the **Audit Findings Explorer**, curators inspect discrepancies with multi-parameter filtering capabilities.
> 
> Users can filter findings by Audit Class—selecting Class A refuted gene assertions, Class B contested evidence, or Class C panel over-inclusions—as well as Risk Severity and Disease Domain.
> 
> As shown in the screenshot, each discrepancy renders as an expandable card featuring a color-coded status badge, the affected gene and disease dyad, the exact ClinVar assertion, the conflicting ClinGen validity status, and the elapsed latency duration.
> 
> Clicking into an individual finding exposes the complete underlying evidence trail, enabling the bioinformatician to evaluate the biological contradiction within seconds."

---

### Slide 18: Evidence Traceability & Remediation Dossiers
- **Time Target:** 00:45 (Running Time: `12:10 – 12:55`)
- **Visual Cue:** Point out the detailed Evidence Traceability table showing PubMed IDs, submitter names, last evaluation dates, and the green 'Generate Clinical Audit Dossier' button.
- **Key Takeaway:** CuraCascade provides complete clinical governance and generates defensible audit reports for laboratory directors.

#### Spoken Transcript
> "Slide 18 demonstrates our commitment to clinical governance: **Evidence Traceability and Remediation**.
> 
> For every flagged finding, CuraCascade reconstructs the complete evidence chain. Curators can view the primary submitter, review status stars, submission accession (SCV), last evaluation date, and direct hyperlinks to primary PubMed literature.
> 
> Furthermore, the engine generates an actionable, standardized **Remediation Recommendation**. For example, on a Class A refuted assertion, the system issues: *'FLAG FOR RECLASSIFICATION: Downgrade from Pathogenic to VUS or Uncertain, or remove gene from clinical diagnostic gene panel'*.
> 
> Curators can click 'Generate Clinical Audit Dossier' to export an ISO 15189-aligned HTML audit report complete with digital timestamps, finding hashes, and governance sign-off fields."

---

### Slide 19: Deep-Dive Case Study: *RAD50* & *MYOZ2*
- **Time Target:** 00:50 (Running Time: `12:55 – 13:45`)
- **Visual Cue:** Compare the two concrete case studies: *RAD50* (Disputed for Breast Cancer) on the left, and *MYOZ2* (Definitive Refuted for Hypertrophic Cardiomyopathy) on the right.
- **Key Takeaway:** Walk through real, verified clinical cases demonstrating the real-world medical impact of evidence discrepancies.

#### Spoken Transcript
> "To understand the clinical reality of these discrepancies, let us examine two verified case studies from our database.
> 
> On the left is **RAD50** (NM_005732.3:c.2119C>T, Arg707Ter). In ClinGen's 2018 expert panel evaluation, the association between *RAD50* and hereditary breast ovarian cancer syndrome was systematically downgraded to **Disputed / Refuted**. Yet in ClinVar, multiple commercial laboratories maintained active assertions classifying this truncating variant as **Pathogenic**. If included on a hereditary cancer gene panel, a woman harboring this variant could be counseled toward unnecessary prophylactic mastectomy.
> 
> On the right is **MYOZ2** (c.731A>G, p.Lys244Arg). ClinGen refuted its role in Hypertrophic Cardiomyopathy in 2019 due to lack of segregation in large cohorts. Yet ClinVar retained active Pathogenic classifications for over five years. CuraCascade flags both cases with complete provenance, protecting laboratories from issuing misinformed clinical reports."

---

### Slide 20: Benchmark Methodology & Validation Design
- **Time Target:** 00:50 (Running Time: `13:45 – 14:35`)
- **Visual Cue:** Highlight the 100-case cohort breakdown (60 Discrepancy cases, 40 Concordant controls) and the dynamic query architecture. Emphasize the red "Strict Label Firewall" badge.
- **Key Takeaway:** Explain the gold-standard reference labels, independent dynamic evaluation, and firewall eliminating data leakage.

#### Spoken Transcript
> "Slide 20 details the rigorous methodology behind our validation benchmark in `pipeline/validation_benchmark.py`.
> 
> We constructed a curated reference truth set of **100 gene–disease dyads** derived from peer-reviewed literature, ClinGen curation releases, and clinical genetic panel guidelines. The cohort contains 60 known discrepancy cases across cancer, cardiovascular, neurodevelopmental, and metabolic domains, and 40 concordant negative controls.
> 
> We enforced a **Strict Label Firewall**: The benchmark engine executes dynamic relational queries directly against the live database schema. It has zero programmatic access to ground-truth label columns, eliminating label leakage.
> 
> Of the 100 benchmark cases, **94 cases** were evaluable in our database snapshot. Six cases—such as *TSC1* and *SMN1*—were absent from the local snapshot and were transparently excluded from the evaluable cohort analysis."

---

### Slide 21: Quantitative Benchmark Results
- **Time Target:** 00:50 (Running Time: `14:35 – 15:25`)
- **Visual Cue:** Walk through the 2x2 confusion matrix (TP=18, FP=0, FN=34, TN=42) and the metrics table showing Precision 100%, Specificity 100%, Recall 34.6%, and Accuracy 63.8% with Wilson 95% confidence intervals.
- **Key Takeaway:** Present the exact, verified mathematical metrics and explain their clinical significance.

#### Spoken Transcript
> "Slide 21 presents the verified quantitative benchmark results.
> 
> Across the 94 evaluable cases, our confusion matrix yielded:
> - **True Positives**: 18
> - **False Positives**: 0
> - **False Negatives**: 34
> - **True Negatives**: 42
> 
> From these counts, we derived standard diagnostic metrics with Wilson score 95% confidence intervals:
> - **Precision is 100.0%** [95% CI: 82.4% to 100.0%]. When CuraCascade raises an alert, it is guaranteed to be an authentic evidence contradiction.
> - **Specificity is 100.0%** [95% CI: 91.6% to 100.0%]. Concordant controls are never misclassified as discrepancies.
> - **Sensitivity (Recall) is 34.6%** [95% CI: 23.2% to 48.2%].
> - **Overall Accuracy is 63.8%** [95% CI: 53.8% to 72.8%], with a Cohen's kappa concordance of 0.3212.
> 
> In clinical software, false positives destroy clinician trust through alert fatigue. CuraCascade deliberately trades aggressive recall to achieve zero false-positive alerts."

---

### Slide 22: Error Analysis: Dissecting the 34 False Negatives
- **Time Target:** 00:50 (Running Time: `15:25 – 16:15`)
- **Visual Cue:** Point to the breakdown chart of the 34 false negatives: Category 1 (Snapshot Data Absence, 16 cases, 47.1%), Category 2 (Phenotype Granularity Disconnect, 14 cases, 41.2%), and Category 3 (0-Star Uncurated Noise, 4 cases, 11.8%).
- **Key Takeaway:** Explain that false negatives are caused by external database boundaries and conservative ontology matching, not software bugs.

#### Spoken Transcript
> "A defense is only as credible as its error analysis. In Slide 22, we dissect exactly why 34 benchmark discrepancies were missed by the automated engine.
> 
> **Category 1 (16 cases, 47.1%)**: The local ClinVar snapshot contained zero active Pathogenic or Likely Pathogenic variants for that specific gene-disease dyad at the time of download. The engine cannot flag a variant that is not in the ingested database.
> 
> **Category 2 (14 cases, 41.2%)**: Phenotype granularity disconnect. In genes like *MYOZ2* and *CAV3*, submitters labeled variants under broad terms such as 'Cardiovascular phenotype'. Because our ontology crosswalk refused to guess without explicit linkage to 'Hypertrophic cardiomyopathy', the engine safely withheld an alert.
> 
> **Category 3 (4 cases, 11.8%)**: Variants had zero-star review status or conflicting submissions where classifications neutralized each other.
> 
> This proves that our 34.6% recall is not an algorithmic bug, but the expected result of conservative ontology thresholds and snapshot boundaries."

---

### Slide 23: Machine Learning Triage & Latency Analytics
- **Time Target:** 00:50 (Running Time: `16:15 – 17:05`)
- **Visual Cue:** Direct attention to the ROC curve (AUROC 0.857), feature importance chart (Review Status Stars 0.32, Submitter Count 0.24, In Silico 0.18), and the prominent "Retrospective Evaluation & Leakage Disclosure" callout.
- **Key Takeaway:** Demonstrate ML exploratory triage while openly disclosing the temporal leakage of snapshot evaluation.

#### Spoken Transcript
> "Slide 23 covers our exploratory machine learning pipeline in `pipeline/ml_evaluator.py`.
> 
> We trained a Balanced Random Forest classifier on 7 engineered metadata features to prioritize which variant assertions are at highest risk of future reclassification.
> 
> The model achieved an **AUROC of 0.857** and a Brier score of 0.1508 on a 20% held-out test split. The most predictive features were ClinVar Review Status Stars (0.32 importance weight), Total Submitter Count (0.24), and In Silico Damaging Consensus (0.18).
> 
> However, we maintain strict scientific integrity regarding its evaluation: **This model was trained on a cross-sectional 2024/2026 snapshot, not historically reconstructed pre-downgrade databases**. Therefore, features contain retrospective temporal leakage. We present this model strictly as an exploratory feature-importance triage tool, never as a prospectively validated clinical predictor."

- **Examiner Trap Avoidance:** Proactively acknowledging temporal leakage before an examiner catches it demonstrates top-tier scientific training.

---

### Slide 24: Engineering Rigor, Reproducibility, and Roadmap
- **Time Target:** 00:45 (Running Time: `17:05 – 17:50`)
- **Visual Cue:** Highlight the verification badge (47/47 pytest suite passing in 54s), SQLite/DuckDB storage metrics, and the three-phase future roadmap.
- **Key Takeaway:** Prove that the software engineering meets professional standards with comprehensive test coverage and reproducible architecture.

#### Spoken Transcript
> "Engineering rigor and scientific reproducibility are central to CuraCascade V2.
> 
> Our automated test suite, executed via `pytest`, contains **47 comprehensive unit and integration tests** covering database schemas, foreign-key constraints, ingestion parsers, ontology matching, and benchmark calculations. All 47 tests pass in 54 seconds on Python 3.13 with zero failures.
> 
> Storage is highly optimized: `curacascade.db` requires only 136 KB for showcase deployments, while `curacascade_full.db` scales to 51,251 findings across 3,033 genes in 48 MB, querying in under 15 milliseconds.
> 
> Our future engineering roadmap includes:
> - Integrating live ClinGen GraphQL API webhooks for real-time alerting.
> - Incorporating the LLM-assisted semi-automated curation workflow outlined in our IEEE report.
> - Expanding the ontology crosswalk to Human Phenotype Ontology (HPO) terms for automated patient chart matching."

---

### Slide 25: Conclusion & Project Defense Summary
- **Time Target:** 00:40 (Running Time: `17:50 – 18:30`)
- **Visual Cue:** Point to the final summary card, GitHub repository URL, and live Streamlit demo URL. Invite questions from the committee.
- **Key Takeaway:** Deliver an authoritative closing statement and open the floor for viva examination.

#### Spoken Transcript
> "In conclusion:
> 
> CuraCascade V2 demonstrates that genomic evidence discrepancies are measurable, persistent, and clinically consequential—manifesting a median propagation lag of 2.82 years across 51,000 assertions.
> 
> We have engineered a 3NF relational framework and ontology-aware audit engine that achieves **100% precision and zero false-positive alerts** on evaluable benchmark cases, supported by 47 automated tests, a live cloud deployment, and reproducible open-source code.
> 
> I invite the committee to inspect the source code on GitHub at `uditshokeen14/curacascadeV2` and test the live application at `curacascadev2.streamlit.app`.
> 
> Thank you for your time and attention. I am now ready to take your questions."

---

## 🛡️ Quick-Reference Timing Summary

| Section | Slides | Topic | Start Time | End Time | Target Duration |
|---|---|---|---|---|---|
| **Section A** | 1–5 | Foundations & Problem | 00:00 | 03:20 | 3 min 20 s |
| **Section B** | 6–10 | Ecosystem, Gap & Scope | 03:20 | 06:55 | 3 min 35 s |
| **Section C** | 11–15 | Architecture & Logic | 06:55 | 10:45 | 3 min 50 s |
| **Section D** | 16–19 | Live App & Case Studies | 10:45 | 13:45 | 3 min 00 s |
| **Section E** | 20–23 | Benchmark & Analytics | 13:45 | 17:05 | 3 min 20 s |
| **Section F** | 24–25 | Engineering & Defense | 17:05 | 18:30 | 1 min 25 s |
| **Total** | **25 Slides** | **Full Academic Defense** | **00:00** | **18:30** | **~18 Minutes** |
