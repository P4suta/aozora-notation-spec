# 0002. Implicit ruby base extends over one character class

- Status: accepted
- Date: 2026-06-16
- Deciders: @P4suta
- Tags: ruby
- Governs: §6.1 (Ruby)

## Context

In the implicit ruby form `…《reading》` (no `｜`), the base is the run of text
immediately preceding `《`. The official guide says to prefix the base with
`｜` when it mixes character types, but does not state precisely how far the
implicit base extends when `｜` is absent — one character? one script class?
to the previous punctuation?

## Decision

The implicit base is the **maximal preceding run of a single character
class**. A processor **MUST** take a trailing run of kanji (CJK ideographs)
as the base; it **MAY** extend the implicit base over another single class
(kana, Latin) but **MUST** stop at a class boundary and at any preceding
notation construct. A base that spans classes is expressed with the explicit
`｜` form.

## Consequences

- Matches the guide's own rationale for `｜` (it exists precisely for the
  cross-class case), and the common corpus pattern of kanji-base ruby.
- The "`MAY` extend over a single non-kanji class" latitude lets a processor
  handle kana/Latin bases without over-reaching across a class boundary,
  where intent is genuinely ambiguous and the author should have used `｜`.

## Alternatives considered

- **Always require `｜`.** Rejected: the corpus is full of bare kanji-base
  ruby; demanding `｜` would mis-handle the majority case.
- **Extend to previous punctuation regardless of class.** Rejected:
  over-captures across script boundaries where the author would have written
  `｜`, producing wrong bases.

## References

- §6.1; official 注記一覧, ルビ (etc.).
