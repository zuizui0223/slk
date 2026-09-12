from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


FREEZE_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1"
RECEIPT_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1"
PRODUCTION_STATUS = "PEDICULARIS_CONTEXT_SCREEN_PROSPECTIVELY_FROZEN"
BASE_CALIBRATION_PLANTS = 84
ALLOWED_SOURCE_TYPES = {
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
    "EXTERNAL_MATCHED_PRIMARY_SOURCE",
    "COMBINED_PREDECLARED",
}
REQUIRED_SOURCE_FIELDS = {
    "screen_effort.minimum_independent_flowering_plants_censused",
    "screen_effort.minimum_pollinator_observation_minutes_total",
    "screen_effort.minimum_pollinator_observation_bouts",
    "screen_effort.minimum_predator_screen_flowers",
    "screen_effort.minimum_water_state_plants",
    "screen_effort.minimum_capacity_margin_fraction",
    "decision_thresholds.minimum_legitimate_pollinator_visits",
    "decision_thresholds.minimum_predator_attacked_flowers",
    "decision_thresholds.minimum_water_positive_plants",
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def _finite(value: object, label: str, *, minimum: float | None = None) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    out = float(value)
    _need(math.isfinite(out), f"{label} must be finite")
    if minimum is not None:
        _need(out >= minimum, f"{label} must be >= {minimum}")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _finite(value, label, minimum=1)
    _need(out.is_integer(), f"{label} must be an integer")
    return int(out)


def _optional_fraction(value: object, label: str) -> float | None:
    if value is None:
        return None
    out = _finite(value, label, minimum=0)
    _need(out <= 1, f"{label} must be <= 1")
    return out


def validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong context-screen freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "context-screen freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong context-screen production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    _need(ctx.get("frozen_before_screen_outcomes") is True, "context screen was not frozen before outcomes")

    effort = freeze.get("screen_effort", {})
    min_census = _positive_int(effort.get("minimum_independent_flowering_plants_censused"), "minimum flowering plants censused")
    min_poll_minutes = _finite(effort.get("minimum_pollinator_observation_minutes_total"), "minimum pollinator minutes", minimum=0.000001)
    min_poll_bouts = _positive_int(effort.get("minimum_pollinator_observation_bouts"), "minimum pollinator bouts")
    min_pred_flowers = _positive_int(effort.get("minimum_predator_screen_flowers"), "minimum predator screen flowers")
    min_water_plants = _positive_int(effort.get("minimum_water_state_plants"), "minimum water-state plants")
    capacity_margin = _finite(effort.get("minimum_capacity_margin_fraction"), "minimum capacity margin fraction", minimum=0)
    _need(capacity_margin <= 1, "minimum capacity margin fraction must be <= 1")

    thresholds = freeze.get("decision_thresholds", {})
    min_poll_visits = _positive_int(thresholds.get("minimum_legitimate_pollinator_visits"), "minimum legitimate pollinator visits")
    min_pred_attacked = _positive_int(thresholds.get("minimum_predator_attacked_flowers"), "minimum predator-attacked flowers")
    min_pred_frac = _optional_fraction(thresholds.get("minimum_predator_attack_fraction"), "minimum predator attack fraction")
    min_water_positive = _positive_int(thresholds.get("minimum_water_positive_plants"), "minimum water-positive plants")
    min_water_frac = _optional_fraction(thresholds.get("minimum_water_positive_fraction"), "minimum water-positive fraction")
    _need(
        thresholds.get("minimum_flowering_plants_for_immediate_calibration") == BASE_CALIBRATION_PLANTS,
        "v1 immediate calibration floor must remain 84 plants",
    )
    _need(
        thresholds.get("calibration_capacity_basis") == "Y_CAL_36_PLUS_D0_CAL_48_DISJOINT_PLANTS",
        "calibration capacity basis changed",
    )
    _need(
        thresholds.get("pollen_limitation_screen_rule") == "CALIBRATION_REQUIRED_NOT_ZERO_INFERENCE",
        "pollen-limitation screen rule changed",
    )
    _need(thresholds.get("pollen_limitation_screen_threshold") is None, "P0 must not invent a pollen-limitation threshold")

    source_policy = freeze.get("source_policy", {})
    allowed = set(source_policy.get("allowed_threshold_sources", []))
    forbidden = set(source_policy.get("forbidden_threshold_sources", []))
    _need(ALLOWED_SOURCE_TYPES <= allowed, "registered allowed threshold sources missing")
    _need(not (allowed & forbidden), "threshold source allow/forbid overlap")
    records = source_policy.get("threshold_source_records", [])
    _need(isinstance(records, list), "threshold_source_records must be a list")
    source_fields = set()
    for row in records:
        field_id = _filled(row.get("field_id"), "threshold source field_id")
        source_type = _filled(row.get("source_type"), f"source_type for {field_id}")
        _need(source_type in ALLOWED_SOURCE_TYPES, f"unapproved threshold source: {field_id}")
        _filled(row.get("source_reference"), f"source_reference for {field_id}")
        _filled(row.get("rationale"), f"rationale for {field_id}")
        source_fields.add(field_id)
    _need(REQUIRED_SOURCE_FIELDS <= source_fields, "not every required P0 threshold/effort field has provenance")

    firewall = freeze.get("firewall", {})
    for key in (
        "context_screen_is_not_g1_or_g2_evidence",
        "low_signal_context_is_not_biological_absence",
        "screen_units_confirmatory_ineligible",
        "no_treatment_effect_estimation_from_screen",
        "thresholds_frozen_before_screen_outcomes",
        "failed_signal_context_may_trigger_relocation_without_negative_claim",
    ):
        _need(firewall.get(key) is True, f"context-screen firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    capacity_required = math.ceil(BASE_CALIBRATION_PLANTS * (1 + capacity_margin))
    return {
        "context": ctx,
        "effort": {
            "minimum_independent_flowering_plants_censused": min_census,
            "minimum_pollinator_observation_minutes_total": min_poll_minutes,
            "minimum_pollinator_observation_bouts": min_poll_bouts,
            "minimum_predator_screen_flowers": min_pred_flowers,
            "minimum_water_state_plants": min_water_plants,
        },
        "thresholds": {
            "minimum_legitimate_pollinator_visits": min_poll_visits,
            "minimum_predator_attacked_flowers": min_pred_attacked,
            "minimum_predator_attack_fraction": min_pred_frac,
            "minimum_water_positive_plants": min_water_positive,
            "minimum_water_positive_fraction": min_water_frac,
            "minimum_flowering_plants_for_calibration_with_reserve": capacity_required,
        },
        "capacity_margin_fraction": capacity_margin,
    }


def adjudicate(receipt: dict, freeze: dict) -> dict:
    cfg = validate_freeze(freeze)
    _need(receipt.get("schema_version") == RECEIPT_SCHEMA, "wrong context-screen receipt schema")

    rctx = receipt.get("context", {})
    fctx = cfg["context"]
    for key in ("system", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _need(rctx.get(key) == fctx.get(key), f"receipt/freeze context mismatch: {key}")

    firewall = receipt.get("firewall", {})
    _need(firewall.get("screen_units_confirmatory_eligible") is False, "screen units cannot be confirmatory eligible")
    _need(firewall.get("screen_used_for_treatment_effect_estimation") is False, "P0 cannot estimate treatment effects")
    _need(firewall.get("zero_detection_interpreted_as_biological_absence") is False, "zero detection cannot mean biological absence")

    pollen = receipt.get("pollen_limitation", {})
    _need(pollen.get("status") == "UNRESOLVED_UNTIL_QP_CALIBRATION", "P0 pollen limitation must remain unresolved")
    _need(pollen.get("used_as_context_screen_pass_gate") is False, "pollen limitation cannot be a P0 pass gate")

    effort_raw = receipt.get("effort", {})
    obs = receipt.get("observations", {})
    census = _finite(effort_raw.get("independent_flowering_plants_censused"), "observed flowering plants", minimum=0)
    poll_minutes = _finite(effort_raw.get("pollinator_observation_minutes_total"), "observed pollinator minutes", minimum=0)
    poll_bouts = _finite(effort_raw.get("pollinator_observation_bouts"), "observed pollinator bouts", minimum=0)
    pred_flowers = _finite(effort_raw.get("predator_screen_flowers"), "observed predator flowers", minimum=0)
    water_plants = _finite(effort_raw.get("water_state_plants"), "observed water-state plants", minimum=0)

    visits = _finite(obs.get("legitimate_pollinator_visits"), "legitimate pollinator visits", minimum=0)
    attacked = _finite(obs.get("predator_attacked_flowers"), "predator-attacked flowers", minimum=0)
    water_positive = _finite(obs.get("water_positive_plants"), "water-positive plants", minimum=0)
    _need(attacked <= pred_flowers, "predator-attacked flowers cannot exceed screened flowers")
    _need(water_positive <= water_plants, "water-positive plants cannot exceed screened plants")
    _filled(obs.get("notes_on_predator_evidence"), "notes_on_predator_evidence")
    _filled(obs.get("notes_on_water_state"), "notes_on_water_state")

    ef = cfg["effort"]
    effort_checks = {
        "flowering_census": census >= ef["minimum_independent_flowering_plants_censused"],
        "pollinator_minutes": poll_minutes >= ef["minimum_pollinator_observation_minutes_total"],
        "pollinator_bouts": poll_bouts >= ef["minimum_pollinator_observation_bouts"],
        "predator_flowers": pred_flowers >= ef["minimum_predator_screen_flowers"],
        "water_plants": water_plants >= ef["minimum_water_state_plants"],
    }
    effort_complete = all(effort_checks.values())

    pred_fraction = attacked / pred_flowers if pred_flowers > 0 else None
    water_fraction = water_positive / water_plants if water_plants > 0 else None
    th = cfg["thresholds"]

    pollinator_pass = visits >= th["minimum_legitimate_pollinator_visits"]
    predator_pass = attacked >= th["minimum_predator_attacked_flowers"]
    if th["minimum_predator_attack_fraction"] is not None:
        predator_pass = predator_pass and pred_fraction is not None and pred_fraction >= th["minimum_predator_attack_fraction"]
    water_pass = water_positive >= th["minimum_water_positive_plants"]
    if th["minimum_water_positive_fraction"] is not None:
        water_pass = water_pass and water_fraction is not None and water_fraction >= th["minimum_water_positive_fraction"]

    capacity_required = th["minimum_flowering_plants_for_calibration_with_reserve"]
    capacity_pass = census >= capacity_required

    if not effort_complete:
        status = "CONTEXT_SCREEN_INCOMPLETE"
    else:
        failed = [
            name
            for name, passed in (
                ("POLLINATOR", pollinator_pass),
                ("PREDATOR", predator_pass),
                ("WATER_STATE", water_pass),
            )
            if not passed
        ]
        if len(failed) > 1:
            status = "CONTEXT_UNINFORMATIVE_MULTIPLE_SIGNALS"
        elif failed == ["POLLINATOR"]:
            status = "CONTEXT_UNINFORMATIVE_POLLINATOR_LOW"
        elif failed == ["PREDATOR"]:
            status = "CONTEXT_UNINFORMATIVE_PREDATOR_LOW"
        elif failed == ["WATER_STATE"]:
            status = "CONTEXT_UNINFORMATIVE_WATER_STATE"
        elif not capacity_pass:
            status = "CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED"
        else:
            status = "CONTEXT_SCREEN_PASS_CALIBRATION_READY"

    calibration_unlocked = status == "CONTEXT_SCREEN_PASS_CALIBRATION_READY"
    relocation_recommended = status.startswith("CONTEXT_UNINFORMATIVE_")

    return {
        "schema_version": "SLK_PEDICULARIS_CONTEXT_SCREEN_ADJUDICATION_V1",
        "status": status,
        "context": {
            "system": "Pedicularis rex",
            "candidate_site_id": fctx["candidate_site_id"],
            "population_id": fctx["population_id"],
            "season_id": fctx["season_id"],
            "screen_window_id": fctx["screen_window_id"],
        },
        "effort": {
            "complete": effort_complete,
            "checks": effort_checks,
        },
        "signals": {
            "pollinator": {
                "pass": pollinator_pass if effort_complete else None,
                "legitimate_visits": visits,
            },
            "predator": {
                "pass": predator_pass if effort_complete else None,
                "attacked_flowers": attacked,
                "screened_flowers": pred_flowers,
                "attack_fraction": pred_fraction,
            },
            "water_state": {
                "pass": water_pass if effort_complete else None,
                "positive_plants": water_positive,
                "screened_plants": water_plants,
                "positive_fraction": water_fraction,
            },
            "pollen_limitation": "UNRESOLVED_UNTIL_QP_CALIBRATION",
        },
        "capacity": {
            "observed_flowering_plants": census,
            "base_calibration_floor": BASE_CALIBRATION_PLANTS,
            "reserve_fraction": cfg["capacity_margin_fraction"],
            "required_with_reserve": capacity_required,
            "pass": capacity_pass if effort_complete else None,
        },
        "next_action": {
            "calibration_unlocked": calibration_unlocked,
            "relocation_recommended": relocation_recommended,
            "low_signal_is_biological_negative": False,
        },
        "firewall": {
            "screen_is_logistical_not_g1_g2": True,
            "screen_units_confirmatory_ineligible": True,
            "zero_detection_not_absence": True,
        },
        "claim_ceiling": "P0_CONTEXT_LOGISTICS_ONLY_NO_G1_G2_OR_DOWNSTREAM_BIOLOGICAL_RESULT",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate a prospective Pedicularis population/season context screen")
    parser.add_argument("screen_receipt_json", type=Path)
    parser.add_argument("screen_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = adjudicate(
        json.loads(args.screen_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.screen_freeze_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
