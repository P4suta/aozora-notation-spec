# 2. Conventions and Terminology

## 2.1 Requirement keywords

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in
[BCP 14](https://www.rfc-editor.org/info/bcp14)
([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119),
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they
appear in all capitals, as shown here.

## 2.2 Grammar notation

Grammar is given in ABNF ([RFC 5234](https://www.rfc-editor.org/rfc/rfc5234)),
with terminals expressed as Unicode scalar values (`%xNNNN`). The collected
grammar is [Annex D](annex/abnf.md); fragments are inlined where relevant.
Because notation is embedded in free Japanese text, the grammar's `text`
production is disambiguated from constructs by the **leftmost-longest** rule
of §5, not by ABNF negation.

## 2.3 Definitions

- **Source** — the input byte sequence (§3), decoded to Unicode scalar
  values.
- **Sanitized source** — the source after the §4 normalization pass. Unless
  stated otherwise, *all byte offsets in this document and in conformance
  vectors are UTF-8 byte offsets into the sanitized source.* For input with
  no BOM, no CR, and no `〔…〕` accent span, the sanitized bytes equal the
  source bytes.
- **Directive** — a bracketed annotation `［＃ … ］` (§5, §6). The text
  between `＃` and `］` is the directive's **body**.
- **Inline construct** — a notation that attaches within a line: ruby,
  bouten/bousen, tate-chu-yoko, gaiji, kaeriten, warichu, and the generic
  annotation.
- **Container** — a construct delimited by a paired *opener* and *closer*
  that governs the enclosed content (§7): block layout (`字下げ` etc.),
  `罫囲み`, and the inline `傍点`/`傍線` range and `割り注`.
- **Ruby** — a reading (furigana) attached to a **base** run, `｜base《reading》`
  or its implicit form (§6.1).
- **Gaiji** (外字) — a character outside the assumed repertoire, written as a
  `※［＃…］` reference resolved to a Unicode scalar where possible (§6.4).
- **Men-ku-ten** (面区点) — a JIS X 0213 plane-row-cell address, e.g.
  `第3水準1-85-54`, used to identify a gaiji (§6.4, [Annex B](annex/gaiji.md)).
- **Kunten / kaeriten** (訓点・返り点) — classical-Chinese reading marks
  (§6.5).
- **Processor** — any implementation that consumes the notation. A
  **conforming processor** satisfies §10.
- **Diagnostic** — a structured, non-fatal observation a processor reports
  about the input (§9). Processing always continues and produces a
  best-effort result.

## 2.4 Error-handling philosophy

The notation has no concept of a fatal parse error. A conforming processor
**MUST** always produce a result for any input, however malformed, and
**MUST NOT** abort. Malformed or suspect input is surfaced through the
diagnostics of §9 while the affected construct degrades to a defined
best-effort form (typically the literal text, or a generic annotation that
preserves the bytes). This *recoverability* requirement is what lets the same
processor handle a century of hand-entered files.

## 2.5 Character repertoire and code points

Significant full-width delimiters are referred to by their Japanese glyph and
Unicode scalar value; the canonical list is in [Annex D](annex/abnf.md). The
most important are `［`=U+FF3B, `＃`=U+FF03, `］`=U+FF3D, `《`=U+300A,
`》`=U+300B, `｜`=U+FF5C, `※`=U+203B, `「`=U+300C, `」`=U+300D, `〔`=U+3014,
`〕`=U+3015.
