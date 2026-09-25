from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS_PATH = (
    ROOT / "data" / "PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json"
)

SCHEMA = "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
HASH_ALGORITHM = "SHA256_CANONICAL_JSON_V1"
ACTIVITY_IDS = set("ABCDEF")
HASH_FIELDS = (
    "activity_id",
    "label",
    "definition_reference",
    "registered_definition",
    "destructive",
    "required_for_default_recovery_p0_scope",
)


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def load_registry() -> dict:
    payload = json.loads(DEFINITIONS_PATH.read_text(encoding="utf-8"))
    _need(payload.get("schema_version") == SCHEMA, "wrong activity-definition schema")
    activities = payload.get("activities")
    _need(
        isinstance(activities, dict) and set(activities) == ACTIVITY_IDS,
        "activity-definition inventory changed",
    )
    for activity_id, row in activities.items():
        _need(isinstance(row, dict), f"activity definition must be object: {activity_id}")
        _need(
            row.get("activity_id") == activity_id,
            f"activity definition id mismatch: {activity_id}",
        )
        for field in HASH_FIELDS:
            _need(field in row, f"activity definition field missing: {activity_id}/{field}")
    return payload


def canonical_activity_payload(activity: dict) -> dict:
    return {field: activity[field] for field in HASH_FIELDS}


def activity_definition_sha256(activity: dict) -> str:
    raw = json.dumps(
        canonical_activity_payload(activity),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def registry_sha256(payload: dict | None = None) -> str:
    payload = payload or load_registry()
    activities = payload["activities"]
    canonical = {
        activity_id: canonical_activity_payload(activities[activity_id])
        for activity_id in sorted(activities)
    }
    raw = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def activity_receipt(activity_id: str) -> dict[str, str]:
    payload = load_registry()
    activity = payload["activities"][activity_id]
    return {
        "definition_reference": activity["definition_reference"],
        "hash_algorithm": HASH_ALGORITHM,
        "definition_sha256": activity_definition_sha256(activity),
        "registry_sha256": registry_sha256(payload),
    }
