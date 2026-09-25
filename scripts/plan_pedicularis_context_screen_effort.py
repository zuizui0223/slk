from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    from scripts.pedicularis_physical_units import validate_firewall_block
except ImportError:
    from pedicularis_physical_units import validate_firewall_block


SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_FREEZE_V1"
PRODUCTION_STATUS = "PEDICULARIS_CONTEXT_SCREEN_EFFORT_PROSPECTIVELY_FROZEN"
ALLOWED_SOURCE_TYPES = {
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
    "EXTERNAL_MATCHED_PRIMARY_SOURCE",
    "COMBINED_PREDECLARED",
}
EXPECTED_QUALIFICATION = {
    "DOWNSTREAM_DESIGN_REQUIREMENT": "DESIGN_REQUIREMENT_QUALIFIED",
    "INDEPENDENT_NATURAL_HISTORY_CALIBRATION": "FRESH_CALIBRATION_QUALIFIED",
    "EXTERNAL_MATCHED_PRIMARY_SOURCE": "NUMERIC_TRANSPORT_QUALIFIED",
    "COMBINED_PREDECLARED": "COMBINED_PREDECLARED_QUALIFIED",
}
CAPACITY_RULE = "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION"
BASE_CALIBRATION_PLANTS = 84
POLLINATOR_RATE_UNIT = "LEGITIMATE_VISITS_PER_FLOWER_MINUTE"
PERMISSION_RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
PERMISSION_RECEIPT_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
REQUIRED_PERMISSION_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"


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


def poisson_exposure_for_detection(rate_per_exposure: float, desired_probability: float) -> int:
    rate = _positive(rate_per_exposure, "event rate per exposure")
    q = _probability(desired_probability, "desired detection probability")
    return max(1, math.ceil(-math.log(1 - q) / rate))


def binomial_units_for_detection(positive_fraction: float, desired_probability: float) -> int:
    p = _probability(positive_fraction, "positive fraction", allow_one=True)
    q = _probability(desired_probability, "desired detection probability")
    if p == 1:
        return 1
    return max(1, math.ceil(math.log(1 - q) / math.log(1 - p)))


def _qualified_source(
    block: dict,
    *,
    type_key: str,
    status_key: str,
    reference_key: str,
    rationale_key: str,
    label: str,
) -> dict:
    source_type = _filled(block.get(type_key), f"{label} source_type")
    _need(source_type in ALLOWED_SOURCE_TYPES, f"unapproved {label} source type")
    status = _filled(block.get(status_key), f"{label} source qualification status")
    _need(
        status == EXPECTED_QUALIFICATION[source_type],
        f"{label} source is not qualified for numeric use: {source_type}/{status}",
    )
    return {
        "source_type": source_type,
        "qualification_status": status,
        "source_reference": _filled(block.get(reference_key), f"{label} source_reference"),
        "rationale": _filled(block.get(rationale_key), f"{label} rationale"),
    }


def plan(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == SCHEMA, "wrong P0 effort-freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "P0 effort freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong P0 effort production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    _need(ctx.get("frozen_before_screen_outcomes") is True, "P0 effort inputs were not frozen before screen outcomes")

    permission = freeze.get("permission_scope_receipt")
    _need(
        isinstance(permission, dict),
        "P0b effort permission scope receipt missing",
    )
    _need(
        permission.get("schema_version") == PERMISSION_RECEIPT_SCHEMA,
        "wrong P0b effort permission receipt schema",
    )
    _need(
        permission.get("status") == PERMISSION_RECEIPT_STATUS,
        "P0b effort permission scope is not confirmed",
    )
    _need(
        permission.get("candidate_id") == ctx["candidate_id"],
        "P0b effort permission candidate mismatch",
    )
    _need(
        permission.get("required_scope") == REQUIRED_PERMISSION_SCOPE,
        "P0b effort permission scope changed",
    )
    matrix = permission.get("required_activity_matrix")
    validity = permission.get("required_activity_validity")
    _need(
        isinstance(matrix, dict) and set(matrix) == {"A", "B", "C"},
        "P0b effort permission activity matrix changed",
    )
    _need(
        isinstance(validity, dict) and set(validity) == {"A", "B", "C"},
        "P0b effort permission validity inventory changed",
    )
    for activity_id in ("A", "B", "C"):
        cell = matrix[activity_id]
        _need(
            isinstance(cell, dict)
            and cell.get("regulatory") == "PASS"
            and cell.get("site") == "PASS",
            f"P0b effort permission scope not passed for activity {activity_id}",
        )

    policy = freeze.get("source_policy", {})
    allowed = set(policy.get("allowed_relevance_sources", []))
    forbidden = set(policy.get("forbidden_relevance_sources", []))
    _need(ALLOWED_SOURCE_TYPES <= allowed, "registered relevance source classes missing")
    _need(not (allowed & forbidden), "relevance source allow/forbid overlap")
    _need(policy.get("required_qualification_status_by_source_type") == EXPECTED_QUALIFICATION, "source qualification map changed")

    poll = freeze.get("pollinator_detection", {})
    _need(poll.get("visit_rate_unit") == POLLINATOR_RATE_UNIT, "pollinator rate must be visits per flower-minute")
    rate = _positive(
        poll.get("minimum_relevant_visit_rate_per_flower_min"),
        "minimum relevant visit rate per flower-minute",
    )
    poll_q = _probability(poll.get("desired_detection_probability"), "pollinator desired detection probability")
    bouts = _positive_int(poll.get("minimum_temporal_bouts"), "minimum temporal bouts")
    min_minutes_per_bout = _positive(poll.get("minimum_minutes_per_bout"), "minimum minutes per bout")
    rate_source = _qualified_source(
        poll,
        type_key="rate_source_type",
        status_key="rate_source_qualification_status",
        reference_key="rate_source_reference",
        rationale_key="rate_rationale",
        label="pollinator rate",
    )
    coverage_source = _qualified_source(
        poll,
        type_key="coverage_source_type",
        status_key="coverage_source_qualification_status",
        reference_key="coverage_source_reference",
        rationale_key="coverage_rationale",
        label="pollinator coverage",
    )

    pred = freeze.get("predator_detection", {})
    pred_fraction = _probability(
        pred.get("minimum_relevant_attack_fraction"),
        "minimum relevant predator attack fraction",
        allow_one=True,
    )
    pred_q = _probability(pred.get("desired_detection_probability"), "predator desired detection probability")
    pred_source = _qualified_source(
        pred,
        type_key="source_type",
        status_key="source_qualification_status",
        reference_key="source_reference",
        rationale_key="biological_rationale",
        label="predator",
    )

    water = freeze.get("water_state_detection", {})
    water_fraction = _probability(
        water.get("minimum_relevant_positive_fraction"),
        "minimum relevant water-positive fraction",
        allow_one=True,
    )
    water_q = _probability(water.get("desired_detection_probability"), "water-state desired detection probability")
    water_source = _qualified_source(
        water,
        type_key="source_type",
        status_key="source_qualification_status",
        reference_key="source_reference",
        rationale_key="biological_rationale",
        label="water-state",
    )

    fresh_plant_calibration_source_used = any(
        source["source_type"] == "INDEPENDENT_NATURAL_HISTORY_CALIBRATION"
        for source in (pred_source, water_source)
    )
    raw_physical_handoff = freeze.get("physical_unit_firewall_handoff")
    physical_handoff = None
    if fresh_plant_calibration_source_used:
        _need(
            isinstance(raw_physical_handoff, dict),
            "fresh calibration source requires physical-unit firewall handoff",
        )
        physical_handoff = validate_firewall_block(raw_physical_handoff)
    elif raw_physical_handoff is not None:
        physical_handoff = validate_firewall_block(raw_physical_handoff)

    capacity = freeze.get("capacity", {})
    reserve = _positive(capacity.get("reserve_fraction"), "capacity reserve fraction")
    _need(reserve <= 1, "capacity reserve fraction must be <= 1")
    capacity_source = _qualified_source(
        capacity,
        type_key="source_type",
        status_key="source_qualification_status",
        reference_key="source_reference",
        rationale_key="rationale",
        label="capacity",
    )
    _need(capacity.get("census_rule") == CAPACITY_RULE, "capacity census rule changed")

    firewall = freeze.get("firewall", {})
    for key in (
        "minimum_relevant_rates_frozen_before_screen_outcomes",
        "desired_detection_probabilities_frozen_before_screen_outcomes",
        "zero_detection_remains_context_uninformative_not_absence",
        "historical_event_rates_not_copied_without_transport_justification",
        "external_numeric_source_requires_transport_qualification",
        "pollinator_detection_uses_flower_minutes_not_raw_minutes",
        "planner_sets_effort_not_biological_effect_thresholds",
    ):
        _need(firewall.get(key) is True, f"P0 effort firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    poisson_flower_minutes = poisson_exposure_for_detection(rate, poll_q)
    temporal_minutes = math.ceil(bouts * min_minutes_per_bout)
    # Conservative v1 rule: if only one focal flower is open during every valid minute,
    # clock minutes still suffice to reach the flower-minute exposure requirement.
    total_poll_minutes = max(poisson_flower_minutes, temporal_minutes)
    total_poll_flower_minutes = poisson_flower_minutes
    pred_flowers = binomial_units_for_detection(pred_fraction, pred_q)
    water_plants = binomial_units_for_detection(water_fraction, water_q)
    capacity_required = math.ceil(BASE_CALIBRATION_PLANTS * (1 + reserve))

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_EFFORT_PLAN_V1",
        "status": "P0_SIGNAL_DETECTION_EFFORT_PROSPECTIVELY_PLANNED",
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": ctx["candidate_id"],
            "candidate_site_id": ctx["candidate_site_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "screen_window_id": ctx["screen_window_id"],
        },
        "pollinator": {
            "minimum_relevant_visit_rate_per_flower_min": rate,
            "visit_rate_unit": POLLINATOR_RATE_UNIT,
            "desired_detection_probability": poll_q,
            "poisson_detection_flower_minutes": poisson_flower_minutes,
            "minimum_temporal_bouts": bouts,
            "minimum_minutes_per_bout": min_minutes_per_bout,
            "temporal_coverage_minutes": temporal_minutes,
            "planned_total_minutes": total_poll_minutes,
            "planned_total_flower_minutes": total_poll_flower_minutes,
            "minimum_detected_visits_for_signal": 1,
            "rate_source": rate_source,
            "coverage_source": coverage_source,
            "worst_case_exposure_rule": "ASSUME_AT_LEAST_ONE_OPEN_FOCAL_FLOWER_PER_VALID_OBSERVATION_MINUTE",
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
        "permission_scope_receipt": permission,
        "physical_unit_firewall_handoff": (
            {
                "schema_version": "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1",
                "require_nonempty_physical_plant_tag": True,
                "prior_physical_plant_tags_forbidden": sorted(
                    physical_handoff["forbidden_tags"]
                ),
                "prior_tag_source_references": physical_handoff[
                    "source_references"
                ],
                "prior_tag_set_sha256": physical_handoff[
                    "prior_tag_set_sha256"
                ],
                "frozen_before_outcomes": True,
            }
            if physical_handoff is not None
            else None
        ),
        "freeze_provenance": {
            "effort_freeze_commit": metadata["freeze_commit"],
            "slk_source_commit": metadata["slk_source_commit"],
        },
        "interpretation": (
            "Pollinator detection uses flower-minute exposure, matching the published P. rex visitation metric structure. "
            "The v1 clock-time floor is conservatively at least the flower-minute requirement, so one open focal flower throughout valid observation minutes is sufficient to reach registered exposure. "
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
