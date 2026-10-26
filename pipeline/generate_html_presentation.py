"""Generate an interactive, standalone HTML presentation deck for CuraCascade.

Features:
- Responsive 16:9 slide container with dark/light themes.
- Keyboard navigation (Left, Right, Space, Home, End, F for Fullscreen, N for Notes).
- Toggleable Presenter Notes drawer with word-for-word spoken defense scripts.
- Embedded high-res figures and publication badges.
- Slide jump menu and progress bar.
"""

from pathlib import Path
import base64

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
OUTPUT_HTML = REPO_ROOT / "docs" / "CuraCascade_Presentation.html"
ROOT_HTML = REPO_ROOT / "CuraCascade_Presentation.html"

def get_b64(path: Path) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    ext = path.suffix.lstrip(".").lower()
    mime = "image/png" if ext == "png" else "image/svg+xml" if ext == "svg" else "image/jpeg"
    return f"data:{mime};base64,{b64}"

def build_presentation_html():
    fig_lag = get_b64(FIG_DIR / "figure_knowledge_lag.png")
    fig_schema = get_b64(FIG_DIR / "figure_schema_architecture.png")
    fig_tax = get_b64(FIG_DIR / "figure_taxonomy_tree.png")
    fig_surv = get_b64(FIG_DIR / "figure_survival_cox.png")
    fig_ml = get_b64(FIG_DIR / "figure_ml_benchmarks.png")
    fig_val = get_b64(FIG_DIR / "figure_validation_matrix.png")

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CuraCascade: Academic Defense & Project Presentation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-dark: #0a192f;
    --navy-slate: #0f172a;
    --card-dark: #1e293b;
    --text-white: #ffffff;
    --text-slate: #94a3b8;
    --text-dark: #0f172a;
    --text-muted: #64748b;
    --border-light: #e2e8f0;
    --blue: #2563eb;
    --blue-bg: #eff6ff;
    --teal: #0d9488;
    --teal-bg: #f0fdfa;
    --emerald: #10b981;
    --rose: #e11d48;
    --rose-bg: #fff1f2;
    --amber: #d97706;
    --amber-bg: #fef3c7;
    --purple: #7c3aed;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #000000;
    color: #0f172a;
    overflow: hidden;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  /* Top Navigation & Toolbar */
  .toolbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 48px;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid #1e293b;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 1000;
    color: #94a3b8;
    font-size: 13px;
  }

  .toolbar-brand {
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .toolbar-brand span {
    color: var(--teal);
    font-size: 11px;
    background: rgba(13, 148, 136, 0.2);
    padding: 2px 8px;
    border-radius: 4px;
  }

  .toolbar-controls {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .btn {
    background: #1e293b;
    border: 1px solid #334155;
    color: #e2e8f0;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
  }

  .btn:hover {
    background: #334155;
    border-color: #475569;
    color: #ffffff;
  }

  .btn-primary {
    background: var(--blue);
    border-color: var(--blue);
    color: #ffffff;
  }

  .btn-primary:hover {
    background: #1d4ed8;
  }

  /* Presentation Stage */
  .stage {
    width: 100vw;
    height: calc(100vh - 48px);
    margin-top: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 20px;
  }

  .slide-container {
    width: 1333px;
    max-width: 95vw;
    aspect-ratio: 16 / 9;
    max-height: calc(100vh - 88px);
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    overflow: hidden;
    position: relative;
    display: none;
    flex-direction: column;
  }

  .slide-container.active {
    display: flex;
    animation: fadeIn 0.2s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0.7; transform: scale(0.99); }
    to { opacity: 1; transform: scale(1); }
  }

  /* Dark Slide Theme */
  .slide-dark {
    background: var(--bg-dark);
    color: #ffffff;
  }

  .slide-light {
    background: #f8fafc;
    color: #0f172a;
  }

  /* Slide Internal Layout */
  .slide-header {
    padding: 30px 48px 10px 48px;
  }

  .slide-category {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--blue);
    margin-bottom: 5px;
  }

  .slide-dark .slide-category {
    color: var(--teal);
  }

  .slide-title {
    font-size: 25px;
    font-weight: 800;
    color: var(--navy-slate);
    line-height: 1.2;
  }

  .slide-dark .slide-title {
    color: #ffffff;
  }

  .slide-subtitle {
    font-size: 12.5px;
    color: var(--text-muted);
    margin-top: 4px;
    line-height: 1.4;
  }

  .slide-dark .slide-subtitle {
    color: var(--text-slate);
  }

  .slide-body {
    flex: 1;
    padding: 10px 48px 24px 48px;
    display: grid;
    gap: 16px;
    overflow-y: auto;
  }

  .grid-2 {
    grid-template-columns: 1fr 1fr;
  }

  .grid-3 {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .grid-4 {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }

  .grid-left-fig {
    grid-template-columns: 1.15fr 0.85fr;
  }

  .grid-right-fig {
    grid-template-columns: 0.9fr 1.1fr;
  }

  /* Cards */
  .card {
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    display: flex;
    flex-direction: column;
  }

  .slide-dark .card {
    background: var(--card-dark);
    border-color: #334155;
  }

  .card-title {
    font-size: 12.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
  }

  .card ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 7px;
  }

  .card li {
    font-size: 12px;
    line-height: 1.45;
    color: #334155;
    position: relative;
    padding-left: 14px;
  }

  .slide-dark .card li {
    color: #cbd5e1;
  }

  .card li::before {
    content: "•";
    color: var(--blue);
    font-weight: bold;
    position: absolute;
    left: 0;
  }

  .card strong {
    color: #0f172a;
  }

  .slide-dark .card strong {
    color: #ffffff;
  }

  /* Stat Badges */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 6px;
  }

  .stat-card {
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 14px;
    text-align: left;
  }

  .stat-val {
    font-size: 24px;
    font-weight: 800;
    line-height: 1.1;
  }

  .stat-label {
    font-size: 11.5px;
    font-weight: 700;
    color: var(--navy-slate);
    margin-top: 4px;
  }

  .stat-sub {
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 2px;
  }

  .stat-red { background: var(--rose-bg); border-color: rgba(225, 29, 72, 0.3); }
  .stat-red .stat-val { color: var(--rose); }

  .stat-amber { background: var(--amber-bg); border-color: rgba(217, 119, 6, 0.3); }
  .stat-amber .stat-val { color: var(--amber); }

  .stat-emerald { background: #ecfdf5; border-color: rgba(16, 185, 129, 0.3); }
  .stat-emerald .stat-val { color: var(--emerald); }

  .stat-blue { background: var(--blue-bg); border-color: rgba(37, 99, 235, 0.3); }
  .stat-blue .stat-val { color: var(--blue); }

  /* Figure Images */
  .figure-box {
    background: #ffffff;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .figure-box img {
    max-width: 100%;
    max-height: 380px;
    object-fit: contain;
    border-radius: 6px;
  }

  .slide-footer {
    height: 32px;
    border-top: 1px solid var(--border-light);
    padding: 0 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 10px;
    color: var(--text-muted);
  }

  .slide-dark .slide-footer {
    border-top-color: #1e293b;
    color: var(--text-slate);
  }

  /* Notes Drawer */
  .notes-drawer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0f172a;
    border-top: 2px solid var(--blue);
    color: #e2e8f0;
    padding: 16px 32px;
    max-height: 220px;
    overflow-y: auto;
    z-index: 2000;
    display: none;
    box-shadow: 0 -10px 25px rgba(0,0,0,0.5);
  }

  .notes-drawer.open {
    display: block;
  }

  .notes-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--teal);
  }

  .notes-content {
    font-size: 13.5px;
    line-height: 1.6;
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
  }

  /* Progress Bar */
  .progress-bar-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: #1e293b;
    z-index: 1001;
  }

  .progress-bar {
    height: 100%;
    background: var(--blue);
    width: 5%;
    transition: width 0.2s ease;
  }
</style>
</head>
<body>

<div class="toolbar">
  <div class="toolbar-brand">
    🧬 CuraCascade <span>RESEARCH DEFENSE</span>
  </div>
  <div class="toolbar-controls">
    <span id="slide-indicator">Slide 1 of 20</span>
    <button class="btn" onclick="prevSlide()" title="Previous Slide (Left Arrow)">◀ Prev</button>
    <button class="btn" onclick="nextSlide()" title="Next Slide (Right Arrow or Space)">Next ▶</button>
    <button class="btn" onclick="toggleNotes()" id="notes-btn" title="Toggle Presenter Script (N)">🎙️ Speaker Script (N)</button>
    <button class="btn" onclick="toggleFullscreen()" title="Fullscreen (F)">⛶ Fullscreen</button>
    <a href="CuraCascade_Presentation.pptx" download class="btn btn-primary" title="Download PowerPoint .pptx">📥 Download PPTX</a>
    <a href="CuraCascade_Publication_Report.pdf" target="_blank" class="btn" title="View Publication PDF Report">📄 Publication Report (PDF)</a>
  </div>
</div>

<div class="progress-bar-container">
  <div class="progress-bar" id="progress-bar"></div>
</div>

<div class="stage">

  <!-- SLIDE 1: Title -->
  <div class="slide-container slide-dark active" id="slide-1">
    <div style="height: 6px; background: var(--blue); width: 100%;"></div>
    <div class="slide-header" style="padding-top: 48px;">
      <div class="slide-category">RESEARCH CAPSTONE & ACADEMIC PROJECT DEFENSE • CLINICAL GENOMICS INFORMATICS</div>
      <div class="slide-title" style="font-size: 42px; line-height: 1.1; margin-top: 8px;">CuraCascade</div>
      <div class="slide-subtitle" style="font-size: 18px; color: #94a3b8; margin-top: 8px;">
        An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades
      </div>
    </div>
    <div class="slide-body grid-2" style="margin-top: 12px;">
      <div class="card" style="background: #1e293b; border-color: #334155;">
        <div class="card-title" style="color: var(--blue);">RESEARCHER & LEAD ARCHITECT</div>
        <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-bottom: 6px;">Udit Shokeen</div>
        <p style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
          School of Computer Science and Engineering (SCOPE)<br>
          Vellore Institute of Technology, Vellore, Tamil Nadu, India<br>
          Contact: <strong>uditshokeen14@gmail.com</strong>
        </p>
        <div style="margin-top: 16px; padding: 10px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 6px; font-size: 12px; color: var(--emerald); font-weight: 600;">
          🎓 Academic Project Evaluation & Thesis Defense
        </div>
      </div>
      <div class="card" style="background: #1e293b; border-color: #334155;">
        <div class="card-title" style="color: var(--teal);">SYSTEM HIGHLIGHTS & DELIVERABLES</div>
        <ul>
          <li><strong>Core Stack:</strong> Python 3.11+ | SQLite 3NF | DuckDB Columnar In-Memory Engine</li>
          <li><strong>Machine Learning:</strong> Balanced Random Forest & Multivariate Cox Proportional Hazards</li>
          <li><strong>CI/CD Automation:</strong> GitHub Actions Automated Audit Gates & Docker Container</li>
          <li><strong>Live Portal:</strong> <span style="color: var(--teal);">curacascade.streamlit.app</span> (Interactive Clinical App)</li>
          <li><strong>Source Repository:</strong> <span style="color: var(--blue);">github.com/uditshokeen14/curacascade</span> (MIT License)</li>
          <li><strong>Publication PDF:</strong> 15-Page Academic Manuscript with Vector Figures & Data Dictionaries</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 1 of 20</span>
    </div>
  </div>

  <!-- SLIDE 2: Executive Summary -->
  <div class="slide-container slide-light" id="slide-2">
    <div class="slide-header">
      <div class="slide-category">EXECUTIVE SUMMARY</div>
      <div class="slide-title">The Clinical Genomics Dilemma at a Glance</div>
      <div class="slide-subtitle">Why upstream evidence updates fail to reach hospital bedsides and how CuraCascade fixes it.</div>
    </div>
    <div class="slide-body" style="display: flex; flex-direction: column;">
      <div class="stat-grid">
        <div class="stat-card stat-red">
          <div class="stat-val">3.2 Years</div>
          <div class="stat-label">Median Latency</div>
          <div class="stat-sub">Delay before downstream retraction</div>
        </div>
        <div class="stat-card stat-amber">
          <div class="stat-val">51,251</div>
          <div class="stat-label">Materialized Lag</div>
          <div class="stat-sub">Discrepancies flagged genome-wide</div>
        </div>
        <div class="stat-card stat-emerald">
          <div class="stat-val">96.3%</div>
          <div class="stat-label">Join Precision</div>
          <div class="stat-sub">PPV vs blinded expert adjudication</div>
        </div>
        <div class="stat-card stat-blue">
          <div class="stat-val">AUROC 0.857</div>
          <div class="stat-label">ML Prediction</div>
          <div class="stat-sub">Genome-wide downgrade vulnerability</div>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex: 1;">
        <div class="card">
          <div class="card-title" style="color: var(--rose);">THE ASYNCHRONOUS KNOWLEDGE DISCONNECT</div>
          <ul>
            <li><strong>Evidence Consensus Shift:</strong> ClinGen panels re-evaluate published genes, downgrading up to 40% to Disputed, Refuted, or Limited.</li>
            <li><strong>Decentralized Lag:</strong> Downstream clinical databases (NCBI ClinVar, PanelApp) operate in silos with no automated synchronization push.</li>
            <li><strong>Direct Clinical Harm:</strong> Patients receive false-positive diagnoses, undergoing unnecessary ICD surgeries, sports bans, and emotional distress.</li>
            <li><strong>Lack of Tooling:</strong> Hospital laboratories accredited under CAP/CLIA lack automated infrastructure to continuously audit their variant databases.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title" style="color: var(--teal);">THE CURACASCADE COMPUTATIONAL SOLUTION</div>
          <ul>
            <li><strong>3NF Normalized Warehouse:</strong> Integrates ClinGen, ClinVar, PanelApp, and gnomAD v4 with dual SQLite/DuckDB engines.</li>
            <li><strong>3-Tier Audit Heuristics:</strong> Deterministically categorizes discrepancies into Classes A, B, and C with automated POSIX exit codes.</li>
            <li><strong>Survival Kinetics:</strong> Kaplan-Meier and multivariate Cox regression model assertion lifespans, identifying a 0.55x commercial lab latency penalty.</li>
            <li><strong>Supervised ML Forecaster:</strong> Balanced Random Forest flags currently supported genes vulnerable to impending downgrade.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 2 of 20</span>
    </div>
  </div>

  <!-- SLIDE 3: Clinical Background -->
  <div class="slide-container slide-light" id="slide-3">
    <div class="slide-header">
      <div class="slide-category">BACKGROUND & CLINICAL RELEVANCE</div>
      <div class="slide-title">Gene Curation & The ClinGen Framework</div>
      <div class="slide-subtitle">Understanding how genetic validity is established and why historical disease associations fail.</div>
    </div>
    <div class="slide-body grid-3">
      <div class="card">
        <div class="card-title" style="color: var(--navy-slate);">1. THE HISTORICAL ERA</div>
        <ul>
          <li><strong>Candidate-Gene Studies (1990s–2000s):</strong> Many monogenic disease associations were published on small kindreds without adequate statistical controls.</li>
          <li><strong>Absent Reference Populations:</strong> Reference databases like gnomAD did not exist; naturally rare benign variants were mistaken for dominant mutations.</li>
          <li><strong>Panel Contamination:</strong> Hundreds of spurious genes made their way onto commercial diagnostic sequencing panels.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--blue);">2. CLINGEN VALIDITY TIERS</div>
        <ul>
          <li><strong>Standardized Matrix:</strong> Gene Curation Expert Panels (GCEPs) evaluate genetic evidence (max 12 pts) and experimental evidence (max 6 pts).</li>
          <li><strong>Formal Qualitative Tiers:</strong><br>
            • Definitive / Strong (12–18 pts)<br>
            • Moderate (7–11 pts)<br>
            • Limited (1–6 pts)<br>
            • Disputed (Conflicting evidence)<br>
            • Refuted (Proven not to cause disease)</li>
          <li><strong>Standardized Re-appraisals:</strong> GCEPs systematically re-appraise published genes.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--rose);">3. LANDMARK REAPPRAISALS</div>
        <ul>
          <li><strong>Cardiovascular Genetics:</strong> Landmark GCEP reappraisals (Ingles et al., 2019; Hosseini et al., 2018) showed up to 40% of cardiomyopathy genes lacked validity!</li>
          <li><strong>Discredited Genes:</strong> Landmark genes like <em>MYLK2</em>, <em>TCAP</em>, <em>MYOZ2</em>, <em>KCNE2</em>, and <em>SCN1B</em> were downgraded to Disputed or Refuted.</li>
          <li><strong>ACMG Guidelines:</strong> Mandate that variants in Disputed/Refuted genes should NEVER be classified as Pathogenic.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 3 of 20</span>
    </div>
  </div>

  <!-- SLIDE 4: Knowledge Cascade Lag -->
  <div class="slide-container slide-light" id="slide-4">
    <div class="slide-header">
      <div class="slide-category">PROBLEM FORMULATION</div>
      <div class="slide-title">The "Knowledge Cascade" Synchronization Lag</div>
      <div class="slide-subtitle">Why downstream clinical databases fail to synchronize when upstream evidence is invalidated.</div>
    </div>
    <div class="slide-body grid-right-fig">
      <div class="card">
        <div class="card-title" style="color: var(--rose);">DECENTRALIZED ARCHITECTURAL FAILURE</div>
        <ul>
          <li><strong>Decoupled Ecosystem:</strong> ClinGen (curation), NCBI ClinVar (variant archive), and PanelApp (diagnostic panels) are maintained by distinct global agencies without an integrated event bus.</li>
          <li><strong>No Automated Webhooks:</strong> When ClinGen publishes a downgrade, downstream registries receive no push notifications to trigger re-curation.</li>
          <li><strong>The Latency Clock:</strong> Downstream databases lag by a median of 3.2 years (and up to 7+ years in commercial testing laboratories).</li>
          <li><strong>Bedside Contamination:</strong> Outdated Pathogenic (P/LP) records persist in ClinVar, while diagnostic exome panels continue routine screening and reporting.</li>
        </ul>
      </div>
      <div class="figure-box">
        <img src="FIG_LAG_PLACEHOLDER" alt="Figure 1: Knowledge Cascade Lag">
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 4 of 20</span>
    </div>
  </div>

  <!-- SLIDE 5: Clinical Harm -->
  <div class="slide-container slide-light" id="slide-5">
    <div class="slide-header">
      <div class="slide-category">CLINICAL IMPACT & BIOETHICS</div>
      <div class="slide-title">Real-World Clinical Harm & Patient Impact</div>
      <div class="slide-subtitle">Tangible repercussions of unpropagated evidence downgrades on patients, families, and healthcare systems.</div>
    </div>
    <div class="slide-body" style="display: flex; flex-direction: column; gap: 16px;">
      <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; flex: 1;">
        <div class="card">
          <div class="card-title" style="color: var(--rose);">CASE 1: MYLK2 & TCAP</div>
          <div style="font-size: 11px; font-style: italic; color: var(--text-muted); margin-bottom: 8px;">Hypertrophic Cardiomyopathy (HCM)</div>
          <ul>
            <li><strong>ClinGen Status:</strong> Refuted by Cardiovascular GCEP.</li>
            <li><strong>ClinVar Reality:</strong> Retained 1-star Pathogenic assertions for years.</li>
            <li><strong>Harm:</strong> Asymptomatic patients misdiagnosed with fatal HCM; received unneeded sports bans and surgical ICD implants.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title" style="color: var(--rose);">CASE 2: SCN1B & KCNE2</div>
          <div style="font-size: 11px; font-style: italic; color: var(--text-muted); margin-bottom: 8px;">Brugada Syndrome & Long QT</div>
          <ul>
            <li><strong>ClinGen Status:</strong> Disputed as cause of Brugada syndrome.</li>
            <li><strong>ClinVar Reality:</strong> Retained multi-submitter Pathogenic status.</li>
            <li><strong>Harm:</strong> Unwarranted cascade screening across extended families, causing severe psychological trauma and medication.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title" style="color: var(--rose);">CASE 3: NBN & RAD50</div>
          <div style="font-size: 11px; font-style: italic; color: var(--text-muted); margin-bottom: 8px;">Hereditary Breast & Ovarian Cancer</div>
          <ul>
            <li><strong>ClinGen Status:</strong> Downgraded to Limited validity.</li>
            <li><strong>ClinVar Reality:</strong> Variants interpreted above VUS ceiling.</li>
            <li><strong>Harm:</strong> Premature diagnostic closure. Patients undergoing risk-reducing mastectomies while true genetic causes remain uninvestigated.</li>
          </ul>
        </div>
      </div>
      <div class="card" style="background: var(--rose-bg); border-color: rgba(225, 29, 72, 0.4); padding: 14px 20px;">
        <div class="card-title" style="color: var(--rose); margin-bottom: 4px;">THE ACCUMULATION OF 'PATIENT-YEARS AT RISK'</div>
        <p style="font-size: 12px; line-height: 1.5; color: #1e293b;">
          The duration between upstream consortium refutation and downstream retraction represents active, unmitigated clinical exposure. Across thousands of active clinical testing panels globally, unpropagated refutations accumulate hundreds of thousands of <strong>patient-years at risk</strong>, during which discredited variants continue to be returned to unsuspecting patients.
        </p>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 5 of 20</span>
    </div>
  </div>

  <!-- SLIDE 6: Solution Overview (Four Pillars) -->
  <div class="slide-container slide-light" id="slide-6">
    <div class="slide-header">
      <div class="slide-category">SYSTEM ARCHITECTURE</div>
      <div class="slide-title">CuraCascade Solution Architecture: Four Core Pillars</div>
      <div class="slide-subtitle">A modular, end-to-end framework integrating data warehousing, deterministic auditing, survival kinetics, and machine learning.</div>
    </div>
    <div class="slide-body grid-4">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">PILLAR 1: 3NF DATA WAREHOUSE</div>
        <ul>
          <li>Normalizes ClinGen, ClinVar, PanelApp, and gnomAD v4.</li>
          <li>Third Normal Form (3NF) relational architecture.</li>
          <li>Dual-engine: Transactional SQLite + Columnar DuckDB in-memory scanner.</li>
          <li>Composite indexing on (gene_symbol, disease_id).</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--teal);">PILLAR 2: DETERMINISTIC AUDIT ENGINE</div>
        <ul>
          <li>Formal heuristics defining Classes A, B, and C.</li>
          <li>Automated join engine materializing unpropagated lag.</li>
          <li>Headless CLI (<code>run.py audit</code>) with POSIX exit codes (0/1/2).</li>
          <li>CI/CD integration for automated quality gate checks.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--purple);">PILLAR 3: SURVIVAL KINETICS</div>
        <ul>
          <li>Time-to-event formulation of assertion lifespan.</li>
          <li>Kaplan–Meier non-parametric survival estimators.</li>
          <li>Multivariate Cox Proportional Hazards regression.</li>
          <li>Quantifies commercial laboratory and star-rating hazard ratios.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--amber);">PILLAR 4: ML TRIAGE FORECASTER</div>
        <ul>
          <li>Balanced Random Forest predicting impending downgrades.</li>
          <li>7 engineered biological & registry features.</li>
          <li>Strict temporal train/test validation split (pre/post-2021).</li>
          <li>Generates calibrated clinical triage priority queues.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 6 of 20</span>
    </div>
  </div>

  <!-- SLIDE 7: 3NF Relational Warehouse -->
  <div class="slide-container slide-light" id="slide-7">
    <div class="slide-header">
      <div class="slide-category">DATABASE ARCHITECTURE & DESIGN</div>
      <div class="slide-title">3NF Relational Warehouse Architecture</div>
      <div class="slide-subtitle">Normalized schema design, foreign key integrity, and dual-engine transactional/analytical processing.</div>
    </div>
    <div class="slide-body grid-right-fig">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">DATABASE DESIGN PRINCIPLES</div>
        <ul>
          <li><strong>Entity Normalization (3NF):</strong> Eliminates biological data redundancy across 5 core tables: <code>genes</code>, <code>diseases</code>, <code>clingen_curations</code>, <code>clinvar_variants</code>, and <code>panelapp_entries</code>.</li>
          <li><strong>Strict Integrity Constraints:</strong> Foreign keys enforce referential integrity with cascading checks (<code>PRAGMA foreign_keys = ON</code>).</li>
          <li><strong>Dual-Engine Architecture:</strong> Transactional SQLite manages point lookups and CLI operations. An in-memory DuckDB columnar scanner attaches directly to SQLite for vectorized analytical aggregation across 50,000+ variants.</li>
          <li><strong>Composite Indexing:</strong> Multi-column B-Tree indexes on <code>(gene_symbol, disease_id)</code> enable sub-millisecond multi-table cross-layer joins.</li>
        </ul>
      </div>
      <div class="figure-box">
        <img src="FIG_SCHEMA_PLACEHOLDER" alt="Figure 2: 3NF Schema Architecture">
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 7 of 20</span>
    </div>
  </div>

  <!-- SLIDE 8: Audit Taxonomy -->
  <div class="slide-container slide-light" id="slide-8">
    <div class="slide-header">
      <div class="slide-category">AUDIT ENGINE ALGORITHMS</div>
      <div class="slide-title">Audit Classification Taxonomy & Heuristics</div>
      <div class="slide-subtitle">Deterministic rule-based stratification of downstream discrepancies into actionable clinical severity tiers.</div>
    </div>
    <div class="slide-body grid-right-fig">
      <div class="card">
        <div class="card-title" style="color: var(--teal);">THE THREE DISCREPANCY CLASSES</div>
        <ul>
          <li><strong style="color: var(--rose);">CLASS A (CRITICAL):</strong> ClinVar asserts Pathogenic (P) or Likely Pathogenic (LP) variants in Disputed or Refuted genes.<br>
            • <em>Risk:</em> Acute false-positive monogenic diagnosis.<br>
            • <em>Rule:</em> (ClinGen in {Disputed, Refuted}) ∧ (ClinVar is_plp = 1)</li>
          <li><strong style="color: var(--amber);">CLASS B (HIGH):</strong> ClinVar asserts P/LP variants in Limited-evidence genes.<br>
            • <em>Risk:</em> Violates ACMG ceiling (variants in Limited genes must not exceed VUS).<br>
            • <em>Rule:</em> (ClinGen = Limited) ∧ (ClinVar is_plp = 1)</li>
          <li><strong style="color: var(--rose);">CLASS C (CRITICAL):</strong> PanelApp retains Green (diagnostic-grade) status in Disputed or Refuted genes.<br>
            • <em>Risk:</em> Routine NHS GMS exome panels screen and report invalid genes.<br>
            • <em>Rule:</em> (ClinGen in {Disputed, Refuted}) ∧ (PanelApp tier = Green)</li>
        </ul>
      </div>
      <div class="figure-box">
        <img src="FIG_TAX_PLACEHOLDER" alt="Figure 3: Audit Classification Taxonomy">
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 8 of 20</span>
    </div>
  </div>

  <!-- SLIDE 9: Population Genetics & MCAF -->
  <div class="slide-container slide-light" id="slide-9">
    <div class="slide-header">
      <div class="slide-category">POPULATION GENOMICS METHODOLOGY</div>
      <div class="slide-title">Population Genetics & MCAF Ceiling Filter</div>
      <div class="slide-subtitle">Using gnomAD v4 and mathematical allele frequency thresholds to refute false-positive assertions.</div>
    </div>
    <div class="slide-body grid-2">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">THE WHIFFIN ET AL. MCAF FRAMEWORK</div>
        <ul>
          <li><strong>Maximum Credible Allele Frequency (MCAF):</strong> The mathematical ceiling above which an allele is too common in the general population to cause a rare Mendelian disorder.</li>
          <li><strong>Dominant Disorders:</strong><br>
            <code>MCAF_dom = (I · h) / (2 · P)</code><br>
            Where <em>I</em> = Disease prevalence (Orphanet), <em>h</em> = Allelic heterogeneity (0.10), <em>P</em> = Penetrance (0.50).</li>
          <li><strong>Recessive Disorders:</strong><br>
            <code>MCAF_rec = √((I · h) / P)</code></li>
          <li><strong>gnomAD v4 Popmax Annotation:</strong> CuraCascade cross-references maximum allele frequency across continental ancestries (AFR, AMR, EAS, NFE, SAS).</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--emerald);">AUTOMATED ACMG BENIGN RULE INVOCATION</div>
        <ul>
          <li><strong>ACMG Rule BA1 (Stand-Alone Benign):</strong> If an allele frequency exceeds 5.0% in any continental population in gnomAD, it is stand-alone benign and cannot cause monogenic disease.</li>
          <li><strong>ACMG Rule BS1 (Strong Benign):</strong> If allele frequency exceeds the calculated MCAF ceiling for the specific disease indication, BS1 is automatically triggered.</li>
          <li><strong>Resolving Ancestral Disparities:</strong> Historically, rare variants in underrepresented ancestries were misclassified as pathogenic because control cohorts were predominantly European. Popmax filtering catches these immediately.</li>
          <li><strong>Evidence Dossier:</strong> Embeds fold-excess frequency multiplier directly into clinical retraction directives.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 9 of 20</span>
    </div>
  </div>

  <!-- SLIDE 10: Survival Kinetics -->
  <div class="slide-container slide-light" id="slide-10">
    <div class="slide-header">
      <div class="slide-category">EVIDENCE LATENCY & SURVIVAL ANALYSIS</div>
      <div class="slide-title">Longitudinal Latency & Survival Kinetics</div>
      <div class="slide-subtitle">Modeling downstream assertion resolution lifespans using Kaplan–Meier and multivariate Cox Proportional Hazards.</div>
    </div>
    <div class="slide-body grid-left-fig">
      <div class="figure-box">
        <img src="FIG_SURV_PLACEHOLDER" alt="Figure 4: Survival Curves and Cox Hazard Ratios">
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--purple);">COX REGRESSION INSIGHTS (C-index = 0.724)</div>
        <ul>
          <li><strong>The Review Star Accelerator (HR = 2.36, p &lt; 0.001):</strong> Assertions with ≥2 review stars resolve 2.36 times faster than 0–1 star assertions. High-star records are actively maintained, whereas 0-star submissions are often abandoned legacy files.</li>
          <li><strong>The Commercial Lab Penalty (HR = 0.55, p &lt; 0.001):</strong> Commercial testing laboratories resolve assertions at nearly HALF the rate of academic centers. Amending past patient reports incurs legal, operational, and financial friction.</li>
          <li><strong>Severity Sensitivity (HR = 2.31, p &lt; 0.001):</strong> Acute Class A refutations resolve 2.3x faster than borderline Class B limited evidence.</li>
          <li><strong>Domain Disparity:</strong> Cardiovascular (HR = 2.37) and cancer (HR = 1.71) resolve much faster than neurology (HR = 0.75).</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 10 of 20</span>
    </div>
  </div>

  <!-- SLIDE 11: ML Forecaster Framework -->
  <div class="slide-container slide-light" id="slide-11">
    <div class="slide-header">
      <div class="slide-category">MACHINE LEARNING ENGINE</div>
      <div class="slide-title">Machine-Learned Downgrade Triage Framework</div>
      <div class="slide-subtitle">Supervised machine learning to forecast impending gene downgrades and prioritize curation queues.</div>
    </div>
    <div class="slide-body grid-3">
      <div class="card">
        <div class="card-title" style="color: var(--amber);">7 ENGINEERED FEATURES</div>
        <ul>
          <li>1. Curation Age (days since last ClinGen formal review)</li>
          <li>2. Total Variant Volume (total cataloged variants in ClinVar)</li>
          <li>3. Asserted P/LP Count (volume of pathogenic variants)</li>
          <li>4. Low ClinVar Star Ratio (fraction with &lt; 2 review stars)</li>
          <li>5. gnomAD Popmax AF (maximum continental frequency)</li>
          <li>6. MCAF Violation Rate (fraction exceeding disease frequency ceiling)</li>
          <li>7. PanelApp Amber/Red Count (non-green panel skepticisms)</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--blue);">MODEL ARCHITECTURE</div>
        <ul>
          <li><strong>Balanced Random Forest:</strong> 100 estimators, max depth 5, inverse class weighting to handle minority downgrade class.</li>
          <li><strong>Logistic Regression Baseline:</strong> L2 regularized balanced logistic regression for linear discrimination baseline.</li>
          <li><strong>Strict Temporal Split:</strong> Train on curations before Jan 1, 2021; Test on curations on/after Jan 1, 2021 to strictly prevent temporal data leakage.</li>
          <li><strong>Permutation Importance:</strong> 10-fold permutation evaluates true non-linear feature contribution.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--emerald);">CLINICAL TRIAGE QUEUE</div>
        <ul>
          <li><strong>Calibrated Probability (S ∈ [0, 1]):</strong> Converts raw ensemble votes into calibrated risk scores.</li>
          <li><strong>High-Risk Queue (S ≥ 0.65):</strong> Flagged for immediate pre-emptive panel review by molecular geneticists.</li>
          <li><strong>Watch Queue (0.35 ≤ S &lt; 0.65):</strong> Scheduled for targeted re-appraisal during annual overhaul.</li>
          <li><strong>Stable (S &lt; 0.35):</strong> High-concordance definitive disease genes.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 11 of 20</span>
    </div>
  </div>

  <!-- SLIDE 12: Empirical ML Results -->
  <div class="slide-container slide-light" id="slide-12">
    <div class="slide-header">
      <div class="slide-category">ML EVALUATION & BENCHMARKS</div>
      <div class="slide-title">Empirical Results: Dual-Regime ML Reporting</div>
      <div class="slide-subtitle">Transparent comparative evaluation between a curated positive control benchmark and the genome-wide empirical corpus.</div>
    </div>
    <div class="slide-body grid-left-fig">
      <div class="figure-box">
        <img src="FIG_ML_PLACEHOLDER" alt="Figure 5: Machine Learning Benchmarks">
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--blue);">HONEST DUAL-REGIME ANALYSIS</div>
        <ul>
          <li><strong>1. Positive Control Benchmark (N = 34):</strong> AUROC = 1.000, Precision@Top-20% = 100%. Linearly separable sanity verification where Curation Age dominates at 78.4% importance.</li>
          <li><strong>2. Genome-Wide Corpus (N = 3,833 genes, 51k variants):</strong> Random Forest AUROC = 0.857 (vs Logistic Regression 0.827), PR-AUC = 0.814, Precision@Top-20% = 75.8%.</li>
          <li><strong>3. The Mechanistic Feature Shift:</strong> In the genome-wide corpus, Curation Age drops to &lt;1%. Instead, Low ClinVar Star Density (70.2%) and PanelApp Discordance (26.0%) become the dominant predictors!</li>
          <li><strong>4. Scientific Takeaway:</strong> In real-world clinical databases, impending downgrades are signaled by conflicting assertions and curator skepticism, not merely passage of time.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 12 of 20</span>
    </div>
  </div>

  <!-- SLIDE 13: Validation Benchmark -->
  <div class="slide-container slide-light" id="slide-13">
    <div class="slide-header">
      <div class="slide-category">CLINICAL VALIDATION BENCHMARK</div>
      <div class="slide-title">Gold-Standard Validation Benchmark</div>
      <div class="slide-subtitle">Evaluating automated join precision against manual blinded adjudication by expert clinical molecular geneticists.</div>
    </div>
    <div class="slide-body grid-left-fig">
      <div class="figure-box">
        <img src="FIG_VAL_PLACEHOLDER" alt="Figure 6: Validation Matrix and Metrics">
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--emerald);">100-GENE CURATED BENCHMARK</div>
        <ul>
          <li><strong>Benchmark Cohort (N = 100):</strong> 54 true published downgrades (cardiovascular, hereditary cancer, neurodevelopmental) vs 46 definitive disease controls.</li>
          <li><strong>Precision (PPV) = 96.3%:</strong> Only 2 false positives out of 54 flagged genes, caused by historical gene symbol aliases that were resolved via HGNC crosswalk.</li>
          <li><strong>Recall (Sensitivity) = 96.3%:</strong> Successfully flagged 52 of 54 verified clinical evidence cascades.</li>
          <li><strong>Specificity = 95.7%:</strong> Accurately cleared 44 of 46 definitive control genes with zero inappropriate flags.</li>
          <li><strong>Cohen's Kappa (κ = 0.920):</strong> Demonstrates near-perfect inter-rater agreement with blinded manual adjudication.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 13 of 20</span>
    </div>
  </div>

  <!-- SLIDE 14: Software Engineering & CI/CD -->
  <div class="slide-container slide-light" id="slide-14">
    <div class="slide-header">
      <div class="slide-category">SOFTWARE ENGINEERING & PRODUCTION INFRASTRUCTURE</div>
      <div class="slide-title">Headless CLI & Automated CI/CD Gates</div>
      <div class="slide-subtitle">Production-grade tooling, POSIX status conventions, Docker containerization, and GitHub Actions workflows.</div>
    </div>
    <div class="slide-body grid-2">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">UNIFIED HEADLESS CLI (run.py)</div>
        <ul>
          <li><strong>Subcommand 'audit':</strong><br>
            <code>python run.py audit --genes BARD1,SCN1B --class all --format table</code><br>
            Exports findings to ASCII tables, JSON payloads, or CSV matrices.</li>
          <li><strong>POSIX Status Conventions for CI Pipelines:</strong><br>
            • Exit 0: Clean audit / Success<br>
            • Exit 1: Critical Class A findings detected (blocks deployment)<br>
            • Exit 2: Integrity or database query failure</li>
          <li><strong>Subcommand 'verify':</strong><br>
            <code>python run.py verify</code><br>
            Executes relational integrity suite (PRAGMA foreign_key_check) and SHA-256 cryptographic provenance verification.</li>
          <li><strong>Subcommand 'serve':</strong> Launches Streamlit dashboard locally on port 8501.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--teal);">ENTERPRISE DEPLOYMENT & CI WORKFLOWS</div>
        <ul>
          <li><strong>GitHub Actions Pipeline (.github/workflows/audit_ci.yml):</strong> Runs on every push/PR to main branch. Automatically provisions environment, runs integrity verification, and executes test suites.</li>
          <li><strong>Comprehensive Pytest Suite:</strong><br>
            • <code>test_cli.py</code>: Validates CLI status codes and formatting.<br>
            • <code>test_dossier.py</code>: Validates clinical governance memo structure and mandatory regulatory sections.</li>
          <li><strong>Docker Containerization (Dockerfile):</strong> Lightweight, reproducible container image with zero external database daemon dependencies.</li>
          <li><strong>Automated Build Artifacts:</strong> Publishes JSON audit summaries and publication PDF directly to workflow artifacts.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 14 of 20</span>
    </div>
  </div>

  <!-- SLIDE 15: Interactive Web Portal -->
  <div class="slide-container slide-light" id="slide-15">
    <div class="slide-header">
      <div class="slide-category">USER INTERFACE & CLINICAL TOOLS</div>
      <div class="slide-title">Clinical Decision Support & Web Portal</div>
      <div class="slide-subtitle">An interactive, executive-grade clinical portal deployed at curacascade.streamlit.app.</div>
    </div>
    <div class="slide-body" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">MODULES 1 & 2: EXECUTIVE KPIS & CUSTOM AUDIT</div>
        <ul>
          <li>Headline metric banners (3,833 genes, 51,251 findings).</li>
          <li>Multi-Gene Custom Audit Portal: laboratory geneticists can paste arbitrary gene lists for instant multi-database cross-referencing.</li>
          <li>Instant summary of downstream ClinVar and PanelApp status.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--teal);">MODULES 3 & 4: INCONSISTENCIES & POPULATION GENETICS</div>
        <ul>
          <li>Interactive discrepancy explorer with sortable variation IDs, ClinGen GCEP links, and elapsed unresolved days.</li>
          <li>gnomAD v4 Population Genetics Inspector with continental popmax frequencies and interactive MCAF ceiling sliders.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--purple);">MODULES 5 & 6: ML TRIAGE QUEUE & SURVIVAL ANALYTICS</div>
        <ul>
          <li>Downgrade Vulnerability Forecaster: ranks supported genes by calibrated risk score and reveals top feature drivers.</li>
          <li>Longitudinal Survival Modeling: interactive Kaplan-Meier curves and multivariate Cox hazard ratio exploration.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--emerald);">MODULES 7 & 8: CLINICAL DOSSIERS & VALIDATION BENCHMARK</div>
        <ul>
          <li>Clinical Governance Dossier Generator: one-click export of regulatory clinical memos in Markdown and PDF format.</li>
          <li>Cross-Layer Validation Benchmark: real-time reporting of PPV (96.3%), Sensitivity, and Cohen's Kappa concordance.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 15 of 20</span>
    </div>
  </div>

  <!-- SLIDE 16: Clinical Governance Dossier -->
  <div class="slide-container slide-light" id="slide-16">
    <div class="slide-header">
      <div class="slide-category">REGULATORY COMPLIANCE & ACCREDITATION</div>
      <div class="slide-title">Clinical Governance & Remediation Dossiers</div>
      <div class="slide-subtitle">Automating regulatory compliance under CAP, CLIA, and ISO 15189:2022 standards.</div>
    </div>
    <div class="slide-body grid-2">
      <div class="card">
        <div class="card-title" style="color: var(--rose);">REGULATORY ACCREDITATION MANDATES</div>
        <ul>
          <li><strong>ISO 15189:2022 Section 7.3:</strong> Mandates that medical laboratories continuously review examination procedures and diagnostic panel contents to ensure ongoing validity.</li>
          <li><strong>CLIA / CAP Requirements:</strong> Requires clinical laboratories to maintain active quality assurance protocols to identify and remediate diagnostic discrepancies.</li>
          <li><strong>The Retraction Dilemma:</strong> When an audit flags a Class A inconsistency, laboratory directors must decide: Which past patient reports require amendment? How should ClinVar submissions be retracted?</li>
          <li><strong>The CuraCascade Firewall:</strong> Acts as an automated pre-report audit firewall in LIMS workflows, halting misclassified variant reports before they reach patients.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--blue);">THE 6-SECTION CLINICAL DOSSIER (pipeline/remediation.py)</div>
        <ul>
          <li><strong>1. Header Directive:</strong> Formal regulatory clinical directive with target gene symbol and evaluation timestamp.</li>
          <li><strong>2. Consensus Metadata Table:</strong> ClinGen GCEP panel identification, classification date, MONDO ID, and evidence URL.</li>
          <li><strong>3. Orthogonal Population Genetics Summary:</strong> gnomAD v4 global & popmax frequency, disease MCAF ceiling, fold-excess multiplier, and ancestry disparity statement.</li>
          <li><strong>4. Downstream Assertions Catalog:</strong> Tabular inventory of all active ClinVar variation IDs and PanelApp diagnostic memberships requiring retraction.</li>
          <li><strong>5. Prescriptive ACMG Remediation Checklist:</strong> Step-by-step guidance to invoke ACMG Rules BA1/BS1, de-escalate variant to Benign/VUS, and initiate patient re-contact protocols.</li>
          <li><strong>6. Formal Attestation Sign-Off Block:</strong> Structured signature blocks for Lead Clinical Molecular Geneticist and Laboratory Medical Director.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 16 of 20</span>
    </div>
  </div>

  <!-- SLIDE 17: Discussion & Limitations -->
  <div class="slide-container slide-light" id="slide-17">
    <div class="slide-header">
      <div class="slide-category">CRITICAL DISCUSSION & LIMITATIONS</div>
      <div class="slide-title">Critical Discussion, Limitations & Ethics</div>
      <div class="slide-subtitle">Proactively addressing operational roadblocks, institutional friction, and ethical responsibilities.</div>
    </div>
    <div class="slide-body grid-3">
      <div class="card">
        <div class="card-title" style="color: var(--rose);">COMMERCIAL LAB INERTIA</div>
        <ul>
          <li>Why do commercial laboratories take longer to retract assertions (HR = 0.55)?</li>
          <li><strong>Legal & Liability Concerns:</strong> Re-contacting ordering physicians and issuing amended diagnostic reports invites legal liability and administrative costs.</li>
          <li><strong>Regulatory Disincentive:</strong> Laboratories often wait for annual panel overhauls rather than executing real-time retract-and-replace updates.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--amber);">ONTOLOGY HARMONIZATION</div>
        <ul>
          <li><strong>Decentralized Ontology Dialects:</strong> ClinGen indexes MONDO concepts, ClinVar indexes MedGen/OMIM, and PanelApp indexes disease names.</li>
          <li><strong>Crosswalk Gaps:</strong> While CuraCascade implements deterministic ontology crosswalks, rare disease subtypes with overlapping phenotypes require ongoing manual curation.</li>
          <li><strong>Variable Penetrance:</strong> Certain genes exhibit reduced penetrance, complicating strict Mendelian MCAF filtering.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--blue);">HUMAN-IN-THE-LOOP ETHICS</div>
        <ul>
          <li><strong>Advisory, Not Autonomous:</strong> CuraCascade is designed as a Decision Support Firewall, not an automated report deleter.</li>
          <li><strong>Human-in-the-Loop:</strong> All flagged Class A findings and ML predictions require review and sign-off by a board-certified clinical geneticist.</li>
          <li><strong>Preventing Harm:</strong> The ethical priority is protecting patients from unnecessary surgeries while ensuring legitimate disease genes are not prematurely dismissed.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 17 of 20</span>
    </div>
  </div>

  <!-- SLIDE 18: Future Work -->
  <div class="slide-container slide-light" id="slide-18">
    <div class="slide-header">
      <div class="slide-category">FUTURE WORK & EXTENSIONS</div>
      <div class="slide-title">Future Directions & System Roadmap</div>
      <div class="slide-subtitle">Strategic extensions for scaling real-time interoperability, natural language processing, and hospital deployment.</div>
    </div>
    <div class="slide-body grid-3">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">1. REAL-TIME WEBHOOKS</div>
        <ul>
          <li><strong>Event-Driven Microservices:</strong> Implement message queues (Kafka/RabbitMQ) listening for real-time ClinGen API webhooks.</li>
          <li><strong>Sub-Hour Synchronization:</strong> Reduce downstream audit latency from monthly batch dumps to minutes following formal GCEP publishing.</li>
          <li><strong>Automated Notifications:</strong> Push alerts directly to diagnostic laboratory directors via webhook integrations.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--teal);">2. LLM LITERATURE CURATION</div>
        <ul>
          <li><strong>Literature Parsing:</strong> Deploy quantized local Large Language Models (LLMs) to scan newly published PubMed abstracts.</li>
          <li><strong>Evidence Extraction:</strong> Automatically extract case kindred counts, functional assay metrics, and segregation ratios for candidate genes.</li>
          <li><strong>Conflict Summarization:</strong> Generate automated synthetic summaries explaining why historical evidence was contradicted.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--purple);">3. EHR & FHIR INTEROPERABILITY</div>
        <ul>
          <li><strong>HL7 FHIR Genomics API:</strong> Integrate directly into hospital Electronic Health Record (EHR) systems (Epic, Cerner).</li>
          <li><strong>Pre-Report Diagnostic Firewall:</strong> Intercept outgoing molecular reports in the Laboratory Information Management System (LIMS).</li>
          <li><strong>Patient Re-Contact:</strong> Automatically alert genetic counselors when a historical patient's reported variant is downgraded.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 18 of 20</span>
    </div>
  </div>

  <!-- SLIDE 19: Conclusion -->
  <div class="slide-container slide-light" id="slide-19">
    <div class="slide-header">
      <div class="slide-category">CONCLUSION & SUMMARY</div>
      <div class="slide-title">Conclusion & Key Project Contributions</div>
      <div class="slide-subtitle">Recapitulating the four foundational innovations delivered by CuraCascade.</div>
    </div>
    <div class="slide-body" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
      <div class="card">
        <div class="card-title" style="color: var(--blue);">1. FIRST UNIFIED 3NF AUDIT WAREHOUSE</div>
        <ul>
          <li>Created a normalized 3NF schema integrating ClinGen, ClinVar, PanelApp, and gnomAD v4.</li>
          <li>Pioneered a dual-engine architecture combining ACID SQLite with DuckDB in-memory columnar scanning for instant analytics across 50,000+ variants.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--purple);">2. LONGITUDINAL SURVIVAL KINETICS</div>
        <ul>
          <li>First study to mathematically model assertion lifespan with Kaplan-Meier and Cox regression.</li>
          <li>Uncovered the 2.36x Review Star Accelerator and the 0.55x Commercial Laboratory Latency Penalty.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--amber);">3. SUPERVISED ML TRIAGE FORECASTER</div>
        <ul>
          <li>Demonstrated predictive downgrade triage with an AUROC of 0.857 across 3,833 genes.</li>
          <li>Provided rigorous dual-regime reporting, proving the mechanistic shift toward star density (70.2%) and panel discordance (26.0%).</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-title" style="color: var(--emerald);">4. PRODUCTION-READY CLINICAL PLATFORM</div>
        <ul>
          <li>Delivered 96.3% join precision (κ = 0.920) on a 100-gene gold-standard benchmark.</li>
          <li>Engineered headless CLI with CI/CD exit codes, Docker deployment, and live cloud portal at curacascade.streamlit.app.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 19 of 20</span>
    </div>
  </div>

  <!-- SLIDE 20: Q&A -->
  <div class="slide-container slide-dark" id="slide-20">
    <div style="height: 6px; background: var(--blue); width: 100%;"></div>
    <div class="slide-header" style="padding-top: 48px;">
      <div class="slide-category">QUESTIONS & ACADEMIC DISCUSSION • PROJECT DEFENSE</div>
      <div class="slide-title" style="font-size: 38px;">Thank You! Questions & Discussion</div>
      <div class="slide-subtitle" style="font-size: 16px; color: #94a3b8; margin-top: 6px;">
        Open floor for Professor feedback, defense questions, and classmate discussion.
      </div>
    </div>
    <div class="slide-body grid-3" style="margin-top: 20px;">
      <div class="card" style="background: #1e293b; border-color: #334155;">
        <div class="card-title" style="color: var(--blue);">LIVE WEB PORTAL</div>
        <ul>
          <li><strong>URL:</strong> curacascade.streamlit.app</li>
          <li>Interactive multi-gene audit portal</li>
          <li>Real-time gnomAD popmax frequency explorer</li>
          <li>One-click PDF clinical dossier generator</li>
        </ul>
      </div>
      <div class="card" style="background: #1e293b; border-color: #334155;">
        <div class="card-title" style="color: var(--teal);">GITHUB REPOSITORY</div>
        <ul>
          <li><strong>URL:</strong> github.com/uditshokeen14/curacascade</li>
          <li>Full source code under MIT License</li>
          <li>Automated CI/CD regression workflows</li>
          <li>Docker build & reproducible seed scripts</li>
        </ul>
      </div>
      <div class="card" style="background: #1e293b; border-color: #334155;">
        <div class="card-title" style="color: var(--emerald);">PUBLICATION REPORT</div>
        <ul>
          <li><strong>File:</strong> CuraCascade_Publication_Report.pdf</li>
          <li>15-page academic journal format</li>
          <li>Comprehensive methodology, proofs & data dictionary</li>
          <li>High-resolution vector figures & bibliography</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <span>CuraCascade: Academic Defense • Udit Shokeen (VIT CSE)</span>
      <span>Slide 20 of 20</span>
    </div>
  </div>

</div>

<!-- Presenter Notes Drawer -->
<div class="notes-drawer" id="notes-drawer">
  <div class="notes-header">
    <span>🎙️ Presenter Script & Talking Points (Slide <span id="notes-slide-num">1</span>)</span>
    <span style="cursor: pointer; color: #94a3b8;" onclick="toggleNotes()">✕ Close (N)</span>
  </div>
  <div class="notes-content" id="notes-text">
    Loading presenter notes...
  </div>
</div>

<script>
  let currentSlide = 1;
  const totalSlides = 20;

  const notesData = [
    // Slide 1
    `"Good morning, respected Professor and dear classmates. Today, I am proud to present CuraCascade—an open-source clinical genomics data warehouse, automated audit engine, and machine-learned triage framework designed to resolve a critical, silent failure mode in modern clinical medicine: unpropagated gene-disease evidence downgrades. Over the next 15 minutes, I will walk you through the biological problem, our 3NF database architecture, the longitudinal latency kinetics we discovered, our machine learning triage engine, and the empirical validation benchmark. Let's begin with the clinical motivation."`,
    // Slide 2
    `"To appreciate the significance of this project, consider this: when an expert body like ClinGen proves that a gene does not cause a disease, it takes an average of 3.2 years before clinical databases reflect that reality. During those 3.2 years, genetic testing laboratories continue to classify mutations in those invalid genes as 'Pathogenic'. In our genome-wide warehouse, we identified 51,251 unpropagated discrepancies. CuraCascade is an end-to-end bioinformatics engine that achieves 96.3% join precision to catch these errors automatically, and deploys machine learning with an AUROC of 0.857 to forecast which genes will be downgraded next."`,
    // Slide 3
    `"Before diving into software, we must understand the biological context. In the 1990s and early 2000s, hundreds of genes were linked to human disease based on small family studies. Scientists didn't have reference population databases like gnomAD, so naturally benign polymorphisms were mistakenly labeled as disease-causing mutations. To fix this, the NIH-funded Clinical Genome Resource (ClinGen) established Gene Curation Expert Panels. They evaluate gene validity on a standardized point matrix into categories: Definitive, Moderate, Limited, Disputed, and Refuted. Remarkably, systematic reappraisals revealed that up to 40% of genes historically screened on cardiomyopathy and arrhythmia panels should actually be downgraded to Disputed or Refuted!"`,
    // Slide 4
    `"Now, why does this happen? Look at the diagram on the right, which is Figure 1 from our publication. At the top, we have the expert consortium level—ClinGen GCEPs re-appraise a gene and publish a downgrade. But biomedical informatics is decentralized. There are no automated push notifications or webhook architectures connecting ClinGen to NCBI ClinVar or Genomics England PanelApp. As a result, NCBI ClinVar continues to report Pathogenic variants in that gene, and diagnostic exome panels continue to test for it. When an NGS pipeline runs, automated software pulls these assertions and prints out a clinical report diagnosing a healthy individual with a fatal genetic condition. The median duration of this disconnect is 3.2 years."`,
    // Slide 5
    `"Let me ground this in real-world clinical consequences. This is not just a theoretical database discrepancy. Consider MYLK2. In 2018, the ClinGen Cardiovascular GCEP formally refuted MYLK2 as a cause of hypertrophic cardiomyopathy. Yet for years, ClinVar retained Pathogenic assertions. Cardiologists who trusted ClinVar misdiagnosed asymptomatic individuals with HCM, recommending surgical implantation of defibrillators. In SCN1B and Brugada syndrome, false-positive reports triggered cascade screening—subjecting healthy children and relatives to invasive electrophysiology tests and severe psychological anxiety. When we multiply this across all diagnostic gene panels, we calculate hundreds of thousands of 'patient-years at risk'."`,
    // Slide 6
    `"To solve this systemic challenge, we architected CuraCascade around four engineering pillars: Pillar 1 is our 3NF Relational Warehouse. It integrates multi-source genomic repositories and pairs transactional SQLite with high-performance DuckDB columnar scanning. Pillar 2 is our Deterministic Audit Engine. It runs formal heuristic rules that classify discrepancies into Classes A, B, and C, outputting POSIX status codes for automated CI/CD pipeline blocking. Pillar 3 is our Longitudinal Survival Kinetics framework. Using Kaplan-Meier curves and Cox regression, we mathematically quantify how long it takes for discrepancies to resolve. Pillar 4 is our Supervised Machine Learning Forecaster. Rather than just waiting for errors to happen, our Random Forest model flags currently supported genes that are biologically primed for an imminent downgrade."`,
    // Slide 7
    `"Slide 7 showcases our database engineering architecture, illustrated in Figure 2 on the right. We designed a normalized Third Normal Form schema. The central hub is the 'genes' entity, connected via primary-to-foreign keys to 'diseases', 'clingen_curations', 'clinvar_variants', and 'panelapp_entries'. One novel technical feature is our Dual-Engine design: For transactions, updates, and CLI scripts, we use standard SQLite with write-ahead logging and strict foreign keys. But when we need to run analytical cohort queries across 50,000 variants, we dynamically mount an in-memory DuckDB engine. DuckDB executes vectorized columnar aggregations directly on SQLite tables with zero-copy overhead, reducing query times from seconds to single-digit milliseconds."`,
    // Slide 8
    `"In Slide 8, we present our audit classification taxonomy, illustrated in Figure 3. Rather than treating all discrepancies equally, CuraCascade establishes three formal tiers based on clinical actionability: Class A is marked CRITICAL. This occurs when ClinVar asserts a variant is Pathogenic in a gene that ClinGen proved is Disputed or Refuted. This is an acute medical hazard because a patient will receive a definitive genetic diagnosis for a gene that does not cause the disease. Class B is marked HIGH. Here, ClinGen rates the gene as Limited evidence, but ClinVar still reports Pathogenic variants. This violates the ACMG guideline, which explicitly states that in a Limited gene, variants must be capped at Variant of Uncertain Significance (VUS). Class C is also CRITICAL. It flags diagnostic panel registries like Genomics England PanelApp that still maintain 'Green' diagnostic-grade tiering for refuted genes. This causes high-throughput automated exome pipelines to flag discredited genes on routine patient runs."`,
    // Slide 9
    `"Slide 9 demonstrates how CuraCascade incorporates population genetics to validate and refute clinical claims. We implemented the statistical framework of Whiffin et al. (2017) to compute the Maximum Credible Allele Frequency, or MCAF. If a disease has a prevalence of 1 in 500, simple population genetics dictates that no single pathogenic mutation can exceed a specific mathematical frequency ceiling in gnomAD. CuraCascade annotates every ClinVar variant with gnomAD v4 Popmax frequencies. If a supposed 'Pathogenic' mutation exceeds MCAF, CuraCascade triggers ACMG Rule BS1, or Rule BA1 if it exceeds 5%. This provides independent, orthogonal proof that the downstream assertion is invalid, eliminating ancestry-related misclassification."`,
    // Slide 10
    `"Slide 10 presents our survival analysis and Cox Proportional Hazards regression, shown in Figure 4. We treated assertion retraction as a time-to-event survival problem. Panel A shows our Kaplan-Meier curves, and Panel B displays our Cox Hazard Ratios. The concordance index was 0.724. Two critical operational findings emerged: First, the 'Review Star Accelerator': variants with 2 or more ClinVar stars resolve 2.36 times faster. Laboratories actively monitor multi-star submissions, while 0-star submissions are often neglected. Second, what we term the 'Commercial Laboratory Latency Penalty': commercial testing labs exhibit a Hazard Ratio of 0.55. They resolve discrepancies at half the rate of academic medical centers. Why? Because retracting an assertion in a commercial lab carries legal liabilities, requiring them to issue amended reports to ordering physicians."`,
    // Slide 11
    `"In Slide 11, we transition from reactive auditing to predictive forecasting. Can we predict which genes currently rated as Definitive or Moderate will be downgraded in the future? To answer this, we engineered 7 biologically grounded features across ClinGen, ClinVar, PanelApp, and gnomAD. We deployed a Balanced Random Forest with inverse class weighting. Crucially, to prevent temporal data leakage, we enforced a strict temporal validation split: the model was trained only on curations evaluated before January 1, 2021, and tested on curations evaluated on or after that date. The model outputs a calibrated risk score that ranks genes into an actionable clinical triage queue."`,
    // Slide 12
    `"Slide 12 highlights one of the most intellectually honest aspects of our research, shown in Figure 5. In academic machine learning, papers often boast 1.0 AUROC without acknowledging that their benchmark was an artificial toy dataset. In CuraCascade, we explicitly report two distinct regimes: On our positive control benchmark of 34 historical landmark genes, the model achieves a perfect AUROC of 1.000. But we explicitly explain in our manuscript that this is a linearly separable sanity check where Curation Age accounts for 78.4% of the signal. When we scale to the unfiltered genome-wide corpus of 3,833 genes, the model achieves an AUROC of 0.857. Crucially, a dramatic mechanistic feature shift occurs: Curation Age drops, and predictive power is dominated by Low ClinVar Star Density (70.2%) and PanelApp disagreement (26.0%). This reflects the biological reality of how discredited genes behave."`,
    // Slide 13
    `"Slide 13 presents our clinical validation benchmark against blinded expert adjudication, shown in Figure 6. To verify that CuraCascade's automated SQL joins and heuristic logic don't produce false alarms, we compiled a gold-standard cohort of 100 genes—54 published downgrades and 46 definitive controls across heart disease, cancer, and neurology. Against manual clinical adjudication: Automated Join Precision was 96.3%, Sensitivity was 96.3%, Specificity was 95.7%, and Cohen's Kappa coefficient was 0.920, representing near-perfect concordance. This proves that CuraCascade can operate safely as an automated clinical audit firewall in a hospital setting."`,
    // Slide 14
    `"Slide 14 demonstrates our commitment to software engineering best practices. CuraCascade is not just a collection of scripts; it is an enterprise CLI tool with strict POSIX exit code conventions: Exit 0 indicates a clean audit. Exit 1 indicates that unpropagated Class A findings were detected, which immediately halts any automated build or sequencing run. Exit 2 indicates an internal database failure. Our GitHub Actions CI/CD pipeline runs test_cli.py and test_dossier.py on every commit, verifying foreign-key constraints and cryptographic checksums. Finally, the entire application is containerized with Docker, packaging the database, engine, and web interface into an immutable image."`,
    // Slide 15
    `"Slide 15 highlights our clinical decision support portal, deployed live at curacascade.streamlit.app. The dashboard is organized into 8 modular clinical interfaces: Modules 1 and 2 give laboratory directors immediate KPI metrics and allow them to paste arbitrary gene lists for real-time audit. Modules 3 and 4 allow deep exploration of ClinVar variant IDs, ClinGen panel URLs, and gnomAD popmax frequencies. Modules 5 and 6 visualize our machine learning triage rankings and interactive Kaplan-Meier survival curves. Modules 7 and 8 provide one-click exports of formal clinical governance dossiers and live benchmark concordance metrics."`,
    // Slide 16
    `"Slide 16 shows how CuraCascade bridges computation and regulatory compliance. Under ISO 15189:2022 Section 7.3, CLIA, and CAP standards, clinical laboratories are legally required to verify that their diagnostic panels remain scientifically valid. When an audit flags a Class A inconsistency, laboratory directors face an administrative headache: drafting remediation notices. To solve this, CuraCascade automatically compiles a 6-Section Clinical Governance Dossier: It documents the ClinGen consensus, provides orthogonal gnomAD proof, catalogs all affected ClinVar variation IDs, gives a step-by-step ACMG de-escalation checklist invoking Rules BA1 and BS1, and ends with formal signature sign-off blocks for the laboratory medical director."`,
    // Slide 17
    `"In Slide 17, we critically discuss limitations and ethical considerations: First, commercial laboratory inertia: our survival analysis proved commercial labs lag behind academic centers. This is driven by legal and operational friction—issuing amended reports is expensive and legally delicate. Second, ontology harmonization: mapping MONDO to OMIM and MedGen is challenging because phenotypic boundaries in rare disease are complex. Third, our ethical framework: CuraCascade is explicitly built with a human-in-the-loop philosophy. The machine learning model and audit rules serve as an advisory decision support firewall—they never autonomously delete clinical records without the oversight and signature of a board-certified clinical molecular geneticist."`,
    // Slide 18
    `"Looking toward future research horizons in Slide 18: Horizon 1 is real-time webhook streaming: replacing monthly batch flat-file dumps with event-driven webhooks so discrepancies are caught in minutes rather than months. Horizon 2 is LLM-assisted curation: using privacy-preserving local language models to parse PubMed literature and summarize newly discovered contradictory functional assays. Horizon 3 is hospital EHR and HL7 FHIR integration: connecting CuraCascade directly into hospital LIMS systems like Epic and Cerner to halt invalid reports at the diagnostic sign-out stage."`,
    // Slide 19
    `"In conclusion, CuraCascade delivers four major contributions: 1. A 3NF clinical genomics warehouse harmonizing 4 major international databases with dual SQLite/DuckDB engines. 2. The first time-to-event survival model quantifying evidence lag, uncovering a 3.2-year median delay and a commercial lab penalty. 3. A supervised machine learning forecaster achieving an AUROC of 0.857 to triage impending gene downgrades. 4. And a production-grade clinical software suite achieving 96.3% precision, with CI/CD gates, Docker containerization, and a live web dashboard. This framework transforms genomic quality control from sporadic, manual guesswork into an automated, continuous firewall."`,
    // Slide 20
    `"Thank you very much for your time, attention, and interest. The live cloud portal is running at curacascade.streamlit.app, the full open-source codebase is on GitHub, and our complete 15-page publication PDF report is compiled and available for inspection. I would now be delighted to answer any questions from the Professor and my classmates. Thank you!"`
  ];

  function updateSlide(index) {
    if (index < 1 || index > totalSlides) return;
    document.querySelectorAll('.slide-container').forEach(el => el.classList.remove('active'));
    const target = document.getElementById('slide-' + index);
    if (target) {
      target.classList.add('active');
      currentSlide = index;
      document.getElementById('slide-indicator').innerText = 'Slide ' + currentSlide + ' of ' + totalSlides;
      document.getElementById('progress-bar').style.width = ((currentSlide / totalSlides) * 100) + '%';
      document.getElementById('notes-slide-num').innerText = currentSlide;
      document.getElementById('notes-text').innerText = notesData[currentSlide - 1];
    }
  }

  function nextSlide() {
    if (currentSlide < totalSlides) updateSlide(currentSlide + 1);
  }

  function prevSlide() {
    if (currentSlide > 1) updateSlide(currentSlide - 1);
  }

  function toggleNotes() {
    const drawer = document.getElementById('notes-drawer');
    drawer.classList.toggle('open');
    const btn = document.getElementById('notes-btn');
    if (drawer.classList.contains('open')) {
      btn.style.background = '#0d9488';
      btn.style.color = '#ffffff';
    } else {
      btn.style.background = '#1e293b';
      btn.style.color = '#e2e8f0';
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => alert(err.message));
    } else {
      document.exitFullscreen();
    }
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      prevSlide();
    } else if (e.key === 'Home') {
      updateSlide(1);
    } else if (e.key === 'End') {
      updateSlide(totalSlides);
    } else if (e.key === 'n' || e.key === 'N') {
      toggleNotes();
    } else if (e.key === 'f' || e.key === 'F') {
      toggleFullscreen();
    }
  });

  // Init notes text
  updateSlide(1);
</script>
</body>
</html>
"""

    html = template.replace("FIG_LAG_PLACEHOLDER", fig_lag)
    html = html.replace("FIG_SCHEMA_PLACEHOLDER", fig_schema)
    html = html.replace("FIG_TAX_PLACEHOLDER", fig_tax)
    html = html.replace("FIG_SURV_PLACEHOLDER", fig_surv)
    html = html.replace("FIG_ML_PLACEHOLDER", fig_ml)
    html = html.replace("FIG_VAL_PLACEHOLDER", fig_val)

    OUTPUT_HTML.write_text(html, encoding="utf-8")
    ROOT_HTML.write_text(html, encoding="utf-8")
    print(f"HTML Presentation successfully generated at:")
    print(f"  - {OUTPUT_HTML}")
    print(f"  - {ROOT_HTML}")

if __name__ == "__main__":
    build_presentation_html()
