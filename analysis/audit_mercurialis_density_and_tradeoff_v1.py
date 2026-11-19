#!/usr/bin/env python3
"""Recalculate published *Mercurialis* aggregates without crossing ploidy or cohorts.

2007 male-frequency arrays tested 0 vs 0.5, not rare frequency; density-only
2003 experiment differs from 2004 factorial. 2026 genetic QTL and geographic
range samples are diploid, distinct from 2007 hexaploid-hermaphrodite arrays.
No individual data, fitness invasion coefficient, or new statistical fit.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/mercurialis_density_ploidy_genetic_tradeoff_v1_20261115.json"


def compute(src: dict) -> dict:
    parts=src["study_blocks"]
    s=parts["mating_2007"]
    g=parts["genetic_2026"]
    geo=parts["natural_geography_2026"]
    if {s["doi"],g["doi"],geo["doi"]}!={"10.1111/j.1558-5646.2007.00195.x","10.1073/pnas.2427240123","10.1093/jeb/voag044"}:
        raise ValueError("DOI_PROVENANCE_CHANGED")
    if ("Allohexaploid" not in s["female_function_phenotype"] or
        "Diploid" not in s["male_function_phenotype"] or
        "Diploid" not in g["target"] or
        "Diploid" not in geo["target"]):
        raise ValueError("CROSS_PLOIDY_STUDY_BRIDGE")
    y3=s["field2003"]
    y4=s["field2004"]
    if (y3["male_frequency"]!=0 or y3["array_n"]!=6 or y3["array_size"]!=100 or
        y3["spacing_m"]!=[.11,.22,.33,.44,.66,1.5] or
        y4["array_n"]!=12 or y4["array_size"]!=100 or
        y4["male_frequencies_tested"]!=[0,.5] or
        y4["spacing_m"]!=[.11,.33]):
        raise ValueError("ORIGINAL_MATING_ARRAY_UNITS_CHANGED")
    if set(y4["original_progeny_per_group"])!={"hermaphrodite_low","hermaphrodite_high","mixed_low","mixed_high"}:
        raise ValueError("PLOIDY_BASED_PROGENY_GROUPS_CHANGED")
    out=y4["array_aggregated_outcross_mean"]
    absent,present=out["male_absent"],out["male_present"]
    if any(type(z) not in (float,int) or not 0<=z<=1 for z in (absent,present)):
        raise ValueError("INVALID_OUTCROSS_RATE")
    tests=y4["original_ANOVA"]
    if (not (tests["male_presence"]["p"]<.05 and tests["density"]["p"]>.05 and
             tests["male_presence_by_density"]["p"]>.05 and
             y3["outcross_by_spacing"]["0.11"]>y3["outcross_by_spacing"]["0.33"])):
        raise ValueError("ORIGINAL_DENSITY_SEX_SYSTEM_CONTRAST_CHANGED")
    beta=y4["male_fecundity_vs_hermaphrodite_siring_beta"]["estimate"]
    lam=y4["pollen_production_lambda_from_Buggs_Pannell_2006"]
    alpha=beta/lam
    if abs(alpha-y4["male_per_pollen_siring_alpha_original_ratio_statement"])>.02:
        raise ValueError("SOURCE_POLLEN_EFFICIENCY_DISAGREEMENT")
    assumption=s["invasion_model"]
    if (assumption["state"]!="PREDICTION_FROM_ORIGINAL_MODEL_NOT_DIRECT_RARE_FREQUENCY_EXPERIMENT" or
        assumption["temporal_fixation_or_invasion_observed"] or
        assumption["native_rare_male_frequency_measured"]):
        raise ValueError("FALSE_DIRECT_RARE_INVASION")
    if g["populations"]!={"control_XY":3,"experiment_XX_only":3} or g["F2_QTL_crosses"]!=4 or g["shared_common_garden"]["individuals"]!=1116 or g["shared_common_garden"]["analysis_subset_N"]!=318:
        raise ValueError("GENETIC_2026_COHORT_CHANGED")
    if g["original_GLMM"]["generation"]["CI"][0]<=0 or g["original_GLMM"]["seed_mass"]["CI"][1]>=0:
        raise ValueError("PUBLISHED_GENETIC_SIGNS_CHANGED")
    q=g["tradeoff_credible_region_examples"]
    if [(z["cross"],z["chromosome"],z["reported_variance_percent"]) for z in q]!=[(1,5,24.1),(2,7,32.0),(4,4,8.03)]:
        raise ValueError("PUBLISHED_QTL_CROSSES_CHANGED")
    if not any("multiple linked" in c for c in g["confounds"]):
        raise ValueError("FALSE_SINGLE_PLEIOTROPIC_GENE_CERTAINTY")
    inc=geo["source_estimands"]["leaky_expression_incidence_with_origin_distance"]
    if not (inc["female_percent_points_per_km_approx"]>0 and inc["male_percent_points_per_km_approx"]>0 and
            inc["female_Z"]>0 and inc["male_Z"]>0 and
            geo["source_estimands"]["expression_degree_given_leaky"]=="NO_DETECTED_RELATION_TO_EXPANSION_DISTANCE_IN_EITHER_SEX"):
        raise ValueError("INCIDENCE_DEGREE_DISTINCTION_LOST")
    fw=src["inferential_firewall"]
    if not (fw["cross_ploidy_cohort_bridge"].startswith("BLOCKED") and
            fw["2007_no_rare_frequency"].find("0 or 50%")>=0 and
            fw["2003_vs_2004"].startswith("2003") and
            not g["archive"]["raw_files_retrieved"] and not geo["raw_files_retrieved"]):
        raise ValueError("ORIGINAL_SOURCE_SCOPE_UNTRUSTWORTHY")
    return {
      "schema":"SLK_MERCURIALIS_PUBLISHED_PLoidY_ECOLOGY_GENETIC_AUDIT_RESULT_V1",
      "source_dois":{k:v["doi"] for k,v in parts.items()},
      "mating_2007":{
        "hermaphrodite_ploidy":6,"male_ploidy":2,
        "male_sired_progeny_ploidy":4,
        "male_fraction_levels_actually_tested_2004":[0,.5],
        "array_replicates_2004":y4["array_n"],
        "total_plants_per_array":y4["array_size"],
        "outcross_mean_no_males":absent,"outcross_mean_half_males":present,
        "outcross_absolute_point_difference":round(present-absent,8),
        "outcross_mean_ratio":round(present/absent,8),
        "original_presence_F":tests["male_presence"]["F"],
        "original_presence_p":tests["male_presence"]["p"],
        "original_2004_density_p":tests["density"]["p"],
        "original_2004_density_interaction_p":tests["male_presence_by_density"]["p"],
        "independent_2003_density_only_outcrossing":y3["outcross_by_spacing"],
        "original_relative_siring_beta":beta,
        "lambda_imported_from_2006_other_study":lam,
        "descriptive_per_pollen_siring_alpha":round(alpha,8),
        "new_alpha_significance_or_ci":None,
        "male_invades_below_reported_spacing_approx_model_only":assumption["substantial_male_persistence_spacing_m_approx"],
        "male_maintenance_density_approx_model_only":assumption["maintenance_density_plants_per_m2_approx"],
        "density_threshold_directly_observed":False,
        "rare_male_invasion_directly_observed":False
      },
      "genetic_2026":{
        "diploid_X_only_populations":g["populations"]["experiment_XX_only"],
        "diploid_XY_control_populations":g["populations"]["control_XY"],
        "evolution_generations":g["selected_generations"],
        "shared_common_garden_total_N":g["shared_common_garden"]["individuals"],
        "trait_model_N":g["shared_common_garden"]["analysis_subset_N"],
        "GLMM_generation_beta":g["original_GLMM"]["generation"]["beta"],
        "GLMM_seed_mass_beta":g["original_GLMM"]["seed_mass"]["beta"],
        "published_QTL_variance_by_cross":q,
        "sex_allocation_locus_categories":["antagonistic_broad_region","single_sex","same_direction","one_side_not_significant"],
        "single_gene_pleiotropy_proven":False,
        "rare_XY_reinvasion_directly_observed":False,
        "raw_phenotype_and_RadSeq_downloaded":False
      },
      "natural_geography_2026":{
        "sexes_with_positive_incidence_distance_gradient":["female","male"],
        "female_incidence_percent_points_per_km_approx":inc["female_percent_points_per_km_approx"],
        "male_incidence_percent_points_per_km_approx":inc["male_percent_points_per_km_approx"],
        "degree_conditional_on_leaky_trend_detected":False,
        "new_geographic_selection_causal_effect":None,
        "individual_data_downloaded":False
      },
      "cross_ploidy_combined_fitness_estimate":None,
      "same_genotype_density_by_QTL_effect":None,
      "SLK_Phi_g0_Delta_R_measured":False,
      "new_p_values":None,
      "raw_individual_reanalysis":False,
      "unmeasured":fw["unmeasured"]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=compute(json.loads(args.source.read_text(encoding="utf-8")))
    blob=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(blob,encoding="utf-8")
    else:
        print(blob,end="")

if __name__=="__main__":
    main()
