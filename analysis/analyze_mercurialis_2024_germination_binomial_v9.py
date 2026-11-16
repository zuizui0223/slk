#!/usr/bin/env python3
"""Source-verified grouped germination audit on the 2024 Mercurialis ring experiment.

Responses are germinated offspring out of seeds sown per maternal plant. Do not
mistake seeds for independent spatial replicates. Intervals resample mothers
within observed (block, morph, distance) cells, not experimental blocks.
"""
import argparse, collections, json, math, random
from reanalyze_mercurialis_2024_parent_to_germination_v1 import prepare, solve, mean

def expit(t):
    if t >= 0:
        return 1.0/(1.0+math.exp(-t))
    y=math.exp(t)
    return y/(1.0+y)

def fit(rs, interaction=False):
    rs=[r for r in rs if r["sown"] is not None and r["sown"]>0 and r["germinated"] is not None]
    if len(rs)<15:return None
    blocks=sorted(set(r["block"] for r in rs))
    def X(r):
        x=[1.0,float(r["Sex"]=="F"),float(r["dist"])]
        x.extend(float(r["block"]==b) for b in blocks[1:])
        if interaction:x.append(float(r["Sex"]=="F")*float(r["dist"]))
        return x
    xx=[X(r) for r in rs]; d=len(xx[0])
    n=[r["sown"] for r in rs]; y=[r["germinated"] for r in rs]
    p=sum(y)/sum(n)
    if p<=0 or p>=1:return None
    beta=[math.log(p/(1-p))]+[0.]*(d-1)
    def ll(b):
        z=0.
        for x,ni,yi in zip(xx,n,y):
            pi=min(1-1e-12,max(1e-12,expit(sum(a*v for a,v in zip(x,b)))))
            z+=yi*math.log(pi)+(ni-yi)*math.log1p(-pi)
        return z
    for _ in range(80):
        h=[[0.]*d for _ in range(d)]; g=[0.]*d
        for x,ni,yi in zip(xx,n,y):
            pi=expit(sum(a*v for a,v in zip(x,beta)))
            weight=max(1e-8,ni*pi*(1-pi))
            for j in range(d):
                g[j]+=x[j]*(yi-ni*pi)
                for k in range(d):h[j][k]+=weight*x[j]*x[k]
        delta=solve(h,g)
        if delta is None:return None
        old=ll(beta); scale=1.
        while scale>1/8192:
            proposal=[b+scale*t for b,t in zip(beta,delta)]
            if ll(proposal)>=old-1e-9:
                beta=proposal;break
            scale/=2
        if max(abs(v)*scale for v in delta)<1e-8:break
    pearson=0.
    for x,ni,yi in zip(xx,n,y):
        pi=expit(sum(a*v for a,v in zip(x,beta)))
        pearson+=(yi-ni*pi)**2/max(1e-8,ni*pi*(1-pi))
    return {"n_mothers":len(rs),"sown":int(sum(n)),"germinated":int(sum(y)),
       "pooled_germination":sum(y)/sum(n),"distance_log_odds_per_m":beta[2],
       "distance_odds_ratio_per_m":math.exp(beta[2]),
       "female_log_odds":beta[1],
       "sex_by_distance_log_odds":beta[-1] if interaction else None,
       "pearson_dispersion_plant_clustered":pearson/max(1,len(rs)-d),
       "method":"grouped binomial point estimate, mother-level bootstrap; fixed block factors"}

def boot(rs,interaction=False,seed=20261117,reps=1200):
    pools=collections.defaultdict(list)
    for r in rs:pools[(r["block"],r["Sex"],r["dist"])].append(r)
    rng=random.Random(seed); vals=[]
    for _ in range(reps):
        sample=[rng.choice(pool) for pool in pools.values() for __ in pool]
        res=fit(sample,interaction)
        if res is not None:vals.append(res)
    def interval(key):
        v=sorted(x[key] for x in vals if x[key] is not None)
        if not v:return None
        return [v[int(.025*(len(v)-1))],v[int(.975*(len(v)-1))]]
    ci=interval("distance_log_odds_per_m")
    return {"successful_mother_resamples":len(vals),"distance_log_odds_95pct":ci,
      "distance_OR_95pct":[math.exp(v) for v in ci] if ci else None,
      "female_log_odds_95pct":interval("female_log_odds"),
      "sex_by_distance_log_odds_95pct":interval("sex_by_distance_log_odds"),
      "caution":"bootstrap conditional on 3 spatial blocks and recorded cell sizes; not a CI for regions/populations"}

def run(path):
    rs=prepare(path)
    cells={}
    for sex in ("F","H"):
        for dist in (0.,.5,1.5):
            selected=[r for r in rs if r["Sex"]==sex and r["dist"]==dist]
            valid=[r for r in selected if r["sown"] is not None and r["sown"]>0 and r["germinated"] is not None]
            cells[f"{sex}_{dist}"]={"n_mothers":len(selected),"n_assayed":len(valid),
                 "sown":int(sum(r["sown"] for r in valid)),
                 "germinated":int(sum(r["germinated"] for r in valid)),
                 "pooled_germination":(sum(r["germinated"] for r in valid)/sum(r["sown"] for r in valid) if valid else None),
                 "mother_mean_germination":mean([r["germination_rate"] for r in valid]),
                 "mean_assayed_seeds":mean([r["sown"] for r in valid]),
                 "mean_fraction_crop_assayed":mean([r["sown"]/r["seeds"] for r in valid if r["seeds"]>0])}
    full=fit(rs)
    xi=fit(rs,True)
    if full is None or xi is None:raise ValueError("Full-rank models failed")
    return {"source":"10.6084/m9.figshare.26521189.v1","source_zip_md5":"365ab41f1d6192344a3b3fec87654e49",
       "paper":"Nguyen Martignier Pannell 2024 10.1002/ajb2.16429",
       "rows_F_H":72,"n_with_germination":71,"sex_ring":cells,
       "main":full,"main_bootstrap":boot(rs),
       "interaction":xi,"interaction_bootstrap":boot(rs,True,seed=20261118),
       "outer_rings_only":fit([r for r in rs if r["dist"]>0]),
       "leave_one_block_out":{b:fit([r for r in rs if r["block"]!=b]) for b in ("1","2","3")},
       "exclude_flagged":fit([r for r in rs if not r["observation"]]),
       "cautions":[
       "Sex×distance interactions are observational conditional relationships, not a randomized genetic-system contrast.",
       "Three experimental blocks provide no generalizable spatial replication.",
       "Sown seeds are nested within mothers; binomial nominal SE would be overconfident.",
       "Distance from central males is not measured pollen load or actual nearest donor.",
       "The ring design also changes spacing, maternal vigor, and potentially microenvironment.",
       "Seed sample selection and nonuniform number sown can bias extrapolation to all mature seeds.",
       "2016 Labouche Richards Pannell already studied distance-to-pollen and offspring quality in distinct dioecious populations; not a first discovery of the mechanism.",
       "No paternity, direct causal mediation, field recruitment, or lifetime invasion was measured."]
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    out=run(a.zip)
    with open(a.out,"w") as f:json.dump(out,f,indent=2,ensure_ascii=False)
    print("SLK_MERCURIALIS_GERMINATION_BINOMIAL_V9_START")
    print(json.dumps(out,indent=2,ensure_ascii=False))
    print("SLK_MERCURIALIS_GERMINATION_BINOMIAL_V9_END")
