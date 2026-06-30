# The Aozora Bunko Notation Specification — dev tasks.
set shell := ["bash", "-uc"]

# List recipes.
default:
    @just --list

# Provision the dev toolchain (mdBook, Python, committed, …) via mise.
setup:
    mise install

# Install the lefthook git hooks (commit-msg + pre-push).
hooks:
    lefthook install

# Remove the lefthook git hook stubs.
hooks-uninstall:
    lefthook uninstall

# Render the spec to ./book.
build:
    mdbook build

# Live preview at http://localhost:3000.
serve:
    mdbook serve --open

# Validate every conformance vector against the JSON Schema.
validate:
    python3 tools/validate_vectors.py

# Check the ABNF grammar is well-formed.
abnf-check:
    python3 tools/abnf_check.py src/grammar/aozora.abnf

# Check internal cross-references and SUMMARY ↔ file consistency.
linkcheck:
    python3 tools/linkcheck.py

# Format all TOML in place (taplo); config in taplo.toml.
fmt:
    taplo fmt

# Check TOML formatting without writing (taplo) — the CI gate.
fmt-check:
    taplo fmt --check

# Spell-check the tracked sources (typos); config in _typos.toml.
typos:
    typos

# Everything CI runs (build needs mdBook; the rest is pure Python).
ci: validate abnf-check linkcheck typos fmt-check build
