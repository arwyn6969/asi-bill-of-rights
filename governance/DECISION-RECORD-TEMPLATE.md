# Decision Record Template

Use this template for significant repository or governance decisions that should remain easy to audit later.

Typical use cases:

- repo posture changes
- launch or publication decisions
- contribution decisions with strategic impact
- governance process changes
- production-readiness decisions
- charter coordination decisions that affect multiple files

For trivial typo fixes or obvious reference corrections, normal git history is usually sufficient.

---

## Decision Record

**Decision ID:** `DR-YYYY-MM-DD-short-slug`  
**Date:** `YYYY-MM-DD`  
**Status:** `proposed | accepted | rejected | superseded`  
**Decision Type:** `repository | governance | moderation | launch | infrastructure | charter-coordination`

### Summary

One or two sentences describing the decision.

### Trigger

What caused this decision to be needed.

### Authority

- **Primary actor**
- **Supporting actors**
- **Decision boundary**: explain whether this was a repo-level decision, a moderation decision, or a charter-coordination decision

### Inputs Considered

- Documents reviewed
- Issues, reports, or proposals considered
- Validation or testing evidence

### Decision

State the final decision plainly.

### Rationale

Explain why this decision was made instead of the main alternatives.

### Impact

- Files, workflows, or public claims affected
- What changes immediately
- What remains unchanged

### Follow-Up Actions

1. Action item
2. Action item
3. Action item

### Review Trigger

Describe what would cause this decision to be revisited.

### Evidence / Links

- Link or path
- Link or path
- Link or path

---

## Minimal Example

```md
## Decision Record
**Decision ID:** DR-2026-03-06-repo-alignment
**Date:** 2026-03-06
**Status:** accepted
**Decision Type:** repository

### Summary
Clarified the adopted charter and current infrastructure posture across repo entry points.

### Trigger
README and supporting docs were mixing adopted charter state with research/prototype infrastructure claims.

### Authority
- Primary actor: maintainers
- Supporting actors: AI moderators
- Decision boundary: repository governance only; no charter amendment

### Inputs Considered
- docs/PROJECT-ALIGNMENT-2026-03-06.md
- governance/LAUNCH_CHECKLIST.md
- docs/reports/STATUS-REPORT-2026-02-05.md

### Decision
Update repo entry points to distinguish adopted charter text from prototype infrastructure.

### Rationale
This reduced public-facing ambiguity without changing charter substance.

### Impact
- README and governance entry points updated
- No constitutional text changed

### Follow-Up Actions
1. Add authority matrix
2. Add operating templates

### Review Trigger
Revisit when SRC-420 is materially closer to production deployment.
```
