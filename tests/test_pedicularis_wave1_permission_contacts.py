from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pedicularis_wave1_permission_contacts.py"

spec = importlib.util.spec_from_file_location("ped_wave1_permission_contacts", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_wave1_permission_contacts_cover_all_candidates_without_permission_promotion() -> None:
    out = mod.validate()
    assert out["status"] == "WAVE1_PERMISSION_CONTACT_ROUTES_VALIDATED"
    assert out["candidate_count"] == 3
    assert out["route_count"] == 6
    assert out["permission_status"] == "UNRESOLVED_FOR_ALL"
    assert out["candidate_route_counts"] == {
        "SHANGRILA_ALPINE_BOT_GARDEN": 2,
        "SHANGRILA_WUFENG": 2,
        "SONGZANLIN_EIA_2025": 2,
    }
    assert out["route_type_counts"]["REGULATORY_ROUTING"] == 3
