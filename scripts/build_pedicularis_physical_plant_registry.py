from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

try:
    from scripts.pedicularis_physical_units import (
        FIREWALL_SCHEMA,
        FIREWALL_SCHEMA,
        canonical_tag_hash,
        validate_firewall_block,
        validate_physical_plant_mapping,
    )
except ImportError:
    from pedicularis_physical_units import (
        canonical_tag_hash,
        validate_firewall_block,
        validate_physical_plant_mapping,
    )


REGISTRY_SCHEMA = "SLK_PEDICULARIS_PHYSICAL_PLANT_REGISTRY_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _resolve_prior_firewall(payload: dict) -> dict:
    if payload.get("schema_version") == FIREWALL_SCHEMA:
        return payload
    direct = payload.get("next_stage_firewall_block")
    if isinstance(direct, dict):
        return direct
    nested = payload.get("physical_unit_firewall")
    if isinstance(nested, dict):
        block = nested.get("next_stage_firewall_block")
        if isinstance(block, dict):
            return block
    raise ValueError("could not resolve prior physical-unit firewall block")


def build_registry(
    cohorts: dict[str, list[dict[str, str]]],
    *,
    context_id: str,
    population_id: str,
    season_id: str,
    prior_firewall: dict | None = None,
) -> dict:
    _need(bool(cohorts), "physical plant registry requires cohorts")
    _need(bool(context_id and population_id and season_id), "registry context required")

    cohort_receipts: dict[str, dict] = {}
    seen_tags: dict[str, str] = {}
    overlaps: list[dict[str, str]] = []

    prior = (
        validate_firewall_block(_resolve_prior_firewall(prior_firewall))
        if prior_firewall
        else None
    )
    prior_tags = set(prior["forbidden_tags"]) if prior else set()

    for cohort_id in sorted(cohorts):
        rows = cohorts[cohort_id]
        _need(bool(rows), f"empty physical plant cohort: {cohort_id}")

        for key, expected in (
            ("context_id", context_id),
            ("population_id", population_id),
            ("season_id", season_id),
        ):
            values = {
                str(row.get(key, "")).strip() for row in rows
            }
            _need(
                values == {expected},
                f"physical plant registry context mismatch: {cohort_id}/{key}",
            )

        mapping = validate_physical_plant_mapping(rows)
        tags = sorted(set(mapping.values()))
        forbidden_overlap = sorted(set(tags) & prior_tags)
        _need(
            not forbidden_overlap,
            "physical plant reuse detected against prior firewall: "
            + ",".join(forbidden_overlap),
        )
        for tag in tags:
            prior = seen_tags.get(tag)
            if prior is not None:
                overlaps.append(
                    {
                        "physical_plant_tag": tag,
                        "first_cohort": prior,
                        "second_cohort": cohort_id,
                    }
                )
            else:
                seen_tags[tag] = cohort_id
        cohort_receipts[cohort_id] = {
            "context_id": context_id,
            "population_id": population_id,
            "season_id": season_id,
            "assignment_plant_count": len(mapping),
            "physical_plant_count": len(tags),
            "tag_set_sha256": canonical_tag_hash(tags),
            "physical_plant_tags": tags,
        }

    _need(
        not overlaps,
        "physical plant reuse detected across cohorts: "
        + ";".join(
            f"{x['physical_plant_tag']}:{x['first_cohort']}->{x['second_cohort']}"
            for x in overlaps
        ),
    )

    current_tags = sorted(seen_tags)
    all_tags = sorted(prior_tags | set(current_tags))
    prior_refs = list(prior["source_references"]) if prior else []
    return {
        "schema_version": REGISTRY_SCHEMA,
        "status": "PHYSICAL_PLANT_COHORTS_VALIDATED_DISJOINT",
        "context": {
            "system": "Pedicularis rex",
            "context_id": context_id,
            "population_id": population_id,
            "season_id": season_id,
        },
        "cohorts": cohort_receipts,
        "current_physical_plant_tags": current_tags,
        "current_tag_set_sha256": canonical_tag_hash(current_tags),
        "prior_firewall_tag_count": len(prior_tags),
        "all_prior_physical_plant_tags": all_tags,
        "all_prior_tag_set_sha256": canonical_tag_hash(all_tags),
        "overlap_count": 0,
        "next_stage_firewall_block": {
            "schema_version": "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1",
            "require_nonempty_physical_plant_tag": True,
            "prior_physical_plant_tags_forbidden": all_tags,
            "prior_tag_source_references": (
                prior_refs
                + ["SLK_PEDICULARIS_PHYSICAL_PLANT_REGISTRY_V1"]
            ),
            "prior_tag_set_sha256": canonical_tag_hash(all_tags),
            "frozen_before_outcomes": True,
        },
        "claim_ceiling": "PHYSICAL_UNIT_IDENTITY_AND_DISJOINTNESS_ONLY_NO_BIOLOGICAL_RESULT",
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a cross-cohort Pedicularis physical-plant registry"
    )
    parser.add_argument("--context-id", required=True)
    parser.add_argument("--population-id", required=True)
    parser.add_argument("--season-id", required=True)
    parser.add_argument(
        "--cohort",
        action="append",
        required=True,
        help="COHORT_ID=CSV_PATH; may be repeated",
    )
    parser.add_argument(
        "--prior-firewall-json",
        type=Path,
        help="Optional previously frozen physical-unit firewall to extend",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cohorts: dict[str, list[dict[str, str]]] = {}
    for item in args.cohort:
        if "=" not in item:
            raise ValueError("--cohort must be COHORT_ID=CSV_PATH")
        cohort_id, raw_path = item.split("=", 1)
        cohort_id = cohort_id.strip()
        if not cohort_id or cohort_id in cohorts:
            raise ValueError("cohort ids must be non-empty and unique")
        cohorts[cohort_id] = _read_csv(Path(raw_path))

    prior_firewall = (
        json.loads(args.prior_firewall_json.read_text(encoding="utf-8"))
        if args.prior_firewall_json
        else None
    )
    result = build_registry(
        cohorts,
        context_id=args.context_id,
        population_id=args.population_id,
        season_id=args.season_id,
        prior_firewall=prior_firewall,
    )
    text_out = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text_out, encoding="utf-8")
    else:
        print(text_out, end="")


if __name__ == "__main__":
    main()
