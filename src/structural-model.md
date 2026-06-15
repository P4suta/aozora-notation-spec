# 7. Structural Processing Model

§5 yields a flat element stream; §6 classifies each directive. This section
defines the **structure** built on top: how openers pair with closers, how
containers nest, how forward references resolve, and how the result
serializes back to source byte-for-byte.

## 7.1 Pairing

Some constructs are **paired**: an opener and a matching closer with content
between them. The paired families are:

- block layout containers — `［＃ここから…］` / `［＃ここで…終わり］` (§6.6);
- `罫囲み` — `［＃罫囲み］` / `［＃罫囲み終わり］` (§6.7);
- `割り注` — `［＃割り注］` / `［＃割り注終わり］` (§6.8); and
- the `傍点`/`傍線` **range** form — `［＃傍点］` / `［＃傍点終わり］` (§6.2).

Pairing uses a **stack**: each opener is pushed; each closer pops the nearest
open of a compatible **family** and forms a pair governing the content
between them. A processor **MUST** pair by family, not by exact variant, so
that e.g. a `2字下げ` opener pairs with a plain `字下げ終わり` closer.

## 7.2 Mismatch and recovery

- A closer whose family differs from the popped opener raises
  [`mismatched-container-close`](diagnostics.md#mismatched-container-close);
  the opener is auto-closed at the closer and the pair is keyed by the
  **opener's** family (recovery).
- Within the `傍点`/`傍線` range family, a 点-vs-線 family disagreement raises
  [`mismatched-bouten-container`](diagnostics.md#mismatched-bouten-container)
  (§6.2); the run is keyed to the opener's variant.
- A closer with no open on the stack, or an opener never closed, is handled
  per [`unmatched-close`](diagnostics.md#unmatched-close) /
  [`unclosed-bracket`](diagnostics.md#unclosed-bracket); the affected marker
  degrades but its bytes are preserved.

## 7.3 Block vs inline; nesting

A paired construct is **block** or **inline**:

- **Block** containers (block layout, `罫囲み`) govern whole lines and may
  nest; rendering wraps them as block elements. Breaks (§6.9) persist across
  a block container (print typography), so a break inside one is **not**
  flagged.
- **Inline** ranges (`傍点`/`傍線` range, `割り注`) attach within a line and
  do not introduce block structure. The corpus shows these never span a line
  in practice.

Containers nest by the stack discipline of §7.1; an inner pair closes before
its outer pair.

## 7.4 Single-line containers

A *single-line* layout directive (`［＃地付き］`, `［＃2字下げ］`, §6.6) has no
closer: it governs the remainder of its line only and is modelled as a
zero-width marker, not a wrapping container. Consequently a page or section
break sharing that line, or a break inside a `割り注` range, drops the
governed scope and raises
[`break-in-single-line-container`](diagnostics.md#break-in-single-line-container)
(§6.9).

## 7.5 Forward-reference resolution

Some directives name a **target** by quoting it and look **backwards** in the
already-seen text to find the run they apply to:

- `［＃「X」に傍点］` and its variants (§6.2),
- `［＃「X」は縦中横］` (§6.3),
- heading hints `［＃「X」は…見出し］` (§6.10), and
- `「ママ」`/textual-note annotations (§6.14).

Resolution rule: a processor scans the text **preceding** the directive (back
to the start of the current line, or the document per the construct) for the
most recent occurrence of the quoted target `X`, and applies the construct to
that run.

- If `X` does not occur in the look-back, the directive degrades to a generic
  annotation and raises the family's "target not found" diagnostic
  (e.g. [`tcy-target-not-found`](diagnostics.md#tcy-target-not-found)).
- If `X` occurs **more than once**, the chosen run may be unintended; a
  processor raises the family's "ambiguous" diagnostic where defined
  (e.g. [`bouten-target-ambiguous`](diagnostics.md#bouten-target-ambiguous))
  and applies the construct to the match its look-back selects.
- The redundant explicit form `平和［＃「平和」に傍点］` (the target literal
  immediately precedes the directive) is common and **MUST** round-trip
  unchanged (§7.6).

## 7.6 Serialization round-trip

A processor that serializes **MUST** be a fixed point: re-parsing a
serialized result yields the same structure, and serializing again yields the
same bytes. Normalization (§4) is loss-free for this reason — the serializer
reconstructs `〔…〕` accent spans, the `｜` of an explicit ruby base, the
literal target of a redundant forward reference, and the original directive
strings. The `serialize` projection of each conformance vector pins this.
