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


def test_theory_documents_explicit_conditional_scope() -> None:
    source = (
        ROOT / "theory" / "PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md"
    ).read_text(encoding="utf-8")
    for term in (
        "A_0(u,v)",
        "I_lambda(1|d_*)",
        "lambda=21/10=2.1",
        "not stability conclusions",
        "exactly identical",
        "established partial resident",
    ):
        assert term in source
