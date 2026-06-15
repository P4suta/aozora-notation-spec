# 5. Lexical Syntax

This section defines how the sanitized source (§4) is decomposed into
**elements**: directives, ruby spans, gaiji references, double-bracket
bouten, accent spans, and runs of plain text. The complete grammar is
[Annex D](annex/abnf.md); the key productions are inlined below.

## 5.1 Element stream

```abnf
document = *element
element  = gaiji-ref / ruby / double-ruby / accent-span / directive / text
```

A processor scans the source left to right, at each position recognizing the
**longest** construct that begins there; if none begins there, the position
contributes to a `text` run. This **leftmost-longest** rule is normative and
resolves the alternatives of `element` (ABNF cannot express the negative
lookahead that "is not the start of a construct" requires). Two consequences:

- A `《《` opens a [double-bracket bouten](notation/bouten.md), never two
  ruby openers, because `double-ruby` out-matches `ruby` at that position.
- A `※` immediately followed by `［＃` is a [gaiji reference](notation/gaiji.md)
  (`gaiji-ref`), not a bare reference mark plus a directive.

## 5.2 Directives

```abnf
directive = LBRACK HASH body RBRACK        ; ［＃ body ］
body      = *body-char                     ; any scalar except ］
```

A **directive** is the universal annotation form: a full-width `［`, a
full-width `＃`, an opaque **body**, and a full-width `］`. Directives do not
nest a `］`; the body runs to the first `］`. The body MAY itself contain
corner-quoted targets (`「…」`) and parenthesised parameters (`（…）`), which
are significant to body classification but not to this lexical layer.

What a directive *means* is determined by classifying its body — this is the
**notation catalogue** of §6. Classification is a function of the body string
(and, for forward-reference directives, of the surrounding text per §7).
A body that matches no known form is retained as a
[generic annotation](notation/annotation.md) (§6.14); a processor MUST NOT
discard it, preserving the guarantee that no bare `［＃` ever reaches output.

## 5.3 Ruby

```abnf
ruby        = [ BAR base ] RUBY-OPEN reading RUBY-CLOSE   ; ［｜］base《reading》
double-ruby = RUBY-OPEN RUBY-OPEN reading RUBY-CLOSE RUBY-CLOSE   ; 《《…》》
```

A **ruby** span is an optional explicit base introduced by `｜`, then a
reading inside `《 … 》`. Without the `｜`, the base is determined by the
look-back rule of §6.1. The detailed semantics are §6.1; the adjacent-double
form `《《…》》` is §6.2.

## 5.4 Gaiji references

```abnf
gaiji-ref = REFMARK directive              ; ※［＃ … ］
```

A **gaiji reference** is a reference mark `※` immediately followed by a
directive. The directive body carries the glyph description and, optionally, a
JIS X 0213 men-ku-ten or a `U+XXXX` code point; resolution is §6.4.

## 5.5 Accent spans

```abnf
accent-span = TORT-OPEN accent-body TORT-CLOSE   ; 〔 … 〕
```

An **accent span** `〔…〕` encloses Latin letters written with a following
combining indicator (`e'` → `é`). It is recognized lexically here but
**resolved during normalization** (§4); by the time §6 classification runs,
an accent span has already been folded to combined Unicode. An accent span
does not cross a line boundary (§4).

## 5.6 Text

All other source is **text**. Text is opaque to this layer except that its
boundaries are set by the leftmost-longest rule of §5.1.

## 5.7 Coordinates

Every element carries a **span**: the half-open `[start, end)` byte range it
occupies in the sanitized source (§2.3). Spans of the top-level element stream
tile the source contiguously, without gaps or overlap. All offsets reported in
§6, §9, and the conformance vectors are these sanitized-source byte offsets.
