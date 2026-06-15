#!/usr/bin/env python3
"""Import conformance vectors from an external fixture set.

A maintenance utility for `conformance/vectors/`. It reads a directory of
fixtures in the standard golden layout — one subdirectory per case, each with
`source.txt`, `meta.toml` (`feature`, `level`), `expected.html`,
`expected.serialize.txt`, and `expected.{diagnostics,nodes,pairs,container_pairs}.json`
(each JSON an `{"schema_version":…,"data":[…]}` envelope) — and collapses each
into one self-contained `vector.json` conforming to
`conformance/schema/vector.schema.json`.

Usage:
    python3 tools/import_vectors.py /path/to/fixtures/render
"""
from __future__ import annotations
import json
import sys
import tomllib
from pathlib import Path

# Feature → the spec section that defines it (informative metadata).
FEATURE_SECTION = {
    "ruby": "6.1", "empty_ruby": "6.1",
    "bouten": "6.2",
    "tate_chu_yoko": "6.3",
    "gaiji": "6.4",
    "kaeriten": "6.5", "kunten": "6.5",
    "indent_container": "6.6", "align_end_container": "6.6", "container": "6.6",
    "keigakomi_container": "6.7",
    "warichu_inline": "6.8",
    "break": "6.9", "page_break": "6.9", "section_break": "6.9",
    "heading": "6.10",
    "sashie": "6.11",
    "annotation": "6.14",
    "plain_text": "5",
    "accent": "4",
    "pua_collision": "3",
    "unclosed": "9",
    "pageful": "10",
}

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "conformance" / "vectors"


def envelope_data(path: Path):
    """Read aozora's {"schema_version":1,"data":[...]} envelope -> the list."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("data", [])


def map_diagnostic(d: dict) -> dict:
    """Fixture diagnostic projection -> spec vector diagnostic.

    The fixture carries a short `kind` (e.g. "empty_ruby_reading"); the spec
    uses the kebab-case code of §9 ("empty-ruby-reading"). Implementation-
    internal sanity checks (a `::`-namespaced kind) are not part of the spec's
    error contract and are dropped.
    """
    kind = d["kind"]
    if "::" in kind:
        return {}  # internal check: not a spec diagnostic
    out = {"code": kind.replace("_", "-"), "severity": d["severity"]}
    if "span" in d:
        out["span"] = d["span"]
    return out


def main(src_root: str) -> int:
    root = Path(src_root)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for case in sorted(p for p in root.iterdir() if p.is_dir()):
        src = case / "source.txt"
        meta_f = case / "meta.toml"
        if not src.exists() or not meta_f.exists():
            continue
        meta = tomllib.loads(meta_f.read_text(encoding="utf-8"))
        feature = str(meta.get("feature", case.name)).split(",")[0].strip()
        level = str(meta.get("level", "should")).strip()
        expected: dict = {}
        html = case / "expected.html"
        ser = case / "expected.serialize.txt"
        if html.exists():
            expected["html"] = html.read_text(encoding="utf-8")
        if ser.exists():
            expected["serialize"] = ser.read_text(encoding="utf-8")
        # `nodes` and `pairs` carry SOURCE-coordinate spans (portable).
        # `container_pairs` is dropped: the fixtures project it in NORMALIZED
        # (sentinel-internal) coordinates, which are implementation-specific —
        # container structure is already captured by the containerOpen /
        # containerClose entries in `nodes`, in source coordinates.
        nodes = envelope_data(case / "expected.nodes.json")
        pairs = envelope_data(case / "expected.pairs.json")
        diags = envelope_data(case / "expected.diagnostics.json")
        if nodes:
            expected["nodes"] = nodes
        if pairs:
            expected["pairs"] = pairs
        # diagnostics is always meaningful (empty list = "no diagnostics");
        # drop internal-check entries that are not spec diagnostics.
        expected["diagnostics"] = [m for d in diags if (m := map_diagnostic(d))]

        vector = {
            "name": case.name,
            "meta": {
                "feature": feature,
                "level": level,
                "spec_section": FEATURE_SECTION.get(feature, "6"),
            },
            "source": src.read_text(encoding="utf-8"),
            "expected": expected,
        }
        dst = OUT / case.name
        dst.mkdir(parents=True, exist_ok=True)
        (dst / "vector.json").write_text(
            json.dumps(vector, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        count += 1
    print(f"seeded {count} vectors into {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
