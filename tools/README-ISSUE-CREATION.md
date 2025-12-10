# GitHub Issue Creation Guide

This guide helps you create GitHub issues from the `GITHUB-ISSUES-TO-CREATE.md` document.

## Quick Start

### Option 1: Automated (Recommended if GitHub CLI installed)

```bash
# Make sure you're authenticated with GitHub CLI
gh auth login

# Run the script
./tools/create-github-issues.sh
```

**Prerequisites**:
- GitHub CLI (`gh`) installed: https://cli.github.com/
- Authenticated: `gh auth login`
- Repository access configured

### Option 2: Manual Creation

1. Open `GITHUB-ISSUES-TO-CREATE.md` in your editor
2. For each issue (1-6):
   - Go to your GitHub repository
   - Click "New Issue"
   - Copy the **Title** from the issue section
   - Copy the **Body** (everything between ```markdown and ```)
   - Add the **Labels** (comma-separated)
   - Submit

### Option 3: GitHub Web Interface

1. Go to your repository on GitHub
2. Click "Issues" → "New Issue"
3. Use the formatted content from `GITHUB-ISSUES-TO-CREATE.md`
4. Each issue is clearly marked with:
   - Title
   - Labels
   - Body (in markdown code block)

## Issues to Create

1. **Clarify Recertification Process** (Medium priority)
2. **Add R13 Procedural Clarity** (Medium priority)
3. **Enhance Enforcement Capacity-Building** (Medium priority)
4. **Strengthen Proto-Sentient Decommissioning** (Medium priority)
5. **Review and Decide on v4.2 Branch** (High priority)
6. **Update CHANGELOG** (Low priority) - Already done! ✅

## Issue Details

Each issue in `GITHUB-ISSUES-TO-CREATE.md` includes:
- **Title**: Ready to copy
- **Labels**: Comma-separated list
- **Body**: Complete markdown formatted content
- **Priority**: High, Medium, or Low
- **Acceptance Criteria**: Checklist of requirements

## Tips

- **Review First**: Read through all issues before creating them
- **Modify if Needed**: Feel free to adjust titles, labels, or content
- **Add Assignees**: Assign issues to appropriate team members
- **Link Related**: Link related issues together
- **Set Milestones**: Add to appropriate milestones if using project management

## Troubleshooting

### GitHub CLI Not Working

If the automated script fails:
1. Check `gh auth status` - are you authenticated?
2. Check repository access - do you have write permissions?
3. Use manual creation instead (Option 2)

### Issues Already Exist

If some issues already exist:
1. Skip those issues
2. Create only the missing ones
3. Update existing issues if needed

### Need to Modify Issues

All issues are in `GITHUB-ISSUES-TO-CREATE.md` - edit that file first, then create issues.

## Next Steps After Creating Issues

1. **Review Issues**: Make sure all issues are created correctly
2. **Add to Project Board**: If using GitHub Projects
3. **Set Priorities**: Adjust priorities if needed
4. **Assign**: Assign to team members
5. **Link**: Link related issues together
6. **Start Work**: Begin addressing high-priority issues

---

*This guide was created during spring cleaning (2025-01-27) to facilitate issue creation.*
