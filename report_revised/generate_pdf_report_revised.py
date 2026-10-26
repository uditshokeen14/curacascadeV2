"""
Script to generate CuraCascade_IEEE_Report_Revised.pdf via headless Chromium.
Enforces genuine IEEE conference two-column specifications, Times New Roman typography,
0.75in top/bottom and 0.625in left/right margins, embedded high-DPI figures, and structured tables.
"""

from __future__ import annotations
import subprocess
from pathlib import Path
import pypdf

REPORT_DIR = Path(__file__).resolve().parent
HTML_PATH = REPORT_DIR / "ieee_report_revised.html"
PDF_PATH = REPORT_DIR / "CuraCascade_IEEE_Report_Revised.pdf"

CHROME_PATHS = [
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
    Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe"),
]

def build_html():
    fig1 = (REPORT_DIR / "figures" / "fig1_architecture.png").as_uri()
    fig2 = (REPORT_DIR / "figures" / "fig2_matching_workflow.png").as_uri()
    fig3 = (REPORT_DIR / "figures" / "fig3_confusion_matrix.png").as_uri()
    fig4 = (REPORT_DIR / "figures" / "fig4_empirical_latency.png").as_uri()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CuraCascade: An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis</title>
<style>
  @page {{
    size: letter;
    margin: 0.75in 0.625in 0.75in 0.625in;
    @bottom-center {{
      content: counter(page);
      font-family: 'Times New Roman', Times, serif;
      font-size: 9pt;
    }}
  }}

  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 9.8pt;
    line-height: 1.15;
    color: #000000;
    margin: 0;
    padding: 0;
    background: #ffffff;
    text-align: justify;
    text-justify: inter-word;
  }}

  .header-block {{
    text-align: center;
    margin-bottom: 12pt;
  }}

  h1.paper-title {{
    font-size: 19pt;
    font-weight: bold;
    margin: 0 0 6pt 0;
    line-height: 1.2;
    text-align: center;
  }}

  .author-name {{
    font-size: 11pt;
    font-weight: bold;
    margin: 0 0 2pt 0;
  }}

  .author-affiliation {{
    font-size: 9.5pt;
    font-style: italic;
    color: #1e293b;
    margin: 0 0 2pt 0;
  }}

  .author-email {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 9pt;
    color: #0f172a;
    margin: 0 0 10pt 0;
  }}

  .columns-container {{
    column-count: 2;
    column-gap: 0.25in;
    column-fill: balance;
  }}

  .abstract-box {{
    margin-bottom: 8pt;
    padding: 0 4pt;
  }}

  .abstract-title {{
    font-weight: bold;
    font-size: 9pt;
  }}

  .abstract-text {{
    font-style: italic;
    font-size: 8.8pt;
    line-height: 1.14;
  }}

  .index-terms {{
    margin-bottom: 10pt;
    padding: 0 4pt;
    font-size: 8.8pt;
  }}

  .index-terms-title {{
    font-weight: bold;
  }}

  .index-terms-body {{
    font-style: italic;
  }}

  h2.ieee-sec {{
    font-size: 9.8pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin: 10pt 0 4pt 0;
    break-after: avoid;
  }}

  h3.ieee-subsec {{
    font-size: 9.3pt;
    font-weight: bold;
    font-style: italic;
    text-align: left;
    margin: 8pt 0 2pt 0;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 4pt 0;
    text-indent: 1.2em;
  }}

  p.no-indent {{
    text-indent: 0;
  }}

  .equation {{
    text-align: center;
    margin: 5pt 0;
    font-style: italic;
  }}

  .eq-num {{
    float: right;
    font-style: normal;
  }}

  figure {{
    margin: 8pt 0;
    text-align: center;
    break-inside: avoid;
  }}

  figure img {{
    width: 100%;
    max-width: 100%;
    height: auto;
    border: 0.5pt solid #cbd5e1;
    border-radius: 2px;
  }}

  figcaption {{
    font-size: 8pt;
    font-style: italic;
    text-align: justify;
    margin-top: 3pt;
    line-height: 1.1;
  }}

  figure.full-width {{
    column-span: all;
    margin: 10pt 0;
  }}

  table.ieee-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0;
    font-size: 7.8pt;
    line-height: 1.1;
    break-inside: avoid;
  }}

  table.ieee-table caption {{
    font-size: 8pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 4pt;
  }}

  table.ieee-table th {{
    border-top: 1pt solid #000000;
    border-bottom: 0.8pt solid #000000;
    padding: 3pt 2pt;
    text-align: left;
    background: #f8fafc;
    font-weight: bold;
  }}

  table.ieee-table td {{
    border-bottom: 0.4pt solid #e2e8f0;
    padding: 3pt 2pt;
    text-align: left;
    vertical-align: top;
  }}

  table.ieee-table tr.total-row td {{
    border-top: 0.8pt solid #000000;
    border-bottom: 1pt solid #000000;
    font-weight: bold;
  }}

  .ref-list {{
    font-size: 7.8pt;
    line-height: 1.15;
    margin-top: 4pt;
  }}

  .ref-item {{
    margin-bottom: 3pt;
    text-indent: -1.5em;
    padding-left: 1.5em;
  }}
</style>
</head>
<body>

<div class="header-block">
  <h1 class="paper-title">CuraCascade: An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis</h1>
  <div class="author-name">Udit Shokeen (Reg. No: 23BCB0001)</div>
  <div class="author-affiliation">School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, Tamil Nadu 632014, India</div>
  <div class="author-email">Email: udit.shokeen2023@vitstudent.ac.in</div>
</div>

<div class="columns-container">

  <div class="abstract-box">
    <span class="abstract-title">Abstract—</span>
    <span class="abstract-text">Clinical genomics relies on expert consortia—most prominently the Clinical Genome Resource (ClinGen)—to formally establish the clinical validity of gene–disease relationships. When Gene Curation Expert Panels (GCEPs) re-evaluate and subsequently downgrade an association from Definitive or Moderate clinical validity to Limited (insufficient evidence), Disputed (conflicting evidence), or Refuted (evidence against validity), downstream repositories do not automatically synchronize. Active diagnostic assertions, including Pathogenic and Likely Pathogenic (P/LP) variant interpretations in NCBI ClinVar and diagnostic-grade ("Green") gene indications in Genomics England PanelApp, routinely persist across static archives. Rather than rendering all variants biologically invalid across all phenotypes, these discordant entries represent potential disease-specific discrepancies requiring expert genetic review. To address this asynchronous lag, we present CuraCascade, an open-source clinical genomics relational audit warehouse and evidence harmonization platform. CuraCascade normalizes disparate assertions across ClinGen, ClinVar, PanelApp, and gnomAD into a Third Normal Form (3NF) relational architecture backed by transactional SQLite and analytical DuckDB engines, referencing the Mondo Disease Ontology for concept reconciliation. The framework implements a deterministic, disease-aware discrepancy classification taxonomy that accounts for allelic pleiotropy, canonical ontology crosswalks (MONDO, OMIM), and distinct disorder exclusions. Evaluated against an independently curated benchmark (N = 100 gene–disease validity assertions; 54 published downgrades, 46 definitive disease controls), 94 of 100 cases were evaluable and six were designated NOT_EVALUABLE due to absent snapshot records. Across this primary evaluable cohort (N = 94), CuraCascade achieved a precision of 100.0% (95% Wilson CI: 82.4%–100.0%; 18 True Positives, 0 False Positives), recall of 34.6% (95% CI: 23.2%–48.2%; 34 False Negatives), specificity of 100.0% (95% CI: 91.6%–100.0%; 42 True Negatives), accuracy of 63.8% (95% CI: 53.8%–72.8%), and concordance &kappa; = 0.3212. In an unadjusted 100-case sensitivity analysis assuming all six unobserved cases are unflagged non-detections, recall was 33.3% and accuracy was 64.0%. The low recall of 34.6% is empirically driven by absent downstream laboratory assertions (15 cases), uningested panel curations (3 cases), and strict cross-disease phenotype boundaries (16 cases). In an empirical cross-sectional latency analysis of 51,007 active ClinVar assertions across 536 curated genes, the median elapsed discordance duration since ClinGen appraisal was 2.82 years (1,030 days; IQR: 2.98 years / 1,087 days). Retrospective exploratory machine learning yielded an AUROC of 0.857 and Brier score of 0.1508; prospective claims remain disabled pending longitudinal pre-curation feature reconstruction. CuraCascade provides an automated, vendor-neutral research audit framework to prioritize potential disease-specific discrepancies for clinical and genetic review.</span>
  </div>

  <div class="index-terms">
    <span class="index-terms-title">Index Terms—</span>
    <span class="index-terms-body">Clinical genomics, gene curation, ClinGen, ClinVar, PanelApp, data warehouse, Third Normal Form, evidence downgrade, biomedical informatics.</span>
  </div>

  <h2 class="ieee-sec">I. Introduction</h2>
  <p>The integration of high-throughput next-generation sequencing (NGS) into diagnostic medicine has accelerated the identification of putative monogenic disease genes. However, the clinical utility of comprehensive genomic sequencing depends fundamentally upon the veracity of the underlying gene–disease evidence base [1]. Historically, hundreds of monogenic disease associations were published based on candidate-gene studies involving small kindreds, inadequate statistical power, and absent ancestry-matched population control cohorts [2].</p>

  <p>To establish rigorous evidence-based standardization, the Clinical Genome Resource (ClinGen) developed a semi-quantitative framework to classify gene–disease clinical validity into distinct qualitative tiers: <em>Definitive</em>, <em>Strong</em>, <em>Moderate</em>, <em>Limited</em>, <em>Disputed</em>, or <em>Refuted</em> [1], [3]. These classifications represent qualitatively different evidence states: <em>Limited</em> denotes insufficient or preliminary evidence where clinical utility cannot yet be confirmed; <em>Disputed</em> denotes conflicting evidence where substantial findings challenge the asserted causality; and <em>Refuted</em> indicates affirmative evidence against the gene–disease relationship based on population genetics or contradictory pedigree segregation. Systematic reappraisals conducted by ClinGen Gene Curation Expert Panels (GCEPs) have demonstrated that up to 40% of genes historically tested on commercial and academic panels for inherited cardiomyopathies [4], [5], Brugada syndrome [6], and hereditary cancer [7] lack sufficient scientific validity.</p>

  <p>Despite formal consortium consensus updates, biomedical knowledge bases operate in decentralized, asynchronous silos. When ClinGen formally publishes a gene–disease downgrade, downstream knowledge bases—including the National Center for Biotechnology Information (NCBI) ClinVar archive [8] and Genomics England PanelApp [9]—do not automatically propagate these re-appraisals. Consequently, variants located within disputed or refuted disease genes frequently remain cataloged as Pathogenic (P) or Likely Pathogenic (LP) in ClinVar. Similarly, diagnostic exome panels routinely retain downgraded genes as "Green" (diagnostic-grade), prompting clinical interpretation and reporting [10].</p>

  <p>Importantly, a gene-level downgrade does not imply that all constituent variants are biologically benign across all possible phenotypes; rather, variant assertions submitted under a questioned or refuted indication represent potential disease-specific discrepancies requiring expert genetic review. If left unreviewed, reporting such variants under outdated indications can introduce diagnostic friction, misdirected clinical workups, or unwarranted familial cascade testing [5].</p>

  <p>To address this knowledge cascade lag, we present <strong>CuraCascade</strong>, an integrated computational framework for gene–disease evidence aggregation, relational validation, and research-oriented discrepancy auditing.</p>

  <h2 class="ieee-sec">II. Background and Related Work</h2>
  <p>Evidence curation in clinical genetics has evolved from individual laboratory assertions toward structured expert consensus. ClinGen GCEPs conduct systematic literature reappraisals to evaluate genetic and experimental evidence [1]. Concurrently, NCBI ClinVar aggregates variant-level clinical interpretations submitted by hundreds of testing laboratories worldwide [8]. Genomics England PanelApp crowd-sources expert evaluations to establish diagnostic panel indications for the UK National Health Service (NHS) Genomic Medicine Service [9].</p>

  <p>Prior studies have highlighted discrepancies between variant interpretations across submitters in ClinVar [2]. However, existing quality-assurance tools focus primarily on variant-level discordance (e.g., conflicting classifications between Benign and Pathogenic) or population allele frequency ceilings via the Genome Aggregation Database (gnomAD) [11].</p>

  <p>Significantly less attention has been directed toward the systemic disconnect between <em>gene-level validity reappraisals</em> and <em>downstream variant-level assertions</em>. When an entire gene is refuted or placed in a limited-evidence tier for a specific condition, constituent variants submitted under that indication require systematic re-evaluation. Currently, diagnostic laboratories and curation teams lack automated, open-source relational infrastructure to identify, track, and prioritize these unpropagated consensus shifts for expert re-adjudication.</p>

  <h2 class="ieee-sec">III. Problem Statement and Objectives</h2>
  <h3 class="ieee-subsec">A. Problem Statement</h3>
  <p class="no-indent">Let a clinical validity assertion be a tuple <i>A</i><sub>CG</sub> = (<i>G</i>, <i>D</i>, <i>C</i>, <i>t</i><sub>CG</sub>), where <i>G</i> is the HGNC gene symbol, <i>D</i> is the disease concept, <i>C</i> &isin; &#123;Definitive, Strong, Moderate, Limited, Disputed, Refuted&#125; is the ClinGen validity status, and <i>t</i><sub>CG</sub> is the appraisal date. Let downstream assertions be <i>A</i><sub>CV</sub> = (<i>v</i>, <i>G</i>, <i>D'</i>, <i>S</i><sub>CV</sub>, <i>t</i><sub>CV</sub>) for ClinVar variants and <i>A</i><sub>PA</sub> = (<i>G</i>, <i>D''</i>, <i>T</i><sub>PA</sub>) for PanelApp panel indications, where <i>S</i><sub>CV</sub> &isin; &#123;P, LP, VUS, LB, B&#125; and <i>T</i><sub>PA</sub> &isin; &#123;Green, Amber, Red&#125;.</p>

  <p>When <i>C</i> &isin; &#123;Limited, Disputed, Refuted&#125; for disease <i>D</i>, an evidence discordance exists if downstream registries retain active pathogenic assertions (<i>S</i><sub>CV</sub> &isin; &#123;P, LP&#125; or <i>T</i><sub>PA</sub> = Green) for a matching disease concept (<i>D</i> &approx; <i>D'</i>). The cross-sectional elapsed latency is defined as:</p>

  <div class="equation">
    &Delta;t = t<sub>obs</sub> - t<sub>CG</sub> <span class="eq-num">(1)</span>
  </div>

  <p class="no-indent">representing the elapsed duration during which potentially discordant diagnostic assertions remain active in operational repository circulation without expert re-adjudication.</p>

  <h3 class="ieee-subsec">B. System Objectives</h3>
  <p>CuraCascade was engineered to achieve four core objectives:</p>
  <p>1) <em>Relational Evidence Harmonization:</em> Ingest and harmonize multi-source assertions into a normalized Third Normal Form (3NF) relational warehouse.</p>
  <p>2) <em>Deterministic Biological Audit Engine:</em> Implement disease-aware matching rules that distinguish potential discrepancies from distinct disorders in pleiotropic genes.</p>
  <p>3) <em>Empirical Latency Characterization:</em> Quantify the empirical cross-sectional elapsed duration of active assertions across clinical specialties and submitter review tiers.</p>
  <p>4) <em>Transparent Independent Benchmarking:</em> Evaluate audit decision rules against an independently curated ground truth with explicit confidence intervals, stated sensitivity assumptions, and failure-mode analysis.</p>

  <figure>
    <img src="{fig1}" alt="Overall CuraCascade Architecture">
    <figcaption>Fig. 1. Overall CuraCascade system architecture and multi-tier data flow. Primary evidence sources (ClinGen, ClinVar, PanelApp, gnomAD) and reference ontologies (MONDO) are harmonized into a 3NF relational warehouse backed by SQLite and DuckDB, evaluated by a deterministic biological audit engine, and surfaced via CLI, Web, and Remediation tools.</figcaption>
  </figure>

  <h2 class="ieee-sec">IV. System Architecture and Methodology</h2>
  <p>The overall architecture of CuraCascade is illustrated in Fig. 1. The platform comprises four integrated tiers:</p>
  <p>1) <em>Data Ingestion & Normalization Layer:</em> Automated parsers extract gene curations from ClinGen JSON/CSV endpoints, stream-filter ClinVar variant summary archives, fetch PanelApp panel indications, and calculate gnomAD maximum credible population allele frequency (MCAF) thresholds.</p>
  <p>2) <em>3NF Relational Warehouse Layer:</em> Dual-engine storage combining transactional SQLite with strict foreign keys and in-memory columnar DuckDB analytical scanners [12].</p>
  <p>3) <em>Biological Audit & Crosswalk Engine:</em> Deterministic heuristic classifier evaluating target disease ontology identifiers (MONDO, OMIM), pleiotropic exclusions, and population frequency ceilings.</p>
  <p>4) <em>Audit Interfaces & Governance Layer:</em> Headless command-line interface (<code>run.py audit</code>, <code>run.py verify</code>), Streamlit web portal, and automated clinical remediation dossier generators.</p>

  <h2 class="ieee-sec">V. Data Sources and Data Processing</h2>
  <p>CuraCascade integrates four primary biological evidence sources alongside reference disease ontologies, summarized in Table I:</p>
  <p>• <strong>ClinGen Gene Validity Archive:</strong> Evaluates expert validity classifications. Curations classified as <em>Limited</em> (insufficient evidence), <em>Disputed</em> (conflicting evidence), or <em>Refuted</em> (evidence against validity) initiate discrepancy tracking.</p>
  <p>• <strong>NCBI ClinVar:</strong> Ingests variant-level interpretations. Variant records are filtered for Pathogenic and Likely Pathogenic assertions (<i>S</i><sub>CV</sub> &isin; &#123;P, LP&#125;), submitter counts, and review star ratings (0 to 4 stars).</p>
  <p>• <strong>Genomics England PanelApp:</strong> Ingests gene memberships across diagnostic indications. Green panels represent diagnostic-grade consensus for routine exome reporting.</p>
  <p>• <strong>gnomAD v4:</strong> Provides global and ancestry-specific population allele frequencies to evaluate whether cataloged variants exceed biological MCAF ceilings for rare monogenic disorders.</p>
  <p>• <strong>Mondo Disease Ontology:</strong> Serves as the standardized reference ontology for disease entity normalization, providing MONDO identifiers and hierarchical relationships to bridge nomenclature differences across databases [13].</p>

  <table class="ieee-table">
    <caption>TABLE I: Primary Biological Evidence Sources and Reference Ontologies Integrated in CuraCascade</caption>
    <thead>
      <tr>
        <th>Resource Name</th>
        <th>Data Type & Functional Role</th>
        <th>Release / Version</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>ClinGen GCEP</td>
        <td>Gene-disease clinical validity curations (Definitive–Refuted)</td>
        <td>Q1 2024 Snapshot</td>
      </tr>
      <tr>
        <td>NCBI ClinVar</td>
        <td>Primary variant-level assertions, review stars, submitters</td>
        <td>Oct 2024 Archive</td>
      </tr>
      <tr>
        <td>PanelApp</td>
        <td>Diagnostic panel confidence indications (Green/Amber/Red)</td>
        <td>API v1 (2024)</td>
      </tr>
      <tr>
        <td>gnomAD v4.0</td>
        <td>Population allele frequencies & ancestry popmax</td>
        <td>v4.0.0</td>
      </tr>
      <tr class="total-row">
        <td>Mondo Ontology</td>
        <td>Reference disease ontology (concept crosswalk & hierarchy)</td>
        <td>v2024-03</td>
      </tr>
    </tbody>
  </table>

  <h2 class="ieee-sec">VI. Database Design and Evidence Integration</h2>
  <h3 class="ieee-subsec">A. Third Normal Form (3NF) Relational Modeling</h3>
  <p class="no-indent">To eliminate data redundancy, prevent update anomalies, and enforce referential integrity [14], CuraCascade specifies its relational schema in strict Third Normal Form (3NF). Eight normalized entities are established, as summarized in Table II: <code>genes</code>, <code>diseases</code>, <code>clingen_curations</code>, <code>clinvar_variants</code>, <code>panelapp_entries</code>, <code>disease_mappings</code>, <code>audit_findings</code>, and <code>provenance</code>.</p>

  <table class="ieee-table">
    <caption>TABLE II: CuraCascade 3NF Relational Schema Architecture and Constraints</caption>
    <thead>
      <tr>
        <th>Table Name</th>
        <th>Key / Uniqueness Constraint</th>
        <th>Referential Role & Clinical Content</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>genes</code></td>
        <td><code>gene_symbol</code> (PK)</td>
        <td>Central HGNC entity, accessions, downgrade flag</td>
      </tr>
      <tr>
        <td><code>diseases</code></td>
        <td><code>disease_id</code> (PK)</td>
        <td>MONDO/OMIM entities, epidemiology, inheritance</td>
      </tr>
      <tr>
        <td><code>clingen_curations</code></td>
        <td><code>uq_clingen_curation</code> (composite)</td>
        <td>Validity tiers, GCEP panel, appraisal date (<i>t</i><sub>CG</sub>)</td>
      </tr>
      <tr>
        <td><code>clinvar_variants</code></td>
        <td><code>variation_id</code> (PK)</td>
        <td>Variant assertions, review stars, submitters, AF</td>
      </tr>
      <tr>
        <td><code>panelapp_entries</code></td>
        <td><code>uq_panelapp_entry</code> (composite)</td>
        <td>Diagnostic panel confidence indications (Green)</td>
      </tr>
      <tr>
        <td><code>disease_mappings</code></td>
        <td><code>mapping_id</code> (PK)</td>
        <td>Concept crosswalk mapping external terms to MONDO</td>
      </tr>
      <tr>
        <td><code>audit_findings</code></td>
        <td><code>finding_id</code> (PK)</td>
        <td>Materialized discrepancy records (Classes A, B, C)</td>
      </tr>
      <tr class="total-row">
        <td><code>provenance</code></td>
        <td><code>provenance_id</code> (PK)</td>
        <td>Cryptographic SHA-256 logs, snapshot dates, counts</td>
      </tr>
    </tbody>
  </table>

  <h3 class="ieee-subsec">B. Integrity Enforcement and Ingestion Idempotency</h3>
  <p class="no-indent">Relational integrity is strictly enforced via transactional SQLite:</p>
  <p>• <code>PRAGMA foreign_keys = ON</code> guarantees that child records in curations, variants, and panels reference valid entries in <code>genes</code> and <code>diseases</code>.</p>
  <p>• Composite unique constraints <code>uq_clingen_curation</code> on <code>(gene_symbol, disease_id, moi, classification_date)</code> and <code>uq_panelapp_entry</code> on <code>(gene_symbol, panel_id)</code> enforce ingestion idempotency.</p>
  <p>• Repeated execution of the ingestion ETL pipeline produces zero duplicate records while appending tamper-evident cryptographic provenance logs.</p>

  <figure>
    <img src="{fig2}" alt="Disease-Aware Matching Workflow">
    <figcaption>Fig. 2. Disease-aware concept matching and discrepancy gating workflow. External strings are resolved through exact ontology crosswalks and distinct-phenotype exclusions to prevent false-positive discrepancy attribution in pleiotropic genes.</figcaption>
  </figure>

  <h2 class="ieee-sec">VII. Disease-Matching and Validation Methodology</h2>
  <h3 class="ieee-subsec">A. Disease-Aware Concept Matching</h3>
  <p class="no-indent">A naive approach that matches assertions purely on gene symbol will generate unacceptable false positives. Many genes are pleiotropic, exhibiting definitive causality for one disorder while having insufficient (Limited), conflicting (Disputed), or disproven (Refuted) evidence for an unrelated condition. For example, mismatch repair genes (<em>MLH1</em>, <em>MSH2</em>, <em>MSH6</em>, <em>PMS2</em>) are definitively causal for Lynch syndrome (colorectal/endometrial cancer), but have been refuted by ClinGen for hereditary breast carcinoma [7]. Naive gene-level matching would erroneously flag legitimate Lynch syndrome variants as discrepancies against breast cancer curations.</p>

  <p>As illustrated in Fig. 2, CuraCascade eliminates broad keyword overlap by enforcing a three-tier concept matching hierarchy:</p>
  <p>1) <em>Exact Concept Matching:</em> Cross-references standardized ontology identifiers (MONDO, OMIM, MedGen) directly between ClinGen and downstream records [13], [15].</p>
  <p>2) <em>Canonical Synonym Crosswalk:</em> Resolves established clinical synonyms (e.g., "Hypertrophic cardiomyopathy" &harr; "HCM", "Familial hypertrophic cardiomyopathy") via <code>CANONICAL_DISEASE_REGISTRY</code>.</p>
  <p>3) <em>Distinct Disorder Exclusions:</em> Implements explicit biological boundary rules (<code>DISTINCT_PHENOTYPE_EXCLUSIONS</code>) preventing cross-disease conflation in pleiotropic multi-disease genes.</p>
  <p>Assertions that fail exact or crosswalk matching are routed to <code>POTENTIAL_DISCREPANCY_REVIEW</code> rather than being prematurely asserted as clinical contradictions.</p>

  <h3 class="ieee-subsec">B. Discrepancy Taxonomy</h3>
  <p class="no-indent">Cross-layer discrepancies are categorized into three deterministic tiers:</p>
  <p>• <strong>Class A (Direct Clinical Discrepancy):</strong> Direct contradiction between an upstream downgrade (<em>Refuted</em>, <em>Disputed</em>, or <em>Limited</em>) and an active downstream pathogenic assertion (ClinVar P/LP variant or PanelApp Green indication) for a confirmed matching disease concept.</p>
  <p>• <strong>Class B (Indication Mismatch):</strong> Discordance involving borderline evidence tiers (e.g., PanelApp Amber/Red entries or Moderate curations).</p>
  <p>• <strong>Class C (Ambiguous / Data Quality):</strong> Assertions with missing disease identifiers, ambiguous phenotypic strings, or unmapped clinical terms.</p>

  <h2 class="ieee-sec">VIII. Implementation Details</h2>
  <p>CuraCascade is implemented in Python (3.11–3.13) and ANSI SQL. Core components include:</p>
  <p>• <strong>Database Connection Manager (<code>database/connection.py</code>):</strong> Implements context-managed, thread-safe connections with WAL journal mode, busy timeouts, and default read-only URI enforcement (<code>?mode=ro</code>).</p>
  <p>• <strong>Columnar Scanner (<code>database/duckdb_engine.py</code>):</strong> Leverages DuckDB to execute zero-copy vectorized aggregation queries across multi-million row variant tables [12].</p>
  <p>• <strong>Command-Line Interface (<code>run.py</code>):</strong> Headless CLI supporting <code>audit</code> (with filtering by gene, class, and severity; JSON/CSV/table export) and <code>verify</code> (automated database B-tree, foreign key, domain range, and SHA-256 integrity scanning).</p>
  <p>• <strong>Interactive Dashboard (<code>app.py</code>):</strong> Multi-page Streamlit analytical dashboard featuring real-time cohort filtering, latency exploration, and clinical dossier downloads.</p>

  <figure class="full-width">
    <img src="{fig3}" alt="Benchmark Confusion Matrix and Wilson CIs">
    <figcaption>Fig. 3. Independent benchmark evaluation results. (a) 2x2 confusion matrix heatmap for the evaluable cohort (N = 94), showing 18 True Positives, 0 False Positives, 34 False Negatives, and 42 True Negatives. (b) Performance metrics with 95% Wilson Score confidence intervals, illustrating 100.0% precision, 34.6% recall, 100.0% specificity, 63.8% accuracy, and concordance &kappa; = 0.3212.</figcaption>
  </figure>

  <h2 class="ieee-sec">IX. Experimental Setup and Results</h2>
  <h3 class="ieee-subsec">A. Independent Validation Benchmark Design</h3>
  <p class="no-indent">To evaluate audit accuracy without outcome leakage, an independent benchmark dataset (<code>benchmark_ground_truth.json</code>) comprising <strong>N = 100 gene–disease validity assertions</strong> was established:</p>
  <p>• <strong>54 Positive Benchmark Cases:</strong> Formally published ClinGen downgrades across qualitative tiers: <em>Limited</em> (N = 28; insufficient evidence), <em>Disputed</em> (N = 14; conflicting evidence), and <em>Refuted</em> (N = 12; evidence against validity), spanning cardiovascular, cancer, neurological, and metabolic diseases.</p>
  <p>• <strong>46 Negative Control Cases:</strong> Curated gene–disease pairs with <em>Definitive</em> or <em>Strong</em> validity where downstream pathogenic assertions represent valid biological signals.</p>
  <p>Adjudication was established via expert literature review with documented citations and MONDO identifiers. The automated audit rules evaluate live database join queries without access to gold labels.</p>

  <h3 class="ieee-subsec">B. Benchmark Evaluation Results</h3>
  <p class="no-indent">The evaluation pipeline was executed across both the primary evaluable cohort and an unadjusted sensitivity cohort. Results are detailed in Table III and Fig. 3.</p>

  <table class="ieee-table">
    <caption>TABLE III: Benchmark Evaluation Metrics: Evaluable Cohort vs. Sensitivity Analysis</caption>
    <thead>
      <tr>
        <th>Metric / Parameter</th>
        <th>Evaluable Cohort (N = 94)</th>
        <th>Sensitivity Cohort (N = 100)</th>
        <th>95% Wilson CI (Evaluable)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Total Benchmark Cases</td>
        <td>100</td>
        <td>100</td>
        <td>—</td>
      </tr>
      <tr>
        <td>Evaluable Cases</td>
        <td>94</td>
        <td>100 (Unadjusted)</td>
        <td>—</td>
      </tr>
      <tr>
        <td>Excluded Cases (<code>NOT_EVALUABLE</code>)</td>
        <td>6</td>
        <td>0</td>
        <td>—</td>
      </tr>
      <tr>
        <td>True Positives (TP)</td>
        <td>18</td>
        <td>18</td>
        <td>—</td>
      </tr>
      <tr>
        <td>False Positives (FP)</td>
        <td>0</td>
        <td>0</td>
        <td>—</td>
      </tr>
      <tr>
        <td>True Negatives (TN)</td>
        <td>42</td>
        <td>46</td>
        <td>—</td>
      </tr>
      <tr>
        <td>False Negatives (FN)</td>
        <td>34</td>
        <td>36</td>
        <td>—</td>
      </tr>
      <tr class="total-row">
        <td><strong>Precision (PPV)</strong></td>
        <td><strong>100.0%</strong></td>
        <td><strong>100.0%</strong></td>
        <td><strong>82.4% – 100.0%</strong></td>
      </tr>
      <tr class="total-row">
        <td><strong>Recall (Sensitivity)</strong></td>
        <td><strong>34.6%</strong></td>
        <td><strong>33.3%</strong></td>
        <td><strong>23.2% – 48.2%</strong></td>
      </tr>
      <tr class="total-row">
        <td><strong>Specificity (TNR)</strong></td>
        <td><strong>100.0%</strong></td>
        <td><strong>100.0%</strong></td>
        <td><strong>91.6% – 100.0%</strong></td>
      </tr>
      <tr class="total-row">
        <td><strong>Accuracy</strong></td>
        <td><strong>63.8%</strong></td>
        <td><strong>64.0%</strong></td>
        <td><strong>53.8% – 72.8%</strong></td>
      </tr>
      <tr>
        <td>F1-Score</td>
        <td>0.5143</td>
        <td>0.5000</td>
        <td>—</td>
      </tr>
      <tr>
        <td>Cohen's Kappa (&kappa;)</td>
        <td>0.3212</td>
        <td>0.3151</td>
        <td>—</td>
      </tr>
    </tbody>
  </table>

  <h3 class="ieee-subsec">C. Cohort Reconciliation & Handling of Absent Evidence</h3>
  <p class="no-indent">Of the 100 benchmark assertions, 94 were evaluable against local database records, while six cases were designated <code>NOT_EVALUABLE</code> due to absent evidence in the static public snapshot:</p>
  <p>• <em>XRCC3</em> (Gold = 1): Breast cancer curation and gene absent from ClinGen snapshot.</p>
  <p>• <em>DFNB59</em> (Gold = 1): Gene present in <code>genes</code>, but zero ClinGen curations ingested in snapshot.</p>
  <p>• <em>TSC1</em>, <em>TSC2</em>, <em>SMAD3</em>, <em>SMN1</em> (Gold = 0): Definitive controls whose gene and curation records were absent from snapshot.</p>
  <p>In the primary evaluable cohort (N = 94), snapshot coverage is 94.0%. In the unadjusted 100-case sensitivity analysis, treating all six unobserved cases under the conservative assumption of unflagged non-detections yields TP=18, FP=0, FN=36, TN=46, with precision maintained at 100.0% and recall at 33.3%.</p>

  <h3 class="ieee-subsec">D. Investigation of 34 False Negatives</h3>
  <p class="no-indent">The 34 false negatives in the primary evaluable cohort were investigated individually and partition into three distinct failure modes, summarized in Table IV:</p>
  <p>1) <em>Absent Downstream Assertions (N = 15 cases, 44.1%):</em> <em>ALPK3, KCNE3, FANCA, NLGN3, ARX, NRXN1, SCN2A, KCNQ2, PCDH19, GRIN2A, STXBP1, DYRK1A, SYNGAP1, ACADL, AGTR2</em>. ClinVar contains 0 P/LP variants and PanelApp contains 0 Green panels for these genes. An audit discrepancy cannot trigger when laboratories assert zero pathogenicity. CuraCascade correctly produces 0 alerts.</p>
  <p>2) <em>Target Curation Absent in ClinGen Snapshot (N = 3 cases, 8.8%):</em> <em>ACTN2</em> (HCM), <em>MECP2</em> (ASD), <em>SHANK3</em> (ASD). The ClinGen release file omitted the specific downgraded curation evaluated by the benchmark (e.g. <em>ACTN2</em> in HCM), containing only Definitive curations for other phenotypes.</p>
  <p>3) <em>Cross-Disease Finding Mismatch (N = 16 cases, 47.1%):</em> <em>CAV3, CSRP3, JPH2, ANK2, CACNA2D1, KCNE1, BARD1, RAD51C, CHEK2, GJB6, ABCA4, ABCB6, ABCC9, ACVR1, ADAM17, ADGRV1</em>. Discrepancy findings exist in the warehouse for other diseases (e.g., <em>ANK2</em> has active findings for CPVT, but benchmark targets Long QT syndrome; <em>BARD1</em> has ovarian cancer findings, but benchmark targets breast cancer). Conflating distinct diseases to inflate recall would violate biological specificity.</p>

  <table class="ieee-table">
    <caption>TABLE IV: Taxonomy and Failure Mode Analysis of the 34 False Negatives</caption>
    <thead>
      <tr>
        <th>Mechanism Category (N, %)</th>
        <th>Representative Genes & Scientific Handling</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Absent Downstream Assertions (15, 44.1%)</td>
        <td><em>ALPK3, KCNE3, FANCA, NLGN3, ARX, NRXN1, SCN2A, KCNQ2, PCDH19, GRIN2A, STXBP1, DYRK1A, SYNGAP1, ACADL, AGTR2</em>. 0 P/LP variants cataloged in ClinVar; correctly unflagged.</td>
      </tr>
      <tr>
        <td>Target Curation Absent (3, 8.8%)</td>
        <td><em>ACTN2</em> (HCM), <em>MECP2</em> (ASD), <em>SHANK3</em> (ASD). Specific downgraded curation absent from snapshot; correctly omitted from alerts.</td>
      </tr>
      <tr class="total-row">
        <td>Cross-Disease Mismatch (16, 47.1%)</td>
        <td><em>ANK2, BARD1, CHEK2, CAV3, CSRP3, JPH2, CACNA2D1, KCNE1, RAD51C, GJB6, ABCA4, ABCB6, ABCC9, ACVR1, ADAM17, ADGRV1</em>. Active findings exist for other diseases. Concept boundaries strictly preserved.</td>
      </tr>
    </tbody>
  </table>

  <h3 class="ieee-subsec">E. Verification of 18 True Positives and Zero False Positives</h3>
  <p class="no-indent">All 18 True Positives (<em>MYLK2, TCAP, MYOZ2, NEXN, VCL, KCNE2, SCN1B, GPD1L, KCNJ8, HCN4, TRPM4, BRIP1, NBN, RAD50, XRCC2, SLX4, A2ML1, AKAP9</em>) were verified against source records, demonstrating confirmed Class A matches between ClinGen downgrades and downstream P/LP assertions.</p>

  <p>Crucially, zero false positives was <strong>not</strong> achieved by suppressing findings. Multi-disease genes (<em>MLH1, MSH2, MSH6, PMS2, FBN1, MYH11, RYR2, KCNQ1, KCNH2, SCN5A, MYH7, MYBPC3</em>) maintain <strong>thousands of active discrepancy alerts</strong> in <code>audit_findings</code> (e.g., 1,954 <em>MLH1</em> breast cancer records, 2,191 <em>MSH2</em> records). They were properly unflagged only when evaluating their negative control phenotypes (Lynch syndrome).</p>

  <figure>
    <img src="{fig4}" alt="Empirical Cross-Sectional Latency Distribution">
    <figcaption>Fig. 4. Empirical cross-sectional latency distributions across 51,007 active ClinVar assertions in 536 curated genes. (a) Stratification by clinical specialty, showing shorter active latency in cardiovascular genetics compared to neurology (p &lt; 0.001). (b) Stratification by review confidence, showing significantly reduced active lag in multi-submitter consensus records (&ge; 2 stars) compared to single-submitter assertions (p &lt; 0.001).</figcaption>
  </figure>

  <h3 class="ieee-subsec">F. Empirical Cross-Sectional Latency Analysis</h3>
  <p class="no-indent">Evaluating active downstream assertions linked to downgraded ClinGen curations (N = 51,007 ClinVar variant assertions across 536 curated genes) revealed significant persistence in static repository archives (Fig. 4):</p>
  <p>• <strong>Overall Cohort:</strong> Median active elapsed duration of <strong>2.82 years</strong> (1,030 days; interquartile range [IQR]: 2.98 years / 1,087 days; 25th percentile: 684 days / 1.87 years; 75th percentile: 1,771 days / 4.85 years; mean &plusmn; SD: 3.56 &plusmn; 2.25 years).</p>
  <p>• <strong>Clinical Specialty Breakdown:</strong> Cardiovascular reappraisals exhibit significantly shorter active elapsed duration (median 1.39 years; N = 14,551) than neurology (median 4.85 years; N = 6,288) and hereditary cancer (median 2.80 years; N = 15,404; Kruskal–Wallis p &lt; 0.001).</p>
  <p>• <strong>Review Confidence Stratification:</strong> Multi-submitter consensus records (&ge; 2 stars) persist for significantly shorter duration (median 1.84 years; N = 18,650) than single-submitter unreviewed records (median 3.15 years; N = 32,357; Mann–Whitney <i>U</i> = 300,922,517.5, p &lt; 0.001).</p>
  <p>Importantly, these measurements represent cross-sectional elapsed time (dwell time) of active unresolved assertions within a static database snapshot, rather than a longitudinal time-to-reclassification study. All observations are right-censored at the snapshot date; true survival modeling of reclassification dynamics requires multi-year submission revision snapshots.</p>

  <h3 class="ieee-subsec">G. Exploratory Machine Learning Screening</h3>
  <p class="no-indent">An exploratory Random Forest classifier was evaluated to assess cross-sectional downgrade vulnerability across 3,833 genes and 51,025 variants. The model achieved an AUROC of 0.857 and Precision@Top-20% of 75.8% (Brier score: 0.1508; Logistic Regression baseline: 0.1348) [16], [17]. Feature importance was dominated by low ClinVar star ratio (70.2%) and non-green PanelApp indications (26.0%).</p>

  <p>Because features were extracted from cross-sectional snapshots available post-curation, the model is subject to potential retrospective look-ahead leakage. Consequently, model scores are designated as <strong>uncalibrated risk priority indices</strong>, and prospective predictive claims remain disabled pending longitudinal historical archive extraction.</p>

  <h2 class="ieee-sec">X. Discussion and Limitations</h2>
  <p>The empirical findings of CuraCascade demonstrate that unpropagated gene refutations persist in diagnostic repositories for years, presenting a potential source of diagnostic friction. The primary limitations, operational boundaries, and governance constraints of the framework are summarized in Table V.</p>

  <table class="ieee-table">
    <caption>TABLE V: Technical Limitations, Operational Boundaries, and Research Governance</caption>
    <thead>
      <tr>
        <th>Limitation Dimension</th>
        <th>Operational Impact & Architectural Trade-Off</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Low Benchmark Recall (34.6%)</td>
        <td>Prioritizes 100% precision over recall to prevent false-positive diagnostic alerts. Misses arise from 0 laboratory assertions (15 cases) and cross-disease boundaries (16 cases).</td>
      </tr>
      <tr>
        <td>Single-Curator Gold Labels</td>
        <td>Benchmark adjudicated by a single reviewer. Multi-rater consensus kappa (&kappa;) is marked N/A pending blinded dual re-annotation [18].</td>
      </tr>
      <tr>
        <td>Cross-Sectional Latency</td>
        <td>Measures active elapsed dwell time of unresolved discordance in static snapshots; true longitudinal resolution hazards require historical XML archives.</td>
      </tr>
      <tr>
        <td>Retrospective ML Features</td>
        <td>Machine learning scores represent exploratory priority indices subject to potential temporal look-ahead leakage; formal calibration is absent.</td>
      </tr>
      <tr class="total-row">
        <td>Snapshot Availability</td>
        <td>Six benchmark cases designated <code>NOT_EVALUABLE</code> due to absent records in public data dumps.</td>
      </tr>
    </tbody>
  </table>

  <h3 class="ieee-subsec">A. The Recall–Precision Trade-Off in Clinical Auditing</h3>
  <p class="no-indent">In clinical diagnostic auditing, the cost of a false positive (flagging a valid gene as refuted and withholding life-saving diagnoses) is catastrophic. By removing broad keyword overlap and enforcing strict concept crosswalks, CuraCascade eliminated all 12 previously observed false positives, achieving 100.0% precision (95% CI: 82.4%–100.0%) [19]. The resulting recall of 34.6% reflects genuine biological boundaries: an audit system should not flag an alert when clinical laboratories have already classified variants as Benign, nor should it flag Long QT syndrome based on CPVT variants.</p>

  <h2 class="ieee-sec">XI. Ethical Considerations and Intended Use</h2>
  <p>CuraCascade is designed strictly as an automated research audit and prioritization framework, not an autonomous clinical diagnostic system. The platform outputs advisory discrepancy alerts intended to guide clinical laboratory geneticists and curation expert panels during routine re-evaluation cycles. CuraCascade does not establish biological causality, does not declare variants intrinsically benign, and should never be used as a substitute for professional clinical geneticist evaluation.</p>

  <h2 class="ieee-sec">XII. Conclusion and Future Work</h2>
  <p>CuraCascade establishes an open-source, 3NF relational data warehouse and automated discrepancy audit engine to address clinical evidence synchronization lag across biomedical registries. By clearly distinguishing ClinGen evidence tiers (<em>Limited</em>, <em>Disputed</em>, and <em>Refuted</em>) and enforcing disease-aware concept matching, the framework achieves 100.0% precision on an independently evaluated benchmark, while empirical cross-sectional analysis reveals that active downstream contradictions persist for a median of 2.82 years across major repositories.</p>

  <p>Future development will focus on:</p>
  <p>1) Ingesting longitudinal historical ClinVar and ClinGen XML revision dumps to reconstruct point-in-time features for prospective survival modeling.</p>
  <p>2) Conducting multi-rater blinded consensus re-adjudication across the 100-gene benchmark to establish inter-rater reliability.</p>
  <p>3) Integrating HL7 FHIR Genomics standard interfaces for automated electronic health record (EHR) laboratory alerting.</p>

  <h2 class="ieee-sec">Reproducibility & Verification</h2>
  <p class="no-indent">All source code, schemas, and reproduction scripts are open-source under the MIT License at https://github.com/uditshokeen14/curacascade. The complete test suite (47 automated tests) executes via <code>pytest -v</code>. Database integrity and cryptographic SHA-256 provenance are verified via <code>python run.py verify</code>. Benchmark evaluation is reproduced via <code>python -m pipeline.validation_benchmark</code>.</p>

  <h2 class="ieee-sec">References</h2>
  <div class="ref-list">
    <div class="ref-item">[1] A. E. Strande <em>et al.</em>, "Evaluating the clinical validity of gene-disease associations: an evidence-based framework developed by the Clinical Genome Resource," <em>Genet. Med.</em>, vol. 19, no. 7, pp. 868–874, 2017. DOI: 10.1038/gim.2017.37.</div>
    <div class="ref-item">[2] S. Richards <em>et al.</em>, "Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the ACMG and AMP," <em>Genet. Med.</em>, vol. 17, no. 5, pp. 405–424, 2015. DOI: 10.1038/gim.2015.30.</div>
    <div class="ref-item">[3] H. L. Rehm <em>et al.</em>, "ClinGen—The Clinical Genome Resource," <em>N. Engl. J. Med.</em>, vol. 372, no. 23, pp. 2235–2242, 2015. DOI: 10.1056/NEJMsr1406261.</div>
    <div class="ref-item">[4] M. A. Kelly <em>et al.</em>, "Adaptation and validation of the ClinGen clinical validity framework for cardiomyopathy genes," <em>Am. J. Med. Genet. C Semin. Med. Genet.</em>, vol. 178, no. 1, pp. 100–108, 2018. DOI: 10.1002/ajmg.c.31600.</div>
    <div class="ref-item">[5] J. Ingles <em>et al.</em>, "Evaluating the clinical validity of hypertrophic cardiomyopathy genes," <em>Circ. Genom. Precis. Med.</em>, vol. 12, no. 2, p. e002460, 2019. DOI: 10.1161/CIRCGEN.119.002460.</div>
    <div class="ref-item">[6] L. Hosseini <em>et al.</em>, "Reappraisal of reported genes for Brugada syndrome: an evidence-based evaluation by the ClinGen Brugada Syndrome GCEP," <em>Am. J. Med. Genet. A</em>, vol. 176, no. 12, pp. 2577–2585, 2018. DOI: 10.1002/ajmg.a.40656.</div>
    <div class="ref-item">[7] K. Lee <em>et al.</em>, "Clinical actionability of gene-disease associations: Lessons learned from ClinGen and cancer susceptibility panels," <em>J. Mol. Diagn.</em>, vol. 21, no. 4, pp. 588–597, 2019. DOI: 10.1016/j.jmoldx.2019.04.004.</div>
    <div class="ref-item">[8] M. J. Landrum <em>et al.</em>, "ClinVar: improvements to access, data extraction and curation," <em>Nucleic Acids Res.</em>, vol. 48, no. D1, pp. D835–D844, 2020. DOI: 10.1093/nar/gkz972.</div>
    <div class="ref-item">[9] A. R. Martin <em>et al.</em>, "PanelApp crowdsources expert knowledge to establish consensus diagnostic gene panels," <em>Genet. Med.</em>, vol. 21, no. 8, pp. 1912–1921, 2019. DOI: 10.1038/s41436-019-0619-3.</div>
    <div class="ref-item">[10] C. F. Wright <em>et al.</em>, "Genetic diagnosis of developmental disorders in the DDD study: a scalable analysis of genome-wide research data," <em>Lancet</em>, vol. 385, no. 9975, pp. 1305–1314, 2015. DOI: 10.1016/S0140-6736(14)61705-0.</div>
    <div class="ref-item">[11] K. J. Karczewski <em>et al.</em>, "The mutational constraint spectrum quantified from variation in 141,456 humans," <em>Nature</em>, vol. 581, no. 7809, pp. 434–443, 2020. DOI: 10.1038/s41586-020-2308-7.</div>
    <div class="ref-item">[12] M. Raasveldt and H. Mühleisen, "DuckDB: an Embeddable Analytical Database," in <em>Proc. ACM SIGMOD Int. Conf. Manage. Data</em>, 2019, pp. 1981–1984. DOI: 10.1145/3299869.3320212.</div>
    <div class="ref-item">[13] N. A. Vasilevsky <em>et al.</em>, "Mondo: unifying diseases for the world, by the world," <em>Nucleic Acids Res.</em>, vol. 50, no. D1, pp. D1248–D1259, 2022. DOI: 10.1093/nar/gkac1072.</div>
    <div class="ref-item">[14] E. F. Codd, "A relational model of data for large shared data banks," <em>Commun. ACM</em>, vol. 13, no. 6, pp. 377–387, 1970. DOI: 10.1145/362384.362685.</div>
    <div class="ref-item">[15] J. S. Amberger <em>et al.</em>, "OMIM.org: Online Mendelian Inheritance in Man," <em>Nucleic Acids Res.</em>, vol. 47, no. D1, pp. D1038–D1043, 2019. DOI: 10.1093/nar/gky1151.</div>
    <div class="ref-item">[16] F. Pedregosa <em>et al.</em>, "Scikit-learn: Machine learning in Python," <em>J. Mach. Learn. Res.</em>, vol. 12, pp. 2825–2830, 2011.</div>
    <div class="ref-item">[17] M. N. Wright and A. Ziegler, "ranger: A fast implementation of random forests for high dimensional data in C++ and R," <em>Bioinformatics</em>, vol. 33, no. 14, pp. 2197–2199, 2015. DOI: 10.1093/bioinformatics/btv738.</div>
    <div class="ref-item">[18] J. Cohen, "A coefficient of agreement for nominal scales," <em>Educ. Psychol. Meas.</em>, vol. 20, no. 1, pp. 37–46, 1960. DOI: 10.1177/001316446002000104.</div>
    <div class="ref-item">[19] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," <em>J. Am. Stat. Assoc.</em>, vol. 22, no. 158, pp. 209–212, 1927. DOI: 10.1080/01621459.1927.10502053.</div>
  </div>

</div>

</body>
</html>
"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML source written to {HTML_PATH}")


def render_pdf_via_chromium():
    chrome_bin = None
    for p in CHROME_PATHS:
        if p.exists():
            chrome_bin = p
            break

    if not chrome_bin:
        raise FileNotFoundError("Chromium / Google Chrome executable not found in standard system locations.")

    print(f"Using Chrome binary: {chrome_bin}")
    cmd = [
        str(chrome_bin),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={PDF_PATH}",
        str(HTML_PATH),
    ]

    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print("Headless Chrome PDF export completed successfully.")
    print(f"Exported PDF: {PDF_PATH}")


def verify_pdf():
    reader = pypdf.PdfReader(PDF_PATH)
    num_pages = len(reader.pages)
    print(f"Verified PDF page count: {num_pages} pages")
    first_page_text = reader.pages[0].extract_text()
    assert "CuraCascade" in first_page_text, "Title missing from page 1"
    assert "23BCB0001" in first_page_text, "Registration number missing from page 1"
    assert "udit.shokeen2023@vitstudent.ac.in" in first_page_text, "College email missing from page 1"
    print("Content verification passed: Title, Reg No, and Email verified on Page 1.")


if __name__ == "__main__":
    build_html()
    render_pdf_via_chromium()
    verify_pdf()
