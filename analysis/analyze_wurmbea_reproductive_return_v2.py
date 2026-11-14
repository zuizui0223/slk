#!/usr/bin/env python3
"""Descriptive stage-matched reanalysis of Wurmbea 2006 Table 2.

Ratios use products of rounded treatment means. They are not raw-family
estimates, actual cohort totals, or lifetime reproductive fitness. No sampling
intervals or new significance tests are calculated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/evidence/wurmbea_2006_reproductive_return_source_v2.json"
FIELDS = ("seeds_mean", "germination_pct_mean", "survival_pct_mean", "corm_mass_mg_mean")
PAIRS = (("Fo", "Mo"), ("Fc", "Mc"), ("Ms", "Mc"), ("Mo", "Mc"), ("Fo", "Fc"))


def stage_indices(row):
    """Return S, S*G, S*G*V, S*G*V*C, with G and V entered as percentages."""
    values = []
    for field in FIELDS:
        value = row[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"NONNUMERIC_MEAN: {field}")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"INVALID_MEAN: {field}")
        if "pct" in field and value > 100:
            raise ValueError(f"PERCENT_OUT_OF_RANGE: {field}")
        values.append(float(value))
    seeds, germination, survival, corm = values
    germinated = seeds * germination / 100
    survivors = germinated * survival / 100
    return [seeds, germinated, survivors, survivors * corm]


def compare_groups(numerator, denominator):
    """Compute stage ratios and rounding-only bounds for one-decimal means."""
    num, den = stage_indices(numerator), stage_indices(denominator)
    if any(x <= 0 for x in den):
        raise ValueError("ZERO_DENOMINATOR")
    ratios = [a / b for a, b in zip(num, den)]
    # Each printed mean is assumed rounded to nearest 0.1 in its original unit.
    # Percentage input thus has a half-width of 0.05 percentage points.
    rounded = []
    for row in (numerator, denominator):
        lo = {f: max(0.0, row[f] - 0.05) for f in FIELDS}
        hi = {f: min(100.0, row[f] + 0.05) if "pct" in f else row[f] + 0.05
              for f in FIELDS}
        rounded.append((stage_indices(lo), stage_indices(hi)))
    (num_lo, num_hi), (den_lo, den_hi) = rounded
    bounds = [[a / b, c / d if d > 0 else None]
              for a, b, c, d in zip(num_lo, den_hi, num_hi, den_lo)]
    return {"stage_ratios": ratios, "rounding_only_bounds": bounds}


def analyze(data):
    if data["measurement_semantics"]["germination_and_survival_unit"] != "percent":
        raise ValueError("EXPECTED_PERCENT_INPUT")
    expected_stages = ["seeds", "seeds_x_germination", "seeds_x_germination_x_survival",
                       "seeds_x_germination_x_survival_x_corm_mass"]
    if data["measurement_semantics"]["stage_order"] != expected_stages:
        raise ValueError("LIFE_STAGE_ORDER_CHANGED")
    groups = data["groups"]
    if set(groups) != {"Ms", "Mo", "Mc", "Fo", "Fc"}:
        raise ValueError("PUBLISHED_TREATMENT_GROUPS_CHANGED")
    comparisons = {f"{a}_over_{b}": compare_groups(groups[a], groups[b]) for a, b in PAIRS}
    cross_rp = comparisons["Fc_over_Mc"]["stage_ratios"][-1]
    open_cross_rp = comparisons["Mo_over_Mc"]["stage_ratios"][-1]
    return {
        "schema": "slk_wurmbea_reproductive_return_result_v2",
        "source": data["source"],
        "stage_order": expected_stages,
        "group_indices": {name: stage_indices(row) for name, row in groups.items()},
        "comparisons": comparisons,
        "self_cross_summary_inbreeding_depression": 1 - comparisons["Ms_over_Mc"]["stage_ratios"][-1],
        "source_sampling": data["sampling"],
        "author_reported": data["author_reported"],
        "source_consistency": {
            "crossed_female_male_four_component_ratio": cross_rp,
            "crossed_male_female_four_component_reciprocal": 1 / cross_rp,
            "open_cross_fruiting_male_four_component_ratio": open_cross_rp,
            "open_cross_reported_minus_recomputed": data["author_reported"]["fruiting_male_open_over_cross_cumulative_results"] - open_cross_rp,
            "status": "TABLE_RECOMPUTATION_WITH_SOURCE_REPORTED_DISCREPANCY_RETAINED"
        },
        "new_confidence_intervals": None,
        "new_p_values": None,
        "rounding_bounds_are_sampling_intervals": False,
        "claim_limits": data["claim_limits"]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    result = analyze(json.loads(source_bytes))
    result["source_file_sha256"] = hashlib.sha256(source_bytes).hexdigest()
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
