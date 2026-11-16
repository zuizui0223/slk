#!/usr/bin/env python3
"""Audit offspring Y-morph bounds, not paternal assignment, in 2024 M. annua.

Parents are F/H phenotypes in the genuine checksum-verified field archive.
Phenotyped "M" and "Mst" are counted together (source's Y-carrier classes);
all "NA" early-death offspring are allowed to be any class. Ratios are based
on germinated progeny, not viable mature offspring or DNA paternity. The source
paper's XY model is a conditional interpretation rather than a genotyped fact.
"""
import argparse
import json
from audit_mercurialis_2024_next_generation_morph_stage_v10 import load

DOI = "10.6084/m9.figshare.26521189.v1"
MD5 = "365ab41f1d6192344a3b3fec87654e49"

def usable(rs):
    out = []
    omitted = []
    for r in rs:
        if r["gap"] == 0:
            out.append(r)
        elif r["mother_seed_total"] == 0 and r["sown"] in (None,0) and r["germinated"] is None:
            omitted.append({"id":r["id"],"reason":"No seed crop or progeny assay"})
        else:
            raise ValueError("Unreconciled sex phenotype and germination counts: "+r["id"])
    if len(out)!=71 or len(omitted)!=1:
        raise ValueError("Published expected 71 mothers with progeny, 1 zero-seed mother")
    return out, omitted

def aggregate(rs):
    n=sum(r["germinated"] for r in rs)
    males=sum(r["Prog_M"]+r["Prog_Mst"] for r in rs)
    unknown=sum(r["Prog_NA"] for r in rs)
    typed=n-unknown
    female=sum(r["Prog_F"] for r in rs)
    herm=sum(r["Prog_H"] for r in rs)
    if n<1 or males+female+herm!=typed:raise ValueError("Invalid phenotype accounting")
    return {
      "mothers":len(rs),"germinated":n,
      "known_Y_morph":males,"unsexed_died_early":unknown,
      "sexed":typed,"known_F":female,"known_H":herm,
      "Y_fraction_lower":males/n,
      "Y_fraction_upper":(males+unknown)/n,
      "H_fraction_among_sexed":herm/typed,
      "conditional_XY_male_pollen_share_proxy_lower":min(1,2*males/n),
      "conditional_XY_male_pollen_share_proxy_upper":min(1,2*(males+unknown)/n)
    }

def compare(h0,hfar):
    low=aggregate(h0); high=aggregate(hfar)
    return {
      "center":low,"far":high,
      "strict_minimum_center_minus_far_Y_fraction":low["Y_fraction_lower"]-high["Y_fraction_upper"],
      "known_Y_fraction_center_minus_far":low["known_Y_morph"]/low["germinated"]-high["known_Y_morph"]/high["germinated"]
    }

def run(zip_path):
    rs,omitted=usable(load(zip_path))
    by_cell={}
    for sex in ("H","F"):
        for d in (0.0,0.5,1.5):
            cohort=[r for r in rs if r["Sex"]==sex and r["dist"]==d]
            by_cell[f"{sex}_{d}"]=aggregate(cohort)
    center=[r for r in rs if r["Sex"]=="H" and r["dist"]==0]
    far=[r for r in rs if r["Sex"]=="H" and r["dist"]==1.5]
    full=compare(center,far)
    leave_one_mother=[]
    for r in center+far:
        c=[x for x in center if x["id"]!=r["id"]]
        f=[x for x in far if x["id"]!=r["id"]]
        temp=compare(c,f)
        leave_one_mother.append({
            "removed_mother_id":r["id"],"position":"center" if r in center else "far",
            "strict_minimum_center_minus_far_Y_fraction":temp["strict_minimum_center_minus_far_Y_fraction"],
            "known_Y_fraction_center_minus_far":temp["known_Y_fraction_center_minus_far"]
        })
    block_pair={}
    for b in ("1","2","3"):
        c=[r for r in center if r["block"]==b]
        f=[r for r in far if r["block"]==b]
        block_pair[b]=compare(c,f)
    leave_one_block={}
    for b in ("1","2","3"):
        c=[r for r in center if r["block"]!=b]
        f=[r for r in far if r["block"]!=b]
        leave_one_block[b]=compare(c,f)
    crop_inconsistent=[
      {"id":r["id"],"mother_sex":r["Sex"],"distance":r["dist"],
       "reported_mature_seeds":r["mother_seed_total"],"reported_sown":r["sown"]}
      for r in rs if r["sown"]>r["mother_seed_total"]]
    without_crop_inconsistent=[r for r in rs if r["sown"]<=r["mother_seed_total"]]
    center_clean=[r for r in without_crop_inconsistent if r["Sex"]=="H" and r["dist"]==0]
    far_clean=[r for r in without_crop_inconsistent if r["Sex"]=="H" and r["dist"]==1.5]
    influence={
      "count":len(leave_one_mother),
      "min_strict_margin":min(t["strict_minimum_center_minus_far_Y_fraction"] for t in leave_one_mother),
      "max_strict_margin":max(t["strict_minimum_center_minus_far_Y_fraction"] for t in leave_one_mother),
      "all_leave_one_mother_out_strict_margins_positive":all(t["strict_minimum_center_minus_far_Y_fraction"]>0 for t in leave_one_mother),
      "lowest_margin_removed_parent":min(leave_one_mother,key=lambda t:t["strict_minimum_center_minus_far_Y_fraction"])["removed_mother_id"],
    }
    result={
      "source":DOI,"zip_md5":MD5,
      "n_published_field_plants":84,"n_F_H_with_progeny":len(rs),
      "excluded_zero_seed_mother":omitted,
      "cell_counts_and_worst_case_early_death_bounds":by_cell,
      "H_center_vs_far":full,
      "H_center_vs_far_by_block":block_pair,
      "H_center_vs_far_leave_one_block_out":leave_one_block,
      "H_center_vs_far_leave_one_mother_out_influence":influence,
      "sown_greater_than_reported_crop_rows":crop_inconsistent,
      "H_center_vs_far_excluding_seed_crop_mismatch":compare(center_clean,far_clean),
      "interpretation_conditions":[
        "The intervals on Y-morph offspring fractions are worst-case allocations of all unsexed germinated progeny, not sampling confidence intervals.",
        "XY-origin pollen fraction = 2 x Y morph fraction is a conditional Mendelian proxy ONLY if every sampled male-sired progeny is 1:1 Y:non-Y, only XY pollen sires can produce Y carriers, and sex-specific survival/sex recognition are equal.",
        "M and male-sterile Mst are grouped as presumed Y phenotypes by the 2024 paper's sex-determination model, not Y-genotyped seedlings.",
        "No single individual mother can be interpreted as an independently randomized genotype; block-level replicates are only three.",
        "The distance to the central male cluster also alters plant spacing; H on all rings provide pollen, and parental genetic backgrounds are unknown.",
        "Detected offspring phenotype composition is not adult sex-ratio evolution, paternal genotype assignment, or proof of selfing.",
        "Source crop/sown anomalies are never silently used to extrapolate absolute morph offspring per female flower."
      ]
    }
    if full["strict_minimum_center_minus_far_Y_fraction"] <= 0:
        raise ValueError("Core worst-case bound no longer nonoverlapping")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    d=run(a.zip)
    with open(a.out,"w") as f:json.dump(d,f,ensure_ascii=False,indent=2)
    print("SLK_2024_XY_MORPH_BOUNDS_V12_START")
    print(json.dumps(d,ensure_ascii=False,indent=2))
    print("SLK_2024_XY_MORPH_BOUNDS_V12_END")
