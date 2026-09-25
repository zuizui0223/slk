from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    from scripts.pedicularis_permission_activity_definitions import (
        HASH_ALGORITHM as ACTIVITY_HASH_ALGORITHM,
        activity_definition_sha256,
        load_registry as load_activity_definition_registry,
        registry_sha256 as activity_registry_sha256,
    )
except ImportError:
    from pedicularis_permission_activity_definitions import (
        HASH_ALGORITHM as ACTIVITY_HASH_ALGORITHM,
        activity_definition_sha256,
        load_registry as load_activity_definition_registry,
        registry_sha256 as activity_registry_sha256,
    )

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"
QUEUE = ROOT / "data" / "PEDICULARIS_CONTEXT_RECOVERY_QUEUE_V1.csv"
SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_RESPONSE_BUNDLE_V1"
READY_STATUS = "FILLED_AUTHORITY_RESPONSES"
REQUIRED_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
REQUIRED_ACTIVITIES = {"A", "B", "C"}
ALL_ACTIVITIES = {"A", "B", "C", "D", "E", "F"}
ALLOWED_DECISIONS = {
    "ALLOWED",
    "NO_PERMISSION_REQUIRED",
    "PROHIBITED",
    "UNRESOLVED",
}
SITE_AUTHORIZING_ROUTE_TYPES = {
    "SITE_MANAGEMENT_ROUTING",
    "INSTITUTIONAL_SITE_ROUTING",
}
ROUTING_ONLY_TYPES = {"LOCAL_TERRITORIAL_ROUTING"}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    _need(value is not None, f"unresolved {label}")
    out = str(value).strip()
    _need(
        bool(out)
        and out.lower() not in {"none", "null"}
        and "REQUIRED_BEFORE_USE" not in out,
        f"unresolved {label}",
    )
    return out


def _required_bool(value: object, label: str) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    _need(
        text in {"true", "false", "1", "0", "yes", "no"},
        f"{label} must be boolean-like",
    )
    return text in {"true", "1", "yes"}


def _iso_date(value: object, label: str) -> date:
    text = _filled(value, label)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


def _adjudication_day(value: object) -> date:
    text = _filled(value, "adjudication_timestamp")
    _need(len(text) >= 10, "adjudication_timestamp must include ISO date")
    try:
        return date.fromisoformat(text[:10])
    except ValueError as exc:
        raise ValueError("adjudication_timestamp must begin YYYY-MM-DD") from exc


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _canonical_routes(candidate_id: str) -> dict[str, dict[str, str]]:
    rows = [
        row for row in _read(ROUTES)
        if row["candidate_id"].strip() == candidate_id
    ]
    _need(bool(rows), f"no registered permission routes for candidate: {candidate_id}")
    return {row["route_id"].strip(): row for row in rows}


def _is_wave1(candidate_id: str) -> bool:
    return any(
        row["candidate_id"].strip() == candidate_id
        and row["recovery_wave"].strip() == "WAVE1"
        for row in _read(QUEUE)
    )


def _decision_map(
    response: dict,
    label: str,
) -> tuple[dict[str, str], dict[str, dict]]:
    rows = response.get("activity_decisions")
    _need(isinstance(rows, list), f"{label} activity_decisions must be a list")
    ids = [str(row.get("activity_id", "")).strip() for row in rows]
    _need(len(ids) == len(set(ids)), f"{label} duplicate activity_id")
    _need(set(ids) == ALL_ACTIVITIES, f"{label} activity inventory must be A-F")
    out: dict[str, str] = {}
    by_id: dict[str, dict] = {}
    for row in rows:
        _need(isinstance(row, dict), f"{label} activity decision must be object")
        activity_id = str(row["activity_id"]).strip()
        decision = _filled(row.get("decision"), f"{label}/{activity_id}/decision")
        _need(
            decision in ALLOWED_DECISIONS,
            f"{label}/{activity_id} unregistered decision: {decision}",
        )
        if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED", "PROHIBITED"}:
            _filled(
                row.get("response_reference"),
                f"{label}/{activity_id}/response_reference",
            )
        out[activity_id] = decision
        by_id[activity_id] = row
    return out, by_id


def adjudicate(payload: dict) -> dict:
    _need(payload.get("schema_version") == SCHEMA, "wrong permission-response schema")
    _need(payload.get("status") == READY_STATUS, "permission responses are not filled")

    candidate_id = _filled(payload.get("candidate_id"), "candidate_id")
    _need(_is_wave1(candidate_id), "permission response candidate must be WAVE1")
    bundle_id = _filled(payload.get("response_bundle_id"), "response_bundle_id")
    canonical = _canonical_routes(candidate_id)
    activity_definition_registry = load_activity_definition_registry()
    activity_definitions = activity_definition_registry["activities"]
    definition_registry_hash = activity_registry_sha256(
        activity_definition_registry
    )

    metadata = payload.get("adjudication_metadata", {})
    for key in ("slk_source_commit", "adjudication_commit", "adjudication_timestamp"):
        _filled(metadata.get(key), f"adjudication_metadata.{key}")
    adjudication_day = _adjudication_day(
        metadata.get("adjudication_timestamp")
    )

    responses = payload.get("responses")
    _need(isinstance(responses, list) and responses, "permission responses missing")
    response_ids = [str(x.get("response_id", "")).strip() for x in responses]
    _need(all(response_ids) and len(response_ids) == len(set(response_ids)), "response_id must be non-empty and unique")

    resolved: list[dict] = []
    activity_by_class: dict[str, dict[str, set[str]]] = {
        "REGULATORY": defaultdict(set),
        "SITE": defaultdict(set),
    }
    validity_by_class: dict[str, dict[str, list[dict[str, str]]]] = {
        "REGULATORY": defaultdict(list),
        "SITE": defaultdict(list),
    }

    for response in responses:
        response_id = _filled(response.get("response_id"), "response_id")
        route_id = _filled(response.get("route_id"), f"route_id/{response_id}")
        _need(route_id in canonical, f"response route not registered for candidate: {route_id}")
        route = canonical[route_id]
        organization = _filled(
            response.get("responding_organization"),
            f"responding_organization/{response_id}",
        )
        _need(
            organization == route["organization"].strip(),
            f"responding organization/route mismatch: {response_id}",
        )
        response_date = _iso_date(
            response.get("response_date"),
            f"response_date/{response_id}",
        )
        response_reference = _filled(
            response.get("response_reference"),
            f"response_reference/{response_id}",
        )
        decisions, decision_rows = _decision_map(response, response_id)
        route_type = route["route_type"].strip()
        if route_type == "REGULATORY_ROUTING":
            route_class = "REGULATORY"
        elif route_type in SITE_AUTHORIZING_ROUTE_TYPES:
            route_class = "SITE"
        elif route_type in ROUTING_ONLY_TYPES:
            route_class = "ROUTING_ONLY"
        else:
            raise ValueError(
                f"unsupported permission response route type: {route_id}"
            )

        if route_class == "ROUTING_ONLY":
            _need(
                all(
                    decision in {"UNRESOLVED", "PROHIBITED"}
                    for decision in decisions.values()
                ),
                f"routing-only contact cannot authorize activities: {route_id}",
            )
        else:
            effective_decisions: dict[str, str] = {}
            for activity_id, decision in decisions.items():
                decision_row = decision_rows[activity_id]
                effective_decision = decision
                if decision in {"ALLOWED", "NO_PERMISSION_REQUIRED"}:
                    valid_from = _iso_date(
                        decision_row.get("valid_from"),
                        f"valid_from/{response_id}/{activity_id}",
                    )
                    valid_through = _iso_date(
                        decision_row.get("valid_through"),
                        f"valid_through/{response_id}/{activity_id}",
                    )
                    _need(
                        valid_from <= valid_through,
                        "permission validity interval reversed: "
                        f"{response_id}/{activity_id}",
                    )
                    _need(
                        response_date <= valid_through,
                        "permission expires before response date: "
                        f"{response_id}/{activity_id}",
                    )
                    conditions = _filled(
                        decision_row.get("conditions"),
                        f"conditions/{response_id}/{activity_id}",
                    )
                    compatible = _required_bool(
                        decision_row.get(
                            "conditions_compatible_with_registered_activity"
                        ),
                        "conditions_compatible_with_registered_activity/"
                        f"{response_id}/{activity_id}",
                    )
                    review_reference = _filled(
                        decision_row.get("conditions_review_reference"),
                        f"conditions_review_reference/{response_id}/{activity_id}",
                    )
                    definition_reference = _filled(
                        decision_row.get("registered_activity_definition_reference"),
                        f"registered_activity_definition_reference/{response_id}/{activity_id}",
                    )
                    expected_definition_reference = activity_definitions[
                        activity_id
                    ]["definition_reference"]
                    _need(
                        definition_reference == expected_definition_reference,
                        "condition review used wrong registered activity definition: "
                        f"{response_id}/{activity_id}",
                    )
                    hash_algorithm = _filled(
                        decision_row.get(
                            "registered_activity_definition_hash_algorithm"
                        ),
                        "registered_activity_definition_hash_algorithm/"
                        f"{response_id}/{activity_id}",
                    )
                    _need(
                        hash_algorithm == ACTIVITY_HASH_ALGORITHM,
                        "condition review used wrong activity-definition hash algorithm: "
                        f"{response_id}/{activity_id}",
                    )
                    definition_hash = _filled(
                        decision_row.get(
                            "registered_activity_definition_sha256"
                        ),
                        "registered_activity_definition_sha256/"
                        f"{response_id}/{activity_id}",
                    )
                    expected_definition_hash = activity_definition_sha256(
                        activity_definitions[activity_id]
                    )
                    _need(
                        definition_hash == expected_definition_hash,
                        "condition review activity-definition hash mismatch: "
                        f"{response_id}/{activity_id}",
                    )
                    registry_hash = _filled(
                        decision_row.get("registered_activity_registry_sha256"),
                        f"registered_activity_registry_sha256/{response_id}/{activity_id}",
                    )
                    _need(
                        registry_hash == definition_registry_hash,
                        "condition review activity-definition registry hash mismatch: "
                        f"{response_id}/{activity_id}",
                    )
                    reviewed_by = _filled(
                        decision_row.get("conditions_reviewed_by"),
                        f"conditions_reviewed_by/{response_id}/{activity_id}",
                    )
                    review_date = _iso_date(
                        decision_row.get("conditions_review_date"),
                        f"conditions_review_date/{response_id}/{activity_id}",
                    )
                    _need(
                        response_date <= review_date <= adjudication_day,
                        "condition review date must fall between response and adjudication: "
                        f"{response_id}/{activity_id}",
                    )
                    review_rationale = _filled(
                        decision_row.get("conditions_review_rationale"),
                        f"conditions_review_rationale/{response_id}/{activity_id}",
                    )
                    if compatible:
                        validity_by_class[route_class][activity_id].append(
                            {
                                "response_id": response_id,
                                "route_id": route_id,
                                "response_reference": _filled(
                                    decision_row.get("response_reference"),
                                    f"{response_id}/{activity_id}/response_reference",
                                ),
                                "decision": decision,
                                "valid_from": valid_from.isoformat(),
                                "valid_through": valid_through.isoformat(),
                                "conditions": conditions,
                                "conditions_compatible_with_registered_activity": True,
                                "conditions_review_reference": review_reference,
                                "registered_activity_definition_reference": (
                                    definition_reference
                                ),
                                "registered_activity_definition_hash_algorithm": (
                                    hash_algorithm
                                ),
                                "registered_activity_definition_sha256": (
                                    definition_hash
                                ),
                                "registered_activity_registry_sha256": (
                                    registry_hash
                                ),
                                "conditions_reviewed_by": reviewed_by,
                                "conditions_review_date": review_date.isoformat(),
                                "conditions_review_rationale": review_rationale,
                            }
                        )
                    else:
                        effective_decision = "PROHIBITED"

                effective_decisions[activity_id] = effective_decision
                activity_by_class[route_class][activity_id].add(
                    effective_decision
                )

        resolved.append(
            {
                "response_id": response_id,
                "route_id": route_id,
                "route_type": route["route_type"].strip(),
                "route_class": route_class,
                "organization": organization,
                "response_date": response_date.isoformat(),
                "response_reference": response_reference,
                "activity_decisions": decisions,
                "effective_scope_decisions": (
                    effective_decisions
                    if route_class != "ROUTING_ONLY"
                    else decisions
                ),
                "activity_decision_details": {
                    activity_id: {
                        "decision": decisions[activity_id],
                        "response_reference": decision_rows[activity_id].get(
                            "response_reference"
                        ),
                        "valid_from": decision_rows[activity_id].get(
                            "valid_from"
                        ),
                        "valid_through": decision_rows[activity_id].get(
                            "valid_through"
                        ),
                        "conditions": decision_rows[activity_id].get(
                            "conditions"
                        ),
                        "conditions_compatible_with_registered_activity": (
                            decision_rows[activity_id].get(
                                "conditions_compatible_with_registered_activity"
                            )
                        ),
                        "conditions_review_reference": decision_rows[
                            activity_id
                        ].get("conditions_review_reference"),
                        "registered_activity_definition_reference": decision_rows[
                            activity_id
                        ].get("registered_activity_definition_reference"),
                        "registered_activity_definition_hash_algorithm": decision_rows[
                            activity_id
                        ].get("registered_activity_definition_hash_algorithm"),
                        "registered_activity_definition_sha256": decision_rows[
                            activity_id
                        ].get("registered_activity_definition_sha256"),
                        "registered_activity_registry_sha256": decision_rows[
                            activity_id
                        ].get("registered_activity_registry_sha256"),
                        "conditions_reviewed_by": decision_rows[
                            activity_id
                        ].get("conditions_reviewed_by"),
                        "conditions_review_date": decision_rows[
                            activity_id
                        ].get("conditions_review_date"),
                        "conditions_review_rationale": decision_rows[
                            activity_id
                        ].get("conditions_review_rationale"),
                    }
                    for activity_id in sorted(ALL_ACTIVITIES)
                },
                "conditions": response.get("conditions"),
            }
        )

    def _class_state(route_class: str, activity_id: str) -> str:
        decisions = activity_by_class[route_class].get(activity_id, set())
        positives = decisions & {"ALLOWED", "NO_PERMISSION_REQUIRED"}
        negative = "PROHIBITED" in decisions
        unresolved = "UNRESOLVED" in decisions
        if positives and negative:
            return "CONFLICT"
        if negative:
            return "BLOCKED"
        if positives:
            return "PASS"
        if unresolved or not decisions:
            return "UNRESOLVED"
        raise ValueError("unreachable permission decision state")

    all_activity_matrix: dict[str, dict[str, str]] = {}
    for activity_id in sorted(ALL_ACTIVITIES):
        all_activity_matrix[activity_id] = {
            "regulatory": _class_state("REGULATORY", activity_id),
            "site": _class_state("SITE", activity_id),
        }

    required_matrix = {
        activity_id: all_activity_matrix[activity_id]
        for activity_id in sorted(REQUIRED_ACTIVITIES)
    }

    all_activity_validity = {
        activity_id: {
            "regulatory": validity_by_class["REGULATORY"].get(
                activity_id, []
            ),
            "site": validity_by_class["SITE"].get(activity_id, []),
        }
        for activity_id in sorted(ALL_ACTIVITIES)
    }

    required_activity_validity = {
        activity_id: {
            "regulatory": validity_by_class["REGULATORY"].get(
                activity_id, []
            ),
            "site": validity_by_class["SITE"].get(activity_id, []),
        }
        for activity_id in sorted(REQUIRED_ACTIVITIES)
    }

    states = {
        state
        for activity in required_matrix.values()
        for state in activity.values()
    }
    if "CONFLICT" in states:
        status = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFLICTING"
    elif "BLOCKED" in states:
        status = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_BLOCKED"
    elif states == {"PASS"}:
        status = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    else:
        status = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_INCOMPLETE"

    confirmed = status == "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
    return {
        "schema_version": "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1",
        "status": status,
        "candidate_id": candidate_id,
        "response_bundle_id": bundle_id,
        "required_scope": REQUIRED_SCOPE,
        "required_activities": sorted(REQUIRED_ACTIVITIES),
        "required_activity_matrix": required_matrix,
        "required_activity_validity": required_activity_validity,
        "all_activity_matrix": all_activity_matrix,
        "all_activity_validity": all_activity_validity,
        "activity_definition_schema": (
            "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
        ),
        "activity_definition_hash_algorithm": ACTIVITY_HASH_ALGORITHM,
        "activity_definition_registry_sha256": definition_registry_hash,
        "responses": resolved,
        "recovery_handoff": {
            "sampling_permission_status": "CONFIRMED" if confirmed else "UNRESOLVED",
            "sampling_permission_scope": REQUIRED_SCOPE if confirmed else None,
            "sampling_permission_reference": (
                "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1@"
                + metadata["adjudication_commit"]
                if confirmed
                else None
            ),
            "required_activity_validity": (
                required_activity_validity if confirmed else None
            ),
            "destructive_activities_D_to_F_required_for_recovery_p0a_p0b": False,
        },
        "claim_ceiling": (
            "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE_PERMISSION_SCOPE_ONLY_"
            "NO_D_TO_F_PERMISSION_INFERENCE_NO_FRESH_CONTEXT_NO_G1_G5_RESULT"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Adjudicate official/site responses for the Pedicularis WAVE1 recovery/P0a permission scope"
    )
    parser.add_argument("response_bundle_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = adjudicate(
        json.loads(args.response_bundle_json.read_text(encoding="utf-8"))
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
