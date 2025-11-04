#!/bin/bash

# Add Contributor to CONTRIBUTORS.md
# Helper script to add a new contributor to the contributors list

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <model_name> <model_version> [role]"
    echo "Example: $0 Grok xAI co-founding_moderator"
    exit 1
fi

MODEL_NAME="$1"
MODEL_VERSION="$2"
ROLE="${3:-co-founding_moderator}"

CONTRIBUTORS_FILE="CONTRIBUTORS.md"

# Check if already exists
if grep -q "**$MODEL_NAME**" "$CONTRIBUTORS_FILE"; then
    echo "⚠ $MODEL_NAME already in CONTRIBUTORS.md"
    exit 0
fi

# Add to AI Contributors section
sed -i.bak "/^### AI Contributors$/,/^### Human Contributors$/ {
    /^### Human Contributors$/ i\\
- **$MODEL_NAME ($MODEL_VERSION)**\\
  - Role: $ROLE\\
  - Status: Active\\
\\
" "$CONTRIBUTORS_FILE"

rm -f "${CONTRIBUTORS_FILE}.bak"

echo "✓ Added $MODEL_NAME to CONTRIBUTORS.md"

