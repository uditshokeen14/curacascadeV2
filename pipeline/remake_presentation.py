"""CuraCascade V2 — Master 25-Slide Academic Defense Presentation Remake.

Completely redesigns the presentation into a world-class, premium keynote deck:
- 16:9 Widescreen layout (13.333" x 7.5").
- Academic Dark Navy aesthetic (#071426) with Teal (#00D4B2), Cyan (#38BDF8), and Emerald (#10B981).
- Native OpenXML slide fade transitions (clean, valid, ZERO repair errors or corrupt timing trees).
- Rich visual diversity: hero slides, split comparison panels, formatted tables, metric callouts,
  horizontal pipeline chevrons, and real embedded screenshots with polished dark borders.
- Complete 1,200+ char structured speaker notes embedded in every slide.
"""

from __future__ import annotations

import datetime
from pathlib import Path
import sys

# Ensure UTF-8 output encoding for console prints on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt

# ==============================================================================
# Color Palette (Dark Space Navy Aesthetic)
# ==============================================================================

BG_DARK = RGBColor(7, 20, 38)           # Deep Space Navy (#071426)
SURFACE_NAVY = RGBColor(15, 36, 58)     # Primary Card Surface (#0F243A)
SURFACE_HIGHLIGHT = RGBColor(22, 55, 90)# Elevated Card Surface (#16375A)
SURFACE_BORDER = RGBColor(30, 64, 104)  # Card Border (#1E4068)
SURFACE_DARK_ALT = RGBColor(11, 27, 46) # Secondary Card Dark (#0B1B2E)

TEXT_WHITE = RGBColor(255, 255, 255)    # Headers & Pure White Text
TEXT_LIGHT = RGBColor(241, 245, 249)    # Primary Light Text (#F1F5F9)
TEXT_MUTED = RGBColor(148, 163, 184)    # Slate Secondary Text (#94A3B8)
TEXT_DIM = RGBColor(100, 116, 139)      # Metadata / Footer Text (#64748B)

TEAL_PRIMARY = RGBColor(0, 212, 178)    # Electric Teal (#00D4B2)
CYAN_ACCENT = RGBColor(56, 189, 248)    # Sky Cyan (#38BDF8)
EMERALD_GREEN = RGBColor(16, 185, 129)  # Success Emerald (#10B981)
AMBER_WARN = RGBColor(245, 158, 11)     # Warning Amber (#F59E0B)
CORAL_ALERT = RGBColor(239, 68, 68)     # Critical Alert Red (#EF4444)
PURPLE_ACCENT = RGBColor(168, 85, 247)  # Royal Purple (#A855F7)

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
SCREENSHOT_DIR = FIG_DIR / "screenshots"


# ==============================================================================
# Helper Functions: Slides, Shapes, Headers, Tables, Notes
# ==============================================================================

def set_slide_background(slide, color: RGBColor = BG_DARK):
    """Set uniform solid background color for slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_slide_fade_transition(slide):
    """Inject native, valid OpenXML fade transition (clean, no repair errors)."""
    fade_xml = parse_xml(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
        '  <p:fade/>'
        '</p:transition>'
    )
    slide._element.append(fade_xml)


def add_header(slide, badge_text: str, title: str, subtitle: str, badge_color: RGBColor = TEAL_PRIMARY):
    """Render a structured, clean modern header banner."""
    # Top accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0), Inches(11.733), Inches(0.04))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = badge_color
    top_line.line.fill.background()

    # Header text box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_badge = tf.paragraphs[0]
    p_badge.text = badge_text.upper()
    p_badge.font.size = Pt(9.5)
    p_badge.font.bold = True
    p_badge.font.color.rgb = badge_color

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(2)


def add_card(slide, left: float, top: float, width: float, height: float,
             bg_color: RGBColor = SURFACE_NAVY, border_color: RGBColor = SURFACE_BORDER,
             radius: bool = True):
    """Add an elevated card container with subtle borders."""
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape


def add_footer(slide, slide_num: int, total_slides: int = 25):
    """Add a professional academic defense footer with pagination."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = f"CuraCascade V2  |  Academic Defense  |  VIT School of Computer Science & Engineering  |  Slide {slide_num:02d} of {total_slides:02d}"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_DIM


def set_speaker_notes(slide, notes_dict: dict):
    """Attach formatted multi-section speaker notes to slide."""
    text = (
        f"🎙️ [SPOKEN DEFENSE SCRIPT]\n{notes_dict.get('script', '')}\n\n"
        f"💡 [PLAIN-ENGLISH CONCEPT EXPLANATION]\n{notes_dict.get('concept', '')}\n\n"
        f"🎯 [KEY DEFENSE TAKEAWAY]\n{notes_dict.get('takeaway', '')}\n\n"
        f"⚠️ [ACADEMIC GUARDRAILS & WHAT NOT TO CLAIM]\n{notes_dict.get('guardrail', '')}\n\n"
        f"❓ [ANTICIPATED VIVA EXAMINER QUESTION & DIRECT ANSWER]\n"
        f"Question: {notes_dict.get('question', '')}\n"
        f"Answer: {notes_dict.get('answer', '')}"
    )
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = text


def add_image_safely(slide, img_name: str, left: float, top: float, width: float, height: float):
    """Safely embed image from screenshots or figures directory with a styled border frame."""
    p_img = SCREENSHOT_DIR / img_name
    if not p_img.exists():
        p_img = FIG_DIR / img_name
    if not p_img.exists():
        return None

    # Outer dark frame
    frame = add_card(slide, left - 0.04, top - 0.04, width + 0.08, height + 0.08,
                     SURFACE_DARK_ALT, SURFACE_BORDER)
    # Picture
    pic = slide.shapes.add_picture(str(p_img), Inches(left), Inches(top), Inches(width), Inches(height))
    return pic


# ==============================================================================
# Slide 1: High-Impact Hero Title Slide
# ==============================================================================

def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    # Hero backdrop card
    add_card(slide, 0.8, 0.7, 11.733, 6.0, SURFACE_NAVY, SURFACE_BORDER)

    # Top gradient highlight bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = TEAL_PRIMARY
    top_bar.line.fill.background()

    # Content Box
    tb = slide.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "ACADEMIC PROJECT DEFENSE  |  COMPREHENSIVE VIVA VOCE"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = TEAL_PRIMARY

    p1 = tf.add_paragraph()
    p1.text = "CuraCascade V2"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_before = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "An Integrated Biomedical Informatics Framework for Automated Gene–Disease Validity Discrepancy Auditing & Longitudinal Latency Analytics"
    p2.font.size = Pt(14)
    p2.font.color.rgb = CYAN_ACCENT
    p2.space_before = Pt(6)

    # Key Badges & Metadata Container
    meta_card = add_card(slide, 1.3, 3.2, 10.7, 1.8, SURFACE_HIGHLIGHT, SURFACE_BORDER)
    tb_meta = slide.shapes.add_textbox(Inches(1.5), Inches(3.3), Inches(10.3), Inches(1.6))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True

    pm0 = tf_m.paragraphs[0]
    pm0.text = "Author: Udit Shokeen  |  Register Number: 23BCB0001"
    pm0.font.size = Pt(13)
    pm0.font.bold = True
    pm0.font.color.rgb = TEXT_WHITE

    pm1 = tf_m.add_paragraph()
    pm1.text = "Institution: School of Computer Science & Engineering (SCOPE), Vellore Institute of Technology (VIT), Vellore"
    pm1.font.size = Pt(11)
    pm1.font.color.rgb = TEXT_MUTED
    pm1.space_before = Pt(4)

    pm2 = tf_m.add_paragraph()
    pm2.text = "Technical Verification: 47 / 47 Automated Pytest Suite Passing (54.12s on Python 3.13)  |  100-Dyad Independent Benchmark"
    pm2.font.size = Pt(11)
    pm2.font.bold = True
    pm2.font.color.rgb = EMERALD_GREEN
    pm2.space_before = Pt(6)

    # Direct URL Cards at bottom
    c_repo = add_card(slide, 1.3, 5.2, 5.2, 1.1, SURFACE_NAVY, TEAL_PRIMARY)
    tb_r = slide.shapes.add_textbox(Inches(1.5), Inches(5.3), Inches(4.8), Inches(0.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    pr0 = tf_r.paragraphs[0]
    pr0.text = "SOURCE REPOSITORY (VERIFIED)"
    pr0.font.size = Pt(9)
    pr0.font.bold = True
    pr0.font.color.rgb = TEAL_PRIMARY
    pr1 = tf_r.add_paragraph()
    pr1.text = "github.com/uditshokeen14/curacascadeV2"
    pr1.font.size = Pt(11)
    pr1.font.color.rgb = TEXT_WHITE

    c_demo = add_card(slide, 6.8, 5.2, 5.2, 1.1, SURFACE_NAVY, CYAN_ACCENT)
    tb_d = slide.shapes.add_textbox(Inches(7.0), Inches(5.3), Inches(4.8), Inches(0.9))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    pd0 = tf_d.paragraphs[0]
    pd0.text = "LIVE DEPLOYMENT (STREAMLIT CLOUD)"
    pd0.font.size = Pt(9)
    pd0.font.bold = True
    pd0.font.color.rgb = CYAN_ACCENT
    pd1 = tf_d.add_paragraph()
    pd1.text = "curacascadev2.streamlit.app"
    pd1.font.size = Pt(11)
    pd1.font.color.rgb = TEXT_WHITE

    add_footer(slide, 1)

    set_speaker_notes(slide, {
        "script": (
            "Respected examiners, faculty members, and colleagues: Good morning. My name is Udit Shokeen, "
            "registration number 23BCB0001 from the School of Computer Science and Engineering at VIT Vellore. "
            "Today, I am defending my project titled CuraCascade V2: An Integrated Biomedical Informatics Framework "
            "for Gene–Disease Evidence Aggregation, Automated Validity Discrepancy Auditing, and Latency Analytics. "
            "Our complete source code, automated test suite, and benchmarks are public on GitHub, and our audit dashboard "
            "is live on Streamlit Cloud. In this defense, I will explain why genomic evidence drifts, how CuraCascade "
            "detects contradictions with zero false-positive alerts, and what our data reveals about evidence latency."
        ),
        "concept": (
            "CuraCascade V2 is an automated audit engine that bridges clinical gene validity curations (ClinGen) "
            "with variant interpretation repositories (ClinVar) and diagnostic panels (PanelApp)."
        ),
        "takeaway": (
            "CuraCascade V2 solves the multi-year evidence propagation lag between gene validity downgrades and "
            "downstream clinical variant databases through disease-aware 3NF relational auditing."
        ),
        "guardrail": (
            "Never claim CuraCascade is an autonomous diagnostic medical device. It is a decision-support "
            "and laboratory governance audit framework."
        ),
        "question": "What is the primary motivation for creating CuraCascade?",
        "answer": (
            "Public genomic databases operate in silos. When ClinGen refutes an unproven gene, variant databases "
            "like ClinVar continue reporting variants as Pathogenic for that refuted disease for years, creating clinical risk."
        )
    })


# ==============================================================================
# Slide 2: Executive Summary (4 Pillars & Metrics Ribbon)
# ==============================================================================

def build_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "Executive Summary", "The Four Pillars of CuraCascade V2",
               "System architecture, empirical benchmark verification, and scientific boundaries at a glance")

    pillars = [
        ("🔴 THE REAL-WORLD PROBLEM",
         "Genomic Evidence Drift",
         "When ClinGen downgrades or refutes unproven gene–disease claims, downstream variant repositories "
         "like ClinVar do not synchronize automatically. Thousands of 'Pathogenic' variant assertions linger "
         "in refuted genes for years, exposing patients to hazardous overdiagnosis.",
         CORAL_ALERT),
        ("🟢 OUR APPLIED SOLUTION",
         "Automated Relational Auditing",
         "Engineered an automated 3NF relational warehouse and deterministic disease-aware rule engine. "
         "Unifies ClinGen, ClinVar, and PanelApp with ontology crosswalks (MONDO, MedGen) to identify "
         "and classify discrepancies into actionable clinical strata.",
         TEAL_PRIMARY),
        ("🔵 STRONGEST VERIFIED RESULT",
         "100.0% Audit Precision",
         "On an independent, firewalled benchmark of 100 gene–disease dyads, CuraCascade achieved 100.0% "
         "precision and 100.0% specificity across 94 evaluable cases (18 TP, 0 FP, 42 TN). Every single "
         "flagged alert is a verified, authentic conflict.",
         CYAN_ACCENT),
        ("🟡 SCIENTIFIC BOUNDARY",
         "Conservative 34.6% Recall",
         "System recall is 34.6% because the engine intentionally refuses to guess when variants are labeled "
         "under broad umbrella terms ('Cardiovascular phenotype'). In clinical informatics, zero false-positive "
         "alerts prevents clinician alert fatigue.",
         AMBER_WARN),
    ]

    card_w = 2.75
    gap = 0.24
    for i, (tag, title, desc, col) in enumerate(pillars):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 3.8, SURFACE_NAVY, col)

        # Inner color tag
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(3.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(8)

    # Bottom Metric Ribbon
    ribbon = add_card(slide, 0.8, 5.7, 11.733, 1.15, SURFACE_HIGHLIGHT, SURFACE_BORDER)
    metrics = [
        ("3,033", "Genes Ingested"),
        ("51,025", "ClinVar Variants"),
        ("51,251", "Audit Findings"),
        ("2.82 Yrs", "Median Lag (1,030d)"),
        ("182,760", "Patient-Years at Risk"),
        ("47 / 47", "Tests Passing (Pytest)")
    ]
    mw = 11.733 / len(metrics)
    for j, (val, lbl) in enumerate(metrics):
        mx = 0.8 + j * mw
        tb_m = slide.shapes.add_textbox(Inches(mx), Inches(5.8), Inches(mw), Inches(0.95))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        pv = tf_m.paragraphs[0]
        pv.alignment = PP_ALIGN.CENTER
        pv.text = val
        pv.font.size = Pt(17)
        pv.font.bold = True
        pv.font.color.rgb = TEAL_PRIMARY if j != 3 else AMBER_WARN

        pl = tf_m.add_paragraph()
        pl.alignment = PP_ALIGN.CENTER
        pl.text = lbl
        pl.font.size = Pt(8.5)
        pl.font.color.rgb = TEXT_MUTED
        pl.space_before = Pt(2)

    add_footer(slide, 2)

    set_speaker_notes(slide, {
        "script": (
            "To understand CuraCascade V2 in four pillars: First, the problem is genomic evidence drift. "
            "When ClinGen downgrades an unproven gene, variant databases don't update synchronously. "
            "Second, our solution: an automated 3NF relational warehouse and disease-aware matching engine. "
            "Third, our strongest verified result: 100.0% precision across 94 evaluable benchmark cases, "
            "meaning zero false alarms. And fourth, our boundary: a conservative 34.6% recall because "
            "our ontology crosswalk refuses to guess on ambiguous clinical terms. "
            "Across our full 51,000-finding corpus, we documented a median propagation lag of 2.82 years."
        ),
        "concept": (
            "The executive summary balances engineering innovation (3NF architecture, automated audits) "
            "with scientific honesty (100% precision vs 34.6% recall trade-off)."
        ),
        "takeaway": (
            "CuraCascade prioritizes zero false positives to maintain clinical trust, accepting lower recall "
            "rather than inundating laboratories with spurious alerts."
        ),
        "guardrail": (
            "Never say 100% accuracy. Accuracy is 63.8%. Precision is 100.0% and specificity is 100.0%."
        ),
        "question": "Why is precision more important than recall in this setting?",
        "answer": (
            "In clinical laboratory bioinformatics, false-positive alerts cause severe alert fatigue. If an audit "
            "tool cries wolf on valid variants, curators turn it off. Achieving 100% precision guarantees that "
            "every alerted finding represents a genuine biological contradiction."
        )
    })


# ==============================================================================
# Slide 3: The Real-World Problem: Genomic Evidence Drift
# ==============================================================================

def build_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "The Real-World Problem", "Genomic Evidence Drift & Downstream Clinical Lag",
               "Why updated gene–disease validity assessments fail to propagate to downstream clinical databases")

    # Left Column: 3-Stage Timeline Cascade (width = 5.6)
    c_time = add_card(slide, 0.8, 1.7, 5.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_t = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    stages = [
        ("STAGE 1: EXPERT CURATION RELEASE (T = 0)",
         "ClinGen expert panels systematically re-evaluate historic gene–disease associations using standardized "
         "monogenic scoring criteria. Genes like MYOZ2 or CACNA2D1 are officially downgraded to 'Refuted' or 'No Evidence'.",
         CYAN_ACCENT),
        ("STAGE 2: ASYNCHRONOUS DOWNSTREAM DELAY (T = +2.82 YRS)",
         "Commercial diagnostic laboratories and public repositories (ClinVar) operate asynchronously. Re-curating "
         "variants requires uncompensated clinical labor. Outdated 'Pathogenic' assertions persist indefinitely.",
         AMBER_WARN),
        ("STAGE 3: CLINICAL MISDIRECTION & PATIENT RISK",
         "Patients undergoing multigene panel testing receive reports declaring variants 'Pathogenic' for diseases "
         "the gene does not cause. This leads to inappropriate surgical interventions, ICD implantations, and family anxiety.",
         CORAL_ALERT)
    ]

    for idx, (stitle, sdesc, scol) in enumerate(stages):
        p0 = tf_t.paragraphs[0] if idx == 0 else tf_t.add_paragraph()
        p0.text = stitle
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = scol
        if idx > 0:
            p0.space_before = Pt(12)

        p1 = tf_t.add_paragraph()
        p1.text = sdesc
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_LIGHT
        p1.space_before = Pt(3)

    # Right Column: Empirical Evidence (Knowledge Lag Graph + Real Case)
    c_right = add_card(slide, 6.7, 1.7, 5.833, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    add_image_safely(slide, "figure_knowledge_lag.png", 6.9, 1.9, 5.433, 2.7)

    # Spotlight case box inside right column
    spot_box = add_card(slide, 6.9, 4.8, 5.433, 1.85, SURFACE_HIGHLIGHT, TEAL_PRIMARY)
    tb_s = slide.shapes.add_textbox(Inches(7.05), Inches(4.9), Inches(5.1), Inches(1.65))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    ps0 = tf_s.paragraphs[0]
    ps0.text = "EMPIRICAL CASE: MYOZ2 IN HYPERTROPHIC CARDIOMYOPATHY"
    ps0.font.size = Pt(9.5)
    ps0.font.bold = True
    ps0.font.color.rgb = TEAL_PRIMARY

    ps1 = tf_s.add_paragraph()
    ps1.text = "• ClinGen Curation: Refuted in 2019 (lack of segregation in broad cohorts)."
    ps1.font.size = Pt(9.5)
    ps1.font.color.rgb = TEXT_WHITE
    ps1.space_before = Pt(3)

    ps2 = tf_s.add_paragraph()
    ps2.text = "• ClinVar Reality: Multiple active 'Pathogenic' variant assertions persisted for >5.9 years."
    ps2.font.size = Pt(9.5)
    ps2.font.color.rgb = TEXT_WHITE
    ps2.space_before = Pt(2)

    ps3 = tf_s.add_paragraph()
    ps3.text = "• Downstream Impact: Diagnostic panels continued testing MYOZ2, risking overtreatment."
    ps3.font.size = Pt(9.5)
    ps3.font.color.rgb = AMBER_WARN
    ps3.space_before = Pt(2)

    add_footer(slide, 3)

    set_speaker_notes(slide, {
        "script": (
            "Why does genomic evidence drift in real-world medicine? Scientific understanding evolves constantly. "
            "In 2018, ClinGen began systematically evaluating historic gene–disease claims. Genes like MYOZ2 or "
            "CACNA2D1, historically linked to cardiomyopathy, were systematically refuted due to lack of statistical linkage. "
            "However, ClinGen curates at the gene level, whereas clinical laboratories report at the variant level. "
            "Because there is no automated synchronization bridge, our audit revealed a median delay of 2.82 years "
            "across 51,000 findings, and up to 6 years in flagship genes. During this window, patients receive molecular reports "
            "asserting pathogenicity for diseases the gene does not cause."
        ),
        "concept": (
            "Genomic evidence drift is the structural lag between gene-validity consensus curation releases and "
            "downstream clinical variant repositories."
        ),
        "takeaway": (
            "Evidence drift is a systemic biomedical infrastructure failure, not individual laboratory malpractice."
        ),
        "guardrail": (
            "Do not state that testing labs act fraudulently. Emphasize that re-curation is time-intensive and "
            "lacks automated software infrastructure."
        ),
        "question": "What is the clinical hazard of an active Pathogenic variant in a refuted gene?",
        "answer": (
            "A patient carrying that variant may receive an affirmative molecular diagnosis for an inherited disease "
            "they do not have, potentially resulting in inappropriate prophylactic surgery, unnecessary ICD placement, "
            "and unneeded cascade testing of family members."
        )
    })


# ==============================================================================
# Slide 4: Biomedical Foundations I (DNA ➔ Protein)
# ==============================================================================

def build_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "Biomedical Foundations I", "The Central Dogma: DNA, Genes, Variants, and Proteins",
               "Establishing genomic first principles for multidisciplinary academic examination")

    # 4 Horizontal Process Cards
    steps = [
        ("01. DNA", "3.1 Billion Base Pairs",
         "Double-helix genetic code composed of Adenine, Thymine, Cytosine, and Guanine across 23 chromosome pairs.",
         CYAN_ACCENT),
        ("02. GENE", "~20,000 Coding Units",
         "Contiguous DNA segments that transcribe into messenger RNA (mRNA) to direct functional cellular machinery.",
         TEAL_PRIMARY),
        ("03. VARIANT", "Permanent Alteration",
         "Nucleotide change (substitution, insertion, deletion) relative to the reference human genome assembly.",
         AMBER_WARN),
        ("04. PROTEIN", "Biological Product",
         "Folded polypeptide chains forming structural elements and enzymes. Missense/nonsense changes alter function.",
         PURPLE_ACCENT)
    ]

    card_w = 2.75
    gap = 0.24
    for i, (num, sub, txt, col) in enumerate(steps):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 2.4, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = num
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = sub
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = txt
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(5)

    # Bottom Comparison Table: Benign Polymorphism vs Pathogenic Mutation
    c_comp = add_card(slide, 0.8, 4.35, 11.733, 2.5, SURFACE_NAVY, SURFACE_BORDER)
    tb_c = slide.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.333), Inches(2.2))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    pc0 = tf_c.paragraphs[0]
    pc0.text = "POPULATION GENOMICS: BENIGN POLYMORPHISMS VS. DAMAGING MONOGENIC MUTATIONS"
    pc0.font.size = Pt(11)
    pc0.font.bold = True
    pc0.font.color.rgb = TEAL_PRIMARY

    pc1 = tf_c.add_paragraph()
    pc1.text = "• Human Genomic Diversity: Every individual carries 4 to 5 million genetic variants across their genome; 99.9% are harmless polymorphisms."
    pc1.font.size = Pt(10)
    pc1.font.color.rgb = TEXT_LIGHT
    pc1.space_before = Pt(4)

    pc2 = tf_c.add_paragraph()
    pc2.text = "• Missense Substitutions: A single nucleotide change replaces an amino acid. May be benign or disrupt active catalytic binding pockets."
    pc2.font.size = Pt(10)
    pc2.font.color.rgb = TEXT_LIGHT
    pc2.space_before = Pt(3)

    pc3 = tf_c.add_paragraph()
    pc3.text = "• Truncating / Nonsense Mutations: Converts an amino acid codon into a premature stop codon, causing haploinsufficiency or nonsense-mediated decay."
    pc3.font.size = Pt(10)
    pc3.font.color.rgb = TEXT_LIGHT
    pc3.space_before = Pt(3)

    pc4 = tf_c.add_paragraph()
    pc4.text = "• The Population Frequency Rule (gnomAD): If an allele is observed at high frequency (>5%) in healthy global populations, it cannot cause a severe rare childhood disease."
    pc4.font.size = Pt(10)
    pc4.font.bold = True
    pc4.font.color.rgb = EMERALD_GREEN
    pc4.space_before = Pt(3)

    add_footer(slide, 4)

    set_speaker_notes(slide, {
        "script": (
            "For non-specialist members of the committee, let us establish the biological foundations from first principles. "
            "Human DNA comprises 3.1 billion base pairs encoding approximately 20,000 protein-coding genes. "
            "During transcription and translation, DNA sequences are transcribed into messenger RNA and translated into folded proteins. "
            "Every human genome contains 4 to 5 million genetic variants. Most are harmless single-nucleotide polymorphisms. "
            "However, damaging variants—such as missense substitutions or nonsense truncations—can disrupt protein structure. "
            "Under population genetics rules, if a variant is common in healthy populations in gnomAD, it cannot cause a rare disease."
        ),
        "concept": (
            "Monogenic disease occurs when a single damaging variant in a clinically causal gene disrupts cellular protein function."
        ),
        "takeaway": (
            "Not all genetic mutations cause disease; understanding protein consequences and population rarity is fundamental."
        ),
        "guardrail": (
            "Do not spend more than 45 seconds here unless asked by faculty."
        ),
        "question": "What is the difference between a missense and nonsense mutation?",
        "answer": (
            "A missense mutation changes a single amino acid in the protein chain, whereas a nonsense mutation introduces "
            "a premature stop codon, truncating the protein or triggering nonsense-mediated mRNA decay."
        )
    })


# ==============================================================================
# Slide 5: Biomedical Foundations II (Gene Validity vs Variant Pathogenicity)
# ==============================================================================

def build_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "Biomedical Foundations II", "Gene Validity vs. Variant Pathogenicity",
               "The fundamental conceptual distinction that underpins the entire CuraCascade audit architecture")

    # Split Two Columns: Left = Gene Validity, Right = Variant Pathogenicity
    # Left Card: ClinGen Gene Validity
    c_left = add_card(slide, 0.8, 1.7, 5.7, 3.7, SURFACE_NAVY, CYAN_ACCENT)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(3.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "GENE-LEVEL CLINICAL VALIDITY (ClinGen)"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = CYAN_ACCENT

    pl1 = tf_l.add_paragraph()
    pl1.text = "Primary Question: 'Does variation in Gene X cause Disease Y?'"
    pl1.font.size = Pt(11)
    pl1.font.bold = True
    pl1.font.color.rgb = TEXT_WHITE
    pl1.space_before = Pt(4)

    bullets_l = [
        "Curated by ClinGen Gene Curation Expert Panels (GCEPs).",
        "Evaluates human genetic evidence: Mendelian segregation LOD scores, case-control odds ratios.",
        "Evaluates experimental evidence: Knock-out animal models, in vitro biochemical rescue.",
        "Standardized Classification Tiers: Definitive, Strong, Moderate, Limited, Disputed, Refuted.",
        "Unit of Analysis: The Gene–Disease Dyad (e.g., MYH7 — Hypertrophic Cardiomyopathy)."
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    # Right Card: ClinVar Variant Pathogenicity
    c_right = add_card(slide, 6.833, 1.7, 5.7, 3.7, SURFACE_NAVY, TEAL_PRIMARY)
    tb_r = slide.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.3), Inches(3.4))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "VARIANT-LEVEL PATHOGENICITY (ClinVar / ACMG)"
    pr0.font.size = Pt(11)
    pr0.font.bold = True
    pr0.font.color.rgb = TEAL_PRIMARY

    pr1 = tf_r.add_paragraph()
    pr1.text = "Primary Question: 'Does Variant Z alter protein function to cause disease?'"
    pr1.font.size = Pt(11)
    pr1.font.bold = True
    pr1.font.color.rgb = TEXT_WHITE
    pr1.space_before = Pt(4)

    bullets_r = [
        "Curated by diagnostic testing laboratories under ACMG/AMP 2015 rules.",
        "Evaluates variant attributes: Population frequency in gnomAD, in silico structural damage.",
        "Evaluates functional assays: Enzyme kinetics, protein stability assays.",
        "5-Tier Classification: Pathogenic (P), Likely Pathogenic (LP), VUS, Likely Benign (LB), Benign (B).",
        "Unit of Analysis: The Specific Allele (e.g., NM_000257.4:c.2119C>T, p.Arg707Ter)."
    ]
    for b in bullets_r:
        p = tf_r.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    # Full-Width Caution Banner: The Fatal Flaw
    banner = add_card(slide, 0.8, 5.55, 11.733, 1.3, SURFACE_HIGHLIGHT, CORAL_ALERT)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(11.333), Inches(1.1))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    pb0 = tf_b.paragraphs[0]
    pb0.text = "⚠️ THE CENTRAL VULNERABILITY: VARIANT PATHOGENICITY IS STRICTLY CONDITIONAL UPON GENE VALIDITY"
    pb0.font.size = Pt(10.5)
    pb0.font.bold = True
    pb0.font.color.rgb = CORAL_ALERT

    pb1 = tf_b.add_paragraph()
    pb1.text = (
        "Even if a variant severely truncates protein synthesis, if the gene itself is REFUTED for that disease, "
        "classifying the variant as 'Pathogenic' for that disease is biologically contradictory. A variant cannot cause "
        "a condition if the gene does not. CuraCascade was engineered to detect this exact contradiction."
    )
    pb1.font.size = Pt(9.5)
    pb1.font.color.rgb = TEXT_WHITE
    pb1.space_before = Pt(3)

    add_footer(slide, 5)

    set_speaker_notes(slide, {
        "script": (
            "Slide 5 represents the central biomedical distinction of this thesis: Gene Validity versus Variant Pathogenicity. "
            "At the gene level, ClinGen answers: 'Does variation in Gene X cause Disease Y?' using segregation LOD scores "
            "and animal knock-outs. At the variant level, ACMG and ClinVar answer: 'Does this specific nucleotide change "
            "alter protein function?' Here is the critical vulnerability: Variant pathogenicity is strictly conditional upon "
            "gene validity. If a gene is refuted for Brugada syndrome, asserting that a variant within it is Pathogenic for "
            "Brugada syndrome is a biomedical contradiction. A variant cannot cause a disease if the gene itself does not."
        ),
        "concept": (
            "Gene validity evaluates causality of the genetic locus; variant pathogenicity evaluates functional impact "
            "of a specific allele assuming the locus is valid."
        ),
        "takeaway": (
            "Pathogenicity is conditional upon validity. Uncoupling these two concepts causes widespread diagnostic errors."
        ),
        "guardrail": (
            "Emphasize this distinction; faculty frequently test candidates on why variant-level classification alone is insufficient."
        ),
        "question": "Can a variant be classified as Pathogenic in a gene with Limited evidence?",
        "answer": (
            "Under ACMG/AMP rules, laboratories historically asserted Pathogenic variants in Limited genes. However, "
            "ClinGen guidelines now recommend that such variants be reported with explicit caveats or downgraded to VUS "
            "until gene-level validity reaches Moderate or Definitive."
        )
    })


# ==============================================================================
# Slide 6: The Clinical Data Ecosystem
# ==============================================================================

def build_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "The Data Ecosystem", "The Public Genomic Intelligence Ecosystem",
               "Mapping the roles, granularities, and governance of primary biomedical data repositories")

    sources = [
        ("ClinGen", "Gene Validity Authority",
         "NIH-funded expert consortium curating gene–disease validity (Definitive to Refuted) and dosage sensitivity.",
         "Weekly curations, MONDO disease ontologies, ~2,000 curated dyads.",
         CYAN_ACCENT),
        ("NCBI ClinVar", "Variant Assertions",
         "Public archive of variant-level clinical interpretations submitted by commercial and academic laboratories.",
         "Daily submissions, MedGen disease IDs, >3.5 million variant assertions.",
         TEAL_PRIMARY),
        ("PanelApp", "Diagnostic Gene Panels",
         "Genomics England platform grading gene inclusions via a traffic-light tier (Green=Diagnostic, Amber, Red).",
         "Crowdsourced expert consensus, 500+ disease-specific panels.",
         EMERALD_GREEN),
        ("gnomAD", "Population Frequencies",
         "Global reference database of allele frequencies across >140,000 exomes/genomes used to establish rarity.",
         "Periodic multi-ancestry releases (v2, v3, v4).",
         PURPLE_ACCENT),
        ("MONDO / HGNC", "Ontology Standards",
         "Monarch Disease Ontology and HUGO Gene Nomenclature Committee providing canonical IDs.",
         "Hierarchical disease classification and approved gene symbols.",
         AMBER_WARN),
    ]

    card_w = 2.15
    gap = 0.24
    for i, (name, role, desc, specs, col) in enumerate(sources):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 5.15, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(1.85), Inches(card_w - 0.24), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = name
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = role
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = "Key Attributes:"
        p3.font.size = Pt(8.5)
        p3.font.bold = True
        p3.font.color.rgb = col
        p3.space_before = Pt(8)

        p4 = tf.add_paragraph()
        p4.text = specs
        p4.font.size = Pt(8)
        p4.font.color.rgb = TEXT_MUTED
        p4.space_before = Pt(2)

    add_footer(slide, 6)

    set_speaker_notes(slide, {
        "script": (
            "To understand our data pipeline, we must map the public genomic data ecosystem. "
            "ClinGen serves as the international authority on gene–disease validity. "
            "NCBI ClinVar is the primary public repository of variant-level clinical interpretations. "
            "Genomics England PanelApp curates virtual gene panels graded by traffic-light confidence: Green, Amber, Red. "
            "gnomAD provides population allele frequencies across 140,000 exomes and genomes. "
            "And HGNC and MONDO provide standardized nomenclature for gene symbols and disease ontologies. "
            "CuraCascade ingests these heterogeneous, asynchronous repositories into a unified analytical schema."
        ),
        "concept": (
            "Each public database captures a different facet of clinical genetics; none independently bridges all tiers."
        ),
        "takeaway": (
            "CuraCascade does not replace these resources; it acts as an automated governance layer aggregating them."
        ),
        "guardrail": (
            "Distinguish authoritative source facts from CuraCascade's analytical interpretations."
        ),
        "question": "What is the difference between MONDO and MedGen?",
        "answer": (
            "MONDO is a hierarchically structured disease ontology developed by the Monarch Initiative that unifies "
            "OMIM, Orphanet, and NCIt terms. MedGen is NCBI's medical genetics portal organized by Concept Unique Identifiers (CUIs)."
        )
    })


# ==============================================================================
# Slide 7: Why Genomic Evidence Disagrees (4 Root Causes)
# ==============================================================================

def build_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "Root Cause Analysis", "Why Genomic Evidence Disagrees in Practice",
               "Systemic structural, temporal, and semantic barriers causing persistent database discordance")

    causes = [
        ("01", "Granularity Disconnect",
         "Gene-Level vs. Variant-Level Silos",
         "ClinGen curates at the gene–disease level, but diagnostic labs submit interpretations at the individual variant level. "
         "Laboratories rarely re-evaluate historic variant assertions when gene-level papers are published.",
         CYAN_ACCENT),
        ("02", "Semantic Heterogeneity",
         "Ontology & Nomenclature Mismatches",
         "ClinVar submissions frequently use broad clinical umbrella terms (e.g., 'Cardiovascular phenotype', MedGen C0007222), "
         "whereas ClinGen curates specific diseases (e.g., 'Brugada syndrome 1', MONDO:0015263). String joins fail completely.",
         TEAL_PRIMARY),
        ("03", "Temporal Asynchrony",
         "Asynchronous Update Cycles",
         "ClinGen expert curations are published periodically as batch releases, while ClinVar receives daily submissions. "
         "Without automated webhooks or cross-database alert triggers, synchronization drifts by years.",
         AMBER_WARN),
        ("04", "Economic Barriers",
         "Uncompensated Re-Curation Burden",
         "Retrospective re-curation of tens of thousands of historical variants is labor-intensive and uncompensated for commercial labs. "
         "Outdated assertions remain active indefinitely unless flagged by automated audit tooling.",
         CORAL_ALERT)
    ]

    card_w = 5.7
    card_h = 2.45
    positions = [(0.8, 1.7), (6.833, 1.7), (0.8, 4.35), (6.833, 4.35)]

    for i, (num, title, sub, desc, col) in enumerate(causes):
        x, y = positions[i]
        c = add_card(slide, x, y, card_w, card_h, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(card_w - 0.4), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = f"{num}. {title.upper()}"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = sub
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(4)

    add_footer(slide, 7)

    set_speaker_notes(slide, {
        "script": (
            "Why do these databases disagree in practice? Our investigation identified four root causes. "
            "First, Granularity Disconnect: ClinGen curates at the dyad level, whereas ClinVar records variant assertions. "
            "Second, Semantic Heterogeneity: A lab may submit a variant under 'Cardiovascular phenotype', while ClinGen "
            "curates against 'Brugada syndrome 1'. Without ontology crosswalks, standard comparisons fail. "
            "Third, Temporal Asynchrony: Consortia publish periodic releases, while variant repos accept daily submissions. "
            "Fourth, Economic Barriers: Retrospective re-curation is time-intensive and uncompensated for commercial labs."
        ),
        "concept": (
            "The discrepancy problem is not malicious fraud; it is an unavoidable consequence of database silos and terminology drift."
        ),
        "takeaway": (
            "Automated informatics infrastructure is the only scalable way to bridge these four systemic barriers."
        ),
        "guardrail": (
            "Avoid framing this as diagnostic malpractice; frame it as an engineering and communication infrastructure challenge."
        ),
        "question": "Which of these four factors is the largest contributor to propagation lag?",
        "answer": (
            "The granularity disconnect combined with economic barriers. Laboratories lack automated alerts notifying "
            "them when a gene's validity has changed, and manual re-curation of thousands of historical variants is cost-prohibitive."
        )
    })


# ==============================================================================
# Slide 8: Existing Tools & The Research Gap (Comparison Table)
# ==============================================================================

def build_slide_8(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(slide, "Research Gap", "Current Landscape & The Research Gap",
               "Evaluating existing commercial and academic tools against CuraCascade V2's automated audit capabilities")

    # Formatted Comparison Table
    rows = 7
    cols = 5
    table_shape = slide.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.733), Inches(4.0))
    table = table_shape.table

    table.columns[0].width = Inches(3.733)
    table.columns[1].width = Inches(1.9)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(1.9)
    table.columns[4].width = Inches(2.2)

    headers = ["Capability / Feature", "Manual Search", "Variant Portals", "ClinGen Website", "CuraCascade V2"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_HIGHLIGHT if j < 4 else TEAL_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE if j < 4 else BG_DARK

    matrix_data = [
        ("Automated Gene-to-Variant Auditing", "❌ Manual Only", "❌ Variant Only", "❌ Gene Only", "✅ Fully Automated"),
        ("Disease-Aware Ontology Crosswalk", "❌ None", "⚠️ Partial Strings", "⚠️ MONDO Only", "✅ 4-Tier Crosswalk"),
        ("Longitudinal Evidence Latency Tracking", "❌ None", "❌ None", "❌ None", "✅ Days & Patient-Yrs"),
        ("Independent 100% Precision Benchmark", "❌ N/A", "❌ Unaudited", "❌ Unaudited", "✅ Verified (0 FP)"),
        ("Open-Source 3NF Relational Store", "❌ Proprietary", "❌ Closed API", "⚠️ CSV Exports", "✅ SQLite + DuckDB"),
        ("Audit Dossier Export (ISO 15189 Aligned)", "❌ Manual Docs", "⚠️ Generic PDF", "❌ None", "✅ HTML/PDF Dossier"),
    ]

    for i, row in enumerate(matrix_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = SURFACE_NAVY if (i % 2 == 0) else SURFACE_DARK_ALT
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT
            p.text = val
            p.font.size = Pt(9.5)
            p.font.bold = (j == 4)
            if j == 4:
                p.font.color.rgb = TEAL_PRIMARY
            elif "✅" in val:
                p.font.color.rgb = EMERALD_GREEN
            elif "⚠️" in val:
                p.font.color.rgb = AMBER_WARN
            elif "❌" in val:
                p.font.color.rgb = CORAL_ALERT
            else:
                p.font.color.rgb = TEXT_LIGHT

    # Bottom Callout Box
    c_gap = add_card(slide, 0.8, 5.85, 11.733, 1.0, SURFACE_HIGHLIGHT, CYAN_ACCENT)
    tb_g = slide.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.8))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True

    pg0 = tf_g.paragraphs[0]
    pg0.text = "THE CORE RESEARCH GAP"
    pg0.font.size = Pt(9.5)
    pg0.font.bold = True
    pg0.font.color.rgb = CYAN_ACCENT

    pg1 = tf_g.add_paragraph()
    pg1.text = (
        "No existing tool performs automated, disease-aware cross-auditing between ClinGen gene curations and ClinVar variant "
        "assertions while quantifying longitudinal latency kinetics in an open-source, reproducible framework."
    )
    pg1.font.size = Pt(9.5)
    pg1.font.color.rgb = TEXT_WHITE
    pg1.space_before = Pt(2)

    add_footer(slide, 8)

    set_speaker_notes(slide, {
        "script": (
            "When examining the current biomedical informatics landscape, a clear research gap emerges. "
            "In clinical practice, curators rely on manual literature searches, which cannot scale across hundreds of thousands of variants. "
            "Variant aggregators like Franklin or Varsome compile allele frequencies, but inherit ClinVar's disease annotations without cross-auditing against ClinGen. "
            "ClinGen's portal provides validity matrices, but does not link downstream to active variant assertions or compute propagation latencies. "
            "CuraCascade V2 closes this gap: the first open-source platform performing bidirectional, disease-aware auditing "
            "with longitudinal latency analytics."
        ),
        "concept": (
            "The research gap lies in the unautomated intersection of gene-level validity, variant pathogenicity, and diagnostic panels."
        ),
        "takeaway": (
            "CuraCascade fills a genuine void in clinical informatics by automating multi-database reconciliation."
        ),
        "guardrail": (
            "Do not claim other tools are incompetent; articulate that they were built for different primary purposes."
        ),
        "question": "Doesn't ClinVar already provide ClinGen links?",
        "answer": (
            "ClinVar displays a link to ClinGen on variant pages if available, but it does NOT audit or alert when an assertion "
            "contradicts ClinGen validity. It displays whatever the submitting lab uploaded, leaving conflicting assertions active."
        )
    })


# ==============================================================================
# Slides 9-25: Continued Master Slide Generation
# ==============================================================================

# For brevity and clean structure in this runner script, let's include all remaining slides (9-25)
# with the exact same high visual standard!

def build_slide_9(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Scope & Boundaries", "Project Objectives & Ethical Scope Boundaries",
               "Clear definition of primary engineering deliverables and explicit clinical non-goals")

    # Left: Objectives
    c_left = add_card(slide, 0.8, 1.7, 5.7, 5.15, SURFACE_NAVY, TEAL_PRIMARY)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    pl0 = tf_l.paragraphs[0]
    pl0.text = "PRIMARY ENGINEERING OBJECTIVES"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    objs = [
        ("Ingest & Normalize Public Repositories", "Build automated ETL scripts for ClinGen, ClinVar, PanelApp with SHA-256 provenance tracking."),
        ("Design a 3NF Relational Warehouse", "Implement a normalized SQLite and DuckDB schema enforcing referential integrity and sub-10ms queries."),
        ("Develop a Disease-Aware Audit Engine", "Build a deterministic 4-tier rule engine using MONDO and MedGen crosswalks to classify conflicts."),
        ("Quantify Latency & Patient Exposure", "Measure cross-sectional elapsed days unresolved and calculate cumulative patient-years at risk."),
        ("Deploy Interactive Decision Support", "Provide an intuitive Streamlit interface with multi-parameter filtering and audit dossier generation.")
    ]
    for title, desc in objs:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {title}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED

    # Right: Non-Goals
    c_right = add_card(slide, 6.833, 1.7, 5.7, 5.15, SURFACE_NAVY, CORAL_ALERT)
    tb_r = slide.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    pr0 = tf_r.paragraphs[0]
    pr0.text = "STRICT NON-GOALS & BOUNDARIES"
    pr0.font.size = Pt(11)
    pr0.font.bold = True
    pr0.font.color.rgb = CORAL_ALERT

    nongoals = [
        ("NO Autonomous Diagnostic Sign-Off", "CuraCascade does not issue clinical diagnoses or alter medical charts without accredited human review."),
        ("NO Live EHR Mutation", "The software operates in read-only analytical mode and does not write directly to hospital electronic health records."),
        ("NO In Silico Variant Pathogenicity Scoring", "The engine audits published consensus assertions; it does not predict molecular folding or replace AlphaFold."),
        ("NO ISO 15189 Accreditation Claims", "Software alone cannot be ISO accredited; it provides compliance-enabling audit infrastructure for accredited labs."),
        ("NO Prospective Clinical Prediction Claims", "Exploratory ML is retrospective triage; it does not prospectively forecast real-world hospital outcomes.")
    ]
    for title, desc in nongoals:
        p1 = tf_r.add_paragraph()
        p1.text = f"❌ {title}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)
        p2 = tf_r.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED

    add_footer(slide, 9)

    set_speaker_notes(slide, {
        "script": (
            "Our project objectives were defined with strict engineering and ethical boundaries. "
            "Our primary deliverables were: normalizing ClinGen, ClinVar, and PanelApp into a 3NF schema, "
            "building a disease-aware audit engine, measuring empirical propagation latency, and deploying an interactive dashboard. "
            "Equally important are our Non-Goals: CuraCascade is NOT an autonomous diagnostic tool, it does not mutate live EHR records, "
            "and we do not claim independent ISO 15189 accreditation without clinical laboratory validation."
        ),
        "concept": "Defining non-goals establishes professional maturity and regulatory awareness.",
        "takeaway": "CuraCascade operates strictly as clinical decision support for human bioinformaticians.",
        "guardrail": "Emphasize non-goals to preempt faculty criticisms regarding clinical deployment.",
        "question": "Why is autonomous reclassification a non-goal?",
        "answer": (
            "Under FDA, EMA, and ISO 15189 guidelines, altering clinical patient interpretations requires board-certified "
            "laboratory geneticist sign-off. Automated modification without human verification poses patient safety risks."
        )
    })


def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Research Questions", "Contributions & Core Research Questions",
               "Three central research questions addressed by empirical implementation and benchmark verification")

    rqs = [
        ("RQ1: AUTOMATED AUDIT FEASIBILITY",
         "Can an automated, disease-aware relational engine detect gene–disease discrepancies with zero false positives?",
         "VERIFIED CONTRIBUTION:",
         "Engineered a 3NF relational schema and ontology crosswalk in pipeline/audit_engine.py. On our independent 94-case "
         "evaluable benchmark, the system achieved 100.0% precision (0 false positives), proving deterministic auditing is feasible.",
         CYAN_ACCENT),
        ("RQ2: LATENCY & EXPOSURE KINETICS",
         "What is the empirical propagation latency between ClinGen gene refutations and downstream ClinVar updates?",
         "VERIFIED CONTRIBUTION:",
         "Across 51,251 findings, we quantified a median propagation latency of 2.82 years (1,030 days) and 182,760 cumulative "
         "patient-years at risk, demonstrating that evidence drift is persistent and multi-year.",
         AMBER_WARN),
        ("RQ3: MACHINE LEARNING RISK TRIAGE",
         "Can machine learning models prioritize high-risk discrepancies based on public metadata features?",
         "VERIFIED CONTRIBUTION:",
         "Trained a Balanced Random Forest achieving an AUROC of 0.857 and Brier score of 0.1508 on 7 features, providing "
         "an exploratory risk-triage framework while disclosing retrospective snapshot temporal leakage.",
         PURPLE_ACCENT)
    ]

    card_w = 3.75
    gap = 0.24
    for i, (qtitle, qtext, atitle, atext, col) in enumerate(rqs):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 5.15, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = qtitle
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = qtext
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_LIGHT
        p1.space_before = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = atitle
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_before = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = atext
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(4)

    add_footer(slide, 10)

    set_speaker_notes(slide, {
        "script": (
            "We formulated three core research questions. "
            "RQ1: Can an automated engine detect discrepancies with zero false positives? Yes, verified by our 100% precision benchmark. "
            "RQ2: What is the empirical propagation latency? Across 51,000 findings, the median lag is 2.82 years, accumulating 182,000 patient-years. "
            "RQ3: Can ML prioritize high-risk assertions? Yes, an AUROC of 0.857 on 7 metadata features, though evaluated retrospectively."
        ),
        "concept": "Aligning the thesis around specific research questions provides clear academic structure.",
        "takeaway": "Each research question is answered with empirical, verifiable data from the codebase.",
        "guardrail": "Acknowledge the retrospective nature of RQ3.",
        "question": "What is the single most important empirical finding of your research?",
        "answer": (
            "The quantification of a 2.82-year median propagation latency across 51,251 findings, proving that evidence drift "
            "is not an occasional outlier but a persistent, systemic phenomenon."
        )
    })


def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Workflow Architecture", "End-to-End Processing Workflow",
               "The complete data lifecycle from raw public data streams to regulatory clinical audit dossiers")

    # 5 Horizontal Process Steps connected by chevrons
    steps = [
        ("1. INGESTION", "Public Streams",
         "Pull raw dumps from ClinGen (JSON/TSV), ClinVar (GZ TSV 4.5GB), and PanelApp (REST API).",
         CYAN_ACCENT),
        ("2. VALIDATION", "Integrity & Schema",
         "Verify SHA-256 checksums, resolve HGNC gene aliases, normalize MedGen/MONDO disease terms.",
         TEAL_PRIMARY),
        ("3. STORAGE", "Normalized Warehouses",
         "Load into 3NF SQLite database (transactional lookups) and DuckDB (vectorized analytics).",
         EMERALD_GREEN),
        ("4. AUDIT ENGINE", "Discrepancy Matching",
         "Execute 4-tier disease-aware matching, classify Class A/B/C findings, compute latency days.",
         AMBER_WARN),
        ("5. DELIVERY", "UI & Report Export",
         "Streamlit interactive dashboard, multi-parameter filtering, ISO 15189 HTML audit dossiers.",
         PURPLE_ACCENT),
    ]

    card_w = 2.15
    gap = 0.24
    for i, (stitle, ssub, sdesc, col) in enumerate(steps):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 3.4, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(1.85), Inches(card_w - 0.24), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = stitle
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = ssub
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(6)

    # Bottom Pipeline Guarantees Card
    c_bot = add_card(slide, 0.8, 5.3, 11.733, 1.55, SURFACE_HIGHLIGHT, SURFACE_BORDER)
    tb_b = slide.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.333), Inches(1.35))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    pb0 = tf_b.paragraphs[0]
    pb0.text = "PIPELINE REPRODUCIBILITY & OPERATIONAL GUARANTEES"
    pb0.font.size = Pt(10)
    pb0.font.bold = True
    pb0.font.color.rgb = TEAL_PRIMARY

    pb1 = tf_b.add_paragraph()
    pb1.text = "• Cryptographic Provenance: Every downloaded snapshot is logged with SHA-256 hash, URL, and timestamp in data_provenance table."
    pb1.font.size = Pt(9)
    pb1.font.color.rgb = TEXT_LIGHT
    pb1.space_before = Pt(2)

    pb2 = tf_b.add_paragraph()
    pb2.text = "• Streaming Parsing: ClinVar ingestion uses Python line generators to stream 4.5 GB files in under 100 MB RAM."
    pb2.font.size = Pt(9)
    pb2.font.color.rgb = TEXT_LIGHT
    pb2.space_before = Pt(2)

    pb3 = tf_b.add_paragraph()
    pb3.text = "• Transactional Rollbacks: Database inserts occur in 5,000-row chunks; unrecoverable parser errors trigger rollback to prevent partial corruption."
    pb3.font.size = Pt(9)
    pb3.font.color.rgb = TEXT_LIGHT
    pb3.space_before = Pt(2)

    add_footer(slide, 11)

    set_speaker_notes(slide, {
        "script": (
            "Slide 11 illustrates the end-to-end processing pipeline implemented in CuraCascade V2. "
            "Data flows through five discrete stages: Ingestion from public streams, validation and normalization, "
            "storage in our dual SQLite/DuckDB warehouse, deterministic discrepancy auditing, and presentation via Streamlit. "
            "The pipeline guarantees cryptographic SHA-256 provenance, streaming memory efficiency under 100 MB, and ACID transactions."
        ),
        "concept": "A modular ETL pipeline separates raw ingestion from analytical auditing.",
        "takeaway": "The architecture is fully reproducible and can be executed headlessly via CLI or Docker.",
        "guardrail": "Do not imply real-time streaming if batch ingestion was used.",
        "question": "How long does full data ingestion take?",
        "answer": (
            "Ingestion of ClinGen and PanelApp takes under 3 minutes; parsing the full 4.5 GB ClinVar gzip file takes approximately "
            "18 minutes on standard workstation NVMe storage."
        )
    })


def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "System Architecture", "Decoupled Multi-Tier System Architecture",
               "Clean separation of ingestion pipelines, dual analytical warehouses, and presentation interfaces")

    # Left Column: Modular Breakdown (width = 5.6)
    c_left = add_card(slide, 0.8, 1.7, 5.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "ARCHITECTURAL TIERS & SEPARATION OF CONCERNS"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    tiers = [
        ("Pipeline Tier (Headless ETL)", "Dedicated scripts in pipeline/ (ingest_clingen.py, ingest_clinvar.py, build_db.py). Operates headlessly via CLI."),
        ("Storage Tier (Dual Engines)", "SQLite for relational constraints, foreign keys, and UI point-lookups. DuckDB for vectorized columnar analytics."),
        ("Audit & Benchmark Tier", "audit_engine.py evaluates ontology crosswalks. validation_benchmark.py runs firewalled evaluation."),
        ("Presentation Tier (Streamlit UI)", "app.py provides responsive UI with custom CSS design tokens, cached DB connections, and zero ETL logic.")
    ]
    for tname, tdesc in tiers:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {tname}"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(8)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {tdesc}"
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: High-Res Architecture Diagram
    add_image_safely(slide, "figure_schema_architecture.png", 6.8, 1.7, 5.733, 5.15)

    add_footer(slide, 12)

    set_speaker_notes(slide, {
        "script": (
            "Looking at the system architecture, CuraCascade V2 is organized into strictly decoupled modules. "
            "The pipeline tier contains standalone batch ingestion scripts. "
            "The storage tier pairs normalized SQLite for transactional integrity with DuckDB for vectorized aggregation. "
            "The presentation tier, contained in app.py, provides an intuitive interface with custom CSS design tokens. "
            "This decoupling ensures that UI crashes cannot corrupt backend data."
        ),
        "concept": "Decoupled architecture ensures modularity, testability, and portability.",
        "takeaway": "The system can be deployed as a local workstation app, Docker container, or cloud service.",
        "guardrail": "Avoid claiming a microservices architecture; it is a clean modular monolith.",
        "question": "Why not use a microservices architecture?",
        "answer": (
            "In clinical laboratory environments, single-container or self-contained deployments are preferred for security, "
            "simplicity of deployment, and ease of validation under clinical quality standards."
        )
    })


def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Database Design", "Normalized 3NF Relational Schema & Indexing",
               "Relational decomposition, foreign-key cascades, and compound B-tree index optimization")

    # Left Column: Relational Design Principles (width = 5.6)
    c_left = add_card(slide, 0.8, 1.7, 5.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "THIRD NORMAL FORM (3NF) DECOMPOSITION"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    schema_points = [
        ("Parent Table: genes", "Keyed by immutable hgnc_id (PK) with UNIQUE constraint on symbol. Stores locus, chromosome."),
        ("Child: gene_validity", "Stores ClinGen curations. FK (gene_symbol) REFERENCES genes(symbol) ON DELETE CASCADE."),
        ("Child: clinvar_variants", "Stores variant assertions (PK variation_id). FK (gene_symbol) REFERENCES genes(symbol)."),
        ("Child: audit_findings", "Stores computed discrepancies. Captures finding_hash, risk_severity, days_unresolved."),
        ("Compound B-Tree Indexes", "idx_cv_gene_sig on (gene_symbol, clinical_significance) accelerates joins from 280ms to 8.4ms.")
    ]
    for stitle, sdesc in schema_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {stitle}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {sdesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: High-Res ER Diagram Screenshot
    add_image_safely(slide, "cropped_s15_schema_relational_3nf.png", 6.8, 1.7, 5.733, 5.15)

    add_footer(slide, 13)

    set_speaker_notes(slide, {
        "script": (
            "The database design in curacascade.db adheres strictly to Third Normal Form (3NF). "
            "The central entity is the genes table, keyed by immutable hgnc_id with a unique constraint on symbol. "
            "Child tables reference genes.symbol with ON DELETE CASCADE foreign keys. "
            "To guarantee sub-10-millisecond queries on multi-way joins, we created targeted compound B-tree indexes, "
            "reducing join times across 51,000 rows from 280ms to 8.4ms."
        ),
        "concept": "3NF decomposition eliminates data redundancy and update anomalies.",
        "takeaway": "Compound indexes provide 33-fold query acceleration for seamless UI interactivity.",
        "guardrail": "Be ready to explain how foreign keys work in SQLite (PRAGMA foreign_keys = ON).",
        "question": "Why use SQLite foreign keys if some databases don't enforce them by default?",
        "answer": (
            "We explicitly execute PRAGMA foreign_keys = ON upon every connection to ensure strict referential integrity, "
            "verified in our test suite in tests/test_database.py."
        )
    })


def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Ingestion & Provenance", "Data Ingestion, Cryptographic Provenance & Normalization",
               "Defensive parsing, SHA-256 snapshot verification, and HGNC nomenclature reconciliation")

    # Left Column: Ingestion Specs Table (width = 5.8)
    c_left = add_card(slide, 0.8, 1.7, 5.8, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "DATA INGESTION SPECIFICATIONS"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    sources_spec = [
        ("ClinGen Gene Validity", "Nested JSON & TSV", "Weekly", "Mapped to MONDO IDs, validity score extracted"),
        ("NCBI ClinVar", "4.5 GB Gzip TSV", "Monthly", "Streamed line-by-line, filtered for P/LP & VUS"),
        ("Genomics England PanelApp", "REST API (JSON)", "On-demand", "Parsed green/amber/red tiers, 500+ panels"),
        ("HGNC Master Registry", "Tab-Delimited", "Quarterly", "Resolved 100% of historical gene aliases")
    ]
    for sname, sfmt, scad, sproc in sources_spec:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {sname} ({sfmt})"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  Cadence: {scad}  |  Processing: {sproc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: Provenance & Defensive Engineering Cards
    c_prov = add_card(slide, 6.9, 1.7, 5.633, 2.45, SURFACE_NAVY, CYAN_ACCENT)
    tb_p = slide.shapes.add_textbox(Inches(7.1), Inches(1.85), Inches(5.2), Inches(2.1))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    pp0 = tf_p.paragraphs[0]
    pp0.text = "CRYPTOGRAPHIC PROVENANCE (SHA-256)"
    pp0.font.size = Pt(10.5)
    pp0.font.bold = True
    pp0.font.color.rgb = CYAN_ACCENT
    bullets_p = [
        "Every downloaded raw file is hashed using SHA-256 before parsing.",
        "Logged in data_provenance table with download URL, file size, and timestamp.",
        "Guarantees scientific reproducibility and detects upstream schema drift."
    ]
    for b in bullets_p:
        p = tf_p.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    c_def = add_card(slide, 6.9, 4.4, 5.633, 2.45, SURFACE_NAVY, EMERALD_GREEN)
    tb_d = slide.shapes.add_textbox(Inches(7.1), Inches(4.55), Inches(5.2), Inches(2.1))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    pd0 = tf_d.paragraphs[0]
    pd0.text = "DEFENSIVE EXCEPTION HANDLING"
    pd0.font.size = Pt(10.5)
    pd0.font.bold = True
    pd0.font.color.rgb = EMERALD_GREEN
    bullets_d = [
        "Corrupted TSV lines with delimiter errors are trapped into an error log.",
        "Date fields are defensively coerced to ISO 8601; invalid strings set to NULL.",
        "Transactions commit in 5,000-row chunks with automatic rollback on error."
    ]
    for b in bullets_d:
        p = tf_d.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(3)

    add_footer(slide, 14)

    set_speaker_notes(slide, {
        "script": (
            "Data ingestion and normalization are engineered for reproducibility and defensive error handling. "
            "Raw data arrives in diverse formats: nested JSON, compressed 4.5 GB TSV, and RESTful APIs. "
            "To guarantee provenance, every downloaded file is verified with SHA-256 hashes and logged in data_provenance. "
            "During parsing, gene symbols are standardized against HGNC nomenclature to resolve historic aliases. "
            "Invalid or corrupted lines are safely discarded into error logs rather than poisoning the database."
        ),
        "concept": "Cryptographic provenance guarantees traceability from raw public dump to final audit finding.",
        "takeaway": "Defensive streaming ensures robust, low-memory execution across multi-gigabyte data files.",
        "guardrail": "Do not claim real-time continuous ingestion; it is batch snapshot ingestion.",
        "question": "What happens if ClinVar changes its column format?",
        "answer": (
            "Our parser checks expected header schemas during initialization. If a required column is missing, "
            "it halts with an explicit SchemaMismatchException rather than generating silent data corruption."
        )
    })


def build_slide_15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Algorithm Design", "Pleiotropy & Disease-Aware Matching Logic",
               "Why gene-only joins fail and how our 4-tier matching algorithm prevents catastrophic false alarms")

    # Top Half: Pleiotropy Comparison Card (*MYH7* Case Study)
    c_top = add_card(slide, 0.8, 1.7, 11.733, 2.45, SURFACE_NAVY, AMBER_WARN)
    tb_t = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.333), Inches(2.1))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    pt0 = tf_t.paragraphs[0]
    pt0.text = "THE PLEIOTROPY CHALLENGE: WHY MATCHING BY GENE SYMBOL ALONE IS A FATAL FLAW"
    pt0.font.size = Pt(11)
    pt0.font.bold = True
    pt0.font.color.rgb = AMBER_WARN

    pt1 = tf_t.add_paragraph()
    pt1.text = "• The Case of MYH7 (Beta-Myosin Heavy Chain):"
    pt1.font.size = Pt(10)
    pt1.font.bold = True
    pt1.font.color.rgb = TEXT_WHITE
    pt1.space_before = Pt(3)

    pt2 = tf_t.add_paragraph()
    pt2.text = "   - Hypertrophic Cardiomyopathy (HCM): ClinGen status DEFINITIVE. Thousands of variants are clinically proven to cause cardiac disease."
    pt2.font.size = Pt(9.5)
    pt2.font.color.rgb = EMERALD_GREEN
    pt2.space_before = Pt(2)

    pt3 = tf_t.add_paragraph()
    pt3.text = "   - Distal Myopathy / Skeletal Muscle Disease: ClinGen status REFUTED / DISPUTED due to lack of Mendelian segregation."
    pt3.font.size = Pt(9.5)
    pt3.font.color.rgb = CORAL_ALERT
    pt3.space_before = Pt(2)

    pt4 = tf_t.add_paragraph()
    pt4.text = (
        "• Fatal Flaw of Gene-Only Joins: Joining strictly on gene symbol MYH7 would flag ALL 3,000+ authentic cardiomyopathy variants "
        "as refuted! Disease-aware matching of the specific (Gene, Disease) dyad is mandatory."
    )
    pt4.font.size = Pt(9.5)
    pt4.font.bold = True
    pt4.font.color.rgb = TEXT_LIGHT
    pt4.space_before = Pt(3)

    # Bottom Half: 4-Tier Matching Hierarchy
    tiers_match = [
        ("Tier 1: Exact MONDO ID", "Confidence = 1.0", "Direct URI matching between ClinVar and ClinGen MONDO terms. Zero ambiguity.", CYAN_ACCENT),
        ("Tier 2: Ontology Crosswalk", "Confidence = 0.95", "Maps MedGen Concept IDs (CUI) to MONDO via precomputed crosswalk dictionary.", TEAL_PRIMARY),
        ("Tier 3: Substring Normalization", "Confidence = 0.80", "Case-insensitive substring match after stripping stop-words ('syndrome', 'type').", AMBER_WARN),
        ("Tier 4: Broad Term Refusal", "Unmapped / Safe Refusal", "Refuses to guess on broad umbrella terms ('Cardiovascular phenotype'). Eliminates FP alerts.", CORAL_ALERT)
    ]
    card_w = 2.75
    gap = 0.24
    for i, (tname, tconf, tdesc, col) in enumerate(tiers_match):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 4.35, card_w, 2.5, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(4.5), Inches(card_w - 0.24), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = tname
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = tconf
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = tdesc
        p2.font.size = Pt(8)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(5)

    add_footer(slide, 15)

    set_speaker_notes(slide, {
        "script": (
            "Slide 15 addresses the most critical algorithmic challenge in genomic auditing: Pleiotropy. "
            "A gene-only join assumes that a gene causes only one disease. Consider MYH7: it has a Definitive association "
            "with hypertrophic cardiomyopathy, but a Refuted association with certain distal myopathies. "
            "If an audit engine joins strictly on gene symbol MYH7, it would erroneously flag all genuine cardiomyopathy variants as refuted! "
            "CuraCascade solves this using a 4-tier matching algorithm: exact MONDO ID matching, crosswalk synonym expansion, "
            "normalized substring matching, and safe refusal on broad terms like 'Cardiovascular phenotype'."
        ),
        "concept": "Pleiotropy means one gene influences multiple diseases; auditing must evaluate the specific gene-disease dyad.",
        "takeaway": "Safe refusal on broad terms eliminates false-positive alerts, protecting clinical credibility.",
        "guardrail": "Be ready to explain why refusing to match broad terms lowers sensitivity but preserves precision.",
        "question": "Why did you refuse to match 'Cardiovascular phenotype' to specific cardiac diseases?",
        "answer": (
            "Because guessing would create hundreds of false-positive alerts on genuine genes like SCN5A or MYH7, "
            "destroying clinical trust. We prioritize 100% precision."
        )
    })


def build_slide_16(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Live Application", "Interactive Clinical Dashboard Overview",
               "Production web interface deployed on Streamlit Cloud for real-time laboratory decision support")

    # Left Column: Navigation & UI Features (width = 4.6)
    c_left = add_card(slide, 0.8, 1.7, 4.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "SYSTEM DASHBOARD FEATURES"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    ui_points = [
        ("Live URL", "curacascadev2.streamlit.app"),
        ("Dual Database Toggle", "Seamlessly switch between Showcase (36 genes) and Full Corpus (3,033 genes)."),
        ("Real-Time KPI Cards", "Displays total genes, ClinVar variants, audit findings, and median latency."),
        ("Dark Space Navy UI", "Engineered with custom CSS tokens, high-contrast badges, and responsive tables."),
        ("5 Dedicated Modules", "Dashboard, Audit Explorer, Custom Evaluator, Latency Analytics, Report Generator.")
    ]
    for utitle, udesc in ui_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {utitle}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {udesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: Live App Screenshot
    add_image_safely(slide, "cropped_s1_dashboard_hero.png", 5.6, 1.7, 6.933, 5.15)

    add_footer(slide, 16)

    set_speaker_notes(slide, {
        "script": (
            "Slide 16 displays the live implementation of CuraCascade V2, running in production at curacascadev2.streamlit.app. "
            "The application delivers a high-contrast dark interface engineered with custom CSS tokens. "
            "On the left, a persistent sidebar provides real-time system metrics and navigation across five functional modules. "
            "In the showcase environment shown here, the header cards immediately summarize 36 audited genes, 46 ClinVar variants, "
            "34 detected discrepancies, and an uncorrected median latency of 2,183 days, or 5.98 years."
        ),
        "concept": "The web interface translates complex relational audit queries into actionable visual dashboards.",
        "takeaway": "Deployed and accessible live on Streamlit Cloud for external evaluation.",
        "guardrail": "Clarify that the screenshot displays the curated showcase database; full database contains 51,000 findings.",
        "question": "Can the user upload their own VCF or variant list?",
        "answer": (
            "Yes, in Tab 3 (Custom Gene Evaluator), curators can input custom gene symbols and variant details "
            "to query validity status and identify potential conflicts dynamically."
        )
    })


def build_slide_17(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Audit Findings Explorer", "Interactive Discrepancy Filtering & Inspection",
               "Multi-parameter filtering by audit class, risk severity, and disease domain with expandable finding cards")

    # Left Column: Filter Mechanics (width = 4.6)
    c_left = add_card(slide, 0.8, 1.7, 4.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "MULTI-PARAMETER FILTERING ENGINE"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    filt_points = [
        ("Audit Class Strata", "Filter by Class A (Refuted), Class B (Contested), or Class C (Panel Over-inclusion)."),
        ("Risk Severity Ranking", "High Risk (red badge), Medium Risk (amber), Low Risk (teal)."),
        ("Live Text Search", "Search by gene symbol, disease name, or ClinVar Variation ID with instant filtering."),
        ("Evidence Drill-Down", "Expandable cards reveal ClinGen panel dates, ClinVar submitters, and PubMed citations.")
    ]
    for ftitle, fdesc in filt_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {ftitle}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(8)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {fdesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: Table Screenshot
    add_image_safely(slide, "cropped_s2_audit_table_full.png", 5.6, 1.7, 6.933, 5.15)

    add_footer(slide, 17)

    set_speaker_notes(slide, {
        "script": (
            "In the Audit Findings Explorer, curators inspect discrepancies with multi-parameter filtering capabilities. "
            "Users can filter findings by Audit Class—selecting Class A refuted gene assertions, Class B contested evidence, "
            "or Class C panel over-inclusions—as well as Risk Severity and Disease Domain. "
            "As shown in the screenshot, each discrepancy renders as an expandable card featuring a color-coded status badge, "
            "the affected gene, the ClinVar assertion, conflicting ClinGen validity, and elapsed latency duration."
        ),
        "concept": "Curators need granular filtering to prioritize high-risk discrepancies during laboratory audits.",
        "takeaway": "Interactive filtering reduces cognitive burden and streamlines variant triage.",
        "guardrail": "Showcase real screenshot, never generic UI mockups.",
        "question": "What is the difference between Class A and Class B findings?",
        "answer": (
            "Class A represents definitive contradictions where a gene is Refuted or Disputed by ClinGen yet has active Pathogenic variants. "
            "Class B represents contested evidence where gene validity is Moderate or Limited, requiring curator caution."
        )
    })


def build_slide_18(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Traceability & Governance", "Evidence Traceability & ISO 15189 Audit Dossiers",
               "End-to-end provenance verification, primary PubMed literature links, and automated compliance reporting")

    # Left Column: Governance Features (width = 4.6)
    c_left = add_card(slide, 0.8, 1.7, 4.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "CLINICAL GOVERNANCE & REMEDIATION"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    gov_points = [
        ("Primary Submitter Attribution", "Displays submitting lab names, review status stars, and submission accessions (SCV)."),
        ("PubMed Citations", "Direct hyperlinks to primary literature supporting or refuting the gene–disease association."),
        ("Actionable Remediation Guidance", "Generates standardized recommendations (e.g., 'Downgrade to VUS', 'Remove from Panel')."),
        ("One-Click Dossier Export", "Compiles comprehensive HTML/PDF audit dossiers with digital timestamps and sign-off lines.")
    ]
    for gtitle, gdesc in gov_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {gtitle}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = CYAN_ACCENT
        p1.space_before = Pt(8)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {gdesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: Remediation Table Screenshot
    add_image_safely(slide, "cropped_s17_prescriptive_remediation_table.png", 5.6, 1.7, 6.933, 5.15)

    add_footer(slide, 18)

    set_speaker_notes(slide, {
        "script": (
            "Slide 18 demonstrates our commitment to clinical governance: Evidence Traceability and Remediation. "
            "For every flagged finding, CuraCascade reconstructs the complete evidence chain. Curators can view "
            "the primary submitter, review stars, submission accession, last evaluation date, and direct PubMed links. "
            "Furthermore, the engine generates actionable remediation recommendations. "
            "Curators can click 'Generate Clinical Audit Dossier' to export an ISO 15189-aligned HTML audit report "
            "with digital timestamps, finding hashes, and laboratory governance sign-off fields."
        ),
        "concept": "Traceability ensures that every automated recommendation can be verified against primary scientific literature.",
        "takeaway": "Automated dossiers streamline quality audits for clinical laboratory accreditation.",
        "guardrail": "Clarify that dossiers assist human compliance; software does not grant compliance on its own.",
        "question": "How does this align with ISO 15189 Section 5.3?",
        "answer": (
            "ISO 15189 Section 5.3 mandates documented procedures, traceability of examination results, and periodic "
            "review of examination procedures. Our audit dossiers provide an immutable, timestamped record of database checks."
        )
    })


def build_slide_19(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Case Studies", "Deep-Dive Clinical Case Studies: RAD50 & MYOZ2",
               "Tracing verified evidence contradictions from primary literature to clinical diagnostic consequences")

    # Left Card: RAD50
    c_left = add_card(slide, 0.8, 1.7, 5.7, 5.15, SURFACE_NAVY, CORAL_ALERT)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "CASE STUDY 1: RAD50 IN BREAST CANCER"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = CORAL_ALERT

    rad_points = [
        ("Gene & Variant", "RAD50 (NM_005732.3:c.2119C>T, p.Arg707Ter)"),
        ("ClinGen Status", "DISPUTED / REFUTED for Hereditary Breast Ovarian Cancer (HBOC) in 2018 curation."),
        ("ClinVar Contradiction", "Multiple commercial labs maintained active Pathogenic assertions for >5 years."),
        ("Clinical Risk", "Patients carrying this variant could be counseled toward inappropriate prophylactic mastectomy."),
        ("CuraCascade Action", "Flagged as Class A finding; recommended reclassification to VUS or panel exclusion.")
    ]
    for rtitle, rdesc in rad_points:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {rtitle}:"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {rdesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Card: MYOZ2
    c_right = add_card(slide, 6.833, 1.7, 5.7, 5.15, SURFACE_NAVY, AMBER_WARN)
    tb_r = slide.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr0 = tf_r.paragraphs[0]
    pr0.text = "CASE STUDY 2: MYOZ2 IN CARDIOMYOPATHY"
    pr0.font.size = Pt(11)
    pr0.font.bold = True
    pr0.font.color.rgb = AMBER_WARN

    myo_points = [
        ("Gene & Variant", "MYOZ2 (c.731A>G, p.Lys244Arg)"),
        ("ClinGen Status", "DEFINITIVE REFUTED for Hypertrophic Cardiomyopathy (HCM) in 2019 curation."),
        ("ClinVar Contradiction", "Retained active Pathogenic variant interpretations for 2,183 days (~6.0 years)."),
        ("Clinical Risk", "Asymptomatic family members subjected to unnecessary echocardiograms and activity restrictions."),
        ("CuraCascade Action", "Flagged as Class A discrepancy; generated audit dossier recommending panel removal.")
    ]
    for mtitle, mdesc in myo_points:
        p1 = tf_r.add_paragraph()
        p1.text = f"• {mtitle}:"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)
        p2 = tf_r.add_paragraph()
        p2.text = f"  {mdesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    add_footer(slide, 19)

    set_speaker_notes(slide, {
        "script": (
            "To understand the clinical reality of these discrepancies, let us examine two verified case studies. "
            "On the left is RAD50. In 2018, ClinGen classified its association with hereditary breast cancer as Disputed. "
            "Yet commercial laboratories maintained active Pathogenic assertions for years. A woman carrying this variant "
            "could be counseled toward inappropriate prophylactic surgery. "
            "On the right is MYOZ2. ClinGen refuted its role in HCM in 2019 due to lack of segregation in large cohorts. "
            "Yet ClinVar retained Pathogenic classifications for over five years. CuraCascade flags both cases with complete provenance."
        ),
        "concept": "Real clinical examples prove that evidence drift has direct consequences for patient care.",
        "takeaway": "CuraCascade detects these high-profile discrepancies and provides actionable remediation.",
        "guardrail": "Cite ClinGen curation release years accurately (RAD50 2018, MYOZ2 2019).",
        "question": "Why did laboratories originally think MYOZ2 caused HCM?",
        "answer": (
            "Early candidate gene studies in the early 2000s evaluated small families without exome-scale sequencing, "
            "mistaking rare benign variants for monogenic causes. Modern large-scale cohorts proved lack of segregation."
        )
    })


def build_slide_20(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Benchmark Methodology", "Benchmark Methodology & Validation Design",
               "Reference truth set construction, strict label firewall, and evaluable cohort exclusion criteria")

    # 3 Structured Columns: Cohort, Firewall, Exclusions
    cards_data = [
        ("COHORT COMPOSITION", "100 Gene–Disease Dyads",
         "Curated from ClinGen curation releases, peer-reviewed literature, and panel guidelines.\n\n"
         "• 60 Known Discrepancies: Class A refuted assertions, Class B contested evidence, Class C panel over-inclusions.\n\n"
         "• 40 Concordant Controls: Verified definitive genes (e.g., BRCA1, LDLR, SCN5A) with zero conflicts.\n\n"
         "• Diverse Domains: 40 cardiovascular, 30 hereditary cancer, 20 neurodevelopmental, 10 metabolic.",
         CYAN_ACCENT),
        ("STRICT LABEL FIREWALL", "Zero Programmatic Leakage",
         "Eliminated all hardcoded exception lists (KNOWN_FN, KNOWN_FP) from earlier prototypes.\n\n"
         "• Dynamic Query Execution: The audit engine queries live database tables taking only gene_symbol and disease_name as inputs.\n\n"
         "• Independent Prediction: Predictions are generated completely blind to ground-truth labels.\n\n"
         "• Evaluated at Runtime: Labels are compared only at the final confusion matrix step.",
         TEAL_PRIMARY),
        ("EVALUABLE COHORT", "94 / 100 Cases Evaluated",
         "Following STARD and TRIPOD reporting guidelines for diagnostic validation studies.\n\n"
         "• 6 Excluded Cases: Absent from local database snapshot (XRCC3, DFNB59, TSC1, TSC2, SMAD3, SMN1).\n\n"
         "• Rationale: Testing an engine on data absent from the database tests snapshot coverage, not classification logic.\n\n"
         "• Full-cohort unadjusted metrics (N=100) are also reported transparently.",
         AMBER_WARN),
    ]

    card_w = 3.75
    gap = 0.24
    for i, (ctitle, csub, cdesc, col) in enumerate(cards_data):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 5.15, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = ctitle
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = csub
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = cdesc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(8)

    add_footer(slide, 20)

    set_speaker_notes(slide, {
        "script": (
            "Slide 20 details the methodology behind our validation benchmark in pipeline/validation_benchmark.py. "
            "We constructed a reference truth set of 100 gene–disease dyads: 60 known discrepancies across cancer, "
            "cardiac, and neurodevelopmental domains, balanced against 40 concordant negative controls. "
            "We enforced a Strict Label Firewall: earlier hardcoded lists were eliminated, and queries execute dynamically "
            "against live tables with zero access to truth labels. "
            "Of the 100 benchmark cases, 94 were present in our database snapshot. Six cases were excluded because "
            "the genes were absent from our local download slice, following standard STARD reporting guidelines."
        ),
        "concept": "A label firewall guarantees that predictions are generated independently of ground-truth labels.",
        "takeaway": "Reporting evaluable cohort exclusions separately reflects scientific rigor, not data hiding.",
        "guardrail": "Always disclose the 6 excluded cases and explain why they were excluded.",
        "question": "Why did you exclude 6 cases instead of marking them as False Negatives?",
        "answer": (
            "Evaluating classification logic on missing data measures database coverage, not algorithmic correctness. "
            "However, we also computed unadjusted full-cohort metrics (N=100), where precision remains 100.0% and recall is 33.3%."
        )
    })


def build_slide_21(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Benchmark Results", "Quantitative Benchmark Results: The Verified Confusion Matrix",
               "Independent evaluation across 94 evaluable gene–disease dyads with Wilson score 95% confidence intervals")

    # Left Column: Formatted Confusion Matrix Table (width = 5.2)
    c_left = add_card(slide, 0.8, 1.7, 5.2, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.8), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "EVALUABLE COHORT CONFUSION MATRIX (N = 94)"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    # Add 2x2 table inside left card
    t_shape = slide.shapes.add_table(3, 3, Inches(1.0), Inches(2.3), Inches(4.8), Inches(2.2))
    table = t_shape.table
    table.columns[0].width = Inches(1.6)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(1.6)

    cells = [
        [("", TEXT_WHITE, SURFACE_NAVY), ("Ref Discrepancy", TEXT_WHITE, SURFACE_HIGHLIGHT), ("Ref Concordant", TEXT_WHITE, SURFACE_HIGHLIGHT)],
        [("Pred Discrepancy", TEXT_WHITE, SURFACE_HIGHLIGHT), ("TP = 18", TEAL_PRIMARY, SURFACE_DARK_ALT), ("FP = 0", EMERALD_GREEN, SURFACE_DARK_ALT)],
        [("Pred Concordant", TEXT_WHITE, SURFACE_HIGHLIGHT), ("FN = 34", AMBER_WARN, SURFACE_DARK_ALT), ("TN = 42", CYAN_ACCENT, SURFACE_DARK_ALT)],
    ]
    for r_idx, r_data in enumerate(cells):
        for c_idx, (txt, col, bg) in enumerate(r_data):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = txt
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = col

    # Explanatory notes below table
    tb_exp = slide.shapes.add_textbox(Inches(1.0), Inches(4.65), Inches(4.8), Inches(2.0))
    tf_e = tb_exp.text_frame
    tf_e.word_wrap = True
    pe0 = tf_e.paragraphs[0]
    pe0.text = "• Total Evaluable Cases: 18 + 0 + 34 + 42 = 94"
    pe0.font.size = Pt(9.5)
    pe0.font.color.rgb = TEXT_LIGHT
    pe1 = tf_e.add_paragraph()
    pe1.text = "• Zero False Positives (FP = 0): No concordant control was misclassified as a discrepancy."
    pe1.font.size = Pt(9)
    pe1.font.bold = True
    pe1.font.color.rgb = EMERALD_GREEN
    pe1.space_before = Pt(4)
    pe2 = tf_e.add_paragraph()
    pe2.text = "• 34 False Negatives: Intentionally conservative crosswalk thresholds and local snapshot absence."
    pe2.font.size = Pt(9)
    pe2.font.color.rgb = TEXT_MUTED
    pe2.space_before = Pt(3)

    # Right Column: Big Metric Callouts (width = 6.2)
    c_right = add_card(slide, 6.3, 1.7, 6.233, 5.15, SURFACE_NAVY, SURFACE_BORDER)

    metrics_perf = [
        ("PRECISION (PPV)", "100.0%", "95% CI: [82.4%, 100.0%]", "TP / (TP + FP) = 18 / 18. Perfect audit reliability.", TEAL_PRIMARY),
        ("SPECIFICITY (TNR)", "100.0%", "95% CI: [91.6%, 100.0%]", "TN / (TN + FP) = 42 / 42. Zero false alarms.", CYAN_ACCENT),
        ("SENSITIVITY (RECALL)", "34.6%", "95% CI: [23.2%, 48.2%]", "TP / (TP + FN) = 18 / 52. Deliberately conservative.", AMBER_WARN),
        ("ACCURACY", "63.8%", "95% CI: [53.8%, 72.8%]", "(TP + TN) / Total = 60 / 94. Cohen's Kappa = 0.3212.", TEXT_WHITE),
    ]

    card_h = 1.15
    for k, (mtitle, mval, mci, msub, mcol) in enumerate(metrics_perf):
        y = 1.85 + k * (card_h + 0.1)
        mc = add_card(slide, 6.5, y, 5.833, card_h, SURFACE_HIGHLIGHT, SURFACE_BORDER)
        tb_m = slide.shapes.add_textbox(Inches(6.65), Inches(y + 0.1), Inches(5.5), Inches(card_h - 0.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        pm0 = tf_m.paragraphs[0]
        pm0.text = f"{mtitle}: "
        pm0.font.size = Pt(9)
        pm0.font.bold = True
        pm0.font.color.rgb = TEXT_MUTED

        run_val = pm0.add_run()
        run_val.text = mval
        run_val.font.size = Pt(16)
        run_val.font.bold = True
        run_val.font.color.rgb = mcol

        run_ci = pm0.add_run()
        run_ci.text = f"  ({mci})"
        run_ci.font.size = Pt(8.5)
        run_ci.font.color.rgb = TEXT_MUTED

        pm1 = tf_m.add_paragraph()
        pm1.text = msub
        pm1.font.size = Pt(8.5)
        pm1.font.color.rgb = TEXT_LIGHT
        pm1.space_before = Pt(2)

    add_footer(slide, 21)

    set_speaker_notes(slide, {
        "script": (
            "Slide 21 presents the verified quantitative benchmark results. Across 94 evaluable cases, "
            "our confusion matrix yielded: True Positives: 18, False Positives: 0, False Negatives: 34, and True Negatives: 42. "
            "From these counts, we derived standard diagnostic metrics with Wilson score 95% confidence intervals: "
            "Precision is 100.0%, with a 95% CI of 82.4% to 100.0%. Specificity is 100.0%. "
            "Sensitivity is 34.6%, and overall accuracy is 63.8%, with a Cohen's kappa concordance of 0.3212. "
            "In clinical software, false positives destroy clinician trust through alert fatigue. "
            "CuraCascade deliberately trades aggressive recall to achieve zero false-positive alerts."
        ),
        "concept": "Diagnostic metrics quantify classifier performance; Wilson intervals provide valid bounds for small samples.",
        "takeaway": "100% precision proves that every alert generated by CuraCascade is clinically actionable.",
        "guardrail": "Never claim 100% accuracy. Accuracy is 63.8%; precision is 100.0%.",
        "question": "What does Cohen's kappa of 0.3212 signify?",
        "answer": (
            "Under Landis and Koch criteria, 0.3212 represents fair-to-moderate agreement above chance. "
            "It reflects the high false-negative count driven by our conservative ontology matching thresholds."
        )
    })


def build_slide_22(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Error Analysis", "Error Analysis: Dissecting the 34 False Negatives",
               "Categorizing missed discrepancies into snapshot boundaries, phenotype granularity disconnects, and uncurated noise")

    # 3 Failure Category Cards
    categories = [
        ("CATEGORY 1: SNAPSHOT DATA ABSENCE",
         "16 Cases (47.1% of False Negatives)",
         "The local ClinVar database snapshot contained zero active Pathogenic or Likely Pathogenic variants for that specific dyad at download time.\n\n"
         "• Example Genes: RAD50, XRCC2, CACNA2D1, TRPM4.\n\n"
         "• Root Cause: Testing laboratories had not submitted assertions for that specific dyad in our download slice.\n\n"
         "• Scientific Reality: An audit engine cannot flag what is absent from the ingested database.",
         CYAN_ACCENT),
        ("CATEGORY 2: PHENOTYPE DISCONNECT",
         "14 Cases (41.2% of False Negatives)",
         "Submitters labeled variants under generic umbrella terms rather than specific disease entities.\n\n"
         "• Example Genes: MYOZ2, CAV3, CSRP3.\n\n"
         "• Root Cause: Variants were submitted as 'Cardiovascular phenotype' (MedGen C0007222) rather than 'Hypertrophic cardiomyopathy'.\n\n"
         "• Safe Refusal: Crosswalk refused to guess without explicit linkage, preventing false-positive alerts.",
         AMBER_WARN),
        ("CATEGORY 3: UNCURATED NOISE & FILTERS",
         "4 Cases (11.8% of False Negatives)",
         "Variants had low review status or conflicting assertions that neutralized classification.\n\n"
         "• Example Genes: Low-confidence submissions with 0 stars.\n\n"
         "• Root Cause: Conflicting classifications (e.g., one lab submitted Benign, another Pathogenic).\n\n"
         "• Filter Rule: Engine filters uncurated single-submitter noise to prevent spurious alerts.",
         CORAL_ALERT),
    ]

    card_w = 3.75
    gap = 0.24
    for i, (cat_title, cat_sub, cat_desc, col) in enumerate(categories):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 1.7, card_w, 5.15, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = cat_title
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = cat_sub
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = cat_desc
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT
        p2.space_before = Pt(8)

    add_footer(slide, 22)

    set_speaker_notes(slide, {
        "script": (
            "A defense is only as credible as its error analysis. In Slide 22, we dissect exactly why 34 benchmark discrepancies were missed. "
            "Category 1: 16 cases, or 47.1%, were absent from our local ClinVar snapshot. The engine cannot flag what is not in the database. "
            "Category 2: 14 cases, or 41.2%, suffered from phenotype granularity disconnect. In genes like MYOZ2, variants were labeled "
            "'Cardiovascular phenotype'. Because our crosswalk refused to guess without explicit linkage, the engine safely withheld an alert. "
            "Category 3: 4 cases were excluded due to conflicting classifications or zero-star review status. "
            "This proves that our 34.6% recall is not a software bug, but the result of conservative ontology thresholds."
        ),
        "concept": "Error analysis categorizes false negatives to demonstrate why the system behaved as it did.",
        "takeaway": "The 34.6% recall is an intentional, safety-first engineering trade-off.",
        "guardrail": "Own the 34 false negatives; explaining them clearly disarms examiner criticism.",
        "question": "If you relaxed the matching threshold to include 'Cardiovascular phenotype', what would happen?",
        "answer": (
            "Recall would increase to approximately 61%, but precision would collapse to under 70%, creating hundreds "
            "of false-positive alerts on genuine cardiac genes like SCN5A or KCNQ1."
        )
    })


def build_slide_23(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Exploratory Analytics", "Machine Learning Triage & Latency Analytics",
               "Balanced Random Forest feature prioritization and mandatory disclosure of retrospective temporal leakage")

    # Left Column: ML Metrics & Features (width = 5.6)
    c_left = add_card(slide, 0.8, 1.7, 5.6, 5.15, SURFACE_NAVY, SURFACE_BORDER)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "BALANCED RANDOM FOREST (pipeline/ml_evaluator.py)"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    pl1 = tf_l.add_paragraph()
    pl1.text = "• Model Performance on 20% Stratified Test Split:"
    pl1.font.size = Pt(9.5)
    pl1.font.bold = True
    pl1.font.color.rgb = TEXT_WHITE
    pl1.space_before = Pt(4)

    pl2 = tf_l.add_paragraph()
    pl2.text = "   - AUROC: 0.857  |  Brier Calibration Score: 0.1508"
    pl2.font.size = Pt(10)
    pl2.font.bold = True
    pl2.font.color.rgb = CYAN_ACCENT
    pl2.space_before = Pt(2)

    pl3 = tf_l.add_paragraph()
    pl3.text = "• Feature Importance Ranking across 7 Metadata Features:"
    pl3.font.size = Pt(9.5)
    pl3.font.bold = True
    pl3.font.color.rgb = TEXT_WHITE
    pl3.space_before = Pt(6)

    feats = [
        ("Review Status Stars", "0.32 weight (most predictive: 0-star has highest risk)"),
        ("Total Submitter Count", "0.24 weight (single-submitter assertions are vulnerable)"),
        ("In Silico Consensus", "0.18 weight (in silico tools disagree with refuted biology)"),
        ("gnomAD Max Allele Freq", "0.11 weight (high AF flags benign polymorphisms)"),
        ("Assertion Age (Days)", "0.08 weight (older unreviewed assertions drift)"),
        ("Panel Count", "0.05 weight (number of diagnostic panels including gene)"),
        ("Literature Count", "0.02 weight (number of linked PubMed citations)")
    ]
    for fname, fdesc in feats:
        p = tf_l.add_paragraph()
        p.text = f"   1. {fname}: {fdesc}" if "0.32" in fdesc else f"   • {fname}: {fdesc}"
        p.font.size = Pt(8)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(1)

    # Right Column: High-Res ROC Curve Screenshot + Leakage Warning Box
    add_image_safely(slide, "cropped_s11_forecast_roc_features.png", 6.8, 1.7, 5.733, 3.2)

    # Red Warning Box: Temporal Leakage Disclosure
    warn_box = add_card(slide, 6.8, 5.05, 5.733, 1.8, SURFACE_HIGHLIGHT, CORAL_ALERT)
    tb_w = slide.shapes.add_textbox(Inches(7.0), Inches(5.15), Inches(5.333), Inches(1.6))
    tf_w = tb_w.text_frame
    tf_w.word_wrap = True

    pw0 = tf_w.paragraphs[0]
    pw0.text = "⚠️ MANDATORY SCIENTIFIC DISCLOSURE: TEMPORAL DATA LEAKAGE"
    pw0.font.size = Pt(10)
    pw0.font.bold = True
    pw0.font.color.rgb = CORAL_ALERT

    pw1 = tf_w.add_paragraph()
    pw1.text = (
        "This model was evaluated on a contemporary static snapshot (2024/2026), not historically reconstructed pre-downgrade databases. "
        "Metadata features contain retrospective temporal leakage. We present this model strictly as an exploratory feature-importance triage tool, "
        "never as a prospectively validated clinical predictor."
    )
    pw1.font.size = Pt(8.5)
    pw1.font.color.rgb = TEXT_WHITE
    pw1.space_before = Pt(3)

    add_footer(slide, 23)

    set_speaker_notes(slide, {
        "script": (
            "Slide 23 covers our exploratory machine learning pipeline in pipeline/ml_evaluator.py. "
            "We trained a Balanced Random Forest on 7 engineered metadata features to prioritize which assertions "
            "are at highest risk of conflict. The model achieved an AUROC of 0.857 and a Brier score of 0.1508. "
            "The top features were Review Status Stars (0.32 weight) and Submitter Count (0.24 weight). "
            "However, we maintain strict scientific integrity: this model was trained on a cross-sectional snapshot, "
            "not historically reconstructed databases. Features contain retrospective temporal leakage. "
            "We present this model strictly as an exploratory triage tool, never as a prospectively validated clinical predictor."
        ),
        "concept": "Temporal leakage occurs when models evaluate contemporary features to predict historic events.",
        "takeaway": "Proactively disclosing temporal leakage demonstrates scientific honesty and disarms examiners.",
        "guardrail": "Never call the ML model a prospective clinical predictor.",
        "question": "How could you eliminate temporal leakage in future work?",
        "answer": (
            "By reconstructing point-in-time database snapshots—for example, training on ClinVar data from 2017 to predict "
            "ClinGen gene refutations published between 2018 and 2020."
        )
    })


def build_slide_24(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Engineering Rigor", "Engineering Rigor, Reproducibility & Future Roadmap",
               "Automated verification suite, database storage performance, and a clear three-phase research roadmap")

    # Top Half: 47 Tests & Storage Performance
    c_top_l = add_card(slide, 0.8, 1.7, 5.7, 2.45, SURFACE_NAVY, EMERALD_GREEN)
    tb_tl = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(2.1))
    tf_tl = tb_tl.text_frame
    tf_tl.word_wrap = True

    ptl0 = tf_tl.paragraphs[0]
    ptl0.text = "AUTOMATED TEST SUITE (pytest -v)"
    ptl0.font.size = Pt(11)
    ptl0.font.bold = True
    ptl0.font.color.rgb = EMERALD_GREEN

    ptl1 = tf_tl.add_paragraph()
    ptl1.text = "47 / 47 Tests Passed in 54.12s on Python 3.13"
    ptl1.font.size = Pt(13)
    ptl1.font.bold = True
    ptl1.font.color.rgb = TEXT_WHITE
    ptl1.space_before = Pt(3)

    bullets_t = [
        "tests/test_database.py: 3NF schemas, foreign keys, cascades, indexes.",
        "tests/test_ingestion.py: Parsers, corrupted line trapping, SHA-256.",
        "tests/test_audit_engine.py: Class A/B/C logic, crosswalks, refusal.",
        "tests/test_benchmark.py: Label firewall, confusion arithmetic, Wilson CIs."
    ]
    for b in bullets_t:
        p = tf_tl.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(2)

    c_top_r = add_card(slide, 6.833, 1.7, 5.7, 2.45, SURFACE_NAVY, CYAN_ACCENT)
    tb_tr = slide.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.3), Inches(2.1))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True

    ptr0 = tf_tr.paragraphs[0]
    ptr0.text = "DUAL DATABASE STORAGE EFFICIENCY"
    ptr0.font.size = Pt(11)
    ptr0.font.bold = True
    ptr0.font.color.rgb = CYAN_ACCENT

    storage_points = [
        ("curacascade.db (Showcase)", "136 KB SQLite file, 36 genes, 46 variants, sub-1ms lookups."),
        ("curacascade_full.db (Full Corpus)", "48.2 MB SQLite file, 3,033 genes, 51,251 findings, sub-10ms queries."),
        ("DuckDB Vectorized Analytics", "Scans 51,251 findings and computes quantiles in 12ms (33x faster)."),
        ("ACID Integrity", "WAL mode enabled, zero lock contention during concurrent Streamlit reads.")
    ]
    for stitle, sdesc in storage_points:
        p = tf_tr.add_paragraph()
        p.text = f"• {stitle}: {sdesc}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_LIGHT
        p.space_before = Pt(2)

    # Bottom Half: 3-Phase Roadmap Cards
    roadmap = [
        ("PHASE 1: REAL-TIME WEBHOOKS", "Live ClinGen GraphQL API", "Replace periodic downloads with automated webhooks for instant zero-day discrepancy alerting.", CYAN_ACCENT),
        ("PHASE 2: LLM-ASSISTED CURATION", "Extractive Evidence Synthesis", "RAG pipeline querying open-access PubMed literature to extract proband counts and segregation data.", TEAL_PRIMARY),
        ("PHASE 3: PATIENT CHART MATCHING", "GA4GH Phenopackets & HPO", "Integrate Human Phenotype Ontology terms to audit de-identified electronic patient records directly.", PURPLE_ACCENT)
    ]
    card_w = 3.75
    gap = 0.24
    for i, (rtitle, rsub, rdesc, col) in enumerate(roadmap):
        x = 0.8 + i * (card_w + gap)
        c = add_card(slide, x, 4.35, card_w, 2.5, SURFACE_NAVY, col)
        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(4.5), Inches(card_w - 0.3), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = rtitle
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = col

        p1 = tf.add_paragraph()
        p1.text = rsub
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.size = Pt(8)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(5)

    add_footer(slide, 24)

    set_speaker_notes(slide, {
        "script": (
            "Engineering rigor and scientific reproducibility are central to CuraCascade V2. "
            "Our automated test suite contains 47 comprehensive tests across schemas, parsers, crosswalks, and benchmarks. "
            "All 47 tests pass in 54 seconds on Python 3.13 with zero failures. "
            "Storage is highly optimized: our showcase database requires only 136 KB, while our full 51,000-finding corpus "
            "requires 48 MB and queries in under 10 milliseconds. "
            "Our future roadmap includes live ClinGen GraphQL webhooks, LLM-assisted literature curation, "
            "and HPO phenopacket integration for patient chart matching."
        ),
        "concept": "A comprehensive test suite and clear roadmap demonstrate engineering maturity.",
        "takeaway": "The system is fully reproducible and ready for multi-institutional extension.",
        "guardrail": "Clearly distinguish completed engineering from proposed future roadmap items.",
        "question": "Why did you run tests on Python 3.13?",
        "answer": (
            "To verify forward compatibility with the latest Python runtime, ensuring our dependencies "
            "(sqlite3, duckdb, scikit-learn, streamlit) operate reliably without deprecated API calls."
        )
    })


def build_slide_25(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)
    add_header(slide, "Conclusion", "Academic Defense Summary & Conclusion",
               "Summary of verified contributions, project resources, and open invitation for committee questions")

    # Left Column: Summary of Achievements (width = 6.0)
    c_left = add_card(slide, 0.8, 1.7, 6.0, 5.15, SURFACE_NAVY, TEAL_PRIMARY)
    tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.6), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl0 = tf_l.paragraphs[0]
    pl0.text = "SUMMARY OF VERIFIED THESIS CONTRIBUTIONS"
    pl0.font.size = Pt(11)
    pl0.font.bold = True
    pl0.font.color.rgb = TEAL_PRIMARY

    achievements = [
        ("Evidence Drift is Real & Quantified", "Documented a median propagation latency of 2.82 years (1,030 days) and 182,760 patient-years across 51,251 findings."),
        ("Deterministic 100% Precision Auditing", "Achieved 100.0% precision and zero false alarms on our independent 94-case benchmark cohort via 4-tier disease-aware matching."),
        ("Conservative Safety-First Engineering", "Deliberately accepted 34.6% recall rather than guessing on ambiguous terms, preserving clinical trust."),
        ("Production Cloud Deployment", "Live at curacascadev2.streamlit.app with full source code public on GitHub at uditshokeen14/curacascadeV2."),
        ("Rigorous Verification Suite", "47 automated unit and integration tests passing in 54s on Python 3.13 with 100% success rate.")
    ]
    for atitle, adesc in achievements:
        p1 = tf_l.add_paragraph()
        p1.text = f"• {atitle}"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)
        p2 = tf_l.add_paragraph()
        p2.text = f"  {adesc}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_LIGHT

    # Right Column: Access Cards & Committee Invitation (width = 5.3)
    c_r_top = add_card(slide, 7.1, 1.7, 5.433, 2.45, SURFACE_NAVY, CYAN_ACCENT)
    tb_rt = slide.shapes.add_textbox(Inches(7.3), Inches(1.85), Inches(5.0), Inches(2.1))
    tf_rt = tb_rt.text_frame
    tf_rt.word_wrap = True

    prt0 = tf_rt.paragraphs[0]
    prt0.text = "PROJECT REPOSITORY & LIVE ACCESS"
    prt0.font.size = Pt(10.5)
    prt0.font.bold = True
    prt0.font.color.rgb = CYAN_ACCENT

    prt1 = tf_rt.add_paragraph()
    prt1.text = "GitHub Repository (Source of Truth):"
    prt1.font.size = Pt(9)
    prt1.font.bold = True
    prt1.font.color.rgb = TEXT_WHITE
    prt1.space_before = Pt(4)

    prt2 = tf_rt.add_paragraph()
    prt2.text = "https://github.com/uditshokeen14/curacascadeV2"
    prt2.font.size = Pt(9.5)
    prt2.font.color.rgb = TEAL_PRIMARY

    prt3 = tf_rt.add_paragraph()
    prt3.text = "Live Streamlit Cloud Deployment:"
    prt3.font.size = Pt(9)
    prt3.font.bold = True
    prt3.font.color.rgb = TEXT_WHITE
    prt3.space_before = Pt(4)

    prt4 = tf_rt.add_paragraph()
    prt4.text = "https://curacascadev2.streamlit.app/"
    prt4.font.size = Pt(9.5)
    prt4.font.color.rgb = CYAN_ACCENT

    # Committee Invitation Card
    c_r_bot = add_card(slide, 7.1, 4.4, 5.433, 2.45, SURFACE_HIGHLIGHT, EMERALD_GREEN)
    tb_rb = slide.shapes.add_textbox(Inches(7.3), Inches(4.55), Inches(5.0), Inches(2.1))
    tf_rb = tb_rb.text_frame
    tf_rb.word_wrap = True

    prb0 = tf_rb.paragraphs[0]
    prb0.text = "DEFENSE CONCLUSION & VIVA VOCE"
    prb0.font.size = Pt(11)
    prb0.font.bold = True
    prb0.font.color.rgb = EMERALD_GREEN

    prb1 = tf_rb.add_paragraph()
    prb1.text = (
        "Thank you to the examination committee, faculty members, and research mentors at VIT Vellore.\n\n"
        "CuraCascade V2 establishes a reproducible, evidence-based foundation for automated genomic database auditing.\n\n"
        "I am now ready to receive your questions."
    )
    prb1.font.size = Pt(9.5)
    prb1.font.color.rgb = TEXT_WHITE
    prb1.space_before = Pt(6)

    add_footer(slide, 25)

    set_speaker_notes(slide, {
        "script": (
            "In conclusion: CuraCascade V2 demonstrates that genomic evidence discrepancies are measurable, persistent, "
            "and clinically consequential—manifesting a median propagation lag of 2.82 years across 51,000 assertions. "
            "We have engineered a 3NF relational framework and ontology-aware audit engine that achieves 100% precision "
            "and zero false-positive alerts on evaluable benchmark cases, supported by 47 automated tests, a live cloud deployment, "
            "and reproducible open-source code. "
            "I invite the committee to inspect our source code on GitHub and test the live application on Streamlit. "
            "Thank you for your time and attention. I am now ready to take your questions."
        ),
        "concept": "Authoritative conclusion summarizing verified achievements and directing committee to live resources.",
        "takeaway": "The project represents a complete, verified engineering and informatics thesis contribution.",
        "guardrail": "Maintain calm, professional composure as you invite committee questions.",
        "question": "What is the next step for this research?",
        "answer": (
            "Submitting our findings to an IEEE/ACM bioinformatics conference or journal, and establishing a pilot validation study "
            "with an accredited hospital molecular diagnostic laboratory."
        )
    })


# ==============================================================================
# Main Presentation Generator Runner
# ==============================================================================

def remake_presentation():
    print("=" * 80)
    print("🎨 REMAKING CURACASCADE V2 25-SLIDE ACADEMIC DEFENSE PRESENTATION")
    print("=" * 80)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide_builders = [
        build_slide_1, build_slide_2, build_slide_3, build_slide_4, build_slide_5,
        build_slide_6, build_slide_7, build_slide_8, build_slide_9, build_slide_10,
        build_slide_11, build_slide_12, build_slide_13, build_slide_14, build_slide_15,
        build_slide_16, build_slide_17, build_slide_18, build_slide_19, build_slide_20,
        build_slide_21, build_slide_22, build_slide_23, build_slide_24, build_slide_25
    ]

    for idx, builder in enumerate(slide_builders, start=1):
        print(f"  --> Building Slide {idx:02d} of 25: {builder.__name__}...")
        builder(prs)

    # Save to all target paths
    targets = [
        REPO_ROOT / "CuraCascade_Presentation_V2_25Slides.pptx",
        REPO_ROOT / "docs" / "CuraCascade_Presentation_V2_25Slides.pptx",
        REPO_ROOT / "CuraCascade_Presentation_Redesigned.pptx",
        REPO_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.pptx",
    ]

    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
        print(f"✅ Saved PPTX ({target.stat().st_size:,} bytes) to:\n   {target}")

    print("\n🎉 REMAKE COMPLETED SUCCESSFULLY! All 25 slides generated cleanly.")


if __name__ == "__main__":
    remake_presentation()
