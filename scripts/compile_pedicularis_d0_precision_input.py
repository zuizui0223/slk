from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path


VARIANCE_SCHEMA = "SLK_PEDICULARIS_D0_VARIANCE_INPUT_V1"
VARIANCE_READY_STATUS = "INDEPENDENT_CALIBRATION_VARIANCE_READY"
OUTPUT_SCHEMA = "SLK_PEDICULARIS_Y_D0_PRECISION_INPUT_V2"

PAIR_EQ_IDS = {
    "D0_Q1_Z",
    "D0_Q1_OPENING",
    "D0_Q1_STIGMA",
    "D0_Q1_ORIENTATION",
    "D0_Q1_DAMAGE",
    "D0_Q3_VISIT",
    "D0_Q3_POLLEN",
    "D0_Q3_INITIAL_SEED",
    "D0_Q4_DRY_RESIDUAL",
    "D0_Q5_BURDEN_EQ",
}
TWO_GROUP_EQ_IDS = {
    "D0_Q2_VOLUME",
    "D0_Q2_DURATION",
    "D0_Q2_COVERAGE",
    "D0_Q2_PROTECTION",
}
WET_EFFECT_ID = "D0_Q4_WET_EFFECT"
BURDEN_PRECISION_ID = "D0_Q5_BURDEN_PRECISION"
HORIZON_ID = "D0_Q6_HORIZON"
EXPECTED_VARIANCE_IDS = PAIR_EQ_IDS | TWO_GROUP_EQ_IDS | {
    WET_EFFECT_ID,
    BURDEN_PRECISION_ID,
}


def _load_margin_validator():
    path = Path(__file__).with_name("validate_pedicularis_d0_margin_freeze.py")
    spec = importlib.util.spec_from_file_location("ped_d0_margin_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate


validate_margin = _load_margin_validator()


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _positive_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0
    )


def _endpoint_map(payload: dict) -> dict[str, dict]:
    endpoints = payload.get("endpoints", [])
    _need(isinstance(endpoints, list) and endpoints, "variance endpoints missing")
    ids = [x.get("endpoint_id") for x in endpoints]
    _need(len(ids) == len(set(ids)), "duplicate variance endpoint_id")
    _need(set(ids) == EXPECTED_VARIANCE_IDS, "variance endpoint inventory mismatch")
    return {x["endpoint_id"]: x for x in endpoints}


def _margin_map(payload: dict) -> dict[str, dict]:
    return {x["endpoint_id"]: x for x in payload["endpoints"]}


def compile_precision_input(margin: dict, variance: dict) -> dict:
    margin_result = validate_margin(margin)
    _need(variance.get("schema_version") == VARIANCE_SCHEMA, "wrong variance schema")
    _need(variance.get("status") == VARIANCE_READY_STATUS, "variance receipt is not ready at the registered calibration floor")

    vctx = variance.get("context", {})
    mctx = margin["context"]
    for key in (
        "system",
        "population_id",
        "season_id",
        "fitness_scale_id",
        "time_horizon_id",
        "y_cal_dataset_id",
        "d0_cal_dataset_id",
        "confirmatory_dataset_id",
    ):
        _need(vctx.get(key) == mctx.get(key), f"margin/variance context mismatch: {key}")
    _need(vctx.get("confirmatory_outcomes_opened") is False, "variance inputs opened confirmatory outcomes")

    defaults = variance.get("planner_defaults", {})
    for key in ("alpha", "power"):
        value = defaults.get(key)
        _need(isinstance(value, (int, float)) and 0 < float(value) < 1, f"bad planner default: {key}")
    attrition = defaults.get("attrition")
    _need(isinstance(attrition, (int, float)) and 0 <= float(attrition) < 1, "bad planner default: attrition")

    vmap = _endpoint_map(variance)
    mmap = _margin_map(margin)
    confirmatory_id = mctx["confirmatory_dataset_id"]
    registered_calibration_ids = {mctx["y_cal_dataset_id"], mctx["d0_cal_dataset_id"]}
    active_margin_ids = [x for x in margin_result["validated_endpoints"] if x != HORIZON_ID]
    planner_endpoints: list[dict] = []

    for endpoint_id in active_margin_ids:
        _need(endpoint_id in vmap, f"variance missing for active endpoint: {endpoint_id}")
        v = vmap[endpoint_id]
        m = mmap[endpoint_id]
        _need(v.get("meets_registered_floor") is True, f"variance endpoint below registered calibration floor: {endpoint_id}")
        _need(v.get("analysis_unit") == "independent_plant", f"wrong analysis unit: {endpoint_id}")
        calibration_id = v.get("calibration_dataset_id")
        _need(calibration_id in registered_calibration_ids, f"variance source is not a registered calibration dataset: {endpoint_id}")
        _need(calibration_id != confirmatory_id, f"variance dataset reuses confirmatory units: {endpoint_id}")
        sd_value = v.get("value")
        _need(_positive_number(sd_value), f"missing/invalid variance input: {endpoint_id}")
        margin_value = m.get("value")
        _need(_positive_number(margin_value), f"missing/invalid frozen margin: {endpoint_id}")

        base = {
            "endpoint_id": endpoint_id,
            "margin_endpoint_id": endpoint_id,
            "variance_source": calibration_id,
            "margin_source_type": m.get("source_type"),
        }
        if endpoint_id in PAIR_EQ_IDS:
            _need(v.get("variance_kind") == "sd_diff", f"expected sd_diff: {endpoint_id}")
            base.update({"kind": "paired_equivalence", "sd_diff": sd_value, "margin": margin_value})
        elif endpoint_id in TWO_GROUP_EQ_IDS:
            _need(v.get("variance_kind") == "sd", f"expected sd: {endpoint_id}")
            base.update({"kind": "two_group_equivalence", "sd": sd_value, "margin": margin_value})
        elif endpoint_id == WET_EFFECT_ID:
            _need(v.get("variance_kind") == "sd_diff", f"expected sd_diff: {endpoint_id}")
            base.update({"kind": "paired_superiority", "sd_diff": sd_value, "min_effect": margin_value, "directional": True})
        elif endpoint_id == BURDEN_PRECISION_ID:
            _need(v.get("variance_kind") == "sd_diff", f"expected sd_diff: {endpoint_id}")
            base.update({"kind": "mean_precision", "sd": sd_value, "half_width": margin_value})
        else:
            raise ValueError(f"no precision mapping for active endpoint: {endpoint_id}")
        planner_endpoints.append(base)

    return {
        "schema_version": OUTPUT_SCHEMA,
        "status": "COMPILED_FROM_FROZEN_MARGINS_AND_INDEPENDENT_CALIBRATION_VARIANCE",
        "defaults": {
            "alpha": float(defaults["alpha"]),
            "power": float(defaults["power"]),
            "attrition": float(defaults["attrition"]),
        },
        "input_provenance": {
            "population_id": mctx["population_id"],
            "season_id": mctx["season_id"],
            "fitness_scale_id": mctx["fitness_scale_id"],
            "time_horizon_id": mctx["time_horizon_id"],
            "y_cal_dataset_id": mctx["y_cal_dataset_id"],
            "d0_cal_dataset_id": mctx["d0_cal_dataset_id"],
            "confirmatory_dataset_id": confirmatory_id,
            "confirmatory_outcomes_opened": False,
            "margin_freeze_commit": margin["freeze_metadata"]["freeze_commit"],
            "q5_route": margin_result["q5_route"],
        },
        "endpoints": planner_endpoints,
        "notes": "Compatible with plan_pedicularis_y_d0_precision.py. Frozen biological margins and independent calibration variance remain separate inputs; this compiler only joins them.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile frozen Pedicularis D0 margins and calibration variance into precision-planner input")
    parser.add_argument("margin_manifest", type=Path)
    parser.add_argument("variance_manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    margin = json.loads(args.margin_manifest.read_text())
    variance = json.loads(args.variance_manifest.read_text())
    result = compile_precision_input(margin, variance)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
