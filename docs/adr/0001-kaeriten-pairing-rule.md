# 0001. Kaeriten pairing is document-wide base presence

- Status: accepted
- Date: 2026
- Governs: §6.5 (Kunten), `bracketed-kaeriten-no-pair`

## Context

A bracketed return mark of rank ≥ 2 (`［＃二］`, `［＃下］`, `［＃乙］`) implies
the existence of a lower mark in its family. We want to flag the genuine
authoring error — a return mark with nothing to return to — without
false-flagging valid 漢文. The official guide shows the marks by example
(e.g. `自［＃二］女王國［＃一］`) but does **not** state a pairing rule, a
scope, or an ordering. Several plausible rules exist:

- *strict contiguous ladder* (a `三` requires both `二` and `一`, in order);
- *per-clause* or *per-line* completeness;
- *document-wide base presence* (a rank ≥ 2 mark requires only its family
  base `一` / `上` / `甲` to exist somewhere in the document).

## Decision

Use **document-wide base presence**: a bracketed mark of rank ≥ 2 raises
`bracketed-kaeriten-no-pair` only when its family base is absent from the
**entire document**. The check is base-only (not a contiguous ladder) and
order-independent.

## Consequences

- Near-zero false positives on real 漢文, which is what an error-severity
  diagnostic requires; the genuine "a `二` with no `一` anywhere" case is
  still caught.
- The check does not validate full ladder structure (a `三` with `一` but no
  `二` is not flagged). That is an accepted limitation: tighter checks
  mis-fire (below).

## Alternatives considered

- **Strict contiguous ladder / per-clause completeness.** Rejected on corpus
  evidence. In real 漢文 the marks are written in *reading* order, so `二`
  precedes `一` on the line (observed in ~99.8% of lines carrying both); a
  return-mark group routinely spans `、` / `。` and line boundaries; and 上下点
  legitimately uses just `上` … `下`, skipping `中`. A per-clause or
  contiguous-ladder rule flags a large fraction of valid kanbun.
- **No check.** Rejected: the genuine unpaired-mark error is worth catching,
  and document-wide base presence catches it with negligible false positives.

## References

- §6.5; diagnostic `bracketed-kaeriten-no-pair` (§9.5).
- Official 注記一覧, 訓点 (返り点). The corpus frequency above is the
  observation that motivated rejecting order-dependent rules.
