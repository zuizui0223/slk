#!/usr/bin/env python3
"""Source-only Sagittaria biological chain: visitor route ≠ siring ≠ invasion.

This script audits published empirical claims and simple arithmetic on
reported aggregates. It does NOT refit independent flower/clone/genotype data,
estimate new P values, equate non-significance with equivalence, or measure
relative rare-mutant fitness, new allelic access, or SLK Phi/g0/Delta_R.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/sagittaria_partner_routing_mating_filter_primary_v2_20261115.json"


def analyze(d):
    p=d["primary_sources"]
    array=p["mating_display_2006"]
    bet=p["natural_bateman_2022"]
    phen=p["temporal_opportunity_2023"]
    mating=p["selfing_inbreeding_2002"]
    if {array["doi"],bet["doi"],phen["doi"],mating["doi"]} != {
        "10.1098/rspb.2006.3599",
        "10.1098/rspb.2022.0919",
        "10.1098/rsos.231117",
        "10.1111/j.0014-3820.2002.tb00847.x"
    }:
        raise ValueError("PRIMARY_DOI_SET_CHANGED")
    if (array["array_trials"],array["plants_per_array"],
        array["total_plant_appearances"])!=(20,4,80):
        raise ValueError("SOURCE_ARRAY_DESIGN_CHANGED")
    if (array["flower_visits"],array["foraging_trips"])!=(3143,872):
        raise ValueError("ORIGINAL_VISIT_DENOMINATORS_CHANGED")
    mean=array["flower_visits"]/array["foraging_trips"]
    if abs(mean-array["author_mean_flower_visits_per_trip"])>.02:
        raise ValueError("ORIGINAL_MEAN_TRIPS_DISAGREEMENT")
    vals=array["published_tests"]
    inter=vals["display_times_sex_system_for_interplant_pollen_delivery_proxy"]
    if not (inter["F"]>0 and 0<inter["p"]<.05 and
            vals["display_association_monoecious"]["p"]<.05 and
            vals["display_association_dioecious"]["p"]>.05 and
            array["observed_direction"]["system_display_rank_reversal"]):
        raise ValueError("POLLEN_TRANSFER_RANK_REVERSAL_EVIDENCE_CHANGED")
    if (array["observed_direction"]["low_display"] !=
            "DIOECIOUS_GREATER_BETWEEN_INDIVIDUAL_POLLEN_DELIVERY_PROXY" or
        array["observed_direction"]["high_display"] !=
            "MONOECIOUS_GREATER_BETWEEN_INDIVIDUAL_POLLEN_DELIVERY_PROXY"):
        raise ValueError("VISITOR_ROUTE_DIRECTION_CHANGED")
    adj=bet["original_table1_size_adjusted"]
    unadj=bet["original_supplement_unadjusted"]
    d_b={}
    for system in ("monoecious","dioecious"):
        A,U=adj[system],unadj[system]
        if not (A["male"]["significant"] and not A["female"]["significant"] and
                A["male"]["beta"]>0 and U["delta_male_minus_female"]<0 and
                A["delta_male_minus_female"]["value"]>0):
            raise ValueError("BATEMAN_ADJUSTED_PUBLISHED_SIGNS_CHANGED")
        d_b[system]={
          "male_size_adjusted_beta":A["male"]["beta"],
          "male_size_adjusted_se":A["male"]["se"],
          "female_size_adjusted_beta":A["female"]["beta"],
          "female_size_adjusted_se":A["female"]["se"],
          "published_male_minus_female_size_adjusted":A["delta_male_minus_female"]["value"],
          "published_male_minus_female_unadjusted":U["delta_male_minus_female"],
          "sign_reversal_after_size_adjustment":True,
          "genet_samples_for_sex_functions":bet["analyzed_mlls"][system],
          "different_estimands_and_not_a_causal_treatment":True
        }
    if abs(d_b["monoecious"]["male_size_adjusted_beta"]-
           d_b["dioecious"]["male_size_adjusted_beta"])>.2:
        raise ValueError("PUBLISHED_MALE_BETAS_ARE_NOT_CLOSE")
    test=phen["published_realized_siring_tests"]
    if not (0<test["siring_by_date"]["p"]<1 and
            0<test["siring_by_pollen_transfer_opportunity"]["p"]<1 and
            test["siring_by_date"]["p"]>.05 and
            test["siring_by_pollen_transfer_opportunity"]["p"]>.05):
        raise ValueError("REALIZED_SIRING_NULL_SCOPE_CHANGED")
    if not (0<phen["paternity_assigned_seeds"]<=phen["genotyped_seeds"] and
            phen["reported_sires_mll"]>=phen["regression_genets"]>0):
        raise ValueError("PATERNITY_SAMPLE_GRAIN_MISMATCH")
    selfing=mating["marker_selfing_rate_population_mean"]
    delta=mating["marker_inbreeding_depression_population_mean"]
    if (mating["surveyed_mating_populations"]!={"monoecious":6,"dioecious":6} or
            not all(0<=v<=1 for v in list(selfing.values())+list(delta.values()))):
        raise ValueError("MARKER_STUDY_POPULATION_FRAME_CHANGED")
    contract=d["inference_contract"]
    if (not contract["raw_data_reanalysis_performed"] and
        not contract["direct_new_p_values_calculated"] and
        contract["pooling_not_permitted"] and
        len(contract["no_direct_empirical_support"])>=6):
        pass
    else:
        raise ValueError("SOURCE_CEILING_VIOLATED")
    return {
      "schema":"SLK_SAGITTARIA_PUBLISHED_ROUTE_TO_FITNESS_AUDIT_V2",
      "source_dois":{k:v["doi"] for k,v in p.items() if isinstance(v,dict) and "doi" in v},
      "experimental_transfer_2006":{
        "array_trials":array["array_trials"],
        "plants_per_array":array["plants_per_array"],
        "observed_flower_visits":array["flower_visits"],
        "observed_foraging_trips":array["foraging_trips"],
        "mean_flower_visits_per_trip_computed":round(mean,8),
        "original_sex_system_by_display_F":inter["F"],
        "original_sex_system_by_display_p":inter["p"],
        "original_low_display_winner":"dioecious",
        "original_high_display_winner":"monoecious",
        "outcome":"BETWEEN_PLANT_TRANSFER_SEQUENCE_PROXY_NOT_PATERNITY",
        "crossing_display_value_measured_exactly":None,
        "relative_lifetime_fitness_ratio":None
      },
      "bateman_natural_2022":{
         "sex_function_gradients":d_b,
         "male_beta_monoecious_minus_dioecious_descriptive":round(
           d_b["monoecious"]["male_size_adjusted_beta"]-
           d_b["dioecious"]["male_size_adjusted_beta"],8),
         "new_equivalence_test_or_p":None,
         "cross_sex_effect_measured":False,
         "published_unadjusted_vs_adjusted_signs_should_not_be_merged":True
      },
      "temporal_paternity_2023":{
         "genotyped_seeds":phen["genotyped_seeds"],
         "paternity_assigned_seeds":phen["paternity_assigned_seeds"],
         "reported_sires_mll":phen["reported_sires_mll"],
         "regression_genets":phen["regression_genets"],
         "date_original_F":test["siring_by_date"]["F"],
         "date_original_p":test["siring_by_date"]["p"],
         "opportunity_original_F":test["siring_by_pollen_transfer_opportunity"]["F"],
         "opportunity_original_p":test["siring_by_pollen_transfer_opportunity"]["p"],
         "evidence_for_positive_temporal_proxy_to_realized_siring":"NOT_DETECTED",
         "spatial_causal_effect_estimated":None,
         "temporal_proxy_hypothesis_proven_false":False
      },
      "marker_mating_2002":{
         "population_count_by_system":mating["surveyed_mating_populations"],
         "population_mean_selfing":selfing,
         "population_mean_marker_inbreeding_depression":delta,
         "monoecious_minus_dioecious_selfing_point_difference":round(
             selfing["monoecious"]-selfing["dioecious"],8),
         "joint_delta_times_selfing_lifetime_fitness_loss":None
      },
      "genet_mutant_frequency_evidence":"ABSENT",
      "rare_complete_dioecy_is_one_single_mutant":False,
      "SLK_Phi_g0_Delta_R_identified":False,
      "new_p_values":None,
      "individual_original_data_downloaded":False,
      "inference_contract":contract
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    d=json.loads(args.source.read_text(encoding="utf-8"))
    result=analyze(d)
    rendered=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered,encoding="utf-8")
    else:
        print(rendered,end="")


if __name__=="__main__":
    main()
