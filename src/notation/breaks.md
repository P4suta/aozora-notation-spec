# 6.9 Breaks (改ページ・改丁・改段・改見開き)

## Synopsis

Break directives mark page-level structure inherited from print: a new page,
a new recto/leaf, a new column section, or a new two-page spread.

## Notation

Each is a self-contained directive on its own line — no opener/closer, no
inner content:

```text
［＃改ページ］      ← new page
［＃改丁］          ← new recto / leaf (丁)
［＃改段］          ← new column section
［＃改見開き］      ← new two-page spread
```

```abnf
break = LBRACK HASH ( %s"改ページ" / %s"改丁" / %s"改段" / %s"改見開き" ) RBRACK
```

## Parameters

None.

## Semantics

- `［＃改ページ］` yields a `page-break` node; `改丁` / `改段` / `改見開き`
  yield a `section-break` node tagged recto / column / spread respectively.
  Both are **block leaves** (§8.1) standing on their own line.
- Reference rendering (§8): `<div class="aozora-page-break"></div>` for
  改ページ; `<div class="aozora-section-break aozora-section-break-<kaicho|kaidan|kaimihiraki>"></div>`
  for the section flavours.
- **Interaction with annotations and containers** (§7.3, §7.4):
  - a break does **not** close a **block** layout container (字下げ, 地付き,
    罫囲み); those persist across page boundaries, matching print typography,
    and a break inside one is **not** flagged;
  - a break that shares a line with a **single-line** layout directive, or
    that falls inside an inline `割り注` range (§6.8), drops that scope and
    raises
    [`break-in-single-line-container`](../diagnostics.md#break-in-single-line-container)
    (§7.4).
- Serialization reconstructs the directive byte-exact (§7.6).

## Error conditions

- [`break-in-single-line-container`](../diagnostics.md#break-in-single-line-container)
  (warning) — see Semantics.

## Conformance vectors

`page_break`, `section_break`, `break-in-single-line-container`.
