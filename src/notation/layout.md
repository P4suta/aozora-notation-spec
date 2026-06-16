# 6.6 Layout containers (字下げ・地付き ほか)

## Synopsis

Layout directives control horizontal placement of lines: **indentation**
(字下げ), **end-alignment** (地付き / 地上げ, i.e. flush to the foot of the
vertical line), line length (字詰め), centring (中央揃え), and margined
right-alignment (地寄せ). Each has a **block** form (a paired container
governing many lines) and, for indent and end-align, a **single-line** form.
This section pins indentation (including the hanging-indent 折り返し字下げ
form) and end-alignment; the remaining layout directives are catalogued below
and in [Annex C.2](../annex/slugs.md).

## Notation

```text
［＃ここから2字下げ］          ← block indent opener
　本文…
［＃ここで字下げ終わり］        ← closer

［＃ここから2字下げ、折り返して4字下げ］  ← hanging indent (first line 2, wrap 4)
　長い本文が折り返して4字下げされる…
［＃ここで字下げ終わり］

［＃2字下げ］この行だけ        ← single-line indent
［＃地付き］平和への誓い        ← single-line end-align (foot)
［＃地から2字上げ］…           ← single-line end-align, 2 from the foot

［＃ここから地付き］…［＃ここで地付き終わり］          ← block end-align
［＃ここから地から2字上げ］…［＃ここで字上げ終わり］   ← block end-align (margin)
```

```abnf
indent-block-open = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ" RBRACK
indent-wrap-open  = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ、折り返して" 1*DIGIT %s"字下げ" RBRACK
indent-single     = LBRACK HASH 1*DIGIT %s"字下げ" RBRACK
align-end-single  = LBRACK HASH %s"地付き" RBRACK
                  / LBRACK HASH %s"地から" 1*DIGIT %s"字上げ" RBRACK
```

(`1*DIGIT` admits ASCII or full-width digits.)

## Parameters

- **amount** — for indent, the number of full-width characters to indent.
- **wrap** — for the hanging-indent form (折り返し字下げ), the indent applied
  to wrapped continuation lines after the first; absent for a plain indent.
- **offset** — for end-align, the distance from the foot: `0` (地付き) or `N`
  (地からN字上げ).

## Semantics

- A **block** opener/closer pair (§7.1) yields a `container` node (family
  `indent` or `align-end`) governing the enclosed lines; containers nest
  (§7.3). Pairing is by **family**, so a `2字下げ` opener pairs with a plain
  `字下げ終わり` (§7.2). The hanging-indent opener
  (`ここからN字下げ、折り返してM字下げ`) is the same `indent` family carrying a
  `wrap` parameter, so it too closes with the shared `字下げ終わり`.
- A **single-line** directive (no `ここから`, no closer) governs only the rest
  of its line and is a **zero-width marker** node (`indent` / `align-end`),
  not a wrapping container (§7.4). It does not capture following lines.
- Breaks persist across a **block** container (not flagged); a break sharing
  a line with a **single-line** directive drops it (§6.9, §7.4).
- Reference rendering (§8): block → `<div class="aozora-container
  aozora-container-<family>">…</div>` (indent adds `aozora-container-indent-N`
  and `data-amount="N"`; the hanging form adds `aozora-container-wrap-indent`
  and `data-wrap="M"`); single-line → a marker
  `<span class="aozora-indent aozora-indent-N">` / `<span class="aozora-align-end"
  data-offset="N">`.
- The official guidance is to prefer an annotation over inserted whitespace,
  so the same visual layout round-trips through the directive, not spaces.

## Error conditions

- [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  — a closer of a different family than its opener (e.g. indent opened,
  end-align closed).
- [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  — a `ここから…` opener naming no known container kind (kept as a generic
  annotation, §6.14).
- [`break-in-single-line-container`](../diagnostics.md#break-in-single-line-container)
  — a break sharing a single-line directive's line (§7.4).

## Further layout directives

The official guide defines additional layout families: 字詰め
(`ここからN字詰め`), 中央揃え (`ここから中央揃え`), and 地寄せ (margined
right-align). Their notation is catalogued in
[Annex C.2](../annex/slugs.md). This revision pins normative semantics for
字下げ (including the 折り返し字下げ hanging form) and 地付き / 地上げ; the
remaining layout families are deferred to a later revision (§10.5). A processor
encountering an unrecognised `ここから…` opener retains it as a generic
annotation (§6.14) and reports
[`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive).

## Conformance vectors

`indent_container`, `wrap_indent`, `align_end_container`, `nested_containers`,
`mismatched-container-close`, `unrecognised-container-directive`,
`break-in-single-line-container`.
