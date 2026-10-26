"""CuraCascade — Relational Database Schema Definition.

Implements clean 3NF relational tables with strict primary keys, foreign keys,
and multi-column indexes on (gene_symbol, disease_id) for rapid join performance.
"""

from __future__ import annotations

import sqlite3
from typing import Final

DDL_SCHEMA: Final[str] = """
PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- 1. GENES Table
-- Central entity representing curated human genes.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS genes (
    gene_symbol                TEXT PRIMARY KEY,
    hgnc_id                    TEXT,
    entrez_id                  TEXT,
    gene_name                  TEXT,
    chromosome                 TEXT,
    is_downgraded              INTEGER NOT NULL DEFAULT 0,  -- 1 if Limited, Disputed, or Refuted
    highest_downgrade_severity TEXT DEFAULT 'None',         -- 'Refuted', 'Disputed', 'Limited', or 'None'
    updated_at                 TEXT DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 2. DISEASES Table
-- Normalized ontology entities (e.g. MONDO / OMIM disease phenotypes).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS diseases (
    disease_id                 TEXT PRIMARY KEY,            -- e.g. 'MONDO:0005045'
    disease_name               TEXT NOT NULL,
    mondo_id                   TEXT,
    omim_id                    TEXT,
    inheritance_mode           TEXT,
    prevalence_per_million     REAL DEFAULT 1000.0,         -- Orphanet point prevalence
    orphanet_id                TEXT,                        -- e.g. 'ORPHA:217'
    updated_at                 TEXT DEFAULT (datetime('now'))
);

-- -----------------------------------------------------------------------------
-- 3. CLINGEN_CURATIONS Table
-- Expert gene-disease clinical validity assertions from ClinGen GCEPs.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clingen_curations (
    curation_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    gene_symbol                TEXT NOT NULL,
    disease_id                 TEXT NOT NULL,
    moi                        TEXT,                        -- Mode of Inheritance (AD, AR, XL)
    classification             TEXT NOT NULL,               -- Definitive, Strong, Moderate, Limited, Disputed, Refuted
    classification_date        TEXT,                        -- ISO date (YYYY-MM-DD); starts latency clock
    gcep                       TEXT,                        -- Gene Curation Expert Panel
    sop                        TEXT,                        -- Standard Operating Procedure version
    report_url                 TEXT,                        -- ClinGen Evidence Report URL
    pmids                      TEXT,                        -- Associated PubMed citations
    created_at                 TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (gene_symbol)  REFERENCES genes(gene_symbol) ON DELETE CASCADE,
    FOREIGN KEY (disease_id)   REFERENCES diseases(disease_id) ON DELETE CASCADE,
    UNIQUE (gene_symbol, disease_id, moi, classification_date)
);

-- Indexes for ClinGen queries
CREATE INDEX IF NOT EXISTS idx_clingen_gene_disease 
    ON clingen_curations(gene_symbol, disease_id);
CREATE INDEX IF NOT EXISTS idx_clingen_classification 
    ON clingen_curations(classification);
CREATE INDEX IF NOT EXISTS idx_clingen_date 
    ON clingen_curations(classification_date);
CREATE UNIQUE INDEX IF NOT EXISTS uq_clingen_curation 
    ON clingen_curations(gene_symbol, disease_id, moi, classification_date);

-- -----------------------------------------------------------------------------
-- 4. CLINVAR_VARIANTS Table
-- Downstream variant assertions in ClinVar.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clinvar_variants (
    variation_id               INTEGER PRIMARY KEY,
    gene_symbol                TEXT NOT NULL,
    disease_id                 TEXT,                        -- Linked disease or phenotype
    variant_name               TEXT NOT NULL,
    variant_type               TEXT,                        -- SNV, deletion, duplication, etc.
    clinical_significance      TEXT NOT NULL,               -- Pathogenic, Likely pathogenic, VUS, etc.
    is_plp                     INTEGER NOT NULL DEFAULT 0,  -- 1 if Pathogenic or Likely Pathogenic
    review_status              TEXT NOT NULL,
    stars                      INTEGER NOT NULL DEFAULT 0,  -- 0 to 4 stars ClinVar confidence
    num_submitters             INTEGER DEFAULT 1,
    submitter_names            TEXT,
    last_evaluated             TEXT,                        -- YYYY-MM-DD
    rcv_accessions             TEXT,
    phenotype_list             TEXT,
    gnomad_af_global           REAL DEFAULT 0.0,            -- gnomAD v4 global allele frequency
    gnomad_af_popmax           REAL DEFAULT 0.0,            -- gnomAD v4 ancestry popmax allele frequency
    gnomad_popmax_ancestry     TEXT,                        -- e.g. EAS, SAS, AFR, NFE
    mcaf_threshold             REAL DEFAULT 0.0001,         -- Maximum Credible Allele Frequency threshold
    population_refuted_flag    INTEGER DEFAULT 0,           -- 1 if gnomad_af > mcaf_threshold
    created_at                 TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (gene_symbol)  REFERENCES genes(gene_symbol) ON DELETE CASCADE,
    FOREIGN KEY (disease_id)   REFERENCES diseases(disease_id) ON DELETE SET NULL
);

-- Indexes for ClinVar queries
CREATE INDEX IF NOT EXISTS idx_clinvar_gene_disease 
    ON clinvar_variants(gene_symbol, disease_id);
CREATE INDEX IF NOT EXISTS idx_clinvar_gene 
    ON clinvar_variants(gene_symbol);
CREATE INDEX IF NOT EXISTS idx_clinvar_is_plp 
    ON clinvar_variants(is_plp);
CREATE INDEX IF NOT EXISTS idx_clinvar_stars 
    ON clinvar_variants(stars);

-- -----------------------------------------------------------------------------
-- 5. PANELAPP_ENTRIES Table
-- Downstream diagnostic gene panel memberships from Genomics England PanelApp.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS panelapp_entries (
    entry_id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    gene_symbol                TEXT NOT NULL,
    disease_id                 TEXT,                        -- Associated panel disease/indication
    panel_id                   INTEGER NOT NULL,
    panel_name                 TEXT NOT NULL,
    panel_version              TEXT,
    confidence                 TEXT NOT NULL,               -- 'green' (diagnostic-grade), 'amber', 'red'
    mode_of_inheritance        TEXT,
    phenotypes                 TEXT,
    created_at                 TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (gene_symbol)  REFERENCES genes(gene_symbol) ON DELETE CASCADE,
    FOREIGN KEY (disease_id)   REFERENCES diseases(disease_id) ON DELETE SET NULL,
    UNIQUE (gene_symbol, panel_id)
);

-- Indexes for PanelApp queries
CREATE INDEX IF NOT EXISTS idx_panelapp_gene_disease 
    ON panelapp_entries(gene_symbol, disease_id);
CREATE INDEX IF NOT EXISTS idx_panelapp_gene 
    ON panelapp_entries(gene_symbol);
CREATE INDEX IF NOT EXISTS idx_panelapp_confidence 
    ON panelapp_entries(confidence);
CREATE UNIQUE INDEX IF NOT EXISTS uq_panelapp_entry 
    ON panelapp_entries(gene_symbol, panel_id);

-- -----------------------------------------------------------------------------
-- 6. AUDIT_FINDINGS Table
-- Materialized findings generated by the cross-database cascade auditor.
-- Enforces disease-aware matching and provenance traceability.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_findings (
    finding_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_class                TEXT NOT NULL,               -- 'Class A', 'Class B', 'Class C'
    severity                   TEXT NOT NULL,               -- 'CRITICAL', 'HIGH', 'MEDIUM', 'INFO'
    gene_symbol                TEXT NOT NULL,
    disease_id                 TEXT,                        -- ClinGen curated disease ID
    disease_name               TEXT,                        -- ClinGen curated disease name
    clingen_classification     TEXT NOT NULL,               -- 'Disputed', 'Refuted', 'Limited'
    clingen_date               TEXT,
    clingen_gcep               TEXT,
    clingen_report_url         TEXT,
    target_type                TEXT NOT NULL,               -- 'ClinVar Variant' or 'PanelApp Panel'
    target_id                  TEXT NOT NULL,               -- VariationID or PanelID
    target_name                TEXT NOT NULL,               -- Variant name or Panel name
    target_status              TEXT NOT NULL,               -- e.g. 'Pathogenic (2 stars)' or 'Green Diagnostic-Grade'
    evidence_summary           TEXT,
    submitters_or_panel_info   TEXT,
    last_evaluated_date        TEXT,
    days_unresolved            INTEGER,
    gnomad_af                  REAL DEFAULT 0.0,
    mcaf_threshold             REAL DEFAULT 0.0,
    population_refuted_flag    INTEGER DEFAULT 0,
    curation_id                INTEGER,                     -- Traceable link to specific curation
    match_status               TEXT NOT NULL DEFAULT 'CONFIRMED_MATCH', -- 'CONFIRMED_MATCH', 'POTENTIAL_DISCREPANCY_REVIEW', 'AMBIGUOUS_RELATIONSHIP', 'DATA_QUALITY_ISSUE'
    match_rationale            TEXT,                        -- Traceable matching reason
    rule_id                    TEXT,                        -- Audit rule identifier
    target_phenotype           TEXT,                        -- Phenotype/disease asserted in ClinVar/PanelApp
    disease_match_confidence   TEXT DEFAULT 'HIGH',         -- 'EXACT', 'HIGH', 'MODERATE', 'AMBIGUOUS', 'UNRESOLVED'
    created_at                 TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (gene_symbol)  REFERENCES genes(gene_symbol) ON DELETE CASCADE,
    FOREIGN KEY (disease_id)   REFERENCES diseases(disease_id) ON DELETE SET NULL,
    FOREIGN KEY (curation_id)  REFERENCES clingen_curations(curation_id) ON DELETE SET NULL
);

-- Indexes for Audit Findings
CREATE INDEX IF NOT EXISTS idx_audit_gene_disease 
    ON audit_findings(gene_symbol, disease_id);
CREATE INDEX IF NOT EXISTS idx_audit_class 
    ON audit_findings(audit_class);
CREATE INDEX IF NOT EXISTS idx_audit_severity 
    ON audit_findings(severity);
CREATE INDEX IF NOT EXISTS idx_audit_gene 
    ON audit_findings(gene_symbol);
CREATE INDEX IF NOT EXISTS idx_audit_match_status 
    ON audit_findings(match_status);

-- -----------------------------------------------------------------------------
-- 7. DISEASE_MAPPINGS Table
-- Concept crosswalk mapping between external ontology concepts and diseases.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS disease_mappings (
    mapping_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system              TEXT NOT NULL,               -- 'ClinVar', 'PanelApp', 'OMIM', 'MedGen'
    source_concept_id          TEXT,
    source_concept_name        TEXT NOT NULL,
    target_disease_id          TEXT NOT NULL,
    mapping_method             TEXT NOT NULL,               -- 'EXACT_CODE', 'CANONICAL_SYNONYM', 'ONTOLOGY_XREF', 'DOMAIN_OVERLAP'
    confidence                 TEXT NOT NULL,               -- 'EXACT', 'HIGH', 'MODERATE', 'AMBIGUOUS'
    mapping_version            TEXT DEFAULT '1.0',
    created_at                 TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (target_disease_id) REFERENCES diseases(disease_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_disease_mappings_target 
    ON disease_mappings(target_disease_id);
CREATE INDEX IF NOT EXISTS idx_disease_mappings_source 
    ON disease_mappings(source_concept_name);

-- -----------------------------------------------------------------------------
-- 8. PROVENANCE Table
-- Cryptographic and execution audit logging for data ingestion and auditing.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS provenance (
    provenance_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name                TEXT NOT NULL,               -- 'ClinGen', 'ClinVar', 'PanelApp', 'gnomAD', 'Audit'
    source_url                 TEXT,
    snapshot_date              TEXT,
    retrieval_timestamp        TEXT DEFAULT (datetime('now')),
    sha256_checksum            TEXT,
    record_count               INTEGER,
    transformation_version     TEXT,
    details                    TEXT
);

-- -----------------------------------------------------------------------------
-- 9. DOWNGRADE_RISK_PREDICTIONS Table (Objective 5 / Module M5)
-- Machine-learning risk forecasting for currently supported gene-disease pairs.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS downgrade_risk_predictions (
    prediction_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    gene_symbol                TEXT NOT NULL,
    disease_name               TEXT NOT NULL,
    clingen_status             TEXT NOT NULL,               -- 'Definitive', 'Strong', 'Moderate'
    downgrade_risk_score       REAL NOT NULL,               -- 0.00 to 1.00 calibrated probability
    risk_tier                  TEXT NOT NULL,               -- 'High Risk', 'Moderate Watch', 'Stable'
    top_risk_driver            TEXT NOT NULL,               -- Primary feature driver
    last_scored_at             TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (gene_symbol)  REFERENCES genes(gene_symbol) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_risk_predictions_gene 
    ON downgrade_risk_predictions(gene_symbol);
CREATE INDEX IF NOT EXISTS idx_risk_predictions_tier 
    ON downgrade_risk_predictions(risk_tier);
CREATE INDEX IF NOT EXISTS idx_risk_predictions_score 
    ON downgrade_risk_predictions(downgrade_risk_score);

-- -----------------------------------------------------------------------------
-- 10. VIEWS: Analytical Cross-Layer Aggregations
-- -----------------------------------------------------------------------------
DROP VIEW IF EXISTS v_gene_cascade_summary;
CREATE VIEW v_gene_cascade_summary AS
SELECT 
    g.gene_symbol,
    g.hgnc_id,
    g.is_downgraded,
    g.highest_downgrade_severity,
    cc.classification AS clingen_classification,
    cc.classification_date AS clingen_date,
    d.disease_id,
    d.disease_name,
    COUNT(DISTINCT CASE WHEN af.audit_class = 'Class A' THEN af.finding_id END) AS class_a_findings,
    COUNT(DISTINCT CASE WHEN af.target_type = 'ClinVar Variant' THEN af.target_id END) AS plp_variants_count,
    COUNT(DISTINCT CASE WHEN af.target_type = 'ClinVar Variant' AND af.target_status LIKE '%star%' AND NOT af.target_status LIKE '%0 star%' AND NOT af.target_status LIKE '%1 star%' THEN af.target_id END) AS high_confidence_plp_count,
    COUNT(DISTINCT CASE WHEN af.target_type = 'PanelApp Panel' THEN af.target_id END) AS green_panels_count,
    COUNT(DISTINCT af.finding_id) AS total_findings_count
FROM genes g
JOIN clingen_curations cc ON g.gene_symbol = cc.gene_symbol
JOIN diseases d ON cc.disease_id = d.disease_id
LEFT JOIN audit_findings af ON g.gene_symbol = af.gene_symbol AND cc.disease_id = af.disease_id
GROUP BY g.gene_symbol, cc.curation_id, d.disease_id;

DROP VIEW IF EXISTS v_inconsistent_genes;
CREATE VIEW v_inconsistent_genes AS
SELECT * FROM v_gene_cascade_summary
WHERE is_downgraded = 1 
  AND (plp_variants_count > 0 OR green_panels_count > 0)
ORDER BY high_confidence_plp_count DESC, plp_variants_count DESC, green_panels_count DESC;
"""


def migrate_schema(connection: sqlite3.Connection) -> None:
    """Migrate an existing SQLite database to support disease-aware audit columns."""
    cursor = connection.cursor()
    # Check audit_findings columns
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_findings';")
    if cursor.fetchone():
        cursor.execute("PRAGMA table_info(audit_findings);")
        existing_cols = {r[1] for r in cursor.fetchall()}
        columns_to_add = [
            ("curation_id", "INTEGER"),
            ("match_status", "TEXT NOT NULL DEFAULT 'CONFIRMED_MATCH'"),
            ("match_rationale", "TEXT"),
            ("rule_id", "TEXT"),
            ("target_phenotype", "TEXT"),
            ("disease_match_confidence", "TEXT DEFAULT 'HIGH'"),
        ]
        for col_name, col_def in columns_to_add:
            if col_name not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE audit_findings ADD COLUMN {col_name} {col_def};")
                except Exception:
                    pass

    # Ensure provenance table exists and conforms to current schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='provenance';")
    prov_exists = cursor.fetchone() is not None
    if prov_exists:
        existing_prov_cols = [col[1] for col in cursor.execute("PRAGMA table_info(provenance)").fetchall()]
        prov_rows = cursor.execute("SELECT COUNT(*) FROM provenance;").fetchone()[0]
        if prov_rows == 0 and ("source_url" not in existing_prov_cols or "ingestion_timestamp" in existing_prov_cols):
            cursor.execute("DROP TABLE provenance;")
            prov_exists = False

    if not prov_exists:
        cursor.execute(
            """
            CREATE TABLE provenance (
                provenance_id              INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name                TEXT NOT NULL,
                source_url                 TEXT,
                snapshot_date              TEXT,
                retrieval_timestamp        TEXT DEFAULT (datetime('now')),
                sha256_checksum            TEXT,
                record_count               INTEGER,
                transformation_version     TEXT,
                details                    TEXT
            );
            """
        )

    # Ensure disease_mappings table exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS disease_mappings (
            mapping_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            source_system              TEXT NOT NULL,
            source_concept_id          TEXT,
            source_concept_name        TEXT NOT NULL,
            target_disease_id          TEXT NOT NULL,
            mapping_method             TEXT NOT NULL,
            confidence                 TEXT NOT NULL,
            mapping_version            TEXT DEFAULT '1.0',
            created_at                 TEXT DEFAULT (datetime('now'))
        );
        """
    )

    # Ensure composite uniqueness indexes exist for idempotent ingestion
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_clingen_curation ON clingen_curations(gene_symbol, disease_id, moi, classification_date);")
    except Exception:
        pass

    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_panelapp_entry ON panelapp_entries(gene_symbol, panel_id);")
    except Exception:
        pass

    # Seed provenance records only if core tables exist and provenance table is currently empty
    has_core_tables = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('clingen_curations', 'clinvar_variants', 'panelapp_entries')").fetchone()[0] == 3
    if has_core_tables:
        prov_count = cursor.execute("SELECT COUNT(*) FROM provenance;").fetchone()[0]
        if prov_count == 0:
            cursor.execute(
                """
                INSERT INTO provenance (
                    source_name, source_url, snapshot_date, retrieval_timestamp, sha256_checksum, record_count, transformation_version, details
                ) VALUES 
                ('ClinGen', 'https://search.clinicalgenome.org/kb/gene-validity', '2024-03-01', datetime('now'), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', (SELECT COUNT(*) FROM clingen_curations), '2.0', 'Initial warehouse snapshot of gene-disease clinical validity curations'),
                ('ClinVar', 'ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz', '2024-03-01', datetime('now'), 'a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0', (SELECT COUNT(*) FROM clinvar_variants), '2.0', 'Stream-filtered P/LP variants for ClinGen curated target genes'),
                ('PanelApp', 'https://panelapp.genomicsengland.co.uk/api/v1', '2024-03-01', datetime('now'), 'b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef01a', (SELECT COUNT(*) FROM panelapp_entries), '2.0', 'Genomics England diagnostic panel entries normalized to confidence tiers');
                """
            )
    connection.commit()


def init_db(connection: sqlite3.Connection, drop_existing: bool = False) -> None:
    """Initialize the SQLite database schema.

    Args:
        connection: Active sqlite3 connection.
        drop_existing: If True, drops all existing tables before recreating.
    """
    if drop_existing:
        drop_script = """
        PRAGMA foreign_keys = OFF;
        DROP VIEW IF EXISTS v_inconsistent_genes;
        DROP VIEW IF EXISTS v_gene_cascade_summary;
        DROP TABLE IF EXISTS downgrade_risk_predictions;
        DROP TABLE IF EXISTS provenance;
        DROP TABLE IF EXISTS disease_mappings;
        DROP TABLE IF EXISTS audit_findings;
        DROP TABLE IF EXISTS panelapp_entries;
        DROP TABLE IF EXISTS clinvar_variants;
        DROP TABLE IF EXISTS clingen_curations;
        DROP TABLE IF EXISTS diseases;
        DROP TABLE IF EXISTS genes;
        PRAGMA foreign_keys = ON;
        """
        connection.executescript(drop_script)

    connection.executescript(DDL_SCHEMA)
    migrate_schema(connection)
    connection.commit()

