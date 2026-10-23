#!/usr/bin/env python3
"""Public ENA sample metadata joins ORIGINAL Aquilegia F2 plant phenotypes.

Johns et al. 2024 (doi:10.1186/s13227-024-00225-3), BioProject
PRJNA1089234. Source ENA file-report read_run aliases are source-provided
metadata only: NOT called SNP genotypes, validated alleles, QTL effects,
functional developmental modules or reconstructed ancestral trait regains.

In particular F2.<id>_2 carries a DIFFERENT BioSample accession from
F2.<id>_1 and may not simply be silently merged as a technical replicate.
Never download all 49.37 GB of phenotyped FASTQ just to validate sample IDs.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path

from audit_aquilegia_f2_partial_reassembly_v1 import (
    load_rows, summarize_rows, require
)

PROJECT = "PRJNA1089234"
DOI = "10.1186/s13227-024-00225-3"
F2_PATTERN = re.compile(r"^F2\.(\d+)(?:_(\d+))?$")


def parse_f2_id(name):
    """Recognize exact public ENA sample alias; preserve suffix separately."""
    if not isinstance(name, str):
        return None
    match = F2_PATTERN.fullmatch(name)
    if match is None:
        return None
    number, suffix = match.groups()
    if int(number) == 0 or (suffix is not None and int(suffix) == 0):
        return None
    return str(int(number))


def load_manifest(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _phenotyped_plants(rows):
    summary=summarize_rows(rows,strict=False)
    p=collections.defaultdict(dict)
    for row in rows:
        id = str(int(row["plant"]))
        key=(row["flower"],row["whorl"])
        require(key not in p[id],"DUPLICATE_FLOWER_WHORL")
        p[id][key]={
            "anther":int(row["anther"]),
            "expansion":int(row["lateral_expansion"]),
            "fusion":int(row["fusion"])
        }
    output={}
    for plant, observations in p.items():
        by=collections.defaultdict(dict)
        for (flower,whorl),value in observations.items():
            by[flower][whorl]=value
        for flower, v in by.items():
            require(set(v)=={"inner","outer"},"MISSING_INNER_OR_OUTER")
        mosaic=any(
            val["anther"]==1 and val["expansion"]>=2 and val["fusion"]==1
            for whorls in by.values() for val in whorls.values()
        )
        violation=any(
            (v["inner"]["anther"]==1 and v["outer"]["anther"]==0)
            or (v["outer"]["expansion"]>=2 and v["inner"]["expansion"]<2)
            for v in by.values())
        output[plant]={
            "flower_count":len(by), "mosaic_any_scored_flower":bool(mosaic),
            "positional_nesting_exception_any":bool(violation),
            "flowers":sorted(by)
        }
    require(len(rows)==summary["source"]["scored_whorl_rows"],
            "PHENOTYPE_SOURCE_ROW_COUNT_DRIFT")
    return output


def link_pheno_to_run_metadata(rows, manifest, strict=True):
    if not isinstance(manifest,dict):
        raise ValueError("INVALID_ENA_METADATA_MANIFEST")
    source=manifest.get("source",{})
    require(source.get("bioproject")==PROJECT and
            source.get("published_article_doi")==DOI,
            "ENA_PROJECT_OR_DOI_MISMATCH")
    pheno=_phenotyped_plants(rows)
    require(manifest.get("context",{}).get("original_F2_phenotyped_plants")
            ==len(pheno), "PHENOTYPE_CONTEXT_MISMATCH")
    records=manifest.get("run_metadata_rows")
    require(isinstance(records,list) and records,"MISSING_ENA_RUN_METADATA")
    seen_runs=set()
    grouped=collections.defaultdict(list)
    nfastq=allbytes=0
    zero=0
    f2rows=0
    for record in records:
        need=("run_accession","sample_accession","sample_alias",
              "experiment_accession","experiment_alias","library_name",
              "fastq_bytes")
        require(all(k in record for k in need),"ENA_REQUIRED_METADATA_MISSING")
        run=record["run_accession"]
        require(re.fullmatch(r"SRR\d+",run) is not None,
                "INVALID_ENA_SRR_ACCESSION")
        require(run not in seen_runs,"DUPLICATE_RUN_ACCESSION")
        seen_runs.add(run)
        require(re.fullmatch(r"SAMN\d+",record["sample_accession"]) is not None,
                "INVALID_ENA_BIOSAMPLE_ACCESSION")
        chunks=record["fastq_bytes"].split(";")
        require(all(re.fullmatch(r"\d+",v) is not None for v in chunks),
                "INVALID_ENA_FASTQ_BYTES")
        sizes=list(map(int,chunks))
        nfastq+=len(sizes)
        n=sum(sizes)
        allbytes+=n
        zero+=int(n==0)
        id=parse_f2_id(record["sample_alias"])
        if id is not None:
            f2rows+=1
            grouped[id].append(record)
        else:
            require(record["sample_alias"]=="Aj2_parent_HMR",
                    "UNKNOWN_NON_F2_ENA_SAMPLE")
    unmatched=sorted((p for p in pheno if p not in grouped),key=int)
    require(not unmatched,
            "ORIGINAL_PHENOTYPE_SAMPLE_HAS_NO_ENA_RUN")
    sample_links=[]
    for plant in sorted(pheno,key=int):
        refs=sorted(grouped[plant],key=lambda x:int(x["run_accession"][3:]))
        item={
            "plant":plant,"sample_aliases":[r["sample_alias"] for r in refs],
            "run_accessions":[r["run_accession"] for r in refs],
            "biosample_accessions":[r["sample_accession"] for r in refs],
            "scored_flower_count":pheno[plant]["flower_count"],
            "mosaic_any_scored_flower":pheno[plant]["mosaic_any_scored_flower"],
            "positional_nesting_exception_any":pheno[plant]["positional_nesting_exception_any"],
        }
        sample_links.append(item)
    multiples=[
        {
            "plant":id,
            "sample_aliases":[r["sample_alias"] for r in sorted(grouped[id],key=lambda x:x["run_accession"])],
            "run_accessions":[r["run_accession"] for r in sorted(grouped[id],key=lambda x:x["run_accession"])],
            "biosample_accessions":[r["sample_accession"] for r in sorted(grouped[id],key=lambda x:x["run_accession"])],
        }
        for id in sorted(grouped,key=int) if len(grouped[id])>1
    ]
    matched_bytes=sum(
        sum(int(t) for t in r["fastq_bytes"].split(";"))
        for plant in pheno for r in grouped[plant]
    )
    manifest_bytes=source.get("estimated_total_fastq_bytes")
    manifest_phen_bytes=source.get("phenotype_id_matched_fastq_bytes")
    require(allbytes==manifest_bytes and matched_bytes==manifest_phen_bytes,
            "SOURCE_ENA_FASTQ_METADATA_BYTES_CHANGED")
    if strict:
        require((len(records),f2rows,len(grouped),len(pheno))
                ==(341,340,336,231),"PINNED_F2_SRA_ID_COUNTS_CHANGED")
        require(len(multiples)==4 and [x["plant"] for x in multiples]
                ==["16","19","36","50"],"ORIGINAL_F2_MULTILIBRARY_ALIAS_DRIFT")
        require(nfastq==681 and zero==0,"ORIGINAL_FASTQ_FILE_METADATA_DRIFT")
        require(sum(x["mosaic_any_scored_flower"] for x in sample_links)
                ==91,"F2_MOSAIC_SOURCE_JOIN_DRIFT")
        require(sum(x["positional_nesting_exception_any"] for x in sample_links)
                ==1,"F2_NESTING_SOURCE_JOIN_DRIFT")
    return {
        "schema":"slk_anto_aquilegia_source_phenotype_to_ena_metadata_v4",
        "source":{
            "morphology_doi":DOI,
            "bioproject":PROJECT,
            "phenotype_source_git_blob_sha1":manifest["context"]["phenotype_source_git_blob_sha1"],
            "ENA_file_report_url":source["enriched_ena_url"],
            "snapshot_date":manifest["snapshot_date"],
            "original_authors_sequenced_DNA_not_ours":True,
        },
        "phenotypes":{
            "unique_F2_plant_ids":len(pheno),
            "original_scored_flowers":sum(x["flower_count"] for x in pheno.values()),
            "mosaic_positive_plants":sum(x["mosaic_any_scored_flower"] for x in pheno.values()),
            "nestedness_exception_plants":sum(x["positional_nesting_exception_any"] for x in pheno.values()),
        },
        "ENA_run_metadata":{
            "total_run_rows":len(records),
            "F2_run_rows":f2rows,
            "canonical_F2_id_count":len(grouped),
            "unphenotyped_SRA_F2_id_count":len(set(grouped)-set(pheno)),
            "canonical_ids_with_more_than_one_run":len(multiples),
            "ambiguous_F2_id_list":[x["plant"] for x in multiples],
            "all_F2_duplicate_records":multiples,
            "duplicated_alias_ids_present_in_phenotypes":sum(x["plant"] in pheno for x in multiples),
            "all_source_FASTQ_bytes":allbytes,
            "phenotyped_plant_alias_matched_FASTQ_bytes":matched_bytes,
            "fastq_file_count":nfastq,
            "zero_bytes_run_count":zero,
        },
        "linked_plant_count":len(sample_links),
        "linked_phenotype_plants":sample_links,
        "unlinked_phenotype_plant_ids":unmatched,
        "scientific_limits":{
            "source_FASTQ_files_have_not_been_downloaded":True,
            "duplicates_cannot_be_assumed_technical_replicates":True,
            "marker_genotypes_computed_or_validated":False,
            "all_source_samples_successfully_passed_author_QTL_QC":False,
            "structural_trait_associated_with_genomic_allele_identified":False,
            "functional_reexpression_genes_confirmed":False,
            "direct_Slk_ANTO_fitness_test_complete":False,
        },
    }


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument("--phenotypes",type=Path,
        default=root/"data/external/johns2024_aquilegia_f2_phenotypes_source.csv")
    parser.add_argument("--manifest",type=Path,
        default=root/"data/external/aquilegia_f2_PRJNA1089234_ena_run_metadata_v4.json")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=link_pheno_to_run_metadata(
        load_rows(args.phenotypes),load_manifest(args.manifest),strict=True)
    t=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output is None:print(t)
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(t,encoding="utf-8")


if __name__=="__main__":
    main()
