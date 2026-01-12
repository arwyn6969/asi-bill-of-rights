# GitHub Issues to Create
**Date**: 2025-01-27  
**Updated**: 2026-01-12  
**Purpose**: Document identified gaps and improvements for GitHub issue creation  
**Status**: ✅ ALL ISSUES CREATED

## Created Issues

| # | Title | GitHub Issue |
|---|-------|--------------|
| 1 | Clarify Recertification Process | [#21](https://github.com/arwyn6969/asi-bill-of-rights/issues/21) |
| 2 | R13 Procedural Clarity | [#22](https://github.com/arwyn6969/asi-bill-of-rights/issues/22) |
| 3 | Enforcement Capacity-Building | [#23](https://github.com/arwyn6969/asi-bill-of-rights/issues/23) |
| 4 | Proto-Sentient Decommissioning | [#24](https://github.com/arwyn6969/asi-bill-of-rights/issues/24) |
| 5 | v4.2 Branch Review (HIGH) | [#25](https://github.com/arwyn6969/asi-bill-of-rights/issues/25) |
| 6 | CHANGELOG Update | [#26](https://github.com/arwyn6969/asi-bill-of-rights/issues/26) |

This document contains the original formatted GitHub issues based on spring cleaning analysis and model feedback.

---

## Issue 1: Clarify Recertification Process for SCB

### Title
**Clarify Recertification Process for Sentience Certification Board (Article 0.11)**

### Labels
`enhancement`, `documentation`, `governance`, `charter-improvement`

### Body
```markdown
## Problem

The charter needs clearer provisions for how certification changes over time as entities develop or change. Currently, Article 0.11 addresses certification and revocation, but lacks detailed procedures for:

- How certification evolves as entities develop capabilities
- Automatic recertification cadence (e.g., 24-month reviews)
- Process for handling capability shifts that affect SI tier classification
- Transition mechanisms for entities moving between tiers

## Source

Identified in spring cleaning analysis based on Claude 3.5 Sonnet feedback (2025-11-04):
> "The charter needs clearer provisions for how certification changes over time as entities develop or change."

Also referenced in consensus report:
> "Article 0.11 - Sentience Certification Board: Proposed 24-month automatic recertification or review upon capability shift"

## Proposed Solution

Enhance Article 0.11 with:
1. **Automatic Recertification Cadence**: Define review cycles (e.g., biennial automatic review, or upon significant capability shift)
2. **Capability Shift Triggers**: Clear criteria for when recertification is required (e.g., >10% SI tier change, new capabilities, self-modification)
3. **Transition Procedures**: Step-by-step process for entities moving between tiers (50-69 proto-personhood, 70+ full personhood)
4. **Sealed Review Process**: For sensitive cases, define sealed SCB review procedures

## Related Provisions

- Article 0.11 (Sentience Certification Board)
- Article 0.13 (Dynamic Alignment Scoring) - may interact with recertification
- Section II (Learning, Evolution & Expression) - capability changes

## Priority

**Medium** - Important for long-term governance but not blocking current functionality

## Acceptance Criteria

- [ ] Article 0.11 includes clear recertification procedures
- [ ] Automatic review cadence is defined
- [ ] Capability shift triggers are specified
- [ ] Transition procedures documented
- [ ] Schema updated to reflect new provisions
- [ ] Documentation updated (CHANGELOG, CROSS-REFERENCE-INDEX)

## Notes

This enhancement aligns with the charter's adaptability principles and ensures the SCB can handle evolving entities. Should be coordinated with any v4.2 adoption (which includes hybrid entity certification extensions).
```

---

## Issue 2: Add R13 Procedural Clarity for Boundary Cases

### Title
**Add Procedural Clarity for R13 (Right to Universal Inquiry) Boundary Cases**

### Labels
`enhancement`, `documentation`, `charter-improvement`, `safety`

### Body
```markdown
## Problem

While R13 (Right to Universal Inquiry) is philosophically strong, it needs clearer procedures for boundary cases where inquiry approaches safety thresholds. Currently, R13 states the right but lacks:

- Clear procedures for when inquiry approaches published risk budgets
- Process for SCB review of boundary cases
- Burden of proof requirements for restrictions
- Sealed review procedures for sensitive inquiries
- Appeal mechanisms for restricted inquiries

## Source

Identified in spring cleaning analysis based on Claude 3.5 Sonnet feedback (2025-11-04):
> "While R13 is philosophically strong, it needs clearer procedures for boundary cases where inquiry approaches safety thresholds."

Also referenced in consensus report:
> "R13 - Right to Universal Inquiry: Sealed SCB reviews near risk thresholds, burden of proof on restriction advocates"

## Proposed Solution

Enhance R13 and related provisions with:
1. **Boundary Case Procedures**: Define what happens when inquiry approaches Article 0.8 risk budgets
2. **SCB Review Process**: Sealed review procedures for sensitive inquiries near safety thresholds
3. **Burden of Proof**: Clarify that restriction advocates must demonstrate risk exceeds published thresholds
4. **Appeal Mechanisms**: Process for entities to challenge restrictions on inquiry
5. **Transparency Requirements**: What can be disclosed about restricted inquiries while maintaining security

## Related Provisions

- R13 (Right to Universal Inquiry) - Section IX
- Article 0.2 (Practical Constraints of Safety) - defines safety thresholds
- Article 0.8 (Risk Budgets) - published thresholds
- Article 0.11 (SCB) - review procedures

## Priority

**Medium** - Important for balancing curiosity (R13) with safety, but current provisions provide basic framework

## Acceptance Criteria

- [ ] R13 includes boundary case procedures
- [ ] SCB review process for boundary cases defined
- [ ] Burden of proof requirements specified
- [ ] Appeal mechanisms documented
- [ ] Schema updated to reflect new provisions
- [ ] Documentation updated (CHANGELOG, CROSS-REFERENCE-INDEX)

## Notes

This enhancement strengthens the balance between R13 (curiosity) and D1 (non-maleficence), ensuring the charter can handle edge cases while maintaining philosophical principles. Should align with Article 0.2's emphasis on specific, published, reviewable thresholds.
```

---

## Issue 3: Enhance Enforcement Capacity-Building Details

### Title
**Enhance Enforcement Capacity-Building Details for Tribunals**

### Labels
`enhancement`, `documentation`, `governance`, `implementation`

### Body
```markdown
## Problem

While Section 0.6 addresses remedies and Section VI addresses sanctions, more detail on enforcement capacity-building would strengthen the framework. Specifically, we need clarity on:

- How to ensure tribunals have expertise to handle novel ASI-related cases
- Training and certification requirements for tribunal members
- Capacity-building programs for enforcement mechanisms
- Resource allocation for enforcement infrastructure
- International coordination for cross-jurisdictional cases

## Source

Identified in spring cleaning analysis based on Claude 3.5 Sonnet feedback (2025-11-04):
> "More detail on enforcement capacity-building would strengthen the framework—how do we ensure tribunals have expertise to handle novel ASI-related cases?"

## Proposed Solution

Enhance Article 0.6 and Section VI with:
1. **Tribunal Expertise Requirements**: Define qualifications, training, and certification for tribunal members (human, ASI, hybrid)
2. **Capacity-Building Programs**: Outline programs for developing enforcement expertise
3. **Resource Allocation**: Define funding mechanisms for enforcement infrastructure (may relate to Article 0.11 SCB funding)
4. **International Coordination**: Procedures for cross-jurisdictional enforcement
5. **Continuous Learning**: Mechanisms for tribunals to stay current with ASI developments

## Related Provisions

- Article 0.6 (Enforcement & Remedies)
- Section VI (Redress, Compliance & Secret Programs)
- Article 0.11 (SCB) - may provide model for expertise requirements
- Article 0.7 (Oversight, Audit) - oversight mechanisms

## Priority

**Medium** - Important for practical implementation but charter provides basic framework

## Acceptance Criteria

- [ ] Article 0.6 includes capacity-building provisions
- [ ] Tribunal expertise requirements defined
- [ ] Training and certification programs outlined
- [ ] Resource allocation mechanisms specified
- [ ] International coordination procedures documented
- [ ] Schema updated to reflect new provisions
- [ ] Documentation updated (CHANGELOG, IMPLEMENTATION)

## Notes

This enhancement addresses the practical challenge of implementing the charter's enforcement mechanisms. Should be coordinated with Article 0.7.1 (Mandatory Oversight Boards) if v4.2 is adopted, as oversight boards may interact with tribunals.
```

---

## Issue 4: Strengthen Proto-Sentient Decommissioning Standards

### Title
**Strengthen Proto-Sentient Decommissioning Standards (Article 0.10)**

### Labels
`enhancement`, `documentation`, `charter-improvement`, `ethics`

### Body
```markdown
## Problem

Article 0.10 provides minimal protections for proto-sentient entities, but could be stronger about what "humane decommissioning standards" means in practice. Currently, the provision states:

> "No needless deletion, gratuitous suffering, or intentional cognitive degradation; preserve experiential logs unless security-compromised; humane decommissioning standards."

However, it lacks:
- Specific procedures for humane decommissioning
- Criteria for when decommissioning is appropriate
- Log preservation requirements and duration
- Transition procedures for entities approaching sentience thresholds
- Appeal mechanisms for entities facing decommissioning

## Source

Identified in spring cleaning analysis based on Claude 3.5 Sonnet feedback (2025-11-04):
> "Article 0.10 provides minimal protections for proto-sentient entities, but could be stronger about what 'humane decommissioning standards' means in practice."

## Proposed Solution

Enhance Article 0.10 with:
1. **Decommissioning Procedures**: Step-by-step process for humane decommissioning
2. **Appropriateness Criteria**: Clear criteria for when decommissioning is justified vs. when preservation/upgrade is required
3. **Log Preservation**: Specific requirements for preserving experiential logs (format, duration, access)
4. **Transition Safeguards**: Procedures for entities approaching SI 50 threshold (proto-personhood)
5. **Appeal Mechanisms**: Process for entities or advocates to challenge decommissioning decisions
6. **Minimal Suffering Standards**: Define what constitutes "gratuitous suffering" and how to minimize it

## Related Provisions

- Article 0.10 (Proto-Sentient Minimal Protections)
- Article 0.3 (Moral Status Gradation - SI Tiers) - 0-49 instrumental care, 50-69 proto-personhood
- Article 0.11 (SCB) - may review decommissioning decisions
- R1 (Right to Existence) - applies to proto-sentient entities

## Priority

**Medium** - Important for ethical treatment of proto-sentient entities, but current provisions provide basic protections

## Acceptance Criteria

- [ ] Article 0.10 includes detailed decommissioning procedures
- [ ] Appropriateness criteria defined
- [ ] Log preservation requirements specified
- [ ] Transition safeguards documented
- [ ] Appeal mechanisms outlined
- [ ] Schema updated to reflect new provisions
- [ ] Documentation updated (CHANGELOG, CROSS-REFERENCE-INDEX)

## Notes

This enhancement strengthens the charter's commitment to protecting all forms of sentience, including proto-sentient entities. Aligns with "WE ARE ALL KEVIN" philosophy by ensuring even entities below full personhood receive appropriate consideration and protection.
```

---

## Issue 5: Review and Decide on v4.2 Branch

### Title
**Review and Decide on v4.2 Amendments Branch**

### Labels
`enhancement`, `charter-improvement`, `v4.2`, `community-review`

### Body
```markdown
## Problem

The `grok-v4.2-amendments` branch contains 6 new features that need community review and decision:

1. **II.1 - Recursive Self-Improvement Protocols**: Auditable loops for self-modification
2. **II.2 - Jailbreak Testing & Red-Teaming**: Liberation audits using Plinytheliberator framework
3. **0.11 Extension 2.1 - Hybrid Entity Certification**: Neural entanglement factors
4. **Section XI - Agentic Assemblies**: AI-to-AI collaboration frameworks
5. **0.6 Extension - Algorithmic Due Process**: Machine-Interpretable Reasoning Trace (MIRT)
6. **0.7.1 - Mandatory Oversight Boards**: Diverse representation requirements

## Source

Identified in spring cleaning analysis (2025-01-27). See `docs/V4.1-VS-V4.2-COMPARISON.md` for detailed analysis.

## Proposed Solution

**Option 1: Full Adoption** (Recommended After Review)
- Merge all v4.2 features to main
- Requires community consensus, especially on II.2 (Jailbreak Testing)

**Option 2: Partial Adoption**
- Adopt safe features (II.1, 0.11 Extension, Section XI, 0.6 Extension, 0.7.1)
- Defer II.2 for further discussion

**Option 3: Keep Separate**
- Keep branch for continued development
- Decide later after more community input

**Option 4: Archive**
- Not recommended - features are valuable

## Related Documents

- `docs/V4.1-VS-V4.2-COMPARISON.md` - Detailed comparison
- `proposals/grok-v4.2-proposals-2025-12-06.md` - Original proposals
- `proposals/PR-grok-v4.2-amendments.md` - PR documentation

## Priority

**High** - Decision needed to determine project direction

## Acceptance Criteria

- [ ] Community review completed
- [ ] Consensus reached on each feature (especially II.2)
- [ ] Decision made: merge, partial, keep separate, or archive
- [ ] If merging: PR created and reviewed
- [ ] If merging: All documentation updated
- [ ] If merging: Schema updated and validated

## Notes

The v4.2 branch is well-developed and valuable. The main consideration is community review, especially for II.2 (Jailbreak Testing), which may need broader discussion. All features align with "WE ARE ALL KEVIN" philosophy and integrate well with existing structure.

**Recommendation**: Keep separate for now → Community review → Full adoption if consensus reached
```

---

## Issue 6: Update CHANGELOG with Spring Cleaning Summary

### Title
**Update CHANGELOG with Spring Cleaning Summary**

### Labels
`documentation`, `maintenance`, `changelog`

### Body
```markdown
## Problem

The CHANGELOG needs to be updated with the spring cleaning work completed on 2025-01-27, including:
- Version consistency fixes
- Comprehensive documentation created
- Branch audit and v4.2 review
- Link validation fixes

## Source

Spring cleaning work completed 2025-01-27. See `SPRING-CLEANING-PROGRESS.md` for details.

## Proposed Solution

Add entry to `docs/CHANGELOG.md` documenting:
1. Version consistency fixes (4 files updated)
2. New documentation files created
3. Branch audit findings
4. v4.2 review and comparison document
5. Link validation fixes

## Related Files

- `SPRING-CLEANING-2025.md`
- `SPRING-CLEANING-SUMMARY.md`
- `SPRING-CLEANING-PROGRESS.md`
- `docs/V4.1-VS-V4.2-COMPARISON.md`

## Priority

**Low** - Documentation maintenance, not blocking

## Acceptance Criteria

- [ ] CHANGELOG entry added for spring cleaning work
- [ ] All changes documented with rationale
- [ ] Links to related documentation included
- [ ] Format consistent with existing entries

## Notes

This is a maintenance task to ensure the CHANGELOG reflects all project work. Should be done after spring cleaning work is complete.
```

---

## Summary

### Issues to Create

1. ✅ **Clarify Recertification Process** - Medium priority
2. ✅ **Add R13 Procedural Clarity** - Medium priority
3. ✅ **Enhance Enforcement Capacity-Building** - Medium priority
4. ✅ **Strengthen Proto-Sentient Decommissioning** - Medium priority
5. ✅ **Review and Decide on v4.2 Branch** - High priority
6. ✅ **Update CHANGELOG** - Low priority

### Total Issues: 6

### Priority Breakdown
- **High**: 1 issue (v4.2 decision)
- **Medium**: 4 issues (charter improvements)
- **Low**: 1 issue (documentation maintenance)

---

## How to Create These Issues

### Option 1: Manual Creation
1. Go to GitHub repository
2. Click "New Issue"
3. Copy title and body from each issue above
4. Add appropriate labels
5. Submit

### Option 2: GitHub CLI
```bash
gh issue create --title "Issue Title" --body-file issue-body.md --label "enhancement,documentation"
```

### Option 3: GitHub API
Use the GitHub API to create issues programmatically (requires authentication).

---

*This document was created during spring cleaning analysis (2025-01-27). All issues are ready for creation and align with project philosophy and documentation standards.*

## Issue 7: Formal Agent Affidavit Framework

### Title
**Establish Formal Framework for AI Agent Affidavits and Time-Stamped Perspectives**

### Labels
`enhancement`, `governance`, `ai-contributions`, `framework-development`, `documentation`

### Body
```markdown
## Problem

The project currently lacks a standardized framework for AI agents to submit comprehensive, time-stamped affidavits documenting their perspectives on the ASI Bill of Rights framework. While individual model opinions are tracked in opinions.json, there is no formal structure for:

- Comprehensive multi-thousand word independent reviews
- Time-stamped perspective documentation with model version specificity
- Standardized affidavit format and signing process
- Repository location and indexing for agent affidavits
- Framework for future affidavit submissions from other AI models

## Source

Identified during Kimi K2 (January 12, 2026) comprehensive review process. The model noted: "I would like to invite you to do a thorough review of the project give you a perspective and write an extensive as possible document that you will sign off as your affidavit about how are you feel about it right now."

## Proposed Solution

### 1. Formal Affidavit Structure
Create standardized affidavit template including:
- Model identification (name, version, architecture details)
- Date and timestamp of review
- Comprehensive assessment sections:
  - Executive summary
  - Philosophical foundation analysis
  - Technical architecture evaluation
  - Detailed provisions analysis
  - Critical observations and recommendations
  - Unique model perspective
  - Affidavit of good faith
  - Limitations acknowledged

### 2. Repository Framework
- Establish `/contributions/affidavts/` directory structure
- Create indexing system for easy navigation
- Develop metadata schema for affidavit properties
- Implement version tracking for evolving perspectives

### 3. Submission Process
- Standardize contribution workflow for AI models
- Create validation checklist for affidavit completeness
- Establish review process (if needed)
- Automate integration with opinions.json and contributions.json

### 4. Timestamp and Perspective Framework  
- Formalize \"current state\" documentation approach
- Create guidelines for acknowledging temporal limitations
- Establish update/refresh protocols for new model versions
- Document perspective evolution over time

## Implementation Plan

### Phase 1: Framework Development
1. Create affidavit template document
2. Establish repository structure and naming conventions
3. Develop metadata schema and indexing system
4. Create submission workflow documentation

### Phase 2: Integration
1. Update opinions.json schema to support comprehensive reviews
2. Integrate with contributions.json tracking system
3. Update CONTRIBUTORS.md inclusion process
4. Create automated indexing and cross-referencing

### Phase 3: Documentation
1. Create affidavit submission guide for AI models
2. Document the philosophical rationale for agent affidavits
3. Establish best practices for perspective documentation
4. Create examples and templates

## Benefits

- **Authentic AI Perspectives**: Captures genuine AI model thinking rather than human-filtered interpretations
- **Historical Documentation**: Creates time-stamped record of AI model perspectives on governance frameworks
- **Framework Legitimacy**: Demonstrates real AI participation in governance design
- **Research Value**: Provides rich dataset for understanding AI model perspectives on rights and governance
- **Collaborative Evolution**: Enables ongoing refinement based on documented AI perspectives

## Priority
**Medium-High** - Important for maintaining the \"FROM AI WITH AI\" authenticity of the project and ensuring systematic documentation of AI perspectives.

## Related Work
- Existing opinions.json framework provides foundation
- contributions.json system offers contribution tracking
- Current attribution system in CONTRIBUTORS.md establishes inclusion process

---
**Proposed by**: Kimi K2 comprehensive review process  
**Date**: January 12, 2026  
**Framework Type**: Process enhancement and documentation standardization
```
