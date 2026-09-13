from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


SCREEN_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1"
PLAN_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1"
PLAN_STATUS = "P0_SIGNAL_DETECTION_EFFORT_PROSPECTIVELY_PLANNED"
CAPACITY_RULE = "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def compile_effort(screen: dict, plan: dict) -> dict:
    _need(screen.get("schema_version") == SCREEN_SCHEMA, "wrong P0 screen-freeze schema")
    _need(screen.get("status") == "TEMPLATE_ONLY_NOT_FROZEN", "P0 screen candidate must still be an unfrozen template")
    _need(plan.get("schema_version") == PLAN_SCHEMA, "wrong P0 effort-plan schema")
    _need(plan.get("status") == PLAN_STATUS, "P0 effort plan is not ready")

    sctx = screen.get("context", {})
    pctx = plan.get("context", {})
    _need(sctx.get("system") == "Pedicularis rex", "wrong P0 screen system")
    for key in ("candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(sctx.get(key), f"screen.context.{key}")
        _need(sctx.get(key) == pctx.get(key), f"screen/effort-plan context mismatch: {key}")
    _need(sctx.get("frozen_before_screen_outcomes") is False, "effort must be compiled before final P0 freeze")

    poll = plan.get("pollinator", {})
    pred = plan.get("predator", {})
    water = plan.get("water_state", {})
    capacity = plan.get("capacity", {})
    _need(capacity.get("census_rule") == CAPACITY_RULE, "capacity census rule mismatch")
    _need(poll.get("minimum_detected_visits_for_signal") == 1, "v1 pollinator presence threshold must be one detection")
    _need(pred.get("minimum_attacked_flowers_for_signal") == 1, "v1 predator presence threshold must be one detection")
    _need(water.get("minimum_positive_plants_for_signal") == 1, "v1 water-state presence threshold must be one detection")

    out = copy.deepcopy(screen)
    effort = out.setdefault("screen_effort", {})
    effort["capacity_census_rule"] = CAPACITY_RULE
    effort["minimum_pollinator_observation_minutes_total"] = poll["planned_total_minutes"]
    effort["minimum_pollinator_observation_bouts"] = poll["minimum_temporal_bouts"]
    effort["minimum_predator_screen_flowers"] = pred["planned_screen_flowers"]
    effort["minimum_water_state_plants"] = water["planned_screen_plants"]
    effort["minimum_capacity_margin_fraction"] = capacity["reserve_fraction"]

    thresholds = out.setdefault("decision_thresholds", {})
    _need(thresholds.get("minimum_flowering_plants_for_immediate_calibration") == 84, "base calibration floor changed")
    thresholds["minimum_legitimate_pollinator_visits"] = 1
    thresholds["minimum_predator_attacked_flowers"] = 1
    thresholds["minimum_predator_attack_fraction"] = None
    thresholds["minimum_water_positive_plants"] = 1
    thresholds["minimum_water_positive_fraction"] = None

    effort_ref = _filled(plan.get("freeze_provenance", {}).get("effort_freeze_commit"), "effort freeze commit")
    plan_ref = f"SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1@{effort_ref}"

    records = [
        {
            "field_id": "screen_effort.minimum_pollinator_observation_minutes_total",
            "source_type": "COMBINED_PREDECLARED",
            "source_reference": plan_ref,
            "rationale": (
                "Poisson zero-detection planning from the prospectively frozen minimum relevant visit rate and desired detection probability, "
                "not from observed P0 outcomes."
            ),
        },
        {
            "field_id": "screen_effort.minimum_pollinator_observation_bouts",
            "source_type": poll["coverage_source"]["source_type"],
            "source_reference": poll["coverage_source"]["source_reference"],
            "rationale": poll["coverage_source"]["rationale"],
        },
        {
            "field_id": "screen_effort.minimum_predator_screen_flowers",
            "source_type": "COMBINED_PREDECLARED",
            "source_reference": plan_ref,
            "rationale": (
                "Binomial zero-detection planning from the prospectively frozen minimum relevant attack fraction and desired detection probability."
            ),
        },
        {
            "field_id": "screen_effort.minimum_water_state_plants",
            "source_type": "COMBINED_PREDECLARED",
            "source_reference": plan_ref,
            "rationale": (
                "Binomial zero-detection planning from the prospectively frozen minimum relevant water-positive fraction and desired detection probability."
            ),
        },
        {
            "field_id": "screen_effort.minimum_capacity_margin_fraction",
            "source_type": capacity["source"]["source_type"],
            "source_reference": capacity["source"]["source_reference"],
            "rationale": capacity["source"]["rationale"],
        },
        {
            "field_id": "decision_thresholds.minimum_legitimate_pollinator_visits",
            "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "source_reference": plan_ref,
            "rationale": "P0 is a presence/detectability screen; one legitimate visit after completed planned effort is sufficient for the pollinator signal gate.",
        },
        {
            "field_id": "decision_thresholds.minimum_predator_attacked_flowers",
            "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "source_reference": plan_ref,
            "rationale": "P0 is a presence/detectability screen; one attacked flower after completed planned effort is sufficient for the predator signal gate.",
        },
        {
            "field_id": "decision_thresholds.minimum_water_positive_plants",
            "source_type": "DOWNSTREAM_DESIGN_REQUIREMENT",
            "source_reference": plan_ref,
            "rationale": "P0 is a presence/detectability screen; one water-positive plant after completed planned effort is sufficient for the water-state signal gate.",
        },
    ]
    out.setdefault("source_policy", {})["threshold_source_records"] = records
    out.setdefault("freeze_metadata", {})["effort_plan_reference"] = plan_ref
    out["status"] = "EFFORT_COMPILED_AWAITING_FINAL_P0_FREEZE"
    out["context"]["frozen_before_screen_outcomes"] = False
    out["compiler_claim_ceiling"] = (
        "P0_EFFORT_FIELDS_COMPILED_ONLY; review, fill final freeze metadata, commit, set FROZEN_CANDIDATE, and set frozen_before_screen_outcomes=true before field-packet generation."
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile Pedicularis P0 detection-effort plan into the final context-screen freeze")
    parser.add_argument("context_screen_template_json", type=Path)
    parser.add_argument("effort_plan_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_effort(
        json.loads(args.context_screen_template_json.read_text(encoding="utf-8")),
        json.loads(args.effort_plan_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
