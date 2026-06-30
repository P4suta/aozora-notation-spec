# 6.4 Gaiji (外字)

## Synopsis

A *gaiji* (外字, "external character") is a glyph outside the assumed
character repertoire — a rare kanji, a special kana, a symbol. It is written
as a `※［＃…］` reference carrying a human description and, where possible, a
machine address (a JIS X 0213 men-ku-ten or a Unicode code point) that
resolves it to an actual character.

## Notation

```abnf
gaiji-ref = REFMARK directive          ; ※［＃ description 〔、address〕 ］
```

```text
※［＃「てへん＋劣」、第3水準1-84-77］     ← JIS X 0213 men-ku-ten
※［＃「口＋世」、U+546D、123-4］          ← Unicode reference (+ provenance)
※［＃「土へん＋竒」、123-4］              ← description only (provenance locator)
※［＃二の字点、1-2-22］                  ← named, with men-ku-ten
※［＃二重かっこ開く］                    ← named, dictionary-resolved (no address)
```

A description in `「…」` quotes is recognised on its own; a **bare (unquoted)
description with no address** is recognised only when it names a known
dictionary glyph (`※［＃二重かっこ開く］` → `｟`, the same glyph as the upstream
`始め二重括弧` entry), so an ordinary `［＃…］` directive is not mistaken for a
gaiji. The canonical serialization quotes the description (`※［＃「二重かっこ開く」］`).
Vector: `gaiji_double_paren`.

A bare **`ローマ数字N`** description (`※［＃ローマ数字17］`) is recognised the same
way, with the glyph **composed** rather than looked up: the numeral `N` is spelled
from the U+2160 (uppercase) / U+2170 (lowercase, `ローマ数字N小文字`) single-letter
Roman-numeral blocks — `17` → `ⅩⅤⅠⅠ` (`Ⅹ`+`Ⅴ`+`Ⅰ`+`Ⅰ`) — because values ≥ 13 have
no single JIS X 0213 cell (the corpus pairs those with a page-line locator, not an
address). It resolves like any other gaiji and serialises to the canonical quoted
form (`※［＃「ローマ数字17」］`). Vector: `roman_numeral`.

The accent form `〔…〕` (§4.3, [Annex A](../annex/accent-table.md)) and the
iteration marks `／＼` / `／″＼` are related glyph-encoding notations covered
in [Annex B](../annex/gaiji.md).

### Standalone form (tolerant)

Some 凡例 write the same `［＃description〔、address〕］` reference **without**
the leading `※` — a standalone descriptive note rather than an inline
insertion. A conforming processor SHOULD recognise it as a `gaiji` node when
the body carries a resolvable description or a mencode / page-line address (so
an ordinary `［＃…］` note is not mistaken for one), and serialise it back
without a `※`. This is a corpus-attested tolerant extension, not part of the
core `external_character.html` notation; the reference-mark form above is
canonical. Vector: `standalone_gaiji`.

## Parameters

- **description** — the text before the first `、`: a radical composition
  (`木＋世`), a name (`二の字点`), or a directly-typed character.
- **address** — an optional `、`-separated trailer: a JIS X 0213 men-ku-ten
  (`第N水準P-R-C` / `面-区-点`), a `U+XXXX` code point, and/or a page-line
  provenance locator.

## Semantics

- The reference yields a `gaiji` node whose span covers the whole
  `※［＃…］`. Resolution order is normative ([Annex B](../annex/gaiji.md)):
  explicit `U+XXXX`, then men-ku-ten, then a named description (including the
  composed `ローマ数字N` numerals), then a single-character description.
- On success the node carries the resolved scalar (or combining sequence);
  reference rendering (§8) emits that character (optionally wrapped for
  styling).
- Serialization reconstructs the `※［＃…］` reference byte-exact (§7.6); a
  resolved gaiji round-trips to its source form, never to the bare glyph.

## Error conditions

- **Unresolved** — a reference that resolves to neither Unicode nor JIS X
  0213 raises [`unresolved-gaiji`](../diagnostics.md#unresolved-gaiji)
  (warning) and falls back to the description text.

## Conformance vectors

`gaiji`, `gaiji_double_paren`, `roman_numeral`, `unresolved-gaiji`,
`accent-decomposition-applied`.
