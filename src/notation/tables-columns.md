# 6.13 Tables and columns (表・段組)

## Synopsis

Two block containers mark **table** (表) and **multi-column** (段組) regions.
Both are *layout* containers: they delimit a region but carry **no cell, row,
or column markup** — the enclosed content is plain text whose alignment is set
by spacing in the source. A processor marks the region; the internal structure
is not machine-readable.

## Notation

```text
［＃ここから表］…［＃ここで表終わり］              ← table region
［＃ここから2段組み］…［＃ここで段組み終わり］     ← 2-column region
```

```abnf
table-block-open   = LBRACK HASH %s"ここから表" RBRACK
table-block-close  = LBRACK HASH %s"ここで表終わり" RBRACK
columns-block-open = LBRACK HASH %s"ここから" 1*DIGIT %s"段組" [ %s"み" ] RBRACK
columns-block-close = LBRACK HASH %s"ここで段組" [ %s"み" ] %s"終わり" RBRACK
```

(The `み` okurigana is optional — `段組` and `段組み` both occur.)

## Parameters

- **count** — for columns (段組), the number of columns (`2段組`, `3段組`, …).

## Semantics

- A **block** opener/closer pair (§7.1) yields a `container` node — family
  `table` or `columns` — governing the enclosed lines; containers nest (§7.3),
  and pairing is by family (§7.2). The columns opener carries a `count`; the
  table opener has no parameter.
- The enclosed content is ordinary flow content (§5); there is **no** notation
  for table cells, rows, or column boundaries. Visual structure depends on the
  source's spacing and the rendering medium.
- Reference rendering (§8): `<div class="aozora-container aozora-container-table">…</div>`
  and `<div class="aozora-container aozora-container-columns" data-columns="N">…</div>`.
  The precise structure is part of the reference mapping (§8.2), not mandated.
- Serialization reconstructs the opener and closer around the content (§7.6);
  the `み` okurigana is normalised to `段組み`.

## Error conditions

- [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  — a closer of a different family than its opener.
- [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  — a `ここから…` opener naming no known container kind (kept as a generic
  annotation, §6.14).

The official guide's column sub-directives — `上段` / `下段` (explicit
upper/lower column), `段間に罫` (rule between columns), `段組み適用外`
(exemption) — and compound forms (`ここから2字下げ、4段組み`) are deferred to a
later revision (§10.5); a processor retains them as generic annotations.

## Conformance vectors

`table_container`, `columns_container`.
