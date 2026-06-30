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
(`ページの左右中央` / `中央揃え`), and the **compound indent** opener — an
indent whose `ここからN字下げ` carries a trailing, `、`-separated stack of
clauses (page-centre, line layout, and the decorative styles ゴシック体 /
横書き / 罫囲み / 小さい活字). The block centring form (which has no closer in
practice) and margined right-alignment (地寄せ) remain deferred (§10.5); they
are catalogued in [Annex C.2](../annex/slugs.md).

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

［＃ここから天付き、折り返して1字下げ］      ← top-flush hanging indent (amount 0, wrap 1)
　長い本文が折り返して1字下げされる…
［＃ここで字下げ終わり］

［＃ここから2字下げ、小さい活字］          ← compound indent + decorative style
　一段小さい活字で組まれた2字下げの本文…
［＃ここで字下げ終わり］

［＃ここから4字下げ、横書き、中央揃え、罫囲み］  ← compound indent + style stack
　横書き・中央揃え・罫囲みの4字下げブロック…
［＃ここで字下げ終わり］

［＃2字下げ］この行だけ        ← single-line indent
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
indent-center-open = LBRACK HASH %s"ここから" 1*DIGIT %s"字下げ、" ( %s"ページの左右中央" [ %s"に" ] / %s"左右中央" ) RBRACK

; compound opener: amount字下げ followed by an open-ended `、`-separated
; stack of clauses (one new modifier = one new `indent-clause` alternative).
; `天付き` is the amount-0 spelling for the top-flush hanging form.
indent-compound-open = LBRACK HASH %s"ここから" ( 1*DIGIT %s"字下げ" / %s"天付き" ) 1*( "、" indent-clause ) RBRACK
indent-clause = %s"折り返して" 1*DIGIT %s"字下げ"                                  ; wrap
              / ( %s"ページの左右中央" [ %s"に" ] / %s"左右中央" / %s"中央揃え" )    ; center
              / 1*DIGIT %s"字詰め" / 1*DIGIT %s"行" 1*DIGIT %s"字組み" [ %s"で" ]    ; line layout
              / %s"ゴシック体" / %s"横書き" / %s"横組み" / %s"罫囲み" / %s"小さい活字" ; decorative style

indent-single     = LBRACK HASH 1*DIGIT %s"字下げ" RBRACK
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
- **center** — `true` for a compound indent carrying a page-centre clause
  (`ページの左右中央` / `左右中央` / `中央揃え`); the indented block is also
  page-centred. `false` otherwise.
- **offset** — for end-align, the distance from the foot: `0` (地付き) or `N`
  (地からN字上げ).
- **width** — for line-width (字詰め), the number of full-width characters per
  line the enclosed run is set to.
- **styles** — for a compound indent, the **co-applied decoration set** carried
  by the opener's clause stack: any of `bold` (ゴシック体), `horizontal`
  (横書き / 横組み), `framed` (罫囲み), and `font` (小さい活字, a one-stage-smaller
  font). The set is **order-independent** on input and **open-ended**: a future
  decorative modifier is one new clause without changing the model (it rides the
  same projections, below). Empty for a plain or center-only indent.

## Semantics

- A **block** opener/closer pair (§7.1) yields a `container` node (family
  `indent`, `align-end`, or `line-width`) governing the enclosed lines;
  containers nest (§7.3). Pairing is by **family**, so a `2字下げ` opener pairs
  with a plain `字下げ終わり` (§7.2). The hanging-indent opener
  (`ここからN字下げ、折り返してM字下げ`) is the same `indent` family carrying a
  `wrap` parameter, so it too closes with the shared `字下げ終わり`. The
  compound opener `ここからN字下げ` followed by a `、`-separated clause stack is
  likewise the `indent` family — carrying a `center` flag and a `styles` set
  drawn from the stack — and **all** compound indents close with the single
  generic `字下げ終わり` (pairing is by family; the **open** payload is
  authoritative). The redundant explicit compound closer
  `字下げ終わり、〈X〉も終わり` folds to the canonical `ここで字下げ終わり`.
- **Compound clause canonicalisation.** The clause stack is **order-independent**
  on input. The serializer re-emits the recognised clauses in a fixed
  **canonical order**: `amount字下げ` → `折り返してM字下げ` →
  `ページの左右中央に` → `{W字詰め | L行W字組みで}` → `ゴシック体` → `横書き` →
  `罫囲み` → `小さい活字`. **Canonical spellings** are normalised on serialize:
  `中央揃え` / `左右中央` → `ページの左右中央に`; `ゴチック` → `ゴシック体`;
  `横組み` → `横書き`. The line-layout clauses `字詰め` (LineWidth) and
  `字組み` (Kumi) are **distinct** and are never merged. The top-flush hanging
  form `ここから天付き、折り返してM字下げ` models as amount `0` plus wrap `M` and
  canonicalises to `ここから0字下げ、折り返してM字下げ`. These canonical picks are
  fixed by [ADR-0004](../../docs/adr/0004-compound-indent-and-rare-bouten.md)
  (extending [ADR-0003](../../docs/adr/0003-canonical-serialization-forms.md)).
- **Decline-whole on any unknown clause (losslessness).** A compound opener
  governs a container **only when every clause is recognised**. If **any**
  clause is unrecognised (e.g. `横組み右揃えで`, `数式`,
  `本文よりひとまわり大きい太ゴシック体`, or an embedded forward reference such
  as `「」は返り点`), the **whole** `［＃…］` is retained as a generic annotation
  (§6.14), reports
  [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive),
  and round-trips **byte-exact**. A partially-recognised set never opens a
  container.
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
- A **compound** indent renders to a **single** `<div>` (one `</div>`) carrying
  **flat** classes: the indent's own classes plus, in the same canonical clause
  order, each decorative style's standalone container class — `ゴシック体` →
  `aozora-container-futoji`, `横書き` → `aozora-container-yokogumi`, `罫囲み` →
  `aozora-container-keigakomi`, `小さい活字` → `aozora-container-font-smaller`
  (with `data-steps="1"`). `data-amount` is emitted as today; the page-centre
  flag adds the centre class as for the existing combined form. The
  **JSON wire is unchanged**: the container-pair `kind` stays `"indent"` and
  `SCHEMA_VERSION` is unchanged. Like `amount` and `center`, the decorative
  `styles` are **not** projected as JSON node/pair fields — they ride the HTML
  classes and the Pandoc key-values (a space-joined `modifiers` kv). Conformance
  therefore pins the styles via the `serialize` and `html` projections, not via
  a new `nodes` field.
- The official guidance is to prefer an annotation over inserted whitespace,
  so the same visual layout round-trips through the directive, not spaces.

## Error conditions

- [`mismatched-container-close`](../diagnostics.md#mismatched-container-close)
  — a closer of a different family than its opener (e.g. indent opened,
  end-align closed).
- [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  — a `ここから…` opener naming no known container kind, **or** a compound
  opener carrying **any** unrecognised clause (the decline-whole rule, above):
  the whole `［＃…］` is kept as a generic annotation (§6.14) and round-trips
  byte-exact, opening no container.
- [`break-in-single-line-container`](../diagnostics.md#break-in-single-line-container)
  — a break sharing a single-line directive's line (§7.4).

## Further layout directives

This revision pins normative semantics for 字下げ (including the 折り返し字下げ
hanging form and the top-flush 天付き form), 地付き / 地上げ, 字詰め
(`ここからN字詰め`), the single-line centring marker
(`ページの左右中央` / `中央揃え`), and the **compound indent** opener whose
`ここからN字下げ` carries a `、`-separated clause stack — a page-centre clause,
a line-layout clause (`字詰め` / `字組み`), and the decorative styles ゴシック体,
横書き (= 横組み), 罫囲み, and 小さい活字 (canonical order, spellings, and the
decline-whole-on-unknown rule are fixed in
[ADR-0004](../../docs/adr/0004-compound-indent-and-rare-bouten.md)).

Deferred to a later revision (§10.5): the **block** centring form
(`ここから中央揃え` / `ここからページの左右中央`, which has no closer in the
corpus and so does not fit the paired-container model — page-centring **within**
an indent is supported, above), and margined right-alignment (地寄せ). Also
deferred (and declining losslessly) are **embedded-directive** compounds, in
which a clause is itself another notation construct rather than a layout
modifier (e.g. `ここから2字下げ、「」は返り点`, `ここから字下げ、ここから数式`).
Their notation is catalogued in [Annex C.2](../annex/slugs.md). A processor
encountering an unrecognised `ここから…` opener — or a compound opener with any
unrecognised clause — retains it as a generic annotation (§6.14) and reports
[`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive).

## Conformance vectors

`indent_container`, `wrap_indent`, `align_end_container`, `line_width_container`,
`center_page`, `indent_compound_styled`, `nested_containers`,
`mismatched-container-close`, `unrecognised-container-directive`,
`break-in-single-line-container`.
