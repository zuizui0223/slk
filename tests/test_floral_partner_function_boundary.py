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
    assert "Mechanically coupled flower parts affect pollen handling" in text
    assert "Supporting filaments may persist without dimorphic anthers" in text
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
    assert "long stamens present without short stamens" in audit.lower()
    assert "repeatedly de novo" in audit or "often arisen de novo" in audit
    assert "not literal observed events" in audit
    assert "a bee's functional role is not fixed" in audit.lower()
    assert "behaves differently on *Bredia* and *Melastoma candidum*" in manuscript_text
    assert "maintenance of dimorphism remains untested" in manuscript_text


def test_filament_contrast_is_not_claimed_as_lifetime_fitness() -> None:
    audit = (ROOT / "docs" / "FLORAL_INTERACTION_MODULE_AUDIT_V1.md").read_text(encoding="utf-8")
    for marker in (
        "treatment B versus treatment D",
        "12/39 (30.77%)",
        "0/31 (0%)",
        "13/39 (33.33%)",
        "not a controlled manipulation of complete life-cycle plant fitness",
        "whether the same visits exhibited slipping and ventral contact",
    ):
        assert marker.lower() in audit.lower()
    assert 12/39 > 0/31
    assert 13/39 > 0/31
    assert "long filaments stabilize buzzing even without their anthers" in manuscript()

def test_separate_de_novo_origin_from_secondary_function_retention() -> None:
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(
        encoding="utf-8"
    )
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(
        encoding="utf-8"
    )
    assert "repeatedly evolved **de novo**" in note
    assert "arose **repeatedly de novo**" in ledger
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


def test_parallel_solanum_comparison_is_natural_evolution_not_causal_slk_confirmation() -> None:
    """Keep structural erosion, pollen dispensing, and hypothesized selfing separate."""
    main = manuscript()
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(encoding="utf-8")
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(encoding="utf-8")
    prior_path = ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md"
    prior = prior_path.read_text(encoding="utf-8") if prior_path.exists() else None
    for doi in ("10.1098/rstb.2013.0256", "10.1002/ajb2.1680"):
        assert doi in main
        assert doi in note
        assert doi in ledger
        if prior is not None:
            assert doi in prior
    assert "field outcrossing rates" in main
    assert "artificial vibrations" in note.lower()
    if prior is not None:
        assert "not measured natural selfing rates" in prior
    assert "**not** selective retention of an ancestral heterantherous" in main


def test_autonomous_selfing_capacity_does_not_imply_measured_field_mating_rate() -> None:
    main = manuscript()
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(encoding="utf-8")
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(encoding="utf-8")
    for item in (main, note, ledger):
        assert "Rubini Pisano" in item
    assert "10.1093/aob/mcag186" in note
    assert "10.1093/aob/mcag186" in ledger
    assert "inconclusive" in note.lower()
    assert "not an informative negative test" in ledger
    assert "field outcrossing rates" in main


def test_solanum_residual_pollen_allocation_and_coordination_shift_are_not_slk_gate_results() -> None:
    """Guard primary-source biology without confusing phenotypic covariance and evolutionary selection."""
    main = manuscript()
    note = (ROOT / "docs" / "FLORAL_PARTNER_FUNCTION_SWITCH_V1.md").read_text(encoding="utf-8")
    ledger = (ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md").read_text(encoding="utf-8")
    prior = ROOT / "docs" / "PRIOR_ART_BOUNDARY_V1.md"
    for source in (main, note, ledger):
        assert "50–67%" in source
        assert "39–41%" in source
        assert "anther–stigma" in source
        assert "Rubini Pisano" in source
    assert "field outcrossing rates" in main
    assert "pollen discounting" in main
    assert "phenotypic" in note.lower()
    assert "not a zero-pollen or fully uniform-anther state" in ledger
    if prior.is_file():
        text = prior.read_text(encoding="utf-8")
        assert "Neither the quantitative pollen reallocation" in text
        assert "Porcher & Lande 2005" in text
    assert 0 < 0.39 <= 0.41 < 0.50 <= 0.67 < 1
