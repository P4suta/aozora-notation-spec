# 6.10 Headings (見出し)

## Synopsis

A heading marks a run of text as a structural title. Aozora distinguishes
levels (大 / 中 / 小 見出し) and styles (standard, *window* 窓見出し, *sub*
副見出し). Headings are most often expressed as a **forward-reference hint**
that promotes a quoted run.

## Notation

```text
　　　　序［＃「序」は大見出し］
［＃「第一章」は中見出し］
```

```abnf
heading-hint = LBRACK HASH LQUOTE target RQUOTE %s"は" level %s"見出し" RBRACK
level        = %s"大" / %s"中" / %s"小"
```

A *window* (窓) heading and a *sub* (副) heading are named likewise
(`…は窓見出し`, `…は副見出し`).

## Parameters

- **target** — the quoted run promoted to a heading (resolved by §7.5).
- **level** — 大 / 中 / 小 (and the 窓 / 副 styles).

## Semantics

- A heading hint resolves its target (§7.5) and promotes that run to a
  `heading` node carrying the level/style.
- Reference rendering (§8) is a heading element appropriate to the level
  (e.g. `<h1>`–`<h3>`), or a styled block for 窓/副; the precise tag is part
  of the reference mapping (§8.3), not mandated.
- Serialization reconstructs the directive (and the literal target it follows)
  byte-exact (§7.6).

## Error conditions

- A heading hint whose target is absent from the look-back degrades to a
  generic annotation (§6.14), as with other forward references (§7.5).

## Conformance vectors

`heading`, `heading_hint`.
