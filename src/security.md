# 11. Security Considerations

The notation is a markup language for archival text; processing untrusted
input nonetheless warrants care.

## 11.1 Resource exhaustion

Constructs nest (containers, §7.3) and forward references scan preceding text
(§7.5). A naive look-back that rescans from the document start for every
reference is quadratic in the number of references; a deeply nested or highly
pathological document can drive memory and time up. A processor **SHOULD**
bound look-back cost (e.g. an index of candidate targets) and **SHOULD** bound
nesting depth, degrading gracefully (a generic annotation) rather than
consuming unbounded resources.

## 11.2 Reserved-code-point confusion

A processor that uses private-use code points as internal markers (§3.4)
**MUST** neutralize any such code point appearing in the source (§4.4) and
report [`source-contains-pua`](diagnostics.md#source-contains-pua); otherwise
crafted input could forge internal markers and corrupt the placeholder
mapping, mis-attributing or mis-rendering spans.

## 11.3 Encoding confusion

Input may be Shift_JIS or UTF-8 (§3.1). Mis-detecting the encoding can change
which bytes form a delimiter and therefore which constructs are recognized. A
processor **SHOULD** obtain the encoding out of band where possible, and
**MUST** replace undecodable bytes with U+FFFD rather than guessing a
delimiter.

## 11.4 Output-context injection

The reference HTML (§8) escapes the five HTML-significant ASCII characters. A
processor emitting HTML (or any other structured output) **MUST** escape for
its output context; gaiji descriptions, annotation bodies, and resolved
targets are author-controlled text and **MUST NOT** be emitted into markup
unescaped.

## 11.5 Gaiji table trust

Gaiji resolution (§6.4, [Annex B](annex/gaiji.md)) maps men-ku-ten and
descriptions to Unicode via data tables. A processor **SHOULD** treat those
tables as a trusted, versioned input; a wrong mapping silently substitutes a
different glyph. Unresolved references degrade visibly
([`unresolved-gaiji`](diagnostics.md#unresolved-gaiji)) rather than guessing.
