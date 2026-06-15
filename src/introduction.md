# 1. Introduction

青空文庫記法 (*Aozora Bunko notation*) is the annotation language used to mark
up the plain-text works of [Aozora Bunko](https://www.aozora.gr.jp/), Japan's
volunteer digital library. It encodes the typographic features of printed
Japanese books — ruby (furigana), emphasis dots and side lines, out-of-
repertoire glyphs (gaiji), classical-Chinese reading marks (kunten),
indentation and alignment, page and section breaks — as inline directives
inside otherwise ordinary text, e.g.

```text
　明治の頃｜青梅《おうめ》街道沿いに、可哀想［＃「可哀想」に傍点］な話。
```

This document specifies that language **normatively**: precisely enough that
two independent implementations, reading only this text, produce the same
result for the same input.

## 1.1 Scope

This specification defines:

- the **character-level input** a conforming processor accepts, and the
  **normalization** applied before parsing (§3, §4);
- the **lexical grammar** of notation constructs (§5, [Annex D](annex/abnf.md));
- the **notation catalogue** — every directive and inline construct, its
  parameters, and its meaning (§6);
- the **structural processing model** — pairing, nesting, and
  forward-reference resolution (§7);
- a **reference rendering** to HTML and a byte-exact **serialization**
  round-trip (§8);
- the **diagnostics** a processor reports for malformed input (§9); and
- **conformance**, anchored by a machine-readable test-vector suite (§10).

It does **not** define a file format, a transport, a stylesheet, or the visual
appearance of any construct beyond a reference mapping.

## 1.2 Relationship to the official 注記一覧

The authoritative human-facing description of the notation is Aozora Bunko's
official 注記一覧 (*annotation guide*),
<https://www.aozora.gr.jp/annotation/>. That guide is the source of record
for **intent**: which constructs exist and what they mean. It is, however,
prose-and-example only — it has no formal grammar, no precise processing
model, and no conformance suite, and in several places it is silent or
ambiguous about edge cases.

This specification follows the official guide wherever it is determinate.
Where the guide is silent or admits more than one reading, this document
makes an **explicit normative decision**, grounded additionally in the forms
and frequencies actually observed in the Aozora Bunko corpus. Each such
decision is recorded as a decision record (referenced from the relevant
section) so that the choice — and its rationale — is auditable rather than
folkloric.

This specification is independent and is **not** endorsed by or affiliated
with Aozora Bunko.

## 1.3 Document status

This is **draft v0.1**. The framework (§§1–5, 7–12) and the notation families
in §6 are normative. A few families that the official guide itself treats as
provisional — 太字 / 斜体 (§6.12), 表 / 段組 (§6.13), saidoku-moji (§6.5),
and some layout directives (§6.6) — are documented with their notation, but
their full normative semantics are deferred to a later revision and not yet
required for conformance; each is flagged where it appears (see §10.5).

## 1.4 Conformance levels (overview)

Normative requirements use the keywords of §2. Conformance is verified
against the test vectors of §10, each tagged `must`, `should`, or `may`.
A *conforming processor* matches every `must`-level expectation; the lower
levels scale the obligation down. The full contract is in §10 and in
`conformance/RUNNER.md` at the repository root.

## 1.5 Document conventions

Japanese notation strings, keywords, and examples are given verbatim in
Japanese; surrounding explanation is in English. Full-width punctuation that
is significant to the grammar (`［ ＃ ］ 《 》 ｜ ※ 「 」 （ ） 〔 〕`) is shown
as-is and identified by Unicode scalar value in [Annex D](annex/abnf.md).
Byte offsets in examples and vectors are **UTF-8 byte offsets into the
sanitized source** (§4).
