#!/usr/bin/env python3
"""Published *Mercurialis* Table 2: female seed-output advantage vs morph frequency.

2012 Perry, Pannell & Dorken PLoS ONE DOI 10.1371/journal.pone.0035597:
reproduce the 20-plot table of relative seed production, and independently
classify whether the female phenotype was more frequent in the next
generation. Printed two-decimal numbers imply +/- 0.005 bounds. No raw
parentage, allelic frequencies, survival or published-model inference.
The Heredity 2025 CMS invasion/maintenance model is separately registered
as PRIOR ART, NOT fitted from the 2012 plots.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/evidence/mercurialis_2008_2012_2024_density_partner_composition_original_v2.json"
PRIOR=ROOT/"data/evidence/mercurialis_2012_seed_advantage_and_CMS_prior_art_v4.json"


def classify(seed_ratio:float, daughter_fraction:float, parent_fraction:float):
    """Conservative signs under +/- 0.005 source rounding for both ratios."""
    values=(seed_ratio,daughter_fraction,parent_fraction)
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or
           not math.isfinite(v) for v in values):
        raise ValueError("BAD_SOURCE_NUMBER")
    if not (0<seed_ratio and 0<=daughter_fraction<=1 and
            0<parent_fraction<1):
        raise ValueError("SOURCE_FREQUENCIES_OUT_OF_RANGE")
    # original prints to 2 decimals; borderline ties remain ambiguous.
    if seed_ratio + .005 < 1:
        advantage="female_seed_allocation_higher"
    elif seed_ratio - .005 > 1:
        advantage="hermaphrodite_seed_allocation_higher"
    else:
        advantage="undetermined_under_source_rounding"

    if daughter_fraction + .005 < parent_fraction:
        morph="female_morph_decrease"
    elif daughter_fraction - .005 > parent_fraction:
        morph="female_morph_increase"
    else:
        morph="undetermined_under_source_rounding"
    return advantage,morph


def compute(original,prior):
    pub=original["study_2012"]
    if pub["doi"]!="10.1371/journal.pone.0035597" or (
        pub["type"]!="TRIOECIOUS_ALL_TREATMENTS_CONTAIN_FEMALES; FACTOR IS MALE_PRESENCE_NOT_FEMALE_PRESENCE"
        or pub["plot_count"]!=20 or len(pub["original_table2"])!=20):
        raise ValueError("INVALID_ORIGINAL_2012_SOURCE_SCOPE")
    if prior["observed_2012_source"]["doi"]!=pub["doi"]:
        raise ValueError("MISMATCHED_PRIMARY_STUDY")
    if prior["method_correction_2026_11_15"]["corrected_endpoint"]!=\
            "SEED_BIOMASS_PER_ABOVEGROUND_BIOMASS_ALLOCATION_FRACTION":
        raise ValueError("ABSOLUTE_FECUNDITY_NOT_MEASURED")
    t=prior["model_2025_prior_art"]
    if (t["doi"]!="10.1038/s41437-024-00729-7" or
        not t["author_simulation_not_natural_invasion"] or
        t["simulated_initial_rare_CMS_frequency"]!=1e-6):
        raise ValueError("UNSUPPORTED_NOVEL_INVASION_CLAIM")
    snail=prior["cross_taxon_direct_selection_prior_art"]
    if (snail["doi"]!="10.1086/735820" or
        snail["study_type"].find("11-generation")<0):
        raise ValueError("INCORRECT_CROSS_TAXON_CMS_SOURCE")

    rows=pub["original_table2"]
    if len({r["id"] for r in rows})!=20:
        raise ValueError("DUPLICATED_EXPERIMENTAL_PLOT")
    expected_groups={d+"_"+m:5 for d in ("low","high")
                      for m in ("absent","present")}
    found_groups={s:0 for s in expected_groups}
    table=[]
    # Same measured seed ratio, different idealized nuclear/cytoplasmic
    # invasion requirements in the PRIOR Heredity paper. Here we record
    # purely descriptive bins, not an empirical invasion test.
    ratio_bins={
      "female_allocation_not_higher":0,
      "female_allocation_ratio_strictly_between_1_and_2":0,
      "female_allocation_ratio_strictly_above_2":0,
      "uncertainty_from_oh_rounding_crossing_bin_boundary":0
    }
    intersection={
      "female_seed_allocation_higher_and_female_morph_decrease":0,
      "female_seed_allocation_higher_and_female_morph_increase":0,
      "female_seed_allocation_higher_and_morph_ambiguous":0,
      "hermaphrodite_seed_allocation_higher_and_female_morph_decrease":0,
      "hermaphrodite_seed_allocation_higher_and_female_morph_increase":0,
      "hermaphrodite_seed_allocation_higher_and_morph_ambiguous":0,
      "seed_allocation_ambiguous":0
    }
    for r in sorted(rows,key=lambda x:x["id"]):
        key=r["density"]+"_"+r["males"]
        if key not in found_groups:
            raise ValueError("UNKNOWN_PLOT_SEX_SYSTEM_OR_DENSITY")
        found_groups[key]+=1
        if (type(r["n"]) is not int or r["n"]<200 or
            not 0<r["oh"]<10 or not 0<=r["female"]<=1):
            raise ValueError("INVALID_PUBLISHED_PLOT")
        parent=pub["parental_sex_counts"][r["density"]][r["males"]]
        if any(type(x)!=int or x<0 for x in parent.values()) or (
            sum(parent.values())!=pub["parent_plants_per_plot"][r["density"]]
            or parent["female"]<=0):
            raise ValueError("ORIGINAL_PARENT_COMPOSITION_CHANGED")
        parent_f=parent["female"]/sum(parent.values())
        seed,morph=classify(r["oh"],r["female"],parent_f)
        if r["oh"]-.005>1:
            bin_name="female_allocation_not_higher"
        elif r["oh"]+.005<.5:
            bin_name="female_allocation_ratio_strictly_above_2"
        elif r["oh"]-.005>.5 and r["oh"]+.005<1:
            bin_name="female_allocation_ratio_strictly_between_1_and_2"
        else:
            bin_name="uncertainty_from_oh_rounding_crossing_bin_boundary"
        ratio_bins[bin_name]+=1
        if seed=="female_seed_allocation_higher":
            if morph=="female_morph_decrease":
                intersection["female_seed_allocation_higher_and_female_morph_decrease"]+=1
            elif morph=="female_morph_increase":
                intersection["female_seed_allocation_higher_and_female_morph_increase"]+=1
            else:
                intersection["female_seed_allocation_higher_and_morph_ambiguous"]+=1
        elif seed=="hermaphrodite_seed_allocation_higher":
            if morph=="female_morph_decrease":
                intersection["hermaphrodite_seed_allocation_higher_and_female_morph_decrease"]+=1
            elif morph=="female_morph_increase":
                intersection["hermaphrodite_seed_allocation_higher_and_female_morph_increase"]+=1
            else:
                intersection["hermaphrodite_seed_allocation_higher_and_morph_ambiguous"]+=1
        else:
            intersection["seed_allocation_ambiguous"]+=1
        table.append({
          "original_plot":r["id"],"treatment_cell":key,
          "source_oh_hermaphrodite_over_female_seed_allocation_fraction":r["oh"],
          "female_over_hermaphrodite_seed_allocation_share_ratio_from_printed_oh":round(1/r["oh"],8),
          "relative_seed_allocation_advantage_under_rounding":seed,
          "relative_allocation_bin_not_model_viable_seed_g":bin_name,
          "parental_female_morph_fraction":round(parent_f,8),
          "source_progeny_female_morph_fraction":r["female"],
          "female_morph_frequency_change_from_parent":round(r["female"]-parent_f,8),
          "female_morph_change_under_rounding":morph,
          "progeny_sample_n":r["n"],
          "inheritance_cytotype_or_parentage_observed":False
        })
    if found_groups!=expected_groups:
        raise ValueError("UNBALANCED_ORIGINAL_PLOT_CELLS")
    if ratio_bins!={
        "female_allocation_not_higher":1,
        "female_allocation_ratio_strictly_between_1_and_2":15,
        "female_allocation_ratio_strictly_above_2":4,
        "uncertainty_from_oh_rounding_crossing_bin_boundary":0
    }:
        raise ValueError("SOURCE_RATIO_THRESHOLDS_NOT_REPRODUCED")
    if (prior["model_2025_prior_art"]["idealized_original_intro_thresholds"]
        ["actual_2012_plot_invasion_inference"]
        !="BLOCKED_BY_ALLOCATION_FRACTION_NOT_VIABLE_SEED_NUMBER_SELFING_EXISTING_MALES_AND_CMS_UNTYPED"):
        raise ValueError("FALSE_INVASION_THRESHOLD_APPLICATION")
    if sum(r["progeny_sample_n"] for r in table)!=6076:
        raise ValueError("SOURCE_2012_PROGENY_TOTAL_CHANGED")
    if intersection!={
      "female_seed_allocation_higher_and_female_morph_decrease":17,
      "female_seed_allocation_higher_and_female_morph_increase":1,
      "female_seed_allocation_higher_and_morph_ambiguous":1,
      "hermaphrodite_seed_allocation_higher_and_female_morph_decrease":0,
      "hermaphrodite_seed_allocation_higher_and_female_morph_increase":1,
      "hermaphrodite_seed_allocation_higher_and_morph_ambiguous":0,
      "seed_allocation_ambiguous":0
    }:
        raise ValueError("SOURCE_CROSS_TAB_PLOT_BIOLOGY_CHANGED")
    limit=prior["claim_limits"]
    if not any("2025 Heredity model" in s for s in limit):
        raise ValueError("THEORETICAL_PRIOR_ART_SCOPE_MISSING")
    return {
      "schema":"SLK_2012_ORIGINAL_PLOT_SEED_BIOMASS_ALLOCATION_VERSUS_MORPH_TURNOVER_V4",
      "primary_source_doi":pub["doi"],
      "interpretive_prior_art_doi":t["doi"],
      "external_cross_taxon_direct_experiment_doi":snail["doi"],
      "count_independent_experimental_plots":20,
      "sex_system_design":"TRIOECY; all plots include female phenotypes",
      "source_ratio_definition":"o_h = (seed dry biomass / aboveground biomass)_hermaphrodite divided by (seed dry biomass / aboveground biomass)_female",
      "male_presence_is_male_for_hermaphrodite_substitution":True,
      "source_values_printed_to_decimals":2,
      "descriptive_female_to_hermaphrodite_seed_allocation_share_ratio_bins_from_oh":ratio_bins,
      "theoretical_prior_nuclear_and_CMS_thresholds_apply_to_real_2012_plots":False,
      "o_h_allocation_ratio_can_equal_Heredity_viable_seed_g":False,
      "idealized_ancestral_thresholds_from_original_Heredity":{
         "nuclear_male_sterility":"g>2",
         "maternally_inherited_CMS":"g>1"
      },
      "joint_outcomes_counted_from_original_plot_summary":intersection,
      "female_seed_biomass_allocation_higher_plots":19,
      "female_morph_frequency_decline_plots":17,
      "female_allocation_higher_plus_decline_plots":17,
      "plot_level_records":table,
      "evidence_morph_increase_when_seed_higher_must_occur":False,
      "same_genotype_genetic_fitness_recovered":False,
      "CMS_cytotype_frequency_or_fatherhood_recovered":False,
      "Heredity_2025_is_existing_theory_not_new_SLK_causal_model":True,
      "experimental_2025_P_phys_acuta_cross_taxon_not_plant":True,
      "no_novel_p_values":True,
      "SLK_Phi_g0_Delta_R_identified":False,
      "limits":limit
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SRC)
    p.add_argument("--prior-art",type=Path,default=PRIOR)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    res=compute(json.loads(args.source.read_text(encoding="utf-8")),
                json.loads(args.prior_art.read_text(encoding="utf-8")))
    text=json.dumps(res,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()
