# CuraCascade: Academic Defense & Presentation Guide

**Project Title:** CuraCascade: An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades  
**Lead Author & Architect:** Udit Shokeen  
**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, Tamil Nadu, India  
**Target Audience:** Professor & Classmates (Project Evaluation / Defense / Class Seminar)  
**Deliverables:**
- **PowerPoint Presentation:** [`CuraCascade_Presentation.pptx`](file:///h:/Projects/curacascade/CuraCascade_Presentation.pptx) (20 Slides, 16:9 Widescreen, Embedded Figures, Speaker Notes)
- **Interactive Web Slides:** [`CuraCascade_Presentation.html`](file:///h:/Projects/curacascade/CuraCascade_Presentation.html) (Keyboard navigable, Fullscreen mode, Toggleable notes)
- **Publication PDF Report:** [`CuraCascade_Publication_Report.pdf`](file:///h:/Projects/curacascade/CuraCascade_Publication_Report.pdf) (15-Page Academic Manuscript with Figures & Bibliography)
- **Live Interactive Portal:** [curacascade.streamlit.app](https://curacascade.streamlit.app)
- **Open-Source Repository:** [github.com/uditshokeen14/curacascade](https://github.com/uditshokeen14/curacascade)

---

## ⏱️ Recommended Timing Breakdown (15-Minute Defense + 5-Minute Q&A)

| Section | Slides | Focus | Recommended Time |
| :--- | :--- | :--- | :---: |
| **I. Motivation & Clinical Stakes** | Slides 1–5 | Background, The Knowledge Cascade Lag, Patient Case Studies | 3.5 minutes |
| **II. System Architecture & Relational Design** | Slides 6–9 | 4 Pillars, 3NF SQLite + DuckDB, Audit Taxonomy, gnomAD MCAF | 4.0 minutes |
| **III. Analytical & Machine Learning Engines** | Slides 10–13 | Cox Survival Kinetics, Random Forest Triage, Dual-Regime Results, 100-Gene Benchmark | 4.5 minutes |
| **IV. Software Engineering, Compliance & Roadmap** | Slides 14–20 | Headless CLI & CI/CD, Streamlit UI, ISO 15189 Dossiers, Limitations, Conclusions & Q&A | 3.0 minutes |
| **Total Presentation Time** | **20 Slides** | — | **15.0 minutes** |

---

## 🎙️ Slide-by-Slide Presenter Script & Talking Points

### Slide 1: Title & Project Overview (Dark Theme)
- **Slide Headline:** CuraCascade: An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades
- **Presenter Speaking Script:**
  > "Good morning, respected Professor and dear classmates. Today, I am proud to present **CuraCascade**—an open-source clinical genomics data warehouse, automated audit engine, and machine-learned triage framework designed to resolve a critical, silent failure mode in modern clinical medicine: unpropagated gene-disease evidence downgrades.
  >
  > Over the next 15 minutes, I will walk you through the biological problem, our 3NF database architecture, the longitudinal latency kinetics we discovered, our machine learning triage engine, and the empirical validation benchmark. Let's begin with the clinical motivation."

---

### Slide 2: Executive Summary & The Problem at a Glance
- **Key Metrics on Slide:**
  - `3.2 Years` Median Latency before downstream retraction
  - `51,251` Materialized Discrepancies flagged across genome-wide warehouse
  - `96.3%` Automated Join Precision (PPV) against expert adjudication
  - `AUROC 0.857` Supervised ML prediction of impending gene downgrades
- **Presenter Speaking Script:**
  > "To appreciate the significance of this project, consider this: when an expert consortium like ClinGen proves that a gene does NOT cause a disease, it takes an average of 3.2 years before clinical databases reflect that reality.
  >
  > During those 3.2 years, genetic testing laboratories continue to classify mutations in those invalid genes as 'Pathogenic'. In our genome-wide warehouse, we identified over 51,000 unpropagated discrepancies. CuraCascade is an end-to-end bioinformatics engine that achieves 96.3% join precision to catch these errors automatically, and deploys machine learning with an AUROC of 0.857 to forecast which genes will be downgraded next."

---

### Slide 3: Clinical Genomics Background & Upstream Curation
- **Core Concepts:**
  - Candidate-gene era (1990s–2000s) lacked population controls (gnomAD), publishing spurious associations.
  - ClinGen established standardized Gene Curation Expert Panels (GCEPs) scoring evidence into 6 tiers: *Definitive*, *Strong*, *Moderate*, *Limited*, *Disputed*, *Refuted*.
  - Landmark reappraisals showed up to 40% of historically tested cardiomyopathy genes lacked validity.
- **Presenter Speaking Script:**
  > "Before diving into software, we must understand the biological context. In the 1990s and early 2000s, hundreds of genes were linked to human disease based on small family studies. Scientists didn't have reference population databases like gnomAD, so naturally benign polymorphisms were mistakenly labeled as disease-causing mutations.
  >
  > To fix this, the NIH-funded Clinical Genome Resource (ClinGen) established Gene Curation Expert Panels. They evaluate gene validity on a standardized point matrix into categories: Definitive, Moderate, Limited, Disputed, and Refuted.
  >
  > Remarkably, systematic reappraisals revealed that up to 40% of genes historically screened on cardiomyopathy and arrhythmia panels should actually be downgraded to Disputed or Refuted!"

---

### Slide 4: The Core Problem: The "Knowledge Cascade" Synchronization Lag
- **Visual:** Figure 1 (Embedded vector diagram of the asynchronous evidence flow)
- **Presenter Speaking Script:**
  > "Now, why does this problem exist? Look at the diagram on the right, which is Figure 1 from our publication.
  >
  > At the top, we have the expert consortium level—ClinGen GCEPs re-appraise a gene and publish a downgrade. But biomedical informatics is decentralized. There are no automated push notifications or webhook architectures connecting ClinGen to NCBI ClinVar or Genomics England PanelApp.
  >
  > As a result, NCBI ClinVar continues to report Pathogenic variants in that gene, and diagnostic exome panels continue to test for it. When an NGS pipeline runs, automated software pulls these assertions and prints out a clinical report diagnosing a healthy individual with a fatal genetic condition. The median duration of this disconnect is 3.2 years."

---

### Slide 5: Real-World Clinical Harm & Patient Case Studies
- **Case Studies Highlighted:**
  - *MYLK2* & *TCAP*: Refuted in Hypertrophic Cardiomyopathy $\to$ Inappropriate surgical Implantable Cardioverter Defibrillator (ICD) implants.
  - *SCN1B* & *KCNE2*: Disputed in Brugada syndrome / Long QT $\to$ Traumatic cascade testing across healthy children and relatives.
  - *NBN* & *RAD50*: Limited in Breast/Ovarian Cancer $\to$ Premature diagnostic closure; patients undergoing unnecessary prophylactic mastectomies.
  - Accumulation of "Patient-Years at Risk".
- **Presenter Speaking Script:**
  > "Let me ground this in real-world clinical consequences. This is not just a theoretical database discrepancy.
  >
  > Consider MYLK2. In 2018, ClinGen formally refuted MYLK2 as a cause of hypertrophic cardiomyopathy. Yet for years, ClinVar retained Pathogenic assertions. Cardiologists who trusted ClinVar misdiagnosed asymptomatic individuals with HCM, recommending surgical implantation of defibrillators.
  >
  > In SCN1B and Brugada syndrome, false-positive reports triggered cascade screening—subjecting healthy children and relatives to invasive electrophysiology tests and severe psychological anxiety. When we multiply this across all diagnostic gene panels, we calculate hundreds of thousands of 'patient-years at risk'."

---

### Slide 6: CuraCascade Solution Architecture: Four Core Pillars
- **Overview of 4 Pillars:**
  1. 3NF Relational Data Warehouse (Multi-source ingestion, SQLite + DuckDB)
  2. Deterministic Audit Engine (Classes A, B, C; POSIX exit codes)
  3. Longitudinal Latency Kinetics (Kaplan-Meier & Cox Proportional Hazards)
  4. Supervised ML Triage Forecaster (Balanced Random Forest vulnerability queue)
- **Presenter Speaking Script:**
  > "To solve this systemic challenge, we architected CuraCascade around four engineering pillars:
  >
  > Pillar 1 is our 3NF Relational Warehouse. It integrates multi-source genomic repositories and pairs transactional SQLite with high-performance DuckDB columnar scanning.
  >
  > Pillar 2 is our Deterministic Audit Engine. It runs formal heuristic rules that classify discrepancies into Classes A, B, and C, outputting POSIX status codes for automated CI/CD pipeline blocking.
  >
  > Pillar 3 is our Longitudinal Survival Kinetics framework. Using Kaplan-Meier curves and Cox regression, we mathematically quantify how long it takes for discrepancies to resolve.
  >
  > Pillar 4 is our Supervised Machine Learning Forecaster. Rather than just waiting for errors to happen, our Random Forest model flags currently supported genes that are biologically primed for an imminent downgrade."

---

### Slide 7: 3NF Relational Warehouse Architecture
- **Visual:** Figure 2 (Normalized schema graph & table relationships)
- **Technical Highlights:**
  - 5 core tables (`genes`, `diseases`, `clingen_curations`, `clinvar_variants`, `panelapp_entries`) + 2 materialized tables (`audit_findings`, `downgrade_risk_predictions`).
  - Third Normal Form (3NF) eliminating redundancy with strict foreign key cascading.
  - Dual-engine design: Transactional SQLite for writes and CLI; in-memory DuckDB columnar scanner for zero-copy vectorized aggregation across 50,000+ variants.
- **Presenter Speaking Script:**
  > "Slide 7 showcases our database engineering architecture, illustrated in Figure 2 on the right.
  >
  > We designed a normalized Third Normal Form schema. The central hub is the 'genes' entity, connected via primary-to-foreign keys to 'diseases', 'clingen_curations', 'clinvar_variants', and 'panelapp_entries'.
  >
  > One novel technical feature is our Dual-Engine design: For transactions, updates, and CLI scripts, we use standard SQLite with write-ahead logging and strict foreign keys. But when we need to run analytical cohort queries across 50,000 variants, we dynamically mount an in-memory DuckDB engine. DuckDB executes vectorized columnar aggregations directly on SQLite tables with zero-copy overhead, reducing query times from seconds to single-digit milliseconds."

---

### Slide 8: Audit Classification Taxonomy & Heuristics
- **Visual:** Figure 3 (Audit taxonomy decision tree)
- **Formal Predicates:**
  - **Class A (`CRITICAL`):** $(\text{ClinGen} \in \{\text{Disputed}, \text{Refuted}\}) \land (\text{ClinVar } \text{is\_plp} = 1)$
  - **Class B (`HIGH`):** $(\text{ClinGen} = \text{Limited}) \land (\text{ClinVar } \text{is\_plp} = 1)$ (Violates ACMG VUS ceiling)
  - **Class C (`CRITICAL`):** $(\text{ClinGen} \in \{\text{Disputed}, \text{Refuted}\}) \land (\text{PanelApp} = \text{Green})$
- **Presenter Speaking Script:**
  > "In Slide 8, we present our audit classification taxonomy, illustrated in Figure 3. Rather than treating all discrepancies equally, CuraCascade establishes three formal tiers based on clinical actionability:
  >
  > Class A is marked CRITICAL. This occurs when ClinVar asserts a variant is Pathogenic in a gene that ClinGen proved is Disputed or Refuted. This is an acute medical hazard because a patient will receive a definitive genetic diagnosis for a gene that does not cause the disease.
  >
  > Class B is marked HIGH. Here, ClinGen rates the gene as Limited evidence, but ClinVar still reports Pathogenic variants. This violates the ACMG guideline, which explicitly states that in a Limited gene, variants must be capped at Variant of Uncertain Significance (VUS).
  >
  > Class C is also CRITICAL. It flags diagnostic panel registries like Genomics England PanelApp that still maintain 'Green' diagnostic-grade tiering for refuted genes. This causes high-throughput automated exome pipelines to flag discredited genes on routine patient runs."

---

### Slide 9: Population Genetics & MCAF Ceiling Filter (gnomAD v4)
- **Formulas & Standards:**
  - $\text{MCAF}_{\text{Dominant}} = \frac{I \cdot h}{2 \cdot P}, \quad \text{MCAF}_{\text{Recessive}} = \sqrt{\frac{I \cdot h}{P}}$
  - Popmax continental frequency in gnomAD v4 (AFR, AMR, EAS, NFE, SAS).
  - Automated invocation of ACMG Rule **BA1** ($>5\%$) and **BS1** (exceeds disease frequency ceiling).
- **Presenter Speaking Script:**
  > "Slide 9 demonstrates how CuraCascade incorporates population genetics to validate and refute clinical claims.
  >
  > We implemented the statistical framework of Whiffin et al. (2017) to compute the Maximum Credible Allele Frequency, or MCAF. If a disease has a prevalence of 1 in 500, simple population genetics dictates that no single pathogenic mutation can exceed a specific mathematical frequency ceiling in gnomAD.
  >
  > CuraCascade annotates every ClinVar variant with gnomAD v4 Popmax frequencies. If a supposed 'Pathogenic' mutation exceeds MCAF, CuraCascade triggers ACMG Rule BS1, or Rule BA1 if it exceeds 5%. This provides independent, orthogonal proof that the downstream assertion is invalid, eliminating ancestry-related misclassification."

---

### Slide 10: Longitudinal Latency & Survival Kinetics
- **Visual:** Figure 4 (Kaplan-Meier survival curves & Cox hazard ratios forest plot)
- **Key Findings:**
  - Review Star Accelerator: $\ge 2$ stars resolves **2.36x faster** ($\text{HR} = 2.36$, $p < 0.001$).
  - Commercial Laboratory Penalty: Commercial labs resolve at **nearly half the rate** of academic centers ($\text{HR} = 0.55$, $p < 0.001$).
  - Concordance Index ($C$-index) = 0.724.
- **Presenter Speaking Script:**
  > "Slide 10 presents our survival analysis and Cox Proportional Hazards regression, shown in Figure 4.
  >
  > We treated assertion retraction as a time-to-event survival problem. Panel A shows our Kaplan-Meier curves, and Panel B displays our Cox Hazard Ratios. The concordance index was 0.724.
  >
  > Two critical operational findings emerged: First, the 'Review Star Accelerator': variants with 2 or more ClinVar stars resolve 2.36 times faster. Laboratories actively monitor multi-star submissions, while 0-star submissions are often neglected.
  >
  > Second, what we term the 'Commercial Laboratory Latency Penalty': commercial testing labs exhibit a Hazard Ratio of 0.55. They resolve discrepancies at half the rate of academic medical centers. Why? Because retracting an assertion in a commercial lab carries legal liabilities, requiring them to issue amended reports to ordering physicians."

---

### Slide 11: Machine-Learned Downgrade Triage Framework
- **Technical Specifications:**
  - 7 Engineered Features: Curation Age, Total Variants, P/LP Count, Low-Star Ratio, gnomAD Popmax AF, MCAF Violation Rate, PanelApp Amber/Red Count.
  - Balanced Random Forest (100 estimators, max depth 5, inverse class weighting) vs Balanced Logistic Regression.
  - Strict Temporal Split: Train on curations evaluated before Jan 1, 2021; Test on curations evaluated on/after Jan 1, 2021 (no temporal data leakage).
- **Presenter Speaking Script:**
  > "In Slide 11, we transition from reactive auditing to predictive forecasting. Can we predict which genes currently rated as Definitive or Moderate will be downgraded in the future?
  >
  > To answer this, we engineered 7 biologically grounded features across ClinGen, ClinVar, PanelApp, and gnomAD. We deployed a Balanced Random Forest with inverse class weighting.
  >
  > Crucially, to prevent temporal data leakage, we enforced a strict temporal validation split: the model was trained only on curations evaluated before January 1, 2021, and tested on curations evaluated on or after that date. The model outputs a calibrated risk score that ranks genes into an actionable clinical triage queue."

---

### Slide 12: Empirical Results: Dual-Regime ML Reporting
- **Visual:** Figure 5 (Dual ROC curves & feature importance comparison)
- **Dual Regimes:**
  - Positive Control Benchmark ($N = 34$): $\text{AUROC} = 1.000$, $\text{Precision@Top-20\%} = 100\%$, Curation Age = 78.4%.
  - Genome-Wide Empirical Corpus ($N = 3,833$ genes, $51,025$ variants): $\text{AUROC} = 0.857$, $\text{PR-AUC} = 0.814$, $\text{Precision@Top-20\%} = 75.8\%$.
  - Mechanistic Feature Shift: Age drops to $<1\%$, replaced by Low ClinVar Star Density (70.2%) and PanelApp Discordance (26.0%).
- **Presenter Speaking Script:**
  > "Slide 12 highlights one of the most intellectually honest aspects of our research, shown in Figure 5.
  >
  > In academic machine learning, papers often boast 1.0 AUROC without acknowledging that their benchmark was an artificial toy dataset. In CuraCascade, we explicitly report two distinct regimes:
  >
  > On our positive control benchmark of 34 historical landmark genes, the model achieves a perfect AUROC of 1.000. But we explicitly explain in our manuscript that this is a linearly separable sanity check where Curation Age accounts for 78.4% of the signal.
  >
  > When we scale to the unfiltered genome-wide corpus of 3,833 genes, the model achieves an AUROC of 0.857. Crucially, a dramatic mechanistic feature shift occurs: Curation Age drops, and predictive power is dominated by Low ClinVar Star Density (70.2%) and PanelApp disagreement (26.0%). This reflects the biological reality of how discredited genes behave."

---

### Slide 13: Gold-Standard Validation Benchmark
- **Visual:** Figure 6 (Confusion matrix & performance metrics)
- **Validation Metrics:**
  - $N = 100$ genes (54 true published downgrades, 46 definitive disease controls).
  - Precision (PPV) = 96.3%
  - Recall (Sensitivity) = 96.3%
  - Specificity = 95.7%
  - Cohen's Kappa ($\kappa = 0.920$) against blinded manual expert adjudication.
- **Presenter Speaking Script:**
  > "Slide 13 presents our clinical validation benchmark against blinded expert adjudication, shown in Figure 6.
  >
  > To verify that CuraCascade's automated SQL joins and heuristic logic don't produce false alarms, we compiled a gold-standard cohort of 100 genes—54 published downgrades and 46 definitive controls across heart disease, cancer, and neurology.
  >
  > Against manual clinical adjudication:
  > - Automated Join Precision was 96.3%
  > - Sensitivity was 96.3%
  > - Specificity was 95.7%
  > - And Cohen's Kappa coefficient was 0.920, representing near-perfect concordance.
  >
  > This proves that CuraCascade can operate safely as an automated clinical audit firewall in a hospital setting."

---

### Slide 14: Software Engineering, Headless CLI & CI/CD
- **Technical Highlights:**
  - Headless CLI (`run.py audit`, `run.py verify`, `run.py serve`).
  - POSIX Exit Status Codes: `0` (Clean), `1` (Critical Class A, halts pipeline), `2` (Error).
  - GitHub Actions automated regression workflow (`.github/workflows/audit_ci.yml`).
  - Comprehensive Pytest suite (`test_cli.py`, `test_dossier.py`).
  - Docker containerization for zero-dependency deployment.
- **Presenter Speaking Script:**
  > "Slide 14 demonstrates our commitment to software engineering best practices.
  >
  > CuraCascade is not just a collection of scripts; it is an enterprise CLI tool with strict POSIX exit code conventions: Exit 0 indicates a clean audit. Exit 1 indicates that unpropagated Class A findings were detected, which immediately halts any automated build or sequencing run. Exit 2 indicates an internal database failure.
  >
  > Our GitHub Actions CI/CD pipeline runs `test_cli.py` and `test_dossier.py` on every commit, verifying foreign-key constraints and cryptographic checksums. Finally, the entire application is containerized with Docker, packaging the database, engine, and web interface into an immutable image."

---

### Slide 15: Clinical Decision Support & Interactive Web Portal
- **8 Integrated Clinical Modules:**
  - Modules 1 & 2: Executive KPIs & Custom Multi-Gene Audit Portal
  - Modules 3 & 4: Inconsistency Explorer & gnomAD MCAF Population Genetics
  - Modules 5 & 6: ML Triage Queue & Longitudinal Survival Analytics
  - Modules 7 & 8: Clinical Governance Dossier Generator & Validation Benchmark
- **Presenter Speaking Script:**
  > "Slide 15 highlights our clinical decision support portal, deployed live at curacascade.streamlit.app.
  >
  > The dashboard is organized into 8 modular clinical interfaces:
  > - Modules 1 and 2 give laboratory directors immediate KPI metrics and allow them to paste arbitrary gene lists for real-time audit.
  > - Modules 3 and 4 allow deep exploration of ClinVar variant IDs, ClinGen panel URLs, and gnomAD popmax frequencies.
  > - Modules 5 and 6 visualize our machine learning triage rankings and interactive Kaplan-Meier survival curves.
  > - Modules 7 and 8 provide one-click exports of formal clinical governance dossiers and live benchmark concordance metrics."

---

### Slide 16: Clinical Governance & Standardized Remediation Dossiers
- **Compliance & Standards:**
  - ISO 15189:2022 Section 7.3, CAP, and CLIA requirements for diagnostic test validity.
  - 6-Section Remediation Dossier: Header Directive, Consensus Metadata, Orthogonal Population Genetics, Downstream Assertions Catalog, ACMG Rule BA1/BS1 Remediation Checklist, Formal Sign-Off Attestation.
- **Presenter Speaking Script:**
  > "Slide 16 shows how CuraCascade bridges computation and regulatory compliance.
  >
  > Under ISO 15189:2022 Section 7.3, CLIA, and CAP standards, clinical laboratories are legally required to verify that their diagnostic panels remain scientifically valid.
  >
  > When an audit flags a Class A inconsistency, laboratory directors face an administrative headache: drafting remediation notices. To solve this, CuraCascade automatically compiles a 6-Section Clinical Governance Dossier:
  > It documents the ClinGen consensus, provides orthogonal gnomAD proof, catalogs all affected ClinVar variation IDs, gives a step-by-step ACMG de-escalation checklist invoking Rules BA1 and BS1, and ends with formal signature sign-off blocks for the laboratory medical director."

---

### Slide 17: Critical Discussion, Limitations & Ethics
- **Key Realities:**
  - Commercial lab latency penalty (legal liability, cost of amending patient reports).
  - Ontology crosswalk complexity (MONDO vs OMIM vs MedGen).
  - Ethical human-in-the-loop philosophy (advisory decision support, not autonomous record deletion).
- **Presenter Speaking Script:**
  > "In Slide 17, we critically discuss limitations and ethical considerations:
  >
  > First, commercial laboratory inertia: our survival analysis proved commercial labs lag behind academic centers. This is driven by legal and operational friction—issuing amended reports is expensive and legally delicate.
  >
  > Second, ontology harmonization: mapping MONDO to OMIM and MedGen is challenging because phenotypic boundaries in rare disease are complex.
  >
  > Third, our ethical framework: CuraCascade is explicitly built with a human-in-the-loop philosophy. The machine learning model and audit rules serve as an advisory decision support firewall—they never autonomously delete clinical records without the oversight and signature of a board-certified clinical molecular geneticist."

---

### Slide 18: Future Directions & System Roadmap
- **Three Strategic Horizons:**
  - Horizon 1: Real-time event-driven webhook architecture (Kafka/RabbitMQ) for sub-hour synchronization.
  - Horizon 2: Local LLM-assisted literature curation to summarize contradictory functional assays from PubMed.
  - Horizon 3: HL7 FHIR Genomics API integration with hospital EHRs (Epic, Cerner) and LIMS.
- **Presenter Speaking Script:**
  > "Looking toward future research horizons in Slide 18:
  >
  > Horizon 1 is real-time webhook streaming: replacing monthly batch flat-file dumps with event-driven webhooks so discrepancies are caught in minutes rather than months.
  >
  > Horizon 2 is LLM-assisted curation: using privacy-preserving local language models to parse PubMed literature and summarize newly discovered contradictory functional assays.
  >
  > Horizon 3 is hospital EHR and HL7 FHIR integration: connecting CuraCascade directly into hospital LIMS systems like Epic and Cerner to halt invalid reports at the diagnostic sign-out stage."

---

### Slide 19: Conclusion & Summary of Contributions
- **Four Core Contributions Recapitulated:**
  1. Unified 3NF Warehouse with dual SQLite/DuckDB engines.
  2. Longitudinal Survival Kinetics (3.2-year median lag, commercial lab penalty).
  3. Supervised ML Triage Model (AUROC 0.857) with honest dual-regime reporting.
  4. Production software suite (96.3% precision, CI/CD gates, Docker, Streamlit cloud portal).
- **Presenter Speaking Script:**
  > "In conclusion, CuraCascade delivers four major contributions:
  > 1. A 3NF clinical genomics warehouse harmonizing 4 major international databases with dual SQLite/DuckDB engines.
  > 2. The first time-to-event survival model quantifying evidence lag, uncovering a 3.2-year median delay and a commercial lab penalty.
  > 3. A supervised machine learning forecaster achieving an AUROC of 0.857 to triage impending gene downgrades.
  > 4. And a production-grade clinical software suite achieving 96.3% precision, with CI/CD gates, Docker containerization, and a live web dashboard.
  >
  > This framework transforms genomic quality control from sporadic, manual guesswork into an automated, continuous firewall."

---

### Slide 20: Q&A, Project Links & Acknowledgments (Dark Theme)
- **Links & Contact:**
  - Live Web App: `https://curacascade.streamlit.app`
  - GitHub Repository: `https://github.com/uditshokeen14/curacascade`
  - Publication PDF Report: `CuraCascade_Publication_Report.pdf`
- **Presenter Speaking Script:**
  > "Thank you very much for your time, attention, and interest. 
  >
  > The live cloud portal is running at curacascade.streamlit.app, the full open-source codebase is on GitHub, and our complete 15-page publication PDF report is compiled and available for inspection.
  >
  > I would now be delighted to answer any questions from the Professor and my classmates. Thank you!"

---

## 🎯 Anticipating the Professor's Toughest Defense Questions (Top 10 Q&A)

Here are the exact questions professors and evaluators love to ask, along with the precise, high-scoring responses:

### Q1: "Why did you use SQLite and DuckDB instead of an enterprise client-server database like PostgreSQL?"
> **Your Answer:**  
> "Excellent question, Professor. We chose a dual SQLite + DuckDB architecture based on clinical informatics constraints and zero-daemon deployment:
> 1. **Client-side zero-daemon footprint:** Diagnostic laboratories and academic research environments frequently operate under strict IT governance where provisioning background server daemons (like PostgreSQL) requires lengthy security reviews. SQLite embeds directly inside the application, enabling zero-configuration Docker containerization.
> 2. **Transactional ACID integrity:** SQLite provides strict foreign-key verification (`PRAGMA foreign_keys = ON`), write-ahead logging, and robust transaction isolation for point lookups.
> 3. **Analytical Columnar Performance via DuckDB:** For heavy analytical aggregations across 50,000+ variants, traditional relational databases can be slow. DuckDB attaches directly to SQLite files via its zero-copy scanner (`ATTACH 'curacascade.db' AS db (TYPE SQLITE)`), providing SIMD-vectorized columnar execution in memory. This gives us the simplicity of SQLite with the analytical speed of Snowflake or ClickHouse."

### Q2: "How did you prevent data leakage in your machine learning models?"
> **Your Answer:**  
> "We implemented a strict **Temporal Validation Split**. In clinical evidence curation, using standard random $K$-fold cross-validation introduces severe temporal data leakage because a future curation might leak information into an earlier curation of the same gene family.
> 
> Therefore, we trained our models exclusively on gene-disease evaluations conducted prior to January 1, 2021, and tested them on evaluations conducted on or after January 1, 2021. This strictly simulates real-world prospective deployment, ensuring the model never sees future consortium consensus during training."

### Q3: "Why did your model score an AUROC of 1.000 on the benchmark but 0.857 on the genome-wide corpus?"
> **Your Answer:**  
> "This is one of the key scientific insights we highlight in our manuscript:
> 
> On our $N=34$ benchmark, the cohort consisted of historical landmark positive controls (like *SCN1B* and *MYLK2*) versus definitive controls (like *BRCA1* and *MYH7*). In this setting, the positive controls were evaluated years earlier, making **Curation Age account for 78.4% of the signal**. We explicitly report this as a linearly separable sanity verification.
> 
> When we scale to the unfiltered genome-wide corpus of 3,833 genes, Curation Age drops to under 1% of importance, and predictive power transitions to **Low ClinVar Star Density (70.2%)** and **PanelApp Disagreements (26.0%)**. In the real world, impending downgrades are signaled by fragmented assertion quality and curator skepticism, not simply elapsed time. Dual-regime reporting ensures academic honesty."

### Q4: "What is MCAF and why can't laboratories just use gnomAD allele frequencies directly?"
> **Your Answer:**  
> "Simply observing a variant in gnomAD is not enough; we need to know the *mathematical ceiling* for a specific disease indication. 
> 
> Based on the statistical genetics framework of Whiffin et al. (2017), MCAF calculates the Maximum Credible Allele Frequency using disease prevalence ($I$), allelic heterogeneity ($h$), and penetrance ($P$). A variant with an allele frequency of 0.05% might be rare enough to cause common schizophrenia, but it is orders of magnitude too common to cause a rare, highly penetrant dominant cardiomyopathy. MCAF establishes a rigorous, disease-specific mathematical ceiling that automatically triggers ACMG benign rules BS1 and BA1."

### Q5: "Why do commercial testing laboratories have a Hazard Ratio of 0.55 in survival analysis?"
> **Your Answer:**  
> "In our multivariate Cox regression, commercial testing laboratories resolve discrepancies at nearly half the rate ($\text{HR} = 0.55$, $p < 0.001$) of academic medical centers and collaborative research consortia.
> 
> This is driven by operational and legal incentives: When an academic center updates an assertion, they do so as a public research contribution. When a commercial lab amends a variant assertion, they face substantial administrative costs, legal liabilities, and the burden of issuing amended diagnostic reports to ordering physicians and patients. As a result, commercial laboratories often postpone retractions until major annual panel overhaul cycles."

### Q6: "How does CuraCascade integrate into a real hospital's LIMS or EHR system?"
> **Your Answer:**  
> "CuraCascade is designed to operate as a **Pre-Report Audit Firewall**:
> 1. In a Laboratory Information Management System (LIMS), an automated script executes `python run.py audit --genes <PATIENT_CANDIDATE_GENES> --class A --format json`.
> 2. If any variant in the patient's report falls into Class A, the script exits with POSIX status `1`, automatically freezing report generation before the PDF is signed.
> 3. The geneticist receives the automated Clinical Governance Dossier to review alternative candidate variants."

### Q7: "What is Cohen's Kappa ($\kappa$) and why is it important that CuraCascade scored 0.920?"
> **Your Answer:**  
> "Cohen's Kappa measures inter-rater agreement between two raters classifying items into categories, while mathematically accounting for agreement occurring purely by chance. 
> 
> A kappa value of 0.920 indicates near-perfect concordance between CuraCascade's automated SQL joins and blinded manual adjudication by board-certified clinical molecular geneticists across our 100-gene gold-standard benchmark. This proves that our rule-based heuristic does not generate erratic false positives."

### Q8: "How does this tool help a diagnostic laboratory maintain CAP/CLIA or ISO 15189 accreditation?"
> **Your Answer:**  
> "Under ISO 15189:2022 Section 7.3 and CAP molecular pathology checklists, accredited laboratories are legally required to verify the ongoing clinical validity of their testing panels. 
> 
> Currently, laboratories perform this manually during sporadic multi-year reviews. CuraCascade automates this compliance obligation. By integrating `run.py audit` into monthly CI/CD workflows and generating signed Clinical Governance Dossiers, laboratories maintain an immutable, audit-ready paper trail proving continuous evidence monitoring."

### Q9: "How do you handle conflicting disease names across different international ontologies?"
> **Your Answer:**  
> "That was one of our primary data harmonization challenges. ClinGen indexes Mondo Disease Ontology (MONDO), ClinVar indexes MedGen and OMIM, and PanelApp often uses free-text NHS disease indications.
> 
> We engineered a deterministic ontology crosswalk in `pipeline/build_full_warehouse.py` that maps MONDO concepts to OMIM and Orphanet identifiers (`prevalence_per_million`). For ambiguous synonyms, we implement primary-key symbol disambiguation through the HGNC approved nomenclature database."

### Q10: "Can CuraCascade automatically retract variant entries in NCBI ClinVar?"
> **Your Answer:**  
> "NCBI ClinVar requires submission files to be submitted by the original laboratory that owns the assertion. Therefore, CuraCascade does NOT autonomously modify third-party database records. 
> 
> Instead, CuraCascade acts as an automated triage and governance engine: it flags the discrepancy, calculates the gnomAD frequency excess, invokes ACMG rules BA1 and BS1, and generates the standardized Clinical Governance Dossier with formal signature blocks so the laboratory director can submit the retraction to NCBI with full regulatory attestation."

---

## 💻 How to Launch & Present

### Option A: Open the PowerPoint Presentation (.pptx)
```bash
# Launch directly in Microsoft PowerPoint:
start CuraCascade_Presentation.pptx
```
*Tip:* Press `F5` to start slide show, or `Alt + F5` for PowerPoint Presenter View to see the embedded speaker notes on your laptop screen while projecting the slides to the classroom!

### Option B: Open the Interactive HTML Slides in Any Web Browser
```bash
# Launch in default browser:
start docs/CuraCascade_Presentation.html
```
*Hotkeys in Browser:*
- `Right Arrow` / `Space` $\to$ Next Slide
- `Left Arrow` $\to$ Previous Slide
- `N` $\to$ Toggle Speaker Script Drawer (shows verbatim speaking script!)
- `F` $\to$ Fullscreen mode
- `Home` / `End` $\to$ Jump to First / Last slide

### Option C: Inspect or Print the Publication PDF Report
```bash
# Open publication PDF report:
start CuraCascade_Publication_Report.pdf
```
