"""Conditional clustered-founder ecology for the partial-resident SLK witness.

Every number is a model consequence, not a natural-population estimate.
"""

from math import isclose
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ETA = 1.5
PARTIAL = 1.0 / 7.0


def intrinsic(d: float) -> float:
    return 0.25 * d + d * d


def dependence(d: float) -> float:
    return 0.1 * d + 0.9 * d * d


def mismatch(u: float, v: float) -> float:
    return abs(dependence(u) - dependence(v))


def conditional_encounters(p: float, r: float) -> tuple[float, float, float, float]:
    """P(v|u), P(u|v), P(u|u), P(v|v)."""
    assert 0.0 < p < 1.0
    assert 0.0 <= r <= 1.0
    return (
        (1.0 - r) * (1.0 - p),
        (1.0 - r) * p,
        r + (1.0 - r) * p,
        r + (1.0 - r) * (1.0 - p),
    )


def selection_from_encounters(u: float, v: float, p: float, r: float) -> float:
    other_for_u, other_for_v, _, _ = conditional_encounters(p, r)
    mismatch_cost = ETA * mismatch(u, v)
    return (intrinsic(u) - mismatch_cost * other_for_u) - (
        intrinsic(v) - mismatch_cost * other_for_v
    )


def direct_selection(u: float, v: float, p: float, r: float) -> float:
    a = intrinsic(u) - intrinsic(v)
    b = ETA * mismatch(u, v)
    return a + b * (1.0 - r) * (2.0 * p - 1.0)


def threshold(r: float) -> float:
    a = intrinsic(1.0) - intrinsic(PARTIAL)
    b = ETA * mismatch(1.0, PARTIAL)
    return 0.5 - a / (2.0 * b * (1.0 - r))


@pytest.mark.parametrize("p", [0.01, 0.10, 0.33, 0.50, 0.81, 0.99])
@pytest.mark.parametrize("r", [0.0, 0.1, 0.2, 0.5, 1.0])
def test_encounters_are_valid_and_reciprocal(p: float, r: float) -> None:
    v_for_u, u_for_v, u_for_u, v_for_v = conditional_encounters(p, r)
    assert all(0.0 <= z <= 1.0 for z in (v_for_u, u_for_v, u_for_u, v_for_v))
    assert isclose(v_for_u + u_for_u, 1.0, abs_tol=1e-14)
    assert isclose(u_for_v + v_for_v, 1.0, abs_tol=1e-14)
    assert isclose(p * v_for_u, (1.0 - p) * u_for_v, abs_tol=1e-14)
    assert isclose(
        selection_from_encounters(1.0, PARTIAL, p, r),
        direct_selection(1.0, PARTIAL, p, r),
        abs_tol=1e-14,
    )


def test_previous_random_mixing_frequency_threshold_recovered() -> None:
    assert isclose(intrinsic(1.0) - intrinsic(PARTIAL), 117.0 / 98.0)
    assert isclose(ETA * mismatch(1.0, PARTIAL), 711.0 / 490.0)
    assert isclose(threshold(0.0), 7.0 / 79.0, abs_tol=1e-14)
    assert isclose(direct_selection(1.0, PARTIAL, threshold(0.0), 0.0), 0.0, abs_tol=1e-14)


def test_assortment_decreases_required_global_founder_fraction() -> None:
    assert isclose(threshold(0.1), 61.0 / 1422.0, abs_tol=1e-14)
    assert isclose(threshold(0.2), -9.0 / 632.0, abs_tol=1e-14)
    assert isclose(1.0 - ((117.0 / 98.0) / (711.0 / 490.0)), 14.0 / 79.0)
    assert threshold(0.0) > threshold(0.1) > 0.0 > threshold(0.2)
    assert direct_selection(1.0, PARTIAL, 0.02, 0.0) < 0.0
    assert direct_selection(1.0, PARTIAL, 0.02, 0.2) > 0.0


@pytest.mark.parametrize("p", [0.05, 0.2, 0.5, 0.8, 0.95])
def test_assortment_effect_changes_sign_at_equal_frequency(p: float) -> None:
    low_r = direct_selection(1.0, PARTIAL, p, 0.0)
    high_r = direct_selection(1.0, PARTIAL, p, 0.5)
    if p < 0.5:
        assert high_r > low_r
    elif p > 0.5:
        assert high_r < low_r
    else:
        assert isclose(low_r, high_r, abs_tol=1e-14)
        assert isclose(high_r, 117.0 / 98.0, abs_tol=1e-14)


def test_assortment_does_not_rescue_an_isolated_mutant_by_assumption() -> None:
    # Model a singleton in a finite neighborhood with no same-type peers.
    # The r>0 limit is only available to clustered multi-individual founders.
    n = 10000
    singleton_frequency = 1.0 / n
    assert direct_selection(1.0, PARTIAL, singleton_frequency, 0.0) < 0.0
    assert direct_selection(1.0, PARTIAL, singleton_frequency, 0.2) > 0.0
    # The second algebraic value is NOT a realizable singleton prediction.
    # Enforce that its biological interpretation is spelled out in source.
    source = (ROOT / "theory" / "ASSORTMENT_PARTIAL_FOUNDER_V1.md").read_text(
        encoding="utf-8"
    )
    assert "do **not rescue an isolated single mutant**" in source
    assert "globally rare but internally clustered propagules" in source


def test_assortment_extension_is_registered_as_conditional_only() -> None:
    source = (ROOT / "theory" / "ASSORTMENT_PARTIAL_FOUNDER_V1.md").read_text(
        encoding="utf-8"
    )
    assert "encounter reciprocity" in source
    assert "r_crit=14/79" in source
    assert "crossover signature" in source
    assert "not a first discovery of spatial rescue" in source
    assert "not population density" in source
