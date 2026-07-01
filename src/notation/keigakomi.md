# 6.7 Keigakomi (罫囲み)

## Synopsis

Keigakomi draws a **ruled frame** (a box) around a block of text — used for
notices, inset boxes, and the like.

## Notation

A paired block container:

```text
［＃罫囲み］
枠の中の文章。
［＃罫囲み終わり］
```

```abnf
keigakomi-open  = LBRACK HASH %s"罫囲み" RBRACK
keigakomi-close = LBRACK HASH %s"罫囲み終わり" RBRACK
```

> The official guide also writes this block as
> `［＃ここから罫囲み］ … ［＃ここで罫囲み終わり］`. The bare opener/closer
> above is the canonical pair in this specification; the `ここから`/`ここで`
> variant is an accepted equivalent and pairs by the same `keigakomi`
> family.

There is also an **inline forward-reference** form that boxes a single run,
the span-level counterpart of the block container (parallel to how 太字 has
both a block range and a `は`-form leaf, §6.12):

```text
注意［＃「注意」は罫囲み］事項。
新興河上［＃「新興河上」に枠囲み］      ← に particle + 枠囲み spelling
```

```abnf
keigakomi-inline = target "［＃「" target "」"
                   (%s"は" / %s"に") (%s"罫囲み" / %s"枠囲み" / %s"枠囲い") "］"
```

Unlike 太字/斜体 (`は`-only, §6.12), the frame decoration accepts **either**
particle — `は` ("is framed") or `に` ("frame applied to") — and the corpus
spells the keyword `罫囲み`, `枠囲み`, or `枠囲い` (okurigana variant). All
canonicalise to `は罫囲み` on serialize.

### Box-character enclosure (「□」囲み)

A second inline form names the **enclosing glyph** explicitly, in a quoted
token after the particle:

```text
一［＃「一」は「□」囲み］
```

```abnf
box-enclosure = target "［＃「" target "」" %s"は「" box-glyph %s"」囲み" "］"
box-glyph     = %x25A1   ; □ (U+25A1) — the only attested glyph
```

This is the same enclosure **family** as 罫囲み — it boxes the target run —
but a distinct **style**: a box glyph rather than a ruled frame. The `□`
names an enclosure *kind*, not free data; a future non-□ glyph would be a
further named kind (compare 二重罫囲み / 点線丸囲み), never an arbitrary
character. The look-back rule of §7.5 consumes the preceding literal exactly
as the other `は`-form leaves.

## Parameters

None for the block form. The inline form names a single **target** (the
quoted run to box), resolved by the look-back rule of §7.5.

## Semantics

- The opener/closer pair (§7.1) yields a `container` node (family
  `keigakomi`) governing the enclosed block; it nests with other block
  containers (§7.3).
- The inline forward-reference form yields an `emphasis` node over its target
  run and is an **inline** construct. The box-character form (`「X」は「□」囲み`)
  likewise yields an `emphasis` node over its target.
- Reference rendering (§8) is
  `<div class="aozora-container aozora-container-keigakomi">…</div>` for the
  block form, `<span class="aozora-keigakomi-inline">…</span>` for the inline
  rule form, and `<span class="aozora-keigakomi-box">…</span>` for the
  box-character form (the box is drawn by the stylesheet, so the `□` glyph is
  not emitted into the body).
- Serialization reconstructs the block opener/closer byte-exact (§7.6); the
  inline rule form canonicalises the particle and keyword to `は罫囲み`
  (`に`→`は`, `枠囲み`/`枠囲い`→`罫囲み`), and the box form reconstructs
  `「X」は「□」囲み` byte-exact — all idempotent after the first pass.

## Error conditions

- [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  — closed by a different container family.
- [`unclosed-bracket`](../diagnostics.md#unclosed-bracket) — opener with no
  closer.

## Conformance vectors

`keigakomi_container`, `keigakomi_inline_forward`, `keigakomi_inline_framed`,
`box_enclosure`, `box_enclosure_no_referent`.
