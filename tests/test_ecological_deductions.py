from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
THEORY = ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md"
FIG2 = ROOT / "figures" / "FIG2_PHASE_MAP.svg"
LEDGER = ROOT / "docs" / "THEOREM_CLAIM_LEDGER_V1.md"


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
    assert "delays" in manuscript
    assert "coexistence" in manuscript


def test_conflict_strength_is_not_promoted_to_differentiation_rank() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "larger conflict load does not necessarily predict stronger differentiation" in manuscript
    assert "UTA1.5" in theory
    assert "UTA1.5" in ledger


def test_discordance_table_contains_process_falsification_case() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "reciprocal fixation and occupancy orderings disagree" in manuscript
    assert "process assumptions are violated" in manuscript


def test_feedback_gradient_generalization_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "eta_0/(a-b)" in manuscript
    assert "UTA1.4b" in theory
    assert "UTA1.4b" in ledger
    assert "Phi'(E_V)-eta'(E_V)" in manuscript


def test_two_frequency_identification_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "Delta(p_+)+Delta(p_-)" in manuscript
    assert "UTA1.6" in theory
    assert "UTA1.6" in ledger


def test_three_frequency_curvature_diagnostic_is_registered() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    assert "UTA1.7" in theory
    assert "UTA1.7" in ledger
    assert "kappa" in manuscript
    assert "Phi>eta-kappa-h0" in manuscript
    assert "does not inherit the canonical exponential-Moran fixation" in theory
