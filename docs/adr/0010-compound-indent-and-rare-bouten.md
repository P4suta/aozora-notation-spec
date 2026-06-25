# 0010. Compound indent modifiers canonicalise; rare bouten ranges stay deferred

- Status: accepted
- Date: 2026
- Governs: §6.6 (Layout containers), §6.2 (Bouten), the serialize and html projections

## Context

An indent opener may carry more than the bare `ここからN字下げ`. The corpus
shows it trailed by a `、`-separated **stack of clauses** — a page-centre flag,
a line-layout clause, and a small set of **decorative styles** — applied
together to one block:

```text
［＃ここから2字下げ、小さい活字］
［＃ここから4字下げ、横書き、中央揃え、罫囲み］
```

The clauses are written in **any order**, are spelled several ways
(`中央揃え` / `左右中央` / `ページの左右中央`; `ゴチック` / `ゴシック体`;
`横組み` / `横書き`), and mix one genuinely-distinct pair — `字詰め`
(characters-per-line) versus `字組み` (lines × characters). A re-serialising
processor therefore needs **one canonical form per compound** — the same
requirement [0003](0003-canonical-serialization-forms.md) fixes for the inline
families — or `parse ∘ serialize` is not a fixed point. It also needs a
**losslessness** rule for the open tail of this set: authors write clauses we do
not (yet) model, and an unrecognised clause must not silently change or drop the
block.

Two further notations sit at the boundary of this revision and were measured for
demand against the reference mirror (P4suta/aozorabunko_text, 17,889 works):

- The **rare bouten in BARE-RANGE form** — 鎖線 / 破線 / 黒三角傍点 written as a
  paired range `［＃鎖線］…［＃鎖線終わり］` — occurs **0** times. The
  forward-reference form (`語句［＃「語句」に鎖線］`) is the one the corpus uses
  and is already normative (its should-level vector `bouten_range_chain_line`
  covers it).
- The **block centring form with no closer** (`ここから中央揃え` = **0**;
  `ここからページの左右中央` = **11**, none with a closer) does not fit the
  paired-container model and is left deferred (§10.5); page-centring **within**
  an indent is supported by decision (a) below.

## Decision

### (a) The compound-indent modifier set is canonicalised

A compound `ここからN字下げ、…` opener is the **`indent` family**. Its clause
stack is **order-independent** on input; the serializer re-emits the recognised
clauses in a fixed **canonical order**:

```text
amount字下げ → 折り返してM字下げ → ページの左右中央に → {W字詰め | L行W字組みで}
            → ゴシック体 → 横書き → 罫囲み → 小さい活字
```

with **canonical spellings** normalised on serialize: `中央揃え` / `左右中央` →
`ページの左右中央に`; `ゴチック` → `ゴシック体`; `横組み` → `横書き`. The
line-layout clauses `字詰め` (LineWidth) and `字組み` (Kumi) stay **distinct**
and are never merged. The top-flush hanging form
`ここから天付き、折り返してM字下げ` models as amount `0` plus wrap `M`,
canonicalising to `ここから0字下げ、折り返してM字下げ`.

The four decorative styles are a **co-applied set** — `bold` (ゴシック体),
`horizontal` (横書き / 横組み), `framed` (罫囲み), `font` (小さい活字, a
one-stage-smaller font) — and the set is **open-ended**: a future decorative
modifier is one new clause alternative, not a model change.

**Decline-whole on losslessness.** A compound opener governs a container **only
when every clause is recognised**. If **any** clause is unrecognised
(`横組み右揃えで`, `数式`, `本文よりひとまわり大きい太ゴシック体`, or an
embedded notation construct such as `「」は返り点`), the **whole** `［＃…］` is
retained as a generic annotation (§6.14), reports
`unrecognised-container-directive`, and round-trips **byte-exact**. A
partially-recognised set never opens a container.

All compound indents **close with the single generic `字下げ終わり`** (pairing is
by family, §7.2; the open payload is authoritative). The redundant explicit
compound closer `字下げ終わり、〈X〉も終わり` folds to the canonical
`ここで字下げ終わり`.

The projections carry the set without a wire change. The **JSON wire is
unchanged**: the container-pair `kind` stays `"indent"` and `SCHEMA_VERSION` is
unchanged; like `amount` and `center`, the `styles` are **not** JSON node/pair
fields. They ride the reference HTML — one `<div>` with **flat** classes in the
same canonical order (`aozora-container-futoji`, `-yokogumi`, `-keigakomi`,
`-font-smaller` with `data-steps="1"`) — and the Pandoc key-values
(a space-joined `modifiers` kv). Conformance pins the styles via the `serialize`
and `html` projections (`indent_compound_styled`), not a new `nodes` field.

This **extends** [0003](0003-canonical-serialization-forms.md): it is the same
least-surprise canonical-form principle applied to a compound rather than a
single inline concept, and the `verbatim` projection still reproduces the
author's bytes regardless.

### (b) Rare bouten in bare-range form stays deferred and lossless

The bare-range bouten variants 鎖線 / 破線 / 黒三角傍点
(`［＃鎖線］…［＃鎖線終わり］`) are **not** promoted to a normative paired
container in this revision. They have **0** corpus occurrences, so there is no
demand to justify a new range family; the **forward-reference** form
(`語句［＃「語句」に鎖線］`) remains the normative spelling, already covered by the
should-level vector `bouten_range_chain_line`. A bare-range opener that names one
of these declines **losslessly** as a generic annotation (§6.14), exactly like an
unrecognised compound clause in (a), and round-trips byte-exact.

## Consequences

- A re-serialising processor has one diff-stable form per compound indent: the
  clause order and spelling are pinned, so `serialize` is a fixed point over the
  whole set (`serialize(parse(serialize(parse(x)))) == serialize(parse(x))`).
- The open tail of the decorative set costs nothing in faithfulness: any
  unmodelled clause keeps the whole bracket verbatim instead of opening a
  lossy container. Adding a recognised modifier later is purely additive.
- The corpus disposition of #78 shrinks the unknown count materially
  (Unknown 3418 → 2848 after this change), driven by the promoted compounds
  (小さい活字 49, ゴシック体 21, 罫囲み ~24, 横書き ~13, the 4-way
  字下げ・横書き・中央揃え・罫囲み, and 天付き 30) together with the structural
  leaves promoted alongside (本文終わり 242, 改行 165, owned by
  §6 structural-markers).
- Two boundaries stay explicit and corpus-justified rather than guessed: the
  bare-range bouten variants (0 occurrences) and the closer-less block centring
  form (`ここから中央揃え` 0, `ここからページの左右中央` 11, none closed) remain
  deferred in §10.5.

## Alternatives considered

- **Project the decorative styles as a JSON `styles` field.** Rejected: it
  would bump `SCHEMA_VERSION` and split the indent into a non-`"indent"` shape
  for a presentation-only decoration that the HTML/Pandoc projections already
  carry. `amount` and `center` set the precedent — layout decoration rides the
  classes/kvs, not the node/pair projection.
- **Open a container on a partially-recognised compound** (apply the known
  clauses, drop the unknown one). Rejected: it is lossy — the dropped clause
  cannot round-trip — and an unmodelled clause may change the block's meaning.
  Decline-whole keeps the bracket byte-exact.
- **Promote the bare-range bouten variants now** for symmetry with the
  forward form. Rejected on corpus evidence: 0 occurrences. The forward form is
  the attested spelling; a range family with no users is speculative surface
  area, and the lossless-generic decline already round-trips the rare case.

## References

- §6.6, §6.2, §7.2; [0003](0003-canonical-serialization-forms.md);
  diagnostic `unrecognised-container-directive`; official 注記一覧
  (字下げ・折り返し・地寄せ・傍点). Corpus counts are whole-corpus observations
  over the reference mirror (P4suta/aozorabunko_text, 17,889 works).
