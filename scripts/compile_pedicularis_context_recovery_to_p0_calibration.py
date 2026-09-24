from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

RECEIPT_SCHEMA = "SLK_PEDICULARIS_CONTEXT_RECOVERY_RECEIPT_V1"
READY_STATUS = "CONTEXT_RECOVERY_READY_FOR_P0_RELEVANCE_CALIBRATION"
CAL_SCHEMA = "SLK_PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def compile_recovery(receipt: dict, calibration_template: dict) -> dict:
    _need(receipt.get("schema_version") == RECEIPT_SCHEMA, "wrong context-recovery receipt schema")
    _need(receipt.get("status") == READY_STATUS, "context recovery is not ready for P0 calibration")
    handoff = receipt.get("downstream_handoff", {})
    _need(handoff.get("p0_relevance_calibration_authorized") is True, "P0 relevance calibration not authorized")
    _need(calibration_template.get("schema_version") == CAL_SCHEMA, "wrong P0 calibration template schema")
    _need(calibration_template.get("status") == "TEMPLATE_ONLY_NOT_FROZEN", "P0 calibration target must be an untouched template")

    out = copy.deepcopy(calibration_template)
    ctx = receipt["context"]
    cctx = out["context"]
    _need(cctx.get("system") == "Pedicularis rex", "wrong P0 calibration system")
    cctx["candidate_site_id"] = ctx["candidate_site_id"]
    cctx["population_id"] = ctx["population_id"]
    cctx["season_id"] = ctx["season_id"]
    cctx["calibration_window_id"] = handoff["p0_relevance_calibration_window_id"]
    cctx["future_p0_screen_window_id"] = handoff["p0_screen_window_id"]
    cctx["frozen_before_calibration_outcomes"] = False
    cctx["p0_outcomes_opened"] = False

    out["status"] = "CONTEXT_RECOVERY_COMPILED_AWAITING_P0_CALIBRATION_DESIGN"
    out.setdefault("freeze_metadata", {})["context_recovery_reference"] = (
        f"SLK_PEDICULARIS_CONTEXT_RECOVERY_RECEIPT_V1@{receipt['freeze_commit']}"
    )
    out["compiler_claim_ceiling"] = (
        "CONTEXT_IDENTIFIERS_AND_WINDOWS_COMPILED_ONLY; sampling floors, bootstrap rule, "
        "freeze metadata and final prospective P0 calibration freeze remain unresolved."
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile a positive Pedicularis context-recovery receipt into the P0 calibration template")
    parser.add_argument("context_recovery_receipt_json", type=Path)
    parser.add_argument("p0_calibration_template_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_recovery(
        json.loads(args.context_recovery_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.p0_calibration_template_json.read_text(encoding="utf-8")),
    )
    text_out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text_out, encoding="utf-8")
    else:
        print(text_out, end="")


if __name__ == "__main__":
    main()
