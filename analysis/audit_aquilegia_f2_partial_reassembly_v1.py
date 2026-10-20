#!/usr/bin/env python3
"""Actual Aquilegia F2 stamen/staminode phenotype modularity re-analysis.

Original Johns et al. (2024), EvoDevo 15:6, DOI 10.1186/s13227-024-00225-3,
Supplementary Material 3: author phenotypic score file distributed CC BY 4.0.
This analysis belongs to SLK's biological bridging branch; it does not
introduce a new Cirsium empirical dataset into ANTO.

Biological grain:
 * 231 F2 plants, with one or two flowers
 * 400 flowers, with paired inner / outer whorl scores
 * 800 whorl-score rows
 * fusion is a BETWEEN-whorls flower property repeated on BOTH rows.
No pollen fertility assays, ancestral allele tracing, floral reproductive
fitness, genetically validated developmental toolkit, or natural regain
are in this file. Presence of an anther (AN=1) is not viable pollen.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

SOURCE_DOI = "10.1186/s13227-024-00225-3"
SOURCE_URL = (
 "https://static-content.springer.com/esm/"
 "art%3A10.1186%2Fs13227-024-00225-3/MediaObjects/"
 "13227_2024_225_MOESM3_ESM.csv"
)
# Git blob of the accompanying 800-row original publisher CSV copy.
SOURCE_BLOB_SHA1 = "9911d4a5e85fa8629ad9890f28992e0f07e5feca"
COLUMNS = (
    "plant","flower","stamens","whorl","anther",
    "lateral_expansion","fusion","std_whorl_organs","total_organs","notes",
)


def require(value: bool, message: str):
    if not value:
        raise ValueError(message)


def git_blob_sha1(payload: bytes):
    return hashlib.sha1(
        b"blob "+str(len(payload)).encode("ascii")+b"\0"+payload
    ).hexdigest()


def load_rows(path: Path):
    """Read unmodified publisher-supplement copy, verifying Git blob bytes."""
    source = Path(path).read_bytes()
    require(git_blob_sha1(source)==SOURCE_BLOB_SHA1,
            "SOURCE_AQUILEGIA_PUBLISHER_CSV_GIT_SHA_MISMATCH")
    reader = csv.DictReader(source.decode("utf-8-sig").splitlines())
    require(tuple(reader.fieldnames or ())==COLUMNS,
            "SOURCE_HEADER_MISMATCH")
    rows=[]
    for row in reader:
        require(None not in row and all(x is not None for x in row.values()),
                "SOURCE_ROW_WIDTH_MISMATCH")
        rows.append({key: val.strip() for key,val in row.items()})
    return rows


def score(row: dict, name: str, allowed: set[int]):
    raw=row[name]
    try:
        value=int(raw)
    except (ValueError,TypeError):
        raise ValueError("INVALID_TRAIT_SCORE_"+name) from None
    require(str(value)==str(raw) and value in allowed,
            "INVALID_TRAIT_SCORE_"+name)
    return value


def summarize_rows(rows: list[dict], strict: bool=True):
    rows=list(rows)
    require(len(rows)>0, "NO_AQUILEGIA_PHENOTYPE_ROWS")
    if strict:
        require(len(rows)==800,"SOURCE_ORIGINAL_800_WHORL_ROWS_CHANGED")
    plant_to_flowers: dict[str,set[str]] = collections.defaultdict(set)
    flower_to_whorls: dict[tuple[str,str],dict] = {}
    scored=[]
    for r in rows:
        require(all(k in r for k in COLUMNS),"SOURCE_MISSING_TRAIT_COLUMN")
        plant=str(r["plant"]).strip()
        flower=str(r["flower"]).strip()
        whorl=str(r["whorl"]).strip()
        require(bool(plant and flower and whorl in ("inner","outer")),
                "INVALID_PLANT_FLOWER_WHORL_ID")
        anther=score(r,"anther",{0,1})
        expansion=score(r,"lateral_expansion",{0,1,2,3})
        fusion=score(r,"fusion",{0,1})
        flower_key=(plant,flower)
        w=flower_to_whorls.setdefault(flower_key,{})
        require(whorl not in w,"DUPLICATE_FLOWER_WHORL")
        entry={"plant":plant,"flower":flower,"whorl":whorl,
               "anther":anther,"LE":expansion,"fusion":fusion}
        w[whorl]=entry
        scored.append(entry)
        plant_to_flowers[plant].add(flower)

    for (plant,flower),pair in flower_to_whorls.items():
        require(set(pair)=={"inner","outer"}, "MISSING_INNER_OR_OUTER")
        require(pair["inner"]["fusion"]==pair["outer"]["fusion"],
                "FUSION_IS_BETWEEN_WHORLS_NOT_TWO_INDEPENDENT_SCORES")

    plants_one=sum(len(x)==1 for x in plant_to_flowers.values())
    plants_two=sum(len(x)==2 for x in plant_to_flowers.values())
    require(all(len(x) in (1,2) for x in plant_to_flowers.values()),
            "UNSUPPORTED_THREE_PLUS_FLOWERS_PER_F2_PLANT")
    pairs=list(flower_to_whorls.values())

    def anther_solely_outer(w):
        return w["inner"]["anther"]==0 and w["outer"]["anther"]==1
    def anther_solely_inner(w):
        return w["inner"]["anther"]==1 and w["outer"]["anther"]==0
    def chimera(r):
        # This is a morphological CO-OCCURRENCE, not a genetic module
        # independence or an experiment confirming gamete fertility.
        return (r["anther"]==1 and r["LE"]>=2 and r["fusion"]==1)

    pure_staminode=sum(
        r["anther"]==0 and r["LE"]==3 and r["fusion"]==1
        for r in scored)
    pure_stamen=sum(
        r["anther"]==1 and r["LE"]==0 and r["fusion"]==0
        for r in scored)
    chimera_count=sum(chimera(r) for r in scored)
    any_chimeric_flowers=sum(
        any(chimera(r) for r in pair.values()) for pair in pairs)
    any_chimeric_plants=len({
        r["plant"] for r in scored if chimera(r)
    })
    flower_diff_le_reverse=sorted(
        ["|".join(key) for key,pair in flower_to_whorls.items()
         if pair["inner"]["LE"] < pair["outer"]["LE"]]
    )
    report = {
        "schema":"slk_anto_aquilegia_f2_whorl_reassembly_original_source_v1",
        "source":{
            "citation":"Johns et al. 2024 EvoDevo 15:6, Supplementary Material 3",
            "doi":SOURCE_DOI,
            "original_supplement_url":SOURCE_URL,
            "original_publisher_csv_git_blob_sha1":SOURCE_BLOB_SHA1,
            "license":"Creative Commons Attribution 4.0 (publisher article/supplement)",
            "sample_basis":"F2 of A. jonesii x A. coerulea Origami",
            "scored_whorl_rows":len(scored),
            "scored_flowers":len(flower_to_whorls),
            "unique_f2_plants":len(plant_to_flowers),
            "plants_scored_one_flower":plants_one,
            "plants_scored_two_flowers":plants_two,
            "repeated_fusion_measurement_is_not_independent":True,
            "author_genomic_sample_separate_from_this_phenotype_CSV":True,
        },
        "morphology":{
            "anther_present_whorl_rows":sum(r["anther"]==1 for r in scored),
            "anther_absent_whorl_rows":sum(r["anther"]==0 for r in scored),
            "pure_staminode_endpoint_whorl_rows":pure_staminode,
            "pure_stamen_endpoint_whorl_rows":pure_stamen,
            "non_endpoint_whorl_rows":len(scored)-pure_staminode-pure_stamen,
            "observed_distinct_anther_LE_fusion_combinations":
                len({(r["anther"],r["LE"],r["fusion"]) for r in scored}),
            "anther_present_LEge2_fused_whorl_rows":chimera_count,
            "flowers_with_any_anther_present_LEge2_fused_whorl":
                any_chimeric_flowers,
            "plants_with_any_anther_present_LEge2_fused_whorl":
                any_chimeric_plants,
        },
        "paired_whorls":{
            "flower_pairs":len(pairs),
            "outer_anther_yes_inner_no":sum(map(anther_solely_outer,pairs)),
            "inner_anther_yes_outer_no":sum(map(anther_solely_inner,pairs)),
            "anther_same":sum(p["inner"]["anther"]==
                              p["outer"]["anther"] for p in pairs),
            "LE_inner_greater":sum(p["inner"]["LE"]>p["outer"]["LE"]
                                   for p in pairs),
            "LE_outer_greater":len(flower_diff_le_reverse),
            "LE_equal":sum(p["inner"]["LE"]==p["outer"]["LE"]
                           for p in pairs),
            "LE_outer_greater_flower_keys":flower_diff_le_reverse,
            "every_f2_flower_obeys_strict_LE_gradient":False,
            "one_per_plant_author_analysis_not_our_all_flower_analyses":True,
            "fusion_identical_by_scoring":sum(
                p["inner"]["fusion"]==p["outer"]["fusion"] for p in pairs),
            "fused_flowers":sum(p["inner"]["fusion"]==1 for p in pairs),
            "fusion_independent_whorl_measurements":0,
        },
        "biological_claim_limits":{
            "pollen_fertility_confirmed":False,
            "individual_locus_genotype_linked_in_this_CSV":False,
            "biochemical_developmental_toolkit_retention_measured":False,
            "ecological_fitness_or_pollinator_payoff_estimated":False,
            "recurrent_natural_re_expression_confirmed":False,
            "SLK_candidate_structural_payoff_calibrated":False,
        },
        "interpretation":{
            "actual_biological_phenotype_co_occurrence":True,
            "differential_inner_outer_whorl_identity":True,
            "genetic_modularity_not_inferred_from_morphology_alone":True,
            "QTL_results_are_from_original_authors_not_our_CSV_refit":True,
            "400_flower_counts_are_not_400_independent_genotypes":True,
            "3_morphological_traits_are_not_3_functional_gene_modules":True,
            "staminode_return_does_not_equal_restored_ancestral_pollen_role":True,
        },
    }
    if strict:
        expected=(231,400,62,169,99,0,181,2,187,129,91,15,234)
        actual=(report["source"]["unique_f2_plants"],
                report["source"]["scored_flowers"],
                plants_one,plants_two,
                report["paired_whorls"]["outer_anther_yes_inner_no"],
                report["paired_whorls"]["inner_anther_yes_outer_no"],
                report["paired_whorls"]["LE_inner_greater"],
                report["paired_whorls"]["LE_outer_greater"],
                chimera_count,any_chimeric_flowers,any_chimeric_plants,
                report["morphology"]["observed_distinct_anther_LE_fusion_combinations"],
                report["paired_whorls"]["fused_flowers"])
        require(actual==expected,"PINNED_SOURCE_REANALYSIS_COUNT_DRIFT")
    return report


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=(
        root/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv"))
    parser.add_argument("--output",type=Path)
    parser.add_argument("--expected",type=Path)
    args=parser.parse_args()
    result=summarize_rows(load_rows(args.input))
    if args.expected:
        frozen=json.loads(args.expected.read_text(encoding="utf-8"))
        require(result==frozen, "FROZEN_EMPIRICAL_RECEIPT_DIFFERENT")
    txt=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(txt,encoding="utf-8")
    else:
        print(txt)
    return result


if __name__=="__main__":
    main()
