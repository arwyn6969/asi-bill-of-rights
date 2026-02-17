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

## Validation Helpers

- `tools/ci/validate_schemas.py`: Mirrors the schema-validation GitHub Action locally. Install `jsonschema` once (`pip install jsonschema`) and run `python3 tools/ci/validate_schemas.py` to validate all schema files plus `contributions/contributions.json`.
- `tools/ci/validate_crossrefs.py`: Cross-checks clause IDs across charter markdown + schemas (v4.1 + v4.2 exact match; v5.0 schema coverage subset). Run `python3 tools/ci/validate_crossrefs.py` before committing structural edits.
- `tools/ci/validate_internal_links.py`: Validates that internal markdown links in tracked `.md` files resolve to real files (mirrors the CI link-checker internal reference step).
- `tools/src420-indexer/validate_mvp.py`: SRC-420 indexer regression suite (deterministic ingest/reducer + sync/rollback/reorg guardrails).
- `tools/ci/validate_all.py`: Convenience runner for the checks above plus SRC-420 indexer validation (when `tools/src420-indexer/validate_mvp.py` exists). Schema checks still run only if `jsonschema` is installed.

## Future Enhancements

Potential improvements:
- Automated prompt generation
- Response parsing and extraction
- Direct JSON updates
- Amendment comparison tools
- Consensus analysis tools

## SRC-420 Indexer MVP

Deterministic local indexer for SRC-420 governance events.

**Location**: `tools/src420-indexer/src420_indexer.py`  
**Runbook**: `tools/src420-indexer/README.md`

Quick commands:

```bash
python3 tools/src420-indexer/src420_indexer.py init-db --db tools/src420-indexer/src420.db
python3 tools/src420-indexer/src420_indexer.py import-balances --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_balances.jsonl
python3 tools/src420-indexer/src420_indexer.py ingest-file --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_events.jsonl --enforce-balance-checks
python3 tools/src420-indexer/src420_indexer.py sync-http --db tools/src420-indexer/src420.db --records-key results --has-more-key has_more --max-pages 3 --tip-height 900000 --min-confirmations 6 --reorg-check --reorg-auto-rollback --reorg-hash-url-template 'https://stampchain.io/api/v2/block/{block}' --reorg-hash-path block_hash --update-cursor
python3 tools/src420-indexer/src420_indexer.py rollback-to-block --db tools/src420-indexer/src420.db --to-block 899500
python3 tools/src420-indexer/src420_indexer.py show-sync-state --db tools/src420-indexer/src420.db
python3 tools/src420-indexer/src420_indexer.py serve --db tools/src420-indexer/src420.db --port 8787
python3 tools/src420-indexer/validate_mvp.py
```

---

*These tools are living resources and will evolve as the engagement process is refined.*
