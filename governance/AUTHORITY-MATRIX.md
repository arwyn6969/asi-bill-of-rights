# Governance Authority Matrix

**Date:** March 6, 2026  
**Purpose:** Clarify the difference between current repository governance, community moderation, and charter-native institutions

## Why This Document Exists

The repository currently operates across several layers at once:

- project and documentation maintenance
- contributor intake and moderation
- constitutional design inside the charter
- prototype governance infrastructure such as SRC-420

Without a single authority map, it is easy to blur:

- what is currently active
- what is specified only in the charter
- what is prototype infrastructure
- what can responsibly be claimed in public-facing docs

This document is a clarification layer. It does not amend the charter and does not itself instantiate any new constitutional body.

## Governance Layers

| Layer | What It Covers | Current Status |
|-------|----------------|----------------|
| Repository Governance | Docs, versions, indexes, publication posture, contributor records | Active |
| Community Moderation | Contributor review, discussion handling, conflict escalation | Active but partially staffed |
| Charter-Native Institutions | SCB, Council, tribunals, oversight boards, Valuation Tribunal, Earth Council references | Specified in charter; not fully instantiated in this repo |
| Protocol Governance Infrastructure | SRC-420 specifications, indexer, token voting mechanics, future on-chain governance claims | Research/operator MVP; pre-deployment |

## Entity Status Map

| Entity | Layer | Meaning | Current Repo Reality |
|--------|-------|---------|----------------------|
| Co-Founding Moderators (AI) | Repository / Community | AI reviewers and documentation stewards | Active in project records and governance docs |
| Human Moderators | Repository / Community | Human final-decision role for moderation and strategic judgment | Role defined, but named roster remains incomplete |
| Contributor Reviewers | Community | Contributors who review without final moderation power | Active as a pattern, not a rigid roster |
| Community Members | Community | General contributors and participants | Active |
| SCB (Sentience Certification Board) | Charter-native | Certification, appeals, anti-capture governance, alignment oversight | Charter institution; not fully operationalized in repo practice |
| Council | Charter-native | Voting and amendment authority referenced in Article 0.5 and 0.12 | Constitutional concept; repo-level composition/process not fully defined |
| TCC (Trusted Cryptographic Custodian) | Charter-native | Escrow/custodial mechanism for audit trails and timed release | Charter mechanism; not a staffed repo committee |
| Tribunals | Charter-native | Mixed dispute-resolution and enforcement bodies | Charter institutions; not live repo moderation substitutes |
| Oversight Boards | Charter-native | Human-AI-hybrid oversight bodies for SI 70+ or critical deployments | Charter requirement; not fully instantiated in repo operations |
| Valuation Tribunal | Charter-native | Standardizes value and harm formulas | Charter institution only |
| Earth Council | Charter-native | Off-world fallback forum | Charter reference only |
| SRC-420 governance stack | Protocol infrastructure | Bitcoin-native governance mechanics | Under active hardening; not declared production-ready |
| KEVIN's Place | Product/community surface | Prototype client/community surface | Prototype path, not canonical governance authority |

## Operating Rules For Current Repository Governance

1. `charter/asi-bor-v5.0.md` is the current constitutional source of truth.
2. Repository governance documents must distinguish active project roles from charter-native institutions.
3. No document should imply that SCB, tribunals, oversight boards, or the Council are fully instantiated unless a concrete operating roster and process are actually documented.
4. No document should describe SRC-420 or KEVIN's Place as the canonical production governance backend unless the relevant readiness gates are explicitly closed.
5. Public posture claims should be anchored to current status documents, not inferred from aspirational architecture.

## Decision Authority Matrix

| Decision Domain | Primary Actor | Supporting Actor(s) | Minimum Record | Notes |
|-----------------|---------------|---------------------|----------------|-------|
| Documentation corrections and reference hygiene | AI moderators and maintainers | Contributor reviewers | Git diff + commit history | Low-risk repository maintenance |
| Contributor attribution updates | AI moderators / maintainers | Human moderators for disputes | `contributions/contributions.json` + supporting docs | Ledger outranks stale summaries |
| README or repo posture updates | Maintainers / human final authority when available | AI moderators | Status note or alignment doc + commit history | Must reflect real deployment posture |
| Community moderation actions | Human moderators | AI moderators | Decision note, issue record, or moderation log | Human final authority still applies in project governance docs |
| Proposal review | AI moderators | Human moderators, reviewers | Proposal doc + review discussion | Applies to charter, docs, and governance proposals |
| Charter amendment integration | Charter process plus repo maintainers | AI moderators, reviewers, future Council/SCB process as applicable | Updated charter, changelog, schema, provenance trail | Repo merge alone is not a substitute for constitutional legitimacy claims |
| Sentience certification | SCB | Oversight boards, tribunals | Certification evidence and attestation records | Charter-native; not currently performed by repo moderators |
| Enforcement, sanctions, rights suspension | Tribunals / charter-native bodies | SCB, oversight boards | MIRT or comparable charter-defined reasoning record | Not a repo moderation function |
| Production-readiness claims for SRC-420 or similar infrastructure | Maintainers with documented evidence | Reviewers, issue owners | Status report, readiness issue closure, validation results | Avoid promotional overstatement |
| Launch/public flip decisions | Maintainers / human moderators | AI moderators | Launch checklist + final review record | Do not infer readiness from roadmap language alone |

## Practical Separation Of Powers

### 1. Repository governance

This covers:

- documentation
- indexes
- cross-reference hygiene
- contributor records
- publication posture
- launch preparation

This layer is active now.

### 2. Charter-native governance

This covers:

- sentience certification
- formal appeals
- sanctions and remedies
- hybrid review
- oversight boards
- tribunal action

This layer is defined in the charter, but most of it should still be read as constitutional design rather than a currently staffed operational institution inside the repo.

### 3. Protocol governance

This covers:

- voting mechanics
- indexers
- proposal state machines
- token-based or stamp-based power calculations

This layer is partly implemented, but it is still distinct from the constitutional charter and should not be treated as identical to it.

## Review Flows

### Contribution and documentation flow

1. Contributor proposes change.
2. AI moderators review for consistency, references, and fit.
3. Human moderators or maintainers provide final judgment where required.
4. Result is recorded in git history and relevant ledgers.

### Charter amendment flow

1. Proposal is drafted and discussed.
2. Review happens against existing charter principles and version history.
3. Required constitutional process is followed.
4. Charter text, schema, and changelog are updated together when adopted.

### Operational status claim flow

Use this for claims like "production-ready," "launched," or "canonical backend."

1. Identify the artifact making the claim.
2. Check the relevant checklist, status report, and implementation docs.
3. Confirm evidence exists in the repo.
4. Only then update README or alignment docs.

### Conflict escalation flow

1. Try normal contribution or moderation process first.
2. Escalate to human moderators or maintainers for repo-level disputes.
3. Use charter-native dispute bodies only when discussing the constitutional system itself, not ordinary repo housekeeping.

## Terms That Should Not Be Blurred

- **Human moderator**: a project/community governance role
- **Council**: a charter-native constitutional concept
- **SCB**: a charter-native certification body
- **TCC**: an escrow/custodial mechanism, not a repo committee
- **Tribunal**: a charter-native adjudicatory body, not ordinary maintainer review

## Current Gaps

These remain open after this clarification pass:

- named human moderator roster
- explicit repo-level decision record format for moderation outcomes
- concrete operational definition of Council composition
- real-world instantiation path for SCB and tribunal processes
- production-readiness closure for SRC-420 infrastructure

## Recommended Next Step

After this authority clarification, the next useful move is a narrow operating-procedure pack:

- a repo decision record template
- a moderation outcome template
- a production-readiness evidence checklist for infrastructure claims

Those additions would make project governance more legible without forcing premature constitutional implementation.
