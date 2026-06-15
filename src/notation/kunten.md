# 6.5 Kunten (訓点・返り点)

## Synopsis

Kunten are the marginal marks that let classical Chinese (漢文) be read in
Japanese word order. This section specifies **kaeriten** (返り点), the
reading-order *return marks*, and their **okurigana**. The official guide
also defines *saidoku-moji* (再読文字, characters read twice); see the note at
the end of this section.

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

## Saidoku-moji (再読文字)

The official guide also defines *saidoku-moji* — a character read twice with
different glosses (e.g. 未, 将, 当), marked with a re-reading note. The
notation belongs to 訓点; this revision specifies kaeriten and okurigana and
defers the full normative treatment of saidoku-moji to a later revision
(§10.5).

## Conformance vectors

`bracketed-kaeriten-no-pair`, `kaeriten-outside-kanbun`, and the kaeriten
recognition cases under `conformance/vectors/`.
