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

`enforce_admins`-equivalent behaviour is the **empty `bypass_actors`** — no
one, including admins, bypasses the rulesets. The repo has no release-plz / App
automation, so there are no `bypass_actors` exemptions to inject (unlike the
sibling `aozora` repo).

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

# Verify.
gh api "repos/$REPO/rulesets" --jq '.[] | {id, name, target, enforcement}'

# Re-sync after editing a file — PUT by id (POST would create a duplicate;
# GitHub allows same-named rulesets).
id=$(gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="main-branch-protection") | .id')
gh api "repos/$REPO/rulesets/$id" -X PUT --input .github/rulesets/main-branch.json
```

## Not included yet

- **`release-tags.json`** (immutable `v*` tags) — deferred until the spec
  actually cuts versioned releases. The CHANGELOG is still `[Unreleased]`
  (draft v0.1), so there is nothing to protect yet.
