# 6.11 Illustrations (挿絵)

## Synopsis

An illustration directive records an inserted image and, optionally, a
caption — a reference to a figure file rather than image data itself.

## Notation

```text
［＃挿絵（fig01.png）入る］
［＃挿絵（fig01.png）「図一」入る］
［＃挿絵（fig42_03.png、横480×縦640）入る］      ← with a pixel-size note
```

```abnf
sashie     = LBRACK HASH %s"挿絵（" path [ %s"、" dimensions ] %s"）" [caption] %s"入る" RBRACK
path       = 1*body-char-not-rparen-not-comma
dimensions = %s"横" 1*DIGIT %s"×縦" 1*DIGIT
caption    = %s"「" 1*body-char-not-rquote %s"」"
```

The path is the figure file name between the full-width parentheses
`（ … ）`. The corpus' standard form bundles a pixel-size note after a `、`
(`横W×縦H`); it is split off the path so the rendered `<img src>` stays a
clean file reference. An OPTIONAL `「caption」` between `）` and `入る` carries
the figure's caption ([AOZORA-ANNOTATION], `graphics.html`).

## Parameters

- **path** — the figure file reference (without any trailing size note).
- **dimensions** — OPTIONAL verbatim pixel-size note (`横W×縦H`); when it
  parses as two digit runs it also supplies the rendered `width`/`height`.
- **caption** — OPTIONAL associated caption text, where the source provides
  one.

## Semantics

- The directive yields a `sashie` node carrying the file reference (and
  caption if present).
- Reference rendering (§8) is an image reference; because this specification
  does not fetch or embed image data, the reference mapping emits a figure
  placeholder/reference rather than pixels. A caption, when present, renders
  into the figure's `<figcaption>`.
- Serialization reconstructs the directive — including the optional
  `「caption」` — byte-exact (§7.6).

## Error conditions

A malformed `挿絵（…）` that does not close as `）入る` is retained as a
generic annotation (§6.14); no dedicated diagnostic is defined.

## Conformance vectors

`sashie`, `sashie_caption`, `sashie_dimensions`.
