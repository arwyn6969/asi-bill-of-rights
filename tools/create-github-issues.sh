#!/bin/bash
# GitHub Issues Creation Script
# Creates issues from GITHUB-ISSUES-TO-CREATE.md
#
# Prerequisites:
# - GitHub CLI (gh) installed and authenticated
# - Repository access configured
#
# Usage:
#   ./tools/create-github-issues.sh
#
# Or create issues manually using the formatted content in GITHUB-ISSUES-TO-CREATE.md

set -e

REPO="$(git remote get-url origin | sed -E 's/.*github.com[:/]([^/]+\/[^/]+)(\.git)?$/\1/')"
ISSUES_FILE="GITHUB-ISSUES-TO-CREATE.md"

if [ ! -f "$ISSUES_FILE" ]; then
    echo "Error: $ISSUES_FILE not found"
    exit 1
fi

echo "Creating GitHub issues from $ISSUES_FILE..."
echo "Repository: $REPO"
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install from: https://cli.github.com/"
    echo ""
    echo "Alternatively, create issues manually using the formatted content in $ISSUES_FILE"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Run: gh auth login"
    exit 1
fi

# Function to extract issue content
extract_issue() {
    local issue_num=$1
    local in_issue=false
    local title=""
    local labels=""
    local body=""
    local collecting_body=false
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##\ Issue\ $issue_num: ]]; then
            in_issue=true
            continue
        fi
        
        if [[ "$in_issue" == true ]] && [[ "$line" =~ ^##\ Issue\ ]]; then
            break
        fi
        
        if [[ "$in_issue" == true ]]; then
            if [[ "$line" =~ ^###\ Title ]]; then
                read -r title_line
                title=$(echo "$title_line" | sed 's/^\*\*//;s/\*\*$//')
            elif [[ "$line" =~ ^###\ Labels ]]; then
                read -r labels_line
                labels=$(echo "$labels_line" | sed "s/\`//g" | tr ',' ' ')
            elif [[ "$line" =~ ^###\ Body ]]; then
                collecting_body=true
                continue
            elif [[ "$collecting_body" == true ]]; then
                if [[ "$line" =~ ^--- ]]; then
                    break
                fi
                body+="$line"$'\n'
            fi
        fi
    done < "$ISSUES_FILE"
    
    echo "$title|$labels|$body"
}

# Create issues
for i in {1..6}; do
    echo "Creating Issue $i..."
    
    issue_data=$(extract_issue $i)
    IFS='|' read -r title labels body <<< "$issue_data"
    
    if [ -z "$title" ]; then
        echo "  Skipping Issue $i (not found or incomplete)"
        continue
    fi
    
    # Create issue using gh CLI
    if gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "$labels" 2>/dev/null; then
        echo "  ✓ Created: $title"
    else
        echo "  ✗ Failed to create: $title"
        echo "  You may need to create this manually from $ISSUES_FILE"
    fi
    
    echo ""
done

echo "Done! Check your GitHub repository for the created issues."
echo ""
echo "Note: If any issues failed to create, you can create them manually"
echo "using the formatted content in $ISSUES_FILE"
