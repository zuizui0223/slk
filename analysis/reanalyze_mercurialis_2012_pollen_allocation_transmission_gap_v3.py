#!/usr/bin/env python3
"""Exploratory original-plot reanalysis of Mercurialis 2012, Table 2.

2012 PLOS ONE DOI 10.1371/journal.pone.0035597 gives 10 male-containing
plots, 5 low and 5 high density, with relative reproductive investment
p_h = pi_hermaphrodite / pi_male and next-generation male morph frequencies.

Enumerates all C(10,5)=252 density relabelings of rounded PLOT-LEVEL means.
This is an EXPLORATORY label-permutation reference distribution, not a
reproduction of the authors' GLM, not raw individual parentage, and not an
SLK rare mutant invasion or causal mediation fit. Fertilizer? None; this
is the original experimental plot density/male-composition design.
"""
from __future__ import annotations
import argparse
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"


def mean(values):
    if not values:
        raise ValueError("EMPTY_MEAN")
    return sum(values)/len(values)


def permutation_split(values, is_high):
    """Two-sided exact label exchange of 10 PLOT summary values, 5 vs 5."""
    if len(values)!=10 or len(is_high)!=10 or sum(is_high)!=5:
        raise ValueError("EXPECTED_FIVE_VS_FIVE_PLOTS")
    if any(type(x) not in (float,int) for x in values):
        raise ValueError("BAD_PLOT_STAT")
    observed=mean([v for v,h in zip(values,is_high) if h])-mean([
        v for v,h in zip(values,is_high) if not h])
    null=[]
    for high_idx in combinations(range(10),5):
        selected=set(high_idx)
        null.append(mean([values[i] for i in range(10) if i in selected])-
                    mean([values[i] for i in range(10) if i not in selected]))
    greater=sum(abs(v)>=abs(observed)-1e-12 for v in null)
    return {
        "high_minus_low_from_published_plot_means":round(observed,8),
        "possible_labelings":len(null),
        "two_sided_extreme_labelings":greater,
        "exploratory_two_sided_permutation_p":round(greater/len(null),10),
        "is_a_new_test_not_original_published_GLMM":True,
        "p_value_from_printed_two_decimal_place_numbers":True,
    }


def analyze(src):
    a=src["study_2012"]
    if a["doi"]!="10.1371/journal.pone.0035597":
        raise ValueError("WRONG_ORIGINAL_SOURCE")
    if a["plot_count"]!=20 or len(a["original_table2"])!=20:
        raise ValueError("ORIGINAL_TABLE_SIZE_CHANGED")
    selected=sorted((r for r in a["original_table2"] if r["males"]=="present"),
                    key=lambda r:(0 if r["density"]=="low" else 1,r["id"]))
    if (len(selected)!=10 or
        {key:sum(r["density"]==key for r in selected)
         for key in ("low","high")}!={"low":5,"high":5}):
        raise ValueError("NOT_ORIGINAL_BALANCED_TRIOECIOUS_DESIGN")
    high=[r["density"]=="high" for r in selected]
    if {r["id"] for r in selected}!={1,3,8,17,19,4,12,13,15,18}:
        raise ValueError("PUBLISHED_PLOT_IDS_NOT_MATCHED")
    if any(r["ph"] is None or not 0<r["ph"]<1 or not 0<=r["male"]<=1
           or not 0<=r["female"]<=1 or r["n"]<200 for r in selected):
        raise ValueError("BAD_SOURCE_PLOT_SUMMARY")

    # Verify biological interpretation from the original Table 2 caption:
    # p_h is relative biomass investment in pollen, NOT directly siring.
    # Hold this meaning in output and note.
    tests={}
    for field,semantic in (
            ("ph","hermaphrodite_over_male_fraction_of_aboveground_biomass_to_pollen"),
            ("male","offspring_male_morph_fraction_after_common_greenhouse"),
            ("female","offspring_female_morph_fraction_after_common_greenhouse")):
        values=[r[field] for r in selected]
        test=permutation_split(values,high)
        low_mean=mean([v for v,h in zip(values,high) if not h])
        high_mean=mean([v for v,h in zip(values,high) if h])
        test["low_density_five_plot_unweighted_mean"]=round(low_mean,8)
        test["high_density_five_plot_unweighted_mean"]=round(high_mean,8)
        test["one_source_unit"]="independently_manipulated_parental_plot"
        test["measurement_semantics"]=semantic
        # Worst-case rounded ±0.005 per plot yields a group contrast ±0.010.
        # Conservative lower/upper of high-low are valid without imputing
        # missing individual phenotypes.
        test["printed_2_decimal_group_gap_rounding_bounds"]=[
            round(high_mean-low_mean-.01,8),
            round(high_mean-low_mean+.01,8)
        ]
        tests[field]=test

    if tests["ph"]["two_sided_extreme_labelings"]!=2:
        raise ValueError("PUBLISHED_POLLEN_EFFORT_SEPARATION_CHANGED")
    if tests["male"]["two_sided_extreme_labelings"]!=210:
        raise ValueError("PUBLISHED_MALE_PROGENY_RELABELLING_CHANGED")
    if not (max(r["ph"] for r in selected if r["density"]=="high")<=
            min(r["ph"] for r in selected if r["density"]=="low")):
        raise ValueError("ORIGINAL_WITHIN_PLOT_POL_LEN_NOT_SEPARATED")
    if (a["original_progeny_GLM"]["male_density_in_males_present_plots"] !=
            {"t":-.54,"p":">.50"}):
        raise ValueError("ORIGINAL_SOURCE_GLM_CHANGED")

    parents=a["parental_sex_counts"]
    parent_male_shares={
        density:parents[density]["present"]["male"]/
                sum(parents[density]["present"].values())
        for density in ("low","high")}
    return {
        "schema":"SLK_MERCURIALIS_2012_POLLEN_EFFORT_TRANSMISSION_GAP_V3",
        "source_doi":a["doi"],
        "published_table":"Table 2, male-present plots only",
        "plot_ids_ordered":[r["id"] for r in selected],
        "low_and_high_plot_counts":{"low":5,"high":5},
        "sex_composition_parental_male_share":{
            k:round(v,8) for k,v in parent_male_shares.items()
        },
        "published_metric_analyses":tests,
        "2012_published_male_progeny_density_GLM":a["original_progeny_GLM"]["male_density_in_males_present_plots"],
        "plot_pollen_alloc_change_and_progeny_change_decouple_in_observed_means":True,
        "evidence_no_effect_on_male_offspring_frequency_proven":False,
        "biomass_pollen_allocation_equivalent_to_actual_siring":False,
        "offspring_sex_frequency_is_actual_fitness_of_rare_genotype":False,
        "multiple_exploratory_tests_family_wise_adjustment":None,
        "novel_individual_observation_data":None,
        "SLK_rare_invasion_estimate":None,
        "claim_limits":[
            "This is an exploratory new plot-level permutation reanalysis of existing printed source means, NOT the 2012 original GLM p-value.",
            "Printed values are rounded to two decimal places; deterministic group-gap bounds and exact label enumeration refer only to printed plot values.",
            "Only the 10 male-present parent plots are compared; 2012 has another 10 male-absent plots and 6076 total assessed offspring.",
            "Comparing a statistically detectable biomass allocation ratio shift and a nonsignificant male progeny fraction shift DOES NOT test whether their true effects differ statistically or whether allocation has zero effect.",
            "p_h is hermaphrodite/male relative pollen investment as fraction of aboveground biomass, not realized pollen receipt, fatherhood, or total absolute pollen flux.",
            "Male progeny morph ratio after one generation is affected by mating, sex determinants and inheritance; it is not directly assigned paternity or SLK mutant invasion fitness.",
            "Male-present low and high treatments have 16/49 versus 75/225 parental male ratio: close to but not perfectly identical.",
            "Original study's parent-plots were controlled but family genotype effects, selection after germination and source-population ancestry are not identifiable from Table 2.",
            "No raw source individual records or 2024 109-population appendix downloaded. The 2024 Figshare endpoint was inaccessible in current environment.",
            "Do not mix 2008 androdioecy, 2012 trioecy and 2024 field populations into a same-genotype causal female buffering estimate."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    out=json.dumps(analyze(json.loads(args.source.read_text(encoding="utf-8"))),
                   ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(out,encoding="utf-8")
    else:
        print(out,end="")

if __name__=="__main__":
    main()
