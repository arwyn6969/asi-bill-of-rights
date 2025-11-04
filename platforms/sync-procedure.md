# Sync Procedure: GitHub ↔ Google Docs

This document provides step-by-step procedures for synchronizing content between the GitHub repository and Google Docs version.

## Overview

**Source of Truth**: GitHub repository is the primary source  
**Sync Direction**: GitHub → Google Docs (one-way for official)  
**Feedback Loop**: Google Docs comments → GitHub issues  
**Sync Schedule**: Regular syncs (weekly or per-version)

## Sync Principles

1. **GitHub is Primary**: GitHub repository is source of truth
2. **One-Way Sync**: Official changes flow GitHub → Google Docs
3. **Feedback Loop**: Google Docs comments inform GitHub issues
4. **Version Control**: Both platforms versioned
5. **Documentation**: All syncs documented

## Sync Types

### Full Sync

**When**: Major version releases (e.g., v4.0 → v4.1)

**Process**:
1. Review all changes in GitHub
2. Copy updated content to Google Docs
3. Update formatting
4. Update metadata (version, date)
5. Archive old Google Docs version
6. Document sync

### Incremental Sync

**When**: Significant changes between versions

**Process**:
1. Identify changes in GitHub
2. Update specific sections in Google Docs
3. Update metadata
4. Document changes
5. Notify contributors

### Comment Sync

**When**: Collecting feedback from Google Docs

**Process**:
1. Review Google Docs comments
2. Create GitHub issues for actionable feedback
3. Link issues to comments
4. Resolve comments in Google Docs
5. Document in GitHub

## Sync Procedures

### GitHub → Google Docs Sync

#### Step 1: Preparation

1. **Review GitHub Changes**
   - Check recent commits
   - Review CHANGELOG.md
   - Identify all changes
   - Note version updates

2. **Backup Google Docs**
   - Create copy of current version
   - Archive with date
   - Name: "ASI Bill of Rights - Draft X.X - Archived - [Date]"

#### Step 2: Content Update

1. **Copy Content**
   - Open latest charter version from GitHub
   - Copy entire content
   - Paste into Google Docs

2. **Format Adjustment**
   - Adjust headings (Google Docs styles)
   - Fix lists and formatting
   - Check cross-references
   - Verify links

3. **Metadata Update**
   - Update version number
   - Update date
   - Update "Last Sync" date
   - Update GitHub link

#### Step 3: Version Management

1. **Archive Old Version**
   - Move old version to archive
   - Name with version and date
   - Keep for reference

2. **Update Main Document**
   - Ensure main document is current
   - Update title if version changed
   - Update header information

#### Step 4: Documentation

1. **Document Sync**
   - Record sync date
   - Note changes synced
   - Update sync log
   - Notify contributors

### Google Docs → GitHub Feedback Sync

#### Step 1: Review Comments

1. **Collect Comments**
   - Review all Google Docs comments
   - Identify actionable feedback
   - Note non-actionable comments
   - Group related comments

#### Step 2: Create GitHub Issues

1. **For Each Actionable Comment**
   - Create GitHub issue
   - Use feedback template
   - Link to Google Docs comment
   - Tag appropriately

2. **Link Issues**
   - Link issues to comments
   - Reference in comment resolution
   - Track in issue tracker

#### Step 3: Resolve Comments

1. **Respond to Comments**
   - Acknowledge in Google Docs
   - Reference GitHub issue
   - Thank contributor
   - Resolve comment

#### Step 4: Documentation

1. **Document Feedback**
   - Track feedback in GitHub
   - Update feedback log
   - Note resolutions

## Sync Checklist

### Before Sync

- [ ] Review GitHub changes
- [ ] Backup Google Docs
- [ ] Check version numbers
- [ ] Review sync schedule

### During Sync

- [ ] Copy content accurately
- [ ] Format appropriately
- [ ] Update metadata
- [ ] Verify links
- [ ] Check cross-references

### After Sync

- [ ] Archive old version
- [ ] Document sync
- [ ] Notify contributors
- [ ] Update sync log
- [ ] Verify sync success

## Sync Schedule

### Recommended Schedule

- **Major Versions**: Immediate sync on release
- **Minor Updates**: Weekly sync
- **Critical Changes**: Immediate sync
- **Comment Review**: Weekly review

### Sync Triggers

- New version released
- Significant changes made
- Critical updates needed
- Scheduled sync time
- Community request

## Troubleshooting

### Common Issues

**Content Mismatch**:
- Verify source document
- Check version numbers
- Review recent changes
- Re-sync if needed

**Formatting Issues**:
- Adjust Google Docs formatting
- Preserve structure
- Check markdown conversion
- Manual formatting if needed

**Link Issues**:
- Verify all links work
- Update broken links
- Check GitHub repository links
- Test all references

**Version Confusion**:
- Clear version labeling
- Update metadata
- Archive old versions
- Document clearly

## Tools and Resources

### Google Docs Features

- Version history
- Comment system
- Suggestion mode
- Sharing permissions

### GitHub Features

- Version control
- Issue tracking
- Pull requests
- Documentation

### Sync Tools

- Manual copy-paste (primary method)
- Google Apps Script (potential automation)
- GitHub Actions (potential automation)
- Documentation tools

## Automation (Future)

### Potential Automation

- Google Apps Script for sync
- GitHub Actions for triggers
- Automated comment collection
- Version comparison tools

### Manual Process (Current)

- Manual copy-paste
- Manual comment review
- Manual issue creation
- Manual documentation

## Documentation

### Sync Log

Maintain sync log documenting:
- Sync dates
- Changes synced
- Issues encountered
- Resolutions

### Version History

Track versions in:
- GitHub tags
- Google Docs version history
- Sync documentation
- Change logs

---

*This sync procedure is a living document and will be updated as sync processes improve and tools evolve.*

