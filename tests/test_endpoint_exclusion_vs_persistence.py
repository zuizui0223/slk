"""Endpoint invasion is not a certificate of whole-continuum resident persistence.

All values here are exact algebraic model witnesses, not empirical estimates.
"""

from math import isclose
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ETA = 1.5
DMAX = 1.0
E = 2.25


def intrinsic_release(d: float, environment: float = E) -> float:
    return d + d * d - (3.0 - environment) * d


def rare_selection(d: float, exponent: float, environment: float = E) -> float:
    return intrinsic_release(d, environment) - ETA * d**exponent


@pytest.mark.parametrize("exponent", [1.0, 2.0, 4.0])
def test_same_endpoint_is_excluded_under_both_feedback_shapes(exponent: float) -> None:
    assert isclose(rare_selection(DMAX, exponent), -0.25)
    assert isclose(intrinsic_release(DMAX), 1.25)
    assert isclose((1.0 - (3.0 - E)), 0.25)


def test_proportional_feedback_endpoint_exclusion_certifies_all_partial_degrees() -> None:
    # R(d)/d=1+d is increasing, so H(d)/d <= H(1).
    assert isclose(rare_selection(1.0, 1.0), -0.25)
    for i in range(1, 10001):
        d = i / 10000.0
        assert rare_selection(d, 1.0) < 0.0
        assert isclose(rare_selection(d, 1.0), -1.25*d + d*d, abs_tol=1e-12)


def test_superlinear_feedback_excludes_endpoint_but_admits_partial_invasion() -> None:
    assert rare_selection(1.0, 2.0) < 0.0
    for d in (1e-6, 0.01, 0.1, 0.25, 0.49):
        assert rare_selection(d, 2.0) > 0.0
    assert isclose(rare_selection(0.5, 2.0), 0.0, abs_tol=1e-12)
    for d in (0.51, 0.75, 1.0):
        assert rare_selection(d, 2.0) < 0.0


@pytest.mark.parametrize("environment", [2.01, 2.1, 2.25, 2.49])
def test_every_reference_ecology_only_environment_is_partially_invadable_if_superlinear(
    environment: float,
) -> None:
    # Reference value >0, g0>0, completed endpoint <0;
    # but a sufficiently small partial variant increases from rarity.
    full = rare_selection(1.0, 2.0, environment)
    g0 = 1.0 - (3.0 - environment)
    phi = intrinsic_release(1.0, environment)
    assert g0 > 0.0 and phi > 0.0 and full < 0.0
    d = min(g0 / 4.0, 0.01)
    assert rare_selection(d, 2.0, environment) > 0.0


def test_w_prime_zero_gives_positive_rare_small_step_selection() -> None:
    for exponent in (2.0, 4.0):
        for d in (1e-5, 1e-6):
            slope_numeric = rare_selection(d, exponent) / d
            assert isclose(slope_numeric, 0.25, abs_tol=1e-4)


def test_declared_mutation_set_is_an_essential_condition() -> None:
    # If only the completed jump is attainable, the resident is
    # resistant against that *declared* alternative. With a continuum
    # of partial mutant degrees it is not.
    accessible_endpoint_only = (1.0,)
    accessible_with_partials = (0.05, 0.10, 0.25, 1.0)
    assert all(rare_selection(d, 2.0) <= 0.0 for d in accessible_endpoint_only)
    assert any(rare_selection(d, 2.0) > 0.0 for d in accessible_with_partials)


def test_manuscript_and_theory_respect_conditional_vs_realized_stasis() -> None:
    manuscript = (ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md")
    if not manuscript.exists():
        manuscript = ROOT / "MANUSCRIPT_SOURCE.md"
    text = manuscript.read_text(encoding="utf-8")
    theory = (ROOT / "theory" / "ENDPOINT_EXCLUSION_VS_PERSISTENCE_V1.md").read_text(
        encoding="utf-8"
    )
    assert "endpoint exclusion does not certify persistence" in theory
    assert "all accessible partial" in text.lower()
    assert "not automatically three" in theory.lower()
