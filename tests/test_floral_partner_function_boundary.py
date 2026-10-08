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
        "10.1007/s00442-022-05246-0",
    ):
        assert doi in ledger
        assert doi in note
    assert "12 of 39" in ledger
    assert "0 of 33" in ledger
    assert "0 of 31" in ledger
    assert "193 h video" in note
    assert "larger bees transfer more pollen with free anthers" in ledger
    assert "Direct intervention evidence" in note


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


def test_flower_module_audit_separates_behavior_mechanics_and_evolutionary_history() -> None:
    audit = (ROOT / "docs" / "FLORAL_INTERACTION_MODULE_AUDIT_V1.md").read_text(
        encoding="utf-8"
    )
    manuscript_text = manuscript()
    for source in (
        "10.26786/1920-7603(2024)810",
        "10.1111/1442-1984.70070",
        "10.1111/evo.14260",
        "10.1007/s00442-023-05413-x",
    ):
        assert source in audit
    for source in (
        "A: all intact",
        "B: only short",
        "C: only entire long",
        "D: long anthers removed",
        "E: long filaments only",
        "F: all stamens removed",
        "39 | 12",
        "26 | 0",
        "31 | 0",
        "2 | 1",
    ):
        assert source in audit
    assert "same flower was visited repeatedly" in audit
    assert "long stamens without short stamens" in audit.lower()
    assert "repeatedly de novo" in audit or "often arisen de novo" in audit
    assert "not literal observed events" in audit
    assert "the *same* bee" in audit
    assert "anther-buzzes in *Melastoma candidum*" in manuscript_text
    assert "an untested evolutionary hypothesis" in manuscript_text


def test_separate_de_novo_origin_from_secondary_function_retention() -> None:
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(
        encoding="utf-8"
    )
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(
        encoding="utf-8"
    )
    assert "repeatedly **de novo**" in note or "repeatedly **de novo**" in ledger
    assert "rather than predominantly persisting" in ledger
    assert "same* bee" in ledger or "same** bee" in ledger
    assert "does not establish that both classes" in note or "does not establish that both classes" in ledger


def test_reference_names_are_in_literature_cited_not_inserted_into_main() -> None:
    text = manuscript()
    main, references = text.split("## Literature Cited", 1)
    for name in ("Fukano, T.", "Rego, J. O."):
        assert name not in main
        assert name in references
    assert "Bredia hirsuta" in main
    assert "Senna arnottiana" in main
