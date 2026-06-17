# 10. Conformance

## 10.1 Conforming processor

A **conforming processor** is an implementation that, for every input:

1. produces a result without aborting (§2.4);
2. applies the §4 normalization and the §5–§7 model; and
3. satisfies every `must`-level expectation of the conformance suite (§10.3).

A processor need not implement every projection (some have no HTML renderer,
some no serializer); it conforms with respect to the projections it produces.
A processor MUST NOT emit, for a `must`-level vector, a projection that
contradicts that vector.

## 10.2 The role of this specification (master)

This specification is designed to be the **single source of truth** a
processor conforms to. The normative prose, the examples, and the
machine-readable suite are kept in one repository so they cannot drift: every
normative example in §6 corresponds to a vector, and a consuming processor
**SHOULD** pin this repository by revision and run the suite in its own CI,
failing on any `must` mismatch.

## 10.3 Conformance suite

The suite lives at `conformance/vectors/`. Each case is a `vector.json`
validating against `conformance/schema/vector.schema.json` and carrying a
`source` plus the `expected` projections (`nodes`, `pairs`, `serialize`,
`diagnostics`, and optionally `html`). The runner contract — how a processor
consumes a vector, which projections are compared, and how matches are scored
by level — is `conformance/RUNNER.md`.

### Levels

| Level | Obligation |
|---|---|
| **must** | Every comparable projection MUST match exactly. A mismatch is non-conformance. |
| **should** | Projections SHOULD match; a documented mismatch is a warning, not non-conformance. |
| **may** | Informational; divergence is permitted. |

For a `must` vector, the `nodes`, `pairs`, and `diagnostics` projections are
mandatory comparisons; `serialize` is compared when the processor has a
serializer; `html` is compared when the processor has the reference renderer
(§8) and the vector's level pins it.

## 10.4 Claiming conformance

An implementation claiming conformance SHOULD state:

- the specification revision it targets (this repository's git revision);
- which projections it produces;
- its results against the suite, including any justified `should`/`may`
  divergences.

## 10.5 Coverage and growth

Not every notation family is at `must` coverage. The directives the official
guide treats as provisional, that lack corpus attestation, or that this
revision has not yet pinned with normative semantics, carry their notation but
no `must` vectors yet:

- **Character-size block form** (`［＃ここから…段階大きな文字］ … ［＃ここで
  大きな文字終わり］`) — the forward-reference size change is now normative
  (§6.17); the block form is corpus-attested but its closer drops the magnitude
  and pairs by direction (大きな vs 小さな), semantics not yet pinned.
- **Left-ruby block form** (`［＃左にルビ付き］…［＃左に「X」のルビ付き終わり］`)
  — the paired-block counterpart of the §6.5 forward-reference left-side ruby;
  the forward form is normative, the block form is not yet pinned.
- **Standalone illustration caption** (`『caption』はキャプション`) — the
  bundled `挿絵（file）「caption」入る` form is now normative (§6.11), but the
  free-standing caption directive that captions a preceding figure across a
  line break is not yet pinned.
- **Right-side ruby / annotation** (`の右に…のルビ`, `の右に…の注記`) — the
  right side is the default `｜《》` ruby; the explicit right-side bracket forms
  have no corpus attestation.
- **Table cell structure** — `［＃ここから表］` (§6.13) marks a table *region*;
  cell and row structure has no sanctioned delimiter (the full-width `／`
  sometimes seen is an editor convention, not a directive), so the region stays
  layout-only.
- **Column sub-regions and inter-column rules** (上段 / 下段, 段間に罫) beyond
  the §6.13 `ここからN段組` region.
- **Block centring with no closer** (`ここから中央揃え` alone) — unattested in
  the corpus; page-centring is covered by the single-line marker (§6.6) and the
  combined `ここからN字下げ、ページの左右中央`.
- **The remaining compound directives** — combinations other than the pinned
  字下げ＋ページの左右中央 (e.g. 字下げ＋字詰め, indent＋横書き＋罫囲み). Each
  component closes independently, so they have no single shared closer.

A conforming processor MAY keep any of these as a generic annotation (§6.14).
As a family gains full normative text it gains `must` vectors, recorded in
[Annex E](annex/changelog.md). Coverage gaps are tracked openly rather than
implied — a processor is never asked to match a behaviour this document has not
pinned with a vector.
