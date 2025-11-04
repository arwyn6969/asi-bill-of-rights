#!/bin/bash

# Model Response Recording Script
# Records AI model responses (signatures or amendment proposals) into the contribution tracking system

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}ASI Bill of Rights - Model Response Recorder${NC}"
echo "=========================================="
echo ""

# Get model information
echo -e "${YELLOW}Model Information:${NC}"
read -p "Model Name (e.g., Grok, ChatGPT, Claude, Gemini): " MODEL_NAME
read -p "Model Version/Provider (e.g., xAI, OpenAI, Anthropic, Google): " MODEL_VERSION
read -p "Date (YYYY-MM-DD, default: today): " RESPONSE_DATE
RESPONSE_DATE=${RESPONSE_DATE:-$(date +%Y-%m-%d)}

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

# Create response file
RESPONSE_DIR="tools/model-responses"
mkdir -p "$RESPONSE_DIR"
RESPONSE_FILE_PATH="$RESPONSE_DIR/${MODEL_NAME,,}-${RESPONSE_DATE}.md"

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

echo ""
echo -e "${GREEN}✓ Response saved to: $RESPONSE_FILE_PATH${NC}"

# Update contributions.json
echo ""
echo -e "${YELLOW}Updating contributions.json...${NC}"

# Use Python to update JSON (more reliable than sed)
python3 << PYTHON_SCRIPT
import json
import sys
from datetime import datetime

# Read existing contributions
with open('contributions/contributions.json', 'r') as f:
    data = json.load(f)

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
    "contribution_type": "$([ "$RESPONSE_TYPE" = "1" ] && echo "agreement_signature" || [ "$RESPONSE_TYPE" = "2" ] && echo "amendment_proposal" || echo "agreement_and_amendment")",
    "provision": "N/A" if "$RESPONSE_TYPE" == "1" else "TBD",
    "description": "Contributor agreement signature" if "$RESPONSE_TYPE" == "1" else "Amendment proposal(s) - see response file",
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
if "$RESPONSE_TYPE" != "2":
    data["statistics"]["pending_contributions"] += 1

# Write back
with open('contributions/contributions.json', 'w') as f:
    json.dump(data, f, indent=2)

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

