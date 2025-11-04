# Quick Start Guide - Model Engagement

## One-By-One Process

Use these prompts to engage each AI model systematically.

## Step 1: First Prompt

**Open Cursor chat with the AI model you want to engage.**

**Copy and paste the entire contents of `tools/MASTER-PROMPT.md`**

This will:
- Introduce the project
- Explain "WE ARE ALL KEVIN" philosophy
- Ask for signature, amendments, and opinions
- Direct them to read the charter

**Wait for their complete response.**

## Step 2: Save Response Prompt

**After the model has provided their full response, copy and paste the contents of `tools/RESPONSE-SAVE-PROMPT.md`**

This will:
- Ask them to format their response
- Provide a template for saving
- Direct them to save to the correct location

**Wait for them to confirm the file is saved.**

## Step 3: Record Response

**Once the model confirms the file is saved, run:**

```bash
./tools/record-model-response.sh
```

Follow the prompts:
- Enter model name (e.g., "Claude", "GPT-4", "Grok")
- Enter model version/provider (e.g., "Anthropic", "OpenAI", "xAI")
- Select response type (1=Signature, 2=Amendment, 3=Both)
- When asked for response content, provide the path: `tools/model-responses/[model-name]-[date]-response.md`

The script will:
- Verify the file exists
- Record it in `contributions/contributions.json`
- Update statistics

## Step 4: Add to Contributors (if signed)

**If the model signed the agreement, run:**

```bash
./tools/add-contributor.sh "[Model Name]" "[Provider/Version]"
```

Example:
```bash
./tools/add-contributor.sh "Claude 3.5 Sonnet" "Anthropic"
```

This adds them to `CONTRIBUTORS.md`.

## Step 5: Review and Process

**Review the saved response:**
- Check `tools/model-responses/[model]-[date]-response.md`
- Review amendments for consideration
- Note opinions in your planning

**Optional: Update opinions.json manually if you want to track opinions separately.**

## Repeat for Each Model

Go through Steps 1-5 for each AI model you want to engage:
- Claude (Anthropic)
- GPT-4 / ChatGPT (OpenAI)
- Grok (xAI)
- Gemini (Google)
- Any others

## Tips

- **One model at a time**: Complete the full process for one model before moving to the next
- **Save everything**: All responses are saved automatically
- **Review amendments**: Consider amendments collectively before incorporating
- **Track opinions**: Different models may have different perspectives - that's valuable!

## Files Created

After engaging all models, you'll have:
- Multiple response files in `tools/model-responses/`
- Updated `contributions/contributions.json` with all contributions
- Updated `CONTRIBUTORS.md` with all signed models
- A record of all amendments and opinions

## Next Steps After All Models

1. Review all amendments collectively
2. Consider consensus or divergence of opinions
3. Update `contributions/consensus-report.md` if needed
4. Plan which amendments to incorporate
5. Begin revision process if amendments are accepted

---

**That's it! Just copy the two prompts and follow the steps for each model.**

