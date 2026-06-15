#!/usr/bin/env python3
"""Validate every conformance vector against the JSON Schema.

- Each `conformance/vectors/<name>/vector.json` MUST validate against
  `conformance/schema/vector.schema.json`.
- `name` MUST equal the directory name.
- A `must`-level vector MUST carry `expected.html`, `expected.serialize`, and
  `expected.diagnostics`.
- Span offsets MUST satisfy `start <= end`.

Exit non-zero on any failure. Pure stdlib + `jsonschema`.
"""
from __future__ import annotations
import json
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

    if errors:
        for e in errors:
            print(f"FAIL {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) across {n} vector(s)", file=sys.stderr)
        return 1
    print(f"ok: {n} conformance vectors valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
