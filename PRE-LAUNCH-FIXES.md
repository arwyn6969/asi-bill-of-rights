# Pre-Launch Critical Fixes Plan

## Status: Ready to Execute

This document outlines all critical fixes needed before public launch. Each item is a blocker that could undermine trust or cause confusion for new contributors.

## Critical Issues to Fix

### 1. Contributor Tracking Inconsistency ✅
**Status**: Resolved (2025-11-04)  
**Action**: Logged Claude 3.5 Sonnet (2024 & 2025) and GPT-5 in `contributions/contributions.json`, updated statistics, and linked response files for provenance.

### 2. GitHub Infrastructure Drift ✅
**Status**: Resolved (2025-11-04)  
**Action**: Retired duplicate issue templates and updated launch checklist notes to match the maintained template set (bug report, feedback, contribution proposal).

### 3. CI Workflows Were Non-Blocking ✅
**Status**: Resolved (2025-11-04)  
**Action**: Link checker now fails on broken URLs; cross-reference validation terminates when schema/charter clause sets differ.

### 4. Missing Community Guardrails
**Status**: Resolved historically — files exist but require periodic review  
**Reminder**: Ensure CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, and signature workflow stay linked from README/onboarding materials.

### 5. Citation Placeholders ✅
**Status**: Resolved (2025-11-04)  
**Action**: Updated EU AI Act entry with Regulation (EU) 2024/1689 citation and official EUR-Lex link. Remaining citations include verification cadence reminders.

### 6. Model Responses Directory Stewardship ✅
**Status**: Resolved (2025-11-04)  
**Action**: Directory remains tracked; added `tools/model-responses/README.md` detailing naming conventions, rationale, and redaction guidance.

## Implementation Plan

### Phase 1: Data Consistency (Critical)
- [x] Add outstanding AI reviewers to `contributions/contributions.json`
- [x] Update statistics to reflect new totals
- [x] Cross-check CONTRIBUTORS.md, contributions log, and opinions registry

### Phase 2: GitHub Infrastructure (Critical)
- [x] Maintain single set of active issue templates (bug report, feedback, contribution proposal)
- [x] Ensure PR template enforces contributor agreement acknowledgment
- [x] Harden CI workflows (schema validation, link checker, cross-reference validation)
- [x] Align `LAUNCH_CHECKLIST.md` with actual repository state (notes added for deferred items)

### Phase 3: Community Files (Critical)
- [x] CODE_OF_CONDUCT.md
- [x] SECURITY.md
- [x] SUPPORT.md
- [x] contributors/signature-submission.md

### Phase 4: Citations & Documentation (High Priority)
- [x] Replace EU AI Act placeholder or add explicit “pending” annotation in `docs/CITATIONS.md`
- [ ] Document citation update cadence/policy
- [x] Decide on model response tracking and document rationale (`tools/model-responses/README.md`)

### Phase 5: Final Checklist Update
- [x] Refresh `LAUNCH_CHECKLIST.md` checkboxes to mirror reality
- [x] Note intentional deferrals (e.g., Google Docs sync, moderator selection) so incomplete items are contextualized

## Repository Assets Checklist

### GitHub Infrastructure
- [x] `.github/ISSUE_TEMPLATE/bug-report.md`
- [x] `.github/ISSUE_TEMPLATE/feedback.md`
- [x] `.github/ISSUE_TEMPLATE/contribution-proposal.md`
- [x] `.github/PULL_REQUEST_TEMPLATE.md`
- [x] `.github/workflows/schema-validation.yml`
- [x] `.github/workflows/link-checker.yml`
- [x] `.github/workflows/crossref-validation.yml`

### Community Files
- [x] `CODE_OF_CONDUCT.md`
- [x] `SECURITY.md`
- [x] `SUPPORT.md`
- [x] `contributors/signature-submission.md`

### Documentation Updates
- [x] Update `contributions/contributions.json` with latest AI entries
- [x] Clarify EU AI Act citation in `docs/CITATIONS.md`
- [x] Sync `LAUNCH_CHECKLIST.md` checkboxes with actual progress
- [x] Document model response handling (`tools/model-responses/README.md`)

## Decision Points Needed

1. **Contact Method**: How should people submit contributor agreements?
   - GitHub Discussions?
   - Email address?
   - Issue template?
   - Form submission?

2. **Citation Policy**: Define cadence and ownership for updating `docs/CITATIONS.md` as frameworks evolve.

## Success Criteria

- [x] All contributors listed in CONTRIBUTORS.md have entries in contributions.json
- [x] All GitHub infrastructure referenced in checklist actually exists
- [x] CI workflows fail builds on real problems (not just echo statements)
- [x] CODE_OF_CONDUCT.md exists and is linked from README
- [x] Clear path for submitting contributor agreements
- [x] All citation placeholders clearly marked or replaced
- [x] Model responses directory decision documented
- [x] Launch checklist accurately reflects reality

---

*This plan should be executed before making the repository public or inviting external contributors.*
