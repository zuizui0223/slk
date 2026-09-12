from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_pedicularis_calibration_layout.py"
SUMMARIZER = ROOT / "scripts" / "summarize_pedicularis_d0_calibration_variance.py"

spec = importlib.util.spec_from_file_location("ped_cal_gen_var", GENERATOR)
gen = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(gen)

spec2 = importlib.util.spec_from_file_location("ped_d0_var", SUMMARIZER)
summary = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(summary)


def _plant_index(plant_id: str) -> int:
    return int(plant_id.rsplit("-", 1)[1])


def _completed_rows() -> list[dict[str, str]]:
    _, rows, _ = gen.generate_layout("ctx1", "pop1", "2027", "FLOWER_TO_MATURE_VIABLE_SEED", 1729)
    out = copy.deepcopy(rows)
    treatment_offset = {"S_CAL": 0.0, "SHAM_CAL": 0.2, "D0_CAL": 0.5, "D_CAL": 0.55, "D_DRAIN_CAL": 0.1}
    for row in out:
        i = _plant_index(row["plant_id"])
        t = row["treatment"]
        o = treatment_offset[t]
        row["exsertion_z"] = str(0.30 + 0.0005 * i + o * 0.002 * i)
        row["opening_width_mm"] = str(4.0 + 0.01 * i + o * 0.02 * i)
        row["stigma_position_mm"] = str(2.0 + 0.005 * i + o * 0.01 * i)
        row["orientation_deg"] = str(20.0 + 0.5 * i + o * 0.4 * i)
        row["mechanical_damage_post_prop"] = str(0.01 + 0.0002 * i + o * 0.0003 * i)

        if t in {"D0_CAL", "D_CAL"}:
            max_ml = 2.0 + 0.02 * i + (0.08 if t == "D_CAL" else 0.0)
            half_life = 35.0 + 0.4 * i + (1.0 if t == "D_CAL" else 0.0)
            protected = 0.70 + 0.002 * i + (0.01 if t == "D_CAL" else 0.0)
        else:
            max_ml = 0.5 + 0.005 * i
            half_life = 8.0 + 0.1 * i
            protected = 0.20 + 0.001 * i
        row["retention_trial1_max_ml"] = str(max_ml)
        row["retention_trial2_max_ml"] = str(max_ml + 0.03 + 0.0005 * i)
        row["retention_trial1_half_life_min"] = str(half_life)
        row["retention_trial2_half_life_min"] = str(half_life + 0.5 + 0.01 * i)
        row["retention_trial1_protected_fraction"] = str(protected)
        row["retention_trial2_protected_fraction"] = str(min(0.99, protected + 0.01))

        row["pollinator_observation_minutes"] = "10"
        visit_base = 4 + (i % 5)
        visits = visit_base + ((i % 3) if t == "D0_CAL" else (i % 2) if t == "SHAM_CAL" else 0)
        row["legitimate_visits"] = str(visits)
        row["pollen_receipt_grains"] = str(10.0 + 0.3 * i + o * 0.12 * i)
        row["initial_seed_set_prop"] = str(0.30 + 0.002 * i + o * 0.001 * i)

        if t == "S_CAL":
            attack = 0.42 + 0.0010 * i
        elif t == "SHAM_CAL":
            attack = 0.40 + 0.0015 * i
        elif t == "D0_CAL":
            attack = 0.20 + 0.0005 * i
        elif t == "D_CAL":
            attack = 0.21 + 0.0008 * i
        else:
            attack = 0.43 + 0.0012 * i
        row["early_attack_prop"] = str(attack)
        row["seed_predation_prop"] = str(min(0.95, attack + 0.08))

        if t == "S_CAL":
            seeds = 12.0 + 0.20 * i
        elif t == "SHAM_CAL":
            seeds = 11.7 + 0.15 * i
        elif t == "D0_CAL":
            seeds = 15.0 + 0.25 * i
        elif t == "D_CAL":
            seeds = 14.8 + 0.22 * i
        else:
            seeds = 11.0 + 0.18 * i
        row["mature_viable_undamaged_seeds"] = str(seeds)
    return out


def _endpoint(receipt: dict, endpoint_id: str) -> dict:
    return next(x for x in receipt["endpoints"] if x["endpoint_id"] == endpoint_id)


def test_complete_registered_calibration_produces_ready_variance_receipt() -> None:
    receipt = summary.summarize(_completed_rows(), "PED_D0_CONFIRM_V1")
    assert receipt["status"] == "INDEPENDENT_CALIBRATION_VARIANCE_READY"
    assert receipt["source_counts"] == {"low_y_plants": 24, "high_y_plants": 24}
    assert receipt["context"]["fitness_scale_id"] == "UNDAMAGED_MATURE_VIABLE_SEEDS_PER_FOCAL_FLOWER"
    assert receipt["context"]["time_horizon_id"] == "FLOWER_TO_MATURE_VIABLE_SEED"
    assert len(receipt["endpoints"]) == 16
    assert all(x["meets_registered_floor"] for x in receipt["endpoints"])
    assert all(x["value"] > 0 for x in receipt["endpoints"])


def test_q4_dry_residual_uses_sham_minus_no_apparatus_s() -> None:
    receipt = summary.summarize(_completed_rows(), "PED_D0_CONFIRM_V1")
    dry = _endpoint(receipt, "D0_Q4_DRY_RESIDUAL")
    assert dry["contrast"] == "SHAM_CAL_MINUS_S_CAL"
    assert dry["variance_kind"] == "sd_diff"


def test_visitation_variance_uses_rate_not_raw_count() -> None:
    receipt = summary.summarize(_completed_rows(), "PED_D0_CONFIRM_V1")
    visit = _endpoint(receipt, "D0_Q3_VISIT")
    assert visit["raw_endpoint"] == "visit_rate_per_min"
    assert visit["analysis_n"] == 24


def test_q2_variance_is_pooled_across_d0_and_natural_d_plants() -> None:
    receipt = summary.summarize(_completed_rows(), "PED_D0_CONFIRM_V1")
    volume = _endpoint(receipt, "D0_Q2_VOLUME")
    assert volume["variance_kind"] == "sd"
    assert volume["analysis_n_group_d0"] == 24
    assert volume["analysis_n_group_d"] == 24
    assert volume["contrast"] == "D0_CAL_VERSUS_D_CAL"


def test_missing_one_required_measurement_marks_receipt_incomplete() -> None:
    rows = _completed_rows()
    target = next(r for r in rows if r["plant_id"] == "D0L-001" and r["treatment"] == "D0_CAL")
    target["pollen_receipt_grains"] = ""
    receipt = summary.summarize(rows, "PED_D0_CONFIRM_V1")
    pollen = _endpoint(receipt, "D0_Q3_POLLEN")
    assert pollen["analysis_n"] == 23
    assert pollen["meets_registered_floor"] is False
    assert receipt["status"] == "INDEPENDENT_CALIBRATION_VARIANCE_INCOMPLETE"


def test_confirmatory_eligible_row_is_rejected() -> None:
    rows = _completed_rows()
    rows[0]["confirmatory_eligible"] = "true"
    with pytest.raises(ValueError, match="confirmatory eligible"):
        summary.summarize(rows, "PED_D0_CONFIRM_V1")


def test_proportion_outside_unit_interval_is_rejected() -> None:
    rows = _completed_rows()
    rows[0]["early_attack_prop"] = "1.2"
    with pytest.raises(ValueError, match="must be in"):
        summary.summarize(rows, "PED_D0_CONFIRM_V1")


def test_confirmatory_dataset_must_not_be_calibration_dataset() -> None:
    with pytest.raises(ValueError, match="invalid confirmatory_dataset_id"):
        summary.summarize(_completed_rows(), "PED_D0_CAL_V1")


def test_multiple_time_horizons_are_rejected() -> None:
    rows = _completed_rows()
    rows[0]["time_horizon_id"] = "OTHER_HORIZON"
    with pytest.raises(ValueError, match="multiple contexts"):
        summary.summarize(rows, "PED_D0_CONFIRM_V1")
