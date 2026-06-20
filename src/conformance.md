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

The §6 catalogue covers the core notation families. The boundary below is
grounded in a **full sweep** of every work in
[`P4suta/aozorabunko_text`](https://github.com/P4suta/aozorabunko_text)
(17,889 files, 2026-06-17) — parsed and bucketed by the reference
implementation, not estimated. Counts are occurrences across that sweep. An
earlier draft of this section misreported several of them (noted inline); they
are corrected here from the measured data.

### Recognised, pending full §6 promotion

These corpus-attested forms are **recognised** by the reference implementation
(typed distinctly, not the generic-annotation fallback). They are listed here
because their full normative §6 text and vectors are still being written; until
then a conforming processor MAY treat them as generic annotations (§6.14), but
the recommended behaviour is the typed form below.

- **File-header 凡例 symbols** — the de-facto-standard legend that prefixes
  nearly every work: `［＃］` (入力者注, ~14k occurrences), `［＃…］` (返り点),
  `［＃（…）］` (訓点送り仮名). Empty / placeholder directives — not unrecognised
  notation. Typed distinctly so they leave the generic-annotation bucket.
- **Bare-range forms** of families whose `ここから…/ここで…終わり` block form is
  already in §6: `［＃{N}段階…文字］…［＃…文字終わり］` (font-size, ~15k),
  `［＃横組み］…終わり` (~3k), `［＃行右/左小書き］…終わり` (~8k),
  `［＃キャプション］…終わり` (~2.5k).
- **Block `罫囲み` / `割り注`** (the `ここから…` region forms; the bare
  `［＃罫囲み］`/`［＃割り注］` remain inline), **`天から{N}字下げ`** (top-origin
  indent), and the bare **`改行天付き、折り返して{N}字下げ`** hanging indent.
- **Range bouten** `「X」～「Y」に<kind>` (also `〜`) — marks the whole preceding
  run from X to Y.
- **Input-editor notes**: `「X」はママ` (*sic*), `「X」は底本では「Y」` (source
  divergence), `「X」に「Y」の注記` (side annotation — see the correction below),
  numbered illustrations `［＃挿絵{N}（…）入る］`, and caption-before figures
  `「caption」のキャプション付きの(図|挿絵|写真)（file）入る`.

### Genuinely outside the model

- **Table cell / row structure** — `［＃ここから表］` marks a *region*; there is
  no sanctioned cell or row delimiter (the full-width `／` is an editor
  convention). `段間に罫` appears just **once** across the sweep (the earlier
  "zero" was imprecise) and `上段`/`下段` never appear as directives — far too
  sparse to pin a sub-region model.
- **Right-side ruby / annotation** — the right side is already the default
  `｜《》` ruby, so an explicit `の右に…のルビ` bracket is redundant. **Corrected
  count: the `の右に…のルビ` and `の右に…の注記` forms have 0 occurrences** (the
  earlier "≈8" was wrong); the attested side-annotation form is
  `「X」に「Y」の注記`, now recognised (above).
- **Left-ruby block form** (`［＃左にルビ付き］…［＃左に「X」のルビ付き終わり］`) —
  the paired-block counterpart of the forward-reference left-side ruby (which
  **is** normative). ~2 occurrences, and the reading sits in the *closer*, so it
  does not fit the streaming per-run container machinery. Pinned only on demand.
- **Dedicated-node layout / structural markers** — `［＃改行］` (forced break),
  `［＃本文終わり］` (body end), `字組み` compounds, and the `ローマ数字、面-区-点`
  gaiji form each need a node the model does not yet carry; left as generic
  annotations until promoted.

The full sweep leaves a residue of generic-annotation occurrences (down from
~194k before successive rounds of corpus grounding). The remainder is
overwhelmingly **correct** as a generic annotation: open-ended 入力者注 free-text
prose (not a fixed notation) and forward references whose target is genuinely
absent — legend *examples* like `（例）［＃「第一章」は中見出し］`, where the quoted
target never occurs as a preceding run. (A heading whose title merely carries
ruby is **not** such a case: its target is present, only ruby-split, and is
resolved ruby-stripped per §7.5 — see `heading_ruby_hint`.)

As a family in the first group gains full normative text it gains a vector,
recorded in [Annex E](annex/changelog.md). Coverage is tracked openly with
full-corpus evidence rather than implied — a processor is never asked to match
a behaviour this document has not pinned with a vector.
