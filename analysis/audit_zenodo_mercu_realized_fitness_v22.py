#!/usr/bin/env python3
"""Source-verified descriptive audit of Chen & Pannell 2025 *Mercurialis* CSVs.

Never executes publisher R scripts. All computed contrasts are descriptive,
with NO estimate of wild inbreeding depression, genetic invasion or causality.
"""
import argparse
import csv
import io
import json
import math
import statistics
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from probe_zenodo_mercu_paternity_v21 import API, checked_digest, file_entries, open_url, safe_source

DOI = "10.5281/zenodo.14542260"
CONCEPT_ID = "14542260"
REQUIRED = {
    "3G.csv": {"ID","Population","Male_flower_total","Female_flower_total","Genotyped_number","Selfed_seed_number","Selfing_rate","Biomass_whole","Realized_G","Phenotypic_G"},
    "3G_ID01.csv": {"ID","Population","Biomass_whole","Realized_G","Male_fitness","Female_fitness","Total_fitness","Inbreeding","Pop_ID"},
    "Genotype_3P.csv": {"Sample_Name","Population","Parent_Offspring"}
}

def parse_csv(z, basename):
    matches=[x for x in z.namelist() if x.rsplit("/",1)[-1]==basename]
    if len(matches)!=1:
        raise ValueError("Expected exactly one original "+basename)
    raw=z.read(matches[0])
    if len(raw)>3_000_000:
        raise ValueError("Unexpectedly large CSV")
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if not rows or not REQUIRED[basename].issubset(rows[0]):
        raise ValueError("Missing required source columns "+basename)
    return rows

def number(x):
    if x is None or x.strip().lower() in {"", "na", "nan", "null"}:
        return None
    try:
        v=float(x)
    except ValueError:
        return None
    return v if math.isfinite(v) else None

def summary(rows, key):
    vals=[number(x[key]) for x in rows]
    v=[x for x in vals if x is not None]
    return {"n_valid":len(v),"mean":round(statistics.mean(v),8) if v else None,
            "min":round(min(v),8) if v else None,"max":round(max(v),8) if v else None}

def analyze_zip(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        data={name:parse_csv(z,name) for name in REQUIRED}
    sex=data["3G.csv"]
    fitness=data["3G_ID01.csv"]
    geno=data["Genotype_3P.csv"]
    sex_ids=[(x["Population"].strip(),x["ID"].strip()) for x in sex]
    fit_ids=[(x["Population"].strip(),x["ID"].strip()) for x in fitness]
    sex_unique=set(sex_ids)
    fit_unique=set(fit_ids)
    by_inbreeding=defaultdict(list)
    for row in fitness:
        by_inbreeding[row["Inbreeding"].strip()].append(row)
    scenarios={}
    for label, rows in sorted(by_inbreeding.items()):
        scenarios[label]={
            "rows":len(rows),
            "unique_mothers":len({(x["Population"].strip(),x["ID"].strip()) for x in rows}),
            "male_fitness":summary(rows,"Male_fitness"),
            "female_fitness":summary(rows,"Female_fitness"),
            "total_fitness":summary(rows,"Total_fitness")
        }
    return {
        "schema":"SLK_MERCURIALIS_2025_ORIGINAL_FITNESS_DESCRIPTIVE_V22",
        "paper_doi":"10.1111/nph.70356",
        "source_concept_doi":DOI,
        "source_verified_archive":True,
        "raw_rows":{"sex_allocation":len(sex),"fitness_scenarios":len(fitness),"genotypes":len(geno)},
        "unique_population_mother_ids":{"sex_allocation":len(sex_unique),"fitness":len(fit_unique)},
        "sex_fitness_overlap_population_mother_ids":len(sex_unique & fit_unique),
        "duplicate_sex_population_mother_ids":len(sex_ids)-len(sex_unique),
        "genotype_parent_offspring_labels":dict(sorted(Counter(x["Parent_Offspring"].strip() for x in geno).items())),
        "sex_allocation":{
            "population_labels":dict(sorted(Counter(x["Population"].strip() for x in sex).items())),
            "selfing_rate":summary(sex,"Selfing_rate"),
            "male_flower_total":summary(sex,"Male_flower_total"),
            "female_flower_total":summary(sex,"Female_flower_total"),
            "genotyped_number":summary(sex,"Genotyped_number"),
            "selfed_seed_number":summary(sex,"Selfed_seed_number")
        },
        "fitness_scenarios":scenarios,
        "limits":[
            "Original 3G_ID01.csv includes multiple assumed inbreeding scenarios; rows are not independent plants.",
            "Do not claim any actual offspring survival or natural inbreeding depression was measured.",
            "No p-values, fitted selection gradients, cross-ploidy effect size or SLK theoretical parameters estimated.",
            "Population + mother ID overlap is only a candidate linkage; validate author code and genotype IDs before parentage re-estimation.",
            "Source CSVs are read only and not committed; archive scripts are never executed."
        ]
    }

def source_audit():
    meta=json.loads(open_url(API).decode("utf8"))
    if str(meta.get("conceptrecid"))!=CONCEPT_ID or str(meta.get("conceptdoi","")).lower()!=DOI.lower():
        raise ValueError("Zenodo concept provenance mismatch")
    files=[x for x in file_entries(meta) if x["name"]=="Geito_NewPhyto_v2.zip"]
    if len(files)!=1:
        raise ValueError("Missing exact expected published source archive")
    f=files[0]
    if not safe_source(f["url"]) or f["size"]>30_000_000:
        raise ValueError("Invalid original file location or size")
    raw=open_url(f["url"])
    digest=checked_digest(raw,f["checksum"])
    out=analyze_zip(raw)
    out["source_version_record_id"]=str(meta["id"])
    out["source_version_doi"]=str(meta.get("doi"))
    out["archive_filename"]=f["name"]
    out["archive_bytes"]=len(raw)
    out["archive_verified_digest"]=digest
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    a=p.parse_args()
    try:
        result=source_audit()
        result["state"]="verified_descriptive"
    except Exception as e:
        result={"schema":"SLK_MERCURIALIS_2025_ORIGINAL_FITNESS_DESCRIPTIVE_V22",
                "state":"unavailable","source_concept_doi":DOI,
                "error":type(e).__name__+": "+str(e)[:200],
                "new_fitness_estimates":False}
    Path(a.out).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("SLK_V22_"+result["state"].upper())

if __name__=="__main__":
    main()
