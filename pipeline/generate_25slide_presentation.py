"""CuraCascade V2 — Master 25-Slide Academic Defense Presentation Generator.

Generates a submission-grade 25-slide PowerPoint deck following IEEE / university project
review standards with:
- 16:9 Widescreen layout.
- Academic Dark Navy aesthetic (#071426) with Teal (#36D6C5) and Cyan (#55B9FF) accents.
- Native OpenXML fade transitions on every slide.
- Sequential click-animations for multi-card reveals.
- Genuine application screenshots and architecture diagrams embedded natively.
- 1,200+ characters of structured speaker notes per slide (Script, Concept, Takeaway, Guardrail, Viva Q&A).
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
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt

# ==============================================================================
# Theme & Color Palette (Dark Space Navy Aesthetic)
# ==============================================================================

BG_DARK = RGBColor(7, 20, 38)          # Deep Space Navy (#071426)
SURFACE_NAVY = RGBColor(13, 31, 56)    # Elevated Surface (#0D1F38)
SURFACE_CARD_ALT = RGBColor(18, 42, 74)# Secondary Card Surface (#122A4A)
SURFACE_BORDER = RGBColor(26, 54, 93)  # Subtle Structural Border (#1A365D)

TEXT_WHITE = RGBColor(241, 245, 249)   # Primary Header / Text (#F1F5F9)
TEXT_MUTED = RGBColor(148, 163, 184)   # Slate Secondary Text (#94A3B8)
TEXT_DIM = RGBColor(100, 116, 139)     # Dim Metadata Text (#64748B)

TEAL_PRIMARY = RGBColor(54, 214, 197)  # Electric Teal (#36D6C5)
CYAN_ACCENT = RGBColor(85, 185, 255)   # Sky Cyan (#55B9FF)
PURPLE_ACCENT = RGBColor(168, 85, 247) # Royal Purple (#A855F7)
ALERT_GREEN = RGBColor(16, 185, 129)   # Success Emerald (#10B981)
ALERT_AMBER = RGBColor(245, 158, 11)   # Warning Amber (#F59E0B)
ALERT_RED = RGBColor(239, 68, 68)      # Critical Alert Red (#EF4444)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / "docs" / "figures"
SCREENSHOT_DIR = FIG_DIR / "screenshots"


# ==============================================================================
# OpenXML Native Animation & Transition Utilities
# ==============================================================================

def add_slide_fade_transition(slide):
    """Inject native OpenXML fade transition into slide properties."""
    fade_xml = parse_xml(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
        '  <p:fade/>'
        '</p:transition>'
    )
    slide._element.insert(0, fade_xml)


def add_sequential_animations(slide, shape_ids: list[int]):
    """Inject native OpenXML sequential click-advance animations for shape IDs."""
    if not shape_ids:
        return

    nodes_xml = ""
    for i, sid in enumerate(shape_ids):
        delay = 0 if i == 0 else 500
        nodes_xml += f"""
        <p:cTn id="{100 + i}" dur="500" fill="hold" nodeType="clickEffect">
          <p:stCondLst>
            <p:cond delay="{delay}"/>
          </p:stCondLst>
          <p:childTnLst>
            <p:set>
              <p:cBhvr>
                <p:cTn id="{200 + i}" dur="1" fill="hold"/>
                <p:tgtEl>
                  <p:spTgt spid="{sid}"/>
                </p:tgtEl>
                <p:attrNameLst>
                  <p:attrName>style.visibility</p:attrName>
                </p:attrNameLst>
              </p:cBhvr>
              <p:to>
                <p:strVal val="visible"/>
              </p:to>
            </p:set>
            <p:anim effect="fade" to="1.0">
              <p:cBhvr>
                <p:cTn id="{300 + i}" dur="500" fill="hold"/>
                <p:tgtEl>
                  <p:spTgt spid="{sid}"/>
                </p:tgtEl>
              </p:cBhvr>
            </p:anim>
          </p:childTnLst>
        </p:cTn>
        """

    timing_xml = parse_xml(f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="always" nodeType="timingRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    {nodes_xml}
                  </p:childTnLst>
                </p:cTn>
                <p:prevCondLst>
                  <p:cond evt="onPrev" delay="0">
                    <p:tgtEl>
                      <p:spTgt spid="2"/>
                    </p:tgtEl>
                  </p:cond>
                </p:prevCondLst>
                <p:nextCondLst>
                  <p:cond evt="onNext" delay="0">
                    <p:tgtEl>
                      <p:spTgt spid="2"/>
                    </p:tgtEl>
                  </p:cond>
                </p:nextCondLst>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
    </p:timing>
    """)
    slide._element.append(timing_xml)


# ==============================================================================
# UI Component Builder Helpers
# ==============================================================================

def set_slide_background(slide, color: RGBColor):
    """Set uniform solid background color for slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, tag: str, title: str, subtitle: str):
    """Create standardized structured top header banner."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_tag = tf.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = TEAL_PRIMARY

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(2)

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(3)


def add_card(slide, left: float, top: float, width: float, height: float,
             bg_color: RGBColor = SURFACE_NAVY, border_color: RGBColor = SURFACE_BORDER):
    """Add elevated rounded rectangle card container."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape


def add_footer(slide, slide_num: int, total_slides: int = 25):
    """Add subtle professional bottom footer with pagination."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
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


# ==============================================================================
# Slide 1: Title & Academic Identity
# ==============================================================================

def build_slide_1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    hero_card = add_card(slide, 0.8, 0.8, 11.733, 5.85, SURFACE_NAVY, SURFACE_BORDER)

    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = TEAL_PRIMARY
    accent_bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ACADEMIC DEFENSE & TECHNICAL EVALUATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf.add_paragraph()
    p.text = "CuraCascade V2: Automated Discrepancy Auditing & Evidence Synchronization Across Clinical Genomics Databases"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(8)

    p = tf.add_paragraph()
    p.text = "A 5-stage deterministic framework closing the multi-year evidence propagation lag between authoritative ClinGen gene downgrades and downstream ClinVar variant assertions & PanelApp diagnostic panels."
    p.font.size = Pt(13)
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(10)

    p = tf.add_paragraph()
    p.text = "────────────────────────────────────────────────────────────────────────────"
    p.font.size = Pt(9)
    p.font.color.rgb = SURFACE_BORDER
    p.space_before = Pt(12)

    p = tf.add_paragraph()
    p.text = "Student Author: Udit Shokeen  |  Register No: 23BCB0001"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(10)

    p = tf.add_paragraph()
    p.text = "School of Computer Science & Engineering  |  Vellore Institute of Technology (VIT), Vellore, India"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(2)

    p = tf.add_paragraph()
    p.text = "Live Web Application: curacascadev2.streamlit.app   •   Code Repository: github.com/uditshokeen14/curacascadeV2"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(10)

    add_footer(slide, 1)

    set_speaker_notes(slide, {
        "script": "Good morning, respected members of the evaluation committee. My name is Udit Shokeen, registration number 23BCB0001 from the School of Computer Science and Engineering at VIT Vellore. Today, I am defending my project: CuraCascade Version 2. This project addresses a critical, under-recognized problem in clinical bioinformatics: when authoritative expert panels downgrade historical candidate genes because they were disproven, downstream variant archives like ClinVar and diagnostic gene panels like PanelApp fail to synchronize automatically. CuraCascade is a deterministic 5-stage software engine that detects, categorizes, and audits these discrepancies before they cause patient harm.",
        "concept": "Clinical genomics is the medical science of sequencing a patient's DNA to diagnose inherited diseases like cancer or cardiac arrest. When researchers discover that an old gene was blamed by mistake, other hospital databases do not update automatically.",
        "takeaway": "CuraCascade bridges the multi-year disconnect between upstream scientific consensus and downstream diagnostic testing.",
        "guardrail": "Do not claim that CuraCascade is an AI doctor or an autonomous diagnostic tool. It is a quality-assurance data synchronization platform for clinical laboratories.",
        "question": "In simple terms, what does CuraCascade actually do?",
        "answer": "It automatically cross-references authoritative expert gene evaluations against active variant databases and hospital diagnostic panels, alerting laboratory geneticists when a test is still reporting a mutation in a gene that has already been disproven."
    })


# ==============================================================================
# Slide 2: Executive Summary
# ==============================================================================

def build_slide_2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "01 // EXECUTIVE SUMMARY",
        "Executive Summary: Problem, Solution & Verified Outcomes",
        "A high-level synthesis of the clinical challenge, software solution, and empirical validation."
    )

    cards_data = [
        ("THE PROBLEM", ALERT_RED,
         "Evidence Synchronization Disconnect",
         "When ClinGen downgrades a gene from causal to Disputed, Refuted, or Limited, downstream ClinVar variants and PanelApp panels do not automatically update.\n\nStale Pathogenic assertions persist for an overall median of 2.82 years (up to 9.9 years), generating false-positive diagnoses and unwarranted invasive clinical interventions."),
        ("THE SOLUTION", TEAL_PRIMARY,
         "Deterministic 5-Stage Audit Pipeline",
         "CuraCascade ingests multi-source data, normalizes disparate disease ontologies via a 3-tier MONDO-to-MedGen crosswalk, and stores data in a 3NF SQLite warehouse + DuckDB OLAP engine.\n\nMaterializes Class A, B, and C discrepancies with actionable prescriptive clinical remediation directives."),
        ("STRONGEST VERIFIED RESULT", ALERT_GREEN,
         "100.0% Precision Across 94 Benchmark Cases",
         "Evaluated on a 100-gene independent expert adjudication benchmark (94 evaluable cases):\n\n• Zero False Positives (100.0% PPV, 95% CI: [82.4%, 100.0%]).\n• Zero false alarms on 42 definitive clinical controls.\n• Scaled to Full Corpus: 51,251 findings across 3,033 genes and 51,025 ClinVar variants."),
        ("BIGGEST HONEST LIMITATION", ALERT_AMBER,
         "34.6% Recall & Static Data Snapshots",
         "The benchmark recall is 34.6% (18/52 detected). This reflects an intentional clinical priority: avoiding alert fatigue via conservative disease matching.\n\nAuditing the 34 false negatives proves that 47% were absent from the local snapshot, and 41% were conservative phenotypic exclusions."),
    ]

    cards = []
    w = 2.76
    gap = 0.23
    for i, (tag, col, title, desc) in enumerate(cards_data):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 2)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 2 gives you the executive summary of the entire project. The core problem is asynchronous database propagation: when ClinGen downgrades a gene, stale pathogenic assertions linger downstream for a median of 2.82 years. Our solution is a deterministic 5-stage automated audit pipeline linking ClinGen, ClinVar, and PanelApp through disease-aware ontology crosswalks. Our strongest verified outcome is 100% precision: in our 94-gene evaluable benchmark, every single flagged finding was a genuine clinical discrepancy, with zero false alarms raised against definitive ACMG controls. Our primary honest limitation is 34.6% recall, which we will dissect in detail later.",
        "concept": "Executive summary is the 'elevator pitch'. In one slide, examiners see the problem, the solution, the best metric, and the biggest limitation, establishing complete academic honesty upfront.",
        "takeaway": "CuraCascade achieves 100% precision with zero false alarms, accepting moderate recall (34.6%) to prevent dangerous clinical alert fatigue.",
        "guardrail": "Never hide the 34.6% recall. Put it right on Slide 2 as a badge of scientific transparency.",
        "question": "Why did you prioritize precision over recall?",
        "answer": "In hospital bioinformatics, false-positive alerts cause severe alert fatigue. If an algorithm flags hundreds of harmless variants, clinical geneticists will turn it off. We prioritized 100% precision so that every alert warrants immediate action."
    })


# ==============================================================================
# Slide 3: The Real-World Problem
# ==============================================================================

def build_slide_3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "02 // THE CLINICAL CHALLENGE",
        "The Evidence-to-Practice Gap in Clinical Genomics",
        "Authoritative gene downgrades fail to propagate to diagnostic databases, risking patient harm."
    )

    # 3 Strategic Cards
    c1 = add_card(slide, 0.8, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(3.25), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. SCIENTIFIC RE-APPRAISAL"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "In early candidate-gene literature, small sample sizes and lack of population controls led researchers to falsely associate genes with severe diseases.\n\nToday, expert consortia like the Clinical Genome Resource (ClinGen) systematically re-evaluate validity, downgrading candidate genes to Disputed, Refuted, or Limited (e.g., SCN1B, MYLK2, KCNE2)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c2 = add_card(slide, 4.84, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(5.04), Inches(2.05), Inches(3.25), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. ASYNCHRONOUS DRIFT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER

    p = tf2.add_paragraph()
    p.text = "Downstream databases operate under independent governance with no automated synchronization:\n\n• NCBI ClinVar: Archival repository; does not re-classify or delete variants when upstream genes are refuted.\n• Genomics England PanelApp: Diagnostic gene panels lag behind published expert consensus.\n\nResult: 51,251 unpropagated discrepancies in our warehouse snapshot."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c3 = add_card(slide, 8.88, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb3 = slide.shapes.add_textbox(Inches(9.08), Inches(2.05), Inches(3.25), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "3. TANGIBLE PATIENT HARM"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    p = tf3.add_paragraph()
    p.text = "When diagnostic laboratories rely on stale assertions, real patients suffer severe clinical harms:\n\n• False-Positive Diagnoses: Healthy individuals labeled as harboring lethal cardiac or cancer risks.\n• Invasive Surgeries: Unnecessary implantable defibrillator (ICD) placements or prophylactic organ resections.\n• Trauma in Families: Inappropriate cascade testing of at-risk children and relatives."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    add_footer(slide, 3)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id, c3.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 3 illustrates why this problem is urgent. Scientific truth evolves: in the early 2000s, genes like SCN1B were published as causal for Brugada syndrome. Decades later, ClinGen re-evaluated the evidence with modern population data and refuted the association. But because NCBI ClinVar is an archive rather than an active evaluator, 18 ClinVar variants remain labeled Pathogenic. If an asymptomatic 25-year-old takes a genetic test and the lab blindly copies ClinVar's classification, that patient could be recommended for an unnecessary, painful ICD heart surgery. That is the evidence-to-practice gap.",
        "concept": "Cascade testing means testing a patient's entire family once a 'mutation' is found. If the original mutation was in a disproven gene, the whole family is subjected to needless anxiety and invasive medical procedures.",
        "takeaway": "Stale genomic assertions are not just data errors; they lead directly to inappropriate invasive surgeries and psychological trauma.",
        "guardrail": "Do not claim that CuraCascade investigated specific hospital patients. We audited public database records against published clinical literature.",
        "question": "Why don't testing labs notice that ClinGen refuted the gene?",
        "answer": "Clinical testing laboratories process thousands of exomes a week. Variant curation teams rely heavily on automated pipeline annotations from ClinVar. Without an automated cross-database audit tool, tracking thousands of ClinGen expert updates manually is impossible."
    })


# ==============================================================================
# Slide 4: Biomedical Foundations I
# ==============================================================================

def build_slide_4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "03 // BIOMEDICAL FOUNDATIONS",
        "Biomedical Foundations I: DNA, Genes, Variants & Proteins",
        "Understanding how genetic variation causes human disease from first principles."
    )

    concepts = [
        ("DNA & CHROMOSOMES", "The Biological Library", TEAL_PRIMARY,
         "• DNA is a chemical double-helix encoded by four chemical bases: A, C, G, and T.\n• Human cells package DNA into 23 pairs of chromosomes (46 total).\n• Think of chromosomes as large reference volumes containing recipes for life."),
        ("GENES & PROTEINS", "The Molecular Machines", CYAN_ACCENT,
         "• A gene is a specific sequence of DNA bases that provides instructions to build a protein.\n• Humans have ~20,000 protein-coding genes.\n• Proteins perform cellular work: building muscle fibers (MYH7), conducting cardiac electrical currents (SCN5A), or repairing DNA (BRCA1)."),
        ("GENETIC VARIANTS", "Typographical Alterations", ALERT_AMBER,
         "• A variant is an alteration in the normal DNA sequence (a typo in the recipe).\n• Benign Variants: Harmless natural diversity found in healthy individuals.\n• Pathogenic Variants: Damaging alterations that disrupt protein structure, causing disease (e.g. missense, nonsense, frameshift mutations)."),
        ("ALLELE FREQUENCY & MCAF", "The Population Ceiling", ALERT_GREEN,
         "• Allele Frequency (AF): Percentage of people carrying a variant in healthy reference cohorts (gnomAD).\n• Whiffin et al. Framework: If a lethal condition occurs in 1 in 10,000 people, a variant present in 1% of healthy adults CANNOT be causal.\n• Establishes Maximum Credible Allele Frequency (MCAF)."),
    ]

    cards = []
    w = 2.76
    gap = 0.23
    for i, (tag, role, col, text) in enumerate(concepts):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = role
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 4)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 4 establishes the biological foundations of our project. Think of a human cell as a library: DNA is the alphabet, a gene is a recipe, and a protein is the finished dish. If there is a typo in a gene recipe—what we call a genetic variant—the protein might fail to work, leading to disease. However, not all typos are harmful; millions of variants are completely benign. To distinguish harmful mutations from normal variation, geneticists rely on population databases like gnomAD. Using the ACMG/Whiffin quantitative framework, if a mutation occurs at a frequency higher than the disease prevalence in healthy populations, that variant is mathematically refuted as benign.",
        "concept": "MCAF stands for Maximum Credible Allele Frequency. It is a mathematical ceiling: if a mutation is more common than the disease itself, it cannot be causing the disease.",
        "takeaway": "Variants in DNA are typos; benign ones are harmless, while pathogenic ones break proteins. High population frequency mathematically disproves disease causality.",
        "guardrail": "Do not confuse genes with variants. A gene is the entire book; a variant is a single typo on a single page.",
        "question": "What is the gnomAD database and how does CuraCascade use it?",
        "answer": "gnomAD is the Genome Aggregation Database, containing sequencing data from hundreds of thousands of healthy individuals across diverse ancestries. CuraCascade uses gnomAD allele frequencies to test whether variants submitted as Pathogenic occur at implausibly high population rates exceeding MCAF thresholds."
    })


# ==============================================================================
# Slide 5: Biomedical Foundations II
# ==============================================================================

def build_slide_5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "04 // BIOMEDICAL FOUNDATIONS",
        "Biomedical Foundations II: Gene Validity vs. Variant Pathogenicity",
        "Crucial distinction: evaluating whether a gene causes disease vs. whether a mutation breaks a gene."
    )

    # 2 Comparison Columns
    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. GENE-LEVEL CLINICAL VALIDITY (CLINGEN)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "Evaluates the fundamental biological relationship: Does variation in Gene X cause Disease Y?"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    clingen_tiers = [
        ("Definitive", "Overwhelming human genetic & experimental replication."),
        ("Strong", "Substantial genetic evidence; pending additional families."),
        ("Moderate", "Preliminary evidence; biologically plausible."),
        ("Limited", "Weak evidence; 1–2 isolated case reports without replication."),
        ("Disputed", "Conflicting evidence; subsequent studies fail to reproduce link."),
        ("Refuted", "Disproven! Robust case-control studies rule out causality."),
    ]
    for tier, desc in clingen_tiers:
        p = tf1.add_paragraph()
        p.text = f"• {tier}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = ALERT_GREEN if tier in ["Definitive", "Strong"] else (ALERT_AMBER if tier == "Limited" else ALERT_RED)
        p.space_before = Pt(3)

    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. VARIANT-LEVEL PATHOGENICITY (CLINVAR / ACMG)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf2.add_paragraph()
    p.text = "Evaluates a specific typographical change in a gene: Does this particular mutation impair protein function?"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    acmg_tiers = [
        ("Pathogenic (P)", "Proven causal mutation; alters critical protein domains."),
        ("Likely Pathogenic (LP)", ">90% probability of being disease-causing."),
        ("Variant of Uncertain Significance (VUS)", "Unknown clinical effect; insufficient data to classify."),
        ("Likely Benign (LB)", ">90% probability of being harmless neutral variation."),
        ("Benign (B)", "Proven harmless; occurs frequently in healthy populations."),
    ]
    for tier, desc in acmg_tiers:
        p = tf2.add_paragraph()
        p.text = f"• {tier}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = ALERT_RED if "Pathogenic" in tier else (ALERT_AMBER if "Uncertain" in tier else ALERT_GREEN)
        p.space_before = Pt(3)

    p = tf2.add_paragraph()
    p.text = "THE LOGICAL DEPENDENCY TRAP:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER
    p.space_before = Pt(8)

    p = tf2.add_paragraph()
    p.text = "Variant pathogenicity is conditionally predicated on gene validity. If a gene is Disputed or Refuted for a disease, NO variant within that gene can legitimately be classified as Pathogenic for that disease!"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(2)

    add_footer(slide, 5)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 5 clarifies the most vital scientific distinction in the entire presentation: Gene-level validity versus Variant-level pathogenicity. ClinGen operates at the gene level—asking 'Does gene X cause disease Y?' ClinVar operates at the variant level—asking 'Does this specific mutation break gene X?' Here is the logical trap: variant pathogenicity depends on gene validity. If an expert panel refutes gene X, then by definition, no mutation in that gene can be labeled Pathogenic for that disease! Yet because ClinVar preserves historical assertions, thousands of variants remain labeled Pathogenic. CuraCascade detects this exact contradiction.",
        "concept": "If a car model is proven to never explode, you cannot claim that a specific scratch on the door caused the explosion. If the gene doesn't cause the disease, mutations in that gene cannot cause the disease.",
        "takeaway": "Variant pathogenicity logically depends on gene validity; when ClinGen refutes a gene, downstream Pathogenic assertions become scientifically invalid.",
        "guardrail": "Never say that variants become non-existent. The variants still exist in patients' DNA, but their clinical label must be capped at VUS or downgraded.",
        "question": "Can a gene be Disputed for one disease but Definitive for another?",
        "answer": "Yes! This is called pleiotropy. For example, ACTN2 is Disputed for Hypertrophic Cardiomyopathy, but Definitive for Distal Myopathy. That is why simple gene-name matching fails and CuraCascade enforces disease-aware matching."
    })


# ==============================================================================
# Slide 6: The Data Ecosystem
# ==============================================================================

def build_slide_6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "05 // DATA ECOSYSTEM",
        "The Fragmented Clinical Genomics Data Ecosystem",
        "Multiple authoritative databases operating on different granularities, ontologies, and cadences."
    )

    sources = [
        ("ClinGen", "Expert Consensus Panels", TEAL_PRIMARY,
         "• Unit: Gene–Disease Dyad (G, D)\n• Ontology: MONDO Disease Ontology\n• Curates: 6 Clinical Validity Tiers\n• Cadence: Multi-year expert panel reviews\n• Limitation: Does not curate variant-level submissions directly."),
        ("NCBI ClinVar", "Variant Assertion Archive", CYAN_ACCENT,
         "• Unit: Allelic Variant (G, V)\n• Ontology: MedGen, OMIM, Free-Text\n• Curates: ACMG 5-Tier Pathogenicity\n• Cadence: Continuous voluntary lab deposits\n• Limitation: Archival; does not re-curate when gene validity shifts."),
        ("PanelApp", "Diagnostic Test Menus", PURPLE_ACCENT,
         "• Unit: Gene Panel Membership (G, P)\n• Ontology: Clinical Indication Codes\n• Curates: Green, Amber, Red Tiers\n• Cadence: Periodic reviews for NHS test directories\n• Limitation: Bed files lag upstream ClinGen determinations."),
        ("gnomAD", "Population Reference", ALERT_GREEN,
         "• Unit: Allele Frequency (AF)\n• Ontology: Continental Ancestries (v4)\n• Curates: Quantitative frequencies in 800k+ individuals\n• Cadence: Multi-year major reference drops\n• Limitation: Lacks clinical disease phenotypes."),
    ]

    cards = []
    w = 2.76
    gap = 0.23
    for i, (name, role, col, text) in enumerate(sources):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name.upper()
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = role
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

        div_mini = tf.add_paragraph()
        div_mini.text = "─────────────────────"
        div_mini.font.size = Pt(8)
        div_mini.font.color.rgb = SURFACE_BORDER
        div_mini.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

    add_footer(slide, 6)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 6 breaks down the four core data resources analyzed by CuraCascade. Notice the fundamental differences: ClinGen curates gene-disease validity using the MONDO disease ontology. ClinVar curates variant assertions using MedGen and OMIM identifiers. PanelApp curates diagnostic gene lists using NHS clinical indication codes. And gnomAD provides raw allele frequencies across continental ancestry groups. None of these four systems share a common primary key or an automated API webhook to synchronize updates. They are completely siloed.",
        "concept": "A data silo is a database that is isolated from others. Because each organization uses different disease terms and update schedules, they cannot synchronize automatically.",
        "takeaway": "Clinical genomics databases operate at different granularities and ontologies without automated cross-database synchronization.",
        "guardrail": "Do not criticize these databases as poorly managed; they were built by different international agencies for different purposes.",
        "question": "What is the MONDO disease ontology?",
        "answer": "MONDO (Monarch Disease Ontology) is an open-source semi-automated ontology that harmonizes disease definitions across OMIM, Orphanet, MedGen, and ICD-10 into unified semantic concepts."
    })


# ==============================================================================
# Slide 7: Why Evidence Can Disagree
# ==============================================================================

def build_slide_7(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "06 // ROOT CAUSE ANALYSIS",
        "Why Clinical Evidence Disagrees: Four Structural Barriers",
        "Analyzing the semantic, organizational, and temporal reasons discrepancies persist."
    )

    barriers = [
        ("1. GRANULARITY MISMATCH", TEAL_PRIMARY,
         "Gene-Level vs. Variant-Level Silos",
         "ClinGen evaluates the gene entity (G). ClinVar tracks the variant entity (V). PanelApp tracks gene panels (P).\n\nWithout a relational bridge connecting variant records to gene validity determinations, updates at the gene level remain invisible to variant pipelines."),
        ("2. ONTOLOGICAL DIVERGENCE", CYAN_ACCENT,
         "Vocabulary & Synonym Discordance",
         "A disease in ClinGen may be recorded as 'Hypertrophic cardiomyopathy 1' (MONDO:0005045), while ClinVar labels variants as 'Familial hypertrophic cardiomyopathy' (MedGen:C0007194) or simply 'Cardiovascular phenotype'.\n\nDirect string matching fails across >60% of entries."),
        ("3. ASYNCHRONOUS CADENCE", ALERT_AMBER,
         "Multi-Year Update Lags",
         "ClinGen expert curation panels meet periodically to review specific disease domains (e.g. Arrhythmia GCEP in 2021, Cardiomyopathy in 2024).\n\nCommercial diagnostic laboratories lack dedicated staff to manually re-curate historical variant submissions, leaving stale assertions active for years."),
        ("4. MISSING ASSERTIONS", ALERT_RED,
         "Data Availability Gaps",
         "Many downgraded genes lack variant submissions in public archives because commercial labs treat internal testing data as proprietary.\n\nIn our benchmark audit, 47% of false negatives occurred simply because the local database snapshot contained zero variant records for that gene."),
    ]

    cards = []
    w = 2.76
    gap = 0.23
    for i, (tag, col, title, desc) in enumerate(barriers):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 7)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 7 addresses the root cause: why does evidence disagree in the real world? There are four structural barriers. First, granularity mismatch: gene-level validity and variant-level pathogenicity are stored in separate databases. Second, ontological divergence: different databases use different names for the same disease. Third, asynchronous cadence: expert panels publish updates, but diagnostic labs don't have the bandwidth to manually review decades of old submissions. And fourth, missing data: many testing labs keep their variant records in proprietary internal silos rather than depositing them in public archives.",
        "concept": "Ontological divergence is like one doctor writing 'heart attack' while another writes 'myocardial infarction' and a database treating them as two completely different diseases.",
        "takeaway": "Evidence disagreement is caused by structural barriers: granularity differences, vocabulary divergence, asynchronous update cadences, and proprietary data gaps.",
        "guardrail": "Do not claim that CuraCascade solves the proprietary data gap; an algorithm can only audit data that is publicly accessible.",
        "question": "How does CuraCascade solve ontological divergence?",
        "answer": "Through a curated MONDO-to-MedGen disease concept crosswalk and normalized synonym matching that maps diverse disease strings into unified semantic clusters."
    })


# ==============================================================================
# Slide 8: Existing Workflows & Research Gap
# ==============================================================================

def build_slide_8(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "07 // RESEARCH GAP",
        "Existing Workflows vs. CuraCascade: The Automated Audit Gap",
        "Comparing manual clinical curation against CuraCascade's automated cross-layer architecture."
    )

    # Left: Existing Manual Workflow
    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "EXISTING CLINICAL WORKFLOWS (MANUAL & SILOED)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER

    p = tf1.add_paragraph()
    p.text = "How clinical laboratories currently handle evidence updates:"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    manual_steps = [
        ("Ad-Hoc Manual Checking", "Geneticists manually look up genes on ClinGen website when a suspicious report is questioned."),
        ("Static Commercial VCF Annotations", "Pipelines annotate variants using static ClinVar VCF drops, inheriting stale classifications without validity validation."),
        ("Gene-Only Lookup Traps", "Simple lookup scripts flag all variants in a downgraded gene, generating false alarms on pleiotropic multi-disease genes."),
        ("No Systematic Remediation", "Laboratories lack automated tools to export formal clinical governance dossiers (.md) citing ClinGen GCEP determination reports."),
    ]
    for title, desc in manual_steps:
        p = tf1.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

    # Right: CuraCascade Automated Approach
    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "THE CURACASCADE AUTOMATED ARCHITECTURE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf2.add_paragraph()
    p.text = "How CuraCascade transforms evidence auditing:"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    curacascade_steps = [
        ("Automated Multi-Source Join", "Relational integration linking ClinGen validity to ClinVar variants, PanelApp tiers, and gnomAD frequencies."),
        ("Disease-Aware Ontology Crosswalk", "Harmonizes MONDO and MedGen IDs; suppresses false alarms for distinct diseases in multi-disease genes."),
        ("Quantitative Population Refutation", "Automatically computes MCAF thresholds to identify variants occurring at implausibly high frequencies in healthy cohorts."),
        ("ISO 15189 Clinical Dossiers", "Generates structured clinical governance audit dossiers with explicit submitter and panel remediation directives."),
    ]
    for title, desc in curacascade_steps:
        p = tf2.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(4)

    add_footer(slide, 8)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 8 highlights the research gap. Today, clinical genetic testing labs rely on ad-hoc manual checking or static ClinVar VCF downloads that blindly inherit stale assertions. If a lab tries to write a simple script to match gene names, they fall into the pleiotropy trap—flagging valid muscular dystrophy variants in ACTN2 because ACTN2 was disputed for cardiomyopathy! CuraCascade fills this gap by providing an automated, disease-aware relational join that links gene validity, variant assertions, panel tiers, and population frequencies, generating actionable clinical governance dossiers.",
        "concept": "VCF stands for Variant Call Format, the standard text file used in bioinformatics to store a patient's genetic mutations. Most labs just match VCFs to ClinVar without checking if the gene is still valid.",
        "takeaway": "CuraCascade replaces error-prone manual cross-referencing with an automated, disease-aware cross-database audit engine.",
        "guardrail": "Do not claim that no other software can query ClinVar. Other tools query ClinVar, but they do not perform disease-aware consistency joins against ClinGen validity determinations.",
        "question": "What is the biggest limitation of existing commercial variant annotation tools?",
        "answer": "Commercial annotators like ANNOVAR or VEP annotate variant consequences, but they assume the underlying gene-disease validity is sound. They do not cross-reference ClinGen GCEP downgrades to verify whether the gene should even be on the diagnostic panel."
    })


# ==============================================================================
# Slide 9: Project Objectives & Scope
# ==============================================================================

def build_slide_9(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "08 // OBJECTIVES & SCOPE",
        "Project Scope, Objectives & Operational Boundaries",
        "Clear demarcation of engineering goals, target user personas, and strict non-goals."
    )

    # 3 Strategic Columns
    c1 = add_card(slide, 0.8, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(3.25), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. CORE ENGINEERING OBJECTIVES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "• Ingest & Harmonize: Multi-source ETL pipelines for ClinGen, ClinVar, PanelApp, and gnomAD.\n\n• Disease-Aware Auditing: Materialize Class A, B, and C discrepancies using ontology crosswalks.\n\n• Population Genetics Filter: Evaluate variant frequencies against Whiffin et al. MCAF thresholds.\n\n• Clinical Decision Support: Deliver interactive Streamlit web dashboard and headless CLI (run.py)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c2 = add_card(slide, 4.84, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(5.04), Inches(2.05), Inches(3.25), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. INTENDED USER PERSONAS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf2.add_paragraph()
    p.text = "• Clinical Laboratory Geneticists: Reviewing variant lists prior to signing out diagnostic reports.\n\n• Diagnostic Panel Curators: Updating hospital gene test directories and exome filtering BED files.\n\n• Quality Assurance Auditors: Reviewing historical laboratory assertion archives for re-curation triage.\n\n• Biomedical Researchers: Investigating evidence propagation kinetics across clinical corpora."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c3 = add_card(slide, 8.88, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb3 = slide.shapes.add_textbox(Inches(9.08), Inches(2.05), Inches(3.25), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "3. STRICT OPERATIONAL BOUNDARIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    p = tf3.add_paragraph()
    p.text = "WHAT CURACASCADE IS NOT:\n\n• NOT an Autonomous Diagnostic Device: It does not diagnose patients or make independent clinical decisions.\n\n• NOT a Black-Box AI: Audit classifications are deterministic, rule-based, and evidence-linked.\n\n• NOT Clinically Validated: No prospective human clinical trials or FDA clearances are claimed.\n\n• Decision Support Only: Triage tool assisting human clinical experts."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)

    add_footer(slide, 9)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id, c3.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 9 defines our project scope and boundaries. Our objectives are to build a deterministic, reproducible audit pipeline, evaluate population frequencies against MCAF ceilings, and deliver an interactive decision-support interface. Our intended users are laboratory geneticists, panel curators, and hospital QA auditors. Crucially, look at column 3: we explicitly state what CuraCascade is NOT. It is NOT an autonomous diagnostic tool, NOT an uninterpretable black-box AI, and NOT a cleared medical device. It is a secondary quality-assurance audit tool that assists human geneticists.",
        "concept": "A 'non-goal' is an explicit statement of what a software system is NOT designed to do. Defining non-goals is a hallmark of professional software engineering and prevents examiners from attacking out-of-scope areas.",
        "takeaway": "CuraCascade is a deterministic decision-support and quality-assurance audit tool for clinical laboratories, not an autonomous diagnostic device.",
        "guardrail": "Never claim FDA clearance, IVDR compliance, or clinical trial validation.",
        "question": "Who is the primary user who clicks buttons in your web app?",
        "answer": "A clinical laboratory geneticist or panel curator who is preparing or auditing a diagnostic gene panel and needs to verify whether any included genes harbor stale assertions."
    })


# ==============================================================================
# Slide 10: Contributions & Research Questions
# ==============================================================================

def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "09 // CONTRIBUTIONS",
        "Key Research Questions & Genuine Project Contributions",
        "Defining the scientific questions answered and the tangible engineering deliverables."
    )

    questions = [
        ("RESEARCH QUESTION 1", TEAL_PRIMARY,
         "How widespread are unpropagated gene downgrades in public archives?",
         "• Contribution: Quantified evidence propagation latency across 51,025 ClinVar assertions, revealing an overall median lag of 2.82 years (1,030 days) and 182,760 cumulative patient-years at risk.\n• Proved that Class B limited-evidence genes linger significantly longer than Class A (3.77 vs 2.80 yrs, p < 0.001)."),
        ("RESEARCH QUESTION 2", CYAN_ACCENT,
         "Can automated cross-layer joins detect discrepancies without alert fatigue?",
         "• Contribution: Designed a 3-tier disease-aware matching heuristic using MONDO-MedGen crosswalks and keyword exclusion guards.\n• Validated on a 100-gene independent benchmark: achieved 100.0% precision (18/18 TP, zero false alarms) on evaluable cases, completely ruling out 42 definitive controls."),
        ("RESEARCH QUESTION 3", ALERT_GREEN,
         "Can population allele frequencies independently refute stale assertions?",
         "• Contribution: Integrated gnomAD v4 continental allele frequencies with Whiffin et al. MCAF formulations across Orphanet prevalence estimates.\n• Demonstrated that 89.3% of audited Class A variants in downgraded genes exceed the MCAF pathogenic ceiling (e.g., KCNE2 175x excess)."),
        ("RESEARCH QUESTION 4", PURPLE_ACCENT,
         "Can machine learning prioritize currently supported genes for re-appraisal?",
         "• Contribution: Trained an exploratory Balanced Random Forest across 7 engineered features, achieving an AUROC of 0.857 and Brier score of 0.1508.\n• Identified Curation Age Elapsed (78.4% perm. wt) as the primary risk driver while transparently disclosing retrospective temporal leakage limits."),
    ]

    cards = []
    w = 5.7
    h = 2.35
    positions = [(0.8, 1.85), (6.8, 1.85), (0.8, 4.35), (6.8, 4.35)]

    for i, ((rq, col, q_text, ans_text), (left, top)) in enumerate(zip(questions, positions)):
        c = add_card(slide, left, top, w, h, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(0.05))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(w - 0.3), Inches(h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = rq
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = q_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = ans_text
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)

    add_footer(slide, 10)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 10 summarizes our four core research questions and genuine contributions. First, we quantified the propagation gap across 51,000 ClinVar assertions, proving a 2.82-year median lag. Second, we designed a disease-aware ontology matching algorithm that achieved 100% precision on our independent benchmark. Third, we integrated gnomAD population genetics, showing that 89.3% of audited variants in downgraded genes exceed the mathematical ceiling of disease plausibility. And fourth, we explored machine learning triage, achieving an AUROC of 0.857 while honestly disclosing its retrospective limitations.",
        "concept": "A research question defines the scientific inquiry. The contribution is the verified factual answer produced by the software and data analysis.",
        "takeaway": "CuraCascade answers four key research questions: quantifying latency (2.82 yrs), proving precision (100%), validating population refutation (89.3%), and testing ML triage (AUROC 0.857).",
        "guardrail": "Do not claim that the ML model is prospective clinical prediction; it is an exploratory retrospective triage experiment.",
        "question": "What is the most unique contribution of this project compared to other student projects?",
        "answer": "The disease-aware ontology crosswalk that prevents pleiotropic false alarms, and the quantitative population genetics evaluation using gnomAD v4 and MCAF thresholds to independently refute stale variant assertions."
    })


# ==============================================================================
# Slide 11: End-to-End Workflow Pipeline
# ==============================================================================

def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "10 // PIPELINE ARCHITECTURE",
        "Deterministic 5-Stage Cross-Layer Audit Pipeline",
        "End-to-end automated framework ingesting, harmonizing, auditing, and triaging genomic discrepancies."
    )

    pipeline_steps = [
        ("STAGE 01", "Multi-Source Ingestion", TEAL_PRIMARY,
         "Automated ETL fetchers pull raw ClinGen GCEP curations, ClinVar variant drops, PanelApp panel APIs, and gnomAD v4 frequencies with cryptographic SHA-256 provenance logging."),
        ("STAGE 02", "Ontology Normalization", CYAN_ACCENT,
         "Standardizes disparate disease terminology via a 3-tier MONDO-to-MedGen concept crosswalk. Resolves canonical HGNC symbols and prevents pleiotropic cross-disease conflation."),
        ("STAGE 03", "3NF Relational Warehouse", PURPLE_ACCENT,
         "Dual-engine architecture: Normalized SQLite 3NF relational database for strict transactional consistency + DuckDB OLAP views for rapid analytical join aggregation."),
        ("STAGE 04", "Cascade Audit Engine", ALERT_RED,
         "Deterministic rule-based joining of upstream ClinGen downgrades with downstream ClinVar P/LP assertions and PanelApp Green tiers. Materializes Class A, B, and C discrepancy findings."),
        ("STAGE 05", "Clinical Decision Support", ALERT_GREEN,
         "Interactive Streamlit web portal, automated command-line interface (run.py), and ISO 15189 compliant clinical governance dossiers (.md) for laboratory re-curation triage."),
    ]

    cards = []
    card_w = 2.18
    gap = 0.20
    for i, (stage, title, col, desc) in enumerate(pipeline_steps):
        left = 0.8 + i * (card_w + gap)
        c = add_card(slide, left, 1.85, card_w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(card_w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(card_w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = stage
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 11)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 11 shows the 5-stage automated architecture of CuraCascade. First, Multi-Source Ingestion extracts raw public data with SHA-256 cryptographic checksums to guarantee reproducibility. Second, Ontology Normalization maps disparate vocabularies into unified concept clusters. Third, the normalized data is loaded into our 3NF relational warehouse backed by SQLite and DuckDB. Fourth, our deterministic audit engine joins upstream validity records against downstream assertions, classifying discrepancies into Class A, B, or C. Finally, the findings are exposed through our interactive web portal, headless CLI, and exportable clinical dossiers.",
        "concept": "A 5-stage pipeline breaks a complex engineering problem into modular, testable steps: Ingest -> Clean/Normalize -> Store -> Audit -> Report.",
        "takeaway": "CuraCascade replaces manual cross-referencing with a deterministic, reproducible, 5-stage automated audit pipeline.",
        "guardrail": "Be clear that this pipeline operates deterministically based on defined clinical rules, not black-box uninterpretable algorithms.",
        "question": "Why did you choose a 5-stage pipeline architecture instead of querying APIs on demand?",
        "answer": "Direct API querying is non-deterministic and computationally slow across thousands of genes and tens of thousands of variants. By staging ingestion into a normalized relational warehouse, we guarantee sub-10ms join performance, cryptographic provenance, and offline reproducibility."
    })


# ==============================================================================
# Slide 12: System Architecture: Dual-Engine Data Warehouse
# ==============================================================================

def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "11 // SYSTEM ARCHITECTURE",
        "System Architecture: Dual-Engine Data Warehouse",
        "Coupling SQLite transactional 3NF integrity with DuckDB columnar analytical aggregation."
    )

    arch_img = FIG_DIR / "figure_schema_architecture.png"
    if arch_img.exists():
        slide.shapes.add_picture(str(arch_img), Inches(0.8), Inches(1.85), width=Inches(6.4))
    else:
        add_card(slide, 0.8, 1.85, 6.4, 4.85, SURFACE_NAVY, SURFACE_BORDER)

    c_right = add_card(slide, 7.4, 1.85, 5.133, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.65), Inches(2.05), Inches(4.6), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FOUR-PILLAR ARCHITECTURAL RIGOR"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    specs = [
        ("1. Transactional Integrity (SQLite)",
         "Strict Third Normal Form (3NF) relational schema with 9 tables, cascading foreign keys, compound indexes on (gene_symbol, disease_id), and automated uniqueness constraints preventing assertion duplication."),
        ("2. Analytical OLAP Acceleration (DuckDB)",
         "In-memory columnar query engine executing complex multi-database joins across 50,000+ variants in sub-10ms response times for real-time dashboard responsiveness."),
        ("3. Cryptographic Provenance",
         "Dedicated provenance audit table capturing SHA-256 checksums, snapshot dates, and transformation versioning for full ISO 15189 reproducibility."),
        ("4. Dual Execution Modality",
         "Fully headless command-line interface (run.py) for automated CI/CD bioinformatics pipelines alongside an interactive clinical decision support dashboard in Streamlit."),
    ]

    for title, desc in specs:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

    add_footer(slide, 12)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 12 details our system architecture. To balance data integrity with high-throughput query performance, we implemented a hybrid dual-engine warehouse. The core transactional store is built in SQLite in strict Third Normal Form across 9 tables. SQLite enforces foreign keys, unique compound constraints, and SHA-256 provenance logging. For complex aggregations across 50,000 variants, we bind DuckDB as an analytical acceleration layer, achieving sub-10 millisecond join speeds. Finally, the system supports both automated headless execution via run.py and an interactive clinical portal in Streamlit.",
        "concept": "Dual-engine architecture combines the best of both worlds: SQLite for rock-solid transactional safety (writing and storing data cleanly) and DuckDB for ultra-fast analytics (reading and aggregating massive tables).",
        "takeaway": "CuraCascade combines SQLite's strict 3NF relational constraints with DuckDB's in-memory columnar join speed for reproducible, low-latency execution.",
        "guardrail": "Ensure that claims of 3NF schema compliance are backed by the actual 9-table schema definition in database/schema.py.",
        "question": "Why did you use SQLite and DuckDB instead of an enterprise client-server database like PostgreSQL?",
        "answer": "Clinical bioinformatics pipelines frequently run in containerized or air-gapped high-performance computing clusters. Serverless, embedded file-based engines like SQLite and DuckDB allow CuraCascade to be distributed as a self-contained Docker container without external database administration overhead, while maintaining full SQL compliance."
    })


# ==============================================================================
# Slide 13: Relational Schema & 3NF Design
# ==============================================================================

def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "12 // RELATIONAL SCHEMA",
        "Relational Schema & Entity-Relationship Architecture (3NF)",
        "Third Normal Form normalized relational structure linking upstream curation with downstream assertions."
    )

    # Left: Embed Live 3NF Schema Diagram Screenshot
    s15_img = SCREENSHOT_DIR / "cropped_s15_schema_relational_3nf.png"
    if s15_img.exists():
        slide.shapes.add_picture(str(s15_img), Inches(0.8), Inches(1.85), width=Inches(6.4))
    else:
        add_card(slide, 0.8, 1.85, 6.4, 4.85, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Relational Architecture Specifications Card
    c_right = add_card(slide, 7.4, 1.85, 5.133, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.65), Inches(2.05), Inches(4.6), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "3NF RELATIONAL SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    schema_points = [
        ("Third Normal Form (3NF) Elimination of Anomalies",
         "Non-key attributes depend strictly on primary keys. Eliminates insertion, update, and deletion anomalies across genes, diseases, curations, and variant records."),
        ("Referential Integrity & Cascading Constraints",
         "Strict Foreign Key enforcement: deleting a gene or disease cascades predictably without creating orphaned variant records. Enforced via SQLite PRAGMA foreign_keys = ON."),
        ("Compound Indexing for Join Acceleration",
         "B-tree composite indexes on (gene_symbol, disease_id) and (gene_symbol, variation_id) optimize join resolution, reducing query plan scan cost from O(N) to O(log N)."),
        ("Verified Scale Across Dual Operating Modes",
         "• Showcase Benchmark Mode: 36 genes, 46 ClinVar variants, 25 panels, 34 findings.\n• Full Corpus Mode: 3,033 genes, 2,147 diseases, 51,025 variants, 507 panels, 51,251 findings."),
    ]

    for title, desc in schema_points:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    add_footer(slide, 13)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 13 displays our actual relational entity-relationship schema, captured directly from Tab 5 of our live web application. The schema is normalized into Third Normal Form across 9 tables. Notice how DISEASES and GENES act as core dimension entities, linked via foreign keys to CLINGEN_CURATIONS, CLINVAR_VARIANTS, and PANELAPP_ENTRIES. The AUDIT_FINDINGS table materializes discrepancy joins with latency metrics. B-tree compound indexes on gene symbol and disease ID reduce query execution from an expensive full-table scan to logarithmic B-tree lookups.",
        "concept": "Third Normal Form (3NF) is a mathematical standard for database design: every piece of data lives in exactly one place. If a gene name changes, you update it once in the GENES table, rather than hunting through 50,000 variant rows.",
        "takeaway": "CuraCascade enforces strict 3NF relational normalization and composite B-tree indexing across 9 tables, ensuring ACID transactional integrity.",
        "guardrail": "Do not claim that this schema is stored in the cloud; the SQLite database file lives locally or containerized in Docker.",
        "question": "What is the purpose of compound indexes on (gene_symbol, disease_id)?",
        "answer": "In clinical auditing, every query filters simultaneously by gene symbol and disease indication. A compound B-tree index allows SQLite and DuckDB to resolve multi-database joins in sub-10 milliseconds without full table scans."
    })


# ==============================================================================
# Slide 14: Data Ingestion & Provenance
# ==============================================================================

def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "13 // DATA INGESTION & ETL",
        "Data Ingestion, Normalization & Forensic Provenance",
        "Extracting, parsing, standardizing, and tracking multi-source biomedical data with cryptographic reproducibility."
    )

    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. MULTI-SOURCE INGESTION & ETL ARCHITECTURE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    etl_steps = [
        ("ClinGen GCEP Fetcher", "Parses ClinGen Gene-Disease Validity CSV releases; maps curation records into structured validity tiers (Definitive to Refuted) and extracts appraisal dates."),
        ("ClinVar Variant Parser", "Parses ClinVar tab-delimited summary releases; extracts variation_id, HGVS expressions, review stars (0 to 4), and ACMG clinical significance."),
        ("PanelApp REST API Client", "Queries Genomics England PanelApp REST API endpoints; retrieves panel entities, versions, and Green/Amber/Red confidence tiers."),
        ("gnomAD v4 Population Pipeline", "Extracts global and continental population allele frequencies; maps maximum population AF (popmax) for quantitative burden evaluation."),
    ]
    for title, desc in etl_steps:
        p = tf1.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(6)

    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. CRYPTOGRAPHIC PROVENANCE & ERROR HANDLING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    prov_steps = [
        ("SHA-256 Checksum Verification", "Every ingested raw dataset is hashed with SHA-256 upon arrival; hashes are stored in the provenance table to guarantee byte-for-byte reproducibility."),
        ("Defensive Error Handling", "ETL fetchers implement exponential backoff retry logic, schema validation checks, and automatic fallback to verified local static archives if remote APIs fail."),
        ("HGNC Symbol Harmonization", "Resolves historical gene synonyms, outdated aliases, and withdrawn symbols against the canonical HGNC database (e.g. mapping GJB6, MYLK2, ACTN2)."),
        ("Idempotent Schema Migrations", "Database creation and migration scripts are strictly idempotent; re-running ingestion cleans and rebuilds tables without duplicate primary key collisions."),
    ]
    for title, desc in prov_steps:
        p = tf2.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = ALERT_GREEN if "SHA-256" in title else TEXT_WHITE
        p.space_before = Pt(6)

    add_footer(slide, 14)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 14 covers data ingestion and provenance. In biomedical informatics, reproducibility is paramount: if you cannot prove which version of a database you used, your results are not scientifically defensible. CuraCascade implements dedicated ETL parsers for ClinGen, ClinVar, PanelApp, and gnomAD. Crucially, as shown on the right, every downloaded file is cryptographically hashed with SHA-256 and recorded in our provenance database table. Our pipeline also includes defensive error handling with exponential backoff and HGNC symbol harmonization to resolve outdated gene aliases.",
        "concept": "A SHA-256 hash is a digital fingerprint of a file. If even a single letter in a 1-gigabyte database changes, the hash changes completely. Storing the hash proves that our audit was run on verified, uncorrupted data.",
        "takeaway": "CuraCascade guarantees scientific reproducibility through automated ETL parsers, HGNC symbol harmonization, and SHA-256 cryptographic provenance logging.",
        "guardrail": "Do not claim that the system re-downloads 50GB of raw ClinVar XML every time it runs. It caches static snapshots with cryptographic hash verification.",
        "question": "What happens if a gene symbol has changed historically, like an old alias?",
        "answer": "Our ingestion pipeline includes an HGNC normalization layer that cross-references gene symbols against the HUGO Gene Nomenclature Committee database, resolving historical aliases to their canonical official symbols."
    })


# ==============================================================================
# Slide 15: Disease-Aware Matching Heuristics
# ==============================================================================

def build_slide_15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "14 // MATCHING LOGIC",
        "Disease-Aware Ontology Matching & Crosswalk Heuristics",
        "Preventing catastrophic false-positive alerts on pleiotropic multi-disease genes."
    )

    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "THE FATAL FLAW OF GENE-SYMBOL-ONLY MATCHING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_RED

    p = tf1.add_paragraph()
    p.text = "In human genetics, a single gene frequently causes multiple completely distinct diseases (pleiotropy)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "Consider ACTN2 (Actinin Alpha 2):\n• Disease A: Hypertrophic Cardiomyopathy (HCM) → ClinGen status: DISPUTED.\n• Disease B: Distal Myopathy (Muscle weakness) → ClinGen status: DEFINITIVE."
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "If an algorithm matches solely by gene symbol 'ACTN2', it sees a Disputed evaluation and falsely invalidates all variants for Distal Myopathy! This would deprive muscular dystrophy patients of life-saving molecular diagnoses."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "CuraCascade's unit of analysis is strictly the Gene–Disease Dyad (G, D), never the gene alone."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(6)

    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "CURACASCADE 3-TIER MATCHING HIERARCHY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    tiers = [
        ("TIER 1: Exact Ontology Concept Crosswalk",
         "Direct mapping between ClinGen MONDO identifier and ClinVar MedGen / OMIM concept ID via curated crosswalk dictionary (ontology_crosswalk.py). Match Confidence = HIGH."),
        ("TIER 2: Substring Matching with Keyword Exclusion Guards",
         "When concept IDs are absent, performs normalized string matching but enforces strict negative keyword guards (e.g. 'hypertrophic cardiomyopathy' does NOT match 'distal myopathy'; 'Brugada' does NOT match 'Long QT'). Match Confidence = MEDIUM."),
        ("TIER 3: Fallback & Review Required",
         "Unmapped, conflicting, or generalized disease terms (e.g. 'Cardiovascular phenotype') are marked as REVIEW_REQUIRED and excluded from automatic discrepancy flagging to protect precision."),
    ]
    for title, desc in tiers:
        p = tf2.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf2.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    add_footer(slide, 15)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 15 explains why CuraCascade's disease-aware matching heuristic is one of our most important technical contributions. Naive software matches databases by gene symbol alone. That works for simple single-disease genes, but it fails catastrophically on pleiotropic genes. Take ACTN2: ClinGen disputed its association with cardiomyopathy, but confirmed it is Definitive for distal myopathy. A gene-only join would wrongly flag all muscular dystrophy variants as fake! CuraCascade treats the Gene-Disease Dyad as the unit of analysis, using a 3-tier matching hierarchy with strict keyword exclusion guards.",
        "concept": "Pleiotropy means one gene does multiple jobs in different body organs. Matching by gene name alone is like firing an entire employee because they made a mistake in accounting, even though they are your best software engineer.",
        "takeaway": "CuraCascade prevents false alarms on pleiotropic genes by enforcing a 3-tier disease-aware matching hierarchy with strict keyword exclusion guards.",
        "guardrail": "Do not claim that CuraCascade uses a large language model for matching. It uses a deterministic, rule-based ontology crosswalk.",
        "question": "How many multi-disease test cases were formally verified in your automated test suite?",
        "answer": "12 multi-disease genes were verified with dedicated unit tests in test_biological_matching.py, including MLH1, MSH2, FBN1, RYR2, KCNQ1, SCN5A, and MYH7, proving that distinct disorders are never falsely flagged."
    })


# ==============================================================================
# Slide 16: Live Clinical Decision Support Portal Overview
# ==============================================================================

def build_slide_16(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "15 // SOFTWARE DEMONSTRATION",
        "Live Clinical Decision Support Portal: System Overview",
        "Interactive laboratory interface deployed on Streamlit Cloud (curacascadev2.streamlit.app)."
    )

    # Top Left: Showcase Benchmark HUD (Cropped S1)
    s1_img = SCREENSHOT_DIR / "cropped_s1_dashboard_hero.png"
    if s1_img.exists():
        slide.shapes.add_picture(str(s1_img), Inches(0.8), Inches(1.85), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 1.85, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Bottom Left: Full Corpus Scale HUD (Cropped S20)
    s20_img = SCREENSHOT_DIR / "cropped_s20_full_corpus_hero.png"
    if s20_img.exists():
        slide.shapes.add_picture(str(s20_img), Inches(0.8), Inches(4.35), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 4.35, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Verified Capabilities Card
    c_right = add_card(slide, 7.05, 1.85, 5.48, 4.9, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.25), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "VERIFIED DEPLOYED CAPABILITIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    callouts = [
        ("1. Real-Time Operational Telemetry",
         "Upper Screenshot: Showcase Mode live HUD displaying 36 Curated Genes, 46 ClinVar Variants, 25 Panels, and 34 Materialized Inconsistencies with 202.5 patient-years at risk."),
        ("2. Real-World Scaling (Full Corpus Mode)",
         "Lower Screenshot: Seamless scaling to 3,033 Genes, 51,025 Variants, and 51,251 Discrepancies (34,800 Class A, 16,350 Class B) with 182,760.4 patient-years at risk."),
        ("3. Database Layer Selector",
         "Interactive sidebar toggle allowing clinical geneticists to switch instantaneously between the curated benchmark demonstration set and the 50k+ full-scale corpus."),
        ("4. Seven Interactive Functional Sections",
         "Complete laboratory navigation: Audit Explorer (01), Gene Detail & Timeline (02), Aggregate Analytics (03), Downgrade Forecast (04), and Clinical Methodology (05)."),
    ]

    for title, desc in callouts:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    add_footer(slide, 16)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 16 introduces our genuine running application, deployed publicly at curacascadev2.streamlit.app. On the upper left, you see the Showcase Mode interface tracking our 34 benchmark findings. Below it, you see the exact same interface switched to Full Corpus Mode, tracking 51,251 findings across 3,033 genes. The sidebar HUD displays real-time table counts and patient-years at risk. Notice that the entire platform is responsive, verified, and accessible to any laboratory geneticist via a standard web browser.",
        "concept": "A dual operating mode allows users to inspect a clean, curated set of 34 benchmark genes for teaching and demonstration, while proving that the underlying architecture scales effortlessly to 50,000+ variants.",
        "takeaway": "CuraCascade provides a production-grade, responsive web portal operating seamlessly in both curated showcase mode and full-scale 50,000+ variant mode.",
        "guardrail": "Do not imply that this website requires paid login credentials. It is deployed as an open-access public resource.",
        "question": "How fast does the web interface respond when switching to Full Corpus mode?",
        "answer": "Thanks to DuckDB in-memory OLAP indexing and Streamlit st.cache_data decorators, initial data loading takes less than 2 seconds, and table filtering executes in sub-10 milliseconds."
    })


# ==============================================================================
# Slide 17: Interactive Inconsistency Audit Explorer
# ==============================================================================

def build_slide_17(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "16 // AUDIT EXPLORER",
        "Interactive Inconsistency Audit Explorer & Multi-Tier Filtering",
        "Materialized discrepancy table with multi-dimensional filtering, search, and CSV export."
    )

    # Top Left: Showcase Audit Table (Cropped S2)
    s2_img = SCREENSHOT_DIR / "cropped_s2_audit_table_full.png"
    if s2_img.exists():
        slide.shapes.add_picture(str(s2_img), Inches(0.8), Inches(1.85), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 1.85, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Bottom Left: Full Corpus Paginated Table (Cropped S21)
    s21_img = SCREENSHOT_DIR / "cropped_s21_full_corpus_audit_explorer.png"
    if s21_img.exists():
        slide.shapes.add_picture(str(s21_img), Inches(0.8), Inches(4.35), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 4.35, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Analytical Features Card
    c_right = add_card(slide, 7.05, 1.85, 5.48, 4.9, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.25), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "INTERACTIVE TRIAGE CAPABILITIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    triage_features = [
        ("Multi-Dimensional Filtering",
         "Filter instantly by Inconsistency Class (Class A Critical, Class B High, Class C Critical), target database layer (ClinVar Variant vs. PanelApp Panel), and prescriptive action."),
        ("Instant Gene Symbol Search",
         "Search any gene symbol (e.g. SCN1B, MYLK2, KCNE2, GJB6) to isolate specific clinical panels or variants undergoing laboratory re-curation."),
        ("Temporal Sorting by Latency",
         "Sort findings by longest unresolved latency days to immediately identify historical candidate genes with the longest uncorrected clinical propagation lags."),
        ("Automated CSV Export for Lab LIMS",
         "One-click 'Export CSV' button generates full cohort exports with all HGVS variants, review stars, MCAF ratios, and ClinGen report URLs for direct laboratory LIMS integration."),
    ]

    for title, desc in triage_features:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    add_footer(slide, 17)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 17 showcases the core working tool of our platform: the Inconsistency Audit Explorer. In the upper screenshot, you see our curated findings table, where every row displays the gene, disease indication, ClinGen status, and downstream ClinVar variant. Below, you see the exact same explorer handling 51,251 findings across 513 pages in Full Corpus Mode. Users can filter by severity, search by gene symbol, sort by unresolved latency, and export the entire dataset to CSV for integration into hospital laboratory information systems (LIMS).",
        "concept": "LIMS stands for Laboratory Information Management System. By allowing one-click CSV export with exact HGVS genomic coordinates, hospital labs can pipe CuraCascade's audit verdicts directly into their internal clinical reporting software.",
        "takeaway": "The Audit Explorer provides high-throughput, multi-dimensional filtering, pagination across 513 pages, and one-click LIMS CSV export.",
        "guardrail": "Do not claim that CuraCascade automatically modifies ClinVar's official database; it exports remediation lists for labs to correct their own submissions.",
        "question": "Can a user filter by specific ClinVar review star levels?",
        "answer": "Yes. The underlying database and export tables capture review stars (0 to 4), allowing geneticists to isolate low-star unreviewed submissions from multi-star expert panel assertions."
    })


# ==============================================================================
# Slide 18: Evidence Traceability & Remediation
# ==============================================================================

def build_slide_18(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "17 // CLINICAL GOVERNANCE",
        "Evidence Traceability & Prescriptive Clinical Remediation",
        "Translating automated audit discrepancies into actionable laboratory directives and ISO 15189 dossiers."
    )

    # Left: Embed Live Remediation Table Screenshot (Cropped S17)
    s17_img = SCREENSHOT_DIR / "cropped_s17_prescriptive_remediation_table.png"
    if s17_img.exists():
        slide.shapes.add_picture(str(s17_img), Inches(0.8), Inches(1.85), width=Inches(6.4))
    else:
        add_card(slide, 0.8, 1.85, 6.4, 4.85, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Concrete Remediation Directives Card
    c_right = add_card(slide, 7.4, 1.85, 5.133, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.65), Inches(2.05), Inches(4.6), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ACTIONABLE CLINICAL DIRECTIVES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    remediation_rules = [
        ("Class A Directive (Disputed / Refuted + P/LP)",
         "• Submitter Action: Formal retraction or downgrade to VUS citing ClinGen GCEP determination report URL.\n• Clinical Governance: Audit historical index cases; cease predictive cascade testing in family members; issue amended reports."),
        ("Class B Directive (Limited Evidence + P/LP)",
         "• Submitter Action: Apply ACMG Guidance Cap (Maximum VUS) until replicated human genetic proof emerges.\n• Diagnostic Directive: Restrict panel reporting to Amber tier; require senior clinical geneticist sign-off."),
        ("Class C Directive (PanelApp Green in Disputed/Refuted)",
         "• Diagnostic Action: Immediate Demotion to Red Tier.\n• Pipeline Directive: Remove genomic coordinates from routine exome/panel filtering BED files; prevent automated primary diagnostic sign-outs."),
        ("Automated Clinical Governance Dossiers",
         "Generates ISO 15189 compliant markdown audit dossiers (.md) capturing full evidence lineage, SHA-256 hashes, and actionable sign-off checklists."),
    ]

    for title, desc in remediation_rules:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ALERT_AMBER if "Class B" in title else (ALERT_RED if "Class A" in title else CYAN_ACCENT)
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(1)

    add_footer(slide, 18)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 18 demonstrates that CuraCascade is not just a passive reporting tool; it is a prescriptive clinical governance engine. In the screenshot on the left, taken from Tab 5 of our live app, you see our remediation matrix. For Class A critical findings, laboratories are instructed to issue amended reports and cease predictive testing in family members. For Class B, ACMG standards cap variants at VUS. For Class C, diagnostic panels are demoted to Red. Furthermore, our pipeline can automatically export complete clinical governance dossiers conforming to ISO 15189 laboratory accreditation standards.",
        "concept": "A prescriptive directive tells the laboratory exactly what action to take (e.g. 'Cease cascade testing' or 'Demote panel to Red') rather than just saying 'there is an error'.",
        "takeaway": "CuraCascade translates raw audit discrepancies into concrete clinical governance directives and ISO 15189 compliant audit dossiers.",
        "guardrail": "Do not claim that CuraCascade automatically updates hospital medical records; it advises the clinical team on the necessary actions.",
        "question": "What is an amended clinical report?",
        "answer": "When a clinical testing laboratory discovers that a previously signed-out diagnostic report contained an erroneous classification, standard hospital accreditation requires issuing a formal amended report to the physician correcting the finding."
    })


# ==============================================================================
# Slide 19: Worked Clinical Case Studies: SCN1B & ACTN2
# ==============================================================================

def build_slide_19(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "18 // CLINICAL CASE STUDIES",
        "Worked Case Studies: Discrepancy Auditing in SCN1B, MYLK2 & ACTN2",
        "Detailed examination of real-world evidence cascades across cardiac and neuromuscular disorders."
    )

    # Top Left: Screenshot S4 (ACTN2 Gene Detail)
    s4_img = SCREENSHOT_DIR / "cropped_s4_gene_detail_actn2.png"
    if s4_img.exists():
        slide.shapes.add_picture(str(s4_img), Inches(0.8), Inches(1.85), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 1.85, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Bottom Left: Screenshot S3 (Custom Gene Evaluator)
    s3_img = SCREENSHOT_DIR / "cropped_s3_custom_gene_evaluator.png"
    if s3_img.exists():
        slide.shapes.add_picture(str(s3_img), Inches(0.8), Inches(4.35), width=Inches(6.0))
    else:
        add_card(slide, 0.8, 4.35, 6.0, 2.4, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Concrete Clinical Audit Breakdown Card
    c_right = add_card(slide, 7.05, 1.85, 5.48, 4.9, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.25), Inches(2.05), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "REAL-WORLD CLINICAL AUDIT FINDINGS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    cases = [
        ("SCN1B — Brugada Syndrome (Class A Finding)",
         "• Upstream Status: DISPUTED in 2021 by ClinGen Arrhythmia GCEP.\n• Downstream Status: 18 ClinVar Pathogenic / Likely Pathogenic assertions remain active.\n• Clinical Hazard: Risk of false-positive diagnosis and unwarranted prophylactic ICD heart surgery in asymptomatic patients."),
        ("MYLK2 — Hypertrophic Cardiomyopathy (Class C Finding)",
         "• Upstream Status: DISPUTED in 2024 by ClinGen Cardiomyopathy GCEP.\n• Downstream Status: Listed as GREEN (diagnostic-grade) on PanelApp panels.\n• Clinical Hazard: Stale coordinates remain in exome filtering BED files in NHS GMS pipelines."),
        ("ACTN2 — Pleiotropic Disease Specificity",
         "• Demonstrated above: CuraCascade identifies ACTN2 as Disputed for HCM while confirming it as Definitive for Distal Myopathy, suppressing false alerts for muscle disease."),
    ]

    for title, desc in cases:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ALERT_AMBER if "ACTN2" in title else ALERT_RED
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(1)

    add_footer(slide, 19)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 19 walks through real-world case studies from our database. In the top screenshot, you see our gene detail inspector for ACTN2. In the lower screenshot, our live multi-gene evaluator audits a custom cardiac panel including ANK2, MYLK2, and TCAP. Consider SCN1B: ClinGen disputed its link to Brugada syndrome in 2021 because modern population sequencing proved that variants occur at similar rates in healthy individuals. Yet in ClinVar, 18 variants remain labeled Pathogenic! Consider MYLK2: disputed in 2024, yet active on diagnostic gene panels. CuraCascade catches these specific discrepancies before reports reach patients.",
        "concept": "A worked example demonstrates the software on real clinical genes that the examiners may recognize from published literature.",
        "takeaway": "Tangible audit findings in SCN1B, MYLK2, and ACTN2 illustrate real clinical hazards where downstream databases lag expert consensus.",
        "guardrail": "Do not state that CuraCascade treated individual hospital patients; these are real database assertions evaluated against published expert consensus.",
        "question": "Why did ClinGen dispute SCN1B in Brugada syndrome?",
        "answer": "Early studies in the 2000s identified SCN1B variants in small family cohorts without adequate control populations. Large-scale sequencing in gnomAD subsequently demonstrated that those exact variants are common in healthy individuals, disproving causality."
    })


# ==============================================================================
# Slide 20: 100-Gene Benchmark Methodology
# ==============================================================================

def build_slide_20(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "19 // VALIDATION METHODOLOGY",
        "Empirical 100-Gene Adjudication Validation Benchmark",
        "Independent expert validation cohort evaluating classifier precision, recall, and label boundaries."
    )

    c1 = add_card(slide, 0.8, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(3.25), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. GOLD-STANDARD COMPOSITION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "The benchmark comprises 100 independently frozen Gene-Disease Clinical Validity Assertions (G, D):\n\n• 54 Published Downgraded Genes: Verified from peer-reviewed literature and ClinGen GCEPs (Cardiomyopathy, Arrhythmia, Hereditary Cancer, Neurodevelopmental).\n\n• 46 Definitive Clinical Controls: Unquestioned gene-disease associations (ACMG SF v3.2 / National Genomic Test Directory, e.g. BRCA1, TP53, MLH1, CFTR)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c2 = add_card(slide, 4.84, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(5.04), Inches(2.05), Inches(3.25), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. COHORT PARTITIONING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf2.add_paragraph()
    p.text = "To maintain statistical integrity, cases are strictly partitioned:\n\n• Evaluable Cohort (N = 94):\nTarget genes and curation records are present in the warehouse snapshot, permitting empirical join evaluation.\n\n• Excluded Cases (N = 6):\nDesignated as NOT_EVALUABLE due to complete absence of gene or curation records in the static snapshot (XRCC3, DFNB59, TSC1, TSC2, SMAD3, SMN1)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    c3 = add_card(slide, 8.88, 1.85, 3.65, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb3 = slide.shapes.add_textbox(Inches(9.08), Inches(2.05), Inches(3.25), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "3. LABEL FIREWALL & RIGOR"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN

    p = tf3.add_paragraph()
    p.text = "Strict adherence to scientific evaluation protocols:\n\n• Zero Hardcoded Predictions: Overrides (KNOWN_FN, KNOWN_FP) completely removed.\n\n• Live Query Execution: Queries execute dynamically against SQLite.\n\n• Wilson Score 95% CIs: Binomial performance intervals computed analytically.\n\n• Classifier Concordance: Inter-rater agreement measured via Cohen's kappa."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    add_footer(slide, 20)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id, c3.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 20 introduces our formal validation benchmark methodology. To evaluate CuraCascade objectively, we compiled a gold-standard benchmark of 100 independently curated gene-disease assertions: 54 published downgraded panels and 46 definitive ACMG controls like BRCA1 and CFTR. In earlier versions of our codebase, there were hardcoded exception lists; in this revised implementation, all overrides have been completely removed. We also transparently partition the cohort: 94 cases are evaluable, while 6 cases are designated NOT_EVALUABLE because their curation records were completely absent from the local snapshot.",
        "concept": "A label firewall means the audit algorithm has zero access to the benchmark answer key while running. Queries run live against the database.",
        "takeaway": "The 100-gene validation benchmark enforces a strict label firewall with zero hardcoded prediction overrides and live relational query execution.",
        "guardrail": "Do not claim that the 100 benchmark cases were evaluated by multiple blinded human curators; this is a single-curator literature-derived benchmark.",
        "question": "Why did you exclude 6 cases as NOT_EVALUABLE instead of counting them as false negatives?",
        "answer": "Counting unobserved data as algorithmic false negatives conflates data availability with classifier logic. In statistical epidemiology, evaluating an algorithm requires that the input data exist. However, to remain completely transparent, we also report unadjusted sensitivity analyses across all 100 cases in our manuscript."
    })


# ==============================================================================
# Slide 21: Quantitative Benchmark Results
# ==============================================================================

def build_slide_21(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "20 // BENCHMARK RESULTS",
        "Empirical Results: The Precision–Recall Trade-Off",
        "Conservative disease matching achieves zero false positives (100% PPV) at the cost of moderate recall."
    )

    # Left Container: Confusion Matrix
    c_cm = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "EVALUABLE COHORT CONFUSION MATRIX (N = 94)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    # 2x2 Matrix Graphic using nested cards
    add_card(slide, 1.1, 2.5, 2.45, 1.45, SURFACE_CARD_ALT, ALERT_GREEN)
    tb_tp = slide.shapes.add_textbox(Inches(1.2), Inches(2.55), Inches(2.25), Inches(1.3))
    tf_tp = tb_tp.text_frame
    p = tf_tp.paragraphs[0]
    p.text = "TRUE POSITIVES (TP)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN
    p = tf_tp.add_paragraph()
    p.text = "18"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_tp.add_paragraph()
    p.text = "Correctly flagged discrepancies"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide, 3.8, 2.5, 2.45, 1.45, SURFACE_CARD_ALT, TEAL_PRIMARY)
    tb_fp = slide.shapes.add_textbox(Inches(3.9), Inches(2.55), Inches(2.25), Inches(1.3))
    tf_fp = tb_fp.text_frame
    p = tf_fp.paragraphs[0]
    p.text = "FALSE POSITIVES (FP)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY
    p = tf_fp.add_paragraph()
    p.text = "0"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_fp.add_paragraph()
    p.text = "Zero false alarms raised"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide, 1.1, 4.15, 2.45, 1.45, SURFACE_CARD_ALT, ALERT_AMBER)
    tb_fn = slide.shapes.add_textbox(Inches(1.2), Inches(4.2), Inches(2.25), Inches(1.3))
    tf_fn = tb_fn.text_frame
    p = tf_fn.paragraphs[0]
    p.text = "FALSE NEGATIVES (FN)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER
    p = tf_fn.add_paragraph()
    p.text = "34"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_fn.add_paragraph()
    p.text = "Undetected discrepancies"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED

    add_card(slide, 3.8, 4.15, 2.45, 1.45, SURFACE_CARD_ALT, CYAN_ACCENT)
    tb_tn = slide.shapes.add_textbox(Inches(3.9), Inches(4.2), Inches(2.25), Inches(1.3))
    tf_tn = tb_tn.text_frame
    p = tf_tn.paragraphs[0]
    p.text = "TRUE NEGATIVES (TN)"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p = tf_tn.add_paragraph()
    p.text = "42"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p = tf_tn.add_paragraph()
    p.text = "Definitive controls ruled out"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED

    tb_cm_sub = slide.shapes.add_textbox(Inches(1.1), Inches(5.8), Inches(5.1), Inches(0.8))
    tf_csub = tb_cm_sub.text_frame
    tf_csub.word_wrap = True
    p = tf_csub.paragraphs[0]
    p.text = "• Denominator: 94 Evaluable (52 Gold Downgraded + 42 Definitive Controls)"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p = tf_csub.add_paragraph()
    p.text = "• Sensitivity Analysis (All 100): Recall = 33.3%, Accuracy = 64.0%"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    # Right Container: Statistical Classification Metrics Card
    c_right = add_card(slide, 6.75, 1.85, 5.78, 2.35, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(6.95), Inches(1.95), Inches(5.4), Inches(2.15))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "STATISTICAL METRICS (WILSON SCORE 95% CIs)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    metrics = [
        ("Precision (PPV)", "100.0%", "[82.4%, 100.0%]", "Zero false alarms across all audited findings"),
        ("Recall (Sensitivity)", "34.6%", "[23.2%, 48.2%]", "Moderate recall from conservative matching & missing data"),
        ("Specificity (TNR)", "100.0%", "[91.6%, 100.0%]", "Perfect rejection of definitive clinical controls"),
        ("Concordance Kappa", "0.3212", "Fair Agreement", "Overall Accuracy: 63.8% [53.8%, 72.8%]"),
    ]

    for name, val, ci, desc in metrics:
        p = tf2.add_paragraph()
        p.text = f"• {name}: {val} {ci} — {desc}"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ALERT_GREEN if "100.0%" in val else (ALERT_AMBER if "34.6%" in val else CYAN_ACCENT)
        p.space_before = Pt(2)

    # Right Bottom: Real Live 100-Gene Adjudication Validation Benchmark Dashboard Screenshot
    s18_img = SCREENSHOT_DIR / "cropped_s18_validation_benchmark_results.png"
    if s18_img.exists():
        slide.shapes.add_picture(str(s18_img), Inches(6.75), Inches(4.35), width=Inches(5.78))
    else:
        add_card(slide, 6.75, 4.35, 5.78, 2.45, SURFACE_NAVY, SURFACE_BORDER)

    add_footer(slide, 21)
    add_sequential_animations(slide, [c_cm.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 21 presents our quantitative empirical results. In the 94 evaluable benchmark cases, CuraCascade achieved 18 True Positives, 42 True Negatives, 0 False Positives, and 34 False Negatives. This translates to 100.0% Precision with an analytical Wilson score 95% confidence interval of 82.4% to 100.0%. Specificity is also 100.0%, meaning not a single definitive control gene was falsely flagged. Recall is 34.6%. In the lower right screenshot, you see these exact benchmark metrics materialized directly in Tab 5 of our live web application. In the next slide, we will audit why those 34 false negatives occurred.",
        "concept": "Precision = TP / (TP + FP). Because FP = 0, precision is 100%. Recall = TP / (TP + FN) = 18 / 52 = 34.6%.",
        "takeaway": "CuraCascade achieves 100.0% precision with zero false alarms, accepting 34.6% recall to prevent alert fatigue in clinical laboratories.",
        "guardrail": "Do not call Cohen's kappa inter-rater reliability. It is classifier concordance kappa.",
        "question": "What is the F1-score of your model?",
        "answer": "The harmonic mean F1-score is 0.5143, reflecting the deliberate trade-off between perfect precision (1.0) and conservative recall (0.346)."
    })


# ==============================================================================
# Slide 22: Failure Mode Analysis: The 34 False Negatives
# ==============================================================================

def build_slide_22(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "21 // ERROR ANALYSIS",
        "Failure Mode Analysis: Dissecting the 34 False Negatives",
        "Transparent scientific breakdown of why 34 benchmark discrepancies were not automatically flagged."
    )

    categories = [
        ("CATEGORY 1: DATA AVAILABILITY", ALERT_AMBER,
         "16 Cases (47.1% of False Negatives)",
         "Downstream Evidence Not Present in Warehouse Snapshot",
         "The gene-disease validity relationship is formally downgraded in ClinGen, but the local ClinVar snapshot contains ZERO Pathogenic/Likely Pathogenic variants for that condition, or PanelApp had already retired the panel.\n\n• Exemplar Genes: RAD50, XRCC2, CACNA2D1, KCNJ8, HCN4, TRPM4, KCNE3, KCNE1.\n• Scientific Assessment: Not an algorithmic flaw; an algorithm cannot flag data that does not exist in the database."),
        ("CATEGORY 2: PHENOTYPIC SPECIFICITY", CYAN_ACCENT,
         "14 Cases (41.2% of False Negatives)",
         "Ontology Disconnect & Broad Term Discrepancy",
         "The gene is downgraded for a specific clinical condition (e.g. Hypertrophic Cardiomyopathy), but downstream ClinVar variants are annotated under broad or distinct phenotypes (e.g. 'Cardiovascular phenotype', 'Inborn genetic diseases', or general 'Cardiomyopathy').\n\n• Exemplar Genes: MYOZ2, CAV3, CSRP3, JPH2, NEXN, VCL.\n• Scientific Assessment: Demonstrates conservative matching; the algorithm deliberately refuses to make unverified assumptions."),
        ("CATEGORY 3: CURATION CRITERIA", PURPLE_ACCENT,
         "4 Cases (11.8% of False Negatives)",
         "Low-Star or Conflicting Assertion Criteria",
         "ClinVar submissions have 0 review stars (no assertion criteria provided) or conflicting interpretations that do not meet the strict P/LP threshold required for Class A alerting.\n\n• Exemplar Genes: GPD1L, CACNB2.\n• Scientific Assessment: Prevents unverified, low-confidence submissions from generating critical clinical alerts."),
    ]

    cards = []
    w = 3.65
    gap = 0.39
    for i, (cat, col, count, title, desc) in enumerate(categories):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(2.05), Inches(w - 0.3), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = cat
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = count
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(6)

    add_footer(slide, 22)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 22 is the most academically rigorous slide in the deck. We do not hide our 34 false negatives; we audited every single one of them. Category 1 accounts for nearly half: 16 cases were simply not present in our ClinVar snapshot. If a testing lab has not deposited any variants for a gene in ClinVar, an automated join cannot flag it. Category 2 accounts for 14 cases: variants were annotated under broad umbrella terms like 'Cardiovascular phenotype', and our disease-aware crosswalk conservatively refused to guess. And Category 3 represents 4 cases where assertions had zero review stars. These false negatives reflect data availability gaps and deliberate conservative suppression, not code defects.",
        "concept": "A failure-mode analysis investigates why software made errors. Examiners respect students who can explain their errors far more than students who pretend their system is 100% perfect.",
        "takeaway": "The 34 false negatives stem from data availability gaps (47.1%) and conservative phenotype matching (41.2%), confirming zero false alarms on clinical controls.",
        "guardrail": "Do not blame ClinVar for being 'bad'; explain that public archives rely on voluntary laboratory deposits.",
        "question": "How could you improve recall from 34.6% to 70% in future work?",
        "answer": "By integrating commercial laboratory proprietary archives and implementing hierarchical ontology expansion, allowing variants labeled 'Cardiovascular phenotype' to match specific cardiomyopathy downgrades when no other disease explanation exists."
    })


# ==============================================================================
# Slide 23: Retrospective Risk Forecasting & Latency Kinetics
# ==============================================================================

def build_slide_23(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "22 // EXPLORATORY ANALYTICS",
        "Retrospective Risk Forecasting & Evidence Latency Kinetics",
        "Exploratory Random Forest triage modeling and cross-sectional empirical latency distribution."
    )

    # Left Column: Exploratory ML Forecasting
    c_left = add_card(slide, 0.8, 1.85, 5.7, 2.4, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(0.95), Inches(1.95), Inches(5.4), Inches(2.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "1. EXPLORATORY MACHINE LEARNING FORECASTING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "Trained a Balanced Random Forest across 7 engineered features (gnomAD AF popmax, low-star ratio, curation age, MCAF violations) to triage currently supported genes for downgrade vulnerability."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(2)

    p = tf1.add_paragraph()
    p.text = "• Discrimination: AUROC = 0.857 (Full Corpus) / 1.000 (Curated Showcase) | Brier: 0.1508\n• Top Risk Driver: Curation Age Elapsed (78.4% perm. wt) & MCAF Violations (10.8%)\n• Caveat: Retrospective static snapshot discrimination; not claimed as prospective clinical predictor."
    p.font.size = Pt(9)
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(3)

    # Left Bottom: Real Live Model ROC & Feature Importance Chart (Cropped S11)
    s11_img = SCREENSHOT_DIR / "cropped_s11_forecast_roc_features.png"
    if s11_img.exists():
        slide.shapes.add_picture(str(s11_img), Inches(0.8), Inches(4.35), width=Inches(5.7))
    else:
        add_card(slide, 0.8, 4.35, 5.7, 2.45, SURFACE_NAVY, SURFACE_BORDER)

    # Right Column: Empirical Latency Kinetics
    c_right = add_card(slide, 6.8, 1.85, 5.73, 2.4, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(6.95), Inches(1.95), Inches(5.4), Inches(2.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "2. EMPIRICAL LATENCY & SUBMITTER KINETICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf2.add_paragraph()
    p.text = "Quantifying temporal propagation lag between authoritative ClinGen validity determinations and downstream assertion correction across active clinical cohorts."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(2)

    p = tf2.add_paragraph()
    p.text = "• Overall Median Latency: 2.82 Years (1,087d IQR) across 51,007 observations (536 genes)\n• Cumulative Patient-Years at Risk: 182,760.4 Years across 51,251 findings\n• Submitter Kinetics: Class A Refuted (2.80 yrs) vs Class B Limited (3.77 yrs, p < 0.001)"
    p.font.size = Pt(9)
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(3)

    # Right Bottom: Real Live Full Corpus Discrepancy Latency Strata Chart (Cropped S24)
    s24_img = SCREENSHOT_DIR / "cropped_s24_full_corpus_discrepancy_strata.png"
    if not s24_img.exists():
        s24_img = SCREENSHOT_DIR / "cropped_s6_latency_cdf_curve.png"
    if s24_img.exists():
        slide.shapes.add_picture(str(s24_img), Inches(6.8), Inches(4.35), width=Inches(5.73))
    else:
        add_card(slide, 6.8, 4.35, 5.73, 2.45, SURFACE_NAVY, SURFACE_BORDER)

    add_footer(slide, 23)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 23 covers our exploratory analytics. On the left, we explored whether supervised machine learning could prioritize genes at risk of future downgrade. Using a Balanced Random Forest across 7 features like gnomAD popmax frequency and low-star ratios, we achieved an AUROC of 0.857 and a Brier score of 0.1508. Notice the live ROC curve and permutation feature importance chart below it, showing curation age as the primary driver. Crucially, we openly disclose potential temporal leakage: features were extracted from static snapshots, so this is an exploratory retrospective triage tool, not prospective clinical forecasting. On the right, our latency analysis across 51,007 ClinVar assertions reveals an overall median lag of 2.82 years, with Class B limited evidence genes persisting even longer at 3.77 years.",
        "concept": "Temporal leakage happens when a machine learning model is trained on data from the future. Because we used a 2024 static database, some post-downgrade evidence may have leaked into the features. Disclosing this openly proves academic maturity.",
        "takeaway": "CuraCascade demonstrates strong retrospective triage capability (AUROC 0.857) and quantifies a 2.82-year cross-sectional evidence propagation lag.",
        "guardrail": "Never claim this machine learning model is clinically validated or ready for diagnostic deployment. Explicitly cite potential temporal leakage.",
        "question": "What is the primary risk of temporal leakage in your machine learning experiment?",
        "answer": "Because features like variant count and allele frequencies were extracted from a 2024 snapshot rather than reconstructed historically from the exact day before each ClinGen downgrade, some post-downgrade evidence shifts may have leaked into the features. That is why we treat this as exploratory retrospective analysis."
    })


# ==============================================================================
# Slide 24: Engineering Quality, Testing & Reproducibility
# ==============================================================================

def build_slide_24(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "23 // SOFTWARE ENGINEERING",
        "Software Engineering Standards, Testing & Reproducibility",
        "Verification suite, CI/CD automated gates, Docker containerization, and forensic provenance."
    )

    pillars = [
        ("47 PASSING AUTOMATED TESTS", ALERT_GREEN,
         "100% Pytest Coverage Suite",
         "Automated test suite (pytest -v) executes 47 tests across CLI commands (10), clinical dossiers (1), disease matching rules (21), database integrity (9), and statistical calculations (6).\n\nExecuted in 54.12s on Python 3.13.13 with zero failures and zero warnings."),
        ("DOCKER & CI/CD GATES", CYAN_ACCENT,
         "Self-Contained Containerization",
         "Standardized multi-stage Dockerfile packaging Python 3.13 runtime, SQLite relational warehouse, and Streamlit dashboard.\n\nGitHub Actions CI/CD workflows enforce automated linting, test suite execution, and SHA-256 integrity validation upon every commit."),
        ("CRYPTOGRAPHIC PROVENANCE", PURPLE_ACCENT,
         "Forensic Data Integrity",
         "Every ingested external dataset (ClinGen, ClinVar, PanelApp, gnomAD) is hashed with SHA-256 upon arrival.\n\nDatabase migration scripts are strictly idempotent; transaction rollbacks prevent partial database writes on network failures."),
        ("TRANSPARENT ROADMAP", ALERT_AMBER,
         "Proposed Future Enhancements",
         "Phase 2 Engineering Milestones:\n• Longitudinal Survival Analysis: Reconstructing historical ClinVar XML releases to compute true time-to-resolution.\n• Hierarchical Ontology Expansion: Semi-automated mapping of broad phenotype terms to boost recall."),
    ]

    cards = []
    w = 2.76
    gap = 0.23
    for i, (tag, col, title, desc) in enumerate(pillars):
        left = 0.8 + i * (w + gap)
        c = add_card(slide, left, 1.85, w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.12), Inches(2.05), Inches(w - 0.24), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 24)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 24 highlights the software engineering rigor behind CuraCascade. A research project is only as good as its code quality. We built a comprehensive pytest test suite comprising 47 unit and integration tests. All 47 tests pass in 54 seconds on Python 3.13, validating everything from command-line arguments to database foreign key enforcement and Wilson score confidence interval math. The entire platform is containerized using Docker, and our GitHub Actions pipeline validates every commit. We also maintain a transparent engineering roadmap, including longitudinal ClinVar XML parsing to measure true historical time-to-resolution.",
        "concept": "Idempotent migrations mean you can run the database setup script ten times in a row, and it will produce the exact same clean database without errors or duplicated data.",
        "takeaway": "CuraCascade adheres to production software engineering standards: 47 passing tests, Docker containerization, SHA-256 provenance, and CI/CD automation.",
        "guardrail": "Be transparent that longitudinal ClinVar XML parsing is on the future roadmap, not yet implemented in the current repository.",
        "question": "What is the biggest technical challenge you faced while implementing the test suite?",
        "answer": "Ensuring that the label firewall was strictly maintained without test contamination, and verifying that multi-disease pleiotropic genes like MLH1 and FBN1 never raised false-positive discrepancy alerts when evaluated against distinct clinical indications."
    })


# ==============================================================================
# Slide 25: Conclusion & Viva Defense Q&A
# ==============================================================================

def build_slide_25(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "24 // CONCLUSION & DEFENSE",
        "Conclusion, Project Summary & Academic Defense Q&A",
        "Closing synthesis of scientific contributions, verified deliverables, and committee Q&A."
    )

    # Left Card: Summary of Academic Contributions
    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CORE SCIENTIFIC CONTRIBUTIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    takeaways = [
        ("Evidence-to-Practice Synchronization",
         "Quantified an empirical propagation lag of 2.82 years (up to 9.9 years) across 51,007 assertions, demonstrating a systemic data synchronization gap in clinical genomics."),
        ("Zero False Alarms (100.0% Precision)",
         "Validated on an independent 100-gene benchmark (94 evaluable cases), achieving 100% precision with zero false alarms raised against definitive clinical controls."),
        ("Disease-Aware Ontology Architecture",
         "Engineered a 3-tier MONDO-to-MedGen crosswalk that successfully prevents false-positive alerts on pleiotropic multi-disease genes like ACTN2 and SCN1B."),
        ("Open-Source Reproducibility",
         "Delivered an open-source, containerized system with 47 passing tests, full SHA-256 provenance logging, and a live web deployment at curacascadev2.streamlit.app."),
    ]
    for title, desc in takeaways:
        p = tf1.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf1.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    # Right Card: Viva Defense Links & Invitation
    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "PROJECT DELIVERABLES & DEFENSE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN

    p = tf2.add_paragraph()
    p.text = "All project assets are publicly accessible and verified:"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    links = [
        ("Live Web Application", "https://curacascadev2.streamlit.app/"),
        ("Source Code Repository", "https://github.com/uditshokeen14/curacascadeV2"),
        ("Project Report", "CuraCascade IEEE Format Publication Report (PDF)"),
        ("Verification Test Suite", "47 Passing Pytest Assertions (Python 3.13)"),
    ]
    for lbl, val in links:
        p = tf2.add_paragraph()
        p.text = f"• {lbl}:\n  {val}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(6)

    p = tf2.add_paragraph()
    p.text = "─────────────────────────────────────────────────────"
    p.font.size = Pt(8)
    p.font.color.rgb = SURFACE_BORDER
    p.space_before = Pt(8)

    p = tf2.add_paragraph()
    p.text = "Thank you for your time and evaluation.\nI welcome questions from the committee."
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY
    p.space_before = Pt(8)

    add_footer(slide, 25)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "In conclusion, CuraCascade addresses a critical, silent failure mode in modern clinical genomics: the evidence synchronization gap. By linking upstream expert validity curations with downstream variant assertions and diagnostic panels, our system prevents stale gene associations from persisting in diagnostic pipelines. We demonstrated 100% precision on an independent 100-gene benchmark, proved our disease-aware crosswalk across 12 pleiotropic gene families, and quantified an overall evidence propagation lag of 2.82 years across 51,000 assertions. The code is fully tested with 47 passing tests and deployed live at curacascadev2.streamlit.app. Thank you for your time and evaluation. I am now ready to answer questions from the committee.",
        "concept": "The conclusion restates the core achievements, thanks the examiners, and invites questions with confidence.",
        "takeaway": "CuraCascade delivers an academically rigorous, empirically verified, and open-source solution to clinical evidence synchronization.",
        "guardrail": "Deliver your final sentence clearly and confidently. Do not rush off the podium.",
        "question": "What is the single most important lesson you learned while building this project?",
        "answer": "That in biomedical informatics, domain knowledge is everything. A naive computer science approach that joins tables by gene symbol alone fails completely on pleiotropic genes. Building software for medicine requires understanding disease ontologies, clinical guidelines, and conservative decision-making."
    })


# ==============================================================================
# Main Presentation Builder Execution
# ==============================================================================

def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("=" * 80)
    print("🎨 GENERATING CURACASCADE V2 MASTER 25-SLIDE DEFENSE PRESENTATION")
    print("=" * 80)

    slides_builders = [
        (1, "Title & Academic Identity", build_slide_1),
        (2, "Executive Summary", build_slide_2),
        (3, "The Real-World Clinical Problem", build_slide_3),
        (4, "Biomedical Foundations I (DNA/Genes/Variants)", build_slide_4),
        (5, "Biomedical Foundations II (Gene vs Variant Validity)", build_slide_5),
        (6, "The Fragmented Data Ecosystem", build_slide_6),
        (7, "Why Evidence Disagrees (Root Causes)", build_slide_7),
        (8, "Existing Workflows & Research Gap", build_slide_8),
        (9, "Project Objectives & Scope", build_slide_9),
        (10, "Contributions & Research Questions", build_slide_10),
        (11, "End-to-End 5-Stage Audit Pipeline", build_slide_11),
        (12, "System Architecture: Dual Engine", build_slide_12),
        (13, "Relational Schema & 3NF Design", build_slide_13),
        (14, "Data Ingestion & Provenance", build_slide_14),
        (15, "Disease-Aware Matching Heuristics", build_slide_15),
        (16, "Live Application Overview", build_slide_16),
        (17, "Audit Findings Explorer", build_slide_17),
        (18, "Evidence Traceability & Remediation", build_slide_18),
        (19, "Worked Clinical Case Studies", build_slide_19),
        (20, "100-Gene Benchmark Methodology", build_slide_20),
        (21, "Quantitative Benchmark Results", build_slide_21),
        (22, "Error Analysis & 34 False Negatives", build_slide_22),
        (23, "Exploratory ML & Latency Kinetics", build_slide_23),
        (24, "Engineering Quality & Testing", build_slide_24),
        (25, "Conclusion & Defense Q&A", build_slide_25),
    ]

    for num, name, builder in slides_builders:
        print(f"  • Building Slide {num:02d}: {name}...")
        builder(prs)

    out_pptx = PROJECT_ROOT / "CuraCascade_Presentation_V2_25Slides.pptx"
    docs_pptx = PROJECT_ROOT / "docs" / "CuraCascade_Presentation_V2_25Slides.pptx"
    redesigned_pptx = PROJECT_ROOT / "CuraCascade_Presentation_Redesigned.pptx"
    docs_redesigned = PROJECT_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.pptx"

    prs.save(str(out_pptx))
    prs.save(str(docs_pptx))
    prs.save(str(redesigned_pptx))
    prs.save(str(docs_redesigned))

    print("\n✅ 25-Slide Master PowerPoint Presentation successfully saved to:")
    print(f"   1. {out_pptx}")
    print(f"   2. {docs_pptx}")
    print(f"   3. {redesigned_pptx}")
    print(f"   4. {docs_redesigned}")


if __name__ == "__main__":
    main()
