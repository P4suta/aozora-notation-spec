# 0003. Canonical serialization picks one surface form per concept

- Status: accepted
- Date: 2026
- Governs: §6 (notation families), §7 (structural model), the serialize projection

## Context

青空文庫記法 is human-authored and offers several **surface forms for the
same meaning**. A run can be emphasised three ways — forward
`語句［＃「語句」に傍点］`, range `［＃傍点］語句［＃傍点終わり］`, or block
`［＃ここから傍点］…［＃ここで傍点終わり］`. Ruby has an implicit (`漢字《よみ》`)
and an explicit (`｜漢字《よみ》`) base form. A gaiji description may be quoted
(`※［＃「desc」、men-ku-ten］`) or bare (`※［＃desc、men-ku-ten］`).

A processor that re-serialises a parsed document needs **one canonical form
per concept**, or `parse ∘ serialize` is not a fixed point. Two projections
are in play and must not be conflated:

- **verbatim** — reproduce the author's exact (sanitised) bytes. This is
  authoritative for faithful reproduction and is *unaffected* by the choices
  below.
- **canonical** — the normalised, diff-stable serialisation. This ADR fixes
  its form.

The core model is **scope-free**: a marked span is one concept
(`Region{format, content}`), not three scope-variants. Surface scope
(forward/range/block) is therefore *not* retained, so the serializer must
choose a single emission form per concept rather than echo the input scope.

## Decision

The canonical form is chosen per concept by **least surprise against the
corpus** (frequencies are whole-corpus counts over the reference mirror; the
verbatim projection preserves the author's form regardless, so a minority
surface form loses nothing in faithfulness):

| Concept | Canonical form | Corpus basis |
|---|---|---|
| Inline span formats (傍点・傍線・太字・斜体・文字サイズ・縦中横・…) | **forward** `語句［＃「語句」に〈keyword〉／は〈keyword〉］` | 傍点 forward 125,229 vs range 1,342 (≈93:1) |
| Multi-target inline (`「A」「B」に傍点`, non-contiguous) | **one forward span per contiguous target** (`A［＃「A」に傍点］とB［＃「B」に傍点］`) | non-contiguous is genuinely several spans |
| Ruby base delimiter | **bare** `漢字《よみ》`; emit `｜` only when the bare form would re-parse to a different base (per [0002](0002-implicit-ruby-base-extent.md)) | implicit base ≈95% of readings |
| Gaiji description | **quoted** `※［＃「desc」、men-ku-ten］` | quoted 40,105 (≈64%) vs bare 22,349 |
| Heading | **promoted** (the referent line is emitted once as the heading) | avoids cross-line duplication |

A processor **MUST** emit the canonical form for each concept and **MUST**
keep `serialize` a fixed point (`serialize(parse(serialize(parse(x)))) ==
serialize(parse(x))`). A processor **MAY** also expose a verbatim projection
that reproduces the input bytes; the two are distinct and the verbatim form
is not required to equal the canonical form.

Because the model is scope-free, the canonical form is reconstructed from the
concept alone; it does not depend on a per-node "how was this written" flag.
This makes the fixed point **structural**: the canonical form parses back to
the same concept, which re-serialises identically.

## Consequences

- The unbounded round-trip growth observed on forward references with an
  intervening delimiter in the target (a quoted phrase, ruby, an explicit
  base) disappears: there is no scope-variant split and no leading-literal
  re-emit flag, so no fragment is stranded and re-prepended per pass.
- `to_source` may differ from the author's surface scope (e.g. a range-form
  傍点 re-serialises as forward); the verbatim projection is the faithful
  reproduction.
- Ruby and gaiji canonical forms are *minimal* with respect to re-parse: a
  `｜` or quote pair is added only when its absence would change the parse.

## Alternatives considered

- **Canonical = range/block** for inline spans. Rejected: with a normalising
  lowering pass both forward and range are fixed points, so the choice is
  pure least-surprise — and range would re-write the 125,229 forward 傍点
  occurrences against the dominant author form.
- **Retain the input scope as provenance and echo it.** Rejected: it
  re-introduces a per-node surface flag (the very coupling this model
  removes) and makes the fixed point depend on that flag rather than on the
  concept.

## References

- §6, §7; [0002](0002-implicit-ruby-base-extent.md); official 注記一覧.
