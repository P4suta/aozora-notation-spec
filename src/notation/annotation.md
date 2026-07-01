# 6.14 Input-editor annotations (入力者注)

## Synopsis

Volunteer transcribers add editorial notes — flagging a surprising spelling
as faithful to the source (`ママ`), recording a divergence from the base text,
and so on. These are the **input-editor annotations**. This family also
includes the **generic annotation**: the defined fate of any `［＃…］` whose
body matches no other construct.

## Notation

```text
怪体な［＃「怪体」に「ママ」の注記］          ← "as-is from the source"
峰﹅［＃「峰」は底本では「峯」］              ← textual divergence note
本文［＃入力者注(5)］                        ← numbered input-typist note (→ 注5)
起上り［＃「起上り」にルビ］                 ← ruby-presence note (X carries ruby)
本文［＃ルビは「材木置場」にかかる］         ← ruby-binding note (ruby applies to X)
親［＃左にルビ付き］子［＃左に「よみ」のルビ付き終わり］  ← left-ruby span pair (reading on closer)
［＃なにかしらの注記］                       ← generic (unrecognised) annotation
```

```abnf
mama-note     = LBRACK HASH LQUOTE target RQUOTE %s"に「ママ」の注記" RBRACK
textual-note  = LBRACK HASH LQUOTE target RQUOTE %s"は底本では" LQUOTE alt RQUOTE RBRACK
editor-note   = LBRACK HASH %s"入力者注(" 1*DIGIT %s")" RBRACK   ; ASCII parens + digits
ruby-attached = LBRACK HASH LQUOTE target RQUOTE %s"にルビ" RBRACK
ruby-retarget = LBRACK HASH %s"ルビは" LQUOTE target RQUOTE %s"にかかる" RBRACK
ruby-pair-open  = LBRACK HASH %s"左にルビ付き" RBRACK
ruby-pair-close = LBRACK HASH %s"左に" LQUOTE reading RQUOTE %s"のルビ付き終わり" RBRACK
annotation    = directive          ; any body not classified by §6.1–§6.13
```

## Parameters

- **target** — for `ママ` and textual-note forms, the quoted run the note
  concerns (resolved per §7.5).
- **alt** — for a textual note, the base-text form the run diverges from.
- **index** — for the numbered input-typist note (`入力者注(N)`), the note
  number `N` (ASCII digits) referenced in the file's 凡例.

## Semantics

- A `ママ` note marks its target as intentionally reproduced from the source;
  a textual note records the base-text reading. Both yield an `annotation`
  node carrying the editorial kind and resolve their target by §7.5.
- A numbered `入力者注(N)` note yields an `annotation` node of editorial kind
  `editor-note`, rendered (§8) as a visible `注N` superscript rather than a
  hidden span. The **whole body** must match exactly; a compound note that
  merely cites a number (e.g. `底本では…。入力者注(6)`) stays a textual note.
- The **ruby-placement notes** — `「X」にルビ` (the run `X` carries a ruby
  gloss) and `ルビは「X」にかかる` (a nearby ruby applies to `X`) — are
  proofreading markers, **not** renderable ruby (the gloss text is not in the
  directive). Each yields an `annotation` node of editorial kind
  `ruby-attached` / `ruby-retarget`, rendered (§8) as a compact visible marker
  (`<sup class="aozora-ruby-note">ルビ</sup>`) rather than the run `X` — `X` is
  usually the adjacent text and re-emitting it would double-render. The raw
  bracket round-trips byte-exact (§7.6).
- The **left-side-ruby span pair** — `左にルビ付き` (opener) … `左に「Y」の
  ルビ付き終わり` (closer) — brackets a run carrying a left-side ruby whose
  reading `Y` is named on the closer. Both markers yield an `annotation` node
  (editorial kinds `ruby-pair-open` / `ruby-pair-close`); like the inline
  warichu pair they are independent raw-preserving directives, **not** coupled
  at the tree level. Reference rendering (§8) is a compact marker on each —
  `左ルビ` on the opener and `左ルビ「Y」` on the closer (the reading `Y` is a
  gloss, not surrounding text, so it does not double-render). Both round-trip
  byte-exact (§7.6).
- **Generic annotation (the catch-all).** Any directive whose body is not
  classified by §6.1–§6.13 yields a generic `annotation` node that **retains
  the directive's literal bytes**. A processor **MUST NOT** drop it: this is
  the guarantee that **no bare `［＃` ever reaches output** — every `［＃…］`
  is claimed, recognized or not. A `ここから…` body that looks like a
  container opener but names none additionally raises
  [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  (§6.6).
- Reference rendering (§8) preserves the annotation (e.g. a hidden or
  side-channel span); serialization reconstructs the original `［＃…］`
  byte-exact (§7.6).

## Error conditions

- [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  — a `ここから…` opener naming no known container.
- Forward-reference notes (`ママ`, textual) whose target is absent degrade per
  §7.5.

## Conformance vectors

`annotation`, `editor_note`, `ruby_attached`, `ruby_retarget`,
`left_ruby_pair`, `unrecognised-container-directive`.
