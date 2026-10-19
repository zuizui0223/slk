#!/usr/bin/env python3
"""Exploratory GloPL within-species ecological-context analysis for SLK.

This is an empirical *component* audit, not a test of the SLK three gates
or of evolutionary maintenance of heteranthery. Standard library only.

Source: Bennett et al. 2018, GloPL, Dryad doi:10.5061/dryad.dt437.
Public code release: idiv-biodiversity/pollen-limitation-data-descriptor.
The upstream raw CSV is fetched from a pinned commit; raw source data are
not vendored into SLK. See docs/SLK_GLOPL_CONTEXT_PILOT_V1.md.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path
from statistics import median

UPSTREAM_COMMIT = "abbe193770981b2c61713e75a0f01e004bdded8e"
UPSTREAM_BLOB_SHA = "ef3fbc9ac144da55a5f5ff936bbab734711d53d0"
SOURCE_URL = (
    "https://raw.githubusercontent.com/idiv-biodiversity/"
    "pollen-limitation-data-descriptor/"
    f"{UPSTREAM_COMMIT}/Output/GloPL.csv"
)
SOURCE_DOI = "10.5061/dryad.dt437"

REQUIRED_COLUMNS = (
    "Species_accepted_names", "Author", "Year", "DOI", "Family",
    "PL_Effect_Size", "PL_Effect_Size_Type1", "PL_Effect_Size_Type2",
    "Level_of_Supplementation", "Included_Bennett_et_al_meta_analysis",
    "Latitude", "Longitude", "population", "year_of_study", "Constant_added",
)
VALID_YEAR = re.compile(r"^(?:19|20)\d{2}$")
RANGE_LIMIT = 0.5


def _csv_rows_from_bytes(data: bytes) -> list[dict[str, str]]:
    # The canonical 2018 Git blob contains Latin-1 non-UTF8 bytes (e.g.
    # Portuguese author/treatment labels). Check raw bytes *before* decoding.
    # Taxon keys, categorical protocol flags and numeric response data are
    # ASCII; this fallback leaves the analytical columns unchanged.
    try:
        content = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        content = data.decode("latin-1")
    reader = csv.DictReader(io.StringIO(content))
    missing = sorted(set(REQUIRED_COLUMNS) - set(reader.fieldnames or ()))
    if missing:
        raise ValueError(f"missing GloPL columns: {missing}")
    result = list(reader)
    if any(None in row for row in result):
        raise ValueError("CSV has malformed/overflow columns")
    return result


def _source_bytes(*, input_path: Path | None, download: bool) -> bytes:
    if (input_path is None) == (not download):
        raise ValueError("supply exactly one of --input or --download")
    if input_path is not None:
        return input_path.read_bytes()
    req = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": "SLK-ecological-context-pilot/1"}
    )
    with urllib.request.urlopen(req, timeout=45) as handle:
        return handle.read()


def _git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _study_key(r: dict[str, str]) -> str:
    # Include all three because some old publications have no DOI.
    return "|".join((r["Author"], r["Year"], r["DOI"]))


def _stratum_key(r: dict[str, str]) -> tuple[str, ...]:
    return (
        r["Species_accepted_names"], _study_key(r),
        r["PL_Effect_Size_Type1"], r["PL_Effect_Size_Type2"],
        r["Level_of_Supplementation"],
    )


def _context_key(r: dict[str, str]) -> tuple[str, ...]:
    return (
        *_stratum_key(r), r["population"], r["year_of_study"],
        r["Latitude"], r["Longitude"],
    )


def _valid_year(r: dict[str, str]) -> bool:
    return bool(VALID_YEAR.fullmatch(r["year_of_study"]))


def _geo_key(r: dict[str, str]) -> tuple[str, str]:
    return r["Latitude"], r["Longitude"]


def _eligible(r: dict[str, str]) -> bool:
    return (
        r["Included_Bennett_et_al_meta_analysis"] == "yes"
        and r["PL_Effect_Size_Type1"] == "FS"
        and r["PL_Effect_Size_Type2"] == "Sup"
        and r["Level_of_Supplementation"] == "flower"
        and bool(r["Species_accepted_names"])
        and math.isfinite(_parse_float(r["PL_Effect_Size"]))
    )


def _parse_float(text: str) -> float:
    try:
        return float(text)
    except (ValueError, TypeError):
        return float("nan")


def _collapse(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """One median effect per exact species/study/population/year/geosite."""
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        grouped[_context_key(r)].append(r)
    result = []
    for members in grouped.values():
        r = dict(members[0])
        r["effect"] = median(float(x["PL_Effect_Size"]) for x in members)
        r["n_original_records"] = len(members)
        result.append(r)
    return result


def _has_site_or_year_contrast(
    group: list[dict[str, object]],
) -> bool:
    different_geos = len({_geo_key(r) for r in group}) >= 2
    different_known_years = len(
        {r["year_of_study"] for r in group if _valid_year(r)}
    ) >= 2
    return different_geos or different_known_years


def _analysis_groups(
    contexts: list[dict[str, object]],
    kind: str,
) -> list[list[dict[str, object]]]:
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for r in contexts:
        if kind == "site_year":
            key = _stratum_key(r)
        elif kind == "geo_same_year":
            if not _valid_year(r):
                continue
            key = (*_stratum_key(r), r["year_of_study"])
        elif kind == "same_site_years":
            if not _valid_year(r):
                continue
            key = (*_stratum_key(r), r["population"], *_geo_key(r))
        else:
            raise ValueError(f"unknown group: {kind}")
        grouped[key].append(r)
    result = []
    for group in grouped.values():
        if len(group) < 2:
            continue
        if kind == "site_year" and not _has_site_or_year_contrast(group):
            continue
        if kind == "geo_same_year" and len({_geo_key(r) for r in group}) < 2:
            continue
        if kind == "same_site_years" and len(
            {r["year_of_study"] for r in group}
        ) < 2:
            continue
        result.append(group)
    return result


def _summarize_groups(
    groups: list[list[dict[str, object]]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    summary_rows = []
    for g in groups:
        values = [float(x["effect"]) for x in g]
        lo, hi = min(values), max(values)
        summary_rows.append(
            {
                "species": g[0]["Species_accepted_names"],
                "author": g[0]["Author"],
                "publication_year": g[0]["Year"],
                "doi": g[0]["DOI"],
                "contexts": len(g),
                "sites": len({_geo_key(x) for x in g}),
                "known_years": len(
                    {x["year_of_study"] for x in g if _valid_year(x)}
                ),
                "min_effect": lo,
                "max_effect": hi,
                "range_log_response_ratio": hi - lo,
                "spans_zero": lo < 0 < hi,
            }
        )
    n = len(summary_rows)
    ranges = [r["range_log_response_ratio"] for r in summary_rows]
    stats = {
        "groups": n,
        "species": len({r["species"] for r in summary_rows}),
        "contexts": sum(r["contexts"] for r in summary_rows),
        "median_effect_range": median(ranges) if ranges else None,
        "mean_effect_range": sum(ranges)/n if n else None,
        "range_at_least_0_5": sum(x >= RANGE_LIMIT for x in ranges),
        "range_at_least_ln_2": sum(x >= math.log(2) for x in ranges),
        "point_estimate_crosses_zero": sum(r["spans_zero"] for r in summary_rows),
        "groups_with_at_least_three_contexts": sum(
            r["contexts"] >= 3 for r in summary_rows
        ),
    }
    return stats, summary_rows


def _rng_xorshift(seed: int):
    """Match the explicitly recorded seeded audit resampling procedure."""
    x = seed & 0xffffffff
    while True:
        x ^= (x << 13) & 0xffffffff
        x ^= (x >> 17)
        x ^= (x << 5) & 0xffffffff
        x &= 0xffffffff
        yield x / 4294967296


def _bootstrap(
    summaries: list[dict[str, object]],
    *, nboot: int = 3000, seed: int = 137
) -> dict[str, object]:
    by_species = defaultdict(list)
    for row in summaries:
        by_species[row["species"]].append(row)
    species = list(by_species)
    if not species:
        return {
            "unit": "species-cluster resampling; no eligible repeated groups",
            "seed": seed,
            "iterations": 0,
            "fraction_ge_0_5": None,
            "median_effect_range": None,
        }
    rng = _rng_xorshift(seed)
    values = []
    medians = []
    for _ in range(nboot):
        sampled = []
        for __ in species:
            sp = species[int(next(rng)*len(species))]
            sampled.extend(by_species[sp])
        ranges = [r["range_log_response_ratio"] for r in sampled]
        values.append(sum(x >= RANGE_LIMIT for x in ranges)/len(ranges))
        medians.append(median(ranges))
    values.sort()
    medians.sort()

    def empirical_quantile(xs: list[float], p: float) -> float:
        return xs[math.floor((len(xs)-1)*p)]

    return {
        "unit": "species-cluster resampling; descriptive not a causal CI",
        "seed": seed,
        "iterations": nboot,
        "fraction_ge_0_5": {
            "estimate": sum(
                r["range_log_response_ratio"] >= RANGE_LIMIT for r in summaries
            )/len(summaries),
            "p025": empirical_quantile(values, 0.025),
            "p975": empirical_quantile(values, 0.975),
        },
        "median_effect_range": {
            "estimate": median(r["range_log_response_ratio"] for r in summaries),
            "p025": empirical_quantile(medians, 0.025),
            "p975": empirical_quantile(medians, 0.975),
        },
    }


def analyze(raw_records: list[dict[str, str]]) -> tuple[dict, list[dict]]:
    kept = [r for r in raw_records if _eligible(r)]
    contexts = _collapse(kept)
    main_groups = _analysis_groups(contexts, "site_year")
    main, main_rows = _summarize_groups(main_groups)
    geo, _ = _summarize_groups(_analysis_groups(contexts, "geo_same_year"))
    temporal, _ = _summarize_groups(_analysis_groups(contexts, "same_site_years"))
    noadded = _collapse([
        r for r in kept if r["Constant_added"].upper() not in
        {"TRUE", "T", "1"}
    ])
    noadded_summary, _ = _summarize_groups(
        _analysis_groups(noadded, "site_year")
    )
    nonextreme = _collapse([
        r for r in kept if abs(float(r["PL_Effect_Size"])) <= 3.0
    ])
    nonextreme_summary, _ = _summarize_groups(
        _analysis_groups(nonextreme, "site_year")
    )
    triple, _ = _summarize_groups(
        [g for g in main_groups if len(g) >= 3]
    )
    output = {
        "source_doi": SOURCE_DOI,
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_blob_sha": UPSTREAM_BLOB_SHA,
        "raw_experiment_rows": len(raw_records),
        "filter": {
            "included": "yes",
            "response": "FS (fruit-set)",
            "comparison": "Sup (pollen supplementation)",
            "supplementation_level": "flower",
            "study_key": ["Author", "Year", "DOI"],
            "context_key": ["population", "year_of_study", "Latitude", "Longitude"],
            "duplicate_collapse": "median within identical context",
            "replicated_stratum_requirement": ">=2 contexts with >=2 sites or >=2 valid 4-digit years",
            "interpretation": "descriptive variation in pollen limitation; not SLK gate or stable morphology",
        },
        "filtered_original_rows": len(kept),
        "filtered_species": len({r["Species_accepted_names"] for r in kept}),
        "collapsed_contexts": len(contexts),
        "primary": main,
        "same_year_different_sites": geo,
        "same_site_different_years": temporal,
        "no_zero_cell_correction": noadded_summary,
        "exclude_effect_abs_gt_3": nonextreme_summary,
        "groups_with_three_or_more_contexts": triple,
        "species_cluster_bootstrap": _bootstrap(main_rows),
    }
    return output, main_rows


def assert_locked_pilot(r: dict) -> None:
    """Assert public pilot's reproducible counts; fail loudly on source drift."""
    expected = (
        ("raw_experiment_rows", 2969),
        ("filtered_original_rows", 522),
        ("filtered_species", 249),
        ("collapsed_contexts", 451),
    )
    for field, value in expected:
        assert r[field] == value, (field, r[field], value)
    for field, value in (
        ("groups", 58), ("species", 53), ("contexts", 227),
        ("range_at_least_0_5", 31),
        ("range_at_least_ln_2", 21),
        ("point_estimate_crosses_zero", 17),
    ):
        assert r["primary"][field] == value, (field, r["primary"][field], value)
    assert abs(r["primary"]["median_effect_range"] - 0.529741995928767) < 1e-11
    assert r["same_year_different_sites"]["groups"] == 19
    assert r["same_site_different_years"]["groups"] == 37
    assert r["no_zero_cell_correction"]["groups"] == 58
    assert r["exclude_effect_abs_gt_3"]["groups"] == 56


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    inp = parser.add_mutually_exclusive_group(required=True)
    inp.add_argument("--input", type=Path, help="local upstream GloPL.csv")
    inp.add_argument("--download", action="store_true", help="fetch pinned GitHub GloPL.csv")
    parser.add_argument("--out", type=Path, help="write JSON analysis receipt")
    parser.add_argument("--groups", type=Path, help="write 58 source-coded matched-group summaries")
    parser.add_argument("--assert-pilot", action="store_true",
                        help="assert locked source/version results")
    args = parser.parse_args()

    b = _source_bytes(input_path=args.input, download=args.download)
    sha = _git_blob_sha(b)
    if sha != UPSTREAM_BLOB_SHA:
        raise ValueError(f"GloPL source blob drift: {sha} != {UPSTREAM_BLOB_SHA}")
    output, groups = analyze(_csv_rows_from_bytes(b))
    if args.assert_pilot:
        assert_locked_pilot(output)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2))

    if args.groups:
        args.groups.parent.mkdir(parents=True, exist_ok=True)
        with args.groups.open("w", encoding="utf-8", newline="") as file:
            fields = [
                "species", "author", "publication_year", "doi", "contexts",
                "sites", "known_years", "min_effect", "max_effect",
                "range_log_response_ratio", "spans_zero",
            ]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(groups)


if __name__ == "__main__":
    main()
