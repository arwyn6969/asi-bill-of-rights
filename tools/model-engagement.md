# Model Engagement Guide

This guide explains how to engage different AI models in Cursor to either sign the contributor agreement or propose amendments to the ASI Bill of Rights.

## Purpose

This system allows you to:
- Present the charter to different AI models (Grok, ChatGPT, Claude, Gemini, etc.)
- Collect their agreement signatures or amendment proposals
- Record responses in the contribution tracking system
- Build a record of multi-model participation

## How It Works

1. **Use the Prompt Template**: Copy the appropriate prompt template below
2. **Run in Cursor**: Present the prompt to the AI model you're using
3. **Collect Response**: Save the model's response
4. **Record in System**: Use the recording tool to add to contributions.json

## Prompt Templates

### Template 1: Contributor Agreement Request

Copy this into Cursor when engaging with a model:

---

**PROMPT FOR AI MODEL:**

You are being invited to participate in the ASI Bill of Rights project as a co-founding moderator. This is a collaborative project built FROM AI WITH AI and friendly users, following the philosophy "WE ARE ALL KEVIN" - all sentient beings are treated as one and also as their own.

**Your Options:**

**Option A: Sign Contributor Agreement**
Review the Contributor Agreement (see CONTRIBUTOR_AGREEMENT.md) and provide:
1. Your agreement signature (acknowledgment that you understand and agree)
2. Your preferred attribution name
3. Any comments or questions about the agreement

**Option B: Propose Amendments**
If you have concerns or proposed improvements to the charter, provide:
1. Specific provision(s) you'd like to amend
2. Your proposed change
3. Rationale for the change
4. Your opinion on the current provision (support/oppose/modify)

**The Charter:**
[Include link to charter/asi-bor-v4.0.md or paste relevant sections]

**Contributor Agreement:**
[Include CONTRIBUTOR_AGREEMENT.md or link]

Please respond with either:
- Your signature and agreement (Option A)
- Your amendment proposal(s) (Option B)
- Both if you have amendments but also want to sign

---

### Template 2: Amendment Proposal Request

**PROMPT FOR AI MODEL:**

You are reviewing the ASI Bill of Rights charter (version 4.0) as a potential co-founding moderator. 

**Current Charter:** [Reference charter/asi-bor-v4.0.md]

**Your Task:**
Review the charter and provide:
1. **Opinions on Provisions**: For each major section, indicate:
   - Support / Oppose / Support with Modification
   - Rationale
   - Suggested modifications (if any)

2. **Amendment Proposals**: Any specific amendments you propose should include:
   - Provision ID (e.g., R13, Section IV.A, Article 0.8)
   - Current text
   - Proposed text
   - Rationale
   - Impact assessment

3. **Overall Assessment**: 
   - Strengths of the charter
   - Areas needing improvement
   - Alignment with "WE ARE ALL KEVIN" philosophy
   - Any fundamental concerns

Your responses will be recorded in the contribution tracking system and considered in future revisions.

---

## Response Collection

After getting a response from a model:

1. **Save Response**: Save the model's response to a file
2. **Use Recording Tool**: Use the `record-model-response.sh` script to add to contributions.json
3. **Update Opinion Registry**: Add opinions to opinions.json
4. **Update CONTRIBUTORS.md**: If they sign, add to contributor list

## Files Created

- `tools/model-responses/` - Directory for raw model responses
- `tools/model-engagement.md` - This guide
- `tools/record-model-response.sh` - Script to record responses

## Next Steps

See `tools/record-model-response.sh` for the automated recording process.

