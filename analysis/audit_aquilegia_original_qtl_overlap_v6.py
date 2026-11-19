#!/usr/bin/env python3
"""Published Aquilegia 2024 Table 1 support-interval overlaps across floral traits.

This is a transparent re-tabulation of author-published QTL summaries, NOT
a genetic linkage-analysis refit, pleiotropy test, allele function or
historical trait re-evolution demonstration. Source 10.1186/s13227-024-00225-3
Table 1 is CC BY 4.0; original source is in data/external.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path

TRAITS={
    "Anther, inner","Anther, outer",
    "Lateral expansion, inner","Lateral expansion, outer",
    "Fusion"
}
SOURCE_DOI="10.1186/s13227-024-00225-3"
SOURCE_URL="https://link.springer.com/article/10.1186/s13227-024-00225-3/tables/1"
INTERVAL_PATTERN=re.compile(r"^([0-9]+(?:\.[0-9]+)?)–([0-9]+(?:\.[0-9]+)?)$")


def fail(condition, reason):
    if not condition:
        raise ValueError(reason)


def parse_publisher_table(path):
    """Parse true 16 table rows; blanks inherit original subtrait label."""
    text=Path(path).read_text(encoding="utf-8")
    lines=[line.strip() for line in text.splitlines() if line.lstrip().startswith("|")]
    fail(len(lines)>=3,"QTL_SOURCE_TABLE_MISSING")
    header=[p.strip() for p in lines[0].split("|")[1:-1]]
    fail(header==[
        "Subtrait","Chr","Name","1.5 LOD int (cM)","1.5LOD marker",
        "Peak position (cM)","LOD","PVE","Total PVE",
        "Additive effect","Dominance deviation","Degree of dominance"
    ],"QTL_SOURCE_HEADER_CHANGED")
    rows=[]
    trait=None
    seen=set()
    for line in lines[2:]:
        cells=[p.strip() for p in line.split("|")[1:-1]]
        fail(len(cells)==12,"QTL_SOURCE_ROW_COLUMNS_CHANGED")
        if cells[0]:
            fail(cells[0] in TRAITS,"UNKNOWN_QTL_TRAIT_LABEL")
            trait=cells[0]
        fail(trait is not None,"QTL_ROW_WITHOUT_TRAIT")
        parsed=INTERVAL_PATTERN.fullmatch(cells[3])
        fail(parsed is not None,"QTL_INTERVAL_PARSE_FAILURE")
        lo,hi=map(float,parsed.groups())
        fail(lo<=hi,"QTL_INTERVAL_INVERTED")
        try:
            chrn=int(cells[1])
            pve=float(cells[7])
            lod=float(cells[6])
            peak=float(cells[5])
        except (ValueError,TypeError):
            raise ValueError("QTL_SCORE_PARSE_FAILURE") from None
        fail(1<=chrn<=7 and 0<=pve<=100 and 0<=lod<1000,
             "QTL_SCORE_INVALID")
        name=cells[2]
        fail(name and name not in seen,"DUPLICATED_OR_UNNAMED_QTL_TRAIT_ROW")
        seen.add(name)
        rows.append({
            "trait":trait,
            "chromosome":chrn,
            "name":name,
            "interval_cM":[lo,hi],
            "peak_cM":peak,
            "LOD":lod,
            "PVE_percent":pve,
            "trait_total_PVE_percent":float(cells[8]) if cells[8] else None,
        })
    return rows


def pairwise_overlap(first,second):
    """All same-chromosome source QTL pairs, preserving both memberships."""
    found=[]
    for x in first:
        for y in second:
            if x["chromosome"]!=y["chromosome"]:
                continue
            lo=max(x["interval_cM"][0],y["interval_cM"][0])
            hi=min(x["interval_cM"][1],y["interval_cM"][1])
            overlap=lo<=hi
            found.append({
                "chromosome":x["chromosome"],
                "A":x["name"],"B":y["name"],
                "A_interval_cM":x["interval_cM"],
                "B_interval_cM":y["interval_cM"],
                "overlap_cM":max(0.,hi-lo),
                "shared_1_5_LOD_interval":overlap,
            })
    return {
        "same_chr_comparisons":len(found),
        "overlapping_support_regions":sum(x["shared_1_5_LOD_interval"] for x in found),
        "pairs":found,
        "overlap_not_pleiotropy_or_same_causal_locus":True,
    }


def audit_original_qtl_table(path,strict=True):
    rows=parse_publisher_table(path)
    by=collections.defaultdict(list)
    for row in rows:
        by[row["trait"]].append(row)
    comparisons={
        "anther_inner_vs_outer":
            ("Anther, inner","Anther, outer"),
        "lateral_expansion_inner_vs_outer":
            ("Lateral expansion, inner","Lateral expansion, outer"),
        "lateral_expansion_outer_vs_fusion":
            ("Lateral expansion, outer","Fusion"),
        "lateral_expansion_inner_vs_fusion":
            ("Lateral expansion, inner","Fusion"),
    }
    contrasts={label:pairwise_overlap(by[a],by[b]) for label,(a,b) in comparisons.items()}
    result={
        "schema":"slk_aquilegia_2024_published_QTL_support_interval_audit_v6",
        "source":{
            "doi":SOURCE_DOI,"original_publisher_table_url":SOURCE_URL,
            "original_table_rows":len(rows),
            "author_reported_independent_QTL":9,
            "trait_row_counts":dict(by_counts := {
                name:len(by[name]) for name in (
                    "Anther, inner","Anther, outer",
                    "Lateral expansion, inner","Lateral expansion, outer","Fusion"
                )
            }),
            "published_genetic_analysis_by_original_authors":True,
            "table_is_not_processed_329_by_599_marker_matrix":True,
        },
        "reported_rows":rows,
        "contrasts":contrasts,
        "interpretive_limits":{
            "author_QTL_analyses_are_not_newly_refit":True,
            "QTL_interval_overlap_proves_pleiotropy":False,
            "QTL_disjointness_proves_gene_modules_independent":False,
            "source_marker_genotype_matrix_loaded":False,
            "QTL_refit_by_this_repository":False,
            "source_QTL_positions_identify_causal_genes":False,
            "same_organ_effect_on_pollen_or_seed_fitness_estimated":False,
            "natural_ancestral_reexpression_confirmed":False,
        }
    }
    if strict:
        fail(len(rows)==16,"AUTHOR_16_TRAIT_ROW_COUNT_DRIFT")
        fail(by_counts=={
            "Anther, inner":3,"Anther, outer":4,
            "Lateral expansion, inner":4,"Lateral expansion, outer":2,"Fusion":3
        },"AUTHOR_QTL_TRAIT_ROW_COUNTS_DRIFT")
        expected={
            "anther_inner_vs_outer":(3,3),
            "lateral_expansion_inner_vs_outer":(3,0),
            "lateral_expansion_outer_vs_fusion":(2,2),
            "lateral_expansion_inner_vs_fusion":(3,0),
        }
        for k,(n,m) in expected.items():
            t=contrasts[k]
            fail((t["same_chr_comparisons"],t["overlapping_support_regions"])
                 ==(n,m),"AUTHOR_QTL_SUPPORT_REGION_PATTERN_DRIFT_"+k)
        largest=next(x for x in rows if x["name"]=="LEOU-Q3")
        fail((largest["chromosome"],largest["interval_cM"],largest["PVE_percent"])
             ==(3,[24.4,27.1],25.5),"ORIGINAL_MAJOR_QTL_NUMBER_CHANGED")
    return result


def main():
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,
                   default=root/"data/external/johns2024_aquilegia_qtl_table1_publisher_v6.md")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=audit_original_qtl_table(args.source,strict=True)
    payload=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload)


if __name__=="__main__":
    main()
