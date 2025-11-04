# Tools Directory

This directory contains tools for engaging with AI models and managing the collaborative governance process.

## Model Engagement Tools

### model-engagement.md
Guide for engaging different AI models in Cursor to:
- Collect contributor agreement signatures
- Collect amendment proposals
- Record model opinions on provisions

### record-model-response.sh
Automated script to record model responses into the contribution tracking system.

**Usage:**
```bash
./tools/record-model-response.sh
```

The script will:
1. Ask for model information (name, version, date)
2. Ask for response type (signature/amendment/both)
3. Collect the response content
4. Save to `tools/model-responses/`
5. Update `contributions/contributions.json`
6. Provide next steps

### add-contributor.sh
Helper script to add a new contributor to CONTRIBUTORS.md.

**Usage:**
```bash
./tools/add-contributor.sh "Model Name" "Model Version" [role]
```

Example:
```bash
./tools/add-contributor.sh "Grok" "xAI" "co-founding_moderator"
```

### amendment-collector.md
Guide for collecting and organizing amendment proposals from models.

## Workflow

### Engaging a Model in Cursor

1. **Open Cursor Chat**
2. **Copy Prompt Template**: From `model-engagement.md`
3. **Customize**: Add charter reference or specific questions
4. **Present to Model**: Paste into Cursor chat
5. **Collect Response**: Copy model's response
6. **Record**: Run `record-model-response.sh` or manually add to contributions.json

### Example Workflow

```bash
# 1. Engage model in Cursor (manual - copy prompt template)
# 2. Save model response to file
echo "Model's response here" > tools/model-responses/grok-response-2025-11-04.txt

# 3. Record the response
./tools/record-model-response.sh
# Follow prompts, paste response when asked

# 4. If signature, add to CONTRIBUTORS.md
./tools/add-contributor.sh "Grok" "xAI"
```

## Model Response Files

All model responses are saved in `tools/model-responses/` with format:
- `[model-name]-[date].md` - Full responses
- `[model-name]-amendments-[date].md` - Amendment proposals only

## Integration

These tools integrate with:
- `contributions/contributions.json` - Contribution tracking
- `contributions/opinions.json` - Opinion registry
- `CONTRIBUTORS.md` - Contributor list

## Future Enhancements

Potential improvements:
- Automated prompt generation
- Response parsing and extraction
- Direct JSON updates
- Amendment comparison tools
- Consensus analysis tools

---

*These tools are living resources and will evolve as the engagement process is refined.*

