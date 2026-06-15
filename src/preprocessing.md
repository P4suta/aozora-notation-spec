# 4. Pre-processing (Normalization)

Before lexing (§5), a processor applies a **normalization** pass producing the
*sanitized source* (§2.3). Normalization is defined to be **loss-free**: the
serializer (§7/§8) reconstructs the original notation, so normalization never
discards information a round-trip needs.

The steps apply in order.

## 4.1 BOM removal

Leading U+FEFF code points are removed (§3.2). Removal is a prefix operation;
it shifts subsequent offsets but introduces no other change.

## 4.2 Line-ending normalization

Every CRLF (U+000D U+000A) and every lone CR (U+000D) is replaced by a single
LF (U+000A). After this step the text contains no CR.

## 4.3 Accent decomposition (`〔…〕`)

An accent span `〔…〕` (§5.5) encloses Latin letters written with a following
ASCII combining indicator; the span is rewritten to the combined Unicode
form. For example `〔e'〕` → `é`, `〔u"〕` → `ü`, `〔n~〕` → `ñ`. The exact
indicator-to-combining-mark mapping is normative and given in
[Annex A](annex/accent-table.md).

Rules:

- An accent span **MUST** begin and end on the same line; an unterminated
  `〔` on a line is not an accent span (it is literal text).
- The whole accented word or phrase is enclosed, not each letter
  individually, matching the official guidance.
- A processor that performs decomposition **MUST** report
  [`accent-decomposition-applied`](diagnostics.md#accent-decomposition-applied)
  (severity `note`) for each span that actually contained a digraph, and the
  reported span is in **post-decomposition** coordinates (the rewrite is not
  length-preserving).
- The transform is loss-free: the serializer reconstructs the `〔…〕` source
  form (§7).

A `〔…〕` whose body contains no recognized digraph is left unchanged and
emits no diagnostic.

## 4.4 Reserved-code-point neutralization

If the source contains a code point the processor reserves internally (§3.4),
the processor neutralizes it here and reports
[`source-contains-pua`](diagnostics.md#source-contains-pua). The neutralized
form is implementation-defined but **MUST NOT** be mistakable for a notation
construct.

## 4.5 Presentational normalization (optional)

A processor MAY apply additional presentational normalizations that do not
change which constructs are recognized — for example, isolating a long
horizontal rule line (a run of `─`, `-`, `=` …) onto its own block so it
renders as a separator. Such steps are OPTIONAL, **MUST** be loss-free, and
**MUST NOT** alter the element stream of §5. They are not part of the
conformance contract.

## 4.6 Result

The output of §4 is the sanitized source. All later phases, all spans in this
document, and all conformance vectors are defined over it.
