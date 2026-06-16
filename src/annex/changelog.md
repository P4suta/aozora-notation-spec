# Annex E. Change log

The authoritative change log is `CHANGELOG.md` at the repository root; this
annex mirrors it for readers of the rendered book.

## Draft v0.1 (unreleased)

**Added** — the initial framework (§§1–5, 7–12) and annexes; normative
notation families (ruby, bouten/bousen including the range form, 左に side,
and the rare 鎖線 / 破線 / 黒三角傍点 variants, tate-chu-yoko, gaiji, the
layout containers including the 折り返し字下げ hanging form and the 字詰め
line-width form, keigakomi, warichu, breaks, headings (大/中/小 levels ×
standard/同行/窓 styles, in forward-reference, paired, and block forms),
illustrations, bold/italic (太字・斜体), input-editor annotations);
the families the official guide treats as provisional, documented with their
notation (kunten saidoku-moji, 中央揃え / 地寄せ, 表・段組); the machine-readable
conformance suite (schema, vectors, runner contract); and the decision
records under `docs/adr/`.

Versioning: the specification is `vMAJOR.MINOR`; a normative change that can
break a conforming processor bumps MAJOR. See §10.5 for how provisional
families graduate to `must` coverage.
