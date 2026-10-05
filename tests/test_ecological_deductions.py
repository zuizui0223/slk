import pytest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
THEORY = ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md"
FIG2 = ROOT / "figures" / "FIG2_PHASE_MAP.svg"
FIG3 = ROOT / "figures" / "FIG3_EMPIRICAL_LADDER.svg"
LEDGER = ROOT / "docs" / "THEOREM_CLAIM_LEDGER_V1.md"

pytestmark = pytest.mark.document_sync


def test_environmental_threshold_displacement_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    figure = FIG3.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    for token in ("E_I=E_V+eta/a", "eta/a"):
        assert token in theory

    assert "UTA1.4" in theory
    assert "UTA1.4" in ledger
    assert "E_I" in manuscript
    assert "E_V" in manuscript
    assert "E_I" in figure
    assert "E_V" in figure

def test_ecological_prediction_distinguishes_frequency_feedback_signs() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Positive frequency dependence" in manuscript
    assert "negative frequency dependence" in manuscript
    assert "fail when uncommon" in manuscript
    assert "promote coexistence" in manuscript


def test_conflict_strength_is_not_promoted_to_differentiation_rank() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "incidence of division of labor need not increase monotonically" in manuscript
    assert "UTA1.5" in theory
    assert "UTA1.5" in ledger


def test_downstream_population_processes_are_demoted_to_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "finite-population fixation and weak-mutation occupancy remain in the supporting theory" in manuscript
    assert "not additional explanations for multifunctionality" in manuscript

def test_persistent_multifunctionality_three_selective_states_are_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.10" in theory
    assert "UTA1.10" in ledger
    assert "Three selective states behind persistent multifunctionality" in manuscript
    assert "Adaptive integration." in manuscript
    assert "Historical or developmental trapping." in manuscript
    assert "Ecological stabilization of integration." in manuscript
    assert "Phi > 0 and g0 < 0" in manuscript
    assert "Phi > 0, g0 > 0, Delta_R < 0" in manuscript
    assert "does not guarantee fixation or historical realization" in manuscript
    assert "same morphology can consequently have different evolutionary meanings" in manuscript

def test_feedback_gradient_generalization_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "eta_0/(a-b)" in theory
    assert "UTA1.4b" in theory
    assert "UTA1.4b" in ledger
    assert "Community turnover can therefore change whether an innovation spreads" in manuscript

def test_two_frequency_identification_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.6" in theory
    assert "UTA1.6" in ledger


def test_three_frequency_curvature_diagnostic_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.7" in theory
    assert "UTA1.7" in ledger
    assert "does not inherit the canonical exponential-Moran fixation" in theory


def test_arbitrary_shape_endpoint_invasion_is_retained_in_supporting_theory() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.8" in theory
    assert "UTA1.8" in ledger
    assert "Delta_R" in manuscript


def test_finite_frequency_endpoint_certification_is_retained_in_supporting_theory() -> None:
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.9" in theory
    assert "UTA1.9" in ledger



def test_environmental_barrier_turnover_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.4c" in theory
    assert "UTA1.4c" in ledger
    assert "E_V<E_A<E_I" in theory
    assert "limiting explanation" in theory
    assert "same integrated phenotype" in theory
    assert "The same phenotype can change evolutionary meaning before it changes form" in manuscript
    assert "E_A" in manuscript
    assert "E_I" in manuscript


def test_natural_systems_anchor_multiple_conflict_resolutions() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    figure = FIG2.read_text(encoding="utf-8")
    for token in (
        "Natural systems show multiple resolutions of functional conflict",
        "Solanum rostratum",
        "Clarkia",
        "Penstemon",
        "Pedicularis rex",
        "Ipomoea purpurea",
        "Primula farinosa",
        "cichlid",
        "structural partitioning",
        "temporal partitioning",
        "ecological coupling",
    ):
        assert token in manuscript
    for token in (
        "Solanum rostratum",
        "Clarkia",
        "Penstemon + Keckiella",
        "Pedicularis rex",
        "Ipomoea + Primula",
        "Cichlid feeding apparatus",
    ):
        assert token in figure


def test_ecology_only_phase_has_general_rare_type_criterion() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    figure = FIG3.read_text(encoding="utf-8")

    for text in (manuscript, theory):
        assert "Delta_R(E_A)<0" in text
        assert "B_A = Phi(E_A)" in text

    assert "ΔR(E_A)" in figure
    assert "ecological stabilization" in figure


def test_architecture_path_hysteresis_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    assert "UTA1.4d" in theory
    assert "UTA1.4d" in ledger
    assert "k_S < k_V < k_D" in theory
    assert "E_H < E_V < E_A" in theory
    assert "architecture-path hysteresis" in theory
    assert "evolutionary legacy" in manuscript.lower()
    assert "frequency-dependent priority effects" in manuscript.lower()


def test_persistence_erosion_thresholds_are_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    assert "UTA1.4e" in theory
    assert "UTA1.4e" in ledger
    assert "R(d_J)/d_J=k" in theory
    assert "p_C" in theory
    assert "(eta-Phi)/(2eta)" in theory
    assert "easier to overturn before morphology changes" in manuscript
    assert "critical initial frequency" in manuscript
