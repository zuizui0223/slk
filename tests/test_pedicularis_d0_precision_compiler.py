from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "scripts" / "compile_pedicularis_d0_precision_input.py"
PLANNER = ROOT / "scripts" / "plan_pedicularis_y_d0_precision.py"
MARGIN_TEMPLATE = ROOT / "data" / "PEDICULARIS_D0_MARGIN_FREEZE_TEMPLATE_V1.json"
VARIANCE_TEMPLATE = ROOT / "data" / "PEDICULARIS_D0_VARIANCE_INPUT_TEMPLATE_V1.json"

spec = importlib.util.spec_from_file_location("ped_d0_compile", COMPILER)
compiler = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(compiler)

spec2 = importlib.util.spec_from_file_location("ped_y_d0_plan", PLANNER)
planner = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(planner)


def _margin(q5_route: str = "NEGLIGIBLE_BURDEN_EQUIVALENCE") -> dict:
    m = json.loads(MARGIN_TEMPLATE.read_text())
    m["context"].update(
        {
            "population_id": "pop1",
            "season_id": "2027",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_CONFIRM_V1",
            "q5_route": q5_route,
        }
    )
    m["freeze_metadata"] = {
        "slk_source_commit": "abc123",
        "freeze_commit": "def456",
        "freeze_timestamp": "2027-05-01T00:00:00Z",
    }
    for endpoint in m["endpoints"]:
        endpoint_id = endpoint["endpoint_id"]
        if endpoint["criterion_type"] != "EXACT_IDENTITY":
            endpoint["value"] = 0.5
        endpoint["margin_basis"] = "independent biological or decision-invariance calibration"
        endpoint["source_reference"] = ["CALIBRATION:PED_D0_CAL_V1"]
        endpoint["biological_rationale"] = "preserves the registered biological interpretation"
        endpoint["calibration_dataset_id"] = "PED_D0_CAL_V1"
        endpoint["frozen_before_confirmatory_outcomes"] = True
        if endpoint_id == "D0_Q4_WET_EFFECT":
            endpoint["source_type"] = "BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION"
        elif endpoint_id in {"D0_Q5_BURDEN_EQ", "D0_Q5_BURDEN_PRECISION"}:
            endpoint["source_type"] = "DOWNSTREAM_DECISION_INVARIANCE"
        elif endpoint_id == "D0_Q6_HORIZON":
            endpoint["source_type"] = "DESIGN_INVARIANCE"
            endpoint["calibration_dataset_id"] = None
        else:
            endpoint["source_type"] = "FUNCTIONAL_INVARIANCE"
    return m


def _variance() -> dict:
    v = json.loads(VARIANCE_TEMPLATE.read_text())
    v["status"] = "INDEPENDENT_CALIBRATION_VARIANCE_READY"
    v["context"].update(
        {
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_CONFIRM_V1",
        }
    )
    for endpoint in v["endpoints"]:
        endpoint["value"] = 1.0
        endpoint["meets_registered_floor"] = True
    return v


def _ids(payload: dict) -> set[str]:
    return {x["endpoint_id"] for x in payload["endpoints"]}


def test_compiled_equivalence_route_is_accepted_by_precision_planner() -> None:
    compiled = compiler.compile_precision_input(_margin(), _variance())
    assert compiled["schema_version"] == "SLK_PEDICULARIS_Y_D0_PRECISION_INPUT_V2"
    assert compiled["input_provenance"]["time_horizon_id"] == "FLOWER_TO_MATURE_VIABLE_SEED"
    assert "D0_Q5_BURDEN_EQ" in _ids(compiled)
    assert "D0_Q5_BURDEN_PRECISION" not in _ids(compiled)
    planned = planner.plan_manifest(compiled)
    assert planned["status"] == "PLANNING_ONLY_NOT_A_BIOLOGICAL_RECEIPT"
    assert planned["maxima_by_allocation_unit"]


def test_compiled_adjustment_route_uses_burden_precision_not_equivalence() -> None:
    compiled = compiler.compile_precision_input(_margin("MEASURED_BURDEN_ADJUSTMENT"), _variance())
    assert "D0_Q5_BURDEN_PRECISION" in _ids(compiled)
    assert "D0_Q5_BURDEN_EQ" not in _ids(compiled)
    burden = next(x for x in compiled["endpoints"] if x["endpoint_id"] == "D0_Q5_BURDEN_PRECISION")
    assert burden["kind"] == "mean_precision"
    assert burden["half_width"] == 0.5


def test_margin_and_variance_contexts_must_match() -> None:
    variance = _variance()
    variance["context"]["population_id"] = "pop2"
    with pytest.raises(ValueError, match="context mismatch"):
        compiler.compile_precision_input(_margin(), variance)


def test_margin_and_variance_horizons_must_match() -> None:
    variance = _variance()
    variance["context"]["time_horizon_id"] = "OTHER_HORIZON"
    with pytest.raises(ValueError, match="time_horizon_id"):
        compiler.compile_precision_input(_margin(), variance)


def test_missing_active_variance_is_rejected() -> None:
    variance = _variance()
    endpoint = next(x for x in variance["endpoints"] if x["endpoint_id"] == "D0_Q2_VOLUME")
    endpoint["value"] = None
    with pytest.raises(ValueError, match="missing/invalid variance input"):
        compiler.compile_precision_input(_margin(), variance)


def test_wrong_variance_kind_is_rejected() -> None:
    variance = _variance()
    endpoint = next(x for x in variance["endpoints"] if x["endpoint_id"] == "D0_Q2_DURATION")
    endpoint["variance_kind"] = "sd_diff"
    with pytest.raises(ValueError, match="expected sd"):
        compiler.compile_precision_input(_margin(), variance)


def test_variance_must_come_from_registered_calibration_dataset() -> None:
    variance = _variance()
    endpoint = next(x for x in variance["endpoints"] if x["endpoint_id"] == "D0_Q3_POLLEN")
    endpoint["calibration_dataset_id"] = "UNREGISTERED_PILOT"
    with pytest.raises(ValueError, match="not a registered calibration dataset"):
        compiler.compile_precision_input(_margin(), variance)


def test_opened_confirmatory_outcomes_block_compilation() -> None:
    variance = _variance()
    variance["context"]["confirmatory_outcomes_opened"] = True
    with pytest.raises(ValueError, match="opened confirmatory outcomes"):
        compiler.compile_precision_input(_margin(), variance)


def test_incomplete_variance_receipt_is_rejected() -> None:
    variance = _variance()
    variance["status"] = "INDEPENDENT_CALIBRATION_VARIANCE_INCOMPLETE"
    with pytest.raises(ValueError, match="variance receipt is not ready"):
        compiler.compile_precision_input(_margin(), variance)


def test_endpoint_below_registered_pilot_floor_is_rejected() -> None:
    variance = _variance()
    endpoint = next(x for x in variance["endpoints"] if x["endpoint_id"] == "D0_Q3_POLLEN")
    endpoint["meets_registered_floor"] = False
    with pytest.raises(ValueError, match="below registered calibration floor"):
        compiler.compile_precision_input(_margin(), variance)
