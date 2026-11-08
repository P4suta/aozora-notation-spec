---
date: 2026-11-08
status: proposed
---
# Sync release App credentials to the main environment

## Context

The release App still requires a private key.
Doppler's [identity limit](https://docs.doppler.com/docs/platform-limits) constrains a separate identity for every repository and purpose.

## Decision

Use [native synchronization](https://docs.doppler.com/docs/github-actions) from a purpose-specific Doppler config into the `release` environment.
Restrict that environment to main before connecting the sync.
Reference canonical credentials using GitHub-compatible names.
Pass individual secrets only to the App token action.
Keep attestation OIDC.

## Alternatives

Doppler OIDC avoids GitHub copies and retains workflow and event checks, but consumes identity capacity.
A service token creates another stored credential to rotate.

## Consequences

GitHub retains long-lived App credential copies.
Protected main and environment restrictions replace Doppler claims.
The shared App key retains its installation authority.
Minted tokens remain repository-scoped.
Reconsider when GitHub supports a direct workload identity for the App.

## Confirmation

Require successful initial synchronization and a manual authentication-only run from reviewed main.
Keep the existing Doppler identity until authentication succeeds.
Migration permits no release or tag.
