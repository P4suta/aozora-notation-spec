# Annex E. Change log

The authoritative change log is `CHANGELOG.md` at the repository root; this
annex mirrors it for readers of the rendered book.

## Draft v0.1.0 (unreleased) <!-- x-release-please-version -->

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

Versioning: the specification follows [Semantic Versioning](https://semver.org).
While pre-1.0 (`0.x`), a normative change that can break a conforming processor
bumps the minor; backward-compatible additions and fixes bump the patch. See
§10.5 for how provisional families graduate to `must` coverage.
