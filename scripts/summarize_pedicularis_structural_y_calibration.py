from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median, stdev


FREEZE_SCHEMA = "SLK_PEDICULARIS_STRUCTURAL_Y_METRIC_FREEZE_V1"
RECEIPT_SCHEMA = "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1"
Y_DATASET_ID = "PED_Y_CAL_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
MIN_PLANTS = 36
FLOWERS_PER_PLANT = 3
TREATMENT = "Y_CAL_REPEATED_MEASUREMENT"
DIRECTION = "HIGHER_IS_MORE_RETENTIVE_OR_PROTECTIVE"
METRICS = {
    "RETENTION_MEAN_MAX_ML": ("retention_trial1_max_ml", "retention_trial2_max_ml", False),
    "RETENTION_MEAN_DEPTH_MM": ("retention_trial1_depth_mm", "retention_trial2_depth_mm", False),
    "RETENTION_MEAN_HALF_LIFE_MIN": ("retention_trial1_half_life_min", "retention_trial2_half_life_min", False),
    "RETENTION_MEAN_PROTECTED_FRACTION": (
        "retention_trial1_protected_fraction",
        "retention_trial2_protected_fraction",
        True,
    ),
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "REQUIRED_BEFORE_USE" not in value


def _number(row: dict[str, str], field: str, proportion: bool = False) -> float:
    raw = str(row.get(field, "")).strip()
    _need(raw != "", f"missing {field}")
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"non-numeric {field}: {raw}") from exc
    _need(math.isfinite(value), f"non-finite {field}")
    if proportion:
        _need(0 <= value <= 1, f"{field} must be in [0,1]")
    return value


def _quantile_type7(values: list[float], p: float) -> float:
    _need(bool(values), "quantile requires values")
    _need(0 <= p <= 1, "quantile p must be in [0,1]")
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    h = (len(xs) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return xs[lo]
    frac = h - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def _sample_cov(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1)


def _corr(x: list[float], y: list[float]) -> float | None:
    cov = _sample_cov(x, y)
    if cov is None:
        return None
    sx = stdev(x)
    sy = stdev(y)
    if sx <= 0 or sy <= 0:
        return None
    return cov / (sx * sy)


def validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong structural-y freeze schema")
    context = freeze.get("context", {})
    _need(context.get("system") == "Pedicularis rex", "wrong structural-y system")
    for key in ("population_id", "season_id", "y_cal_dataset_id", "primary_y_metric"):
        _need(_filled(context.get(key)), f"unfrozen structural-y field: {key}")
    _need(context.get("y_cal_dataset_id") == Y_DATASET_ID, "wrong Y-CAL dataset id")
    metric = context.get("primary_y_metric")
    allowed = set(freeze.get("allowed_primary_y_metrics", []))
    _need(metric in METRICS and metric in allowed, "unregistered primary y metric")
    _need(context.get("metric_direction") == DIRECTION, "wrong primary y direction")
    _need(context.get("frozen_before_y_cal_outcomes") is True, "primary y metric not frozen before Y-CAL outcomes")

    band = freeze.get("band_rule", {})
    _need(
        band.get("low_y") == "PLANT_MEAN_AT_OR_BELOW_Y_CAL_ONE_THIRD_QUANTILE",
        "low-y band rule changed",
    )
    _need(
        band.get("high_y") == "PLANT_MEAN_AT_OR_ABOVE_Y_CAL_TWO_THIRDS_QUANTILE",
        "high-y band rule changed",
    )
    _need(
        band.get("dynamic_range_rule")
        == "MEDIAN_HIGH_MINUS_MEDIAN_LOW_GTE_MAX_BETWEEN_PLANT_SD_AND_TWO_X_MEASUREMENT_ERROR_SD",
        "dynamic-range rule changed",
    )
    _need(band.get("posthoc_cutpoint_search_forbidden") is True, "posthoc band search firewall disabled")

    firewall = freeze.get("firewall", {})
    for key in (
        "choose_metric_by_smallest_variance_forbidden",
        "choose_metric_by_largest_observed_high_low_gap_forbidden",
        "choose_metric_by_best_downstream_fitness_association_forbidden",
        "y_cal_units_confirmatory_ineligible",
    ):
        _need(firewall.get(key) is True, f"structural-y firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _need(_filled(metadata.get(key)), f"structural-y freeze metadata missing: {key}")
    return {"primary_y_metric": metric}


def summarize(rows: list[dict[str, str]], freeze: dict) -> dict:
    frozen = validate_freeze(freeze)
    metric_id = frozen["primary_y_metric"]
    trial1_field, trial2_field, proportion = METRICS[metric_id]
    _need(bool(rows), "Y-CAL rows are empty")

    for row in rows:
        _need(row.get("dataset_id") == Y_DATASET_ID, "wrong dataset_id in Y-CAL")
        _need(str(row.get("confirmatory_eligible", "")).strip().lower() == "false", "Y-CAL row marked confirmatory eligible")
        _need(row.get("treatment") == TREATMENT, "unexpected Y-CAL treatment")

    context_values = {
        (
            row.get("context_id"),
            row.get("population_id"),
            row.get("season_id"),
            row.get("fitness_scale_id"),
            row.get("time_horizon_id"),
        )
        for row in rows
    }
    _need(len(context_values) == 1, "Y-CAL contains multiple contexts")
    context_id, population_id, season_id, fitness_scale_id, time_horizon_id = next(iter(context_values))
    _need(bool(context_id and population_id and season_id and fitness_scale_id and time_horizon_id), "Y-CAL context fields incomplete")
    _need(population_id == freeze["context"]["population_id"], "Y-CAL/freeze population mismatch")
    _need(season_id == freeze["context"]["season_id"], "Y-CAL/freeze season mismatch")
    _need(fitness_scale_id == FITNESS_SCALE_ID, "wrong Y-CAL fitness scale")

    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        plant_id = str(row.get("plant_id", "")).strip()
        _need(plant_id, "Y-CAL missing plant_id")
        by_plant[plant_id].append(row)

    plant_means: list[float] = []
    plant_z: list[float] = []
    flower_means_by_plant: dict[str, list[float]] = {}
    trial_differences: list[float] = []
    complete_plants = 0

    for plant_id in sorted(by_plant):
        plant_rows = by_plant[plant_id]
        if len(plant_rows) != FLOWERS_PER_PLANT:
            continue
        flower_means: list[float] = []
        z_values: list[float] = []
        plant_trial_differences: list[float] = []
        complete = True
        for row in plant_rows:
            try:
                t1 = _number(row, trial1_field, proportion=proportion)
                t2 = _number(row, trial2_field, proportion=proportion)
                z = _number(row, "exsertion_z")
            except ValueError:
                complete = False
                break
            flower_means.append((t1 + t2) / 2)
            plant_trial_differences.append(t1 - t2)
            z_values.append(z)
        if not complete:
            continue
        complete_plants += 1
        flower_means_by_plant[plant_id] = flower_means
        plant_means.append(sum(flower_means) / FLOWERS_PER_PLANT)
        plant_z.append(sum(z_values) / FLOWERS_PER_PLANT)
        trial_differences.extend(plant_trial_differences)

    floor_pass = complete_plants >= MIN_PLANTS
    if complete_plants < 2:
        return {
            "schema_version": RECEIPT_SCHEMA,
            "status": "STRUCTURAL_Y_CALIBRATION_INCOMPLETE",
            "primary_y_metric": metric_id,
            "complete_independent_plants": complete_plants,
            "registered_floor_plants": MIN_PLANTS,
            "complete_plant_floor_pass": False,
            "claim_ceiling": "Y_CAL_INCOMPLETE_NO_STRUCTURAL_Y_PROMOTION",
        }

    n = complete_plants
    k = FLOWERS_PER_PLANT
    grand = sum(plant_means) / n
    ss_between = k * sum((m - grand) ** 2 for m in plant_means)
    ms_between = ss_between / (n - 1)
    ss_within = sum(
        sum((value - (sum(values) / k)) ** 2 for value in values)
        for values in flower_means_by_plant.values()
    )
    ms_within = ss_within / (n * (k - 1))
    between_var = max((ms_between - ms_within) / k, 0.0)
    within_var = max(ms_within, 0.0)
    between_sd = math.sqrt(between_var)
    within_sd = math.sqrt(within_var)
    denom = between_var + within_var
    icc = between_var / denom if denom > 0 else None

    measurement_error_sd = None
    if len(trial_differences) >= 2:
        measurement_error_sd = stdev(trial_differences) / math.sqrt(2)

    q1 = _quantile_type7(plant_means, 1 / 3)
    q2 = _quantile_type7(plant_means, 2 / 3)
    low_values = [x for x in plant_means if x <= q1]
    high_values = [x for x in plant_means if x >= q2]
    low_median = median(low_values)
    high_median = median(high_values)
    band_gap = high_median - low_median
    dynamic_threshold = None
    dynamic_pass = False
    if measurement_error_sd is not None:
        dynamic_threshold = max(between_sd, 2 * measurement_error_sd)
        dynamic_pass = floor_pass and between_sd > 0 and band_gap >= dynamic_threshold

    covariance_zy = _sample_cov(plant_z, plant_means)
    correlation_zy = _corr(plant_z, plant_means)
    y1_audited = correlation_zy is not None

    if not floor_pass:
        status = "STRUCTURAL_Y_CALIBRATION_INCOMPLETE"
    elif not dynamic_pass:
        status = "STRUCTURAL_Y_CALIBRATION_COMPLETE_RANGE_UNRESOLVED"
    elif not y1_audited:
        status = "STRUCTURAL_Y_RANGE_QUALIFIED_Y1_UNRESOLVED"
    else:
        status = "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"

    recruitment_authorized = status == "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"
    return {
        "schema_version": RECEIPT_SCHEMA,
        "status": status,
        "context": {
            "system": "Pedicularis rex",
            "context_id": context_id,
            "population_id": population_id,
            "season_id": season_id,
            "fitness_scale_id": fitness_scale_id,
            "time_horizon_id": time_horizon_id,
            "y_cal_dataset_id": Y_DATASET_ID,
        },
        "primary_y_metric": metric_id,
        "complete_independent_plants": complete_plants,
        "registered_floor_plants": MIN_PLANTS,
        "complete_plant_floor_pass": floor_pass,
        "variance_components": {
            "between_plant_sd": between_sd,
            "within_plant_flower_sd": within_sd,
            "measurement_error_sd_from_trial_pairs": measurement_error_sd,
            "icc_plant_over_flower_means": icc,
        },
        "band_freeze": {
            "low_y_max": q1,
            "high_y_min": q2,
            "low_group_median": low_median,
            "high_group_median": high_median,
            "median_gap": band_gap,
            "dynamic_range_threshold": dynamic_threshold,
            "dynamic_range_pass": dynamic_pass,
            "low_y_rule": "PLANT_MEAN_AT_OR_BELOW_Y_CAL_ONE_THIRD_QUANTILE",
            "high_y_rule": "PLANT_MEAN_AT_OR_ABOVE_Y_CAL_TWO_THIRDS_QUANTILE",
            "recruitment_authorized_for_disjoint_d0_cal": recruitment_authorized,
        },
        "x_y_coupling_audit": {
            "plant_mean_z_y_covariance": covariance_zy,
            "plant_mean_z_y_correlation": correlation_zy,
            "y1_coupling_audited": y1_audited,
            "interpretation": "Correlation is reported, not used as an automatic exclusion threshold. Strong coupling lowers the modularity claim ceiling but does not erase a repeatable second functional phenotype.",
        },
        "firewall": {
            "primary_metric_frozen_before_y_cal_outcomes": True,
            "cutpoints_derived_only_from_y_cal_primary_metric": True,
            "y_cal_units_confirmatory_ineligible": True,
        },
        "claim_ceiling": "Y0_RANGE_AND_Y1_COUPLING_ONLY; Y2_PREFERENTIAL_LOADING, Y3_INTERVENTION, D0, R, K, AND_PHI_REMAIN_OPEN",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Pedicularis Y-CAL structural-y repeatability and recruitment bands")
    parser.add_argument("y_cal_csv", type=Path)
    parser.add_argument("metric_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = summarize(
        _read_csv(args.y_cal_csv),
        json.loads(args.metric_freeze_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
