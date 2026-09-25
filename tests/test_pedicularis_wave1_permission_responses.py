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


def _definition_receipt(activity_id: str) -> dict[str, str]:
    registry = adj.load_activity_definition_registry()
    activity = registry["activities"][activity_id]
    return {
        "reference": activity["definition_reference"],
        "algorithm": adj.ACTIVITY_HASH_ALGORITHM,
        "sha256": adj.activity_definition_sha256(activity),
        "registry_sha256": adj.activity_registry_sha256(registry),
    }


def _activities(default: str = "UNRESOLVED") -> list[dict]:
    return [
        {
            "activity_id": activity_id,
            "decision": default,
            "response_reference": (
                "RESP-REF" if default != "UNRESOLVED" else None
            ),
            "valid_from": (
                "2027-05-01"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "valid_through": (
                "2027-09-30"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions": (
                "NO_ADDITIONAL_CONDITIONS"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions_compatible_with_registered_activity": (
                True
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions_review_reference": (
                "COND-REVIEW"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "registered_activity_definition_reference": (
                _definition_receipt(activity_id)["reference"]
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "registered_activity_definition_hash_algorithm": (
                _definition_receipt(activity_id)["algorithm"]
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "registered_activity_definition_sha256": (
                _definition_receipt(activity_id)["sha256"]
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "registered_activity_registry_sha256": (
                _definition_receipt(activity_id)["registry_sha256"]
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions_reviewed_by": (
                "TEST-REVIEWER"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions_review_date": (
                "2027-05-12"
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            ),
            "conditions_review_rationale": (
                "Authority condition is compatible with the registered activity definition."
                if default in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
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
            row["valid_from"] = (
                "2027-05-01"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["valid_through"] = (
                "2027-09-30"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions"] = (
                "NO_ADDITIONAL_CONDITIONS"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions_compatible_with_registered_activity"] = (
                True
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions_review_reference"] = (
                f"{prefix}-COND-REVIEW-{row['activity_id']}"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["registered_activity_definition_reference"] = (
                _definition_receipt(row["activity_id"])["reference"]
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["registered_activity_definition_hash_algorithm"] = (
                _definition_receipt(row["activity_id"])["algorithm"]
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["registered_activity_definition_sha256"] = (
                _definition_receipt(row["activity_id"])["sha256"]
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["registered_activity_registry_sha256"] = (
                _definition_receipt(row["activity_id"])["registry_sha256"]
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions_reviewed_by"] = (
                "TEST-REVIEWER"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions_review_date"] = (
                "2027-05-12"
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )
            row["conditions_review_rationale"] = (
                "Authority condition is compatible with the registered activity definition."
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}
                else None
            )


def _fill_condition_review(
    row: dict,
    prefix: str,
    *,
    compatible: bool,
    rationale: str | None = None,
) -> None:
    row["conditions_compatible_with_registered_activity"] = compatible
    row["conditions_review_reference"] = f"{prefix}-COND-REVIEW"
    row["registered_activity_definition_reference"] = _definition_receipt(
        row["activity_id"]
    )["reference"]
    row["registered_activity_definition_hash_algorithm"] = _definition_receipt(
        row["activity_id"]
    )["algorithm"]
    row["registered_activity_definition_sha256"] = _definition_receipt(
        row["activity_id"]
    )["sha256"]
    row["registered_activity_registry_sha256"] = _definition_receipt(
        row["activity_id"]
    )["registry_sha256"]
    row["conditions_reviewed_by"] = "TEST-REVIEWER"
    row["conditions_review_date"] = "2027-05-13"
    row["conditions_review_rationale"] = (
        rationale
        or (
            "Authority conditions are compatible with the registered activity definition."
            if compatible
            else "Authority conditions conflict with the registered activity definition."
        )
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
                "conditions": "non-destructive scope only",
            },
            {
                "response_id": "SITE-001",
                "route_id": "SONGZANLIN_SITE_MANAGEMENT",
                "responding_organization": "Shangri-La Songzanlin Monastery Management Bureau",
                "response_date": "2027-05-12",
                "response_reference": "SITE-LETTER-001",
                "activity_decisions": site,
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
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    assert out["required_scope"] == "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
    assert out["required_activities"] == ["A", "B", "C"]
    for activity_id in "ABC":
        assert out["required_activity_matrix"][activity_id] == {
            "regulatory": "PASS",
            "site": "PASS",
        }
    assert out["recovery_handoff"]["sampling_permission_status"] == "CONFIRMED"
    assert set(out["all_activity_matrix"]) == set("ABCDEF")
    assert set(out["all_activity_validity"]) == set("ABCDEF")
    for activity_id in "ABC":
        assert out["required_activity_validity"][activity_id]["regulatory"]
        assert out["required_activity_validity"][activity_id]["site"]
    assert out["recovery_handoff"]["destructive_activities_D_to_F_required_for_recovery_p0a_p0b"] is False


def test_destructive_D_to_F_can_remain_unresolved_without_blocking_recovery_scope() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
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
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_BLOCKED"
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
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFLICTING"


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
    assert fresh["sampling_permission_scope"] == "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
    assert fresh["sampling_permission_reference"].endswith("@perm123")
    assert out["permission_scope_receipt"]["candidate_id"] == "SONGZANLIN_EIA_2025"
    assert set(out["permission_scope_receipt"]["required_activity_validity"]) == {
        "A", "B", "C"
    }
    assert out["permission_scope_receipt"]["sampling_permission_reference"].endswith(
        "@perm123"
    )
    assert set(out["permission_scope_receipt"]["all_activity_matrix"]) == set(
        "ABCDEF"
    )
    assert set(out["permission_scope_receipt"]["all_activity_validity"]) == set(
        "ABCDEF"
    )


def test_unconfirmed_scope_cannot_compile_into_recovery_observation() -> None:
    payload = _songzanlin_bundle()
    payload["responses"].pop()
    receipt = adj.adjudicate(payload)
    assert receipt["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_INCOMPLETE"
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
            },
            {
                "response_id": "SITE-001",
                "route_id": "WUFENG_JIANTANG_FOREST_FARM",
                "responding_organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
                "response_date": "2027-05-11",
                "response_reference": "FOREST-FARM-LETTER-001",
                "activity_decisions": site,
            },
        ],
        "adjudication_metadata": {
            "slk_source_commit": "abc123",
            "adjudication_commit": "perm789",
            "adjudication_timestamp": "2027-05-12T00:00:00Z",
        },
    }
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    assert out["candidate_id"] == "SHANGRILA_WUFENG"



def test_positive_required_scope_response_requires_activity_validity_dates() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["valid_through"] = None
    with pytest.raises(ValueError, match="valid_through/REG-001/A"):
        adj.adjudicate(payload)


def test_activity_permission_validity_interval_cannot_be_reversed() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "B"
    )
    target["valid_from"] = "2027-10-01"
    target["valid_through"] = "2027-09-30"
    with pytest.raises(ValueError, match="validity interval reversed: REG-001/B"):
        adj.adjudicate(payload)


def test_activity_permission_cannot_expire_before_response_date() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "C"
    )
    target["valid_from"] = "2027-04-01"
    target["valid_through"] = "2027-05-01"
    with pytest.raises(ValueError, match="expires before response date: REG-001/C"):
        adj.adjudicate(payload)



def test_optional_D_permission_is_receipted_without_becoming_required_scope() -> None:
    payload = _songzanlin_bundle()
    for response, prefix in zip(payload["responses"], ("REGD", "SITED")):
        target = next(
            row for row in response["activity_decisions"]
            if row["activity_id"] == "D"
        )
        target["decision"] = "ALLOWED"
        target["response_reference"] = f"{prefix}-D"
        target["valid_from"] = "2027-06-01"
        target["valid_through"] = "2027-06-30"
        target["conditions"] = "voucher-only June window"
        _fill_condition_review(target, f"{prefix}-D", compatible=True)
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    assert out["required_activities"] == ["A", "B", "C"]
    assert out["all_activity_matrix"]["D"] == {
        "regulatory": "PASS",
        "site": "PASS",
    }
    assert out["all_activity_validity"]["D"]["regulatory"]
    assert out["all_activity_validity"]["D"]["site"]


def test_optional_positive_D_permission_still_requires_validity_dates() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "D"
    )
    target["decision"] = "ALLOWED"
    target["response_reference"] = "REG-D"
    target["valid_from"] = "2027-06-01"
    target["valid_through"] = None
    target["conditions"] = "voucher-only June window"
    _fill_condition_review(target, "REG-D", compatible=True)
    with pytest.raises(ValueError, match="valid_through/REG-001/D"):
        adj.adjudicate(payload)



def test_activity_specific_D_validity_can_be_narrower_than_A_C() -> None:
    payload = _songzanlin_bundle()
    for response, prefix in zip(payload["responses"], ("REGD", "SITED")):
        d = next(
            row for row in response["activity_decisions"]
            if row["activity_id"] == "D"
        )
        d["decision"] = "ALLOWED"
        d["response_reference"] = f"{prefix}-D"
        d["valid_from"] = "2027-06-10"
        d["valid_through"] = "2027-06-20"
        d["conditions"] = "voucher only during June 10-20"
        _fill_condition_review(d, f"{prefix}-D", compatible=True)
    out = adj.adjudicate(payload)
    assert out["required_activity_validity"]["A"]["regulatory"][0][
        "valid_through"
    ] == "2027-09-30"
    assert out["all_activity_validity"]["D"]["regulatory"][0][
        "valid_through"
    ] == "2027-06-20"
    assert out["all_activity_validity"]["D"]["regulatory"][0][
        "conditions"
    ] == "voucher only during June 10-20"


def test_response_level_validity_does_not_substitute_for_activity_validity() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["valid_from"] = None
    target["valid_through"] = None
    payload["responses"][0]["valid_from"] = "2027-05-01"
    payload["responses"][0]["valid_through"] = "2027-09-30"
    with pytest.raises(ValueError, match="valid_from/REG-001/A"):
        adj.adjudicate(payload)



def test_positive_activity_requires_condition_compatibility_review() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["conditions_compatible_with_registered_activity"] = None
    with pytest.raises(
        ValueError,
        match="conditions_compatible_with_registered_activity/REG-001/A",
    ):
        adj.adjudicate(payload)


def test_positive_activity_requires_condition_review_reference() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "B"
    )
    target["conditions_review_reference"] = None
    with pytest.raises(ValueError, match="conditions_review_reference/SITE-001/B"):
        adj.adjudicate(payload)


def test_incompatible_allowed_condition_blocks_required_scope() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "C"
    )
    target["conditions"] = "site staff prohibit touching or measuring flowers"
    target["conditions_compatible_with_registered_activity"] = False
    target["conditions_review_reference"] = "METHOD-REVIEW-C-BLOCK"
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_BLOCKED"
    site_response = next(
        row for row in out["responses"] if row["route_class"] == "SITE"
    )
    assert site_response["activity_decisions"]["C"] == "NO_PERMISSION_REQUIRED"
    assert site_response["effective_scope_decisions"]["C"] == "PROHIBITED"
    assert out["required_activity_matrix"]["C"]["site"] == "BLOCKED"
    assert out["required_activity_validity"]["C"]["site"] == []


def test_incompatible_optional_D_condition_does_not_block_default_A_C_scope() -> None:
    payload = _songzanlin_bundle()
    for response, prefix in zip(payload["responses"], ("REGD", "SITED")):
        d = next(
            row for row in response["activity_decisions"]
            if row["activity_id"] == "D"
        )
        d["decision"] = "ALLOWED"
        d["response_reference"] = f"{prefix}-D"
        d["valid_from"] = "2027-06-01"
        d["valid_through"] = "2027-06-30"
        d["conditions"] = "voucher only outside the registered recovery area"
        _fill_condition_review(
            d,
            f"{prefix}-D-BLOCK",
            compatible=False,
            rationale="Voucher condition excludes the registered recovery area.",
        )
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    assert out["all_activity_matrix"]["D"] == {
        "regulatory": "BLOCKED",
        "site": "BLOCKED",
    }
    assert out["all_activity_validity"]["D"] == {
        "regulatory": [],
        "site": [],
    }



def test_null_top_level_permission_response_reference_is_rejected() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["response_reference"] = None
    with pytest.raises(ValueError, match="response_reference/REG-001"):
        adj.adjudicate(payload)


def test_null_activity_response_reference_is_rejected() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["response_reference"] = None
    with pytest.raises(ValueError, match="REG-001/A/response_reference"):
        adj.adjudicate(payload)



def test_positive_activity_requires_explicit_conditions_text() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["conditions"] = None
    with pytest.raises(ValueError, match="conditions/REG-001/A"):
        adj.adjudicate(payload)


def test_no_additional_conditions_sentinel_is_explicitly_accepted() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    reg = next(row for row in out["responses"] if row["route_class"] == "REGULATORY")
    assert reg["activity_decision_details"]["A"]["conditions"] == (
        "NO_ADDITIONAL_CONDITIONS"
    )



def test_positive_activity_requires_registered_activity_definition_reference() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["registered_activity_definition_reference"] = (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#B"
    )
    with pytest.raises(ValueError, match="wrong registered activity definition"):
        adj.adjudicate(payload)


def test_positive_activity_requires_condition_reviewer() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["conditions_reviewed_by"] = None
    with pytest.raises(ValueError, match="conditions_reviewed_by/REG-001/A"):
        adj.adjudicate(payload)


def test_condition_review_date_cannot_precede_authority_response() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "B"
    )
    target["conditions_review_date"] = "2027-05-11"
    with pytest.raises(ValueError, match="must fall between response and adjudication"):
        adj.adjudicate(payload)


def test_condition_review_date_cannot_follow_adjudication() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "C"
    )
    target["conditions_review_date"] = "2027-05-14"
    with pytest.raises(ValueError, match="must fall between response and adjudication"):
        adj.adjudicate(payload)


def test_positive_activity_requires_condition_review_rationale() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["conditions_review_rationale"] = None
    with pytest.raises(ValueError, match="conditions_review_rationale/SITE-001/A"):
        adj.adjudicate(payload)


def test_confirmed_receipt_preserves_condition_review_audit_metadata() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    interval = out["required_activity_validity"]["A"]["regulatory"][0]
    assert interval["registered_activity_definition_reference"] == (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#A"
    )
    assert interval["registered_activity_definition_hash_algorithm"] == (
        "SHA256_CANONICAL_JSON_V1"
    )
    assert interval["registered_activity_definition_sha256"] == (
        _definition_receipt("A")["sha256"]
    )
    assert interval["registered_activity_registry_sha256"] == (
        _definition_receipt("A")["registry_sha256"]
    )
    assert interval["conditions_reviewed_by"] == "TEST-REVIEWER"
    assert interval["conditions_review_date"] == "2027-05-12"
    assert interval["conditions_review_rationale"]
    assert out["activity_definition_schema"] == (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
    )



def test_condition_review_rejects_activity_definition_hash_mismatch() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["registered_activity_definition_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="activity-definition hash mismatch"):
        adj.adjudicate(payload)


def test_condition_review_rejects_registry_hash_mismatch() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "C"
    )
    target["registered_activity_registry_sha256"] = "f" * 64
    with pytest.raises(ValueError, match="registry hash mismatch"):
        adj.adjudicate(payload)


def test_condition_review_rejects_wrong_hash_algorithm() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "B"
    )
    target["registered_activity_definition_hash_algorithm"] = "SHA1"
    with pytest.raises(ValueError, match="wrong activity-definition hash algorithm"):
        adj.adjudicate(payload)
