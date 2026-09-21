from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_calibration_layout.py"
SIMULATOR = ROOT / "scripts" / "simulate_pedicularis_d0_joint_power.py"

spec = importlib.util.spec_from_file_location("ped_cal_gen_joint", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_d0_joint_power", SIMULATOR)
sim = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(sim)


def _calibration_rows() -> list[dict[str, str]]:
    _, rows, _ = gen.generate_layout(
        "ctx1",
        "pop1",
        "2027",
        "FLOWER_TO_MATURE_VIABLE_SEED",
        1729,
    )
    for row in rows:
        i = int(row["plant_id"].rsplit("-", 1)[1])
        t = row["treatment"]

        if t == "D0_CAL":
            row["exsertion_z"] = str(0.300 + 0.0005 * i)
            max_ml = 2.00 + 0.01 * i
            attack = 0.20 + 0.001 * i
            seeds = 12.0 + 0.10 * i
        elif t == "SHAM_CAL":
            row["exsertion_z"] = str(0.302 + 0.0005 * i)
            max_ml = 0.50 + 0.005 * i
            attack = 0.40 + 0.001 * i
            seeds = 11.95 + 0.10 * i
        elif t == "S_CAL":
            row["exsertion_z"] = str(0.301 + 0.0005 * i)
            max_ml = 0.45 + 0.005 * i
            attack = 0.41 + 0.001 * i
            seeds = 12.00 + 0.10 * i
        elif t == "D_CAL":
            row["exsertion_z"] = str(0.35 + 0.0005 * i)
            max_ml = 2.02 + 0.01 * i
            attack = 0.205 + 0.001 * i
            seeds = 13.0 + 0.10 * i
        else:
            row["exsertion_z"] = str(0.35 + 0.0005 * i)
            max_ml = 0.4 + 0.005 * i
            attack = 0.42 + 0.001 * i
            seeds = 11.0 + 0.10 * i

        row["retention_trial1_max_ml"] = str(max_ml - 0.01)
        row["retention_trial2_max_ml"] = str(max_ml + 0.01)
        row["early_attack_prop"] = str(attack)
        row["mature_viable_undamaged_seeds"] = str(seeds)

    return rows


def _compiled() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_Y_D0_PRECISION_INPUT_V2",
        "status": "COMPILED_FROM_FROZEN_MARGINS_AND_INDEPENDENT_CALIBRATION_VARIANCE",
        "defaults": {
            "alpha": 0.05,
            "power": 0.80,
            "joint_qualification_power": 0.80,
            "attrition": 0.0,
        },
        "input_provenance": {
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "confirmatory_dataset_id": "PED_D0_CONFIRM_V1",
            "confirmatory_outcomes_opened": False,
            "margin_freeze_commit": "margin123",
            "q5_route": "NEGLIGIBLE_BURDEN_EQUIVALENCE",
        },
        "endpoints": [
            {
                "endpoint_id": "D0_Q1_Z",
                "kind": "paired_equivalence",
                "sd_diff": 0.01,
                "margin": 0.10,
            },
            {
                "endpoint_id": "D0_Q2_VOLUME",
                "kind": "two_group_equivalence",
                "sd": 0.10,
                "margin": 0.40,
            },
            {
                "endpoint_id": "D0_Q4_WET_EFFECT",
                "kind": "paired_superiority",
                "sd_diff": 0.02,
                "min_effect": 0.10,
                "planning_effect": 0.20,
                "planning_effect_source": "PED_D0_CAL_V1",
                "directional": True,
            },
            {
                "endpoint_id": "D0_Q5_BURDEN_EQ",
                "kind": "paired_equivalence",
                "sd_diff": 0.05,
                "margin": 0.50,
            },
        ],
    }


def _planned() -> dict:
    return {
        "joint_qualification_design": {
            "target_all_pass_power": 0.80,
        },
        "results": [],
    }


def _freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_D0_JOINT_POWER_SIMULATION_FREEZE_V1",
        "status": "D0_JOINT_POWER_SIMULATION_PROSPECTIVELY_FROZEN",
        "context": {
            "system": "Pedicularis rex",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "d0_cal_dataset_id": "PED_D0_CAL_V1",
            "confirmatory_dataset_id": "PED_D0_CONFIRM_V1",
            "margin_freeze_commit": "margin123",
            "confirmatory_outcomes_opened": False,
        },
        "simulation": {
            "model": "WHOLE_PLANT_EMPIRICAL_RESAMPLING_NORMAL_APPROX_ENDPOINT_ADJUDICATION",
            "random_seed": 99173,
            "reps": 1000,
            "minimum_reps": 1000,
            "mc_interval_level": 0.95,
            "target_all_pass_power": 0.80,
            "attrition_source": "COMPILED_PRECISION_INPUT_FROZEN_DEFAULT",
        },
        "field_burden_weights": {
            "low_y_recruit": 3,
            "high_y_recruit": 1,
        },
        "candidate_allocations": [
            {"n_low_recruit": 8, "n_high_recruit": 8},
            {"n_low_recruit": 20, "n_high_recruit": 20},
        ],
        "firewall": {
            "calibration_units_confirmatory_eligible": False,
            "candidate_grid_frozen_before_confirmatory_outcomes": True,
            "simulation_seed_frozen_before_confirmatory_outcomes": True,
            "planning_truths_from_confirmatory_outcomes_forbidden": True,
        },
        "freeze_metadata": {
            "freeze_commit": "joint123",
            "freeze_timestamp": "2027-05-03T00:00:00Z",
        },
    }


def test_joint_simulation_runs_whole_plant_design_and_selects_feasible_candidate() -> None:
    result = sim.simulate_joint_power(
        _calibration_rows(),
        _compiled(),
        _planned(),
        _freeze(),
    )
    assert result["status"] == "JOINT_SIMULATION_DESIGN_FOUND"
    assert result["selected_allocation"] is not None
    assert result["selected_allocation"]["meets_joint_target_by_lower_mc_bound"] is True
    assert result["selected_allocation"]["n_low_recruit"] in {8, 20}
    assert result["selected_allocation"]["n_high_recruit"] in {8, 20}
    assert result["simulation_model"].startswith("WHOLE_PLANT_EMPIRICAL_RESAMPLING")
    assert result["calibration_context"]["population_id"] == "pop1"
    assert set(result["selected_allocation"]["gate_pass_probabilities"]) == {
        "Q1",
        "Q2",
        "Q4",
        "Q5",
    }


def test_joint_simulation_rejects_unfrozen_candidate_grid() -> None:
    freeze = _freeze()
    freeze["firewall"]["candidate_grid_frozen_before_confirmatory_outcomes"] = False
    with pytest.raises(ValueError, match="candidate grid not frozen"):
        sim.simulate_joint_power(
            _calibration_rows(),
            _compiled(),
            _planned(),
            freeze,
        )


def test_joint_simulation_rejects_context_mismatch() -> None:
    freeze = _freeze()
    freeze["context"]["population_id"] = "other"
    with pytest.raises(ValueError, match="joint simulation/precision mismatch"):
        sim.simulate_joint_power(
            _calibration_rows(),
            _compiled(),
            _planned(),
            freeze,
        )


def test_joint_simulation_rejects_target_drift() -> None:
    freeze = _freeze()
    freeze["simulation"]["target_all_pass_power"] = 0.90
    with pytest.raises(ValueError, match="target differs"):
        sim.simulate_joint_power(
            _calibration_rows(),
            _compiled(),
            _planned(),
            freeze,
        )
