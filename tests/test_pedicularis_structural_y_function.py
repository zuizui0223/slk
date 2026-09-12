from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_calibration_layout.py"
ADJUDICATOR = ROOT / "scripts" / "adjudicate_pedicularis_structural_y_function.py"

spec = importlib.util.spec_from_file_location("ped_cal_gen_func", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_y_func", ADJUDICATOR)
func = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(func)


def _y_receipt() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1",
        "status": "STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED",
        "context": {
            "system": "Pedicularis rex",
            "context_id": "ctx1",
            "population_id": "pop1",
            "season_id": "2027",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "y_cal_dataset_id": "PED_Y_CAL_V1",
        },
        "primary_y_metric": "RETENTION_MEAN_MAX_ML",
        "band_freeze": {
            "low_y_max": 2.0,
            "high_y_min": 3.0,
            "dynamic_range_pass": True,
            "recruitment_authorized_for_disjoint_d0_cal": True,
        },
    }


def _freeze() -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_STRUCTURAL_Y_FUNCTION_FREEZE_V1",
        "status": "FROZEN_CANDIDATE",
        "context": {
            "system": "Pedicularis rex",
            "population_id": "pop1",
            "season_id": "2027",
            "y_cal_dataset_id": "PED_Y_CAL_V1",
            "d0_cal_dataset_id": "PED_D0_CAL_V1",
            "structural_y_receipt_id": "PED_STRUCTURAL_Y_RECEIPT_POP1_2027_V1",
            "primary_y_metric": "RETENTION_MEAN_MAX_ML",
            "fitness_scale_id": "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER",
            "time_horizon_id": "FLOWER_TO_MATURE_VIABLE_SEED",
            "frozen_before_d0_cal_outcomes": True,
        },
        "y2": {
            "natural_antagonist_endpoint": "EARLY_ATTACK_PROP",
            "allowed_antagonist_endpoints": [
                "EARLY_ATTACK_PROP",
                "SEED_PREDATION_PROP",
                "MATURE_VIABLE_UNDAMAGED_SEEDS",
            ],
            "natural_pollination_endpoint": "POLLEN_RECEIPT_GRAINS",
            "allowed_pollination_endpoints": [
                "VISIT_RATE_PER_MIN",
                "POLLEN_RECEIPT_GRAINS",
                "INITIAL_SEED_SET_PROP",
            ],
            "pollination_beta_y_equivalence_margin": 0.20,
            "minimum_complete_n": 48,
            "antagonist_ci_level": 0.95,
            "pollination_equivalence_ci_level": 0.90,
            "control_coordinate": "EXSERTION_Z",
            "natural_comparison_rows": "LOW_Y_S_CAL_PLUS_HIGH_Y_D_CAL",
        },
        "y3": {
            "intervention_comparison": "LOW_Y_D0_CAL_MINUS_SHAM_CAL",
            "minimum_primary_y_gain": 0.50,
            "max_abs_exsertion_shift": 0.01,
            "y_gain_ci_level": 0.95,
            "z_equivalence_ci_level": 0.90,
            "minimum_complete_paired_plants": 24,
            "interpretation": "FUNCTIONAL_PERFORMANCE_INTERVENTION_NOT_HISTORICAL_ORIGIN",
        },
        "bootstrap": {
            "seed": 2027,
            "reps": 2000,
            "minimum_reps": 2000,
            "resampling_unit": "INDEPENDENT_PLANT",
        },
        "firewall": {
            "endpoint_selection_after_outcomes_forbidden": True,
            "pollination_margin_from_nonsignificance_forbidden": True,
            "y_gain_threshold_from_observed_d0_effect_forbidden": True,
            "z_margin_from_observed_d0_effect_forbidden": True,
            "d0_cal_units_confirmatory_g3_g5_ineligible": True,
            "natural_y2_and_intervention_y3_kept_distinct": True,
        },
        "freeze_metadata": {
            "slk_source_commit": "abc123",
            "freeze_commit": "def456",
            "freeze_timestamp": "2027-05-01T00:00:00Z",
        },
    }


def _completed_rows() -> list[dict[str, str]]:
    _, rows, _ = gen.generate_layout(
        "ctx1", "pop1", "2027", "FLOWER_TO_MATURE_VIABLE_SEED", 1729
    )
    out = copy.deepcopy(rows)
    for row in out:
        i = int(row["plant_id"].rsplit("-", 1)[1])
        t = row["treatment"]
        stratum = row["phenotype_stratum"]

        # Natural LOW-Y and HIGH-Y states remain inside the frozen Y-CAL bands.
        if stratum == "LOW_Y":
            natural_y = 1.20 + 0.015 * i
        else:
            natural_y = 3.40 + 0.020 * i

        if t == "D0_CAL":
            y = 3.30 + 0.018 * i
        elif t == "D_DRAIN_CAL":
            y = 1.00 + 0.010 * i
        else:
            y = natural_y

        row["retention_trial1_max_ml"] = str(y - 0.01 * (i % 3))
        row["retention_trial2_max_ml"] = str(y + 0.01 * ((i + 1) % 3))

        # z varies within both strata rather than serving as a group label.
        z = 0.28 + 0.004 * (i % 7) + 0.0007 * i
        if t == "D0_CAL":
            z += 0.001 + 0.00002 * i
        elif t == "SHAM_CAL":
            z += 0.0002 * (i % 2)
        row["exsertion_z"] = str(z)

        # Natural structural y preferentially loads on antagonist protection.
        attack = 0.72 - 0.11 * y + 0.10 * z + 0.004 * ((i % 5) - 2)
        row["early_attack_prop"] = str(max(0.01, min(0.95, attack)))
        row["seed_predation_prop"] = str(max(0.01, min(0.95, attack + 0.08)))
        row["mature_viable_undamaged_seeds"] = str(9.0 + 2.2 * y - 1.0 * z + 0.1 * (i % 4))

        # Pollination depends on z but has negligible y loading.
        row["pollen_receipt_grains"] = str(12.0 + 18.0 * z + 0.02 * y + 0.08 * ((i % 6) - 2.5))
        row["initial_seed_set_prop"] = str(0.30 + 0.20 * z + 0.001 * y)
        row["pollinator_observation_minutes"] = "10"
        row["legitimate_visits"] = str(3 + (i % 5))
    return out


def test_y2_preferential_loading_and_y3_performance_intervention_both_pass() -> None:
    result = func.adjudicate(_completed_rows(), _y_receipt(), _freeze())
    assert result["status"] == "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION"
    assert result["y2"]["complete_n"] == 48
    assert result["y2"]["antagonist_expected_direction_pass"] is True
    assert result["y2"]["pollination_equivalence_pass"] is True
    assert result["y2"]["pass"] is True
    assert result["y3"]["paired_complete_n"] == 24
    assert result["y3"]["y_gain_pass"] is True
    assert result["y3"]["z_equivalence_pass"] is True
    assert result["y3"]["pass"] is True


def test_pollination_contamination_blocks_y2_promotion() -> None:
    rows = _completed_rows()
    for row in rows:
        if row["treatment"] in {"S_CAL", "D_CAL"}:
            y = (
                float(row["retention_trial1_max_ml"])
                + float(row["retention_trial2_max_ml"])
            ) / 2
            z = float(row["exsertion_z"])
            row["pollen_receipt_grains"] = str(10.0 + 18.0 * z + 1.2 * y)
    result = func.adjudicate(rows, _y_receipt(), _freeze())
    assert result["y2"]["pollination_equivalence_pass"] is False
    assert result["y2"]["pass"] is False
    assert result["status"] != "STRUCTURAL_Y_Y2_PREFERENTIAL_LOADING_Y3_PERFORMANCE_INTERVENTION"


def test_exsertion_contamination_blocks_y3_intervention() -> None:
    rows = _completed_rows()
    for row in rows:
        if row["phenotype_stratum"] == "LOW_Y" and row["treatment"] == "D0_CAL":
            row["exsertion_z"] = str(float(row["exsertion_z"]) + 0.06)
    result = func.adjudicate(rows, _y_receipt(), _freeze())
    assert result["y3"]["z_equivalence_pass"] is False
    assert result["y3"]["pass"] is False


def test_primary_y_metric_must_match_y_receipt() -> None:
    f = _freeze()
    f["context"]["primary_y_metric"] = "RETENTION_MEAN_HALF_LIFE_MIN"
    with pytest.raises(ValueError, match="primary y metric mismatch"):
        func.adjudicate(_completed_rows(), _y_receipt(), f)


def test_structural_y_receipt_must_be_ready() -> None:
    receipt = _y_receipt()
    receipt["status"] = "STRUCTURAL_Y_CALIBRATION_COMPLETE_RANGE_UNRESOLVED"
    with pytest.raises(ValueError, match="not ready"):
        func.adjudicate(_completed_rows(), receipt, _freeze())


def test_d0_calibration_row_cannot_be_confirmatory_eligible() -> None:
    rows = _completed_rows()
    rows[0]["confirmatory_eligible"] = "true"
    with pytest.raises(ValueError, match="confirmatory eligible"):
        func.adjudicate(rows, _y_receipt(), _freeze())


def test_bootstrap_is_deterministic_under_frozen_seed() -> None:
    r1 = func.adjudicate(_completed_rows(), _y_receipt(), _freeze())
    r2 = func.adjudicate(_completed_rows(), _y_receipt(), _freeze())
    assert r1["y2"]["beta_y_antagonist_ci"] == r2["y2"]["beta_y_antagonist_ci"]
    assert r1["y2"]["beta_y_pollination_equivalence_ci"] == r2["y2"]["beta_y_pollination_equivalence_ci"]
    assert r1["y3"]["primary_y_gain_ci"] == r2["y3"]["primary_y_gain_ci"]


def test_one_natural_band_failure_breaks_registered_48_plant_y2_floor() -> None:
    rows = _completed_rows()
    target = next(
        row for row in rows
        if row["plant_id"] == "D0H-001" and row["treatment"] == "D_CAL"
    )
    target["retention_trial1_max_ml"] = "1.5"
    target["retention_trial2_max_ml"] = "1.5"
    result = func.adjudicate(rows, _y_receipt(), _freeze())
    assert result["y2"]["complete_n"] == 47
    assert result["y2"]["natural_band_failure_count"] == 1
    assert result["y2"]["pass"] is False
