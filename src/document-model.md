# 3. Document Model and Character Encoding

## 3.1 Input

A notation document is a sequence of bytes representing Japanese text with
embedded notation. Historically Aozora Bunko files are encoded in
**Shift_JIS** (specifically the Microsoft / JIS X 0208 variant); modern
tooling also uses **UTF-8**.

- A conforming processor **MUST** accept UTF-8 input.
- A conforming processor **SHOULD** accept Shift_JIS input and decode it to
  Unicode before processing. A byte that does not decode under the declared
  or detected encoding is replaced by U+FFFD; a processor MAY additionally
  report this.

Once decoded, the input is a sequence of **Unicode scalar values**; all
subsequent sections operate on that sequence (after §4 normalization). This
specification does not define encoding detection; the encoding is either
declared out of band or detected by the processor.

## 3.2 Byte-order mark

A leading U+FEFF (BOM), in any number, is removed during normalization (§4)
and carries no meaning.

## 3.3 Line structure

Lines are separated by LF (U+000A). CR (U+000D) and CRLF are normalized to LF
(§4). A *line* is a maximal run with no LF. Several constructs are
line-scoped — single-line layout directives (§6.6), accent spans (§5.5, §4),
and the break interaction of §6.6/§6.9 — and refer to this definition.

## 3.4 Reserved private-use code points

Some processors use private-use scalar values internally as placeholder
markers while rewriting the text. A processor that does so **MUST** ensure
such code points cannot be confused with source content: if the source itself
contains one of its reserved scalars, the processor neutralizes the
occurrence during §4 and reports
[`source-contains-pua`](diagnostics.md#source-contains-pua). Which code points
are reserved is an implementation detail; that source occurrences are made
harmless is normative. Real Aozora Bunko text does not contain such code
points.

## 3.5 Coordinates

After §4, the text is the **sanitized source**. Every span in this document
and in the conformance vectors is a half-open UTF-8 byte range into the
sanitized source (§2.3). For input with no BOM, no CR, and no `〔…〕` accent
span, the sanitized bytes equal the decoded source bytes, so offsets coincide.
