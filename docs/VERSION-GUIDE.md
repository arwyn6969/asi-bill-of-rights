# Version Reference Guide

This document provides comprehensive guidance on version numbering, date formats, and version references across the ASI Bill of Rights project.

## Purpose

This guide ensures:
- Consistent version numbering
- Standardized date formats
- Accurate version references
- Clear version migration paths

## Version Numbering

### Format
- **Standard**: Lowercase "v" followed by version number
- **Format**: vMAJOR.MINOR (e.g., v3.0, v4.0)
- **Examples**: v3.0, v4.0, v4.1

### Version Types

#### Major Versions (v3.0 → v4.0)
- Significant structural changes
- New major features
- Breaking changes
- Requires new schema file

#### Minor Versions (v4.0 → v4.1)
- Minor additions
- Clarifications
- Non-breaking changes
- Updates existing schema

#### Patch Versions (v4.0 → v4.0.1)
- Bug fixes
- Corrections
- Typo fixes
- Updates existing schema

## Date Formats

### Standard Format
- **Format**: "Month DD, YYYY" (e.g., "November 04, 2025")
- **Use**: Charter documents, README files, human-readable dates

### ISO Format
- **Format**: "YYYY-MM-DD" (e.g., "2025-11-04")
- **Use**: Schemas, JSON files, machine-readable dates
- **Standard**: ISO 8601

### Version Dates
- **Current Version**: v4.1 - November 04, 2025 (2025-11-04)
- **Previous Version**: v4.0 - November 04, 2025 (2025-11-04)
- **Historical Version**: v3.0 - November 02, 2025 (2025-11-02)

## Version References

### Charter Documents
- **Current**: `charter/asi-bor-v4.1.md`
- **Previous**: `charter/asi-bor-v4.0.md`
- **Historical**: `charter/asi-bor-v3.0.md`
- **Naming**: `asi-bor-v{version}.md`

### Schemas
- **Current**: `schemas/charter.v4.1.json`
- **Previous**: `schemas/charter.v4.json`
- **Historical**: `schemas/charter.v3.json`
- **Naming**: `charter.v{version}.json`

### Version Badges
```markdown
[![Version](https://img.shields.io/badge/version-4.0-blue.svg)](charter/asi-bor-v4.0.md)
```

## Version Consistency Checklist

When updating versions:

- [ ] Update version number in charter file
- [ ] Update version number in schema file
- [ ] Update version number in README.md
- [ ] Update version number in CHANGELOG.md
- [ ] Update date in all version references
- [ ] Update badges (if used)
- [ ] Verify all cross-references are updated
- [ ] Update schema metadata

## Version Migration

### Migrating from v3.0 to v4.0

**Key Changes**:
- Arms race mitigation provisions (IX.1)
- Innovation waivers for anti-monopoly (IV.A)
- Escalation protocols (0.8)
- 2025 framework integration (Appendix B)

**Migration Steps**:
1. Review CHANGELOG.md for all changes
2. Update references from v3.0 to v4.0
3. Review new provisions (IX.1, 0.8 enhancements)
4. Update integration mappings
5. Verify schema compatibility

### Schema Migration

**v3.0 to v4.0**:
- New schema file created (charter.v4.json)
- v3.0 schema preserved for reference
- Backward compatibility maintained where possible
- New fields added for new provisions

## Version Reference Map

### Current Version (v4.1)
- **Charter**: `charter/asi-bor-v4.1.md`
- **Schema**: `schemas/charter.v4.1.json`
- **Date**: November 04, 2025 (2025-11-04)
- **Status**: Current

### Previous Version (v4.0)
- **Charter**: `charter/asi-bor-v4.0.md`
- **Schema**: `schemas/charter.v4.json`
- **Date**: November 04, 2025 (2025-11-04)
- **Status**: Previous

### Previous Versions

#### v3.0
- **Charter**: `charter/asi-bor-v3.0.md`
- **Schema**: `schemas/charter.v3.json`
- **Date**: November 02, 2025 (2025-11-02)
- **Status**: Historical

## Version in Different Contexts

### README References
```markdown
- **Latest Version**: [Draft 4.1](charter/asi-bor-v4.1.md) (November 04, 2025)
- **Previous Version**: [Draft 4.0](charter/asi-bor-v4.0.md) (November 04, 2025)
- **Historical Version**: [Draft 3.0](charter/asi-bor-v3.0.md) (November 02, 2025)
```

### Code/Schema References
```json
{
  "version": "4.1",
  "date": "2025-11-04"
}
```

### Citation Format
```
ASI Bill of Rights, Draft 4.1, November 04, 2025
```

## Related Files

- See `/docs/CHANGELOG.md` for version history
- See `/charter/` for charter versions
- See `/schemas/` for schema versions
- See `/docs/CROSS-REFERENCE-INDEX.md` for reference formats

## Maintenance

This guide should be:
- Updated when version numbering changes
- Referenced when creating new versions
- Used for version consistency checks
- Maintained collaboratively

## Collaborative Nature

This version guide reflects the collaborative "WE ARE ALL KEVIN" philosophy and is maintained through collaborative input.

