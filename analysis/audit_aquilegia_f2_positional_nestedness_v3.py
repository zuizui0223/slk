#!/usr/bin/env python3
"""Observed positional nesting of Aquilegia F2 stamen/staminode scores.

Original F2 source: Johns et al. (2024), EvoDevo 15:6,
DOI 10.1186/s13227-024-00225-3, Supplementary Material 3 (CC BY 4.0).

This does NOT observe evolutionary transitions, gene-module independence,
regained pollen fertility, reproductive fitness or ecological sorting.
Crucially, whorl labels are positions relative to carpels, NOT times.
The marginal-independence calculations are transparent counterfactual
random-repairing checks, NOT a plausible generative biological null model.
"""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path
from audit_aquilegia_f2_partial_reassembly_v1 import (
    load_rows, summarize_rows, require,
)


def _anther(sample):
    n=len(sample)
    inner=sum(x["inner"]["AN"] == 1 for x in sample)
    outer=sum(x["outer"]["AN"] == 1 for x in sample)
    v=sum(x["inner"]["AN"] == 1 and x["outer"]["AN"] == 0 for x in sample)
    r=sum(x["outer"]["AN"] == 1 and x["inner"]["AN"] == 0 for x in sample)
    return {
        "n_flowers":n, "inner_anther_present":inner,
        "outer_anther_present":outer, "inner_yes_outer_no_violation":v,
        "outer_yes_inner_no":r,
        "inner_yes_outer_yes":inner-v,
        "inner_no_outer_no":n-outer-v,
    }


def _expansion(sample, threshold):
    n=len(sample)
    inner=sum(x["inner"]["LE"]>=threshold for x in sample)
    outer=sum(x["outer"]["LE"]>=threshold for x in sample)
    violating=sorted(x["plant"]+"|"+x["flower"] for x in sample
        if x["outer"]["LE"]>=threshold and x["inner"]["LE"]<threshold)
    onlyinner=sum(x["inner"]["LE"]>=threshold and x["outer"]["LE"]<threshold
                  for x in sample)
    return {
        "n_flowers":n, "inner_high":inner, "outer_high":outer,
        "outer_high_inner_low_violation":len(violating),
        "inner_high_outer_low":onlyinner,
        "both_high":outer-len(violating),
        "both_low":n-inner-len(violating),
        "violation_plant_flower_keys":violating,
    }


def _both_rules(sample):
    exceptions=sorted(x["plant"]+"|"+x["flower"] for x in sample
        if (x["inner"]["AN"]==1 and x["outer"]["AN"]==0)
        or (x["outer"]["LE"]>=2 and x["inner"]["LE"]<2))
    return {
        "n_flowers":len(sample),
        "both_rules_hold":len(sample)-len(exceptions),
        "either_rule_fails":len(exceptions),
        "observed_exception_keys":exceptions,
    }


def summarize_ordered_identity(rows, strict=True):
    rows=list(rows)
    verified=summarize_rows(rows,strict=strict)
    flowers=collections.defaultdict(dict)
    plant=collections.defaultdict(dict)
    for r in rows:
        k=(r["plant"].strip(),r["flower"].strip())
        flowers[k][r["whorl"]]={
            "AN":int(r["anther"]), "LE":int(r["lateral_expansion"]),
            "FU":int(r["fusion"]),
        }
    sample=[]
    for (p,f),whorls in flowers.items():
        require(set(whorls)=={"inner","outer"},
                "MISSING_INNER_OR_OUTER")
        x={"plant":p,"flower":f,"inner":whorls["inner"],
           "outer":whorls["outer"]}
        sample.append(x)
        plant[p][f]=x
    first=[v["a"] if "a" in v else v["b"] for v in plant.values()]
    double_a=[v["a"] for v in plant.values() if len(v)==2]
    double_b=[v["b"] for v in plant.values() if len(v)==2]
    subsets={
        "all_flowers":sample,
        "first_flower_per_plant":first,
        "double_scored_flower_a":double_a,
        "double_scored_flower_b":double_b,
    }
    anthers={k:_anther(v) for k,v in subsets.items()}
    tarr=[{
        "threshold":t,
        "score_definition":(
            "any_lateral_expansion_beyond_halfway" if t==3
            else "expansion_at_least_halfway" if t==2
            else "any_positive_expansion"),
        "all_flowers":_expansion(sample,t),
        "first_flower_per_plant":_expansion(first,t),
    } for t in (1,2,3)]
    both={k:_both_rules(v) for k,v in subsets.items()}
    ax=anthers["first_flower_per_plant"]
    lx=tarr[1]["first_flower_per_plant"]
    n=len(first)
    independent={
        "n_genotypes":n,
        "anther_expected_violations_if_unpaired":
            ax["inner_anther_present"]*
            (n-ax["outer_anther_present"])/n,
        "LE2_expected_violations_if_unpaired":
            lx["outer_high"]*(n-lx["inner_high"])/n,
    }
    if strict:
        require(n==231 and len(sample)==400 and len(double_a)==169,
                "PINNED_F2_SOURCE_GRAIN_DRIFT")
        require((anthers["all_flowers"]["inner_anther_present"],
                 anthers["all_flowers"]["outer_anther_present"],
                 anthers["all_flowers"]["inner_yes_outer_no_violation"],
                 anthers["all_flowers"]["outer_yes_inner_no"])
                ==(184,283,0,99), "PINNED_AN_POSITIONAL_CONSTRAINT_DRIFT")
        require([(x["threshold"],
                  x["all_flowers"]["outer_high_inner_low_violation"])
                 for x in tarr]==[(1,1),(2,1),(3,0)],
                "PINNED_LE_THRESHOLD_SENSITIVITY_DRIFT")
        require(both["all_flowers"]["both_rules_hold"]==399 and
                both["first_flower_per_plant"]["both_rules_hold"]==230,
                "PINNED_CONJUNCTION_DRIFT")
    return {
        "schema":"slk_anto_aquilegia_source_positional_nesting_v3",
        "source":{
            "doi":"10.1186/s13227-024-00225-3",
            "original_publisher_git_blob_sha1":
                verified["source"]["original_publisher_csv_git_blob_sha1"],
            "phenotype_source_owned_by_authors":True,
            "within_flower_anther_score_not_fertility":True,
            "whorls_are_positions_not_evolutionary_time":True,
        },
        "sample":{
            "plants":len(plant), "flowers":len(sample),
            "inner_outer_whorl_score_rows":len(rows),
            "one_flower_per_plant_sensitivity_n":len(first),
            "double_scored_plants":len(double_a),
        },
        "positionally_nested_anther":anthers,
        "lateral_expansion_threshold_sensitivity":tarr,
        "conjunctive_nesting_at_LE2":{
            **both,"observed_exception_keys":both["all_flowers"]["observed_exception_keys"],
        },
        "marginal_independence_counterfactual":{
            "one_flower_per_plant":independent,
            "independent_pairing_is_biologically_realistic_null":False,
            "marginal_null_means_genetically_independent_modules":False,
            "contrasts_are_descriptive_morphology_not_selection":True,
        },
        "evidence_ceiling":{
            "observed_gene_modules_independent":False,
            "pollen_viability_of_anther_positive_organs_known":False,
            "whorl_order_equates_developmental_or_evolutionary_time":False,
            "field_pollinator_fitness_of_mosaics_measured":False,
            "natural_ancestral_trait_regain_rate_estimated":False,
            "direct_same_lineage_SLK_ANTO_causal_test_complete":False,
        },
    }


def main():
    parser=argparse.ArgumentParser()
    root=Path(__file__).resolve().parents[1]
    parser.add_argument("--input",type=Path,
        default=root/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv")
    parser.add_argument("--output",type=Path)
    parser.add_argument("--expected",type=Path)
    args=parser.parse_args()
    r=summarize_ordered_identity(load_rows(args.input),strict=True)
    if args.expected:
        frozen=json.loads(args.expected.read_text(encoding="utf-8"))
        require(frozen==r,"INDEPENDENT_SOURCE_NESTING_RECEIPT_DRIFT")
    payload=json.dumps(r,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload)


if __name__=="__main__":
    main()
