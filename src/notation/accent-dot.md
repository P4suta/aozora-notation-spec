# 6.21 Dotted letters (ドット付き)

## Synopsis

The **ドット付き** (dotted-letter) directive composes a combining dot above or
below a base Latin letter in the immediately-preceding run — `m` → ṁ, `s` → ṣ.
It records the diacritics of transliterated Sanskrit / Pāli that Aozora Bunko's
plain-text encoding cannot spell directly. It is a forward reference with the
`は` particle, yielding an `emphasis` node.

This is a **distinct mechanism** from the §6.19 accent decomposition of Annex A:
that scheme rewrites ASCII digraphs (`a` + `` ` `` → à) inside a `〔…〕` span at
the character level; this directive instead *names* a letter of the preceding
run and asks for a dot. The two compose — a dotted letter frequently sits inside
an already-decomposed `〔…〕` span (see the vectors).

The official 注記一覧 ([AOZORA-ANNOTATION]) lists it among the emphasis-page
treatments; the corpus attests only the forward-reference form.

## Notation

The directive has **no `「X」` quoted target**. Its body is a selector that names
a letter (and, optionally, which occurrence) of the preceding run, the `は`
particle, a position (`上` above / `下` below), and the keyword `ドット付き`.

```abnf
dotted     = run "［＃" clause *( ( "。" / "、" ) clause ) "］"
clause     = selector "は" [ set-adv ] position "ドット付き"
selector   = [ ordinal ] letters
ordinal    = number "つめの" / "最後の" / "前の" / "後の"
set-adv    = "ともに" / "それぞれ"
position   = "上" / "下"
letters    = 1*ALPHA            ; ASCII letters, case-significant for the glyph
number     = 1*DIGIT            ; ASCII or fullwidth digits
```

A body may carry several `。`- or `、`-joined clauses; every clause addresses the
**same** preceding run, and their substitutions are applied together.

```text
Sam［＃mは上ドット付き］
Sisa［＃２つめのsは下ドット付き］
Visnu［＃snはともに下ドット付き］
〔Mīhr〕［＃hは下ドット付き］
Samsa［＃mは上ドット付き。２つめのsは下ドット付き］
Konkana［＃前のnは上ドット付き、後のnは下ドット付き］
```

`run` is the source text immediately preceding the bracket: a bare Latin word,
or a whole `〔…〕` accent span (whose tortoiseshell brackets are retained).

## Parameters

- **selector** — names the base letter(s):
  - a **bare** letter (`m`) selects the first *composable* occurrence in the run
    (a word-initial capital with no dotted glyph, e.g. the `N` of `Nara-sinha`,
    is skipped in favour of the intended lowercase letter);
  - an **ordinal** `Nつめの` / `最後の` / `前の` / `後の` selects the N-th /
    last / first / last occurrence, **counting case-insensitively** (an
    uppercase `S` is occurrence 1 for a `２つめのs` over `Sīsa`); `前の` / `後の`
    name the earlier / later of a letter's two occurrences across a `、`-joined
    pair; the selected position must itself be composable;
  - a **cluster** of several letters with `ともに` / `それぞれ` dots each listed
    letter's first occurrence independently (`sn` → the first `s` and first `n`).
- **position** — `上` (dot above) or `下` (dot below).

The `ともに` / `それぞれ` adverb is spelling-only: it is preserved verbatim on
serialization but does not change which occurrences are dotted.

## Semantics

- The directive resolves against the reclaimed preceding run (§7.5) and yields an
  `emphasis` node over it, with `Reclaimed` provenance: the run is pulled back so
  the composed span is its sole rendered copy, and serialization (§7.6) re-emits
  the literal run followed by the raw directive body, byte-exact. It is an
  **inline** construct.
- Composition is **NFC**: each `(letter, position)` pair maps to a single
  precomposed scalar (ṁ U+1E41, ṅ U+1E45, ṃ U+1E43, ṇ U+1E47, ṣ U+1E63, ṭ U+1E6D,
  ḥ U+1E25, ṛ U+1E5B, ḍ U+1E0D, and capitals Ṭ U+1E6C, Ṛ U+1E5A). Composition is
  case-preserving (`t` → ṭ, `T` → Ṭ).
- Reference rendering (§8) emits the composed run inside a wrapper —

  ```text
  ドット付き → <span class="aozora-accent-dot">…composed run…</span>
  ```

  `aozora-accent-dot` does not collide with any other treatment's class.
- A **multi-clause** body applies every clause's substitutions to the one
  reclaimed run (resolve-all-then-substitute, so an earlier dot never shifts a
  later clause's index) and still yields a single node.

## Error conditions

- **No reclaimable run** — when a `》` ruby close or Japanese text butts the
  bracket there is no preceding Latin run (dot-over-ruby-base is not
  representable in a text-only forward leaf, the bouten-over-ruby limitation of
  §6.2). The directive degrades to an unrecognised directive (§6.14), rendered as
  a hidden raw span and serialized verbatim.
- **Absent or un-composable occurrence** — a selector naming a letter absent from
  the run, an ordinal out of range, or a `(letter, position)` pair with no
  precomposed glyph (e.g. an uppercase `S` below) degrades likewise, losing no
  input.
- **Word-qualified and 段目 forms** — a word-qualified selector (`simhaのm…`) and
  a `段目` table-row reference (`４段目、Sinhaのn…`) address a *named word* or a
  table row rather than the adjacent run; their `、`-split pieces are not pure
  ASCII-letter selectors, so they degrade to an unrecognised directive. A body
  in which *any* clause fails to parse degrades as a whole.

## Conformance vectors

`accent_dot_above`, `accent_dot_below`, `accent_dot_tortoise`,
`accent_dot_ordinal`, `accent_dot_uppercase`, `accent_dot_cluster`,
`accent_dot_multi_clause`, `accent_dot_former_latter`,
`accent_dot_ruby_base_unknown`, `accent_dot_dangyou_unknown` (under
`conformance/vectors/`).
