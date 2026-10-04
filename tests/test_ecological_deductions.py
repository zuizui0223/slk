import pytest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
THEORY = ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md"
FIG2 = ROOT / "figures" / "FIG2_PHASE_MAP.svg"
LEDGER = ROOT / "docs" / "THEOREM_CLAIM_LEDGER_V1.md"

pytestmark = pytest.mark.document_sync


def test_environmental_threshold_displacement_is_registered_everywhere() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    figure = FIG2.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")

    for token in ("E_I=E_V+eta/a", "eta/a"):
        assert token in manuscript
        assert token in theory

    assert "UTA1.4" in theory
    assert "UTA1.4" in ledger
    assert "E_I" in figure
    assert "E_V" in figure


def test_ecological_prediction_distinguishes_positive_and_negative_feedback() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "If `eta>0`" in manuscript
    assert "If `eta<0`" in manuscript
    assert "differentiation already pays but cannot establish from rarity" in manuscript
    assert "negative-frequency feedback allows the differentiated type to invade" in manuscript
    assert "coexistence" in manuscript


def test_conflict_strength_is_not_promoted_to_differentiation_rank() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "larger conflict load does not necessarily predict stronger differentiation" in manuscript
    assert "UTA1.5" in theory
    assert "UTA1.5" in ledger


def test_downstream_process_extension_is_not_a_fourth_persistence_explanation() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "downstream consequences after establishment" in manuscript
    assert "reciprocal fixation ordering and monomorphic occupancy re-align" in manuscript
    assert "not as a fourth ecological explanation" in manuscript


def test_persistent_multifunctionality_three_cause_diagnosis_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.10" in theory
    assert "UTA1.10" in ledger
    assert "Three evolutionary states behind persistent multifunctionality" in manuscript
    assert "Phi>0, g_0<0" in manuscript
    assert "Phi>0, g_0>0, Delta_R<0" in manuscript
    assert "Phi>0, g_0>0, Delta_R>0" in manuscript
    assert "does not prove that differentiation must fix or persist historically" in manuscript
    assert "Persistent integration is not a diagnosis of weak conflict" in manuscript


def test_feedback_gradient_generalization_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "eta_0/(a-b)" in manuscript
    assert "UTA1.4b" in theory
    assert "UTA1.4b" in ledger
    assert "Phi'(E_V)-eta'(E_V)" in manuscript


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
    assert "reason for persistence can change" in manuscript
    assert "E_V < E_A < E_I" in manuscript


def test_natural_systems_anchor_multiple_conflict_resolutions() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    for token in (
        "Natural systems show multiple resolutions of functional conflict",
        "Solanum rostratum",
        "Clarkia",
        "Penstemon",
        "Pedicularis rex",
        "cichlid",
        "spatial partitioning",
        "temporal partitioning",
        "ecological re-coupling",
        "Ipomoea purpurea",
        "Dactylorhiza sambucina",
        "Primula farinosa",
    ):
        assert token in manuscript
