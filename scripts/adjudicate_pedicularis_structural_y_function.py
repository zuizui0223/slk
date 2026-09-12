from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path


FREEZE_SCHEMA = "SLK_PEDICULARIS_STRUCTURAL_Y_FUNCTION_FREEZE_V1"
Y_RECEIPT_SCHEMA = "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1"
D0_DATASET_ID = "PED_D0_CAL_V1"
FITNESS_SCALE_ID = "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
Y_READY_STATUS = "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED"

Y_METRICS = {
    "RETENTION_MEAN_MAX_ML": ("retention_trial1_max_ml", "retention_trial2_max_ml", False),
    "RETENTION_MEAN_DEPTH_MM": ("retention_trial1_depth_mm", "retention_trial2_depth_mm", False),
    "RETENTION_MEAN_HALF_LIFE_MIN": ("retention_trial1_half_life_min", "retention_trial2_half_life_min", False),
    "RETENTION_MEAN_PROTECTED_FRACTION": (
        "retention_trial1_protected_fraction",
        "retention_trial2_protected_fraction",
        True,
    ),
}
ANTAGONIST_ENDPOINTS = {
    "EARLY_ATTACK_PROP": ("early_attack_prop", -1, True),
    "SEED_PREDATION_PROP": ("seed_predation_prop", -1, True),
    "MATURE_VIABLE_UNDAMAGED_SEEDS": ("mature_viable_undamaged_seeds", 1, False),
}
POLLINATION_ENDPOINTS = {
    "VISIT_RATE_PER_MIN": ("VISIT_RATE_PER_MIN", False),
    "POLLEN_RECEIPT_GRAINS": ("pollen_receipt_grains", False),
    "INITIAL_SEED_SET_PROP": ("initial_seed_set_prop", True),
}


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "REQUIRED_BEFORE_USE" not in value


def _positive(value: object, label: str) -> float:
    _need(isinstance(value, (int, float)) and not isinstance(value, bool), f"{label} must be numeric")
    value = float(value)
    _need(math.isfinite(value) and value > 0, f"{label} must be finite and > 0")
    return value


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


def _mean_two(row: dict[str, str], field1: str, field2: str, proportion: bool) -> float:
    return (_number(row, field1, proportion) + _number(row, field2, proportion)) / 2


def _y_value(row: dict[str, str], metric: str) -> float:
    _need(metric in Y_METRICS, "unregistered structural-y metric")
    f1, f2, proportion = Y_METRICS[metric]
    return _mean_two(row, f1, f2, proportion)


def _endpoint_value(row: dict[str, str], endpoint: str, pollination: bool = False) -> float:
    if pollination:
        field, proportion = POLLINATION_ENDPOINTS[endpoint]
        if field == "VISIT_RATE_PER_MIN":
            visits = _number(row, "legitimate_visits")
            minutes = _number(row, "pollinator_observation_minutes")
            _need(minutes > 0, "pollinator_observation_minutes must be > 0")
            return visits / minutes
        return _number(row, field, proportion)
    field, _, proportion = ANTAGONIST_ENDPOINTS[endpoint]
    value = _number(row, field, proportion)
    if field == "mature_viable_undamaged_seeds":
        _need(value >= 0, "mature viable seeds must be >= 0")
    return value


def _quantile(values: list[float], p: float) -> float:
    _need(values, "quantile requires values")
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


def _ci(values: list[float], level: float) -> tuple[float, float]:
    alpha = 1 - level
    return _quantile(values, alpha / 2), _quantile(values, 1 - alpha / 2)


def _ols_y_z(records: list[tuple[float, float, float]]) -> dict | None:
    if len(records) < 3:
        return None
    ys = [r[0] for r in records]
    zs = [r[1] for r in records]
    outs = [r[2] for r in records]
    my = sum(ys) / len(ys)
    mz = sum(zs) / len(zs)
    mo = sum(outs) / len(outs)
    syy = sum((y - my) ** 2 for y in ys)
    szz = sum((z - mz) ** 2 for z in zs)
    syz = sum((y - my) * (z - mz) for y, z in zip(ys, zs))
    syo = sum((y - my) * (o - mo) for y, o in zip(ys, outs))
    szo = sum((z - mz) * (o - mo) for z, o in zip(zs, outs))
    determinant = syy * szz - syz * syz
    if determinant <= 1e-12:
        return None
    beta_y = (syo * szz - szo * syz) / determinant
    beta_z = (szo * syy - syo * syz) / determinant
    intercept = mo - beta_y * my - beta_z * mz
    return {
        "intercept": intercept,
        "beta_y": beta_y,
        "beta_z": beta_z,
        "determinant": determinant,
    }


def _bootstrap_beta_y(
    records: list[tuple[float, float, float]], seed: int, reps: int
) -> tuple[list[float], int]:
    rng = random.Random(seed)
    n = len(records)
    values: list[float] = []
    for _ in range(reps):
        sample = [records[rng.randrange(n)] for _ in range(n)]
        fit = _ols_y_z(sample)
        if fit is not None:
            values.append(fit["beta_y"])
    return values, len(values)


def _bootstrap_mean_difference(
    differences: list[float], seed: int, reps: int
) -> list[float]:
    rng = random.Random(seed)
    n = len(differences)
    return [sum(differences[rng.randrange(n)] for _ in range(n)) / n for _ in range(reps)]


def _validate_freeze(freeze: dict) -> dict:
    _need(freeze.get("schema_version") == FREEZE_SCHEMA, "wrong structural-y function freeze schema")
    ctx = freeze.get("context", {})
    _need(ctx.get("system") == "Pedicularis rex", "wrong system")
    for key in (
        "population_id",
        "season_id",
        "y_cal_dataset_id",
        "d0_cal_dataset_id",
        "structural_y_receipt_id",
        "primary_y_metric",
        "fitness_scale_id",
        "time_horizon_id",
    ):
        _need(_filled(ctx.get(key)), f"unfrozen structural-y function field: {key}")
    _need(ctx.get("y_cal_dataset_id") == "PED_Y_CAL_V1", "wrong Y-CAL id")
    _need(ctx.get("d0_cal_dataset_id") == D0_DATASET_ID, "wrong D0-CAL id")
    _need(ctx.get("primary_y_metric") in Y_METRICS, "unregistered primary y metric")
    _need(ctx.get("fitness_scale_id") == FITNESS_SCALE_ID, "wrong frozen fitness scale")
    _need(ctx.get("frozen_before_d0_cal_outcomes") is True, "Y2/Y3 config not frozen before D0-CAL outcomes")

    y2 = freeze.get("y2", {})
    ant = y2.get("natural_antagonist_endpoint")
    poll = y2.get("natural_pollination_endpoint")
    _need(ant in ANTAGONIST_ENDPOINTS, "unregistered antagonist endpoint")
    _need(ant in set(y2.get("allowed_antagonist_endpoints", [])), "antagonist endpoint not allowed")
    _need(poll in POLLINATION_ENDPOINTS, "unregistered pollination endpoint")
    _need(poll in set(y2.get("allowed_pollination_endpoints", [])), "pollination endpoint not allowed")
    poll_margin = _positive(y2.get("pollination_beta_y_equivalence_margin"), "pollination beta_y equivalence margin")
    min_n = y2.get("minimum_complete_n")
    _need(isinstance(min_n, int) and min_n >= 48, "Y2 minimum_complete_n must be >= 48")
    ant_level = float(y2.get("antagonist_ci_level"))
    poll_level = float(y2.get("pollination_equivalence_ci_level"))
    _need(0 < ant_level < 1 and 0 < poll_level < 1, "invalid Y2 CI level")
    _need(y2.get("control_coordinate") == "EXSERTION_Z", "Y2 control coordinate changed")
    _need(y2.get("natural_comparison_rows") == "LOW_Y_S_CAL_PLUS_HIGH_Y_D_CAL", "Y2 natural-row contract changed")

    y3 = freeze.get("y3", {})
    _need(y3.get("intervention_comparison") == "LOW_Y_D0_CAL_MINUS_SHAM_CAL", "Y3 comparison changed")
    min_y_gain = _positive(y3.get("minimum_primary_y_gain"), "minimum primary y gain")
    max_z_shift = _positive(y3.get("max_abs_exsertion_shift"), "max abs exsertion shift")
    y3_n = y3.get("minimum_complete_paired_plants")
    _need(isinstance(y3_n, int) and y3_n >= 24, "Y3 minimum paired plants must be >= 24")
    y_gain_level = float(y3.get("y_gain_ci_level"))
    z_eq_level = float(y3.get("z_equivalence_ci_level"))
    _need(0 < y_gain_level < 1 and 0 < z_eq_level < 1, "invalid Y3 CI level")
    _need(
        y3.get("interpretation") == "FUNCTIONAL_PERFORMANCE_INTERVENTION_NOT_HISTORICAL_ORIGIN",
        "Y3 interpretation changed",
    )

    boot = freeze.get("bootstrap", {})
    seed = boot.get("seed")
    reps = boot.get("reps")
    min_reps = boot.get("minimum_reps")
    _need(isinstance(seed, int), "bootstrap seed must be an integer")
    _need(isinstance(min_reps, int) and min_reps >= 1000, "invalid bootstrap minimum reps")
    _need(isinstance(reps, int) and reps >= min_reps, "bootstrap reps below frozen minimum")
    _need(boot.get("resampling_unit") == "INDEPENDENT_PLANT", "wrong bootstrap unit")

    firewall = freeze.get("firewall", {})
    for key in (
        "endpoint_selection_after_outcomes_forbidden",
        "pollination_margin_from_nonsignificance_forbidden",
        "y_gain_threshold_from_observed_d0_effect_forbidden",
        "z_margin_from_observed_d0_effect_forbidden",
        "d0_cal_units_confirmatory_g3_g5_ineligible",
        "natural_y2_and_intervention_y3_kept_distinct",
    ):
        _need(firewall.get(key) is True, f"Y2/Y3 firewall disabled: {key}")

    metadata = freeze.get("freeze_metadata", {})
    for key in ("slk_source_commit", "freeze_commit", "freeze_timestamp"):
        _need(_filled(metadata.get(key)), f"freeze metadata missing: {key}")

    return {
        "antagonist_endpoint": ant,
        "pollination_endpoint": poll,
        "pollination_margin": poll_margin,
        "minimum_y2_n": min_n,
        "antagonist_ci_level": ant_level,
        "pollination_ci_level": poll_level,
        "minimum_y_gain": min_y_gain,
        "max_z_shift": max_z_shift,
        "minimum_y3_n": y3_n,
        "y_gain_ci_level": y_gain_level,
        "z_equivalence_ci_level": z_eq_level,
        "seed": seed,
        "reps": reps,
    }


def _validate_y_receipt(receipt: dict, freeze: dict) -> dict:
    _need(receipt.get("schema_version") == Y_RECEIPT_SCHEMA, "wrong structural-y receipt schema")
    _need(receipt.get("status") == Y_READY_STATUS, "structural-y Y0/Y1 receipt not ready")
    _need(
        receipt.get("band_freeze", {}).get("recruitment_authorized_for_disjoint_d0_cal") is True,
        "D0-CAL recruitment not authorized by Y receipt",
    )
    rctx = receipt.get("context", {})
    fctx = freeze["context"]
    for key in ("population_id", "season_id", "fitness_scale_id", "time_horizon_id", "y_cal_dataset_id"):
        _need(rctx.get(key) == fctx.get(key), f"Y receipt/function-freeze mismatch: {key}")
    _need(receipt.get("primary_y_metric") == fctx.get("primary_y_metric"), "primary y metric mismatch")
    return receipt["band_freeze"]


def adjudicate(rows: list[dict[str, str]], y_receipt: dict, freeze: dict) -> dict:
    cfg = _validate_freeze(freeze)
    bands = _validate_y_receipt(y_receipt, freeze)
    _need(bool(rows), "D0-CAL rows are empty")

    for row in rows:
        _need(row.get("dataset_id") == D0_DATASET_ID, "wrong dataset_id in D0-CAL")
        _need(str(row.get("confirmatory_eligible", "")).strip().lower() == "false", "D0-CAL row marked confirmatory eligible")

    contexts = {
        (
            row.get("population_id"),
            row.get("season_id"),
            row.get("fitness_scale_id"),
            row.get("time_horizon_id"),
        )
        for row in rows
    }
    _need(len(contexts) == 1, "D0-CAL contains multiple contexts")
    population_id, season_id, fitness_scale_id, time_horizon_id = next(iter(contexts))
    fctx = freeze["context"]
    _need(population_id == fctx["population_id"], "D0-CAL/freeze population mismatch")
    _need(season_id == fctx["season_id"], "D0-CAL/freeze season mismatch")
    _need(fitness_scale_id == fctx["fitness_scale_id"], "D0-CAL/freeze fitness scale mismatch")
    _need(time_horizon_id == fctx["time_horizon_id"], "D0-CAL/freeze time horizon mismatch")

    by_plant: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    strata: dict[str, str] = {}
    for row in rows:
        plant_id = str(row.get("plant_id", "")).strip()
        treatment = str(row.get("treatment", "")).strip()
        stratum = str(row.get("phenotype_stratum", "")).strip()
        _need(plant_id and treatment and stratum, "D0-CAL row missing identifiers")
        _need(treatment not in by_plant[plant_id], f"duplicate treatment within plant: {plant_id}")
        by_plant[plant_id][treatment] = row
        if plant_id in strata:
            _need(strata[plant_id] == stratum, f"mixed stratum within plant: {plant_id}")
        else:
            strata[plant_id] = stratum

    metric = fctx["primary_y_metric"]
    ant_endpoint = cfg["antagonist_endpoint"]
    poll_endpoint = cfg["pollination_endpoint"]
    low_max = float(bands["low_y_max"])
    high_min = float(bands["high_y_min"])

    natural_ant: list[tuple[float, float, float]] = []
    natural_poll: list[tuple[float, float, float]] = []
    natural_band_failures: list[str] = []

    for plant_id in sorted(by_plant):
        stratum = strata[plant_id]
        treatment = "S_CAL" if stratum == "LOW_Y" else "D_CAL" if stratum == "HIGH_Y" else None
        if treatment is None or treatment not in by_plant[plant_id]:
            continue
        row = by_plant[plant_id][treatment]
        try:
            y = _y_value(row, metric)
            z = _number(row, "exsertion_z")
            ant = _endpoint_value(row, ant_endpoint, pollination=False)
            poll = _endpoint_value(row, poll_endpoint, pollination=True)
        except ValueError:
            continue
        band_ok = (stratum == "LOW_Y" and y <= low_max) or (stratum == "HIGH_Y" and y >= high_min)
        if not band_ok:
            natural_band_failures.append(plant_id)
            continue
        natural_ant.append((y, z, ant))
        natural_poll.append((y, z, poll))

    y2_n = len(natural_ant)
    _need(y2_n == len(natural_poll), "Y2 endpoint completeness mismatch")
    y2_floor_pass = y2_n >= cfg["minimum_y2_n"]
    ant_fit = _ols_y_z(natural_ant) if y2_floor_pass else None
    poll_fit = _ols_y_z(natural_poll) if y2_floor_pass else None

    ant_boot: list[float] = []
    poll_boot: list[float] = []
    ant_valid = 0
    poll_valid = 0
    if ant_fit is not None and poll_fit is not None:
        ant_boot, ant_valid = _bootstrap_beta_y(natural_ant, cfg["seed"], cfg["reps"])
        poll_boot, poll_valid = _bootstrap_beta_y(natural_poll, cfg["seed"] + 1, cfg["reps"])
    min_valid = math.ceil(cfg["reps"] * 0.90)
    bootstrap_ready = ant_valid >= min_valid and poll_valid >= min_valid

    ant_ci = None
    poll_ci = None
    antagonist_pass = False
    pollination_equivalence_pass = False
    if bootstrap_ready:
        ant_ci = _ci(ant_boot, cfg["antagonist_ci_level"])
        poll_ci = _ci(poll_boot, cfg["pollination_ci_level"])
        expected_sign = ANTAGONIST_ENDPOINTS[ant_endpoint][1]
        antagonist_pass = ant_ci[1] < 0 if expected_sign < 0 else ant_ci[0] > 0
        margin = cfg["pollination_margin"]
        pollination_equivalence_pass = poll_ci[0] > -margin and poll_ci[1] < margin

    y2_pass = (
        y2_floor_pass
        and bootstrap_ready
        and antagonist_pass
        and pollination_equivalence_pass
        and not natural_band_failures
    )

    y3_y_diffs: list[float] = []
    y3_z_diffs: list[float] = []
    y3_baseline_band_failures: list[str] = []
    for plant_id in sorted(by_plant):
        if strata[plant_id] != "LOW_Y":
            continue
        treatments = by_plant[plant_id]
        if "D0_CAL" not in treatments or "SHAM_CAL" not in treatments:
            continue
        d0 = treatments["D0_CAL"]
        sham = treatments["SHAM_CAL"]
        try:
            y_d0 = _y_value(d0, metric)
            y_sham = _y_value(sham, metric)
            z_d0 = _number(d0, "exsertion_z")
            z_sham = _number(sham, "exsertion_z")
        except ValueError:
            continue
        if y_sham > low_max:
            y3_baseline_band_failures.append(plant_id)
            continue
        y3_y_diffs.append(y_d0 - y_sham)
        y3_z_diffs.append(z_d0 - z_sham)

    y3_n = len(y3_y_diffs)
    _need(y3_n == len(y3_z_diffs), "Y3 paired completeness mismatch")
    y3_floor_pass = y3_n >= cfg["minimum_y3_n"]
    y_gain_ci = None
    z_shift_ci = None
    y_gain_pass = False
    z_equivalence_pass = False
    if y3_floor_pass:
        y_boot = _bootstrap_mean_difference(y3_y_diffs, cfg["seed"] + 2, cfg["reps"])
        z_boot = _bootstrap_mean_difference(y3_z_diffs, cfg["seed"] + 3, cfg["reps"])
        y_gain_ci = _ci(y_boot, cfg["y_gain_ci_level"])
        z_shift_ci = _ci(z_boot, cfg["z_equivalence_ci_level"])
        y_gain_pass = y_gain_ci[0] > cfg["minimum_y_gain"]
        z_margin = cfg["max_z_shift"]
        z_equivalence_pass = z_shift_ci[0] > -z_margin and z_shift_ci[1] < z_margin

    y3_pass = y3_floor_pass and y_gain_pass and z_equivalence_pass and not y3_baseline_band_failures

    if y2_pass and y3_pass:
        status = "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION"
    elif y2_pass:
        status = "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_OPEN"
    elif y3_pass:
        status = "STRUCTURAL_Y_Y3_PERFORMANCE_INTERVENTION_Y2_OPEN"
    else:
        status = "STRUCTURAL_Y_FUNCTION_NOT_PROMOTED"

    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_FUNCTION_RECEIPT_V1",
        "status": status,
        "context": {
            "system": "Pedicularis rex",
            "population_id": population_id,
            "season_id": season_id,
            "fitness_scale_id": fitness_scale_id,
            "time_horizon_id": time_horizon_id,
            "d0_cal_dataset_id": D0_DATASET_ID,
        },
        "primary_y_metric": metric,
        "y2": {
            "natural_antagonist_endpoint": ant_endpoint,
            "natural_pollination_endpoint": poll_endpoint,
            "complete_n": y2_n,
            "minimum_complete_n": cfg["minimum_y2_n"],
            "natural_band_failure_count": len(natural_band_failures),
            "beta_y_antagonist": ant_fit["beta_y"] if ant_fit else None,
            "beta_y_antagonist_ci": list(ant_ci) if ant_ci else None,
            "antagonist_expected_direction_pass": antagonist_pass,
            "beta_y_pollination": poll_fit["beta_y"] if poll_fit else None,
            "beta_y_pollination_equivalence_ci": list(poll_ci) if poll_ci else None,
            "pollination_beta_y_equivalence_margin": cfg["pollination_margin"],
            "pollination_equivalence_pass": pollination_equivalence_pass,
            "bootstrap_valid_antagonist": ant_valid,
            "bootstrap_valid_pollination": poll_valid,
            "pass": y2_pass,
        },
        "y3": {
            "paired_complete_n": y3_n,
            "minimum_complete_paired_plants": cfg["minimum_y3_n"],
            "baseline_low_y_band_failure_count": len(y3_baseline_band_failures),
            "mean_primary_y_gain": (sum(y3_y_diffs) / y3_n) if y3_n else None,
            "primary_y_gain_ci": list(y_gain_ci) if y_gain_ci else None,
            "minimum_primary_y_gain": cfg["minimum_y_gain"],
            "y_gain_pass": y_gain_pass,
            "mean_exsertion_shift": (sum(y3_z_diffs) / y3_n) if y3_n else None,
            "exsertion_shift_equivalence_ci": list(z_shift_ci) if z_shift_ci else None,
            "max_abs_exsertion_shift": cfg["max_z_shift"],
            "z_equivalence_pass": z_equivalence_pass,
            "pass": y3_pass,
            "interpretation": "FUNCTIONAL_PERFORMANCE_INTERVENTION_NOT_HISTORICAL_ORIGIN",
        },
        "firewall": {
            "d0_cal_units_confirmatory_g3_g5_ineligible": True,
            "natural_y2_and_intervention_y3_kept_distinct": True,
            "no_historical_modularization_claim": True,
        },
        "claim_ceiling": (
            "STRUCTURAL_Y_PREFERENTIAL_LOADING_AND_PERFORMANCE_MANIPULABILITY_AT_MOST; "
            "TRAIT_LEVEL_DIMENSIONAL_RELEASE, HISTORICAL_MODULARIZATION, D0_CONFIRMATORY_QUALIFICATION, R, K, AND_PHI_REMAIN_OPEN"
        ),
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Adjudicate Pedicularis structural-y Y2 preferential loading and Y3 performance intervention")
    parser.add_argument("d0_cal_csv", type=Path)
    parser.add_argument("structural_y_receipt_json", type=Path)
    parser.add_argument("function_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = adjudicate(
        _read_csv(args.d0_cal_csv),
        json.loads(args.structural_y_receipt_json.read_text(encoding="utf-8")),
        json.loads(args.function_freeze_json.read_text(encoding="utf-8")),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
