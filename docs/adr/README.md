# Decision records

Where the official 注記一覧 is silent or admits more than one reading, this specification makes an explicit normative decision and records it here, with its rationale, so the choice is auditable.
Each record is referenced from the section it governs.

These are [MADR 4.0](https://adr.github.io/madr/) Architecture Decision Records.
Read the one that governs an area before changing what it governs.
Once accepted an ADR is never edited for content — it is *superseded* by a later ADR that links back.
(Clerical metadata — date format, `Deciders`, `Tags` — may be normalised.)

| ADR | Title | Status |
|---|---|---|
| [0001](0001-kaeriten-pairing-rule.md) | Kaeriten pairing is document-wide base presence | accepted |
| [0002](0002-implicit-ruby-base-extent.md) | Implicit ruby base extends over one character class | accepted |
| [0003](0003-canonical-serialization-forms.md) | Canonical serialization picks one surface form per concept | accepted |
| [0004](0004-compound-indent-and-rare-bouten.md) | Compound indent modifiers canonicalise; rare bouten ranges stay deferred | accepted |
| [0005](0005-adopt-semver-and-a-version-single-source-of-truth.md) | Adopt SemVer and a version single source of truth | accepted |
| [0006](0006-automated-releases-via-release-please-with-a-dormant-github-app.md) | Automated releases via Release Please with a dormant GitHub App | accepted |
| [0007](0007-release-safety-layers.md) | Release safety layers — approval gate, App-only tags, provenance | accepted |
| [Source preservation](preserve-source-during-recovery.md) | Preserve decoded source during recovery serialization | accepted |

Decisions are grounded in the official guide and the real Aozora Bunko corpus; corpus frequency claims cite the observation that motivated them.

## Authoring a new ADR

Name a new record after its decision and add `date: YYYY-MM-DD` to its front matter.
Use `0000-template.md` for the section structure.
Cite the official 注記一覧 and corpus evidence, and name the sections the decision governs.
Add the record to the index above and reference it from the affected specification sections.
ADRs normally become `accepted` on merge; keep an unaccepted decision `proposed`.

## Numbering

Existing numbered records keep their filenames and references.
New records use descriptive paths instead of the sequential `just new-adr` scaffold.
