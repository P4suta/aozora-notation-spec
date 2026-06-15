# 6.14 Input-editor annotations (入力者注)

## Synopsis

Volunteer transcribers add editorial notes — flagging a surprising spelling
as faithful to the source (`ママ`), recording a divergence from the base text,
and so on. These are the **input-editor annotations**. This family also
includes the **generic annotation**: the defined fate of any `［＃…］` whose
body matches no other construct.

## Notation

```text
怪体な［＃「怪体」に「ママ」の注記］          ← "as-is from the source"
峰﹅［＃「峰」は底本では「峯」］              ← textual divergence note
［＃なにかしらの注記］                       ← generic (unrecognised) annotation
```

```abnf
mama-note     = LBRACK HASH LQUOTE target RQUOTE %s"に「ママ」の注記" RBRACK
textual-note  = LBRACK HASH LQUOTE target RQUOTE %s"は底本では" LQUOTE alt RQUOTE RBRACK
annotation    = directive          ; any body not classified by §6.1–§6.13
```

## Parameters

- **target** — for `ママ` and textual-note forms, the quoted run the note
  concerns (resolved per §7.5).
- **alt** — for a textual note, the base-text form the run diverges from.

## Semantics

- A `ママ` note marks its target as intentionally reproduced from the source;
  a textual note records the base-text reading. Both yield an `annotation`
  node carrying the editorial kind and resolve their target by §7.5.
- **Generic annotation (the catch-all).** Any directive whose body is not
  classified by §6.1–§6.13 yields a generic `annotation` node that **retains
  the directive's literal bytes**. A processor **MUST NOT** drop it: this is
  the guarantee that **no bare `［＃` ever reaches output** — every `［＃…］`
  is claimed, recognized or not. A `ここから…` body that looks like a
  container opener but names none additionally raises
  [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  (§6.6).
- Reference rendering (§8) preserves the annotation (e.g. a hidden or
  side-channel span); serialization reconstructs the original `［＃…］`
  byte-exact (§7.6).

## Error conditions

- [`unrecognised-container-directive`](../diagnostics.md#unrecognised-container-directive)
  — a `ここから…` opener naming no known container.
- Forward-reference notes (`ママ`, textual) whose target is absent degrade per
  §7.5.

## Conformance vectors

`annotation`, `unrecognised-container-directive`.
