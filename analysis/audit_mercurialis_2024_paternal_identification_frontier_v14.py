#!/usr/bin/env python3
"""Algebraic partial-identification audit for the published 2024 hexaploid
Mercurialis annua *offspring phenotype* contrast.

No fresh observations or inferred genetic paternity. Source male-like
offspring phenotypes are M+Mst after germination, while sex-unknown early
deaths can be either class. Sire-model q and p are hypothetical parameters.

Under explicit assumptions:
  y_d = p_d * q_d, where:
  y_d = fraction of *germinated* offspring with Y-like phenotype,
  p_d = fraction of germinated offspring with an XY male father,
  q_d = P(Y-like phenotype | XY father, germinated offspring)
  P(Y-like phenotype | XX father) is assumed zero.
Note that "germinated" conditions on survival, so q includes distortion
from segregation, pre-germination viability, sex-expression and detection.

If q_far/q_near is NOT known, the observed contrast DOES NOT identify
p_far/p_near. The one source F x M outlier (5/49 Y-like) refutes treating
q=0.5 as universal, but cannot determine q for ring-array offspring.

Run only on frozen results already derived from publisher-MD5 verified ZIP.
"""
import argparse
import json
from pathlib import Path

DOI="10.6084/m9.figshare.26521189.v1"
MD5="365ab41f1d6192344a3b3fec87654e49"

def compute(v12,v13):
    if v12["source"]!=DOI or v13["source_doi"]!=DOI:
        raise ValueError("Source DOI not canonical")
    if v12["zip_md5"]!=MD5 or v13["publisher_archive_md5"]!=MD5:
        raise ValueError("Source MD5 not canonical")
    def cell(sex,site):
        return v12["cell_counts_and_worst_case_early_death_bounds"][sex+"_"+site]
    h0,hf=cell("H","0.0"),cell("H","1.5")
    f0,ff=cell("F","0.0"),cell("F","1.5")
    def ratio(r0,rf):
        near_lo,near_hi=r0["Y_fraction_lower"],r0["Y_fraction_upper"]
        far_lo,far_hi=rf["Y_fraction_lower"],rf["Y_fraction_upper"]
        return {"near_Ylike_range":[near_lo,near_hi],
                "far_Ylike_range":[far_lo,far_hi],
                "far_over_near_Ylike_range":[far_lo/near_hi,far_hi/near_lo],
                "far_over_near_known_only":far_lo/near_lo}
    hr=ratio(h0,hf)
    fr=ratio(f0,ff)
    # Observationally identical but causally different demonstrations:
    # Scenario A: common conditional Y-morph transmission q=.5.
    # Scenario B: common paternal XY fraction p=.8, q varies with position.
    scenarios={
      "A_constant_Y_morph_given_XY_q_half":{
         "assume_q_center":0.5,"assume_q_far":0.5,
         "implied_XY_paternity_share_center":h0["Y_fraction_lower"]/0.5,
         "implied_XY_paternity_share_far":hf["Y_fraction_lower"]/0.5,
         "logic":"Uses source-determined male-like fraction lower endpoints (all unsexed treated as non-Y). Only a hypothetical model, not genetic paternity."
      },
      "B_constant_XY_paternity_share_p_80pct":{
        "assume_XY_paternity_share_center":0.8,
        "assume_XY_paternity_share_far":0.8,
        "implied_Y_morph_probability_given_XY_center":h0["Y_fraction_lower"]/0.8,
        "implied_Y_morph_probability_given_XY_far":hf["Y_fraction_lower"]/0.8,
        "logic":"Same observable fractions with NO father-composition change; hypothetical position-dependent Y phenotype transmission or viability."
      }
    }
    if not all(0<=v<=1 for s in scenarios.values() for k,v in s.items() if k.startswith(("assume","implied")) and isinstance(v,float)):
        raise ValueError("Algebraically infeasible counterexample")
    out={
       "publisher_source_doi":DOI,"publisher_MD5":MD5,
       "input_references":["results/mercurialis_2024_xy_morph_route_bounds_v12.json",
                           "results/mercurialis_2024_maternal_sex_distance_DID_v13.json"],
       "H_mothers":hr,
       "F_mothers":fr,
       "nonnegative_sex_unknowns_always":{
          "H_center_minus_far_minimum":h0["Y_fraction_lower"]-hf["Y_fraction_upper"],
          "H_minus_F_difference_in_drops_minimum":v13["main"]["H_drop_minus_F_drop_worstcase"][0],
          "H_minus_F_difference_in_drops_maximum":v13["main"]["H_drop_minus_F_drop_worstcase"][1],
       },
       "conditional_identification_frontier":{
         "assumption":"Non-XY fathers cannot produce Y-like children; among XY-sired germinated offspring, q_d may differ by position.",
         "equation":"(p_far/p_center) = (y_far/y_center)/(q_far/q_center)",
         "threshold_q_far_over_q_center_for_FORCED_XY_siring_drop_under_any_unsexed_assignment":hr["far_over_near_Ylike_range"][1],
         "to_explain_without_any_male_sire_fraction_change_required_qfar_over_qnear_range":hr["far_over_near_Ylike_range"],
         "meaning":"If effective Y-morph transmission among XY-sired offspring at far distance is > 0.5063 of center's, p_far is necessarily lower; otherwise unchanged p is algebraically possible. q is NOT observed."
       },
       "source_controlled_cross_counterexample":{
         "paper_doi":"10.1002/ajb2.16429",
         "cross_type":"female X XY male in a separate controlled-cross experiment",
         "sex_phenotyped_offspring":49,
         "fertile_males":4,"male_sterile_males":1,
         "Y_like_offspring":5,
         "Y_like_fraction":5/49,
         "caution":"One genuine anomalous controlled family, not a generalizable q estimate for the 2024 field ring experiment; segregational versus survival mechanisms unresolved."
       },
       "hypothetical_nonidentifiability_scenarios":scenarios,
       "warnings":[
          "The 2024 article genetically inferred Y male determination, but ring offspring have no direct genetic Y typing or paternal assignment.",
          "The q=0.5 assumption is not empirically guaranteed for each family: original F x M outlier is 5 male-like among 49 progeny.",
          "This algebra conditions on the observed germinated offspring and ignores selective germination as a separate measured process.",
          "If non-XY paternity can yield Y-like phenotypes by contamination/misclassification, paternal identification weakens further.",
          "The source did not randomize CMS/restorer genotype and all aspects of pollen access; do not infer evolutionary adaptation or selfing.",
          "The H vs F difference in Y-like offspring is a robust *phenotypic contrast*, not a proven change in paternal-route composition."
       ]
    }
    if not out["nonnegative_sex_unknowns_always"]["H_minus_F_difference_in_drops_minimum"]>0:
        raise ValueError("Missingness-bound contrast missing")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--v12",required=True)
    p.add_argument("--v13",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    with open(args.v12) as f:a=json.load(f)
    with open(args.v13) as f:b=json.load(f)
    result=compute(a,b)
    with open(args.out,"w") as f:json.dump(result,f,indent=2,ensure_ascii=False)
    print("SLK_XY_MORPH_IDENTIFICATION_FRONTIER_V14_START")
    print(json.dumps(result,indent=2,ensure_ascii=False))
    print("SLK_XY_MORPH_IDENTIFICATION_FRONTIER_V14_END")

if __name__=="__main__":
    main()
