# 6.10 Headings (見出し)

## Synopsis

A heading marks a run of text as a structural title. Aozora distinguishes
three **levels** (大 / 中 / 小 見出し) and, orthogonally, three **styles** —
standard, *same-line* (同行, the title shares its line with the body that
follows) and *window* (窓, an inset title). Style and level combine freely:
同行中見出し, 窓小見出し, and so on. Headings are most often expressed as a
**forward-reference hint** that promotes or marks a quoted run.

## Notation

A heading is written in one of three forms — a forward-reference **hint**, a
**paired** delimiter, or a **block** (`ここから…`) delimiter:

```text
　　　　序［＃「序」は大見出し］                           ← hint (forward-reference)
萩原朔太郎［＃「萩原朔太郎」は同行中見出し］　二十年の友。…  ← hint (same-line)
［＃窓小見出し］チベット探検の動機［＃窓小見出し終わり］     ← paired
［＃ここから中見出し］本文…［＃ここで中見出し終わり］       ← block
```

```abnf
heading-hint         = LBRACK HASH LQUOTE target RQUOTE %s"は" [ style ] level %s"見出し" RBRACK
heading-paired-open  = LBRACK HASH [ style ] level %s"見出し" RBRACK
heading-paired-close = LBRACK HASH [ style ] level %s"見出し終わり" RBRACK
heading-block-open   = LBRACK HASH %s"ここから" [ style ] level %s"見出し" RBRACK
heading-block-close  = LBRACK HASH %s"ここで" [ style ] level %s"見出し終わり" RBRACK
level                = %s"大" / %s"中" / %s"小"
style                = %s"同行" / %s"窓"
```

The optional *style* prefix selects 同行 (same-line) or 窓 (window); its
absence is the standard style. Style and level pair freely
(`…は同行中見出し`, `［＃窓小見出し］`, `［＃ここから大見出し］`). The 窓 style
appears almost exclusively in the paired form.

## Parameters

- **target** — (hint form) the quoted run promoted or marked as a heading
  (resolved by §7.5). The paired and block forms have no quoted target: the
  content delimited between the opener and closer is the heading text.
- **level** — 大 / 中 / 小.
- **style** — standard (no prefix), 同行 (same-line), or 窓 (window).

## Semantics

- A heading hint resolves its target (§7.5) and carries the level and style. It
  **promotes** that run to a `heading` node when the target is the bare line
  immediately preceding the directive — the run is pulled out of the flow and
  becomes the heading. When the referent is not such a clean preceding line, the
  hint is retained inline (a `heading-hint` marker) rather than promoted, so no
  run is mis-titled and no input is lost. The quoted target is matched
  **ruby-stripped** (§7.5), so a title carrying ruby —
  `両頭《りやうとう》の蛇《へび》` — is still recognised by its base text
  `両頭の蛇` (retained as a hint, since a ruby-bearing run is not a clean bare
  line). The 同行 (same-line) and 窓 styles in
  practice run into the body on their own line, so they are typically retained
  as hints; the standard style with a bare title line is the usual promotion
  case.
- A **paired** (`［＃<style?><level>見出し］ … ［＃<style?><level>見出し終わり］`)
  or **block** (`［＃ここから…見出し］ … ［＃ここで…見出し終わり］`) opener/closer
  pair (§7.1) **delimits** its content explicitly and yields a `heading` node
  wrapping that content — no forward reference or promotion is involved. Pairing
  is by the heading family at a matching level and style; a closer of a different
  level or style than its opener is a mismatch (§7.2). The 窓 style uses the
  paired form almost exclusively; the standard and 同行 styles occur in all three
  forms.
- Reference rendering (§8): a promoted standard 大 / 中 / 小 heading is
  `<h1>`–`<h3>` (`class="aozora-heading aozora-heading-<large|medium|small>"`);
  the 同行 / 窓 styles add an `aozora-heading-<same-line|window>` modifier (and
  窓 renders as a styled `<div>` rather than an outline `<hN>`); an unpromoted
  hint is a hidden inline marker (`<span class="aozora-heading-hint"
  data-level=… data-style=… data-target=… hidden>`), with `data-style` present
  only for a non-standard style. The precise tag is part of the reference
  mapping (§8.2), not mandated. The paired and block forms render the same
  heading element (`<hN>` / `<div>` with the level and style classes) wrapping
  their delimited content directly (phrasing content, not a nested paragraph).
- Serialization reconstructs the directive (the hint's literal target, or the
  paired / block opener and closer around the content) byte-exact (§7.6).

## Error conditions

- A heading hint whose target is absent from the look-back degrades to a
  generic annotation (§6.14), as with other forward references (§7.5).

## Conformance vectors

`heading`, `heading_hint`, `heading_ruby_hint`, `heading_promoted`,
`heading_same_line`, `heading_window`, `heading_paired_window`, `heading_block`.
