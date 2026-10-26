"""Tests for biological entity matching, disease concept crosswalks, and pleiotropy handling.

Verifies:
- Exact concept matching via canonical synonyms.
- Distinct disease exclusion (e.g. SCN1B Brugada vs Dravet/Epilepsy).
- Multi-disease gene matching without false cross-phenotype flags.
- Pleiotropic multi-phenotype handling (POTENTIAL_DISCREPANCY_REVIEW).
- Data quality issue handling for placeholder phenotypes ('not provided').
- Diagnostic panel indication matching and non-indicated panel exclusion.
"""

from __future__ import annotations

import pytest
from pipeline.disease_mapping import (
    evaluate_disease_match,
    match_variant_to_curation_disease,
    match_panel_to_curation_disease,
    normalize_text,
    split_phenotype_list,
    CANONICAL_DISEASE_REGISTRY,
)


def test_exact_disease_match():
    """Brugada syndrome curation matches Brugada ClinVar phenotype."""
    match = match_variant_to_curation_disease(
        gene_symbol="SCN1B",
        variant_disease_id=None,
        variant_phenotypes="Brugada syndrome 1",
        clingen_disease_id="MONDO:0015263",
        clingen_disease_name="Brugada syndrome",
    )
    assert match.is_match is True
    assert match.match_status == "CONFIRMED_MATCH"
    assert match.confidence in ("EXACT", "HIGH")
    assert "Brugada" in match.target_phenotype


def test_distinct_disease_exclusion_scn1b():
    """SCN1B variant asserted only for Dravet/Epilepsy must NOT match Brugada curation."""
    match = match_variant_to_curation_disease(
        gene_symbol="SCN1B",
        variant_disease_id=None,
        variant_phenotypes="Dravet syndrome; Generalized epilepsy with febrile seizures plus",
        clingen_disease_id="MONDO:0015263",
        clingen_disease_name="Brugada syndrome",
    )
    assert match.is_match is False
    assert match.match_status == "DISEASE_MISMATCH"
    assert match.rule_id == "RULE_DISTINCT_DISEASE_EXCLUSION"


def test_distinct_disease_exclusion_kcne2():
    """KCNE2 variant asserted for periodic paralysis must NOT match LQTS curation."""
    match = match_variant_to_curation_disease(
        gene_symbol="KCNE2",
        variant_disease_id=None,
        variant_phenotypes="Hypokalemic periodic paralysis type 2",
        clingen_disease_id="MONDO:0002442",
        clingen_disease_name="Long QT syndrome",
    )
    assert match.is_match is False
    assert match.match_status == "DISEASE_MISMATCH"


def test_pleiotropic_variant_flagged_for_review():
    """Variant reported with both target condition and another phenotype is flagged for expert review."""
    match = match_variant_to_curation_disease(
        gene_symbol="SCN1B",
        variant_disease_id=None,
        variant_phenotypes="Brugada syndrome; Epilepsy, generalized",
        clingen_disease_id="MONDO:0015263",
        clingen_disease_name="Brugada syndrome",
    )
    assert match.is_match is True
    assert match.match_status == "POTENTIAL_DISCREPANCY_REVIEW"
    assert match.rule_id == "RULE_PLEIOTROPIC_MATCH"


def test_placeholder_phenotype_data_quality_issue():
    """Placeholder terms like 'not provided' or 'allHighlyPenetrant' trigger DATA_QUALITY_ISSUE."""
    for placeholder in ["not provided", "not specified", "allhighlypenetrant"]:
        match = match_variant_to_curation_disease(
            gene_symbol="MYLK2",
            variant_disease_id=None,
            variant_phenotypes=placeholder,
            clingen_disease_id="MONDO:0005045",
            clingen_disease_name="Hypertrophic cardiomyopathy",
        )
        assert match.match_status == "DATA_QUALITY_ISSUE"
        assert match.rule_id == "RULE_MISSING_PHENOTYPE"


def test_panel_matching_concordant():
    """Cardiomyopathy diagnostic panel matches HCM curation."""
    match = match_panel_to_curation_disease(
        gene_symbol="MYLK2",
        panel_id=134,
        panel_name="Hypertrophic cardiomyopathy - adult onset",
        panel_phenotypes="Hypertrophic cardiomyopathy",
        clingen_disease_id="MONDO:0005045",
        clingen_disease_name="Hypertrophic cardiomyopathy",
    )
    assert match.is_match is True
    assert match.match_status == "CONFIRMED_MATCH"


def test_panel_matching_discordant():
    """Unrelated panel (e.g. Hereditary renal cancer) does NOT match arrhythmia curation."""
    match = match_panel_to_curation_disease(
        gene_symbol="SCN1B",
        panel_id=500,
        panel_name="Hereditary renal cancer panel",
        panel_phenotypes="Renal carcinoma",
        clingen_disease_id="MONDO:0015263",
        clingen_disease_name="Brugada syndrome",
    )
    assert match.is_match is False
    assert match.match_status == "DISEASE_MISMATCH"


def test_broad_keyword_overlap_insufficient_for_match():
    """Generic broad category keywords alone do NOT establish a confirmed match."""
    match = match_variant_to_curation_disease(
        gene_symbol="TTN",
        variant_disease_id=None,
        variant_phenotypes="Cardiomyopathy; Cardiovascular phenotype",
        clingen_disease_id="MONDO:0005045",
        clingen_disease_name="Hypertrophic cardiomyopathy",
    )
    assert match.is_match is False
    assert match.match_status == "POTENTIAL_DISCREPANCY_REVIEW"
    assert match.rule_id == "RULE_BROAD_PHENOTYPE_OVERLAP"


def test_ontology_crosswalk_identifier_match():
    """MedGen identifier crosswalk correctly confirms match to canonical disease concept."""
    match = match_variant_to_curation_disease(
        gene_symbol="MYH7",
        variant_disease_id="MedGen:C0007194",
        variant_phenotypes="Hypertrophic cardiomyopathy",
        clingen_disease_id="MONDO:0005045",
        clingen_disease_name="Hypertrophic cardiomyopathy",
    )
    assert match.is_match is True
    assert match.match_status == "CONFIRMED_MATCH"
    assert match.rule_id in ("RULE_DIRECT_IDENTIFIER_EXACT", "RULE_ONTOLOGY_CROSSWALK_MATCH")


@pytest.mark.parametrize("gene,curation_did,curation_name,variant_pheno", [
    ("MLH1", "MONDO:0016419", "Hereditary breast carcinoma", "Colorectal cancer, hereditary nonpolyposis, type 2; Lynch syndrome"),
    ("MSH2", "MONDO:0016419", "Hereditary breast carcinoma", "Lynch syndrome; Muir-Torre syndrome"),
    ("MSH6", "MONDO:0016419", "Hereditary breast carcinoma", "Lynch syndrome"),
    ("PMS2", "MONDO:0016419", "Hereditary breast carcinoma", "Lynch syndrome; Mismatch repair cancer syndrome 1"),
    ("FBN1", "MONDO:0008426", "Shprintzen-Goldberg syndrome", "Marfan syndrome; Thoracic aortic aneurysm and aortic dissection"),
    ("MYH11", "MONDO:0005453", "Congenital heart disease", "Familial thoracic aortic aneurysm and aortic dissection"),
    ("RYR2", "MONDO:0016587", "Arrhythmogenic right ventricular cardiomyopathy", "Catecholaminergic polymorphic ventricular tachycardia"),
    ("KCNQ1", "MONDO:0005045", "Hypertrophic cardiomyopathy", "Long QT syndrome 1; Jervell and Lange-Nielsen syndrome"),
    ("KCNH2", "MONDO:0015263", "Brugada syndrome", "Long QT syndrome 2"),
    ("SCN5A", "MONDO:0005453", "Congenital heart disease", "Long QT syndrome 3; Brugada syndrome 1"),
    ("MYH7", "MONDO:0016587", "Arrhythmogenic right ventricular cardiomyopathy", "Hypertrophic cardiomyopathy 1"),
    ("MYBPC3", "MONDO:0016587", "Arrhythmogenic right ventricular cardiomyopathy", "Hypertrophic cardiomyopathy 4"),
])
def test_multi_disease_genes_distinct_disorders_not_flagged(gene, curation_did, curation_name, variant_pheno):
    """Multi-disease genes must not conflate distinct allelic disorders with disputed curations."""
    match = match_variant_to_curation_disease(
        gene_symbol=gene,
        variant_disease_id=None,
        variant_phenotypes=variant_pheno,
        clingen_disease_id=curation_did,
        clingen_disease_name=curation_name,
    )
    assert match.is_match is False
    assert match.match_status == "DISEASE_MISMATCH"
    assert match.rule_id == "RULE_DISTINCT_DISEASE_EXCLUSION"

