from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json"


def test_permission_activity_definition_registry_is_complete_and_stable() -> None:
    payload = json.loads(PATH.read_text())
    assert payload["schema_version"] == (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1"
    )
    activities = payload["activities"]
    assert set(activities) == set("ABCDEF")
    for activity_id, row in activities.items():
        assert row["activity_id"] == activity_id
        assert row["definition_reference"] == (
            "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#"
            + activity_id
        )
        assert row["registered_definition"]
    assert all(
        activities[x]["required_for_default_recovery_p0_scope"] is True
        and activities[x]["destructive"] is False
        for x in "ABC"
    )
    assert all(
        activities[x]["required_for_default_recovery_p0_scope"] is False
        and activities[x]["destructive"] is True
        for x in "DEF"
    )


def test_condition_review_policy_requires_auditable_metadata() -> None:
    policy = json.loads(PATH.read_text())["review_policy"]
    assert policy["positive_decisions_requiring_condition_review"] == [
        "ALLOWED",
        "NO_PERMISSION_REQUIRED",
    ]
    assert policy["reviewer_must_be_identified"] is True
    assert policy["review_date_required"] is True
    assert policy["review_rationale_required"] is True
    assert policy["review_reference_required"] is True
    assert policy["no_additional_conditions_sentinel"] == (
        "NO_ADDITIONAL_CONDITIONS"
    )
