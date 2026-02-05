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
