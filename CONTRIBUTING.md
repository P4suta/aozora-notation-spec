# Contributing

This is a **normative specification**. Edits change what conforming
implementations must do, so they follow a stricter discipline than ordinary
docs.

## Ground rules

1. **Two sources of truth.** Every normative statement must be justified
   against (a) the official 注記一覧
   (<https://www.aozora.gr.jp/annotation/>) and (b) the real Aozora Bunko
   corpus (observed forms / frequencies). Cite them. The official guide wins
   on *intent*; the corpus wins on *what actually occurs*.
2. **No fiction.** Do not document a form or behaviour that the official guide
   does not define and the corpus does not use. Underspecification is what
   this project exists to remove — do not add more.
3. **Where the official guide is silent or ambiguous, decide explicitly.**
   Record the decision and its rationale in `docs/adr/` and reference the ADR
   from the relevant section.
4. **RFC 2119 keywords are normative.** Use MUST / SHOULD / MAY (and their
   negatives) per [§2](src/conventions.md); use them deliberately, not for
   emphasis.
5. **Every normative example is a conformance vector.** If a section shows
   `input → result`, add (or point at) a vector under `conformance/vectors/`
   so the example is machine-checked, never just asserted in prose.

## Per-family section template

See [`src/notation/ruby.md`](src/notation/ruby.md) for the canonical shape:
Synopsis → Notation (ABNF + examples) → Parameters → Semantics (normative) →
Error conditions → Conformance vectors.

## Checks

Run `just ci` before opening a PR:

- `just validate` — every vector matches the schema; every `must` vector has
  its required projections.
- `just abnf-check` — the grammar is well-formed.
- `just linkcheck` — cross-references and `SUMMARY.md` are consistent.
- `just build` — the mdBook renders.
