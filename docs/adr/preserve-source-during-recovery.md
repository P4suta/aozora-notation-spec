---
date: 2026-11-05
---

# Preserve decoded source during recovery serialization

## Status

Accepted.
Partly supersedes [ADR-0003](0003-canonical-serialization-forms.md) for serialization after `unclosed-bracket`, `mismatched-container-close`, or `nested-ruby`.
The canonical forms for well-formed notation remain unchanged.

## Context

The [official ruby guidance](https://www.aozora.gr.jp/annotation/etc.html) defines base delimiters for valid ruby, and the [official layout guidance](https://www.aozora.gr.jp/annotation/layout_2.html) defines container notation.
Neither defines a canonical repair for an incomplete delimiter, a mismatched container family, or nested ruby.
The [corpus inventory](../../src/conformance.md#still-deferred) also records centring openers without matching closers, so recovery can't assume every input contains a complete pair.
The recovery vectors are synthetic contract examples, not claims that their exact strings occur in the corpus.

Canonical serialization of a recovered tree can remove an explicit ruby-base marker or insert directive spacing even though the input still needs correction.
Saving an incomplete document would then change text beyond the user's edit.
The decoded source provides an unambiguous persistence result without guessing the intended repair.

## Decision

Default serialization reproduces the entire decoded source byte-for-byte in UTF-8 when parsing reports `unclosed-bracket`, `mismatched-container-close`, or `nested-ruby`.
Source preservation includes any BOM, original line endings, accent digraphs, explicit ruby-base markers, and directive spacing.
The exception applies to the whole document because canonicalizing an otherwise valid region would still change the saved input.
Nodes, diagnostics, and HTML rendering remain available during recovery.
An explicitly requested normalization operation may rewrite malformed input.

Reported spans use the decoded source's UTF-8 byte coordinates before pre-processing.
A processor maps any internal sanitized-source ranges back to that coordinate space before exposing nodes, pairs, or diagnostics.
Coordinates don't refer to the encoded bytes of a Shift_JIS file.

[Serialization](../../src/structural-model.md#76-serialization-round-trip) defines the default projection without adding API fields or changing the conformance JSON structure.
The [unclosed bracket](../../conformance/vectors/unclosed_bracket/vector.json), [mismatched container](../../conformance/vectors/mismatched_container_close/vector.json), and [nested ruby](../../conformance/vectors/nested_ruby/vector.json) vectors pin preservation.
The [accent vector](../../conformance/vectors/accent_decomposition_applied/vector.json) distinguishes source coordinates from normalized serialization.

## Consequences

Saving an incomplete document preserves the decoded input even when parsing recovers a usable structure.
Source spans continue to identify the original text after BOM removal, newline normalization, or accent decomposition.
Well-formed notation keeps ADR-0003's canonical forms and serialization fixed point.
Processors need source information alongside the recovered semantic structure.

Canonicalizing recovered nodes can repair or rewrite input without an explicit request, violating source preservation.
Preserving only the malformed region also changes the saved input because normalization elsewhere would still change the document.
Returning sanitized source loses the original BOM, line endings, and accent spelling.
