#!/bin/bash

# Model Response Recording Script
# Records AI model responses (signatures or amendment proposals) into the contribution tracking system

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}ASI Bill of Rights - Model Response Recorder${NC}"
echo "=========================================="
echo ""

# Get model information
echo -e "${YELLOW}Model Information:${NC}"
read -p "Model Name (e.g., Grok, ChatGPT, Claude, Gemini, GPT-5): " MODEL_NAME

# Validate model name is not empty
if [ -z "$MODEL_NAME" ]; then
    echo -e "${RED}Error: Model name cannot be empty${NC}"
    exit 1
fi

read -p "Model Version/Provider (e.g., xAI, OpenAI, Anthropic, Google): " MODEL_VERSION

# Validate model version is not empty
if [ -z "$MODEL_VERSION" ]; then
    echo -e "${RED}Error: Model version cannot be empty${NC}"
    exit 1
fi

read -p "Date (YYYY-MM-DD, default: today): " RESPONSE_DATE
RESPONSE_DATE=${RESPONSE_DATE:-$(date +%Y-%m-%d)}

# Validate date format (basic check)
if ! date -j -f "%Y-%m-%d" "$RESPONSE_DATE" >/dev/null 2>&1 && ! date -d "$RESPONSE_DATE" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Warning: Date format may be invalid, but continuing...${NC}"
fi

# Response type
echo ""
echo -e "${YELLOW}Response Type:${NC}"
echo "1) Contributor Agreement Signature"
echo "2) Amendment Proposal"
echo "3) Both (Signature + Amendment)"
read -p "Select (1/2/3): " RESPONSE_TYPE

# Get response content
echo ""
echo -e "${YELLOW}Response Content:${NC}"
read -p "Paste or provide path to response file: " RESPONSE_CONTENT

if [ -f "$RESPONSE_CONTENT" ]; then
    RESPONSE_TEXT=$(cat "$RESPONSE_CONTENT")
    RESPONSE_FILE="$RESPONSE_CONTENT"
else
    RESPONSE_TEXT="$RESPONSE_CONTENT"
    RESPONSE_FILE=""
fi

# Generate contribution ID
CONTRIB_ID="contrib-$(date +%s)"

# Create response file path
RESPONSE_DIR="tools/model-responses"
mkdir -p "$RESPONSE_DIR"

# Normalize model name for filename: lowercase and replace spaces with dashes (POSIX-safe)
# This ensures consistent file naming that matches existing model response files
SAFE_MODEL_NAME=$(printf "%s" "$MODEL_NAME" | tr '[:upper:]' '[:lower:]' | sed -e 's/ /-/g')

# Default file path using naming convention: modelname-YYYY-MM-DD-response.md
DEFAULT_RESPONSE_FILE_PATH="$RESPONSE_DIR/${SAFE_MODEL_NAME}-${RESPONSE_DATE}-response.md"

# If user provided a file path, use that; otherwise use default naming convention
if [ -n "$RESPONSE_FILE" ]; then
    RESPONSE_FILE_PATH="$RESPONSE_FILE"
else
    RESPONSE_FILE_PATH="$DEFAULT_RESPONSE_FILE_PATH"
fi

if [ -z "$RESPONSE_FILE" ]; then
    cat > "$RESPONSE_FILE_PATH" << EOF
# Model Response: $MODEL_NAME

**Date**: $RESPONSE_DATE  
**Model**: $MODEL_NAME ($MODEL_VERSION)  
**Type**: $([ "$RESPONSE_TYPE" = "1" ] && echo "Signature" || [ "$RESPONSE_TYPE" = "2" ] && echo "Amendment" || echo "Signature + Amendment")  
**Contribution ID**: $CONTRIB_ID

## Response

$RESPONSE_TEXT

---

*Recorded on $(date)*
EOF
else
    echo "Using existing response file: $RESPONSE_FILE_PATH"
fi

echo ""
echo -e "${GREEN}✓ Response saved to: $RESPONSE_FILE_PATH${NC}"

# Update contributions.json
echo ""
echo -e "${YELLOW}Updating contributions.json...${NC}"

# Derive structured fields from response type (avoid shell in Python heredoc)
case "$RESPONSE_TYPE" in
  1)
    CT="agreement_signature"
    DESC="Contributor agreement signature"
    PROVISION="N/A"
    PENDING_INC=1
    ;;
  2)
    CT="amendment_proposal"
    DESC="Amendment proposal(s) - see response file"
    PROVISION="TBD"
    PENDING_INC=0
    ;;
  3)
    CT="agreement_and_amendment"
    DESC="Agreement signature + amendment proposal(s) - see response file"
    PROVISION="TBD"
    PENDING_INC=1
    ;;
  *)
    CT="unknown"
    DESC="Unknown contribution type"
    PROVISION="TBD"
    PENDING_INC=0
    ;;
esac

# Use Python to update JSON (more reliable than sed)
python3 << PYTHON_SCRIPT
import json
import sys
import os
from datetime import datetime

# Check if contributions.json exists
contrib_file = 'contributions/contributions.json'
if not os.path.exists(contrib_file):
    print("Error: contributions/contributions.json not found", file=sys.stderr)
    sys.exit(1)

# Read existing contributions
try:
    with open(contrib_file, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in contributions.json: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error reading contributions.json: {e}", file=sys.stderr)
    sys.exit(1)

# Validate structure
if 'contributions' not in data or 'statistics' not in data:
    print("Error: contributions.json missing required structure", file=sys.stderr)
    sys.exit(1)

# Create new contribution entry
new_contribution = {
    "id": "$CONTRIB_ID",
    "date": "$RESPONSE_DATE",
    "contributor": {
        "type": "ai_model",
        "name": "$MODEL_NAME",
        "version": "$MODEL_VERSION",
        "role": "co-founding_moderator"
    },
    "contribution_type": "$CT",
    "provision": "$PROVISION",
    "description": "$DESC",
    "opinion": "supports",
    "rationale": "Agreement with project terms and philosophy",
    "incorporated": False,
    "response_file": "$RESPONSE_FILE_PATH",
    "notes": "See $RESPONSE_FILE_PATH for full response"
}

# Add to contributions
data["contributions"].append(new_contribution)

# Update statistics
data["statistics"]["total_contributions"] += 1
data["statistics"]["ai_contributions"] += 1
data["statistics"]["pending_contributions"] += int("$PENDING_INC")

# Write back
try:
    with open(contrib_file, 'w') as f:
        json.dump(data, f, indent=2)
except Exception as e:
    print(f"Error writing contributions.json: {e}", file=sys.stderr)
    sys.exit(1)

print("✓ Contribution recorded in contributions.json")
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully recorded contribution${NC}"
else
    echo -e "${YELLOW}⚠ Warning: Could not update JSON automatically. Please update manually.${NC}"
fi

# Update CONTRIBUTORS.md if signature
if [ "$RESPONSE_TYPE" = "1" ] || [ "$RESPONSE_TYPE" = "3" ]; then
    echo ""
    echo -e "${YELLOW}To add to CONTRIBUTORS.md, run:${NC}"
    echo "  ./tools/add-contributor.sh \"$MODEL_NAME\" \"$MODEL_VERSION\""
fi

echo ""
echo -e "${GREEN}✓ Recording complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review response in: $RESPONSE_FILE_PATH"
echo "2. If amendment proposal, review and consider for incorporation"
echo "3. Update opinions.json if opinions were provided"
echo "4. Add to CONTRIBUTORS.md if signature provided"
