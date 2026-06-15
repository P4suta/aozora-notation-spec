# 6.11 Illustrations (挿絵)

## Synopsis

An illustration directive records an inserted image and, optionally, a
caption — a reference to a figure file rather than image data itself.

## Notation

```text
［＃挿絵（fig01.png）入る］
```

```abnf
sashie = LBRACK HASH %s"挿絵（" path %s"）入る" RBRACK
path   = 1*body-char-not-rparen
```

The path is the figure file name between the full-width parentheses
`（ … ）`.

## Parameters

- **path** — the figure file reference.
- **caption** — OPTIONAL associated caption text, where the source provides
  one.

## Semantics

- The directive yields a `sashie` node carrying the file reference (and
  caption if present).
- Reference rendering (§8) is an image reference; because this specification
  does not fetch or embed image data, the reference mapping emits a figure
  placeholder/reference rather than pixels.
- Serialization reconstructs the directive byte-exact (§7.6).

## Error conditions

A malformed `挿絵（…）` that does not close as `）入る` is retained as a
generic annotation (§6.14); no dedicated diagnostic is defined.

## Conformance vectors

`sashie`.
