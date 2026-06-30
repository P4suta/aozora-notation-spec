# Releasing the specification

Releases are automated by **Release Please** (`.github/workflows/release-please.yml`,
[ADR-0006](adr/0006-automated-releases-via-release-please-with-a-dormant-github-app.md)).
Conventional Commits on `main` accumulate into a single **Release PR** that bumps
`version.txt` + `CHANGELOG.md` and syncs the doc version strings; squash-merging
that PR cuts the `vX.Y.Z` tag, the GitHub Release (notes from the CHANGELOG), and
attaches the conformance bundle + ABNF.

The workflow ships **dormant**: until a release GitHub App is configured it is a
green no-op. The steps below activate it. They are a one-time maintainer task.

## Versioning

Semantic Versioning, pre-1.0 contract ([ADR-0005](adr/0005-adopt-semver-and-a-version-single-source-of-truth.md)):
while `0.x`, a normative-breaking change (`feat!:` / `BREAKING CHANGE:`) bumps the
**minor**; `feat:` / `fix:` bump the **patch**. `version.txt` is the machine
source of truth, maintained by `.release-please-manifest.json`; never hand-edit
either.

## Activation (one-time)

1. **Create a GitHub App** (under your account or the org) and install it on
   `P4suta/aozora-notation-spec`. Repository permissions:
   - **Contents: Read & write** (push the `release-please--*` branch; create the
     tag + Release),
   - **Pull requests: Read & write** (open / maintain the Release PR),
   - (add **Issues: Read & write** only if Release Please label creation fails).
   No webhook needed. Record the **Client ID**; also note the numeric **App ID**
   if you intend to apply the optional tag-creation lock later.

2. **Create the `release` environment** (Settings → Environments):
   deployment branch policy = `main` only, **no required reviewers**, no wait
   timer. (Its only job is to scope the App secrets; the human gate is the
   manual Release-PR merge, so a reviewer here would just stall PR upkeep.)

3. **Add the App secrets to the `release` environment** (not repo-wide):
   `RELEASE_APP_CLIENT_ID` (the App's Client ID) and `RELEASE_APP_PRIVATE_KEY`
   (the App's generated private key, full PEM). This flips the workflow's
   `HAS_APP` gate to `true`.

4. **Trigger the first run:** `gh workflow run release-please.yml` (or push any
   commit to `main`). Release Please opens the first **Release PR** proposing
   `0.1.0` (forced by `release-as` in `release-please-config.json`). Because the
   App is a non-`GITHUB_TOKEN` identity, the required CI checks
   (`spec` / `lint` / `codeql (python)` / `release-gate`) actually run on the PR.

5. **Approve + curate + merge:** add the **`release: approved`** label to the
   Release PR — the deliberate "we are releasing" step; the required `release-gate`
   check stays red without it (re-run that job after labelling). Edit the Release
   PR branch so the generated `## [0.1.0]` CHANGELOG section keeps the curated prose
   from the old `[Unreleased]` block, then **squash-merge by hand** (auto-merge is
   force-disabled by `no-automerge-on-release-pr.yml`). The same run cuts tag
   `v0.1.0`, the GitHub Release, and uploads
   `aozora-notation-conformance-v0.1.0.{tar.gz,zip}`, `aozora-v0.1.0.abnf`, and
   `SHA256SUMS` — each with SLSA build provenance (ADR-0007).

6. **Remove the bootstrap lever:** delete `"release-as": "0.1.0"` from
   `release-please-config.json` so subsequent versions are inferred from commits.

7. **Tag protection** is already applied as code — `release-tags.json` (immutable
   `v*`) and the App-only `v*` *creation* lock (ADR-0007); see
   [`.github/rulesets/README.md`](../.github/rulesets/README.md). Nothing to do
   here unless you rotate the App (then re-inject its App ID into the creation lock).

## Day-to-day

Nothing manual. Land Conventional Commits on `main`; the Release PR keeps itself
up to date. When you want to cut a release, add **`release: approved`** to the
Release PR (satisfies `release-gate`) and squash-merge it by hand.
