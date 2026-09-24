from __future__ import annotations

import hashlib
import json
from typing import Iterable


FIREWALL_SCHEMA = "SLK_PEDICULARIS_PHYSICAL_PLANT_FIREWALL_V1"


def _need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def _filled(value: object, label: str) -> str:
    out = str(value).strip()
    _need(bool(out) and "REQUIRED_BEFORE_USE" not in out, f"unfrozen {label}")
    return out


def canonical_tag_hash(tags: Iterable[str]) -> str:
    cleaned = sorted({_filled(tag, "physical plant tag") for tag in tags})
    payload = json.dumps(cleaned, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_physical_plant_mapping(
    rows: list[dict[str, str]],
    *,
    assignment_key: str = "plant_id",
    physical_tag_key: str = "physical_plant_tag",
) -> dict[str, str]:
    """Require a one-to-one assignment-ID <-> physical-plant-tag mapping.

    Multiple rows may represent multiple flowers or treatments on the same plant,
    but one physical plant may not be hidden behind two assignment IDs and one
    assignment ID may not switch physical plants across rows.
    """
    _need(bool(rows), "physical plant mapping requires rows")

    assignment_to_tag: dict[str, str] = {}
    tag_to_assignment: dict[str, str] = {}

    for row in rows:
        assignment = _filled(
            row.get(assignment_key),
            f"{assignment_key}",
        )
        tag = _filled(
            row.get(physical_tag_key),
            f"{physical_tag_key}/{assignment}",
        )

        prior_tag = assignment_to_tag.get(assignment)
        if prior_tag is not None:
            _need(
                prior_tag == tag,
                f"assignment plant id maps to multiple physical tags: {assignment}",
            )
        assignment_to_tag[assignment] = tag

        prior_assignment = tag_to_assignment.get(tag)
        if prior_assignment is not None:
            _need(
                prior_assignment == assignment,
                "physical plant tag reused across assignment IDs: "
                f"{tag}/{prior_assignment}/{assignment}",
            )
        tag_to_assignment[tag] = assignment

    return assignment_to_tag


def validate_firewall_block(block: dict) -> dict:
    _need(
        block.get("schema_version") == FIREWALL_SCHEMA,
        "wrong physical plant firewall schema",
    )
    _need(
        block.get("require_nonempty_physical_plant_tag") is True,
        "physical plant tag requirement disabled",
    )
    _need(
        block.get("frozen_before_outcomes") is True,
        "physical plant firewall not frozen before outcomes",
    )

    forbidden_raw = block.get("prior_physical_plant_tags_forbidden")
    _need(
        isinstance(forbidden_raw, list),
        "prior physical plant tags must be a list",
    )
    forbidden = [_filled(x, "prior physical plant tag") for x in forbidden_raw]
    _need(
        len(forbidden) == len(set(forbidden)),
        "duplicate prior physical plant tag in firewall",
    )

    references = block.get("prior_tag_source_references")
    _need(
        isinstance(references, list) and references,
        "prior physical plant tag source references missing",
    )
    clean_refs = [_filled(x, "prior tag source reference") for x in references]

    expected_hash = _filled(
        block.get("prior_tag_set_sha256"),
        "prior_tag_set_sha256",
    )
    observed_hash = canonical_tag_hash(forbidden)
    _need(
        observed_hash == expected_hash,
        "prior physical plant tag hash mismatch",
    )

    return {
        "forbidden_tags": set(forbidden),
        "forbidden_tag_count": len(forbidden),
        "prior_tag_set_sha256": observed_hash,
        "source_references": clean_refs,
    }


def validate_current_against_forbidden(
    rows: list[dict[str, str]],
    firewall: dict,
) -> dict:
    mapping = validate_physical_plant_mapping(rows)
    current_tags = set(mapping.values())
    overlap = sorted(current_tags & firewall["forbidden_tags"])
    _need(
        not overlap,
        "current cohort reuses prior physical plants: " + ",".join(overlap),
    )
    return {
        "assignment_to_physical_tag": mapping,
        "current_physical_plant_count": len(current_tags),
        "current_tag_set_sha256": canonical_tag_hash(current_tags),
        "forbidden_tag_count": firewall["forbidden_tag_count"],
        "prior_tag_set_sha256": firewall["prior_tag_set_sha256"],
        "overlap_count": 0,
    }
