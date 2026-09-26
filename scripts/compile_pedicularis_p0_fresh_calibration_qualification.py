from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

try:
    from scripts.pedicularis_permission_scope import (
        validate_confirmed_permission_scope,
    )
except ImportError:
    from pedicularis_permission_scope import (
        validate_confirmed_permission_scope,
    )


CAL_SCHEMA = "SLK_PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_RECEIPT_V1"
CAL_READY = "P0_RELEVANCE_FRESH_CALIBRATION_QUALIFIED"
QUAL_SCHEMA = "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def compile_qualification(calibration: dict, template: dict) -> dict:
    _need(calibration.get("schema_version") == CAL_SCHEMA, "wrong fresh-calibration receipt schema")
    _need(calibration.get("status") == CAL_READY, "fresh calibration is not qualified")
    _need(calibration.get("qualification_ready") is True, "fresh calibration qualification_ready is false")
    _need(template.get("schema_version") == QUAL_SCHEMA, "wrong relevance qualification template schema")
    _need(template.get("status") == "TEMPLATE_ONLY_NOT_QUALIFIED", "qualification target must be an untouched template")

    cctx = calibration.get("context", {})
    tctx = template.get("context", {})
    _need(tctx.get("system") == "Pedicularis rex", "wrong qualification system")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id"):
        _need(tctx.get(key) == cctx.get(key), f"calibration/qualification context mismatch: {key}")
    _need(tctx.get("p0_outcomes_opened") is False and cctx.get("p0_outcomes_opened") is False, "P0 outcomes already opened")
    _need(tctx.get("screen_window_id") == cctx.get("future_p0_screen_window_id"), "future P0 screen-window mismatch")

    estimates = calibration.get("estimates", {})
    values = calibration.get("recommended_minimum_relevance_values") or {}
    mapping = {
        "P0_POLLINATOR_MIN_RATE": ("pollinator", "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"),
        "P0_PREDATOR_MIN_PREVALENCE": ("predator", "PROPORTION_0_1"),
        "P0_WATER_POSITIVE_PREVALENCE": ("water_state", "PROPORTION_0_1"),
    }

    out = copy.deepcopy(template)
    out["context"]["candidate_id"] = cctx["candidate_id"]
    permission_receipt = calibration.get("permission_scope_receipt")
    _need(
        isinstance(permission_receipt, dict),
        "qualified fresh calibration permission scope receipt missing",
    )
    validate_confirmed_permission_scope(
        permission_receipt,
        expected_candidate_id=cctx["candidate_id"],
    )
    out["permission_scope_receipt"] = copy.deepcopy(permission_receipt)
    rows = {row["input_id"]: row for row in out["inputs"]}
    freeze_commit = calibration.get("qualification_rule", {}).get("freeze_commit")
    _need(isinstance(freeze_commit, str) and freeze_commit.strip(), "calibration freeze commit missing")

    for input_id, (estimate_key, units) in mapping.items():
        _need(input_id in values, f"calibration value missing: {input_id}")
        estimate = estimates.get(estimate_key) or {}
        row = rows[input_id]
        row["qualification_route"] = "FRESH_INDEPENDENT_CALIBRATION"
        row["source_type"] = "INDEPENDENT_NATURAL_HISTORY_CALIBRATION"
        row["source_reference"] = f"PED_P0_NAT_HIST_CAL_V1@{freeze_commit}"
        row["source_metric"] = estimate.get("metric")
        row["numeric_value"] = float(values[input_id])
        row["numeric_units"] = units
        row["endpoint_match"] = True
        row["unit_or_denominator_match"] = True
        row["context_transport_justified"] = False
        row["fresh_calibration_units_independent_of_p0"] = True
        row["fresh_calibration_units_downstream_confirmatory_ineligible"] = True
        row["biological_rationale"] = (
            "Independent fresh natural-history calibration lower signal bound under the prospectively frozen one-sided bootstrap rule; used only to plan P0 detectability effort."
        )
        row["qualification_status"] = "FRESH_CALIBRATION_QUALIFIED"
        row["frozen_before_p0_outcomes"] = True

    handoff = calibration.get("physical_unit_registry_handoff", {}).get(
        "next_stage_firewall_block"
    )
    _need(isinstance(handoff, dict), "fresh calibration physical-unit firewall handoff missing")
    out["physical_unit_firewall_handoff"] = copy.deepcopy(handoff)

    out["status"] = "CALIBRATION_VALUES_COMPILED_AWAITING_QUALIFICATION_METADATA"
    out["context"]["p0_outcomes_opened"] = False
    out["qualification_metadata"] = {
        "slk_source_commit": "REQUIRED_BEFORE_USE",
        "qualification_commit": "REQUIRED_BEFORE_USE",
        "qualification_timestamp": "REQUIRED_BEFORE_USE",
    }
    out["compiler_claim_ceiling"] = (
        "FRESH_CALIBRATION_VALUES_COMPILED_ONLY; review and commit the qualification payload, then set status=QUALIFICATION_CANDIDATE before running the relevance-source validator."
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile qualified fresh Pedicularis P0 calibration into relevance-source qualification candidate")
    parser.add_argument("calibration_receipt_json", type=Path)
    parser.add_argument("qualification_template_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_qualification(
        json.loads(args.calibration_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.qualification_template_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
