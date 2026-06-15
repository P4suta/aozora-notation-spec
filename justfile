# The Aozora Bunko Notation Specification — dev tasks.
set shell := ["bash", "-uc"]

# List recipes.
default:
    @just --list

# Install the doc toolchain (mdBook + linkcheck backend).
setup:
    cargo install mdbook mdbook-linkcheck

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

# Everything CI runs (build needs mdBook; the rest is pure Python).
ci: validate abnf-check linkcheck build
