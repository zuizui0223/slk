import pytest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.document_sync
MANUSCRIPT = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
TITLE_PAGE = ROOT / "manuscript" / "AMNAT_TITLE_PAGE_V1.md"
FIG1 = ROOT / "figures" / "FIG1_LOGIC_DIAGRAM.svg"
THEORY = ROOT / "theory" / "UNIFIED_THRESHOLD_ATLAS_V1.md"
AUDIT = ROOT / "manuscript" / "SLK_MANUSCRIPT_V0.md"


def test_submission_title_is_synchronized() -> None:
    manuscript_title = MANUSCRIPT.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ").strip()
    title_page_title = TITLE_PAGE.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ").strip()
    assert manuscript_title == title_page_title
    assert manuscript_title == (
        "Multifunctional structures can persist while barriers to division of labor change"
    )


def test_figure1_centers_three_selective_states_of_persistence() -> None:
    text = FIG1.read_text(encoding="utf-8")
    for token in (
        "One persistent phenotype can hide different evolutionary bottlenecks",
        "Adaptive integration",
        "Historical / developmental",
        "trapping",
        "Ecological stabilization",
        "persistent multifunctionality",
        "architecture, history, and ecology",
    ):
        assert token in text


def test_theory_registers_cross_level_phi_compatibility() -> None:
    text = THEORY.read_text(encoding="utf-8")
    for token in (
        "Compatibility lemma",
        "A_DD/2 - A_SS/2",
        "canonical self-play gap",
        "fixation log-ratio",
        "occupancy log-ratio",
    ):
        assert token in text


def test_theory_is_preserved_while_submission_is_biology_first() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    assert "persistent multifunctionality" in manuscript
    assert "Three evolutionary bottlenecks behind one persistent phenotype" in manuscript
    assert "Full constructive witness families" in manuscript
    assert "UTA1" in audit
    assert "R(d)=d+d^2" in audit


def test_submission_does_not_emit_duplicate_pandoc_figure_captions() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "![Figure 1" not in text
    assert "![Figure 2" not in text
    assert "![Figure 3" not in text
    assert "![](../figures/FIG1_LOGIC_DIAGRAM.svg)" in text
    assert "![](../figures/FIG2_PHASE_MAP.svg)" in text
    assert "![](../figures/FIG3_EMPIRICAL_LADDER.svg)" in text
