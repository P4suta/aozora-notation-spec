# Change log

All notable changes to this specification are recorded here. This document
follows [Keep a Changelog](https://keepachangelog.com/) conventions and the
specification is versioned per [Semantic Versioning](https://semver.org).
**Pre-1.0 (`0.x`):** a normative change that can break a conforming processor
bumps the **minor** (`0.x → 0.(x+1).0`); backward-compatible additions and fixes
bump the **patch**. At `1.0.0` the contract switches to MAJOR-for-breaking.

## [Unreleased]

### Added

- Initial framework: introduction, conventions (RFC 2119), document model and
  encoding, pre-processing (normalization), lexical syntax (ABNF), structural
  processing model, reference rendering, diagnostics, conformance, security,
  references, and annexes.
- Normative notation families: ruby (incl. the left-side ruby that, with
  okurigana and a return mark, composes a saidoku-moji 再読文字), bouten/bousen
  (including the range form, 左に position, and the rare 鎖線 / 破線 /
  黒三角傍点 variants), tate-chu-yoko, gaiji
  (men-ku-ten / U+XXXX / description fallback + 〔…〕 accent decomposition),
  layout containers (字下げ — incl. the 折り返し字下げ hanging form — /
  地付き / 地上げ, block and single-line; 字詰め line-width, block; the
  single-line centring marker ページの左右中央 / 中央揃え),
  tables and columns (表 / N段組, block layout containers),
  keigakomi, warichu, breaks,
  headings (大/中/小 levels × standard/同行/窓 styles; forward-reference
  promotion to `<h1>`–`<h3>`, plus paired and block delimited forms),
  illustrations, bold / italic (太字・斜体 — forward-reference, bare inline
  range, and ここから block range), input-editor annotations, and double-angle
  quotation (二重山括弧, input `≪…≫` → display `《…》`).
- Families the official guide treats as provisional, documented with their
  notation pending full normative text: the
  block centring form, margined right-alignment (地寄せ), and the table/column
  sub-directives (上段/下段, 段間に罫).
- Machine-readable conformance test-vector suite (`conformance/vectors/`) with
  its JSON Schema and runner contract.
- Decision records under `docs/adr/` for normative choices made where the
  official 注記一覧 is silent or ambiguous.

### Changed

- Recharacterized the double-angle quotation (二重山括弧, §6.15). An earlier
  draft described `《《…》》` as a "double-bracket bouten" construct selected over
  ruby by the leftmost-longest rule. That was incorrect: the input encoding is
  `≪…≫` (U+226A / U+226B), restored to the display form `《…》`
  (U+300A / U+300B), and a literal `《《…》》` in source is two ruby openers
  (a `nested-ruby` error). The `double_ruby` conformance vector is renamed
  `angle_quote`.
