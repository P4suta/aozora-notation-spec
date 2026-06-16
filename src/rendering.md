# 8. Reference Rendering

This specification defines notation in terms of an abstract **node model**; a
processor's primary output is that structure (the `nodes` / `pairs`
projections of §10). This section gives a **reference rendering** to semantic
HTML5. The node model is normative; the specific HTML is a **reference
mapping** — informative, so that the conformance suite can pin a concrete
output, but a processor MAY target a different presentation.

## 8.1 Node model (normative)

Parsing yields a tree of nodes. Each node has a **kind** and a
sanitized-source **span**; container nodes have children. The kinds, with the
family that produces them, are:

| Kind | Family | Notes |
|---|---|---|
| `ruby` | §6.1 | base + reading |
| `bouten` | §6.2 | dot/line variant + side |
| `emphasis` | §6.12 | bold / italic weight (forward-reference form) |
| `tate-chu-yoko` | §6.3 | rotated run |
| `gaiji` | §6.4 | resolved scalar or description fallback |
| `kaeriten` | §6.5 | return-mark text |
| `indent` / `align-end` / `center` | §6.6 | single-line layout markers |
| `container` | §6.6/6.7/6.8/6.2/6.10/6.12/6.13 | paired; tagged by family |
| `page-break` / `section-break` | §6.9 | block leaves |
| `heading` | §6.10 | 大/中/小 level × standard/同行/窓 style |
| `sashie` | §6.11 | illustration reference |
| `annotation` | §6.14 | generic / editor annotation |
| `double-ruby` | §6.2 | `《《…》》` |

The `nodes` conformance projection lists recognized nodes in source order,
each with its span; container open/close appear as `containerOpen` /
`containerClose` entries (in source coordinates).

## 8.2 Reference HTML mapping (informative)

| Construct | HTML |
|---|---|
| Ruby | `<ruby>base<rp>(</rp><rt>reading</rt><rp>)</rp></ruby>` (a left-side ruby adds `class="aozora-ruby-left"` on the `<rt>`) |
| Bouten / bousen | `<em class="aozora-bouten aozora-bouten-<variant> aozora-bouten-<side>">…</em>` |
| Bold / italic (inline) | `<b class="aozora-bold">…</b>` / `<i class="aozora-italic">…</i>` |
| Tate-chu-yoko | `<span class="aozora-tcy">…</span>` |
| Gaiji (resolved) | the resolved character, optionally `<span class="aozora-gaiji" …>…</span>` |
| Gaiji (unresolved) | `<span class="aozora-gaiji" data-description="…">…</span>` |
| Kaeriten | `<sup class="aozora-kaeriten">…</sup>` |
| Single-line indent / align / center | `<span class="aozora-indent aozora-indent-N">` / `<span class="aozora-align-end" …>` / `<span class="aozora-center">` |
| Block container | `<div class="aozora-container aozora-container-<family>">…</div>` (incl. `table`, `columns` with `data-columns="N"`) |
| Heading (大/中/小 × style) | `<h1>`–`<h3>` (standard / 同行) or `<div>` (窓), `class="aozora-heading aozora-heading-<large\|medium\|small>"` plus `aozora-heading-<same-line\|window>` for a non-standard style |
| Heading hint (unpromoted) | `<span class="aozora-heading-hint" data-level data-style data-target hidden></span>` (`data-style` only when non-standard) |
| Page break | `<div class="aozora-page-break"></div>` |
| Section break | `<div class="aozora-section-break aozora-section-break-<choho\|dan\|spread>"></div>` |

Text is grouped into paragraphs (`<p>`); a blank line ends a paragraph; a
single newline within a paragraph is a `<br />`. The five HTML-significant
ASCII characters (`< > & " '`) are escaped. The reference renderer ships no
stylesheet; the `aozora-*` class hooks are presentation contracts a consumer
styles.

## 8.3 Why a reference mapping, not a mandated one

The notation describes Japanese typography (vertical writing, ruby, emphasis
dots); the faithful visual result depends on the rendering medium. Pinning a
reference HTML lets the suite check a concrete output and lets tools
interoperate, without forcing every processor — a paginator, an EPUB
builder, a search indexer — to emit identical markup. A processor claims
conformance against the projections it produces (§10.1).
