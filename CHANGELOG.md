# Change log

All notable changes to this specification are recorded here. This document
follows [Keep a Changelog](https://keepachangelog.com/) conventions; the
specification itself is versioned `vMAJOR.MINOR` (a normative change that can
break a conforming processor bumps MAJOR).

## [Unreleased] — draft v0.1

### Added

- Initial framework: introduction, conventions (RFC 2119), document model and
  encoding, pre-processing (normalization), lexical syntax (ABNF), structural
  processing model, reference rendering, diagnostics, conformance, security,
  references, and annexes.
- Normative notation families: ruby, bouten/bousen
  (including the range form, 左に position, and the rare 鎖線 / 破線 /
  黒三角傍点 variants), tate-chu-yoko, gaiji
  (men-ku-ten / U+XXXX / description fallback + 〔…〕 accent decomposition),
  layout containers (字下げ — incl. the 折り返し字下げ hanging form — /
  地付き / 地上げ, block and single-line; 字詰め line-width, block),
  keigakomi, warichu, breaks,
  headings (大/中/小 levels × standard/同行/窓 styles; forward-reference
  promotion to `<h1>`–`<h3>`, plus paired and block delimited forms),
  illustrations, bold / italic (太字・斜体 — forward-reference, bare inline
  range, and ここから block range), and input-editor annotations.
- Families the official guide treats as provisional, documented with their
  notation pending full normative text: kunten saidoku-moji (再読文字),
  中央揃え / 地寄せ, and tables and columns (表・段組).
- Machine-readable conformance test-vector suite (`conformance/vectors/`) with
  its JSON Schema and runner contract.
- Decision records under `docs/adr/` for normative choices made where the
  official 注記一覧 is silent or ambiguous.
