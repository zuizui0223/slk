from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    from scripts.pedicularis_permission_scope import (
        activities_cover_window,
        validate_confirmed_permission_scope,
    )
    from scripts.pedicularis_physical_units import (
        FIREWALL_SCHEMA,
        canonical_tag_hash,
        validate_physical_plant_mapping,
    )
except ImportError:
    from pedicularis_permission_scope import (
        activities_cover_window,
        validate_confirmed_permission_scope,
    )
    from pedicularis_physical_units import (
        FIREWALL_SCHEMA,
        canonical_tag_hash,
        validate_physical_plant_mapping,
    )


SCHEMA = "SLK_PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_V1"
PRODUCTION_STATUS = "PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_PROSPECTIVELY_FROZEN"
DATASET_ID = "PED_P0_NAT_HIST_CAL_V1"
ENDPOINTS = {
    "pollinator": "LEGITIMATE_VISITS_PER_FLOWER_MINUTE",
    "predator": "EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS",
    "water_state": "WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS",
}
ALLOWED_SAMPLING_SOURCES = {
    "CALIBRATION_FEASIBILITY_ONLY",
    "EXTERNAL_METHOD_ANCHOR",
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "COMBINED_PREDECLARED",
}
ALLOWED_RULE_SOURCES = {
    "DOWNSTREAM_DESIGN_REQUIREMENT",
    "COMBINED_PREDECLARED",
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


def _number(value: object, label: str, minimum: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    _need(math.isfinite(out) and out >= minimum, f"{label} must be finite and >= {minimum}")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _number(value, label, minimum=1)
    _need(out.is_integer(), f"{label} must be an integer")
    return int(out)


def _bool(value: object, label: str) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    _need(text in {"true", "false", "1", "0", "yes", "no"}, f"{label} must be boolean-like")
    return text in {"true", "1", "yes"}


def _quantile(values: list[float], q: float) -> float:
    _need(bool(values), "cannot take quantile of empty list")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = q * (len(ordered) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ordered[lo]
    frac = pos - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == SCHEMA, "wrong natural-history calibration schema")
    _need(freeze.get("status") == "FROZEN_CANDIDATE", "calibration freeze must be FROZEN_CANDIDATE")
    _need(freeze.get("production_status") == PRODUCTION_STATUS, "wrong calibration production status")

    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    _need(ctx.get("dataset_id") == DATASET_ID, "wrong calibration dataset id")
    for key in ("candidate_id", "candidate_site_id", "population_id", "season_id", "calibration_window_id", "future_p0_screen_window_id"):
        _filled(ctx.get(key), f"context.{key}")
    planned_start = _iso_date(
        ctx.get("planned_calibration_start_date"),
        "context.planned_calibration_start_date",
    )
    planned_end = _iso_date(
        ctx.get("planned_calibration_end_date"),
        "context.planned_calibration_end_date",
    )
    _need(
        planned_start <= planned_end,
        "planned calibration date interval reversed",
    )
    _need(ctx.get("frozen_before_calibration_outcomes") is True, "calibration not frozen before outcomes")
    _need(ctx.get("p0_outcomes_opened") is False, "P0 outcomes already opened")

    permission = freeze.get("permission_scope_receipt")
    _need(
        isinstance(permission, dict),
        "P0a permission scope receipt missing",
    )
    validated_permission = validate_confirmed_permission_scope(
        permission,
        expected_candidate_id=ctx["candidate_id"],
    )
    _need(
        activities_cover_window(
            validated_permission,
            planned_start,
            planned_end,
        ),
        "P0a planned calibration window outside permission validity",
    )

    sampling = freeze.get("sampling", {})
    floors = {
        "pollinator_bouts": _positive_int(sampling.get("minimum_pollinator_bouts"), "minimum pollinator bouts"),
        "pollinator_minutes": _number(sampling.get("minimum_pollinator_minutes_total"), "minimum pollinator minutes", minimum=0.000001),
        "predator_flowers": _positive_int(sampling.get("minimum_predator_flowers"), "minimum predator flowers"),
        "water_plants": _positive_int(sampling.get("minimum_water_state_plants"), "minimum water-state plants"),
    }
    sampling_source = _filled(sampling.get("sampling_floor_source_type"), "sampling floor source type")
    _need(sampling_source in ALLOWED_SAMPLING_SOURCES, "unapproved sampling floor source type")
    _filled(sampling.get("sampling_floor_source_reference"), "sampling floor source reference")
    _filled(sampling.get("sampling_floor_rationale"), "sampling floor rationale")

    rule = freeze.get("qualification_rule", {})
    _need(rule.get("rule") == "ONE_SIDED_INDEPENDENT_UNIT_BOOTSTRAP_LOWER_QUANTILE", "qualification rule changed")
    lower_q = _number(rule.get("lower_quantile"), "lower quantile", minimum=0.000001)
    _need(lower_q < 0.5, "lower quantile must be < 0.5")
    seed = rule.get("bootstrap_seed")
    reps = rule.get("bootstrap_reps")
    min_reps = rule.get("minimum_bootstrap_reps")
    _need(isinstance(seed, int), "bootstrap seed must be integer")
    _need(isinstance(min_reps, int) and min_reps >= 1000, "minimum bootstrap reps must be >=1000")
    _need(isinstance(reps, int) and reps >= min_reps, "bootstrap reps below frozen minimum")
    valid_fraction = _number(rule.get("minimum_valid_fraction"), "minimum valid fraction", minimum=0.000001)
    _need(valid_fraction <= 1, "minimum valid fraction must be <=1")
    rule_source = _filled(rule.get("lower_quantile_source_type"), "lower-quantile source type")
    _need(rule_source in ALLOWED_RULE_SOURCES, "unapproved lower-quantile source type")
    _filled(rule.get("lower_quantile_source_reference"), "lower-quantile source reference")
    _filled(rule.get("lower_quantile_rationale"), "lower-quantile rationale")
    _need(rule.get("require_all_three_lower_bounds_strictly_positive") is True, "all-positive lower-bound rule disabled")

    endpoints = freeze.get("endpoints", {})
    for key, metric in ENDPOINTS.items():
        _need(endpoints.get(key, {}).get("metric") == metric, f"endpoint metric changed: {key}")

    firewall = freeze.get("firewall", {})
    for key in (
        "calibration_units_p0_decision_ineligible",
        "calibration_units_qz_qp_qg_ineligible",
        "calibration_units_g1_g2_ineligible",
        "calibration_units_y_d0_ineligible",
        "calibration_units_g3_g5_ineligible",
        "calibration_values_may_define_p0_effort_only",
        "lower_bound_rule_frozen_before_calibration_outcomes",
        "failed_or_zero_compatible_calibration_not_rescued_posthoc",
    ):
        _need(firewall.get(key) is True, f"calibration firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _filled(metadata.get(key), f"freeze_metadata.{key}")

    return {
        "context": ctx,
        "permission_scope_receipt": permission,
        "planned_calibration_start_date": planned_start.isoformat(),
        "planned_calibration_end_date": planned_end.isoformat(),
        "floors": floors,
        "lower_quantile": lower_q,
        "seed": seed,
        "reps": reps,
        "minimum_valid_fraction": valid_fraction,
        "freeze_commit": metadata["freeze_commit"],
    }


def _bootstrap_pollinator(bouts: list[tuple[float, int, float]], reps: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    n = len(bouts)
    out = []
    for _ in range(reps):
        sampled = [bouts[rng.randrange(n)] for _ in range(n)]
        visits = sum(x[2] for x in sampled)
        flower_minutes = sum(x[0] * x[1] for x in sampled)
        if flower_minutes > 0:
            out.append(visits / flower_minutes)
    return out


def _bootstrap_binary(values: list[int], reps: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    return [sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(reps)]


def summarize(rows: list[dict[str, str]], freeze: dict) -> dict:
    cfg = validate_freeze(freeze)
    _need(bool(rows), "calibration rows are empty")
    ctx = cfg["context"]

    for row in rows:
        _need(row.get("dataset_id") == DATASET_ID, "wrong calibration row dataset id")
        for key in ("candidate_site_id", "population_id", "season_id", "calibration_window_id"):
            _need(row.get(key) == ctx.get(key), f"row/freeze context mismatch: {key}")
        _need(_bool(row.get("calibration_only"), "calibration_only") is True, "row must remain calibration-only")
        _need(_bool(row.get("p0_decision_eligible"), "p0_decision_eligible") is False, "calibration row cannot be a P0 decision unit")
        _need(_bool(row.get("downstream_confirmatory_eligible"), "downstream_confirmatory_eligible") is False, "calibration row cannot be downstream confirmatory")

    physical_rows = [
        row
        for row in rows
        if row.get("record_type") in {"PREDATOR_FLOWER", "WATER_PLANT"}
    ]
    physical_mapping = validate_physical_plant_mapping(physical_rows)
    physical_tags = sorted(set(physical_mapping.values()))

    planned_start = date.fromisoformat(
        cfg["planned_calibration_start_date"]
    )
    planned_end = date.fromisoformat(
        cfg["planned_calibration_end_date"]
    )
    observed_dates: list[date] = []

    poll_bouts: list[tuple[float, int, float]] = []
    predator: list[int] = []
    water: list[int] = []
    poll_minutes = 0.0
    poll_flower_minutes = 0.0
    poll_visits = 0.0
    incomplete_records: list[dict[str, str]] = []

    for row in rows:
        kind = row.get("record_type")
        if kind == "POLLINATOR_BOUT":
            date_raw = str(row.get("observation_date", "")).strip()
            minutes_raw = str(row.get("observed_minutes", "")).strip()
            flowers_raw = str(row.get("simultaneously_open_focal_flowers", "")).strip()
            visits_raw = str(row.get("legitimate_pollinator_visits", "")).strip()
            if not (date_raw and minutes_raw and flowers_raw and visits_raw):
                missing_fields = [
                    field
                    for field, value in (
                        ("observation_date", date_raw),
                        ("observed_minutes", minutes_raw),
                        (
                            "simultaneously_open_focal_flowers",
                            flowers_raw,
                        ),
                        ("legitimate_pollinator_visits", visits_raw),
                    )
                    if not value
                ]
                incomplete_records.append(
                    {
                        "record_id": str(row.get("record_id", "")),
                        "record_type": "POLLINATOR_BOUT",
                        "reason": "MISSING_REQUIRED_MEASUREMENT",
                        "detail": ",".join(missing_fields),
                    }
                )
                continue
            observation_date = _iso_date(
                date_raw,
                f"observation date/{row['record_id']}",
            )
            _need(
                planned_start <= observation_date <= planned_end,
                f"P0a observation outside planned calibration window: {row['record_id']}",
            )
            observed_dates.append(observation_date)
            minutes = _number(minutes_raw, "pollinator observed minutes", minimum=0.000001)
            flowers = _positive_int(float(flowers_raw), "simultaneously open focal flowers")
            visits = _number(visits_raw, "legitimate pollinator visits", minimum=0)
            poll_bouts.append((minutes, flowers, visits))
            poll_minutes += minutes
            poll_flower_minutes += minutes * flowers
            poll_visits += visits
        elif kind == "PREDATOR_FLOWER":
            date_raw = str(row.get("observation_date", "")).strip()
            raw = str(row.get("early_attack_or_oviposition_positive", "")).strip()
            if not (date_raw and raw):
                missing_fields = [
                    field
                    for field, value in (
                        ("observation_date", date_raw),
                        ("early_attack_or_oviposition_positive", raw),
                    )
                    if not value
                ]
                incomplete_records.append(
                    {
                        "record_id": str(row.get("record_id", "")),
                        "record_type": "PREDATOR_FLOWER",
                        "reason": "MISSING_REQUIRED_MEASUREMENT",
                        "detail": ",".join(missing_fields),
                    }
                )
                continue
            observation_date = _iso_date(
                date_raw,
                f"observation date/{row['record_id']}",
            )
            _need(
                planned_start <= observation_date <= planned_end,
                f"P0a observation outside planned calibration window: {row['record_id']}",
            )
            observed_dates.append(observation_date)
            _filled(row.get("plant_id"), "predator plant_id")
            _filled(row.get("flower_id"), "predator flower_id")
            predator.append(int(_bool(raw, "early_attack_or_oviposition_positive")))
        elif kind == "WATER_PLANT":
            date_raw = str(row.get("observation_date", "")).strip()
            raw = str(row.get("water_positive", "")).strip()
            if not (date_raw and raw):
                missing_fields = [
                    field
                    for field, value in (
                        ("observation_date", date_raw),
                        ("water_positive", raw),
                    )
                    if not value
                ]
                incomplete_records.append(
                    {
                        "record_id": str(row.get("record_id", "")),
                        "record_type": "WATER_PLANT",
                        "reason": "MISSING_REQUIRED_MEASUREMENT",
                        "detail": ",".join(missing_fields),
                    }
                )
                continue
            observation_date = _iso_date(
                date_raw,
                f"observation date/{row['record_id']}",
            )
            _need(
                planned_start <= observation_date <= planned_end,
                f"P0a observation outside planned calibration window: {row['record_id']}",
            )
            observed_dates.append(observation_date)
            _filled(row.get("plant_id"), "water plant_id")
            water.append(int(_bool(raw, "water_positive")))
        else:
            raise ValueError(f"unknown calibration record_type: {kind}")

    floors = cfg["floors"]
    floor_checks = {
        "pollinator_bouts": len(poll_bouts) >= floors["pollinator_bouts"],
        "pollinator_minutes": poll_minutes >= floors["pollinator_minutes"],
        "predator_flowers": len(predator) >= floors["predator_flowers"],
        "water_plants": len(water) >= floors["water_plants"],
    }
    floors_pass = all(floor_checks.values())
    registered_rows_complete = not incomplete_records

    reason_counts: dict[str, int] = {}
    for item in incomplete_records:
        reason = item["reason"]
        reason_counts[reason] = reason_counts.get(reason, 0) + 1

    estimates = {
        "pollinator": None,
        "predator": None,
        "water_state": None,
    }
    qualified = False
    if floors_pass and registered_rows_complete:
        poll_boot = _bootstrap_pollinator(
            poll_bouts, cfg["reps"], cfg["seed"]
        )
        pred_boot = _bootstrap_binary(predator, cfg["reps"], cfg["seed"] + 1)
        water_boot = _bootstrap_binary(water, cfg["reps"], cfg["seed"] + 2)
        min_valid = math.ceil(cfg["reps"] * cfg["minimum_valid_fraction"])
        _need(len(poll_boot) >= min_valid, "too few valid pollinator bootstrap replicates")
        _need(len(pred_boot) >= min_valid, "too few valid predator bootstrap replicates")
        _need(len(water_boot) >= min_valid, "too few valid water bootstrap replicates")

        poll_point = poll_visits / poll_flower_minutes
        pred_point = sum(predator) / len(predator)
        water_point = sum(water) / len(water)
        estimates = {
            "pollinator": {
                "metric": ENDPOINTS["pollinator"],
                "point": poll_point,
                "lower_bound": _quantile(poll_boot, cfg["lower_quantile"]),
                "lower_quantile": cfg["lower_quantile"],
                "independent_bouts": len(poll_bouts),
                "total_minutes": poll_minutes,
                "total_flower_minutes": poll_flower_minutes,
                "legitimate_visits": poll_visits,
            },
            "predator": {
                "metric": ENDPOINTS["predator"],
                "point": pred_point,
                "lower_bound": _quantile(pred_boot, cfg["lower_quantile"]),
                "lower_quantile": cfg["lower_quantile"],
                "independent_flowers": len(predator),
                "positive_flowers": sum(predator),
            },
            "water_state": {
                "metric": ENDPOINTS["water_state"],
                "point": water_point,
                "lower_bound": _quantile(water_boot, cfg["lower_quantile"]),
                "lower_quantile": cfg["lower_quantile"],
                "independent_plants": len(water),
                "positive_plants": sum(water),
            },
        }
        qualified = all(estimates[key]["lower_bound"] > 0 for key in estimates)

    if not floors_pass or not registered_rows_complete:
        status = "P0_RELEVANCE_FRESH_CALIBRATION_INCOMPLETE"
    elif qualified:
        status = "P0_RELEVANCE_FRESH_CALIBRATION_QUALIFIED"
    else:
        status = "P0_RELEVANCE_FRESH_CALIBRATION_ZERO_COMPATIBLE_UNRESOLVED"

    return {
        "schema_version": "SLK_PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_RECEIPT_V1",
        "status": status,
        "context": {
            "system": "Pedicularis rex",
            "candidate_id": ctx["candidate_id"],
            "candidate_site_id": ctx["candidate_site_id"],
            "population_id": ctx["population_id"],
            "season_id": ctx["season_id"],
            "calibration_window_id": ctx["calibration_window_id"],
            "future_p0_screen_window_id": ctx["future_p0_screen_window_id"],
            "dataset_id": DATASET_ID,
            "p0_outcomes_opened": False,
        },
        "permission_scope_receipt": cfg["permission_scope_receipt"],
        "permission_scope_audit": {
            "status": "P0A_PERMISSION_VALIDITY_CONFIRMED_FOR_PLANNED_WINDOW",
            "required_scope": cfg["permission_scope_receipt"]["required_scope"],
            "sampling_permission_reference": cfg["permission_scope_receipt"].get(
                "sampling_permission_reference"
            ),
            "planned_calibration_start_date": cfg[
                "planned_calibration_start_date"
            ],
            "planned_calibration_end_date": cfg[
                "planned_calibration_end_date"
            ],
            "required_activities": ["A", "B", "C"],
            "planned_window_fully_covered": True,
            "observed_date_min": (
                min(observed_dates).isoformat() if observed_dates else None
            ),
            "observed_date_max": (
                max(observed_dates).isoformat() if observed_dates else None
            ),
            "all_completed_rows_within_planned_window": True,
        },
        "physical_unit_registry_handoff": {
            "status": "P0_CALIBRATION_PLANT_TAGS_VALIDATED",
            "assignment_to_physical_tag": physical_mapping,
            "current_physical_plant_count": len(physical_tags),
            "current_physical_plant_tags": physical_tags,
            "current_tag_set_sha256": canonical_tag_hash(physical_tags),
            "next_stage_firewall_block": {
                "schema_version": FIREWALL_SCHEMA,
                "require_nonempty_physical_plant_tag": True,
                "prior_physical_plant_tags_forbidden": physical_tags,
                "prior_tag_source_references": [
                    f"PED_P0_NAT_HIST_CAL_V1@{cfg['freeze_commit']}"
                ],
                "prior_tag_set_sha256": canonical_tag_hash(physical_tags),
                "frozen_before_outcomes": True,
            },
            "scope_note": (
                "Permanent-tag firewall covers plant/flower-based predator and water calibration units. "
                "Pollinator calibration independence remains temporal at the observation-bout level."
            ),
        },
        "sampling_floor_checks": floor_checks,
        "sampling_floors_pass": floors_pass,
        "completion_audit": {
            "registered_rows": len(rows),
            "completed_pollinator_bouts": len(poll_bouts),
            "completed_predator_flowers": len(predator),
            "completed_water_plants": len(water),
            "incomplete_records": len(incomplete_records),
            "registered_rows_complete": registered_rows_complete,
            "incomplete_reason_counts": reason_counts,
            "incomplete_record_details": incomplete_records,
            "sensitivity_required": bool(incomplete_records),
        },
        "qualification_rule": {
            "rule": "ONE_SIDED_INDEPENDENT_UNIT_BOOTSTRAP_LOWER_QUANTILE",
            "lower_quantile": cfg["lower_quantile"],
            "bootstrap_reps": cfg["reps"],
            "minimum_valid_fraction": cfg["minimum_valid_fraction"],
            "freeze_commit": cfg["freeze_commit"],
        },
        "estimates": estimates,
        "qualification_ready": qualified,
        "recommended_minimum_relevance_values": (
            {
                "P0_POLLINATOR_MIN_RATE": estimates["pollinator"]["lower_bound"],
                "P0_PREDATOR_MIN_PREVALENCE": estimates["predator"]["lower_bound"],
                "P0_WATER_POSITIVE_PREVALENCE": estimates["water_state"]["lower_bound"],
            }
            if qualified
            else None
        ),
        "firewall": {
            "calibration_units_p0_decision_ineligible": True,
            "calibration_units_downstream_confirmatory_ineligible": True,
            "values_may_define_p0_effort_only": True,
            "no_posthoc_rescue_if_zero_compatible": True,
            "incomplete_registered_calibration_rows_block_qualification": True,
        },
        "claim_ceiling": "FRESH_NATURAL_HISTORY_SIGNAL_FLOOR_CALIBRATION_ONLY_NO_P0_PASS_NO_G1_G5_RESULT",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize independent Pedicularis P0 natural-history calibration")
    parser.add_argument("calibration_csv", type=Path)
    parser.add_argument("calibration_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(
        _read_csv(args.calibration_csv),
        json.loads(args.calibration_freeze_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
