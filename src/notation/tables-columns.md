# 6.13 Tables and columns (表・段組)

## Synopsis

The official guide describes notation for **tables** (表) and **multi-column**
layout (段組) in print works. These are rare, presentation-heavy, and
provisional in the official guide; this specification treats them as
**Optional**.

## Notation

Tables and columns are described in the official 注記一覧
([§12 \[AOZORA-ANNOTATION\]](../references.md)) using `［＃…］` directives that
delimit regions and cells. The exact directive set is not yet pinned here.

## Semantics

Support for tables and columns is **OPTIONAL**. A processor MAY support them;
one that does not **MUST** retain the directives as generic annotations
(§6.14) so that no information is lost and the "no bare `［＃`" guarantee
holds. A processor that does support them SHOULD follow the official guide's
structure and document its mapping.

The exact directive set is provisional in the official guide and is not yet
pinned normatively here; a stable directive set and normative text may be
added in a later revision (§10.5).

## Conformance vectors

None in this revision (§10.5).
