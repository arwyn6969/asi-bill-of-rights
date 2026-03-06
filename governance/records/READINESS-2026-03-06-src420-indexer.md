# Production Readiness Evidence Checklist

Use this checklist before describing any infrastructure component as:

- production-ready
- launched
- live governance infrastructure
- canonical backend
- default public path

This checklist is evidence-oriented. It is meant to slow down optimistic claims until the repo can support them.

## Scope

**Artifact:** `tools/src420-indexer/`  
**Version / commit / build:** `75ee7b2` plus current branch context as of 2026-03-06  
**Owner or steward:** repository maintainers / protocol tooling contributors  
**Claim being evaluated:** whether the SRC-420 indexer can be described as production-ready  
**Date:** `2026-03-06`

## 1. Functional Definition

- [x] The artifact's scope is described in one sentence.
- [x] The intended users or operators are identified.
- [x] The boundaries are explicit: prototype, operator MVP, beta, or production.
- [x] The source-of-truth documentation is linked.

Notes:
- Current posture is best described as **research/operator MVP**, not production-ready.
- Primary docs: `tools/src420-indexer/README.md` and `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`.

## 2. Build and Run Evidence

- [x] Setup or deployment instructions exist and are current.
- [ ] Required environment variables, secrets, or services are documented.
- [x] A clean-start runbook exists.
- [x] A rollback or recovery path exists.
- [x] Known platform assumptions are documented.

Notes:
- A local runbook exists, including sync and rollback commands.
- A production sync wrapper exists, but environment and upstream dependencies still need stronger operator documentation.

## 3. Validation Evidence

- [x] Relevant tests or validators have been run recently.
- [x] The exact commands or workflows are recorded.
- [x] Results are attached or linked.
- [x] Failure modes relevant to the artifact have been exercised.
- [x] Known gaps are listed, not hidden.

Notes:
- `tools/src420-indexer/README.md` documents `validate_mvp.py` and `tools/ci/validate_all.py`.
- The production-readiness issue explicitly lists deferred full-spec work and remaining hard problems.

## 4. Operational Readiness

- [ ] Monitoring or basic health checks exist.
- [x] Logging or auditability is available to operators.
- [ ] There is a named support or triage path.
- [ ] Incident response expectations are documented.
- [ ] If keys, funds, or credentials are involved, handling expectations are documented.

Notes:
- There is a query API and health endpoint, but the repo does not yet show full operational ownership or incident handling for a live service.

## 5. Governance and Documentation Readiness

- [x] Repo posture docs do not contradict the readiness claim.
- [x] README and status docs use the same language.
- [ ] Launch or release checklists relevant to this artifact are satisfied or explicitly deferred.
- [x] The artifact is clearly separated from charter-native institutions unless they are actually instantiated.
- [x] Public claims avoid overstating production status.

Notes:
- The documentation cleanup now treats the indexer as pre-deployment infrastructure.
- Launch gating still has open work; this blocks a production-ready posture.

## 6. Decision Record

- [x] A decision record exists for the readiness claim.
- [x] Reviewers are named.
- [x] Open risks are listed.
- [x] The claim is one of:
  - [ ] Approved
  - [x] Deferred
  - [ ] Rejected

Notes:
- This checklist itself, together with the associated repo alignment record and issue tracker item, forms the current evidence bundle.

## 7. Evidence Links

- [x] Status report
- [x] Runbook
- [x] Validation output
- [x] Relevant issue tracker item(s)
- [x] Decision record

Evidence:
- `docs/reports/STATUS-REPORT-2026-02-05.md`
- `tools/src420-indexer/README.md`
- `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`
- `governance/records/DR-2026-03-06-repo-alignment.md`

## Recommendation

**Recommended posture:** `operator MVP`  
**Approved claim language:** `The SRC-420 indexer is a hardened research/operator MVP under active hardening. It should not yet be described as production-ready governance infrastructure.`  
**Open blockers:** canonical quadratic semantics, broader strategy engine support, stronger operator and incident documentation, and completion of launch/readiness gating

## Review Sign-Off

- **Primary reviewer:** repository maintainer
- **Supporting reviewer(s):** AI moderators / documentation reviewers
- **Decision date:** `2026-03-06`

## Notes

If stronger production claims are needed later, they should be supported by a new decision record and a refreshed checklist rather than by informal README wording.
