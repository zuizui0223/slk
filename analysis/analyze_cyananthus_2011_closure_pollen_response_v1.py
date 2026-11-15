#!/usr/bin/env python3
"""Reconstruct ONLY the original 2011 Cyananthus Table 1 closure contingency.

All results use rounded published group counts / means. No new plant-level
inference, covariate adjustment, causal closure benefit or SLK gate estimate.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/evidence/cyananthus_2011_closure_pollen_response_primary_source_v1.json"


def compute(data):
    if data["citation"]["doi"]!="10.1093/aob/mcr224":
        raise ValueError("UNEXPECTED_PRIMARY_SOURCE")
    f=data["female_experiment"]
    if f["initiated_total"]!=216 or f["initiated_flowers_per_pollen_dose"]!=72:
        raise ValueError("ORIGINAL_EXPOSURE_DENOMINATOR_CHANGED")
    doses=("10","20","30")
    if set(f["source_table1_usable"])!=set(doses):
        raise ValueError("ORIGINAL_POLLEN_DOSES_CHANGED")
    rows=[]
    for dose in doses:
        row=f["source_table1_usable"][dose]
        a,b=row["closed"],row["open"]
        if (any(isinstance(v,bool) or not isinstance(v,int) or v<0 for v in (a,b))
                or a+b==0):
            raise ValueError("INVALID_TABLE_COUNT")
        rows.append([a,b])
    total=sum(sum(r) for r in rows)
    if total!=f["usable_total"] or total>=f["initiated_total"]:
        raise ValueError("ORIGINAL_USABLE_SAMPLE_CHANGED")
    rowsum=[sum(r) for r in rows]
    colsum=[sum(row[c] for row in rows) for c in range(2)]
    if min(colsum)<=0:
        raise ValueError("DEGENERATE_TABLE")
    chisq=sum(
        (rows[i][j]-rowsum[i]*colsum[j]/total)**2/
        (rowsum[i]*colsum[j]/total)
        for i in range(3) for j in range(2)
    )
    # df = (3 - 1) * (2 - 1) = 2; exact chi-square survival for df=2
    p=math.exp(-chisq/2)
    if abs(chisq-f["original_pearson_chisq"])>0.001:
        raise ValueError("PUBLISHED_TEST_NOT_REPRODUCED")
    pexp=data["perfect_experiment"]
    if pexp["initiated_total"]!=180 or pexp["usable_total"]!=98:
        raise ValueError("ORIGINAL_PERFECT_FLOWER_COUNTS_CHANGED")
    perf={}
    for source in ("cross","self"):
        group=pexp["source_table1_usable"][source]
        perf[source]={}
        for dose in ("20","30"):
            row=group[dose]
            a,b=row["closed"],row["open"]
            if (any(isinstance(v,bool) or not isinstance(v,int) or v<0 for v in (a,b))
                    or a+b==0):
                raise ValueError("INVALID_PERFECT_COUNT")
            perf[source][dose]={"closed":a,"open":b,"usable_n":a+b,
                                "closure_fraction":round(a/(a+b),8)}
    if sum(v["usable_n"] for group in perf.values() for v in group.values())!=98:
        raise ValueError("PERFECT_COHORT_MISMATCH")
    ring=data["paired_prevent_closure_sufficient_cross_pollen"]
    if ring["perfect"]["pairs"]!=22 or ring["female"]["pairs"]!=30:
        raise ValueError("PAIRED_SAMPLES_CHANGED")
    closure_fractions={d:round(rows[i][0]/rowsum[i],8)
                       for i,d in enumerate(doses)}
    return {
        "schema":"slk_cyananthus_2011_closure_published_table1_result_v1",
        "doi":data["citation"]["doi"],
        "female_usable_table_rows":{
            d:{"closed":rows[i][0],"open":rows[i][1],"usable_n":rowsum[i],
               "closure_fraction":closure_fractions[d]}
            for i,d in enumerate(doses)
        },
        "female_source_treated_n":f["initiated_total"],
        "female_source_usable_n":total,
        "female_source_unusable_n":f["initiated_total"]-total,
        "female_source_usable_fraction":round(total/f["initiated_total"],8),
        "pearson_chisq_on_published_usable_counts":round(chisq,8),
        "pearson_df":2,
        "pearson_p_for_df2":round(p,12),
        "published_original_chisq":f["original_pearson_chisq"],
        "perfect_source_treated_n":pexp["initiated_total"],
        "perfect_source_usable_n":pexp["usable_total"],
        "perfect_source_unusable_n":pexp["initiated_total"]-pexp["usable_total"],
        "perfect_source_usable_fraction":round(pexp["usable_total"]/pexp["initiated_total"],8),
        "perfect_usable_closure_table":perf,
        "closure_latency_hours":{
            sex:{"mean":data["closure_latency"][sex]["mean_hours"],
                 "se":data["closure_latency"][sex]["se_hours"],
                 "n":data["closure_latency"][sex]["n"]}
            for sex in ("female","perfect_cross")
        },
        "paired_ring_ample_pollen":{
            sex:{"pairs":ring[sex]["pairs"],
                 "seed_mean_ring_minus_control":round(
                     ring[sex]["ring_prevented_seed_mean"]-
                     ring[sex]["control_seed_mean"],5),
                 "original_p":ring[sex]["original_p"]}
            for sex in ("female","perfect")
        },
        "different_flower_cohorts_not_one_path":True,
        "new_plant_cluster_adjusted_p":None,
        "new_confidence_intervals":None,
        "early_closure_caused_seed_loss_under_low_pollen":None,
        "pollen_donor_manipulation_established":False,
        "slk_historical_origin_or_fitness_gate":None,
        "claim_limits":data["claim_limits"]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,default=SOURCE)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=compute(json.loads(args.source.read_text(encoding="utf-8")))
    blob=json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(blob,encoding="utf-8")
    else:
        print(blob,end="")


if __name__=="__main__":
    main()
