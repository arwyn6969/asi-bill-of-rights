# Project Alignment

**Date:** March 6, 2026  
**Scope:** Whole-repo alignment for strategy, launch posture, and active delivery work

## Purpose

This document defines the current operating truth for the ASI Bill of Rights repository.

It exists because the repo now contains several distinct but related tracks:

- charter and schema development
- governance process and launch preparation
- Bitcoin-native SRC-420 governance infrastructure research
- KEVIN's Place prototype/product work
- outreach, publication, and adoption materials

Without one alignment layer, those tracks can drift and create contradictory signals about what is adopted, what is experimental, and what is actually ready to deploy.

## Canonical Sources Of Truth

Use these files in this order when deciding what is current:

1. `charter/asi-bor-v5.0.md`
   Current adopted charter text as of January 31, 2026.
2. `schemas/charter.v5.0.json`
   Machine-readable coverage layer for v5.0.
3. `docs/reports/STATUS-REPORT-2026-02-05.md`
   Operational status baseline for the repo and delivery posture.
4. `governance/MASTER-PLAN.md`
   Long-range strategy and infrastructure direction.
5. `governance/LAUNCH_CHECKLIST.md`
   Launch gating checklist for governance/community readiness.
6. `governance/SRC-420/SRC-420-SPECIFICATION.md`
   Protocol specification for Bitcoin-native governance.
7. `tools/src420-indexer/README.md`
   Actual implementation/runbook for the local SRC-420 indexer.
8. `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`
   Remaining hardening work before production claims.

## Stabilization Rules

Apply these rules when cleaning up or updating the repo:

- Historical planning and research documents should stay in the repo, but they must be labeled as historical once adoption or implementation has overtaken them.
- Machine-readable ledgers and schemas outrank stale narrative summaries when counts or status differ.
- High-confidence path, version, terminology, and status corrections can be made directly.
- Substantive charter or governance changes should be proposed separately from stabilization work.
- Do not invent named operators, human moderators, or concrete institutions that the repo does not already support.

## Current Aligned Position

As of March 6, 2026, the project should be described this way:

- The **core deliverable** is the adopted charter in `charter/asi-bor-v5.0.md`.
- The **current software posture** is mixed:
  - documentation and schema infrastructure are active and usable
  - the SRC-420 indexer is a hardened research/operator MVP
  - KEVIN's Place remains a prototype path, not the canonical governance system
- The **governance token direction** is Bitcoin-native and centered on `$KVNSI`
- The **deployment posture** for SRC-420 is still research and pre-deployment, not public production
- The **cloud strategy** points toward Google Cloud, but the repo still contains local-first and mixed-platform tooling

## What We Should Say Publicly

Use this phrasing consistently:

- "The ASI Bill of Rights charter v5.0 is adopted."
- "The Bitcoin-native governance stack is under active hardening and research."
- "SRC-420 tooling exists locally and has automated validation, but has not been declared production-ready."
- "KEVIN's Place is a prototype product surface, not the final governance source of truth."

Avoid saying:

- that SRC-420 is already deployed
- that governance is already live on-chain
- that KEVIN's Place is the canonical governance backend
- that Google Cloud migration is complete

## Active Workstreams

### 1. Charter and publication

Goal:
- keep v5.0 authoritative and easy to publish, compile, and explain

Primary files:
- `charter/asi-bor-v5.0.md`
- `docs/CHANGELOG.md`
- `docs/publication/README.md`
- `tools/publication/build_bible.py`

### 2. Governance launch readiness

Goal:
- make the repo, process, and moderation posture launchable without creating governance theatre

Primary files:
- `governance/LAUNCH_CHECKLIST.md`
- `governance/GOVERNANCE.md`
- `governance/decision-process.md`
- `contributors/ONBOARDING.md`

### 3. Bitcoin-native governance infrastructure

Goal:
- harden SRC-420 indexing, sync, rollback, and operator documentation until it is honest to call it deployable

Primary files:
- `governance/SRC-420/SRC-420-SPECIFICATION.md`
- `tools/src420-indexer/src420_indexer.py`
- `tools/src420-indexer/README.md`
- `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`

### 4. Product and community surface

Goal:
- decide whether KEVIN's Place is a demo, community hub, or governance client, then harden only to that scope

Primary files:
- `kevins-place/`
- `docs/strategy/MOTHERSHIP_IMPLEMENTATION_PLAN.md`
- `governance/MASTER-PLAN.md`

## Immediate Alignment Gaps

These are the highest-value cleanup items:

1. The root `README.md` needs to reflect the actual repo structure and current deployment posture.
2. The repo lacks a single maintainers' alignment note tying strategy, launch, and implementation together.
3. SRC-420 should be described everywhere as pre-deployment infrastructure until the production-readiness issue is materially closed.
4. KEVIN's Place needs a clearer repo-level label: prototype, demo, or product track.
5. The launch checklist, master plan, and status report should be treated as complementary, not competing, sources.

## Next 30 Days

Recommended priority order:

1. Publication artifact
   Deliver a repeatable "Bible" build and one public release-quality artifact.
2. Governance readiness
   Close the highest-risk checklist items in `governance/LAUNCH_CHECKLIST.md`.
3. SRC-420 production gate
   Resolve the top remaining items in `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`.
4. Product scope decision
   Decide what KEVIN's Place is expected to be in launch terms.

## After Stabilization

The next responsible step after this alignment pass is governance hardening:

- define institutional roles, authority boundaries, and evidence standards in one place
- specify review flows, quorum rules, and appeal paths without rewriting the charter's moral core
- keep that work separate from historical cleanup and repo-consistency edits

## Definition Of Aligned

The project is aligned when:

- repo entry points describe the same current version and posture
- roadmap, launch checklist, and status docs do not contradict each other
- implementation docs distinguish clearly between adopted, prototype, and research systems
- contributors can identify the current charter, current infrastructure status, and next priorities without guessing
