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



def mixed_feedback_selection(d: float, frequency: float, environment: float, alpha: float) -> float:
    """Feedback with a tunable linear onset and a quadratic remainder."""
    assert 0.0 <= alpha <= 1.0
    w = alpha * (d / DMAX) + (1.0 - alpha) * (d / DMAX) ** 2
    return intrinsic(d, environment) + ETA * w * (2 * frequency - 1)


def onset_threshold(eta: float = ETA) -> float:
    """alpha_crit = 1 - B_A/eta for the normalized quadratic witness."""
    k_local = 1.0
    k_global = 2.0
    b_access = DMAX * (k_global - k_local)
    return 1.0 - b_access / eta


def test_critical_onset_slope_continuously_changes_invasion_order() -> None:
    alpha_crit = onset_threshold()
    assert isclose(alpha_crit, 1.0 / 3.0)

    e_endpoint = 2.5
    for alpha in (0.0, 0.1, 0.3, alpha_crit, 0.6, 1.0):
        e_partial = 2.0 + ETA * alpha / DMAX
        if isclose(alpha, alpha_crit):
            assert isclose(e_partial, e_endpoint, abs_tol=1e-12)
        elif alpha < alpha_crit:
            assert e_partial < e_endpoint
        else:
            assert e_partial > e_endpoint
        assert isclose(mixed_feedback_selection(1.0, 0.0, e_endpoint, alpha), 0.0)
        h = 1e-8
        numeric = mixed_feedback_selection(h, 0.0, e_partial, alpha) / h
        assert isclose(numeric, 0.0, abs_tol=2e-8)


def test_mixed_feedback_partial_only_invasion_has_finite_window() -> None:
    environment = 2.25
    alpha = 0.1
    for d in (0.01, 0.1, 0.25):
        assert mixed_feedback_selection(d, 0.0, environment, alpha) > 0
        assert isclose(
            mixed_feedback_selection(d, 0.0, environment, alpha),
            0.1 * d - 0.35 * d * d,
            abs_tol=1e-12,
        )
    assert isclose(mixed_feedback_selection(2.0 / 7.0, 0.0, environment, alpha), 0.0, abs_tol=1e-12)
    for d in (0.3, 0.75, 1.0):
        assert mixed_feedback_selection(d, 0.0, environment, alpha) < 0


def test_large_linear_onset_removes_partial_only_invasion() -> None:
    environment = 2.25
    alpha = 0.6
    for d in (0.01, 0.2, 0.6, 1.0):
        expected = -0.65 * d + 0.4 * d * d
        assert isclose(mixed_feedback_selection(d, 0.0, environment, alpha), expected, abs_tol=1e-12)
        assert expected < 0.0


def test_common_linear_cost_shift_preserves_selection_and_positive_cost() -> None:
    # An apparently negative cost at the proportional formal crossing can
    # be removed without altering payoffs by adding the same linear term
    # to structural recovery and architectural cost.
    assert isclose(cost(3.5), -0.5)
    assert isclose(4.0 - 3.5, 0.5)
    for e in (1.5, 2.25, 3.0, 3.5):
        for d in (0.01, 0.25, 0.75, 1.0):
            shifted_intrinsic = (2.0 * d + d * d) - (4.0 - e) * d
            assert isclose(shifted_intrinsic, intrinsic(d, e), abs_tol=1e-12)


def test_paper_distinguishes_reference_access_from_rare_access() -> None:
    manuscript = (ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md").read_text(
        encoding="utf-8"
    )
    theory = (ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md").read_text(
        encoding="utf-8"
    )
    assert "actual local gradient is `g_0-eta w'(0+)`" in manuscript
    assert "rare partial division becomes invasible before complete division" in manuscript
    assert "g_rare(E)" in theory
    assert "E_A,rare=E_A+eta/(c dmax)" in theory
    assert "not a new empirical finding" in theory
    assert "alpha < 1-B_A/eta" in theory
    assert "s_crit" in theory
