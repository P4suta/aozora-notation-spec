# Annex E. Change log

The authoritative change log is `CHANGELOG.md` at the repository root; this
annex mirrors it for readers of the rendered book.

## Draft v0.2 (unreleased)

**Added** — corpus-attested notation forms that an earlier revision missed,
each grounded in a fresh `P4suta/aozorabunko_text` frequency survey and pinned
with a conformance vector:

- the **改行天付き hanging indent** `［＃ここから改行天付き、折り返してM字下げ］`
  (and its single-line form) — first line flush to the head, wrapped lines
  indent by M (§6.6; the corpus' single most common compound-indent form,
  ~8k occurrences). Vectors `head_flush_wrap_indent`, `head_flush_single`.
- the **head-anchored single-line indent** `［＃天からN字下げ］` (§6.6). Vector
  `indent_from_top`.
- the **bare-range 行右/行左小書き** `［＃行右小書き］…［＃行右小書き終わり］`
  (§6.16; ~4k paired occurrences each). Vectors `side_glyph_right_range`,
  `side_glyph_left_range`.
- the **bare-range character-size** `［＃N段階小さな文字］…［＃小さな文字終わり］`
  (§6.17; ~9k paired occurrences, more common than the block form). Vector
  `font_size_bare_range`.
- the **input-editor `はママ` (sic) and `は底本では「…」` textual-divergence
  notes** (§6.14; ~3k and ~7k occurrences) — the `はママ` shape replaces the
  earlier, corpus-unattested `に「ママ」の注記` ABNF. Vectors `correction_sic`,
  `correction_textual_note`.
- the **composed-glyph gaiji** `※［＃「X」の「Y」に代えて「Z」、第N水準P-R-C］`
  (§6.4; ~2.8k occurrences) — the whole pre-address body is the description,
  serialized verbatim. Fixes a round-trip data loss that dropped everything
  after the first quote. Vector `gaiji_composed_glyph`.
- the **illustration pixel-size note** `［＃挿絵（file、横W×縦H）入る］`
  (§6.11) — split off the path so `<img src>` stays clean and `width`/`height`
  are supplied. Vector `sashie_dimensions`.

**Changed** — §1.3 promoted to v0.2 and the stale "deferred families" note
removed (every §6 family now carries a vector); §10.5 records compound
forward-references (`「X」は縦中横、行右小書き`) as a preserved-verbatim boundary.

## Draft v0.1 (unreleased)

**Added** — the initial framework (§§1–5, 7–12) and annexes; normative
notation families (ruby including the left-side ruby (saidoku-moji building
block) and the left-side annotation 注記, bouten/bousen including the range form, 左に side,
and the rare 鎖線 / 破線 / 黒三角傍点 variants, tate-chu-yoko, gaiji, the
layout containers including the 折り返し字下げ hanging form, the 字詰め
line-width form, the single-line centring marker and the combined 字下げ＋ページ
左右中央 form, tables / columns (表・段組
block layout containers), keigakomi, warichu, breaks, headings (大/中/小 levels ×
standard/同行/窓 styles, in forward-reference, paired, and block forms),
illustrations, bold/italic (太字・斜体), input-editor annotations,
double-angle quotation (二重山括弧, ≪…≫ → 《…》), the superscript /
subscript / side-glyph families (§6.16: 上付き小文字・下付き小文字・
行右小書き・行左小書き), the character-size change (§6.17:
`N段階大きな/小さな文字`, both the forward-reference and `ここから/ここで`
block forms), and horizontal writing (§6.18: 横組み, inline `は横組み` and the
`ここから/ここで` block));
the bundled illustration caption `挿絵（file）「caption」入る` (§6.11);
the families the official guide treats as provisional or that this revision has
not yet pinned, documented with their notation (the block centring form, the
段組 sub-directives, the left-ruby block form, and the standalone caption
directive — see §10.5); the machine-readable
conformance suite (schema, vectors, runner contract); and the decision
records under `docs/adr/`.

**Changed** — recharacterized the double-angle quotation (二重山括弧, §6.15):
an earlier draft mis-described `《《…》》` as a "double-bracket bouten" selected
over ruby by leftmost-longest. The input encoding is `≪…≫` (U+226A/U+226B),
restored to the display form `《…》` (U+300A/U+300B); a literal `《《…》》` in
source is two ruby openers (a `nested-ruby` error). The `double_ruby` vector
is renamed `angle_quote`.

Versioning: the specification is `vMAJOR.MINOR`; a normative change that can
break a conforming processor bumps MAJOR. See §10.5 for how provisional
families graduate to `must` coverage.
