# Annex E. Change log

The authoritative change log is `CHANGELOG.md` at the repository root; this
annex mirrors it for readers of the rendered book.

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
illustrations, bold/italic (太字・斜体), input-editor annotations);
the families the official guide treats as provisional, documented with their
notation (the block centring form, the 段組
sub-directives); the machine-readable
conformance suite (schema, vectors, runner contract); and the decision
records under `docs/adr/`.

Versioning: the specification is `vMAJOR.MINOR`; a normative change that can
break a conforming processor bumps MAJOR. See §10.5 for how provisional
families graduate to `must` coverage.
