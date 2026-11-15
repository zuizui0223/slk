#!/usr/bin/env python3
"""Author-reported published results: Mercurialis real 2021 sex-system reversal.

Source #1: Cossard et al. Current Biology 2021 Table 1 and G5 sex-ratio
proxy for XX female paternity.
Source #2: Santos Del Blanco et al. Ecology Letters 2019 independent,
nonisogenic inflorescence comparisons, author-reported siring penalties.
NO new genotype level fitness model or original raw Data S1 refit.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/mercurialis_2019_2021_restored_function_siring_source_v6.json"


def mean(z):
    if not z:
        raise ValueError("EMPTY_SOURCE_POPULATION_SET")
    return sum(z)/len(z)


def compute(s):
    x=s["experimental_2021"]
    y=s["architecture_2019"]
    if {x["doi"],y["doi"]}!={"10.1016/j.cub.2020.12.028","10.1111/ele.13207"}:
        raise ValueError("WRONG_PRIMARY_SOURCE_DOI")
    d=x["population_replicates"]
    if d!={"female_only":3,"male_female_controls":3} or x["plant_n_per_population"]!={"G0":180,"G1_G4":210}:
        raise ValueError("EXPERIMENTAL_DESIGN_CHANGED")
    if x["original_G1_common_garden_male_flower_ratio_vs_control"]!=8.77 or x["original_G4_common_garden_male_flower_ratio_vs_control"]!=23.3:
        raise ValueError("ORIGINAL_CONTROL_RELATIVE_MALE_FLOWER_RESULT_CHANGED")
    if x["male_flower_positive_females"]!={"G0":.0548,"G4":.693}:
        raise ValueError("SAME_GENETIC_COHORT_FLOWERING_DIRECTION_CHANGED")
    t=x["selfing_genotypes"]
    if t["markers"]!=8 or x["author_G1_vs_G4_selfing_difference_p"]!=.10:
        raise ValueError("SELFING_SOURCE_OR_NULL_STAT_CHANGED")
    groups={}
    for gen in ("G1","G4"):
        per=[]
        control=[]
        for kind,prows in (("female_only",per),("control",control)):
            pop=t[gen+"_"+kind+"_selfing"] if gen+"_"+kind+"_selfing" in t else t[gen+"_"+kind]
            # Source uses G1 and G4 keys with explicit control/female-only groups
            assert set(pop)==({"S1","S2","S3"} if kind=="female_only" else {"C1","C2","C3"})
            for pid,r in sorted(pop.items()):
                if (type(r["n"]) is not int or not 103<=r["n"]<=120
                    or not 0<=r["s"]<=1 or type(r["nonzero_significant"]) is not bool):
                    raise ValueError("INVALID_ORIGINAL_MICROSATELLITE_TABLE")
                prows.append((pid,r["n"],r["s"],r["nonzero_significant"]))
        values=[r[2] for r in per]
        weighted=sum(n*ss for _,n,ss,_ in per)/sum(n for _,n,ss,_ in per)
        groups[gen]={
          "female_only_population_estimates":[
              {"population":pid,"genotyped_offspring":n,"author_RMES_selfing_s":sv,
               "nonzero_significant":sig}
              for pid,n,sv,sig in per],
          "controls_population_estimates":[
              {"population":pid,"genotyped_offspring":n,"author_RMES_selfing_s":sv,
               "nonzero_significant":sig}
              for pid,n,sv,sig in control],
          "female_only_unweighted_mean_s":round(mean(values),9),
          "female_only_offspring_count_weighted_mean_of_estimates_NOT_pooled_fit":round(weighted,9),
          "female_only_population_n":len(per),
          "control_population_n":len(control),
          "female_only_significantly_nonzero_populations":sum(int(z[3]) for z in per),
          "female_only_reported_n_genotyped":sum(r[1] for r in per)
        }
    g1=groups["G1"]["female_only_unweighted_mean_s"]
    g4=groups["G4"]["female_only_unweighted_mean_s"]
    if not(abs(g1-x["paper_mean_selfing_G1_female_only"])<.005 and
           abs(g4-x["paper_mean_selfing_G4_female_only"])<.005):
        raise ValueError("PRINTED_SELFING_AUTHOR_AVERAGES_CHANGED")
    z=x["G5_reintroduced_males"]
    if (z["arrays"]!=6 or z["array_females"]!=50 or z["array_XY_males"]!=50
        or z["selected_XX_mothers_male_progeny_fraction"]!=.436
        or z["control_XX_mothers_male_progeny_fraction"]!=.503
        or z["paper_male_sired_sex_ratio_null"]!=.5
        or z["paper_inferred_fraction_XX_female_sired"]!=.128):
        raise ValueError("G5_REINTRODUCTION_SOURCE_CHANGED")
    inferred=2*(.5-z["selected_XX_mothers_male_progeny_fraction"])
    if abs(inferred-z["paper_inferred_fraction_XX_female_sired"])>1e-10:
        raise ValueError("FEMALE_PATERNITY_RATIO_REPRODUCTION_FAILED")
    immigration=x["G0_contaminant_males"]
    if (immigration["males"]!=9 or immigration["offspring"]!=812
        or sum(immigration["population_males"])!=9
        or sum(immigration["population_denominators"])!=812):
        raise ValueError("G0_POLLEN_IMMIGRATION_SOURCE_CHANGED")
    if (y["exp1"]["mating_arrays"]!=30 or y["exp1"]["progeny_sex_phenotyped"]!=6000
        or y["exp2"]["mating_arrays"]!=12 or y["exp2"]["offspring_genotyped"]!=720
        or y["exp2"]["marker_loci"]!=5
        or not y["exp2"]["exp2_31pct_comparison_requires_equal_selfing_assumption"]):
        raise ValueError("2019_ARCHITECTURE_SIRING_EXPERIMENT_CHANGED")
    if (y["exp1"]["F_like_siring_less_than_M_like_fraction"]!=.25 or
        y["exp2"]["F_like_siring_less_than_M_like_fraction"]!=.31
        or not y["not_the_2021_evolved_lineages"]
        or not y["not_a_randomized_in_the_same_genome_inflorescence_manipulation"]):
        raise ValueError("SOURCE_MORPHOLOGY_INFERENCE_CHANGED")
    return {
      "schema":"SLK_MERCURIALIS_2021_EXP_REVERSAL_2019_SIRING_LEGACY_RESULT_V6",
      "source_dois":{"experiment_2021":x["doi"],"morphology_2019":y["doi"]},
      "true_population_evolutionary_replicates":d["female_only"],
      "G0_acute_plastic_ratio_vs_same_generation_controls":x["original_G0_mate_absence_male_flower_ratio"],
      "G1_evolved_line_male_flower_ratio_vs_current_controls":x["original_G1_common_garden_male_flower_ratio_vs_control"],
      "G4_evolved_line_male_flower_ratio_vs_current_controls":x["original_G4_common_garden_male_flower_ratio_vs_control"],
      "base_to_G4_incidence_male_flowers":x["male_flower_positive_females"],
      "base_to_G4_incidence_difference_percentage_points":round(
           100*(x["male_flower_positive_females"]["G4"]-
                x["male_flower_positive_females"]["G0"]),8),
      "selfing_8_SSR_markers_author_RMES":{
        **groups,
        "G4_minus_G1_female_only_unweighted_mean_s":round(g4-g1,9),
        "author_test_between_G1_and_G4_p":x["author_G1_vs_G4_selfing_difference_p"],
        "increasing_selfing_proven":False,
        "new_selfing_model_fit":None
      },
      "G0_immigrant_male_progeny":{
        "original_male_n":immigration["males"],
        "original_offspring_n":immigration["offspring"],
        "male_fraction":round(immigration["males"]/immigration["offspring"],9),
        "confirms_mating_system_not_perfectly_hermetically_sealed":True
      },
      "G5_XY_males_reintroduced_sex_ratio_fatherhood":{
         "reintroduction_mating_arrays":z["arrays"],
         "female_plants_per_array":z["array_females"],
         "XY_males_per_array":z["array_XY_males"],
         "control_male_progeny_fraction":z["control_XX_mothers_male_progeny_fraction"],
         "evolved_XX_mother_male_progeny_fraction":z["selected_XX_mothers_male_progeny_fraction"],
         "son_deficit_vs_XY_half_sex_ratio":round(
             z["paper_male_sired_sex_ratio_null"]-
             z["selected_XX_mothers_male_progeny_fraction"],8),
         "source_author_inferred_XX_female_sired_fraction":round(inferred,8),
         "not_direct_father_genotypes":True,
         "selfing_fraction_cannot_be_separated_from_XX_cross":True,
         "one_generation_not_male_reinvasion_fixed":True
      },
      "2019_independent_source_architecture_paternal_penalty":{
         "exp1_arrays":y["exp1"]["mating_arrays"],
         "exp1_original_progeny_sexed":y["exp1"]["progeny_sex_phenotyped"],
         "exp1_F_like_paternal_reduction_vs_M_like_with_males":y["exp1"]["F_like_siring_less_than_M_like_fraction"],
         "exp2_arrays":y["exp2"]["mating_arrays"],
         "exp2_5_SSR_offspring_genotyped":y["exp2"]["offspring_genotyped"],
         "exp2_F_like_paternal_reduction_vs_M_like":y["exp2"]["F_like_siring_less_than_M_like_fraction"],
         "exp2_equal_selfing_assumption_required":True,
         "exp2_M_like_selfing_unidentified":True,
         "not_same_cohort_as_2021_selected_XX":True,
         "not_isogenic_inflorescence_swap":True
      },
      "source_2021_initial_seed_origin_20_vs_35_discrepancy_unresolved":True,
      "2021_data_S1_Excel_raw_downloaded":False,
      "new_p_values_or_CIs":None,
      "rare_genotype_or_historical_origin_SLK_Phi_g0_Delta_R":None,
      "limits":s["critical_scope"]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    res=compute(json.loads(a.source.read_text(encoding="utf-8")))
    content=json.dumps(res,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(content,encoding="utf-8")
    else:
        print(content,end="")


if __name__=="__main__":
    main()
