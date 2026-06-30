# 6.20 Fractions (分数)

## Synopsis

The **分数** (fraction) forward reference typesets a short run as a fraction —
a numerator over a denominator — rather than as inline text. It is the
mathematical-typography sibling of the script glyphs (§6.16): a forward
reference with the `は` particle and a single target, yielding an `emphasis`
node. The official 注記一覧 lists it among the emphasis-page treatments
([AOZORA-ANNOTATION], `etc.html`); the corpus attests only the
forward-reference form.

## Notation

**Forward reference only** — quote the target; the treatment applies to the
most recent preceding occurrence (§7.5). The particle is `は`. The target is a
fraction expression separated by a slash, either ASCII `/` (U+002F) or
fullwidth `／` (U+FF0F); both widths occur in the corpus.

```abnf
fraction = target "［＃「" target "」は分数］"
target   = numerator slash denominator
slash    = "/" / "／"
```

```text
1/4［＃「1/4」は分数］
１／４［＃「１／４」は分数］
```

Unlike 太字/斜体 (§6.12) there is **no bare inline range and no
`ここから`/`ここで` block range** for 分数: the official guide gives only the
forward-reference form, and the corpus attests only it. A comma-joined compound
that pairs 分数 with another treatment in one bracket
(`［＃「3」は上付き小文字、「1/143」は分数］`) is **not** this single-target shape; it
degrades to an unrecognised directive (§6.14) pending the multi-directive
grammar.

## Parameters

- **target** — the single quoted run to typeset. As with §6.16, the form names
  exactly one target; a multi-quote body is not a recognised shape and degrades
  (§6.14). The renderer splits the target on the first slash: text before the
  slash is the numerator, text after it the denominator.

## Semantics

- The form resolves its target by the look-back rule of §7.5 and yields an
  `emphasis` node over that run. It is an **inline** construct.
- The node carries the 分数 attribute so serialization (§7.6) can reconstruct
  the source directive, including the redundant preceding target copy,
  byte-exact.
- Reference rendering (§8): the target is split on the first slash into a
  numerator and a denominator, joined by the fraction slash `⁄` (U+2044) —

  ```text
  分数 → <span class="aozora-bunsu"><sup>NUM</sup>⁄<sub>DEN</sub></span>
  ```

  The `aozora-bunsu` wrapper distinguishes a fraction from the lone `<sup>` of
  §6.16 (`aozora-uwatsuki`); neither collides with the `<b>`/`<i>` of §6.12, the
  `<em>` of bouten (§6.2), or the `<ruby>` of §6.1. A target with no slash (not
  attested) renders verbatim inside the wrapper.

## Error conditions

- **Target with no referent** — a `は分数` directive whose quoted target does
  not occur in the preceding text has no earlier run to treat, so the quoted
  target is itself the treated run: a **self-contained** forward reference,
  rendered as the fraction wrapper above. Serialization reconstructs the
  directive byte-exact (§7.6); no input is lost (parallel to the §6.16 rule).

## Conformance vectors

`fraction_forward`, `fraction_forward_no_referent` (under
`conformance/vectors/`).
