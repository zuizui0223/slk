from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
CONFIRMED_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
OBS_SCHEMA = "SLK_PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1"
REQUIRED_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def compile_permission(receipt: dict, observation: dict) -> dict:
    _need(receipt.get("schema_version") == RECEIPT_SCHEMA, "wrong permission-scope receipt schema")
    _need(receipt.get("status") == CONFIRMED_STATUS, "permission scope is not confirmed")
    _need(receipt.get("required_scope") == REQUIRED_SCOPE, "permission scope changed")
    handoff = receipt.get("recovery_handoff", {})
    _need(handoff.get("sampling_permission_status") == "CONFIRMED", "permission handoff is not confirmed")
    _need(handoff.get("sampling_permission_scope") == REQUIRED_SCOPE, "permission handoff scope changed")
    reference = handoff.get("sampling_permission_reference")
    _need(isinstance(reference, str) and reference.strip(), "permission handoff reference missing")

    _need(observation.get("schema_version") == OBS_SCHEMA, "wrong recovery observation schema")
    candidate_id = observation.get("context", {}).get("candidate_id")
    _need(candidate_id == receipt.get("candidate_id"), "permission/recovery candidate mismatch")

    out = copy.deepcopy(observation)
    fresh = out.setdefault("fresh_verification", {})
    fresh["sampling_permission_status"] = "CONFIRMED"
    fresh["sampling_permission_scope"] = REQUIRED_SCOPE
    fresh["sampling_permission_reference"] = reference
    validity = receipt.get("required_activity_validity")
    _need(
        isinstance(validity, dict) and set(validity) == {"A", "B", "C"},
        "permission validity inventory missing",
    )
    all_matrix = receipt.get("all_activity_matrix")
    all_validity = receipt.get("all_activity_validity")
    _need(
        isinstance(all_matrix, dict) and set(all_matrix) == set("ABCDEF"),
        "all-activity permission matrix missing",
    )
    _need(
        isinstance(all_validity, dict) and set(all_validity) == set("ABCDEF"),
        "all-activity permission validity missing",
    )
    out["permission_scope_receipt"] = {
        "schema_version": RECEIPT_SCHEMA,
        "status": CONFIRMED_STATUS,
        "candidate_id": receipt["candidate_id"],
        "response_bundle_id": receipt["response_bundle_id"],
        "required_scope": REQUIRED_SCOPE,
        "required_activity_matrix": receipt["required_activity_matrix"],
        "required_activity_validity": copy.deepcopy(validity),
        "all_activity_matrix": copy.deepcopy(all_matrix),
        "all_activity_validity": copy.deepcopy(all_validity),
        "sampling_permission_reference": reference,
    }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile a confirmed WAVE1 permission-scope receipt into a fresh context-recovery observation"
    )
    parser.add_argument("permission_scope_receipt_json", type=Path)
    parser.add_argument("recovery_observation_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_permission(
        json.loads(args.permission_scope_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.recovery_observation_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
