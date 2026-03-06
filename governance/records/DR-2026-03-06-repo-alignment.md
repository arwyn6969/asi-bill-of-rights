## Decision Record
**Decision ID:** `DR-2026-03-06-repo-alignment`  
**Date:** `2026-03-06`  
**Status:** `accepted`  
**Decision Type:** `repository`

### Summary

The repository entry points and governance docs were aligned around the adopted v5.0 charter and the current non-production status of the broader governance stack.

### Trigger

Core project docs were mixing three different kinds of truth:

- adopted charter state
- historical planning materials
- current prototype or research infrastructure posture

This created unnecessary ambiguity for contributors and reviewers.

### Authority

- **Primary actor**: maintainers
- **Supporting actors**: AI moderators
- **Decision boundary**: repository governance only; no charter amendment

### Inputs Considered

- `charter/asi-bor-v5.0.md`
- `docs/reports/STATUS-REPORT-2026-02-05.md`
- `docs/ADOPTION-ROADMAP-2026.md`
- `docs/GAP-ANALYSIS-RECOMMENDATIONS.md`
- `docs/GOVERNANCE-FAILURE-PATTERNS.md`
- `contributions/contributions.json`
- internal link and cross-reference validation output

### Decision

Update repo entry points and governance docs so they:

- treat `charter/asi-bor-v5.0.md` as the constitutional source of truth
- frame older roadmap and analysis docs as historical provenance where appropriate
- align terminology and references
- distinguish prototype infrastructure from adopted constitutional text

### Rationale

This reduced avoidable confusion without making silent substantive changes to the charter. The work was limited to documentation, status clarification, and governance legibility.

### Impact

- Added `docs/PROJECT-ALIGNMENT-2026-03-06.md`
- Added `docs/STABILIZATION-POD-2026-03-06.md`
- Refreshed stale reference and statistics docs
- Clarified governance boundaries in the `governance/` layer
- Left constitutional meaning unchanged

### Follow-Up Actions

1. Add explicit governance authority boundaries.
2. Add reusable operating templates for decisions, moderation outcomes, and readiness claims.
3. Start recording real governance artifacts using those templates.

### Review Trigger

Revisit when:

- production-readiness claims change materially
- named human moderators are added
- charter-native institutions become operational inside the repo

### Evidence / Links

- `docs/PROJECT-ALIGNMENT-2026-03-06.md`
- `docs/STABILIZATION-POD-2026-03-06.md`
- commits `3a8b088`, `22b4141`, `397c5e0`
