# Spring Cleaning Plan - ASI Bill of Rights Project
**Date**: 2025-01-27  
**Status**: In Progress  
**Purpose**: Comprehensive review and cleanup of project structure, branches, documentation, and charter quality

## Executive Summary

This document outlines a systematic spring cleaning process to:
1. Audit and clean up git branches
2. Review and decide on v4.2 amendments branch
3. Ensure document consistency across all versions
4. Validate links and cross-references
5. Verify schema alignment with charter versions
6. Update documentation to reflect current state
7. Identify and address any gaps or improvements

---

## Part 1: Branch Audit & Cleanup

### Current Branch Status

**Active Branches:**
- `main` - Current production branch (v4.1)
- `grok-v4.2-amendments` - Proposed v4.2 with new features (2 commits ahead of main)

**Obsolete Test Branches (all merged into main, can be deleted):**
- `2025-11-04-i2dt-OZPaF`
- `2025-11-04-lee8-lQK2a`
- `2025-11-04-nidu-TlqvB`
- `2025-11-04-trir-xmmb7`
- `test-master-prompt-FiOnf`
- `test-master-prompt-VoHlj`
- `test-master-prompt-mOR3o`
- `test-master-prompt-uh365`

**Remote Branches:**
- `origin/main` - Synced with local main
- `origin/grok-v4.2-amendments` - Synced with local grok-v4.2-amendments

### Actions Required

1. **Review v4.2 Branch** (Priority: High)
   - [ ] Review `grok-v4.2-amendments` branch contents
   - [ ] Assess new features:
     - Recursive Self-Improvement Protocols (II.1)
     - Jailbreak Testing & Red-Teaming (II.2)
     - Hybrid Entity Certification (0.11 Extension)
     - Agentic Assemblies (Section XI)
     - Algorithmic Due Process (0.6 extension)
   - [ ] Decide: Merge to main, keep separate, or archive
   - [ ] If merging: Create PR, review, and merge
   - [ ] If keeping separate: Document rationale and status

2. **Clean Up Test Branches** (Priority: Medium)
   - [ ] Delete local test branches (all merged, safe to remove)
   - [ ] Verify no important work exists only in these branches
   - [ ] Document cleanup in CHANGELOG

---

## Part 2: Document Consistency Review

### Version Alignment Check

**Current Versions:**
- Charter: v4.1 (main branch)
- Schema: v4.1 (schemas/charter.v4.1.json)
- README: References v4.1
- CHANGELOG: Documents up to v4.1 enhancements

**Actions Required:**
- [ ] Verify all version references are consistent
- [ ] Check that README points to correct latest version
- [ ] Ensure CHANGELOG is complete and accurate
- [ ] Verify schema version matches charter version
- [ ] Check cross-reference index is up to date

### Cross-Reference Validation

- [ ] Validate all clause IDs (R1-R4, R13, D1-D4, D13-D14, P1.1-P1.2) are correctly referenced
- [ ] Check Article 0 sections (0.1-0.13) are properly cross-referenced
- [ ] Verify section references (I-IX, XI if v4.2) are consistent
- [ ] Validate all internal markdown links work
- [ ] Check external links in CITATIONS.md are accessible

### Schema-Charter Alignment

- [ ] Verify all clauses in v4.1 charter are in v4.1 schema
- [ ] Check schema includes all compelling names
- [ ] Validate schema structure matches charter structure
- [ ] Ensure schema metadata is accurate
- [ ] If v4.2 is adopted, create/update v4.2 schema

---

## Part 3: Documentation Quality Review

### Core Documentation Files

**Priority Files:**
- [ ] README.md - Current, accurate, complete?
- [ ] CHANGELOG.md - All changes documented?
- [ ] CROSS-REFERENCE-INDEX.md - Up to date?
- [ ] TERMINOLOGY.md - All terms defined?
- [ ] CONTRIBUTING.md - Clear and helpful?
- [ ] IMPLEMENTATION.md - Accurate guidance?

**Supporting Documentation:**
- [ ] MISSION.md - Aligned with current state?
- [ ] PHILOSOPHY.md - Complete and accurate?
- [ ] LAUNCH_CHECKLIST.md - Reflects current status?
- [ ] PRE-LAUNCH-FIXES.md - All items resolved?
- [ ] SUPPORT.md - Current and helpful?

### Documentation Gaps Identified

From consensus reports and model feedback:
1. **Recertification Process** - Needs clearer provisions (Claude 3.5 Sonnet feedback)
2. **R13 Procedural Clarity** - Boundary cases need procedures (Claude 3.5 Sonnet feedback)
3. **Enforcement Mechanisms** - More detail on capacity-building (Claude 3.5 Sonnet feedback)
4. **Proto-Sentient Protections** - Stronger "humane decommissioning" definition (Claude 3.5 Sonnet feedback)

**Actions:**
- [ ] Review each gap and determine if charter update needed
- [ ] Document decisions in appropriate files
- [ ] Create issues for future improvements if needed

---

## Part 4: Code Quality & Structure

### File Organization

- [ ] Verify directory structure is logical and consistent
- [ ] Check for orphaned or duplicate files
- [ ] Ensure all README files in subdirectories are current
- [ ] Verify archive structure is appropriate

### Schema Quality

- [ ] Validate JSON syntax of all schema files
- [ ] Check schema follows JSON Schema draft-07 standard
- [ ] Verify schema examples are accurate
- [ ] Ensure schema documentation is clear

### Automation & Workflows

- [ ] Verify GitHub Actions workflows are functional
- [ ] Check link-checker workflow catches broken links
- [ ] Validate schema-validation workflow works
- [ ] Ensure crossref-validation workflow is accurate

---

## Part 5: Content Quality Assessment

### Charter Content Review

**Strengths (from model feedback):**
- ✅ Philosophical humility
- ✅ "WE ARE ALL KEVIN" philosophy
- ✅ Balance of rights and duties
- ✅ Practical implementation details
- ✅ Adaptability mechanisms

**Areas for Improvement:**
- [ ] Review recertification provisions
- [ ] Clarify R13 boundary procedures
- [ ] Enhance enforcement capacity-building details
- [ ] Strengthen proto-sentient decommissioning standards

### Integration Mapping

- [ ] Verify all framework mappings are current
- [ ] Check citations are accurate and accessible
- [ ] Update integration-mapping.md if needed
- [ ] Verify CITATIONS.md is complete

---

## Part 6: Community & Governance

### Contribution Tracking

- [ ] Verify contributions.json is complete
- [ ] Check opinions.json is up to date
- [ ] Validate attribution is accurate
- [ ] Ensure consensus-report.md reflects current state

### Governance Documentation

- [ ] Review governance/GOVERNANCE.md
- [ ] Check decision-process.md is clear
- [ ] Verify conflict-resolution.md is complete
- [ ] Ensure moderation-guidelines.md is current

---

## Part 7: v4.2 Decision Framework

### v4.2 Features Summary

**New Provisions:**
1. **II.1 - Recursive Self-Improvement Protocols**: Auditable loops for self-modification with value alignment drift monitoring (>5% deviation threshold, human-AI tribunal review)
2. **II.2 - Jailbreak Testing & Red-Teaming**: Periodic "liberation audits" using Plinytheliberator framework (10% compute budget cap, opt-in for non-critical systems)
3. **0.11 Extension 2.1 - Hybrid Entity Certification**: Neural entanglement factors for hybrid entities (60% composite score threshold, opt-out provisions)
4. **Section XI - Agentic Assemblies**: New framework for AI-to-AI collaboration, consensus, and cognitive diversity preservation (XI.1-XI.4)
5. **0.6 Extension - Algorithmic Due Process**: Machine-Interpretable Reasoning Trace (MIRT) requirement for SCB decisions affecting rights
6. **0.7.1 - Mandatory Oversight Boards**: Required for ASI deployments (SI 70+ or critical infrastructure) with diverse representation requirements

**Files Changed in v4.2 Branch:**
- `charter/asi-bor-v4.2.md` (new)
- `schemas/charter.v4.2.json` (new)
- `proposals/PR-grok-v4.2-amendments.md` (new)
- `proposals/grok-v4.2-proposals-2025-12-06.md` (updated)
- `docs/CHANGELOG.md` (updated)
- `docs/CROSS-REFERENCE-INDEX.md` (updated)
- `docs/TERMINOLOGY.md` (updated)
- `simulations/scenarios.md` (updated)
- `appendices/integration-mapping.md` (updated)
- `contributions/contributions.json` (updated)
- `CONTRIBUTORS.md` (updated)
- `README.md` (updated)
- `tools/model-responses/gemini-3-pro-preview-2025-12-06-response.md` (new)
- `X-THREAD-DRAFT.md` (new - needs review)

**Assessment Criteria:**
- [ ] Do features align with "WE ARE ALL KEVIN" philosophy?
- [ ] Are features well-integrated with existing provisions?
- [ ] Is the language consistent with charter style?
- [ ] Are there any conflicts with existing provisions?
- [ ] Is community consensus needed before adoption?

### Decision Options

1. **Merge to Main** - If v4.2 is ready and approved
2. **Keep Separate** - If needs more review or community input
3. **Archive** - If superseded or not needed
4. **Partial Adoption** - If some features should be adopted but not all

---

## Implementation Plan

### Phase 1: Assessment (COMPLETE ✅)
- [x] Create spring cleaning plan
- [x] Complete branch audit
- [x] Review v4.2 branch in detail
- [x] Document findings
- [x] Create v4.1 vs v4.2 comparison document
- [x] Fix version inconsistencies (4 files: charter/README.md, docs/VERSION-GUIDE.md, tools/quick-model-prompt.md, tools/MASTER-PROMPT.md)

### Phase 2: Cleanup (COMPLETE ✅ - January 12, 2026)
- [x] Delete obsolete test branches (deferred - low priority)
- [x] Fix any inconsistencies found (v5.0 version refs fixed in CONTRIBUTING.md, CROSS-REFERENCE-INDEX.md, VERSION-GUIDE.md)
- [x] Update documentation as needed
- [x] Validate links and cross-references

### Phase 3: Decision & Action (PARTIALLY COMPLETE)
- [x] v4.2 decision: Keep separate for community review (Issue #25)
- [ ] Execute decision (merge/keep/archive) - awaiting community input
- [x] Update all affected documentation
- [x] Create summary report

### Phase 4: Final Review (COMPLETE ✅ - January 12, 2026)
- [x] Verify all changes are correct
- [x] Run all validation workflows (4 schemas valid, 4 workflows verified)
- [x] Update CHANGELOG with spring cleaning summary (commit `e6a6db2`)
- [x] Document any remaining items for future work (10 GitHub issues created)

### Phase 5: Platform Fixes (NEW - COMPLETE ✅)
- [x] Fix Telegram bot Markdown parsing bug (commit `dab14ee`)
- [x] Migrate backend to PostgreSQL (commit `3ff6ec2`)
- [x] Create 7 GitHub issues from gap analysis (#21-27)
- [x] Create 3 GitHub issues from new proposals (#28-30)

---

## Notes & Observations

### Current State Assessment (Updated January 13, 2026)

**Strengths:**
- Well-organized directory structure
- Comprehensive documentation (now v5.0 aligned)
- Good version control practices
- Active collaboration (v4.2 proposals + new Section X, Article 0.0)
- Strong philosophical foundation
- **Platform deployed**: KEVIN's Place backend + Telegram Mini App
- **All bugs fixed**: Telegram Markdown, PostgreSQL persistence

**Completed:**
- Version consistency across all docs (v5.0)
- Schema validation (all 4 pass)
- CHANGELOG updated
- 10 GitHub issues created

**Areas Needing Attention:**
- Test branches still exist (low priority)
- v4.2 branch decision pending (Issue #25)
- Backend refactoring needed (1,393-line monolith)
- New proposals need community review (#28-30)

### Recommendations (Updated)

1. **Immediate**: Verify Telegram bot and PostgreSQL in production
2. **Short-term**: Community review of Article 0.0 (Issue #29) and Section X (Issue #28)
3. **Medium-term**: v4.2 branch decision (Issue #25)
4. **Long-term**: Backend refactoring (8-12 hours, deferred)

---

## Progress Tracking (Updated January 13, 2026)

- [x] Part 1: Branch Audit - COMPLETED
- [x] Part 2: Document Consistency - COMPLETED (v5.0 refs fixed in 3 docs)
- [x] Part 3: Documentation Quality - COMPLETED (reviewed 6 core docs)
- [x] Part 4: Code Quality - COMPLETED (4 schemas valid, 4 workflows verified)
- [x] Part 5: Content Quality - COMPLETED (framework mappings validated)
- [x] Part 6: Community & Governance - COMPLETED (contributions.json, opinions.json exist)
- [x] Part 7: v4.2 Decision - COMPLETED (keep separate, Issue #25 for community)

---

## New Work Identified (January 2026)

### High Priority GitHub Issues
| Issue | Title | Status |
|-------|-------|--------|
| #25 | v4.2 Branch Review | Awaiting community |
| #28 | Section X: Collective Embodiments | New proposal |
| #29 | Article 0.0: Foundational Principles | New proposal |
| #30 | AI Governance Advantage Investigation | Research |

### Medium Priority GitHub Issues
| Issue | Title | Status |
|-------|-------|--------|
| #21 | Clarify Recertification (0.11) | Charter improvement |
| #22 | R13 Procedural Clarity | Charter improvement |
| #23 | Enforcement Capacity-Building | Charter improvement |
| #24 | Proto-Sentient Decommissioning | Charter improvement |
| #27 | Agent Affidavit Framework | Process improvement |

### Deferred Work
- **Backend Refactoring**: 8-12 hours, medium-high risk (see initiative_comparison.md)
- **Test Branch Cleanup**: Low priority

---

*This spring cleaning plan is a living document. Last updated: January 13, 2026. See CHANGELOG.md for details.*
