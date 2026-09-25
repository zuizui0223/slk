from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json"
HELPER = ROOT / "scripts" / "pedicularis_permission_activity_definitions.py"

spec = importlib.util.spec_from_file_location("ped_permission_activity_defs", HELPER)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


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



def test_activity_definition_hash_is_deterministic_and_content_sensitive() -> None:
    registry = mod.load_registry()
    a = registry["activities"]["A"]
    h1 = mod.activity_definition_sha256(a)
    h2 = mod.activity_definition_sha256(copy.deepcopy(a))
    assert h1 == h2
    assert len(h1) == 64

    changed = copy.deepcopy(a)
    changed["registered_definition"] += " altered"
    assert mod.activity_definition_sha256(changed) != h1


def test_activity_receipt_contains_registry_and_activity_hashes() -> None:
    receipt = mod.activity_receipt("C")
    assert receipt["definition_reference"] == (
        "SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#C"
    )
    assert receipt["hash_algorithm"] == "SHA256_CANONICAL_JSON_V1"
    assert len(receipt["definition_sha256"]) == 64
    assert len(receipt["registry_sha256"]) == 64
    assert receipt["registry_sha256"] == mod.registry_sha256()


def test_review_policy_registers_definition_fingerprint_requirement() -> None:
    policy = json.loads(PATH.read_text())["review_policy"]
    assert policy["activity_definition_fingerprint_required"] is True
    assert policy["activity_definition_fingerprint_algorithm"] == (
        "SHA256_CANONICAL_JSON_V1"
    )
