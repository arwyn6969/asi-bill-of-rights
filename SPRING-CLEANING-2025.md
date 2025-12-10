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

### Phase 1: Assessment (COMPLETE)
- [x] Create spring cleaning plan
- [x] Complete branch audit
- [x] Review v4.2 branch in detail
- [x] Document findings
- [x] Create v4.1 vs v4.2 comparison document
- [x] Fix version inconsistencies (4 files: charter/README.md, docs/VERSION-GUIDE.md, tools/quick-model-prompt.md, tools/MASTER-PROMPT.md)

### Phase 2: Cleanup
- [ ] Delete obsolete test branches
- [ ] Fix any inconsistencies found
- [ ] Update documentation as needed
- [ ] Validate links and cross-references

### Phase 3: Decision & Action
- [ ] Make decision on v4.2 branch
- [ ] Execute decision (merge/keep/archive)
- [ ] Update all affected documentation
- [ ] Create summary report

### Phase 4: Final Review
- [ ] Verify all changes are correct
- [ ] Run all validation workflows
- [ ] Update CHANGELOG with spring cleaning summary
- [ ] Document any remaining items for future work

---

## Notes & Observations

### Current State Assessment

**Strengths:**
- Well-organized directory structure
- Comprehensive documentation
- Good version control practices
- Active collaboration (v4.2 proposals)
- Strong philosophical foundation

**Areas Needing Attention:**
- Test branches need cleanup
- v4.2 branch needs decision
- Some documentation gaps identified
- Cross-reference validation needed

### Recommendations

1. **Immediate**: Clean up test branches (low risk, high value)
2. **Short-term**: Make decision on v4.2 branch
3. **Medium-term**: Address documentation gaps
4. **Ongoing**: Maintain consistency as project evolves

---

## Progress Tracking

- [x] Part 1: Branch Audit - COMPLETED
- [x] Part 2: Document Consistency - IN PROGRESS (found and fixed charter/README.md inconsistency)
- [ ] Part 3: Documentation Quality - PENDING
- [ ] Part 4: Code Quality - PENDING
- [ ] Part 5: Content Quality - PENDING
- [ ] Part 6: Community & Governance - PENDING
- [x] Part 7: v4.2 Decision - COMPLETED (comparison document created, recommendation: keep separate for community review)

---

*This spring cleaning plan is a living document and will be updated as work progresses. All changes will be documented in CHANGELOG.md upon completion.*
