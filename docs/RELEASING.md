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

3. **Create the `release-assets` environment**: branches `main` + tags `v*`,
   **0 required reviewers** to start. Add a required reviewer later if you want a
   human checkpoint before assets are attached (the build is already separate and
   ungated).

4. **Add the App secrets to the `release` environment** (not repo-wide):
   `RELEASE_APP_CLIENT_ID` (the App's Client ID) and `RELEASE_APP_PRIVATE_KEY`
   (the App's generated private key, full PEM). This flips the workflow's
   `HAS_APP` gate to `true`.

5. **Trigger the first run:** `gh workflow run release-please.yml` (or push any
   commit to `main`). Release Please opens the first **Release PR** proposing
   `0.1.0` (forced by `release-as` in `release-please-config.json`). Because the
   App is a non-`GITHUB_TOKEN` identity, the required CI checks
   (`spec` / `lint` / `codeql (python)`) actually run on the PR.

6. **Curate + merge:** edit the Release PR branch so the generated
   `## [0.1.0]` CHANGELOG section keeps the curated prose from the old
   `[Unreleased]` block, then **squash-merge by hand** (auto-merge is force-
   disabled by `no-automerge-on-release-pr.yml`). The same run cuts tag `v0.1.0`,
   the GitHub Release, and uploads `aozora-notation-conformance-v0.1.0.{tar.gz,zip}`,
   `aozora-v0.1.0.abnf`, and `SHA256SUMS`.

7. **Remove the bootstrap lever:** delete `"release-as": "0.1.0"` from
   `release-please-config.json` so subsequent versions are inferred from commits.

8. **Lock the tags:** apply `release-tags.json` (immutable `v*`) per
   [`.github/rulesets/README.md`](../.github/rulesets/README.md). Optionally apply
   the App-only `v*` tag-creation lock last (after the first release).

## Day-to-day

Nothing manual. Land Conventional Commits on `main`; the Release PR keeps itself
up to date. When you want to cut a release, squash-merge the open Release PR.
