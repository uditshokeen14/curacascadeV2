"""Generate an academic-defense PowerPoint presentation for CuraCascade.

Creates:
- CuraCascade_Presentation.pptx (16:9 Widescreen, publication-grade styling,
  embedded figures, metrics cards, tables, and comprehensive presenter speaker notes).
"""

from pathlib import Path
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
OUTPUT_PPTX = REPO_ROOT / "CuraCascade_Presentation.pptx"
DOCS_PPTX = REPO_ROOT / "docs" / "CuraCascade_Presentation.pptx"

# Colors
COLOR_NAVY_DARK = RGBColor(10, 25, 47)      # #0A192F
COLOR_NAVY_SLATE = RGBColor(15, 23, 42)     # #0F172A
COLOR_SLATE_800 = RGBColor(30, 41, 59)      # #1E293B
COLOR_SLATE_600 = RGBColor(71, 85, 105)     # #475569
COLOR_SLATE_400 = RGBColor(148, 163, 184)   # #94A3B8
COLOR_SLATE_200 = RGBColor(226, 232, 240)   # #E2E8F0
COLOR_SLATE_100 = RGBColor(241, 245, 249)   # #F1F5F9
COLOR_BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF

COLOR_BLUE_PRIMARY = RGBColor(37, 99, 235)  # #2563EB
COLOR_BLUE_LIGHT = RGBColor(239, 246, 255)  # #EFF6FF
COLOR_TEAL = RGBColor(13, 148, 136)         # #0D9488
COLOR_TEAL_LIGHT = RGBColor(240, 253, 250)  # #F0FDFA
COLOR_EMERALD = RGBColor(16, 185, 129)      # #10B981
COLOR_ROSE_CRITICAL = RGBColor(225, 29, 72) # #E11D48
COLOR_ROSE_LIGHT = RGBColor(255, 241, 242)  # #FFF1F2
COLOR_AMBER_HIGH = RGBColor(217, 119, 6)    # #D97706
COLOR_AMBER_LIGHT = RGBColor(254, 243, 199) # #FEF3C7
COLOR_PURPLE = RGBColor(124, 58, 237)       # #7C3AED

TOTAL_SLIDES = 20

def create_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, color: RGBColor):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, category: str, title: str, subtitle: str = "", is_dark: bool = False):
    # Category badge / breadcrumb
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_TEAL if is_dark else COLOR_BLUE_PRIMARY

    # Title & Subtitle box
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.85))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE if is_dark else COLOR_NAVY_SLATE

    if subtitle:
        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = COLOR_SLATE_400 if is_dark else COLOR_SLATE_600
        p_sub.space_before = Pt(3)

def add_footer(slide, current_idx: int, is_dark: bool = False):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_SLATE_800 if is_dark else COLOR_SLATE_200
    line.line.fill.background()

    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.35))
    tf = foot_box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"CuraCascade: Clinical Evidence Downgrade Audit Engine  •  Udit Shokeen (VIT CSE)  •  Academic Defense  •  Slide {current_idx} of {TOTAL_SLIDES}"
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_SLATE_400 if is_dark else COLOR_SLATE_600

def add_card(slide, left: float, top: float, width: float, height: float,
             bg_color: RGBColor = COLOR_WHITE, border_color: RGBColor = COLOR_SLATE_200):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_stat_box(slide, left: float, top: float, width: float, height: float,
                 val: str, label: str, sub: str = "", theme: str = "blue"):
    themes = {
        "blue": (COLOR_BLUE_LIGHT, COLOR_BLUE_PRIMARY, COLOR_NAVY_SLATE),
        "red": (COLOR_ROSE_LIGHT, COLOR_ROSE_CRITICAL, COLOR_ROSE_CRITICAL),
        "teal": (COLOR_TEAL_LIGHT, COLOR_TEAL, COLOR_TEAL),
        "amber": (COLOR_AMBER_LIGHT, COLOR_AMBER_HIGH, COLOR_AMBER_HIGH),
        "emerald": (RGBColor(236, 253, 245), COLOR_EMERALD, COLOR_EMERALD),
    }
    bg_col, accent_col, val_col = themes.get(theme, themes["blue"])
    add_card(slide, left, top, width, height, bg_col, accent_col)

    box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.1), Inches(width - 0.3), Inches(height - 0.2))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.text = val
    p_val.font.size = Pt(22)
    p_val.font.bold = True
    p_val.font.color.rgb = val_col

    p_lbl = tf.add_paragraph()
    p_lbl.text = label
    p_lbl.font.size = Pt(11)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_NAVY_SLATE
    p_lbl.space_before = Pt(2)

    if sub:
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = COLOR_SLATE_600
        p_sub.space_before = Pt(2)

def set_notes(slide, notes: str):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes.strip()

# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1(prs):
    """Slide 1: Title Slide (Dark Theme)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_NAVY_DARK)

    # Accent decorative top bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_BLUE_PRIMARY
    bar.line.fill.background()

    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(0.4))
    tf_c = cat_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "RESEARCH CAPSTONE & ACADEMIC PROJECT DEFENSE • CLINICAL GENOMICS INFORMATICS"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_TEAL

    # Main Project Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.4))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "CuraCascade"
    p_t.font.size = Pt(44)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "An Open-Source Clinical Genomics Audit Engine and Machine-Learned Triage Framework for Unpropagated Gene-Disease Evidence Downgrades"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = COLOR_SLATE_400
    p_sub.space_before = Pt(8)

    # Divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.2), Inches(11.333), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_SLATE_800
    div.line.fill.background()

    # Details Cards
    # Left Card: Author & Affiliation
    add_card(slide, 1.0, 3.5, 5.4, 2.7, COLOR_SLATE_800, COLOR_SLATE_600)
    auth_box = slide.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(5.0), Inches(2.3))
    tf_a = auth_box.text_frame
    tf_a.word_wrap = True
    
    p = tf_a.paragraphs[0]
    p.text = "RESEARCHER & LEAD ARCHITECT"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY

    p2 = tf_a.add_paragraph()
    p2.text = "Udit Shokeen"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(4)

    p3 = tf_a.add_paragraph()
    p3.text = "School of Computer Science and Engineering (SCOPE)\nVellore Institute of Technology, Vellore, Tamil Nadu, India\nContact: uditshokeen14@gmail.com"
    p3.font.size = Pt(11)
    p3.font.color.rgb = COLOR_SLATE_400
    p3.space_before = Pt(6)

    p4 = tf_a.add_paragraph()
    p4.text = "Academic Evaluation • Project Presentation & Defense"
    p4.font.size = Pt(10)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_EMERALD
    p4.space_before = Pt(6)

    # Right Card: Project Technology & Artifacts
    add_card(slide, 6.8, 3.5, 5.5, 2.7, COLOR_SLATE_800, COLOR_SLATE_600)
    tech_box = slide.shapes.add_textbox(Inches(7.0), Inches(3.7), Inches(5.1), Inches(2.3))
    tf_tech = tech_box.text_frame
    tf_tech.word_wrap = True

    pt = tf_tech.paragraphs[0]
    pt.text = "SYSTEM HIGHLIGHTS & DELIVERABLES"
    pt.font.size = Pt(10)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_TEAL

    items = [
        "Core Stack: Python 3.11+ | SQLite 3NF | DuckDB Columnar Engine",
        "Machine Learning: Balanced Random Forest & Cox Proportional Hazards",
        "CI/CD Pipeline: GitHub Actions Automated Audit & Docker Container",
        "Live Deployment: curacascade.streamlit.app (Interactive Portal)",
        "Open-Source Repository: github.com/uditshokeen14/curacascade",
        "Publication Manuscript: 15-Page Academic PDF & Comprehensive Audit Dossier"
    ]
    for it in items:
        p_it = tf_tech.add_paragraph()
        p_it.text = f"•  {it}"
        p_it.font.size = Pt(10.5)
        p_it.font.color.rgb = COLOR_SLATE_200
        p_it.space_before = Pt(3)

    add_footer(slide, 1, is_dark=True)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 1):
"Good morning, respected Professor and dear classmates. Today, I am proud to present CuraCascade—an open-source clinical genomics data warehouse, automated audit engine, and machine-learned triage framework designed to resolve a critical, silent failure mode in modern clinical medicine: unpropagated gene-disease evidence downgrades.

Over the next 15 minutes, I will walk you through the biological problem, our 3NF database architecture, the longitudinal latency kinetics we discovered, our machine learning triage engine, and the empirical validation benchmark. Let's begin with the clinical motivation."
""")

def build_slide_2(prs):
    """Slide 2: Executive Summary & The Problem at a Glance."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "EXECUTIVE SUMMARY", "The Clinical Genomics Dilemma at a Glance",
               "Why upstream evidence updates fail to reach hospital bedsides and how CuraCascade fixes it.")

    # 4 Key Stat Callouts across top
    add_stat_box(slide, 0.8, 1.7, 2.7, 1.35, "3.2 Years", "Median Latency", "Delay before downstream retraction", "red")
    add_stat_box(slide, 3.75, 1.7, 2.7, 1.35, "51,251", "Materialized Lag", "Discrepancies flagged genome-wide", "amber")
    add_stat_box(slide, 6.7, 1.7, 2.7, 1.35, "96.3%", "Join Precision", "PPV vs blinded expert adjudication", "emerald")
    add_stat_box(slide, 9.65, 1.7, 2.85, 1.35, "AUROC 0.857", "ML Prediction", "Genome-wide downgrade vulnerability", "blue")

    # Left Column: The Problem Breakdown
    add_card(slide, 0.8, 3.25, 5.65, 3.45)
    box_l = slide.shapes.add_textbox(Inches(1.0), Inches(3.4), Inches(5.25), Inches(3.1))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE ASYNCHRONOUS KNOWLEDGE DISCONNECT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_CRITICAL

    points_l = [
        ("Evidence Consensus Shift: ", "Consortia like ClinGen systematically re-appraise published disease genes, downgrading up to 40% to Disputed, Refuted, or Limited."),
        ("Decentralized Lag: ", "Downstream clinical registries (NCBI ClinVar, PanelApp) operate in decentralized silos and do NOT automatically retract assertions."),
        ("Direct Clinical Harm: ", "Patients continue to receive false-positive reports, leading to unwarranted implantable cardiac defibrillators, prophylactic surgeries, and familial distress."),
        ("Absence of Tooling: ", "Hospital molecular labs accredited under CAP/CLIA lack automated tools to continuously audit their variant master databases.")
    ]
    for title, desc in points_l:
        p_pt = tf_l.add_paragraph()
        p_pt.text = f"• {title}{desc}"
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = COLOR_NAVY_SLATE
        p_pt.space_before = Pt(6)

    # Right Column: CuraCascade Solution
    add_card(slide, 6.8, 3.25, 5.7, 3.45)
    box_r = slide.shapes.add_textbox(Inches(7.0), Inches(3.4), Inches(5.3), Inches(3.1))
    tf_r = box_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "THE CURACASCADE COMPUTATIONAL SOLUTION"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_TEAL

    points_r = [
        ("3NF Normalized Warehouse: ", "Harmonizes ClinGen, ClinVar, PanelApp, and gnomAD v4 into a dual-engine transactional (SQLite) and analytical (DuckDB) core."),
        ("3-Tier Audit Heuristics: ", "Deterministically categorizes inconsistencies into Classes A, B, and C with automated CI/CD POSIX exit codes."),
        ("Survival Kinetics: ", "Kaplan–Meier and multivariate Cox regression model assertion lifespans, identifying a 0.55x commercial laboratory latency penalty."),
        ("Supervised ML Forecaster: ", "Balanced Random Forest flags currently supported genes at high risk of impending downgrade to prioritize curation queues.")
    ]
    for title, desc in points_r:
        p_pt = tf_r.add_paragraph()
        p_pt.text = f"• {title}{desc}"
        p_pt.font.size = Pt(10.5)
        p_pt.font.color.rgb = COLOR_NAVY_SLATE
        p_pt.space_before = Pt(6)

    add_footer(slide, 2)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 2):
"To appreciate the significance of this project, consider this: when an expert body like ClinGen proves that a gene does not cause a disease, it takes an average of 3.2 years before clinical databases reflect that reality.

During those 3.2 years, genetic testing laboratories continue to classify mutations in those invalid genes as 'Pathogenic'. In our genome-wide warehouse, we identified 51,251 unpropagated discrepancies. 

CuraCascade is an end-to-end bioinformatics engine that achieves 96.3% join precision to catch these errors automatically, and deploys machine learning with an AUROC of 0.857 to forecast which genes will be downgraded next."
""")

def build_slide_3(prs):
    """Slide 3: Clinical Genomics Background & Upstream Curation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "BACKGROUND & CLINICAL RELEVANCE", "Gene Curation & The ClinGen Framework",
               "Understanding how genetic validity is determined and why historical gene associations fail.")

    # 3 Cards Layout
    # Card 1: The Historical Era
    add_card(slide, 0.8, 1.8, 3.65, 4.9)
    b1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.25), Inches(4.5))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "1. THE HISTORICAL ERA"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_SLATE_800

    items1 = [
        "Candidate-Gene Era (1990s–2000s): Many monogenic disease genes were published based on small families (underpowered linkage analysis).",
        "Absent Control Populations: Controls like ExAC and gnomAD did not exist; rare benign variants were mistaken for dominant mutations.",
        "Over-Diagnosis: Hundreds of spurious genes made their way onto commercial diagnostic testing panels."
    ]
    for it in items1:
        p = tf1.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_SLATE_600
        p.space_before = Pt(8)

    # Card 2: The ClinGen Framework
    add_card(slide, 4.8, 1.8, 3.65, 4.9)
    b2 = slide.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.25), Inches(4.5))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "2. CLINGEN VALIDITY TIERS"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_BLUE_PRIMARY

    items2 = [
        "Semi-Quantitative Matrix: Gene Curation Expert Panels (GCEPs) score genetic evidence (max 12 pts) and experimental evidence (max 6 pts).",
        "Clinical Validity Tiers:\n  - Definitive / Strong (12–18 pts)\n  - Moderate (7–11 pts)\n  - Limited (1–6 pts)\n  - Disputed (Convincing counter-evidence)\n  - Refuted (Proven not to cause disease)",
        "Standardized Reappraisals: GCEPs perform systematic consensus reassessments across disease domains."
    ]
    for it in items2:
        p = tf2.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_SLATE_600
        p.space_before = Pt(8)

    # Card 3: Landmark Downgrades
    add_card(slide, 8.8, 1.8, 3.7, 4.9)
    b3 = slide.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.5))
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "3. LANDMARK REAPPRAISALS"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_ROSE_CRITICAL

    items3 = [
        "Cardiovascular Genetics: Landmark GCEP reappraisals (Ingles et al., 2019; Hosseini et al., 2018) revealed up to 40% of cardiomyopathy genes lacked validity.",
        "Discredited Disease Genes: Genes like MYLK2, TCAP, MYOZ2, KCNE2, and SCN1B were downgraded to Disputed or Refuted.",
        "ACMG Clinical Mandate: Guidelines mandate that variants in Disputed/Refuted genes should NEVER be interpreted as Pathogenic."
    ]
    for it in items3:
        p = tf3.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_SLATE_600
        p.space_before = Pt(8)

    add_footer(slide, 3)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 3):
"Before diving into software, we must understand the biological context. In the 1990s and early 2000s, hundreds of genes were linked to human disease based on small family studies. Scientists didn't have reference population databases like gnomAD, so naturally benign polymorphisms were mistakenly labeled as disease-causing mutations.

To fix this, the NIH-funded Clinical Genome Resource (ClinGen) established Gene Curation Expert Panels. They evaluate gene validity on a standardized point matrix into categories: Definitive, Moderate, Limited, Disputed, and Refuted.

Remarkably, systematic reappraisals revealed that up to 40% of genes historically screened on cardiomyopathy and arrhythmia panels should actually be downgraded to Disputed or Refuted!"
""")

def build_slide_4(prs):
    """Slide 4: The Core Problem - Knowledge Cascade Lag."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "PROBLEM FORMULATION", "The 'Knowledge Cascade' Synchronization Lag",
               "Why downstream databases fail to synchronize when upstream evidence is invalidated.")

    # Left: Explanation Card
    add_card(slide, 0.8, 1.8, 5.2, 4.9)
    box_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "DECENTRALIZED ARCHITECTURAL FAILURE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_CRITICAL

    points = [
        ("The Decoupled Ecosystem: ", "ClinGen (curation), NCBI ClinVar (variants), and PanelApp (diagnostic panels) are maintained by different global agencies with no unified event bus."),
        ("No Push Notifications: ", "When ClinGen publishes a downgrade, downstream registries receive no automated webhooks or signals to trigger re-curation."),
        ("The Latency Clock: ", "Downstream clinical databases lag by an empirical median of 3.2 years (and up to 7+ years in commercial laboratories)."),
        ("Bedside Contamination: ", "Pathogenic (P) and Likely Pathogenic (LP) variant assertions persist in ClinVar, while diagnostic panels continue routine screening.")
    ]
    for t_str, d_str in points:
        pt = tf_l.add_paragraph()
        pt.text = f"• {t_str}{d_str}"
        pt.font.size = Pt(10.5)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(7)

    # Right: Embedded Figure (figure_knowledge_lag.png)
    add_card(slide, 6.3, 1.8, 6.2, 4.9)
    fig_path = FIG_DIR / "figure_knowledge_lag.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(6.5), Inches(2.0), Inches(5.8), Inches(4.5))
    else:
        # Fallback text box
        fb = slide.shapes.add_textbox(Inches(6.5), Inches(2.2), Inches(5.8), Inches(4.0))
        fb.text_frame.text = "[Figure 1: Knowledge Cascade Synchronization Lag Diagram]"

    add_footer(slide, 4)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 4):
"Now, why does this happen? Look at the diagram on the right, which is Figure 1 from our publication.

At the top, we have the expert consortium level—ClinGen GCEPs re-appraise a gene and publish a downgrade. But biomedical informatics is decentralized. There are no automated push notifications or webhook architectures connecting ClinGen to NCBI ClinVar or Genomics England PanelApp.

As a result, NCBI ClinVar continues to report Pathogenic variants in that gene, and diagnostic exome panels continue to test for it. When an NGS pipeline runs, automated software pulls these assertions and prints out a clinical report diagnosing a healthy individual with a fatal genetic condition. The median duration of this disconnect is 3.2 years."
""")

def build_slide_5(prs):
    """Slide 5: Clinical Harm & Patient Case Studies."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "CLINICAL IMPACT & BIOETHICS", "Real-World Clinical Harm & Patient Impact",
               "Tangible repercussions of unpropagated evidence downgrades on patients, families, and healthcare systems.")

    # 3 Specific Case Study Cards
    add_card(slide, 0.8, 1.8, 3.65, 3.5)
    b1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.25), Inches(3.1))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "CASE 1: MYLK2 & TCAP"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_ROSE_CRITICAL

    sub1 = tf1.add_paragraph()
    sub1.text = "Hypertrophic Cardiomyopathy (HCM)"
    sub1.font.size = Pt(9.5)
    sub1.font.italic = True
    sub1.font.color.rgb = COLOR_SLATE_600

    items1 = [
        "ClinGen Status: Refuted by Cardiovascular GCEP.",
        "ClinVar Reality: Retained multiple 1-star Pathogenic assertions for years.",
        "Clinical Harm: Healthy patients received false-positive HCM diagnoses, resulting in unjustified sports bans and prophylactic Implantable Cardioverter Defibrillator (ICD) surgery."
    ]
    for it in items1:
        p = tf1.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_NAVY_SLATE
        p.space_before = Pt(5)

    add_card(slide, 4.8, 1.8, 3.65, 3.5)
    b2 = slide.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.25), Inches(3.1))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "CASE 2: SCN1B & KCNE2"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_ROSE_CRITICAL

    sub2 = tf2.add_paragraph()
    sub2.text = "Brugada Syndrome & Long QT"
    sub2.font.size = Pt(9.5)
    sub2.font.italic = True
    sub2.font.color.rgb = COLOR_SLATE_600

    items2 = [
        "ClinGen Status: Disputed as a cause of Brugada Syndrome.",
        "ClinVar Reality: Multiple submitters asserting Pathogenic status.",
        "Clinical Harm: Initiated inappropriate cascade family screening across multiple generations, causing severe psychological distress and unneeded antiarrhythmic medication."
    ]
    for it in items2:
        p = tf2.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_NAVY_SLATE
        p.space_before = Pt(5)

    add_card(slide, 8.8, 1.8, 3.7, 3.5)
    b3 = slide.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(3.1))
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "CASE 3: NBN & RAD50"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_ROSE_CRITICAL

    sub3 = tf3.add_paragraph()
    sub3.text = "Hereditary Breast & Ovarian Cancer"
    sub3.font.size = Pt(9.5)
    sub3.font.italic = True
    sub3.font.color.rgb = COLOR_SLATE_600

    items3 = [
        "ClinGen Status: Downgraded to Limited clinical validity.",
        "ClinVar Reality: Variants classified above VUS ceiling.",
        "Clinical Harm: Premature diagnostic closure. Patients may undergo unnecessary risk-reducing mastectomies while true genetic causes remain uninvestigated."
    ]
    for it in items3:
        p = tf3.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_NAVY_SLATE
        p.space_before = Pt(5)

    # Bottom Full-Width Banner: Patient-Years at Risk
    add_card(slide, 0.8, 5.5, 11.7, 1.25, COLOR_ROSE_LIGHT, COLOR_ROSE_CRITICAL)
    bb = slide.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.0))
    tf_bb = bb.text_frame
    tf_bb.word_wrap = True
    p_bh = tf_bb.paragraphs[0]
    p_bh.text = "THE CONCEPT OF 'PATIENT-YEARS AT RISK'"
    p_bh.font.size = Pt(11)
    p_bh.font.bold = True
    p_bh.font.color.rgb = COLOR_ROSE_CRITICAL

    p_bd = tf_bb.add_paragraph()
    p_bd.text = "The duration between an upstream consortium refutation and downstream retraction represents active clinical exposure. Across thousands of active clinical testing panels globally, unpropagated refutations accumulate hundreds of thousands of patient-years at risk, where misclassified variants continue to be returned to patients."
    p_bd.font.size = Pt(10.5)
    p_bd.font.color.rgb = COLOR_NAVY_SLATE
    p_bd.space_before = Pt(2)

    add_footer(slide, 5)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 5):
"Let me ground this in real-world clinical consequences. This is not just a theoretical database discrepancy.

Consider MYLK2. In 2018, the ClinGen Cardiovascular GCEP formally refuted MYLK2 as a cause of hypertrophic cardiomyopathy. Yet for years, ClinVar retained Pathogenic assertions. Cardiologists who trusted ClinVar misdiagnosed asymptomatic individuals with HCM, recommending surgical implantation of defibrillators.

In SCN1B and Brugada syndrome, false-positive reports triggered cascade screening—subjecting healthy children and relatives to invasive electrophysiology tests and severe psychological anxiety.

When we multiply this across all diagnostic gene panels, we calculate hundreds of thousands of 'patient-years at risk'."
""")

def build_slide_6(prs):
    """Slide 6: CuraCascade Solution Architecture (Four Pillars)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "SYSTEM ARCHITECTURE", "CuraCascade Solution Architecture: Four Core Pillars",
               "A modular, end-to-end framework integrating data warehousing, deterministic auditing, survival kinetics, and machine learning.")

    # 4 Column Cards
    pillars = [
        ("PILLAR 1", "3NF Relational Data Warehouse", COLOR_BLUE_PRIMARY, [
            "Normalizes ClinGen, ClinVar, PanelApp, and gnomAD v4.",
            "Third Normal Form (3NF) relational architecture.",
            "Dual-engine: Transactional SQLite + Columnar DuckDB in-memory scanner.",
            "Composite indexing on (gene_symbol, disease_id)."
        ]),
        ("PILLAR 2", "Deterministic Audit Engine", COLOR_TEAL, [
            "Formal heuristics defining Classes A, B, and C.",
            "Automated join engine materializing unpropagated lag.",
            "Headless CLI (run.py audit) with POSIX exit codes (0/1/2).",
            "CI/CD integration for automated quality gate checks."
        ]),
        ("PILLAR 3", "Longitudinal Survival Kinetics", COLOR_PURPLE, [
            "Time-to-event formulation of assertion lifespan.",
            "Kaplan–Meier non-parametric survival estimators.",
            "Multivariate Cox Proportional Hazards regression.",
            "Quantifies commercial laboratory and star-rating hazard ratios."
        ]),
        ("PILLAR 4", "Supervised ML Triage Forecaster", COLOR_AMBER_HIGH, [
            "Balanced Random Forest predicting impending downgrades.",
            "7 engineered biological & registry features.",
            "Strict temporal train/test validation split (pre/post-2021).",
            "Generates calibrated clinical triage priority queues."
        ])
    ]

    for idx, (p_tag, p_title, p_col, items) in enumerate(pillars):
        left = 0.8 + idx * 2.97
        add_card(slide, left, 1.8, 2.85, 4.9)

        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(2.0), Inches(2.55), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        p_tg = tf.paragraphs[0]
        p_tg.text = p_tag
        p_tg.font.size = Pt(10)
        p_tg.font.bold = True
        p_tg.font.color.rgb = p_col

        p_tt = tf.add_paragraph()
        p_tt.text = p_title
        p_tt.font.size = Pt(12)
        p_tt.font.bold = True
        p_tt.font.color.rgb = COLOR_NAVY_SLATE
        p_tt.space_before = Pt(3)

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"• {it}"
            p_it.font.size = Pt(10)
            p_it.font.color.rgb = COLOR_SLATE_600
            p_it.space_before = Pt(6)

    add_footer(slide, 6)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 6):
"To solve this systemic challenge, we architected CuraCascade around four engineering pillars:

Pillar 1 is our 3NF Relational Warehouse. It integrates multi-source genomic repositories and pairs transactional SQLite with high-performance DuckDB columnar scanning.

Pillar 2 is our Deterministic Audit Engine. It runs formal heuristic rules that classify discrepancies into Classes A, B, and C, outputting POSIX status codes for automated CI/CD pipeline blocking.

Pillar 3 is our Longitudinal Survival Kinetics framework. Using Kaplan-Meier curves and Cox regression, we mathematically quantify how long it takes for discrepancies to resolve.

Pillar 4 is our Supervised Machine Learning Forecaster. Rather than just waiting for errors to happen, our Random Forest model flags currently supported genes that are biologically primed for an imminent downgrade."
""")

def build_slide_7(prs):
    """Slide 7: 3NF Relational Warehouse Architecture & Schema."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "DATABASE ARCHITECTURE & DESIGN", "3NF Relational Warehouse Architecture",
               "Normalized schema design, foreign key integrity, and dual-engine transactional/analytical processing.")

    # Left: Explanation Card
    add_card(slide, 0.8, 1.8, 5.2, 4.9)
    box_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "DATABASE DESIGN PRINCIPLES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY

    points = [
        ("Entity Normalization (3NF): ", "Eliminates biological data duplication across 5 core tables: genes, diseases, clingen_curations, clinvar_variants, and panelapp_entries."),
        ("Strict Integrity Constraints: ", "Foreign keys enforce referential integrity with cascading checks (PRAGMA foreign_keys = ON)."),
        ("Dual-Engine Architecture: ", "Transactional SQLite manages point lookups, CRUD operations, and CLI execution. An in-memory DuckDB columnar scanner attaches directly to SQLite for vectorized cohort aggregation across 50,000+ variants."),
        ("Composite Indexing: ", "Multi-column B-Tree indexes on (gene_symbol, disease_id) enable sub-millisecond multi-table cross-layer joins.")
    ]
    for t_str, d_str in points:
        pt = tf_l.add_paragraph()
        pt.text = f"• {t_str}{d_str}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(7)

    # Right: Embedded Figure (figure_schema_architecture.png)
    add_card(slide, 6.3, 1.8, 6.2, 4.9)
    fig_path = FIG_DIR / "figure_schema_architecture.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(6.5), Inches(2.0), Inches(5.8), Inches(4.5))
    else:
        fb = slide.shapes.add_textbox(Inches(6.5), Inches(2.2), Inches(5.8), Inches(4.0))
        fb.text_frame.text = "[Figure 2: CuraCascade 3NF Schema Architecture Diagram]"

    add_footer(slide, 7)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 7):
"Slide 7 showcases our database engineering architecture, illustrated in Figure 2 on the right.

We designed a normalized Third Normal Form schema. The central hub is the 'genes' entity, connected via primary-to-foreign keys to 'diseases', 'clingen_curations', 'clinvar_variants', and 'panelapp_entries'. 

One novel technical feature is our Dual-Engine design:
For transactions, updates, and CLI scripts, we use standard SQLite with write-ahead logging and strict foreign keys. But when we need to run analytical cohort queries across 50,000 variants, we dynamically mount an in-memory DuckDB engine. DuckDB executes vectorized columnar aggregations directly on SQLite tables with zero-copy overhead, reducing query times from seconds to single-digit milliseconds."
""")

def build_slide_8(prs):
    """Slide 8: Audit Classification Taxonomy & Heuristics."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "AUDIT ENGINE ALGORITHMS", "Audit Classification Taxonomy & Heuristics",
               "Deterministic rule-based stratification of downstream discrepancies into actionable clinical severity tiers.")

    # Left: Explanation & Formulas
    add_card(slide, 0.8, 1.8, 5.5, 4.9)
    box_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.1), Inches(4.5))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE THREE DISCREPANCY CLASSES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    classes = [
        ("CLASS A (CRITICAL SEVERITY)", COLOR_ROSE_CRITICAL,
         "ClinVar asserts Pathogenic (P) or Likely Pathogenic (LP) variants in Disputed or Refuted genes.\n"
         "• Risk: Acute false-positive diagnosis.\n"
         "• Rule: (ClinGen in {Disputed, Refuted}) AND (ClinVar is_plp = 1)"),
        ("CLASS B (HIGH SEVERITY)", COLOR_AMBER_HIGH,
         "ClinVar asserts P/LP variants in Limited-evidence genes.\n"
         "• Risk: Violates ACMG ceiling (variants in Limited genes must not exceed VUS).\n"
         "• Rule: (ClinGen = Limited) AND (ClinVar is_plp = 1)"),
        ("CLASS C (CRITICAL SEVERITY)", COLOR_ROSE_CRITICAL,
         "PanelApp retains Green (diagnostic-grade) status in Disputed or Refuted genes.\n"
         "• Risk: Routine NHS GMS exome panels screen and report invalid genes.\n"
         "• Rule: (ClinGen in {Disputed, Refuted}) AND (PanelApp tier = Green)")
    ]

    for c_title, c_col, c_desc in classes:
        p_c = tf_l.add_paragraph()
        p_c.text = c_title
        p_c.font.size = Pt(10.5)
        p_c.font.bold = True
        p_c.font.color.rgb = c_col
        p_c.space_before = Pt(8)

        p_d = tf_l.add_paragraph()
        p_d.text = c_desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = COLOR_NAVY_SLATE
        p_d.space_before = Pt(2)

    # Right: Embedded Figure (figure_taxonomy_tree.png)
    add_card(slide, 6.6, 1.8, 5.9, 4.9)
    fig_path = FIG_DIR / "figure_taxonomy_tree.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(6.8), Inches(2.0), Inches(5.5), Inches(4.5))
    else:
        fb = slide.shapes.add_textbox(Inches(6.8), Inches(2.2), Inches(5.5), Inches(4.0))
        fb.text_frame.text = "[Figure 3: Audit Classification Taxonomy Tree]"

    add_footer(slide, 8)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 8):
"In Slide 8, we present our audit classification taxonomy, illustrated in Figure 3. Rather than treating all discrepancies equally, CuraCascade establishes three formal tiers based on clinical actionability:

Class A is marked CRITICAL. This occurs when ClinVar asserts a variant is Pathogenic in a gene that ClinGen proved is Disputed or Refuted. This is an acute medical hazard because a patient will receive a definitive genetic diagnosis for a gene that does not cause the disease.

Class B is marked HIGH. Here, ClinGen rates the gene as Limited evidence, but ClinVar still reports Pathogenic variants. This violates the ACMG guideline, which explicitly states that in a Limited gene, variants must be capped at Variant of Uncertain Significance (VUS).

Class C is also CRITICAL. It flags diagnostic panel registries like Genomics England PanelApp that still maintain 'Green' diagnostic-grade tiering for refuted genes. This causes high-throughput automated exome pipelines to flag discredited genes on routine patient runs."
""")

def build_slide_9(prs):
    """Slide 9: Population Genetics & MCAF Ceiling Filter (gnomAD v4)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "POPULATION GENOMICS METHODOLOGY", "Population Genetics & MCAF Ceiling Filter",
               "Using gnomAD v4 and mathematical allele frequency thresholds to refute false-positive assertions.")

    # Left: The Mathematical Framework
    add_card(slide, 0.8, 1.8, 5.65, 4.9)
    b_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.25), Inches(4.5))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "THE WHIFFIN ET AL. MCAF FRAMEWORK"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY

    items_l = [
        ("Maximum Credible Allele Frequency (MCAF): ", "The mathematical ceiling above which an allele is too common in the general population to cause a rare Mendelian disorder."),
        ("Dominant Disorders: ", "MCAF_dom = (I * h) / (2 * P)\nWhere I = Disease prevalence (Orphanet), h = Allelic heterogeneity (default 0.10), P = Penetrance (default 0.50)."),
        ("Recessive Disorders: ", "MCAF_rec = sqrt((I * h) / P)"),
        ("gnomAD v4 Popmax Annotation: ", "CuraCascade cross-references the maximum allele frequency across continental ancestries (African/African American, Latino, East Asian, European, South Asian).")
    ]
    for t_str, d_str in items_l:
        pt = tf_l.add_paragraph()
        pt.text = f"• {t_str}{d_str}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    # Right: Clinical Impact & ACMG Rule Invocation
    add_card(slide, 6.8, 1.8, 5.7, 4.9)
    b_r = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "AUTOMATED ACMG BENIGN RULE INVOCATION"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_EMERALD

    items_r = [
        ("ACMG Rule BA1 (Stand-Alone Benign): ", "If an allele frequency exceeds 5.0% in any continental population in gnomAD, it is stand-alone benign and cannot cause monogenic disease."),
        ("ACMG Rule BS1 (Strong Benign): ", "If allele frequency exceeds the calculated MCAF ceiling for the specific disease indication, BS1 is automatically triggered."),
        ("Resolving Ancestral Disparities: ", "Historically, rare variants in underrepresented minority ancestries were misclassified as pathogenic because control cohorts were predominantly European. Popmax filtering immediately catches these false positives."),
        ("Automated Evidence Dossier: ", "CuraCascade embeds the fold-excess frequency multiplier directly into the clinical retraction memo.")
    ]
    for t_str, d_str in items_r:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_str}{d_str}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    add_footer(slide, 9)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 9):
"Slide 9 demonstrates how CuraCascade incorporates population genetics to validate and refute clinical claims.

We implemented the statistical framework of Whiffin et al. (2017) to compute the Maximum Credible Allele Frequency, or MCAF. If a disease has a prevalence of 1 in 500, simple population genetics dictates that no single pathogenic mutation can exceed a specific mathematical frequency ceiling in gnomAD.

CuraCascade annotates every ClinVar variant with gnomAD v4 Popmax frequencies. If a supposed 'Pathogenic' mutation exceeds MCAF, CuraCascade triggers ACMG Rule BS1, or Rule BA1 if it exceeds 5%. This provides independent, orthogonal proof that the downstream assertion is invalid, eliminating ancestry-related misclassification."
""")

def build_slide_10(prs):
    """Slide 10: Longitudinal Latency & Survival Kinetics."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "EVIDENCE LATENCY & SURVIVAL ANALYSIS", "Longitudinal Latency & Survival Kinetics",
               "Modeling downstream assertion resolution lifespans using Kaplan–Meier and multivariate Cox Proportional Hazards.")

    # Left: Embedded Figure (figure_survival_cox.png)
    add_card(slide, 0.8, 1.8, 6.2, 4.9)
    fig_path = FIG_DIR / "figure_survival_cox.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(1.0), Inches(2.0), Inches(5.8), Inches(4.5))
    else:
        fb = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.8), Inches(4.0))
        fb.text_frame.text = "[Figure 4: Kaplan-Meier Survival Curves & Cox Forest Plot]"

    # Right: Statistical & Operational Findings
    add_card(slide, 7.3, 1.8, 5.2, 4.9)
    b_r = slide.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "COX REGRESSION INSIGHTS (C-index = 0.724)"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_PURPLE

    items = [
        ("The Review Star Accelerator (HR = 2.36, p < 0.001): ", "Assertions with >=2 review stars resolve 2.36 times faster than 0-1 star assertions. High-star records are actively maintained, whereas 0-star submissions are often abandoned legacy files."),
        ("The Commercial Lab Penalty (HR = 0.55, p < 0.001): ", "Commercial testing laboratories resolve assertions at nearly HALF the rate of academic centers. Why? Amending past patient reports incurs legal, operational, and financial friction."),
        ("Severity Sensitivity (HR = 2.31, p < 0.001): ", "Acute Class A refutations resolve 2.3x faster than borderline Class B limited evidence."),
        ("Domain Disparity: ", "Cardiovascular (HR = 2.37) and cancer (HR = 1.71) resolve much faster than neurology (HR = 0.75).")
    ]
    for t_str, d_str in items:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_str}{d_str}"
        pt.font.size = Pt(9.8)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    add_footer(slide, 10)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 10):
"Slide 10 presents our survival analysis and Cox Proportional Hazards regression, shown in Figure 4.

We treated assertion retraction as a time-to-event survival problem. Panel A shows our Kaplan-Meier curves, and Panel B displays our Cox Hazard Ratios. The concordance index was 0.724.

Two critical operational findings emerged:
First, the 'Review Star Accelerator': variants with 2 or more ClinVar stars resolve 2.36 times faster. Laboratories actively monitor multi-star submissions, while 0-star submissions are often neglected.

Second, what we term the 'Commercial Laboratory Latency Penalty': commercial testing labs exhibit a Hazard Ratio of 0.55. They resolve discrepancies at half the rate of academic medical centers. Why? Because retracting an assertion in a commercial lab carries legal liabilities, requiring them to issue amended reports to ordering physicians."
""")

def build_slide_11(prs):
    """Slide 11: Machine-Learned Downgrade Triage Framework."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "MACHINE LEARNING ENGINE", "Machine-Learned Downgrade Triage Framework",
               "Supervised machine learning to forecast impending gene downgrades and prioritize curation queues.")

    # 3 Cards Layout
    # Card 1: The 7 Engineered Features
    add_card(slide, 0.8, 1.8, 3.65, 4.9)
    b1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.25), Inches(4.5))
    tf1 = b1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "7 ENGINEERED FEATURES"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_AMBER_HIGH

    feats = [
        "1. Curation Age (days since last ClinGen formal review)",
        "2. Total Variant Volume (total cataloged variants in ClinVar)",
        "3. Asserted P/LP Count (volume of pathogenic variants)",
        "4. Low ClinVar Star Ratio (fraction with < 2 review stars)",
        "5. gnomAD Popmax AF (maximum continental frequency)",
        "6. MCAF Violation Rate (fraction exceeding disease frequency ceiling)",
        "7. PanelApp Amber/Red Count (non-green panel skepticisms)"
    ]
    for f in feats:
        p = tf1.add_paragraph()
        p.text = f"• {f}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_SLATE_600
        p.space_before = Pt(5)

    # Card 2: Model Architecture
    add_card(slide, 4.8, 1.8, 3.65, 4.9)
    b2 = slide.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.25), Inches(4.5))
    tf2 = b2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "MODEL ARCHITECTURE"
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_BLUE_PRIMARY

    arch = [
        ("Balanced Random Forest: ", "100 estimators, max depth 5, inverse class weighting to handle minority downgrade class."),
        ("Logistic Regression Baseline: ", "L2 regularized balanced logistic regression for linear discrimination baseline."),
        ("Strict Temporal Split: ", "Train on curations before Jan 1, 2021; Test on curations on/after Jan 1, 2021 to strictly avoid data leakage."),
        ("Permutation Importance: ", "10-fold permutation importance evaluates true non-linear feature contribution.")
    ]
    for t_s, d_s in arch:
        p = tf2.add_paragraph()
        p.text = f"• {t_s}{d_s}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_NAVY_SLATE
        p.space_before = Pt(6)

    # Card 3: Actionable Triage Queue
    add_card(slide, 8.8, 1.8, 3.7, 4.9)
    b3 = slide.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.3), Inches(4.5))
    tf3 = b3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = "CLINICAL TRIAGE QUEUE"
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_EMERALD

    triage = [
        ("Calibrated Probability (S in [0, 1]): ", "Converts raw ensemble votes into calibrated risk scores."),
        ("High-Risk Queue (S >= 0.65): ", "Flagged for immediate pre-emptive panel review by molecular geneticists."),
        ("Watch Queue (0.35 <= S < 0.65): ", "Scheduled for targeted re-appraisal during annual overhaul."),
        ("Stable (S < 0.35): ", "High-concordance definitive disease genes.")
    ]
    for t_s, d_s in triage:
        p = tf3.add_paragraph()
        p.text = f"• {t_s}{d_s}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_NAVY_SLATE
        p.space_before = Pt(6)

    add_footer(slide, 11)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 11):
"In Slide 11, we transition from reactive auditing to predictive forecasting. 

Can we predict which genes currently rated as Definitive or Moderate will be downgraded in the future?

To answer this, we engineered 7 biologically grounded features across ClinGen, ClinVar, PanelApp, and gnomAD. We deployed a Balanced Random Forest with inverse class weighting. 

Crucially, to prevent temporal data leakage, we enforced a strict temporal validation split: the model was trained only on curations evaluated before January 1, 2021, and tested on curations evaluated on or after that date. The model outputs a calibrated risk score that ranks genes into an actionable clinical triage queue."
""")

def build_slide_12(prs):
    """Slide 12: Empirical Results - Dual Regime ML Reporting."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "ML EVALUATION & BENCHMARKS", "Empirical Results: Dual-Regime ML Reporting",
               "Transparent comparative evaluation between a curated positive control benchmark and the genome-wide empirical corpus.")

    # Left: Embedded Figure (figure_ml_benchmarks.png)
    add_card(slide, 0.8, 1.8, 6.2, 4.9)
    fig_path = FIG_DIR / "figure_ml_benchmarks.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(1.0), Inches(2.0), Inches(5.8), Inches(4.5))
    else:
        fb = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.8), Inches(4.0))
        fb.text_frame.text = "[Figure 5: ML Benchmarks & Feature Importance Comparison]"

    # Right: Academic Dual Reporting Breakdown
    add_card(slide, 7.3, 1.8, 5.2, 4.9)
    b_r = slide.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "HONEST DUAL-REGIME ANALYSIS"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_BLUE_PRIMARY

    regimes = [
        ("1. Positive Control Benchmark (N = 34): ", "AUROC = 1.000, Precision@Top-20% = 100%. Linearly separable sanity verification where Curation Age dominates at 78.4% importance."),
        ("2. Genome-Wide Corpus (N = 3,833 genes, 51k variants): ", "Random Forest AUROC = 0.857 (vs Logistic Regression 0.827), PR-AUC = 0.814, Precision@Top-20% = 75.8%."),
        ("3. The Mechanistic Feature Shift: ", "In the genome-wide corpus, Curation Age drops to <1%. Instead, Low ClinVar Star Density (70.2%) and PanelApp Discordance (26.0%) become the dominant predictors!"),
        ("4. Scientific Takeaway: ", "In real-world databases, impending downgrades are signaled by conflicting assertions and curator skepticism, not merely passage of time.")
    ]
    for t_s, d_s in regimes:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(9.8)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    add_footer(slide, 12)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 12):
"Slide 12 highlights one of the most intellectually honest aspects of our research, shown in Figure 5.

In academic machine learning, papers often boast 1.0 AUROC without acknowledging that their benchmark was an artificial toy dataset. In CuraCascade, we explicitly report two distinct regimes:

On our positive control benchmark of 34 historical landmark genes, the model achieves a perfect AUROC of 1.000. But we explicitly explain in our manuscript that this is a linearly separable sanity check where Curation Age accounts for 78.4% of the signal.

When we scale to the unfiltered genome-wide corpus of 3,833 genes, the model achieves an AUROC of 0.857. Crucially, a dramatic mechanistic feature shift occurs: Curation Age drops, and predictive power is dominated by Low ClinVar Star Density (70.2%) and PanelApp disagreement (26.0%). This reflects the biological reality of how discredited genes behave."
""")

def build_slide_13(prs):
    """Slide 13: Gold-Standard Validation Benchmark."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "CLINICAL VALIDATION BENCHMARK", "Gold-Standard Validation Benchmark",
               "Evaluating automated join precision against manual blinded adjudication by expert clinical molecular geneticists.")

    # Left: Embedded Figure (figure_validation_matrix.png)
    add_card(slide, 0.8, 1.8, 6.2, 4.9)
    fig_path = FIG_DIR / "figure_validation_matrix.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(1.0), Inches(2.0), Inches(5.8), Inches(4.5))
    else:
        fb = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.8), Inches(4.0))
        fb.text_frame.text = "[Figure 6: Confusion Matrix & Performance Metrics]"

    # Right: Metric Breakdown & Rigor
    add_card(slide, 7.3, 1.8, 5.2, 4.9)
    b_r = slide.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "100-GENE CURATED BENCHMARK"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_EMERALD

    items = [
        ("Benchmark Cohort (N = 100): ", "54 true published downgrades (cardiovascular, hereditary cancer, neurodevelopmental) vs 46 definitive disease controls."),
        ("Precision (PPV) = 96.3%: ", "Only 2 false positives out of 54 flagged genes, caused by historical gene symbol aliases that were resolved via HGNC crosswalk."),
        ("Recall (Sensitivity) = 96.3%: ", "Successfully flagged 52 of 54 verified clinical evidence cascades."),
        ("Specificity = 95.7%: ", "Accurately cleared 44 of 46 definitive control genes with zero inappropriate flags."),
        ("Cohen's Kappa (kappa = 0.920): ", "Demonstrates near-perfect inter-rater agreement with blinded manual adjudication.")
    ]
    for t_s, d_s in items:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    add_footer(slide, 13)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 13):
"Slide 13 presents our clinical validation benchmark against blinded expert adjudication, shown in Figure 6.

To verify that CuraCascade's automated SQL joins and heuristic logic don't produce false alarms, we compiled a gold-standard cohort of 100 genes—54 published downgrades and 46 definitive controls across heart disease, cancer, and neurology.

Against manual clinical adjudication:
- Automated Join Precision was 96.3%
- Sensitivity was 96.3%
- Specificity was 95.7%
- And Cohen's Kappa coefficient was 0.920, representing near-perfect concordance.

This proves that CuraCascade can operate safely as an automated clinical audit firewall in a hospital setting."
""")

def build_slide_14(prs):
    """Slide 14: Software Engineering, Headless CLI & CI/CD."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "SOFTWARE ENGINEERING & PRODUCTION INFRASTRUCTURE", "Headless CLI & Automated CI/CD Gates",
               "Production-grade tooling, POSIX status conventions, Docker containerization, and GitHub Actions workflows.")

    # Left: CLI Architecture
    add_card(slide, 0.8, 1.8, 5.65, 4.9)
    b_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.25), Inches(4.5))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "UNIFIED HEADLESS CLI (run.py)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE_PRIMARY

    cli_items = [
        ("Subcommand 'audit': ", "python run.py audit --genes BARD1,SCN1B --class all --format table\nExports findings to ASCII tables, JSON payloads, or CSV."),
        ("POSIX Status Conventions for CI: ", "• Exit 0: Clean audit / Success\n• Exit 1: Critical Class A findings detected (blocks deployment)\n• Exit 2: Integrity or query failure"),
        ("Subcommand 'verify': ", "python run.py verify\nExecutes automated relational integrity suite (PRAGMA foreign_key_check) and SHA-256 cryptographic provenance checks."),
        ("Subcommand 'serve': ", "python run.py serve\nLaunches Streamlit dashboard locally on port 8501.")
    ]
    for t_s, d_s in cli_items:
        pt = tf_l.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    # Right: Production CI/CD & Docker
    add_card(slide, 6.8, 1.8, 5.7, 4.9)
    b_r = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "ENTERPRISE DEPLOYMENT & CI WORKFLOWS"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_TEAL

    ci_items = [
        ("GitHub Actions Pipeline (.github/workflows/audit_ci.yml): ", "Runs on every push/PR to main branch. Automatically provisions environment, runs integrity verification, and executes test suites."),
        ("Comprehensive Pytest Suite: ", "• test_cli.py: Validates CLI status codes and formatting.\n• test_dossier.py: Validates clinical governance memo structure and mandatory regulatory sections."),
        ("Docker Containerization (Dockerfile): ", "Lightweight, reproducible container image. Zero external database daemon dependencies—runs anywhere with 'docker run -p 8501:8501 curacascade'."),
        ("Automated Build Artifacts: ", "Publishes JSON audit summaries and publication PDF directly to workflow artifacts.")
    ]
    for t_s, d_s in ci_items:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    add_footer(slide, 14)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 14):
"Slide 14 demonstrates our commitment to software engineering best practices. 

CuraCascade is not just a collection of scripts; it is an enterprise CLI tool with strict POSIX exit code conventions:
- Exit 0 indicates a clean audit.
- Exit 1 indicates that unpropagated Class A findings were detected, which immediately halts any automated build or sequencing run.
- Exit 2 indicates an internal database failure.

Our GitHub Actions CI/CD pipeline runs `test_cli.py` and `test_dossier.py` on every commit, verifying foreign-key constraints and cryptographic checksums. Finally, the entire application is containerized with Docker, packaging the database, engine, and web interface into an immutable image."
""")

def build_slide_15(prs):
    """Slide 15: Clinical Decision Support & Interactive Web Portal."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "USER INTERFACE & CLINICAL TOOLS", "Clinical Decision Support & Web Portal",
               "An interactive, executive-grade clinical portal deployed at curacascade.streamlit.app.")

    # 4 Cards Layout (2x2 Grid)
    modules = [
        ("MODULES 1 & 2: EXECUTIVE KPIS & CUSTOM AUDIT", COLOR_BLUE_PRIMARY, [
            "Headline metric banners (3,833 genes, 51,251 findings).",
            "Multi-Gene Custom Audit Portal: laboratory geneticists can paste arbitrary gene lists for instant multi-database cross-referencing.",
            "Instant summary of downstream ClinVar and PanelApp status."
        ]),
        ("MODULES 3 & 4: INCONSISTENCIES & POPULATION GENETICS", COLOR_TEAL, [
            "Interactive discrepancy explorer with sortable variation IDs, ClinGen GCEP links, and elapsed unresolved days.",
            "gnomAD v4 Population Genetics Inspector with continental popmax frequencies and interactive MCAF ceiling sliders."
        ]),
        ("MODULES 5 & 6: ML TRIAGE QUEUE & SURVIVAL ANALYTICS", COLOR_PURPLE, [
            "Downgrade Vulnerability Forecaster: ranks supported genes by calibrated risk score and reveals top feature drivers.",
            "Longitudinal Survival Modeling: interactive Kaplan-Meier curves and multivariate Cox hazard ratio exploration."
        ]),
        ("MODULES 7 & 8: CLINICAL DOSSIERS & VALIDATION BENCHMARK", COLOR_EMERALD, [
            "Clinical Governance Dossier Generator: one-click export of regulatory clinical memos in Markdown and PDF format.",
            "Cross-Layer Validation Benchmark: real-time reporting of PPV (96.3%), Sensitivity, and Cohen's Kappa concordance."
        ])
    ]

    coords = [(0.8, 1.8), (6.8, 1.8), (0.8, 4.3), (6.8, 4.3)]
    for idx, (title, col, items) in enumerate(modules):
        left, top = coords[idx]
        add_card(slide, left, top, 5.7, 2.4)
        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(5.4), Inches(2.1))
        tf = box.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"• {it}"
            p_it.font.size = Pt(9.8)
            p_it.font.color.rgb = COLOR_NAVY_SLATE
            p_it.space_before = Pt(3)

    add_footer(slide, 15)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 15):
"Slide 15 highlights our clinical decision support portal, deployed live at curacascade.streamlit.app.

The dashboard is organized into 8 modular clinical interfaces:
- Modules 1 and 2 give laboratory directors immediate KPI metrics and allow them to paste arbitrary gene lists for real-time audit.
- Modules 3 and 4 allow deep exploration of ClinVar variant IDs, ClinGen panel URLs, and gnomAD popmax frequencies.
- Modules 5 and 6 visualize our machine learning triage rankings and interactive Kaplan-Meier survival curves.
- Modules 7 and 8 provide one-click exports of formal clinical governance dossiers and live benchmark concordance metrics."
""")

def build_slide_16(prs):
    """Slide 16: Clinical Governance & Standardized Dossier."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "REGULATORY COMPLIANCE & ACCREDITATION", "Clinical Governance & Remediation Dossiers",
               "Automating regulatory compliance under CAP, CLIA, and ISO 15189:2022 standards.")

    # Left: ISO 15189 & Regulatory Mandate
    add_card(slide, 0.8, 1.8, 5.2, 4.9)
    b_l = slide.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf_l = b_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "REGULATORY ACCREDITATION MANDATES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE_CRITICAL

    reg_items = [
        ("ISO 15189:2022 Section 7.3: ", "Mandates that medical laboratories continuously review examination procedures and diagnostic panel contents to ensure ongoing validity."),
        ("CLIA / CAP Requirements: ", "Requires clinical laboratories to maintain active quality assurance protocols to identify and remediate diagnostic discrepancies."),
        ("The Retraction Dilemma: ", "When an audit flags a Class A inconsistency, laboratory directors must decide: Which past patient reports require amendment? How should ClinVar submissions be retracted?"),
        ("The CuraCascade Firewall: ", "Acts as an automated pre-report audit firewall in LIMS workflows, halting misclassified variant reports before they reach patients.")
    ]
    for t_s, d_s in reg_items:
        pt = tf_l.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(10)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(6)

    # Right: The 6-Section Dossier Framework
    add_card(slide, 6.3, 1.8, 6.2, 4.9)
    b_r = slide.shapes.add_textbox(Inches(6.5), Inches(2.0), Inches(5.8), Inches(4.5))
    tf_r = b_r.text_frame
    tf_r.word_wrap = True

    pr = tf_r.paragraphs[0]
    pr.text = "THE 6-SECTION CLINICAL DOSSIER (pipeline/remediation.py)"
    pr.font.size = Pt(11)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_BLUE_PRIMARY

    dossier_sections = [
        ("1. Header Directive: ", "Formal regulatory clinical directive with target gene symbol and evaluation timestamp."),
        ("2. Consensus Metadata Table: ", "ClinGen GCEP panel identification, classification date, MONDO ID, and evidence URL."),
        ("3. Orthogonal Population Genetics Summary: ", "gnomAD v4 global & popmax frequency, disease MCAF ceiling, fold-excess multiplier, and ancestry disparity statement."),
        ("4. Downstream Assertions Catalog: ", "Tabular inventory of all active ClinVar variation IDs and PanelApp diagnostic memberships requiring retraction."),
        ("5. Prescriptive ACMG Remediation Checklist: ", "Step-by-step guidance to invoke ACMG Rules BA1/BS1, de-escalate variant to Benign/VUS, and initiate patient re-contact protocols."),
        ("6. Formal Attestation Sign-Off Block: ", "Structured signature blocks for Lead Clinical Molecular Geneticist and Laboratory Medical Director.")
    ]
    for t_s, d_s in dossier_sections:
        pt = tf_r.add_paragraph()
        pt.text = f"• {t_s}{d_s}"
        pt.font.size = Pt(9.5)
        pt.font.color.rgb = COLOR_NAVY_SLATE
        pt.space_before = Pt(4)

    add_footer(slide, 16)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 16):
"Slide 16 shows how CuraCascade bridges computation and regulatory compliance.

Under ISO 15189:2022 Section 7.3, CLIA, and CAP standards, clinical laboratories are legally required to verify that their diagnostic panels remain scientifically valid.

When an audit flags a Class A inconsistency, laboratory directors face an administrative headache: drafting remediation notices. To solve this, CuraCascade automatically compiles a 6-Section Clinical Governance Dossier:
It documents the ClinGen consensus, provides orthogonal gnomAD proof, catalogs all affected ClinVar variation IDs, gives a step-by-step ACMG de-escalation checklist invoking Rules BA1 and BS1, and ends with formal signature sign-off blocks for the laboratory medical director."
""")

def build_slide_17(prs):
    """Slide 17: Critical Discussion, Limitations & Ethics."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "CRITICAL DISCUSSION & LIMITATIONS", "Critical Discussion, Limitations & Ethics",
               "Proactively addressing operational roadblocks, institutional friction, and ethical responsibilities.")

    # 3 Cards Layout
    cards = [
        ("COMMERCIAL LABORATORY INERTIA", COLOR_ROSE_CRITICAL, [
            "Why do commercial laboratories take longer to retract assertions (HR = 0.55)?",
            "Legal & Liability Concerns: Re-contacting ordering physicians and issuing amended diagnostic reports invites legal liability and administrative costs.",
            "Regulatory Disincentive: Laboratories often wait for annual panel overhauls rather than executing real-time retract-and-replace updates."
        ]),
        ("ONTOLOGY & PHENOTYPE HARMONIZATION", COLOR_AMBER_HIGH, [
            "Decentralized Ontology Dialects: ClinGen indexes MONDO concepts, ClinVar indexes MedGen/OMIM, and PanelApp indexes disease names.",
            "Crosswalk Gaps: While CuraCascade implements deterministic ontology crosswalks, rare disease subtypes with overlapping phenotypes require ongoing manual curation.",
            "Variable Penetrance: Certain genes exhibit reduced penetrance, complicating strict Mendelian MCAF filtering."
        ]),
        ("ETHICAL & HUMAN-IN-THE-LOOP TRIAGE", COLOR_BLUE_PRIMARY, [
            "Advisory, Not Autonomous: CuraCascade is designed as a Decision Support Firewall, not an automated report deleter.",
            "Human-in-the-Loop: All flagged Class A findings and ML predictions require review and sign-off by a board-certified clinical geneticist.",
            "Preventing Harm: The ethical priority is protecting patients from unnecessary surgeries while ensuring legitimate disease genes are not prematurely dismissed."
        ])
    ]

    for idx, (title, col, items) in enumerate(cards):
        left = 0.8 + idx * 3.95
        add_card(slide, left, 1.8, 3.8, 4.9)
        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(2.0), Inches(3.5), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = col

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_SLATE_600
            p.space_before = Pt(8)

    add_footer(slide, 17)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 17):
"In Slide 17, we critically discuss limitations and ethical considerations:

First, commercial laboratory inertia: our survival analysis proved commercial labs lag behind academic centers. This is driven by legal and operational friction—issuing amended reports is expensive and legally delicate.

Second, ontology harmonization: mapping MONDO to OMIM and MedGen is challenging because phenotypic boundaries in rare disease are complex.

Third, our ethical framework: CuraCascade is explicitly built with a human-in-the-loop philosophy. The machine learning model and audit rules serve as an advisory decision support firewall—they never autonomously delete clinical records without the oversight and signature of a board-certified clinical molecular geneticist."
""")

def build_slide_18(prs):
    """Slide 18: Future Directions & System Roadmap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "FUTURE WORK & EXTENSIONS", "Future Directions & System Roadmap",
               "Strategic extensions for scaling real-time interoperability, natural language processing, and hospital deployment.")

    # 3 Strategic Horizons
    horizons = [
        ("HORIZON 1: REAL-TIME WEBHOOK ARCHITECTURE", COLOR_BLUE_PRIMARY, [
            "Event-Driven Microservices: Implement Kafka/RabbitMQ message queues listening for real-time ClinGen API webhooks.",
            "Sub-Hour Synchronization: Reduce downstream audit latency from monthly batch dumps to minutes following formal GCEP publishing.",
            "Automated Notification Bus: Push automated Slack, Teams, or email alerts directly to diagnostic laboratory directors."
        ]),
        ("HORIZON 2: LLM-ASSISTED LITERATURE CURATION", COLOR_TEAL, [
            "Literature Parsing: Deploy quantized local Large Language Models (LLMs) to scan newly published PubMed abstracts.",
            "Evidence Extraction: Automatically extract case kindred counts, functional assay metrics, and segregation ratios for candidate genes.",
            "Conflict Summarization: Generate automated synthetic summaries explaining why historical evidence was contradicted."
        ]),
        ("HORIZON 3: EHR & FHIR GENOMICS INTEROPERABILITY", COLOR_PURPLE, [
            "HL7 FHIR Genomics API: Integrate directly into hospital Electronic Health Record (EHR) systems (Epic, Cerner).",
            "Pre-Report Diagnostic Firewall: Intercept outgoing molecular reports in the Laboratory Information Management System (LIMS).",
            "Continuous Patient Re-Contact: Automatically alert genetic counselors when a historical patient's reported variant is downgraded."
        ])
    ]

    for idx, (title, col, items) in enumerate(horizons):
        left = 0.8 + idx * 3.95
        add_card(slide, left, 1.8, 3.8, 4.9)
        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(2.0), Inches(3.5), Inches(4.5))
        tf = box.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = col

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_SLATE_600
            p.space_before = Pt(8)

    add_footer(slide, 18)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 18):
"Looking toward future research horizons in Slide 18:

Horizon 1 is real-time webhook streaming: replacing monthly batch flat-file dumps with event-driven webhooks so discrepancies are caught in minutes rather than months.

Horizon 2 is LLM-assisted curation: using privacy-preserving local language models to parse PubMed literature and summarize newly discovered contradictory functional assays.

Horizon 3 is hospital EHR and HL7 FHIR integration: connecting CuraCascade directly into hospital LIMS systems like Epic and Cerner to halt invalid reports at the diagnostic sign-out stage."
""")

def build_slide_19(prs):
    """Slide 19: Conclusion & Summary of Contributions."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_BG_LIGHT)
    add_header(slide, "CONCLUSION & SUMMARY", "Conclusion & Key Project Contributions",
               "Recapitulating the four foundational innovations delivered by CuraCascade.")

    # 4 Structured Summary Cards (2x2 Grid)
    cards = [
        ("1. FIRST UNIFIED 3NF AUDIT WAREHOUSE", COLOR_BLUE_PRIMARY, [
            "Created a normalized 3NF schema integrating ClinGen, ClinVar, PanelApp, and gnomAD v4.",
            "Pioneered a dual-engine architecture combining ACID SQLite with DuckDB in-memory columnar scanning."
        ]),
        ("2. LONGITUDINAL SURVIVAL KINETICS", COLOR_PURPLE, [
            "First study to mathematically model assertion lifespan with Kaplan-Meier and Cox regression.",
            "Uncovered the 2.36x Review Star Accelerator and the 0.55x Commercial Laboratory Latency Penalty."
        ]),
        ("3. SUPERVISED ML TRIAGE FORECASTER", COLOR_AMBER_HIGH, [
            "Demonstrated predictive downgrade triage with an AUROC of 0.857 across 3,833 genes.",
            "Provided rigorous dual-regime reporting, proving the mechanistic shift toward star density and panel discordance."
        ]),
        ("4. PRODUCTION-READY CLINICAL PLATFORM", COLOR_EMERALD, [
            "Delivered 96.3% join precision (kappa = 0.920) on a 100-gene gold-standard benchmark.",
            "Engineered headless CLI with CI/CD exit codes, Docker deployment, and live cloud portal at curacascade.streamlit.app."
        ])
    ]

    coords = [(0.8, 1.8), (6.8, 1.8), (0.8, 4.3), (6.8, 4.3)]
    for idx, (title, col, items) in enumerate(cards):
        left, top = coords[idx]
        add_card(slide, left, top, 5.7, 2.4)
        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(5.4), Inches(2.1))
        tf = box.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"• {it}"
            p_it.font.size = Pt(10)
            p_it.font.color.rgb = COLOR_NAVY_SLATE
            p_it.space_before = Pt(4)

    add_footer(slide, 19)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 19):
"In conclusion, CuraCascade delivers four major contributions:
1. A 3NF clinical genomics warehouse harmonizing 4 major international databases with dual SQLite/DuckDB engines.
2. The first time-to-event survival model quantifying evidence lag, uncovering a 3.2-year median delay and a commercial lab penalty.
3. A supervised machine learning forecaster achieving an AUROC of 0.857 to triage impending gene downgrades.
4. And a production-grade clinical software suite achieving 96.3% precision, with CI/CD gates, Docker containerization, and a live web dashboard.

This framework transforms genomic quality control from sporadic, manual guesswork into an automated, continuous firewall."
""")

def build_slide_20(prs):
    """Slide 20: Q&A, Links & Acknowledgments (Dark Theme)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, COLOR_NAVY_DARK)

    # Decorative bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_BLUE_PRIMARY
    bar.line.fill.background()

    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(0.4))
    tf_c = cat_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "QUESTIONS & ACADEMIC DISCUSSION • PROJECT DEFENSE"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_TEAL

    # Main Heading
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.2))
    tf_t = title_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "Thank You! Questions & Discussion"
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Open floor for Professor feedback, defense questions, and classmate discussion."
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COLOR_SLATE_400
    p_sub.space_before = Pt(6)

    # 3 Cards for Links & Resources
    resources = [
        ("LIVE WEB PORTAL", COLOR_BLUE_PRIMARY, [
            "URL: curacascade.streamlit.app",
            "Interactive multi-gene audit portal",
            "Real-time gnomAD popmax frequency explorer",
            "One-click PDF clinical dossier generator"
        ]),
        ("GITHUB REPOSITORY", COLOR_TEAL, [
            "URL: github.com/uditshokeen14/curacascade",
            "Full source code under MIT License",
            "Automated CI/CD regression workflows",
            "Docker build & reproducible seed scripts"
        ]),
        ("PUBLICATION REPORT", COLOR_EMERALD, [
            "File: CuraCascade_Publication_Report.pdf",
            "15-page academic journal format",
            "Comprehensive methodology, proofs & data dictionary",
            "High-resolution vector figures & bibliography"
        ])
    ]

    for idx, (r_title, r_col, items) in enumerate(resources):
        left = 1.0 + idx * 3.85
        add_card(slide, left, 3.2, 3.65, 3.2, COLOR_SLATE_800, COLOR_SLATE_600)
        box = slide.shapes.add_textbox(Inches(left + 0.15), Inches(3.4), Inches(3.35), Inches(2.8))
        tf = box.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = r_title
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = r_col

        for it in items:
            p = tf.add_paragraph()
            p.text = f"• {it}"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_SLATE_200
            p.space_before = Pt(6)

    add_footer(slide, 20, is_dark=True)
    set_notes(slide, """
SPEAKER SCRIPT (Slide 20):
"Thank you very much for your time, attention, and interest. 

The live cloud portal is running at curacascade.streamlit.app, the full open-source codebase is on GitHub, and our complete 15-page publication PDF report is compiled and available for inspection.

I would now be delighted to answer any questions from the Professor and my classmates. Thank you!"
""")

# ==============================================================================
# MAIN RUNNER
# ==============================================================================

def main():
    prs = create_deck()

    print("Building slides...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs)
    build_slide_9(prs)
    build_slide_10(prs)
    build_slide_11(prs)
    build_slide_12(prs)
    build_slide_13(prs)
    build_slide_14(prs)
    build_slide_15(prs)
    build_slide_16(prs)
    build_slide_17(prs)
    build_slide_18(prs)
    build_slide_19(prs)
    build_slide_20(prs)

    prs.save(str(OUTPUT_PPTX))
    prs.save(str(DOCS_PPTX))
    print(f"PowerPoint Presentation successfully saved to:")
    print(f"  - {OUTPUT_PPTX}")
    print(f"  - {DOCS_PPTX}")

if __name__ == "__main__":
    main()
