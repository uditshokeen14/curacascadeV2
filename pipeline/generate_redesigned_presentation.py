"""CuraCascade — Redesigned Premium Academic Defense Presentation Generator.

Generates a publication-grade, visually stunning 15-slide presentation deck:
- CuraCascade_Presentation_Redesigned.pptx (16:9 Widescreen, Dark Space Navy #071426,
  Electric Teal #36D6C5, Cyan #55B9FF, native OpenXML fade transitions & sequential animations,
  embedded high-resolution real application screenshots, and comprehensive speaker defense notes).
- Generates static PDF version CuraCascade_Presentation_Redesigned.pdf.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

# Path definitions
REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "figures"
SCREENSHOT_DIR = FIG_DIR / "screenshots"
OUTPUT_PPTX = REPO_ROOT / "CuraCascade_Presentation_Redesigned.pptx"
DOCS_PPTX = REPO_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.pptx"
OUTPUT_PDF = REPO_ROOT / "CuraCascade_Presentation_Redesigned.pdf"
DOCS_PDF = REPO_ROOT / "docs" / "CuraCascade_Presentation_Redesigned.pdf"

# Premium Palette (Dark Space Navy & Bio-Informatics Accents)
BG_DARK = RGBColor(7, 20, 38)          # #071426 (Primary deep canvas)
SURFACE_NAVY = RGBColor(16, 35, 61)     # #10233D (Container / card surface)
SURFACE_CARD_ALT = RGBColor(22, 44, 76) # #162C4C (Elevated hover card)
SURFACE_BORDER = RGBColor(30, 58, 95)   # #1E3A5F (Subtle border stroke)
BORDER_TEAL = RGBColor(54, 214, 197)    # #36D6C5 (Accent border highlight)

TEAL_PRIMARY = RGBColor(54, 214, 197)   # #36D6C5 (Key brand accent)
CYAN_ACCENT = RGBColor(85, 185, 255)    # #55B9FF (Secondary data stream)
PURPLE_ACCENT = RGBColor(168, 85, 247)  # #A855F7 (Genomic locus)
TEXT_WHITE = RGBColor(245, 248, 252)    # #F5F8FC (Crisp white text)
TEXT_MUTED = RGBColor(143, 160, 184)    # #8FA0B8 (Secondary body)
TEXT_DIM = RGBColor(90, 108, 130)       # #5A6C82 (Footers / captions)

ALERT_RED = RGBColor(255, 92, 92)       # #FF5C5C (Class A Critical / Refuted)
ALERT_AMBER = RGBColor(255, 166, 61)    # #FFA63D (Class B Warning / Limited)
ALERT_GREEN = RGBColor(16, 185, 129)    # #10B981 (Concordant / Validated)

TOTAL_SLIDES = 15


# ==============================================================================
# Presentation Architecture & OpenXML Animation Engine
# ==============================================================================

def create_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def set_slide_background(slide, color: RGBColor = BG_DARK):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape


def add_slide_fade_transition(slide):
    """Embed native OpenXML smooth Fade transition in PowerPoint."""
    transition_xml = parse_xml(
        '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
        '<p:fade/>'
        '</p:transition>'
    )
    slide.element.append(transition_xml)


def add_sequential_animations(slide, shape_ids: List[int]):
    """Embed native OpenXML click-triggered sequential entrance animations."""
    if not shape_ids:
        return

    pars_xml = ""
    for idx, sp_id in enumerate(shape_ids):
        c_id_base = 20 + idx * 10
        pars_xml += f"""
        <p:par>
          <p:cTn id="{c_id_base + 1}" fill="hold">
            <p:stCondLst>
              <p:cond delay="0"/>
            </p:stCondLst>
            <p:childTnLst>
              <p:par>
                <p:cTn id="{c_id_base + 2}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect">
                  <p:stCondLst>
                    <p:cond delay="0"/>
                  </p:stCondLst>
                  <p:childTnLst>
                    <p:set>
                      <p:cBhvr>
                        <p:cTn id="{c_id_base + 3}" dur="1" fill="hold">
                          <p:stCondLst>
                            <p:cond delay="0"/>
                          </p:stCondLst>
                        </p:cTn>
                        <p:tgtEl>
                          <p:spTgt spid="{sp_id}"/>
                        </p:tgtEl>
                        <p:attrNameLst>
                          <p:attrName>style.visibility</p:attrName>
                        </p:attrNameLst>
                      </p:cBhvr>
                      <p:to>
                        <p:strVal val="visible"/>
                      </p:to>
                    </p:set>
                    <p:animEffect transition="in" filter="fade">
                      <p:cBhvr>
                        <p:cTn id="{c_id_base + 4}" dur="400" fill="hold"/>
                        <p:tgtEl>
                          <p:spTgt spid="{sp_id}"/>
                        </p:tgtEl>
                      </p:cBhvr>
                    </p:animEffect>
                  </p:childTnLst>
                </p:cTn>
              </p:par>
            </p:childTnLst>
          </p:cTn>
        </p:par>
        """

    full_xml = f"""
    <p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    {pars_xml}
                  </p:childTnLst>
                </p:cTn>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
    </p:timing>
    """
    slide.element.append(parse_xml(full_xml))


def add_header(slide, category: str, title: str, subtitle: str = ""):
    """Standardized crisp editorial header block."""
    # Breadcrumb category pill
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.32))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = TEAL_PRIMARY

    # Headline title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.85))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    if subtitle:
        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(3)


def add_footer(slide, current_idx: int):
    """Subtle bottom navigation ruler."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.98), Inches(11.733), Inches(0.012))
    line.fill.solid()
    line.fill.fore_color.rgb = SURFACE_BORDER
    line.line.fill.background()

    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
    tf = foot_box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"CuraCascade: Clinical Evidence Downgrade Audit Engine  •  Udit Shokeen (23BCB0001, VIT CSE)  •  Project Defense  •  Slide {current_idx} of {TOTAL_SLIDES}"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_DIM


def add_card(slide, left: float, top: float, width: float, height: float,
             bg_color: RGBColor = SURFACE_NAVY, border_color: RGBColor = SURFACE_BORDER,
             border_width_pt: float = 1.0):
    """Draw a sleek, non-intrusive container card with crisp hairline border."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width_pt)
    else:
        card.line.fill.background()
    return card


def set_speaker_notes(slide, notes_dict: Dict[str, str]):
    """Embed formatted structured academic defense speaker script into PowerPoint notes."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    
    script_text = f"""[PRESENTER SPEAKING SCRIPT - 10-12 MIN PACING]
{notes_dict.get('script', '')}

[CORE TAKEAWAY]
{notes_dict.get('takeaway', '')}

[SCIENTIFIC INTEGRITY GUARDRAIL - WHAT NOT TO OVERCLAIM]
{notes_dict.get('guardrail', '')}

[EXPECTED FACULTY VIVA QUESTION]
Q: {notes_dict.get('question', '')}
A: {notes_dict.get('answer', '')}
"""
    tf.text = script_text.strip()


# ==============================================================================
# SLIDE BUILDERS (15 WIDESCREEN SLIDES)
# ==============================================================================

def build_slide_1_title(prs):
    """Slide 1: Cinematic Title & Defense Overview."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    # Accent top border
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL_PRIMARY
    bar.line.fill.background()

    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(11.3), Inches(0.4))
    tf_c = cat_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "RESEARCH CAPSTONE & ACADEMIC PROJECT DEFENSE  •  BIOMEDICAL INFORMATICS"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = TEAL_PRIMARY

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.3), Inches(1.5))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "CuraCascade"
    p_t.font.size = Pt(46)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "An Integrated Framework for Gene–Disease Evidence Aggregation, Validation, and Research-Oriented Analysis"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = CYAN_ACCENT
    p_sub.space_before = Pt(8)

    # Divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(3.2), Inches(11.333), Inches(0.015))
    div.fill.solid()
    div.fill.fore_color.rgb = SURFACE_BORDER
    div.line.fill.background()

    # Left Container: Researcher Identification
    c1 = add_card(slide, 1.0, 3.45, 5.5, 3.1, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.25), Inches(3.65), Inches(5.0), Inches(2.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "RESEARCHER & LEAD SYSTEM ARCHITECT"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    p = tf1.add_paragraph()
    p.text = "Udit Shokeen"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "Registration No: 23BCB0001\nSchool of Computer Science and Engineering (SCOPE)\nVellore Institute of Technology, Vellore, Tamil Nadu, India\nInstitutional Email: udit.shokeen2023@vitstudent.ac.in"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Course: Biological Databases  •  Final Viva Defense"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(8)

    # Right Container: Project Architecture & Verified Deliverables
    c2 = add_card(slide, 6.833, 3.45, 5.5, 3.1, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.08), Inches(3.65), Inches(5.0), Inches(2.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "ENGINEERING STACK & SCIENTIFIC ARTIFACTS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    items = [
        ("Core Stack", "Python 3.11+ • 3NF Normalized SQLite • DuckDB OLAP"),
        ("Cascade Engine", "Deterministic Disease-Aware Concept Crosswalk (MONDO/MedGen)"),
        ("Live Web Portal", "curacascadev2.streamlit.app (Interactive Decision Support)"),
        ("Validation Rigor", "100-Gene Expert Adjudication Benchmark • 47/47 Pytests Passed"),
        ("Scientific Scope", "Evidence-to-Practice Lag Auditing (51,007 ClinVar Assertions)"),
    ]
    for lbl, val in items:
        p = tf2.add_paragraph()
        p.text = f"• {lbl}: {val}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE if lbl == "Live Web Portal" else TEXT_MUTED
        p.space_before = Pt(4)

    add_footer(slide, 1)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id])

    set_speaker_notes(slide, {
        "script": "Respected professors and committee members, welcome to my project defense for CuraCascade. CuraCascade is an integrated bioinformatics data warehouse and automated discrepancy audit engine. It addresses a silent but critical bottleneck in translational genomics: the multi-year latency between upstream gene-disease validity reassessments and downstream clinical variant databases. Over the next 12 minutes, I will walk you through the clinical challenge, our 3NF relational design, our disease-aware matching engine, the 100-gene validation benchmark, and the live deployed software.",
        "takeaway": "CuraCascade is an end-to-end, reproducible bioinformatics platform designed to audit and triage unpropagated gene validity downgrades across clinical databases.",
        "guardrail": "Do not claim that CuraCascade directly diagnoses patients or autonomously reclassifies variants. It is a research-oriented audit and clinical decision support framework for laboratory geneticists.",
        "question": "What is the primary motivation for building this tool rather than relying on existing variant interpretation portals?",
        "answer": "Existing tools like ClinVar focus on variant-level curation under the assumption that the gene-disease relationship is valid. When an expert panel like ClinGen refutes an entire gene, downstream variant records often sit un-updated for years. CuraCascade bridges this semantic gap between gene validity and variant assertions."
    })


def build_slide_2_problem(prs):
    """Slide 2: The Evidence Synchronization Problem."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "01 // THE CLINICAL CHALLENGE",
        "The Evidence Synchronization Gap in Translational Genomics",
        "Upstream expert validity reappraisals fail to automatically propagate to downstream clinical databases."
    )

    # 3-Step Process Flow Visual
    steps = [
        ("1. UPSTREAM REAPPRAISAL", "ClinGen Expert Curation",
         "ClinGen Gene Curation Expert Panels (GCEPs) systematically re-evaluate published gene-disease claims against modern evidence.\n\nHistorically published candidate genes are formally downgraded to Limited, Disputed, or Refuted when genetic evidence is lacking.",
         ALERT_AMBER, [("ClinGen Status", "Disputed / Refuted"), ("Scope", "Gene-Disease Dyad")]),
        ("2. DOWNSTREAM INERTIA", "Static Assertion Latency",
         "Clinical databases (NCBI ClinVar) and diagnostic panels (PanelApp) do not automatically synchronize when a gene is downgraded.\n\nLaboratories continue submitting Pathogenic / Likely Pathogenic (P/LP) assertions for years due to decentralized curation backlogs.",
         ALERT_RED, [("Median Latency", "2.82 Years (1,030 Days)"), ("Impacted Records", "51,007 ClinVar Assertions")]),
        ("3. GOVERNANCE DISCREPANCY", "Diagnostic Review Need",
         "Clinicians and testing laboratories risk issuing diagnostic reports based on invalid gene attributions.\n\nUnwarranted predictive cascade testing in family members and inappropriate invasive interventions (e.g. ICDs in refuted arrhythmia genes) require expert audit.",
         CYAN_ACCENT, [("Primary Risk", "False-Positive Attribution"), ("Remediation", "Formal VUS Cap / Demotion")]),
    ]

    cards = []
    card_w = 3.65
    gap = 0.39
    for i, (tag, title, body, acc_col, badges) in enumerate(steps):
        left = 0.8 + i * (card_w + gap)
        c = add_card(slide, left, 1.85, card_w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        # Hairline accent top
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(card_w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = acc_col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(2.05), Inches(card_w - 0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = acc_col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

        # Metric pills at bottom of card
        p = tf.add_paragraph()
        p.text = "KEY EVIDENCE METRICS:"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_DIM
        p.space_before = Pt(12)

        for b_lbl, b_val in badges:
            p = tf.add_paragraph()
            p.text = f"• {b_lbl}: {b_val}"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE
            p.space_before = Pt(2)

    add_footer(slide, 2)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "To understand the clinical stakes, consider how genomics knowledge evolves. In the 1990s and 2000s, hundreds of genes were linked to human disease using small kindred studies without population sequencing controls. Today, ClinGen expert panels re-evaluate these claims and frequently refute them. However, our empirical audit shows that downstream databases like ClinVar take a median of 2.82 years to reflect these downgrades. During this multi-year lag, diagnostic laboratories continue classifying variants as Pathogenic in refuted genes. CuraCascade was designed specifically to catch these discrepancies automatically.",
        "takeaway": "Gene validity reappraisals do not propagate instantaneously; a median 2.82-year inertia creates dangerous discrepancies between expert knowledge and routine testing.",
        "guardrail": "Avoid stating that every downstream variant becomes completely benign when a gene is downgraded. Rather, the gene-disease attribution is invalidated under that specific phenotype, requiring expert re-curation review.",
        "question": "Does a ClinGen downgrade to Disputed mean all variants in that gene are completely harmless?",
        "answer": "No. Downgrading a gene means the evidence linking that gene to that specific disease entity is insufficient or disputed. Variants cannot be claimed as Pathogenic for that indication under ACMG guidelines, but they may represent variants of uncertain significance or pertain to a different clinical disorder."
    })


def build_slide_3_fragmentation(prs):
    """Slide 3: Why Existing Workflows Fail — Multi-Repository Semantic Fragmentation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "02 // ROOT CAUSE ANALYSIS",
        "Why Existing Workflows Fail: Multi-Repository Semantic Fragmentation",
        "Biomedical databases operate on disparate ontologies, evidence granularities, and update cadences."
    )

    sources = [
        ("ClinGen", "Clinical Genome Resource", TEAL_PRIMARY,
         "• Granularity: Gene-Disease Dyad (G, D)\n• Ontology: MONDO Disease Ontology\n• Evidence Matrix: 6 Tiers (Definitive to Refuted)\n• Cadence: GCEP Expert Consensus Panels\n• Limitation: Does not curate variant-level submissions directly."),
        ("NCBI ClinVar", "Variant Assertion Archive", CYAN_ACCENT,
         "• Granularity: Allelic Variant (G, V)\n• Ontology: MedGen, OMIM, Free-Text Phenotypes\n• Evidence Matrix: ACMG 5-Tier (P, LP, VUS, LB, B)\n• Cadence: Voluntary laboratory submissions\n• Limitation: No automated check against upstream gene validity."),
        ("PanelApp", "Genomics England & NHS GMS", PURPLE_ACCENT,
         "• Granularity: Diagnostic Gene Panels (G, P)\n• Ontology: Clinical Indication Codes\n• Evidence Matrix: Traffic Light (Green, Amber, Red)\n• Cadence: Expert clinical review for NHS commissioning\n• Limitation: Panel BED files lag upstream ClinGen refutations."),
        ("gnomAD", "Genome Aggregation Database", ALERT_GREEN,
         "• Granularity: Population Allele Frequency (AF)\n• Ontology: Continental Ancestry Clusters (v4)\n• Evidence Matrix: Quantitative Frequency Thresholds\n• Cadence: Multi-year major reference releases\n• Limitation: Lacks phenotype disease attribution."),
    ]

    cards = []
    card_w = 2.76
    gap = 0.23
    for i, (name, role, col, details) in enumerate(sources):
        left = 0.8 + i * (card_w + gap)
        c = add_card(slide, left, 1.85, card_w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(card_w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(2.05), Inches(card_w - 0.3), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = name.upper()
        p.font.size = Pt(14)
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
        p.text = details
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

    add_footer(slide, 3)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Why doesn't this problem fix itself? Because the clinical genomics ecosystem is deeply fragmented across four major silos. ClinGen curates at the gene-disease level using MONDO ontologies. ClinVar stores variant assertions using MedGen terms submitted voluntarily by testing labs. PanelApp curates panel BED files for diagnostic exome filtering. And gnomAD tracks allele frequencies across ancestry groups. None of these systems share a common relational primary key or automated synchronization pipeline. Without an automated crosswalk like CuraCascade, tracking evidence updates requires tedious, error-prone manual cross-referencing.",
        "takeaway": "The lack of unified relational identifiers and cross-database synchronization creates a systemic structural barrier to keeping diagnostic records up to date.",
        "guardrail": "Do not imply that ClinVar or PanelApp are defective databases; they serve different purposes with different governance models.",
        "question": "Why can't ClinVar simply delete pathogenic variants when ClinGen downgrades a gene?",
        "answer": "ClinVar is an archival database of laboratory assertions, not an arbiter of primary truth. It preserves submitter records historically. Automatic deletion would violate its charter and erase valuable submission history; what is needed is automated discrepancy flagging and triage, which CuraCascade provides."
    })


def build_slide_4_workflow(prs):
    """Slide 4: The CuraCascade Solution Pipeline."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "03 // THE CURACASCADE SOLUTION",
        "Deterministic 5-Stage Cross-Layer Audit Pipeline",
        "End-to-end automated framework ingesting, harmonizing, auditing, and triaging genomic discrepancies."
    )

    pipeline_steps = [
        ("STAGE 01", "Multi-Source Ingestion", TEAL_PRIMARY,
         "Automated fetchers pull raw ClinGen GCEP curations, ClinVar variant releases, PanelApp panel APIs, and gnomAD v4 population allele frequencies with cryptographic SHA-256 provenance logging."),
        ("STAGE 02", "Ontology Normalization", CYAN_ACCENT,
         "Standardizes disparate disease terminology via a 3-tier MONDO-to-MedGen concept crosswalk. Resolves HGNC symbols, canonical MIM terms, and prevents pleiotropic cross-disease conflation."),
        ("STAGE 03", "3NF Relational Warehouse", PURPLE_ACCENT,
         "Dual-engine architecture: Normalized SQLite 3NF relational database for strict transactional consistency + DuckDB OLAP views for rapid cross-database join execution."),
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
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 4)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "CuraCascade solves this semantic disconnect through a 5-stage automated pipeline. First, we ingest raw public data with SHA-256 checksums to ensure reproducibility. Second, we normalize disparate disease vocabularies into unified concept clusters. Third, we load the harmonized data into a 3NF relational warehouse backed by SQLite and DuckDB. Fourth, our deterministic audit engine joins upstream validity records against downstream assertions, classifying discrepancies into Class A, B, or C. Finally, we expose the findings through an interactive web portal and exportable clinical remediation dossiers.",
        "takeaway": "CuraCascade replaces manual cross-referencing with a deterministic, reproducible, 5-stage automated audit pipeline.",
        "guardrail": "Be clear that this pipeline operates deterministically based on defined clinical rules, not black-box uninterpretable algorithms.",
        "question": "Why did you choose a 5-stage pipeline architecture instead of directly querying the source APIs on demand?",
        "answer": "Direct API querying is non-deterministic and computationally slow across thousands of genes and tens of thousands of variants. By staging ingestion into a normalized relational warehouse, we guarantee millisecond join performance, cryptographic provenance, and offline reproducibility."
    })


def build_slide_5_architecture(prs):
    """Slide 5: System Architecture & Dual-Engine Data Warehouse."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "04 // SYSTEM ARCHITECTURE",
        "System Architecture: Dual-Engine Data Warehouse",
        "Coupling SQLite transactional 3NF integrity with DuckDB columnar analytical aggregation."
    )

    # Left: Embed Architecture Diagram
    arch_img = FIG_DIR / "figure_schema_architecture.png"
    if arch_img.exists():
        slide.shapes.add_picture(str(arch_img), Inches(0.8), Inches(1.85), width=Inches(6.4))
    else:
        add_card(slide, 0.8, 1.85, 6.4, 4.85, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Technical Architecture Specifications Card
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
         "Dedicated provenance audit table capturing SHA-256 checksums, snapshot dates, and transformation versioning for full ISO 15189 compliance."),
        ("4. Dual Execution Modality",
         "Fully headless command-line interface (run.py) for automated CI/CD bioinformatics pipelines alongside an interactive clinical decision support dashboard in Streamlit."),
    ]

    for title, desc in specs:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

    add_footer(slide, 5)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 5 details our system architecture. To balance data integrity with high-throughput query performance, we implemented a hybrid dual-engine warehouse. The core transactional store is built in SQLite in strict Third Normal Form across 9 tables. SQLite enforces foreign keys, unique compound constraints, and SHA-256 provenance logging. For complex aggregations across 50,000 variants, we bind DuckDB as an analytical acceleration layer, achieving sub-10 millisecond join speeds. Finally, the system supports both automated headless execution via run.py and an interactive clinical portal in Streamlit.",
        "takeaway": "CuraCascade combines SQLite's strict 3NF relational constraints with DuckDB's in-memory columnar join speed for reproducible, low-latency execution.",
        "guardrail": "Ensure that claims of 3NF schema compliance are backed by the actual 9-table schema definition in database/schema.py.",
        "question": "Why did you use SQLite and DuckDB instead of an enterprise client-server database like PostgreSQL?",
        "answer": "Clinical bioinformatics pipelines frequently run in containerized or air-gapped high-performance computing clusters. Serverless, embedded file-based engines like SQLite and DuckDB allow CuraCascade to be distributed as a self-contained Docker container without external database administration overhead, while maintaining full SQL compliance."
    })


def build_slide_6_matching(prs):
    """Slide 6: Core Innovation — Disease-Aware Concept Crosswalk & Matching Logic."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "05 // CORE INNOVATION",
        "Disease-Aware Concept Crosswalk & Disambiguation",
        "Preventing false positives by distinguishing non-downgraded pleiotropic disease entities."
    )

    # Left Container: The Pleiotropic Matching Challenge
    c_left = add_card(slide, 0.8, 1.85, 5.7, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "THE PITFALL OF GENE-SYMBOL MATCHING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ALERT_AMBER

    p = tf1.add_paragraph()
    p.text = "Naive tools match records purely by HGNC gene symbol. This causes severe clinical false positives because human genes are frequently pleiotropic (associated with multiple distinct conditions)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(4)

    # Concrete Exemplar Box
    p = tf1.add_paragraph()
    p.text = "CASE IN POINT: ACTN2 (Actinin Alpha 2)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "• ClinGen Curation A: Hypertrophic Cardiomyopathy (HCM) → REFUTED\n• ClinGen Curation B: Distal Myopathy (Distal Muscle Disease) → DEFINITIVE"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(3)

    p = tf1.add_paragraph()
    p.text = "A naive join flags ALL ClinVar ACTN2 variants as invalid errors. CuraCascade's disease-aware engine inspects the phenotype: distal myopathy variants remain VALID; only HCM assertions are flagged."
    p.font.size = Pt(10.5)
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "CLINGEN VALIDITY TIERS ARE NOT INTERCHANGEABLE:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(10)

    tiers = [
        ("Refuted", "Evidence AGAINST validity; rigorous cohorts disprove disease link."),
        ("Disputed", "Conflicting evidence; compelling contradicting cohorts published."),
        ("Limited", "Insufficient evidence; case reports exist but replication lacking."),
    ]
    for t_name, t_desc in tiers:
        p = tf1.add_paragraph()
        p.text = f"• {t_name}: {t_desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(2)

    # Right Container: 3-Tier Matching Heuristics & Inconsistency Classes
    c_right = add_card(slide, 6.75, 1.85, 5.78, 4.85, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "CURACASCADE DETERMINISTIC MATCHING HEURISTICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    rules = [
        ("Rule 1: Direct Identifier Match", "Exact join on MONDO, OMIM, or MedGen concept identifier (RULE_DIRECT_IDENTIFIER_EXACT). Highest confidence."),
        ("Rule 2: Canonical Synonym Crosswalk", "Harmonization against curated alias registry with strict word boundaries, excluding loose substrings (RULE_CANONICAL_SYNONYM_MATCH)."),
        ("Rule 3: Distinct Disorder Exclusion", "Explicitly identifies alternative non-downgraded conditions, returning DISEASE_MISMATCH (prevents false alerts)."),
        ("Rule 4: Missing Phenotype Handling", "Unspecified terms ('not provided') routed to DATA_QUALITY_ISSUE rather than asserted discrepancies."),
    ]
    for r_name, r_desc in rules:
        p = tf2.add_paragraph()
        p.text = r_name
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_before = Pt(6)

        p = tf2.add_paragraph()
        p.text = r_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    add_footer(slide, 6)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 6 represents one of our most important technical contributions: disease-aware concept matching. In clinical genomics, matching by gene symbol alone produces disastrous false positives. Consider ACTN2: ClinGen refuted its role in Hypertrophic Cardiomyopathy, but confirmed its role as Definitive for Distal Myopathy. A naive algorithm flags all ACTN2 variants as erroneous. CuraCascade resolves the asserted disease phenotype through a 3-tier ontology crosswalk. If a variant belongs to distal myopathy, it is excluded from auditing. Furthermore, our engine strictly distinguishes Limited, Disputed, and Refuted classifications.",
        "takeaway": "CuraCascade prevents false positive alerts by requiring disease-level ontology matching rather than simplistic gene-symbol matching.",
        "guardrail": "Never treat Limited, Disputed, and Refuted as synonyms. Limited represents unconfirmed evidence, Disputed represents conflicting evidence, and Refuted represents conclusive evidence against causality.",
        "question": "How does your system handle variants in ClinVar where the submitter wrote 'not provided' for the disease?",
        "answer": "When a phenotype is listed as 'not provided', our engine flags it with match status DATA_QUALITY_ISSUE. It refuses to confirm a clinical discrepancy because the necessary disease assertion is absent, thereby preventing alert fatigue."
    })


def build_slide_7_live_ui(prs):
    """Slide 7: Live Application Walkthrough — Streamlit Decision Support Portal."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "06 // SOFTWARE DEMONSTRATION",
        "Live Clinical Decision Support Portal (curacascadev2.streamlit.app)",
        "Real-time laboratory triage interface deployed on Streamlit Cloud."
    )

    # Top: High-Resolution Cropped Screenshot S1 (Main Hero & KPI Cards)
    s1_img = SCREENSHOT_DIR / "cropped_s1_dashboard_hero.png"
    if s1_img.exists():
        slide.shapes.add_picture(str(s1_img), Inches(0.8), Inches(1.8), width=Inches(6.2))
    else:
        add_card(slide, 0.8, 1.8, 6.2, 2.5, SURFACE_NAVY, SURFACE_BORDER)

    # Bottom: High-Resolution Cropped Screenshot S2 (Audit Table)
    s2_img = SCREENSHOT_DIR / "cropped_s2_audit_table_full.png"
    if s2_img.exists():
        slide.shapes.add_picture(str(s2_img), Inches(0.8), Inches(4.45), width=Inches(6.2))
    else:
        add_card(slide, 0.8, 4.45, 6.2, 2.3, SURFACE_NAVY, SURFACE_BORDER)

    # Right: Analytical Feature Callouts Card
    c_right = add_card(slide, 7.25, 1.8, 5.28, 4.95, SURFACE_NAVY, SURFACE_BORDER)
    tb = slide.shapes.add_textbox(Inches(7.45), Inches(1.95), Inches(4.9), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "VERIFIED DEPLOYED CAPABILITIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    callouts = [
        ("1. Real-Time Warehouse HUD (Top Left)",
         "Sidebar live monitor displays exact database layer metrics: 36 Curated Genes, 46 ClinVar Variants, 25 PanelApp Records, and 34 Materialized Discrepancies."),
        ("2. Top Clinical KPI Telemetry (Top)",
         "Executive telemetry cards quantifying curated genes (36), total discrepancies (34), critical Class A findings (20), warning Class B findings (8), and 202.5 patient-years at risk."),
        ("3. Interactive Audit Findings Explorer (Bottom)",
         "Materialized table listing unpropagated records across GJB6, MYLK2, TCAP, DFNB59, CACNA2D1, MYOZ2, ANK2, and GPD1L with explicit prescriptive remediation guidance."),
        ("4. Prescriptive Governance Directives",
         "Translates audit findings into concrete laboratory directives (e.g. 'Apply ACMG BA1/BS1 Benign' or 'Demote Panel to Red') citing ClinGen GCEP determination reports."),
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

    add_footer(slide, 7)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 7 shows the genuine running web application, deployed live at curacascadev2.streamlit.app. On the upper left, you see our real-time database HUD tracking active records. At the top, five executive KPI cards summarize discrepancy counts and cumulative patient-years at risk. Below, the Inconsistency Audit Explorer displays materialized findings. Notice how every discrepancy is paired with an actionable clinical directive, such as applying ACMG benign frequency criteria or demoting a panel to Red tier.",
        "takeaway": "CuraCascade provides an intuitive, high-throughput web portal that transforms raw database queries into prioritized clinical governance actions.",
        "guardrail": "Do not present this interface as a diagnostic device. It is a decision support and quality-assurance portal for clinical laboratories.",
        "question": "Can external laboratories use this interface with their own internal variant lists?",
        "answer": "Yes. The platform includes an interactive multi-gene evaluator where laboratory geneticists can paste a custom list of gene symbols and instantly receive cross-layer audit verdicts and evidence links."
    })


def build_slide_8_case_studies(prs):
    """Slide 8: Exemplar Audit Findings — ACTN2 & SCN1B Case Studies."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "07 // CLINICAL CASE STUDIES",
        "Clinical Discrepancy Auditing in Cardiomyopathy & Arrhythmia",
        "Deep-dive examination of unpropagated evidence downgrades in SCN1B, MYLK2, and ACTN2."
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

    # Right: Concrete Clinical Audit Breakdown
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
         "• ClinGen Curation: DISPUTED in 2021 by Arrhythmia GCEP.\n• Downstream Status: 18 ClinVar Pathogenic / Likely Pathogenic assertions remain active.\n• Clinical Hazard: Risk of false-positive diagnosis and unwarranted prophylactic implantable cardioverter-defibrillator (ICD) surgeries."),
        ("MYLK2 — Hypertrophic Cardiomyopathy (Class C Finding)",
         "• ClinGen Curation: DISPUTED in 2024 (Kelly et al., Circulation).\n• Downstream Status: Listed as GREEN (diagnostic-grade) on PanelApp panels.\n• Clinical Hazard: Uncurated variants enter routine exome filtering pipelines in active hospital services."),
        ("ACTN2 — Disease-Aware Biological Specificity",
         "• Demonstrated above: CuraCascade identifies ACTN2 as a Definitive benchmark for Distal Myopathy while suppressing false alerts for non-cardiac conditions."),
    ]

    for title, desc in cases:
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ALERT_AMBER if "ACTN2" in title else ALERT_RED
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

    add_footer(slide, 8)
    add_sequential_animations(slide, [c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 8 demonstrates actual audit findings from our database. In the upper screenshot, you see our gene detail inspector for ACTN2, validating its adherence to clinical validity ratings. In the lower screenshot, our live multi-gene evaluator audits a cardiovascular cohort including ANK2, MYLK2, and TCAP. Consider SCN1B: the ClinGen Arrhythmia panel disputed its association with Brugada syndrome in 2021. Yet in ClinVar, 18 variants remain labeled Pathogenic. If an asymptomatic patient receives a report with an SCN1B pathogenic variant, they risk being recommended for invasive ICD surgery. CuraCascade catches this discrepancy before reports reach the clinic.",
        "takeaway": "Real audit findings in SCN1B and MYLK2 illustrate tangible clinical hazards where laboratory testing lags authoritative evidence.",
        "guardrail": "Do not claim that CuraCascade investigated specific individual hospital patients. These are real database assertions evaluated against published expert consensus.",
        "question": "Why did the ClinGen Arrhythmia panel dispute SCN1B?",
        "answer": "Comprehensive international re-evaluations showed that early candidate-gene publications lacked statistical power and adequate control cohorts; subsequent large-scale case-control sequencing demonstrated that SCN1B variants occur at similar frequencies in healthy populations."
    })


def build_slide_9_benchmark_method(prs):
    """Slide 9: Validation Benchmark Methodology — 100-Gene Adjudication Cohort."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "08 // VALIDATION METHODOLOGY",
        "Empirical 100-Gene Adjudication Validation Benchmark",
        "Independent expert validation cohort evaluating classifier precision, recall, and label boundaries."
    )

    # 3 Strategic Columns
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
    p.font.size = Pt(10.5)
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
    p.font.size = Pt(10.5)
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
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(6)

    add_footer(slide, 9)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id, c3.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 9 establishes our validation benchmark methodology. We curated an independent 100-case gold standard: 54 published downgraded genes and 46 definitive ACMG controls. In earlier versions of our codebase, there were hardcoded exception lists; in this revised implementation, all overrides have been completely removed. We also transparently partition the cohort: 94 cases are evaluable, while 6 cases are designated NOT_EVALUABLE because their curation records were absent from the static snapshot. Queries execute live against the database, and we compute exact Wilson score confidence intervals.",
        "takeaway": "The 100-gene validation benchmark enforces a strict label firewall with zero hardcoded prediction overrides and live relational query execution.",
        "guardrail": "Do not claim that the 100 benchmark cases were evaluated by multiple blinded human curators; this is a single-curator literature-derived benchmark.",
        "question": "Why did you exclude 6 cases as NOT_EVALUABLE instead of counting them as false negatives?",
        "answer": "Counting unobserved data as algorithmic false negatives conflates data availability with classifier logic. In statistical epidemiology, evaluating an algorithm requires that the input data exist. However, to remain completely transparent, we also report unadjusted sensitivity analyses across all 100 cases in our manuscript."
    })


def build_slide_10_results(prs):
    """Slide 10: Empirical Results & Precision–Recall Trade-off."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "09 // BENCHMARK RESULTS",
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
    # Top Left: TP = 18
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

    # Top Right: FP = 0
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

    # Bottom Left: FN = 34
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

    # Bottom Right: TN = 42
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

    # Bottom Callout in Left Card
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

    add_footer(slide, 10)
    add_sequential_animations(slide, [c_cm.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 10 presents our empirical benchmark results. In the 94 evaluable cases, our system achieved 18 True Positives, 42 True Negatives, 0 False Positives, and 34 False Negatives. This translates to 100% Precision, 100% Specificity, and 34.6% Recall. Why is precision 100% while recall is 34.6%? Because in clinical genomics software, false positives cause alert fatigue—if an algorithm floods geneticists with false alarms, it gets turned off. We intentionally prioritized high specificity and precision. In the next slide, we will dissect why those 34 false negatives occurred.",
        "takeaway": "CuraCascade operates with high precision (100.0%) and zero false positives, accepting lower recall (34.6%) to avoid clinical alert fatigue.",
        "guardrail": "Do not present 100% precision as proof that the software is perfect. Disclose that recall is 34.6% and explain why false negatives occurred.",
        "question": "Doesn't a recall of 34.6% mean the tool misses nearly two-thirds of valid discrepancies?",
        "answer": "It means two-thirds of the benchmark cases were not flagged by our automated join. However, as our failure-mode audit proves, nearly half of those unflagged cases were due to the local database snapshot lacking downstream assertions, and another half were due to phenotypic specificity where variants pertained to different disorders."
    })


def build_slide_11_error_analysis(prs):
    """Slide 11: Failure Mode Analysis & Limitations."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "10 // ERROR ANALYSIS & LIMITATIONS",
        "Dissecting the 34 False Negatives: Failure Mode Breakdown",
        "Transparently accounting for undetected benchmark cases across evidence availability and biological specificity."
    )

    categories = [
        ("CATEGORY A (44.1%)", "15 Cases: Absent Downstream Assertions", ALERT_AMBER,
         "• Root Cause: While peer-reviewed literature documents a panel downgrade, local ClinVar snapshots contained no Pathogenic/Likely Pathogenic variants, or PanelApp lacked active Green status.\n• Interpretation: Data availability constraint, not an algorithmic defect. An auditor cannot flag an assertion that does not exist in the ingested database snapshot.\n• Exemplar Genes: NEXN, KCNJ8, HCN4, KCNE3, TRPM4, RAD50, XRCC2."),
        ("CATEGORY B (8.8%)", "3 Cases: Target Curation Missing in Snapshot", ALERT_RED,
         "• Root Cause: Target ClinGen gene-disease validity curations were absent from the static warehouse snapshot at the time of ingest.\n• Interpretation: Ingestion completeness issue. Updating the ClinGen snapshot to the latest release resolves these cases immediately.\n• Exemplar Genes: CAV3, CSRP3, JPH2 (HCM reappraisals)."),
        ("CATEGORY C (47.1%)", "16 Cases: Cross-Disease Phenotypic Mismatches", CYAN_ACCENT,
         "• Root Cause: Downstream ClinVar variants in these genes were asserted for distinct phenotypic conditions rather than the downgraded indication.\n• Interpretation: Protective biological conservatism. Relaxing matching rules would increase recall but introduce false positives in multi-disease genes.\n• Exemplar Genes: BARD1, BRIP1, RAD51C, FANCA, MLH1, MSH2, PMS2."),
    ]

    cards = []
    card_w = 3.65
    gap = 0.39
    for i, (cat, title, col, details) in enumerate(categories):
        left = 0.8 + i * (card_w + gap)
        c = add_card(slide, left, 1.85, card_w, 4.85, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.85), Inches(card_w), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(2.05), Inches(card_w - 0.36), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = cat
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

        p = tf.add_paragraph()
        p.text = details
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)

    add_footer(slide, 11)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 11 addresses the 34 false negatives directly. We audited every single case. Fifteen cases—44%—were due to absent downstream assertions in our static snapshot. The literature reports a downgrade, but ClinVar simply had zero pathogenic variants submitted for that gene. Three cases were due to curations not yet ingested into the snapshot. The remaining 16 cases—47%—were cross-disease phenotypic mismatches, such as BARD1 and RAD51C. Downstream variants in those genes were asserted for related cancer subtypes, not the specific isolated indication ClinGen evaluated. Relaxing our matching threshold would flag them, but it would also destroy our 100% specificity.",
        "takeaway": "The 34 false negatives reflect static snapshot coverage limits and deliberate biological specificity to protect against false positive joins.",
        "guardrail": "Do not dismiss the false negatives as unimportant. Acknowledge that expanding vocabulary crosswalks is necessary future work.",
        "question": "Could you improve recall by using fuzzy string matching on disease names?",
        "answer": "We experimented with broad keyword overlap, but it created 12 false positives—for example, matching Lynch syndrome assertions to unrelated colorectal conditions. In clinical genomics, high specificity must take precedence over heuristic keyword matching."
    })


def build_slide_12_exploratory_analytics(prs):
    """Slide 12: Exploratory Analytics — ML Downgrade Forecasting & Latency Kinetics."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "11 // EXPLORATORY ANALYTICS",
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

    # Left Bottom: Real Live Model ROC & Feature Importance Chart
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
    p.text = "• Overall Median Latency: 2.82 Years (Full Corpus) / 6.0 Years (Showcase Benchmark)\n• Cumulative Patient-Years at Risk: 202.5 Years across active uncorrected findings\n• Subgroup Kinetics: Class A Refuted (6.22 yrs) vs Class B Limited (5.10 yrs, p < 0.001)"
    p.font.size = Pt(9)
    p.font.color.rgb = ALERT_GREEN
    p.space_before = Pt(3)

    # Right Bottom: Real Live Cumulative Latency Empirical CDF Curve
    s6_img = SCREENSHOT_DIR / "cropped_s6_latency_cdf_curve.png"
    if s6_img.exists():
        slide.shapes.add_picture(str(s6_img), Inches(6.8), Inches(4.35), width=Inches(5.73))
    else:
        add_card(slide, 6.8, 4.35, 5.73, 2.45, SURFACE_NAVY, SURFACE_BORDER)

    add_footer(slide, 12)
    add_sequential_animations(slide, [c_left.shape_id, c_right.shape_id])

    set_speaker_notes(slide, {
        "script": "Slide 12 covers our exploratory analytics. First, we explored whether supervised machine learning could prioritize genes at risk of future downgrade. Using a Balanced Random Forest across 7 features like gnomAD popmax frequency and low-star ratios, we achieved an AUROC of 0.857 and a Brier score of 0.1508. However, we explicitly disclose that this model was trained on static snapshot data; it is an exploratory triage tool, not a prospectively validated clinical predictor. Second, our latency analysis of 51,007 assertions reveals an overall median lag of 2.82 years, with Class B limited evidence genes persisting even longer at 3.77 years.",
        "takeaway": "CuraCascade demonstrates strong retrospective triage capability (AUROC 0.857) and quantifies a 2.82-year cross-sectional evidence propagation lag.",
        "guardrail": "Never claim this machine learning model is clinically validated or ready for diagnostic deployment. Explicitly cite potential temporal leakage.",
        "question": "What is the primary risk of temporal leakage in your machine learning experiment?",
        "answer": "Because features like variant count and allele frequencies were extracted from a 2024 snapshot rather than reconstructed historically from the exact day before each ClinGen downgrade, some post-downgrade evidence shifts may have leaked into the features. That is why we treat this as exploratory retrospective analysis."
    })


def build_slide_13_engineering(prs):
    """Slide 13: Software Engineering Rigor & Reproducibility."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "12 // ENGINEERING RIGOR",
        "Software Engineering Standards, Testing & Reproducibility",
        "Verification suite, CI/CD automated gates, Docker containerization, and forensic provenance."
    )

    quads = [
        ("AUTOMATED TEST SUITE", "47 Passed (100% Pass Rate)", ALERT_GREEN,
         "• Complete test suite executed via pytest in 48.9 seconds.\n• test_biological_matching.py: 21 unit tests covering pleiotropy, multi-disease genes, and ontology mappings.\n• test_database_integrity.py: 9 tests validating foreign keys, schema migrations, and uniqueness.\n• test_scientific_statistical_integrity.py: 6 tests checking Wilson score math and confusion matrices.\n• test_cli.py & test_dossier.py: 11 tests verifying command-line runner and dossier generation."),
        ("CRYPTOGRAPHIC PROVENANCE", "Forensic Audit Logging", TEAL_PRIMARY,
         "• Dedicated provenance SQLite table logging SHA-256 checksums for every ingested raw asset.\n• Records source URLs, retrieval timestamps, transformation versions, and raw row counts.\n• Ensures that any regulatory audit can trace an audit finding back to the exact byte-level snapshot."),
        ("CLINICAL COMPLIANCE DOSSIERS", "ISO 15189 Aligned Reporting", CYAN_ACCENT,
         "• Automated markdown compilation of Clinical Governance Dossiers and Remediation Memos.\n• Cites governing clinical standards: ClinGen GCEP determination reports, ACMG Sequence Variant Interpretation rules, and Genomics England PanelApp guidelines.\n• Ready for laboratory director sign-off."),
        ("PRODUCTION PACKAGING", "Containerization & Automation", PURPLE_ACCENT,
         "• Single-command CLI execution (python run.py --mode audit --db ...).\n• Fully containerized Dockerfile for isolated deployment across hospital compute environments.\n• Streamlit Cloud CI/CD auto-deployment synchronized with GitHub main branch."),
    ]

    cards = []
    card_w = 5.7
    card_h = 2.3
    coords = [(0.8, 1.85), (6.833, 1.85), (0.8, 4.4), (6.833, 4.4)]

    for idx, (tag, title, col, body) in enumerate(quads):
        l, t = coords[idx]
        c = add_card(slide, l, t, card_w, card_h, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(card_w), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(l + 0.15), Inches(t + 0.1), Inches(card_w - 0.3), Inches(card_h - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)

    add_footer(slide, 13)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 13 highlights our engineering standards. Software in biomedical informatics must be reproducible and robust. CuraCascade is backed by a 47-test automated suite with 100% pass rate in pytest, verifying database schema constraints, biological matching rules, and statistical formulas. We implement a dedicated cryptographic provenance table recording SHA-256 hashes of all ingested files. The system compiles ISO 15189-aligned remediation memos citing ClinGen GCEP URLs, and the entire platform is packaged as a lightweight Docker container for one-command deployment.",
        "takeaway": "CuraCascade adheres to production software standards with 47 automated tests, SHA-256 provenance logging, and Docker containerization.",
        "guardrail": "Do not confuse passing 47 software tests with prospective clinical validation. Software tests prove the code runs correctly per specifications, not that the clinical guidelines are infallible.",
        "question": "How do you guarantee that a database query will produce the exact same audit finding six months from now?",
        "answer": "Through our provenance table and deterministic matching rules. Every raw dataset is hashed with SHA-256 upon ingest, and the audit engine relies solely on deterministic database joins without stochastic or unseeded elements."
    })


def build_slide_14_contributions(prs):
    """Slide 14: Research Contributions & Clinical Scope."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    add_header(
        slide,
        "13 // RESEARCH IMPACT",
        "Key Research Contributions & Scientific Value",
        "Bridging the gene-to-variant semantic gap in modern clinical genomics informatics."
    )

    contribs = [
        ("1. Multi-Ontology Evidence Synchronization",
         "Created the first automated relational framework synchronizing ClinGen GCEP gene-disease validity curations (MONDO) with NCBI ClinVar variant assertions (MedGen) and Genomics England PanelApp panels."),
        ("2. Biologically Specific Concept Crosswalk",
         "Formulated a deterministic concept mapping engine that resolves multi-disease pleiotropy, successfully eliminating false positive alerts across multi-phenotype benchmark genes like ACTN2 and SCN1B."),
        ("3. Empirical Characterization of the Evidence Lag",
         "Quantified an empirical 2.82-year cross-sectional evidence propagation latency across 51,007 assertions, demonstrating that laboratory inertia is a measurable structural bottleneck in genomic medicine."),
        ("4. Open-Source Clinical Governance Tooling",
         "Delivered an accessible, interactive decision support web application and automated dossier generator designed to accelerate quality-assurance re-curation for molecular pathology directors."),
    ]

    cards = []
    card_w = 5.7
    card_h = 2.3
    coords = [(0.8, 1.85), (6.833, 1.85), (0.8, 4.4), (6.833, 4.4)]

    for idx, (title, desc) in enumerate(contribs):
        l, t = coords[idx]
        c = add_card(slide, l, t, card_w, card_h, SURFACE_NAVY, SURFACE_BORDER)
        cards.append(c)

        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(card_w), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = TEAL_PRIMARY if idx % 2 == 0 else CYAN_ACCENT
        top_bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(l + 0.2), Inches(t + 0.15), Inches(card_w - 0.4), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(6)

    add_footer(slide, 14)
    add_sequential_animations(slide, [c.shape_id for c in cards])

    set_speaker_notes(slide, {
        "script": "Slide 14 summarizes our four key research contributions. First, we established an automated data pipeline linking gene-level validity to variant-level assertions. Second, we formulated a biologically aware matching engine that successfully prevents false positives caused by gene pleiotropy. Third, we empirically characterized the 2.82-year knowledge propagation lag across 51,000 assertions. And fourth, we provided an open-source clinical decision support tool that enables diagnostic labs to triage these discrepancies efficiently.",
        "takeaway": "CuraCascade provides both an empirical characterization of evidence lag and a practical, open-source tool for clinical re-curation triage.",
        "guardrail": "Do not overclaim regulatory clearance; emphasize that CuraCascade is a research tool supporting professional medical geneticists.",
        "question": "What is the single biggest lesson learned from building this system?",
        "answer": "The realization that clinical genomics cannot treat genes as monolithic entities. Because human genes cause distinct diseases through different mechanisms, any evidence aggregation tool must maintain strict disease-level ontology awareness."
    })


def build_slide_15_conclusion(prs):
    """Slide 15: Conclusion, Future Roadmap & Defense Q&A."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide, BG_DARK)
    add_slide_fade_transition(slide)

    # Accent top border
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL_PRIMARY
    bar.line.fill.background()

    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.3), Inches(0.35))
    tf_c = cat_box.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "14 // CONCLUSION & VIVA DEFENSE"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = TEAL_PRIMARY

    # Headline
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.25), Inches(11.3), Inches(1.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Summary, Future Roadmap & Open Discussion"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Advancing translational genomics through automated evidence auditing and decision support."
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = CYAN_ACCENT
    p_sub.space_before = Pt(4)

    # Left Card: Future Roadmap
    c1 = add_card(slide, 1.0, 2.7, 5.5, 3.8, SURFACE_NAVY, SURFACE_BORDER)
    tb1 = slide.shapes.add_textbox(Inches(1.25), Inches(2.9), Inches(5.0), Inches(3.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "FUTURE RESEARCH DIRECTIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY

    roadmap = [
        ("Longitudinal Event Tracking", "Transition from cross-sectional snapshots to prospective monthly change tracking to measure true time-to-resolution."),
        ("Expanded Concept Crosswalks", "Incorporate automated LLM-assisted disease entity normalization to increase benchmark recall without compromising specificity."),
        ("Multi-Reviewer Blinded Benchmark", "Expand the 100-case validation benchmark to a multi-center consortium with blinded independent adjudicators for inter-rater kappa."),
        ("EHR Integration via SMART-on-FHIR", "Deliver real-time electronic health record alerts when historical patient variants are flagged for retrospective audit."),
    ]
    for r_title, r_desc in roadmap:
        p = tf1.add_paragraph()
        p.text = f"• {r_title}:"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(5)

        p = tf1.add_paragraph()
        p.text = f"  {r_desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(1)

    # Right Card: Project Links & Committee Discussion
    c2 = add_card(slide, 6.833, 2.7, 5.5, 3.8, SURFACE_NAVY, SURFACE_BORDER)
    tb2 = slide.shapes.add_textbox(Inches(7.08), Inches(2.9), Inches(5.0), Inches(3.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "PROJECT REPOSITORY & DEMONSTRATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf2.add_paragraph()
    p.text = "• Live Interactive Dashboard: curacascadev2.streamlit.app\n• GitHub Repository: github.com/uditshokeen14/curacascade\n• IEEE Conference Manuscript: docs/CuraCascade_IEEE_Report_Revised.pdf\n• Docker Container: curacascade:v2.4-production"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)

    # Big Q&A Prompt
    p = tf2.add_paragraph()
    p.text = "Questions & Discussion"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEAL_PRIMARY
    p.space_before = Pt(18)

    p = tf2.add_paragraph()
    p.text = "I welcome questions, technical critiques, and suggestions from the committee."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(4)

    add_footer(slide, 15)
    add_sequential_animations(slide, [c1.shape_id, c2.shape_id])

    set_speaker_notes(slide, {
        "script": "In conclusion, CuraCascade demonstrates that automated cross-layer auditing is both technically feasible and clinically necessary. By linking ClinGen, ClinVar, PanelApp, and gnomAD through a disease-aware relational warehouse, we achieved 100% precision in flagging unpropagated discrepancies and quantified an empirical 2.82-year knowledge lag. For future work, we plan to implement prospective longitudinal tracking and EHR integration. I want to sincerely thank the examination committee for their time and guidance, and I now welcome your questions and discussion.",
        "takeaway": "CuraCascade bridges a critical gap in clinical genomics through reproducible engineering, open-source decision support, and strict scientific integrity.",
        "guardrail": "Be open and receptive to faculty questions; defend the choices made in 3NF design and disease-aware matching without being defensive.",
        "question": "What is the most immediate clinical benefit if a diagnostic lab adopts CuraCascade tomorrow?",
        "answer": "The lab can immediately perform a retrospective audit of all historical patient cases where variants were signed out as Pathogenic in disputed genes like SCN1B or MYLK2, allowing them to issue amended reports and prevent unnecessary cascade screening in family members."
    })


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

def build_complete_presentation():
    print("=" * 80)
    print("🎨 GENERATING CURACASCADE REDESIGNED PRESENTATION (15 WIDESCREEN SLIDES)")
    print("=" * 80)

    prs = create_deck()

    builders = [
        ("Slide 01: Title & Defense Overview", build_slide_1_title),
        ("Slide 02: Evidence Synchronization Gap", build_slide_2_problem),
        ("Slide 03: Multi-Repository Fragmentation", build_slide_3_fragmentation),
        ("Slide 04: The CuraCascade Pipeline", build_slide_4_workflow),
        ("Slide 05: System Architecture (Dual Engine)", build_slide_5_architecture),
        ("Slide 06: Disease-Aware Matching Heuristics", build_slide_6_matching),
        ("Slide 07: Live Streamlit Application Walkthrough", build_slide_7_live_ui),
        ("Slide 08: Clinical Discrepancy Case Studies", build_slide_8_case_studies),
        ("Slide 09: 100-Gene Benchmark Methodology", build_slide_9_benchmark_method),
        ("Slide 10: Empirical Results & Precision-Recall", build_slide_10_results),
        ("Slide 11: Error Analysis & 34 False Negatives", build_slide_11_error_analysis),
        ("Slide 12: Exploratory ML & Latency Kinetics", build_slide_12_exploratory_analytics),
        ("Slide 13: Software Engineering Rigor & Tests", build_slide_13_engineering),
        ("Slide 14: Research Contributions & Impact", build_slide_14_contributions),
        ("Slide 15: Conclusion, Roadmap & Defense Q&A", build_slide_15_conclusion),
    ]

    for title, fn in builders:
        print(f"  • Building {title}...")
        fn(prs)

    # Save to Root and Docs
    prs.save(str(OUTPUT_PPTX))
    DOCS_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(DOCS_PPTX))

    print(f"\n✅ PowerPoint Presentation successfully saved to:")
    print(f"   1. {OUTPUT_PPTX}")
    print(f"   2. {DOCS_PPTX}")


if __name__ == "__main__":
    build_complete_presentation()
