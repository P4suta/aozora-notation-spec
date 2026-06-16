# Annex C. Directive vocabulary (slugs)

This annex enumerates the controlled vocabulary of directive keywords — the
fixed strings a directive body (§5.2) is classified against. It is the
companion data to §6. Keywords are matched against the body verbatim;
parameter slots are shown as `N` (a decimal count, ASCII or full-width) or
`…` (a quoted target / path).

## C.1 Breaks (§6.9)

| Keyword | Construct |
|---|---|
| `改ページ` | page break |
| `改丁` | section break — recto/leaf |
| `改段` | section break — column |
| `改見開き` | section break — spread |

## C.2 Layout containers (§6.6)

| Opener | Closer | Family |
|---|---|---|
| `ここからN字下げ` (and `ここから字下げ`) | `ここで字下げ終わり` | indent (block) |
| `ここからN字下げ、折り返してM字下げ` | `ここで字下げ終わり` | indent (hanging) |
| `ここから地付き` / `ここから地からN字上げ` | `ここで地付き終わり` / `ここで字上げ終わり` | align-end (block) |
| `ここからN字詰め` | `ここで字詰め終わり` | line-width (block) |
| `N字下げ` | (single line) | indent |
| `地付き` / `地からN字上げ` | (single line) | align-end |

Further layout keywords (§6.6, deferred): `ここから中央揃え`/`ここで中央揃え終わり`,
`…地寄せ`.

## C.3 Keigakomi (§6.7) and warichu (§6.8)

| Opener | Closer |
|---|---|
| `罫囲み` | `罫囲み終わり` |
| `割り注` | `割り注終わり` |

## C.4 Bouten / bousen variants (§6.2)

The 点 (dot) family and 線 (line) family. Each appears in the inline
forward-reference form (`［＃「X」に <kw>］`) and the range form
(`［＃<kw>］ … ［＃<kw>終わり］`), optionally prefixed by `左に` for the left
side.

| Keyword | Family | Slug |
|---|---|---|
| `傍点` | 点 | `goma` |
| `白ゴマ傍点` | 点 | `white-sesame` |
| `丸傍点` | 点 | `circle` |
| `白丸傍点` | 点 | `white-circle` |
| `二重丸傍点` | 点 | `double-circle` |
| `蛇の目傍点` | 点 | `janome` |
| `ばつ傍点` | 点 | `cross` |
| `白三角傍点` | 点 | `white-triangle` |
| `波線` | 線 | `wavy-line` |
| `傍線` | 線 | `under-line` |
| `二重傍線` | 線 | `double-under-line` |
| `鎖線` | 線 | `chain-line` |
| `破線` | 線 | `dashed-line` |
| `黒三角傍点` | 点 | `black-triangle` |

(鎖線 / 破線 / 黒三角傍点 are official but corpus-sparse; a processor renders
them like any other variant where it has a glyph, otherwise degrading per
§6.14.)

## C.5 Kaeriten marks (§6.5)

**Single** (12): `一` `二` `三` `四` `上` `中` `下` `甲` `乙` `丙` `丁` `レ`.
**Compound** (6, `Xレ`): `一レ` `二レ` `三レ` `上レ` `中レ` `下レ`.
**Okurigana**: `（…）` (parenthesised kana).

Ladder families and bases (§6.5): numeric `一<二<三<四` (base `一`), jouge
`上<中<下` (base `上`), kō-otsu `甲<乙<丙<丁` (base `甲`). `レ` is standalone.

## C.6 Other directives

| Keyword / shape | Construct |
|---|---|
| `挿絵（…）入る` | illustration (§6.11) |
| `「X」は…見出し` | heading hint (§6.10) |
| `「X」は縦中横` | tate-chu-yoko (§6.3) |
| `「X」に「ママ」の注記` / `「X」は底本では「Y」` | editor annotation (§6.14) |

Any body matching no keyword here is a generic annotation (§6.14); a
`ここから…` opener matching no container raises
[`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive).
