#!/usr/bin/env python3
"""Noninferential source-mean comparison within Case & Barrett 2004.

Preserves directionally opposite flower-visit and seed-to-ovule ordering.
Different flowering dates and sexual-system populations PRECLUDE causal
conversion, per-visit fertility, lifetime-fitness or same-individual inferences.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/evidence/wurmbea_2004_visit_to_seed_stage_source_v3.json"


def analyze(source):
    if source["source"]["doi"] != "10.1086/382796":
        raise ValueError("DOI_NOT_REGISTERED")
    design = source["observation_design"]
    if not (design["sex_system_populations_distinct"] and
            design["flowering_periods_nonoverlapping"] and
            not design["paired_individual_visit_and_seed_records_available"]):
        raise ValueError("UNSUPPORTED_MATCHED_COHORT_ASSUMPTION")
    means = source["fly_visits_per_flower_15min"]
    ranges = source["female_seed_to_ovule_reported_ranges"]
    for sex in ("female", "male", "cosexual"):
        row = means[sex]
        for key in ("mean", "se"):
            val = row[key]
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                raise ValueError("NONNUMERIC_FLY_RATE")
            if not math.isfinite(val) or val < 0:
                raise ValueError("INVALID_FLY_RATE")
    for sex in ("female", "fruiting_male", "cosexual"):
        lo, hi = ranges[sex]["min"], ranges[sex]["max"]
        if (isinstance(lo, bool) or isinstance(hi, bool) or
                not all(isinstance(v, (int, float)) and math.isfinite(v)
                        for v in (lo, hi)) or
                not 0 < lo <= hi <= 1):
            raise ValueError("INVALID_SEED_OVULE_RANGE")
    f, c = means["female"]["mean"], means["cosexual"]["mean"]
    if f <= 0 or c <= 0:
        raise ValueError("ZERO_FLY_VISIT_DENOMINATOR")
    fr, cr = ranges["female"], ranges["cosexual"]
    timing = source["anther_presentation_same_paper"]
    onset = timing["days_from_anthesis_until_first_pollen_presentation"]
    six = timing["days_to_dehisce_all_six_anthers"]
    first_day = timing["first_day_percent_of_total_pollen_removed"]
    for group in (onset, six, first_day):
        for sex in ("male", "cosexual"):
            for key in ("mean", "se"):
                value = group[sex][key]
                if (isinstance(value, bool) or
                        not isinstance(value, (float, int)) or
                        not math.isfinite(value) or value <= 0):
                    raise ValueError("INVALID_POLLEN_PRESENTATION_MEASURE")
    if not 0 < six["original_mann_whitney_p"] < 1:
        raise ValueError("INVALID_ORIGINAL_P")
    if not (first_day["male"]["mean"] < first_day["cosexual"]["mean"] and
            onset["male"]["mean"] < onset["cosexual"]["mean"] and
            six["male"]["mean"] > six["cosexual"]["mean"]):
        raise ValueError("POLLEN_METERING_SOURCE_DIRECTION_CHANGED")
    source_outcomes = source["author_reported_outcomes"]
    if (source_outcomes["pollen_deposition_female_vs_cosexual"] !=
            "NO_SIGNIFICANT_DIFFERENCE_DETECTED"):
        raise ValueError("POLLEN_RECEIPT_UNSUPPORTED")
    if (source_outcomes["additional_hand_cross_pollination_effect_on_fruit_or_seed_set"] !=
            "NO_SIGNIFICANT_EFFECT_DETECTED"):
        raise ValueError("POLLEN_SUPPLEMENT_UNSUPPORTED")
    return {
        "schema": "slk_wurmbea_2004_visit_seed_decoupling_result_v3",
        "source_doi": source["source"]["doi"],
        "same_paper_opposite_ordering": bool(
            c > f and fr["min"] > cr["max"]),
        "fly_visits_cosexual_over_female_from_rounded_means": c / f,
        "fly_visits_female_over_cosexual_from_rounded_means": f / c,
        "seed_to_ovule_female_over_cosexual_reported_range_ratio": [
            fr["min"] / cr["max"], fr["max"] / cr["min"]
        ],
        "pollen_deposition_female_vs_cosexual":
            source_outcomes["pollen_deposition_female_vs_cosexual"],
        "hand_cross_supplementation":
            source_outcomes["additional_hand_cross_pollination_effect_on_fruit_or_seed_set"],
        "pollen_presentation_biology": {
            "male_over_cosexual_onset_days_ratio":
                onset["male"]["mean"] / onset["cosexual"]["mean"],
            "male_over_cosexual_complete_anther_dehiscence_days_ratio":
                six["male"]["mean"] / six["cosexual"]["mean"],
            "male_over_cosexual_first_day_pollen_removed_ratio":
                first_day["male"]["mean"] / first_day["cosexual"]["mean"],
            "published_mann_whitney_p_anther_duration":
                six["original_mann_whitney_p"],
            "male_reclosure_observed_in_some_plants":
                timing["anther_reclosure_after_wet_or_windy_weather"]["males_some_observed"],
            "new_p_value": None,
            "male_paternity": None,
        },
        "same_season_or_same_individual_comparison": False,
        "per_visit_seed_fitness_ratio": None,
        "new_p_values": None,
        "new_confidence_intervals": None,
        "slk_gate_fit": None,
        "causal_origin_of_gender_dimorphism": None,
        "published_ranges_are_sampling_intervals": False,
        "interpretation": ("Opposite observed group orderings in one published paper; "
                           "no visit-to-seed causal attribution or fertility-per-visit calculation."),
        "design_warnings": source["limits"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(json.loads(args.source.read_text(encoding="utf-8")))
    output = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
