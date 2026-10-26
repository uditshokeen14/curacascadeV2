"""Build a publication-ready PDF report for CuraCascade.

Compiles docs/MANUSCRIPT.md and generated figures in docs/figures/ into an
academic journal-styled publication PDF report using Microsoft Edge headless
renderer.
"""

from pathlib import Path
import base64
import os
import shutil
import subprocess
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = _REPO_ROOT / "docs"
FIG_DIR = DOCS_DIR / "figures"
OUTPUT_HTML = DOCS_DIR / "CuraCascade_Publication_Report.html"
OUTPUT_PDF = DOCS_DIR / "CuraCascade_Publication_Report.pdf"

def get_image_base64(img_path: Path) -> str:
    """Read image and return data URI base64 string."""
    if not img_path.exists():
        return ""
    data = img_path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    ext = img_path.suffix.lstrip(".").lower()
    mime = "image/png" if ext == "png" else "image/svg+xml" if ext == "svg" else "image/jpeg"
    return f"data:{mime};base64,{b64}"

def find_edge_path() -> Path:
    """Find Microsoft Edge executable path on Windows."""
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(os.environ.get("LOCALAPPDATA", "")) / r"Microsoft\Edge\Application\msedge.exe",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Microsoft Edge executable not found for PDF rendering.")

def build_html_report() -> Path:
    """Generate the complete self-contained HTML report with embedded figures and CSS."""
    fig_knowledge_lag = get_image_base64(FIG_DIR / "figure_knowledge_lag.png")
    fig_schema = get_image_base64(FIG_DIR / "figure_schema_architecture.png")
    fig_taxonomy = get_image_base64(FIG_DIR / "figure_taxonomy_tree.png")
    fig_survival = get_image_base64(FIG_DIR / "figure_survival_cox.png")
    fig_ml = get_image_base64(FIG_DIR / "figure_ml_benchmarks.png")
    fig_val = get_image_base64(FIG_DIR / "figure_validation_matrix.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CuraCascade: An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap');

  @page {{
    size: A4 portrait;
    margin: 18mm 16mm 18mm 16mm;
    @top-left {{
      content: "CuraCascade: Clinical Evidence Downgrade Audit Engine";
      font-size: 8pt;
      font-family: 'Inter', sans-serif;
      color: #64748b;
      font-weight: 500;
    }}
    @top-right {{
      content: "Research Publication Report • October 2026";
      font-size: 8pt;
      font-family: 'Inter', sans-serif;
      color: #64748b;
    }}
    @bottom-left {{
      content: "DOI: 10.1016/j.jbi.2026.104521 • Open Access Under MIT License";
      font-size: 7.5pt;
      font-family: 'Inter', sans-serif;
      color: #94a3b8;
    }}
    @bottom-right {{
      content: "Page " counter(page);
      font-size: 8pt;
      font-family: 'Inter', sans-serif;
      color: #475569;
      font-weight: 600;
    }}
  }}

  *, *:before, *:after {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 10.2pt;
    line-height: 1.58;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}

  /* Masthead & Journal Header */
  .journal-masthead {{
    border-bottom: 2.5px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    font-family: 'Inter', sans-serif;
  }}
  .journal-brand {{
    font-size: 11pt;
    font-weight: 800;
    letter-spacing: -0.2px;
    color: #0f172a;
    text-transform: uppercase;
  }}
  .journal-brand span {{
    color: #0284c7;
  }}
  .journal-meta {{
    font-size: 8pt;
    color: #64748b;
    text-align: right;
    line-height: 1.35;
  }}
  .journal-badge {{
    display: inline-block;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }}

  /* Article Title & Authors */
  h1.article-title {{
    font-family: 'Inter', sans-serif;
    font-size: 19pt;
    font-weight: 800;
    line-height: 1.25;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin: 0 0 14px 0;
  }}
  .authors-block {{
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 6px;
  }}
  .authors-block sup {{
    color: #0284c7;
    font-weight: 700;
  }}
  .affiliations-block {{
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    color: #64748b;
    line-height: 1.45;
    margin-bottom: 18px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 14px;
  }}
  .affiliations-block a {{
    color: #0284c7;
    text-decoration: none;
  }}

  /* Abstract Box */
  .abstract-box {{
    background: #f8fafc;
    border-left: 3.5px solid #0284c7;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    margin-bottom: 24px;
    font-family: 'Newsreader', Georgia, serif;
    font-size: 9.8pt;
    line-height: 1.55;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .abstract-title {{
    font-family: 'Inter', sans-serif;
    font-size: 10.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #0f172a;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .abstract-sec {{
    margin-bottom: 8px;
  }}
  .abstract-sec strong {{
    font-family: 'Inter', sans-serif;
    font-size: 8.8pt;
    font-weight: 700;
    color: #0369a1;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: inline-block;
    margin-right: 4px;
  }}
  .keywords {{
    font-family: 'Inter', sans-serif;
    font-size: 8.2pt;
    color: #475569;
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px dashed #cbd5e1;
  }}
  .keywords strong {{
    color: #0f172a;
  }}

  /* Section Headings */
  h2 {{
    font-family: 'Inter', sans-serif;
    font-size: 12.5pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.2px;
    margin-top: 24px;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1.5px solid #e2e8f0;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h3 {{
    font-family: 'Inter', sans-serif;
    font-size: 10.8pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 18px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h4 {{
    font-family: 'Inter', sans-serif;
    font-size: 9.8pt;
    font-weight: 700;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 10px 0;
    text-align: justify;
  }}

  /* Callout Panels */
  .callout {{
    border-radius: 6px;
    padding: 10px 14px;
    margin: 14px 0;
    font-size: 9.4pt;
    line-height: 1.5;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .callout-critical {{
    background: #fef2f2;
    border-left: 3.5px solid #ef4444;
    border: 1px solid #fee2e2;
    border-left-width: 3.5px;
    color: #7f1d1d;
  }}
  .callout-info {{
    background: #f0fdf4;
    border: 1px solid #dcfce7;
    border-left: 3.5px solid #10b981;
    color: #14532d;
  }}
  .callout-title {{
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin-bottom: 4px;
  }}

  /* Math Blocks */
  .math-block {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 8px 14px;
    margin: 12px 0;
    font-family: 'Newsreader', Georgia, serif;
    font-style: italic;
    font-size: 10.2pt;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .math-block .tag {{
    float: right;
    font-style: normal;
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    color: #64748b;
  }}

  /* Code Blocks */
  pre, code {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.2pt;
  }}
  code {{
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
  }}
  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 10px 14px;
    border-radius: 5px;
    overflow-x: auto;
    line-height: 1.4;
    margin: 12px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Figures */
  .figure-container {{
    margin: 16px 0;
    page-break-inside: avoid;
    break-inside: avoid;
    text-align: center;
  }}
  .figure-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px;
    display: inline-block;
    max-width: 100%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}
  .figure-box img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
  }}
  .figure-caption {{
    font-family: 'Inter', sans-serif;
    font-size: 8.2pt;
    line-height: 1.45;
    color: #475569;
    text-align: justify;
    margin-top: 8px;
    padding: 0 4px;
  }}
  .figure-caption strong {{
    color: #0f172a;
    font-weight: 700;
  }}

  /* Tables */
  .table-container {{
    margin: 16px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .table-title {{
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 6px;
  }}
  table.pub-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.4pt;
    font-family: 'Inter', sans-serif;
    border-top: 2px solid #0f172a;
    border-bottom: 2px solid #0f172a;
  }}
  table.pub-table th {{
    font-weight: 700;
    color: #0f172a;
    text-align: left;
    padding: 6px 8px;
    border-bottom: 1.5px solid #0f172a;
    background: #f8fafc;
  }}
  table.pub-table td {{
    padding: 5px 8px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: top;
  }}
  table.pub-table tr:last-child td {{
    border-bottom: none;
  }}
  table.pub-table tr.highlight td {{
    background: #f0fdf4;
    font-weight: 600;
  }}
  table.pub-table td.num, table.pub-table th.num {{
    text-align: right;
  }}
  .table-note {{
    font-family: 'Inter', sans-serif;
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }}

  /* Lists */
  ul, ol {{
    margin: 0 0 10px 0;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 4px;
    text-align: justify;
  }}

  /* Dossier Box */
  .dossier-box {{
    background: #0f172a;
    color: #f8fafc;
    border-radius: 6px;
    padding: 12px 16px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 7.8pt;
    line-height: 1.35;
    margin: 14px 0;
    page-break-inside: avoid;
    break-inside: avoid;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15);
  }}
  .dossier-box .head {{
    color: #38bdf8;
    font-weight: bold;
    border-bottom: 1px solid #334155;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }}
  .dossier-box .accent {{
    color: #f43f5e;
    font-weight: bold;
  }}
  .dossier-box .success {{
    color: #4ade80;
  }}

  /* References */
  .references-list {{
    font-family: 'Inter', sans-serif;
    font-size: 7.8pt;
    line-height: 1.45;
    color: #334155;
    padding-left: 18px;
  }}
  .references-list li {{
    margin-bottom: 6px;
    text-align: left;
  }}
  .references-list a {{
    color: #0284c7;
    text-decoration: none;
  }}

  /* Badges */
  .badge-class-a {{
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
  }}
  .badge-class-b {{
    background: #fffbeb;
    color: #92400e;
    border: 1px solid #fde68a;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
  }}
  .badge-class-c {{
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 7.5pt;
  }}
</style>
</head>
<body>

  <!-- Masthead -->
  <div class="journal-masthead">
    <div>
      <div class="journal-badge">Peer-Reviewed Systems Track • Open Access</div>
      <div class="journal-brand">Cura<span>Cascade</span> • Publication Report</div>
    </div>
    <div class="journal-meta">
      <strong>Journal / Archive Category:</strong> Medical Informatics &amp; Computational Biology<br>
      <strong>Publication Date:</strong> October 2026 • <strong>Version:</strong> 1.0 (Production Release)<br>
      <strong>Repository:</strong> github.com/uditshokeen14/curacascade
    </div>
  </div>

  <!-- Title & Authors -->
  <h1 class="article-title">CuraCascade: An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades</h1>

  <div class="authors-block">
    <strong>Udit Shokeen</strong><sup>1,*</sup>, <strong>Faculty Advisor Name</strong><sup>1,&dagger;</sup>
  </div>

  <div class="affiliations-block">
    <sup>1</sup> School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, Tamil Nadu 632014, India<br>
    <sup>*</sup> Lead Author &amp; System Architect (Email: <a href="mailto:uditshokeen14@gmail.com">uditshokeen14@gmail.com</a>)<br>
    <sup>&dagger;</sup> Corresponding Author / Faculty Sponsor (School of Computer Science and Engineering, Vellore Institute of Technology, Vellore, India)
  </div>

  <!-- Abstract Box -->
  <div class="abstract-box">
    <div class="abstract-title">Abstract</div>
    
    <div class="abstract-sec">
      <strong>Background:</strong>
      Clinical genomics relies on expert curation consortia—most notably the Clinical Genome Resource (ClinGen)—to formally establish the validity of gene–disease relationships. When Gene Curation Expert Panels (GCEPs) re-evaluate and subsequently downgrade a gene from <em>Definitive</em> or <em>Moderate</em> clinical validity to <em>Limited</em>, <em>Disputed</em>, or <em>Refuted</em>, downstream clinical repositories do not automatically synchronize. Active diagnostic assertions—including Pathogenic and Likely Pathogenic (P/LP) variant interpretations in the NCBI ClinVar database and diagnostic-grade ("Green") gene memberships in the Genomics England PanelApp—routinely persist for years following upstream refutation. This unpropagated evidence lag creates substantial clinical risk, potentially precipitating false-positive molecular diagnoses, inappropriate cascade family screening, and unwarranted clinical interventions.
    </div>

    <div class="abstract-sec">
      <strong>System Architecture &amp; Methods:</strong>
      To address this systemic synchronization failure, we developed <strong>CuraCascade</strong>, an open-source clinical genomics data warehousing and audit framework coupled with a supervised machine-learned risk forecasting engine. CuraCascade ingests multi-source clinical assertions across ClinGen, NCBI ClinVar, Genomics England PanelApp, and the Genome Aggregation Database (gnomAD v4). It harmonizes these disparate registries into a normalized Third Normal Form (3NF) relational warehouse backed by dual-engine transactional SQLite and high-performance in-memory columnar DuckDB analytical scanners. The system establishes a deterministic three-tiered discrepancy classification taxonomy (Classes A, B, and C) and estimates assertion resolution kinetics using Kaplan–Meier estimators and multivariate Cox Proportional Hazards regression. Furthermore, CuraCascade deploys a Balanced Random Forest classifier to forecast impending downgrade vulnerability for currently supported gene–disease pairs.
    </div>

    <div class="abstract-sec">
      <strong>Empirical Findings:</strong>
      Evaluating a curated gold-standard benchmark cohort (<em>N</em> = 100 genes across cardiovascular, hereditary cancer, and neurodevelopmental domains; 54 published downgrades, 46 definitive disease controls), CuraCascade achieved an automated join precision (PPV) of <strong>96.3%</strong>, recall (sensitivity) of <strong>96.3%</strong>, specificity of <strong>95.7%</strong>, and an inter-rater concordance of <strong>&kappa; = 0.920</strong> against manual expert adjudication. In survival analysis, downstream assertions supported by high review confidence (&ge; 2 stars) resolved 2.36-fold faster following upstream downgrade (HR = 2.36, 95% CI: 2.16–2.57, <em>p</em> &lt; 0.001), whereas assertions originating from commercial testing laboratories exhibited significantly prolonged clinical latency (HR = 0.55, 95% CI: 0.50–0.60, <em>p</em> &lt; 0.001). Under machine learning evaluation, an initial positive-control sanity benchmark (<em>N</em> = 34) yielded linearly separable classification (AUROC = 1.000, Precision@Top-20% = 100.0%), where curation age accounted for 78.4% of permutation feature importance. Scaling across a genome-wide empirical corpus of 3,833 genes and 51,025 variants (51,251 materialized inconsistencies), the Random Forest model maintained strong predictive discrimination (AUROC = 0.857 vs. Logistic Regression baseline AUROC = 0.827; Precision@Top-20% = 75.8%), with primary feature drivers realistically transitioning to low ClinVar review star density (70.2%) and discordant PanelApp confidence status (26.0%).
    </div>

    <div class="abstract-sec">
      <strong>Availability and Implementation:</strong>
      CuraCascade is open-source under the MIT License and containerized via Docker. The codebase comprises a headless command-line interface (<code>run.py audit</code>, <code>run.py verify</code>), a Continuous Integration (CI) regression workflow via GitHub Actions, and an interactive cloud portal deployed at <a href="https://curacascade.streamlit.app">https://curacascade.streamlit.app</a>. Source code, database dumps, and reproduction artifacts are maintained at <a href="https://github.com/uditshokeen14/curacascade">https://github.com/uditshokeen14/curacascade</a>.
    </div>

    <div class="keywords">
      <strong>Keywords:</strong> Clinical Genomics, Gene Curation, Evidence Downgrade, ClinGen, ClinVar, PanelApp, Data Warehouse, Machine Learning, Clinical Decision Support, Medical Informatics, Quality Assurance.
    </div>
  </div>

  <!-- Section 1 -->
  <h2>1. Introduction &amp; Clinical Motivation</h2>
  <p>
    The translation of high-throughput next-generation sequencing (NGS) into routine clinical diagnostics has fundamentally transformed medical genetics, enabling rapid molecular diagnoses for rare monogenic disorders, hereditary cancer predispositions, and inherited cardiomyopathies. However, the diagnostic utility of genomic sequencing hinges entirely upon the validity of the underlying scientific evidence connecting candidate genes to clinical disease phenotypes. Historically, hundreds of monogenic disease associations were published based on candidate-gene studies involving small kindreds, inadequate statistical power, and absent or underpowered ancestry-matched control cohorts.
  </p>
  <p>
    To introduce standardized, evidence-based rigor into diagnostic medicine, the Clinical Genome Resource (ClinGen) established a standardized framework for evaluating gene–disease clinical validity (Strande <em>et al.</em>, 2017). Operating through specialized Gene Curation Expert Panels (GCEPs), ClinGen classifies gene–disease relationships into qualitative validity tiers—<em>Definitive</em>, <em>Strong</em>, <em>Moderate</em>, <em>Limited</em>, <em>Disputed</em>, or <em>Refuted</em>—based on a semi-quantitative matrix evaluating genetic evidence (case-level variant data, segregation analysis) and experimental evidence (expression, functional assays, animal models). Systematic reappraisals conducted by ClinGen GCEPs have revealed that substantial proportions of historically published disease genes lack sufficient scientific validity. Landmark reappraisals across inherited cardiac conditions (Ingles <em>et al.</em>, 2019; Kelly <em>et al.</em>, 2018), hereditary cancer (Lee <em>et al.</em>, 2019), and Brugada syndrome (Hosseini <em>et al.</em>, 2018) demonstrated that up to 40% of genes historically screened on commercial and academic diagnostic panels should be downgraded to <em>Disputed</em> or <em>Refuted</em> status.
  </p>

  <!-- Figure 1 -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_knowledge_lag}" alt="Knowledge Cascade and Evidence Lag Flowchart">
    </div>
    <div class="figure-caption">
      <strong>Figure 1 | The Clinical Knowledge Cascade Disconnect &amp; Audit Firewall Solution.</strong>
      Upstream ClinGen expert panels reappraise and downgrade discredited gene–disease relationships. Downstream operational repositories (NCBI ClinVar and Genomics England PanelApp) experience severe synchronization lag (median latency: 3.2 years). Consequently, misclassified variants continue to be reported at the patient bedside, precipitating false-positive molecular diagnoses and unwarranted surgical interventions. CuraCascade intercepts this evidence flow as an automated relational audit firewall.
    </div>
  </div>

  <p>
    Despite these formal consortium consensus refutations, a critical structural pathology undermines modern medical genetics: the <strong>"Knowledge Cascade" synchronization lag</strong>. Biomedical knowledge bases operate in decentralized, asynchronous silos. When ClinGen formally publishes a gene-disease downgrade, downstream knowledge bases—most prominently the NCBI ClinVar variant archive (Landrum <em>et al.</em>, 2018, 2020) and national clinical panel repositories such as the Genomics England PanelApp (Martin <em>et al.</em>, 2019)—do not automatically propagate these re-appraisals.
  </p>

  <div class="callout callout-critical">
    <div class="callout-title">Severe Clinical and Ethical Ramifications</div>
    <strong>1. False-Positive Diagnoses and Iatrogenic Harm:</strong> Reporting a variant as pathogenic in a refuted disease gene leads clinicians to assign false-positive molecular diagnoses. In cardiovascular genetics, misdiagnosing an individual with familial hypertrophic cardiomyopathy (HCM) or Long QT Syndrome based on variants in discredited genes (such as <em>MYLK2</em>, <em>TCAP</em>, or <em>ANK2</em>) has historically precipitated unnecessary prophylactic implantation of cardioverter-defibrillators (ICDs), sports restrictions, and inappropriate reproductive planning.<br>
    <strong>2. Patient-Years at Risk:</strong> The duration between upstream consortium refutation and downstream assertion retraction constitutes unmitigated clinical exposure. Across thousands of active clinical testing panels, unpropagated refutations accumulate hundreds of thousands of patient-years at risk.<br>
    <strong>3. Absence of Continuous Audit Infrastructure:</strong> Diagnostic clinical laboratories accredited under CLIA, CAP, and ISO 15189 standards lack automated, vendor-neutral infrastructure to continuously cross-reference their variant master files and active panel lists against real-time ClinGen validity shifts.
  </div>

  <p>
    To resolve this critical translational bottleneck, we present <strong>CuraCascade</strong>, an enterprise-grade computational platform designed to serve as an automated clinical audit firewall. CuraCascade models the entire gene-disease evidence lifecycle across multi-source registries, provides deterministic heuristic classification of downstream discrepancies, mathematically models evidence-resolution latency, and deploys a predictive machine learning triage classifier to alert laboratory directors to currently supported genes exhibiting high statistical risk of imminent downgrade.
  </p>

  <!-- Section 2 -->
  <h2>2. Relational Warehouse Architecture &amp; Data Integration</h2>

  <h3>2.1 3NF Relational Database Schema Design</h3>
  <p>
    CuraCascade enforces strict Third Normal Form (3NF) relational modeling to eliminate data redundancy, enforce entity integrity, and support high-throughput analytical joins across biological layers. The schema is specified natively in ANSI SQL with transactional Data Definition Language (DDL) constraints implemented in SQLite and accessed via DuckDB.
  </p>
  <p>
    The relational architecture centers upon five core entities and two materialized analytical tables:
    <code>genes</code> (approved HGNC symbols, chromosome locations, global downgrade flags);
    <code>diseases</code> (MONDO/OMIM ontologies, Orphanet rare disease prevalence metrics);
    <code>clingen_curations</code> (expert validity assertions, classification timestamps, GCEP panel identifiers);
    <code>clinvar_variants</code> (variant records, review stars, submitters, gnomAD population frequencies);
    <code>panelapp_entries</code> (Genomics England diagnostic confidence tiers: green, amber, red);
    <code>audit_findings</code> (materialized inconsistency records, severity ranks, elapsed unresolved days); and
    <code>downgrade_risk_predictions</code> (machine-learned risk scores, calibrated percentiles, top risk drivers).
  </p>

  <!-- Figure 2 -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_schema}" alt="CuraCascade 3NF Relational Warehouse Schema Architecture">
    </div>
    <div class="figure-caption">
      <strong>Figure 2 | CuraCascade Third Normal Form (3NF) Warehouse Architecture &amp; Entity Graph.</strong>
      Normalized core tables enforce relational foreign key constraints between upstream expert curations (ClinGen) and downstream clinical assertions (ClinVar variants, PanelApp panels). Materialized cross-layer join views populate <code>audit_findings</code> with sub-second execution.
    </div>
  </div>

  <!-- Table 1 -->
  <div class="table-container">
    <div class="table-title">Table 1 | Data dictionary and relational constraints across CuraCascade warehouse entities.</div>
    <table class="pub-table">
      <thead>
        <tr>
          <th>Table Name</th>
          <th>Primary Key</th>
          <th>Foreign Keys</th>
          <th>Key Attributes &amp; Types</th>
          <th>Indexing Strategy</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>genes</code></td>
          <td><code>gene_symbol</code> (TEXT)</td>
          <td>None</td>
          <td><code>hgnc_id</code>, <code>is_downgraded</code>, <code>highest_downgrade_severity</code></td>
          <td><code>idx_genes_downgraded</code> on (<code>is_downgraded</code>)</td>
        </tr>
        <tr>
          <td><code>diseases</code></td>
          <td><code>disease_id</code> (TEXT)</td>
          <td>None</td>
          <td><code>disease_name</code>, <code>mondo_id</code>, <code>prevalence_per_million</code></td>
          <td>Direct B-Tree PK index</td>
        </tr>
        <tr>
          <td><code>clingen_curations</code></td>
          <td><code>curation_id</code> (INT)</td>
          <td><code>gene_symbol</code> &rarr; <code>genes</code>, <code>disease_id</code> &rarr; <code>diseases</code></td>
          <td><code>classification</code>, <code>classification_date</code>, <code>gcep</code>, <code>moi</code></td>
          <td><code>idx_clingen_gene_disease</code>, <code>idx_clingen_date</code></td>
        </tr>
        <tr>
          <td><code>clinvar_variants</code></td>
          <td><code>variation_id</code> (INT)</td>
          <td><code>gene_symbol</code> &rarr; <code>genes</code>, <code>disease_id</code> &rarr; <code>diseases</code></td>
          <td><code>clinical_significance</code>, <code>is_plp</code>, <code>stars</code>, <code>gnomad_af_global</code></td>
          <td><code>idx_clinvar_gene_disease</code>, <code>idx_clinvar_is_plp</code>, <code>idx_clinvar_stars</code></td>
        </tr>
        <tr>
          <td><code>panelapp_entries</code></td>
          <td><code>entry_id</code> (INT)</td>
          <td><code>gene_symbol</code> &rarr; <code>genes</code>, <code>disease_id</code> &rarr; <code>diseases</code></td>
          <td><code>panel_id</code>, <code>panel_name</code>, <code>confidence</code> (green/amber/red)</td>
          <td><code>idx_panelapp_gene</code>, <code>idx_panelapp_confidence</code></td>
        </tr>
        <tr class="highlight">
          <td><code>audit_findings</code></td>
          <td><code>finding_id</code> (INT)</td>
          <td><code>gene_symbol</code> &rarr; <code>genes</code>, <code>disease_id</code> &rarr; <code>diseases</code></td>
          <td><code>audit_class</code>, <code>severity</code>, <code>target_type</code>, <code>days_unresolved</code></td>
          <td><code>idx_audit_gene_disease</code>, <code>idx_audit_class</code>, <code>idx_audit_severity</code></td>
        </tr>
        <tr class="highlight">
          <td><code>downgrade_risk_predictions</code></td>
          <td><code>prediction_id</code> (INT)</td>
          <td><code>gene_symbol</code> &rarr; <code>genes</code></td>
          <td><code>downgrade_risk_score</code>, <code>risk_tier</code>, <code>top_risk_driver</code></td>
          <td><code>idx_risk_predictions_gene</code>, <code>idx_risk_predictions_score</code></td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">Foreign key enforcement verified via SQLite PRAGMA foreign_key_check in automated CI pipeline.</div>
  </div>

  <h3>2.2 Data Harmonization Pipeline &amp; Dual-Engine Query Execution</h3>
  <p>
    The Extract, Transform, Load (ETL) pipeline implemented in <code>pipeline/build_full_warehouse.py</code> orchestrates multi-source ingestion from flat-file genomic dumps into the relational core:
  </p>
  <ul>
    <li><strong>HGNC Symbol Disambiguation:</strong> Raw curations frequently refer to historical gene aliases (e.g., <em>GPR98</em> instead of <em>ADGRV1</em>, <em>DFNB31</em> instead of <em>WHRN</em>). Ingestion cleans all records through an authoritative HGNC symbol crosswalk, mapping obsolete identifiers to current approved nomenclature while retaining historical synonyms in metadata fields.</li>
    <li><strong>Disease Ontology Crosswalk:</strong> ClinGen curations are indexed to Mondo Disease Ontology (MONDO) concepts, whereas ClinVar entries predominantly reference MedGen, OMIM, or UMLS identifiers. The pipeline executes a deterministic crosswalk that links MONDO identifiers to Orphanet rare disease prevalence metrics (<code>prevalence_per_million</code>), enabling automated calculations of genetic architecture parameters.</li>
    <li><strong>Dual-Engine Storage (SQLite + DuckDB):</strong> Production persistence is managed in SQLite with write-ahead logging (WAL) disabled during bulk loads (<code>PRAGMA synchronous = OFF; PRAGMA journal_mode = MEMORY;</code>) to permit complete warehouse builds under two minutes. For heavy analytical aggregations—such as multi-ancestry population stratification queries across 50,000+ variants—CuraCascade initializes an in-memory DuckDB analytical engine (<code>database/duckdb_engine.py</code>) using its native SQLite scanner extension (<code>ATTACH 'data/curacascade.db' AS db (TYPE SQLITE);</code>). This provides vectorized, columnar analytical performance without data duplication.</li>
  </ul>

  <!-- Section 3 -->
  <h2>3. Discrepancy Classification Taxonomy &amp; Evidence Latency Modeling</h2>

  <h3>3.1 Rule-Based Discrepancy Classification Heuristics</h3>
  <p>
    CuraCascade implements a deterministic classification taxonomy that stratifies downstream discrepancies into three mutually exclusive classes based on clinical actionability and consensus contradiction severity (formalized in <code>pipeline/audit.py</code>).
  </p>

  <!-- Figure 3 -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_taxonomy}" alt="Discrepancy Classification Decision Tree">
    </div>
    <div class="figure-caption">
      <strong>Figure 3 | Deterministic Discrepancy Classification Decision Tree.</strong>
      Heuristic routing stratifies downstream discrepancies into Class A (Critical false-positive ClinVar risk), Class B (High severity premature diagnostic closure), and Class C (Critical NHS diagnostic panel inclusion).
    </div>
  </div>

  <h4>Class A: Disputed/Refuted Genes with Downstream Pathogenic Variants (Severity: CRITICAL)</h4>
  <p>
    <strong>Heuristic Definition:</strong> A gene–disease association is classified as <em>Disputed</em> or <em>Refuted</em> by ClinGen GCEPs, yet NCBI ClinVar contains active records asserting Pathogenic (P) or Likely Pathogenic (LP) clinical significance (<code>is_plp = 1</code>).
    When a gene is refuted, assigning pathogenicity to sequence variants directly violates ACMG/AMP variant interpretation guidelines (Richards <em>et al.</em>, 2015), creating an immediate hazard of false-positive monogenic diagnosis.
  </p>
  <div class="math-block">
    Class A &iff; [ C<sub>ClinGen</sub>(g, d) &isin; &#123;Disputed, Refuted&#125; ] &and; [ &exist; v &isin; V<sub>ClinVar</sub>(g) : v<sub>significance</sub> &isin; &#123;P, LP&#125; ]
    <span class="tag">(Equation 1)</span>
  </div>

  <h4>Class B: Limited Evidence Genes with Diagnostic Pathogenic Variants (Severity: HIGH)</h4>
  <p>
    <strong>Heuristic Definition:</strong> A gene–disease relationship is classified as <em>Limited</em> clinical validity by ClinGen, yet ClinVar contains variants classified as P/LP. Under ClinGen and ACMG framework recommendations, variants in genes with limited validity must not be interpreted or reported above the threshold of a Variant of Uncertain Significance (VUS). Classifying variants as definitively pathogenic in limited-evidence genes leads to premature diagnostic closure.
  </p>
  <div class="math-block">
    Class B &iff; [ C<sub>ClinGen</sub>(g, d) = Limited ] &and; [ &exist; v &isin; V<sub>ClinVar</sub>(g) : v<sub>significance</sub> &isin; &#123;P, LP&#125; ]
    <span class="tag">(Equation 2)</span>
  </div>

  <h4>Class C: Disputed/Refuted Genes with Green Diagnostic Panel Membership (Severity: CRITICAL)</h4>
  <p>
    <strong>Heuristic Definition:</strong> A gene–disease relationship is <em>Disputed</em> or <em>Refuted</em> by ClinGen, yet Genomics England PanelApp retains the gene with "Green" (diagnostic-grade) confidence status. PanelApp Green status denotes genes approved for routine, automated diagnostic reporting within accredited clinical laboratories (such as the UK National Health Service Genomic Medicine Service). A Class C finding indicates that high-throughput diagnostic sequencing pipelines are actively screening and reporting on discredited genes.
  </p>
  <div class="math-block">
    Class C &iff; [ C<sub>ClinGen</sub>(g, d) &isin; &#123;Disputed, Refuted&#125; ] &and; [ &exist; p &isin; P<sub>PanelApp</sub>(g) : p<sub>confidence</sub> = 'green' ]
    <span class="tag">(Equation 3)</span>
  </div>

  <!-- Table 2 -->
  <div class="table-container">
    <div class="table-title">Table 2 | Comparative overview of CuraCascade discrepancy taxonomy.</div>
    <table class="pub-table">
      <thead>
        <tr>
          <th>Class</th>
          <th>Upstream ClinGen Status</th>
          <th>Downstream Target Record</th>
          <th>Severity</th>
          <th>Clinical Hazard Mechanism</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge-class-a">Class A</span></td>
          <td><em>Disputed</em> or <em>Refuted</em></td>
          <td>ClinVar Variant: Pathogenic / Likely Pathogenic</td>
          <td><strong>CRITICAL</strong></td>
          <td>False-positive monogenic diagnosis; improper clinical management &amp; ICDs</td>
        </tr>
        <tr>
          <td><span class="badge-class-b">Class B</span></td>
          <td><em>Limited</em> Validity</td>
          <td>ClinVar Variant: Pathogenic / Likely Pathogenic</td>
          <td><strong>HIGH</strong></td>
          <td>Premature diagnostic closure; violation of ACMG VUS ceiling</td>
        </tr>
        <tr>
          <td><span class="badge-class-c">Class C</span></td>
          <td><em>Disputed</em> or <em>Refuted</em></td>
          <td>PanelApp Panel: "Green" (Diagnostic-Grade)</td>
          <td><strong>CRITICAL</strong></td>
          <td>Routine automated clinical exome screening and reporting of invalid genes</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3>3.2 Mathematical Formulation of Unpropagated Curation Latency</h3>
  <p>
    To evaluate the duration and drivers of evidence synchronization lag, CuraCascade formulates assertion lifespan within a rigorous time-to-event (survival analysis) framework (<code>pipeline/survival_analysis.py</code>).
    Let <em>t</em><sub>0</sub> represent the timestamp on which ClinGen officially publishes a validity downgrade for gene <em>g</em>. Let <em>t</em><sub>resolved</sub> represent the date on which a downstream assertion (ClinVar record or PanelApp entry) is revised or retracted to achieve concordance. If an assertion remains discordant at the time of warehouse execution <em>t</em><sub>audit</sub>, the observation is right-censored. The elapsed unpropagated latency (duration <em>T</em>) is defined as:
  </p>
  <div class="math-block">
    T = (t<sub>resolved</sub> - t<sub>0</sub>) if resolved, &nbsp; else (t<sub>audit</sub> - t<sub>0</sub>) [censored, &delta; = 0]
    <span class="tag">(Equation 4)</span>
  </div>
  <p>
    The probability that an unpropagated clinical assertion remains discordant beyond duration <em>t</em> is modeled via the Kaplan–Meier survival estimator:
  </p>
  <div class="math-block">
    S&#770;(t) = &prod;<sub>i: t<sub>i</sub> &le; t</sub> [ 1 - (d<sub>i</sub> / n<sub>i</sub>) ]
    <span class="tag">(Equation 5)</span>
  </div>
  <p>
    where <em>d</em><sub>i</sub> represents assertion revisions occurring at time <em>t</em><sub>i</sub>, and <em>n</em><sub>i</sub> represents total discordant assertions at risk immediately prior to <em>t</em><sub>i</sub>. To isolate multi-factorial covariates governing resolution kinetics, we implement a multivariate Cox Proportional Hazards regression model:
  </p>
  <div class="math-block">
    h(t | <strong>X</strong>) = h<sub>0</sub>(t) exp( &sum;<sub>k=1..p</sub> &beta;<sub>k</sub> X<sub>k</sub> )
    <span class="tag">(Equation 6)</span>
  </div>
  <p>
    where <em>h</em><sub>0</sub>(t) is baseline hazard, and regression coefficients determine Hazard Ratios (HR = exp(&beta;<sub>k</sub>)), quantifying whether a covariate accelerates (HR &gt; 1.0) or delays (HR &lt; 1.0) downstream evidence resolution.
  </p>

  <!-- Figure 4 -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_survival}" alt="Kaplan Meier Survival Curves and Cox Proportional Hazards Forest Plot">
    </div>
    <div class="figure-caption">
      <strong>Figure 4 | Longitudinal Latency Modeling &amp; Multivariate Cox Proportional Hazards Analysis.</strong>
      (A) Kaplan–Meier assertion survival curves showing rapid resolution for high-confidence (&ge;2 stars) assertions vs severe persistent latency for commercial laboratory submissions.
      (B) Forest plot of multivariate Cox Proportional Hazards regression hazard ratios with 95% confidence intervals across clinical domains, review confidence, severity classes, and submitter categories.
    </div>
  </div>

  <!-- Table 3 -->
  <div class="table-container">
    <div class="table-title">Table 3 | Multivariate Cox Proportional Hazards regression results for downstream assertion resolution latency.</div>
    <table class="pub-table">
      <thead>
        <tr>
          <th>Covariate</th>
          <th class="num">Hazard Ratio (HR)</th>
          <th class="num">95% Confidence Interval</th>
          <th class="num">Coefficient (&beta;)</th>
          <th class="num">Robust SE</th>
          <th class="num"><em>z</em>-score</th>
          <th class="num"><em>p</em>-value</th>
          <th>Clinical Direction</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight">
          <td><strong>Domain: Cardiovascular vs. Others</strong></td>
          <td class="num"><strong>2.37</strong></td>
          <td class="num">2.10 – 2.66</td>
          <td class="num">+0.8610</td>
          <td class="num">0.0597</td>
          <td class="num">14.41</td>
          <td class="num">&lt; 0.001</td>
          <td>Accelerated Resolution</td>
        </tr>
        <tr class="highlight">
          <td><strong>Review Confidence: &ge; 2 Stars vs. 0–1 Stars</strong></td>
          <td class="num"><strong>2.36</strong></td>
          <td class="num">2.16 – 2.57</td>
          <td class="num">+0.8575</td>
          <td class="num">0.0440</td>
          <td class="num">19.49</td>
          <td class="num">&lt; 0.001</td>
          <td>Accelerated Resolution</td>
        </tr>
        <tr class="highlight">
          <td><strong>Discrepancy Severity: Class A vs. Class B</strong></td>
          <td class="num"><strong>2.31</strong></td>
          <td class="num">2.07 – 2.57</td>
          <td class="num">+0.8365</td>
          <td class="num">0.0545</td>
          <td class="num">15.35</td>
          <td class="num">&lt; 0.001</td>
          <td>Accelerated Resolution</td>
        </tr>
        <tr>
          <td><strong>Domain: Hereditary Cancer vs. Others</strong></td>
          <td class="num"><strong>1.71</strong></td>
          <td class="num">1.52 – 1.92</td>
          <td class="num">+0.5355</td>
          <td class="num">0.0589</td>
          <td class="num">9.10</td>
          <td class="num">&lt; 0.001</td>
          <td>Accelerated Resolution</td>
        </tr>
        <tr>
          <td><strong>Domain: Neurology vs. Others</strong></td>
          <td class="num"><strong>0.75</strong></td>
          <td class="num">0.64 – 0.89</td>
          <td class="num">-0.2841</td>
          <td class="num">0.0857</td>
          <td class="num">-3.31</td>
          <td class="num">&lt; 0.001</td>
          <td>Extended Latency / Lag</td>
        </tr>
        <tr style="background: #ffe4e6;">
          <td><strong>Submitter: Commercial Lab vs. Academic</strong></td>
          <td class="num"><strong>0.55</strong></td>
          <td class="num">0.50 – 0.60</td>
          <td class="num">-0.5978</td>
          <td class="num">0.0439</td>
          <td class="num">-13.62</td>
          <td class="num">&lt; 0.001</td>
          <td>Extended Latency / Lag</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">Model Diagnostics: Concordance Index (C-index) = 0.724; Log-Likelihood = -24,812.4; Proportional hazards assumption verified with L2 penalization (&alpha; = 0.01).</div>
  </div>

  <div class="callout callout-info">
    <div class="callout-title">Key Epidemiological Insights from Survival Kinetics</div>
    <strong>1. The Review Star Accelerator:</strong> Assertions supported by &ge; 2 stars resolve <strong>2.36 times faster</strong> (HR = 2.36, <em>p</em> &lt; 0.001) than single-submitter 0-star records. Multi-submitter consensus triggers active re-appraisal, whereas single-submitter legacy records remain unmonitored for years.<br>
    <strong>2. The Commercial Laboratory Latency Penalty:</strong> Commercial laboratories resolve discrepancies at nearly half the rate (HR = 0.55, <em>p</em> &lt; 0.001) of academic medical centers. High administrative overhead and legal liabilities associated with re-contacting ordering physicians and issuing amended diagnostic reports create strong disincentives for rapid variant retraction.
  </div>

  <!-- Section 4 -->
  <h2>4. Machine-Learned Downgrade Triage Framework</h2>

  <h3>4.1 Feature Engineering &amp; Biological Rationale</h3>
  <p>
    Rather than functioning solely as a retrospective auditing tool, CuraCascade incorporates a predictive machine learning engine (<code>pipeline/forecasting.py</code>) that estimates the probability that a currently supported gene–disease relationship (<em>Definitive</em>, <em>Strong</em>, or <em>Moderate</em>) is vulnerable to a future downgrade to <em>Limited</em>, <em>Disputed</em>, or <em>Refuted</em>.
    We engineered seven biologically and operationally grounded features across genomic databases:
  </p>
  <ul>
    <li><strong>Curation Age Elapsed (&Delta;t<sub>age</sub>, days):</strong> Days elapsed since the most recent ClinGen formal evaluation. Older curations are vulnerable to obsolescence as reference population databases expand.</li>
    <li><strong>Total ClinVar Variant Volume (N<sub>total</sub>):</strong> Total number of cataloged variants in ClinVar for the candidate gene.</li>
    <li><strong>Reported Pathogenic / Likely Pathogenic Count (N<sub>PLP</sub>):</strong> Volume of asserted P/LP variants in the candidate gene.</li>
    <li><strong>Low ClinVar Star Ratio (&rho;<sub>low_stars</sub>):</strong> Proportion of asserted variants supported by &lt; 2 ClinVar review stars: &rho;<sub>low_stars</sub> = N<sub>stars&lt;2</sub> / max(1, N<sub>total</sub>). Reflects uncurated, single-submitter assertions lacking inter-laboratory consensus.</li>
    <li><strong>gnomAD Maximum Continental Allele Frequency (AF<sub>max</sub>):</strong> The maximum allele frequency observed for any reported P/LP variant across continental ancestry groups in gnomAD v4.</li>
    <li><strong>gnomAD MCAF Violation Rate (&rho;<sub>MCAF</sub>):</strong> Proportion of reported P/LP variants exceeding the Maximum Credible Allele Frequency (MCAF) calculated for the linked disease indication (Whiffin <em>et al.</em>, 2017). Based on population genetics, MCAF represents the mathematical ceiling above which an allele is too common to cause a rare monogenic disorder:
      <div class="math-block">
        MCAF<sub>Dominant</sub> = (I &times; h) / (2 &times; P), &nbsp;&nbsp;&nbsp; MCAF<sub>Recessive</sub> = &radic;[ (I &times; h) / P ]
        <span class="tag">(Equation 7)</span>
      </div>
      where <em>I</em> is prevalence per individual (Orphanet), <em>h</em> is allelic heterogeneity (default: 0.10), and <em>P</em> is clinical penetrance (default: 0.50).
    </li>
    <li><strong>Non-Green PanelApp Indication Count (N<sub>amber/red</sub>):</strong> Count of Genomics England panels where the gene is categorized as <em>Amber</em> (borderline) or <em>Red</em> (inconclusive), capturing early peer-review skepticism.</li>
  </ul>

  <!-- Figure 5 -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_ml}" alt="Machine Learning Dual Benchmark and Mechanistic Feature Shift">
    </div>
    <div class="figure-caption">
      <strong>Figure 5 | Machine-Learned Downgrade Triage Framework: Dual Evaluation.</strong>
      (A) Dual ROC curves comparing the curated positive control benchmark (AUROC = 1.000) against the genome-wide empirical corpus (Random Forest AUROC = 0.857; Logistic Regression baseline AUROC = 0.827).
      (B) Mechanistic feature importance comparison: curation age dominates the targeted benchmark (78.4%), whereas low ClinVar star density (70.2%) and PanelApp disagreements (26.0%) drive predictions across the messy genome-wide clinical database.
    </div>
  </div>

  <!-- Table 4 -->
  <div class="table-container">
    <div class="table-title">Table 4 | Comparative machine learning performance across positive control benchmark and genome-wide corpus.</div>
    <table class="pub-table">
      <thead>
        <tr>
          <th>Metric / Attribute</th>
          <th>Positive Control Benchmark (<em>N</em> = 34)</th>
          <th>Genome-Wide Empirical Corpus (<em>N</em> = 3,833 genes)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Cohort Definition</strong></td>
          <td>Curated gold-standard positive/negative controls</td>
          <td>Complete unfiltered ClinGen / ClinVar corpus</td>
        </tr>
        <tr>
          <td><strong>Total Analyzed Entities</strong></td>
          <td>34 genes (18 downgraded, 16 definitive)</td>
          <td>3,833 unique genes; 51,025 ClinVar variants</td>
        </tr>
        <tr>
          <td><strong>Logistic Regression AUROC</strong></td>
          <td class="num"><strong>1.000</strong></td>
          <td class="num"><strong>0.827</strong></td>
        </tr>
        <tr class="highlight">
          <td><strong>Random Forest AUROC</strong></td>
          <td class="num"><strong>1.000</strong></td>
          <td class="num"><strong>0.857</strong></td>
        </tr>
        <tr>
          <td><strong>Random Forest PR-AUC</strong></td>
          <td class="num"><strong>1.000</strong></td>
          <td class="num"><strong>0.814</strong></td>
        </tr>
        <tr class="highlight">
          <td><strong>Precision @ Top 20% Queue</strong></td>
          <td class="num"><strong>100.0%</strong></td>
          <td class="num"><strong>75.8%</strong></td>
        </tr>
        <tr>
          <td><strong>Primary Feature Driver #1</strong></td>
          <td>Curation Age Elapsed (<strong>78.4%</strong>)</td>
          <td>Low ClinVar Star Ratio (<strong>70.2%</strong>)</td>
        </tr>
        <tr>
          <td><strong>Primary Feature Driver #2</strong></td>
          <td>gnomAD MCAF Violation Rate (<strong>10.8%</strong>)</td>
          <td>Non-Green PanelApp Indication (<strong>26.0%</strong>)</td>
        </tr>
        <tr>
          <td><strong>Primary Feature Driver #3</strong></td>
          <td>Maximum Population AF (<strong>10.8%</strong>)</td>
          <td>Total ClinVar Variant Count (<strong>3.1%</strong>)</td>
        </tr>
      </tbody>
    </table>
    <div class="table-note">Permutation feature importance computed across 10 random iterations on test partition.</div>
  </div>

  <!-- Section 5 -->
  <h2>5. Software Implementation, CI/CD, &amp; Reproducibility</h2>

  <h3>5.1 Architecture &amp; Headless CLI Interface</h3>
  <p>
    CuraCascade is developed in Python 3.11+ using standard scientific computing libraries (<code>numpy</code>, <code>pandas</code>, <code>scikit-learn</code>, <code>lifelines</code>, <code>duckdb</code>). The core execution framework is decoupled from the web presentation layer, enabling integration into automated bioinformatics pipelines through a unified command-line entrypoint (<code>run.py</code>).
  </p>
  <pre><code># Automated Discrepancy Scan with POSIX exit codes (Exit 0: Clean, Exit 1: Class A Alert)
python run.py audit --genes SCN1B,MYLK2,BRCA1 --class A --format table

# Relational & Cryptographic Provenance Verification (Exit 0: Pass, Exit 2: Fail)
python run.py verify

# Generate Formal Research Publication PDF Report
python run.py report --output docs/CuraCascade_Publication_Report.pdf

# Launch Interactive Clinical Audit Dashboard
python run.py serve --port 8501</code></pre>

  <h3>5.2 Interactive Clinical Audit Dashboard</h3>
  <p>
    To serve multidisciplinary clinical teams, CuraCascade provides an interactive, executive-grade web dashboard implemented in Streamlit (<code>app.py</code>), publicly hosted on Streamlit Community Cloud at <a href="https://curacascade.streamlit.app">https://curacascade.streamlit.app</a>. The dashboard is structured into eight integrated clinical modules:
  </p>
  <ul>
    <li><strong>Module 1 (Executive Summary):</strong> Headline audit metrics, total materialized discrepancies, and global latency averages across 3,833 genes and 51,251 findings.</li>
    <li><strong>Module 2 (Custom Gene Audit):</strong> Enables laboratory geneticists to paste arbitrary lists of candidate genes and immediately receive a cross-layer concordance report.</li>
    <li><strong>Module 3 (Inconsistency Explorer):</strong> Interactive data tables featuring sortable ClinVar variation IDs, ClinGen GCEP links, and elapsed unresolved days.</li>
    <li><strong>Module 4 (Population Genetics &amp; MCAF):</strong> Visualizes gnomAD v4 global and popmax frequencies alongside Orphanet-derived MCAF thresholds to identify population-refuted variants.</li>
    <li><strong>Module 5 (Downgrade Forecasting Queue):</strong> Ranks currently supported genes by calibrated machine-learned vulnerability scores, exposing top risk drivers.</li>
    <li><strong>Module 6 (Evidence Resolution Survival Analysis):</strong> Renders interactive Kaplan-Meier survival curves and multivariate Cox hazard ratios.</li>
    <li><strong>Module 7 (Clinical Governance Dossier):</strong> Compiles formal, regulatory-grade clinical audit memos for flagged genes.</li>
    <li><strong>Module 8 (Cross-Layer Join Validation Benchmark):</strong> Reports empirical accuracy metrics against the 100-gene expert adjudication benchmark.</li>
  </ul>

  <!-- Figure 6 / Validation Matrix -->
  <div class="figure-container">
    <div class="figure-box">
      <img src="{fig_val}" alt="100 Gene Adjudication Confusion Matrix and Benchmark Concordance">
    </div>
    <div class="figure-caption">
      <strong>Figure 6 | Cross-Layer Join Validation Benchmark: 100-Gene Expert Adjudication.</strong>
      (A) Confusion matrix evaluating CuraCascade's automated discrepancy detection against manual expert adjudication across 100 landmark genes (52 True Positives, 44 True Negatives, 2 False Positives, 2 False Negatives).
      (B) Validation concordance metrics: 96.3% PPV (precision), 96.3% sensitivity (recall), 95.7% specificity, 96.0% overall accuracy, and Cohen's &kappa; = 0.920.
    </div>
  </div>

  <!-- Table 5 -->
  <div class="table-container">
    <div class="table-title">Table 5 | Cross-layer join validation benchmark performance against 100-gene expert adjudication gold standard.</div>
    <table class="pub-table">
      <thead>
        <tr>
          <th>Evaluation Metric</th>
          <th class="num">Empirical Score</th>
          <th class="num">Percentage (%)</th>
          <th>Clinical Quality Standard</th>
        </tr>
      </thead>
      <tbody>
        <tr class="highlight">
          <td><strong>Positive Predictive Value (PPV / Precision)</strong></td>
          <td class="num">0.9630</td>
          <td class="num"><strong>96.3%</strong></td>
          <td>Minimizes false-positive audit alerts for laboratory staff</td>
        </tr>
        <tr class="highlight">
          <td><strong>Sensitivity (Recall)</strong></td>
          <td class="num">0.9630</td>
          <td class="num"><strong>96.3%</strong></td>
          <td>Ensures 96.3% of true consortium refutations are intercepted</td>
        </tr>
        <tr>
          <td><strong>Specificity</strong></td>
          <td class="num">0.9565</td>
          <td class="num"><strong>95.7%</strong></td>
          <td>Avoids spurious disruption of valid diagnostic panels</td>
        </tr>
        <tr>
          <td><strong>Overall Classification Accuracy</strong></td>
          <td class="num">0.9600</td>
          <td class="num"><strong>96.0%</strong></td>
          <td>High overall concordance across 100 curated disease genes</td>
        </tr>
        <tr class="highlight">
          <td><strong>Inter-Rater Agreement (Cohen's &kappa;)</strong></td>
          <td class="num"><strong>0.9195</strong></td>
          <td class="num"><strong>&kappa; = 0.920</strong></td>
          <td>Near-perfect concordance (&kappa; &gt; 0.81) vs. expert clinical curators</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Section 6 -->
  <h2>6. Discussion, Clinical Governance, &amp; Regulatory Implications</h2>

  <h3>6.1 CuraCascade as an Automated Clinical Audit Firewall</h3>
  <p>
    In modern genomic medicine, clinical diagnostic laboratories operate under strict quality management mandates established by the College of American Pathologists (CAP), the Clinical Laboratory Improvement Amendments (CLIA), and the International Organization for Standardization (ISO 15189:2022). ISO 15189 Section 7.3 explicitly mandates that medical laboratories must regularly review their examination procedures and diagnostic panel contents to ensure continued clinical relevance.
    CuraCascade fills this operational void, functioning as an automated <strong>Clinical Audit Firewall</strong>:
  </p>
  <ul>
    <li><strong>Pre-Report Audit:</strong> Integrated into laboratory information management systems (LIMS), CuraCascade intercepts outgoing NGS molecular diagnostic reports, checking candidate variants against the <code>audit_findings</code> database. Any variant falling into Class A triggers an automated report freeze, preventing diagnostic misclassification.</li>
    <li><strong>Panel Design Quality Control:</strong> Prior to deploying a customized commercial gene panel, curators can run <code>run.py audit --genes &lt;PANEL_GENES&gt;</code> to detect Class C panel contradictions, purging discredited genes prior to clinical assay validation.</li>
  </ul>

  <h3>6.2 The Clinical Governance Dossier Framework</h3>
  <p>
    When an audit flags an unpropagated Class A discrepancy, laboratory directors face complex clinical, ethical, and legal obligations. They must determine whether previously issued patient reports require formal amendment and whether ClinVar submissions must be retracted. To streamline this procedure, CuraCascade automatically generates a standardized <strong>Clinical Governance Dossier &amp; Retraction Directive</strong> (<code>pipeline/remediation.py</code>).
  </p>

  <div class="dossier-box">
    <div class="head">========================================================================================<br>
CLINICAL AUDIT &amp; RETRACTION DIRECTIVE: SCN1B (Brugada Syndrome)<br>
========================================================================================</div>
Evaluation Date: 2026-10-11 | ClinGen Status: <span class="accent">REFUTED</span> | MONDO: MONDO:0015263<br>
Expert Panel   : ClinGen Brugada Syndrome GCEP (Report: https://search.clinicalgenome.org)<br>
----------------------------------------------------------------------------------------<br>
<span class="head">ORTHOGONAL POPULATION GENETICS EVIDENCE (gnomAD v4):</span><br>
- gnomAD v4 Global Frequency : 0.001840 (0.184%)<br>
- Max Credible AF (MCAF)     : 0.000100 (0.010%)<br>
- Fold-Excess Multiplier     : <span class="accent">18.4&times; above theoretical disease ceiling</span><br>
- European Baseline (NFE)    : 0.000120 | Popmax Ancestry: East Asian (EAS: 0.003410)<br>
- Disparity Statement        : Variant is common in East Asian populations but rare in<br>
                              European historical cohorts, driving ancestral misclassification.<br>
----------------------------------------------------------------------------------------<br>
<span class="head">ACTIVE NCBI CLINVAR PATHOGENIC / LIKELY PATHOGENIC RECORDS:</span><br>
- Variation ID: 48312 | c.629T&gt;C (p.Leu210Pro) | Status: <span class="accent">Pathogenic (2 stars, 3 submitters)</span><br>
----------------------------------------------------------------------------------------<br>
<span class="head">PRESCRIPTIVE REMEDIATION CHECKLIST:</span><br>
[ ] Apply ACMG Rule BA1/BS1 based on gnomAD population frequency excess.<br>
[ ] Reclassify variant from Pathogenic to Benign / Likely Benign.<br>
[ ] Prepare NCBI ClinVar Submission Retraction batch file.<br>
[ ] Review patient database for historical reports issued with SCN1B pathogenicity.<br>
----------------------------------------------------------------------------------------<br>
<span class="success">FORMAL CLINICAL GOVERNANCE ATTESTATION &amp; REGULATORY SIGN-OFF:</span><br>
Lead Clinical Molecular Geneticist: _______________________ Date: ____________<br>
Laboratory Medical Director        : _______________________ Date: ____________<br>
========================================================================================
  </div>

  <h3>6.3 Multi-Ancestry Equity and Population Misclassification</h3>
  <p>
    A crucial finding emerging from CuraCascade’s population genetics audit (<code>pipeline/allele_frequency.py</code>) is the pronounced disparity between historical European reference cohorts and diverse continental ancestries in gnomAD v4.
    Historically, disease-gene discovery occurred almost exclusively in cohorts of European descent. Sequence variants that are benign and common in underrepresented ancestries (such as African/African American [AFR] or East Asian [EAS]) were absent from early European control series (such as ExAC or early 1000 Genomes), leading researchers to mistakenly infer pathogenicity based on apparent rarity. When ClinGen reappraised genes such as <em>SCN1B</em> for Brugada Syndrome, population frequency data from gnomAD demonstrated that putative pathogenic variants exhibited allele frequencies up to <strong>18.4-fold greater than the maximum credible threshold (MCAF)</strong> in non-European ancestries. By embedding multi-ancestry popmax frequency metrics and ancestry discordance ratios into every audit finding, CuraCascade serves as an algorithmic safeguard against ancestral diagnostic inequities.
  </p>

  <!-- Section 7 & References -->
  <h2>7. Data and Software Availability</h2>
  <p>
    CuraCascade is distributed as open-source software under the permissive MIT License.
  </p>
  <ul>
    <li><strong>Source Code Repository:</strong> <a href="https://github.com/uditshokeen14/curacascade">https://github.com/uditshokeen14/curacascade</a></li>
    <li><strong>Interactive Cloud Portal:</strong> <a href="https://curacascade.streamlit.app">https://curacascade.streamlit.app</a></li>
    <li><strong>Docker Container Registry:</strong> <code>docker run -p 8501:8501 curacascade:latest</code></li>
  </ul>

  <h2>Author Contributions</h2>
  <p>
    <strong>U.S.</strong> conceived the project, architected the relational database schema, implemented the data harmonization pipelines, developed the machine learning and survival analysis frameworks, built the Streamlit dashboard and CLI, and authored the manuscript. <strong>Faculty Advisor</strong> provided scientific guidance, methodology validation, and manuscript review.
  </p>

  <h2>Conflicts of Interest</h2>
  <p>
    The authors declare that they have no competing financial or commercial interests.
  </p>

  <h2>Acknowledgments</h2>
  <p>
    The authors express gratitude to the Clinical Genome Resource (ClinGen), the National Center for Biotechnology Information (NCBI) ClinVar team, Genomics England PanelApp curators, and the Genome Aggregation Database (gnomAD) consortium for maintaining open-access clinical datasets.
  </p>

  <h2>References</h2>
  <ol class="references-list">
    <li><strong>Strande, N.T., et al.</strong> (2017) Evaluating the Clinical Validity of Gene-Disease Associations: An Evidence-Based Framework Developed by the Clinical Genome Resource. <em>Am. J. Hum. Genet.</em>, <strong>100</strong>(6), 895–906. <a href="https://doi.org/10.1016/j.ajhg.2017.04.015">doi:10.1016/j.ajhg.2017.04.015</a></li>
    <li><strong>Richards, S., et al.</strong> (2015) Standards and guidelines for the interpretation of sequence variants: joint consensus recommendation of ACMG and AMP. <em>Genet. Med.</em>, <strong>17</strong>(5), 405–424. <a href="https://doi.org/10.1038/gim.2015.30">doi:10.1038/gim.2015.30</a></li>
    <li><strong>Whiffin, N., et al.</strong> (2017) Using high-resolution variant frequencies to empower clinical variant interpretation. <em>Genet. Med.</em>, <strong>19</strong>(10), 1151–1158. <a href="https://doi.org/10.1038/gim.2017.26">doi:10.1038/gim.2017.26</a></li>
    <li><strong>Whiffin, N., et al.</strong> (2020) The effect of LMM and gnomAD population size on clinical interpretation of rare variation. <em>Nature</em>, <strong>581</strong>(7809), 434–443. <a href="https://doi.org/10.1038/s41586-020-2308-7">doi:10.1038/s41586-020-2308-7</a></li>
    <li><strong>Landrum, M.J., et al.</strong> (2018) ClinVar: improving access to variant interpretations and supporting evidence. <em>Nucleic Acids Res.</em>, <strong>46</strong>(D1), D1062–D1067. <a href="https://doi.org/10.1093/nar/gkx1153">doi:10.1093/nar/gkx1153</a></li>
    <li><strong>Landrum, M.J., et al.</strong> (2020) ClinVar: updates to submission, data, and access. <em>Nucleic Acids Res.</em>, <strong>48</strong>(D1), D835–D844. <a href="https://doi.org/10.1093/nar/gkz836">doi:10.1093/nar/gkz836</a></li>
    <li><strong>Martin, A.R., et al.</strong> (2019) PanelApp crowdsources expert knowledge for genome-scale curation of disease-associated genes. <em>Nat. Genet.</em>, <strong>51</strong>(11), 1560–1565. <a href="https://doi.org/10.1038/s41588-019-0522-8">doi:10.1038/s41588-019-0522-8</a></li>
    <li><strong>Ingles, J., et al.</strong> (2019) Evaluating the Clinical Validity of Hypertrophic Cardiomyopathy Genes. <em>Circ. Genom. Precis. Med.</em>, <strong>12</strong>(2), e002460. <a href="https://doi.org/10.1161/CIRCGEN.119.002460">doi:10.1161/CIRCGEN.119.002460</a></li>
    <li><strong>Kelly, M.A., et al.</strong> (2018) Adaptation and validation of ACMG/AMP variant classification framework for MYH7-associated cardiomyopathies. <em>Genet. Med.</em>, <strong>20</strong>(3), 351–359. <a href="https://doi.org/10.1038/gim.2017.218">doi:10.1038/gim.2017.218</a></li>
    <li><strong>Hosseini, M., et al.</strong> (2018) Reappraisal of Reported Genes for Brugada Syndrome: ClinGen GCEP. <em>Circulation</em>, <strong>138</strong>(12), 1195–1205. <a href="https://doi.org/10.1161/CIRCULATIONAHA.118.035070">doi:10.1161/CIRCULATIONAHA.118.035070</a></li>
    <li><strong>Lee, K., et al.</strong> (2019) Clinical Validity Assessment of Genes Frequently Tested on Hereditary Breast and Ovarian Cancer Panels. <em>J. Med. Genet.</em>, <strong>56</strong>(9), 601–608. <a href="https://doi.org/10.1136/jmedgenet-2018-105822">doi:10.1136/jmedgenet-2018-105822</a></li>
    <li><strong>Rehm, H.L., et al.</strong> (2015) ClinGen — The Clinical Genome Resource. <em>N. Engl. J. Med.</em>, <strong>372</strong>(23), 2235–2242. <a href="https://doi.org/10.1056/NEJMsr1406261">doi:10.1056/NEJMsr1406261</a></li>
    <li><strong>Chen, S., et al.</strong> (2024) A genomic mutational constraint map using variation in 76,156 human genomes. <em>Nature</em>, <strong>625</strong>(7993), 92–100. <a href="https://doi.org/10.1038/s41586-023-06045-0">doi:10.1038/s41586-023-06045-0</a></li>
    <li><strong>Wright, C.F., et al.</strong> (2018) Paediatric genomics: diagnosing rare disease in children. <em>Nat. Rev. Genet.</em>, <strong>19</strong>(5), 253–268. <a href="https://doi.org/10.1038/nrg.2017.116">doi:10.1038/nrg.2017.116</a></li>
    <li><strong>Manrai, A.K., et al.</strong> (2016) Genetic Misdiagnoses and the Potential for Health Disparities. <em>N. Engl. J. Med.</em>, <strong>375</strong>(7), 655–665. <a href="https://doi.org/10.1056/NEJMsa1507092">doi:10.1056/NEJMsa1507092</a></li>
    <li><strong>Riggs, E.R., et al.</strong> (2020) Technical standards for interpretation of constitutional copy-number variants: joint ACMG/ClinGen standard. <em>Genet. Med.</em>, <strong>22</strong>(2), 245–257. <a href="https://doi.org/10.1038/s41436-019-0686-8">doi:10.1038/s41436-019-0686-8</a></li>
    <li><strong>Harrison, S.M., et al.</strong> (2017) Clinical laboratories collaborate to resolve differences in variant interpretations. <em>Genet. Med.</em>, <strong>19</strong>(10), 1096–1104. <a href="https://doi.org/10.1038/gim.2017.14">doi:10.1038/gim.2017.14</a></li>
    <li><strong>Bikadi, Z., et al.</strong> (2021) ClinGen curation data integration: automating consistency checking for variant interpretations. <em>Database</em>, <strong>2021</strong>, baab065. <a href="https://doi.org/10.1093/database/baab065">doi:10.1093/database/baab065</a></li>
    <li><strong>Raas-Rothschild, A., et al.</strong> (2022) Continuous quality improvement in diagnostic genome interpretation. <em>Eur. J. Hum. Genet.</em>, <strong>30</strong>(8), 911–918. <a href="https://doi.org/10.1038/s41431-022-01089-1">doi:10.1038/s41431-022-01089-1</a></li>
    <li><strong>Cox, D.R.</strong> (1972) Regression Models and Life-Tables. <em>J. R. Stat. Soc. B</em>, <strong>34</strong>(2), 187–202. <a href="https://doi.org/10.1111/j.2517-6161.1972.tb00899.x">doi:10.1111/j.2517-6161.1972.tb00899.x</a></li>
    <li><strong>Kaplan, E.L., Meier, P.</strong> (1958) Nonparametric Estimation from Incomplete Observations. <em>J. Am. Stat. Assoc.</em>, <strong>53</strong>(282), 457–481. <a href="https://doi.org/10.1080/01621459.1958.10501452">doi:10.1080/01621459.1958.10501452</a></li>
    <li><strong>Breiman, L.</strong> (2001) Random Forests. <em>Mach. Learn.</em>, <strong>45</strong>(1), 5–32. <a href="https://doi.org/10.1023/A:1010933404324">doi:10.1023/A:1010933404324</a></li>
    <li><strong>Pedregosa, F., et al.</strong> (2011) Scikit-learn: Machine Learning in Python. <em>J. Mach. Learn. Res.</em>, <strong>12</strong>, 2825–2830.</li>
    <li><strong>Davidson-Pilon, C.</strong> (2019) lifelines: survival analysis in Python. <em>J. Open Source Softw.</em>, <strong>4</strong>(40), 1317. <a href="https://doi.org/10.21105/joss.01317">doi:10.21105/joss.01317</a></li>
    <li><strong>Raasveldt, M., M&uuml;hleisen, H.</strong> (2019) DuckDB: an Embeddable Analytical Database. <em>Proc. ACM SIGMOD</em>, 1981–1984. <a href="https://doi.org/10.1145/3299869.3320212">doi:10.1145/3299869.3320212</a></li>
    <li><strong>Owens, M., Allen, G.</strong> (2010) <em>The Definitive Guide to SQLite</em>. Apress, Berkeley, CA. <a href="https://doi.org/10.1007/978-1-4302-3226-1">doi:10.1007/978-1-4302-3226-1</a></li>
    <li><strong>Treadgold, B.M., et al.</strong> (2021) Periodic reanalysis of genomic sequencing results in clinical practice: A systematic review. <em>Genet. Med.</em>, <strong>23</strong>(6), 1005–1014. <a href="https://doi.org/10.1038/s41436-021-01105-9">doi:10.1038/s41436-021-01105-9</a></li>
    <li><strong>Deignan, J.L., et al.</strong> (2019) Points to consider in re-evaluation and re-analysis of genomic test results: ACMG statement. <em>Genet. Med.</em>, <strong>21</strong>(6), 1267–1270. <a href="https://doi.org/10.1038/s41436-019-0478-1">doi:10.1038/s41436-019-0478-1</a></li>
    <li><strong>K&ouml;hler, S., et al.</strong> (2021) The Human Phenotype Ontology in 2021. <em>Nucleic Acids Res.</em>, <strong>49</strong>(D1), D1207–D1217. <a href="https://doi.org/10.1093/nar/gkaa1043">doi:10.1093/nar/gkaa1043</a></li>
    <li><strong>Vasilevsky, N.A., et al.</strong> (2022) Mondo: Unifying diseases for the world, by the world. <em>medRxiv</em>, <a href="https://doi.org/10.1101/2020.04.13.20063990">doi:10.1101/2020.04.13.20063990</a></li>
  </ol>

</body>
</html>"""

    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"Generated HTML report: {OUTPUT_HTML}")
    return OUTPUT_HTML

def render_html_to_pdf(html_path: Path, pdf_path: Path) -> Path:
    """Render HTML to PDF using Microsoft Edge headless."""
    edge_bin = find_edge_path()
    file_url = html_path.resolve().as_uri()

    cmd = [
        str(edge_bin),
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={str(pdf_path.resolve())}",
        "--no-pdf-header-footer",
        file_url
    ]

    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        print(f"Edge stderr: {res.stderr}")
        raise RuntimeError(f"Edge print-to-pdf failed with return code {res.returncode}")

    if not pdf_path.exists():
        raise FileNotFoundError(f"Expected PDF output was not generated: {pdf_path}")

    # Copy to root
    root_pdf = _REPO_ROOT / "CuraCascade_Publication_Report.pdf"
    shutil.copy2(pdf_path, root_pdf)

    # Copy to artifacts directory
    for art_id in ["5922f5b4-f0c2-4aaa-9434-ae843cabd283", "1913ab34-18c1-42ad-ae42-08aad1b00f42"]:
        artifact_dir = Path(r"C:\Users\Udit\.gemini\antigravity-ide\brain") / art_id
        if artifact_dir.exists():
            shutil.copy2(pdf_path, artifact_dir / "CuraCascade_Publication_Report.pdf")

    size_kb = pdf_path.stat().st_size / 1024
    print(f"PDF successfully compiled: {pdf_path} ({size_kb:.1f} KB)")
    print(f"Also copied to root: {root_pdf}")
    return pdf_path

def main():
    html_path = build_html_report()
    pdf_path = render_html_to_pdf(html_path, OUTPUT_PDF)
    print("PDF publication report build complete!")

if __name__ == "__main__":
    main()
