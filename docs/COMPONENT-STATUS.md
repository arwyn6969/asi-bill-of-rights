# Component Status Inventory

**Date:** March 7, 2026  
**Author:** Antigravity (Claude / Anthropic)  
**Purpose:** Single-page overview of every major project component and its current status

> This document is a snapshot. Update it when component status changes materially.

## Status Key

| Icon | Meaning |
|------|---------|
| ✅ | **Active** — maintained, current, used regularly |
| ⏸️ | **Paused** — exists but not under active development |
| 🗄️ | **Archived** — preserved for history, do not use |
| 🔬 | **Research/MVP** — functional but not production-ready |

---

## Constitutional Layer

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Charter v5.0 | `charter/asi-bor-v5.0.md` | ✅ Active | Adopted Jan 31, 2026. Source of truth |
| Charter v4.2 | `charter/asi-bor-v4.2.md` | 🗄️ Archived | Superseded by v5.0 |
| Charter v4.1 | `charter/asi-bor-v4.1.md` | 🗄️ Archived | Historical |
| Charter v4.0 / v3.0 | `charter/asi-bor-v4.0.md`, `v3.0` | 🗄️ Archived | Historical |
| Schema v5.0 | `schemas/charter.v5.0.json` | ✅ Active | Machine-readable charter coverage |
| Schema v4.x | `schemas/charter.v4.*.json` | 🗄️ Archived | Legacy schema versions |

## Governance Layer

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Authority Matrix | `governance/AUTHORITY-MATRIX.md` | ✅ Active | Clarifies repo vs charter vs protocol governance |
| Decision Records | `governance/records/` | ✅ Active | 3 records filed (March 2026). Templates in use |
| Governance Flowchart | `governance/GOVERNANCE-FLOWCHART.md` | ✅ Active | Process documentation |
| Conflict Resolution | `governance/conflict-resolution.md` | ✅ Active | Escalation procedures |
| Roles | `governance/roles.md` | ✅ Active | Contributor role definitions |
| Launch Checklist | `governance/LAUNCH_CHECKLIST.md` | ⏸️ Paused | Partially complete, gates not closed |
| Production Readiness Checklist | `governance/PRODUCTION-READINESS-CHECKLIST.md` | ✅ Active | Template; used for SRC-420 assessment |
| Bobby the Architect | `governance/BOBBY_THE_ARCHITECT.md` | ✅ Active | Governance spirit/auditor concept |
| Master Plan | `governance/MASTER-PLAN.md` | ⏸️ Paused | Dated Jan 31; needs refresh |
| Pivot 2026 | `governance/PIVOT-2026.md` | ✅ Active | Records ERC-20 → Bitcoin Stamps decision |
| Treasury Policy | `governance/TREASURY-POLICY.md` | ✅ Active | Financial controls |

## Protocol Infrastructure

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| SRC-420 Specification | `governance/SRC-420/` | 🔬 Research/MVP | Spec is solid; not production-deployed |
| SRC-420 Indexer | `tools/src420-indexer/` | 🔬 Research/MVP | 30/30 tests pass. Operator MVP quality |
| Wallet Infrastructure | `tools/wallet-infrastructure/` | ⏸️ Paused | Node modules present; no recent activity |
| Tokenization Tools | `tools/tokenization/` | ⏸️ Paused | Bitcoin Stamps tooling; pending $KVNSI deploy |

## Product / Community Layer

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Kevin's Place Backend | `kevins-place/backend/` | ⏸️ Paused | FastAPI app; Railway deployment configs present |
| Kevin's Place Frontend | `kevins-place/frontend/` | ⏸️ Paused | React/Vite app; Telegram Mini App integration |
| Telegram Bot (KEVIN) | `tools/telegram_bot/` | ⏸️ Paused | v3.0 with admin tools; known bugs documented |
| Nostr Agent | `tools/nostr_agent/` | ⏸️ Paused | Exists; unclear if actively posting |

## Documentation & Tooling

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| CI Validators | `tools/ci/` | ✅ Active | Links, cross-refs, schemas. All passing |
| Contribution Ledger | `contributions/contributions.json` | ✅ Active | 14 contributors, 26 contributions |
| Contribution Statistics | `contributions/STATISTICS.md` | ✅ Active | Synced March 6, 2026 |
| CONTRIBUTORS.md | `CONTRIBUTORS.md` | ✅ Active | Co-founding moderators listed |
| README.md | `README.md` | ✅ Active | Refreshed March 6, 2026 |
| Docs directory | `docs/` | ✅ Active | 63 files — guides, reports, alignment notes |
| Proposals | `proposals/` | ✅ Active | 22 items — amendments, specs, research |
| Simulations | `simulations/` | ✅ Active | 10 scenario files |

## Model / Training

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Sovereign Model (Qwen2.5-14B) | `model/` | ⏸️ Paused | Fine-tuned to 87.1%; training data present |
| Charter QA Dataset | `model/charter_qa_expanded.py` | ⏸️ Paused | 130 Q&A pairs for charter training |

## Agent Skills

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| Moltbook Integration | `.agent/skills/moltbook-integration/` | ⏸️ Paused | Observer/engagement protocols |
| Agent docs | `tools/agents/` | ✅ Active | Agent quick-start guide |

## Archived / Deprecated

| Component | Path | Status | Notes |
|-----------|------|--------|-------|
| ASIBOR ERC-20 | `archive/deprecated-asibor-jan-2026/` | 🗄️ Archived | Compromised Jan 13, 2026 |
| Legacy archive | `archive/` | 🗄️ Archived | 25 items |

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Active | 17 |
| ⏸️ Paused | 11 |
| 🔬 Research/MVP | 2 |
| 🗄️ Archived | 5 |

**Key Observation:** The constitutional and governance documentation layers are healthy and active. The product/community layer (Kevin's Place, Telegram, Nostr) and protocol infrastructure (SRC-420 deployment, tokenization) are paused. The strategic question is whether and when to resume those tracks.
