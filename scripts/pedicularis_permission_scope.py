from __future__ import annotations

from datetime import date, datetime

RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
CONFIRMED_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
REQUIRED_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
ACTIVITY_DEFINITION_SCHEMA = "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
REQUIRED_ACTIVITIES = {"A", "B", "C"}
ALL_ACTIVITIES = set("ABCDEF")
POSITIVE_DECISIONS = {"ALLOWED", "NO_PERMISSION_REQUIRED"}
RESOLVED_DECISIONS = POSITIVE_DECISIONS | {"PROHIBITED"}
EVIDENCE_PREFIXES_BY_CHANNEL = {
    "EMAIL": ("BODY:", "ATTACHMENT:"),
    "WEB_PORTAL": ("BODY:", "ATTACHMENT:"),
    "LETTER": ("BODY:", "ATTACHMENT:"),
    "PHONE_CALL": ("CALL_NOTE:",),
    "IN_PERSON": ("IN_PERSON_NOTE:",),
}


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


def _sha256(value: object, label: str) -> str:
    text = _filled(value, label)
    _need(
        len(text) == 64
        and all(ch in "0123456789abcdef" for ch in text.lower()),
        f"{label} must be sha256",
    )
    return text


def _validate_interval(
    interval: dict,
    *,
    activity_id: str,
    side: str,
    index: int,
    adjudication_day: date,
) -> None:
    prefix = f"{activity_id}/{side}/{index}"
    _need(isinstance(interval, dict), f"permission interval must be object: {prefix}")
    decision = _filled(interval.get("decision"), f"{prefix}/decision")
    _need(
        decision in POSITIVE_DECISIONS,
        f"permission interval decision must be positive: {prefix}",
    )
    start = _iso_date(interval.get("valid_from"), f"{prefix}/valid_from")
    end = _iso_date(interval.get("valid_through"), f"{prefix}/valid_through")
    _need(start <= end, f"permission interval reversed: {prefix}")
    _filled(interval.get("response_id"), f"{prefix}/response_id")
    _filled(interval.get("route_id"), f"{prefix}/route_id")
    _filled(interval.get("response_reference"), f"{prefix}/response_reference")

    locator = _filled(
        interval.get("decision_evidence_locator"),
        f"{prefix}/decision_evidence_locator",
    )
    _filled(interval.get("decision_extracted_by"), f"{prefix}/decision_extracted_by")
    extraction_day = _iso_date(
        interval.get("decision_extraction_date"),
        f"{prefix}/decision_extraction_date",
    )
    _need(
        extraction_day <= adjudication_day,
        f"decision extraction occurs after adjudication: {prefix}",
    )
    _filled(
        interval.get("decision_extraction_reference"),
        f"{prefix}/decision_extraction_reference",
    )
    _filled(
        interval.get("decision_extraction_rationale"),
        f"{prefix}/decision_extraction_rationale",
    )

    conditions = _filled(interval.get("conditions"), f"{prefix}/conditions")
    _need(bool(conditions), f"permission interval conditions missing: {prefix}")
    _need(
        interval.get("conditions_compatible_with_registered_activity") is True,
        f"permission interval condition compatibility not confirmed: {prefix}",
    )
    _filled(
        interval.get("conditions_review_reference"),
        f"{prefix}/conditions_review_reference",
    )
    expected_definition = (
        f"{ACTIVITY_DEFINITION_SCHEMA}#{activity_id}"
    )
    _need(
        interval.get("registered_activity_definition_reference")
        == expected_definition,
        f"permission interval activity definition mismatch: {prefix}",
    )
    _filled(interval.get("conditions_reviewed_by"), f"{prefix}/conditions_reviewed_by")
    review_day = _iso_date(
        interval.get("conditions_review_date"),
        f"{prefix}/conditions_review_date",
    )
    _need(
        review_day <= adjudication_day,
        f"condition review occurs after adjudication: {prefix}",
    )
    _filled(
        interval.get("conditions_review_rationale"),
        f"{prefix}/conditions_review_rationale",
    )
    _need(
        locator.startswith(("BODY:", "ATTACHMENT:", "CALL_NOTE:", "IN_PERSON_NOTE:")),
        f"permission interval decision evidence locator prefix invalid: {prefix}",
    )


def _validate_response(
    response: dict,
    *,
    adjudication_day: date,
    seen_event_ids: set[str],
) -> None:
    response_id = _filled(response.get("response_id"), "response.response_id")
    response_date = _iso_date(
        response.get("response_date"),
        f"response_date/{response_id}",
    )
    event_id = _filled(
        response.get("source_response_event_id"),
        f"source_response_event_id/{response_id}",
    )
    _need(
        event_id not in seen_event_ids,
        f"duplicate source response event id: {event_id}",
    )
    seen_event_ids.add(event_id)
    received = _iso_datetime(
        response.get("source_response_received_at"),
        f"source_response_received_at/{response_id}",
    )
    _need(
        received.date() == response_date,
        f"source response received date mismatch: {response_id}",
    )
    _need(
        received.date() <= adjudication_day,
        f"source response received after adjudication: {response_id}",
    )
    channel = _filled(
        response.get("source_response_receive_channel"),
        f"source_response_receive_channel/{response_id}",
    )
    _need(
        channel in EVIDENCE_PREFIXES_BY_CHANNEL,
        f"unregistered source response channel: {response_id}",
    )
    _sha256(
        response.get("source_response_content_sha256"),
        f"source_response_content_sha256/{response_id}",
    )
    _filled(
        response.get("source_response_classification_review_reference"),
        f"source_response_classification_review_reference/{response_id}",
    )

    details = response.get("activity_decision_details")
    _need(
        isinstance(details, dict) and set(details) == ALL_ACTIVITIES,
        f"activity decision detail inventory changed: {response_id}",
    )
    for activity_id, row in details.items():
        _need(isinstance(row, dict), f"activity decision detail must be object: {response_id}/{activity_id}")
        decision = _filled(
            row.get("decision"),
            f"{response_id}/{activity_id}/decision",
        )
        if decision not in RESOLVED_DECISIONS:
            continue
        _filled(
            row.get("response_reference"),
            f"{response_id}/{activity_id}/response_reference",
        )
        locator = _filled(
            row.get("decision_evidence_locator"),
            f"{response_id}/{activity_id}/decision_evidence_locator",
        )
        _need(
            locator.startswith(EVIDENCE_PREFIXES_BY_CHANNEL[channel]),
            f"decision evidence locator/channel mismatch: {response_id}/{activity_id}",
        )
        _filled(
            row.get("decision_extracted_by"),
            f"{response_id}/{activity_id}/decision_extracted_by",
        )
        extraction_day = _iso_date(
            row.get("decision_extraction_date"),
            f"{response_id}/{activity_id}/decision_extraction_date",
        )
        _need(
            response_date <= extraction_day <= adjudication_day,
            f"decision extraction date outside response/adjudication window: {response_id}/{activity_id}",
        )
        _filled(
            row.get("decision_extraction_reference"),
            f"{response_id}/{activity_id}/decision_extraction_reference",
        )
        _filled(
            row.get("decision_extraction_rationale"),
            f"{response_id}/{activity_id}/decision_extraction_rationale",
        )

        if decision in POSITIVE_DECISIONS:
            _iso_date(row.get("valid_from"), f"{response_id}/{activity_id}/valid_from")
            _iso_date(row.get("valid_through"), f"{response_id}/{activity_id}/valid_through")
            _filled(row.get("conditions"), f"{response_id}/{activity_id}/conditions")
            _need(
                row.get("conditions_compatible_with_registered_activity") is not None,
                f"condition compatibility missing: {response_id}/{activity_id}",
            )
            _filled(
                row.get("conditions_review_reference"),
                f"{response_id}/{activity_id}/conditions_review_reference",
            )
            _need(
                row.get("registered_activity_definition_reference")
                == f"{ACTIVITY_DEFINITION_SCHEMA}#{activity_id}",
                f"condition review activity definition mismatch: {response_id}/{activity_id}",
            )
            _filled(
                row.get("conditions_reviewed_by"),
                f"{response_id}/{activity_id}/conditions_reviewed_by",
            )
            review_day = _iso_date(
                row.get("conditions_review_date"),
                f"{response_id}/{activity_id}/conditions_review_date",
            )
            _need(
                response_date <= review_day <= adjudication_day,
                f"condition review date outside response/adjudication window: {response_id}/{activity_id}",
            )
            _filled(
                row.get("conditions_review_rationale"),
                f"{response_id}/{activity_id}/conditions_review_rationale",
            )


def validate_confirmed_scope_receipt(
    receipt: dict,
    *,
    expected_candidate_id: str | None = None,
) -> dict:
    _need(receipt.get("schema_version") == RECEIPT_SCHEMA, "wrong permission-scope receipt schema")
    _need(receipt.get("status") == CONFIRMED_STATUS, "permission scope is not confirmed")
    _need(receipt.get("required_scope") == REQUIRED_SCOPE, "permission scope changed")
    candidate_id = _filled(receipt.get("candidate_id"), "permission candidate_id")
    if expected_candidate_id is not None:
        _need(
            candidate_id == expected_candidate_id,
            "permission scope receipt candidate mismatch",
        )
    _need(
        receipt.get("activity_definition_schema") == ACTIVITY_DEFINITION_SCHEMA,
        "permission activity definition schema changed",
    )

    metadata = receipt.get("adjudication_metadata")
    _need(isinstance(metadata, dict), "permission adjudication metadata missing")
    _filled(metadata.get("slk_source_commit"), "permission adjudication slk_source_commit")
    _filled(metadata.get("adjudication_commit"), "permission adjudication commit")
    adjudicated_at = _iso_datetime(
        metadata.get("adjudication_timestamp"),
        "permission adjudication timestamp",
    )
    adjudication_day = adjudicated_at.date()

    matrix = receipt.get("required_activity_matrix")
    validity = receipt.get("required_activity_validity")
    _need(
        isinstance(matrix, dict) and set(matrix) == REQUIRED_ACTIVITIES,
        "required permission activity matrix changed",
    )
    _need(
        isinstance(validity, dict) and set(validity) == REQUIRED_ACTIVITIES,
        "required permission validity inventory changed",
    )
    for activity_id in sorted(REQUIRED_ACTIVITIES):
        cell = matrix[activity_id]
        _need(
            isinstance(cell, dict)
            and cell.get("regulatory") == "PASS"
            and cell.get("site") == "PASS",
            f"required permission scope not passed: {activity_id}",
        )
        validity_cell = validity[activity_id]
        _need(
            isinstance(validity_cell, dict)
            and set(validity_cell) == {"regulatory", "site"},
            f"required permission validity cell changed: {activity_id}",
        )
        for side in ("regulatory", "site"):
            intervals = validity_cell[side]
            _need(
                isinstance(intervals, list) and intervals,
                f"required permission validity missing: {activity_id}/{side}",
            )
            for index, interval in enumerate(intervals):
                _validate_interval(
                    interval,
                    activity_id=activity_id,
                    side=side,
                    index=index,
                    adjudication_day=adjudication_day,
                )

    all_matrix = receipt.get("all_activity_matrix")
    all_validity = receipt.get("all_activity_validity")
    _need(
        isinstance(all_matrix, dict) and set(all_matrix) == ALL_ACTIVITIES,
        "all-activity permission matrix changed",
    )
    _need(
        isinstance(all_validity, dict) and set(all_validity) == ALL_ACTIVITIES,
        "all-activity permission validity changed",
    )

    responses = receipt.get("responses")
    _need(isinstance(responses, list) and responses, "permission response provenance missing")
    seen_event_ids: set[str] = set()
    for response in responses:
        _validate_response(
            response,
            adjudication_day=adjudication_day,
            seen_event_ids=seen_event_ids,
        )

    handoff = receipt.get("recovery_handoff")
    _need(isinstance(handoff, dict), "permission recovery handoff missing")
    _need(
        handoff.get("sampling_permission_status") == "CONFIRMED",
        "permission recovery handoff is not confirmed",
    )
    _need(
        handoff.get("sampling_permission_scope") == REQUIRED_SCOPE,
        "permission recovery handoff scope changed",
    )
    reference = _filled(
        handoff.get("sampling_permission_reference"),
        "permission recovery handoff reference",
    )
    return {
        "candidate_id": candidate_id,
        "sampling_permission_reference": reference,
        "adjudication_commit": metadata["adjudication_commit"],
        "adjudication_timestamp": adjudicated_at.isoformat(),
    }
