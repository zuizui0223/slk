from __future__ import annotations

import re
from pathlib import Path

MANUSCRIPT = Path("manuscript/SLK_MANUSCRIPT_AMNAT_V4.md")


def words(text: str) -> list[str]:
    # Stable submission-count approximation: count lexical tokens after removing
    # Markdown punctuation; mathematical identifiers still count as words.
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)


def section(text: str, start: str, end: str | None = None) -> str:
    i = text.index(start) + len(start)
    if end is None:
        return text[i:]
    j = text.index(end, i)
    return text[i:j]


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    abstract = section(text, "## Abstract", "## 1. Introduction")
    pre_refs = text.split("## Literature Cited", 1)[0]
    figure_refs = len(
        re.findall(r"!\[[^\]]*\]\(\.\./figures/FIG\d+_[^)]+\.svg\)", text)
    )
    table_refs = len(
        re.findall(r"^\|(?:\s*:?-{3,}:?\s*\|){2,}\s*$", text, flags=re.MULTILINE)
    )

    title_n = len(words(title))
    abstract_n = len(words(abstract))
    text_n = len(words(pre_refs)) - title_n

    print(f"AMNAT_TITLE_WORDS={title_n}")
    print(f"AMNAT_ABSTRACT_WORDS={abstract_n}")
    print(f"AMNAT_TEXT_WORDS_EXCL_LITERATURE_CITED={text_n}")
    print(f"AMNAT_FIGURE_COUNT={figure_refs}")
    print(f"AMNAT_TABLE_COUNT={table_refs}")
    print(f"AMNAT_FIGURE_TABLE_TOTAL={figure_refs + table_refs}")

    assert abstract_n <= 200, f"abstract exceeds 200 words: {abstract_n}"
    assert text_n <= 7500, f"text exceeds usual 7500-word Major Article limit: {text_n}"
    assert figure_refs + table_refs <= 6, (
        "figures + tables exceed 6-item Major Article guidance: "
        f"{figure_refs}+{table_refs}={figure_refs + table_refs}"
    )
    assert 1 <= title_n <= 20, f"unexpected title word count: {title_n}"


if __name__ == "__main__":
    main()
