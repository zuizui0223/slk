from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "QUANTITATIVE_RESULTS_DISCUSSION_AUDIT_V1.md"
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"


def test_quantitative_results_discussion_audit_has_three_column_contract() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "| Qualitative claim | Quantitative claim licensed | Ceiling / not licensed |" in text


def test_audit_preserves_slk_split_and_invariant_numbers() -> None:
    ledger = LEDGER.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for token in (
        "R(d)=d+d^2",
        "L=2, k=2.2",
        "k=0.8, eta=1.5",
        "k=2.2, eta=-1",
        "rho(j|i)>rho(i|j)",
    ):
        assert token in ledger
        assert token in audit


def test_audit_blocks_empirical_overpromotion() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED" in text
    assert "No single biological system" in text
    assert "not an empirical estimate" in text
