# 6.8 Warichu (割り注)

## Synopsis

Warichu (割り注, "split note") is an inset two-line annotation set at half
size within the run of the main text — a traditional interlinear note.

## Notation

A paired **inline** range:

```text
本文［＃割り注］注の内容［＃割り注終わり］に続く本文。
```

```abnf
warichu-open  = LBRACK HASH %s"割り注" RBRACK
warichu-close = LBRACK HASH %s"割り注終わり" RBRACK
```

## Parameters

None; the enclosed content is the note body.

## Semantics

- The opener and closer are recognized as inline annotation markers; the
  content between them is the warichu body. The pair is an **inline**
  construct (§7.3) — it does not introduce block structure and, in the
  corpus, does not span a line.
- Reference rendering (§8) wraps the body as inline:
  `<span class="aozora-warichu">…</span>`.
- Serialization reconstructs the opener/closer byte-exact (§7.6).

## Error conditions

- [`break-in-single-line-container`](../diagnostics.md#break-in-single-line-container)
  (warning) — a page or section break **inside** an open warichu range drops
  it (§7.4, §6.9): a break is block-level and a warichu is inline.
- [`unclosed-bracket`](../diagnostics.md#unclosed-bracket) — an opener with no
  closer.

## Conformance vectors

`warichu_inline`.
