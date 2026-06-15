#!/usr/bin/env python3
"""Offline cross-reference check for the mdBook sources.

- Every `](path)` in `src/SUMMARY.md` points to a file that exists.
- Every relative Markdown link in `src/**.md` resolves to an existing file.
- Every in-book anchor (`file.md#anchor` or bare `#anchor`) resolves to a
  heading in the target file (GitHub/mdBook-style slug).

External links (`http(s)://`, `mailto:`) are not fetched (offline). Exit
non-zero on any dangling internal reference.
"""
from __future__ import annotations
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slugify(text: str) -> str:
    """Approximate mdBook's heading-id algorithm."""
    text = re.sub(r"`([^`]*)`", r"\1", text)  # drop inline-code backticks
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch.isalnum() or ch == "-":
            out.append(ch)
        elif ch in " \t":
            out.append("-")
        # else drop
    slug = "".join(out)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return unicodedata.normalize("NFC", slug)


def headings(path: Path) -> set[str]:
    slugs: set[str] = set()
    if not path.exists():
        return slugs
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = slugify(m.group(1))
        n = counts.get(base, 0)
        counts[base] = n + 1
        slugs.add(base if n == 0 else f"{base}-{n}")
    return slugs


def main() -> int:
    problems: list[str] = []
    md_files = sorted(SRC.rglob("*.md"))
    if not md_files:
        print("no markdown under src/", file=sys.stderr)
        return 1

    for md in md_files:
        for raw in LINK_RE.findall(md.read_text(encoding="utf-8")):
            target = raw.strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            anchor = None
            if "#" in target:
                path_part, anchor = target.split("#", 1)
            else:
                path_part = target
            if path_part == "":
                dest = md  # same-file anchor
            else:
                dest = (md.parent / path_part).resolve()
                if not dest.exists():
                    problems.append(f"{md.relative_to(REPO)} -> missing file {path_part}")
                    continue
            if anchor:
                if dest.suffix == ".md" and anchor not in headings(dest):
                    problems.append(
                        f"{md.relative_to(REPO)} -> dead anchor #{anchor} in {dest.name}"
                    )

    if problems:
        for p in problems:
            print(f"FAIL link: {p}", file=sys.stderr)
        print(f"\n{len(problems)} dangling reference(s)", file=sys.stderr)
        return 1
    print(f"ok: cross-references resolve ({len(md_files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
