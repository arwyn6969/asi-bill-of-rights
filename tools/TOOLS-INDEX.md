# Tools Index

This document provides a comprehensive index of all tools available in the ASI Bill of Rights project.

## Purpose

This index helps:
- Find the right tool for a task
- Understand tool usage
- Learn tool dependencies
- Get help with tools

## Available Tools

### Model Engagement Tools

#### record-model-response.sh
**Purpose**: Records AI model responses into the contribution tracking system

**Location**: `tools/record-model-response.sh`

**Usage**:
```bash
./tools/record-model-response.sh
```

**What It Does**:
1. Prompts for model information (name, version, date)
2. Asks for response type (signature/amendment/both)
3. Collects response content
4. Saves to `tools/model-responses/`
5. Updates `contributions/contributions.json`
6. Provides next steps

**Dependencies**: Bash, JSON processing

**Error Handling**: Validates inputs, checks file existence, handles errors gracefully

**Documentation**: See `tools/README.md` for detailed usage

#### add-contributor.sh
**Purpose**: Helper script to add a new contributor to CONTRIBUTORS.md

**Location**: `tools/add-contributor.sh`

**Usage**:
```bash
./tools/add-contributor.sh "Model Name" "Model Version" [role]
```

**Example**:
```bash
./tools/add-contributor.sh "Grok" "xAI" "co-founding_moderator"
```

**What It Does**:
1. Validates input parameters
2. Checks if contributor already exists
3. Adds contributor to CONTRIBUTORS.md
4. Provides confirmation

**Dependencies**: Bash, grep

**Error Handling**: Validates inputs, checks file existence, prevents duplicates

**Documentation**: See `tools/README.md` for detailed usage

### Documentation Tools

#### model-engagement.md
**Purpose**: Guide for engaging different AI models in Cursor

**Location**: `tools/model-engagement.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Prompt templates
- Engagement workflows
- Best practices
- Examples

#### amendment-collector.md
**Purpose**: Guide for collecting and organizing amendment proposals

**Location**: `tools/amendment-collector.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Amendment collection process
- Organization guidelines
- Review procedures

#### quick-model-prompt.md
**Purpose**: Quick reference for model engagement prompts

**Location**: `tools/quick-model-prompt.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Quick prompt templates
- Common scenarios
- Quick reference

#### MASTER-PROMPT.md
**Purpose**: Comprehensive master prompt for model engagement

**Location**: `tools/MASTER-PROMPT.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Complete prompt template
- All engagement scenarios
- Comprehensive guidance

#### RESPONSE-SAVE-PROMPT.md
**Purpose**: Prompt for saving model responses

**Location**: `tools/RESPONSE-SAVE-PROMPT.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Response saving instructions
- Format guidelines
- Best practices

### Workflow Tools

#### QUICK-START.md
**Purpose**: Quick start guide for tools and workflows

**Location**: `tools/QUICK-START.md`

**Usage**: Reference guide (not executable)

**What It Provides**:
- Quick start instructions
- Common workflows
- Tool usage examples

#### ci/validate_schemas.py
**Purpose**: Mirrors the schema-validation GitHub Action locally (charter schemas + contributions metadata).

**Location**: `tools/ci/validate_schemas.py`

**Usage**:
```bash
pip install jsonschema  # required once
python3 tools/ci/validate_schemas.py
```

**What It Does**:
1. Validates `schemas/charter.v5.0.json`, `schemas/charter.v4.2.json`, `schemas/charter.v4.1.json`, `schemas/charter.v4.json`, `schemas/charter.v3.json`, plus `schemas/charter.v5.0-cae-extension.json` against Draft 7.
2. Confirms required top-level fields exist.
3. Verifies `contributions/contributions.json` statistics match recorded entries.

#### ci/validate_crossrefs.py
**Purpose**: Cross-checks clause IDs across charter markdown + schemas.

**Location**: `tools/ci/validate_crossrefs.py`

**Usage**:
```bash
python3 tools/ci/validate_crossrefs.py
```

**What It Does**:
1. v4.1 + v4.2: Ensures every clause ID exists in both charter and schema (exact match).
2. v5.0: Ensures every clause ID present in the schema exists in the charter (schema coverage subset).
3. Prints concise ✓/✗ output identical to the CI job.

#### ci/validate_internal_links.py
**Purpose**: Validates that internal markdown links in tracked `.md` files resolve to real files.

**Location**: `tools/ci/validate_internal_links.py`

**Usage**:
```bash
python3 tools/ci/validate_internal_links.py
```

**What It Does**:
1. Scans tracked markdown files (`git ls-files '*.md'`) for links of the form `[text] (path)`.
2. Skips external links and pure anchors; strips fragments/querystrings.
3. Reports broken internal references with `file:line` diagnostics.

#### ci/validate_all.py
**Purpose**: Runs the local validation helpers in one command (internal links + crossrefs + schemas when available + SRC-420 validator when present).

**Location**: `tools/ci/validate_all.py`

**Usage**:
```bash
python3 tools/ci/validate_all.py
```

**What It Does**:
1. Runs internal markdown link validation.
2. Runs charter/schema cross-reference validation.
3. Runs schema validation when `jsonschema` is installed.
4. Runs SRC-420 indexer regression validation when `tools/src420-indexer/validate_mvp.py` exists.

### Governance Infrastructure Tools

#### src420_indexer.py
**Purpose**: Deterministic SRC-420 indexer MVP with SQLite state and query API.

**Location**: `tools/src420-indexer/src420_indexer.py`

**Usage**:
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

**What It Does**:
1. Initializes indexer schema (`events`, `spaces`, `proposals`, `votes`, `delegations`, `attestations`, `balance_snapshots`, `sync_state`).
2. Imports block-height balance snapshots for snapshot voting power.
3. Ingests and validates SRC-420 operations (`DEPLOY`, `PROPOSE`, `VOTE`, `DELEGATE`, `ATTEST`) in deterministic order.
4. Syncs paginated HTTP feeds via `sync-http` with cursor tracking, finality gating, and optional reorg checks.
5. Supports `rollback-to-block` rebuilds from event history for reorg recovery.
6. Exposes read APIs for spaces, proposals, votes, tallies, delegations, and voting power.
7. Includes a regression validation suite (`validate_mvp.py`) for spec-critical rules, including rollback/reorg tests.

**Fixtures**:
- `tools/src420-indexer/fixtures/sample_balances.jsonl`
- `tools/src420-indexer/fixtures/sample_events.jsonl`

**Runbook**:
- `tools/src420-indexer/README.md`

## Tool Categories

### By Function

- **Model Engagement**: Tools for engaging AI models
- **Contribution Tracking**: Tools for tracking contributions
- **Documentation**: Tools for documentation management
- **Workflow**: Tools for workflow management

### By Type

- **Scripts**: Executable bash scripts
- **Guides**: Documentation and reference materials
- **Templates**: Prompt templates and examples

## Tool Dependencies

### Required Software
- Bash (for scripts)
- Git (for version control)
- Text editor (for documentation)

### Optional Software
- Python (for JSON processing, if needed)
- jq (for JSON parsing, if needed)

## Usage Examples

### Example 1: Recording a Model Response

```bash
# Navigate to project root
cd "/path/to/ASI-BILL-OF-RIGHTS"

# Run the script
./tools/record-model-response.sh

# Follow prompts:
# - Model Name: Grok
# - Model Version: xAI
# - Date: 2025-11-05
# - Response Type: 1 (Signature)
# - Paste response content
```

### Example 2: Adding a Contributor

```bash
# Add a new AI contributor
./tools/add-contributor.sh "NewModel" "Provider" "co-founding_moderator"
```

## Error Handling

All scripts include:
- Input validation
- Error messages
- Graceful failure
- Helpful error descriptions

## Related Files

- See `tools/README.md` for detailed tool documentation
- See `docs/CONTRIBUTING.md` for contribution workflows
- See `docs/CONTRIBUTOR-JOURNEY.md` for contributor workflows

## Maintenance

Tools should be:
- Updated when processes change
- Tested regularly
- Documented clearly
- Maintained with error handling

## Collaborative Nature

These tools support the collaborative "WE ARE ALL KEVIN" philosophy by facilitating engagement with AI models and tracking contributions from all participants.
