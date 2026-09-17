from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_SUFFIX = "." + "md"
TRIAGE = ROOT / "docs" / f"REVIEWER_QUANTITATIVE_REQUEST_TRIAGE_V1{DOC_SUFFIX}"
AUDIT = ROOT / "docs" / f"QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1{DOC_SUFFIX}"


def test_reviewer_quantitative_triage_declares_decision_contract() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    assert "| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |" in text
    for decision in ("DO_NOW", "DO_IF_REQUESTED", "DECLINE"):
        assert f"`{decision}`" in text


def test_slk_triage_prioritizes_identification_not_parameter_volume() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    assert "INV1" in text
    assert "asymmetric mutation" in text
    assert "dense parameter sweep" in text
    assert "empirical calibration of L/R/K/Phi" in text


def test_slk_triage_preserves_claim_ceiling() -> None:
    audit = AUDIT.read_text(encoding="utf-8")
    triage = TRIAGE.read_text(encoding="utf-8")
    for token in (
        "FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED",
        "No single biological system",
        "not an empirical estimate",
    ):
        assert token in audit
        assert token in triage
