from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path


QUAL_SCHEMA = "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_V1"
EFFORT_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_V1"


def _load_validator():
    path = Path(__file__).with_name("validate_pedicularis_p0_relevance_qualification.py")
    spec = importlib.util.spec_from_file_location("ped_p0_relevance_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate


validate_qualification = _load_validator()


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _row_map(payload: dict) -> dict[str, dict]:
    return {row["input_id"]: row for row in payload["inputs"]}


def compile_relevance(effort: dict, qualification: dict) -> dict:
    _need(effort.get("schema_version") == EFFORT_SCHEMA, "wrong P0 effort-freeze schema")
    _need(effort.get("status") == "TEMPLATE_ONLY_NOT_FROZEN", "P0 effort candidate must still be an unfrozen template")
    _need(qualification.get("schema_version") == QUAL_SCHEMA, "wrong relevance qualification schema")
    receipt = validate_qualification(qualification)

    ectx = effort.get("context", {})
    qctx = receipt.get("context", {})
    for key in ("system", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _need(ectx.get(key) == qctx.get(key), f"effort/qualification context mismatch: {key}")
    _need(ectx.get("frozen_before_screen_outcomes") is False, "relevance must be compiled before final effort freeze")

    rows = _row_map(qualification)
    poll = rows["P0_POLLINATOR_MIN_RATE"]
    pred = rows["P0_PREDATOR_MIN_PREVALENCE"]
    water = rows["P0_WATER_POSITIVE_PREVALENCE"]

    out = copy.deepcopy(effort)
    poll_block = out.setdefault("pollinator_detection", {})
    poll_block["minimum_relevant_visit_rate_per_flower_min"] = float(poll["numeric_value"])
    poll_block["visit_rate_unit"] = "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"
    poll_block["rate_source_type"] = poll["source_type"]
    poll_block["rate_source_qualification_status"] = poll["qualification_status"]
    poll_block["rate_source_reference"] = poll["source_reference"]
    poll_block["rate_rationale"] = poll["biological_rationale"]

    pred_block = out.setdefault("predator_detection", {})
    pred_block["minimum_relevant_attack_fraction"] = float(pred["numeric_value"])
    pred_block["source_type"] = pred["source_type"]
    pred_block["source_qualification_status"] = pred["qualification_status"]
    pred_block["source_reference"] = pred["source_reference"]
    pred_block["biological_rationale"] = pred["biological_rationale"]

    water_block = out.setdefault("water_state_detection", {})
    water_block["minimum_relevant_positive_fraction"] = float(water["numeric_value"])
    water_block["source_type"] = water["source_type"]
    water_block["source_qualification_status"] = water["qualification_status"]
    water_block["source_reference"] = water["source_reference"]
    water_block["biological_rationale"] = water["biological_rationale"]

    out["status"] = "RELEVANCE_COMPILED_AWAITING_DESIGN_DECISIONS"
    out.setdefault("freeze_metadata", {})["relevance_qualification_reference"] = (
        "SLK_PEDICULARIS_P0_RELEVANCE_QUALIFICATION_RECEIPT_V1@"
        + receipt["qualification_commit"]
    )
    out["context"]["frozen_before_screen_outcomes"] = False
    out["compiler_claim_ceiling"] = (
        "BIOLOGICAL_MINIMUM_RELEVANCE_VALUES_COMPILED_ONLY; detection probabilities, temporal coverage, capacity reserve, final freeze metadata and source-qualified design decisions remain to be frozen before effort planning."
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile qualified Pedicularis P0 minimum-relevance values into the effort-freeze template")
    parser.add_argument("effort_freeze_template_json", type=Path)
    parser.add_argument("relevance_qualification_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_relevance(
        json.loads(args.effort_freeze_template_json.read_text(encoding="utf-8")),
        json.loads(args.relevance_qualification_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
