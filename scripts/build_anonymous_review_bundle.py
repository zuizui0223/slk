from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

try:
    from scripts.verify_amnat_claims import verify
except ImportError:  # direct execution via `python scripts/...`
    from verify_amnat_claims import verify

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "submission" / "amnat_review" / "generated" / "reviewer_bundle"

FILES = {
    "manuscript/SLK_MANUSCRIPT_AMNAT_V4.md": "MANUSCRIPT_SOURCE.md",
    "manuscript/AMNAT_TITLE_PAGE_V1.md": "ANONYMOUS_TITLE_PAGE_SOURCE.md",
    "theory/SLK_CORE_THEORY_V1.md": "theory/SLK_CORE_THEORY_V1.md",
    "theory/UNIFIED_THRESHOLD_ATLAS_V1.md": "theory/UNIFIED_THRESHOLD_ATLAS_V1.md",
    "theory/PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md": "theory/PARTIAL_DIVISION_RESIDENT_STABILITY_V1.md",
    "theory/ASSORTMENT_PARTIAL_FOUNDER_V1.md": "theory/ASSORTMENT_PARTIAL_FOUNDER_V1.md",
    "theory/STOCHASTIC_PARTNER_ASSEMBLY_V1.md": "theory/STOCHASTIC_PARTNER_ASSEMBLY_V1.md",
    "theory/ENDPOINT_EXCLUSION_VS_PERSISTENCE_V1.md": "theory/ENDPOINT_EXCLUSION_VS_PERSISTENCE_V1.md",
    "theory/NON_EQUIVALENCE_THEOREM_V1.md": "theory/NON_EQUIVALENCE_THEOREM_V1.md",
    "docs/INV1_EXECUTABLE_VALIDATION_V1.md": "docs/INV1_EXECUTABLE_VALIDATION_V1.md",
    "docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md": "docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md",
    "figures/FIG1_LOGIC_DIAGRAM.svg": "figures/FIG1_LOGIC_DIAGRAM.svg",
    "figures/FIG2_PHASE_MAP.svg": "figures/FIG2_PHASE_MAP.svg",
    "figures/FIG3_EMPIRICAL_LADDER.svg": "figures/FIG3_EMPIRICAL_LADDER.svg",
    "scripts/slk_threshold_atlas.py": "scripts/slk_threshold_atlas.py",
    "scripts/verify_amnat_claims.py": "scripts/verify_amnat_claims.py",
    "tests/test_moran_process_invariant.py": "tests/test_moran_process_invariant.py",
    "tests/test_rare_path_feedback.py": "tests/test_rare_path_feedback.py",
    "tests/test_partial_division_resident_stability.py": "tests/test_partial_division_resident_stability.py",
    "tests/test_assortment_partial_founder.py": "tests/test_assortment_partial_founder.py",
    "tests/test_stochastic_partner_assembly.py": "tests/test_stochastic_partner_assembly.py",
    "tests/test_endpoint_exclusion_vs_persistence.py": "tests/test_endpoint_exclusion_vs_persistence.py",
    "pytest.ini": "pytest.ini",
}

FORBIDDEN_IDENTITY_STRINGS = (
    "zuizui0223",
    "rachelzhang0223",
    "zhang ruiqi",
    "張瑞琪",
    "チョウ ズイキ",
)

README = """# Anonymous reviewer code/theory package

This package accompanies the manuscript **Multifunctional structures can persist while barriers to division of labor change**.

## Scope

The submitted paper is an evolutionary-ecology theory paper about why comparable functional conflicts have different natural resolutions and why one multifunctional architecture can persist in different selective states. It does not estimate its headline results from a private or external empirical dataset. The natural-system examples, including *Pedicularis rex*, are literature based rather than new empirical results.

The package contains the exact manuscript source, supporting theory notes, the three submitted figure sources, the mathematical implementation, a curated literature-based empirical evidence ledger, an independent Moran-process regression test, and a Python verifier. The manuscript centers adaptive integration, historical/developmental trapping, and ecological stabilization, together with the prediction that an unchanged integrated phenotype can lose evolutionary resistance before structural division of labor appears. The fuller theory files retain downstream fixation/occupancy and numerical derivations as supporting results rather than as the biological subject of the paper. The matched-assay partial-division models and associated tests reproduce the distinction between rare-mutant resistance, finite-frequency escape, and onward specialization without claiming empirical confirmation. The conditional delayed-assembly extension separately demonstrates that absolute demographic turnover affects lineage survival even under identical net selective differences; it does not infer empirical extinction rates. A precomputed `CLAIM_VERIFICATION_RECEIPT.json` is included and can be regenerated locally.

## Reproduce the registered numerical checks

From the root of this extracted package, run:

```bash
python scripts/verify_amnat_claims.py --output CLAIM_VERIFICATION_RECEIPT.json
python -m pytest -q -c pytest.ini tests/test_moran_process_invariant.py tests/test_rare_path_feedback.py tests/test_partial_division_resident_stability.py tests/test_assortment_partial_founder.py tests/test_stochastic_partner_assembly.py tests/test_endpoint_exclusion_vs_persistence.py
```

A successful run writes a JSON receipt with `all_checks_pass: true`.

The regenerated receipt is a numerical audit, not a byte-for-byte reproducibility target. Last-bit floating-point values can differ at machine precision across Python/platform builds while all registered inequalities, tolerances, and process checks remain unchanged. Use the project numerical tolerance policy and `all_checks_pass`; do not treat a one-ULP JSON difference as a scientific discrepancy.

## Double-anonymous review

This reviewer bundle is intentionally detached from repository history, remote URLs, author metadata, acknowledgments, and contributor information. `ANONYMITY_AUDIT.txt` records the automated identity-string scan. The bundle should be uploaded directly to the journal review system or another anonymous reviewer-accessible deposit; an identity-bearing repository URL should not be inserted into the anonymous manuscript.
"""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build(out_dir: Path = DEFAULT_OUT) -> Path:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for src_rel, dst_rel in FILES.items():
        src = ROOT / src_rel
        if not src.is_file():
            raise FileNotFoundError(src)
        dst = out_dir / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    (out_dir / "README.md").write_text(README, encoding="utf-8")
    (out_dir / "CLAIM_VERIFICATION_RECEIPT.json").write_text(
        json.dumps(verify(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    leaks: list[str] = []
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
        if path.name in {"ANONYMITY_AUDIT.txt", "SHA256SUMS.txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for token in FORBIDDEN_IDENTITY_STRINGS:
            if token.lower() in text:
                leaks.append(f"{path.relative_to(out_dir)}: {token}")

    if leaks:
        raise RuntimeError("Identity leak(s) in reviewer bundle:\n" + "\n".join(leaks))

    (out_dir / "ANONYMITY_AUDIT.txt").write_text(
        "identity_scan=PASS\n"
        + "forbidden_strings_checked=" + ",".join(FORBIDDEN_IDENTITY_STRINGS) + "\n"
        + "repository_history_included=false\n"
        + "repository_remote_url_included=false\n"
        + "author_metadata_included=false\n",
        encoding="utf-8",
    )

    manifest_lines = []
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"):
        manifest_lines.append(f"{sha256(path)}  {path.relative_to(out_dir).as_posix()}")
    (out_dir / "SHA256SUMS.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    return out_dir


def main() -> None:
    out = build()
    print(out)


if __name__ == "__main__":
    main()
