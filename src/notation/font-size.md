# 6.17 Character size (文字サイズ)

## Synopsis

A character-size directive shifts a run's type size by a relative number of
stages, larger or smaller, without changing its weight (§6.12) or position
(§6.16). It is the typographic device the official guide records for editor's
notes, mathematics, and emphasis where weight is unsuitable
([AOZORA-ANNOTATION], `etc.html`).

## Notation

Two forms occur. The **forward-reference** form (particle `は`) resizes a
single run:

```abnf
font-size  = target "［＃「" target "」は" size-spec "］"
size-spec  = magnitude %s"段階" direction %s"文字"
magnitude  = 1*DIGIT          ; ASCII or full-width, 1..127
direction  = %s"大きな" / %s"小さな"
```

```text
見出し［＃「見出し」は2段階大きな文字］
注記［＃「注記」は1段階小さな文字］
```

The **block** form resizes the enclosed paragraphs:

```abnf
font-size-open  = LBRACK HASH %s"ここから" size-spec RBRACK
font-size-close = LBRACK HASH %s"ここで" direction %s"文字終わり" RBRACK
```

```text
［＃ここから2段階大きな文字］
大きく組まれた段落。
［＃ここで大きな文字終わり］
```

The block closer drops the magnitude — it names only the **direction**
(`大きな` / `小さな`); the opener's stage count is authoritative.

### Absolute sizes (特大 / 大 / 中 / 小文字)

A second, **absolute** scale names a fixed size rather than a relative stage —
`特大文字` > `大文字` > `中文字` > (body) > `小文字`. The forward-reference form
is corpus-attested (`「X」は小文字`); unlike the relative scale it takes no
magnitude.

```abnf
abs-size    = target "［＃「" target "」は" abs-keyword "］"
abs-keyword = %s"特大文字" / %s"大文字" / %s"中文字" / %s"小文字"
```

```text
ヱ［＃「ヱ」は小文字］
```

The absolute `小文字` is a *size*, distinct from the script-glyph
`上付き小文字` / `下付き小文字` (§6.16) whose keyword it is a substring of: the
recogniser matches the whole `は…` body, so the two never collide. (The
single-work postfix headline forms `［＃大文字］` / `［＃大文字、太字］` apply the
same scale at the line scope; they are documented under the line directives.)

## Parameters

- **magnitude** — the number of stages, 1‥127. A leading run of ASCII or
  full-width digits; a missing or zero magnitude, or one that overflows the
  stage range, is not a recognised size change and degrades (§6.14).
- **direction** — `大きな` (larger, a positive stage count) or `小さな`
  (smaller, negative).
- **target** — the single quoted run to resize (as §6.12 / §6.16).

## Semantics

- The forward-reference form resolves its target by the look-back rule of §7.5
  and yields an `emphasis` node carrying the signed stage count. It is an
  **inline** construct.
- The block form pairs opener and closer by the `font-size` family (§7.1) and
  yields a **block** `container` node carrying the opener's signed stage count.
  Because the closer names only a direction, a 大きな opener closed by a 小さな
  closer is **not** flagged as a family mismatch; the corpus never mixes them.
- Reference rendering (§8): the inline form is
  `<span class="aozora-font-larger" data-steps="N">…</span>` (大きな) /
  `<span class="aozora-font-smaller" …>` (小さな); the block form is
  `<div class="aozora-container aozora-container-font-larger" data-steps="N">…</div>`
  (resp. `aozora-container-font-smaller`), where `N` is the (positive)
  magnitude. A stylesheet maps the stage count to a size.
- Serialization (§7.6) reconstructs `［＃「X」はN段階大きな/小さな文字］`. A
  full-width magnitude canonicalises to ASCII; the mapping is idempotent, so
  the parse∘serialize fixed point holds after the first pass.
- The **absolute** forward form yields an `emphasis` node carrying the absolute
  size; reference rendering (§8) is `<span class="aozora-font-{slug}">…</span>`
  with slug `font-extra-large` / `font-large` / `font-medium` / `font-small`.
  Serialization reconstructs `［＃「X」は…文字］` byte-exact.

## Error conditions

- **Target with no referent** — a `は…文字` directive whose quoted target does
  not occur in the preceding text has no earlier run to resize, so the quoted
  target is itself the resized run: a **self-contained** forward reference,
  rendered `<span data-steps>`. Serialization reconstructs the directive
  byte-exact (§7.6).
- **Malformed magnitude** — a zero, missing, or out-of-range stage count
  degrades (§6.14); no dedicated diagnostic is defined.

## Conformance vectors

`font_size_larger_forward`, `font_size_smaller_forward`, `font_size_block`,
`font_size_larger_no_referent`, `font_size_absolute_small_forward` (under
`conformance/vectors/`).
