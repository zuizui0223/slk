from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "adjudicate_pedicularis_g3_g5_effect.py"
spec = importlib.util.spec_from_file_location("ped_g35_scale_consistency", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _cfg(scale: float = 1.0) -> dict:
    return {
        "context": {
            "context_id": "ctx",
            "population_id": "pop",
            "season_id": "season",
            "fitness_scale_id": "fit",
            "time_horizon_id": "horizon",
        },
        "z_levels": [
            {
                "level_id": "Z1",
                "target_exsertion_z": 1.0 * scale,
                "tolerance": 0.1 * scale,
            },
            {
                "level_id": "Z2",
                "target_exsertion_z": 2.0 * scale,
                "tolerance": 0.1 * scale,
            },
        ],
        "bands": {"low_y_max": 10.0, "high_y_min": 20.0},
    }


def _rows(scale: float = 1.0, baseline_values=(1.0, 1.0)) -> list[dict[str, str]]:
    rows = []
    for index, level in enumerate(_cfg(scale)["z_levels"]):
        target = level["target_exsertion_z"]
        rows.append(
            {
                "dataset_id": module.DECOMP_DATASET,
                "block_role": "DECOMPOSITION_RK",
                "assignment_frozen": "true",
                "g3_g5_eligible": "true",
                "context_id": "ctx",
                "population_id": "pop",
                "season_id": "season",
                "fitness_scale_id": "fit",
                "time_horizon_id": "horizon",
                "world": "S",
                "plant_id": "P1",
                "z_level_id": level["level_id"],
                "baseline_primary_y_value": str(baseline_values[index]),
                "target_exsertion_z": str(target),
                "z_tolerance": str(level["tolerance"]),
                "realized_exsertion_z": str(target),
                "mature_viable_undamaged_seeds": str((index + 1) * scale),
            }
        )
    return rows


def _prepare(rows: list[dict[str, str]], cfg: dict):
    return module._prepare_plants(
        rows,
        module.DECOMP_DATASET,
        "DECOMPOSITION_RK",
        {"S"},
        cfg,
    )


def _reasons(exclusions: list[dict]) -> set[str]:
    return {str(item["reason"]) for item in exclusions}


def test_frozen_target_change_is_rejected_even_in_tiny_z_units():
    scale = 1e-13
    cfg = _cfg(scale)
    rows = _rows(scale)
    rows[0]["target_exsertion_z"] = str(2.0 * cfg["z_levels"][0]["target_exsertion_z"])
    rows[0]["realized_exsertion_z"] = rows[0]["target_exsertion_z"]

    complete, _, exclusions = _prepare(rows, cfg)
    assert complete["S"] == {}
    assert "TARGET_Z_CHANGED" in _reasons(exclusions)


def test_frozen_tolerance_change_is_rejected_even_in_tiny_z_units():
    scale = 1e-13
    cfg = _cfg(scale)
    rows = _rows(scale)
    rows[0]["z_tolerance"] = str(2.0 * cfg["z_levels"][0]["tolerance"])

    complete, _, exclusions = _prepare(rows, cfg)
    assert complete["S"] == {}
    assert "Z_TOLERANCE_CHANGED" in _reasons(exclusions)


def test_identical_frozen_values_are_admitted_after_common_z_rescaling():
    for scale in (1e-13, 1.0, 1e13):
        complete, _, exclusions = _prepare(_rows(scale), _cfg(scale))
        assert exclusions == []
        assert set(complete["S"]) == {"P1"}


def test_baseline_constancy_gate_is_invariant_to_y_units():
    for scale in (1e-13, 1.0, 1e13):
        rows = _rows(1.0, baseline_values=(1.0 * scale, 2.0 * scale))
        complete, _, exclusions = _prepare(rows, _cfg(1.0))
        assert complete["S"] == {}
        assert "BASELINE_Y_NOT_PLANT_CONSTANT" in _reasons(exclusions)

        same = _rows(1.0, baseline_values=(1.5 * scale, 1.5 * scale))
        complete_same, _, exclusions_same = _prepare(same, _cfg(1.0))
        assert exclusions_same == []
        assert set(complete_same["S"]) == {"P1"}


def test_optimizing_z_ids_are_invariant_to_fitness_units():
    levels = [{"level_id": "Z1"}, {"level_id": "Z2"}]
    for scale in (1e-13, 1.0, 1e13):
        plants = {
            "P1": {"Z1": 1.0 * scale, "Z2": 2.0 * scale},
            "P2": {"Z1": 1.0 * scale, "Z2": 2.0 * scale},
        }
        point = module._world_point(plants, levels)
        assert point["optimizing_z_level_ids"] == ["Z2"]

        tied = {
            "P1": {"Z1": 2.0 * scale, "Z2": 2.0 * scale},
            "P2": {"Z1": 2.0 * scale, "Z2": 2.0 * scale},
        }
        tied_point = module._world_point(tied, levels)
        assert tied_point["optimizing_z_level_ids"] == ["Z1", "Z2"]


def test_registered_realized_z_tolerance_remains_a_physical_gate():
    for scale in (1e-13, 1.0, 1e13):
        cfg = _cfg(scale)
        rows = _rows(scale)
        target = cfg["z_levels"][0]["target_exsertion_z"]
        tolerance = cfg["z_levels"][0]["tolerance"]
        rows[0]["realized_exsertion_z"] = str(target + 2.0 * tolerance)

        complete, _, exclusions = _prepare(rows, cfg)
        assert complete["S"] == {}
        assert "REALIZED_Z_OUTSIDE_TOLERANCE" in _reasons(exclusions)


def test_relative_identity_comparison_has_no_absolute_unit_floor():
    assert module._relative_close(0.0, 0.0)
    assert not module._relative_close(1e-13, 0.0)
    assert not module._relative_close(1e-13, 2e-13)
    for scale in (1e-13, 1.0, 1e13):
        assert module._relative_close(scale, scale)
        assert module._relative_close(scale, scale * (1.0 + 5e-15))
