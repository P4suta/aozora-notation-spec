#!/usr/bin/env python3
"""Validate every conformance vector against the JSON Schema.

- Each `conformance/vectors/<name>/vector.json` MUST validate against
  `conformance/schema/vector.schema.json`.
- `name` MUST equal the directory name.
- A `must`-level vector MUST carry `expected.html`, `expected.serialize`, and
  `expected.diagnostics`.
- Span offsets MUST satisfy `start <= end`.
- `meta.note` is REQUIRED and MUST begin with `[provenance:` (enforced by the
  schema). This is the de-circularisation contract — a vector's expected output
  is hand-derived from the spec + corpus, never imported from a processor.
- Corpus-verify: a vector carrying `meta.corpus` whose `source` is a real
  corpus fragment is confirmed to actually occur in that file, *when*
  `$AOZORA_CORPUS_ROOT` is set. Skipped (not failed) when the corpus is absent,
  so the structural checks still run in a corpus-less CI.

Exit non-zero on any failure. Pure stdlib + `jsonschema`.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "conformance" / "schema" / "vector.schema.json"
VECTORS = REPO / "conformance" / "vectors"


def spans(obj):
    """Yield every {start,end} span anywhere in the vector."""
    if isinstance(obj, dict):
        if "start" in obj and "end" in obj and isinstance(obj["start"], int):
            yield obj
        for v in obj.values():
            yield from spans(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from spans(v)


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    if not VECTORS.is_dir():
        print(f"no vectors directory at {VECTORS}", file=sys.stderr)
        return 1
    corpus_env = os.environ.get("AOZORA_CORPUS_ROOT")
    corpus_root = Path(corpus_env) if corpus_env else None
    corpus_checked = 0

    errors: list[str] = []
    n = 0
    for vfile in sorted(VECTORS.glob("*/vector.json")):
        n += 1
        case = vfile.parent.name
        try:
            vec = json.loads(vfile.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{case}: invalid JSON: {e}")
            continue
        for err in validator.iter_errors(vec):
            errors.append(f"{case}: schema: {err.message} (at {list(err.path)})")
        if vec.get("name") != case:
            errors.append(f"{case}: name {vec.get('name')!r} != directory {case!r}")
        if vec.get("meta", {}).get("level") == "must":
            exp = vec.get("expected", {})
            for need in ("html", "serialize", "diagnostics"):
                if need not in exp:
                    errors.append(f"{case}: must-level vector missing expected.{need}")
        for sp in spans(vec):
            if sp["start"] > sp["end"]:
                errors.append(f"{case}: span start {sp['start']} > end {sp['end']}")

        # Corpus-verify: confirm a cited corpus fragment actually occurs in its
        # source file. Skipped (not an error) when the corpus is unavailable.
        corpus_meta = vec.get("meta", {}).get("corpus")
        if corpus_meta and corpus_root is not None:
            work = corpus_root / corpus_meta["work"]
            if not work.is_file():
                errors.append(f"{case}: corpus work not found: {corpus_meta['work']}")
            else:
                text = work.read_text(encoding="utf-8", errors="replace")
                fragment = vec.get("source", "").strip("\n")
                if fragment and fragment not in text:
                    errors.append(
                        f"{case}: source fragment absent from {corpus_meta['work']} "
                        f"(corpus-verify) — provenance claim unmet"
                    )
                else:
                    corpus_checked += 1

    if errors:
        for e in errors:
            print(f"FAIL {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) across {n} vector(s)", file=sys.stderr)
        return 1
    if corpus_root is None:
        print(f"ok: {n} conformance vectors valid (corpus-verify skipped: $AOZORA_CORPUS_ROOT unset)")
    else:
        print(f"ok: {n} conformance vectors valid; {corpus_checked} corpus-verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
