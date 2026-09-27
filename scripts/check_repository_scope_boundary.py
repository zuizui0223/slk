from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass

OPERATIONAL_PATTERNS = (
    re.compile(r"^docs/PEDICULARIS_"),
    re.compile(r"^data/PEDICULARIS_"),
    re.compile(r"^scripts/[^/]*pedicularis[^/]*\.py$", re.IGNORECASE),
    re.compile(r"^tests/test_pedicularis_[^/]*\.py$", re.IGNORECASE),
)


@dataclass(frozen=True)
class Change:
    status: str
    old_path: str | None
    new_path: str


def is_pedicularis_operational(path: str) -> bool:
    return any(pattern.search(path) for pattern in OPERATIONAL_PATTERNS)


def parse_name_status(line: str) -> Change:
    parts = line.rstrip("\n").split("\t")
    if not parts or not parts[0]:
        raise ValueError("empty git diff --name-status line")
    status = parts[0]
    code = status[0]
    if code in {"R", "C"}:
        if len(parts) != 3:
            raise ValueError(f"rename/copy status requires two paths: {line!r}")
        return Change(status=status, old_path=parts[1], new_path=parts[2])
    if len(parts) != 2:
        raise ValueError(f"status requires one path: {line!r}")
    return Change(status=status, old_path=None, new_path=parts[1])


def scope_violations(changes: list[Change]) -> list[str]:
    violations: list[str] = []
    for change in changes:
        code = change.status[0]
        touched = [change.new_path]
        if change.old_path is not None:
            touched.append(change.old_path)

        if not any(is_pedicularis_operational(path) for path in touched):
            continue

        # Deletion from SLK is the intended migration direction.
        if code == "D":
            continue

        violations.append(
            f"{change.status}\t"
            + ("\t".join(touched))
        )
    return violations


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Enforce the SLK flagship boundary: Pedicularis-specific operational "
            "files are frozen in place and may only be deleted during migration."
        )
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read git diff --name-status lines from stdin.",
    )
    args = parser.parse_args()
    if not args.stdin:
        parser.error("--stdin is required")

    lines = [line for line in sys.stdin if line.strip()]
    changes = [parse_name_status(line) for line in lines]
    violations = scope_violations(changes)
    if violations:
        print(
            "SLK repository scope violation: Pedicularis-specific operational "
            "files are frozen in the flagship repository.",
            file=sys.stderr,
        )
        print(
            "Move operational development to the Pedicularis empirical companion. "
            "Deletion from SLK during migration is allowed; additions, edits, copies "
            "and renames are not.",
            file=sys.stderr,
        )
        for item in violations:
            print(f"  {item}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "repository scope boundary: PASS "
        "(no new/modified Pedicularis operational surface)"
    )


if __name__ == "__main__":
    main()
