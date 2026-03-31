"""Tests for ActionableEvidence verdict engine."""

import sys
import os
import math

sys.path.insert(0, "C:/MetaAudit")
sys.path.insert(0, "C:/Models/ActionableEvidence")

import numpy as np
import pytest

from metaaudit.recompute import RecomputedMA, recompute_ma
from metaaudit.loader import DataType
from compute_verdicts import (
    extract_review_id,
    compute_total_n,
    pi_crosses_null,
    evaluate_criteria,
)
import pandas as pd


# ── Helpers ────────────────────────────────────────────────────────────

def make_recomp(
    k=10, estimate=-0.5, p_value=0.001, significant=True,
    pi_lower=-1.0, pi_upper=-0.1, pi_computable=True,
    tau2=0.05, se=0.1, se_hksj=0.12, I2=50.0, Q=18.0,
    measure="logOR",
):
    """Create a synthetic RecomputedMA for testing."""
    yi = np.zeros(k)
    vi = np.ones(k) * 0.1
    return RecomputedMA(
        k=k, yi=yi, vi=vi, estimate=estimate, se=se, se_hksj=se_hksj,
        ci_lower=estimate - 1.96 * se_hksj, ci_upper=estimate + 1.96 * se_hksj,
        p_value=p_value, tau2=tau2, I2=I2, Q=Q, significant=significant,
        pi_lower=pi_lower, pi_upper=pi_upper, pi_computable=pi_computable,
        data_type=DataType.BINARY, measure=measure,
    )


def make_audit(n_fails=0, pub_bias_fail=False):
    return {"n_fails": n_fails, "pub_bias_fail": pub_bias_fail}


# ── Unit tests: extract_review_id ─────────────────────────────────────

def test_extract_review_id_normal():
    assert extract_review_id("CD000028_pub4_data__A1") == "CD000028"


def test_extract_review_id_long():
    assert extract_review_id("CD012335_pub2_data__A5") == "CD012335"


def test_extract_review_id_no_match():
    assert extract_review_id("invalid_id") == ""


# ── Unit tests: pi_crosses_null ────────────────────────────────────────

def test_pi_crosses_null_yes():
    assert pi_crosses_null(-0.5, 0.3, "logOR") is True


def test_pi_crosses_null_no_negative():
    assert pi_crosses_null(-1.0, -0.1, "logOR") is False


def test_pi_crosses_null_no_positive():
    assert pi_crosses_null(0.1, 1.0, "logOR") is False


def test_pi_crosses_null_boundary():
    # Boundary: PI upper == 0 exactly
    assert pi_crosses_null(-0.5, 0.0, "logOR") is True


# ── Unit tests: evaluate_criteria ──────────────────────────────────────

def test_all_pass_actionable():
    """When all 6 criteria pass, verdict is ACTIONABLE."""
    recomp = make_recomp(k=10, p_value=0.001, significant=True,
                         pi_lower=-1.0, pi_upper=-0.1, pi_computable=True)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["verdict"] == "ACTIONABLE"
    assert result["failed_criteria"] == []


def test_not_significant_fails():
    """Non-significant result -> NOT YET."""
    recomp = make_recomp(k=10, p_value=0.15, significant=False)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["verdict"] == "NOT YET"
    assert "significance" in result["failed_criteria"]


def test_pi_crossing_null_fails():
    """PI crossing null -> NOT YET."""
    recomp = make_recomp(k=10, pi_lower=-0.5, pi_upper=0.3, pi_computable=True)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["verdict"] == "NOT YET"
    assert "prediction_interval" in result["failed_criteria"]


def test_pi_not_computable_passes():
    """k < 3 -> PI not computable -> passes by default."""
    recomp = make_recomp(k=2, pi_computable=False)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["pi_ok"] is True


def test_fragile_fails():
    """Fragile robustness -> NOT YET."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Fragile",
                               fragility_covered=True)
    assert result["verdict"] == "NOT YET"
    assert "robustness" in result["failed_criteria"]


def test_unstable_fails():
    """Unstable robustness -> NOT YET."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Unstable",
                               fragility_covered=True)
    assert "robustness" in result["failed_criteria"]


def test_moderate_passes():
    """Moderate robustness -> passes."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Moderate",
                               fragility_covered=True)
    assert result["robust"] is True


def test_fragility_not_covered_passes():
    """Review not in FragilityAtlas -> benefit of doubt = pass."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class=None,
                               fragility_covered=False)
    assert result["robust"] is True


def test_audit_fails_fail():
    """Any FAIL/CRITICAL audit flag -> NOT YET."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(n_fails=2, pub_bias_fail=False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["verdict"] == "NOT YET"
    assert "audit_flags" in result["failed_criteria"]


def test_no_audit_info_fails():
    """No audit data available -> audit criterion fails."""
    recomp = make_recomp()
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=None,
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["no_fails"] is False


def test_low_k_fails_volume():
    """k < 5 -> evidence volume fails."""
    recomp = make_recomp(k=3)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert "evidence_volume" in result["failed_criteria"]


def test_low_n_fails_volume():
    """total N < 500 -> evidence volume fails."""
    recomp = make_recomp(k=10)
    result = evaluate_criteria(recomp, total_n=200,
                               audit_info=make_audit(0, False),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert "evidence_volume" in result["failed_criteria"]


def test_pub_bias_fail_high_k():
    """k >= 10 and pub_bias FAIL -> NOT YET."""
    recomp = make_recomp(k=15)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, pub_bias_fail=True),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert "pub_bias" in result["failed_criteria"]


def test_pub_bias_low_k_passes():
    """k < 10 -> Egger's not applicable -> passes by default."""
    recomp = make_recomp(k=7)
    result = evaluate_criteria(recomp, total_n=1000,
                               audit_info=make_audit(0, pub_bias_fail=True),
                               fragility_class="Robust",
                               fragility_covered=True)
    assert result["no_pub_bias"] is True


def test_multiple_failures_recorded():
    """Multiple criteria can fail simultaneously."""
    recomp = make_recomp(k=3, p_value=0.5, significant=False,
                         pi_lower=-0.5, pi_upper=0.3, pi_computable=True)
    result = evaluate_criteria(recomp, total_n=100,
                               audit_info=make_audit(n_fails=3, pub_bias_fail=True),
                               fragility_class="Unstable",
                               fragility_covered=True)
    assert result["verdict"] == "NOT YET"
    assert len(result["failed_criteria"]) >= 3
    assert "significance" in result["failed_criteria"]
    assert "evidence_volume" in result["failed_criteria"]
    assert "robustness" in result["failed_criteria"]


# ── Integration test: recompute + evaluate on synthetic binary data ────

def test_recompute_and_evaluate_binary():
    """End-to-end: create binary data, recompute, evaluate."""
    np.random.seed(42)
    k = 8
    df = pd.DataFrame({
        "Experimental.cases": np.array([15, 20, 25, 18, 22, 30, 12, 28]),
        "Experimental.N": np.array([100, 120, 150, 110, 130, 160, 90, 140]),
        "Control.cases": np.array([25, 30, 35, 28, 32, 40, 22, 38]),
        "Control.N": np.array([100, 120, 150, 110, 130, 160, 90, 140]),
    })
    recomp = recompute_ma(df, DataType.BINARY)
    assert recomp.k == k
    # The treatment group has fewer events -> protective effect (negative logOR)
    assert recomp.estimate < 0
    total_n = df["Experimental.N"].sum() + df["Control.N"].sum()
    result = evaluate_criteria(
        recomp, total_n=int(total_n),
        audit_info=make_audit(0, False),
        fragility_class="Robust",
        fragility_covered=True,
    )
    # With clear treatment effect and adequate sample, should be actionable
    assert result["verdict"] == "ACTIONABLE"


def test_recompute_and_evaluate_null_effect():
    """Null effect binary data should be NOT YET."""
    np.random.seed(42)
    df = pd.DataFrame({
        "Experimental.cases": np.array([25, 30, 35, 28, 32, 40]),
        "Experimental.N": np.array([100, 120, 150, 110, 130, 160]),
        "Control.cases": np.array([24, 31, 34, 29, 31, 41]),
        "Control.N": np.array([100, 120, 150, 110, 130, 160]),
    })
    recomp = recompute_ma(df, DataType.BINARY)
    # Nearly identical event rates -> non-significant
    result = evaluate_criteria(
        recomp, total_n=int(df["Experimental.N"].sum() + df["Control.N"].sum()),
        audit_info=make_audit(0, False),
        fragility_class="Robust",
        fragility_covered=True,
    )
    assert result["verdict"] == "NOT YET"
    assert "significance" in result["failed_criteria"]


# ── Test compute_total_n ───────────────────────────────────────────────

def test_compute_total_n_binary():
    df = pd.DataFrame({
        "Experimental.N": [100, 200],
        "Control.N": [100, 200],
    })
    assert compute_total_n(df) == 600


def test_compute_total_n_missing_cols():
    df = pd.DataFrame({"other": [1, 2, 3]})
    assert compute_total_n(df) == 0


# ── Run on small real subset ──────────────────────────────────────────

def test_real_data_5_reviews():
    """Integration: run on 5 real Pairwise70 reviews and verify structure."""
    from metaaudit.loader import load_all_reviews

    PAIRWISE70_DIR = "C:/Users/user/OneDrive - NHS/Documents/Pairwise70/data"
    if not os.path.exists(PAIRWISE70_DIR):
        pytest.skip("Pairwise70 data not available")

    reviews = load_all_reviews(PAIRWISE70_DIR, max_reviews=5)
    assert len(reviews) > 0

    actionable_count = 0
    not_yet_count = 0

    for review in reviews:
        review_id = extract_review_id(review.review_id)
        for ag in review.analyses:
            recomp = recompute_ma(ag.df, ag.data_type)
            total_n = compute_total_n(ag.df)
            result = evaluate_criteria(
                recomp, total_n=total_n,
                audit_info=make_audit(0, False),
                fragility_class="Robust",
                fragility_covered=True,
            )
            assert result["verdict"] in ("ACTIONABLE", "NOT YET")
            assert isinstance(result["failed_criteria"], list)
            if result["verdict"] == "ACTIONABLE":
                actionable_count += 1
            else:
                not_yet_count += 1
                assert len(result["failed_criteria"]) > 0

    # Should have some of each (with 5 reviews, ~40 MAs)
    total = actionable_count + not_yet_count
    assert total > 0
    print(f"5-review test: {actionable_count} ACTIONABLE, {not_yet_count} NOT YET out of {total}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
