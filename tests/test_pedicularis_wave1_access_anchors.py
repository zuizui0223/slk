from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_wave1_access_anchors.py"

spec = importlib.util.spec_from_file_location("ped_wave1_access", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_wave1_access_anchors_cover_all_wave1_candidates_without_permission_promotion() -> None:
    out = mod.validate()
    assert out["status"] == "WAVE1_ACCESS_PREFLIGHT_ANCHORS_VALIDATED"
    assert out["candidate_count"] == 3
    assert set(out["candidate_ids"]) == {
        "SONGZANLIN_EIA_2025",
        "SHANGRILA_WUFENG",
        "SHANGRILA_ALPINE_BOT_GARDEN",
    }
    assert out["sampling_permission_status"] == "UNRESOLVED_FOR_ALL"
