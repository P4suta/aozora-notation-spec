# 6.12 Bold and italic (太字・斜体)

## Synopsis

Bold (太字) and italic (斜体) mark emphasis as a weight/slant rather than the
dots/lines of bouten (§6.2). Unlike bouten, they use the `ここから`/`ここで`
**block** opener/closer form.

## Notation

```text
［＃ここから太字］強調する段落。［＃ここで太字終わり］
［＃ここから斜体］…［＃ここで斜体終わり］
```

```abnf
bold-open   = LBRACK HASH %s"ここから太字" RBRACK
bold-close  = LBRACK HASH %s"ここで太字終わり" RBRACK
italic-open = LBRACK HASH %s"ここから斜体" RBRACK
italic-close= LBRACK HASH %s"ここで斜体終わり" RBRACK
```

An inline forward-reference form (`［＃「X」は太字］`) also occurs.

## Parameters

None beyond the target (for the forward-reference form).

## Semantics

太字 / 斜体 pair as a block container (§7.1) by family `bold` / `italic`,
the reference rendering being `<strong>` / `<em>` (or styled `<span>`s); the
inline forward-reference form resolves its target per §7.5.

This revision documents the notation but does not yet pin its full normative
semantics or conformance vectors; they are deferred to a later revision
(§10.5). A processor that does not implement 太字 / 斜体 retains the opener as
a generic annotation (§6.14), so no input is lost.

## Conformance vectors

None in this revision (§10.5).
