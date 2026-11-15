#!/usr/bin/env python3
"""Check published Cossard & Pannell 2021 experimental sex-expression response.

Author's source result: 3 all-female vs 3 male-female common-garden plots,
female male-flower biomass/vegetative biomass = 2.33 times in all-female.
No individual Dryad rows retrieved, no re-fit or original genotype-level
fitness. Uncertainty/p-values come from the AUTHOR paper, not this script.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/evidence/mercurialis_2021_mate_absence_leaky_female_source_v1.json"


def compute(s):
    if (s["primary_source"]["doi"]!="10.1111/jeb.13720" or
        s["plant"]["ploidy"]!="DIPLOID_XX_FEMALES_XY_MALES"):
        raise ValueError("SOURCE_PLOIDY_OR_PROVENANCE_CHANGED")
    d=s["design"]
    if (d["experimental_common_gardens"]!=6 or
        d["control_dioecious_plots"]!=3 or d["all_female_plots"]!=3 or
        d["control_population_parent_sex_counts"]!={"male":90,"female":90} or
        d["all_female_population_parent_sex_counts"]!={"male":0,"female":180}
        or d["initial_total_plants"]!=1080 or d["treated_growth_weeks"]!=7):
        raise ValueError("SOURCE_RANDOMIZED_MATE_CONTEXT_CHANGED")
    if (d["source_demographically_mixed_seeds_from_demes"]!=35 or
        d["scored_female_plants"]!=272 or
        not d["measured_population_replicates_not_272_independent_populations"]):
        raise ValueError("SOURCE_POPULATION_AND_NESTING_CHANGED")
    p=d["sampled_pot_occupancy_counts"]
    n1=p["one_female_from_each_pot"]
    n2=p["pots_with_two_sampled_females"]
    n3=p["pots_with_three_sampled_females"]
    if (any(type(v)!=int or v<0 for v in (n1,n2,n3))
        or n1+2*n2+3*n3!=272 or
        d["pot_structure"].split("×")[0]!="60 pots per plot "):
        raise ValueError("NESTED_SAMPLE_COUNT_NOT_REPRODUCED")
    ppub=s["published_results"]
    if (ppub["male_reproductive_effort_all_female_over_control_ratio"]!=2.33
        or ppub["male_effort_group_treatment_p"]!=.01
        or ppub["leakiness_incidence_group_difference_p"]!=.058
        or ppub["female_effort_group_treatment_p"]!=.19
        or ppub["number_of_males_in_same_pot_male_effort_p"]!=.851
        or ppub["number_of_males_in_same_pot_female_effort_p"]!=.977):
        raise ValueError("REPORTED_TREATMENT_OR_RESPONSE_CHANGED")
    if (ppub["actual_self_sired_seed_count_in_original_plots"]!="NOT_MEASURED"
        or ppub["pollen_viability_of_induced_male_flowers"]!="NOT_MEASURED"
        or ppub["adaptive_plasticity_causal_fitness_evidence"]!="NOT_DEMONSTRATED_AS_DUAL_ENVIRONMENT_GENOTYPE_FITNESS_CROSSOVER"):
        raise ValueError("FALSE_ADAPTIVE_PLASTICITY_FITNESS_PROOF")
    if "95th percentile" not in d["leakiness_threshold_rule"]:
        raise ValueError("CONTROL_5_PERCENT_INCIDENT_CIRCULARITY_LOST")
    if not any("2021 diploid XX" in x for x in s["limitations"]):
        raise ValueError("CROSS_PLOIDY_NONCOMPARABILITY_LOST")
    sampled_pots=n1+n2+n3
    females_in_multi_sampled_pots=n2*2+n3*3
    return {
        "schema":"SLK_MERCURIALIS_2021_ORIGINAL_MATE_ABSENCE_SOURCE_AUDIT_V1",
        "source_doi":s["primary_source"]["doi"],
        "source_ploidy":"DIPLOID_XX_FEMALES_XY_MALES",
        "source_seed_demes":d["source_demographically_mixed_seeds_from_demes"],
        "treatment_population_counts":{
            "controls_with_males":d["control_dioecious_plots"],
            "female_only":d["all_female_plots"]
        },
        "parental_sex_counts_per_population":{
            "control":d["control_population_parent_sex_counts"],
            "female_only":d["all_female_population_parent_sex_counts"]
        },
        "initial_control_total_plants":d["control_dioecious_plots"]*180,
        "initial_female_only_total_plants":d["all_female_plots"]*180,
        "initial_total_plants":d["initial_total_plants"],
        "female_phenotyped_n":d["scored_female_plants"],
        "sampled_unique_pots_from_source_occupancy":sampled_pots,
        "sampled_female_plants_sharing_pots_with_other_sampled_females":females_in_multi_sampled_pots,
        "fraction_females_from_multi_sampled_pots":round(females_in_multi_sampled_pots/272,8),
        "experimental_plot_replicates":d["experimental_common_gardens"],
        "male_relative_reproductive_allocation_no_mates_over_with_males":{
            "published_ratio":ppub["male_reproductive_effort_all_female_over_control_ratio"],
            "published_p":ppub["male_effort_group_treatment_p"],
            "metric":"male flower dry biomass divided by vegetative aboveground biomass",
            "new_effect_size_or_CI":None
        },
        "incidence_of_leaky_females":{
            "published_group_comparison_p":ppub["leakiness_incidence_group_difference_p"],
            "significant_at_point_zero_five":False,
            "source_control_incidence_by_threshold_definition":.05,
            "control_incidence_is_not_independent_natural_prevalence":True
        },
        "female_reproductive_effort":{
            "published_group_comparison_p":ppub["female_effort_group_treatment_p"],
            "no_detected_mean_difference":True,
            "zero_female_cost_proven":False
        },
        "pot_male_neighbor_count":{
            "male_effort_original_p":ppub["number_of_males_in_same_pot_male_effort_p"],
            "female_effort_original_p":ppub["number_of_males_in_same_pot_female_effort_p"],
            "pollen_or_fruit_signal_identity_demonstrated":False
        },
        "same_clonal_genotype_treatment_comparison":False,
        "self_paternity_or_seed_viability_measured":False,
        "adaptive_reaction_norm_crossing_with_fitness_measured":False,
        "published_paper_proposes_island_colonization_without_testing_islands":True,
        "raw_Dryad_individual_file_downloaded":False,
        "may_be_pooled_with_2024_hexaploid_distance_LMM":False,
        "SLK_Phi_g0_Delta_R_measured":False,
        "all_new_p_values":None,
        "limitations":s["limitations"]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=SRC)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    res=compute(json.loads(a.source.read_text(encoding="utf-8")))
    blob=json.dumps(res,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(blob,encoding="utf-8")
    else:
        print(blob,end="")


if __name__=="__main__":
    main()
