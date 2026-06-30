# Decision records

Where the official 注記一覧 is silent or admits more than one reading, this
specification makes an explicit normative decision and records it here, with
its rationale, so the choice is auditable. Each record is referenced from the
section it governs.

These are [MADR 4.0](https://adr.github.io/madr/) Architecture Decision Records.
Read the one that governs an area before changing what it governs. Once accepted
an ADR is never edited for content — it is *superseded* by a later ADR that links
back. (Clerical metadata — date format, `Deciders`, `Tags` — may be normalised.)

| ADR | Title | Status |
|---|---|---|
| [0001](0001-kaeriten-pairing-rule.md) | Kaeriten pairing is document-wide base presence | accepted |
| [0002](0002-implicit-ruby-base-extent.md) | Implicit ruby base extends over one character class | accepted |
| [0003](0003-canonical-serialization-forms.md) | Canonical serialization picks one surface form per concept | accepted |
| [0004](0004-compound-indent-and-rare-bouten.md) | Compound indent modifiers canonicalise; rare bouten ranges stay deferred | accepted |
| [0005](0005-adopt-semver-and-a-version-single-source-of-truth.md) | Adopt SemVer and a version single source of truth | accepted |
| [0006](0006-automated-releases-via-release-please-with-a-dormant-github-app.md) | Automated releases via Release Please with a dormant GitHub App | accepted |

Decisions are grounded in the official guide and the real Aozora Bunko
corpus; corpus frequency claims cite the observation that motivated them.

## Authoring a new ADR

1. Scaffold with `just new-adr "Short imperative title"` (copies
   `0000-template.md` to the next sequential number, slugifies the title, and
   stamps today's date).
2. Fill in the sections; cite the two sources of truth (official 注記一覧 +
   corpus) and keep paragraphs short and action-oriented.
3. Add a row to the table above and set `Governs:` to the section(s) it binds.
4. Reference the ADR in the commit body and open a PR. ADRs are normally
   accepted on merge; controversial ones land as `proposed` and flip to
   `accepted` once the discussion concludes.

## Numbering

ADRs use a single sequential counter starting at `0001`, with no gaps. The next
ADR is `0007`. `just new-adr` picks the next number automatically (highest + 1).
