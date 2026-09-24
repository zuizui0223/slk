from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_context_recovery_scouting.py"

spec = importlib.util.spec_from_file_location("ped_context_recovery_scouting", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_scouting_locators_validate_against_queue_and_ledger() -> None:
    out = mod.validate()
    assert out["status"] == "SCOUTING_LOCATORS_VALIDATED"
    assert out["locator_count"] == 4
    assert out["wave1_locator_count"] == 3
    assert set(out["candidate_ids"]) == {
        "SHANGRILA_WUFENG",
        "SHANGRILA_ALPINE_BOT_GARDEN",
        "SONGZANLIN_EIA_2025",
        "HUTIAOXIA_SHANGRILA",
    }
