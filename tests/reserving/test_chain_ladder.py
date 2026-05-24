"""Tests for reserving.chain_ladder: normal, edge, and failure cases."""

import numpy as np
import pytest

from pystatsinsurance import reserving

NAN = np.nan

# A small triangle with hand-computable factors:
#   f0 = (150+165)/(100+110) = 1.5
#   f1 = 180/150           = 1.2
TRIANGLE = [
    [100.0, 150.0, 180.0],
    [110.0, 165.0, NAN],
    [120.0, NAN, NAN],
]


# ---------------------------------------------------------------------------
# Normal cases
# ---------------------------------------------------------------------------

def test_development_factors():
    r = reserving.chain_ladder(TRIANGLE)
    assert r.development_factors == pytest.approx([1.5, 1.2])


def test_ultimates_and_reserves():
    r = reserving.chain_ladder(TRIANGLE)
    assert r.ultimates == pytest.approx([180.0, 198.0, 216.0])
    assert r.latest == pytest.approx([180.0, 165.0, 120.0])
    assert r.reserves == pytest.approx([0.0, 33.0, 96.0])
    assert r.total_reserve == pytest.approx(129.0)


def test_full_triangle_completed():
    r = reserving.chain_ladder(TRIANGLE)
    # Known cells unchanged, unknowns filled by projection.
    assert r.full_triangle[1, 2] == pytest.approx(198.0)
    assert r.full_triangle[2, 1] == pytest.approx(180.0)
    assert r.full_triangle[2, 2] == pytest.approx(216.0)
    assert not np.any(np.isnan(r.full_triangle))


def test_reserve_equals_ultimate_minus_latest():
    r = reserving.chain_ladder(TRIANGLE)
    assert r.reserves == pytest.approx(r.ultimates - r.latest)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_fully_developed_square_has_zero_reserves():
    # No NaN: every origin is already at ultimate -> reserves are zero.
    full = [
        [100.0, 150.0, 180.0],
        [110.0, 165.0, 198.0],
        [120.0, 180.0, 216.0],
    ]
    r = reserving.chain_ladder(full)
    assert r.total_reserve == pytest.approx(0.0)
    assert r.reserves == pytest.approx([0.0, 0.0, 0.0])


def test_accepts_numpy_array_input():
    r = reserving.chain_ladder(np.array(TRIANGLE))
    assert r.total_reserve == pytest.approx(129.0)


def test_summary_is_string():
    r = reserving.chain_ladder(TRIANGLE)
    assert isinstance(r.summary(), str)
    assert "Chain-Ladder" in r.summary()


# ---------------------------------------------------------------------------
# Failure cases
# ---------------------------------------------------------------------------

def test_ragged_row_raises():
    bad = [[100.0, NAN, 180.0], [110.0, 165.0, 200.0]]
    with pytest.raises(ValueError, match="ragged"):
        reserving.chain_ladder(bad)


def test_increasing_known_counts_raises():
    bad = [[100.0, NAN], [110.0, 165.0]]
    with pytest.raises(ValueError, match="run-off triangle"):
        reserving.chain_ladder(bad)


def test_negative_value_raises():
    bad = [[100.0, 150.0], [-110.0, 165.0]]
    with pytest.raises(ValueError, match="negative"):
        reserving.chain_ladder(bad)


def test_too_small_raises():
    with pytest.raises(ValueError, match="at least 2x2"):
        reserving.chain_ladder([[100.0], [110.0]])


def test_not_2d_raises():
    with pytest.raises(ValueError, match="2-dimensional"):
        reserving.chain_ladder([100.0, 150.0, 180.0])


def test_zero_denominator_factor_raises():
    # First development column is all zeros -> factor undefined.
    bad = [[0.0, 150.0, 180.0], [0.0, 165.0, NAN], [0.0, NAN, NAN]]
    with pytest.raises(ValueError, match="sum to zero"):
        reserving.chain_ladder(bad)
