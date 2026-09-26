from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

try:
    from scripts.pedicularis_permission_scope import (
        validate_confirmed_scope_receipt,
    )
except ImportError:
    from pedicularis_permission_scope import (
        validate_confirmed_scope_receipt,
    )

RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
CONFIRMED_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
OBS_SCHEMA = "SLK_PEDICULARIS_CONTEXT_RECOVERY_OBSERVATION_V1"
REQUIRED_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def compile_permission(receipt: dict, observation: dict) -> dict:
    _need(observation.get("schema_version") == OBS_SCHEMA, "wrong recovery observation schema")
    candidate_id = observation.get("context", {}).get("candidate_id")
    validated = validate_confirmed_scope_receipt(
        receipt,
        expected_candidate_id=candidate_id,
    )
    reference = validated["sampling_permission_reference"]

    out = copy.deepcopy(observation)
    fresh = out.setdefault("fresh_verification", {})
    fresh["sampling_permission_status"] = "CONFIRMED"
    fresh["sampling_permission_scope"] = REQUIRED_SCOPE
    fresh["sampling_permission_reference"] = reference
    out["permission_scope_receipt"] = copy.deepcopy(receipt)
    out["permission_scope_receipt"][
        "sampling_permission_reference"
    ] = reference
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
