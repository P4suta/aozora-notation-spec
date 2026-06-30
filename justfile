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

# Everything CI runs (build needs mdBook; the rest is pure Python).
ci: validate abnf-check linkcheck build

# Scaffold a new ADR under docs/adr/ from the template: picks the next
# 4-digit number, slugifies the title, stamps today's date, and writes a
# skeleton. Pure host-side file templating — no toolchain needed.
#   just new-adr "Make the kaeriten check streaming"
new-adr TITLE:
    #!/usr/bin/env bash
    set -euo pipefail
    last=$(ls docs/adr/ | grep -oE '^[0-9]{4}' | sort -n | tail -1)
    n=$(printf '%04d' $((10#$last + 1)))
    slug=$(printf '%s' "{{TITLE}}" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')
    f="docs/adr/${n}-${slug}.md"
    [[ -e "$f" ]] && { echo "$f already exists" >&2; exit 1; }
    cp docs/adr/0000-template.md "$f"
    sed -i -e "s/^# NNNN. TITLE_HERE/# ${n}. {{TITLE}}/" -e "s/YYYY-MM-DD/$(date +%F)/" "$f"
    echo "Created $f"
