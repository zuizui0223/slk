"""Preserve published flower-mechanics results and their ecological claim ceiling.

Scientific sources: Vallejo-Marin et al. Evolution 2022 (doi:10.1111/evo.14485);
Monteiro et al. Annals of Botany 2025 (doi:10.1093/aob/mcae210);
Fukano and Denda Plant Species Biology 2026 (doi:10.1111/1442-1984.70070).
No previously published data are re-labelled as original SLK experiments.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "FLORAL_SHARED_MECHANICS_EVIDENCE_V1.md"
LEDGER = ROOT / "docs" / "EMPIRICAL_BRIDGE_EVIDENCE_V1.md"


def manuscript() -> str:
    path = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not path.is_file():
        path = ROOT / "MANUSCRIPT_SOURCE.md"
    return path.read_text(encoding="utf-8")


def test_three_mechanical_routes_are_supported_at_the_correct_biological_level() -> None:
    source = NOTE.read_text(encoding="utf-8")
    for title in (
        "Joined anther cones transmit vibrations",
        "A modified petal redirects pollen from both anther classes",
        "Stamen filament support changes live-bee posture",
    ):
        assert title in source

    for doi in (
        "10.1111/evo.14485",
        "10.1093/aob/mcae210",
        "10.1111/1442-1984.70070",
    ):
        assert doi in source
        assert doi in LEDGER.read_text(encoding="utf-8")

    assert "three" in source.lower()
    assert "S. elaeagnifolium" in source
    assert "S. sisymbriifolium" in source
    assert "S. pyracanthos" in source
    assert "P=0.169" in source
    assert "9.88" in source
    assert "2.31" in source
    assert "1.59" in source


def test_organ_function_is_not_confused_with_male_fitness_or_stable_morphology() -> None:
    source = NOTE.read_text(encoding="utf-8")
    manuscript_source = manuscript()
    for phrase in (
        "not 9.88-fold or 2.31-fold increases in male fitness",
        "not significantly shifted",
        "not independently retrieved/reanalysed",
    ):
        assert phrase in source, phrase

    assert "retention" in source
    assert "evolutionary retention remains untested" in manuscript_source.lower()
    assert "mechanical coupling changes different stages of pollen delivery" in manuscript_source.lower()
    assert "new origin of differentiated anatomy" in manuscript_source.lower()


def test_anonymous_evidence_does_not_identify_repository_or_pr_branch() -> None:
    source = NOTE.read_text(encoding="utf-8")
    for forbidden in (
        "github.com/",
        "SLK PR #",
        "biology/scaffold-bypass-test",
        "zuizui" + "0223",
    ):
        assert forbidden not in source


def test_solanum_pollen_release_and_reproductive_export_are_separated() -> None:
    note = NOTE.read_text(encoding="utf-8")
    assert "Pollen **release** is not yet reproductive pollen **export**" in note
    assert "mechanical transmission" in note
    assert "species-dependent downstream response" in LEDGER.read_text(encoding="utf-8")
    assert "No study cited here directly identifies" not in note  # standalone scope language
    assert "three-barrier turnover" in note
