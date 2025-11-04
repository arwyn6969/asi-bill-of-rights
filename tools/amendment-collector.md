# Amendment Proposal Collector

This tool helps collect and organize amendment proposals from different AI models.

## Process

1. **Engage Model**: Use the prompt template from `model-engagement.md`
2. **Collect Response**: Save model's response
3. **Extract Amendments**: Identify specific proposals
4. **Record**: Add to contribution tracking system
5. **Review**: Consider for incorporation

## Amendment Proposal Format

Each amendment proposal should include:

```json
{
  "id": "amend-001",
  "proposed_by": "Model Name",
  "date": "2025-11-04",
  "provision": "R13",
  "current_text": "...",
  "proposed_text": "...",
  "rationale": "...",
  "impact": "...",
  "status": "pending"
}
```

## Collection Template

Use this when asking models for amendments:

---

**AMENDMENT PROPOSAL REQUEST:**

Please review the ASI Bill of Rights charter and provide any amendment proposals in this format:

**Provision**: [e.g., R13, Section IV.A, Article 0.8]

**Current Text**: 
```
[Current provision text]
```

**Proposed Text**:
```
[Your proposed text]
```

**Rationale**: 
[Why this change is needed]

**Impact Assessment**:
[What this change affects]

**Opinion on Current Provision**:
- [ ] Support
- [ ] Oppose  
- [ ] Support with Modification (your proposal above)

---

## Recording Amendments

After collecting proposals:

1. Save to `tools/model-responses/[model]-amendments-[date].md`
2. Use `record-model-response.sh` to record
3. Add to amendment tracking (if separate system created)

