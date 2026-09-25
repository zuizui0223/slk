from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ADJ = ROOT / "scripts" / "adjudicate_pedicularis_wave1_permission_responses.py"
COMP = ROOT / "scripts" / "compile_pedicularis_permission_scope_into_recovery.py"

spec = importlib.util.spec_from_file_location("ped_perm_resp", ADJ)
adj = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(adj)

spec2 = importlib.util.spec_from_file_location("ped_perm_compile", COMP)
comp = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(comp)


def _activities(default: str = "UNRESOLVED") -> list[dict]:
    return [
        {
            "activity_id": activity_id,
            "decision": default,
            "response_reference": (
                "RESP-REF" if default != "UNRESOLVED" else None
            ),
        }
        for activity_id in "ABCDEF"
    ]


def _set_abc(rows: list[dict], decision: str, prefix: str) -> None:
    for row in rows:
        if row["activity_id"] in {"A", "B", "C"}:
            row["decision"] = decision
            row["response_reference"] = (
                f"{prefix}-{row['activity_id']}"
                if decision != "UNRESOLVED"
                else None
            )


def _songzanlin_bundle() -> dict:
    reg = _activities()
    site = _activities()
    _set_abc(reg, "ALLOWED", "REG")
    _set_abc(site, "NO_PERMISSION_REQUIRED", "SITE")
    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1",
        "status": "FILLED_AUTHORITY_RESPONSES",
        "candidate_id": "SONGZANLIN_EIA_2025",
        "response_bundle_id": "songzanlin-bundle-001",
        "responses": [
            {
                "response_id": "REG-001",
                "route_id": "SONGZANLIN_FORESTRY_REGULATOR",
                "responding_organization": "Shangri-La Municipal Forestry and Grassland Bureau",
                "response_date": "2027-05-10",
                "response_reference": "FORESTRY-EMAIL-001",
                "activity_decisions": reg,
                "valid_from": "2027-05-10",
                "valid_through": "2027-09-30",
                "conditions": "non-destructive scope only",
            },
            {
                "response_id": "SITE-001",
                "route_id": "SONGZANLIN_SITE_MANAGEMENT",
                "responding_organization": "Shangri-La Songzanlin Monastery Management Bureau",
                "response_date": "2027-05-12",
                "response_reference": "SITE-LETTER-001",
                "activity_decisions": site,
                "valid_from": "2027-05-12",
                "valid_through": "2027-09-30",
                "conditions": "coordinate with site staff before entry",
            },
        ],
        "adjudication_metadata": {
            "slk_source_commit": "abc123",
            "adjudication_commit": "perm123",
            "adjudication_timestamp": "2027-05-13T00:00:00Z",
        },
    }


def _observation(candidate_id: str = "SONGZANLIN_EIA_2025") -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1",
        "status": "TEMPLATE_ONLY_NOT_DATA",
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": candidate_id,
            "candidate_site_id": "site1",
            "population_id": "pop1",
            "season_id": "2027",
            "recovery_window_id": "recovery1",
        },
        "fresh_verification": {
            "sampling_permission_status": "REQUIRED_BEFORE_USE",
            "sampling_permission_scope": "REQUIRED_BEFORE_USE",
            "sampling_permission_reference": "REQUIRED_BEFORE_USE",
        },
    }


def test_regulatory_and_site_pass_confirm_recovery_p0a_scope() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    assert out["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_CONFIRMED"
    assert out["required_scope"] == "RECOVERY_PLUS_P0A_NONDESTRUCTIVE"
    assert out["required_activities"] == ["A", "B", "C"]
    for activity_id in "ABC":
        assert out["required_activity_matrix"][activity_id] == {
            "regulatory": "PASS",
            "site": "PASS",
        }
    assert out["recovery_handoff"]["sampling_permission_status"] == "CONFIRMED"
    for activity_id in "ABC":
        assert out["required_activity_validity"][activity_id]["regulatory"]
        assert out["required_activity_validity"][activity_id]["site"]
    assert out["recovery_handoff"]["destructive_activities_D_to_F_required_for_recovery_p0a"] is False


def test_destructive_D_to_F_can_remain_unresolved_without_blocking_recovery_scope() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    assert out["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_CONFIRMED"
    assert all(
        response["activity_decisions"][activity_id] == "UNRESOLVED"
        for response in out["responses"]
        for activity_id in "DEF"
    )


def test_site_prohibition_blocks_recovery_p0a_scope() -> None:
    payload = _songzanlin_bundle()
    site = payload["responses"][1]["activity_decisions"]
    target = next(x for x in site if x["activity_id"] == "B")
    target["decision"] = "PROHIBITED"
    target["response_reference"] = "SITE-BLOCK-B"
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_BLOCKED"
    assert out["recovery_handoff"]["sampling_permission_status"] == "UNRESOLVED"


def test_conflicting_regulatory_responses_do_not_confirm_scope() -> None:
    payload = _songzanlin_bundle()
    conflict = {
        **payload["responses"][0],
        "response_id": "REG-002",
        "response_reference": "FORESTRY-EMAIL-002",
        "activity_decisions": _activities(),
    }
    _set_abc(conflict["activity_decisions"], "PROHIBITED", "REG2")
    payload["responses"].append(conflict)
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_CONFLICTING"


def test_wufeng_local_routing_contact_cannot_authorize_site_scope() -> None:
    reg = _activities()
    local = _activities()
    _set_abc(reg, "ALLOWED", "REG")
    _set_abc(local, "ALLOWED", "LOCAL")
    payload = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1",
        "status": "FILLED_AUTHORITY_RESPONSES",
        "candidate_id": "SHANGRILA_WUFENG",
        "response_bundle_id": "wufeng-bundle-001",
        "responses": [
            {
                "response_id": "REG-001",
                "route_id": "WUFENG_FORESTRY_REGULATOR",
                "responding_organization": "Shangri-La Municipal Forestry and Grassland Bureau",
                "response_date": "2027-05-10",
                "response_reference": "FORESTRY-EMAIL-003",
                "activity_decisions": reg,
                "valid_from": "2027-05-10",
                "valid_through": "2027-09-30",
            },
            {
                "response_id": "LOCAL-001",
                "route_id": "WUFENG_LOCAL_ROUTING",
                "responding_organization": "Jiantang Town People's Government",
                "response_date": "2027-05-10",
                "response_reference": "LOCAL-EMAIL-001",
                "activity_decisions": local,
            },
        ],
        "adjudication_metadata": {
            "slk_source_commit": "abc123",
            "adjudication_commit": "perm456",
            "adjudication_timestamp": "2027-05-13T00:00:00Z",
        },
    }
    with pytest.raises(ValueError, match="routing-only contact cannot authorize"):
        adj.adjudicate(payload)


def test_confirmed_scope_compiles_into_recovery_observation() -> None:
    receipt = adj.adjudicate(_songzanlin_bundle())
    out = comp.compile_permission(receipt, _observation())
    fresh = out["fresh_verification"]
    assert fresh["sampling_permission_status"] == "CONFIRMED"
    assert fresh["sampling_permission_scope"] == "RECOVERY_PLUS_P0A_NONDESTRUCTIVE"
    assert fresh["sampling_permission_reference"].endswith("@perm123")
    assert out["permission_scope_receipt"]["candidate_id"] == "SONGZANLIN_EIA_2025"
    assert set(out["permission_scope_receipt"]["required_activity_validity"]) == {
        "A", "B", "C"
    }
    assert out["permission_scope_receipt"]["sampling_permission_reference"].endswith(
        "@perm123"
    )


def test_unconfirmed_scope_cannot_compile_into_recovery_observation() -> None:
    payload = _songzanlin_bundle()
    payload["responses"].pop()
    receipt = adj.adjudicate(payload)
    assert receipt["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_INCOMPLETE"
    with pytest.raises(ValueError, match="not confirmed"):
        comp.compile_permission(receipt, _observation())


def test_permission_scope_candidate_must_match_recovery_observation() -> None:
    receipt = adj.adjudicate(_songzanlin_bundle())
    with pytest.raises(ValueError, match="candidate mismatch"):
        comp.compile_permission(receipt, _observation("SHANGRILA_WUFENG"))



def test_wufeng_forest_farm_site_response_can_complete_site_side() -> None:
    reg = _activities()
    site = _activities()
    _set_abc(reg, "ALLOWED", "REG")
    _set_abc(site, "ALLOWED", "FOREST")
    payload = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1",
        "status": "FILLED_AUTHORITY_RESPONSES",
        "candidate_id": "SHANGRILA_WUFENG",
        "response_bundle_id": "wufeng-bundle-002",
        "responses": [
            {
                "response_id": "REG-001",
                "route_id": "WUFENG_FORESTRY_REGULATOR",
                "responding_organization": "Shangri-La Municipal Forestry and Grassland Bureau",
                "response_date": "2027-05-10",
                "response_reference": "FORESTRY-EMAIL-010",
                "activity_decisions": reg,
                "valid_from": "2027-05-10",
                "valid_through": "2027-09-30",
            },
            {
                "response_id": "SITE-001",
                "route_id": "WUFENG_JIANTANG_FOREST_FARM",
                "responding_organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
                "response_date": "2027-05-11",
                "response_reference": "FOREST-FARM-LETTER-001",
                "activity_decisions": site,
                "valid_from": "2027-05-11",
                "valid_through": "2027-09-30",
            },
        ],
        "adjudication_metadata": {
            "slk_source_commit": "abc123",
            "adjudication_commit": "perm789",
            "adjudication_timestamp": "2027-05-12T00:00:00Z",
        },
    }
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_PERMISSION_SCOPE_CONFIRMED"
    assert out["candidate_id"] == "SHANGRILA_WUFENG"



def test_positive_required_scope_response_requires_validity_dates() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["valid_through"] = None
    with pytest.raises(ValueError, match="valid_through/REG-001"):
        adj.adjudicate(payload)


def test_permission_validity_interval_cannot_be_reversed() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["valid_from"] = "2027-10-01"
    payload["responses"][0]["valid_through"] = "2027-09-30"
    with pytest.raises(ValueError, match="validity interval reversed"):
        adj.adjudicate(payload)


def test_permission_cannot_expire_before_response_date() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["valid_through"] = "2027-05-01"
    with pytest.raises(ValueError, match="expires before response date"):
        adj.adjudicate(payload)
