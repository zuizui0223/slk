#!/usr/bin/env python3
"""Within-experiment phenotype-by-distance contrast with adversarial missing sex.

Hexaploid Mercurialis annua, Nguyen et al. 2024, original Figshare
doi:10.6084/m9.figshare.26521189.v1; MD5 verified by source parser.
This is a comparison of observed *offspring morphs* conditional on germination,
not DNA siring, seed viability, genotypic invasion, or evolutionary response.
"""
import argparse
import collections
import json
import random
from audit_mercurialis_2024_xy_pollen_route_bounds_v12 import load, usable, aggregate

DOI="10.6084/m9.figshare.26521189.v1"
MD5="365ab41f1d6192344a3b3fec87654e49"

def by(rs,sex,dist):
    return [r for r in rs if r["Sex"]==sex and r["dist"]==dist]

def contrast(rs):
    # Center vs far only. The 0.5m ring is intentionally not forced into
    # a linear relationship, because the main F/H phenotype responses
    # are not monotonically ordered by distance.
    keys = {}
    for sex in ("H","F"):
        for dist in (0.,1.5):
            a=by(rs,sex,dist)
            if not a:return None
            keys[f"{sex}_{dist}"]=aggregate(a)
    h0,h1,f0,f1=(keys["H_0.0"],keys["H_1.5"],keys["F_0.0"],keys["F_1.5"])
    # Drop(sex) = P(Y | center,sex)-P(Y | far,sex). Y phenotype M+Mst.
    def drop_lo(a,b):return a["Y_fraction_lower"]-b["Y_fraction_upper"]
    def drop_hi(a,b):return a["Y_fraction_upper"]-b["Y_fraction_lower"]
    hd=(drop_lo(h0,h1),drop_hi(h0,h1))
    fd=(drop_lo(f0,f1),drop_hi(f0,f1))
    bound=(hd[0]-fd[1],hd[1]-fd[0])
    def typed_ratio(r):return r["known_Y_morph"]/r["sexed"]
    typed=(typed_ratio(h0)-typed_ratio(h1))-(typed_ratio(f0)-typed_ratio(f1))
    return {
        "n_mothers":{k:v["mothers"] for k,v in keys.items()},
        "group_germinated":{k:v["germinated"] for k,v in keys.items()},
        "group_unsexed":{k:v["unsexed_died_early"] for k,v in keys.items()},
        "H_center_minus_far_Y_drop_worstcase":list(hd),
        "F_center_minus_far_Y_drop_worstcase":list(fd),
        "H_drop_minus_F_drop_worstcase":list(bound),
        "sexed_only_difference_in_drops":typed,
        "strict_worstcase_positive":bound[0]>0
    }

def selected_mother_influence(rs):
    focus=[r for r in rs if r["dist"] in (0.,1.5)]
    results=[]
    for mother in focus:
        q=[r for r in rs if r["id"]!=mother["id"]]
        x=contrast(q)
        if x is None:raise ValueError("Unidentified contrast after dropping mother "+mother["id"])
        results.append({"removed_id":mother["id"],"sex":mother["Sex"],"dist":mother["dist"],
                        "lowerbound":x["H_drop_minus_F_drop_worstcase"][0],
                        "upperbound":x["H_drop_minus_F_drop_worstcase"][1]})
    return {
        "n_removed_one_by_one":len(results),
        "lowest_lowerbound":min(v["lowerbound"] for v in results),
        "highest_lowerbound":max(v["lowerbound"] for v in results),
        "all_positive":all(v["lowerbound"]>0 for v in results),
        "least_favorable_deleted_mother":min(results,key=lambda v:v["lowerbound"]),
        "source":"exact all-mother delete-one influence; not an uncertainty interval"
    }

def bootstrap(rs,reps=3000,seed=20261117):
    # Conditional on observed block × sex × distance cells: descriptive
    # sampling variation among mothers. Three blocks cannot quantify
    # random spatial block/site effects.
    rng=random.Random(seed)
    pools=collections.defaultdict(list)
    for x in rs:
        if x["dist"] in (0.,1.5):
            pools[(x["block"],x["Sex"],x["dist"])].append(x)
    values=[]
    for _ in range(reps):
        sample=[rng.choice(p) for p in pools.values() for j in range(len(p))]
        r=contrast(sample)
        if r is None:continue
        values.append((r["H_drop_minus_F_drop_worstcase"][0],
                       r["H_drop_minus_F_drop_worstcase"][1],
                       r["sexed_only_difference_in_drops"]))
    if len(values)<int(reps*.95):raise ValueError("Too many invalid source-stratum bootstrap samples")
    def percentile(i):
        a=sorted(t[i] for t in values)
        return [a[int(.025*(len(a)-1))],a[int(.975*(len(a)-1))]]
    return {
        "successful_samples":len(values),
        "worstcase_lowerbound_bootstrap_95pct":percentile(0),
        "worstcase_upperbound_bootstrap_95pct":percentile(1),
        "sexed_only_DID_bootstrap_95pct":percentile(2),
        "fraction_of_bootstraps_whose_worstcase_lowerbound_positive":sum(v[0]>0 for v in values)/len(values),
        "scope":"mother resampling within fixed source block x sexual morph x 0/1.5m cell, conditional on just 3 blocks",
        "not_a_confidence_interval_on_genetic_siring":True
    }

def run(zip_path):
    rows,unassayed=usable(load(zip_path))
    full=contrast(rows)
    if full is None:raise ValueError("Required maternal contrast does not exist")
    blocks={}
    leave_blocks={}
    for b in ("1","2","3"):
        blocks[b]=contrast([x for x in rows if x["block"]==b])
        leave_blocks[b]=contrast([x for x in rows if x["block"]!=b])
    out={
        "source_doi":DOI,"publisher_archive_md5":MD5,"n_plants_original":84,
        "n_maternal_F_H":72,"n_with_assayed_sex_morphs":len(rows),
        "excluded_zero_seed_mothers":unassayed,
        "contrast":"(P(Yphenotype|H center)-P(Yphenotype|H far)) - (P(Yphenotype|F center)-P(Yphenotype|F far))",
        "main":full,
        "within_block":blocks,
        "leave_one_block_out":leave_blocks,
        "one_mother_influence":selected_mother_influence(rows),
        "mother_bootstrap":bootstrap(rows),
        "source_crop_vs_assay_inconsistencies":[
          {"mother_id":r["id"],"reported_crop":r["mother_seed_total"],"assayed_sown":r["sown"],
           "sex":r["Sex"],"dist":r["dist"]}
          for r in rows if r["sown"]>r["mother_seed_total"]],
        "exclude_crop_assay_mismatch":contrast([r for r in rows if r["sown"]<=r["mother_seed_total"]]),
        "falsification_firewall":[
          "Missingness bounds are worst-case allocations of known early-unsexed germinants, NOT confidence intervals.",
          "Bootstrap considers mother-to-mother variability conditional on 3 blocks, NOT genetic parentage or independent sites.",
          "Offspring maleness M+Mst is used as a Y-carrier proxy based on separate controlled crosses; no Y genotyping done for this field cohort.",
          "Conditional paternal share two times phenotype fraction needs 1:1 sex segregation and no sex-specific survival; neither is verified in field ring experiment.",
          "No direct self-pollen transmission, H-to-H outcrossing, realized DNA paternal contributions or genotype-specific invasion rate.",
          "Spatial position influences pollen access, density/spacing and maternal environment; same genetic background not guaranteed.",
          "The 2017 Labouche et al. study demonstrated distance, pollen and offspring-quality relationships in different dioecious populations. Novelty is this public-data phenotype-by-morph contrast only."
        ]
    }
    if full["H_drop_minus_F_drop_worstcase"][0]<=0:raise ValueError("Source no longer supports strict worst-case morph contrast")
    return out

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--zip",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    o=run(a.zip)
    with open(a.out,"w",encoding="utf-8") as f:json.dump(o,f,ensure_ascii=False,indent=2)
    print("SLK_2024_MATERNAL_MORPH_DID_V13_START")
    print(json.dumps(o,ensure_ascii=False,indent=2))
    print("SLK_2024_MATERNAL_MORPH_DID_V13_END")
