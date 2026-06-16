# 6. Notation Catalogue

This section defines every notation family: the directives and inline
constructs a processor recognizes, their parameters, and their meaning. Each
family is a subsection (§6.1–§6.14).

## 6.0.1 Per-family template

Every family subsection follows the same shape:

1. **Synopsis** — what the construct does, in one or two sentences.
2. **Notation** — the source forms, with an ABNF fragment and verbatim
   examples.
3. **Parameters** — any variable parts (counts, variant keywords, targets).
4. **Semantics** — normative behaviour (RFC 2119 keywords), including how the
   construct relates to the node model (§8) and serialization (§7).
5. **Error conditions** — the §9 diagnostics this family can raise.
6. **Conformance vectors** — the `conformance/vectors/` cases that pin it.

Where the official 注記一覧 is silent or ambiguous, the **Semantics** make an
explicit decision and cite a decision record under `docs/adr/`. A family
the official guide treats as provisional (§6.13) is documented here with its
notation; its full normative semantics are deferred (§10.5).

## 6.0.2 Family index

| § | Family | Notation (representative) |
|---|---|---|
| 6.1 | Ruby (ルビ) | `｜青梅《おうめ》` |
| 6.2 | Bouten / bousen (傍点・傍線) | `［＃「X」に傍点］`, `［＃傍点］…［＃傍点終わり］` |
| 6.3 | Tate-chu-yoko (縦中横) | `［＃「24」は縦中横］` |
| 6.4 | Gaiji (外字) | `※［＃「…」、第3水準1-85-54］` |
| 6.5 | Kunten (訓点・返り点) | `［＃二］ … ［＃一］`, `［＃（リ）］` |
| 6.6 | Layout containers (字下げ ほか) | `［＃ここから2字下げ］…`, `［＃地付き］` |
| 6.7 | Keigakomi (罫囲み) | `［＃罫囲み］…［＃罫囲み終わり］` |
| 6.8 | Warichu (割り注) | `［＃割り注］…［＃割り注終わり］` |
| 6.9 | Breaks | `［＃改ページ］`, `［＃改丁／改段／改見開き］` |
| 6.10 | Headings (見出し) | `［＃「序」は大見出し］` |
| 6.11 | Illustrations (挿絵) | `［＃挿絵（fig.png）入る］` |
| 6.12 | Bold / italic (太字・斜体) | `［＃太字］…［＃太字終わり］`, `［＃「X」は太字］` |
| 6.13 | Tables / columns (表・段組) | (page-described) |
| 6.14 | Input-editor annotations (入力者注) | `［＃「X」に「ママ」の注記］`, unrecognised `［＃…］` |
