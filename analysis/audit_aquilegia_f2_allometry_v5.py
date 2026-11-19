#!/usr/bin/env python3
"""Original-source Aquilegia F2 organ reassembly across stamen-number classes.

Johns et al (2024), EvoDevo DOI 10.1186/s13227-024-00225-3.
The biological insight tested is spatially ordered anther/laminar identities
across low/high organ numbers; the prior authors already reported small
allometric effects. These are garden F2 phenotypes, not genes, selection or
native evolutionary regain.

Use only ONE predeclared flower per distinct plant for the unadjusted
logistic description; treat all 400 repeatedly measured flowers separately.
Do not impute missing stamen counts to zero. No genotypes or QTL are refit.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path

from audit_aquilegia_f2_partial_reassembly_v1 import (
    load_rows, summarize_rows, require
)


def _count(raw):
    if raw in ("NA", ""):
        return None
    try:
        n=int(raw)
    except (ValueError,TypeError):
        raise ValueError("INVALID_STAMEN_COUNT") from None
    if str(n)!=str(raw).strip() or n<=0:
        raise ValueError("INVALID_STAMEN_COUNT")
    return n


def prepare_original_flowers(rows):
    rows=list(rows)
    _=summarize_rows(rows,strict=False)  # validates original score/whorl keys
    by=collections.defaultdict(dict)
    for row in rows:
        key=(str(row["plant"]).strip(),str(row["flower"]).strip())
        whorl=row["whorl"]
        n=_count(row["stamens"])
        by[key][whorl]={
            "stamens":n,
            "AN":int(row["anther"]),
            "LE":int(row["lateral_expansion"]),
            "FU":int(row["fusion"])
        }
    flowers=[]
    for (plant,flower),score in by.items():
        i,o=score["inner"],score["outer"]
        require(i["stamens"]==o["stamens"],
                "CONFLICTING_INNER_OUTER_STAMEN_COUNT")
        flowers.append({
            "plant":plant,"flower":flower,"stamens":i["stamens"],
            "mosaic":int(
                any(v["AN"]==1 and v["LE"]>=2 and v["FU"]==1
                    for v in (i,o))
            ),
            "anther_inner_only_violation":int(
                i["AN"]==1 and o["AN"]==0
            ),
            "LE2_outer_only_violation":int(
                o["LE"]>=2 and i["LE"]<2
            ),
        })
    return flowers


def fit_binomial_logit(x,y):
    """Finite two-parameter logistic MLE; logodds unit supplied by caller.

    Inversion of observed Fisher Hessian gives descriptive individual-level
    Wald intervals. This is NOT a model of F2 allele segregation.
    """
    x=list(x);y=list(y)
    require(len(x)==len(y) and len(x)>=10,"LOGIT_INSUFFICIENT_ROWS")
    require(all(math.isfinite(float(t)) for t in x) and
            all(v in (0,1) for v in y),"LOGIT_INVALID_INPUT")
    require(0<sum(y)<len(y),"LOGIT_OUTCOME_SINGLE_CLASS")
    a=math.log((sum(y)+.5)/(len(y)-sum(y)+.5))
    b=0.0
    for _ in range(100):
        h00=h01=h11=g0=g1=0.0
        for t,z in zip(x,y):
            expTerm=max(-40,min(40,a+b*t))
            p=1/(1+math.exp(-expTerm))
            w=p*(1-p)
            g0+=z-p;g1+=(z-p)*t
            h00+=w;h01+=w*t;h11+=w*t*t
        det=h00*h11-h01*h01
        require(det>1e-12,"LOGIT_SINGULAR_DESIGN")
        d0=(h11*g0-h01*g1)/det
        d1=(h00*g1-h01*g0)/det
        require(max(abs(d0),abs(d1))<100,"LOGIT_DIVERGED")
        a+=d0;b+=d1
        if max(abs(d0),abs(d1))<1e-11:
            break
    else:
        raise ValueError("LOGIT_DID_NOT_CONVERGE")
    # recompute Fisher Hessian at final MLE
    h00=h01=h11=0.0
    for t in x:
        p=1/(1+math.exp(-max(-40,min(40,a+b*t))))
        w=p*(1-p)
        h00+=w;h01+=w*t;h11+=w*t*t
    det=h00*h11-h01*h01
    require(det>1e-12,"LOGIT_SINGULAR_DESIGN")
    se=math.sqrt(h00/det)
    return {
        "intercept":a,"slope":b,"standard_error":se,
        "OR":math.exp(b),
        "OR_95_CI":[math.exp(b-1.96*se),math.exp(b+1.96*se)],
        "wald_ci_not_clade_replicate_or_causal":True,
    }


def analyse_mosaic_allometry(rows,strict=True):
    rows=list(rows)
    base=summarize_rows(rows,strict=strict)
    flowers=prepare_original_flowers(rows)
    require(len(flowers)==base["source"]["scored_flowers"],
            "UNEXPECTED_FLOWER_SOURCE_NUMBER")
    byplant=collections.defaultdict(list)
    for item in flowers:
        byplant[item["plant"]].append(item)
    first=[]
    for plant in sorted(byplant,key=lambda v:int(v)):
        a=byplant[plant]
        chosen=next((f for f in a if f["flower"]=="a"),None)
        if chosen is None:
            require(len(a)==1,"MISSING_FIRST_FLOWER_IN_DUPLICATED_PLANT")
            chosen=a[0]
        first.append(chosen)
    known_stamens=sorted(x["stamens"] for x in flowers
                         if x["stamens"] is not None)
    require(known_stamens,"NO_STAMEN_NUMBER_OBSERVATIONS")
    def percentile(q):
        return known_stamens[int((len(known_stamens)-1)*q)]
    t1,t2=percentile(1/3),percentile(2/3)
    require(t1<t2,"STAMEN_COUNT_TERTILES_UNIDENTIFIABLE")

    def group(arr):
        filtered=[x for x in arr if x["stamens"] is not None]
        subsets={
            "low":[x for x in filtered if x["stamens"]<=t1],
            "middle":[x for x in filtered if t1<x["stamens"]<=t2],
            "high":[x for x in filtered if x["stamens"]>t2],
        }
        def stats(xs):
            n=len(xs)
            return {
                "n":n,"mosaic_count":sum(x["mosaic"] for x in xs),
                "mosaic_fraction":sum(x["mosaic"] for x in xs)/n if n else None,
                "full_nesting_exceptions":sum(
                    bool(x["anther_inner_only_violation"] or
                         x["LE2_outer_only_violation"]) for x in xs),
                "anther_inner_only_violations":sum(
                    x["anther_inner_only_violation"] for x in xs),
                "LE2_outer_only_violations":sum(
                    x["LE2_outer_only_violation"] for x in xs),
            }
        return {
            "sample_n":len(filtered),
            "mosaic_phenotypes":sum(x["mosaic"] for x in filtered),
            "full_nesting_exception_count":sum(
                bool(x["anther_inner_only_violation"] or
                     x["LE2_outer_only_violation"]) for x in filtered),
            "allometry_classes":{k:stats(v) for k,v in subsets.items()}
        }
    allflowers=group(flowers)
    oneper=group(first)
    fit=fit_binomial_logit(
        [(r["stamens"]-40)/10 for r in first
         if r["stamens"] is not None],
        [r["mosaic"] for r in first if r["stamens"] is not None]
    )
    oneper["unadjusted_logit"]={
        "model":"binary_mosaic_vs_centered_stamen_count_unadjusted_one_flower_per_F2_plant",
        "stamen_number_unit":"per 10 additional fertile stamens",
        "OR_per_10_stamens":fit["OR"],
        "lower_95_percent_Wald_CI":fit["OR_95_CI"][0],
        "upper_95_percent_Wald_CI":fit["OR_95_CI"][1],
        "slope":fit["slope"],
        "SE":fit["standard_error"],
        "independent_genetic_effect_inferred":False,
    }
    result={
        "schema":"slk_aquilegia_original_F2_allometry_vs_organ_mosaic_v5",
        "source":{
            "doi":"10.1186/s13227-024-00225-3",
            "phenotype_git_blob_sha1":
                base["source"]["original_publisher_csv_git_blob_sha1"],
            "F2_plants":len(byplant),"flowers":len(flowers),
            "whorl_score_rows":len(rows),
            "flowers_with_stamen_count":len(known_stamens),
            "flowers_missing_stamen_count":len(flowers)-len(known_stamens),
            "one_per_plant_with_stamen_count":oneper["sample_n"],
            "one_per_plant_missing_stamen_count":
                len(first)-oneper["sample_n"],
            "size_tertile_cutoffs_calculated_on_all_available_flowers":
                [t1,t2],
            "missing_stamen_count_not_assigned_zero":True,
        },
        "all_scored_flowers":allflowers,
        "first_flower_per_genotype":oneper,
        "biological_ceiling":{
            "400_flowers_equal_400_independent_genotypes":False,
            "parent_stamen_count_is_unbiased_reproductive_resource_measure":False,
            "non_significant_mosaic_slope_proves_zero_allometry":False,
            "morphological_nesting_proves_genetic_module_independence":False,
            "floral_organ_pollen_fertility_measured":False,
            "SLK_structural_payoff_or_pollinator_selection_estimated":False,
            "ANTO_native_re_expression_genetic_rate_estimated":False,
            "genotype_marker_matrix_loaded":False,
        },
    }
    if strict:
        require((len(byplant),len(flowers),len(known_stamens),
                 oneper["sample_n"],t1,t2)==(231,400,367,211,37,43),
                 "PINNED_ORIGINAL_MORPHOMETRIC_ALLOMETRY_DRIFT")
        require([(oneper["allometry_classes"][k]["n"],
                  oneper["allometry_classes"][k]["mosaic_count"])
                 for k in ("low","middle","high")]
                ==[(67,17),(72,26),(72,28)],
                "PINNED_ORIGINAL_MOSAIC_BY_SIZE_DRIFT")
        require([oneper["allometry_classes"][k]["full_nesting_exceptions"]
                 for k in ("low","middle","high")]
                ==[1,0,0], "PINNED_DIRECTIONAL_WHORL_CONSTRAINT_DRIFT")
    return result


def main():
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=root/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv")
    p.add_argument("--expected",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    report=analyse_mosaic_allometry(load_rows(args.input),strict=True)
    if args.expected is not None:
        reference=json.loads(args.expected.read_text(encoding="utf-8"))
        require(report==reference,"ALLOMETRY_SOURCE_RECEIPT_DRIFT")
    text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text)


if __name__=="__main__":
    main()
