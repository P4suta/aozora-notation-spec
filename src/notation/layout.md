# 6.6 Layout containers (字下げ・地付き ほか)

## Synopsis

Layout directives control horizontal placement of lines: **indentation**
(字下げ), **end-alignment** (地付き / 地上げ, i.e. flush to the foot of the
vertical line), line length (字詰め), centring (中央揃え), and margined
right-alignment (地寄せ). Each has a **block** form (a paired container
governing many lines) and, for indent, end-align, and centring, a
**single-line** form; line length (字詰め) has a block form only. This section
pins indentation (including the hanging-indent 折り返し字下げ form),
end-alignment, line length, the **single-line** centring marker
(`ページの左右中央` / `中央揃え`), and the combined indent-plus-centre form
(`ここからN字下げ、ページの左右中央`). The block centring form (which has no
closer in practice) and the remaining compound directives are deferred
(§10.5); they are catalogued in [Annex C.2](../annex/slugs.md).

## Notation

```text
［＃ここから2字下げ］          ← block indent opener
　本文…
［＃ここで字下げ終わり］        ← closer

［＃ここから5字下げ、ページの左右中央に］  ← indent + page-centre
　献辞…
［＃ここで字下げ終わり］

［＃ここから2字下げ、折り返して4字下げ］  ← hanging indent (first line 2, wrap 4)
　長い本文が折り返して4字下げされる…
［＃ここで字下げ終わり］

［＃ここから改行天付き、折り返して1字下げ］  ← 改行天付き hanging (first line flush, wrap 1)
　和歌や箇条書きの本文…
［＃ここで字下げ終わり］

［＃2字下げ］この行だけ        ← single-line indent
［＃改行天付き、折り返して2字下げ］この行  ← single-line 改行天付き hanging
［＃天から3字下げ］この行だけ   ← single-line head-anchored indent
［＃地付き］平和への誓い        ← single-line end-align (foot)
［＃地から2字上げ］…           ← single-line end-align, 2 from the foot
［＃ページの左右中央］          ← single-line centring marker (page centre)

［＃ここから地付き］…［＃ここで地付き終わり］          ← block end-align
［＃ここから地から2字上げ］…［＃ここで字上げ終わり］   ← block end-align (margin)

［＃ここから26字詰め］…［＃ここで字詰め終わり］        ← block line-width (26 chars/line)
```

```abnf
indent-block-open = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ" RBRACK
indent-wrap-open  = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ、折り返して" 1*DIGIT %s"字下げ" RBRACK
indent-headflush-open = LBRACK HASH %s"ここから改行天付き、折り返して" 1*DIGIT %s"字下げ" RBRACK
indent-center-open = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ、" ( %s"ページの左右中央" [ %s"に" ] / %s"左右中央" ) RBRACK
indent-single     = LBRACK HASH 1*DIGIT %s"字下げ" RBRACK
indent-headflush-single = LBRACK HASH %s"改行天付き、折り返して" 1*DIGIT %s"字下げ" RBRACK
indent-fromtop-single = LBRACK HASH %s"天から" 1*DIGIT %s"字下げ" RBRACK
line-width-open   = LBRACK HASH %s"ここから" 1*DIGIT %s"字詰め" RBRACK
align-end-single  = LBRACK HASH %s"地付き" RBRACK
                  / LBRACK HASH %s"地から" 1*DIGIT %s"字上げ" RBRACK
center-single     = LBRACK HASH ( %s"ページの左右中央" / %s"中央揃え" ) RBRACK
```

(`1*DIGIT` admits ASCII or full-width digits.)

## Parameters

- **amount** — for indent, the number of full-width characters to indent.
- **wrap** — for the hanging-indent form (折り返し字下げ), the indent applied
  to wrapped continuation lines after the first; absent for a plain indent.
- **head_flush** — `true` for the 改行天付き hanging form
  (`改行天付き、折り返してM字下げ`): the first line is flush to the head
  (天付き, so **amount** is `0`) and only wrapped lines indent by **wrap**.
- **from_top** — `true` for the head-anchored single-line form
  (`天からN字下げ`), the top-edge counterpart of `地からN字上げ`. Rendered
  identically to a plain `N字下げ`; the flag preserves the source spelling.
- **center** — `true` for the combined `ここからN字下げ、ページの左右中央`
  form (the indented block is also page-centred); `false` otherwise.
- **offset** — for end-align, the distance from the foot: `0` (地付き) or `N`
  (地からN字上げ).
- **width** — for line-width (字詰め), the number of full-width characters per
  line the enclosed run is set to.

## Semantics

- A **block** opener/closer pair (§7.1) yields a `container` node (family
  `indent`, `align-end`, or `line-width`) governing the enclosed lines;
  containers nest (§7.3). Pairing is by **family**, so a `2字下げ` opener pairs
  with a plain `字下げ終わり` (§7.2). The hanging-indent opener
  (`ここからN字下げ、折り返してM字下げ`) is the same `indent` family carrying a
  `wrap` parameter, so it too closes with the shared `字下げ終わり`. The
  combined opener `ここからN字下げ、ページの左右中央` is likewise the `indent`
  family — carrying a `center` flag (an indented, page-centred block) — and
  also closes with `字下げ終わり`.
- The **line-width** opener (`ここからN字詰め`) is the `line-width` family
  carrying a `width` parameter; it is **block-only** (no single-line form) and
  closes with `字詰め終わり` (§7.2).
- The **end-align** block opener (`ここから地付き` / `ここから地からN字上げ`) is
  the `align-end` family carrying an `offset` parameter, closed by **either**
  `字上げ終わり` or `地付き終わり` (pairing is by family, §7.2). The opener's
  `offset` is authoritative; the closer carries none. Round-tripping (§7.6)
  preserves that offset and canonicalises the closer to `地付き終わり`.
- A **single-line** directive (no `ここから`, no closer) governs only the rest
  of its line and is a **zero-width marker** node (`indent` / `align-end` /
  `center`), not a wrapping container (§7.4). It does not capture following
  lines. The centring marker (`ページの左右中央` / `中央揃え`) flags its line as
  page-centred; the actual centring is a presentation concern (§8).
- Breaks persist across a **block** container (not flagged); a break sharing
  a line with a **single-line** directive drops it (§6.9, §7.4).
- Reference rendering (§8): block → `<div class="aozora-container
  aozora-container-<family>">…</div>` (indent adds `aozora-container-indent-N`
  and `data-amount="N"`; the hanging form adds `aozora-container-wrap-indent`
  and `data-wrap="M"`; line-width adds `data-width="N"`); single-line → a marker
  `<span class="aozora-indent aozora-indent-N">` / `<span class="aozora-align-end"
  data-offset="N">` / `<span class="aozora-center">`.
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

This revision pins normative semantics for 字下げ (including the 折り返し字下げ
hanging form), 地付き / 地上げ, 字詰め (`ここからN字詰め`), and the single-line
centring marker (`ページの左右中央` / `中央揃え`). Deferred to a later revision
(§10.5): the **block** centring form (`ここから…中央…`, which has no closer in
practice), margined right-alignment (地寄せ), and **compound** directives that
combine families in one bracket (e.g. `ここから2字下げ、中央揃え`). Their notation
is catalogued in [Annex C.2](../annex/slugs.md). A processor encountering an
unrecognised `ここから…` opener retains it as a generic annotation (§6.14) and
reports
[`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive).

## Conformance vectors

`indent_container`, `wrap_indent`, `align_end_container`, `line_width_container`,
`center_page`, `nested_containers`, `mismatched-container-close`,
`unrecognised-container-directive`, `break-in-single-line-container`.
