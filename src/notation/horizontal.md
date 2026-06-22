# 6.18 Horizontal writing (横組み)

## Synopsis

A 横組み directive sets a run or a block of text **horizontally** inside an
otherwise vertical document — used for Western dates, formulae, and tabular
fragments ([AOZORA-ANNOTATION], `etc.html`). Two forms occur: an inline
forward reference for a single run and a `ここから`/`ここで` block region.

## Notation

```abnf
horizontal-inline = target "［＃「" target "」は横組み］"
horizontal-open   = LBRACK HASH %s"ここから横組み" RBRACK
horizontal-close  = LBRACK HASH %s"ここで横組み終わり" RBRACK
```

```text
西暦［＃「西暦」は横組み］

［＃ここから横組み］
2024年1月
［＃ここで横組み終わり］
```

## Parameters

- **target** — for the inline form, the single quoted run to set horizontally
  (resolved by the look-back rule, §7.5).

## Semantics

- The inline forward-reference form yields an `emphasis` node over its target
  and is an **inline** construct.
- The block form pairs opener and closer by the `horizontal` family (§7.1) and
  yields a **block** `container` node governing the enclosed paragraphs; it
  nests with other block containers (§7.3).
- Reference rendering (§8) is `<span class="aozora-yokogumi">…</span>` for
  the inline form and
  `<div class="aozora-container aozora-container-yokogumi">…</div>` for the
  block form. Whether a processor reorients glyphs or merely tags the region is
  a presentation choice; the node model only records that the run is 横組み.
- Serialization reconstructs the inline directive or the block opener/closer
  byte-exact (§7.6).

## Error conditions

- **Target with no referent (inline)** — degrades to a generic annotation
  (§6.14).
- **Mismatched / unclosed block** — handled per
  [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  and [`unclosed-bracket`](../diagnostics.md#unclosed-bracket).

## Conformance vectors

`horizontal_inline_forward`, `horizontal_container` (under
`conformance/vectors/`).
