## Summary

<!-- One or two sentences: what this PR changes and why. -->

## Type of change

- [ ] New / changed normative text (notation family, processing model, diagnostic)
- [ ] New ADR (records a decision where the official guide is silent or ambiguous)
- [ ] Conformance vectors only
- [ ] Editorial / documentation (no normative change)
- [ ] CI / developer tooling

## Checklist

- [ ] `just ci` passes locally (validate · abnf-check · linkcheck · typos ·
      fmt-check · build).
- [ ] Normative claims cite **both** sources of truth — the official 注記一覧
      and the real Aozora Bunko corpus (with frequency where it matters).
- [ ] No fiction: nothing documented that is absent from *both* the official
      guide and the corpus.
- [ ] Every new normative example has a conformance vector under
      `conformance/vectors/`.
- [ ] RFC 2119 keywords (MUST / SHOULD / MAY) are used deliberately, not for
      emphasis.
- [ ] Where the guide is silent or ambiguous, the decision is recorded in
      `docs/adr/` and referenced from the section it governs.

## Related

<!-- Closes #N / part of #M / spec section(s) / ADR. -->
