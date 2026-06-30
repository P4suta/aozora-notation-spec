# Repository rulesets (as code)

Branch protection for `P4suta/aozora-notation-spec` lives here as
version-controlled JSON, applied through the GitHub REST API. This is the
modern replacement for classic branch-protection rules: reviewable in a PR,
reproducible, and auditable — instead of opaque clicks in the settings UI.

GitHub's own ruleset import/export uses exactly this JSON shape
(`POST/PUT /repos/{owner}/{repo}/rulesets`), so these files round-trip with the UI.

## The rulesets

| File | Target | What it enforces |
| --- | --- | --- |
| `main-branch.json` | default branch | required checks (strict), PR (0 approvals, dismiss-stale, conversation resolution), linear history, no force-push, no deletion |
| `require-signed-commits.json` | all branches | signed commits |
| `release-tags.json` | `v*` tags | immutable: no delete / update / force-push |

`enforce_admins`-equivalent behaviour is the **empty `bypass_actors`** — no
one, including admins, bypasses the rulesets. The release automation (Release
Please, ADR-0006) needs **no `bypass_actors` exemption**: it commits through the
GitHub API, so its commits are already GitHub-signed and satisfy
`require-signed-commits` — unlike sibling `aozora`'s release-plz, which raw-pushes
unsigned commits and must exempt its App.

### Required status checks

`main-branch.json` requires the `spec`, `lint`, `codeql (python)`, and
`release-gate` checks (`integration_id: 15368` is GitHub Actions). These must
match the actual job names in `.github/workflows/` — if a workflow job is
renamed, update the context here too. `release-gate` enforces the
`release: approved` label on a Release PR (ADR-0007). `commitlint` is
intentionally **not** required: it is skipped on Dependabot PRs (see `ci.yml`),
and a skipped required check blocks the merge; the commit-msg lefthook hook plus
the visible PR check cover it.

> Add a context here only **after** the job exists on `main`; otherwise every
> PR waits forever on a check that never runs. (`release-gate` was added with
> ADR-0007, after its `ci.yml` job merged.)

## Applying / re-syncing (maintainer only)

A maintainer runs these with repo-admin scope; committing the JSON does **not**
activate anything.

```sh
REPO=P4suta/aozora-notation-spec

# Create (POST). Run once per ruleset.
gh api "repos/$REPO/rulesets" -X POST --input .github/rulesets/main-branch.json
gh api "repos/$REPO/rulesets" -X POST --input .github/rulesets/require-signed-commits.json
gh api "repos/$REPO/rulesets" -X POST --input .github/rulesets/release-tags.json   # before the first release

# Verify.
gh api "repos/$REPO/rulesets" --jq '.[] | {id, name, target, enforcement}'

# Re-sync after editing a file — PUT by id (POST would create a duplicate;
# GitHub allows same-named rulesets).
id=$(gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="main-branch-protection") | .id')
gh api "repos/$REPO/rulesets/$id" -X PUT --input .github/rulesets/main-branch.json
```

## App-only `v*` tag creation (ADR-0007)

Complements `release-tags-immutable` (which blocks delete / update / force-push)
by restricting tag **creation** to the release App, so no human can hand-push a
`v*` tag to fire a release. **Inline only — never a committed file**, because a
committed file with an empty `bypass_actors` would lock out the App too. Apply
with the App's numeric **App ID** (App settings page — *not* the Client ID, *not*
the bot user id) injected at apply time:

```sh
REPO=P4suta/aozora-notation-spec
APP_ID=<release App's numeric App ID>
gh api "repos/$REPO/rulesets" -X POST --input <(jq -n --argjson app "$APP_ID" '{
  name: "release-tags-app-only",
  target: "tag",
  enforcement: "active",
  conditions: { ref_name: { include: ["refs/tags/v*"], exclude: [] } },
  rules: [{ type: "creation" }],
  bypass_actors: [{ actor_id: $app, actor_type: "Integration", bypass_mode: "always" }]
}')
```

Safe to apply pre-release: the first release's `v*` tag is created by the App
(release-please), not by hand. (Mirrors sibling `aozora`'s "release-tags-app-only".)
