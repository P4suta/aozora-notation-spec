# 6.1 Ruby (ルビ)

## Synopsis

Ruby attaches a small **reading** (furigana) to a **base** run of text. It is
the most common construct in the corpus.

## Notation

```abnf
ruby = [ BAR base ] RUBY-OPEN reading RUBY-CLOSE   ; ［｜］ base 《 reading 》
```

The reading is written in double angle brackets `《 … 》` immediately after
the base. The base is identified in one of two ways:

- **Explicit base** — a `｜` (U+FF5C) marks where the base begins; the base is
  the run from `｜` up to `《`:

  ```text
  ｜青梅《おうめ》
  ｜後手々々《ごてごて》
  ```

- **Implicit base** — with no `｜`, the base is the maximal run of
  *same-class* characters immediately preceding `《` (see Parameters):

  ```text
  青空《あおぞら》
  ```

## Parameters

- **base** — the run the reading applies to.
  - For the **explicit** form, the base is exactly the text between `｜` and
    `《`.
  - For the **implicit** form, the base is the maximal preceding run of one
    character class — a processor **MUST** take a trailing run of kanji (CJK
    ideographs); it **MAY** extend the implicit base over other single
    classes (kana, Latin) as the official guide allows, but **MUST** stop at a
    class boundary or at any preceding notation construct. When the intended
    base spans classes, the author uses the explicit `｜` form; this is why
    `｜` exists.
- **reading** — the furigana text inside `《 … 》`; it is plain text and
  **MUST NOT** itself contain a ruby (see Error conditions).

## Semantics

- A ruby span yields a `ruby` node whose span covers the whole construct
  (from `｜` or the implicit base start, through the closing `》`), carrying
  the base and the reading.
- Reference rendering (§8) is HTML5 `<ruby>` with `<rp>` fallback
  parentheses:

  ```html
  <ruby>青梅<rp>(</rp><rt>おうめ</rt><rp>)</rp></ruby>
  ```

- Serialization (§7) reconstructs the source form, including the `｜` when the
  base was explicit, so the round-trip is byte-exact.
- An adjacent **`《《…》》`** **is** two ruby openers — a
  [nested ruby](../diagnostics.md#nested-ruby) error, not a single construct.
  The double-angle quotation notation (§6.15) is the distinct `≪…≫`.

## Error conditions

- **Empty reading with explicit base** — `｜青梅《》` raises
  [`empty-ruby-reading`](../diagnostics.md#empty-ruby-reading) (error) and
  degrades to plain text. A bare `《》` with no `｜` is literal text and is
  **not** flagged.
- **Nested ruby** — a reading body that opens another ruby
  (`｜漢《か《ん》じ》`) raises
  [`nested-ruby`](../diagnostics.md#nested-ruby) (error); the outer ruby is
  parsed best-effort and the label points at the inner `《`.
- **Unclosed `《`** — a reading with no closing `》` raises
  [`unclosed-bracket`](../diagnostics.md#unclosed-bracket); the region
  degrades to plain text.

## Conformance vectors

`ruby_explicit`, `ruby_implicit`, `empty-ruby-reading`, `nested-ruby`,
`mixed_ruby_bouten` (under `conformance/vectors/`).
