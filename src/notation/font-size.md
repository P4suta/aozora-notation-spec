# 6.17 Character size (文字サイズ)

## Synopsis

A character-size directive shifts a run's type size by a relative number of
stages, larger or smaller, without changing its weight (§6.12) or position
(§6.16). It is the typographic device the official guide records for editor's
notes, mathematics, and emphasis where weight is unsuitable
([AOZORA-ANNOTATION], `etc.html`).

## Notation

The **forward-reference** form (particle `は`) is the corpus-attested and
normative form:

```abnf
font-size = target "［＃「" target "」は" magnitude %s"段階" direction %s"文字" "］"
magnitude = 1*DIGIT          ; ASCII or full-width, 1..127
direction = %s"大きな" / %s"小さな"
```

```text
見出し［＃「見出し」は2段階大きな文字］
注記［＃「注記」は1段階小さな文字］
```

A `ここから…段階大きな文字 … ここで大きな文字終わり` block form also occurs in
the corpus; its closer drops the magnitude and pairs by direction. Its pairing
semantics are not yet pinned and it remains deferred (§10.5).

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
- Reference rendering (§8) is
  `<span class="aozora-font-larger" data-steps="N">…</span>` for 大きな and
  `<span class="aozora-font-smaller" data-steps="N">…</span>` for 小さな, where
  `N` is the (positive) magnitude. A stylesheet maps the stage count to a size.
- Serialization (§7.6) reconstructs `［＃「X」はN段階大きな/小さな文字］`. A
  full-width magnitude canonicalises to ASCII; the mapping is idempotent, so
  the parse∘serialize fixed point holds after the first pass.

## Error conditions

- **Target with no referent** — a `は…文字` directive whose quoted target does
  not occur in the preceding text degrades to a generic annotation (§6.14).
- **Malformed magnitude** — a zero, missing, or out-of-range stage count
  degrades (§6.14); no dedicated diagnostic is defined.

## Conformance vectors

`font_size_larger_forward`, `font_size_smaller_forward` (under
`conformance/vectors/`).
