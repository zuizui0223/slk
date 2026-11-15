#!/usr/bin/env python3
"""Re-express original 2024 Mercurialis LMM at observed ring positions.

Not a new fit or raw-plant reanalysis. Pollen limitation endpoint is *fruit
nondevelopment*, interpreted by source authors as pollen-delivery proxy.
No reconstructed coefficient covariance; no CI on combined predictions.
Source Table 1 narrative t=2.91/p=.097/CI crossing zero is inconsistent;
do not "correct" authors' p or silently promote significance.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/mercurialis_2024_pollen_distance_unfruiting_vs_seed_v5.json"

def compute(source):
    if source["source"]["doi"]!="10.1002/ajb2.16429":
        raise ValueError("WRONG_PRIMARY_PAPER")
    d=source["distance_experiment"]
    if (d["experimental_replicate_assemblies"]!=3 or
        d["plants_per_assembly"]!=28 or d["total_planted"]!=84 or
        d["reported_model_observations"]!=71 or
        d["radial_distance_m"]!=[.5,1.5] or
        d["central_group_each_assembly"]!={"male":4,"female":4,"hermaphrodite":4,"number":12}):
        raise ValueError("SOURCE_RING_DESIGN_OR_MISSINGNESS_CHANGED")
    if "DID NOT develop fruits" not in d["response_definition"]:
        raise ValueError("FALSE_DIRECT_STIGMA_POLLEN_ESTIMATE")
    co=d["reported_linear_mixed_model"]
    intercept=co["intercept_at_zero_distance_hermaphrodite"]
    female=co["female_vs_hermaphrodite_offset"]
    slope=co["distance_from_center_per_m"]
    interaction=co["distance_by_morph_interaction"]
    for k in (intercept,female,slope):
        if (not isinstance(k["estimate"],(float,int)) or
            not all(isinstance(v,(float,int)) for v in k["CI95"]) or
            not k["CI95"][0]<=k["estimate"]<=k["CI95"][1]):
            raise ValueError("INVALID_PUBLISHED_LMM_COEFFICIENT")
    if (intercept["estimate"]!=.152 or female["estimate"]!=.053 or
        slope["estimate"]!=.084 or
        female["reported_p"]!=.029 or
        slope["reported_p"]!="<0.001" or interaction["reported_p"]!=.80):
        raise ValueError("PUBLISHED_DISTANCE_SEX_CONTRAST_CHANGED")
    sites={}
    for x in d["radial_distance_m"]:
        H=intercept["estimate"]+slope["estimate"]*x
        F=H+female["estimate"]
        if not 0<=H<=1 or not 0<=F<=1:
            raise ValueError("PREDICTED_UNFRUITING_OUTSIDE_FRACTION")
        sites[f"{x:.1f}m"]={
           "published_model_conditional_hermaphrodite":round(H,8),
           "published_model_conditional_female":round(F,8),
           "female_minus_hermaphrodite":round(F-H,8),
           "source_level":"LMM fitted-value arithmetic, NOT measured plant group mean",
           "model_CI_with_covariances":None
        }
    radial_spread=d["radial_distance_m"][1]-d["radial_distance_m"][0]
    distance_shift=slope["estimate"]*radial_spread
    distance_ci_on_comparison=[round(v*radial_spread,8) for v in slope["CI95"]]
    if (not 0<distance_shift<1 or
        distance_ci_on_comparison!=[.047,.121]):
        raise ValueError("PUBLISHED_DISTANCE_EFFECT_EXPECTATION_CHANGED")
    seeds=d["seed_biomass_followup"]
    s_sex=seeds["female_vs_hermaphrodite_effect"]
    s_dist=seeds["distance_effect"]
    if (s_sex["reported_p"]!=.58 or s_dist["reported_p"]!=.17 or
        s_sex["CI95"][0]>=0 or s_sex["CI95"][1]<=0 or
        s_dist["CI95"][0]>=0 or s_dist["CI95"][1]<=0):
        raise ValueError("UNSUPPORTED_SEED_BIOMASS_SIGNIFICANCE")
    common=source["separate_morph_common_garden"]
    if (common["reported_table1_analyzed_by_endpoint"]!={
           "male_flower_biomass":201,
           "seed_biomass_per_aboveground_biomass":383,
           "seed_count_per_biomass":383}
        or common["male_vs_hermaphrodite_male_effort_ratio"]["estimate"]!=11.7):
        raise ValueError("SEPARATE_COMMON_GARDEN_SOURCE_CHANGED")
    p=common["female_vs_hermaphrodite_seed_count_per_biomass"]
    if not (p["text_reported_t"]==2.91 and
            p["text_reported_df"]==213 and p["text_reported_p"]==.097 and
            p["CI95"][0]<0<p["CI95"][1]):
        raise ValueError("ORIGINAL_TEXT_T_P_CI_INCONSISTENCY_NOT_PRESERVED")
    # The CI includes 0 and source p>.05, whereas |t|=2.91 with df213
    # must reject at the 5% level. Never invent a corrected t here.
    fit_assumptions=source["independent_original_population_survey_and_model"]
    if (fit_assumptions["original_population_n"]!=109 or
        fit_assumptions["documented_trioecious_populations"]!=36 or
        fit_assumptions["source_model_rescue_conditions"]
            ["restorer_cost_rho_simulation_range_for_field_morph_ratios"]!=[.15,.4] or
        not fit_assumptions["no_fitted_population_specific_ecological_coefficients"]):
        raise ValueError("FITNESS_COST_PRIOR_MODEL_NOT_NEW_EMPIRICAL_ESTIMATE")
    if not any("Fruit failure proxy" in v for v in source["limitations"]):
        raise ValueError("POLLEN_LIMITATION_PROXY_NOT_ACKNOWLEDGED")
    return {
      "schema":"SLK_MERCURIALIS_2024_ORIGINAL_POLLEN_DISTANCE_SOURCE_LMM_REEXPRESSION_V5",
      "source_doi":source["source"]["doi"],
      "year_published":2024,
      "original_distance_experimental_plants_planted":d["total_planted"],
      "original_analyzed_distance_plants":d["reported_model_observations"],
      "original_n_from_central_plus_rings":d["experimental_replicate_assemblies"]*d["plants_per_assembly"],
      "source_unfruiting_proxy_not_direct_pollen_receipt":True,
      "model_fitted_unfruiting_fraction_by_original_ring":sites,
      "one_meter_difference_both_morphs":round(distance_shift,8),
      "one_meter_slope_95CI_from_original_model":distance_ci_on_comparison,
      "female_minus_hermaphrodite_offset":female["estimate"],
      "original_female_offset_95CI":female["CI95"],
      "original_female_offset_p":female["reported_p"],
      "original_slope_p":slope["reported_p"],
      "source_no_detected_morph_distance_interaction_p":interaction["reported_p"],
      "source_morph_by_distance_interaction_effect_estimated":None,
      "source_relative_seed_biomass_morph_test_p":s_sex["reported_p"],
      "source_relative_seed_biomass_distance_test_p":s_dist["reported_p"],
      "full_model_prediction_CIs_without_covariance":None,
      "common_garden_separate_male_effort_ratio":common["male_vs_hermaphrodite_male_effort_ratio"],
      "source_common_garden_seed_count_model_internal_conflict":{
         "reported_t":p["text_reported_t"],
         "reported_df":p["text_reported_df"],
         "reported_p":p["text_reported_p"],
         "reported_CI":p["CI95"],
         "CI_includes_zero":True,
         "t_and_p_cannot_both_be_correct":True,
         "independent_corrected_t":None,
         "new_p_values":None,
         "safe_conclusion":"No significant difference detected by printed p and CI; do not treat narrative t=2.91 as reliable"
      },
      "original_model_required_restorer_cost_rho_simulated_range":
          fit_assumptions["source_model_rescue_conditions"]
               ["restorer_cost_rho_simulation_range_for_field_morph_ratios"],
      "original_restorer_fitness_cost_measured":False,
      "actual_male_or_female_genotype_frequency_invasion":None,
      "SLK_Phi_g0_Delta_R_measured":False,
      "original_2024_raw_109pop_and_71plant_records_downloaded":False,
      "limitation_receipt":source["limitations"]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    out=json.dumps(compute(json.loads(a.source.read_text(encoding="utf-8"))),
                   ensure_ascii=False,allow_nan=False,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(out,encoding="utf-8")
    else:
        print(out,end="")


if __name__=="__main__":
    main()
