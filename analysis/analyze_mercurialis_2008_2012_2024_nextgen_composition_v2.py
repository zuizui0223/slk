#!/usr/bin/env python3
"""Source-level biological comparison: partner composition vs next-generation sex morphs.

Replicates 2008 8-pop density-paired sex ratio means/t from ORIGINAL rounded
Table 1; 2012 20 plot-level offspring proportions and 2024 primary reported
109-pop landscape. Data levels, reproductive modes, population structures
and years are different. DO NOT fit cross-experiment "female buffering" causal
effect, call non-significant density differences zero, or infer SLK rare invasion.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"


def mean(x):
    if not x:
        raise ValueError("EMPTY_STUDY_CELL")
    return sum(x)/len(x)


def paired_t(a,b):
    if len(a)!=len(b) or len(a)<3:
        raise ValueError("INVALID_PAIRED_SAMPLE")
    diff=[x-y for x,y in zip(a,b)]
    std=statistics.stdev(diff)
    if std==0:
        raise ValueError("DEGENERATE_PAIRED_SAMPLE")
    return mean(diff)/(std/math.sqrt(len(diff)))


def analyze(src):
    p=src["study_2008"]
    t=src["study_2012"]
    g=src["study_2024"]
    if (p["doi"]!="10.1086/587524" or t["doi"]!="10.1371/journal.pone.0035597"
        or g["doi"]!="10.1002/ajb2.16429"):
        raise ValueError("PRIMARY_DOI_MISMATCH")
    if (p["experimental_source_populations"]!=8 or
        len(p["original_table1"])!=8 or
        p["density_plants_per_m2"]!={"low":12.25,"high":250} or
        p["array_parent_sex_system"]!="ANDRODIOECY_MALES_AND_HERMAPHRODITES_NO_FEMALES"):
        raise ValueError("SOURCE_2008_UNIT_CHANGED")
    rows=p["original_table1"]
    if len({r["id"] for r in rows})!=8:
        raise ValueError("DUPLICATE_2008_POPULATION")
    for row in rows:
        for level in ("low","high"):
            z=row[level]
            if not (0<=z["parent_male"]<=1 and 0<=z["progeny_male"]<=1
                    and z["lambda"]>0 and type(z["parent_n"]) is int
                    and type(z["progeny_n"]) is int and z["progeny_n"]>0):
                raise ValueError("INVALID_2008_ORIGINAL_FRACTION")
    low=[r["low"]["progeny_male"] for r in rows]
    high=[r["high"]["progeny_male"] for r in rows]
    lowp=[r["low"]["parent_male"] for r in rows]
    highp=[r["high"]["parent_male"] for r in rows]
    lowlambda=[r["low"]["lambda"] for r in rows]
    highlambda=[r["high"]["lambda"] for r in rows]
    raw_t=paired_t(high,low)
    change_t=paired_t([x-y for x,y in zip(high,highp)],
                      [x-y for x,y in zip(low,lowp)])
    lambda_t=paired_t(highlambda,lowlambda)
    tests=p["original_stat_tests"]
    if (abs(raw_t-tests["high_minus_low_progeny_male_paired_t_magnitude"])>.12
        or abs(change_t-tests["high_minus_low_progeny_change_from_parent_paired_t"])>.12
        or abs(lambda_t-tests["lambda_high_low_t_magnitude"])>.12):
        raise ValueError("ORIGINAL_2008_PAIRED_T_NOT_REPRODUCED")
    if any(abs(mean(q)-p["original_means"][k])>.02 for q,k in (
            (low,"low_progeny_male"),(high,"high_progeny_male"),
            (lowlambda,"low_lambda"),(highlambda,"high_lambda"))):
        raise ValueError("ORIGINAL_2008_PRINTED_MEANS_MISMATCH")
    nrows={level:sum(r[level]["progeny_n"] for r in rows)
           for level in ("low","high")}
    reported=p["original_table1_published_total_progeny"]
    if nrows["high"]!=reported["high"] or nrows["low"]-reported["low"]!=54:
        raise ValueError("PUBLISHED_2008_TABLE_INTERNAL_N_MISMATCH_LOST")

    if (t["plot_count"]!=20 or len(t["original_table2"])!=20
        or t["plots_per_density_male_presence"]!=5
        or t["density_plants_per_m2"]!={"low":8.5,"high":156.25}
        or t["type"]!="TRIOECIOUS_ALL_TREATMENTS_CONTAIN_FEMALES; FACTOR IS MALE_PRESENCE_NOT_FEMALE_PRESENCE"):
        raise ValueError("ORIGINAL_2012_PLOT_DESIGN_CHANGED")
    row12=t["original_table2"]
    if len(set(row["id"] for row in row12))!=20 or sum(r["n"] for r in row12)!=6076:
        raise ValueError("ORIGINAL_2012_PLOT_COUNTS_CHANGED")
    cells={}
    parent_fraction={}
    declines={"decrease":0,"increase":0,"ambiguous":0}
    checks=[]
    for density in ("low","high"):
        for maletreat in ("absent","present"):
            key=density+"_"+maletreat
            selected=[r for r in row12 if r["density"]==density and r["males"]==maletreat]
            if len(selected)!=5:
                raise ValueError("ORIGINAL_2012_FACTORIAL_CELL_CHANGED")
            parent=t["parental_sex_counts"][density][maletreat]
            if sum(parent.values())!=t["parent_plants_per_plot"][density]:
                raise ValueError("ORIGINAL_2012_PARENTS_INVALID")
            pf=parent["female"]/sum(parent.values())
            parent_fraction[key]=pf
            for r in selected:
                if (type(r["n"]) is not int or r["n"]<200
                    or not all(0<=r[k]<=1 for k in ("female","male","herm"))
                    or abs(sum(r[k] for k in ("female","male","herm"))-1)>.011):
                    raise ValueError("ORIGINAL_2012_PROPORTION_INVALID")
                if maletreat=="absent" and r["ph"] is not None:
                    raise ValueError("POLLEN_RELATIVE_MALE_COMPARISON_WITH_NO_MALES")
                if maletreat=="present" and (r["ph"] is None or r["ph"]<=0):
                    raise ValueError("MISSING_ORIGINAL_MALE_POLLEN_ALLOCATION")
                # Published table reports 2 decimal digits; conservative
                # interval accommodates rounding without claiming integer
                # offspring counts from parent-level n.
                label=("decrease" if r["female"]+.005<pf
                       else "increase" if r["female"]-.005>pf
                       else "ambiguous")
                declines[label]+=1
                checks.append({"plot":r["id"],"density":density,
                               "male_treatment":maletreat,
                               "female_change_vs_parent_with_rounding":label})
            cells[key]={
                "n_plots":len(selected),
                "n_progeny_reported":sum(r["n"] for r in selected),
                "male_progeny_plot_mean":round(mean([r["male"] for r in selected]),8),
                "female_progeny_plot_mean":round(mean([r["female"] for r in selected]),8),
                "hermaphrodite_progeny_plot_mean":round(mean([r["herm"] for r in selected]),8),
                "parental_female_share":round(pf,8),
                "source_proportions_are_rounded":True
            }
    if declines!={"decrease":17,"increase":2,"ambiguous":1}:
        raise ValueError("FEMALE_NEXT_GEN_DIRECTION_BOUND_CHANGED")
    if (t["original_progeny_GLM"]["male_density_in_males_present_plots"]["p"]!=">.50"
        or t["original_progeny_GLM"]["female_density"]["p"]!=">.50"):
        raise ValueError("ORIGINAL_2012_NONSIGNIFICANCE_CHANGED")
    effort=t["original_table1_reproductive_effort"]
    maternal_f=effort["female_seed_biomass_fraction"]["mean"]
    maternal_h=effort["hermaphrodite_seed_biomass_fraction"]["mean"]
    paternal_m=effort["male_pollen_biomass_fraction"]["mean"]
    paternal_h=effort["hermaphrodite_pollen_biomass_fraction"]["mean"]
    if not (maternal_f>maternal_h and paternal_m>paternal_h):
        raise ValueError("ORIGINAL_2012_ALLOCATION_ORDER_CHANGED")

    if (g["sample_size_populations"]!=109 or
        sum(g["source_category_counts"].values())!=109 or
        g["sex_system_threshold_per_sex_frequency"]!=.025 or
        g["long_term_tracking"]["persisted_three_years"]!=5):
        raise ValueError("ORIGINAL_2024_POPULATION_FRAME_CHANGED")
    glm=g["original_full_population_glm"]
    if (glm["female_vs_density"]["p"]<=.05
        or glm["female_vs_male_frequency"]["p"]<=.05
        or g["female_mean_grouped_by_males_above_2_5_percent"]["original_wilcoxon_p"]!="<.0001"):
        raise ValueError("MISREAD_2024_GROUP_DIFFERENCE_AS_GENERAL_EFFECT")

    return {
      "schema":"SLK_MERCURIALIS_2008_2012_2024_ORIGINAL_AGGREGATE_AUDIT_V2",
      "source_dois":{"2008":p["doi"],"2012":t["doi"],"2024":g["doi"]},
      "androdioecy_2008":{
        "populations":8,
        "low_density":p["density_plants_per_m2"]["low"],
        "high_density":p["density_plants_per_m2"]["high"],
        "progeny_male_low_unweighted_plot_fraction":round(mean(low),8),
        "progeny_male_high_unweighted_plot_fraction":round(mean(high),8),
        "progeny_male_high_minus_low":round(mean(high)-mean(low),8),
        "male_frequency_change_high_minus_low_after_parent_adjustment":round(
             mean([h-p for h,p in zip(high,highp)])-
             mean([l-p for l,p in zip(low,lowp)]),8),
        "paired_t_high_minus_low_rounded_source":round(raw_t,8),
        "paired_t_parent_delta_rounded_source":round(change_t,8),
        "lambda_high_mean":round(mean(highlambda),8),
        "lambda_low_mean":round(mean(lowlambda),8),
        "lambda_paired_t_rounded_source":round(lambda_t,8),
        "source_original_paired_t_significance":"Original parent-adjusted t=2.6, df=7, p<.05",
        "original_published_progeny_total":reported,
        "sum_of_original_row_progeny_N":nrows,
        "unresolved_original_low_N_difference":nrows["low"]-reported["low"],
        "new_p_values":None,
        "individual_pedigree_recovered":False
      },
      "trioecy_2012":{
        "plot_replicates":20,
        "offspring_phenotyped":6076,
        "female_present_in_all_20_plots":True,
        "male_treatment_is_presence_not_female_presence":True,
        "factorial_cells":cells,
        "parental_female_fraction_by_cell":{k:round(v,8) for k,v in parent_fraction.items()},
        "male_present_high_minus_low_progeny_male_plot_mean":round(
            cells["high_present"]["male_progeny_plot_mean"]-
            cells["low_present"]["male_progeny_plot_mean"],8),
        "male_absent_low_plot_mean_male_progeny":cells["low_absent"]["male_progeny_plot_mean"],
        "male_absent_high_plot_mean_male_progeny":cells["high_absent"]["male_progeny_plot_mean"],
        "male_progeny_without_male_parents_indicates_gene_flow":True,
        "female_seed_allocation_fraction_relative_to_hermaphrodite":round(
            maternal_f/maternal_h,8),
        "male_pollen_allocation_fraction_relative_to_hermaphrodite":round(
            paternal_m/paternal_h,8),
        "female_next_generation_direction_certain_under_rounding":declines,
        "female_direction_per_plot":checks,
        "original_male_density_test":t["original_progeny_GLM"]["male_density_in_males_present_plots"],
        "original_female_density_test":t["original_progeny_GLM"]["female_density"],
        "new_offspring_level_significance":None,
        "causal_female_buffering_effect_measured":False
      },
      "natural_trioecy_2024":{
        "studied_population_count":109,
        "reported_categories":g["source_category_counts"],
        "original_grouping_threshold":g["sex_system_threshold_per_sex_frequency"],
        "female_mean_in_male_rich_vs_poor_populations":g["female_mean_grouped_by_males_above_2_5_percent"],
        "full_population_female_vs_density_p":glm["female_vs_density"]["p"],
        "full_population_female_vs_male_frequency_p":glm["female_vs_male_frequency"]["p"],
        "five_of_eight_persisted_three_years":True,
        "demonstrated_indefinite_evolutionary_equilibrium":False,
        "CMS_nuclear_restorer_linkage_confirmed_molecularly":False,
        "restorer_fitness_cost_measured":False
      },
      "cross_study_difference_in_density_contrast_2008_vs_2012_descriptive":round(
          (mean(high)-mean(low))-
          (cells["high_present"]["male_progeny_plot_mean"]-
           cells["low_present"]["male_progeny_plot_mean"]),8),
      "cross_study_difference_significance":None,
      "directly_randomized_female_presence_between_studies":False,
      "SLK_Phi_g0_Delta_R_measured":False,
      "new_causal_effect_sizes":None,
      "limits":src["inferential_limits"]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=analyze(json.loads(args.source.read_text(encoding="utf-8")))
    output=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf-8")
    else:
        print(output,end="")

if __name__=="__main__":
    main()
