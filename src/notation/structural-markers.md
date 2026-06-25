# 6.19 Structural markers (本文終わり・改行)

## Synopsis

Two self-contained marker directives carry document structure rather than
inline styling. `本文終わり` marks the end of the main body — a colophon or
afterword follows — and is a **block-level** structural leaf. `改行` is a
**forced in-paragraph line break** — an **inline** leaf.

## Notation

Each is a self-contained directive with no opener/closer and no inner content:

```text
［＃本文終わり］    ← end of the main body (a colophon/afterword follows)
［＃改行］          ← forced in-paragraph line break
```

```abnf
body-end     = LBRACK HASH %s"本文終わり" RBRACK
forced-break = LBRACK HASH %s"改行" RBRACK
```

## Parameters

None.

## Semantics

- `［＃本文終わり］` yields a zero-width `bodyEnd` node — a **block leaf**
  (§8.1, like a break) standing on its own line. It marks the boundary after
  which a colophon or afterword follows; it does **not** capture or govern the
  following lines.
- `［＃改行］` yields a `forcedBreak` node — an **inline leaf** forcing a line
  break inside the current paragraph without ending it.
- Reference rendering (§8): `bodyEnd` → `<div class="aozora-body-end"></div>`;
  `forcedBreak` → `<br />`.
- `改行` is **longest-match disambiguated** from `改行天付き` (the §6.6
  top-flush hanging-indent form): only a bare `［＃改行］` is a forced break;
  `［＃ここから改行］天付き…` opens an indent region (§6.6) instead.
- Serialization reconstructs each directive byte-exact (§7.6).

## Error conditions

- None specific. A malformed marker body (an unrecognised directive between
  `［＃` and `］`) falls to the generic annotation handling of §6.14 and
  round-trips byte-exact.

## Conformance vectors

`body_end`, `forced_break` (under `conformance/vectors/`).
