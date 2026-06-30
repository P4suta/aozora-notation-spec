# 0007. Release safety layers — approval gate, App-only tags, provenance

- Status: accepted
- Date: 2026-07-01
- Deciders: @P4suta
- Tags: release, ci, security, supply-chain
- Governs: `.github/workflows/ci.yml` (`release-gate`), `.github/rulesets/main-branch.json`, the App-only tag-creation ruleset (`.github/rulesets/README.md`), `.github/workflows/release-please.yml` (provenance)

## Context

[ADR-0006](0006-automated-releases-via-release-please-with-a-dormant-github-app.md)
made releases automatic. Cutting a release is irreversible — `release-tags-immutable`
makes a `vX.Y.Z` tag undeletable, and a published Release is public — so the act of
cutting one deserves defence in depth, matching sibling `aozora`'s release guardrails.
Before this ADR the only release-specific guards were `no-automerge-on-release-pr` and
the immutable-tag ruleset; nothing forced a *deliberate* human decision to release, no
rule stopped a hand-pushed `v*` tag, and the published artifacts carried no provenance.

## Decision

Add three layers (Rust/registry-specific aozora layers — OIDC trusted publishing,
`cargo-semver-checks`, build-version stamping — are N/A and omitted):

1. **`release: approved` label gate.** A `release-gate` job in `ci.yml` fails a PR that
   carries Release Please's `autorelease: pending` label but **not** `release: approved`;
   it is a **required status check** (`main-branch.json`). A Release PR therefore cannot
   merge until a maintainer deliberately applies `release: approved`. Normal PRs (no
   `autorelease: pending`) pass unconditionally. Labels are read live, so re-running the
   job after labelling is enough.
2. **App-only `v*` tag creation.** An inline ruleset restricts `refs/tags/v*` **creation**
   to the release App (`rules:[{type:"creation"}]`, App in `bypass_actors` as an
   `Integration`). Combined with `release-tags-immutable` (delete/update/force), the full
   tag lifecycle is locked: only the App creates a release tag, and once created it is
   frozen. Kept inline (App ID injected at apply) — a committed file with an empty bypass
   would lock out the App itself.
3. **SLSA build provenance.** The `upload` job attests the release assets (conformance
   bundle + ABNF) with `actions/attest-build-provenance`, proving which workflow built
   which bytes from which commit (`gh attestation verify`). The assets — the authoritative
   conformance suite and grammar — are exactly what a consumer must trust, so attestation
   is valuable even though the spec ships no binaries. `SHA256SUMS` accompanies them.

Also: **the `release-assets` environment is removed.** With the reviewer gate declined it
held no secrets and no reviewers, so it added nothing; aozora has no such environment. The
`release` environment (which scopes the App secrets) stays.

## Consequences

- A release now requires two deliberate human acts on the Release PR — the `release:
  approved` label and the manual squash-merge — and cannot be triggered by a stray tag
  push. Defence in depth around an irreversible action.
- Downstream consumers can cryptographically verify the conformance suite / ABNF they pin.
- One more required check (`release-gate`) runs on every PR; it is a few-second label read
  and passes transparently on non-release PRs.
- Cost: the App ID must be re-injected into the creation lock if the release App is rotated
  (noted in `.github/rulesets/README.md`).

## Alternatives considered

**A `ci-success` aggregate check (as in aozora) instead of adding `release-gate` directly
to the required list.** Rejected: this spec already lists its checks directly in
`main-branch.json`; adding one more context is simpler than introducing an aggregate job.

**Keep `release-assets` with a required reviewer.** Rejected for now: the Release itself
is already gated by the label, the spec holds no publish credentials, and a sole
maintainer approving their own deployment adds friction without meaningful protection. The
upload job is ungated; a reviewer can be re-introduced later if desired.

**A committed `release-tags-app-only.json`.** Rejected: its base state (empty
`bypass_actors`) would lock out the App, so it is applied inline with the App ID injected.

## References

- `release-gate`: `.github/workflows/ci.yml`; required via `.github/rulesets/main-branch.json`
- App-only tag creation + the immutable-tag ruleset: `.github/rulesets/README.md`,
  `.github/rulesets/release-tags.json`
- Provenance: `.github/workflows/release-please.yml` (`upload` job)
- Builds on: [ADR-0006](0006-automated-releases-via-release-please-with-a-dormant-github-app.md)
- Sibling precedent: `aozora` ADR-0020 (release secret hardening / trusted publishing) —
  the registry/OIDC parts of which are N/A here
