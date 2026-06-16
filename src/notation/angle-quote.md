# 6.15 Double-angle quotation (二重山括弧)

## Synopsis

A source text (底本) may set a phrase inside twin angle brackets `《…》`. Those
glyphs (U+300A / U+300B) are exactly the ruby reading markers (§6.1), so an
Aozora Bunko transcription cannot write them literally without colliding with
ruby. The transcription therefore **encodes** the quotation as `≪…≫`
(U+226A / U+226B) and a processor **restores** the display form `《…》`.

底本 `《重要》` → transcription `≪重要≫` → display `《重要》`.

## Notation

A run delimited by `≪` (U+226A) and `≫` (U+226B):

```text
≪重要≫
```

```abnf
angle-quote   = ANGLE-OPEN angle-content ANGLE-CLOSE   ; ≪ … ≫
ANGLE-OPEN    = %x226A                                 ; ≪
ANGLE-CLOSE   = %x226B                                 ; ≫
```

The delimiters are distinct Unicode scalars from the ruby markers `《`/`》`
(U+300A / U+300B), so this construct never competes with ruby under the
leftmost-longest rule (§5.1).

## Parameters

- **content** — the quoted run between the delimiters. It MAY contain the same
  nested inline constructs a ruby reading may (e.g. a gaiji reference), folded
  the same way (§7).

## Semantics

- A well-formed `≪content≫` yields an `angle-quote` node over the run.
- Reference rendering (§8) is `<span class="aozora-angle-quote">《…》</span>`:
  the processor restores the **display** brackets `《…》` (U+300A / U+300B)
  inside the span. The input scalars `≪`/`≫` are not emitted.
- Serialization (§7.6) reconstructs the **input** form `≪content≫`
  (U+226A / U+226B), byte-exact; `parse ∘ serialize` is a fixed point.
- An adjacent `《《…》》` in source is **not** this construct: those are two ruby
  openers and raise [`nested-ruby`](../diagnostics.md#nested-ruby) (§9). The
  double-angle quotation is only ever the distinct `≪…≫` encoding.

## Error conditions

- **Unclosed `≪`** — a `≪` with no matching `≫` is handled per
  [`unclosed-bracket`](../diagnostics.md#unclosed-bracket) (error); the region
  degrades to plain text.
- **Empty `≪≫`** — an empty body produces no node; the bytes degrade to plain
  text and are **not** flagged (mirroring a bare `《》`).
- A stray `≫` with no opener is literal text and is not flagged.

## Conformance vectors

`angle_quote` (under `conformance/vectors/`).
