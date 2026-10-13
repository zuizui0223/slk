"""Conditional ecological ranking of nested stamen modules.

The Bredia treatment records support a behavior contrast only. The fitness
numbers below are illustrative mathematical witnesses, not field estimates.
"""

from math import isclose
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def three_nested_fitness_values(indiscriminate_visitor_share: float) -> tuple[float, float, float]:
    q = indiscriminate_visitor_share
    assert 0.0 <= q <= 1.0
    short_only = 0.0
    support_increment = 0.9 - 1.1 * q
    long_anther_increment = 0.9 - 1.6 * q
    filament_only = short_only + support_increment
    complete_dimorphism = filament_only + long_anther_increment
    return short_only, filament_only, complete_dimorphism


@pytest.mark.parametrize(
    ("q", "best"),
    [
        (0.0, "D"),
        (0.5, "D"),
        (0.60, "P"),
        (0.75, "P"),
        (0.8, "P"),
        (0.9, "S"),
        (1.0, "S"),
    ],
)
def test_partner_turnover_can_change_best_nested_architecture(q: float, best: str) -> None:
    payoffs = dict(zip(("S", "P", "D"), three_nested_fitness_values(q)))
    assert max(payoffs, key=payoffs.get) == best


def test_partial_flower_is_favored_between_anther_and_filament_crossings() -> None:
    anther_loss_boundary = 9.0 / 16.0
    filament_loss_boundary = 9.0 / 11.0
    assert anther_loss_boundary < filament_loss_boundary
    for q in (0.56 + 0.005, 0.6, 0.75, 0.8):
        S, P, D = three_nested_fitness_values(q)
        assert P > S and P > D
        assert isclose(P-S, 0.9-1.1*q, abs_tol=1e-12)
        assert isclose(D-P, 0.9-1.6*q, abs_tol=1e-12)
    assert isclose(three_nested_fitness_values(0.75)[1], 0.075, abs_tol=1e-12)
    assert isclose(three_nested_fitness_values(0.75)[2], -0.225, abs_tol=1e-12)


def test_no_universal_order_when_support_is_costly_but_anthers_are_beneficial() -> None:
    # With h<0 and a>0, S versus D changes with h+a.
    S = 0.0
    h = -1.0
    assert S+h+2.0 > S
    assert S+h+0.5 < S


def test_identical_behavioral_support_can_be_consistent_with_opposing_selection() -> None:
    # Slipping probabilities are behavioral contrasts, not reproductive payoffs.
    slip_short_only = 12.0/39.0
    slip_filament_only = 0.0/31.0
    assert slip_short_only > slip_filament_only

    case_partial_favored = dict(S=0.0, P=1.0, D=0.5)
    case_complete_favored = dict(S=0.0, P=-0.2, D=0.5)
    assert case_partial_favored["P"] > max(case_partial_favored["S"], case_partial_favored["D"])
    assert case_complete_favored["D"] > max(case_complete_favored["S"], case_complete_favored["P"])


def test_primary_evidence_is_not_relabelled_as_heritable_staminode() -> None:
    theory = (ROOT / "theory" / "FLORAL_MODULE_RETENTION_AND_EROSION_V1.md").read_text(encoding="utf-8")
    empirical = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(encoding="utf-8")
    prior_art = (ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md").read_text(encoding="utf-8")
    manuscript = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not manuscript.exists():
        manuscript = ROOT / "MANUSCRIPT_SOURCE.md"
    text = manuscript.read_text(encoding="utf-8")

    for token in (
        "h(E) = W_P(E) - W_S(E)",
        "a(E) = W_D(E) - W_P(E)",
        "q_A=9/16",
        "q_F=9/11",
        "the same observed slipping contrast",
        "not a heritable natural staminode-like phenotype",
        "not a new discovery that sterile stamens can be functional",
    ):
        assert token.lower() in theory.lower(), token

    for doi in ("10.2307/2656866", "10.1111/j.0014-3820.2001.tb00782.x"):
        assert doi in theory
        assert doi in empirical
        assert doi in prior_art

    assert "staminodes are established" in text
    assert "remains untested" in text
    assert "The 2026 behavioral data estimate neither fitness increment" in empirical
