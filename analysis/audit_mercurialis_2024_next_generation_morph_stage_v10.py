#!/usr/bin/env python3
"""Mother-level offspring phenotype and early-loss audit for Nguyen et al. 2024.

Purely source-reproducible: checksum-verified original field experiment CSV.
All child categories describe phenotype AFTER germination/sex assessment, NOT
Mendelian genotypes, genetic parentage, juvenile lifetime survival or invasion.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import zipfile

from analyze_mercurialis_2024_germination_binomial_v9 import fit, boot

SOURCE_MD5 = "365ab41f1d6192344a3b3fec87654e49"
SOURCE_DOI = "10.6084/m9.figshare.26521189.v1"
SOURCE_FILE = "Data_field_experiment/Pollination and distance/Data_pollen_limitation_and_distance.csv"
CATEGORIES = ("Prog_F", "Prog_M", "Prog_H", "Prog_NA", "Prog_Mst")


def nonneg_int(s):
    if s is None or not s.strip() or s.strip().upper() in ("NA","NAN"):return None
    x=float(s)
    if x<0 or not x.is_integer():raise ValueError("Invalid offspring count: "+s)
    return int(x)


def load(path):
    with open(path,"rb") as f: data=f.read()
    if hashlib.md5(data).hexdigest()!=SOURCE_MD5:raise ValueError("Original archive MD5 mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        rows=list(csv.DictReader(io.StringIO(z.read(SOURCE_FILE).decode("utf-8-sig"))))
    if len(rows)!=84:raise ValueError("Unexpected raw plant count")
    out=[]
    for r in rows:
        if r["Sex"] not in ("F","H"):continue
        d={"id":r["ID"],"Sex":r["Sex"],"dist":float(r["Dist"]),
           "block":r["Bloc"],"observations":r["Observation"],
           "mother_flower_total":nonneg_int(r["Female_flowers_tot"]),
           "mother_seed_total":nonneg_int(r["nombre graines"]),
           "sown":nonneg_int(r["Seed_sown"]),
           "germinated":nonneg_int(r["Prog_tot"])}
        for k in CATEGORIES:d[k]=nonneg_int(r[k])
        d["complete_category_counts"]=all(d[k] is not None for k in CATEGORIES)
        if d["complete_category_counts"] and d["germinated"] is not None:
            d["category_sum"]=sum(d[k] for k in CATEGORIES)
            d["gap"]=d["category_sum"]-d["germinated"]
            d["typed"]=d["germinated"]-d["Prog_NA"]
            if d["typed"]<0 or d["category_sum"]>d["sown"]:
                raise ValueError("Invalid category or sowing denominators: "+d["id"])
        else:
            d["category_sum"]=None
            d["gap"]=None
            d["typed"]=None
        out.append(d)
    if len(out)!=72:raise ValueError("Unexpected F/H count")
    if len(set(d["id"] for d in out))!=72:raise ValueError("Duplicated plants")
    return out


def overview(rs):
    r={"n_mothers_total":len(rs),"n_with_germinated":sum(x["germinated"] is not None for x in rs),
       "n_complete_category_counts":sum(x["complete_category_counts"] for x in rs),
       "n_complete_with_no_sum_gap":sum(x["gap"]==0 for x in rs),
       "n_with_mismatch":sum(x["gap"] is not None and x["gap"]!=0 for x in rs)}
    complete=[x for x in rs if x["gap"]==0]
    r["sown"]=sum(x["sown"] for x in complete)
    r["germinated"]=sum(x["germinated"] for x in complete)
    r["typed"]=sum(x["typed"] for x in complete)
    r["category_total"]={k:sum(x[k] for x in complete) for k in CATEGORIES}
    r["mismatches"]=[{"id":x["id"],"gap":x["gap"],"total":x["germinated"],"sum":x["category_sum"]}
                 for x in rs if x["gap"] is not None and x["gap"]!=0][:20]
    r["unresolved_ids"]=[x["id"] for x in rs if x["gap"] is None]
    return r


def prepared(rs,numer,denom):
    out=[]
    for r in rs:
        if r["gap"]!=0:continue
        target=numer(r)
        total=denom(r)
        if target is None or total is None or total<=0:continue
        if target>total or target<0:raise ValueError("Invalid outcome numerator")
        out.append({"Sex":r["Sex"],"dist":r["dist"],"block":r["block"],
                    "sown":float(total),"germinated":float(target),
                    "observations":r["observations"]})
    return out


def summarize(rs):
    target=overview(rs)
    unassayed=[x for x in rs if x["gap"] is None]
    # The only missing progeny phenotype record is the H mother with zero
    # mature seeds. It cannot contribute to a conditional phenotype ratio.
    allowed_structural_zero=all(x["mother_seed_total"]==0 and
                               (x["sown"] in (None,0)) and
                               x["germinated"] is None for x in unassayed)
    if target["n_with_mismatch"] or not allowed_structural_zero:
        # Never silently impute phenotype labels for an unknown seed family.
        return {"state":"INVALID_OR_INCOMPLETE_COUNTS","audit":target}
    target["excluded_from_phenotype_models"]=[
        {"id":x["id"],"sex":x["Sex"],"reason":"No mature seeds, no germination assay"}
        for x in unassayed]
    typed=prepared(rs,lambda r:r["Prog_F"],lambda r:r["typed"])
    male=prepared(rs,lambda r:r["Prog_M"]+r["Prog_Mst"],lambda r:r["typed"])
    herm=prepared(rs,lambda r:r["Prog_H"],lambda r:r["typed"])
    lost=prepared(rs,lambda r:r["Prog_NA"],lambda r:r["germinated"])
    specs={"female_phenotype_fraction_among_typed":typed,
           "male_plus_male_sterile_fraction_among_typed":male,
           "hermaphrodite_fraction_among_typed":herm,
           "unsexed_died_early_fraction_among_germinated":lost}
    analyses={}
    for name,x in specs.items():
        analyses[name]={"point":fit(x),"mother_bootstrap":boot(x),
                         "sex_distance_point":fit(x,True),
                         "sex_distance_bootstrap":boot(x,True,seed=20261118),
                         "leave_one_block_out":{b:fit([r for r in x if r["block"]!=b])
                                                for b in ("1","2","3")}}
    cells={}
    for sex in ("F","H"):
        for d in (0,.5,1.5):
            subset=[x for x in rs if x["Sex"]==sex and x["dist"]==d and x["gap"]==0]
            base=overview(subset)
            typ=base["typed"]
            germ=base["germinated"]
            base["female_among_typed"]=base["category_total"]["Prog_F"]/typ if typ else None
            base["herm_among_typed"]=base["category_total"]["Prog_H"]/typ if typ else None
            base["unknown_among_germinated"]=base["category_total"]["Prog_NA"]/germ if germ else None
            cells[f"{sex}_{d}"]=base
    return {"state":"COMPLETE","overall":target,"by_cell":cells,"analyses":analyses}


def main(path):
    rows=load(path)
    result=summarize(rows)
    result.update({"source":SOURCE_DOI,"source_zip_md5":SOURCE_MD5,
                   "source_csv":SOURCE_FILE,
                   "original_total_plants":84,
                   "n_female_and_hermaphrodite":len(rows),
                   "interpretation":["All offspring morphs are classified after germination and survival to sex assessment, not genotypes.",
                   "Unsexed progeny include plants dying too early to assign a phenotype; never assume they are females or males.",
                   "Mother F/H differs in inherited cytoplasmic sterility and nuclear restoration background; morph fraction is not a causal estimate of genetic selection.",
                   "Unknown pollen donors and selfing are not measured in this ring experiment.",
                   "The 2017 J Ecol study has already reported offspring sex-dependent responses in different dioecious plants.",
                   "Phenotypic ratios in the offspring are not equal to the next adult-generation population sex ratio.",
                   "Multiple exploratory outcomes and only three blocks prohibit confirmatory claims."]})
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    z=main(args.zip)
    with open(args.out,"w") as f:json.dump(z,f,ensure_ascii=False,indent=2)
    print("SLK_2024_OFFSPRING_MORPH_AUDIT_V10_START")
    print(json.dumps(z,ensure_ascii=False,indent=2))
    print("SLK_2024_OFFSPRING_MORPH_AUDIT_V10_END")
