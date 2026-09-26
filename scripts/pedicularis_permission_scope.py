from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "data" / "PEDICULARIS_WAVE1_PERMISSION_CONTACT_ROUTES_V1.csv"
ACTIVITY_DEFINITIONS = (
    ROOT / "data" / "PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json"
)

RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
CONFIRMED_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
REQUIRED_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
ACTIVITY_DEFINITION_SCHEMA = "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
REQUIRED_ACTIVITIES = {"A", "B", "C"}
ALL_ACTIVITIES = {"A", "B", "C", "D", "E", "F"}
ALLOWED_DECISIONS = {
    "ALLOWED",
    "NO_PERMISSION_REQUIRED",
    "PROHIBITED",
    "UNRESOLVED",
}
RESOLVED_DECISIONS = {"ALLOWED", "NO_PERMISSION_REQUIRED", "PROHIBITED"}
POSITIVE_DECISIONS = {"ALLOWED", "NO_PERMISSION_REQUIRED"}
SOURCE_CHANNELS = {
    "EMAIL",
    "WEB_PORTAL",
    "LETTER",
    "PHONE_CALL",
    "IN_PERSON",
}
DECISION_EVIDENCE_PREFIXES_BY_CHANNEL = {
    "EMAIL": ("BODY:", "ATTACHMENT:"),
    "WEB_PORTAL": ("BODY:", "ATTACHMENT:"),
    "LETTER": ("BODY:", "ATTACHMENT:"),
    "PHONE_CALL": ("CALL_NOTE:",),
    "IN_PERSON": ("IN_PERSON_NOTE:",),
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
    text = str(value).strip()
    _need(
        bool(text)
        and text.lower() not in {"none", "null"}
        and "REQUIRED_BEFORE_USE" not in text,
        f"unresolved {label}",
    )
    return text


def _iso_date(value: object, label: str) -> date:
    text = _filled(value, label)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


def _iso_datetime(value: object, label: str) -> datetime:
    text = _filled(value, label)
    try:
        out = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO 8601 datetime") from exc
    _need(out.tzinfo is not None, f"{label} must include timezone offset")
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


def _is_sha256(value: str) -> bool:
    return (
        len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value.lower())
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _canonical_routes(candidate_id: str) -> dict[str, dict[str, str]]:
    rows = [
        row
        for row in _read_csv(ROUTES)
        if row["candidate_id"].strip() == candidate_id
    ]
    _need(
        bool(rows),
        f"no registered permission routes for candidate: {candidate_id}",
    )
    return {row["route_id"].strip(): row for row in rows}


def _activity_definitions() -> dict[str, dict]:
    payload = json.loads(ACTIVITY_DEFINITIONS.read_text(encoding="utf-8"))
    _need(
        payload.get("schema_version") == ACTIVITY_DEFINITION_SCHEMA,
        "wrong permission activity-definition schema",
    )
    activities = payload.get("activities")
    _need(
        isinstance(activities, dict) and set(activities) == ALL_ACTIVITIES,
        "permission activity-definition inventory changed",
    )
    return activities


def _route_class(route_type: str) -> str:
    if route_type == "REGULATORY_ROUTING":
        return "REGULATORY"
    if route_type in SITE_AUTHORIZING_ROUTE_TYPES:
        return "SITE"
    if route_type in ROUTING_ONLY_TYPES:
        return "ROUTING_ONLY"
    raise ValueError(f"unsupported permission route type: {route_type}")


def _class_state(decisions: set[str]) -> str:
    positives = decisions & POSITIVE_DECISIONS
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


def _expected_interval(
    response_id: str,
    route_id: str,
    detail: dict,
    extraction_date: date,
    review_date: date,
    definition_reference: str,
) -> dict:
    return {
        "response_id": response_id,
        "route_id": route_id,
        "response_reference": _filled(
            detail.get("response_reference"),
            f"{response_id}/response_reference",
        ),
        "decision_evidence_locator": _filled(
            detail.get("decision_evidence_locator"),
            f"{response_id}/decision_evidence_locator",
        ),
        "decision_extracted_by": _filled(
            detail.get("decision_extracted_by"),
            f"{response_id}/decision_extracted_by",
        ),
        "decision_extraction_date": extraction_date.isoformat(),
        "decision_extraction_reference": _filled(
            detail.get("decision_extraction_reference"),
            f"{response_id}/decision_extraction_reference",
        ),
        "decision_extraction_rationale": _filled(
            detail.get("decision_extraction_rationale"),
            f"{response_id}/decision_extraction_rationale",
        ),
        "decision": detail["decision"],
        "valid_from": _iso_date(
            detail.get("valid_from"),
            f"{response_id}/valid_from",
        ).isoformat(),
        "valid_through": _iso_date(
            detail.get("valid_through"),
            f"{response_id}/valid_through",
        ).isoformat(),
        "conditions": _filled(
            detail.get("conditions"),
            f"{response_id}/conditions",
        ),
        "conditions_compatible_with_registered_activity": True,
        "conditions_review_reference": _filled(
            detail.get("conditions_review_reference"),
            f"{response_id}/conditions_review_reference",
        ),
        "registered_activity_definition_reference": definition_reference,
        "conditions_reviewed_by": _filled(
            detail.get("conditions_reviewed_by"),
            f"{response_id}/conditions_reviewed_by",
        ),
        "conditions_review_date": review_date.isoformat(),
        "conditions_review_rationale": _filled(
            detail.get("conditions_review_rationale"),
            f"{response_id}/conditions_review_rationale",
        ),
    }


def validate_confirmed_permission_scope(
    receipt: dict,
    *,
    expected_candidate_id: str | None = None,
) -> dict:
    _need(
        receipt.get("schema_version") == RECEIPT_SCHEMA,
        "wrong permission-scope receipt schema",
    )
    _need(
        receipt.get("status") == CONFIRMED_STATUS,
        "permission scope receipt is not confirmed",
    )
    candidate_id = _filled(receipt.get("candidate_id"), "candidate_id")
    if expected_candidate_id is not None:
        _need(
            candidate_id == expected_candidate_id,
            "permission scope receipt candidate mismatch",
        )
    bundle_id = _filled(receipt.get("response_bundle_id"), "response_bundle_id")
    _need(
        receipt.get("required_scope") == REQUIRED_SCOPE,
        "permission scope changed",
    )
    required_activities = receipt.get("required_activities")
    _need(
        isinstance(required_activities, list)
        and set(required_activities) == REQUIRED_ACTIVITIES
        and len(required_activities) == len(REQUIRED_ACTIVITIES),
        "required permission activity inventory changed",
    )
    _need(
        receipt.get("activity_definition_schema")
        == ACTIVITY_DEFINITION_SCHEMA,
        "permission activity-definition schema changed",
    )

    metadata = receipt.get("adjudication_metadata")
    _need(
        isinstance(metadata, dict),
        "permission adjudication metadata missing",
    )
    for key in (
        "slk_source_commit",
        "adjudication_commit",
        "adjudication_timestamp",
    ):
        _filled(metadata.get(key), f"adjudication_metadata.{key}")
    adjudication_day = _iso_date(
        str(metadata["adjudication_timestamp"])[:10],
        "adjudication_metadata.adjudication_timestamp",
    )

    canonical_routes = _canonical_routes(candidate_id)
    activity_definitions = _activity_definitions()

    responses = receipt.get("responses")
    _need(
        isinstance(responses, list) and responses,
        "permission receipt responses missing",
    )
    response_ids = [
        _filled(response.get("response_id"), "response_id")
        for response in responses
    ]
    _need(
        len(response_ids) == len(set(response_ids)),
        "permission receipt response_id duplicated",
    )
    source_event_ids: set[str] = set()

    activity_by_class: dict[str, dict[str, set[str]]] = {
        "REGULATORY": defaultdict(set),
        "SITE": defaultdict(set),
    }
    expected_validity: dict[str, dict[str, list[dict]]] = {
        activity_id: {"regulatory": [], "site": []}
        for activity_id in sorted(ALL_ACTIVITIES)
    }

    for response in responses:
        response_id = _filled(response.get("response_id"), "response_id")
        route_id = _filled(
            response.get("route_id"),
            f"route_id/{response_id}",
        )
        _need(
            route_id in canonical_routes,
            f"permission response route not canonical: {route_id}",
        )
        canonical_route = canonical_routes[route_id]
        route_type = canonical_route["route_type"].strip()
        route_class = _route_class(route_type)
        _need(
            response.get("route_type") == route_type,
            f"permission response route_type mismatch: {response_id}",
        )
        _need(
            response.get("route_class") == route_class,
            f"permission response route_class mismatch: {response_id}",
        )
        _need(
            response.get("organization")
            == canonical_route["organization"].strip(),
            f"permission response organization mismatch: {response_id}",
        )

        response_date = _iso_date(
            response.get("response_date"),
            f"response_date/{response_id}",
        )
        _filled(
            response.get("response_reference"),
            f"response_reference/{response_id}",
        )
        source_event_id = _filled(
            response.get("source_response_event_id"),
            f"source_response_event_id/{response_id}",
        )
        _need(
            source_event_id not in source_event_ids,
            f"duplicate source response event id: {source_event_id}",
        )
        source_event_ids.add(source_event_id)
        received_at = _iso_datetime(
            response.get("source_response_received_at"),
            f"source_response_received_at/{response_id}",
        )
        _need(
            received_at.date() == response_date,
            f"source response received date mismatch: {response_id}",
        )
        _need(
            received_at.date() <= adjudication_day,
            f"source response received after adjudication: {response_id}",
        )
        channel = _filled(
            response.get("source_response_receive_channel"),
            f"source_response_receive_channel/{response_id}",
        )
        _need(
            channel in SOURCE_CHANNELS,
            f"unregistered source response channel: {response_id}/{channel}",
        )
        source_hash = _filled(
            response.get("source_response_content_sha256"),
            f"source_response_content_sha256/{response_id}",
        )
        _need(
            _is_sha256(source_hash),
            f"source response content hash must be sha256: {response_id}",
        )
        _filled(
            response.get("source_response_classification_review_reference"),
            f"source_response_classification_review_reference/{response_id}",
        )

        decisions = response.get("activity_decisions")
        effective = response.get("effective_scope_decisions")
        details = response.get("activity_decision_details")
        _need(
            isinstance(decisions, dict) and set(decisions) == ALL_ACTIVITIES,
            f"activity decision inventory changed: {response_id}",
        )
        _need(
            isinstance(effective, dict) and set(effective) == ALL_ACTIVITIES,
            f"effective activity decision inventory changed: {response_id}",
        )
        _need(
            isinstance(details, dict) and set(details) == ALL_ACTIVITIES,
            f"activity decision detail inventory changed: {response_id}",
        )

        if route_class == "ROUTING_ONLY":
            _need(
                all(
                    decision in {"UNRESOLVED", "PROHIBITED"}
                    for decision in decisions.values()
                ),
                f"routing-only response authorizes activity: {response_id}",
            )

        for activity_id in sorted(ALL_ACTIVITIES):
            decision = decisions[activity_id]
            _need(
                decision in ALLOWED_DECISIONS,
                f"unregistered activity decision: {response_id}/{activity_id}",
            )
            detail = details[activity_id]
            _need(
                isinstance(detail, dict),
                f"activity detail must be object: {response_id}/{activity_id}",
            )
            _need(
                detail.get("decision") == decision,
                f"activity detail decision mismatch: {response_id}/{activity_id}",
            )

            extraction_date = None
            if decision in RESOLVED_DECISIONS:
                _filled(
                    detail.get("response_reference"),
                    f"{response_id}/{activity_id}/response_reference",
                )
                locator = _filled(
                    detail.get("decision_evidence_locator"),
                    f"{response_id}/{activity_id}/decision_evidence_locator",
                )
                _need(
                    locator.startswith(
                        DECISION_EVIDENCE_PREFIXES_BY_CHANNEL[channel]
                    ),
                    "decision evidence locator/channel mismatch: "
                    f"{response_id}/{activity_id}/{channel}",
                )
                _filled(
                    detail.get("decision_extracted_by"),
                    f"{response_id}/{activity_id}/decision_extracted_by",
                )
                extraction_date = _iso_date(
                    detail.get("decision_extraction_date"),
                    f"{response_id}/{activity_id}/decision_extraction_date",
                )
                _need(
                    response_date <= extraction_date <= adjudication_day,
                    "decision extraction date outside response/adjudication window: "
                    f"{response_id}/{activity_id}",
                )
                _filled(
                    detail.get("decision_extraction_reference"),
                    f"{response_id}/{activity_id}/decision_extraction_reference",
                )
                _filled(
                    detail.get("decision_extraction_rationale"),
                    f"{response_id}/{activity_id}/decision_extraction_rationale",
                )

            expected_effective = decision
            if decision in POSITIVE_DECISIONS:
                valid_from = _iso_date(
                    detail.get("valid_from"),
                    f"{response_id}/{activity_id}/valid_from",
                )
                valid_through = _iso_date(
                    detail.get("valid_through"),
                    f"{response_id}/{activity_id}/valid_through",
                )
                _need(
                    valid_from <= valid_through,
                    f"permission validity interval reversed: {response_id}/{activity_id}",
                )
                _need(
                    response_date <= valid_through,
                    f"permission expires before response date: {response_id}/{activity_id}",
                )
                _filled(
                    detail.get("conditions"),
                    f"{response_id}/{activity_id}/conditions",
                )
                compatible = _required_bool(
                    detail.get(
                        "conditions_compatible_with_registered_activity"
                    ),
                    "conditions_compatible_with_registered_activity/"
                    f"{response_id}/{activity_id}",
                )
                definition_reference = _filled(
                    detail.get("registered_activity_definition_reference"),
                    "registered_activity_definition_reference/"
                    f"{response_id}/{activity_id}",
                )
                _need(
                    definition_reference
                    == activity_definitions[activity_id]["definition_reference"],
                    "condition review used wrong registered activity definition: "
                    f"{response_id}/{activity_id}",
                )
                review_date = _iso_date(
                    detail.get("conditions_review_date"),
                    f"{response_id}/{activity_id}/conditions_review_date",
                )
                _need(
                    response_date <= review_date <= adjudication_day,
                    "condition review date outside response/adjudication window: "
                    f"{response_id}/{activity_id}",
                )
                _filled(
                    detail.get("conditions_review_reference"),
                    f"{response_id}/{activity_id}/conditions_review_reference",
                )
                _filled(
                    detail.get("conditions_reviewed_by"),
                    f"{response_id}/{activity_id}/conditions_reviewed_by",
                )
                _filled(
                    detail.get("conditions_review_rationale"),
                    f"{response_id}/{activity_id}/conditions_review_rationale",
                )
                if compatible:
                    _need(
                        extraction_date is not None,
                        f"positive activity extraction date missing: {response_id}/{activity_id}",
                    )
                    expected_validity[activity_id][
                        "regulatory" if route_class == "REGULATORY" else "site"
                    ].append(
                        _expected_interval(
                            response_id,
                            route_id,
                            detail,
                            extraction_date,
                            review_date,
                            definition_reference,
                        )
                    )
                else:
                    expected_effective = "PROHIBITED"

            _need(
                effective[activity_id] == expected_effective,
                f"effective activity decision mismatch: {response_id}/{activity_id}",
            )
            if route_class in {"REGULATORY", "SITE"}:
                activity_by_class[route_class][activity_id].add(
                    expected_effective
                )

    recomputed_matrix = {
        activity_id: {
            "regulatory": _class_state(
                activity_by_class["REGULATORY"].get(activity_id, set())
            ),
            "site": _class_state(
                activity_by_class["SITE"].get(activity_id, set())
            ),
        }
        for activity_id in sorted(ALL_ACTIVITIES)
    }

    all_matrix = receipt.get("all_activity_matrix")
    _need(
        isinstance(all_matrix, dict) and set(all_matrix) == ALL_ACTIVITIES,
        "all-activity permission matrix inventory changed",
    )
    _need(
        all_matrix == recomputed_matrix,
        "all-activity permission matrix does not match response audit trail",
    )
    required_matrix = receipt.get("required_activity_matrix")
    _need(
        isinstance(required_matrix, dict)
        and set(required_matrix) == REQUIRED_ACTIVITIES,
        "required permission matrix inventory changed",
    )
    expected_required_matrix = {
        activity_id: recomputed_matrix[activity_id]
        for activity_id in sorted(REQUIRED_ACTIVITIES)
    }
    _need(
        required_matrix == expected_required_matrix,
        "required permission matrix does not match all-activity matrix",
    )
    _need(
        all(
            state == "PASS"
            for cell in required_matrix.values()
            for state in cell.values()
        ),
        "confirmed permission scope has non-PASS required activity cell",
    )

    all_validity = receipt.get("all_activity_validity")
    _need(
        isinstance(all_validity, dict) and set(all_validity) == ALL_ACTIVITIES,
        "all-activity permission validity inventory changed",
    )
    _need(
        all_validity == expected_validity,
        "all-activity permission validity does not match response audit trail",
    )
    required_validity = receipt.get("required_activity_validity")
    _need(
        isinstance(required_validity, dict)
        and set(required_validity) == REQUIRED_ACTIVITIES,
        "required permission validity inventory changed",
    )
    expected_required_validity = {
        activity_id: expected_validity[activity_id]
        for activity_id in sorted(REQUIRED_ACTIVITIES)
    }
    _need(
        required_validity == expected_required_validity,
        "required permission validity does not match all-activity validity",
    )
    for activity_id in sorted(REQUIRED_ACTIVITIES):
        for side in ("regulatory", "site"):
            _need(
                bool(required_validity[activity_id][side]),
                f"confirmed permission scope lacks validity: {activity_id}/{side}",
            )

    handoff = receipt.get("recovery_handoff")
    handoff_reference = None
    if handoff is not None:
        _need(
            isinstance(handoff, dict),
            "permission recovery_handoff must be object",
        )
        _need(
            handoff.get("sampling_permission_status") == "CONFIRMED",
            "permission recovery_handoff is not confirmed",
        )
        _need(
            handoff.get("sampling_permission_scope") == REQUIRED_SCOPE,
            "permission recovery_handoff scope changed",
        )
        handoff_reference = _filled(
            handoff.get("sampling_permission_reference"),
            "sampling_permission_reference",
        )
        _need(
            handoff.get("required_activity_validity")
            == required_validity,
            "permission recovery_handoff validity changed",
        )
        _need(
            handoff.get(
                "destructive_activities_D_to_F_required_for_recovery_p0a_p0b"
            )
            is False,
            "default permission handoff destructive-activity rule changed",
        )

    root_reference = receipt.get("sampling_permission_reference")
    if root_reference is not None:
        root_reference = _filled(
            root_reference,
            "sampling_permission_reference",
        )
    if handoff_reference is not None and root_reference is not None:
        _need(
            handoff_reference == root_reference,
            "permission sampling reference/handoff mismatch",
        )
    permission_reference = root_reference or handoff_reference
    _need(
        permission_reference is not None,
        "permission sampling reference missing",
    )

    return {
        "candidate_id": candidate_id,
        "response_bundle_id": bundle_id,
        "required_scope": REQUIRED_SCOPE,
        "sampling_permission_reference": permission_reference,
        "required_activity_matrix": required_matrix,
        "required_activity_validity": required_validity,
        "all_activity_matrix": all_matrix,
        "all_activity_validity": all_validity,
        "responses": responses,
        "adjudication_metadata": metadata,
    }


def activity_valid_on_day(
    validated: dict,
    activity_id: str,
    day: date,
) -> bool:
    _need(activity_id in ALL_ACTIVITIES, f"unknown permission activity: {activity_id}")
    matrix = validated["all_activity_matrix"][activity_id]
    if not (
        matrix["regulatory"] == "PASS"
        and matrix["site"] == "PASS"
    ):
        return False
    validity = validated["all_activity_validity"][activity_id]
    return all(
        any(
            date.fromisoformat(interval["valid_from"])
            <= day
            <= date.fromisoformat(interval["valid_through"])
            for interval in validity[side]
        )
        for side in ("regulatory", "site")
    )


def activities_cover_window(
    validated: dict,
    start: date,
    end: date,
    *,
    activities: tuple[str, ...] = ("A", "B", "C"),
) -> bool:
    _need(start <= end, "permission coverage window reversed")
    for activity_id in activities:
        _need(
            activity_id in ALL_ACTIVITIES,
            f"unknown permission activity: {activity_id}",
        )
        matrix = validated["all_activity_matrix"][activity_id]
        if not (
            matrix["regulatory"] == "PASS"
            and matrix["site"] == "PASS"
        ):
            return False
        validity = validated["all_activity_validity"][activity_id]
        for side in ("regulatory", "site"):
            if not any(
                date.fromisoformat(interval["valid_from"]) <= start
                and end <= date.fromisoformat(interval["valid_through"])
                for interval in validity[side]
            ):
                return False
    return True
