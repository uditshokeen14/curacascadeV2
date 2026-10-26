"""Tests for database architecture, schema migrations, constraints, and relational integrity.

Verifies:
- Foreign key enforcement (PRAGMA foreign_keys = ON).
- Primary key uniqueness across core relational tables.
- Migration idempotency (migrate_schema can be run repeatedly without error).
- Transaction rollback on simulated failure.
- View integrity and prevention of Cartesian join explosion (v_gene_cascade_summary).
"""

from __future__ import annotations

from pathlib import Path
import sqlite3
import pytest

from database.connection import get_connection
from database.schema import DDL_SCHEMA, init_db, migrate_schema


@pytest.fixture
def memory_db():
    """Create an in-memory test database initialized with DDL schema and foreign keys enabled."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    init_db(conn, drop_existing=False)
    yield conn
    conn.close()


def test_foreign_key_enforcement(memory_db):
    """Inserting a ClinVar variant for a non-existent gene raises IntegrityError."""
    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute(
            """
            INSERT INTO clinvar_variants (
                variation_id, gene_symbol, variant_name, clinical_significance, stars
            ) VALUES (12345, 'NONEXISTENT_GENE', 'c.1A>G', 'Pathogenic', 2);
            """
        )
        memory_db.commit()


def test_primary_key_uniqueness(memory_db):
    """Duplicate primary keys on genes table must raise IntegrityError."""
    memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id) VALUES ('TEST1', 'HGNC:001');")
    memory_db.commit()

    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id) VALUES ('TEST1', 'HGNC:002');")
        memory_db.commit()


def test_schema_migration_idempotent(memory_db):
    """Running migrate_schema multiple times must succeed without error or duplicate columns."""
    migrate_schema(memory_db)
    migrate_schema(memory_db)
    migrate_schema(memory_db)

    # Check that audit_findings columns exist
    cols = [r[1] for r in memory_db.execute("PRAGMA table_info(audit_findings);").fetchall()]
    assert "curation_id" in cols
    assert "match_status" in cols
    assert "rule_id" in cols
    assert "disease_match_confidence" in cols


def test_transaction_rollback_on_failure(memory_db):
    """An uncommitted transaction with a failure rolls back completely."""
    memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id) VALUES ('GENE_A', 'HGNC:100');")
    memory_db.commit()

    try:
        with memory_db:
            memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id) VALUES ('GENE_B', 'HGNC:101');")
            # Force integrity failure
            memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id) VALUES ('GENE_A', 'HGNC:102');")
    except sqlite3.IntegrityError:
        pass

    # GENE_B should NOT have been committed
    row = memory_db.execute("SELECT gene_symbol FROM genes WHERE gene_symbol = 'GENE_B';").fetchone()
    assert row is None


def test_no_cartesian_join_in_cascade_summary(memory_db):
    """v_gene_cascade_summary must aggregate through audit_findings without Cartesian duplication."""
    # Insert 1 gene
    memory_db.execute("INSERT INTO genes (gene_symbol, hgnc_id, is_downgraded) VALUES ('MULTI1', 'HGNC:200', 1);")
    
    # Insert 2 curations for this gene
    memory_db.execute("INSERT INTO diseases (disease_id, disease_name) VALUES ('MONDO:001', 'Disease 1');")
    memory_db.execute("INSERT INTO diseases (disease_id, disease_name) VALUES ('MONDO:002', 'Disease 2');")
    memory_db.execute("INSERT INTO clingen_curations (curation_id, gene_symbol, disease_id, classification) VALUES (1, 'MULTI1', 'MONDO:001', 'Refuted');")
    memory_db.execute("INSERT INTO clingen_curations (curation_id, gene_symbol, disease_id, classification) VALUES (2, 'MULTI1', 'MONDO:002', 'Definitive');")

    # Insert 3 variants for this gene
    for i in range(1, 4):
        memory_db.execute(
            f"INSERT INTO clinvar_variants (variation_id, gene_symbol, variant_name, clinical_significance, review_status, stars, is_plp) "
            f"VALUES ({i}, 'MULTI1', 'var_{i}', 'Pathogenic', 'Criteria provided', 2, 1);"
        )

    # Insert exactly 1 Class A audit finding linked to Disease 1
    memory_db.execute(
        """
        INSERT INTO audit_findings (
            finding_id, audit_class, severity, gene_symbol, disease_id, clingen_classification,
            target_type, target_id, target_name, target_status, match_status
        ) VALUES (1, 'Class A', 'CRITICAL', 'MULTI1', 'MONDO:001', 'Refuted', 'ClinVar Variant', '1', 'var_1', 'Pathogenic', 'CONFIRMED_MATCH');
        """
    )
    memory_db.commit()

    # Query cascade summary view
    row = memory_db.execute("SELECT * FROM v_gene_cascade_summary WHERE gene_symbol = 'MULTI1';").fetchone()
    assert row is not None
    # total_inconsistencies must be 1, not multiplied by curations count (2 * 1 = 2)
    col_names = [d[0] for d in memory_db.execute("SELECT * FROM v_gene_cascade_summary LIMIT 1;").description]
    res_dict = dict(zip(col_names, row))
    assert res_dict["total_findings_count"] == 1
    assert res_dict["class_a_findings"] == 1


def test_curation_composite_uniqueness(memory_db):
    """clingen_curations rejects identical (gene, disease, moi, date) but allows distinct MOIs."""
    memory_db.execute("INSERT INTO genes (gene_symbol) VALUES ('UNIQ_GENE');")
    memory_db.execute("INSERT INTO diseases (disease_id, disease_name) VALUES ('MONDO:999', 'Test Disease');")
    memory_db.commit()

    # Insert initial curation
    memory_db.execute(
        """
        INSERT INTO clingen_curations (gene_symbol, disease_id, moi, classification, classification_date)
        VALUES ('UNIQ_GENE', 'MONDO:999', 'AD', 'Strong', '2023-10-19');
        """
    )
    memory_db.commit()

    # Different MOI for same disease and date MUST be permitted (e.g. AD vs AR in ACO2)
    memory_db.execute(
        """
        INSERT INTO clingen_curations (gene_symbol, disease_id, moi, classification, classification_date)
        VALUES ('UNIQ_GENE', 'MONDO:999', 'AR', 'Definitive', '2023-10-19');
        """
    )
    memory_db.commit()

    # Exact duplicate (same gene, disease, moi, date) must raise IntegrityError
    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute(
            """
            INSERT INTO clingen_curations (gene_symbol, disease_id, moi, classification, classification_date)
            VALUES ('UNIQ_GENE', 'MONDO:999', 'AD', 'Strong', '2023-10-19');
            """
        )

    # Idempotent re-ingestion with INSERT OR REPLACE succeeds without creating a duplicate row
    memory_db.execute(
        """
        INSERT OR REPLACE INTO clingen_curations (gene_symbol, disease_id, moi, classification, classification_date)
        VALUES ('UNIQ_GENE', 'MONDO:999', 'AD', 'Strong', '2023-10-19');
        """
    )
    memory_db.commit()
    count = memory_db.execute("SELECT COUNT(*) FROM clingen_curations WHERE gene_symbol = 'UNIQ_GENE';").fetchone()[0]
    assert count == 2


def test_panelapp_composite_uniqueness(memory_db):
    """panelapp_entries rejects duplicate (gene, panel_id) on direct insert and supports idempotent replace."""
    memory_db.execute("INSERT INTO genes (gene_symbol) VALUES ('PAN_GENE');")
    memory_db.execute(
        """
        INSERT INTO panelapp_entries (gene_symbol, panel_id, panel_name, confidence)
        VALUES ('PAN_GENE', 101, 'Cardiac Panel', 'green');
        """
    )
    memory_db.commit()

    # Duplicate insertion fails
    with pytest.raises(sqlite3.IntegrityError):
        memory_db.execute(
            """
            INSERT INTO panelapp_entries (gene_symbol, panel_id, panel_name, confidence)
            VALUES ('PAN_GENE', 101, 'Cardiac Panel', 'green');
            """
        )

    # Idempotent replace succeeds
    memory_db.execute(
        """
        INSERT OR REPLACE INTO panelapp_entries (gene_symbol, panel_id, panel_name, confidence)
        VALUES ('PAN_GENE', 101, 'Cardiac Panel Updated', 'green');
        """
    )
    memory_db.commit()
    count = memory_db.execute("SELECT COUNT(*) FROM panelapp_entries WHERE gene_symbol = 'PAN_GENE';").fetchone()[0]
    assert count == 1


def test_provenance_records_integrity(memory_db):
    """Provenance table captures source, snapshot dates, checksums, and record counts."""
    memory_db.execute(
        """
        INSERT INTO provenance (
            source_name, source_url, snapshot_date, retrieval_timestamp, sha256_checksum, record_count, transformation_version, details
        ) VALUES (
            'ClinGen', 'https://search.clinicalgenome.org', '2024-03-01', datetime('now'),
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 3672, '2.0', 'Test ingestion'
        );
        """
    )
    memory_db.commit()

    row = memory_db.execute("SELECT source_name, snapshot_date, record_count, sha256_checksum FROM provenance WHERE source_name = 'ClinGen' ORDER BY provenance_id DESC LIMIT 1;").fetchone()
    assert row is not None
    assert row[0] == "ClinGen"
    assert row[1] == "2024-03-01"
    assert row[2] == 3672
    assert len(row[3]) == 64


def test_clean_rebuild_and_repeated_ingestion_integrity(tmp_path):
    """Verify clean database build and repeated ingestion preserves constraints, provenance, and zero duplicate rows."""
    from database.connection import get_connection
    from pipeline.fetch_data import ingest_all_into_db
    import pandas as pd

    test_db = tmp_path / "rebuild_test.db"

    # 1. Initialize clean database with DDL_SCHEMA
    with get_connection(test_db, readonly=False) as conn:
        init_db(conn, drop_existing=True)
        indexes = [r[1] for r in conn.execute("SELECT type, name FROM sqlite_master WHERE type='index'").fetchall()]
        assert "uq_clingen_curation" in indexes
        assert "uq_panelapp_entry" in indexes

    # 2. Mock data batches
    cg_df = pd.DataFrame([{
        "gene_symbol": "REBUILD_G1",
        "hgnc_id": "HGNC:99999",
        "disease_id": "MONDO:0005045",
        "disease_name": "Hypertrophic cardiomyopathy",
        "mondo_id": "MONDO:0005045",
        "moi": "AD",
        "classification": "Refuted",
        "classification_date": "2024-01-01",
        "gcep": "Cardio Panel",
        "sop": "v8",
        "report_url": "http://example.com"
    }])

    pa_df = pd.DataFrame([{
        "gene_symbol": "REBUILD_G1",
        "disease_id": "MONDO:0005045",
        "panel_id": 999,
        "panel_name": "Test Panel",
        "panel_version": "v1.0",
        "confidence": "green",
        "mode_of_inheritance": "AD",
        "phenotypes": "HCM"
    }])

    cv_df = pd.DataFrame([{
        "variation_id": 999001,
        "gene_symbol": "REBUILD_G1",
        "disease_id": "MONDO:0005045",
        "variant_name": "c.1A>G",
        "variant_type": "SNV",
        "clinical_significance": "Pathogenic",
        "is_plp": 1,
        "review_status": "criteria provided, multiple submitters, no conflicts",
        "stars": 2,
        "num_submitters": 3,
        "last_evaluated": "2024-01-01",
        "phenotype_list": "HCM",
        "gnomad_af_global": 0.00001,
        "gnomad_af_popmax": 0.00002,
        "gnomad_popmax_ancestry": "NFE",
        "mcaf_threshold": 0.0001,
        "population_refuted_flag": 0
    }])

    # 3. First Ingestion
    ingest_all_into_db(cg_df, pa_df, cv_df, db_path=test_db)

    with get_connection(test_db, readonly=True) as conn:
        assert conn.execute("SELECT COUNT(*) FROM clingen_curations WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM panelapp_entries WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM clinvar_variants WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        initial_prov = conn.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
        assert initial_prov >= 3

    # 4. Repeated (Idempotent) Ingestion
    ingest_all_into_db(cg_df, pa_df, cv_df, db_path=test_db)

    with get_connection(test_db, readonly=True) as conn:
        # Assert NO duplicate rows created
        assert conn.execute("SELECT COUNT(*) FROM clingen_curations WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM panelapp_entries WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM clinvar_variants WHERE gene_symbol = 'REBUILD_G1'").fetchone()[0] == 1
        # Provenance records updated
        second_prov = conn.execute("SELECT COUNT(*) FROM provenance").fetchone()[0]
        assert second_prov > initial_prov

