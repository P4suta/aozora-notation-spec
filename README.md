# The Aozora Bunko Notation Specification

A **normative, RFC-quality specification** of 青空文庫記法 (Aozora Bunko
notation) — the inline / block annotation language used by
[Aozora Bunko](https://www.aozora.gr.jp/) plain-text works (ruby
`｜青梅《おうめ》`, emphasis dots `［＃「X」に傍点］`, gaiji `※［＃…］`,
kunten/kaeriten, layout containers `［＃ここから2字下げ］…`, page breaks, …).

## Why this exists

Aozora Bunko's official 注記一覧 is authoritative but **prose-only and, in
places, underspecified** — it documents the notation by example without a
formal grammar, a precise processing model, or a machine-checkable
conformance suite. Downstream tools each re-derive the rules and drift.

This repository fixes the root cause: it defines the notation **like an
RFC** — RFC 2119 normative keywords, an [ABNF](https://www.rfc-editor.org/rfc/rfc5234)
grammar, an explicit processing model, a diagnostics catalogue, and a
**machine-readable conformance test-vector suite**. It is grounded in two
sources of truth:

1. the official 注記一覧 (<https://www.aozora.gr.jp/annotation/>), and
2. the real Aozora Bunko corpus (notation forms and frequencies observed in
   actual works).

Where the official documentation is silent or ambiguous, this spec makes an
**explicit normative decision** and records it in [`docs/adr/`](docs/adr/).

## Status

Draft `v0.1`. The framework and the §6 notation families are normative; a few
families the official guide itself treats as provisional are documented with
their notation, their full normative semantics deferred to a later revision.
See the [change log](src/annex/changelog.md).

This document is **not** affiliated with or endorsed by Aozora Bunko.

## Layout

| Path | Contents |
|---|---|
| `src/` | The specification (mdBook). Numbered normative sections + annexes. |
| `src/grammar/aozora.abnf` | The collected normative ABNF grammar. |
| `conformance/schema/vector.schema.json` | JSON Schema for a conformance test vector. |
| `conformance/vectors/` | The normative test-vector corpus (one directory per case). |
| `conformance/RUNNER.md` | The contract an implementation satisfies to claim conformance. |
| `docs/adr/` | Specification-level decision records. |

## Building

```sh
just build        # render the mdBook to ./book
just serve        # live preview
just linkcheck    # check internal/external links
just validate     # validate every conformance vector against the schema
just ci           # everything CI runs
```

mdBook and the link checker are installed by the tooling step (`just setup`)
or by CI; the conformance and ABNF validators are pure Python / Node and run
with the interpreters already on a typical dev box.

## Conformance and the "master" role

The intent is for this repository to become the **single source of truth**
that notation processors conform to. An implementation claims conformance by
running the vectors under `conformance/vectors/` per
[`conformance/RUNNER.md`](conformance/RUNNER.md) and matching every
`must`-level expectation. A consuming implementation pins this repository
(e.g. by git revision) and fails its CI on divergence.

## Licence

Dual-licensed under [Apache-2.0](LICENSE-APACHE) OR [MIT](LICENSE-MIT) —
permissive licensing so any implementation can adopt it.
