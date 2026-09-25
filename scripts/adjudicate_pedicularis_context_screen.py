from __future__ import annotations

import argparse
import json
import math
from datetime import date
from pathlib import Path

try:
    from scripts.pedicularis_physical_units import (
        FIREWALL_SCHEMA,
        canonical_tag_hash,
        validate_firewall_block,
    )
except ImportError:
    from pedicularis_physical_units import (
        FIREWALL_SCHEMA,
        canonical_tag_hash,
        validate_firewall_block,
    )


FREEZE_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_FREEZE_V1"
RECEIPT_SCHEMA = "SLK_PEDICULARIS_CONTEXT_SCREEN_RECEIPT_V1"
PRODUCTION_STATUS = "PEDICULARIS_CONTEXT_SCREEN_PROSPECTIVELY_FROZEN"
BASE_CALIBRATION_PLANTS = 84
CAPACITY_CENSUS_RULE = "STOP_AT_REQUIRED_CAPACITY_OR_EXHAUST_FOCAL_POPULATION"
PERMISSION_RECEIPT_SCHEMA = "SLK_PEDICULARIS_WAVE1_PERMISSION_SCOPE_RECEIPT_V1"
PERMISSION_RECEIPT_STATUS = "RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED"
REQUIRED_PERMISSION_SCOPE = "RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE"
ALLOWED_SOURCE_TYPES = {
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "INDEPENDENT_NATURAL_HISTORY_CALIBRATION",
    "EXTERNAL_MATCHED_PRIMARY_SOURCE",
    "COMBINED_PREDECLARED",
}
REQUIRED_SOURCE_FIELDS = {
    "screen_effort.minimum_pollinator_observation_minutes_total",
    "screen_effort.minimum_pollinator_flower_minutes_total",
    "screen_effort.minimum_pollinator_observation_bouts",
    "screen_effort.minimum_pollinator_minutes_per_bout",
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


def _iso_date(value: object, label: str) -> date:
    text = _filled(value, label)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO YYYY-MM-DD") from exc


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


def _nonnegative_int(value: object, label: str) -> int:
    out = _finite(value, label, minimum=0)
    _need(out.is_integer(), f"{label} must be an integer")
    return int(out)


def _optional_fraction(value: object, label: str) -> float | None:
    if value is None:
        return None
    out = _finite(value, label, minimum=0)
    _need(out <= 1, f"{label} must be <= 1")
    return out


def _optional_bool(value: object, label: str) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text == "":
        return None
    _need(text in {"true", "false", "1", "0", "yes", "no"}, f"{label} must be boolean-like")
    return text in {"true", "1", "yes"}


def validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong context-screen freeze schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "context-screen freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong context-screen production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    planned_start = _iso_date(
        ctx.get("planned_screen_start_date"),
        "context.planned_screen_start_date",
    )
    planned_end = _iso_date(
        ctx.get("planned_screen_end_date"),
        "context.planned_screen_end_date",
    )
    _need(planned_start <= planned_end, "planned P0b screen interval reversed")
    _need(ctx.get("frozen_before_screen_outcomes") is True, "context screen was not frozen before outcomes")

    permission = freeze.get("permission_scope_receipt")
    _need(
        isinstance(permission, dict),
        "P0b permission scope receipt missing",
    )
    _need(
        permission.get("schema_version") == PERMISSION_RECEIPT_SCHEMA,
        "wrong P0b permission scope receipt schema",
    )
    _need(
        permission.get("status") == PERMISSION_RECEIPT_STATUS,
        "P0b permission scope is not confirmed",
    )
    _need(
        permission.get("candidate_id") == ctx["candidate_id"],
        "P0b permission scope receipt candidate mismatch",
    )
    _need(
        permission.get("required_scope") == REQUIRED_PERMISSION_SCOPE,
        "P0b permission scope changed",
    )
    permission_matrix = permission.get("required_activity_matrix")
    permission_validity = permission.get("required_activity_validity")
    _need(
        isinstance(permission_matrix, dict)
        and set(permission_matrix) == {"A", "B", "C"},
        "P0b permission activity matrix changed",
    )
    _need(
        isinstance(permission_validity, dict)
        and set(permission_validity) == {"A", "B", "C"},
        "P0b permission validity inventory changed",
    )
    for activity_id in ("A", "B", "C"):
        cell = permission_matrix[activity_id]
        _need(
            isinstance(cell, dict)
            and cell.get("regulatory") == "PASS"
            and cell.get("site") == "PASS",
            f"P0b permission scope not passed for activity {activity_id}",
        )
        validity_cell = permission_validity[activity_id]
        _need(
            isinstance(validity_cell, dict)
            and set(validity_cell) == {"regulatory", "site"},
            f"P0b permission validity cell changed: {activity_id}",
        )
        for side in ("regulatory", "site"):
            intervals = validity_cell[side]
            _need(
                isinstance(intervals, list) and intervals,
                f"P0b permission validity missing: {activity_id}/{side}",
            )
            covers_window = False
            for index, interval in enumerate(intervals):
                _need(
                    isinstance(interval, dict),
                    f"P0b permission interval must be object: {activity_id}/{side}/{index}",
                )
                valid_from = _iso_date(
                    interval.get("valid_from"),
                    f"P0b permission valid_from/{activity_id}/{side}/{index}",
                )
                valid_through = _iso_date(
                    interval.get("valid_through"),
                    f"P0b permission valid_through/{activity_id}/{side}/{index}",
                )
                _need(
                    valid_from <= valid_through,
                    f"P0b permission interval reversed: {activity_id}/{side}/{index}",
                )
                if valid_from <= planned_start and planned_end <= valid_through:
                    covers_window = True
            _need(
                covers_window,
                f"P0b planned screen interval outside permission validity: {activity_id}/{side}",
            )

    effort = freeze.get("screen_effort", {})
    _need(effort.get("capacity_census_rule") == CAPACITY_CENSUS_RULE, "capacity census rule changed")
    min_poll_minutes = _finite(
        effort.get("minimum_pollinator_observation_minutes_total"),
        "minimum pollinator minutes",
        minimum=0.000001,
    )
    min_poll_flower_minutes = _finite(
        effort.get("minimum_pollinator_flower_minutes_total"),
        "minimum pollinator flower-minutes",
        minimum=0.000001,
    )
    min_poll_bouts = _positive_int(
        effort.get("minimum_pollinator_observation_bouts"),
        "minimum pollinator bouts",
    )
    min_poll_minutes_per_bout = _finite(
        effort.get("minimum_pollinator_minutes_per_bout"),
        "minimum pollinator minutes per bout",
        minimum=0.000001,
    )
    _need(
        min_poll_minutes
        >= min_poll_bouts * min_poll_minutes_per_bout,
        "total pollinator minutes are inconsistent with the frozen per-bout minimum",
    )
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
        "capacity_shortfall_requires_exhaustive_census",
        "pollinator_detection_requires_flower_minute_exposure",
    ):
        _need(firewall.get(key) is True, f"context-screen firewall disabled: {key}")

    physical_firewall = validate_firewall_block(
        freeze.get("physical_unit_firewall", {})
    )

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    capacity_required = math.ceil(BASE_CALIBRATION_PLANTS * (1 + capacity_margin))
    return {
        "context": ctx,
        "effort": {
            "capacity_census_rule": CAPACITY_CENSUS_RULE,
            "minimum_pollinator_observation_minutes_total": min_poll_minutes,
            "minimum_pollinator_flower_minutes_total": min_poll_flower_minutes,
            "minimum_pollinator_observation_bouts": min_poll_bouts,
            "minimum_pollinator_minutes_per_bout": min_poll_minutes_per_bout,
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
        "permission_scope_receipt": permission,
        "planned_screen_start_date": planned_start.isoformat(),
        "planned_screen_end_date": planned_end.isoformat(),
        "physical_unit_firewall": physical_firewall,
        "freeze_commit": metadata["freeze_commit"],
    }


def adjudicate(receipt: dict, freeze: dict) -> dict:
    cfg = validate_freeze(freeze)
    _need(receipt.get("schema_version") == RECEIPT_SCHEMA, "wrong context-screen receipt schema")
    _need(
        receipt.get("status") == "FILLED_SCREEN_DATA",
        "context-screen receipt is not filled screen data",
    )

    rctx = receipt.get("context", {})
    fctx = cfg["context"]
    for key in ("system", "candidate_id", "candidate_site_id", "population_id", "season_id", "screen_window_id"):
        _need(rctx.get(key) == fctx.get(key), f"receipt/freeze context mismatch: {key}")

    timing = receipt.get("field_timing_audit")
    _need(isinstance(timing, dict), "P0b field timing audit missing")
    capacity_census_dated = timing.get("capacity_census_dated") is True
    observed_min = _iso_date(
        timing.get("observed_date_min"),
        "P0b observed_date_min",
    )
    observed_max = _iso_date(
        timing.get("observed_date_max"),
        "P0b observed_date_max",
    )
    _need(observed_min <= observed_max, "P0b observed date range reversed")
    planned_start = date.fromisoformat(cfg["planned_screen_start_date"])
    planned_end = date.fromisoformat(cfg["planned_screen_end_date"])
    _need(
        planned_start <= observed_min and observed_max <= planned_end,
        "P0b completed observations outside planned screen interval",
    )

    physical_audit = receipt.get("physical_unit_audit", {})
    _need(
        physical_audit.get("status") == "P0_SCREEN_PLANT_TAGS_VALIDATED",
        "P0 screen physical-unit audit missing",
    )
    current_tags_raw = physical_audit.get("current_physical_plant_tags")
    _need(
        isinstance(current_tags_raw, list) and current_tags_raw,
        "P0 screen physical tags missing",
    )
    current_tags = [str(x).strip() for x in current_tags_raw]
    _need(
        all(current_tags) and len(current_tags) == len(set(current_tags)),
        "P0 screen physical tags must be non-empty and unique",
    )
    _need(
        physical_audit.get("current_physical_plant_count") == len(current_tags),
        "P0 screen physical tag count mismatch",
    )
    current_hash = canonical_tag_hash(current_tags)
    _need(
        physical_audit.get("current_tag_set_sha256") == current_hash,
        "P0 screen physical tag hash mismatch",
    )
    prior_physical = cfg["physical_unit_firewall"]
    overlap = sorted(set(current_tags) & prior_physical["forbidden_tags"])
    _need(
        not overlap,
        "P0 screen reuses prior calibration physical plants: "
        + ",".join(overlap),
    )
    combined_tags = sorted(prior_physical["forbidden_tags"] | set(current_tags))
    next_physical_firewall = {
        "schema_version": FIREWALL_SCHEMA,
        "require_nonempty_physical_plant_tag": True,
        "prior_physical_plant_tags_forbidden": combined_tags,
        "prior_tag_source_references": (
            list(prior_physical["source_references"])
            + [f"PED_P0_CONTEXT_SCREEN@{cfg['freeze_commit']}"]
        ),
        "prior_tag_set_sha256": canonical_tag_hash(combined_tags),
        "frozen_before_outcomes": True,
    }

    firewall = receipt.get("firewall", {})
    _need(firewall.get("screen_units_confirmatory_eligible") is False, "screen units cannot be confirmatory eligible")
    _need(firewall.get("screen_used_for_treatment_effect_estimation") is False, "P0 cannot estimate treatment effects")
    _need(firewall.get("zero_detection_interpreted_as_biological_absence") is False, "zero detection cannot mean biological absence")
    _need(
        firewall.get("pollinator_exposure_unit") == "FLOWER_MINUTES",
        "pollinator exposure unit must remain FLOWER_MINUTES",
    )

    packet_completion = receipt.get("packet_completion")
    _need(
        isinstance(packet_completion, dict),
        "packet_completion must be an object",
    )

    pollen = receipt.get("pollen_limitation", {})
    _need(pollen.get("status") == "UNRESOLVED_UNTIL_QP_CALIBRATION", "P0 pollen limitation must remain unresolved")
    _need(pollen.get("used_as_context_screen_pass_gate") is False, "pollen limitation cannot be a P0 pass gate")

    effort_raw = receipt.get("effort", {})
    obs = receipt.get("observations", {})
    census = _nonnegative_int(
        effort_raw.get("independent_flowering_plants_censused"),
        "observed flowering plants",
    )
    census_exhausted = _optional_bool(effort_raw.get("population_census_exhausted"), "population_census_exhausted")
    poll_minutes = _finite(effort_raw.get("pollinator_observation_minutes_total"), "observed pollinator minutes", minimum=0)
    poll_flower_minutes = _finite(effort_raw.get("pollinator_flower_minutes_total"), "observed pollinator flower-minutes", minimum=0)
    poll_bouts = _nonnegative_int(
        effort_raw.get("pollinator_observation_bouts"),
        "observed pollinator bouts",
    )
    pred_flowers = _nonnegative_int(
        effort_raw.get("predator_screen_flowers"),
        "observed predator flowers",
    )
    water_plants = _nonnegative_int(
        effort_raw.get("water_state_plants"),
        "observed water-state plants",
    )

    visits = _nonnegative_int(
        obs.get("legitimate_pollinator_visits"),
        "legitimate pollinator visits",
    )
    attacked = _nonnegative_int(
        obs.get("predator_attacked_flowers"),
        "predator-attacked flowers",
    )
    water_positive = _nonnegative_int(
        obs.get("water_positive_plants"),
        "water-positive plants",
    )
    _need(attacked <= pred_flowers, "predator-attacked flowers cannot exceed screened flowers")
    _need(water_positive <= water_plants, "water-positive plants cannot exceed screened plants")
    _filled(obs.get("notes_on_predator_evidence"), "notes_on_predator_evidence")
    _filled(obs.get("notes_on_water_state"), "notes_on_water_state")

    registered_poll = _nonnegative_int(
        packet_completion.get("registered_pollinator_rows"),
        "registered pollinator rows",
    )
    completed_poll = _nonnegative_int(
        packet_completion.get("completed_pollinator_rows"),
        "completed pollinator rows",
    )
    registered_pred = _nonnegative_int(
        packet_completion.get("registered_predator_rows"),
        "registered predator rows",
    )
    completed_pred = _nonnegative_int(
        packet_completion.get("completed_predator_rows"),
        "completed predator rows",
    )
    registered_water = _nonnegative_int(
        packet_completion.get("registered_water_rows"),
        "registered water rows",
    )
    completed_water = _nonnegative_int(
        packet_completion.get("completed_water_rows"),
        "completed water rows",
    )
    _need(
        completed_poll == poll_bouts,
        "pollinator packet completion disagrees with effort count",
    )
    _need(
        completed_pred == pred_flowers,
        "predator packet completion disagrees with effort count",
    )
    _need(
        completed_water == water_plants,
        "water packet completion disagrees with effort count",
    )

    bout_details = effort_raw.get("pollinator_bout_details")
    _need(
        isinstance(bout_details, list)
        and len(bout_details) == poll_bouts,
        "pollinator bout detail count mismatch",
    )
    bout_ids: set[str] = set()
    valid_duration_bouts = 0
    detail_total_minutes = 0.0
    detail_total_flower_minutes = 0.0
    detail_total_visits = 0
    for detail in bout_details:
        _need(isinstance(detail, dict), "pollinator bout detail must be object")
        record_id = _filled(
            detail.get("record_id"),
            "pollinator bout record_id",
        )
        _need(record_id not in bout_ids, "duplicate pollinator bout detail")
        bout_ids.add(record_id)
        observed_minutes = _finite(
            detail.get("observed_minutes"),
            f"observed minutes/{record_id}",
            minimum=0.000001,
        )
        open_flowers = _positive_int(
            detail.get("simultaneously_open_focal_flowers"),
            f"open focal flowers/{record_id}",
        )
        bout_visits = _nonnegative_int(
            detail.get("legitimate_visits"),
            f"legitimate visits/{record_id}",
        )
        if (
            observed_minutes
            >= cfg["effort"]["minimum_pollinator_minutes_per_bout"]
        ):
            valid_duration_bouts += 1
        detail_total_minutes += observed_minutes
        detail_total_flower_minutes += observed_minutes * open_flowers
        detail_total_visits += bout_visits

    _need(
        math.isclose(
            detail_total_minutes,
            poll_minutes,
            rel_tol=1e-10,
            abs_tol=1e-10,
        ),
        "pollinator bout-detail minutes disagree with aggregate effort",
    )
    _need(
        math.isclose(
            detail_total_flower_minutes,
            poll_flower_minutes,
            rel_tol=1e-10,
            abs_tol=1e-10,
        ),
        "pollinator bout-detail flower-minutes disagree with aggregate effort",
    )
    _need(
        detail_total_visits == visits,
        "pollinator bout-detail visits disagree with aggregate observation",
    )

    ef = cfg["effort"]
    signal_effort_checks = {
        "pollinator_minutes": poll_minutes >= ef["minimum_pollinator_observation_minutes_total"],
        "pollinator_flower_minutes": poll_flower_minutes >= ef["minimum_pollinator_flower_minutes_total"],
        "pollinator_bouts": poll_bouts >= ef["minimum_pollinator_observation_bouts"],
        "pollinator_bout_duration": (
            valid_duration_bouts >= ef["minimum_pollinator_observation_bouts"]
        ),
        "registered_pollinator_rows": (
            registered_poll >= ef["minimum_pollinator_observation_bouts"]
        ),
        "predator_flowers": pred_flowers >= ef["minimum_predator_screen_flowers"],
        "registered_predator_rows": (
            registered_pred >= ef["minimum_predator_screen_flowers"]
        ),
        "water_plants": water_plants >= ef["minimum_water_state_plants"],
        "registered_water_rows": (
            registered_water >= ef["minimum_water_state_plants"]
        ),
    }
    signal_effort_complete = all(signal_effort_checks.values())

    pred_fraction = attacked / pred_flowers if pred_flowers > 0 else None
    water_fraction = water_positive / water_plants if water_plants > 0 else None
    poll_rate = visits / poll_flower_minutes if poll_flower_minutes > 0 else None
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
    capacity_count_resolved = capacity_pass or census_exhausted is True
    capacity_resolved = capacity_count_resolved and capacity_census_dated

    effort_checks = {
        **signal_effort_checks,
        "capacity_census_resolved": capacity_resolved,
        "capacity_census_dated": capacity_census_dated,
    }
    effort_complete = signal_effort_complete and capacity_resolved

    failed = []
    if signal_effort_complete:
        failed = [
            name
            for name, passed in (
                ("POLLINATOR", pollinator_pass),
                ("PREDATOR", predator_pass),
                ("WATER_STATE", water_pass),
            )
            if not passed
        ]

    if not signal_effort_complete:
        status = "CONTEXT_SCREEN_INCOMPLETE"
    elif len(failed) > 1:
        status = "CONTEXT_UNINFORMATIVE_MULTIPLE_SIGNALS"
    elif failed == ["POLLINATOR"]:
        status = "CONTEXT_UNINFORMATIVE_POLLINATOR_LOW"
    elif failed == ["PREDATOR"]:
        status = "CONTEXT_UNINFORMATIVE_PREDATOR_LOW"
    elif failed == ["WATER_STATE"]:
        status = "CONTEXT_UNINFORMATIVE_WATER_STATE"
    elif not capacity_resolved:
        status = "CONTEXT_SCREEN_INCOMPLETE"
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
            "candidate_id": fctx["candidate_id"],
            "candidate_site_id": fctx["candidate_site_id"],
            "population_id": fctx["population_id"],
            "season_id": fctx["season_id"],
            "screen_window_id": fctx["screen_window_id"],
        },
        "permission_scope_audit": {
            "status": "P0B_PERMISSION_VALIDITY_CONFIRMED_FOR_PLANNED_AND_OBSERVED_WINDOW",
            "required_scope": cfg["permission_scope_receipt"]["required_scope"],
            "planned_screen_start_date": cfg["planned_screen_start_date"],
            "planned_screen_end_date": cfg["planned_screen_end_date"],
            "observed_date_min": observed_min.isoformat(),
            "observed_date_max": observed_max.isoformat(),
            "planned_window_fully_covered": True,
            "completed_observations_within_planned_window": True,
        },
        "physical_unit_firewall": {
            "status": "P0_SCREEN_PHYSICAL_TAGS_DISJOINT_FROM_PRIOR",
            "prior_forbidden_tag_count": len(
                prior_physical["forbidden_tags"]
            ),
            "current_physical_plant_count": len(current_tags),
            "current_tag_set_sha256": current_hash,
            "overlap_count": 0,
            "next_stage_firewall_block": next_physical_firewall,
        },
        "effort": {
            "complete": effort_complete,
            "signal_effort_complete": signal_effort_complete,
            "checks": effort_checks,
        },
        "signals": {
            "pollinator": {
                "pass": pollinator_pass if signal_effort_complete else None,
                "legitimate_visits": visits,
                "flower_minutes": poll_flower_minutes,
                "observed_visit_rate_per_flower_min": poll_rate,
                "completed_bouts": poll_bouts,
                "bouts_meeting_minimum_duration": valid_duration_bouts,
                "minimum_minutes_per_bout": ef[
                    "minimum_pollinator_minutes_per_bout"
                ],
            },
            "predator": {
                "pass": predator_pass if signal_effort_complete else None,
                "attacked_flowers": attacked,
                "screened_flowers": pred_flowers,
                "attack_fraction": pred_fraction,
            },
            "water_state": {
                "pass": water_pass if signal_effort_complete else None,
                "positive_plants": water_positive,
                "screened_plants": water_plants,
                "positive_fraction": water_fraction,
            },
            "pollen_limitation": "UNRESOLVED_UNTIL_QP_CALIBRATION",
        },
        "capacity": {
            "census_rule": CAPACITY_CENSUS_RULE,
            "observed_flowering_plants": census,
            "population_census_exhausted": census_exhausted,
            "base_calibration_floor": BASE_CALIBRATION_PLANTS,
            "reserve_fraction": cfg["capacity_margin_fraction"],
            "required_with_reserve": capacity_required,
            "resolved": capacity_resolved,
            "pass": capacity_pass if capacity_resolved else None,
        },
        "next_action": {
            "calibration_unlocked": calibration_unlocked,
            "relocation_recommended": relocation_recommended,
            "low_signal_is_biological_negative": False,
            "continue_capacity_census": (
                signal_effort_complete
                and not failed
                and not capacity_count_resolved
            ),
        },
        "packet_completion_audit": packet_completion,
        "missingness_sensitivity_required": (
            bool(
                packet_completion
                and packet_completion.get(
                    "missingness_sensitivity_required", False
                )
            )
        ),
        "firewall": {
            "screen_is_logistical_not_g1_g2": True,
            "screen_units_confirmatory_ineligible": True,
            "zero_detection_not_absence": True,
            "pollinator_signal_uses_flower_minute_exposure": True,
            "capacity_shortfall_declared_only_after_exhaustive_census": (
                status != "CONTEXT_SIGNAL_PRESENT_CAPACITY_LIMITED" or census_exhausted is True
            ),
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
