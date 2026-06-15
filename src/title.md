# The Aozora Bunko Notation Specification

**Status:** Draft v0.1 · **Date:** 2026 · **License:** Apache-2.0 OR MIT

This document specifies **青空文庫記法** (Aozora Bunko notation): the
inline and block annotation language used to mark up plain-text works in the
[Aozora Bunko](https://www.aozora.gr.jp/) digital library — ruby, emphasis
dots and side lines, gaiji (out-of-repertoire glyph) references, kunten /
return marks, layout containers, page and section breaks, and editor
annotations.

It is written to be **implementable from the text alone**: it uses
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
keywords, an [ABNF](https://www.rfc-editor.org/rfc/rfc5234) grammar, an
explicit processing model, a diagnostics catalogue, and a machine-readable
[conformance suite](conformance.md).

> This specification is an independent formalisation. It is **not**
> affiliated with or endorsed by Aozora Bunko. The authoritative
> human-facing source is the official 注記一覧
> (<https://www.aozora.gr.jp/annotation/>); where that source is silent or
> ambiguous, this document makes an explicit normative decision and records
> the rationale.

See [§1 Introduction](introduction.md) to begin.
