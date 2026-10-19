#!/usr/bin/env python3
"""Cross-database plant autofertility × pollen limitation: exploratory macro pilot.

Datasets (original primary public releases):
- Bennett et al. 2018, GloPL, Dryad doi:10.5061/dryad.dt437,
  idiv-biodiversity/pollen-limitation-data-descriptor pinned Git commit.
- Razanajatovo et al. 2016, Nat Commun 7:13313, Supplementary Data 1,
  doi:10.1038/ncomms13313.

This is NOT a test of SLK specialization barriers, adaptive maintenance, or
mating-system causation. Exact species matching, one response per species,
permutation checks and bounded sample sizes. Raw sources are not rehosted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import median

from analyze_glopl_context_variation import (
    SOURCE_URL, UPSTREAM_BLOB_SHA, _analysis_groups, _collapse,
    _csv_rows_from_bytes, _eligible, _git_blob_sha,
)
from audit_glopl_breeding_overlap import (
    BREEDING_URL, BREEDING_DOI, download, normalize_species, read_xlsx,
)

EXPECTED_BREEDING_SHA256 = "cb17009ae65c4f6cb2d28b21239714782600d0904effa77c5635249d28e62fc0"
SHEET = "xl/worksheets/sheet2.xml"
TRAITS = (
    "Autofertility_index_FS",
    "Self-compatibility_index_FS",
    "Autofertility_index_SFL",
    "Self-compatibility_index_SFL",
)
MAX_P = 10000


def _numeric(value: object) -> float | None:
    try:
        num = float(str(value))
    except (TypeError, ValueError):
        return None
    return num if math.isfinite(num) else None


def extract_breeding_traits(supplement: bytes) -> dict[str, dict]:
    sheets = read_xlsx(supplement)
    if SHEET not in sheets:
        raise ValueError(f"expected breeding-system worksheet {SHEET} missing")
    matrix = sheets[SHEET]
    header = matrix[0]
    expected = ("Species", "Family", "Data_source", "Annual_Biennial", *TRAITS)
    missing = sorted(set(expected) - set(header))
    if missing:
        raise ValueError(f"missing breeding trait headers: {missing}")
    index = {name: header.index(name) for name in header}
    values: dict[str, list[dict]] = defaultdict(list)
    for row in matrix[1:]:
        if len(row) < len(header):
            row = row + [""]*(len(header)-len(row))
        sp = normalize_species(row[index["Species"]])
        if sp is None:
            continue
        dat = {}
        for field in TRAITS:
            dat[field] = _numeric(row[index[field]])
        life_history = _numeric(row[index["Annual_Biennial"]])
        dat.update({
            "family": row[index["Family"]],
            "source": row[index["Data_source"]],
            "annual_biennial": life_history,
        })
        values[sp].append(dat)

    combined = {}
    for sp, records in values.items():
        d = {"source_count": len(records)}
        for field in TRAITS:
            eligible = [r[field] for r in records if r[field] is not None]
            d[field] = median(eligible) if eligible else None
            d[field+"_source_count"] = len(eligible)
        d["annual_biennial"] = next(
            (r["annual_biennial"] for r in records if r["annual_biennial"] is not None), None
        )
        families = [r["family"] for r in records if r["family"] not in ("", "NA")]
        d["family"] = families[0] if families else None
        d["sources"] = sorted(set(r["source"] for r in records))
        combined[sp] = d
    return combined


def _species_gopl_effects(original_records: list[dict]) -> dict[str, dict]:
    # Restrict to fruit set after supplementing open flowers; median each exact
    # population/year/geographic context, then median context within each
    # literature study, then median study within each species. A species has
    # one weight irrespective of site/year sampling intensity.
    rows = [r for r in original_records if _eligible(r)]
    context = _collapse(rows)
    species_studies: dict[str, dict[tuple[str, str, str], list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in context:
        sp = normalize_species(r["Species_accepted_names"])
        if sp is None:
            continue
        study = (r["Author"], r["Year"], r["DOI"])
        species_studies[sp][study].append(float(r["effect"]))
    effects = {}
    for sp, studies in species_studies.items():
        values = [median(v) for v in studies.values()]
        effects[sp] = {
            "pollen_limitation_lnRR": median(values),
            "independent_literature_studies": len(studies),
            "contexts": sum(map(len, studies.values())),
        }
    return effects


def _rank(values: list[float]) -> list[float]:
    ordered = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0]*len(values)
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and values[ordered[i]] == values[ordered[j]]:
            j += 1
        center = (i+j+1)/2
        for k in ordered[i:j]:
            out[k] = center
        i = j
    return out


def _correlation(x: list[float], y: list[float]) -> float | None:
    n = len(x)
    if n != len(y) or n < 3:
        return None
    mx, my = sum(x)/n, sum(y)/n
    a, b = [v-mx for v in x], [v-my for v in y]
    xx, yy = sum(v*v for v in a), sum(v*v for v in b)
    if xx <= 0 or yy <= 0:
        return None
    return sum(v*w for v,w in zip(a,b))/math.sqrt(xx*yy)


def _spearman(x: list[float], y: list[float]) -> float | None:
    return _correlation(_rank(x), _rank(y))


def _spearman_audit(
    pairs: list[tuple[float, float]], *,
    seed: int, nperm: int = 9999, nbootstrap: int = 1000,
) -> dict:
    n = len(pairs)
    if n < 6:
        return {"species": n, "rho": None, "permutation_p": None,
                "reason": "under six independently matched species"}
    x, y = list(zip(*pairs))
    rho = _spearman(list(x), list(y))
    if rho is None:
        return {"species": n, "rho": None, "permutation_p": None,
                "reason": "zero rank variation"}
    rng = random.Random(seed)
    count = 0
    perm_y = list(y)
    for _ in range(nperm):
        rng.shuffle(perm_y)
        v = _spearman(list(x), perm_y)
        if v is not None and abs(v) >= abs(rho)-1e-12:
            count += 1
    p = (count+1)/(nperm+1)
    boot = []
    for _ in range(nbootstrap):
        picks = [pairs[rng.randrange(n)] for __ in range(n)]
        xx,yy = zip(*picks)
        value = _spearman(list(xx),list(yy))
        if value is not None:
            boot.append(value)
    boot.sort()
    return {
        "species": n,
        "rho": rho,
        "permutation_p_two_sided": p,
        "permutations": nperm,
        "species_bootstrap_rho_95pct": (
            [boot[int(0.025*(len(boot)-1))],boot[int(0.975*(len(boot)-1))]]
            if len(boot) > 30 else None
        ),
        "bootstrap_valid": len(boot),
        "scope": "unadjusted species-level exploratory correlation; phylogeny not modeled",
    }



def _paired_trait_comparison(rows: list[dict]) -> dict:
    """Compare AF and SC *on identical species*, avoiding unequal-sample bias."""
    subset = [
        r for r in rows if r["af_fruit_set"] is not None
        and r["sc_fruit_set"] is not None
    ]
    base = {
        "matched_species": len(subset),
        "matched_families": len({r["family"] for r in subset}),
        "common_subset_af": _spearman_audit([
            (r["af_fruit_set"],r["fruit_set_pollen_limitation_lnRR"])
            for r in subset
        ],seed=3001),
        "common_subset_sc": _spearman_audit([
            (r["sc_fruit_set"],r["fruit_set_pollen_limitation_lnRR"])
            for r in subset
        ],seed=3002),
        "af_sc_rank_association": _spearman_audit([
            (r["af_fruit_set"],r["sc_fruit_set"]) for r in subset
        ],seed=3003),
    }
    if len(subset) >= 6:
        def contrast(values: list[dict]) -> float | None:
            af=_spearman([r["af_fruit_set"] for r in values],
                         [r["fruit_set_pollen_limitation_lnRR"] for r in values])
            sc=_spearman([r["sc_fruit_set"] for r in values],
                         [r["fruit_set_pollen_limitation_lnRR"] for r in values])
            return sc-af if sc is not None and af is not None else None
        delta=contrast(subset)
        rng=random.Random(314159)
        boot=[]
        for _ in range(3000):
            x=[subset[rng.randrange(len(subset))] for i in subset]
            c=contrast(x)
            if c is not None:
                boot.append(c)
        boot.sort()
        base["paired_rho_sc_minus_rho_af"] = delta
        base["paired_bootstrap_95pct"] = (
            [boot[int(.025*(len(boot)-1))],boot[int(.975*(len(boot)-1))]]
            if len(boot)>200 else None
        )
        base["comparison_inference"] = (
            "Paired species bootstrap of rank-correlation contrast; "
            "no causal or independent trait-effect claim."
        )
    return base


def _family_level_correlations(rows: list[dict]) -> dict:
    """Coarse sensitivity only; family-level aggregation is not a phylogeny."""
    by_family=defaultdict(list)
    for r in rows:
        if r["family"] not in (None,"","NA"):
            by_family[r["family"]].append(r)
    out={}
    for key in ("af_fruit_set","sc_fruit_set"):
        pairs=[]
        for records in by_family.values():
            eligible=[r for r in records if r[key] is not None]
            if eligible:
                pairs.append((
                    median(r[key] for r in eligible),
                    median(r["fruit_set_pollen_limitation_lnRR"] for r in eligible),
                ))
        out[key]={
            "families":len(pairs),
            "rho":_spearman([p[0] for p in pairs],[p[1] for p in pairs])
                   if len(pairs)>2 else None,
            "scope":"sensitivity to dominant plant families, not a phylogenetic regression",
        }
    return out


def _life_history_strata(rows: list[dict]) -> dict:
    result={}
    for k,label in ((0,"perennial"),(1,"annual_biennial")):
        cohort=[r for r in rows if r["annual_biennial"]==k]
        result[label]={
            "species":len(cohort),
            "af":_spearman_audit([
                (r["af_fruit_set"],r["fruit_set_pollen_limitation_lnRR"])
                for r in cohort if r["af_fruit_set"] is not None
            ],seed=700+k,nperm=1999,nbootstrap=500),
            "sc":_spearman_audit([
                (r["sc_fruit_set"],r["fruit_set_pollen_limitation_lnRR"])
                for r in cohort if r["sc_fruit_set"] is not None
            ],seed=702+k,nperm=1999,nbootstrap=500),
        }
    return result


def _source_handling_sensitivity(
    pollen: list[dict], breeding: dict[str,dict]
) -> dict:
    variants={
        "exclude_emasculated_yes": [
            r for r in pollen if r.get("Emasculated_treatment","").lower()!="yes"
        ],
        "exclude_zero_count_corrections": [
            r for r in pollen if r.get("Constant_added","").lower()
            not in ("true","t","1")
        ],
        "exclude_abs_effect_gt_3": [
            r for r in pollen
            if _numeric(r["PL_Effect_Size"]) is not None
            and abs(float(r["PL_Effect_Size"])) <= 3.0
        ],
    }
    out={}
    for label,data in variants.items():
        v=_species_gopl_effects(data)
        subset=[]
        for sp in set(v) & set(breeding):
            d=breeding[sp]
            subset.append({
                "pl":v[sp]["pollen_limitation_lnRR"],
                "af":d["Autofertility_index_FS"],
                "sc":d["Self-compatibility_index_FS"],
            })
        vals={}
        for trait in ("af","sc"):
            pairs=[(r[trait],r["pl"]) for r in subset if r[trait] is not None]
            vals[trait]={"n":len(pairs),"spearman":_spearman(
                [r[0] for r in pairs],[r[1] for r in pairs]
            ) if len(pairs)>=3 else None}
        out[label]={"species_any_trait":len(subset),**vals}
    return out


def analyze(raw_glopl: bytes, raw_breeding: bytes) -> tuple[dict, list[dict]]:
    if _git_blob_sha(raw_glopl) != UPSTREAM_BLOB_SHA:
        raise ValueError("GloPL input does not match pinned Git blob")
    pollen = _csv_rows_from_bytes(raw_glopl)
    breeding_sha = hashlib.sha256(raw_breeding).hexdigest()
    if breeding_sha != EXPECTED_BREEDING_SHA256:
        raise ValueError(
            "breeding XLSX source SHA256 drift: "
            f"{breeding_sha} != {EXPECTED_BREEDING_SHA256}"
        )
    breeding = extract_breeding_traits(raw_breeding)
    vals = _species_gopl_effects(pollen)
    strict_groups = _analysis_groups(_collapse([
        r for r in pollen if _eligible(r)
    ]), "site_year")
    strict = {}
    for group in strict_groups:
        sp = normalize_species(group[0]["Species_accepted_names"])
        if sp is None:
            continue
        effects = [float(r["effect"]) for r in group]
        d = max(effects)-min(effects)
        if sp not in strict or d > strict[sp]["range_logRR"]:
            strict[sp] = {
                "range_logRR": d,
                "contexts": len(group),
            }
    all_glopl = set()
    for row in pollen:
        n = normalize_species(row["Species_accepted_names"])
        if n is not None:
            all_glopl.add(n)
    merged = []
    for species in sorted(set(vals) & set(breeding)):
        p,t = vals[species],breeding[species]
        merged.append({
            "species": species,
            "family": t["family"],
            "fruit_set_pollen_limitation_lnRR": p["pollen_limitation_lnRR"],
            "gopl_studies": p["independent_literature_studies"],
            "gopl_contexts": p["contexts"],
            "af_fruit_set": t["Autofertility_index_FS"],
            "sc_fruit_set": t["Self-compatibility_index_FS"],
            "af_seed_flower": t["Autofertility_index_SFL"],
            "sc_seed_flower": t["Self-compatibility_index_SFL"],
            "annual_biennial": t["annual_biennial"],
            "breeding_source_count": t["source_count"],
            "eligible_strict_site_year": species in strict,
            "strict_within_species_effect_range": (
                strict.get(species, {}).get("range_logRR")
            ),
        })
    all_breeding = set(breeding)
    correlation = {}
    for field in ("af_fruit_set", "sc_fruit_set", "af_seed_flower", "sc_seed_flower"):
        pairs = [(r[field],r["fruit_set_pollen_limitation_lnRR"]) for r in merged
                 if r[field] is not None]
        correlation[field] = _spearman_audit(pairs,seed=981+len(field))
        correlation[field]["trait_observed"] = len(pairs)
    both = [r for r in merged if r["af_fruit_set"] is not None and
            r["sc_fruit_set"] is not None]
    strict_pairs = [r for r in merged if r["eligible_strict_site_year"]]
    strict_af = [(r["af_fruit_set"],r["strict_within_species_effect_range"])
                 for r in strict_pairs if r["af_fruit_set"] is not None]
    strict_sc = [(r["sc_fruit_set"],r["strict_within_species_effect_range"])
                 for r in strict_pairs if r["sc_fruit_set"] is not None]
    report = {
        "GloPL_records": len(pollen),
        "GloPL_all_binomial_species": len(all_glopl),
        "GloPL_FS_Sup_flower_species": len(vals),
        "breeding_species": len(breeding),
        "all_glopl_breeding_overlap": len(all_glopl & all_breeding),
        "fruit_set_study_protocol_exact_species_overlap": len(merged),
        "species_with_both_SC_FS_and_AF_FS": len(both),
        "matched_strict_context_species_overlap": len(strict_pairs),
        "trait_coverage": {
            name: sum(r[name] is not None for r in merged)
            for name in ("af_fruit_set","sc_fruit_set","af_seed_flower","sc_seed_flower")
        },
        "species_binned_source_count": {
            ">1_breeding_study": sum(r["breeding_source_count"]>1 for r in merged),
            ">1_GloPL_study": sum(r["gopl_studies"]>1 for r in merged),
        },
        "species_level_rank_correlations": correlation,
        "paired_SC_AF_comparison": _paired_trait_comparison(merged),
        "family_aggregation_sensitivity": _family_level_correlations(merged),
        "life_history_strata": _life_history_strata(merged),
        "source_processing_sensitivities": _source_handling_sensitivity(
            pollen, breeding
        ),
        "strict_context_association": {
            "af_vs_within_species_range":
                _spearman_audit(strict_af,seed=418),
            "sc_vs_within_species_range":
                _spearman_audit(strict_sc,seed=419),
        },
        "full_dataset_sha256": {
            "GloPL": hashlib.sha256(raw_glopl).hexdigest(),
            "breeding": hashlib.sha256(raw_breeding).hexdigest(),
        },
        "datasets": {
            "pollen_limitation": SOURCE_URL,
            "breeding": BREEDING_URL,
            "breeding_doi": BREEDING_DOI,
        },
        "analysis_limitations": [
            "Species names matched exactly; taxonomic synonyms were not harmonized.",
            "Each species contributes one outcome; source contexts collapsed before study and species aggregation.",
            "Breeding traits may derive from different year, site or phenotype than GloPL outcomes.",
            "Global literature sampling is non-random; no phylogenetic control in this screening.",
            "Pollen limitation and autofertility may be jointly affected by life history and ecology.",
            "Within-species range increases with number of measured contexts; not a stable trait.",
            "Positive or negative correlations cannot confirm SLK structural specialization or its three barriers.",
        ],
    }
    return report, merged


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path)
    p.add_argument("--species-csv",type=Path)
    p.add_argument("--breeding-file",type=Path)
    args=p.parse_args()
    source=download(SOURCE_URL)
    breeding=(args.breeding_file.read_bytes() if args.breeding_file else
              download(BREEDING_URL))
    result,rows=analyze(source,breeding)
    text=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(text+"\n",encoding="utf-8")
    print(text)
    if args.species_csv:
        import csv
        args.species_csv.parent.mkdir(parents=True,exist_ok=True)
        with args.species_csv.open("w",newline="",encoding="utf-8") as fh:
            writer=csv.DictWriter(fh,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
