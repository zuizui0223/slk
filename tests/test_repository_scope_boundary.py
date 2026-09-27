from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_repository_scope_boundary.py"

spec = importlib.util.spec_from_file_location("scope_guard", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def change(line: str):
    return mod.parse_name_status(line)


def test_pedicularis_operational_patterns_are_frozen() -> None:
    assert mod.is_pedicularis_operational(
        "docs/PEDICULARIS_CONTEXT_RECOVERY_V1.md"
    )
    assert mod.is_pedicularis_operational(
        "data/PEDICULARIS_CONTEXT_RECOVERY_FREEZE_TEMPLATE_V1.json"
    )
    assert mod.is_pedicularis_operational(
        "scripts/adjudicate_pedicularis_context_recovery.py"
    )
    assert mod.is_pedicularis_operational(
        "tests/test_pedicularis_context_recovery.py"
    )


def test_flagship_theory_and_boundary_files_remain_editable() -> None:
    assert not mod.is_pedicularis_operational("README.md")
    assert not mod.is_pedicularis_operational(
        "docs/REPOSITORY_SCOPE_BOUNDARY_V1.md"
    )
    assert not mod.is_pedicularis_operational(
        "theory/UNIFIED_THRESHOLD_ATLAS_V1.md"
    )
    assert not mod.is_pedicularis_operational(
        "manuscript/SLK_MANUSCRIPT_AMNAT_V4.md"
    )


def test_delete_of_pedicularis_operational_file_is_allowed_for_migration() -> None:
    violations = mod.scope_violations(
        [change("D\tdocs/PEDICULARIS_CONTEXT_RECOVERY_V1.md")]
    )
    assert violations == []


def test_modification_of_pedicularis_operational_file_is_blocked() -> None:
    violations = mod.scope_violations(
        [change("M\tscripts/adjudicate_pedicularis_context_recovery.py")]
    )
    assert len(violations) == 1


def test_addition_of_pedicularis_operational_file_is_blocked() -> None:
    violations = mod.scope_violations(
        [change("A\tdata/PEDICULARIS_NEW_OPERATION_V1.json")]
    )
    assert len(violations) == 1


def test_rename_of_pedicularis_operational_file_is_blocked() -> None:
    violations = mod.scope_violations(
        [
            change(
                "R100\t"
                "docs/PEDICULARIS_CONTEXT_RECOVERY_V1.md\t"
                "docs/PEDICULARIS_CONTEXT_RECOVERY_V2.md"
            )
        ]
    )
    assert len(violations) == 1


def test_copy_from_pedicularis_operational_file_is_blocked() -> None:
    violations = mod.scope_violations(
        [
            change(
                "C100\t"
                "scripts/adjudicate_pedicularis_context_recovery.py\t"
                "scripts/adjudicate_pedicularis_context_recovery_v2.py"
            )
        ]
    )
    assert len(violations) == 1


def test_unrelated_repository_changes_pass() -> None:
    violations = mod.scope_violations(
        [
            change("M\tREADME.md"),
            change("M\ttheory/UNIFIED_THRESHOLD_ATLAS_V1.md"),
            change("A\tscripts/new_theory_check.py"),
        ]
    )
    assert violations == []
