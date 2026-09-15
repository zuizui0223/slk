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
    "manuscript/SLK_MANUSCRIPT_AMNAT_V3.md": "MANUSCRIPT_SOURCE.md",
    "manuscript/AMNAT_TITLE_PAGE_V1.md": "ANONYMOUS_TITLE_PAGE_SOURCE.md",
    "theory/SLK_CORE_THEORY_V1.md": "theory/SLK_CORE_THEORY_V1.md",
    "theory/NON_EQUIVALENCE_THEOREM_V1.md": "theory/NON_EQUIVALENCE_THEOREM_V1.md",
    "figures/FIG1_LOGIC_DIAGRAM.svg": "figures/FIG1_LOGIC_DIAGRAM.svg",
    "figures/FIG2_PHASE_MAP.svg": "figures/FIG2_PHASE_MAP.svg",
    "figures/FIG3_EMPIRICAL_LADDER.svg": "figures/FIG3_EMPIRICAL_LADDER.svg",
    "scripts/verify_amnat_claims.py": "code/verify_amnat_claims.py",
}

FORBIDDEN_IDENTITY_STRINGS = (
    "zuizui0223",
    "rachelzhang0223",
    "zhang ruiqi",
    "張瑞琪",
    "チョウ ズイキ",
)

README = """# Anonymous reviewer code/theory package

This package accompanies the manuscript **From functional conflict to evolutionary architecture across biological scales**.

## Scope

The submitted paper is a theory/concept paper. It does not estimate its headline results from a private or external empirical dataset. Numerical values in the witness table are constructive parameter regimes used to demonstrate logical non-implications. The three figures are theory diagrams/phase summaries.

The package therefore contains the exact manuscript source, the two theory notes underlying the registered split-and-invariant claims, the three submitted figure sources, and a standard-library Python verifier for the five witness regimes plus the fixation-occupancy invariant. A precomputed `CLAIM_VERIFICATION_RECEIPT.json` is included and can be regenerated locally.

## Reproduce the registered numerical checks

From the root of this extracted package, run:

```bash
python code/verify_amnat_claims.py --output CLAIM_VERIFICATION_RECEIPT.json
```

A successful run writes a JSON receipt with `all_checks_pass: true`.

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
