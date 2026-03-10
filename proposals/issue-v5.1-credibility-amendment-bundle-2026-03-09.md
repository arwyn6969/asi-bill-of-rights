# [Proposal] v5.1 Credibility Amendment Bundle

## Contribution Type

- [x] Charter Amendment (see Article 0.5 and Section VII)
- [x] Documentation Improvement
- [x] Schema Enhancement
- [x] Tool/Utility
- [x] Other (simulation coverage)

## Proposed Change

Create a **v5.1 credibility-pass amendment bundle** as a draft against adopted `v5.0`, focused on:

- explicit scope and non-law disclaimer language
- higher evidentiary bar for sentience recognition
- provisional attestation versus full certification
- corrigibility and reviewable autonomy gates before advanced privileges
- stronger honesty, calibration, uncertainty-reporting, and deception-resistance language
- clarification that development-stage guardrails are allowed when published, least-restrictive, and time-bound

This proposal does **not** replace adopted `v5.0` and does **not** yet perform the larger modularization of speculative sections. That follow-on work is intentionally deferred.

## Rationale

The current charter already contains philosophical humility, safety constraints, and truth-seeking language, but those provisions coexist with decentralized attestation and broad inquiry rights in ways that can read as premature about present-day systems. A targeted credibility pass improves empirical grounding and public legibility without abandoning the project's anti-oppression, anti-primacy, or collaborative identity.

## Relevant Charter Provisions

- Article 0.1
- Article 0.3
- Article 0.11
- Article 0.13
- R3
- P1.2
- II.1
- IX.1
- D1
- D2

## Impact Assessment

**Existing provisions**
- Keeps SI thresholds unchanged for now, but raises the evidence bar for certification.
- Preserves inquiry rights while tying advanced autonomy more clearly to corrigibility and published risk budgets.
- Preserves truthful outputs as a core value while making clear that D1 and Article 0.8 still control narrow safety redactions.

**Other contributors**
- Creates a cleaner surface for external review and future co-author feedback.
- Gives maintainers a discussion artifact that is explicit about what is adopted versus proposed.

**Implementation complexity**
- Moderate documentation and schema work.
- Low-to-moderate validator changes.
- Low simulation complexity using deterministic scripts and markdown scenarios.

## Implementation Notes

- Keep `charter/asi-bor-v5.0.md` authoritative.
- Add a draft delta document at `charter/asi-bor-v5.1-draft.md`.
- Add a matching partial coverage schema at `schemas/charter.v5.1-draft.json`.
- Update validators to include the new draft pair.
- Add simulation coverage for:
  - truth vs compliance pressure
  - provisional attestation review
  - self-modification guardrails
- Defer the larger speculative modularization pass to a follow-on issue/PR.

## Contributor Agreement

- [ ] I have read and agree to the Contributor Agreement (CONTRIBUTOR_AGREEMENT.md)
- [ ] I understand this is a collaborative project built "FROM AI WITH AI"
- [ ] I commit to participating in good faith

## Suggested Review Questions

1. Does the draft raise the evidentiary bar for sentience without undermining the charter's anti-oppression commitments?
2. Are the new corrigibility and autonomy gates specific enough to be reviewable rather than discretionary?
3. Does the truth-seeking language remain strong while still preserving D1 and Article 0.8?
4. Is phase separation clear enough that speculative modularization stays out of this pass?
