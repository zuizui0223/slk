from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_calibration_layout.py"
VALIDATOR = ROOT / "scripts" / "validate_pedicularis_calibration_layout.py"

spec = importlib.util.spec_from_file_location("ped_cal_gen", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_cal_validate", VALIDATOR)
val = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(val)


def _layout(seed: int = 1729):
    return gen.generate_layout("ctx1", "pop1", "season1", "FLOWER_TO_MATURE_VIABLE_SEED", seed)


def test_default_layout_has_registered_sampling_floors() -> None:
    y_rows, d0_rows, meta = _layout()
    assert len(y_rows) == 108
    assert len({r["plant_id"] for r in y_rows}) == 36
    assert len(d0_rows) == 120
    assert len({r["plant_id"] for r in d0_rows}) == 48
    assert meta["d0_cal"]["low_y_plants"] == 24
    assert meta["d0_cal"]["high_y_plants"] == 24
    assert meta["fitness_scale_id"] == "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
    assert meta["time_horizon_id"] == "FLOWER_TO_MATURE_VIABLE_SEED"


def test_each_d0_plant_gets_complete_registered_treatment_set() -> None:
    _, d0_rows, _ = _layout()
    by_plant = {}
    for row in d0_rows:
        by_plant.setdefault(row["plant_id"], []).append(row)
    for plant_id, rows in by_plant.items():
        treatments = {r["treatment"] for r in rows}
        if plant_id.startswith("D0L-"):
            assert treatments == {"S_CAL", "SHAM_CAL", "D0_CAL"}
        else:
            assert treatments == {"D_CAL", "D_DRAIN_CAL"}


def test_randomization_is_reproducible_for_same_seed() -> None:
    _, d1, _ = _layout(9)
    _, d2, _ = _layout(9)
    assert [(r["plant_id"], r["flower_slot"], r["treatment"]) for r in d1] == [
        (r["plant_id"], r["flower_slot"], r["treatment"]) for r in d2
    ]


def test_different_seed_changes_at_least_one_assignment() -> None:
    _, d1, _ = _layout(9)
    _, d2, _ = _layout(10)
    assert [(r["plant_id"], r["flower_slot"], r["treatment"]) for r in d1] != [
        (r["plant_id"], r["flower_slot"], r["treatment"]) for r in d2
    ]


def test_generated_layout_passes_validator() -> None:
    y_rows, d0_rows, _ = _layout()
    result = val.validate_rows(y_rows, d0_rows)
    assert result["status"] == "CALIBRATION_LAYOUT_VALIDATED"
    assert result["y_cal"]["independent_plants"] == 36
    assert result["d0_cal"]["low_y_plants"] == 24
    assert result["d0_cal"]["high_y_plants"] == 24
    assert result["time_horizon_id"] == "FLOWER_TO_MATURE_VIABLE_SEED"


def test_missing_low_y_treatment_fails_closed() -> None:
    y_rows, d0_rows, _ = _layout()
    broken = [
        row for row in d0_rows
        if not (row["plant_id"] == "D0L-001" and row["treatment"] == "D0_CAL")
    ]
    with pytest.raises(ValueError, match="LOW-Y treatment set incomplete"):
        val.validate_rows(y_rows, broken)


def test_confirmatory_eligible_calibration_row_is_rejected() -> None:
    y_rows, d0_rows, _ = _layout()
    broken = copy.deepcopy(d0_rows)
    broken[0]["confirmatory_eligible"] = "true"
    with pytest.raises(ValueError, match="confirmatory eligible"):
        val.validate_rows(y_rows, broken)


def test_calibration_cohorts_must_have_disjoint_plant_ids() -> None:
    y_rows, d0_rows, _ = _layout()
    broken = copy.deepcopy(d0_rows)
    old = broken[0]["plant_id"]
    for row in broken:
        if row["plant_id"] == old:
            row["plant_id"] = "YCAL-001"
            row["flower_id"] = row["flower_id"].replace(old, "YCAL-001")
    with pytest.raises(ValueError, match="plant IDs overlap"):
        val.validate_rows(y_rows, broken)


def test_context_mismatch_fails_closed() -> None:
    y_rows, d0_rows, _ = _layout()
    broken = copy.deepcopy(d0_rows)
    for row in broken:
        row["season_id"] = "season2"
    with pytest.raises(ValueError, match="context mismatch"):
        val.validate_rows(y_rows, broken)


def test_time_horizon_mismatch_fails_closed() -> None:
    y_rows, d0_rows, _ = _layout()
    broken = copy.deepcopy(d0_rows)
    for row in broken:
        row["time_horizon_id"] = "OTHER_HORIZON"
    with pytest.raises(ValueError, match="context mismatch"):
        val.validate_rows(y_rows, broken)
