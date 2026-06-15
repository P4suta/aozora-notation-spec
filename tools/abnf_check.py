#!/usr/bin/env python3
"""Lightweight well-formedness check for the ABNF grammar (RFC 5234).

This is not a full ABNF parser; it catches the mistakes that actually creep
into a hand-maintained grammar:

- every line is either blank, a comment (`;`), a rule definition
  (`name = …` / `name =/ …`), or a continuation (indented) of the previous
  rule;
- every referenced rule name is defined somewhere (modulo RFC 5234 core
  rules: ALPHA DIGIT HEXDIG DQUOTE SP HTAB WSP CRLF CR LF CTL VCHAR CHAR
  OCTET BIT);
- no rule is defined twice with `=` (use `=/` to extend);
- brackets/parens/quotes within a rule body are balanced.

Exit non-zero on any problem.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

CORE = {
    "ALPHA", "BIT", "CHAR", "CR", "CRLF", "CTL", "DIGIT", "DQUOTE", "HEXDIG",
    "HTAB", "LF", "LWSP", "OCTET", "SP", "VCHAR", "WSP",
}
RULENAME = r"[A-Za-z][A-Za-z0-9-]*"
DEF_RE = re.compile(rf"^({RULENAME})\s*(=/?)\s*(.*)$")
REF_RE = re.compile(RULENAME)
# tokens that look like rule names but are operators / quoted / numeric.
NONREF_PREFIX = ("%", '"', "'")


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    defined: set[str] = set()
    redefined: list[str] = []
    rules: dict[str, str] = {}  # name -> accumulated body
    current: str | None = None
    problems: list[str] = []

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split(";", 1)[0].rstrip()  # strip comments
        if not line.strip():
            continue
        if raw[:1] in (" ", "\t"):  # continuation
            if current is None:
                problems.append(f"{lineno}: continuation with no rule open")
            else:
                rules[current] += " " + line.strip()
            continue
        m = DEF_RE.match(line)
        if not m:
            problems.append(f"{lineno}: not a rule definition or continuation: {line!r}")
            continue
        name, op, body = m.group(1), m.group(2), m.group(3)
        if op == "=":
            if name in defined:
                redefined.append(name)
            defined.add(name)
            rules[name] = body
        else:  # =/
            rules[name] = rules.get(name, "") + " " + body
        current = name

    # balance + reference check per rule body
    known = defined | CORE
    for name, body in rules.items():
        for op, cl in (("(", ")"), ("[", "]")):
            if body.count(op) != body.count(cl):
                problems.append(f"rule {name}: unbalanced {op}{cl}")
        if body.count('"') % 2 != 0:
            problems.append(f"rule {name}: unbalanced quotes")
        # collect references: identifiers not inside quotes, not %-terminals
        stripped = re.sub(r'"[^"]*"', " ", body)
        stripped = re.sub(r"%[bxd][0-9A-Fa-f.\-]+", " ", stripped)
        for tok in REF_RE.findall(stripped):
            if tok not in known:
                problems.append(f"rule {name}: undefined reference {tok!r}")

    for r in redefined:
        problems.append(f"rule {r}: defined twice with '=' (use '=/' to extend)")

    if problems:
        for p in problems:
            print(f"FAIL abnf: {p}", file=sys.stderr)
        print(f"\n{len(problems)} ABNF problem(s)", file=sys.stderr)
        return 1
    print(f"ok: ABNF well-formed ({len(defined)} rules)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: abnf_check.py <grammar.abnf>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
