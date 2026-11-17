#!/usr/bin/env python3
"""Biology-first descriptive contrast using source-verified Mercurialis V11.

This script derives only *arithmetic summaries* from already-frozen means for
experimentally germinated offspring per original female flower. It performs
no independent offspring reanalysis, causal identification or paternity fit.
"""
import argparse
import json
from pathlib import Path

DOI = "10.6084/m9.figshare.26521189.v1"
MD5 = "365ab41f1d6192344a3b3fec87654e49"

def r(x):
    return round(float(x), 9)

def compute(d):
    if d["source"] != DOI or d["zip_md5"] != MD5:
        raise ValueError("Not the source-verified 2024 parental assay")
    if d["source_n_mothers"] != 72 or d["n_mothers_with_phenotyped_progeny"] != 71:
        raise ValueError("2024 source sample definition changed")
    if len(d["sample_exclusions"]) != 3:
        raise ValueError("Crop/sowing inconsistency exclusion has changed")
    required = ["F_0.0", "F_1.5", "H_0.0", "H_1.5"]
    for c in required:
        m = d["cell_summary"][c]["means"]
        components = ("per_flower_female","per_flower_hermaphrodite",
                      "per_flower_male","per_flower_male_sterile",
                      "per_flower_unsexed_died_early")
        if abs(sum(m[k] for k in components)-m["per_flower_total"]) > 1e-10:
            raise ValueError("Morph totals no longer reconcile in "+c)
    def means(c):
        return d["cell_summary"][c]["means"]
    f0,ff,h0,hf = [means(k) for k in required]
    def cell(c):
        m=means(c)
        return {
            "n_crop_consistent_mothers": d["cell_summary"][c]["n_assay_crop_consistent"],
            "all_germinants": r(m["per_flower_total"]),
            "H_like_germinants": r(m["per_flower_hermaphrodite"]),
            "M_like_germinants": r(m["per_flower_male"]+m["per_flower_male_sterile"])
        }
    total=lambda m:m["per_flower_total"]
    m_like=lambda m:m["per_flower_male"]+m["per_flower_male_sterile"]
    analysis=d["analyses"]["per_flower_total"]
    ci=analysis["interaction_bootstrap"]["sex_by_distance_CI"]
    if analysis["interaction"]["n_mothers"] != 69:
        raise ValueError("Model sample definition changed")
    if not (ci[0] < 0 < ci[1]):
        raise ValueError("Previously unresolved interaction is no longer unresolved")
    return {
        "schema": "SLK_MERCURIALIS_2024_MATERNAL_BUFFER_DESCRIPTIVE_V15",
        "input": "results/mercurialis_2024_morph_specific_germinants_v11.json",
        "source_doi": d["source"], "publisher_zip_md5": d["zip_md5"],
        "data_scope": "Already-verified published 2024 hexaploid field ring cohort; no new mother-level model, paternity genotypes, survival, or raw ZIP retrieval.",
        "denominator": "Estimated laboratory-germinated offspring per source female flower; mother-level seed-assay subsample assumed representative of original crop.",
        "n_original_F_H_mothers": d["source_n_mothers"],
        "n_with_sexed_progeny": d["n_mothers_with_phenotyped_progeny"],
        "n_excluded_crop_inconsistent": len(d["sample_exclusions"]),
        "n_model_mothers": analysis["interaction"]["n_mothers"],
        "n_independent_field_blocks": 3,
        "cells": {"F_center":cell("F_0.0"),"F_far":cell("F_1.5"),
                  "H_center":cell("H_0.0"),"H_far":cell("H_1.5")},
        "descriptive_contrasts": {
            "H_minus_F_center":r(total(h0)-total(f0)),
            "H_minus_F_far":r(total(hf)-total(ff)),
            "H_minus_F_change_in_center_far_difference":r((total(hf)-total(h0))-(total(ff)-total(f0))),
            "H_far_over_F_far":r(total(hf)/total(ff)),
            "H_center_to_far_percent_change":r(100*(total(hf)/total(h0)-1)),
            "F_center_to_far_percent_change":r(100*(total(ff)/total(f0)-1)),
            "H_like_germinants_H_mother_far_minus_center":r(hf["per_flower_hermaphrodite"]-h0["per_flower_hermaphrodite"]),
            "M_like_germinants_H_mother_far_minus_center":r(m_like(hf)-m_like(h0))
        },
        "source_existing_total_interaction": {
            "F_minus_H_distance_slope":r(analysis["interaction"]["sex_by_distance"]),
            "conditional_bootstrap_95pct_interval":[r(ci[0]),r(ci[1])],
            "interval_crosses_zero":True,
            "resampling_replicates":analysis["interaction_bootstrap"]["successful_resamples"],
            "inference":"Source V11 exploratory 3-block fixed-block mother-bootstrap; 95% interval does not establish a generalized sex-by-distance advantage."
        },
        "biological_claim_boundary":[
            "Means are already in V11; the newly juxtaposed H-versus-F far contrast is an arithmetic synthesis, not a new independent empirical experiment.",
            "Do not call this a fitness benefit, reproductive assurance causally established, genotype-specific adaptability, or an increase in lifetime descendants.",
            "H and F can differ in CMS/restorer nuclear and cytoplasmic background; pollen sources include nearby H plants at every ring.",
            "Remote H sample excludes one crop-inconsistent mother; totals and source Y-like offspring fraction analyses have different denominators.",
            "The sex-by-distance source-bootstrap interval includes zero. Male-like offspring phenotype does not genetically identify fathers."
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    d=json.loads(Path(args.source).read_text(encoding="utf-8"))
    result=compute(d)
    Path(args.out).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("SLK_V15_REAL_MATERNAL_DESC_SUCCESS")

if __name__ == "__main__":
    main()
