"""Guard figure-axis integrity and candidate-specific persistence claims.

The anonymous reviewer bundle is an independent replay target: its manuscript
is named MANUSCRIPT_SOURCE.md rather than the source-tree Markdown path.
"""

from pathlib import Path
import re
from xml.etree import ElementTree as ET

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIG1 = ROOT / "figures" / "FIG1_LOGIC_DIAGRAM.svg"
FIG3 = ROOT / "figures" / "FIG3_EMPIRICAL_LADDER.svg"
SECTION_MAP = ROOT / "docs" / "SECTION_CLAIM_MAP_V1.md"

pytestmark = pytest.mark.document_sync


def manuscript_text() -> str:
    source = ROOT / "manuscript" / "SLK_MANUSCRIPT_AMNAT_V4.md"
    if not source.exists():
        source = ROOT / "MANUSCRIPT_SOURCE.md"
    return source.read_text(encoding="utf-8")


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text))


def test_abstract_preserves_scientific_scope_within_submission_limit() -> None:
    manuscript = manuscript_text()
    abstract = manuscript.split("## Abstract", 1)[1].split("## 1. Introduction", 1)[0]
    title = manuscript.splitlines()[0].removeprefix("# ")
    main = manuscript.split("## Literature Cited", 1)[0]
    assert word_count(abstract) <= 200
    assert word_count(main) - word_count(title) <= 7500
    assert "endpoint exclusion alone cannot certify resident stasis" in abstract
    assert "accessible partial alternatives" in manuscript
    assert "candidate-specific criteria" in manuscript


def test_figure_1_records_conditional_status_in_the_actual_artwork() -> None:
    figure = FIG1.read_text(encoding="utf-8")
    ET.fromstring(figure)
    assert "Same resident architecture (conditional)" in figure
    assert "all accessible partial variants need testing" in figure
    assert "Endpoint exclusion alone does not establish resistance" in figure
    assert "integration persists because of ecology" not in figure


def test_figure_3_uses_correct_axes_and_candidate_relative_claim() -> None:
    artwork = FIG3.read_text(encoding="utf-8")
    root = ET.fromstring(artwork)
    ns = "{http://www.w3.org/2000/svg}"
    labels = [(x.attrib.get("x"), "".join(x.itertext())) for x in root.iter(ns + "text")]
    assert ("90", "net value Φ") in labels
    assert ("1040", "structural release d") in labels
    assert "net value of differentiation Φ</text>" not in artwork
    assert "Endpoint barrier order alone does not prove resident stasis" in artwork
    assert "partial mutants need separate checks" in artwork


def test_frequency_feedback_sign_alone_does_not_imply_coexistence_or_bistability() -> None:
    artwork = FIG3.read_text(encoding="utf-8")
    manuscript = manuscript_text()
    assert "alternative states if η&gt;0 and |Φ|&lt;η" in artwork
    assert "coexistence if η&lt;0 and |Φ|&lt;|η|" in artwork
    assert "both architectures invade from rarity" in manuscript

    def selection(phi: float, eta: float, p: float) -> float:
        return phi + eta * (2.0*p-1.0)

    # For eta>0, both states repel a rare alternative only for |phi|<eta.
    assert selection(0.25, 0.8, 0.0) < 0.0 < selection(0.25, 0.8, 1.0)
    # Positive feedback alone may instead yield unconditional D advantage.
    assert selection(1.2, 0.8, 0.0) > 0.0
    assert selection(1.2, 0.8, 1.0) > 0.0

    # For eta<0, the two morphs can coexist when each increases from rarity.
    assert selection(0.25, -0.8, 0.0) > 0.0 > selection(0.25, -0.8, 1.0)
    # Negative feedback alone is also insufficient.
    assert selection(1.2, -0.8, 0.0) > 0.0
    assert selection(1.2, -0.8, 1.0) > 0.0


def test_claim_map_uses_the_proportional_feedback_escape_equation() -> None:
    claim_map = SECTION_MAP.read_text(encoding="utf-8")
    assert "1/2-[dmax/(2eta)]*[R(d)/d-k]" in claim_map
    assert "1/2-[R(d)-kd]/(2eta)" not in claim_map
    assert "conditional candidate comparisons" in claim_map
    dmax, eta, k = 1.0, 0.8, 1.5

    def p_escape(d: float) -> float:
        recovery = d + d * d
        return 0.5 - dmax * (recovery/d-k) / (2.0*eta)

    assert p_escape(0.25) == pytest.approx(0.65625)
    assert p_escape(0.75) == pytest.approx(0.34375)
    assert p_escape(1.0) == pytest.approx(0.1875)
