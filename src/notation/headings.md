# 6.10 Headings (見出し)

## Synopsis

A heading marks a run of text as a structural title. Aozora distinguishes
three **levels** (大 / 中 / 小 見出し) and, orthogonally, three **styles** —
standard, *same-line* (同行, the title shares its line with the body that
follows) and *window* (窓, an inset title). Style and level combine freely:
同行中見出し, 窓小見出し, and so on. Headings are most often expressed as a
**forward-reference hint** that promotes or marks a quoted run.

## Notation

```text
　　　　序［＃「序」は大見出し］
［＃「第一章」は中見出し］
萩原朔太郎［＃「萩原朔太郎」は同行中見出し］　二十年の友。…
```

```abnf
heading-hint = LBRACK HASH LQUOTE target RQUOTE %s"は" [ style ] level %s"見出し" RBRACK
level        = %s"大" / %s"中" / %s"小"
style        = %s"同行" / %s"窓"
```

The optional *style* prefix selects 同行 (same-line) or 窓 (window); its
absence is the standard style. Style and level pair freely
(`…は同行中見出し`, `…は窓小見出し`).

## Parameters

- **target** — the quoted run promoted or marked as a heading (resolved by §7.5).
- **level** — 大 / 中 / 小.
- **style** — standard (no prefix), 同行 (same-line), or 窓 (window).

## Semantics

- A heading hint resolves its target (§7.5) and carries the level and style. It
  **promotes** that run to a `heading` node when the target is the bare line
  immediately preceding the directive — the run is pulled out of the flow and
  becomes the heading. When the referent is not such a clean preceding line, the
  hint is retained inline (a `heading-hint` marker) rather than promoted, so no
  run is mis-titled and no input is lost. The 同行 (same-line) and 窓 styles in
  practice run into the body on their own line, so they are typically retained
  as hints; the standard style with a bare title line is the usual promotion
  case.
- Reference rendering (§8): a promoted standard 大 / 中 / 小 heading is
  `<h1>`–`<h3>` (`class="aozora-heading aozora-heading-<large|medium|small>"`);
  the 同行 / 窓 styles add an `aozora-heading-<same-line|window>` modifier (and
  窓 renders as a styled `<div>` rather than an outline `<hN>`); an unpromoted
  hint is a hidden inline marker (`<span class="aozora-heading-hint"
  data-level=… data-style=… data-target=… hidden>`), with `data-style` present
  only for a non-standard style. The precise tag is part of the reference
  mapping (§8.2), not mandated.
- Serialization reconstructs the directive (and the literal target it follows)
  byte-exact (§7.6).

## Error conditions

- A heading hint whose target is absent from the look-back degrades to a
  generic annotation (§6.14), as with other forward references (§7.5).

## Further heading forms

Two block-delimited heading forms are catalogued but deferred to a later
revision (§10.5): the **paired window** form
`［＃窓<level>見出し］ … ［＃窓<level>見出し終わり］` and the **block** form
`［＃ここから<level>見出し］ … ［＃ここで<level>見出し終わり］`. A processor that
does not recognise them retains the directives as generic annotations (§6.14).

## Conformance vectors

`heading`, `heading_hint`, `heading_promoted`, `heading_same_line`,
`heading_window`.
