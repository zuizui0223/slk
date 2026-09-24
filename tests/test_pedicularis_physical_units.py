from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = ROOT / "scripts" / "pedicularis_physical_units.py"
REGISTRY = ROOT / "scripts" / "build_pedicularis_physical_plant_registry.py"

spec = importlib.util.spec_from_file_location("ped_physical_unit_test", PHYSICAL)
physical = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(physical)

spec2 = importlib.util.spec_from_file_location("ped_physical_registry_test", REGISTRY)
registry = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(registry)


def _rows(prefix: str, tags: list[str]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for index, tag in enumerate(tags, start=1):
        plant_id = f"{prefix}-{index:03d}"
        for flower in (1, 2):
            out.append(
                {
                    "context_id": "ctx1",
                    "population_id": "pop1",
                    "season_id": "2027",
                    "plant_id": plant_id,
                    "physical_plant_tag": tag,
                    "flower_id": f"{plant_id}-F{flower}",
                }
            )
    return out


def test_physical_tag_hash_is_order_invariant() -> None:
    a = physical.canonical_tag_hash(["P3", "P1", "P2"])
    b = physical.canonical_tag_hash(["P2", "P3", "P1"])
    assert a == b
    assert len(a) == 64


def test_multiple_rows_for_same_assignment_and_same_physical_plant_pass() -> None:
    mapping = physical.validate_physical_plant_mapping(
        _rows("A", ["PHY-1", "PHY-2"])
    )
    assert mapping == {
        "A-001": "PHY-1",
        "A-002": "PHY-2",
    }


def test_assignment_id_cannot_switch_physical_plants() -> None:
    rows = _rows("A", ["PHY-1"])
    rows[1]["physical_plant_tag"] = "PHY-OTHER"
    with pytest.raises(ValueError, match="maps to multiple physical tags"):
        physical.validate_physical_plant_mapping(rows)


def test_same_physical_plant_cannot_hide_under_two_assignment_ids() -> None:
    rows = _rows("A", ["PHY-1", "PHY-2"])
    for row in rows:
        if row["plant_id"] == "A-002":
            row["physical_plant_tag"] = "PHY-1"
    with pytest.raises(ValueError, match="reused across assignment IDs"):
        physical.validate_physical_plant_mapping(rows)


def test_registry_rejects_cross_cohort_physical_reuse() -> None:
    cohorts = {
        "YCAL": _rows("Y", ["PHY-1", "PHY-2"]),
        "D0CAL": _rows("D", ["PHY-2", "PHY-3"]),
    }
    with pytest.raises(ValueError, match="reuse detected across cohorts"):
        registry.build_registry(
            cohorts,
            context_id="ctx1",
            population_id="pop1",
            season_id="2027",
        )


def test_registry_emits_valid_next_stage_firewall() -> None:
    result = registry.build_registry(
        {
            "YCAL": _rows("Y", ["PHY-1", "PHY-2"]),
            "D0CAL": _rows("D", ["PHY-3", "PHY-4"]),
        },
        context_id="ctx1",
        population_id="pop1",
        season_id="2027",
    )
    firewall = physical.validate_firewall_block(
        result["next_stage_firewall_block"]
    )
    assert firewall["forbidden_tag_count"] == 4
    assert result["overlap_count"] == 0
    assert (
        firewall["prior_tag_set_sha256"]
        == result["all_prior_tag_set_sha256"]
    )


def test_current_cohort_is_rejected_if_tag_is_in_registry_firewall() -> None:
    result = registry.build_registry(
        {"PRIOR": _rows("P", ["PHY-PRIOR"])},
        context_id="ctx1",
        population_id="pop1",
        season_id="2027",
    )
    firewall = physical.validate_firewall_block(
        result["next_stage_firewall_block"]
    )
    with pytest.raises(ValueError, match="reuses prior physical plants"):
        physical.validate_current_against_forbidden(
            _rows("NEW", ["PHY-PRIOR"]),
            firewall,
        )


def test_registry_rejects_context_drift() -> None:
    rows = _rows("Y", ["PHY-1"])
    rows[0]["population_id"] = "other"
    with pytest.raises(ValueError, match="registry context mismatch"):
        registry.build_registry(
            {"YCAL": rows},
            context_id="ctx1",
            population_id="pop1",
            season_id="2027",
        )



def _prior_firewall(tags: list[str]) -> dict:
    return {
        "schema_version": "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1",
        "require_nonempty_physical_plant_tag": True,
        "prior_physical_plant_tags_forbidden": tags,
        "prior_tag_source_references": ["TEST_P0_PRIOR"],
        "prior_tag_set_sha256": physical.canonical_tag_hash(tags),
        "frozen_before_outcomes": True,
    }


def test_registry_rejects_reuse_against_prior_p0_firewall() -> None:
    with pytest.raises(ValueError, match="against prior firewall"):
        registry.build_registry(
            {"YCAL": _rows("Y", ["PHY-P0", "PHY-NEW"])},
            context_id="ctx1",
            population_id="pop1",
            season_id="2027",
            prior_firewall=_prior_firewall(["PHY-P0"]),
        )


def test_registry_extends_prior_firewall_with_new_calibration_tags() -> None:
    result = registry.build_registry(
        {"YCAL": _rows("Y", ["PHY-Y1", "PHY-Y2"])},
        context_id="ctx1",
        population_id="pop1",
        season_id="2027",
        prior_firewall=_prior_firewall(["PHY-P0-A", "PHY-P0-B"]),
    )
    block = result["next_stage_firewall_block"]
    assert set(block["prior_physical_plant_tags_forbidden"]) == {
        "PHY-P0-A",
        "PHY-P0-B",
        "PHY-Y1",
        "PHY-Y2",
    }
    assert block["prior_tag_set_sha256"] == physical.canonical_tag_hash(
        block["prior_physical_plant_tags_forbidden"]
    )
