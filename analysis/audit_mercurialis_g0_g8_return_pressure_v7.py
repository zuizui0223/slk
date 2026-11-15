#!/usr/bin/env python3
"""Join separate original-source receipts for the Mercurialis G0-G8 biology.

This is arithmetic on *published aggregate results*, NOT a raw genotype refit,
lifetime-fitness reconstruction, estimated inbreeding depression, or an
observed evolutionary reversion to dioecy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/evidence/mercurialis_g0_g8_return_pressure_source_v7.json"
G2021 = ROOT / "data/evidence/mercurialis_2019_2021_restored_function_siring_source_v6.json"
G2025 = ROOT / "data/evidence/mercurialis_inbreeding_disruption_2025_primary_v1.json"


def compute(gate: dict, source_2021: dict, source_2025: dict) -> dict:
    if gate["schema"] != "SLK_MERCURIALIS_G0_G8_FUNCTION_RETURN_AND_RETURN_PRESSURE_V7":
        raise ValueError("WRONG_CROSS_STUDY_SCHEMA")
    links = gate["study_relationships"]
    x = source_2021["experimental_2021"]
    morph = source_2021["architecture_2019"]
    y = source_2025["experiment"]
    original = gate["g8_original_source_additional_receipt"]
    if (links["experimental_reversion_2021_doi"] != x["doi"]
            or links["published_g8_fitness_2025_doi"] != source_2025["source"]["doi"]
            or links["independent_morphology_2019_doi"] != morph["doi"]):
        raise ValueError("ORIGINAL_STUDY_RELATIONSHIP_OR_DOI_CHANGED")
    if (not links["G0_G4_G5_G8_same_experimental_program_not_independent_evolutionary_reversals"]
            or links["longitudinal_individual_matched_G4_G8"]
            or not links["distinct_2019_cohort_and_genetic_background"]
            or not morph["not_the_2021_evolved_lineages"]):
        raise ValueError("FALSE_INDEPENDENCE_OR_ISOGENIC_CAUSALITY")
    if (x["population_replicates"] != {"female_only": 3, "male_female_controls": 3}
            or y["prior_evolution_generations"] != 8
            or y["common_garden_replicates"] != 3
            or y["individuals_per_replicate"] != 61
            or y["phenotyped_n"] != 180
            or original["source_population_seeds_evolved_male_free_generations"] != 8):
        raise ValueError("GENERATION_OR_REPLICATE_SOURCE_CHANGED")

    g5 = x["G5_reintroduced_males"]
    if (g5["arrays"], g5["females_per_array"], g5["XY_males_per_array"]) != (6, 50, 50):
        raise ValueError("G5_FATHERHOOD_EXPERIMENT_CHANGED")
    if (g5["selected_XX_mothers_male_progeny_fraction"] != .436
            or g5["expected_male_fraction_from_XY_fathers"] != .5
            or g5["author_inferred_fraction_XX_female_sired"] != .128):
        raise ValueError("G5_SEX_RATIO_PATERNITY_SOURCE_CHANGED")
    inferred_g5 = 2 * (g5["expected_male_fraction_from_XY_fathers"]
                       - g5["selected_XX_mothers_male_progeny_fraction"])
    if abs(inferred_g5 - g5["author_inferred_fraction_XX_female_sired"]) > 1e-12:
        raise ValueError("BAD_G5_PATERNITY_INFERENCE")

    if (original["parents_DNA_extracted_n"] != 181
            or original["progeny_DNA_extracted_n"] != 958
            or original["published_approximate_total_progeny_n"] != 13800
            or original["paternity_marker_loci"] != 9
            or original["paternity_assignment_Cervus_relaxed_confidence"] != .8
            or (original["seed_sampled_per_mother_min"], original["seed_sampled_per_mother_max"]) != (5, 10)
            or original["raw_Zenodo_data_downloaded_or_refit"]):
        raise ValueError("G8_ORIGINAL_PARENTS_GENOTYPE_SAMPLING_CHANGED")
    if (y["successful_genotyping_seeds"] != 948
            or y["assigned_paternity_seeds"] != 915
            or y["selfing_analyzed_n"] != 172
            or y["mean_selfing_rate"] != .296):
        raise ValueError("G8_DIRECT_PATERNITY_OR_SELFING_SOURCE_CHANGED")
    if (source_2025["fitness_estimands"]["inbreeding_scenarios"] != [0, 1]
            or source_2025["fitness_estimands"]["diploid_actual_delta"] != "NOT_MEASURED_IN_THIS_STUDY"):
        raise ValueError("G8_DELTA_OBSERVED_VERSUS_ASSUMED_CHANGED")

    rate = source_2021["experimental_2021"]["selfing_genotypes"]
    if rate["markers"] != 8 or x["author_G1_vs_G4_selfing_difference_p"] != .1:
        raise ValueError("G1_G4_POPULATION_RMES_SOURCE_CHANGED")
    s1 = [rate["G1"][k]["s"] for k in ("S1", "S2", "S3")]
    s4 = [rate["G4"][k]["s"] for k in ("S1", "S2", "S3")]
    if s1 != [.124, .225, .225] or s4 != [.172, .074, .121]:
        raise ValueError("G1_G4_RMES_TABLE_CHANGED")
    if x["original_G4_common_garden_male_flower_ratio_vs_control"] != 23.3:
        raise ValueError("G4_FLOWER_RATIO_NOT_CONTEMPORARY_CONTROL")

    qc = {}
    qsource = source_2025["primary_table1_total_fitness_quadratic"]
    for size in ("small", "medium", "large"):
        a = qsource[size]
        expected = (size != "small")
        if a["delta0_significant"] or a["delta1_significant"] != expected:
            raise ValueError("G8_PUBLISHED_CURVATURE_SIGNIFICANCE_CHANGED")
        if (a["delta0_se"] != a["delta1_se"]
                or original["original_table1_quadratic_effect_comparison_delta0_vs_delta1"][size]
                   != ("P<0.001" if expected else "NOT_REPORTED_SIGNIFICANT")):
            raise ValueError("G8_PUBLISHED_TABLE1_SCENARIO_COMPARISON_CHANGED")
        qc[size] = {
            "quadratic_delta0_published": a["delta0"],
            "quadratic_delta1_published": a["delta1"],
            "printed_common_se_each_scenario": a["delta0_se"],
            "published_delta0_quadratic_significant": a["delta0_significant"],
            "published_delta1_quadratic_significant": a["delta1_significant"],
            "arithmetic_delta1_minus_delta0_no_new_inference": round(a["delta1"] - a["delta0"], 2),
            "source_scenario_comparison": original[
                "original_table1_quadratic_effect_comparison_delta0_vs_delta1"][size]
        }
    ceiling = gate["biological_ceiling"]
    if (ceiling["inbreeding_depression"] != "DELTA_0_OR_1_ASSUMED_NOT_DIPLOID_FIELD_MEASURED"
            or ceiling["directional_evolutionary_return_to_dioecy"] != "NOT_OBSERVED"
            or ceiling["g5_female_XX_siring"] != "INDIRECT_SEX_RATIO_ESTIMATE_NOT_SSR_PARENTAGE"
            or ceiling["g8_siring"] != "SSR_FATHER_ASSIGNMENT_ON_SAMPLE_NOT_ALL_SEEDS"):
        raise ValueError("FALSE_EVOLUTIONARY_CAUSAL_PROMOTION")

    g8_success = y["assigned_paternity_seeds"]
    g8_genotyped = y["successful_genotyping_seeds"]
    g8_extracted = original["progeny_DNA_extracted_n"]
    return {
        "schema": "SLK_MERCURIALIS_G0_G8_CONDITIONAL_RETURN_PRESSURE_RESULT_V7",
        "original_dois": {
            "2021_selection_and_G5": x["doi"],
            "2025_G8_assigned_fathers": source_2025["source"]["doi"],
            "2019_independent_morphology": morph["doi"]
        },
        "linked_evolution_program_not_independent_origins": True,
        "G4_to_G8_same_individual_longitudinal_data": False,
        "G4_male_flower_ratio_vs_contemporaneous_controls": 23.3,
        "G5_XX_paternal_fraction_from_offspring_sex_ratio": round(inferred_g5, 9),
        "G5_measured_individual_XX_fathers_by_SSR": False,
        "G8_paternity": {
            "parents_DNA_extracted": original["parents_DNA_extracted_n"],
            "seed_DNA_extracted": g8_extracted,
            "successfully_genotyped": g8_genotyped,
            "paternity_assigned": g8_success,
            "not_successfully_genotyped_of_extracted": g8_extracted - g8_genotyped,
            "genotyped_without_father_assignment": g8_genotyped - g8_success,
            "assignment_fraction_of_genotyped_not_population_coverage": round(g8_success / g8_genotyped, 9),
            "sampled_paternity_fraction_of_approx_total_seed_population": round(
                g8_success / original["published_approximate_total_progeny_n"], 9),
            "paternity_assignment_Cervus_confidence": original["paternity_assignment_Cervus_relaxed_confidence"],
            "original_raw_Zenodo_reanalysis": False
        },
        "selfing_estimates_not_longitudinally_comparable": {
            "G1_2021_mean_of_three_population_RMES": round(sum(s1) / 3, 9),
            "G4_2021_mean_of_three_population_RMES": round(sum(s4) / 3, 9),
            "G4_minus_G1_descriptive_not_significant": round((sum(s4)-sum(s1))/3, 9),
            "G1_G4_author_difference_p": x["author_G1_vs_G4_selfing_difference_p"],
            "G8_2025_mean_of_172_individual_selfing_fractions": y["mean_selfing_rate"],
            "G8_n_individuals": y["selfing_analyzed_n"],
            "SSR_methods_differ_8_vs_9_loci": True,
            "G4_to_G8_selfing_change_estimable": False
        },
        "G8_relative_total_fitness_quadratic_from_original_table1": qc,
        "G8_actual_diploid_inbreeding_depression_measured": False,
        "observed_G8_reversion_to_XX_XY_dioecy": False,
        "rare_mutant_invasion_or_SLK_Phi_g0_Delta_R_estimated": False,
        "biological_interpretation": (
            "Real restored sex function under mate exclusion is accompanied by "
            "observed male-allocation/selfing association; potential pressure "
            "toward redivision is conditional on unmeasured inbreeding depression. "
            "No re-evolution of dioecy is observed."
        )
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = compute(*[
        json.loads(path.read_text(encoding="utf-8"))
        for path in (GATE, G2021, G2025)
    ])
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
