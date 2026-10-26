# CuraCascade: Academic Project Defense Speaker Notes & Script

**Project Title:** CuraCascade: An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis  
**Presenter & Architect:** Udit Shokeen (Reg. No: 23BCB0001)  
**Department:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Vellore, Tamil Nadu, India  
**Target Duration:** 10–12 Minutes (+ 5 Minutes Committee Q&A)  
**Deliverables:**
- PowerPoint Presentation: [`CuraCascade_Presentation_Redesigned.pptx`](file:///h:/Projects/curacascade/CuraCascade_Presentation_Redesigned.pptx) (15 Widescreen 16:9 Slides, Dark Theme, OpenXML Native Fade Transitions & Sequential Entrance Animations, Embedded Screenshots)
- Static Vector PDF: [`CuraCascade_Presentation_Redesigned.pdf`](file:///h:/Projects/curacascade/CuraCascade_Presentation_Redesigned.pdf) (15-Page High-DPI Widescreen Static Export)
- Live Web Deployment: [curacascadev2.streamlit.app](https://curacascadev2.streamlit.app)
- Open-Source Codebase: [github.com/uditshokeen14/curacascade](https://github.com/uditshokeen14/curacascade)

---

## ⏱️ Recommended Presentation Timing Strategy

| Phase | Slides | Content Focus | Target Time |
| :--- | :--- | :--- | :---: |
| **I. Motivation & Problem** | Slides 1–3 | Title, Clinical Knowledge Lag, Database Silos | 2.5 min |
| **II. System Architecture** | Slides 4–6 | 5-Stage Pipeline, SQLite 3NF + DuckDB, Disease-Aware Crosswalk | 3.0 min |
| **III. Software & Case Studies**| Slides 7–8 | Live Streamlit Walkthrough, SCN1B / MYLK2 / ACTN2 Audits | 2.0 min |
| **IV. Validation & Performance**| Slides 9–11 | 100-Gene Benchmark, 100% PPV vs 34.6% Recall, 34 FN Breakdown | 2.5 min |
| **V. Analytics, Rigor & Q&A** | Slides 12–15 | ML Triage, 2.82-Yr Latency, 47 Pytests, Future Roadmap & Q&A | 2.0 min |
| **Total Talk Duration** | **15 Slides** | — | **12.0 min** |

---

## Slide-by-Slide Defense Script, Guardrails & Viva Q&A

### Slide 1: Title & Academic Identification
* **Presenter Script:**
  > "Respected committee members, professor, and colleagues: Good morning. Today, I am presenting my capstone research project, **CuraCascade: An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis**.
  >
  > In modern clinical medicine, the validity of gene-disease relationships is constantly evolving. However, there is a dangerous, multi-year latency between upstream expert reappraisals and downstream clinical variant databases. CuraCascade is a deterministic bioinformatics data warehouse and discrepancy audit engine built to bridge this gap. Over the next 12 minutes, I will walk you through the biological problem, our relational architecture, the disease-aware matching logic, our 100-gene validation benchmark, and the live deployed software."
* **Core Takeaway:** CuraCascade is an end-to-end, reproducible bioinformatics platform designed to audit and triage unpropagated gene validity downgrades across clinical databases.
* **What NOT to Overclaim:** Do not claim that CuraCascade directly diagnoses patients or autonomously alters patient electronic health records. It is a research-oriented decision support and quality-assurance engine for laboratory geneticists.
* **Likely Faculty Question:** *What is the primary motivation for building this tool rather than relying on existing variant interpretation portals like ClinVar?*
* **Defensible Answer:** "Existing portals like ClinVar curate individual variant assertions under the implicit assumption that the overarching gene-disease relationship is established. When an expert consortium like ClinGen refutes an entire gene, downstream variant records often sit un-synchronized for years. CuraCascade addresses this semantic gap between gene validity and variant pathogenicity."

---

### Slide 2: The Clinical Challenge — The Evidence Synchronization Gap
* **Presenter Script:**
  > "To understand the clinical motivation, consider how genomics knowledge progresses. In the 1990s and early 2000s, hundreds of genes were linked to human disease based on small family studies without modern population controls. Today, ClinGen expert panels systematically re-evaluate these candidate genes and frequently downgrade them to Limited, Disputed, or Refuted.
  >
  > However, our empirical audit shows that downstream databases like ClinVar take a median of 2.82 years to reflect these downgrades. During this multi-year lag, diagnostic laboratories continue classifying variants as Pathogenic in disputed genes. If an asymptomatic patient receives a report with a pathogenic variant in a refuted arrhythmia gene, they risk unwarranted predictive testing in family members or even inappropriate surgical recommendations like an implantable cardioverter-defibrillator."
* **Core Takeaway:** Gene validity reappraisals do not propagate instantaneously; a median 2.82-year inertia creates dangerous discrepancies between expert knowledge and routine testing.
* **What NOT to Overclaim:** Avoid claiming that every downstream variant becomes completely benign when a gene is downgraded. The gene-disease attribution is invalidated under that specific phenotype, requiring expert re-curation review.
* **Likely Faculty Question:** *Does a ClinGen downgrade to Disputed mean that all variants in that gene are completely harmless polymorphisms?*
* **Defensible Answer:** "No. Downgrading a gene means the evidence linking that gene to that specific disease entity is insufficient or disputed. Variants cannot be claimed as Pathogenic for that indication under ACMG guidelines, but they may represent variants of uncertain significance (VUS) or pertain to a different clinical disorder."

---

### Slide 3: Why Existing Workflows Fail — Multi-Repository Semantic Fragmentation
* **Presenter Script:**
  > "Why doesn't this problem fix itself automatically? Because the genomic data ecosystem is deeply fragmented across four distinct silos. ClinGen curates at the gene-disease dyad level using MONDO ontologies. ClinVar archives variant assertions using MedGen terms submitted voluntarily by testing labs. PanelApp curates panel BED files for diagnostic exome filtering. And gnomAD tracks allele frequencies across ancestry clusters.
  >
  > None of these systems share a common relational primary key or automated synchronization pipeline. Without an automated crosswalk like CuraCascade, tracking evidence updates requires tedious, error-prone manual cross-referencing that laboratory geneticists simply do not have time to conduct for thousands of historical cases."
* **Core Takeaway:** The lack of unified relational identifiers and cross-database synchronization creates a systemic structural barrier to keeping diagnostic records up to date.
* **What NOT to Overclaim:** Do not imply that ClinVar or PanelApp are defective databases; they serve different purposes with different governance models.
* **Likely Faculty Question:** *Why can't ClinVar simply delete pathogenic variants when ClinGen downgrades a gene?*
* **Defensible Answer:** "ClinVar is an archival database of laboratory assertions, not an arbiter of primary truth. It preserves submitter records historically. Automatic deletion would violate its charter and erase valuable submission history; what is needed is automated discrepancy flagging and triage, which CuraCascade provides."

---

### Slide 4: The CuraCascade Solution — Deterministic 5-Stage Pipeline
* **Presenter Script:**
  > "CuraCascade solves this semantic disconnect through a 5-stage automated pipeline. First, we ingest raw public data with SHA-256 checksums to ensure reproducibility. Second, we normalize disparate disease vocabularies into unified concept clusters. Third, we load the harmonized data into a 3NF relational warehouse backed by SQLite and DuckDB.
  >
  > Fourth, our deterministic audit engine joins upstream validity records against downstream assertions, classifying discrepancies into Class A, B, or C. Finally, we expose the findings through an interactive web portal and exportable clinical remediation dossiers ready for laboratory director sign-off."
* **Core Takeaway:** CuraCascade replaces manual cross-referencing with a deterministic, reproducible, 5-stage automated audit pipeline.
* **What NOT to Overclaim:** Be clear that this pipeline operates deterministically based on defined clinical rules, not black-box uninterpretable algorithms.
* **Likely Faculty Question:** *Why did you choose a 5-stage pipeline architecture instead of directly querying the source APIs on demand?*
* **Defensible Answer:** "Direct API querying is non-deterministic and computationally slow across thousands of genes and tens of thousands of variants. By staging ingestion into a normalized relational warehouse, we guarantee millisecond join performance, cryptographic provenance, and offline reproducibility."

---

### Slide 5: System Architecture — Dual-Engine Data Warehouse
* **Presenter Script:**
  > "Slide 5 details our system architecture. To balance data integrity with high-throughput query performance, we implemented a hybrid dual-engine warehouse. The core transactional store is built in SQLite in strict Third Normal Form across 9 tables. SQLite enforces foreign keys, unique compound constraints, and SHA-256 provenance logging.
  >
  > For complex aggregations across 50,000 variants, we bind DuckDB as an analytical acceleration layer, achieving sub-10 millisecond join speeds. Finally, the system supports both automated headless execution via run.py and an interactive clinical portal in Streamlit."
* **Core Takeaway:** CuraCascade combines SQLite's strict 3NF relational constraints with DuckDB's in-memory columnar join speed for reproducible, low-latency execution.
* **What NOT to Overclaim:** Ensure that claims of 3NF schema compliance are backed by the actual 9-table schema definition in database/schema.py.
* **Likely Faculty Question:** *Why did you use SQLite and DuckDB instead of an enterprise client-server database like PostgreSQL?*
* **Defensible Answer:** "Clinical bioinformatics pipelines frequently run in containerized or air-gapped high-performance computing clusters. Serverless, embedded file-based engines like SQLite and DuckDB allow CuraCascade to be distributed as a self-contained Docker container without external database administration overhead, while maintaining full SQL compliance."

---

### Slide 6: Core Innovation — Disease-Aware Concept Crosswalk & Matching Logic
* **Presenter Script:**
  > "Slide 6 represents one of our most important technical contributions: disease-aware concept matching. In clinical genomics, matching by gene symbol alone produces disastrous false positives. Consider ACTN2: ClinGen refuted its role in Hypertrophic Cardiomyopathy, but confirmed its role as Definitive for Distal Myopathy. A naive algorithm flags all ACTN2 variants as erroneous.
  >
  > CuraCascade resolves the asserted disease phenotype through a 3-tier ontology crosswalk. If a variant belongs to distal myopathy, it is excluded from auditing. Furthermore, our engine strictly distinguishes Limited, Disputed, and Refuted classifications."
* **Core Takeaway:** CuraCascade prevents false positive alerts by requiring disease-level ontology matching rather than simplistic gene-symbol matching.
* **What NOT to Overclaim:** Never treat Limited, Disputed, and Refuted as synonyms. Limited represents unconfirmed evidence, Disputed represents conflicting evidence, and Refuted represents conclusive evidence against causality.
* **Likely Faculty Question:** *How does your system handle variants in ClinVar where the submitter wrote 'not provided' for the disease?*
* **Defensible Answer:** "When a phenotype is listed as 'not provided', our engine flags it with match status DATA_QUALITY_ISSUE. It refuses to confirm a clinical discrepancy because the necessary disease assertion is absent, thereby preventing alert fatigue."

---

### Slide 7: Live Application Walkthrough — Streamlit Decision Support Portal
* **Presenter Script:**
  > "Slide 7 shows the genuine running web application, deployed live at curacascadev2.streamlit.app. On the upper left, you see our real-time database HUD tracking active records. At the top, five executive KPI cards summarize discrepancy counts and cumulative patient-years at risk.
  >
  > Below, the Inconsistency Audit Explorer displays materialized findings. Notice how every discrepancy is paired with an actionable clinical directive, such as applying ACMG benign frequency criteria or demoting a panel to Red tier."
* **Core Takeaway:** CuraCascade provides an intuitive, high-throughput web portal that transforms raw database queries into prioritized clinical governance actions.
* **What NOT to Overclaim:** Do not present this interface as an autonomous diagnostic device. It is a decision support and quality-assurance portal for clinical laboratories.
* **Likely Faculty Question:** *Can external laboratories use this interface with their own internal variant lists?*
* **Defensible Answer:** "Yes. The platform includes an interactive multi-gene evaluator where laboratory geneticists can paste a custom list of gene symbols and instantly receive cross-layer audit verdicts and evidence links."

---

### Slide 8: Exemplar Audit Findings — ACTN2 & SCN1B Case Studies
* **Presenter Script:**
  > "Slide 8 demonstrates actual audit findings from our database. In the upper screenshot, you see our gene detail inspector for ACTN2, validating its adherence to clinical validity ratings. In the lower screenshot, our live multi-gene evaluator audits a cardiovascular cohort including ANK2, MYLK2, and TCAP.
  >
  > Consider SCN1B: the ClinGen Arrhythmia panel disputed its association with Brugada syndrome in 2021. Yet in ClinVar, 18 variants remain labeled Pathogenic. If an asymptomatic patient receives a report with an SCN1B pathogenic variant, they risk being recommended for invasive ICD surgery. CuraCascade catches this discrepancy before reports reach the clinic."
* **Core Takeaway:** Real audit findings in SCN1B and MYLK2 illustrate tangible clinical hazards where laboratory testing lags authoritative evidence.
* **What NOT to Overclaim:** Do not claim that CuraCascade investigated specific individual hospital patients. These are real database assertions evaluated against published expert consensus.
* **Likely Faculty Question:** *Why did the ClinGen Arrhythmia panel dispute SCN1B?*
* **Defensible Answer:** "Comprehensive international re-evaluations showed that early candidate-gene publications lacked statistical power and adequate control cohorts; subsequent large-scale case-control sequencing demonstrated that SCN1B variants occur at similar frequencies in healthy populations."

---

### Slide 9: Validation Benchmark Methodology — 100-Gene Adjudication Cohort
* **Presenter Script:**
  > "Slide 9 establishes our validation benchmark methodology. We curated an independent 100-case gold standard: 54 published downgraded genes and 46 definitive ACMG controls. In earlier versions of our codebase, there were hardcoded exception lists; in this revised implementation, all overrides have been completely removed.
  >
  > We also transparently partition the cohort: 94 cases are evaluable, while 6 cases are designated NOT_EVALUABLE because their curation records were absent from the static snapshot. Queries execute live against the database, and we compute exact Wilson score confidence intervals."
* **Core Takeaway:** The 100-gene validation benchmark enforces a strict label firewall with zero hardcoded prediction overrides and live relational query execution.
* **What NOT to Overclaim:** Do not claim that the 100 benchmark cases were evaluated by multiple blinded human curators; this is a single-curator literature-derived benchmark.
* **Likely Faculty Question:** *Why did you exclude 6 cases as NOT_EVALUABLE instead of counting them as false negatives?*
* **Defensible Answer:** "Counting unobserved data as algorithmic false negatives conflates data availability with classifier logic. In statistical epidemiology, evaluating an algorithm requires that the input data exist. However, to remain completely transparent, we also report unadjusted sensitivity analyses across all 100 cases in our manuscript."

---

### Slide 10: Empirical Results & Precision–Recall Trade-Off
* **Presenter Script:**
  > "Slide 10 presents our empirical benchmark results. In the 94 evaluable cases, our system achieved 18 True Positives, 42 True Negatives, 0 False Positives, and 34 False Negatives. This translates to 100% Precision, 100% Specificity, and 34.6% Recall.
  >
  > Why is precision 100% while recall is 34.6%? Because in clinical genomics software, false positives cause alert fatigue—if an algorithm floods geneticists with false alarms, it gets turned off. We intentionally prioritized high specificity and precision. In the next slide, we will dissect why those 34 false negatives occurred."
* **Core Takeaway:** CuraCascade operates with high precision (100.0%) and zero false positives, accepting lower recall (34.6%) to avoid clinical alert fatigue.
* **What NOT to Overclaim:** Do not present 100% precision as proof that the software is perfect. Disclose that recall is 34.6% and explain why false negatives occurred.
* **Likely Faculty Question:** *Doesn't a recall of 34.6% mean the tool misses nearly two-thirds of valid discrepancies?*
* **Defensible Answer:** "It means two-thirds of the benchmark cases were not flagged by our automated join. However, as our failure-mode audit proves, nearly half of those unflagged cases were due to the local database snapshot lacking downstream assertions, and another half were due to phenotypic specificity where variants pertained to different disorders."

---

### Slide 11: Failure Mode Analysis & Limitations — Dissecting 34 False Negatives
* **Presenter Script:**
  > "Slide 11 addresses the 34 false negatives directly. We audited every single case. Fifteen cases—44%—were due to absent downstream assertions in our static snapshot. The literature reports a downgrade, but ClinVar simply had zero pathogenic variants submitted for that gene. Three cases were due to curations not yet ingested into the snapshot.
  >
  > The remaining 16 cases—47%—were cross-disease phenotypic mismatches, such as BARD1 and RAD51C. Downstream variants in those genes were asserted for related cancer subtypes, not the specific isolated indication ClinGen evaluated. Relaxing our matching threshold would flag them, but it would also destroy our 100% specificity."
* **Core Takeaway:** The 34 false negatives reflect static snapshot coverage limits and deliberate biological specificity to protect against false positive joins.
* **What NOT to Overclaim:** Do not dismiss the false negatives as unimportant. Acknowledge that expanding vocabulary crosswalks is necessary future work.
* **Likely Faculty Question:** *Could you improve recall by using fuzzy string matching on disease names?*
* **Defensible Answer:** "We experimented with broad keyword overlap, but it created 12 false positives—for example, matching Lynch syndrome assertions to unrelated colorectal conditions. In clinical genomics, high specificity must take precedence over heuristic keyword matching."

---

### Slide 12: Exploratory Analytics — ML Downgrade Forecasting & Latency Kinetics
* **Presenter Script:**
  > "Slide 12 covers our exploratory analytics. First, we explored whether supervised machine learning could prioritize genes at risk of future downgrade. Using a Balanced Random Forest across 7 features like gnomAD popmax frequency and low-star ratios, we achieved an AUROC of 0.857 and a Brier score of 0.1508. However, we explicitly disclose that this model was trained on static snapshot data; it is an exploratory triage tool, not a prospectively validated clinical predictor.
  >
  > Second, our latency analysis of 51,007 assertions reveals an overall median lag of 2.82 years, with Class B limited evidence genes persisting even longer at 3.77 years."
* **Core Takeaway:** CuraCascade demonstrates strong retrospective triage capability (AUROC 0.857) and quantifies a 2.82-year cross-sectional evidence propagation lag.
* **What NOT to Overclaim:** Never claim this machine learning model is clinically validated or ready for diagnostic deployment. Explicitly cite potential temporal leakage.
* **Likely Faculty Question:** *What is the primary risk of temporal leakage in your machine learning experiment?*
* **Defensible Answer:** "Because features like variant count and allele frequencies were extracted from a 2024 snapshot rather than reconstructed historically from the exact day before each ClinGen downgrade, some post-downgrade evidence shifts may have leaked into the features. That is why we treat this as exploratory retrospective analysis."

---

### Slide 13: Software Engineering Rigor & Reproducibility
* **Presenter Script:**
  > "Slide 13 highlights our engineering standards. Software in biomedical informatics must be reproducible and robust. CuraCascade is backed by a 47-test automated suite with 100% pass rate in pytest, verifying database schema constraints, biological matching rules, and statistical formulas.
  >
  > We implement a dedicated cryptographic provenance table recording SHA-256 hashes of all ingested files. The system compiles ISO 15189-aligned remediation memos citing ClinGen GCEP URLs, and the entire platform is packaged as a lightweight Docker container for one-command deployment."
* **Core Takeaway:** CuraCascade adheres to production software standards with 47 automated tests, SHA-256 provenance logging, and Docker containerization.
* **What NOT to Overclaim:** Do not confuse passing 47 software tests with prospective clinical validation. Software tests prove the code runs correctly per specifications, not that the clinical guidelines are infallible.
* **Likely Faculty Question:** *How do you guarantee that a database query will produce the exact same audit finding six months from now?*
* **Defensible Answer:** "Through our provenance table and deterministic matching rules. Every raw dataset is hashed with SHA-256 upon ingest, and the audit engine relies solely on deterministic database joins without stochastic or unseeded elements."

---

### Slide 14: Research Contributions & Clinical Scope
* **Presenter Script:**
  > "Slide 14 summarizes our four key research contributions. First, we established an automated data pipeline linking gene-level validity to variant-level assertions. Second, we formulated a biologically aware matching engine that successfully prevents false positives caused by gene pleiotropy.
  >
  > Third, we empirically characterized the 2.82-year knowledge propagation lag across 51,000 assertions. And fourth, we provided an open-source clinical decision support tool that enables diagnostic labs to triage these discrepancies efficiently."
* **Core Takeaway:** CuraCascade provides both an empirical characterization of evidence lag and a practical, open-source tool for clinical re-curation triage.
* **What NOT to Overclaim:** Do not overclaim regulatory clearance; emphasize that CuraCascade is a research tool supporting professional medical geneticists.
* **Likely Faculty Question:** *What is the single biggest lesson learned from building this system?*
* **Defensible Answer:** "The realization that clinical genomics cannot treat genes as monolithic entities. Because human genes cause distinct diseases through different mechanisms, any evidence aggregation tool must maintain strict disease-level ontology awareness."

---

### Slide 15: Conclusion, Future Roadmap & Defense Q&A
* **Presenter Script:**
  > "In conclusion, CuraCascade demonstrates that automated cross-layer auditing is both technically feasible and clinically necessary. By linking ClinGen, ClinVar, PanelApp, and gnomAD through a disease-aware relational warehouse, we achieved 100% precision in flagging unpropagated discrepancies and quantified an empirical 2.82-year knowledge lag.
  >
  > For future work, we plan to implement prospective longitudinal tracking and EHR integration. I want to sincerely thank the examination committee for their time and guidance, and I now welcome your questions and discussion."
* **Core Takeaway:** CuraCascade bridges a critical gap in clinical genomics through reproducible engineering, open-source decision support, and strict scientific integrity.
* **What NOT to Overclaim:** Be open and receptive to faculty questions; defend the choices made in 3NF design and disease-aware matching without being defensive.
* **Likely Faculty Question:** *What is the most immediate clinical benefit if a diagnostic lab adopts CuraCascade tomorrow?*
* **Defensible Answer:** "The lab can immediately perform a retrospective audit of all historical patient cases where variants were signed out as Pathogenic in disputed genes like SCN1B or MYLK2, allowing them to issue amended reports and prevent unnecessary cascade screening in family members."
