#!/usr/bin/env python3
"""Source-verifiable descriptive stage accounting, Nguyen et al. (2024).
This intentionally does NOT fit the paper's mixed models, estimate paternal
success, offspring lifetime survival, or make a cross-ploidy time series.
Only uses the fixed publisher ZIP and its own data dictionary.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import random
import zipfile

SOURCE_DOI = "10.6084/m9.figshare.26521189.v1"
ZIP_MD5 = "365ab41f1d6192344a3b3fec87654e49"
CSV_PATH = "Data_field_experiment/Pollination and distance/Data_pollen_limitation_and_distance.csv"
NA = {"", "NA", "NaN", "nan", "None"}

def number(s):
    if s is None or str(s).strip() in NA: return None
    return float(s)

def mean(x):
    x = [v for v in x if v is not None and math.isfinite(v)]
    return sum(x) / len(x) if x else None

def solve(a,b):
    # Gaussian elimination with partial pivoting; small fixed X'X system.
    n = len(b)
    c = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = max(range(j,n),key=lambda i:abs(c[i][j]))
        if abs(c[pivot][j])<1e-12:return None
        c[j],c[pivot]=c[pivot],c[j]
        fac=c[j][j]
        for k in range(j,n+1):c[j][k]/=fac
        for i in range(n):
            if i==j:continue
            fac=c[i][j]
            for k in range(j,n+1):c[i][k]-=fac*c[j][k]
    return [c[i][-1] for i in range(n)]

def matrix_row(r):
    return [1., float(r["Sex"]=="F"),r["dist"],float(r["block"]=="2"),float(r["block"]=="3")]

def fit(rows,metric):
    valid=[r for r in rows if r.get(metric) is not None and math.isfinite(r[metric])]
    if len(valid)<8:return None
    xx=[[0.]*5 for _ in range(5)]
    xy=[0.]*5
    for r in valid:
        x=matrix_row(r)
        y=r[metric]
        for i in range(5):
            xy[i]+=x[i]*y
            for j in range(5):xx[i][j]+=x[i]*x[j]
    beta=solve(xx,xy)
    if beta is None:return None
    ys=[r[metric] for r in valid]
    avg=mean(ys)
    sse=sum((r[metric]-sum(a*b for a,b in zip(matrix_row(r),beta)))**2 for r in valid)
    sst=sum((y-avg)**2 for y in ys)
    return {"n":len(valid),"F_minus_H":beta[1],"distance_per_m":beta[2],"r2":(1-sse/sst if sst>0 else None)}

def bootstrap(rows,metric,n_reps=1200,seed=20261116):
    # Within-block × sex × distance resampling preserves observed sampling design.
    strata=collections.defaultdict(list)
    for r in rows:strata[(r["block"],r["Sex"],r["dist"])].append(r)
    pools=list(strata.values())
    rng=random.Random(seed)
    effects=[]
    for _ in range(n_reps):
        sample=[rng.choice(pool) for pool in pools for j in range(len(pool))]
        est=fit(sample,metric)
        if est:effects.append((est["F_minus_H"],est["distance_per_m"]))
    if len(effects)<n_reps*.95:return {"successful_bootstraps":len(effects),"status":"insufficient"}
    def ci(k):
        x=sorted(y[k] for y in effects)
        return [x[int(.025*(len(x)-1))],x[int(.975*(len(x)-1))]]
    return {"successful_bootstraps":len(effects),"F_minus_H_95pct":ci(0),"distance_per_m_95pct":ci(1),
            "method":"plant-level stratified percentile bootstrap, fixed observed block/sex/distance cells; not block-level inference"}

def prepare(zip_path):
    with open(zip_path,"rb") as f:
        content=f.read()
    actual=hashlib.md5(content).hexdigest()
    if actual!=ZIP_MD5:raise ValueError("Published archive MD5 mismatch: "+actual)
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        raw=z.read(CSV_PATH).decode("utf-8-sig")
    all_rows=list(csv.DictReader(io.StringIO(raw)))
    if len(all_rows)!=84:raise ValueError("Unexpected number of field experiment rows")
    output=[]
    for r in all_rows:
        if r["Sex"] not in ("F","H"):continue
        flowers=number(r["Female_flowers_tot"])
        nonfruit=number(r["Female_flowers_unfert"])
        seeds=number(r["nombre graines"])
        seedmass=number(r["Seed_masse"])
        sown=number(r["Seed_sown"])
        germinated=number(r["Prog_tot"])
        reported_germ=number(r["Germ_rate"])
        if flowers is None or flowers<=0 or nonfruit is None or nonfruit<0 or nonfruit>flowers:raise ValueError("Invalid female-flower denominator")
        if seeds is None or seeds<0:raise ValueError("Missing seed-count response")
        calculated_germ=germinated/sown if sown is not None and sown>0 and germinated is not None else None
        if calculated_germ is not None and reported_germ is not None and abs(calculated_germ-reported_germ)>1e-10:
            raise ValueError("Germ_rate not germinated / seeds sown")
        if calculated_germ is not None and not 0<=calculated_germ<=1:raise ValueError("Invalid germination rate")
        fruits=flowers-nonfruit
        # If zero mature seeds, germinants are structurally zero even without a germination assay.
        expected=(seeds/flowers*calculated_germ if calculated_germ is not None else (0 if seeds==0 else None))
        output.append({
            "id":r["ID"],"Sex":r["Sex"],"block":r["Bloc"],"dist":number(r["Dist"]),
            "observation":r["Observation"],"flowers":flowers,"nonfruit":nonfruit,
            "seeds":seeds,"seedmass":seedmass,"sown":sown,"germinated":germinated,
            "unfruiting_fraction":nonfruit/flowers,"fruiting_fraction":fruits/flowers,
            "seeds_per_female_flower":seeds/flowers,
            "seeds_per_fruiting_flower":(seeds/fruits if fruits>0 else None),
            "germination_rate":calculated_germ,
            "expected_germinants_per_female_flower":expected,
            "seed_mass_per_female_flower":(seedmass/flowers if seedmass is not None else None),
        })
    if len(output)!=72:raise ValueError("Expect 72 F/H plants, plus 12 M")
    if len({r["id"] for r in output})!=72:raise ValueError("Duplicated plant IDs")
    return output

def group(rows):
    metrics=("unfruiting_fraction","seeds_per_female_flower","seeds_per_fruiting_flower",
             "germination_rate","expected_germinants_per_female_flower")
    d={"n_plants":len(rows)}
    for metric in metrics:
        v=[r[metric] for r in rows if r[metric] is not None]
        d[metric]={"n":len(v),"mean":mean(v)}
    return d

def run(zip_path):
    rows=prepare(zip_path)
    bysex={sex:group([r for r in rows if r["Sex"]==sex]) for sex in ("F","H")}
    bycell={}
    for sex in ("F","H"):
        for dist in (0.,.5,1.5):
            bycell[sex+"_"+str(dist)]=group([r for r in rows if r["Sex"]==sex and r["dist"]==dist])
    adjusted={}
    for k in ("unfruiting_fraction","seeds_per_female_flower","seeds_per_fruiting_flower","germination_rate","expected_germinants_per_female_flower"):
        adjusted[k]={"ols":fit(rows,k),"bootstrap":bootstrap(rows,k)}
    flagged=[r for r in rows if r["observation"].strip()]
    clean=[r for r in rows if not r["observation"].strip()]
    sensitivity={k:fit(clean,k) for k in ("unfruiting_fraction","seeds_per_female_flower","germination_rate","expected_germinants_per_female_flower")}
    return {"source_doi":SOURCE_DOI,"source_zip_md5":ZIP_MD5,"data_csv":CSV_PATH,
        "analysis":"exploratory within-original-experiment plant-stage accounting; not fitted paper GLMM, no causal mediation",
        "denominators":{"N_all":84,"N_female_or_hermaphrodite":len(rows),
          "N_with_measured_germination":sum(r["germination_rate"] is not None for r in rows),
          "N_expected_germinants_defined":sum(r["expected_germinants_per_female_flower"] is not None for r in rows),
          "N_flagged_observation":len(flagged),
          "N_with_zero_seed":sum(r["seeds"]==0 for r in rows)},
        "by_sex":bysex,"by_sex_distance":bycell,
        "adjusted_effects":adjusted,
        "sensitivity_excluding_observation_flags":{"n":len(clean),"estimates":sensitivity},
        "cautions":["Sex-by-distance nonrandom allocation cannot be assumed to identify causal effect without original randomization details.",
            "Unfruiting flowers are not a direct measurement of pollen delivery/fertilization.",
            "Seeds per fruiting flower is a retrospective ratio and need not be statistically independent from unfruiting fraction.",
            "Expected germinants = (mature seeds/female flower) × (sown germinants/sown seeds). No field offspring survival, seed paternity, or lifetime fitness.",
            "Bootstrap conditions on only 3 fixed experimental blocks and small cells; exploratory confidence intervals are not population-wide block inference.",
            "F/H hexaploid 2024 raw data and diploid 2025 G8 are independent genetic systems, not longitudinal evolution."]}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    result=run(args.zip)
    with open(args.out,"w") as f:json.dump(result,f,indent=2,ensure_ascii=False)
    print("SLK_REPRODUCTIVE_STAGE_REANALYSIS_START")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("SLK_REPRODUCTIVE_STAGE_REANALYSIS_END")
