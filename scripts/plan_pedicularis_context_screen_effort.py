from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_V1"
PRODUCTION_STATUS = "PEDICULARIS_CONTEXT_SCREEN_EFFORT_PROSPECTIVELY_FROZEN"
ALLOWED_SOURCE_TYPES = {
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
    "EXTERNAL_MATCHED_PRIMARY_SOURCE",
    "COMBINED_PREDECLARED",
}
CAPACITY_RULE = "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION"
BASE_CALIBRATION_PLANTS = 84


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _positive(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out) and out > 0, f"{label} must be finite and > 0")
    return out


def _probability(value: object, label: str, *, allow_one: bool = False) -> float:
    out = _positive(value, label)
    upper_ok = out <= 1 if allow_one else out < 1
    _need(upper_ok, f"{label} must be {'<= 1' if allow_one else '< 1'}")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _positive(value, label)
    _need(out.is_integer(), f"{label} must be an integer")
    return int(out)


def poisson_minutes_for_detection(rate_per_min: float, desired_probability: float) -> int:
    rate = _positive(rate_per_min, "visit rate")
    q = _probability(desired_probability, "desired detection probability")
    return max(1, math.ceil(-math.log(1 - q) / rate))


def binomial_units_for_detection(positive_fraction: float, desired_probability: float) -> int:
    p = _probability(positive_fraction, "positive fraction", allow_one=True)
    q = _probability(desired_probability, "desired detection probability")
    if p == 1:
        return 1
    return max(1, math.ceil(math.log(1 - q) / math.log(1 - p)))


def _source(block: dict, prefix: str) -> dict:
    source_type = _filled(block.get(f"{prefix}_source_type"), f"{prefix}_source_type")
    _need(source_type in ALLOWED_SOURCE_TYPES, f"unapproved {prefix} source type")
    return {
        "source_type": source_type,
        "source_reference": _filled(block.get(f"{prefix}_source_reference"), f"{prefix}_source_reference"),
        "rationale": _filled(block.get(f"{prefix}_rationale"), f"{prefix}_rationale"),
    }


def plan(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == SCHEMA, "wrong P0 effort-freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "P0 effort freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong P0 effort production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    _need(ctx.get("frozen_before_screen_outcomes") is True, "P0 effort inputs were not frozen before screen outcomes")

    policy = freeze.get("source_policy", {})
    allowed = set(policy.get("allowed_relevance_sources", []))
    forbidden = set(policy.get("forbidden_relevance_sources", []))
    _need(ALLOWED_SOURCE_TYPES <= allowed, "registered relevance source classes missing")
    _need(not (allowed & forbidden), "relevance source allow/forbid overlap")

    poll = freeze.get("pollinator_detection", {})
    rate = _positive(poll.get("minimum_relevant_visit_rate_per_min"), "minimum relevant visit rate")
    poll_q = _probability(poll.get("desired_detection_probability"), "pollinator desired detection probability")
    bouts = _positive_int(poll.get("minimum_temporal_bouts"), "minimum temporal bouts")
    min_minutes_per_bout = _positive(poll.get("minimum_minutes_per_bout"), "minimum minutes per bout")
    rate_source = _source(poll, "rate")
    coverage_source = _source(poll, "coverage")

    pred = freeze.get("predator_detection", {})
    pred_fraction = _probability(pred.get("minimum_relevant_attack_fraction"), "minimum relevant predator attack fraction", allow_one=True)
    pred_q = _probability(pred.get("desired_detection_probability"), "predator desired detection probability")
    pred_source_type = _filled(pred.get("source_type"), "predator source_type")
    _need(pred_source_type in ALLOWED_SOURCE_TYPES, "unapproved predator source type")
    pred_source = {
        "source_type": pred_source_type,
        "source_reference": _filled(pred.get("source_reference"), "predator source_reference"),
        "rationale": _filled(pred.get("biological_rationale"), "predator biological_rationale"),
    }

    water = freeze.get("water_state_detection", {})
    water_fraction = _probability(water.get("minimum_relevant_positive_fraction"), "minimum relevant water-positive fraction", allow_one=True)
    water_q = _probability(water.get("desired_detection_probability"), "water-state desired detection probability")
    water_source_type = _filled(water.get("source_type"), "water source_type")
    _need(water_source_type in ALLOWED_SOURCE_TYPES, "unapproved water-state source type")
    water_source = {
        "source_type": water_source_type,
        "source_reference": _filled(water.get("source_reference"), "water source_reference"),
        "rationale": _filled(water.get("biological_rationale"), "water biological_rationale"),
    }

    capacity = freeze.get("capacity", {})
    reserve = _positive(capacity.get("reserve_fraction"), "capacity reserve fraction")
    _need(reserve <= 1, "capacity reserve fraction must be <= 1")
    capacity_source_type = _filled(capacity.get("source_type"), "capacity source_type")
    _need(capacity_source_type in ALLOWED_SOURCE_TYPES, "unapproved capacity source type")
    capacity_source = {
        "source_type": capacity_source_type,
        "source_reference": _filled(capacity.get("source_reference"), "capacity source_reference"),
        "rationale": _filled(capacity.get("rationale"), "capacity rationale"),
    }
    _need(capacity.get("census_rule") == CAPACITY_RULE, "capacity census rule changed")

    firewall = freeze.get("firewall", {})
    for key in (
        "minimum_relevant_rates_frozen_before_screen_outcomes",
        "desired_detection_probabilities_frozen_before_screen_outcomes",
        "zero_detection_remains_context_uninformative_not_absence",
        "historical_event_rates_not_copied_without_transport_justification",
        "planner_sets_effort_not_biological_effect_thresholds",
    ):
        _need(firewall.get(key) is True, f"P0 effort firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    poisson_minutes = poisson_minutes_for_detection(rate, poll_q)
    temporal_minutes = math.ceil(bouts * min_minutes_per_bout)
    total_poll_minutes = max(poisson_minutes, temporal_minutes)
    pred_flowers = binomial_units_for_detection(pred_fraction, pred_q)
    water_plants = binomial_units_for_detection(water_fraction, water_q)
    capacity_required = math.ceil(BASE_CALIBRATION_PLANTS * (1 + reserve))

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1",
        "status": "P0_SIGNAL_DETECTION_EFFORT_PROSPECTIVELY_PLANNED",
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": ctx["candidate_site_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "screen_window_id": ctx["screen_window_id"],
        },
        "pollinator": {
            "minimum_relevant_visit_rate_per_min": rate,
            "desired_detection_probability": poll_q,
            "poisson_detection_minutes": poisson_minutes,
            "minimum_temporal_bouts": bouts,
            "minimum_minutes_per_bout": min_minutes_per_bout,
            "temporal_coverage_minutes": temporal_minutes,
            "planned_total_minutes": total_poll_minutes,
            "minimum_detected_visits_for_signal": 1,
            "rate_source": rate_source,
            "coverage_source": coverage_source,
        },
        "predator": {
            "minimum_relevant_attack_fraction": pred_fraction,
            "desired_detection_probability": pred_q,
            "planned_screen_flowers": pred_flowers,
            "minimum_attacked_flowers_for_signal": 1,
            "source": pred_source,
        },
        "water_state": {
            "minimum_relevant_positive_fraction": water_fraction,
            "desired_detection_probability": water_q,
            "planned_screen_plants": water_plants,
            "minimum_positive_plants_for_signal": 1,
            "source": water_source,
        },
        "capacity": {
            "base_calibration_floor": BASE_CALIBRATION_PLANTS,
            "reserve_fraction": reserve,
            "required_flowering_plants": capacity_required,
            "census_rule": CAPACITY_RULE,
            "source": capacity_source,
        },
        "freeze_provenance": {
            "effort_freeze_commit": metadata["freeze_commit"],
            "slk_source_commit": metadata["slk_source_commit"],
        },
        "interpretation": (
            "Effort is chosen so that a signal at or above each frozen minimum-relevance rate has the declared probability of at least one detection. "
            "Failure to detect remains context-uninformative rather than evidence of biological absence."
        ),
        "claim_ceiling": "P0_EFFORT_PLAN_ONLY_NO_CONTEXT_OR_G1_G5_BIOLOGICAL_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan Pedicularis P0 screen effort from prospective minimum-relevance rates")
    parser.add_argument("effort_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = plan(json.loads(args.effort_freeze_json.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
