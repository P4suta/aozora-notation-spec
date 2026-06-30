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

`main-branch.json` requires the `spec`, `lint`, and `codeql (python)` checks
(`integration_id: 15368` is GitHub Actions). These must match the actual job
names in `.github/workflows/` — if a workflow job is renamed, update the
context here too. `commitlint` is intentionally **not** required: it is skipped
on Dependabot PRs (see `ci.yml`), and a skipped required check blocks the merge;
the commit-msg lefthook hook plus the visible PR check cover it.

> Apply this only **after** the `lint` job (shared-config PR) and the
> `codeql` workflow (this PR) have merged to `main`, so all three contexts
> exist; otherwise PRs wait forever on a check that never runs.

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

## Optional, apply after the first release

- **App-only `v*` tag creation.** Once the spec cuts its first release, a
  maintainer MAY add an inline ruleset restricting `v*` tag *creation* to the
  release App (`rules: [{ "type": "creation" }]`, `bypass_actors` = the App as an
  `Integration`). Built inline with `jq` — not a committed file, since an empty
  `bypass_actors` would lock out everyone, including the App. Apply it **last**,
  after the first successful release, so it never blocks a manual bootstrap tag.
  (Mirrors sibling `aozora`'s "release-tags-app-only".)
