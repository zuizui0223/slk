#!/usr/bin/env python3
"""Paired-flowER developmental organ-state repeatability from real Aquilegia F2.

Source Johns et al. 2024 (doi:10.1186/s13227-024-00225-3) Supplement 3,
retrieved with original publisher attribution, immutable Git blob in SLK.
No pollen viability, native genetic function, seed fitness, pollination ecology,
transgenerational regained capacity or trait-developmental independence measured.

Authors themselves described strong yet incomplete repeatability; this is an
independent SAME-PLANT quantitative reinterpretation for SLK x ANTO, NOT
a new genetic association test.
"""
from __future__ import annotations
import argparse
import collections
import json
from fractions import Fraction as F
from pathlib import Path
from audit_aquilegia_f2_partial_reassembly_v1 import (
    load_rows, summarize_rows, require,
)

def summarize_repeated_plants(rows, strict=True):
    raw=summarize_rows(rows,strict=strict)  # catches missing whorl/duplicate/invalid score
    plants=collections.defaultdict(dict)
    for row in rows:
        key=str(row["plant"]).strip()
        flower=str(row["flower"]).strip()
        whorl=str(row["whorl"]).strip()
        v=plants[key].setdefault(flower,{})
        v[whorl]={
            "AN":int(row["anther"]),
            "LE":int(row["lateral_expansion"]),
            "FU":int(row["fusion"]),
        }
    n1=sum(len(fl)==1 for fl in plants.values())
    n2=sum(len(fl)==2 for fl in plants.values())
    pairs=[]
    for plant, flowers in plants.items():
        if len(flowers)==2:
            require(set(flowers)=={"a","b"},"UNEXPECTED_REPLICATED_FLOWER_NAMES")
            pairs.append((flowers["a"],flowers["b"]))
    require(len(pairs)==n2 and len(pairs)>0,"NO_TWO_FLOWER_F2_PLANTS")

    def same(one,two,trait,whorl):
        return one[whorl][trait]==two[whorl][trait]

    status=collections.Counter()
    for a,b in pairs:
        ia=same(a,b,"AN","inner")
        oa=same(a,b,"AN","outer")
        status["AN_inner_same"]+=ia
        status["AN_outer_same"]+=oa
        status["AN_both_whorls_same"]+=ia and oa
        status["AN_inner_different_only"]+=(not ia) and oa
        status["AN_outer_different_only"]+=ia and (not oa)
        status["AN_both_whorls_different"]+=(not ia) and (not oa)
        status["LE_inner_same"]+=same(a,b,"LE","inner")
        status["LE_outer_same"]+=same(a,b,"LE","outer")
        status["FU_flower_level_same"]+=same(a,b,"FU","inner")
    status["LE_inner_different"]=n2-status["LE_inner_same"]
    status["LE_outer_different"]=n2-status["LE_outer_same"]
    status["FU_flower_level_different"]=n2-status["FU_flower_level_same"]

    def mosaic(f):
        return any(r["AN"]==1 and r["LE"]>=2 and r["FU"]==1
                   for r in f.values())
    m=collections.Counter()
    for a,b in pairs:
        A,B=mosaic(a),mosaic(b)
        m["both_flower_mosaic"]+=A and B
        m["only_flower_a_mosaic"]+=A and not B
        m["only_flower_b_mosaic"]+=B and not A
        m["neither_flower_mosaic"]+=not A and not B
        m["double_plants_any_flower_mosaic"]+=A or B
        m["double_plants_a_flower_mosaic"]+=A
        m["double_plants_b_flower_mosaic"]+=B
        m["double_plants_discordant_mosaic"]+=A!=B
    m["single_plants_any_flower_mosaic"]=sum(
        mosaic(next(iter(flowers.values()))) for flowers in plants.values()
        if len(flowers)==1)
    m["all_F2_plants_any_mosaic"]=(
        m["double_plants_any_flower_mosaic"]+
        m["single_plants_any_flower_mosaic"]
    )
    m["double_plants_first_flower_detection_rate"]=F(
        m["double_plants_a_flower_mosaic"],n2)
    m["double_plants_two_flower_detection_rate"]=F(
        m["double_plants_any_flower_mosaic"],n2)
    denom=n2-m["double_plants_a_flower_mosaic"]
    m["among_first_flower_negative_second_positive"]=(
        F(m["only_flower_b_mosaic"],denom) if denom else None)

    # Within-genotype agreement compared to *marginal chance* when first
    # and second flower records are randomly assigned to unrelated plants.
    # This null is descriptive only; age/greenhouse environments and the
    # non-random phenotyped-F2 subset can also cause repeatability.
    null={}
    for key,trait,whorl in (("AN_inner","AN","inner"),("AN_outer","AN","outer"),
                             ("LE_inner","LE","inner"),("LE_outer","LE","outer"),
                             ("FU","FU","inner")):
        left=collections.Counter(a[whorl][trait] for a,b in pairs)
        right=collections.Counter(b[whorl][trait] for a,b in pairs)
        exp=sum(left[x]*right[x] for x in set(left)|set(right))
        chance=F(exp,n2*n2)
        agree=(F(status["FU_flower_level_same"],n2) if key=="FU"
               else F(status[key+"_same"],n2))
        null[key]={
            "same_plant_agreement_fraction":float(agree),
            "independently_paired_expected_agreement_fraction":float(chance),
            "agreement_excess_over_marginal_independence":float(agree-chance),
            "formal_genetic_heritability_or_environment_partition":False,
        }

    def as_json(v):
        if isinstance(v,F):
            return float(v)
        if isinstance(v,dict):
            return {k:as_json(x) for k,x in v.items()}
        return v

    out={
        "schema":"aquilegia_original_F2_individual_repeat_expression_v2",
        "source_scope":{
            "article_doi":"10.1186/s13227-024-00225-3",
            "supplement":"Supplementary Material 3, original 800 whorl scores",
            "source_git_blob_sha1":raw["source"]["original_publisher_csv_git_blob_sha1"],
            "fusion_is_one_flower_trait":True,
            "authors_existing_repeatability_claims_not_new_discovery":True,
            "LE_inner_exact_disagreement_with_paper_report":{
                "our_rows_same":int(status["LE_inner_same"]),
                "authors_prose_reports_same":139,
                "meaning":"possible dataset/edit/definition discrepancy; not an inference of incorrect authors",
            },
        },
        "sample":{
            "plants":len(plants),
            "flowers":raw["source"]["scored_flowers"],
            "whorl_rows":len(rows),
            "one_flower_plants":n1,
            "two_flower_plants":n2,
            "F2_cross_not_natural_regain":True,
        },
        "paired_flower_concordance":dict(status),
        "mosaic_anther_and_staminode_filament":as_json(dict(m)),
        "replication_vs_marginal_null":null,
        "inference_limits":{
            "failure_to_see_mosaic_means_no_competence":False,
            "shared_plant_genotype_implies_genetic_locus_identified":False,
            "field_trait_regain_documented":False,
            "fertile_pollen_or_ovary_protection_assayed":False,
            "natural_heritable_capacity_transition_rate_estimated":False,
            "SLK_floral_architecture_payoff_identified":False,
            "same_genotype_functional_gene_toolkit_measured":False,
            "one_flower_is_independent_new_genetic_replicate":False,
        }
    }
    if strict:
        require((len(plants),n1,n2)==(231,62,169),"ORIGINAL_SAMPLE_COUNT_DRIFT")
        expected={
            "AN_inner_same":139,"AN_outer_same":139,
            "AN_both_whorls_same":119,
            "AN_inner_different_only":20,"AN_outer_different_only":20,
            "AN_both_whorls_different":10,
            "LE_inner_same":138,"LE_outer_same":123,
            "FU_flower_level_same":154,
        }
        require(all(status[k]==v for k,v in expected.items()),
                "ORIGINAL_WITHIN_PLANT_CONCORDANCE_COUNT_DRIFT")
        require((m["both_flower_mosaic"],m["only_flower_a_mosaic"],
                 m["only_flower_b_mosaic"],m["neither_flower_mosaic"])
                ==(38,23,16,92),
                "ORIGINAL_WITHIN_PLANT_MOSAIC_COUNT_DRIFT")
    return out

def main():
    parser=argparse.ArgumentParser()
    root=Path(__file__).resolve().parents[1]
    parser.add_argument("--input",type=Path,default=root/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv")
    parser.add_argument("--output",type=Path)
    parser.add_argument("--expected",type=Path)
    args=parser.parse_args()
    out=summarize_repeated_plants(load_rows(args.input),strict=True)
    if args.expected:
        frozen=json.loads(args.expected.read_text(encoding="utf-8"))
        require(frozen==out,"FROZEN_SOURCE_REANALYSIS_DRIFT")
    content=json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content,encoding="utf-8")
    else:
        print(content)
    return out

if __name__=="__main__":
    main()
