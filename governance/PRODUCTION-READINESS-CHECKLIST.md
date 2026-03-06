# Production Readiness Evidence Checklist

Use this checklist before describing any infrastructure component as:

- production-ready
- launched
- live governance infrastructure
- canonical backend
- default public path

This checklist is evidence-oriented. It is meant to slow down optimistic claims until the repo can support them.

## Scope

**Artifact:**  
**Version / commit / build:**  
**Owner or steward:**  
**Claim being evaluated:**  
**Date:**  

## 1. Functional Definition

- [ ] The artifact's scope is described in one sentence.
- [ ] The intended users or operators are identified.
- [ ] The boundaries are explicit: prototype, operator MVP, beta, or production.
- [ ] The source-of-truth documentation is linked.

## 2. Build and Run Evidence

- [ ] Setup or deployment instructions exist and are current.
- [ ] Required environment variables, secrets, or services are documented.
- [ ] A clean-start runbook exists.
- [ ] A rollback or recovery path exists.
- [ ] Known platform assumptions are documented.

## 3. Validation Evidence

- [ ] Relevant tests or validators have been run recently.
- [ ] The exact commands or workflows are recorded.
- [ ] Results are attached or linked.
- [ ] Failure modes relevant to the artifact have been exercised.
- [ ] Known gaps are listed, not hidden.

## 4. Operational Readiness

- [ ] Monitoring or basic health checks exist.
- [ ] Logging or auditability is available to operators.
- [ ] There is a named support or triage path.
- [ ] Incident response expectations are documented.
- [ ] If keys, funds, or credentials are involved, handling expectations are documented.

## 5. Governance and Documentation Readiness

- [ ] Repo posture docs do not contradict the readiness claim.
- [ ] README and status docs use the same language.
- [ ] Launch or release checklists relevant to this artifact are satisfied or explicitly deferred.
- [ ] The artifact is clearly separated from charter-native institutions unless they are actually instantiated.
- [ ] Public claims avoid overstating production status.

## 6. Decision Record

- [ ] A decision record exists for the readiness claim.
- [ ] Reviewers are named.
- [ ] Open risks are listed.
- [ ] The claim is one of:
  - [ ] Approved
  - [ ] Deferred
  - [ ] Rejected

## 7. Evidence Links

- [ ] Status report
- [ ] Runbook
- [ ] Validation output
- [ ] Relevant issue tracker item(s)
- [ ] Decision record

## Recommendation

**Recommended posture:** `prototype | operator MVP | beta | production-ready`  
**Approved claim language:**  
**Open blockers:**  

## Review Sign-Off

- **Primary reviewer:**  
- **Supporting reviewer(s):**  
- **Decision date:**  

## Notes

If this checklist cannot be completed cleanly, the default posture should stay below production-ready.
