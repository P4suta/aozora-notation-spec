# Annex B. Gaiji resolution

This annex defines how a `※［＃…］` gaiji reference (§6.4) resolves to a
character. It is **normative** as to the *order* of resolution and the
*forms* recognized; the underlying JIS X 0213 and description tables are
versioned data (§11.5).

## B.1 Reference forms

A gaiji reference is `※` followed by a directive whose body is a glyph
**description** optionally followed by an address. The forms, by the address
they carry:

| Form | Example | Address |
|---|---|---|
| Men-ku-ten (JIS X 0213) | `※［＃「てへん＋劣」、第3水準1-84-77］` | `第N水準 面-区-点` |
| Unicode reference | `※［＃「口＋世」、U+546D、123-4］` | `U+XXXX` (+ page-line) |
| Description only | `※［＃「土へん＋竒」、123-4］` | page-line locator only |
| Named (JIS X 0213) | `※［＃二の字点、1-2-22］` | `面-区-点` |

The body before the first `、` is the human description (radical-composition
like `木＋世`, or a name like `二の字点`). The `、`-separated trailer carries
the address(es). A bare page-line locator (`123-4`) is a provenance note, not
a resolvable address.

## B.2 Resolution order

A processor resolves the reference by trying, in order, and stopping at the
first hit:

1. an explicit `U+XXXX` in the body — validated with `char::from_u32`
   semantics (a value that is not a Unicode scalar does not resolve here);
2. a JIS X 0213 **men-ku-ten** (`第N水準P-R-C` or `面-区-点`) → the scalar (or
   combining sequence) for that cell;
3. a **description** that names a known glyph (the 外字注記辞書 / description
   table) → its scalar;
4. a **single-character description** — if the description is itself exactly
   one character, that character.

If none resolves, the reference is **unresolved**: the processor reports
[`unresolved-gaiji`](../diagnostics.md#unresolved-gaiji) (warning) and the
reference falls back to its description text (§6.4, §8).

## B.3 Special forms

- **くの字点** (kunojiten, the vertical iteration mark) is written `／＼`, and
  its voiced form `／″＼`. These are notation, not a `※［＃…］` reference.
- A men-ku-ten cell MAY map to a **combining sequence** (more than one
  scalar), e.g. a base kana plus a combining mark; resolution yields the
  full sequence.

## B.4 Round-trip

Resolution is for rendering; the serializer (§7.6) reconstructs the original
`※［＃…］` reference verbatim, so a resolved or unresolved reference
round-trips losslessly.

> The men-ku-ten and description tables derive from JIS X 0213
> ([§12 \[JISX0213\]](../references.md)) and Aozora Bunko's 外字注記辞書. A
> processor SHOULD treat them as trusted, versioned inputs (§11.5).
