# 9. Diagnostics and Error Handling

A processor reports **diagnostics**: structured, non-fatal observations about
the input. Per §2.4 a processor **MUST** always produce a result and **MUST
NOT** abort; diagnostics annotate what it noticed and how the affected
construct degraded.

## 9.1 Diagnostic structure

Each diagnostic carries:

- a stable **code** — a kebab-case identifier such as `empty-ruby-reading`.
  Codes are stable across minor revisions; new diagnostics add new codes.
- a **severity** — `error`, `warning`, or `note`.
- a **span** — a byte range in the sanitized source (§2.3) locating the
  construct.

A conforming processor **MUST** detect and report every `error`-severity
diagnostic in §9.2–§9.5 whose triggering condition the input meets (these are
the `must`-level diagnostics of §10), with the specified code and severity.
`warning` and `note` diagnostics are RECOMMENDED. A processor MAY report
additional diagnostics under codes not defined here.

## 9.2 Encoding and lexical

### Source contains PUA

`source-contains-pua` · **warning**

The source contains a code point that a processor reserves internally as a
placeholder (§3.4). This diagnostic applies only to a processor that uses such
a strategy; it neutralizes the occurrence during §4 and reports this. Real
Aozora Bunko text does not contain such code points.

### Unclosed bracket

`unclosed-bracket` · **error**

An opener (ruby `《`, a directive `［＃`, a quote, …) reached end of input with
no matching closer. **Recovery:** the region degrades to plain text; no pair
is emitted. The label points at the opener.

### Unmatched close

`unmatched-close` · **error**

A closer appeared with no matching opener, or against a different kind of
opener. **Recovery:** the stray closer is treated as plain text. The label
points at the closer.

## 9.3 Normalization and gaiji

### Accent decomposition applied

`accent-decomposition-applied` · **note**

A `〔…〕` accent digraph was rewritten to its combined Unicode form during §4
(`〔e'〕` → `é`). Intended behaviour, surfaced as a note so an editor can show
what changed; the transform is loss-free and the serializer (§7) reconstructs
the `〔…〕` form. The span is in post-decomposition coordinates.

### Unresolved gaiji

`unresolved-gaiji` · **warning**

A `※［＃…］` reference resolved to neither a Unicode scalar nor a JIS X 0213
cell (§6.4). **Recovery:** rendering falls back to the description text. The
label points at the reference.

## 9.4 Ruby

### Empty ruby reading

`empty-ruby-reading` · **error**

An explicit-base ruby supplied a base (`｜` precedes `《`) but an empty `《》`
reading. A bare `《》` with no `｜` is *not* flagged (it is literal text).
**Recovery:** degrades to plain text. The label spans the whole `｜base《》`.

### Nested ruby

`nested-ruby` · **error**

A ruby reading body itself opened another ruby (`｜漢《か《ん》じ》`). Ruby does
not nest. An adjacent `《《…》》` is **not** nested ruby — it is
[double-bracket bouten](notation/bouten.md). **Recovery:** the outer ruby is
parsed best-effort; the label points at the inner `《`.

## 9.5 Containers, forward references, and kunten

### Mismatched container close

`mismatched-container-close` · **error**

A paired container opened with one family (`indent` / `align-end` /
`keigakomi` / `warichu`) was closed by a closer of a different family.
Comparison is by family, so `2字下げ` closed by a plain `字下げ終わり` is
**not** flagged. **Recovery:** the opener is auto-closed at the closer, keyed
by the open family. The label points at the closer.

### Unrecognised container directive

`unrecognised-container-directive` · **warning**

A `［＃ここから…］` opener named no known container kind. **Recovery:** kept as
a generic annotation (the "no bare `［＃`" guarantee, §6.14, holds); no
container is opened. The label spans the directive.

### Mismatched bouten container

`mismatched-bouten-container` · **error**

A 傍点/傍線 range (§6.2) opened with one family (点 dots / 線 line) and was
closed by the other (`［＃傍点］…［＃傍線終わり］`). **Recovery:** the run is
keyed to the opener's variant. The label points at the closer.

### Break in single-line container

`break-in-single-line-container` · **warning**

A page or section break shares a source line with a single-line layout
directive (§6.6), or falls inside a `割り注` range (§6.8). A single-line
container governs only the rest of its line, so the break drops it. Block
containers persist across breaks and are **not** flagged. The label points at
the break.

### TCY target not found

`tcy-target-not-found` · **warning**

A `［＃「X」は縦中横］` forward reference (§6.3) named a target absent from the
preceding text. **Recovery:** degrades to a generic annotation. The label
spans the directive.

### Bouten target ambiguous

`bouten-target-ambiguous` · **warning**

A `［＃「X」に傍点］` forward reference (§6.2) named a target that occurs more
than once in the preceding look-back. **Recovery:** applied to the match the
look-back rule selects, which may not be intended. The label spans the
directive.

### Bracketed kaeriten no pair

`bracketed-kaeriten-no-pair` · **error**

A bracketed kaeriten of rank ≥ 2 (`［＃二］` / `［＃下］` / `［＃乙］`) appeared in
a document whose family base (`一` / `上` / `甲`) is absent entirely (§6.5).
The check is document-wide and base-only. **Recovery:** the mark is kept. The
label points at the unpaired mark.

### Kaeriten outside kanbun

`kaeriten-outside-kanbun` · **warning**

A kaeriten is the only one in the document and its surroundings read as
ordinary kana prose, i.e. it is likely a stray annotation rather than a return
mark (§6.5). A conservative lookahead heuristic; a cluster of kaeriten is
never flagged. The label points at the lone mark.

## 9.6 Diagnostic ordering

When a processor exposes diagnostics as an ordered sequence, that sequence
**SHOULD** be non-decreasing by processing phase — normalization (§4) before
lexical/pairing before classification (§5, §6) before the post-pass that
resolves containers (§7). This keeps editor surfaces and golden tests stable.
Ordering within a phase is not constrained.
