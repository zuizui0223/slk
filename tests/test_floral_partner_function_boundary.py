"""Protect the biological claim boundary between observed floral function and
the untested evolutionary maintenance of differentiated organs.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def manuscript() -> str:
    source = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not source.exists():
        source = ROOT / "MANUSCRIPT_SOURCE.md"
    return source.read_text(encoding="utf-8")


def test_peer_review_can_verify_flower_function_evidence() -> None:
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(
        encoding="utf-8"
    )
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(
        encoding="utf-8"
    )
    for doi in (
        "10.1111/plb.13673",
        "10.1111/1442-1984.70070",
        "10.1111/evo.14260",
    ):
        assert doi in ledger
        assert doi in note
    assert "12 of 39" in ledger
    assert "0 of 33" in ledger
    assert "0 of 31" in ledger
    assert "193 h video" in note


def test_morphological_retention_is_explicitly_unproven() -> None:
    text = manuscript()
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(
        encoding="utf-8"
    )
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(
        encoding="utf-8"
    )
    assert "Visitor identity can uncouple anther dimorphism" in text
    assert "remains an untested evolutionary hypothesis" in text
    assert "untested bridge hypothesis" in ledger.lower()
    assert "not demonstrated by juxtaposing" in ledger.lower()
    assert "proposed natural-history hypothesis" in note
    assert "No study cited here directly identifies" in note
    assert "No first-discovery claim" not in text


def test_reference_names_are_in_literature_cited_not_inserted_into_main() -> None:
    text = manuscript()
    main, references = text.split("## Literature Cited", 1)
    for name in ("Fukano, T.", "Rego, J. O."):
        assert name not in main
        assert name in references
    assert "Bredia hirsuta" in main
    assert "Senna arnottiana" in main
