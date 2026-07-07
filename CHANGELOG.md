# Change log

All notable changes to this specification are recorded here. This document
follows [Keep a Changelog](https://keepachangelog.com/) conventions and the
specification is versioned per [Semantic Versioning](https://semver.org).
**Pre-1.0 (`0.x`):** a normative change that can break a conforming processor
bumps the **minor** (`0.x → 0.(x+1).0`); backward-compatible additions and fixes
bump the **patch**. At `1.0.0` the contract switches to MAJOR-for-breaking.

## 0.1.0 (2026-07-07)


### ⚠ BREAKING CHANGES

* sync conformance vectors to aozora API naming

### Added

* §7.5 in-place forward-reference styling ([#49](https://github.com/P4suta/aozora-notation-spec/issues/49)) ([c4bc221](https://github.com/P4suta/aozora-notation-spec/commit/c4bc221c8a28b0da1d495affba4daddd9dd1c8c5))
* absolute font sizes 特大/大/中/小文字 (§6.17) ([#42](https://github.com/P4suta/aozora-notation-spec/issues/42)) ([d5930e9](https://github.com/P4suta/aozora-notation-spec/commit/d5930e9a5b77fd91f4accaf63139958a00847336))
* add compound indent line-layout vectors ([#12](https://github.com/P4suta/aozora-notation-spec/issues/12)) ([cf6a496](https://github.com/P4suta/aozora-notation-spec/commit/cf6a496886fbb0c9f3d1a4134e129143fd42349c))
* add 正字 composed-glyph gaiji vector ([#11](https://github.com/P4suta/aozora-notation-spec/issues/11)) ([177f0cb](https://github.com/P4suta/aozora-notation-spec/commit/177f0cb4a7960efdc6577316c5b63a4c7f459a1a))
* bare dictionary gaiji (二重かっこ) ([#33](https://github.com/P4suta/aozora-notation-spec/issues/33)) ([38e2149](https://github.com/P4suta/aozora-notation-spec/commit/38e214970850c1c93b314708f2ee9c76bdc57635))
* bare ローマ数字N gaiji composition (§6.4) ([#41](https://github.com/P4suta/aozora-notation-spec/issues/41)) ([3f44d0d](https://github.com/P4suta/aozora-notation-spec/commit/3f44d0de7c184c960041904fd2b4a5310d99f527))
* box-character enclosure (§6.7) ([#44](https://github.com/P4suta/aozora-notation-spec/issues/44)) ([9560321](https://github.com/P4suta/aozora-notation-spec/commit/95603214f7dff1375b57987905fd8dbaee36f3f9))
* canonicalize inline bouten to forward ([#16](https://github.com/P4suta/aozora-notation-spec/issues/16)) ([2dcae1c](https://github.com/P4suta/aozora-notation-spec/commit/2dcae1ce343723ef5583c504af7ae23cb8463c68))
* canonicalize inline emphasis to forward ([#15](https://github.com/P4suta/aozora-notation-spec/issues/15)) ([2dab45d](https://github.com/P4suta/aozora-notation-spec/commit/2dab45dc3ff1657c60d799e0b121709fbcb02dfa))
* canonicalize inline script/tcy to forward ([#17](https://github.com/P4suta/aozora-notation-spec/issues/17)) ([8f80949](https://github.com/P4suta/aozora-notation-spec/commit/8f80949f7df4ea1374d3ad14ce7ac4aab35ef9b5))
* **conformance:** add 10 corpus-attested vectors ([#5](https://github.com/P4suta/aozora-notation-spec/issues/5)) ([beaf571](https://github.com/P4suta/aozora-notation-spec/commit/beaf571f1d62bfb6bfc9f023a24891e2901dcf08))
* dotted-letter composition (§6.21) ([#47](https://github.com/P4suta/aozora-notation-spec/issues/47)) ([624743f](https://github.com/P4suta/aozora-notation-spec/commit/624743f8f1b8dab7a40fb1ab57e7c33896ecbf0f))
* emphasis CSS classes → reading romaji ([#13](https://github.com/P4suta/aozora-notation-spec/issues/13)) ([0175f08](https://github.com/P4suta/aozora-notation-spec/commit/0175f088f0409d350e1f1a8b476aa9e5a9860e53))
* **gaiji:** document standalone (no-mark) form ([#7](https://github.com/P4suta/aozora-notation-spec/issues/7)) ([c05c9f6](https://github.com/P4suta/aozora-notation-spec/commit/c05c9f6a5b086666fe8f3e798bcdab97e3720971))
* initial Aozora Bunko notation specification (draft v0.1) ([48e5e9a](https://github.com/P4suta/aozora-notation-spec/commit/48e5e9a5ba802aeb31541388664e530193092020))
* keigakomi inline 枠囲み + に particle ([#35](https://github.com/P4suta/aozora-notation-spec/issues/35)) ([f4833e7](https://github.com/P4suta/aozora-notation-spec/commit/f4833e7865eff0236e9617e1e3b9f8e454959ce3))
* left-side-ruby span pair note (§6.14) ([#46](https://github.com/P4suta/aozora-notation-spec/issues/46)) ([edece73](https://github.com/P4suta/aozora-notation-spec/commit/edece73865b686ec7cdf111a77fad58e117d1e7a))
* multi-clause dotted-letter selectors (§6.21) ([#48](https://github.com/P4suta/aozora-notation-spec/issues/48)) ([aa75af4](https://github.com/P4suta/aozora-notation-spec/commit/aa75af458b3cfa515efe1d887e6babdda01b6f8e))
* **notation:** §6.16–§6.18 new families + full vector de-circularisation ([#79](https://github.com/P4suta/aozora-notation-spec/issues/79)) ([#1](https://github.com/P4suta/aozora-notation-spec/issues/1)) ([8bc62ad](https://github.com/P4suta/aozora-notation-spec/commit/8bc62ada8c26119f53a2f37ae743faeaf885fa97))
* **notation:** add 傍記 marginal annotation ([#8](https://github.com/P4suta/aozora-notation-spec/issues/8)) ([16c39f4](https://github.com/P4suta/aozora-notation-spec/commit/16c39f4fda577e8ba73b5cb903084cd639edb848))
* **notation:** combined 字下げ＋ページ左右中央 + serialize amount fix ([680a3a8](https://github.com/P4suta/aozora-notation-spec/commit/680a3a84c29c361abdb8a54dc98c305592d827c3))
* **notation:** left-side ruby + saidoku-moji as composition (§6.5) ([5bf44f0](https://github.com/P4suta/aozora-notation-spec/commit/5bf44f01798a2fd648880e7c96aaa44550abe90f))
* **notation:** normative centring marker (§6.6) + tables/columns (§6.13) ([261028f](https://github.com/P4suta/aozora-notation-spec/commit/261028fa80d87ed950169b3e1241a6f0888a44d8))
* **notation:** normative paired/block heading forms (§6.10) ([d69a32f](https://github.com/P4suta/aozora-notation-spec/commit/d69a32fe98338ef3739a454f783f26e632f96d59))
* **notation:** normative 太字/斜体 (bold/italic) emphasis (§6.12) ([89fa3c8](https://github.com/P4suta/aozora-notation-spec/commit/89fa3c84df3ccc6f45034e680104f5e639fcee61))
* **notation:** normative 字詰め (line-width) layout container ([519732a](https://github.com/P4suta/aozora-notation-spec/commit/519732acbca05d95c5e7aa675d91c3c9ac6d666a))
* **notation:** normative 折り返し字下げ, rare bouten, heading promotion + vectors ([750667d](https://github.com/P4suta/aozora-notation-spec/commit/750667d6134131381cb057b9d5be642b40e52413))
* **notation:** recognise ruby-bearing heading targets ([#9](https://github.com/P4suta/aozora-notation-spec/issues/9)) ([d67c3c0](https://github.com/P4suta/aozora-notation-spec/commit/d67c3c01b59b519b991a3046b8363a14317ca7ab))
* **notation:** side annotation (注記) — promote from deferred ([7ae59b1](https://github.com/P4suta/aozora-notation-spec/commit/7ae59b13b63d0fe1566374db30d08387d56c8f02))
* promote [#78](https://github.com/P4suta/aozora-notation-spec/issues/78) compound indent + leaf markers ([#20](https://github.com/P4suta/aozora-notation-spec/issues/20)) ([c064e2d](https://github.com/P4suta/aozora-notation-spec/commit/c064e2d986f90902f84336078d169246eb496174))
* promote gothic; decline convention forms ([#52](https://github.com/P4suta/aozora-notation-spec/issues/52)) ([f02014d](https://github.com/P4suta/aozora-notation-spec/commit/f02014d6490cfe5390fb7511891f495f56ae3835))
* ruby-placement editorial notes (§6.14) ([#45](https://github.com/P4suta/aozora-notation-spec/issues/45)) ([3858175](https://github.com/P4suta/aozora-notation-spec/commit/3858175adfd9f2191b84076fda43b82b8c9dbcca))
* self-contained no-referent forward bouten ([#23](https://github.com/P4suta/aozora-notation-spec/issues/23)) ([0b9b7c3](https://github.com/P4suta/aozora-notation-spec/commit/0b9b7c379791aca24b78e764648a35c7a3230b1a))
* self-contained no-referent forward emphasis ([#22](https://github.com/P4suta/aozora-notation-spec/issues/22)) ([2195e8b](https://github.com/P4suta/aozora-notation-spec/commit/2195e8ba77661f90fdb72e4ddd67b1eb1e9745b7))
* self-contained no-referent forward heading ([#39](https://github.com/P4suta/aozora-notation-spec/issues/39)) ([ed72b9b](https://github.com/P4suta/aozora-notation-spec/commit/ed72b9bf4dbd252c20eb06478bed6795407789f8))
* single-line absolute font size (§6.6) ([#43](https://github.com/P4suta/aozora-notation-spec/issues/43)) ([012d31e](https://github.com/P4suta/aozora-notation-spec/commit/012d31e647975fdb7c48c6f432b3ef0508a89508))
* この行はゴシック体 single-line bold ([#37](https://github.com/P4suta/aozora-notation-spec/issues/37)) ([f86833f](https://github.com/P4suta/aozora-notation-spec/commit/f86833f74bfcec71c4be629d78bb59c6d034616b))
* 入力者注(N) numbered editor note ([#38](https://github.com/P4suta/aozora-notation-spec/issues/38)) ([d1e7351](https://github.com/P4suta/aozora-notation-spec/commit/d1e7351ca8588f400fcb010627f8d1094be5c532))
* 分数 fraction forward notation (§6.20) ([#40](https://github.com/P4suta/aozora-notation-spec/issues/40)) ([8428a67](https://github.com/P4suta/aozora-notation-spec/commit/8428a679def06e5cd06f1364043ec053569d5c06))


### Fixed

* **conformance:** de-circularise align-end close + offset round-trip ([cf8b8ab](https://github.com/P4suta/aozora-notation-spec/commit/cf8b8ab1a00facb45fb0235a274e7b9077c6ee91))
* **conformance:** de-circularise sashie reference html ([7ad3a13](https://github.com/P4suta/aozora-notation-spec/commit/7ad3a13476128ba1270d7f9a02b08701e5c9d77a))
* **conformance:** de-dup Referenced forward HTML ([#19](https://github.com/P4suta/aozora-notation-spec/issues/19)) ([cddd12c](https://github.com/P4suta/aozora-notation-spec/commit/cddd12caf9eebede2ed095b59b59add244a06a00))
* mixed_ruby_bouten reflects ruby-base emphasis ([#50](https://github.com/P4suta/aozora-notation-spec/issues/50)) ([b60665f](https://github.com/P4suta/aozora-notation-spec/commit/b60665fd50b596c967254f99b61f418495656fef))
* **notation:** correct heading model to level×style, drop 副見出し fiction ([6158d90](https://github.com/P4suta/aozora-notation-spec/commit/6158d903e80d487f8157861f6d4ae1590d26bc4d))
* **notation:** 二重山括弧 — ≪≫ input → 《》 display (§6.15) ([10f61d6](https://github.com/P4suta/aozora-notation-spec/commit/10f61d6ba08a96d50ab03006de1996ae548cf0e1))
* **slugs:** Hepburn romaji for section-break slugs ([339f7d2](https://github.com/P4suta/aozora-notation-spec/commit/339f7d216bebe7e153befa27ad16d97202ed9e42))


### Documentation

* adopt SemVer + a version source of truth ([#31](https://github.com/P4suta/aozora-notation-spec/issues/31)) ([bd97cf9](https://github.com/P4suta/aozora-notation-spec/commit/bd97cf98cde5fbac8174b524c19d857720ef570b))
* **adr:** adopt MADR 4.0 template + numbering ([#24](https://github.com/P4suta/aozora-notation-spec/issues/24)) ([339988c](https://github.com/P4suta/aozora-notation-spec/commit/339988c9ba7f6b32d5f217cc65edb563bc9a2858))
* **adr:** canonical serialization forms ([#14](https://github.com/P4suta/aozora-notation-spec/issues/14)) ([8755fd7](https://github.com/P4suta/aozora-notation-spec/commit/8755fd720047a52221f292b4a14e2fbb6f9708b7))
* **adr:** correct ADR-0003 forward provenance ([#18](https://github.com/P4suta/aozora-notation-spec/issues/18)) ([8352df6](https://github.com/P4suta/aozora-notation-spec/commit/8352df6c9239fabb809f439fb3edd40385c50918))
* **conformance:** corpus-grounded coverage boundary (§10.5) ([a9e0e46](https://github.com/P4suta/aozora-notation-spec/commit/a9e0e463c3684a61346ecf30ad7ea32aeb73745c))


### Chore

* sync conformance vectors to aozora API naming ([92474ea](https://github.com/P4suta/aozora-notation-spec/commit/92474ea4f8cd8f9964c715dac9ffa8c042d00931))

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
