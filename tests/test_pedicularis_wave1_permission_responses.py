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


def _decision_audit(
    activity_id: str,
    *,
    resolved: bool,
    prefix: str = "TEST",
) -> dict:
    return {
        "decision_evidence_locator": (
            f"BODY:paragraph-{activity_id}"
            if resolved
            else None
        ),
        "decision_extracted_by": (
            "TEST-EXTRACTOR"
            if resolved
            else None
        ),
        "decision_extraction_date": (
            "2027-05-12"
            if resolved
            else None
        ),
        "decision_extraction_reference": (
            f"{prefix}-EXTRACT-{activity_id}"
            if resolved
            else None
        ),
        "decision_extraction_rationale": (
            "Decision category was extracted from the cited response passage."
            if resolved
            else None
        ),
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
                "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#"
                + activity_id
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
            **_decision_audit(
                activity_id,
                resolved=default != "UNRESOLVED",
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
            row.update(
                _decision_audit(
                    row["activity_id"],
                    resolved=decision != "UNRESOLVED",
                    prefix=prefix,
                )
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
                "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#"
                + row["activity_id"]
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


def _fill_decision_audit(row: dict, prefix: str) -> None:
    row.update(
        _decision_audit(
            row["activity_id"],
            resolved=True,
            prefix=prefix,
        )
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
    row["registered_activity_definition_reference"] = (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#"
        + row["activity_id"]
    )
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


def _source_response_provenance(
    response_id: str,
    response_date: str,
    prefix: str,
) -> dict:
    return {
        "source_response_event_id": f"{prefix}-EVENT-{response_id}",
        "source_response_received_at": response_date + "T09:00:00+08:00",
        "source_response_receive_channel": "EMAIL",
        "source_response_content_sha256": "d" * 64,
        "source_response_classification_review_reference": (
            f"{prefix}-CLASS-REVIEW-{response_id}"
        ),
    }


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
                **_source_response_provenance(
                    "REG-001",
                    "2027-05-10",
                    "FORESTRY",
                ),
                "activity_decisions": reg,
                "conditions": "non-destructive scope only",
            },
            {
                "response_id": "SITE-001",
                "route_id": "SONGZANLIN_SITE_MANAGEMENT",
                "responding_organization": "Shangri-La Songzanlin Monastery Management Bureau",
                "response_date": "2027-05-12",
                "response_reference": "SITE-LETTER-001",
                **_source_response_provenance(
                    "SITE-001",
                    "2027-05-12",
                    "SITE",
                ),
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
    _fill_decision_audit(target, "SITE-BLOCK-B")
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_BLOCKED"
    assert out["recovery_handoff"]["sampling_permission_status"] == "UNRESOLVED"


def test_conflicting_regulatory_responses_do_not_confirm_scope() -> None:
    payload = _songzanlin_bundle()
    conflict = {
        **payload["responses"][0],
        "response_id": "REG-002",
        "response_reference": "FORESTRY-EMAIL-002",
        **_source_response_provenance(
            "REG-002",
            "2027-05-10",
            "FORESTRY2",
        ),
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
                **_source_response_provenance(
                    "REG-001",
                    "2027-05-10",
                    "WUFENG-REG",
                ),
                "activity_decisions": reg,
            },
            {
                "response_id": "LOCAL-001",
                "route_id": "WUFENG_LOCAL_ROUTING",
                "responding_organization": "Jiantang Town People's Government",
                "response_date": "2027-05-10",
                "response_reference": "LOCAL-EMAIL-001",
                **_source_response_provenance(
                    "LOCAL-001",
                    "2027-05-10",
                    "WUFENG-LOCAL",
                ),
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
                **_source_response_provenance(
                    "REG-001",
                    "2027-05-10",
                    "WUFENG-REG2",
                ),
                "activity_decisions": reg,
            },
            {
                "response_id": "SITE-001",
                "route_id": "WUFENG_JIANTANG_FOREST_FARM",
                "responding_organization": "Shangri-La State-owned Forest Farm, Jiantang Branch",
                "response_date": "2027-05-11",
                "response_reference": "FOREST-FARM-LETTER-001",
                **_source_response_provenance(
                    "SITE-001",
                    "2027-05-11",
                    "WUFENG-SITE",
                ),
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
        _fill_decision_audit(target, f"{prefix}-D")
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
    _fill_decision_audit(target, "REG-D")
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
        _fill_decision_audit(d, f"{prefix}-D")
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
        _fill_decision_audit(d, f"{prefix}-D")
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
    assert interval["conditions_reviewed_by"] == "TEST-REVIEWER"
    assert interval["conditions_review_date"] == "2027-05-12"
    assert interval["conditions_review_rationale"]
    assert out["activity_definition_schema"] == (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
    )



def test_permission_bundle_requires_incoming_response_provenance() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0].pop("source_response_event_id")
    with pytest.raises(ValueError, match="source_response_event_id/REG-001"):
        adj.adjudicate(payload)


def test_permission_bundle_rejects_duplicate_source_response_event() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][1]["source_response_event_id"] = payload[
        "responses"
    ][0]["source_response_event_id"]
    with pytest.raises(ValueError, match="duplicate source response event id"):
        adj.adjudicate(payload)


def test_permission_bundle_rejects_non_sha_source_response_hash() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["source_response_content_sha256"] = "bad"
    with pytest.raises(ValueError, match="content hash must be sha256"):
        adj.adjudicate(payload)


def test_permission_receipt_preserves_incoming_response_provenance() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    response = out["responses"][0]
    assert response["source_response_event_id"].startswith("FORESTRY-EVENT")
    assert response["source_response_received_at"] == (
        "2027-05-10T09:00:00+08:00"
    )
    assert response["source_response_receive_channel"] == "EMAIL"
    assert len(response["source_response_content_sha256"]) == 64
    assert response["source_response_classification_review_reference"].startswith(
        "FORESTRY-CLASS-REVIEW"
    )



def test_resolved_activity_requires_decision_evidence_locator() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["decision_evidence_locator"] = None
    with pytest.raises(ValueError, match="decision_evidence_locator"):
        adj.adjudicate(payload)


def test_decision_evidence_locator_requires_registered_source_prefix() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["decision_evidence_locator"] = "VAGUE:somewhere"
    with pytest.raises(ValueError, match="unregistered prefix"):
        adj.adjudicate(payload)


def test_resolved_activity_requires_decision_extractor() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "B"
    )
    target["decision_extracted_by"] = None
    with pytest.raises(ValueError, match="decision_extracted_by"):
        adj.adjudicate(payload)


def test_decision_extraction_date_cannot_precede_response() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][1]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["decision_extraction_date"] = "2027-05-11"
    with pytest.raises(ValueError, match="decision extraction date must fall"):
        adj.adjudicate(payload)


def test_decision_extraction_date_cannot_follow_bundle_adjudication() -> None:
    payload = _songzanlin_bundle()
    target = next(
        row for row in payload["responses"][0]["activity_decisions"]
        if row["activity_id"] == "A"
    )
    target["decision_extraction_date"] = "2027-05-14"
    with pytest.raises(ValueError, match="decision extraction date must fall"):
        adj.adjudicate(payload)


def test_confirmed_receipt_preserves_activity_decision_extraction_audit() -> None:
    out = adj.adjudicate(_songzanlin_bundle())
    details = out["responses"][0]["activity_decision_details"]["A"]
    assert details["decision_evidence_locator"] == "BODY:paragraph-A"
    assert details["decision_extracted_by"] == "TEST-EXTRACTOR"
    assert details["decision_extraction_date"] == "2027-05-12"
    assert details["decision_extraction_reference"] == "REG-EXTRACT-A"
    assert details["decision_extraction_rationale"]

    interval = out["required_activity_validity"]["A"]["regulatory"][0]
    assert interval["decision_evidence_locator"] == "BODY:paragraph-A"
    assert interval["decision_extraction_reference"] == "REG-EXTRACT-A"



def test_routing_only_prohibition_still_requires_valid_extraction_date() -> None:
    payload = _songzanlin_bundle()
    response = payload["responses"][0]
    response["route_id"] = "SONGZANLIN_FORESTRY_REGULATOR"
    # Use a normal authorizing route to build a resolved row, then verify the
    # extraction-date audit itself is route-class independent via a Wufeng
    # routing-only bundle.
    reg = _activities()
    local = _activities()
    _set_abc(reg, "ALLOWED", "REG")
    target = next(row for row in local if row["activity_id"] == "A")
    target["decision"] = "PROHIBITED"
    target["response_reference"] = "LOCAL-A-PROHIBIT"
    _fill_decision_audit(target, "LOCAL-A-PROHIBIT")
    target["decision_extraction_date"] = "2027-05-09"

    bundle = {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1",
        "status": "FILLED_AUTHORITY_RESPONSES",
        "candidate_id": "SHANGRILA_WUFENG",
        "response_bundle_id": "wufeng-routing-prohibit",
        "responses": [
            {
                "response_id": "REG-001",
                "route_id": "WUFENG_FORESTRY_REGULATOR",
                "responding_organization": "Shangri-La Municipal Forestry and Grassland Bureau",
                "response_date": "2027-05-10",
                "response_reference": "REG-RESP",
                **_source_response_provenance(
                    "REG-001",
                    "2027-05-10",
                    "REG",
                ),
                "activity_decisions": reg,
            },
            {
                "response_id": "LOCAL-001",
                "route_id": "WUFENG_LOCAL_ROUTING",
                "responding_organization": "Jiantang Town People's Government",
                "response_date": "2027-05-10",
                "response_reference": "LOCAL-RESP",
                **_source_response_provenance(
                    "LOCAL-001",
                    "2027-05-10",
                    "LOCAL",
                ),
                "activity_decisions": local,
            },
        ],
        "adjudication_metadata": {
            "slk_source_commit": "abc123",
            "adjudication_commit": "decision-audit-1",
            "adjudication_timestamp": "2027-05-12T00:00:00Z",
        },
    }
    with pytest.raises(ValueError, match="decision extraction date must fall"):
        adj.adjudicate(bundle)



def test_phone_response_requires_call_note_decision_evidence() -> None:
    payload = _songzanlin_bundle()
    payload["responses"][0]["source_response_receive_channel"] = "PHONE_CALL"
    with pytest.raises(ValueError, match="locator/channel mismatch"):
        adj.adjudicate(payload)


def test_phone_response_accepts_call_note_decision_evidence() -> None:
    payload = _songzanlin_bundle()
    response = payload["responses"][0]
    response["source_response_receive_channel"] = "PHONE_CALL"
    for row in response["activity_decisions"]:
        if row["decision"] != "UNRESOLVED":
            row["decision_evidence_locator"] = (
                "CALL_NOTE:activity-" + row["activity_id"]
            )
    out = adj.adjudicate(payload)
    assert out["status"] == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    details = out["responses"][0]["activity_decision_details"]["A"]
    assert details["decision_evidence_locator"].startswith("CALL_NOTE:")
