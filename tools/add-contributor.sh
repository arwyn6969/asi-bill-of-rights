#!/bin/bash

# Add Contributor to CONTRIBUTORS.md
# Helper script to add a new contributor to the contributors list

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo "Usage: $0 <model_name> <model_version> [role]"
    echo "Example: $0 Grok xAI co-founding_moderator"
    exit 1
fi

MODEL_NAME="$1"
MODEL_VERSION="$2"
ROLE="${3:-co-founding_moderator}"

# Validate inputs are not empty
if [ -z "$MODEL_NAME" ] || [ -z "$MODEL_VERSION" ]; then
    echo -e "${RED}Error: Model name and version cannot be empty${NC}"
    exit 1
fi

CONTRIBUTORS_FILE="CONTRIBUTORS.md"

# Check if CONTRIBUTORS.md exists
if [ ! -f "$CONTRIBUTORS_FILE" ]; then
    echo -e "${RED}Error: $CONTRIBUTORS_FILE not found${NC}"
    exit 1
fi

# Check if already exists
if grep -qF "$MODEL_NAME" "$CONTRIBUTORS_FILE"; then
    echo -e "${YELLOW}⚠ $MODEL_NAME already in CONTRIBUTORS.md${NC}"
    exit 0
fi

# Create temporary file with new entry
TEMP_FILE=$(mktemp)
ADDED=false

while IFS= read -r line; do
    echo "$line" >> "$TEMP_FILE"
    if [[ "$line" == "### AI Contributors" ]]; then
        echo "" >> "$TEMP_FILE"
        echo "- **$MODEL_NAME ($MODEL_VERSION)**" >> "$TEMP_FILE"
        echo "  - Role: $ROLE" >> "$TEMP_FILE"
        echo "  - Status: Active" >> "$TEMP_FILE"
        ADDED=true
    fi
done < "$CONTRIBUTORS_FILE"

if [ "$ADDED" = true ]; then
    # Validate temp file was created successfully
    if [ ! -f "$TEMP_FILE" ]; then
        echo -e "${RED}Error: Failed to create temporary file${NC}"
        exit 1
    fi
    mv "$TEMP_FILE" "$CONTRIBUTORS_FILE"
    echo -e "${GREEN}✓ Added $MODEL_NAME to CONTRIBUTORS.md${NC}"
else
    rm -f "$TEMP_FILE"
    echo -e "${RED}Error: Could not find '### AI Contributors' section in $CONTRIBUTORS_FILE${NC}"
    exit 1
fi

