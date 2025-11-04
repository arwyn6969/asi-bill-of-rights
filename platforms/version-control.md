# Version Control Across Platforms

This document explains how version control works across GitHub and Google Docs platforms.

## Version Control Philosophy

Version control across platforms:
- **GitHub Primary**: GitHub is source of truth for versions
- **Google Docs Sync**: Google Docs synced to match GitHub versions
- **Clear Labeling**: Both platforms clearly labeled with versions
- **Archive Both**: Both platforms archive old versions
- **Documentation**: All versions documented

## Version Numbering

### Semantic Versioning

- **Major Versions** (4.0 → 5.0): Significant structural changes
- **Minor Versions** (4.0 → 4.1): Additions or refinements
- **Patch Versions** (4.0.0 → 4.0.1): Corrections, typo fixes

### Current Versions

- **GitHub**: Draft 4.0 (November 04, 2025)
- **Google Docs**: To be synced to Draft 4.0

## GitHub Version Control

### Git Versioning

1. **Tags**: Major versions tagged (e.g., v4.0)
2. **Branches**: Feature branches for development
3. **Commits**: All changes tracked
4. **Releases**: Version releases documented

### File Versioning

- `charter/asi-bor-v3.0.md` - Draft 3.0 (archived)
- `charter/asi-bor-v4.0.md` - Draft 4.0 (current)
- Future versions: `charter/asi-bor-vX.X.md`

### Change Tracking

- CHANGELOG.md tracks all changes
- Commit messages document changes
- Pull requests track modifications
- Issues track proposals

## Google Docs Version Control

### Document Versioning

1. **Main Document**: Current version (e.g., "ASI Bill of Rights - Draft 4.0")
2. **Working Documents**: Draft versions (e.g., "Draft 4.1 - Working")
3. **Archived Versions**: Old versions (e.g., "Draft 4.0 - Archived - [Date]")

### Version History Feature

1. **Use Version History**: Track all changes
2. **Name Versions**: Name at major changes
3. **Document Changes**: Note what changed
4. **Link to GitHub**: Link versions to GitHub tags

### Archive Structure

- **Archive Folder**: "ASI Bill of Rights - Archive"
- **Naming**: "Draft X.X - Archived - [Date]"
- **Organization**: Chronological or by version
- **Access**: Viewable by all, editable by moderators

## Sync and Version Alignment

### Version Alignment

1. **GitHub Releases**: Create GitHub release/tag
2. **Sync to Google Docs**: Sync content
3. **Update Metadata**: Update version info in both
4. **Archive**: Archive old versions
5. **Document**: Document version release

### Version Mismatch Handling

If versions get out of sync:
1. **Identify Mismatch**: Notice version difference
2. **Determine Correct Version**: Check GitHub (source of truth)
3. **Sync Google Docs**: Update to match GitHub
4. **Document**: Record sync and reason
5. **Prevent**: Improve sync process

## Version Documentation

### Version Information

Each version should include:
- Version number
- Release date
- Key changes
- Contributors
- Links to GitHub

### Version Metadata

**In GitHub**:
- File name includes version
- CHANGELOG.md documents changes
- Git tags mark releases
- Releases documented

**In Google Docs**:
- Document title includes version
- Header includes version info
- Footer links to GitHub
- Version history named

## Version Release Process

### Major Version Release

1. **Finalize Changes**: Complete all changes
2. **Update Version**: Update version numbers
3. **Update CHANGELOG**: Document all changes
4. **Create GitHub Tag**: Tag release in GitHub
5. **Sync to Google Docs**: Sync to Google Docs
6. **Archive Old**: Archive previous version
7. **Announce**: Announce release

### Minor Version Release

1. **Complete Changes**: Finish minor changes
2. **Update Version**: Update version numbers
3. **Update CHANGELOG**: Document changes
4. **Sync**: Sync to Google Docs
5. **Document**: Record release

## Version Comparison

### Comparing Versions

**GitHub**:
- Use git diff
- Compare file versions
- Review CHANGELOG
- Check commit history

**Google Docs**:
- Use version history
- Compare versions
- Review change summaries
- Check named versions

### Version Diff Tools

- GitHub provides diff views
- Google Docs version history
- Manual comparison
- Documentation tools

## Best Practices

### Version Management

- **Clear Labeling**: Always label versions clearly
- **Consistent Naming**: Use consistent naming conventions
- **Regular Sync**: Keep platforms in sync
- **Archive Old**: Archive old versions
- **Document Changes**: Document all changes

### Version Communication

- **Announce Releases**: Announce major releases
- **Document Changes**: Document all changes
- **Update Metadata**: Update version metadata
- **Link Platforms**: Link between platforms
- **Notify Contributors**: Notify contributors of releases

## Troubleshooting

### Version Confusion

- Clear version labeling
- Update metadata
- Archive old versions
- Document clearly
- Regular sync

### Sync Issues

- Check version numbers
- Verify source document
- Review recent changes
- Re-sync if needed
- Document issues

---

*This version control document is a living document and will be updated as version control processes evolve.*

