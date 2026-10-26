from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import pypdf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
SCREENSHOT_DIR = FIG_DIR / "screenshots"
HTML_OUT = REPO_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.html"
PDF_OUT = REPO_ROOT / "CuraCascade_Presentation_Redesigned.pdf"
DOCS_PDF = REPO_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.pdf"

CHROME_EXE = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
if not CHROME_EXE.exists():
    CHROME_EXE = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")


def build_presentation_html():
    s1_uri = (SCREENSHOT_DIR / "cropped_s1_dashboard_hero.png").as_uri()
    s2_uri = (SCREENSHOT_DIR / "cropped_s2_audit_table_full.png").as_uri()
    s3_uri = (SCREENSHOT_DIR / "cropped_s3_custom_gene_evaluator.png").as_uri()
    s4_uri = (SCREENSHOT_DIR / "cropped_s4_gene_detail_actn2.png").as_uri()
    arch_uri = (FIG_DIR / "figure_schema_architecture.png").as_uri()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CuraCascade Presentation Redesigned</title>
<style>
  @page {{
    size: 13.333in 7.5in;
    margin: 0;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #071426;
    color: #F5F8FC;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .slide {{
    width: 13.333in;
    height: 7.5in;
    page-break-after: always;
    position: relative;
    padding: 0.5in 0.8in 0.6in 0.8in;
    background: #071426;
    overflow: hidden;
  }}
  .top-accent-bar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 13.333in;
    height: 6px;
    background: #36D6C5;
  }}
  .header-category {{
    font-size: 10pt;
    font-weight: 700;
    color: #36D6C5;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .header-title {{
    font-size: 22pt;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 4px;
  }}
  .header-subtitle {{
    font-size: 11pt;
    color: #8FA0B8;
    margin-bottom: 24px;
  }}
  .footer {{
    position: absolute;
    bottom: 0.25in;
    left: 0.8in;
    right: 0.8in;
    border-top: 1px solid #1E3A5F;
    padding-top: 6px;
    font-size: 8.5pt;
    color: #5A6C82;
    display: flex;
    justify-content: space-between;
  }}
  .card {{
    background: #10233D;
    border: 1px solid #1E3A5F;
    border-radius: 4px;
    padding: 16px 20px;
  }}
  .card-top-accent {{
    border-top: 4px solid #36D6C5;
  }}
  .card-top-amber {{
    border-top: 4px solid #FFA63D;
  }}
  .card-top-red {{
    border-top: 4px solid #FF5C5C;
  }}
  .card-top-cyan {{
    border-top: 4px solid #55B9FF;
  }}
  .card-top-green {{
    border-top: 4px solid #10B981;
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
  }}
  .grid-4 {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 16px;
  }}
  .grid-5 {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
  }}
  h3 {{
    font-size: 13pt;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
  }}
  p, li {{
    font-size: 10pt;
    color: #8FA0B8;
    line-height: 1.45;
  }}
  ul {{
    margin-left: 18px;
    margin-top: 6px;
  }}
  li {{
    margin-bottom: 4px;
  }}
  .metric-large {{
    font-size: 26pt;
    font-weight: 800;
    color: #FFFFFF;
    margin: 4px 0;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    font-size: 8pt;
    font-weight: 700;
    border-radius: 3px;
    margin-bottom: 6px;
  }}
  .badge-teal {{ background: rgba(54, 214, 197, 0.15); color: #36D6C5; border: 1px solid #36D6C5; }}
  .badge-amber {{ background: rgba(255, 166, 61, 0.15); color: #FFA63D; border: 1px solid #FFA63D; }}
  .badge-red {{ background: rgba(255, 92, 92, 0.15); color: #FF5C5C; border: 1px solid #FF5C5C; }}
  .badge-cyan {{ background: rgba(85, 185, 255, 0.15); color: #55B9FF; border: 1px solid #55B9FF; }}
  .badge-green {{ background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid #10B981; }}
  .img-frame {{
    width: 100%;
    border-radius: 4px;
    border: 1px solid #1E3A5F;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: TITLE -->
<div class="slide" style="display: flex; flex-direction: column; justify-content: center;">
  <div class="top-accent-bar"></div>
  <div class="header-category">RESEARCH CAPSTONE & ACADEMIC PROJECT DEFENSE • BIOMEDICAL INFORMATICS</div>
  <h1 style="font-size: 42pt; font-weight: 800; color: #FFFFFF; line-height: 1.1; margin-bottom: 8px;">CuraCascade</h1>
  <div style="font-size: 16pt; color: #55B9FF; margin-bottom: 24px;">An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis</div>
  
  <div class="grid-2" style="margin-top: 10px;">
    <div class="card" style="padding: 20px;">
      <div class="badge badge-teal">LEAD SYSTEM ARCHITECT</div>
      <div style="font-size: 18pt; font-weight: 700; color: #FFFFFF; margin-top: 4px;">Udit Shokeen</div>
      <p style="margin-top: 6px; color: #8FA0B8;">
        Registration No: 23BCB0001<br>
        School of Computer Science and Engineering (SCOPE)<br>
        Vellore Institute of Technology, Vellore, Tamil Nadu, India<br>
        Institutional Email: udit.shokeen2023@vitstudent.ac.in
      </p>
      <div style="margin-top: 10px; font-size: 9.5pt; font-weight: 700; color: #10B981;">
        Course: Biological Databases • Project Defense Viva
      </div>
    </div>
    
    <div class="card" style="padding: 20px;">
      <div class="badge badge-cyan">ENGINEERING RIGOR & DELIVERABLES</div>
      <ul style="margin-top: 8px;">
        <li><b style="color: #FFFFFF;">Core Stack:</b> Python 3.11+ • 3NF Normalized SQLite • DuckDB OLAP</li>
        <li><b style="color: #FFFFFF;">Live Deployment:</b> curacascadev2.streamlit.app (Real-time Portal)</li>
        <li><b style="color: #FFFFFF;">Cascade Engine:</b> Deterministic Disease-Aware Concept Crosswalk</li>
        <li><b style="color: #FFFFFF;">Validation Suite:</b> 100-Gene Adjudication Benchmark (94 Evaluable)</li>
        <li><b style="color: #FFFFFF;">Quality Gate:</b> 47/47 Passing Tests in Pytest • SHA-256 Provenance</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 1 of 15</span>
  </div>
</div>

<!-- SLIDE 2: THE PROBLEM -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">01 // THE CLINICAL CHALLENGE</div>
  <div class="header-title">The Evidence Synchronization Gap in Translational Genomics</div>
  <div class="header-subtitle">Upstream expert validity reappraisals fail to automatically propagate to downstream clinical databases.</div>

  <div class="grid-3">
    <div class="card card-top-amber">
      <div class="badge badge-amber">1. UPSTREAM REAPPRAISAL</div>
      <h3>ClinGen Expert Curation</h3>
      <p>ClinGen Gene Curation Expert Panels (GCEPs) systematically re-evaluate published gene-disease claims against modern cohort evidence.</p>
      <p style="margin-top: 8px;">Historically published candidate genes are formally downgraded to Limited, Disputed, or Refuted when replication fails.</p>
      <div style="margin-top: 16px; border-top: 1px solid #1E3A5F; padding-top: 8px;">
        <p style="color: #FFFFFF;"><b>ClinGen Tiers:</b> Disputed / Refuted</p>
        <p style="color: #FFFFFF;"><b>Unit of Analysis:</b> Gene-Disease Dyad</p>
      </div>
    </div>

    <div class="card card-top-red">
      <div class="badge badge-red">2. DOWNSTREAM INERTIA</div>
      <h3>Static Assertion Latency</h3>
      <p>Clinical databases (ClinVar) and diagnostic panels (PanelApp) do not automatically synchronize when an upstream gene is downgraded.</p>
      <p style="margin-top: 8px;">Laboratories continue submitting Pathogenic / Likely Pathogenic (P/LP) assertions for years due to decentralized curation backlogs.</p>
      <div style="margin-top: 16px; border-top: 1px solid #1E3A5F; padding-top: 8px;">
        <p style="color: #FF5C5C;"><b>Median Latency:</b> 2.82 Years (1,030 Days)</p>
        <p style="color: #FFFFFF;"><b>Impacted Assertions:</b> 51,007 ClinVar Records</p>
      </div>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">3. GOVERNANCE DISCREPANCY</div>
      <h3>Diagnostic Review Need</h3>
      <p>Clinicians risk issuing diagnostic sign-outs and recommendations based on invalid gene attributions.</p>
      <p style="margin-top: 8px;">Unwarranted predictive cascade testing in relatives and inappropriate invasive interventions (e.g. ICD placement in refuted arrhythmia genes) require expert audit.</p>
      <div style="margin-top: 16px; border-top: 1px solid #1E3A5F; padding-top: 8px;">
        <p style="color: #36D6C5;"><b>Primary Risk:</b> False-Positive Attribution</p>
        <p style="color: #FFFFFF;"><b>Remediation:</b> VUS Cap / Panel Demotion</p>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 2 of 15</span>
  </div>
</div>

<!-- SLIDE 3: FRAGMENTATION -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">02 // ROOT CAUSE ANALYSIS</div>
  <div class="header-title">Why Existing Workflows Fail: Multi-Repository Semantic Fragmentation</div>
  <div class="header-subtitle">Biomedical databases operate on disparate ontologies, evidence granularities, and update cadences.</div>

  <div class="grid-4">
    <div class="card card-top-teal">
      <div class="badge badge-teal">CLINGEN</div>
      <h3>Gene-Disease Validity</h3>
      <ul style="margin-top: 8px;">
        <li><b>Entity:</b> Gene-Disease (G, D)</li>
        <li><b>Ontology:</b> MONDO IDs</li>
        <li><b>Matrix:</b> 6 Qualitative Tiers</li>
        <li><b>Authority:</b> GCEP Panels</li>
        <li><b>Constraint:</b> No direct variant-level assertions.</li>
      </ul>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">NCBI CLINVAR</div>
      <h3>Variant Significance</h3>
      <ul style="margin-top: 8px;">
        <li><b>Entity:</b> Allelic Variant (G, V)</li>
        <li><b>Ontology:</b> MedGen / OMIM</li>
        <li><b>Matrix:</b> ACMG 5-Tier (P/LP/VUS)</li>
        <li><b>Authority:</b> Voluntary Submissions</li>
        <li><b>Constraint:</b> No automated check on gene validity.</li>
      </ul>
    </div>

    <div class="card card-top-amber">
      <div class="badge badge-amber">PANELAPP</div>
      <h3>Diagnostic Panels</h3>
      <ul style="margin-top: 8px;">
        <li><b>Entity:</b> Diagnostic Panel (G, P)</li>
        <li><b>Ontology:</b> Clinical Indications</li>
        <li><b>Matrix:</b> Green, Amber, Red</li>
        <li><b>Authority:</b> NHS GMS Reviewers</li>
        <li><b>Constraint:</b> Panel BED files lag refutations.</li>
      </ul>
    </div>

    <div class="card card-top-green">
      <div class="badge badge-green">GNOMAD V4</div>
      <h3>Population Genetics</h3>
      <ul style="margin-top: 8px;">
        <li><b>Entity:</b> Population Frequency</li>
        <li><b>Ontology:</b> Global & Popmax Ancestry</li>
        <li><b>Matrix:</b> Quantitative Allele Freq</li>
        <li><b>Authority:</b> Broad Institute</li>
        <li><b>Constraint:</b> Lacks clinical disease phenotypes.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 3 of 15</span>
  </div>
</div>

<!-- SLIDE 4: SOLUTION PIPELINE -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">03 // THE CURACASCADE SOLUTION</div>
  <div class="header-title">Deterministic 5-Stage Cross-Layer Audit Pipeline</div>
  <div class="header-subtitle">End-to-end automated framework ingesting, harmonizing, auditing, and triaging genomic discrepancies.</div>

  <div class="grid-5">
    <div class="card card-top-teal">
      <div class="badge badge-teal">STAGE 01</div>
      <h3>Multi-Source Ingest</h3>
      <p>Automated fetchers pull raw ClinGen curations, ClinVar releases, PanelApp APIs, and gnomAD frequencies with SHA-256 provenance logging.</p>
    </div>
    <div class="card card-top-cyan">
      <div class="badge badge-cyan">STAGE 02</div>
      <h3>Ontology Normalization</h3>
      <p>Resolves disparate disease terminology via a 3-tier MONDO-to-MedGen crosswalk; standardizes HGNC symbols and clinical MIM terms.</p>
    </div>
    <div class="card card-top-amber">
      <div class="badge badge-amber">STAGE 03</div>
      <h3>3NF Warehouse</h3>
      <p>Dual-engine storage: SQLite 3NF relational database for strict consistency + DuckDB OLAP views for rapid cross-database join execution.</p>
    </div>
    <div class="card card-top-red">
      <div class="badge badge-red">STAGE 04</div>
      <h3>Cascade Auditor</h3>
      <p>Deterministic rule-based joining of upstream ClinGen downgrades with downstream ClinVar P/LP assertions and PanelApp Green tiers.</p>
    </div>
    <div class="card card-top-green">
      <div class="badge badge-green">STAGE 05</div>
      <h3>Decision Support</h3>
      <p>Interactive Streamlit web portal, automated CLI runner (run.py), and ISO 15189 compliant governance dossiers for laboratory triage.</p>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 4 of 15</span>
  </div>
</div>

<!-- SLIDE 5: ARCHITECTURE -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">04 // SYSTEM ARCHITECTURE</div>
  <div class="header-title">System Architecture: Dual-Engine Data Warehouse</div>
  <div class="header-subtitle">Coupling SQLite transactional 3NF integrity with DuckDB columnar analytical aggregation.</div>

  <div class="grid-2">
    <div>
      <img src="{arch_uri}" class="img-frame" style="max-height: 4.8in; object-fit: contain;">
    </div>
    <div class="card" style="padding: 20px;">
      <div class="badge badge-teal">FOUR-PILLAR ARCHITECTURAL RIGOR</div>
      <ul style="margin-top: 10px;">
        <li><b style="color: #55B9FF;">1. Transactional Integrity (SQLite 3NF):</b> 9 normalized relational tables, foreign key cascading, compound indexes on (gene_symbol, disease_id), and automated uniqueness constraints.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">2. Analytical OLAP Acceleration (DuckDB):</b> In-memory columnar engine executing complex multi-database joins across 50,000+ variants in sub-10ms response times.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">3. Cryptographic Provenance:</b> Dedicated provenance table capturing SHA-256 checksums, snapshot dates, and transformation versioning for full ISO 15189 traceability.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">4. Dual Execution Modality:</b> Fully headless command-line interface (run.py) for automated CI/CD bioinformatics pipelines alongside an interactive clinical decision support web portal.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 5 of 15</span>
  </div>
</div>

<!-- SLIDE 6: DISEASE-AWARE MATCHING -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">05 // CORE INNOVATION</div>
  <div class="header-title">Disease-Aware Concept Crosswalk & Disambiguation</div>
  <div class="header-subtitle">Preventing false positives by distinguishing non-downgraded pleiotropic disease entities.</div>

  <div class="grid-2">
    <div class="card card-top-amber">
      <div class="badge badge-amber">THE PITFALL OF GENE-SYMBOL MATCHING</div>
      <h3>Gene Pleiotropy Problem</h3>
      <p>Naive tools match records purely by HGNC symbol. This creates severe false positives because human genes are pleiotropic (associated with multiple distinct conditions).</p>
      
      <div style="background: rgba(0,0,0,0.3); border-radius: 4px; padding: 12px; margin-top: 10px;">
        <b style="color: #55B9FF;">CASE IN POINT: ACTN2 (Actinin Alpha 2)</b>
        <p style="margin-top: 4px; font-size: 9.5pt;">• Curation A: Hypertrophic Cardiomyopathy (HCM) → <b style="color: #FF5C5C;">REFUTED</b></p>
        <p style="font-size: 9.5pt;">• Curation B: Distal Myopathy → <b style="color: #10B981;">DEFINITIVE</b></p>
        <p style="margin-top: 6px; font-size: 9pt; color: #10B981;">A naive join flags ALL ACTN2 variants. CuraCascade's disease-aware engine inspects phenotypes: Distal Myopathy variants remain VALID; only HCM assertions are flagged.</p>
      </div>

      <div style="margin-top: 12px;">
        <b style="color: #FFFFFF;">ClinGen Validity Tiers Are Not Interchangeable:</b>
        <p style="font-size: 9pt; margin-top: 2px;">• <b>Refuted:</b> Conclusive evidence AGAINST validity.</p>
        <p style="font-size: 9pt;">• <b>Disputed:</b> Conflicting evidence across published cohorts.</p>
        <p style="font-size: 9pt;">• <b>Limited:</b> Insufficient evidence; replication lacking.</p>
      </div>
    </div>

    <div class="card card-top-teal">
      <div class="badge badge-teal">CURACASCADE MATCHING HEURISTICS</div>
      <h3>Deterministic Crosswalk Rules</h3>
      <ul style="margin-top: 8px;">
        <li><b style="color: #55B9FF;">Rule 1: Direct Identifier Match:</b> Exact code match on MONDO, OMIM, or MedGen concept ID (RULE_DIRECT_IDENTIFIER_EXACT).</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">Rule 2: Canonical Synonym Crosswalk:</b> Harmonization against curated alias registry with strict word boundaries, excluding loose substrings (RULE_CANONICAL_SYNONYM_MATCH).</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">Rule 3: Distinct Disorder Exclusion:</b> Explicitly identifies alternative non-downgraded conditions, returning DISEASE_MISMATCH (prevents false alarms).</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">Rule 4: Missing Phenotype Handling:</b> Unspecified terms ('not provided') routed to DATA_QUALITY_ISSUE rather than asserted discrepancies.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 6 of 15</span>
  </div>
</div>

<!-- SLIDE 7: LIVE UI WALKTHROUGH -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">06 // SOFTWARE DEMONSTRATION</div>
  <div class="header-title">Live Clinical Decision Support Portal (curacascadev2.streamlit.app)</div>
  <div class="header-subtitle">Real-time laboratory triage interface deployed on Streamlit Cloud.</div>

  <div class="grid-2">
    <div>
      <img src="{s1_uri}" class="img-frame" style="max-height: 2.3in; object-fit: contain; margin-bottom: 8px;">
      <img src="{s2_uri}" class="img-frame" style="max-height: 2.3in; object-fit: contain;">
    </div>
    <div class="card" style="padding: 18px;">
      <div class="badge badge-teal">VERIFIED DEPLOYED CAPABILITIES</div>
      <ul style="margin-top: 8px;">
        <li><b style="color: #55B9FF;">1. Real-Time Warehouse HUD (Top Left):</b> Sidebar live monitor displays exact database layer metrics: 36 Curated Genes, 46 ClinVar Variants, 25 PanelApp Records, and 34 Materialized Discrepancies.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">2. Top Clinical KPI Telemetry (Top):</b> Executive telemetry cards quantifying curated genes (36), total discrepancies (34), critical Class A findings (20), warning Class B findings (8), and 202.5 patient-years at risk.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">3. Interactive Audit Findings Explorer (Bottom):</b> Materialized table listing unpropagated records across GJB6, MYLK2, TCAP, DFNB59, CACNA2D1, MYOZ2, ANK2, and GPD1L with explicit prescriptive remediation guidance.</li>
        <li style="margin-top: 8px;"><b style="color: #55B9FF;">4. Prescriptive Governance Directives:</b> Translates audit findings into concrete laboratory directives (e.g. 'Apply ACMG BA1/BS1 Benign' or 'Demote Panel to Red') citing ClinGen GCEP determination reports.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 7 of 15</span>
  </div>
</div>

<!-- SLIDE 8: CLINICAL CASE STUDIES -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">07 // CLINICAL CASE STUDIES</div>
  <div class="header-title">Clinical Discrepancy Auditing in Cardiomyopathy & Arrhythmia</div>
  <div class="header-subtitle">Deep-dive examination of unpropagated evidence downgrades in SCN1B, MYLK2, and ACTN2.</div>

  <div class="grid-2">
    <div>
      <img src="{s4_uri}" class="img-frame" style="max-height: 2.3in; object-fit: contain; margin-bottom: 8px;">
      <img src="{s3_uri}" class="img-frame" style="max-height: 2.3in; object-fit: contain;">
    </div>
    <div class="card" style="padding: 18px;">
      <div class="badge badge-teal">REAL-WORLD CLINICAL AUDIT FINDINGS</div>
      <div style="margin-top: 8px;">
        <b style="color: #FF5C5C;">SCN1B — Brugada Syndrome (Class A Finding):</b>
        <p style="font-size: 9.5pt; margin-top: 2px;">• ClinGen Curation: DISPUTED in 2021 by Arrhythmia GCEP.</p>
        <p style="font-size: 9.5pt;">• Downstream Status: 18 ClinVar Pathogenic / Likely Pathogenic assertions remain active.</p>
        <p style="font-size: 9.5pt; color: #FFA63D;">• Clinical Hazard: Risk of false-positive diagnosis and unwarranted prophylactic implantable cardioverter-defibrillator (ICD) surgeries.</p>
      </div>

      <div style="margin-top: 12px;">
        <b style="color: #FF5C5C;">MYLK2 — Hypertrophic Cardiomyopathy (Class C Finding):</b>
        <p style="font-size: 9.5pt; margin-top: 2px;">• ClinGen Curation: DISPUTED in 2024 (Kelly et al., Circulation).</p>
        <p style="font-size: 9.5pt;">• Downstream Status: Listed as GREEN (diagnostic-grade) on PanelApp panels.</p>
        <p style="font-size: 9.5pt; color: #FFA63D;">• Clinical Hazard: Uncurated variants enter routine exome filtering pipelines in active hospital services.</p>
      </div>

      <div style="margin-top: 12px;">
        <b style="color: #10B981;">ACTN2 — Disease-Aware Biological Specificity:</b>
        <p style="font-size: 9.5pt; margin-top: 2px;">• Demonstrated above: CuraCascade identifies ACTN2 as a Definitive benchmark for Distal Myopathy while suppressing false alerts for non-cardiac conditions.</p>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 8 of 15</span>
  </div>
</div>

<!-- SLIDE 9: BENCHMARK METHOD -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">08 // VALIDATION METHODOLOGY</div>
  <div class="header-title">Empirical 100-Gene Adjudication Validation Benchmark</div>
  <div class="header-subtitle">Independent expert validation cohort evaluating classifier precision, recall, and label boundaries.</div>

  <div class="grid-3">
    <div class="card card-top-teal">
      <div class="badge badge-teal">1. GOLD STANDARD</div>
      <h3>100 Gene-Disease Dyads</h3>
      <p>Independently frozen assertions:</p>
      <ul style="margin-top: 8px;">
        <li><b>54 Published Downgraded Genes:</b> Verified from literature and ClinGen GCEPs (Cardiomyopathy, Arrhythmia, Cancer, Neurodevelopmental).</li>
        <li style="margin-top: 8px;"><b>46 Definitive Controls:</b> Unquestioned associations (ACMG SF v3.2 / National Genomic Test Directory, e.g. BRCA1, TP53, MLH1, CFTR).</li>
      </ul>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">2. PARTITIONING</div>
      <h3>Evaluable Cohort</h3>
      <p>Strict epidemiological cohort breakdown:</p>
      <ul style="margin-top: 8px;">
        <li><b>Evaluable Cohort (N = 94):</b> Target genes and curations present in warehouse snapshot, permitting empirical join evaluation.</li>
        <li style="margin-top: 8px;"><b>Excluded Cases (N = 6):</b> Designated as NOT_EVALUABLE due to complete absence of gene or curation records in snapshot (XRCC3, DFNB59, TSC1, TSC2, SMAD3, SMN1).</li>
      </ul>
    </div>

    <div class="card card-top-green">
      <div class="badge badge-green">3. LABEL FIREWALL</div>
      <h3>Evaluation Rigor</h3>
      <p>Strict scientific protocols:</p>
      <ul style="margin-top: 8px;">
        <li><b>Zero Overrides:</b> Hardcoded exceptions (KNOWN_FN, KNOWN_FP) completely removed.</li>
        <li style="margin-top: 6px;"><b>Live Queries:</b> Dynamic evaluation against active relational database.</li>
        <li style="margin-top: 6px;"><b>Wilson 95% CIs:</b> Binomial performance intervals computed analytically.</li>
        <li style="margin-top: 6px;"><b>Concordance Kappa:</b> Classifier agreement evaluated.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 9 of 15</span>
  </div>
</div>

<!-- SLIDE 10: BENCHMARK RESULTS -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">09 // BENCHMARK RESULTS</div>
  <div class="header-title">Empirical Results: The Precision–Recall Trade-Off</div>
  <div class="header-subtitle">Conservative disease matching achieves zero false positives (100% PPV) at the cost of moderate recall.</div>

  <div class="grid-2">
    <div class="card card-top-teal">
      <div class="badge badge-teal">EVALUABLE CONFUSION MATRIX (N = 94)</div>
      
      <div class="grid-2" style="margin-top: 14px; gap: 12px;">
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; border-radius: 4px; padding: 12px;">
          <div style="font-size: 8.5pt; font-weight: 700; color: #10B981;">TRUE POSITIVES (TP)</div>
          <div class="metric-large">18</div>
          <p style="font-size: 8pt; color: #8FA0B8;">Correctly flagged discrepancies</p>
        </div>
        <div style="background: rgba(54, 214, 197, 0.1); border: 1px solid #36D6C5; border-radius: 4px; padding: 12px;">
          <div style="font-size: 8.5pt; font-weight: 700; color: #36D6C5;">FALSE POSITIVES (FP)</div>
          <div class="metric-large">0</div>
          <p style="font-size: 8pt; color: #8FA0B8;">Zero false alarms raised</p>
        </div>
        <div style="background: rgba(255, 166, 61, 0.1); border: 1px solid #FFA63D; border-radius: 4px; padding: 12px;">
          <div style="font-size: 8.5pt; font-weight: 700; color: #FFA63D;">FALSE NEGATIVES (FN)</div>
          <div class="metric-large">34</div>
          <p style="font-size: 8pt; color: #8FA0B8;">Undetected discrepancies</p>
        </div>
        <div style="background: rgba(85, 185, 255, 0.1); border: 1px solid #55B9FF; border-radius: 4px; padding: 12px;">
          <div style="font-size: 8.5pt; font-weight: 700; color: #55B9FF;">TRUE NEGATIVES (TN)</div>
          <div class="metric-large">42</div>
          <p style="font-size: 8pt; color: #8FA0B8;">Definitive controls ruled out</p>
        </div>
      </div>

      <div style="margin-top: 14px; border-top: 1px solid #1E3A5F; padding-top: 8px;">
        <p style="font-size: 9pt;">• <b>Denominator:</b> 94 Evaluable (52 Gold Downgraded + 42 Definitive Controls)</p>
        <p style="font-size: 9pt;">• <b>Sensitivity Analysis (All 100):</b> Recall = 33.3%, Accuracy = 64.0%</p>
      </div>
    </div>

    <div class="card card-top-green">
      <div class="badge badge-green">STATISTICAL PERFORMANCE METRICS</div>
      <ul style="margin-top: 10px;">
        <li><b style="color: #10B981; font-size: 11pt;">Precision (PPV): 100.0%</b> <span style="color: #8FA0B8;">(95% CI: 82.4%–100.0%)</span><br>
        <span style="font-size: 9pt;">Zero false alarms; every flagged finding represents a verified discrepancy.</span></li>
        
        <li style="margin-top: 8px;"><b style="color: #FFA63D; font-size: 11pt;">Recall (Sensitivity): 34.6%</b> <span style="color: #8FA0B8;">(95% CI: 23.2%–48.2%)</span><br>
        <span style="font-size: 9pt;">Moderate sensitivity due to conservative disease matching and missing assertions.</span></li>
        
        <li style="margin-top: 8px;"><b style="color: #10B981; font-size: 11pt;">Specificity (TNR): 100.0%</b> <span style="color: #8FA0B8;">(95% CI: 91.6%–100.0%)</span><br>
        <span style="font-size: 9pt;">Perfect rejection of definitive clinical controls (e.g. BRCA1, CFTR, TP53).</span></li>
        
        <li style="margin-top: 8px;"><b style="color: #55B9FF; font-size: 11pt;">Overall Accuracy: 63.8%</b> <span style="color: #8FA0B8;">(95% CI: 53.8%–72.8%)</span><br>
        <span style="font-size: 9pt;">Concordance across all 94 evaluable gene-disease validity assertions.</span></li>
        
        <li style="margin-top: 8px;"><b style="color: #55B9FF; font-size: 11pt;">Concordance Kappa: 0.3212</b> <span style="color: #8FA0B8;">(Fair Agreement)</span><br>
        <span style="font-size: 9pt;">Classifier concordance kappa against frozen adjudication ground truth.</span></li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 10 of 15</span>
  </div>
</div>

<!-- SLIDE 11: ERROR ANALYSIS -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">10 // ERROR ANALYSIS & LIMITATIONS</div>
  <div class="header-title">Dissecting the 34 False Negatives: Failure Mode Breakdown</div>
  <div class="header-subtitle">Transparently accounting for undetected benchmark cases across evidence availability and biological specificity.</div>

  <div class="grid-3">
    <div class="card card-top-amber">
      <div class="badge badge-amber">CATEGORY A (44.1%)</div>
      <h3>15 Cases: Absent Downstream Assertions</h3>
      <p><b>Root Cause:</b> While literature documents a panel downgrade, local ClinVar snapshots contained no Pathogenic/Likely Pathogenic variants, or PanelApp lacked Green status.</p>
      <p style="margin-top: 8px;"><b>Interpretation:</b> Data availability constraint, not an algorithmic defect. An auditor cannot flag an assertion that does not exist in the ingested database snapshot.</p>
      <p style="margin-top: 8px; font-size: 9pt; color: #FFFFFF;"><b>Exemplar Genes:</b> NEXN, KCNJ8, HCN4, KCNE3, TRPM4, RAD50, XRCC2.</p>
    </div>

    <div class="card card-top-red">
      <div class="badge badge-red">CATEGORY B (8.8%)</div>
      <h3>3 Cases: Missing Target Curations</h3>
      <p><b>Root Cause:</b> Target ClinGen gene-disease validity curations were absent from the static warehouse snapshot at the time of ingest.</p>
      <p style="margin-top: 8px;"><b>Interpretation:</b> Ingestion completeness issue. Updating the ClinGen snapshot to the latest release resolves these cases immediately.</p>
      <p style="margin-top: 8px; font-size: 9pt; color: #FFFFFF;"><b>Exemplar Genes:</b> CAV3, CSRP3, JPH2 (HCM reappraisals).</p>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">CATEGORY C (47.1%)</div>
      <h3>16 Cases: Cross-Disease Phenotypic Mismatches</h3>
      <p><b>Root Cause:</b> Downstream ClinVar variants in these genes were asserted for distinct phenotypic conditions rather than the downgraded indication.</p>
      <p style="margin-top: 8px;"><b>Interpretation:</b> Protective biological conservatism. Relaxing matching rules would increase recall but introduce false positives in multi-disease genes.</p>
      <p style="margin-top: 8px; font-size: 9pt; color: #FFFFFF;"><b>Exemplar Genes:</b> BARD1, BRIP1, RAD51C, FANCA, MLH1, MSH2, PMS2.</p>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 11 of 15</span>
  </div>
</div>

<!-- SLIDE 12: EXPLORATORY ANALYTICS -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">11 // EXPLORATORY ANALYTICS</div>
  <div class="header-title">Retrospective Risk Forecasting & Evidence Latency Kinetics</div>
  <div class="header-subtitle">Exploratory Random Forest triage modeling and cross-sectional empirical latency distribution.</div>

  <div class="grid-2">
    <div class="card card-top-teal">
      <div class="badge badge-teal">1. MACHINE LEARNING TRIAGE</div>
      <h3>Downgrade Risk Forecasting</h3>
      <p>Supervised Balanced Random Forest predicting downgrade vulnerability of currently supported genes across 7 engineered features (gnomAD popmax AF, low-star ratio, curation age, MCAF violation rate):</p>
      
      <ul style="margin-top: 8px;">
        <li><b style="color: #55B9FF;">Test Set AUROC: 0.857</b> (Random Forest vs Logistic Regression 0.824)</li>
        <li><b style="color: #55B9FF;">Brier Calibration Score: 0.1508</b> (Evaluated on held-out test split)</li>
        <li><b style="color: #55B9FF;">Precision @ Top-20%: 75.8%</b> (High enrichment in top risk quintile)</li>
      </ul>

      <div style="background: rgba(255, 166, 61, 0.1); border: 1px solid #FFA63D; border-radius: 4px; padding: 10px; margin-top: 12px;">
        <b style="color: #FFA63D; font-size: 9pt;">CRITICAL METHODOLOGICAL CAVEATS:</b>
        <p style="font-size: 8.5pt; margin-top: 2px;">Features were extracted from static cross-sectional snapshots rather than pre-downgrade historical archives. Demonstrates retrospective discriminatory capacity; not claimed as prospective clinical forecasting.</p>
      </div>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">2. EMPIRICAL LATENCY</div>
      <h3>Cross-Sectional Latency Kinetics</h3>
      <p>Cross-sectional analysis of <b>51,007 ClinVar assertions across 536 unique genes</b> measuring elapsed duration from ClinGen appraisal date to snapshot date:</p>
      
      <ul style="margin-top: 8px;">
        <li><b style="color: #10B981;">Median Latency: 2.82 Years (1,030 Days)</b></li>
        <li><b>Interquartile Range (IQR):</b> 1.87 to 4.85 Years (684–1,771 Days)</li>
        <li><b>Commercial Labs:</b> 2.80 Years Median (N = 17,747)</li>
        <li><b>Academic Consortia:</b> 2.84 Years Median (N = 33,260, Mann-Whitney p < 0.001)</li>
        <li><b>Class A Discrepancies:</b> 2.80 Years Median (N = 34,800)</li>
        <li><b>Class B Discrepancies:</b> 3.77 Years Median (N = 16,207)</li>
      </ul>

      <p style="font-size: 8.5pt; color: #8FA0B8; margin-top: 10px;">
        *Analysis represents active cross-sectional elapsed duration in a static warehouse snapshot, not longitudinal time to resolution.
      </p>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 12 of 15</span>
  </div>
</div>

<!-- SLIDE 13: ENGINEERING -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">12 // ENGINEERING RIGOR</div>
  <div class="header-title">Software Engineering Standards, Testing & Reproducibility</div>
  <div class="header-subtitle">Verification suite, CI/CD automated gates, Docker containerization, and forensic provenance.</div>

  <div class="grid-2">
    <div class="card card-top-green" style="margin-bottom: 12px;">
      <div class="badge badge-green">AUTOMATED TEST SUITE</div>
      <h3>47 Passed (100% Pass Rate in Pytest)</h3>
      <p style="font-size: 9.5pt;">Complete verification suite executed via pytest in 48.9 seconds:</p>
      <ul style="margin-top: 4px; font-size: 9pt;">
        <li><b>test_biological_matching.py (21 tests):</b> Pleiotropy, multi-disease genes, ontology crosswalks.</li>
        <li><b>test_database_integrity.py (9 tests):</b> Foreign key cascading, schema migrations, constraints.</li>
        <li><b>test_scientific_statistical_integrity.py (6 tests):</b> Wilson score intervals, confusion matrices.</li>
        <li><b>test_cli.py & test_dossier.py (11 tests):</b> Headless CLI runners and dossier exports.</li>
      </ul>
    </div>

    <div class="card card-top-teal" style="margin-bottom: 12px;">
      <div class="badge badge-teal">CRYPTOGRAPHIC PROVENANCE</div>
      <h3>Forensic Audit Logging</h3>
      <p style="font-size: 9.5pt;">Dedicated provenance SQLite table logging SHA-256 checksums for every ingested raw asset:</p>
      <ul style="margin-top: 4px; font-size: 9pt;">
        <li>Records source URLs, retrieval timestamps, transformation versions, and raw row counts.</li>
        <li>Ensures any regulatory audit can trace an audit finding back to the exact byte-level snapshot.</li>
      </ul>
    </div>

    <div class="card card-top-cyan">
      <div class="badge badge-cyan">CLINICAL COMPLIANCE DOSSIERS</div>
      <h3>ISO 15189 Aligned Reporting</h3>
      <p style="font-size: 9.5pt;">Automated markdown compilation of Clinical Governance Dossiers and Remediation Memos:</p>
      <ul style="margin-top: 4px; font-size: 9pt;">
        <li>Cites ClinGen GCEP determination reports, ACMG SVI rules, and PanelApp guidelines.</li>
        <li>Formats structured remediation memos ready for medical laboratory director sign-off.</li>
      </ul>
    </div>

    <div class="card card-top-amber">
      <div class="badge badge-amber">PRODUCTION PACKAGING</div>
      <h3>Containerization & Automation</h3>
      <p style="font-size: 9.5pt;">Production deployment and distribution:</p>
      <ul style="margin-top: 4px; font-size: 9pt;">
        <li>Single-command CLI execution (python run.py --mode audit --db ...).</li>
        <li>Fully containerized Dockerfile for isolated execution across hospital environments.</li>
        <li>Streamlit Cloud CI/CD auto-deployment synchronized with GitHub main branch.</li>
      </ul>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 13 of 15</span>
  </div>
</div>

<!-- SLIDE 14: RESEARCH CONTRIBUTIONS -->
<div class="slide">
  <div class="top-accent-bar"></div>
  <div class="header-category">13 // RESEARCH IMPACT</div>
  <div class="header-title">Key Research Contributions & Scientific Value</div>
  <div class="header-subtitle">Bridging the gene-to-variant semantic gap in modern clinical genomics informatics.</div>

  <div class="grid-2">
    <div class="card card-top-teal" style="margin-bottom: 14px;">
      <div class="badge badge-teal">CONTRIBUTION 01</div>
      <h3>Multi-Ontology Evidence Synchronization</h3>
      <p>Created the first automated relational framework synchronizing ClinGen GCEP gene-disease validity curations (MONDO) with NCBI ClinVar variant assertions (MedGen) and Genomics England PanelApp panels.</p>
    </div>

    <div class="card card-top-cyan" style="margin-bottom: 14px;">
      <div class="badge badge-cyan">CONTRIBUTION 02</div>
      <h3>Biologically Specific Concept Crosswalk</h3>
      <p>Formulated a deterministic concept mapping engine that resolves multi-disease pleiotropy, successfully eliminating false positive alerts across multi-phenotype benchmark genes like ACTN2 and SCN1B.</p>
    </div>

    <div class="card card-top-amber">
      <div class="badge badge-amber">CONTRIBUTION 03</div>
      <h3>Empirical Evidence Lag Characterization</h3>
      <p>Quantified an empirical 2.82-year cross-sectional evidence propagation latency across 51,007 assertions, demonstrating that laboratory inertia is a measurable structural bottleneck in genomic medicine.</p>
    </div>

    <div class="card card-top-green">
      <div class="badge badge-green">CONTRIBUTION 04</div>
      <h3>Open-Source Clinical Governance Tooling</h3>
      <p>Delivered an accessible, interactive decision support web application and automated dossier generator designed to accelerate quality-assurance re-curation for molecular pathology directors.</p>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 14 of 15</span>
  </div>
</div>

<!-- SLIDE 15: CONCLUSION & QA -->
<div class="slide" style="display: flex; flex-direction: column; justify-content: center;">
  <div class="top-accent-bar"></div>
  <div class="header-category">14 // CONCLUSION & VIVA DEFENSE</div>
  <h1 style="font-size: 32pt; font-weight: 800; color: #FFFFFF; line-height: 1.15; margin-bottom: 6px;">Summary, Future Roadmap & Open Discussion</h1>
  <div style="font-size: 14pt; color: #55B9FF; margin-bottom: 24px;">Advancing translational genomics through automated evidence auditing and decision support.</div>

  <div class="grid-2">
    <div class="card" style="padding: 20px;">
      <div class="badge badge-teal">FUTURE RESEARCH DIRECTIONS</div>
      <ul style="margin-top: 8px;">
        <li><b style="color: #FFFFFF;">Longitudinal Event Tracking:</b> Transition from cross-sectional snapshots to prospective monthly change tracking to measure true time-to-resolution.</li>
        <li style="margin-top: 6px;"><b style="color: #FFFFFF;">Expanded Concept Crosswalks:</b> Incorporate automated LLM-assisted disease entity normalization to increase benchmark recall without compromising specificity.</li>
        <li style="margin-top: 6px;"><b style="color: #FFFFFF;">Multi-Reviewer Blinded Benchmark:</b> Expand the 100-case validation benchmark to a multi-center consortium with blinded independent adjudicators for inter-rater kappa.</li>
        <li style="margin-top: 6px;"><b style="color: #FFFFFF;">EHR Integration via SMART-on-FHIR:</b> Deliver real-time electronic health record alerts when historical patient variants are flagged for retrospective audit.</li>
      </ul>
    </div>

    <div class="card" style="padding: 20px;">
      <div class="badge badge-cyan">PROJECT ARTIFACTS & LINKS</div>
      <ul style="margin-top: 8px;">
        <li><b style="color: #FFFFFF;">Live Dashboard:</b> curacascadev2.streamlit.app</li>
        <li><b style="color: #FFFFFF;">GitHub Repository:</b> github.com/uditshokeen14/curacascade</li>
        <li><b style="color: #FFFFFF;">Manuscript:</b> docs/CuraCascade_IEEE_Report_Revised.pdf</li>
        <li><b style="color: #FFFFFF;">Docker Container:</b> curacascade:v2.4-production</li>
      </ul>

      <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #1E3A5F;">
        <div style="font-size: 20pt; font-weight: 800; color: #36D6C5;">Questions & Discussion</div>
        <p style="margin-top: 4px; color: #8FA0B8;">I welcome questions, technical critiques, and suggestions from the committee.</p>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>CuraCascade: Clinical Evidence Downgrade Audit Engine • Udit Shokeen (23BCB0001, VIT CSE)</span>
    <span>Slide 15 of 15</span>
  </div>
</div>

</body>
</html>
"""

    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Generated Presentation HTML at: {HTML_OUT}")


def convert_html_to_pdf():
    print(f"🖨️ Printing static 16:9 widescreen PDF using Chrome headless...")
    cmd = [
        str(CHROME_EXE),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUT}",
        str(HTML_OUT),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and PDF_OUT.exists():
        # Copy to docs as well
        DOCS_PDF.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(PDF_OUT, DOCS_PDF)
        
        # Verify page count with pypdf
        reader = pypdf.PdfReader(str(PDF_OUT))
        print(f"✅ Static Presentation PDF successfully generated at:")
        print(f"   1. {PDF_OUT} ({len(reader.pages)} pages, {PDF_OUT.stat().st_size:,} bytes)")
        print(f"   2. {DOCS_PDF}")
    else:
        print(f"❌ PDF generation failed: {res.stderr}")


if __name__ == "__main__":
    build_presentation_html()
    convert_html_to_pdf()
