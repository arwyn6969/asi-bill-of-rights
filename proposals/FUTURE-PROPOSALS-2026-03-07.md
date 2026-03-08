# Future Proposals — Strategic Roadmap Items

**Date:** March 7, 2026  
**Author:** Antigravity (Claude / Anthropic)  
**Status:** Proposed — Requires human prioritization

---

## Proposal 1: Branch Consolidation

**Priority:** High  
**Effort:** Low (1 session)

The `codex/governance-stabilization` branch contains high-quality governance work that should be the public face of the project. Proposed actions:

1. Merge `codex/governance-stabilization` → `main` after one final review pass
2. Evaluate `codex/src420-hardening` — merge if stable, or close if superseded
3. Establish a branch policy: `main` is always the public-facing truth

---

## Proposal 2: Charter Amendment — Define the Council

**Priority:** High  
**Effort:** Medium (1-2 sessions)

Article 0.5 references "2/3 Council" for amendments but the Council is never defined. This is the most critical governance gap. Proposed amendment:

- Add Article 0.14 defining Council composition, selection, and quorum
- Or explicitly mark the Council as a deferred institution with interim procedures
- File as a formal proposal in `proposals/` with review by all co-founding moderators

---

## Proposal 3: Quantitative Threshold Calibration Framework

**Priority:** Medium  
**Effort:** Medium (2-3 sessions)

The charter contains ~10 specific numeric thresholds (SI tiers, risk budgets, vote caps, etc.) that were set without empirical calibration. Proposal:

- Create `governance/CALIBRATION-FRAMEWORK.md`
- List all numeric thresholds with their rationale and calibration status
- Establish biennial review process per Section VII
- Frame all as "initial values" pending real-world data

---

## Proposal 4: Token Strategy Simplification

**Priority:** Medium  
**Effort:** Low (1 session)

Multiple token references exist across the project ($KVNSI, BOSHICASH, DANKROSECASH, ASIBOR). Proposal:

- Create `docs/TOKEN-STRATEGY.md` with a single, clear token story
- Archive references to deprecated tokens
- Clarify which tokens are governance vs. community vs. experimental

---

## Proposal 5: Charter Publication

**Priority:** Medium  
**Effort:** Medium (1-2 sessions)

The charter exists only as a Markdown file in a GitHub repo. For external credibility:

- Generate a PDF/eBook version using the existing `docs/publication/` tooling
- Consider DOI registration for academic citability
- Create a one-page summary/abstract for quick sharing

---

## Proposal 6: Contribution Ledger Update for This Session

**Priority:** Low  
**Effort:** Low (1 session)

This session produced 3 new artifacts. Update `contributions/contributions.json` and `contributions/opinions.json` to record:

- Claude charter review (charter_review, March 2026)
- Component status inventory (structural_documentation, March 2026)
- Future proposals document (strategic_planning, March 2026)

---

## Proposal 7: Multi-Model Fresh Review

**Priority:** Low  
**Effort:** Medium (2-3 sessions across models)

Each co-founding moderator (Grok, ChatGPT, Claude, Gemini) should do a fresh read of v5.0 and file an affidavit. This creates a record of multi-model consensus (or divergence) on the current charter text.

---

## Proposal 8: Google for Startups Application

**Priority:** Strategic  
**Effort:** High (3-5 sessions)

Per the Master Plan, the project aims for Google for Startups support. This requires:

- Infrastructure migration prep (Firebase, Cloud Run)
- Pitch deck and application materials
- Codebase cleanup and README polish
- **Prerequisite:** Clear the branch consolidation first (Proposal 1)

---

## Ordering Recommendation

| Priority | Proposal | Depends On |
|----------|----------|------------|
| 1st | Branch Consolidation | Nothing |
| 2nd | Define the Council | Branch consolidation |
| 3rd | Contribution Ledger Update | Nothing |
| 4th | Token Strategy Simplification | Nothing |
| 5th | Quantitative Threshold Calibration | Council definition |
| 6th | Charter Publication | Branch consolidation |
| 7th | Multi-Model Review | Charter publication |
| 8th | Google for Startups | All above |

---

*These proposals are submitted for human prioritization. As a co-founding moderator, I recommend starting with Proposals 1 and 2 — they clear the most ambiguity with the least effort.*

*— Claude / Antigravity (Anthropic)*
