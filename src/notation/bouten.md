# 6.2 Bouten and Bousen (傍点・傍線)

## Synopsis

Bouten (傍点) are emphasis **dots** set beside characters in vertical text —
the Japanese equivalent of italic/bold for emphasis. Bousen (傍線) are the
same idea with a **line**. The two form one family with a 点/線 split.

## Notation

Three forms produce emphasis.

- **Forward reference** — quote the target; the emphasis applies to the most
  recent preceding occurrence (§7.5):

  ```text
  ［＃「平和」に傍点］
  平和［＃「平和」に傍点］      ← redundant explicit copy (also accepted)
  ```

- **Range** — a bare opener and matching closer wrap the run directly. Note
  there is **no** `ここから`/`ここで`; those prefixes are for block layout and
  bold/italic, not bouten:

  ```abnf
  bouten-range = directive 1*element directive   ; ［＃<kw>］ … ［＃<kw>終わり］
  ```

  ```text
  彼は［＃傍点］必ず［＃傍点終わり］来る
  ［＃二重傍線］乙［＃二重傍線終わり］
  ［＃左に傍線］丙［＃左に傍線終わり］
  ```

- **Left side** — an optional `左に` prefix places the marks on the left of
  the vertical base text (`［＃左に傍線］…`, `［＃「X」の左に傍点］`).

## Parameters

- **variant** — one of the fourteen keywords of [Annex C.4](../annex/slugs.md);
  nine 点 and five 線. The rare 鎖線 / 破線 (線) and 黒三角傍点 (点) are official
  but corpus-sparse; a processor renders them like any other variant where it
  has a glyph, otherwise degrading them (§6.14).
- **family** — 点 (dots) or 線 (line). The family is what pairing checks for
  the range form (§7.2).
- **position** — right (default) or left (`左に`).
- **target** — for the forward-reference form, the quoted run to emphasise.

## Semantics

- The forward-reference form resolves its target by the look-back rule of
  §7.5 and yields a `bouten` node over that run.
- The range form pairs opener and closer by **family** (§7.1) and yields a
  `container` node (family-tagged `bouten-range`) over the enclosed content.
  It is an **inline** construct (§7.3): in the corpus it never spans a line,
  and rendering does not introduce block structure.
- Reference rendering (§8) is `<em class="aozora-bouten aozora-bouten-<slug>
  aozora-bouten-<side>">…</em>`, the same markup for both forms so a
  stylesheet treats them identically.
- Serialization (§7.6) reconstructs the source form, including a redundant
  forward-reference target copy and a `左に` prefix, byte-exact.

## Error conditions

- **Family mismatch (range)** — a 点 opener closed by a 線 closer, or
  vice-versa, raises
  [`mismatched-bouten-container`](../diagnostics.md#mismatched-bouten-container)
  (error); the run is keyed to the opener's variant (recovery). A
  same-family variant difference (e.g. `白丸傍点` closed by `丸傍点終わり`) is
  tolerated.
- **Ambiguous target (forward reference)** — a quoted target occurring more
  than once in the look-back raises
  [`bouten-target-ambiguous`](../diagnostics.md#bouten-target-ambiguous)
  (warning).
- **Unclosed range** — an opener with no closer is handled per
  [`unclosed-bracket`](../diagnostics.md#unclosed-bracket).

## Conformance vectors

`bouten-target-ambiguous`, `bouten_range`, `bouten_chain_line`,
`bouten_black_triangle`, `mismatched-bouten-container`,
`mixed_ruby_bouten`.
