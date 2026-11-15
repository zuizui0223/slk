#!/usr/bin/env python3
"""Original published Sagittaria genotype access and resource reaction bounds.

Uses printed 2004 Table 2 fractions, n and crossover resource genotypes.
No fabricated flower-level or clone-paired individuals, no newly calculated
source G-test p, and no claim of new mutation, SLK invasion or fixation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/evidence/sagittaria_genetic_access_and_ecological_filter_primary_v1.json"


def compatible_count_interval(n, fraction, precision=2):
    if (type(n) is not int or n<=0 or isinstance(fraction,bool)
            or not isinstance(fraction,(float,int))
            or not math.isfinite(fraction) or not 0<=fraction<=1):
        raise ValueError("INVALID_ORIGINAL_ROUNDED_FRACTION")
    half=0.5*10**(-precision)
    # Observed printed fraction to nearest 0.01 (ties are not assumed).
    lo=max(0, math.ceil((fraction-half)*n-1e-10))
    hi=min(n, math.ceil((fraction+half)*n-1e-10)-1)
    if lo>hi:
        raise ValueError("NO_FEASIBLE_INTEGER")
    return [lo,hi]


def compute(src):
    g=src["studies"]["genetic_access_2004"]
    if g["doi"]!="10.1098/rspb.2003.2580":
        raise ValueError("WRONG_ORIGINAL_GENETIC_SOURCE")
    f2=g["f2_and_backcross_original_table2"]["class_a"]
    if (f2["n"]!=676 or f2["families"]!=8 or
        f2["original_pooled_G"]!=1.37 or f2["original_p"]!=.63):
        raise ValueError("ORIGINAL_F2_STUDY_UNITS_CHANGED")
    classes=("male","hermaphrodite","female")
    intervals={c:compatible_count_interval(f2["n"],f2[c+"_fraction"]) for c in classes}
    n=f2["n"]
    feasible=[
        (m,h,n-m-h)
        for m in range(intervals["male"][0],intervals["male"][1]+1)
        for h in range(intervals["hermaphrodite"][0],intervals["hermaphrodite"][1]+1)
        if intervals["female"][0]<=n-m-h<=intervals["female"][1]
    ]
    if not feasible:
        raise ValueError("NO_REAL_F2_COUNTS_MATCH_PRINTED_ROUNDING")
    hmin=min(x[1] for x in feasible)
    hmax=max(x[1] for x in feasible)
    f1=g["f1_original_table1"]["dioecious_male_x_monoecious_hermaphrodite"]
    if (f1["n"]!=241 or f1["original_p"]!=.01 or f1["expected_male_fraction"]!=.5):
        raise ValueError("ORIGINAL_F1_DIFFERENCE_CHANGED")
    mrange=compatible_count_interval(f1["n"],f1["male_fraction"])
    r=src["studies"]["sex_expression_resource_2004"]
    if (r["male_clone_genotypes"]!=23 or r["female_clone_genotypes"]!=27 or
       r["male_ramets_total"]!=92 or r["per_genotype_ramets_high"]!=2 or
       r["per_genotype_ramets_low"]!=2):
        raise ValueError("ORIGINAL_MALE_CLONAL_DESIGN_CHANGED")
    high_mixed=r["male_genotypes_with_male_and_female_flowers_high"]
    low_male_only=r["male_genotypes_reported_male_only_low"]
    total=r["male_clone_genotypes"]
    if (any(type(x)!=int for x in (high_mixed,low_male_only,total))
            or min(high_mixed,low_male_only)<0 or
            max(high_mixed,low_male_only)>total):
        raise ValueError("INVALID_RESOURCE_COUNTS")
    # A union bound on the intersection of high_mixed and low_male_only.
    # At least this many original genotypes MUST have been mixed only
    # under high fertilizer, irrespective of unknown paired identities.
    forced_transition=max(0,high_mixed+low_male_only-total)
    low_other=total-low_male_only
    if forced_transition!=8 or low_other!=2:
        raise ValueError("SOURCE_RESOURCE_PIGEONHOLE_CHANGED")
    return {
       "schema":"SLK_SAGITTARIA_GENOTYPE_AND_RESOURCE_BOUNDS_V1",
       "source_genetic_doi":g["doi"],
       "f2_observed_rounded_three_morph_shares":{
          c:f2[c+"_fraction"] for c in classes
       },
       "f2_offspring":n,"f2_families":f2["families"],
       "f2_feasible_integer_ranges":intervals,
       "f2_feasible_joint_integer_triples":len(feasible),
       "f2_hermaphroditic_offspring_minimum":hmin,
       "f2_hermaphroditic_offspring_maximum":hmax,
       "original_f2_pooled_G":f2["original_pooled_G"],
       "original_f2_pooled_G_p":f2["original_p"],
       "new_genotype_access_p_values":None,
       "f1_male_x_monoecious_hermaphrodite":{
         "offspring":f1["n"],
         "published_male_share":f1["male_fraction"],
         "male_integer_interval":mrange,
         "original_pooled_G":f1["original_pooled_G"],
         "original_pooled_G_p":f1["original_p"],
         "F1_skew_must_not_be_hidden":True
       },
       "resource_same_genotype":{
         "male_genotypes":total,
         "high_fertilizer_male_and_female_genotypes":high_mixed,
         "low_fertilizer_male_only_genotypes":low_male_only,
         "low_fertilizer_other_genotypes_upper_bound":low_other,
         "male_genotypes_forced_high_mixed_and_low_male_only_minimum":forced_transition,
         "minimum_fraction_forced_high_mixed_low_male_only":round(forced_transition/total,8),
         "low_treatment_mixed_count_exact":None,
         "paired_male_genotype_records_recovered":None,
         "male_genotype_independence_test":None,
         "female_genotypes_ever_male_flowering":r["female_genotypes_with_male_flowers_either_condition"]
       },
       "recombination_or_existing_genotype_segregation_not_new_mutations":True,
       "actual_rare_invasion_rate":None,
       "historical_gynodioecy_path_fixed":None,
       "cross_study_joint_fitness_model":None,
       "claim_limits":src["cross_source_claim_limits"]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=compute(json.loads(args.source.read_text(encoding="utf-8")))
    rendered=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered,encoding="utf-8")
    else:
        print(rendered,end="")


if __name__=="__main__":
    main()
