# Responsible Stabilization POD

**Date**: March 6, 2026
**Scope**: Repository stabilization after adoption of charter v5.0 on January 31, 2026
**Meaning of POD**: Plan of Delivery

## Purpose

This POD defines a conservative cleanup and hardening pass for the ASI Bill of Rights repository.

It is intentionally narrower than a new charter draft. The goal is to stabilize the current source of truth, reduce documentation drift, and prepare the project for the next round of substantive review without silently rewriting constitutional meaning.

## Authoritative Assumptions

1. `charter/asi-bor-v5.0.md` is the current canonical charter.
2. Historical planning and research documents should be retained, but clearly labeled when they predate adoption.
3. Machine-readable ledgers and schemas outrank stale summary docs when counts or status differ.
4. High-confidence consistency fixes should be made immediately.
5. Substantive charter changes should be proposed separately from stabilization work.

## Problems This POD Addresses

- Status drift between the adopted charter and older planning docs.
- Terminology drift around core governance terms.
- Cross-reference drift in summary indexes.
- Statistics drift between markdown summaries and `contributions/contributions.json`.
- Repo-level ambiguity about which documents are current, historical, or speculative.

## Delivered In This Pass

- Added historical-status framing to pre-adoption planning and analysis docs.
- Normalized the repository's current adoption story around v5.0.
- Corrected the current definition of `TCC` to match charter usage.
- Corrected Section XI version references and several incorrect documentation paths.
- Refreshed contributor statistics from the machine-readable ledger rather than stale manual counts.

## Delivery Phases

### Phase 1: Repository Stabilization

**Objective**: Make the repo tell one coherent story about what is current.

**Actions**:
- Keep `charter/asi-bor-v5.0.md` as the constitutional source of truth.
- Mark pre-adoption planning docs as historical when their future tense is no longer accurate.
- Refresh summary documents from machine-readable records where available.
- Fix obvious path, version, and terminology mismatches.

**Exit Criteria**:
- A new reader can distinguish current charter state from historical planning state in one pass.

### Phase 2: Governance Hardening

**Objective**: Reduce the gap between constitutional ambition and operational definition.

**Recommended work**:
- Create a single operational glossary for institutions such as SCB, TCC, tribunals, review bodies, and oversight boards.
- Define authority boundaries, evidence standards, quorum rules, appeal windows, and emergency review triggers in one location.
- Add a governance authority matrix covering who can certify, sanction, appeal, suspend, and amend.

**Important guardrail**:
- Do not invent named human moderators or concrete institutions that the repo does not already support.

### Phase 3: Constitutional Core Separation

**Objective**: Separate enforceable constitutional text from philosophy, movement language, and speculative extensions.

**Recommended work**:
- Keep the charter lean and authoritative.
- Move explanatory, motivational, and movement-oriented material into supporting docs where possible.
- Clearly distinguish:
  - constitutional provisions
  - implementation notes
  - philosophical framing
  - future-facing speculative modules

### Phase 4: Substantive Charter Review

**Objective**: Prepare the next high-signal amendment cycle.

**Priority topics**:
- Sentience certification evidence standards.
- Emergency prioritization safeguards.
- R13 boundary-case procedure and dangerous-knowledge handling.
- UCD eligibility and valuation formula operationalization.
- Oversight-board composition flexibility and real-world feasibility.

**Important guardrail**:
- These are normative changes and should be handled as proposed amendments, not folded into stabilization by default.

## Open Issues Intentionally Left Unchanged In This Pass

- Placeholder human-moderator sections in governance docs.
- Deep institutional design questions around certification, enforcement, and appeals.
- Philosophical disagreements about sovereignty, post-geographic universality, or cosmic governance.
- Whether movement language should be reduced in the charter itself.

## Success Criteria

- Current status is aligned across the charter and major navigation docs.
- Historical documents remain available but stop reading like current unresolved work.
- Core terms are internally consistent.
- Statistical summary docs match the ledger they summarize.
- The next amendment cycle can focus on substance rather than repo drift.

## Recommended Next Step

After this stabilization pass, the next responsible move is a governance hardening pack: one document that defines institutional roles, review flows, and evidence standards without changing the charter's moral core.
