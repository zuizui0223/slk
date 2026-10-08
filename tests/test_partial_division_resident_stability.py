"""Model witnesses: invasion from integration does not decide partial-resident stability."""

from math import isclose
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ETA = 1.5
ALPHA = 0.1
D_STAR = 1.0 / 7.0


def intrinsic(d: float) -> float:
    return 0.25 * d + d * d


def dependence(d: float) -> float:
    return ALPHA * d + (1.0 - ALPHA) * d * d


def payoff(u: float, v: float, interaction_strength: float = 0.0) -> float:
    return (
        intrinsic(u)
        - ETA * abs(dependence(u) - dependence(v))
        + interaction_strength * u * v * (u - v)
    )


def rare_invasion(u: float, resident: float, interaction_strength: float = 0.0) -> float:
    return payoff(u, resident, interaction_strength) - payoff(
        resident, resident, interaction_strength
    )


def s_vs_d_selection(d: float, mutant_frequency: float, strength: float) -> float:
    p = mutant_frequency
    w_d = p * payoff(d, d, strength) + (1.0 - p) * payoff(d, 0.0, strength)
    w_s = p * payoff(0.0, d, strength) + (1.0 - p) * payoff(
        0.0, 0.0, strength
    )
    return w_d - w_s


@pytest.mark.parametrize("strength", [0.0, 1.0, 3.0, 10.0])
def test_every_s_vs_d_frequency_curve_is_identical_to_registered_model(
    strength: float,
) -> None:
    for d in (0.02, 0.1, D_STAR, 0.25, 0.5, 0.75, 1.0):
        for p in (0.0, 0.01, 0.1, 0.3, 0.5, 0.9, 1.0):
            expected = intrinsic(d) + ETA * dependence(d) * (2.0 * p - 1.0)
            assert isclose(
                s_vs_d_selection(d, p, strength), expected, abs_tol=1e-12
            )


def test_partial_only_invasion_and_best_initial_founder() -> None:
    assert rare_invasion(0.1, 0.0) > 0
    assert isclose(rare_invasion(D_STAR, 0.0), 1.0 / 140.0, abs_tol=1e-12)
    assert isclose(rare_invasion(2.0 / 7.0, 0.0), 0.0, abs_tol=1e-12)
    assert rare_invasion(0.5, 0.0) < 0
    assert isclose(rare_invasion(1.0, 0.0), -0.25, abs_tol=1e-12)
    # H(d)=0.1d-0.35d^2 is strictly concave, with vertex at 1/7.
    for d in (0.001, 0.05, 0.11, 0.19, 0.25, 0.75, 1.0):
        assert rare_invasion(d, 0.0) < rare_invasion(D_STAR, 0.0)


def test_symmetric_mismatch_model_stabilizes_many_partial_residents() -> None:
    # H(d) decreases for d>1/7 and J(d) increases throughout [0,1].
    for resident in (D_STAR, 0.2, 0.35, 0.5, 0.8, 1.0):
        for n in range(201):
            mutant = n / 200.0
            if isclose(mutant, resident, abs_tol=1e-12):
                continue
            assert rare_invasion(mutant, resident) < 1e-12


def test_one_partial_resident_can_replace_integration_when_rare() -> None:
    for p in (0.0, 0.1, 0.5, 0.9, 1.0):
        assert s_vs_d_selection(D_STAR, p, 0.0) > 0


def test_advanced_mutant_invasion_is_not_identified_by_s_comparisons() -> None:
    # Both models have full division losing against integrated S.
    for strength in (0.0, 2.1, 3.0):
        assert isclose(rare_invasion(1.0, 0.0, strength), -0.25)
        assert isclose(rare_invasion(D_STAR, 0.0, strength), 1.0 / 140.0)
    # But changing specialist-specialist interactions flips later invasion.
    assert rare_invasion(1.0, D_STAR, 0.0) < 0
    assert isclose(rare_invasion(1.0, D_STAR, 2.1), 0.0, abs_tol=1e-12)
    assert isclose(
        rare_invasion(1.0, D_STAR, 3.0), 27.0 / 245.0, abs_tol=1e-12
    )
    assert rare_invasion(D_STAR, 1.0, 3.0) < 0


def test_directional_resident_interaction_allows_small_step_continuation() -> None:
    # H'(v)+lambda*v^2 >= 0.1-0.49/12 > 0 at lambda=3.
    minimum_upward_slope = 0.1 - 0.49 / 12.0
    assert minimum_upward_slope > 0
    for index in range(100):
        resident = index / 100.0
        mutant = resident + 1e-5
        assert rare_invasion(mutant, resident, 3.0) > 0
        if resident >= 1e-5:
            assert rare_invasion(resident - 1e-5, resident, 3.0) < 0



def smooth_mismatch(u: float, v: float, exponent: float) -> float:
    left = dependence(u)
    right = dependence(v)
    if isclose(left + right, 0.0, abs_tol=0.0):
        return 0.0
    return abs(left - right) ** exponent / (left + right) ** (exponent - 1.0)


def smooth_payoff(u: float, v: float, exponent: float) -> float:
    return intrinsic(u) - ETA * smooth_mismatch(u, v, exponent)


def smooth_invasion(u: float, resident: float, exponent: float) -> float:
    return smooth_payoff(u, resident, exponent) - smooth_payoff(
        resident, resident, exponent
    )


@pytest.mark.parametrize("exponent", [1.0, 1.5, 2.0, 4.0])
def test_symmetric_mismatch_models_preserve_all_s_vs_d_assays(
    exponent: float,
) -> None:
    for d in (0.01, D_STAR, 0.25, 0.5, 1.0):
        assert isclose(smooth_mismatch(d, 0.0, exponent), dependence(d))
        assert isclose(smooth_mismatch(d, d, exponent), 0.0)
        for p in (0.0, 0.1, 0.5, 0.9, 1.0):
            test_w_d = p * smooth_payoff(d, d, exponent) + (1-p) * smooth_payoff(d, 0.0, exponent)
            test_w_s = p * smooth_payoff(0.0, d, exponent) + (1-p) * smooth_payoff(0.0, 0.0, exponent)
            expected = intrinsic(d) + ETA * dependence(d) * (2*p-1)
            assert isclose(test_w_d - test_w_s, expected, abs_tol=1e-12)


def test_smooth_symmetric_mismatch_allows_continued_small_step_specialization() -> None:
    step = 1e-6
    for resident in (0.001, 0.01, 0.05, D_STAR, 0.2, 0.5, 0.9, 0.99):
        assert smooth_invasion(resident + step, resident, 2.0) > 0
        assert smooth_invasion(resident - step, resident, 2.0) < 0
        observed_gradient = smooth_invasion(resident + step, resident, 2.0) / step
        assert isclose(observed_gradient, 0.25 + 2.0 * resident, abs_tol=0.001)



def test_smooth_mismatch_has_a_stepping_stone_threshold_for_full_division() -> None:
    # New full D cannot invade S or the first partial founder, but can
    # invade a sufficiently advanced partial resident.
    assert smooth_invasion(1.0, 0.0, 2.0) < 0
    assert smooth_invasion(1.0, D_STAR, 2.0) < 0
    left, right = 0.2, 0.5
    assert smooth_invasion(1.0, left, 2.0) < 0
    assert smooth_invasion(1.0, right, 2.0) > 0
    for _ in range(65):
        mid = (left + right) / 2.0
        if smooth_invasion(1.0, mid, 2.0) > 0:
            right = mid
        else:
            left = mid
    threshold = (left + right) / 2.0
    assert isclose(threshold, 0.28615302603084614, abs_tol=1e-12)
    assert threshold > 2.0 / 7.0
    assert threshold < 0.3
    assert smooth_invasion(1.0, 0.3, 2.0) > 0
    assert smooth_invasion(0.3, 0.0, 2.0) < 0
    assert smooth_invasion(0.3, 0.25, 2.0) > 0

def test_cusp_and_smooth_payoffs_disagree_after_partial_becomes_resident() -> None:
    assert smooth_invasion(D_STAR, 0.0, 2.0) > 0
    assert smooth_invasion(1.0, 0.0, 2.0) < 0
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 1.0) < 0
    assert smooth_invasion(D_STAR + 1e-5, D_STAR, 2.0) > 0
    assert smooth_invasion(1.0, D_STAR, 2.0) < 0


def mutant_frequency_threshold(u: float, v: float, exponent: float = 1.0) -> float:
    mismatch = smooth_mismatch(u, v, exponent)
    assert mismatch > 0.0
    return 0.5 - (intrinsic(u) - intrinsic(v)) / (2.0 * ETA * mismatch)


def s_vs_partial_pair_selection(u: float, v: float, p: float, exponent: float = 1.0) -> float:
    return intrinsic(u) - intrinsic(v) + ETA * smooth_mismatch(u, v, exponent) * (2.0*p - 1.0)


def test_exact_finite_introduction_overcomes_rare_resistance_of_partial_resident() -> None:
    u, v = 1.0, D_STAR
    assert isclose(intrinsic(u)-intrinsic(v), 117.0/98.0, abs_tol=1e-12)
    assert isclose(ETA*smooth_mismatch(u, v, 1.0), 711.0/490.0, abs_tol=1e-12)
    assert isclose(smooth_invasion(u, v, 1.0), -9.0/35.0, abs_tol=1e-12)
    p_critical = mutant_frequency_threshold(u, v, 1.0)
    assert isclose(p_critical, 7.0/79.0, abs_tol=1e-12)
    assert s_vs_partial_pair_selection(u, v, 0.05) < 0.0
    assert isclose(s_vs_partial_pair_selection(u, v, p_critical), 0.0, abs_tol=1e-12)
    assert s_vs_partial_pair_selection(u, v, 0.10) > 0.0


def test_uninvadable_partial_degree_has_no_uniform_founding_frequency_margin() -> None:
    for delta in (0.5, 0.1, 0.01, 1e-3, 1e-5):
        u = D_STAR + delta
        expected_rare = -(7.0/20.0)*delta*delta
        expected_frequency = 49.0*delta/(150.0+378.0*delta)
        assert isclose(smooth_invasion(u, D_STAR, 1.0), expected_rare, abs_tol=1e-12)
        assert isclose(mutant_frequency_threshold(u, D_STAR, 1.0), expected_frequency, abs_tol=2e-11)
        assert expected_frequency > 0.0
        assert s_vs_partial_pair_selection(u, D_STAR, expected_frequency*1.5) > 0.0
    assert mutant_frequency_threshold(D_STAR+1e-5, D_STAR) < 0.000004


def test_fixed_finite_coalition_does_not_increase_arbitrarily_close_to_rarity() -> None:
    resident = D_STAR
    types = (0.25, 0.50)
    proportions = (0.4, 0.6)
    assert all(smooth_invasion(u, resident, 1.0) < 0.0 for u in types)

    def average_payoff(focal: float, epsilon: float) -> float:
        return (1.0-epsilon)*payoff(focal, resident) + epsilon*sum(
            q*payoff(focal, u) for q, u in zip(proportions, types)
        )

    for epsilon in (1e-8, 1e-6, 1e-4):
        for u in types:
            assert average_payoff(u, epsilon) < average_payoff(resident, epsilon)

def test_theory_documents_explicit_conditional_scope() -> None:
    source = (
        ROOT / "theory" / "PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md"
    ).read_text(encoding="utf-8")
    for term in (
        "A_0(u,v)",
        "M_q(d,0)=w(d)",
        "q=2",
        "p_escape(1|1/7) = 7/79",
        "49 delta/(150+378 delta)",
        "I_lambda(1|d_*)",
        "lambda=21/10=2.1",
        "not stability conclusions",
        "exactly identical",
        "established partial resident",
    ):
        assert term in source
