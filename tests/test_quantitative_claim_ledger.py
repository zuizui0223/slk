from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "QUANTITATIVE_CLAIM_LEDGER_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"

CLASSES = (
    "EMPIRICAL",
    "LITERATURE-AUDIT",
    "THEORETICAL-WITNESS",
    "MODEL-PREDICTION",
    "NOT-ESTIMATED",
)


def test_quantitative_claim_ledger_declares_all_claim_classes() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for claim_class in CLASSES:
        assert f"`{claim_class}`" in text


def test_ledger_preserves_registered_slk_witness_values() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    tokens = (
        "R(d)=d+d^2",
        "L=2, k=2.2",
        "k=1.5",
        "k=0.8, eta=1.5",
        "k=2.2, eta=-1",
        "k=2.1, eta=-0.5",
    )
    for token in tokens:
        assert token in manuscript
        assert token in ledger


def test_ledger_blocks_empirical_overpromotion() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    assert "No single biological system" in text
    assert "not an empirical estimate" in text
    assert "NATURAL_PREVALENCE = NOT_ESTIMATED" in text
