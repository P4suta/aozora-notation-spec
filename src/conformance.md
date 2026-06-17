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

The §6 catalogue covers every notation family that has a **parseable form
attested in the corpus**. What remains here is of two distinct kinds, kept
separate so the boundary is honest rather than a catch-all "deferred" bucket.

### No parseable notation

These are not deferred features — the corpus has **no `［＃…］` directive
form** for them, so there is nothing for a processor to parse. (Corpus
evidence: [`P4suta/aozorabunko_text`](https://github.com/P4suta/aozorabunko_text),
sampled 2026-06-17.)

- **Table cell / row structure** — `［＃ここから表］` (§6.13) marks a table
  *region*; there is no sanctioned cell or row delimiter (the full-width `／`
  sometimes seen is an editor convention, not a directive), so the region stays
  layout-only.
- **Column sub-regions** (上段 / 下段, 段間に罫) — `［＃上段］` and
  `［＃ここから上段］` have **zero** corpus occurrences; 上段 / 下段 appear only
  as body text, never as directives. There is no sub-region notation to pin.
- **Block centring with no closer** (`ここから中央揃え` alone) — zero corpus
  occurrences; page-centring is fully covered by the single-line marker (§6.6)
  and the combined `ここからN字下げ、ページの左右中央`.
- **Open-ended compound directives** — combinations beyond the pinned
  字下げ＋ページの左右中央 (e.g. 字下げ＋字詰め＋罫囲み). Each component opens and
  **closes independently**, so there is no single compound directive (and no
  shared closer) to recognise; the components are simply nested §6.6/§6.7
  containers, already covered individually.

### Real but unpinned

These have a real form but are vanishingly rare and/or architecturally
ill-fitting, so they carry their notation but no vector yet; a conforming
processor MAY keep them as a generic annotation (§6.14).

- **Left-ruby block form** (`［＃左にルビ付き］…［＃左に「X」のルビ付き終わり］`)
  — the paired-block counterpart of the §6.5 forward-reference left-side ruby
  (which **is** normative). Only ~2 corpus occurrences, and the reading sits in
  the *closer*, so the run's reading is unknown until the block ends — a model
  that does not fit the streaming per-run container machinery. Pinned only when
  real demand justifies the special case.
- **Standalone illustration caption** (`『caption』はキャプション`) — the
  bundled `挿絵（file）「caption」入る` form is normative (§6.11); the
  free-standing directive that captions a *preceding* figure across a line
  break is not yet pinned.
- **Explicit right-side ruby / annotation** (`の右に…のルビ`) — the right side
  is already the default `｜《》` ruby, so the explicit right-side ruby bracket
  is redundant and essentially unattested; the right-side *annotation* mirror of
  the §6.5 左 note is marginal (≈8 corpus hits).
- **Compound forward-references** (`「X」は縦中横、行右小書き`) — a single target
  taking two treatments at once (here 縦中横 §6.3 *and* 行右小書き §6.16). About
  900 corpus occurrences, but a forward-reference yields one node per §7.5, so a
  composite (nested) inline node is an architectural extension out of proportion
  to the frequency. A conforming processor keeps the directive as a generic
  annotation (§6.14) — **preserved verbatim and round-tripped byte-exact, not
  dropped** — until the composite model is pinned.

As a family in the second group gains full normative text it gains a vector,
recorded in [Annex E](annex/changelog.md). Coverage gaps are tracked openly
with corpus evidence rather than implied — a processor is never asked to match
a behaviour this document has not pinned with a vector.
