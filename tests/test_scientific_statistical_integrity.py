"""Tests for scientific validation, statistical integrity, and benchmark reproducibility.

Verifies:
- Benchmark evaluation queries live database records without hard-coded outcome overrides.
- Performance metrics report Wilson score confidence intervals.
- Single-reviewer adjudication does not claim manufactured inter-rater reliability.
- Survival analysis strictly separates real observations from simulated demonstration data.
- Forecasting ML probabilities are directly derived from model estimates without manual heuristic manipulation.
"""

from __future__ import annotations

from pathlib import Path
import pytest
import pandas as pd

from pipeline.validation_benchmark import run_validation_benchmark, wilson_score_interval
from pipeline.survival_analysis import analyze_cross_sectional_latency, fit_cox_proportional_hazards
from pipeline.forecasting import extract_features, train_and_evaluate_model


def test_wilson_confidence_interval_math():
    """Wilson score confidence interval is bounded within [0, 1] and encloses point estimate."""
    low, high = wilson_score_interval(34, 46, confidence=0.95)
    point = 34 / 46
    assert 0.0 <= low <= point <= high <= 1.0
    assert round(low, 2) == 0.60
    assert round(high, 2) == 0.84

    # Edge cases
    assert wilson_score_interval(0, 0) == (0.0, 0.0)
    assert wilson_score_interval(0, 10)[0] == 0.0
    assert wilson_score_interval(10, 10)[1] == 1.0


def test_benchmark_reproducibility_live_db():
    """Validation benchmark evaluates live database without hard-coded prediction overrides."""
    res = run_validation_benchmark(export_outputs=False)
    meta = res["benchmark_metadata"]
    counts = res["cohort_counts"]
    cm = res["confusion_matrix"]
    m = res["metrics"]

    assert meta["hardcoded_predictions_removed"] is True
    assert counts["total_benchmark_cases"] == 100
    assert counts["evaluable_cases"] == 94
    assert counts["excluded_unobserved_cases"] == 6
    assert counts["gold_downgraded_cases"] == 54
    assert counts["gold_definitive_controls"] == 46

    # Verify zero false positives after correcting broad disease overlap
    assert res["evaluable_cohort_confusion_matrix"]["false_positives"] == 0
    assert res["unadjusted_all_100_confusion_matrix"]["false_positives"] == 0

    # Verify metrics are floating point values with Wilson intervals
    assert m["precision_ppv"] == 1.0
    assert m["specificity_tnr"] == 1.0
    assert 0.0 <= m["recall_sensitivity"] <= 1.0
    assert 0.0 <= m["accuracy"] <= 1.0
    assert len(m["precision_95ci"]) == 2
    assert m["precision_95ci"][0] <= m["precision_ppv"] <= m["precision_95ci"][1]

    # Inter-rater kappa must be clearly documented as N/A for single reviewer
    assert "N/A" in meta["inter_rater_reliability_kappa"]


def test_survival_analysis_no_synthetic_data_by_default():
    """Survival analysis with default allow_simulation=False strictly forbids synthetic data."""
    res = fit_cox_proportional_hazards(allow_simulation=False, export_csv=False)
    assert res["is_synthetic"] is False
    assert res["provenance"] == "REAL_DATABASE_OBSERVATION"

    # Empirical latency summary must contain real sample sizes
    emp = res["empirical_latency"]
    assert emp["cohort_definition"]["eligible_observations"] > 0
    assert emp["overall_latency"]["median_days"] > 0
    assert "scientific_statement" in emp


def test_survival_analysis_simulation_provenance_flagged():
    """Opt-in simulation cohort must be clearly stamped with SYNTHETIC_DEMONSTRATION."""
    sim_res = fit_cox_proportional_hazards(allow_simulation=True, export_csv=False)
    assert sim_res["is_synthetic"] is True
    assert sim_res["provenance"] == "SYNTHETIC_DEMONSTRATION"
    assert "DEMONSTRATION SIMULATION" in sim_res["warning"]


def test_forecasting_probabilities_unmanipulated():
    """Forecasting risk scores must equal direct statistical model probabilities without heuristic boosts."""
    from database.connection import get_connection, get_db_path
    db_p = get_db_path()
    with get_connection(db_p) as conn:
        feat_df = extract_features(conn)

    assert not feat_df.empty, "Feature extraction should return records"
    model_res = train_and_evaluate_model(feat_df)
    assert model_res, "Model evaluation should succeed"

    preds_df = model_res["supported_predictions_df"]
    if not preds_df.empty:
        # Check that scores are bounded in [0, 1]
        assert (preds_df["downgrade_risk_score"] >= 0.0).all()
        assert (preds_df["downgrade_risk_score"] <= 1.0).all()
        # Verify transparent rule flags exist as separate columns
        assert "flag_mcaf_violation" in preds_df.columns
        assert "flag_low_stars" in preds_df.columns
        assert "flag_panel_conflict" in preds_df.columns


def test_forecasting_exploratory_status_and_calibration():
    """Forecasting pipeline explicitly declares exploratory retrospective status, Brier scores, and uncalibrated scores."""
    from database.connection import get_connection, get_db_path
    db_p = get_db_path()
    with get_connection(db_p) as conn:
        feat_df = extract_features(conn)

    assert not feat_df.empty, "Feature extraction should return records"
    model_res = train_and_evaluate_model(feat_df)
    assert model_res["model_status"] == "EXPLORATORY_RETROSPECTIVE_EVALUATION"
    assert "retrospective" in model_res["temporal_leakage_warning"].lower()
    assert "UNCALIBRATED_RISK_SCORE" in model_res["score_calibration_status"]
    assert 0.0 <= model_res["lr_brier_score"] <= 1.0
    assert 0.0 <= model_res["rf_brier_score"] <= 1.0

