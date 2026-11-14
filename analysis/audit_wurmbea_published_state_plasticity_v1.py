#!/usr/bin/env python3
"""Recompute published Wurmbea field sex-switching and resource-expression totals.

This program reads only *author-reported aggregate Table 1 and percentages*
stored in data/evidence. It is not an individual-level data download, genetic
analysis, new evidence for trait reacquisition, or SLK fitness fit.
Primary studies:
 Ramsey & Vaughton (1999), J Ecol doi:10.1046/j.1365-2745.1999.00336.x
 Vaughton & Ramsey (2012), Ann Bot doi:10.1093/aob/mcr163
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


def choose(n,k):
    if k<0 or k>n:
        return 0
    return math.comb(n,k)


def fisher_two_sided(a,b,c,d):
    require(all(type(x) is int and x>=0 for x in (a,b,c,d)),
            "INVALID_2X2_POSITIVE_COUNTS")
    total=a+b+c+d
    successes=a+c
    sample=a+b
    require(total>0 and sample>0 and sample<total, "INVALID_2X2_SAMPLE")
    def prob(k):
        return choose(successes,k)*choose(total-successes,sample-k)/choose(total,sample)
    obs=prob(a)
    return min(1.0,sum(prob(k) for k in range(max(0,sample-(total-successes)),min(successes,sample)+1)
                       if prob(k)<=obs*(1+1e-10)))


def audit_wurmbea_published_aggregates(data,strict=True):
    study=data["original_1999"]
    rows=study["followup_1983"]
    require([r["source_1981"] for r in rows]==["female","male_only","fruiting_male"],
            "PUBLISHED_TRANSITION_STATES_CHANGED")
    for r in rows:
        require(sum(r[k] for k in ("count_F_1983","count_M_1983",
                                    "count_FM_1983","count_nonflower_1983"))==r["n_1981"],
                "PUBLISHED_1999_ROW_SUM_CHANGED")
    n=sum(r["n_1981"] for r in rows)
    refl=sum(r["count_F_1983"]+r["count_M_1983"]+r["count_FM_1983"] for r in rows)
    non=n-refl
    require(n==study["tagged_same_plants_1981"],"ORIGINAL_1999_TAGGED_COHORT_CHANGED")
    male,fruiting=rows[1],rows[2]
    male_ref=male["count_M_1983"]+male["count_FM_1983"]
    fm_ref=fruiting["count_M_1983"]+fruiting["count_FM_1983"]
    row=data["original_2012"]
    groups=row["population_groups"]
    require(len(groups)==4,"PUBLISHED_2012_POPULATIONS_CHANGED")
    for g in groups:
        require(g["high"]["n"]+g["low"]["n"]==g["n"],"PUBLISHED_RESOURCE_COHORT_CHANGED")
        require(0<=g["high"]["positive"]<=g["high"]["n"] and
                0<=g["low"]["positive"]<=g["low"]["n"],
                "INVALID_PUBLISHED_PERFECT_FLOWER_COUNTS")
    # Only the original Wallan, W. dioica subdioecious 100-male
    # experiment is used in the original within-pop resource contrast.
    wallan=next(g for g in groups if g["name"].startswith("W. dioica subdioecious"))
    a=wallan["high"]["positive"]
    b=wallan["high"]["n"]-a
    c=wallan["low"]["positive"]
    d=wallan["low"]["n"]-c
    results={
      "schema":"wurmbea_original_published_individual_expression_math_check_v1",
      "1999_tagged":n,
      "1999_1983_reflowered":refl,
      "1999_1983_nonflowering":non,
      "1999_male_to_fruiting_male":male["count_FM_1983"],
      "1999_male_reflowered":male_ref,
      "1999_male_to_fruiting_male_fraction":male["count_FM_1983"]/male_ref,
      "1999_fruiting_male_to_male":fruiting["count_M_1983"],
      "1999_fruiting_male_reflowered":fm_ref,
      "1999_fruiting_male_to_male_fraction":fruiting["count_M_1983"]/fm_ref,
      "1999_females_remaining_female_if_reflowered":rows[0]["count_F_1983"],
      "2012_subdioecious_high_positive":a,
      "2012_subdioecious_low_positive":c,
      "2012_resource_absolute_difference":a/(a+b)-c/(c+d),
      "2012_resource_exact_fisher_two_sided":fisher_two_sided(a,b,c,d),
      "2012_dioecious_perfect_flower_positive":
          next(g for g in groups if g["name"].startswith("W. dioica dioecious"))["high"]["positive"]+
          next(g for g in groups if g["name"].startswith("W. dioica dioecious"))["low"]["positive"],
      "2012_biglandulosa_all_positive":all(
          g["high"]["positive"]==g["high"]["n"] and
          g["low"]["positive"]==g["low"]["n"] for g in groups
          if "biglandulosa" in g["name"]),
      "published_aggregate_only_not_raw_population_experiment":True,
      "observed_within_lifetime_sex_change_not_native_genetic_regain":True
    }
    if strict:
        require((n,refl,non)==(90,68,22),"ORIGINAL_1999_FOLLOWUP_TOTALS_CHANGED")
        require((male_ref,male["count_FM_1983"],fm_ref,fruiting["count_M_1983"])==(28,14,23,7),
                "ORIGINAL_1999_MALE_TRANSITIONS_CHANGED")
        require((a,b,c,d)==(33,17,21,29),"ORIGINAL_2012_WALLAN_COUNTS_CHANGED")
        require(math.isclose(results["2012_resource_exact_fisher_two_sided"],
                             0.026802559248039502,rel_tol=0,abs_tol=1e-12),
                "ORIGINAL_2012_TWO_SIDED_FISHER_CHANGED")
    return results


def main():
    p=argparse.ArgumentParser()
    root=Path(__file__).resolve().parents[1]
    p.add_argument("--source",type=Path,default=root/"data/evidence/WURMBEA_1999_2012_REAL_SEX_REEXPRESSION_SOURCE_RECEIPT_V1.json")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    r=audit_wurmbea_published_aggregates(json.loads(args.source.read_text(encoding="utf-8")))
    text=json.dumps(r,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text)


if __name__=="__main__":
    main()
