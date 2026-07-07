# 6.12 Bold and Italic (太字・斜体)

## Synopsis

太字 (bold / ゴシック) and 斜体 (italic) mark a run for emphasis as a change of
**weight** or **slant**, rather than the dots or lines of bouten (§6.2). The
two form one family with a 太字/斜体 split, parallel to the 点/線 split of
bouten.

## Notation

Three forms produce emphasis. Unlike bouten the particle is `は` (not `に`), and
the family has both a bare inline range and a `ここから`/`ここで` block range.

- **Forward reference** — quote the target; the emphasis applies to the most
  recent preceding occurrence (§7.5):

  ```text
  作者附記［＃「作者附記」は太字］
  序文［＃「序文」は斜体］
  ```

- **Inline range** — a bare opener and matching closer wrap the run directly,
  within a line. This is the most common form in the corpus:

  ```abnf
  emphasis-range = directive 1*element directive   ; ［＃太字］ … ［＃太字終わり］
  ```

  ```text
  本文［＃太字］註［＃太字終わり］。
  値は［＃斜体］ｅ［＃斜体終わり］である。
  ```

- **Block range** — the `ここから`/`ここで…終わり` form wraps one or more whole
  paragraphs; the opener sits on its own line:

  ```text
  ［＃ここから太字］
  強調する段落。
  ［＃ここで太字終わり］
  ```

## Parameters

- **weight** — 太字 (bold) or 斜体 (italic). The weight is what pairing checks
  for the range forms (§7.2): a 太字 opener pairs with a 太字 closer.
- **target** — for the forward-reference form, the single quoted run to
  emphasise. The form names exactly one target; a multi-quote body
  (`「A」「B」は太字`) is not a recognised emphasis shape and degrades (§6.14).

## Semantics

- The forward-reference form resolves its target by the look-back rule of §7.5
  and yields an `emphasis` node over that run. It is an **inline** construct.
- The inline range form pairs opener and closer by **weight** (§7.1) and is an
  **inline** construct (§7.3): in the corpus it never spans a line, and
  rendering does not introduce block structure. It yields a `container` node
  (weight-tagged `bold` / `italic`) over the enclosed content.
- The block range form pairs the same way but is a **block** construct: it
  wraps the enclosed paragraphs in a weight-tagged `container` node.
- Reference rendering (§8): the inline forms are `<b class="aozora-futoji">…</b>`
  (太字) and `<i class="aozora-shatai">…</i>` (斜体) — presentational elements
  distinct from the `<em>` of bouten, so the two families never collide on one
  tag. The block form is a block container, `<div class="aozora-container
  aozora-container-futoji">…</div>` (resp. `aozora-container-shatai`), so the
  wrapped paragraphs nest validly.
- Serialization (§7.6) reconstructs the source form — the `は` forward
  reference (including a redundant preceding target copy), the bare inline
  range, or the `ここから`/`ここで` block range — byte-exact.

## Error conditions

- **Weight mismatch (range)** — a 太字 opener closed by a 斜体 closer, or
  vice-versa, raises
  [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  (error); the run is keyed to the opener's weight (recovery).
- **Unclosed range** — an opener with no closer is handled per
  [`unclosed-bracket`](../diagnostics.md#unclosed-bracket).
- **Target with no referent (forward reference)** — a `は太字` / `は斜体`
  directive whose quoted target does not occur in the preceding text has no
  earlier run to emphasise, so the quoted target is itself the styled run: a
  **self-contained** forward reference, rendered `<b>` / `<i>`. `ゴシック体` is a
  **first-class gothic construct** (§6.6), distinct from `太字` — the corpus uses
  them in disjoint works and gothic is a typeface family, not a bold weight — so
  the parser preserves its spelling and never folds it to `太字`; serialization
  reconstructs `［＃「X」はゴシック体／太字／斜体］` byte-exact (§7.6). The vanishing
  `ゴチック` variant degrades (§6.14) with a lint suggesting `ゴシック体`.
  (Contrast the multi-quote body above, which is still unrecognised and
  degrades, §6.14.)

## Conformance vectors

`bold_inline`, `italic_inline`, `bold_block`, `italic_block`, `bold_forward`,
`italic_forward`, `emphasis_mixed`, `bold_forward_no_referent`,
`italic_forward_no_referent`, `bold_forward_gothic_no_referent` (under
`conformance/vectors/`).
