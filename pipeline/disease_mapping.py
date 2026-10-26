"""CuraCascade — Disease-Aware Biological Entity Matching and Crosswalk Engine.

Provides authoritative ontology concept harmonization, crosswalk mapping between
ClinGen (MONDO), NCBI ClinVar (MedGen, phenotype terms), and Genomics England
PanelApp (panel indications, phenotypes).

Distinguishes among:
- CONFIRMED_MATCH: Verified match on disease concept identifier or canonical label.
- POTENTIAL_DISCREPANCY_REVIEW: Related phenotype or pleiotropic variant requiring expert review.
- AMBIGUOUS_RELATIONSHIP: Ambiguous mapping matching multiple disparate conditions.
- DATA_QUALITY_ISSUE: Missing or placeholder phenotype ('not provided').
- DISEASE_MISMATCH: Asserted condition is distinct from the downgraded condition (NOT FLAGGED).

Prevents Cartesian gene-level joins from flagging variants in multi-disease genes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class MappingMatch:
    """Outcome of disease/phenotype comparison."""
    is_match: bool
    match_status: str  # 'CONFIRMED_MATCH', 'POTENTIAL_DISCREPANCY_REVIEW', 'AMBIGUOUS_RELATIONSHIP', 'DATA_QUALITY_ISSUE', 'DISEASE_MISMATCH'
    confidence: str    # 'EXACT', 'HIGH', 'MODERATE', 'AMBIGUOUS', 'UNRESOLVED', 'NONE'
    rule_id: str
    target_phenotype: str
    matched_disease_id: Optional[str]
    matched_disease_name: Optional[str]
    rationale: str


# ==============================================================================
# Canonical Disease Concept Dictionary & Cross-Ontology Crosswalk
# ==============================================================================

# Core curated disease registry with MONDO, OMIM, MedGen, and common phenotype aliases
CANONICAL_DISEASE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "MONDO:0005045": {
        "disease_name": "Hypertrophic cardiomyopathy",
        "omim_ids": ["192600", "608751", "612098", "612099", "612124", "613251", "613873", "613874"],
        "medgen_ids": ["C0007194", "CN030278"],
        "aliases": [
            "hypertrophic cardiomyopathy",
            "hcm",
            "familial hypertrophic cardiomyopathy",
            "hypertrophic obstructive cardiomyopathy",
            "hocm",
            "hypertrophic cardiomyopathy 1",
            "hypertrophic cardiomyopathy 2",
            "hypertrophic cardiomyopathy 3",
            "hypertrophic cardiomyopathy 4",
            "hypertrophic cardiomyopathy 6",
            "hypertrophic cardiomyopathy 7",
            "hypertrophic cardiomyopathy 8",
            "hypertrophic cardiomyopathy 10",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0005014": {
        "disease_name": "Dilated cardiomyopathy",
        "omim_ids": ["115200", "601494", "604145", "613172"],
        "medgen_ids": ["C0007193"],
        "aliases": [
            "dilated cardiomyopathy",
            "dcm",
            "primary dilated cardiomyopathy",
            "familial dilated cardiomyopathy",
            "dilated cardiomyopathy 1a",
            "dilated cardiomyopathy 1dd",
            "dilated cardiomyopathy 1s",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0001625": {
        "disease_name": "Long QT syndrome",
        "omim_ids": ["192500", "613688", "613695", "601005", "603830"],
        "medgen_ids": ["C0023976"],
        "aliases": [
            "long qt syndrome",
            "lqts",
            "inherited long qt syndrome",
            "long qt syndrome 1",
            "long qt syndrome 2",
            "long qt syndrome 3",
            "long qt syndrome 4",
            "long qt syndrome 5",
            "romano-ward syndrome",
            "jervell and lange-nielsen syndrome",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0002442": {
        "disease_name": "Long QT syndrome",
        "omim_ids": ["192500"],
        "medgen_ids": ["C0023976"],
        "aliases": [
            "long qt syndrome",
            "lqts",
            "inherited long qt syndrome",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0015263": {
        "disease_name": "Brugada syndrome",
        "omim_ids": ["601144", "611875", "611876", "612838", "613119", "613120"],
        "medgen_ids": ["C1142166"],
        "aliases": [
            "brugada syndrome",
            "brs",
            "brugada syndrome 1",
            "brugada syndrome 2",
            "brugada syndrome 3",
            "brugada syndrome 4",
            "brugada syndrome 5",
            "brugada ecg pattern",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0017990": {
        "disease_name": "Catecholaminergic polymorphic ventricular tachycardia",
        "omim_ids": ["604772", "611938"],
        "medgen_ids": ["C1853685"],
        "aliases": [
            "catecholaminergic polymorphic ventricular tachycardia",
            "cpvt",
            "familial ventricular tachycardia",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0000453": {
        "disease_name": "Short QT syndrome",
        "omim_ids": ["609620", "609621", "609622"],
        "medgen_ids": ["C1838183"],
        "aliases": [
            "short qt syndrome",
            "sqts",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0011448": {
        "disease_name": "Hereditary breast and ovarian cancer syndrome",
        "omim_ids": ["604370", "612555", "114480", "613399"],
        "medgen_ids": ["C2676676", "C0677776"],
        "aliases": [
            "hereditary breast and ovarian cancer syndrome",
            "hereditary breast cancer",
            "hboc",
            "breast-ovarian cancer, familial 1",
            "breast-ovarian cancer, familial 2",
            "breast cancer",
            "familial breast cancer",
            "hereditary breast",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Breast/Ovary",
    },
    "MONDO:0007254": {
        "disease_name": "Breast cancer",
        "omim_ids": ["114480"],
        "medgen_ids": ["C0006142"],
        "aliases": [
            "breast cancer",
            "hereditary breast cancer",
            "invasive ductal carcinoma",
            "triple-negative breast cancer",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Breast",
    },
    "MONDO:0016248": {
        "disease_name": "Familial ovarian cancer",
        "omim_ids": ["167000"],
        "medgen_ids": ["C0029925"],
        "aliases": [
            "familial ovarian cancer",
            "ovarian cancer",
            "ovarian neoplasm",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Ovary",
    },
    "MONDO:0005260": {
        "disease_name": "Autism spectrum disorder",
        "omim_ids": ["209850"],
        "medgen_ids": ["C1510586"],
        "aliases": [
            "autism spectrum disorder",
            "asd",
            "autism",
            "autism, susceptibility to",
            "autistic disorder",
            "pervasive developmental disorder",
        ],
        "domain": "Neurology",
        "organ_system": "Brain",
    },
    "MONDO:0001071": {
        "disease_name": "Intellectual disability",
        "omim_ids": ["300495"],
        "medgen_ids": ["C3714756"],
        "aliases": [
            "intellectual disability",
            "mental retardation",
            "intellectual developmental disorder",
            "id",
        ],
        "domain": "Neurology",
        "organ_system": "Brain",
    },
    "MONDO:0010675": {
        "disease_name": "Phelan-McDermid syndrome",
        "omim_ids": ["606232"],
        "medgen_ids": ["C1853688"],
        "aliases": [
            "phelan-mcdermid syndrome",
            "22q13.3 deletion syndrome",
        ],
        "domain": "Neurology",
        "organ_system": "Brain",
    },
    "MONDO:0007817": {
        "disease_name": "Autosomal dominant nonsyndromic hearing loss",
        "omim_ids": ["600791"],
        "medgen_ids": ["C1864930"],
        "aliases": [
            "autosomal dominant nonsyndromic hearing loss",
            "nonsyndromic genetic hearing loss",
            "sensorineural hearing loss",
            "deafness",
            "hearing loss",
        ],
        "domain": "Others",
        "organ_system": "Ear",
    },
    "MONDO:0019497": {
        "disease_name": "Nonsyndromic genetic hearing loss",
        "omim_ids": ["600791"],
        "medgen_ids": ["C1864930"],
        "aliases": [
            "nonsyndromic genetic hearing loss",
            "autosomal dominant nonsyndromic hearing loss",
            "sensorineural hearing loss",
            "deafness",
            "hearing loss",
        ],
        "domain": "Others",
        "organ_system": "Ear",
    },
    "MONDO:0008304": {
        "disease_name": "Autosomal dominant polycystic kidney disease",
        "omim_ids": ["173900", "613095"],
        "medgen_ids": ["C0032580"],
        "aliases": [
            "autosomal dominant polycystic kidney disease",
            "adpkd",
            "polycystic kidney disease 1",
            "polycystic kidney disease 2",
        ],
        "domain": "Others",
        "organ_system": "Kidney",
    },
    "MONDO:0010894": {
        "disease_name": "Maturity-onset diabetes of the young",
        "omim_ids": ["606391", "125850"],
        "medgen_ids": ["C0342286"],
        "aliases": [
            "maturity-onset diabetes of the young",
            "mody",
            "mody 1",
            "mody 2",
            "mody 3",
        ],
        "domain": "Others",
        "organ_system": "Pancreas",
    },
    "MONDO:0016575": {
        "disease_name": "Primary ciliary dyskinesia",
        "omim_ids": ["244400"],
        "medgen_ids": ["C0008780"],
        "aliases": [
            "primary ciliary dyskinesia",
            "kartagener syndrome",
            "ciliary dyskinesia",
        ],
        "domain": "Others",
        "organ_system": "Respiratory",
    },
    "MONDO:0015924": {
        "disease_name": "Pulmonary arterial hypertension",
        "omim_ids": ["178630"],
        "medgen_ids": ["C2939433"],
        "aliases": [
            "pulmonary arterial hypertension",
            "pah",
            "primary pulmonary hypertension",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Pulmonary",
    },
    "MONDO:0005835": {
        "disease_name": "Lynch syndrome",
        "omim_ids": ["120435", "120436", "609310", "614350", "614337"],
        "medgen_ids": ["C0009405", "CN029419"],
        "aliases": [
            "lynch syndrome",
            "lynch syndrome 1",
            "lynch syndrome 2",
            "hereditary nonpolyposis colorectal cancer",
            "hereditary nonpolyposis colorectal neoplasms",
            "hnpcc",
            "colorectal cancer, hereditary nonpolyposis, type 2",
            "colorectal cancer, hereditary nonpolyposis, type 1",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Colorectal",
    },
    "MONDO:0016419": {
        "disease_name": "Hereditary breast carcinoma",
        "omim_ids": ["114480"],
        "medgen_ids": ["C0006142"],
        "aliases": [
            "hereditary breast carcinoma",
            "hereditary breast cancer",
            "familial breast carcinoma",
            "familial breast cancer",
            "breast carcinoma",
            "breast cancer, susceptibility to",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Breast",
    },
    "MONDO:0010159": {
        "disease_name": "Mismatch repair cancer syndrome 1",
        "omim_ids": ["276300"],
        "medgen_ids": ["C1849156"],
        "aliases": [
            "mismatch repair cancer syndrome 1",
            "constitutional mismatch repair deficiency",
            "cmmrd",
            "turcot syndrome",
        ],
        "domain": "Hereditary Cancer",
        "organ_system": "Colorectal/Brain",
    },
    "MONDO:0016587": {
        "disease_name": "Arrhythmogenic right ventricular cardiomyopathy",
        "omim_ids": ["107970", "604400", "607450", "609040"],
        "medgen_ids": ["C0349788"],
        "aliases": [
            "arrhythmogenic right ventricular cardiomyopathy",
            "arrhythmogenic right ventricular dysplasia",
            "arvc",
            "arvd",
            "arrhythmogenic right ventricular cardiomyopathy 1",
            "arrhythmogenic right ventricular cardiomyopathy 2",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0008426": {
        "disease_name": "Shprintzen-Goldberg syndrome",
        "omim_ids": ["182212"],
        "medgen_ids": ["C1321551"],
        "aliases": [
            "shprintzen-goldberg syndrome",
            "shprintzen goldberg syndrome",
            "sgs",
            "marfanoid craniosynostosis syndrome",
        ],
        "domain": "Connective Tissue",
        "organ_system": "Skeletal/Vascular",
    },
    "MONDO:0005453": {
        "disease_name": "Congenital heart disease",
        "omim_ids": ["600001", "108900"],
        "medgen_ids": ["C0018798"],
        "aliases": [
            "congenital heart disease",
            "congenital heart defects",
            "chd",
            "cardiac malformation",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0019625": {
        "disease_name": "Familial thoracic aortic aneurysm and aortic dissection",
        "omim_ids": ["154700", "132900", "609192"],
        "medgen_ids": ["C0024796", "C0345070"],
        "aliases": [
            "familial thoracic aortic aneurysm and aortic dissection",
            "familial thoracic aortic aneurysm",
            "thoracic aortic aneurysm",
            "taad",
            "marfan syndrome",
            "marfan",
            "thoracic aortic aneurysm and aortic dissection",
            "aortic dissection",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Vascular",
    },
    "MONDO:0011001": {
        "disease_name": "Brugada syndrome 1",
        "omim_ids": ["601144"],
        "medgen_ids": ["C1142166"],
        "aliases": [
            "brugada syndrome 1",
            "brugada syndrome",
            "brs1",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0011003": {
        "disease_name": "Dilated cardiomyopathy 1E",
        "omim_ids": ["601154"],
        "medgen_ids": ["C1832342"],
        "aliases": [
            "dilated cardiomyopathy 1e",
            "dcm 1e",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0013262": {
        "disease_name": "Dilated cardiomyopathy 1S",
        "omim_ids": ["613426"],
        "medgen_ids": ["C3150882"],
        "aliases": [
            "dilated cardiomyopathy 1s",
            "dcm 1s",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
    "MONDO:0008050": {
        "disease_name": "MYH7-related skeletal myopathy",
        "omim_ids": ["608358", "255320"],
        "medgen_ids": ["C1837336"],
        "aliases": [
            "myh7-related skeletal myopathy",
            "laing distal myopathy",
            "hyaline body myopathy",
            "scapuloperoneal myopathy",
        ],
        "domain": "Neuromuscular",
        "organ_system": "Muscle",
    },
    "MONDO:0002441": {
        "disease_name": "Jervell and Lange-Nielsen syndrome",
        "omim_ids": ["220290"],
        "medgen_ids": ["C0022388"],
        "aliases": [
            "jervell and lange-nielsen syndrome",
            "jervell and lange nielsen syndrome",
            "jlns",
        ],
        "domain": "Cardiovascular",
        "organ_system": "Heart",
    },
}

# Gene-Disease Established Allelic Mechanisms and Pleiotropic Phenotypes
# Distinct phenotypes for multi-disease genes that MUST NOT be conflated
DISTINCT_PHENOTYPE_EXCLUSIONS: Dict[str, Dict[str, List[str]]] = {
    # For gene SCN1B:
    # If ClinGen curation is Brugada syndrome, epilepsy-specific assertions are non-Brugada
    "SCN1B": {
        "MONDO:0015263": [  # Brugada syndrome
            "epilepsy", "dravet", "gefs", "febrile seizure", "seizure",
            "developmental and epileptic encephalopathy"
        ],
        "MONDO:0011001": [
            "epilepsy", "dravet", "gefs", "febrile seizure", "seizure",
            "developmental and epileptic encephalopathy"
        ],
    },
    # For gene KCNE2:
    # If ClinGen curation is Brugada syndrome or Long QT, periodic paralysis is distinct
    "KCNE2": {
        "MONDO:0015263": ["periodic paralysis", "thyrotoxic hypokalemic"],
        "MONDO:0002442": ["periodic paralysis", "thyrotoxic hypokalemic"],
    },
    # For MMR genes (MLH1, MSH2, MSH6, PMS2):
    # Breast cancer refutation must not conflate with definitive Lynch / colorectal assertions
    "MLH1": {
        "MONDO:0016419": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer", "muir-torre"],
        "MONDO:0011448": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
    },
    "MSH2": {
        "MONDO:0016419": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer", "muir-torre"],
        "MONDO:0011448": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
    },
    "MSH6": {
        "MONDO:0016419": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
        "MONDO:0011448": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
    },
    "PMS2": {
        "MONDO:0016419": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
        "MONDO:0011448": ["lynch", "colorectal", "hnpcc", "endometrial", "mismatch repair", "colon cancer"],
    },
    # For FBN1:
    # Shprintzen-Goldberg dispute must not conflate with definitive Marfan / TAAD
    "FBN1": {
        "MONDO:0008426": ["marfan", "thoracic aortic aneurysm", "ectopia lentis", "aortic dissection", "taad"],
    },
    # For MYH11:
    # Congenital heart disease dispute must not conflate with definitive TAAD
    "MYH11": {
        "MONDO:0005453": ["thoracic aortic aneurysm", "aortic dissection", "taad", "patent ductus arteriosus"],
    },
    # For RYR2:
    # ARVC / cardiomyopathy disputes must not conflate with definitive CPVT
    "RYR2": {
        "MONDO:0016587": ["catecholaminergic polymorphic ventricular tachycardia", "cpvt"],
        "MONDO:0005045": ["catecholaminergic polymorphic ventricular tachycardia", "cpvt"],
        "MONDO:0005021": ["catecholaminergic polymorphic ventricular tachycardia", "cpvt"],
    },
    # For KCNQ1:
    # HCM dispute must not conflate with definitive Long QT / JLNS
    "KCNQ1": {
        "MONDO:0005045": ["long qt", "lqts", "jervell", "jlns", "romano-ward", "short qt"],
    },
    # For KCNH2:
    # Brugada dispute must not conflate with definitive Long QT
    "KCNH2": {
        "MONDO:0015263": ["long qt", "lqts", "short qt", "sqts"],
    },
    # For SCN5A:
    # Congenital heart disease / ARVC disputes must not conflate with definitive Long QT / Brugada / DCM
    "SCN5A": {
        "MONDO:0005453": ["long qt", "lqts", "brugada", "cardiac rhythm", "dilated cardiomyopathy"],
        "MONDO:0016587": ["long qt", "lqts", "brugada", "cardiac rhythm", "dilated cardiomyopathy"],
    },
    # For MYH7 & MYBPC3:
    # ARVC / congenital heart disease disputes must not conflate with definitive HCM / DCM
    "MYH7": {
        "MONDO:0005045": ["laing distal myopathy", "scapuloperoneal myopathy", "myopathy"],
        "MONDO:0016587": ["hypertrophic cardiomyopathy", "hcm", "dilated cardiomyopathy", "dcm", "myopathy"],
        "MONDO:0005453": ["hypertrophic cardiomyopathy", "hcm", "dilated cardiomyopathy", "dcm"],
    },
    "MYBPC3": {
        "MONDO:0016587": ["hypertrophic cardiomyopathy", "hcm", "dilated cardiomyopathy", "dcm"],
        "MONDO:0005453": ["hypertrophic cardiomyopathy", "hcm", "dilated cardiomyopathy", "dcm"],
    },
    # For ACTN2:
    "ACTN2": {
        "MONDO:0005045": ["distal myopathy", "muscular dystrophy", "myopathy"],
    },
    # For BARD1:
    "BARD1": {
        "MONDO:0011448": ["neuroblastoma", "wilms tumor", "glioma"],
    },
    # For CAV3:
    "CAV3": {
        "MONDO:0001625": ["limb-girdle muscular dystrophy", "rippling muscle disease", "hyperckemia"],
    },
}

# Generic / Placeholder tokens in ClinVar phenotype strings
PLACEHOLDER_PHENOTYPES: Set[str] = {
    "", "not provided", "not specified", "not_provided", "not_specified",
    "-", "none", "unknown", "other", "see cases", "allhighlypenetrant", "all highly penetrant"
}


# ==============================================================================
# Helper Functions: String & Token Normalization
# ==============================================================================

def normalize_text(text: Optional[str]) -> str:
    """Normalize phenotype or disease text for comparison."""
    if not text:
        return ""
    t = str(text).lower().strip()
    t = re.sub(r"[^\w\s-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def split_phenotype_list(raw_phenotypes: Optional[str]) -> List[str]:
    """Split ClinVar/PanelApp compound phenotype string into individual concepts."""
    if not raw_phenotypes:
        return []
    s = str(raw_phenotypes)
    # Delimiters can be semicolons, pipes, or commas in compound lists
    parts = re.split(r"[|;]", s)
    cleaned = []
    for p in parts:
        pt = p.strip()
        if pt:
            cleaned.append(pt)
    return cleaned


# ==============================================================================
# Core Matching & Evaluation Engine
# ==============================================================================

def match_variant_to_curation_disease(
    gene_symbol: str,
    variant_disease_id: Optional[str],
    variant_phenotypes: Optional[str],
    clingen_disease_id: str,
    clingen_disease_name: str,
) -> MappingMatch:
    """Evaluate whether a ClinVar variant assertion pertains to the ClinGen curated disease.

    Enforces disease-aware join logic:
    - Never flags a variant if it solely belongs to a distinct non-downgraded condition.
    - Accurately identifies confirmed identifier matches vs potential or ambiguous cases.

    Args:
        gene_symbol: HGNC gene symbol (e.g., 'SCN1B').
        variant_disease_id: Stored variant disease ID (if any).
        variant_phenotypes: ClinVar raw phenotype string (e.g. 'Brugada syndrome 1; Epilepsy').
        clingen_disease_id: ClinGen curation disease ID (e.g. 'MONDO:0015263').
        clingen_disease_name: ClinGen curation disease label (e.g. 'Brugada syndrome').

    Returns:
        MappingMatch detailing whether to match and the exact clinical rationale.
    """
    sym = gene_symbol.strip().upper()
    cg_did = str(clingen_disease_id).strip()
    cg_name = clingen_disease_name.strip() if clingen_disease_name else cg_did
    norm_cg_name = normalize_text(cg_name)

    # Retrieve canonical disease metadata if available
    registry_entry = CANONICAL_DISEASE_REGISTRY.get(cg_did, {})

    # 1. Direct Stable Identifier Match (MONDO, OMIM, MedGen)
    if variant_disease_id:
        v_did_clean = str(variant_disease_id).strip()
        v_did_bare = re.sub(r'^(OMIM|MedGen|MONDO):', '', v_did_clean, flags=re.IGNORECASE)
        if v_did_clean == cg_did:
            return MappingMatch(
                is_match=True,
                match_status="CONFIRMED_MATCH",
                confidence="EXACT",
                rule_id="RULE_DIRECT_IDENTIFIER_EXACT",
                target_phenotype=variant_phenotypes or cg_name,
                matched_disease_id=cg_did,
                matched_disease_name=cg_name,
                rationale=f"Direct stable ontology identifier match ({cg_did}).",
            )
        if registry_entry:
            omims = [re.sub(r'^OMIM:', '', o, flags=re.IGNORECASE) for o in registry_entry.get("omim_ids", [])]
            medgens = [re.sub(r'^MedGen:', '', m, flags=re.IGNORECASE) for m in registry_entry.get("medgen_ids", [])]
            if v_did_bare in omims or v_did_bare in medgens:
                return MappingMatch(
                    is_match=True,
                    match_status="CONFIRMED_MATCH",
                    confidence="EXACT",
                    rule_id="RULE_ONTOLOGY_CROSSWALK_MATCH",
                    target_phenotype=variant_phenotypes or cg_name,
                    matched_disease_id=cg_did,
                    matched_disease_name=cg_name,
                    rationale=f"Ontology crosswalk identifier match ({variant_disease_id} -> {cg_did}).",
                )

    # 2. Check for Missing / Placeholder Phenotype Data
    pheno_items = split_phenotype_list(variant_phenotypes)
    non_placeholder_items = [p for p in pheno_items if normalize_text(p) not in PLACEHOLDER_PHENOTYPES]

    if not non_placeholder_items:
        return MappingMatch(
            is_match=False,
            match_status="DATA_QUALITY_ISSUE",
            confidence="UNRESOLVED",
            rule_id="RULE_MISSING_PHENOTYPE",
            target_phenotype="not provided",
            matched_disease_id=None,
            matched_disease_name=None,
            rationale="ClinVar variant assertion lacks specific disease phenotype ('not provided'); cannot confirm conflict with ClinGen appraisal.",
        )

    aliases: Set[str] = set()
    if registry_entry:
        aliases.update(normalize_text(a) for a in registry_entry.get("aliases", []))
    if norm_cg_name:
        aliases.add(norm_cg_name)

    # Check distinct exclusion terms for this gene & disease
    exclusions = DISTINCT_PHENOTYPE_EXCLUSIONS.get(sym, {}).get(cg_did, [])

    # Classify each phenotype item
    has_target_match = False
    has_exclusion_match = False
    has_broad_match = False
    matched_term = ""

    for item in non_placeholder_items:
        norm_item = normalize_text(item)

        # Check exact alias match
        if norm_item in aliases:
            has_target_match = True
            matched_term = item
            break

        # Check word-boundary match for specific disease concept (avoid loose single words)
        for alias in aliases:
            if len(alias) >= 8 and " " in alias:
                if re.search(r'\b' + re.escape(alias) + r'\b', norm_item):
                    has_target_match = True
                    matched_term = item
                    break
        if has_target_match:
            break

        # Check if item is explicitly an excluded, distinct disorder
        for excl in exclusions:
            if re.search(r'\b' + re.escape(excl) + r'\b', norm_item) or excl in norm_item:
                has_exclusion_match = True

        # Check broad category match (e.g. 'cardiomyopathy' or 'arrhythmia')
        if any(term in norm_item for term in ["cardiomyopathy", "arrhythmia", "cancer", "autism"]):
            has_broad_match = True

    # 3. Decision Logic Based on Findings
    # If the variant was asserted ONLY for a distinct non-downgraded disorder
    if has_exclusion_match and not has_target_match:
        return MappingMatch(
            is_match=False,
            match_status="DISEASE_MISMATCH",
            confidence="NONE",
            rule_id="RULE_DISTINCT_DISEASE_EXCLUSION",
            target_phenotype="; ".join(non_placeholder_items),
            matched_disease_id=None,
            matched_disease_name=None,
            rationale=f"Variant phenotype ('{'; '.join(non_placeholder_items)}') pertains to distinct, non-downgraded allelic disorder in {sym}.",
        )

    if has_target_match:
        # Check if pleiotropic with other conditions
        if len(non_placeholder_items) > 1:
            return MappingMatch(
                is_match=True,
                match_status="POTENTIAL_DISCREPANCY_REVIEW",
                confidence="HIGH",
                rule_id="RULE_PLEIOTROPIC_MATCH",
                target_phenotype="; ".join(non_placeholder_items),
                matched_disease_id=cg_did,
                matched_disease_name=cg_name,
                rationale=f"Variant reported with multiple phenotypes including target condition '{matched_term}'; requires expert pleiotropy review.",
            )
        return MappingMatch(
            is_match=True,
            match_status="CONFIRMED_MATCH",
            confidence="HIGH",
            rule_id="RULE_CANONICAL_SYNONYM_MATCH",
            target_phenotype=matched_term,
            matched_disease_id=cg_did,
            matched_disease_name=cg_name,
            rationale=f"Authoritative disease concept match to ClinGen curation '{cg_name}' via canonical alias '{matched_term}'.",
        )

    # If only broad terms are provided (e.g. 'Cardiovascular phenotype' or 'Cardiomyopathy')
    # Broad keyword overlap is NOT sufficient evidence for a disease match
    if has_broad_match:
        return MappingMatch(
            is_match=False,
            match_status="POTENTIAL_DISCREPANCY_REVIEW",
            confidence="UNRESOLVED",
            rule_id="RULE_BROAD_PHENOTYPE_OVERLAP",
            target_phenotype="; ".join(non_placeholder_items),
            matched_disease_id=None,
            matched_disease_name=None,
            rationale=f"Broad phenotype ('{'; '.join(non_placeholder_items)}') overlaps clinical domain of {cg_name} but lacks specific concept identity; insufficient evidence for confirmed discrepancy.",
        )

    # Default: Unmatched distinct phenotype
    return MappingMatch(
        is_match=False,
        match_status="DISEASE_MISMATCH",
        confidence="NONE",
        rule_id="RULE_UNMATCHED_PHENOTYPE",
        target_phenotype="; ".join(non_placeholder_items),
        matched_disease_id=None,
        matched_disease_name=None,
        rationale=f"Variant phenotype ('{'; '.join(non_placeholder_items)}') does not match ClinGen appraised disease '{cg_name}'.",
    )


def match_panel_to_curation_disease(
    gene_symbol: str,
    panel_id: int,
    panel_name: str,
    panel_phenotypes: Optional[str],
    clingen_disease_id: str,
    clingen_disease_name: str,
) -> MappingMatch:
    """Evaluate whether a Genomics England PanelApp panel corresponds to the ClinGen curated disease.

    Prevents diagnostic panels for unrelated organs from being marked as Class C discrepancies.

    Args:
        gene_symbol: HGNC gene symbol.
        panel_id: Numeric PanelApp panel ID.
        panel_name: Title of diagnostic panel.
        panel_phenotypes: Associated phenotype string.
        clingen_disease_id: ClinGen curation disease ID.
        clingen_disease_name: ClinGen curation disease label.

    Returns:
        MappingMatch.
    """
    p_name = panel_name.strip()
    norm_p_name = normalize_text(p_name)
    cg_did = str(clingen_disease_id).strip()
    cg_name = clingen_disease_name.strip() if clingen_disease_name else cg_did
    norm_cg_name = normalize_text(cg_name)

    registry_entry = CANONICAL_DISEASE_REGISTRY.get(cg_did, {})
    aliases: Set[str] = set()
    if registry_entry:
        aliases.update(normalize_text(a) for a in registry_entry.get("aliases", []))
    if norm_cg_name:
        aliases.add(norm_cg_name)

    # Check for direct panel name match
    for alias in aliases:
        if len(alias) >= 4 and (alias in norm_p_name or norm_p_name in alias):
            return MappingMatch(
                is_match=True,
                match_status="CONFIRMED_MATCH",
                confidence="HIGH",
                rule_id="RULE_PANEL_NAME_MATCH",
                target_phenotype=p_name,
                matched_disease_id=cg_did,
                matched_disease_name=cg_name,
                rationale=f"Diagnostic panel '{p_name}' directly matches ClinGen downgraded disease indication '{cg_name}'.",
            )

    # Check panel phenotypes
    if panel_phenotypes:
        p_items = split_phenotype_list(panel_phenotypes)
        for item in p_items:
            norm_item = normalize_text(item)
            for alias in aliases:
                if len(alias) >= 4 and (alias in norm_item or norm_item in alias):
                    return MappingMatch(
                        is_match=True,
                        match_status="CONFIRMED_MATCH",
                        confidence="HIGH",
                        rule_id="RULE_PANEL_PHENOTYPE_MATCH",
                        target_phenotype=p_name,
                        matched_disease_id=cg_did,
                        matched_disease_name=cg_name,
                        rationale=f"Diagnostic panel phenotypes ('{item}') match ClinGen downgraded condition '{cg_name}'.",
                    )

    # Broad domain match (e.g. cardiac panel for cardiac curation)
    # Broad domain overlap is NOT sufficient evidence for a confirmed discrepancy
    cg_domain = registry_entry.get("domain", "")
    if cg_domain == "Cardiovascular" and any(k in norm_p_name for k in ["cardiomyopathy", "arrhythmia", "cardiac"]):
        return MappingMatch(
            is_match=False,
            match_status="POTENTIAL_DISCREPANCY_REVIEW",
            confidence="UNRESOLVED",
            rule_id="RULE_PANEL_DOMAIN_OVERLAP",
            target_phenotype=p_name,
            matched_disease_id=None,
            matched_disease_name=None,
            rationale=f"Panel '{p_name}' belongs to same clinical domain ({cg_domain}) as downgraded disease '{cg_name}' but is not indicated specifically for {cg_name}.",
        )

    return MappingMatch(
        is_match=False,
        match_status="DISEASE_MISMATCH",
        confidence="NONE",
        rule_id="RULE_PANEL_MISMATCH",
        target_phenotype=p_name,
        matched_disease_id=None,
        matched_disease_name=None,
        rationale=f"Panel '{p_name}' is not indicated for ClinGen downgraded disease '{cg_name}'.",
    )


# Authoritative alias for variant-disease evaluation
evaluate_disease_match = match_variant_to_curation_disease

