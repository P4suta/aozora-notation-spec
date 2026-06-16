# 6.5 Kunten (訓点・返り点)

## Synopsis

Kunten are the marginal marks that let classical Chinese (漢文) be read in
Japanese word order. This section specifies **kaeriten** (返り点), the
reading-order *return marks*, their **okurigana**, and the **left-side ruby**
that — composed with these — expresses a *saidoku-moji* (再読文字, a character
read twice). See the final subsection.

## Notation

Kaeriten are recognized only in **bracketed** form — a mark inside a
directive:

```text
有［＃二］朋自遠方来［＃一］
未［＃レ］嘗［＃（ハ）］
```

```abnf
kaeriten = LBRACK HASH ( ladder-mark / okurigana ) RBRACK
```

- **ladder-mark** — one of the single marks `一 二 三 四 上 中 下 甲 乙 丙
  丁 レ` or the `Xレ` compounds `一レ 二レ 三レ 上レ 中レ 下レ`
  ([Annex C.5](../annex/slugs.md)).
- **okurigana** — parenthesised kana `（…）`, a reading aid.

A bare reading-mark glyph written inline in running text (`有レ朋`) is
**not** recognized — a processor cannot tell a genuine 返り点 from an ordinary
`一`/`上`/`レ` in prose, which is exactly why the bracketed form exists.

## Parameters

- **mark** — the literal mark text; classified into a family and rank for the
  pairing check (below). The ladder families and bases are: numeric
  `一<二<三<四` (base `一`), jouge `上<中<下` (base `上`), kō-otsu
  `甲<乙<丙<丁` (base `甲`). `レ` is standalone; okurigana never ladders.

## Semantics

- Each recognized mark yields a `kaeriten` node carrying the mark text.
- Reference rendering (§8) is `<sup class="aozora-kaeriten">mark</sup>`.
- Serialization reconstructs `［＃mark］` byte-exact (§7.6).

### Pairing (document-wide base presence)

A return mark of rank ≥ 2 implies the existence of its family **base**. A
processor checks this **document-wide** and base-only: if a mark of rank ≥ 2
(`二`/`三`/`四`, `中`/`下`, `乙`/`丙`/`丁`) appears but its family base
(`一`/`上`/`甲`) is absent from the entire document, it raises
[`bracketed-kaeriten-no-pair`](../diagnostics.md#bracketed-kaeriten-no-pair)
(error).

The scope is deliberately the whole document and the test deliberately
base-only — **not** per-clause and **not** a strict contiguous ladder. This
is forced by the corpus: real kanbun writes `二` before `一` (reading order),
return-mark groups routinely span `、`/`。` and line boundaries, and 上下点
legitimately uses just `上`…`下` (skipping `中`). A narrower scope or stricter
ladder flags valid kanbun. This decision is recorded in
`docs/adr/0001-kaeriten-pairing-rule.md`.

## Error conditions

- [`bracketed-kaeriten-no-pair`](../diagnostics.md#bracketed-kaeriten-no-pair)
  — see Pairing above.
- [`kaeriten-outside-kanbun`](../diagnostics.md#kaeriten-outside-kanbun)
  (warning) — a conservative heuristic: when a document contains exactly one
  kaeriten and its surroundings read as ordinary kana prose, the lone mark is
  likely a stray annotation, not a return mark. A document with a cluster of
  kaeriten (real 漢文) is never flagged.

## Left-side ruby and saidoku-moji (再読文字)

*Saidoku-moji* (再読文字) — a kanbun character read twice with different glosses
(e.g. 未, 将, 当) — has **no dedicated notation**. It is written as a
*composition* of constructs already defined: a **left-side ruby** for the
second reading, plus okurigana and a return mark. For example, 未 read
「いまだ…ず」 is `未［＃「未」の左に「ザル」のルビ］［＃（ダ）］［＃レ］`.

The **left-side ruby** is the one piece §6 does not otherwise cover. A
forward-reference directive attaches a reading to the *left* of the preceding
run (vs §6.1 ruby, which is on the right):

```text
未［＃「未」の左に「ザル」のルビ］
```

```abnf
left-ruby = LBRACK HASH LQUOTE target RQUOTE %s"の左に" LQUOTE reading RQUOTE %s"のルビ" RBRACK
```

- **target** — the preceding run the reading attaches to (resolved by §7.5).
- **reading** — the left-side reading text.

A left-side ruby yields a `ruby` node with a *left* side. Reference rendering
(§8): `<ruby>X<rp>(</rp><rt class="aozora-ruby-left">Y</rt><rp>)</rp></ruby>`.
Serialization reconstructs `X［＃「X」の左に「Y」のルビ］` byte-exact (§7.6). The
right-side variant (`の右に…のルビ`) is deferred (§10.5); the left-side
*annotation* form (`の左に…の注記`) is covered next.

## Side annotation (注記)

A **side annotation** (注記) attaches an editorial note — *not* a phonetic
reading — to the *left* of the preceding run. It shares the forward-reference
shape of the left-side ruby but ends in `の注記`, so a processor keeps it
distinct: a `side-note` node, never `ruby`.

```text
未来［＃「未来」の左に「みらい」の注記］
```

```abnf
side-note = LBRACK HASH LQUOTE target RQUOTE %s"の左に" LQUOTE note RQUOTE %s"の注記" RBRACK
```

- **target** — the preceding run the note attaches to (resolved by §7.5).
- **note** — the left-side annotation text.

A side annotation yields a `side-note` node. Reference rendering (§8) places the
note like a left-side ruby but marks it a note:
`<ruby>X<rp>(</rp><rt class="aozora-sidenote">Y</rt><rp>)</rp></ruby>`.
Serialization reconstructs `X［＃「X」の左に「Y」の注記］` byte-exact (§7.6). The
right-side annotation form (`の右に…の注記`) is deferred (§10.5).

## Conformance vectors

`bracketed-kaeriten-no-pair`, `kaeriten-outside-kanbun`, `left_ruby`,
`side_note_left`, and the kaeriten recognition cases under
`conformance/vectors/`.
