# 0005. Adopt SemVer and a version single source of truth

- Status: accepted
- Date: 2026-06-30
- Deciders: @P4suta
- Tags: release, versioning, docs
- Governs: `CHANGELOG.md`, `version.txt`, §1.3 (Document status), §10.2 / §10.4 (Conformance), Annex E (`src/annex/changelog.md`), `conformance/RUNNER.md`

## Context

This specification needs versioned, citable releases so a conforming processor
can pin a stable target (§10.2 / §10.4 ask consumers to pin the spec). Two
problems block that:

1. **No machine-readable version.** The string `v0.1` is hand-duplicated across
   six places — `CHANGELOG.md`, `src/title.md`, `src/introduction.md` (§1.3),
   `README.md`, and `src/annex/changelog.md` (heading + versioning prose). There
   is no single fact a tool or a release process can read or write; every bump
   would be a manual search-and-replace that some file always misses.
2. **The `vMAJOR.MINOR` scheme is not tool-parseable and lacks a patch level.**
   It cannot express an editorial fix that changes nothing normative, and no
   release tool recognises a two-component version.

## Decision

1. **Adopt [Semantic Versioning](https://semver.org)** (`vMAJOR.MINOR.PATCH`)
   for the specification, replacing `vMAJOR.MINOR`.
2. **Pre-1.0 compatibility contract.** While the version is `0.x`, a normative
   change that **can break a conforming processor** bumps the **minor**
   (`0.x → 0.(x+1).0`); a backward-compatible addition or fix bumps the
   **patch**. At `1.0.0` the contract switches to the usual MAJOR-for-breaking.
   This is the faithful translation of the old rule (only a normative-breaking
   change moves the headline component).
3. **`version.txt` is the machine source of truth** — a one-line, greppable
   version string kept in lockstep by the release tooling's
   `.release-please-manifest.json` ledger (see the companion release-automation
   ADR, ADR-0006). Neither file is ever hand-edited.
4. **Docs derive, never compete.** The version strings in §1.3, the title page,
   `README.md`, and Annex E are **mechanically rewritten** by the release tool
   (each carries an `x-release-please-version` marker). Policy prose stays
   **version-neutral** ("pin a tagged release", "the current release") and never
   inlines a number anywhere else.
5. **Consumers pin a tagged release.** §10.2 / §10.4, `README.md`, and
   `conformance/RUNNER.md` now recommend pinning a `vX.Y.Z` release tag; pinning
   a git revision remains acceptable.

## Consequences

- One machine fact (`version.txt`) means the documented version cannot disagree
  with itself; the spec gains citable, immutable release points.
- The version bump is a single mechanical step the release tool performs, not a
  repo-wide manual edit — and unlike sibling `aozora`'s ADR-0009 (which keeps one
  hand-reconciled pin and rejected build-time substitution as over-engineering),
  this repo gets the doc-string sync **for free** because the release tool
  already rewrites those files; no preprocessor is added.
- The cost is the discipline of merging the Release PR (the one human step).

## Alternatives considered

**Keep `vMAJOR.MINOR`.** Rejected: no patch level for editorial fixes, and no
release tool parses a two-component version, so the automation in ADR-0006 could
not drive it.

**An mdBook preprocessor that substitutes `{{version}}` at build.** Genuinely
single-source, but adds a preprocessor and build-time coupling for a number
touched a handful of times a year. The release tool's `extra-files` rewrite
achieves the same single-source guarantee with no new build machinery.

**Manifest only, no `version.txt`.** Rejected for ergonomics: tools and
consumers want one plain greppable file, not the release tool's internal JSON.

## References

- Machine source: `version.txt`; ledger: `.release-please-manifest.json`
- Mechanically-synced docs: `src/title.md`, `src/introduction.md` (§1.3),
  `README.md`, `src/annex/changelog.md`
- Consumer pin guidance: §10.2 / §10.4 (`src/conformance.md`),
  `conformance/RUNNER.md`, `README.md`
- Release automation that maintains all of the above: ADR-0006 (automated
  releases via Release Please, dormant GitHub App)
- Sibling precedent: `aozora` ADR-0009 (single source of truth for version pins)
