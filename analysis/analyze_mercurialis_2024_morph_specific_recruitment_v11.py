#!/usr/bin/env python3
"""2024 mother-level sex-morph offspring accounting (descriptive only).

Effective output = maternal mature-seed/flower * sex-phenotype count / seeds sown.
This assumes sampled seeds represent a maternal crop. Values are laboratory
phenotypes after germination, not adult reproduction, genotypes, or actual paternity.
"""
import argparse
import collections
import json
import math
import random

from audit_mercurialis_2024_next_generation_morph_stage_v10 import load
from reanalyze_mercurialis_2024_parent_to_germination_v1 import solve, mean

OUTCOMES={
    "female":"Prog_F",
    "hermaphrodite":"Prog_H",
    "male":"Prog_M",
    "male_sterile":"Prog_Mst",
    "unsexed_died_early":"Prog_NA",
}

def enrich(rs):
    out=[]
    for a in rs:
        r=dict(a)
        seeds=r["mother_seed_total"]
        flowers=r["mother_flower_total"]
        if flowers is None or flowers<=0 or seeds is None or seeds<0:
            raise ValueError("Missing or invalid flower/seed total")
        if r["gap"]==0:
            if not r["sown"] or r["germinated"]>r["sown"]:
                raise ValueError("Invalid maternal seed sample denominator: "+r["id"])
            if r["sown"]>seeds:
                # A published data-quality mismatch. Never extrapolate an assay
                # with more sampled seeds than the recorded total crop.
                r["sample_exclusion"]="sown_seed_count_exceeds_reported_total_crop"
                for label in OUTCOMES:r["per_flower_"+label]=None
            else:
                r["sample_exclusion"]=None
                for label,col in OUTCOMES.items():
                    r["per_flower_"+label]=(seeds/flowers)*(r[col]/r["sown"])
        elif seeds==0 and r["sown"] in (None,0) and r["germinated"] is None:
            for label in OUTCOMES:r["per_flower_"+label]=0.0
            r["sample_exclusion"]=None
        else:raise ValueError("Not a source-verified zero-seed row")
        r["per_flower_total"]=(sum(r["per_flower_"+c] for c in OUTCOMES)
                              if r["sample_exclusion"] is None else None)
        r["mother_seed_per_flower"]=seeds/flowers
        if r["gap"]==0 and r["sample_exclusion"] is None:
            expected=(seeds/flowers)*(r["germinated"]/r["sown"])
            if abs(expected-r["per_flower_total"])>1e-12:
                raise ValueError("Phenotype contributions do not sum to germinants per flower")
        out.append(r)
    if len(out)!=72:raise ValueError("Wrong mother N")
    return out

def vec(r,interaction):
    x=[1.,float(r["Sex"]=="F"),float(r["dist"]),
       float(r["block"]=="2"),float(r["block"]=="3")]
    if interaction:x.append(float(r["Sex"]=="F")*float(r["dist"]))
    return x

def fit(rs,metric,interaction=False):
    valid=[r for r in rs if r.get(metric) is not None and math.isfinite(r[metric])]
    n=len(vec(valid[0],interaction))
    if len(valid)<n+4:return None
    xx=[[0.]*n for _ in range(n)]
    xy=[0.]*n
    for r in valid:
        v=vec(r,interaction); y=r[metric]
        for i in range(n):
            xy[i]+=v[i]*y
            for j in range(n):xx[i][j]+=v[i]*v[j]
    beta=solve(xx,xy)
    if beta is None:return None
    return {"n_mothers":len(valid),"distance_slope_H":beta[2],
            "distance_slope_F":beta[2]+beta[5] if interaction else beta[2],
            "F_minus_H":beta[1],"sex_by_distance":beta[5] if interaction else None}

def boot(rs,metric,interaction=False,reps=1500,seed=20261117):
    pools=collections.defaultdict(list)
    for r in rs:pools[(r["block"],r["Sex"],r["dist"])].append(r)
    rng=random.Random(seed)
    out=[]
    for _ in range(reps):
        sample=[rng.choice(pool) for pool in pools.values() for i in range(len(pool))]
        item=fit(sample,metric,interaction)
        if item:out.append(item)
    def interval(key):
        xs=sorted(x[key] for x in out if x[key] is not None)
        if len(xs)<reps*.95:return None
        return [xs[int(.025*(len(xs)-1))],xs[int(.975*(len(xs)-1))]]
    return {"successful_resamples":len(out),"H_slope_CI":interval("distance_slope_H"),
            "F_slope_CI":interval("distance_slope_F"),
            "sex_by_distance_CI":interval("sex_by_distance"),
            "limits":"mother resamples in fixed block x sex x distance; 3 blocks not general-population replication"}

def run(zip_path):
    rs=enrich(load(zip_path))
    keys=["per_flower_"+x for x in OUTCOMES]+["per_flower_total","mother_seed_per_flower"]
    cells={}
    for sex in ("F","H"):
        for distance in (0.,.5,1.5):
            grp=[r for r in rs if r["Sex"]==sex and r["dist"]==distance]
            cells[f"{sex}_{distance}"]={"n_mothers":len(grp),
                   "means":{k:mean([r[k] for r in grp]) for k in keys},
                   "n_assay_crop_consistent":sum(r["sample_exclusion"] is None for r in grp),
                   "sum_expected_morph_offspring":sum(r["per_flower_total"] for r in grp if r["per_flower_total"] is not None)}
    analyses={}
    for metric in keys:
        analyses[metric]={"main":fit(rs,metric),"main_bootstrap":boot(rs,metric),
                 "interaction":fit(rs,metric,True),
                 "interaction_bootstrap":boot(rs,metric,True,seed=20261118),
                 "leave_one_block_out":{
                    block:fit([r for r in rs if r["block"]!=block],metric,True)
                    for block in ("1","2","3")}}
    return {
        "source":"10.6084/m9.figshare.26521189.v1",
        "zip_md5":"365ab41f1d6192344a3b3fec87654e49",
        "source_n_mothers":72,
        "sample_exclusions":[{"id":r["id"],"sex":r["Sex"],"distance":r["dist"],
                              "crop_seeds":r["mother_seed_total"],"sown":r["sown"],
                              "reason":r["sample_exclusion"]}
                             for r in rs if r["sample_exclusion"]],
        "n_mothers_with_phenotyped_progeny":71,
        "source_categories":"F, M, H, Mst, NA (died before sex could be assigned)",
        "cell_summary":cells,
        "analyses":analyses,
        "cautions":[
            "This quantity is expected number of laboratory germinated morphs per source female flower, inferred from subsampled sown seeds.",
            "It is not lifetime offspring, DNA sex-genotype transmission, selfing rate, paternity, or evolution of dioecy.",
            "A female morph descendant and a male-sterile-male phenotype must not be equated with specific alleles or CMS cytotypes.",
            "Sampling fraction of seeds differs by mother and distance; representative seed-assay subsampling is not established.",
            "If sowing sample count exceeds reported crop count the mother is explicitly excluded from extrapolated morph-per-flower endpoints; parent count discrepancies are reported.",
            "Sex expression is measured after germination; unsexed early deaths are kept as their own category.",
            "Ring placement simultaneously changes distance to central males, plant spacing, resource gradient and potentially paternal pollen composition.",
            "Sex by distance analyses are exploratory, only 3 blocks and 9 distant hermaphrodite mothers.",
            "1997 Pannell and 2007 Eppley-Pannell previously established male availability/density as mating-system controls in nonidentical systems."
        ]}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    o=run(a.zip)
    with open(a.out,"w") as f:json.dump(o,f,indent=2,ensure_ascii=False)
    print("SLK_MERCURIALIS_2024_PER_FLOWER_MORPH_V11_START")
    print(json.dumps(o,ensure_ascii=False,indent=2))
    print("SLK_MERCURIALIS_2024_PER_FLOWER_MORPH_V11_END")
