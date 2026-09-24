from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_context_recovery_queue.py"

spec = importlib.util.spec_from_file_location("ped_context_recovery_queue", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_recovery_queue_covers_candidate_ledger_once() -> None:
    out = mod.validate()
    assert out["status"] == "RECOVERY_QUEUE_VALIDATED"
    assert out["candidate_count"] == 11
    assert set(out["wave1_candidates"]) == {
        "SONGZANLIN_EIA_2025",
        "SHANGRILA_WUFENG",
        "SHANGRILA_ALPINE_BOT_GARDEN",
    }
    assert out["wave_counts"]["WAVE1"] == 3
    assert out["wave_counts"]["WAVE2"] == 4
    assert out["wave_counts"]["WAVE3"] == 4
