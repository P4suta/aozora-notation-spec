# 0006. Automated releases via Release Please with a dormant GitHub App

- Status: accepted
- Date: 2026-06-30
- Deciders: @P4suta
- Tags: release, ci, security, supply-chain
- Governs: `.github/workflows/release-please.yml`, `release-please-config.json`, `.release-please-manifest.json`, `.github/workflows/no-automerge-on-release-pr.yml`, `.github/rulesets/release-tags.json`, `docs/RELEASING.md`

## Context

[ADR-0005](0005-adopt-semver-and-a-version-single-source-of-truth.md) gave the
spec SemVer and a machine version source; this ADR adds the automation that
cuts releases. Sibling `aozora` uses **release-plz**, but that is Cargo-only —
this repository is mdBook + Python + JSON with **no package registry**. So a
"release" here is a `vX.Y.Z` git tag, a GitHub Release whose notes come from the
CHANGELOG, and attached artifacts a consumer can pin. Two live constraints shape
the design: every branch requires **signed commits** (`require-signed-commits`,
empty bypass), and `main` requires PRs to pass the strict checks `spec` / `lint`
/ `codeql (python)`.

## Decision

1. **Release Please** (`release-please-action`, language-agnostic, `simple`
   release-type) maintains a single **Release PR** from Conventional Commits:
   it bumps `version.txt` + `CHANGELOG.md` and syncs the doc version strings
   (`extra-files`). Squash-merging the PR cuts the tag + GitHub Release; the
   **same workflow run** then builds and attaches the **conformance bundle**
   (`vectors/` + `schema/` + `RUNNER.md`) and **`src/grammar/aozora.abnf`**.
2. **A GitHub App identity, kept dormant** behind a `HAS_APP` boolean gate: with
   the App secrets unset the workflow is a green no-op; setting them activates it
   (see `docs/RELEASING.md`). The App is required because a `GITHUB_TOKEN`-opened
   PR does **not** trigger the required CI checks, so it could never satisfy
   branch protection.
3. **No signing bypass.** Release Please commits through the GitHub API, so its
   commits on the `release-please--*` branch are GitHub-signed and satisfy
   `require-signed-commits` with **no `bypass_actors` exemption** — the key
   simplification versus `aozora`'s release-plz, which raw-pushes unsigned
   commits and must exempt its App.
4. **No tag-triggered fan-out.** Assets attach in the same run via the action's
   `release_created` output, so we never depend on a tag-push event (a
   `GITHUB_TOKEN`-pushed tag would not fire downstream workflows).
5. **Hardening:** least-privilege per-job `permissions`, a credential-scoping
   `release` environment, a separately-gateable `release-assets` environment
   (ungated build, optionally reviewer-gated upload), SHA-pinned actions, and a
   `no-automerge-on-release-pr` guard so a release is always a deliberate manual
   squash-merge. Tags are made immutable by `release-tags.json`.

## Consequences

- Releases become a one-action event (merge the Release PR); the CHANGELOG is
  the single source of the release notes, so they cannot drift.
- The scaffold can land long before any App exists — it is inert until ignited,
  so there is no half-configured window.
- The cost is the one-time App/environment/ruleset setup, documented as a runbook
  in `docs/RELEASING.md`.

## Alternatives considered

**release-plz** (the sibling's tool). Rejected: Cargo-only; it manages a
`[workspace.package].version` and crates.io publishing that do not exist here.

**Hand-cut tags + a tag-fired release workflow.** Rejected: no version source of
truth (the drift ADR-0005 fixes), and a `GITHUB_TOKEN`-pushed tag does not
trigger downstream workflows — the very pitfall the single-run design avoids.

**A long-lived PAT instead of an App.** Rejected for posture: a PAT is a
long-lived credential tied to a person; the App is installation-scoped, rotates
short-lived tokens, and matches the sibling repo's model.

## References

- Workflow: `.github/workflows/release-please.yml`; guard:
  `.github/workflows/no-automerge-on-release-pr.yml`
- Config: `release-please-config.json`; ledger: `.release-please-manifest.json`;
  machine version: `version.txt`
- Tag protection: `.github/rulesets/release-tags.json` (+ `.github/rulesets/README.md`)
- Activation runbook: `docs/RELEASING.md`
- Versioning basis: [ADR-0005](0005-adopt-semver-and-a-version-single-source-of-truth.md)
- Sibling precedent: `aozora` ADR-0009 / its release-plz workflows (the Cargo
  analogue this adapts)
