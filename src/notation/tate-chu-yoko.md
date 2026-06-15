# 6.3 Tate-chu-yoko (縦中横)

## Synopsis

Tate-chu-yoko ("horizontal-within-vertical") sets a short run — typically
multi-digit numbers or Latin initialisms — **upright and horizontal** inside
vertical text, so e.g. `24` reads as a unit rather than two stacked digits.

## Notation

A forward-reference directive names the run:

```text
昭和二十四年は西暦19［＃「19」は縦中横］24［＃「24」は縦中横］年。
```

```abnf
tcy = LBRACK HASH LQUOTE target RQUOTE %s"は縦中横" RBRACK
```

## Parameters

- **target** — the quoted run to rotate. It is resolved against the preceding
  text by the look-back rule (§7.5).

## Semantics

- The directive resolves its target (§7.5) and yields a `tate-chu-yoko` node
  over the matched run.
- Reference rendering (§8) is `<span class="aozora-tcy">…</span>`.
- Serialization reconstructs the directive (and the literal target it follows)
  byte-exact (§7.6).

## Error conditions

- **Target not found** — a target absent from the look-back raises
  [`tcy-target-not-found`](../diagnostics.md#tcy-target-not-found) (warning);
  the directive degrades to a generic annotation (§6.14).

## Conformance vectors

`tate_chu_yoko`.
