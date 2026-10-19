#!/usr/bin/env python3
"""Audit taxon overlap between verified GloPL and Razanajatovo 2016 breeding data.

This deliberately stops at *coverage* (not ecological association).
Use direct published, externally hosted supplementary XLSX; do not redistribute.
The analysis core uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
import zipfile
from collections import Counter
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

from analyze_glopl_context_variation import (
    SOURCE_URL,
    _csv_rows_from_bytes,
    _eligible,
    _git_blob_sha,
    UPSTREAM_BLOB_SHA,
)

BREEDING_URL = (
    "https://media.springernature.com/original/springer-static/"
    "esm/art%3A10.1038%2Fncomms13313/MediaObjects/"
    "41467_2016_BFncomms13313_MOESM1062_ESM.xlsx"
)
BREEDING_DOI = "10.1038/ncomms13313"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
CELL_REF = re.compile(r"^([A-Z]+)")
BINOMIAL = re.compile(r"^[A-Za-z][A-Za-z-]+\s+[a-z][a-z-]+$")
PLANT_WORD = re.compile(r"\s+")


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (SLK independent published-data audit)",
        "Accept": "application/octet-stream,*/*",
    })
    with urllib.request.urlopen(req, timeout=45) as stream:
        return stream.read()


def _column_number(ref: str) -> int:
    match = CELL_REF.match(ref)
    if not match:
        raise ValueError(f"invalid Excel cell coordinate: {ref}")
    n = 0
    for ch in match.group(1):
        n = n * 26 + ord(ch) - ord("A") + 1
    return n - 1


def read_xlsx(data: bytes, *, max_rows: int = 40000) -> dict[str, list[list[str]]]:
    if data[:2] != b"PK":
        raise ValueError("supplement is not an XLSX ZIP file")
    result = {}
    with zipfile.ZipFile(BytesIO(data)) as z:
        names = set(z.namelist())
        if "xl/workbook.xml" not in names:
            raise ValueError("XLSX missing xl/workbook.xml")
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            x = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = [
                "".join(node.text or "" for node in item.iter(f"{NS}t"))
                for item in x.findall(f"{NS}si")
            ]
        # These empirical supplementary files have standard worksheets.
        sheetpaths = sorted(
            p for p in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", p)
        )
        for sheet_name in sheetpaths:
            x = ET.fromstring(z.read(sheet_name))
            output = []
            for row in x.iter(f"{NS}row"):
                vals = {}
                for cell in row.findall(f"{NS}c"):
                    col = _column_number(cell.attrib.get("r", "A1"))
                    typ = cell.attrib.get("t", "")
                    if typ == "inlineStr":
                        val = "".join(node.text or "" for node in cell.iter(f"{NS}t"))
                    else:
                        child = cell.find(f"{NS}v")
                        val = "" if child is None else (child.text or "")
                        if typ == "s" and val:
                            val = shared[int(val)]
                    vals[col] = val
                if vals:
                    limit = min(max(vals) + 1, 500)
                    output.append([vals.get(i, "") for i in range(limit)])
                if len(output) >= max_rows:
                    raise ValueError("XLSX unexpectedly exceeds size guard")
            result[sheet_name] = output
    if not result:
        raise ValueError("no worksheets")
    return result


def normalize_species(text: str) -> str | None:
    name = text.strip().replace("_", " ").replace("\u00a0", " ")
    name = PLANT_WORD.sub(" ", name)
    # Exact genus/species only: never expand cf., varieties or fuzzy synonyms.
    if not BINOMIAL.fullmatch(name):
        return None
    a, b = name.split(" ")
    return f"{a.capitalize()} {b.lower()}"


def overlap_report(
    raw_glopl: bytes, supplement: bytes,
) -> dict:
    if _git_blob_sha(raw_glopl) != UPSTREAM_BLOB_SHA:
        raise ValueError("GloPL input changed from locked upstream")
    rows = _csv_rows_from_bytes(raw_glopl)
    all_glopl = {
        normalize_species(x["Species_accepted_names"])
        for x in rows
    } - {None}
    focus = {
        normalize_species(x["Species_accepted_names"])
        for x in rows if _eligible(x)
    } - {None}
    from analyze_glopl_context_variation import _analysis_groups, _collapse
    matched_strata = _analysis_groups(_collapse([
        x for x in rows if _eligible(x)
    ]), "site_year")
    strict = {
        normalize_species(g[0]["Species_accepted_names"])
        for g in matched_strata
    } - {None}

    sheets = read_xlsx(supplement)
    observed = []
    for sheet, matrix in sheets.items():
        hit_columns = Counter()
        matched_species = set()
        focus_matches = set()
        strict_matches = set()
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                taxon = normalize_species(cell)
                if taxon in all_glopl:
                    hit_columns[j] += 1
                    matched_species.add(taxon)
                    if taxon in focus:
                        focus_matches.add(taxon)
                    if taxon in strict:
                        strict_matches.add(taxon)
        # One column, not arbitrary free text, must supply unambiguous species.
        if hit_columns:
            col, count = hit_columns.most_common(1)[0]
        else:
            col, count = -1, 0
        if col >= 0:
            column_species = {
                normalize_species(row[col]) for row in matrix if len(row) > col
            } - {None}
            matched = all_glopl & column_species
            focused = focus & column_species
            strict_overlap = strict & column_species
        else:
            matched = focused = strict_overlap = set()

        observed.append({
            "sheet_path": sheet,
            "rows": len(matrix),
            "top_candidate_species_column_index_0_based": col,
            "top_column_exact_species_hits": count,
            "all_glopl_matched_species": len(matched),
            "fruit_set_protocol_matched_species": len(focused),
            "strict_context_pilot_matched_species": len(strict_overlap),
            "strict_context_species_names": sorted(strict_overlap),
            "headers_first_5_rows_first_25_cols": [
                row[:25] for row in matrix[:5]
            ],
            "species_rows_first_5": [
                row[:25] for row in matrix
                if col >= 0 and len(row) > col
                and normalize_species(row[col]) in all_glopl
            ][:5],
            "species_match_by_column": hit_columns.most_common(8),
        })
    return {
        "GloPL_pinned_source": SOURCE_URL,
        "GloPL_records": len(rows),
        "GloPL_distinct_species": len(all_glopl),
        "GloPL_FS_Sup_flower_distinct_species": len(focus),
        "GloPL_strict_context_distinct_species": len(strict),
        "breeding_source": BREEDING_URL,
        "breeding_doi": BREEDING_DOI,
        "breeding_sha256": hashlib.sha256(supplement).hexdigest(),
        "breeding_byte_count": len(supplement),
        "sheets": observed,
        "claim_ceiling": (
            "Cross-database exact binomial overlap only. No association or "
            "causal inference; use adequate independent species after "
            "taxonomy, trait-column and source-context checks."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--breeding-file", type=Path)
    args = parser.parse_args()
    g = download(SOURCE_URL)
    b = args.breeding_file.read_bytes() if args.breeding_file else download(BREEDING_URL)
    result = overlap_report(g, b)
    text = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
