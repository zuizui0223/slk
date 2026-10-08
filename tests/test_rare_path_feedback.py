"""Guard the distinction between intrinsic accessibility and rare-mutant accessibility.

The numerical witness shares the existing UTA1.4c constants.  No observed
organism is fitted by these synthetic parameters.
"""

from math import isclose
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DMAX = 1.0
ETA = 1.5


def cost(environment: float) -> float:
    return 3.0 - environment


def intrinsic(d: float, environment: float) -> float:
    return d + d * d - cost(environment) * d


def selection(d: float, frequency: float, environment: float, exponent: float) -> float:
    return intrinsic(d, environment) + ETA * (d / DMAX) ** exponent * (
        2 * frequency - 1
    )


def intrinsic_local_gradient(environment: float) -> float:
    return 1.0 - cost(environment)


def rare_local_gradient(environment: float, exponent: float) -> float:
    feedback_slope = 1.0 / DMAX if exponent == 1.0 else 0.0
    return intrinsic_local_gradient(environment) - ETA * feedback_slope


def test_reference_turnover_is_conditional_on_feedback_shape() -> None:
    e_value = 1.0
    e_access = 2.0
    e_endpoint_rare = 2.5
    e_rare_partial_proportional = 3.5
    assert e_value < e_access < e_endpoint_rare < e_rare_partial_proportional
    assert isclose(intrinsic(1.0, e_value), 0.0)
    assert isclose(intrinsic_local_gradient(e_access), 0.0)
    assert isclose(selection(1.0, 0.0, e_endpoint_rare, 1.0), 0.0)
    assert isclose(rare_local_gradient(e_rare_partial_proportional, 1.0), 0.0)


def test_proportional_feedback_blocks_rare_small_steps_after_intrinsic_access() -> None:
    environment = 2.25
    assert intrinsic_local_gradient(environment) > 0
    assert isclose(rare_local_gradient(environment, 1.0), -1.25)
    assert selection(0.01, 0.0, environment, 1.0) < 0
    assert selection(1.0, 0.0, environment, 1.0) < 0


def test_full_division_can_invade_before_rare_small_step_under_proportional_feedback() -> None:
    environment = 3.0
    assert selection(1.0, 0.0, environment, 1.0) > 0
    assert rare_local_gradient(environment, 1.0) < 0
    assert selection(0.01, 0.0, environment, 1.0) < 0


def test_quadratic_feedback_opens_rare_partial_window_before_full_division() -> None:
    environment = 2.25
    assert isclose(rare_local_gradient(environment, 2.0), 0.25)
    assert isclose(selection(0.25, 0.0, environment, 2.0), 0.03125)
    assert selection(0.49, 0.0, environment, 2.0) > 0
    assert isclose(selection(0.5, 0.0, environment, 2.0), 0.0)
    assert selection(0.75, 0.0, environment, 2.0) < 0
    assert isclose(selection(1.0, 0.0, environment, 2.0), -0.25)


def test_near_zero_numeric_limit_matches_analytic_local_gradient() -> None:
    for environment in (1.5, 2.25, 3.0, 3.75):
        for exponent in (1.0, 2.0, 4.0):
            numeric = selection(1e-8, 0.0, environment, exponent) / 1e-8
            analytic = rare_local_gradient(environment, exponent)
            assert isclose(numeric, analytic, abs_tol=2e-8)


def test_paper_distinguishes_reference_access_from_rare_access() -> None:
    manuscript = (ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md").read_text(
        encoding="utf-8"
    )
    theory = (ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md").read_text(
        encoding="utf-8"
    )
    assert "actual local gradient is `g_0-eta w'(0+)`" in manuscript
    assert "rare intermediates can still be disfavored after `E_A`" in manuscript
    assert "g_rare(E)" in theory
    assert "E_A,rare=E_A+eta/(c dmax)" in theory
    assert "not a new empirical finding" in theory
