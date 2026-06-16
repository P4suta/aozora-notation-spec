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

Not every notation family is yet at `must` coverage. The directives the
official guide treats as provisional (§6.5 saidoku-moji, the deferred §6.6
layout directives — the block centring form, 地寄せ, compound directives — and
the §6.13 column sub-directives) carry their notation but no `must` vectors
yet. As such a family gains
full normative text it gains `must` vectors, recorded in
[Annex E](annex/changelog.md). Coverage gaps are tracked openly rather than
implied — a processor is never asked to match a behaviour this document has
not pinned with a vector.
