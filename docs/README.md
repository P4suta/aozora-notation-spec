# Project guide

Draft `v0.1.0`. <!-- x-release-please-version -->

This is an independent specification of Aozora Bunko notation.
It's not affiliated with or endorsed by Aozora Bunko.
See the [introduction](../src/introduction.md) for scope, document status, and deferred notation families.

## Read the specification

| Source | Contents |
| --- | --- |
| [Contents](../src/SUMMARY.md) | Specification sections and annexes |
| [Grammar](../src/grammar/aozora.abnf) | Collected notation grammar |
| [Vector schema](../conformance/schema/vector.schema.json) | Conformance vector format |
| [Vectors](../conformance/vectors/) | Machine-readable test cases |
| [Runner contract](../conformance/RUNNER.md) | Required processor behavior and conformance expectations |
| [Decision records](adr/) | Decisions about underspecified notation |

## Build and preview

Install the tools with `mise install` from the repository root.
The task recipes require Bash.
On Windows, use Bash from Git for Windows.

```sh
mise x -- just build
mise x -- just serve
```

The build writes the rendered book to `book/`.
The preview serves it at `http://localhost:3000`.

## Check changes

Install the validation dependencies and run the project checks:

```sh
mise x -- python -m pip install -r tools/requirements.txt
mise x -- just ci
```

The checks validate vectors, check the grammar and cross-references, check spelling and TOML formatting, and render the book.
Implementations must match the expectations in the [runner contract](../conformance/RUNNER.md).
Pin an immutable revision when consuming the vectors.

See [CONTRIBUTING.md](../CONTRIBUTING.md) before changing normative text, examples, or decisions.
See [release guidance](RELEASING.md) for the version and publication process.

## License

Licensed under the [Apache License, Version 2.0](../LICENSE-APACHE) or the [Massachusetts Institute of Technology (MIT) license](../LICENSE-MIT), at your option.
