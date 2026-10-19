"""GloPL ecological pilot: synthetic tests only, no network access required."""

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.analyze_glopl_context_variation import (
    REQUIRED_COLUMNS,
    _csv_rows_from_bytes,
    _git_blob_sha,
    _rng_xorshift,
    analyze,
)


def record(species, value, *, population="1", year="2000",
           latitude="40", longitude="-70", mode="Sup", added="FALSE",
           included="yes", response="FS", level="flower"):
    item = {name: "NA" for name in REQUIRED_COLUMNS}
    item.update({
        "Species_accepted_names": species,
        "Family": "Exampleaceae",
        "Author": "Synthetic",
        "Year": "2020",
        "DOI": "10.0/example",
        "PL_Effect_Size": str(value),
        "PL_Effect_Size_Type1": response,
        "PL_Effect_Size_Type2": mode,
        "Level_of_Supplementation": level,
        "Included_Bennett_et_al_meta_analysis": included,
        "Latitude": latitude,
        "Longitude": longitude,
        "population": population,
        "year_of_study": year,
        "Constant_added": added,
    })
    return item


def fixture():
    return [
        record("Example_A", 0.1),
        record("Example_A", 0.3),  # same context; median -> 0.2
        record("Example_A", 0.5, population="2", longitude="-71"),
        record("Example_A", 1.0, year="2001"),
        record("Example_B", 0.2, year="2001", population="1"),
        record("Example_B", 0.9, year="2001", population="2", longitude="-72"),
        record("Example_B", 9.9, mode="Bagout"),  # incompatible treatment
        record("Example_B", 8.8, response="SPFR"),  # incompatible outcome
        record("Example_B", 7.7, included="no"),
        record("Example_C", 3.0),  # no matched replication
    ]


def test_replicated_species_stratify_contexts_without_pseudoreplication():
    data, groups = analyze(fixture())
    assert data["raw_experiment_rows"] == 10
    assert data["filtered_original_rows"] == 7
    assert data["filtered_species"] == 3
    assert data["collapsed_contexts"] == 6
    main = data["primary"]
    assert main["groups"] == 2
    assert main["species"] == 2
    assert main["contexts"] == 5
    assert main["range_at_least_0_5"] == 2
    assert main["point_estimate_crosses_zero"] == 0
    values = sorted(round(x["range_log_response_ratio"], 9) for x in groups)
    assert values == [0.7, 0.8]
    assert data["same_year_different_sites"]["groups"] == 2
    assert data["same_site_different_years"]["groups"] == 1
    assert data["groups_with_three_or_more_contexts"]["groups"] == 1
    assert data["no_zero_cell_correction"]["groups"] == 2


def test_context_bootstrap_is_reproducible_and_yields_bounded_interval():
    receipt1, _ = analyze(fixture())
    receipt2, _ = analyze(fixture())
    assert receipt1["species_cluster_bootstrap"] == receipt2["species_cluster_bootstrap"]
    ci = receipt1["species_cluster_bootstrap"]["median_effect_range"]
    assert 0.7 <= ci["p025"] <= ci["estimate"] <= ci["p975"] <= 0.8
    assert len({next(_rng_xorshift(137)) for _ in range(3)}) == 1


def test_csv_reader_handles_quotes_and_blob_hash_has_git_header():
    rows = fixture()
    buf = __import__("io").StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(REQUIRED_COLUMNS))
    writer.writeheader()
    writer.writerows(rows)
    raw = buf.getvalue().encode("utf-8")
    result = _csv_rows_from_bytes(raw)
    assert len(result) == len(rows)
    assert result[0]["Species_accepted_names"] == "Example_A"
    assert len(_git_blob_sha(raw)) == 40


def test_na_year_is_not_interpreted_as_temporal_replication():
    rows = [
        record("A", 0.0, year="NA"),
        record("A", 1.0, year="2001"),
    ]
    out, _ = analyze(rows)
    assert out["primary"]["groups"] == 0
    assert out["same_site_different_years"]["groups"] == 0
