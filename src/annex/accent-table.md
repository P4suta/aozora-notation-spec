# Annex A. Accent decomposition table

This annex is **normative**. It defines the indicator-to-character mapping for
the `〔…〕` accent decomposition of §4.3. Within an accent span, a Latin base
letter immediately followed by an ASCII **indicator** is rewritten to the
corresponding precomposed Unicode character.

## A.1 Indicators

| Indicator | Diacritic | Example | → |
|---|---|---|---|
| `` ` `` | grave | `e\`` | è |
| `'` | acute | `e'` | é |
| `^` | circumflex | `e^` | ê |
| `~` | tilde | `n~` | ñ |
| `:` | diaeresis / umlaut | `u:` | ü |
| `_` | macron | `o_` | ō |
| `,` | cedilla | `c,` | ç |
| `/` | stroke / slash | `o/` | ø |
| `&` | ring above | `a&` | å |

The `&` indicator also forms **ligatures**, which are checked before the
ring-above reading (longest match wins, §A.3):

| Sequence | → |
|---|---|
| `ae&` / `AE&` | æ / Æ |
| `oe&` / `OE&` | œ / Œ |
| `s&` | ß (eszett — **not** `s` + ring) |

## A.2 Coverage

Not every (letter, indicator) pair has a precomposed form; only the pairs
that map to a Unicode character are decomposed. The closed set is enumerated
below (lower- and upper-case share the same indicators):

| Base | Indicators that decompose |
|---|---|
| a / A | `` ` `` `'` `^` `~` `:` `&` `_` |
| e / E | `` ` `` `'` `^` `:` `_` `~` |
| i / I | `` ` `` `'` `^` `:` `_` `~` `/` |
| o / O | `` ` `` `'` `^` `~` `:` `/` `_` |
| u / U | `` ` `` `'` `^` `:` `_` `&` `~` |
| c / C | `,` `'` `^` |
| n / N | `` ` `` `~` `'` |
| s / S | `'` `,` `^` |
| y / Y | `'` `:` |
| d / D | `/` · g/G,h,j/J: `^` · h: `/` · l/L: `/` `'` · m: `'` · r/R: `'` · t: `,` · z/Z: `'` |

A `〔…〕` span whose body contains no sequence in this table is left unchanged
and emits no diagnostic (§4.3).

## A.3 Rules

- **Longest match.** A multi-character ligature (`ae&`, `s&`, …) is matched in
  preference to a shorter reading of its prefix. `s&` is ß, never `s` + ring.
- **Line-bounded.** An accent span begins and ends on one line (§4.3, §5.5).
- **Loss-free.** The serializer reconstructs the original `〔…〕` source form
  (§7.6); decomposition is reversible by construction.
- **Diagnostic.** Each span that actually contained a digraph raises
  [`accent-decomposition-applied`](../diagnostics.md#accent-decomposition-applied)
  (note), in post-decomposition coordinates.

> The enumeration above follows the official 外字 accent guidance
> ([§12 \[AOZORA-ANNOTATION\]](../references.md)). Additions are a MINOR
> revision: a new (letter, indicator) row never changes an existing mapping.
