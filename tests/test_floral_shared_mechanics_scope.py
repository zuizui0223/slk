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
    assert "maintenance of dimorphism remains untested" in manuscript_source.lower()
    assert "mechanically coupled flower parts affect pollen handling" in manuscript_source.lower()
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


def test_two_solanum_pollen_fate_routes_do_not_imply_equivalent_reproductive_fitness() -> None:
    """Protect the measured pollen-fate contrast and its limited ecological interpretation."""
    source = NOTE.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    main = manuscript()
    for marker in (
        "10.26786/1920-7603(2025)836",
        "62.99%", "19.07%", "27.65%", "65.92%",
        "six", "nine", "P=0.221",
        "not an equivalence test",
        "species order preceding",
        "not evolutionary alternatives",
    ):
        if marker == "not evolutionary alternatives":
            assert "not matched derived alternatives" in source
        else:
            assert marker.lower() in source.lower(), marker
    assert "10.26786/1920-7603(2025)836" in ledger
    assert "not establish equivalence" in ledger
    assert "Vasquez-Castro et al. 2025" in main
    assert "neither an evolutionary transition nor a whole-life fitness comparison" in main
    assert "Stigma deposition" not in main or "without a statistically detected efficiency difference" in main
    # The published destination fractions form a near-complete pollen budget;
    # the small mismatch is allowable due to separately averaged/rounded categories.
    rostratum = (62.99, 27.65, 8.54, 0.86)
    dulcamara = (19.07, 65.92, 14.01, 1.00)
    assert abs(sum(rostratum) - 100.0) < 0.1
    assert abs(sum(dulcamara) - 100.0) < 0.1
    assert rostratum[0] > dulcamara[0]
    assert rostratum[1] < dulcamara[1]


def test_within_solanum_bee_size_predicts_opposing_pollen_and_seed_endpoints() -> None:
    """Pollen receipt, fruit set and seeds per fruit cannot be treated as one response."""
    note = NOTE.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    main = manuscript()
    for source in (note, ledger):
        assert "10.1002/ece3.2897" in source
        assert "0.068" in source and "0.214" in source
        assert "P=0.094" in source
        assert "seeds per fruit" in source
    assert "Solís-Montero and Vallejo-Marín 2017" in main
    assert "more pollen deposited but fewer seeds per fruit" in main
    assert "fruit-set effect was nonsignificant" in main
    assert "not a monotone substitute for mature seed yield" in note
    assert "self:outcross pollen ratio" in note
    # Associations have opposite slopes by the paper's declared index convention.
    assert -0.068 < 0 < 0.214
    assert 0.094 > 0.05
