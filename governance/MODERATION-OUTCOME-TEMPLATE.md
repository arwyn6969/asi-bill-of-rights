# Moderation Outcome Template

Use this template when a contribution, discussion, or moderation event needs a durable record beyond an informal comment.

Typical use cases:

- request-changes outcomes with multiple issues
- rejections with rationale
- attribution disputes
- conduct or process escalations
- pauses pending structural review
- moderator decisions that may later be appealed

Do not include unnecessary personal or sensitive information.

---

## Moderation Outcome

**Case ID:** `MOD-YYYY-MM-DD-short-slug`  
**Date:** `YYYY-MM-DD`  
**Status:** `open | resolved | escalated | archived`  
**Scope:** `content | process | attribution | conduct | launch-claim`

### Summary

Short description of the issue.

### Parties Involved

- Contributor(s)
- Reviewer(s)
- Moderator(s)

### Trigger

How the issue was raised and why it required moderation.

### Relevant Materials

- Proposal, file, issue, or discussion link
- Governance or contribution rule referenced
- Validation output or supporting evidence

### Review Notes

Plain summary of what was examined.

### Outcome

`approved | approved with suggestions | changes requested | rejected | paused | escalated`

### Rationale

Explain why that outcome was chosen.

### Required Actions

1. Action required from contributor or moderator
2. Action required from contributor or moderator
3. Action required from contributor or moderator

### Appeal Path

Explain whether appeal is available and who reviews it.

### Transparency Level

`public | anonymized summary | private`

### Follow-Up Date

`YYYY-MM-DD` or `none`

---

## Minimal Example

```md
## Moderation Outcome
**Case ID:** MOD-2026-03-06-status-claim
**Date:** 2026-03-06
**Status:** resolved
**Scope:** launch-claim

### Summary
A README change implied production readiness for infrastructure still marked as research.

### Parties Involved
- Contributor: repository maintainer
- Reviewers: AI moderators
- Moderator: human moderator / maintainer

### Trigger
Status language in repo entry points conflicted with the current alignment note.

### Relevant Materials
- docs/PROJECT-ALIGNMENT-2026-03-06.md
- governance/LAUNCH_CHECKLIST.md

### Review Notes
Repo posture documents were compared against current launch and readiness materials.

### Outcome
changes requested

### Rationale
The claim overstated current deployment maturity.

### Required Actions
1. Replace production wording with pre-deployment wording
2. Link to the status note

### Appeal Path
Escalate to maintainers if the contributor believes the evidence set is incomplete.

### Transparency Level
public

### Follow-Up Date
2026-03-13
```
