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
    assert "do not rescue an isolated single mutant**" in source
    assert "globally rare but internally clustered propagules" in source



def complementary_role_selection(p: float, r: float, intrinsic_gap: float = -0.25, benefit: float = 1.0) -> float:
    """Unlike-type contacts support both role specialists."""
    _, _, _, _ = conditional_encounters(p, r)
    return intrinsic_gap + benefit * (1.0 - r) * (1.0 - 2.0*p)


@pytest.mark.parametrize("p", [0.1, 0.25, 0.5, 0.75, 0.9])
def test_partner_matching_and_complementarity_reverse_assortment_effects(p: float) -> None:
    # Full D versus partial P has a mismatch loss when unlike;
    # the separate cross-role game has a BENEFIT from unlike encounters.
    m_low = direct_selection(1.0, PARTIAL, p, 0.0)
    m_high = direct_selection(1.0, PARTIAL, p, 0.5)
    c_low = complementary_role_selection(p, 0.0)
    c_high = complementary_role_selection(p, 0.5)
    if p < 0.5:
        assert m_high > m_low
        assert c_high < c_low
    elif p > 0.5:
        assert m_high < m_low
        assert c_high > c_low
    else:
        assert isclose(m_low, m_high, abs_tol=1e-12)
        assert isclose(c_low, c_high, abs_tol=1e-12)


def test_cross_role_benefit_needs_heterotypic_contacts() -> None:
    # This is a within-divided-collective model and NOT S->D invasion.
    assert isclose(complementary_role_selection(0.1, 0.0), 0.55)
    assert isclose(complementary_role_selection(0.1, 0.8), -0.09)
    assert complementary_role_selection(0.001, 0.0) > 0
    assert complementary_role_selection(0.001, 0.8) < 0
    assert isclose(complementary_role_selection(0.375, 0.0), 0.0)
    assert isclose(complementary_role_selection(0.25, 0.5), 0.0)
    assert isclose(complementary_role_selection(0.001, 0.75), -0.0005, abs_tol=1e-12)


def test_contact_polarity_distinguishes_functional_scale() -> None:
    source = (ROOT / "theory" / "ASSORTMENT_PARTIAL_FOUNDER_V1.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "Complementary spatial organization",
        "Within-flower structural division",
        "does **not** automatically represent microbial division",
        "Delta_complement",
        "p_star(r)",
        "not invasion of a complete divided organization",
        "Effective encounter topology",
    ):
        assert token in source


def endogenous_assortment(p: float, center: float, slope: float) -> float:
    """A bounded example of partner sorting that depends on local frequency."""
    import math

    return 0.2 + 0.7 / (1.0 + math.exp(-slope * (p - center)))


def matched_selection_with_sorting(p: float) -> float:
    return direct_selection(1.0, PARTIAL, p, endogenous_assortment(p, 0.8, 40.0))


def complementary_selection_with_sorting(p: float) -> float:
    return complementary_role_selection(p, endogenous_assortment(p, 0.2, -40.0))


def test_endogenous_sorting_changes_realized_frequency_gradient() -> None:
    step = 1e-5
    # With r fixed, matching creates positive frequency dependence.
    p_high = 0.8
    r_high = endogenous_assortment(p_high, 0.8, 40.0)
    assert direct_selection(1.0, PARTIAL, p_high + step, r_high) > direct_selection(
        1.0, PARTIAL, p_high - step, r_high
    )
    # But a rapid increase of partner sorting with p can reverse the
    # observed selection-frequency slope, without reversing the effect
    # of a controlled r intervention at fixed p.
    assert matched_selection_with_sorting(p_high + step) < matched_selection_with_sorting(
        p_high - step
    )
    assert direct_selection(1.0, PARTIAL, p_high, r_high + 0.01) < direct_selection(
        1.0, PARTIAL, p_high, r_high
    )

    # Fixed r in the unlike-role complementarity model creates a
    # negative frequency slope; endogenous sorting can reverse it.
    p_low = 0.2
    r_low = endogenous_assortment(p_low, 0.2, -40.0)
    assert complementary_role_selection(p_low + step, r_low) < complementary_role_selection(
        p_low - step, r_low
    )
    assert complementary_selection_with_sorting(p_low + step) > complementary_selection_with_sorting(
        p_low - step
    )
    assert complementary_role_selection(p_low, r_low + 0.01) < complementary_role_selection(
        p_low, r_low
    )


def test_literature_audit_marks_both_causal_directions_not_slk_gate_closure() -> None:
    theory = (ROOT / "theory" / "ASSORTMENT_PARTIAL_FOUNDER_V1.md").read_text(
        encoding="utf-8"
    )
    evidence = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "van Gestel et al. (2014",
        "Momeni, Brileya, Fields & Shou (2013",
        "d Delta_match/dp",
        "d Delta_complement/dp",
        "final spatial snapshot is insufficient",
        "not** a division-of-labour comparison",
    ):
        assert token in theory, token
    for token in (
        "Two causal arrows are already experimentally documented",
        "founder density was manipulated",
        "reverse causal direction",
        "does not establish whether arrangement caused",
    ):
        assert token in evidence, token

def test_assortment_extension_is_registered_as_conditional_only() -> None:
    source = (ROOT / "theory" / "ASSORTMENT_PARTIAL_FOUNDER_V1.md").read_text(
        encoding="utf-8"
    )
    assert "encounter reciprocity" in source
    assert "r_crit=14/79" in source
    assert "crossover signature" in source
    assert "not a first discovery of spatial rescue" in source
    assert "not population density" in source
