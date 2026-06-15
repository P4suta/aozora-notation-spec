# 6.7 Keigakomi (罫囲み)

## Synopsis

Keigakomi draws a **ruled frame** (a box) around a block of text — used for
notices, inset boxes, and the like.

## Notation

A paired block container:

```text
［＃罫囲み］
枠の中の文章。
［＃罫囲み終わり］
```

```abnf
keigakomi-open  = LBRACK HASH %s"罫囲み" RBRACK
keigakomi-close = LBRACK HASH %s"罫囲み終わり" RBRACK
```

> The official guide also writes this block as
> `［＃ここから罫囲み］ … ［＃ここで罫囲み終わり］`. The bare opener/closer
> above is the canonical pair in this specification; the `ここから`/`ここで`
> variant is an accepted equivalent and pairs by the same `keigakomi`
> family.

## Parameters

None.

## Semantics

- The opener/closer pair (§7.1) yields a `container` node (family
  `keigakomi`) governing the enclosed block; it nests with other block
  containers (§7.3).
- Reference rendering (§8) is
  `<div class="aozora-container aozora-container-keigakomi">…</div>`.
- Serialization reconstructs the opener/closer byte-exact (§7.6).

## Error conditions

- [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  — closed by a different container family.
- [`unclosed-bracket`](../diagnostics.md#unclosed-bracket) — opener with no
  closer.

## Conformance vectors

`keigakomi_container`.
