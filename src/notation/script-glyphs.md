# 6.16 Superscript, subscript, and side glyphs (上付き・下付き・小書き)

## Synopsis

Four forward-reference families set a short run as a **small glyph** offset from
the baseline rather than changing its weight or slant (§6.12):

- **上付き小文字** (superscript) and **下付き小文字** (subscript) — the
  横組み (horizontal-writing) raised/lowered small characters of mathematics
  (exponents) and chemistry (formula indices).
- **行右小書き** and **行左小書き** — the 縦組み (vertical-writing) small
  glyphs set to the right or left of the line.

All four are documented on the official 注記一覧 "その他" page
([AOZORA-ANNOTATION], `etc.html`). They share the forward-reference shape and
the `は` particle with 太字/斜体 (§6.12) and yield the same `emphasis` node, so
the spec groups them as one inline family distinct from bouten (§6.2).

## Notation

Each family is **forward reference only** — quote the target; the treatment
applies to the most recent preceding occurrence (§7.5). The particle is `は`.

```abnf
script-glyph = target "［＃「" target "」は" keyword "］"
keyword      = "上付き小文字" / "下付き小文字" / "行右小書き" / "行左小書き"
```

```text
ｅ２［＃「２」は上付き小文字］
Ｈ２［＃「２」は下付き小文字］
あい［＃「い」は行右小書き］
あい［＃「い」は行左小書き］
```

Unlike 太字/斜体 there is **no bare inline range and no `ここから`/`ここで`
block range** for these families: the official guide gives only the
forward-reference form, and the corpus attests only it.

## Parameters

- **kind** — one of 上付き小文字 / 下付き小文字 / 行右小書き / 行左小書き.
- **target** — the single quoted run to treat. As with §6.12, the form names
  exactly one target; a multi-quote body is not a recognised shape and degrades
  (§6.14).

## Semantics

- Each form resolves its target by the look-back rule of §7.5 and yields an
  `emphasis` node over that run. It is an **inline** construct.
- The node carries the kind so serialization (§7.6) can reconstruct the source
  directive, including the redundant preceding target copy, byte-exact.
- Reference rendering (§8):
  - 上付き小文字 → `<sup class="aozora-uwatsuki">…</sup>`
  - 下付き小文字 → `<sub class="aozora-shitatsuki">…</sub>`
  - 行右小書き → `<span class="aozora-kogaki-right">…</span>`
  - 行左小書き → `<span class="aozora-kogaki-left">…</span>`

  The `<sup>` / `<sub>` elements give super- and sub-script their conventional
  horizontal rendering; the 小書き families, which are positional in vertical
  writing, render as side `<span>`s a stylesheet can place. None collides with
  the `<b>` / `<i>` of §6.12, the `<em>` of bouten (§6.2), or the `<ruby>` of
  §6.1.

## Error conditions

- **Target with no referent** — a `は…` directive whose quoted target does not
  occur in the preceding text has no run to treat; it is not recognised as this
  family and degrades to a generic annotation (§6.14), so no input is lost
  (parallel to the 太字/斜体 rule, §6.12).

## Conformance vectors

`superscript_forward`, `subscript_forward`, `side_glyph_right`,
`side_glyph_left` (under `conformance/vectors/`).
