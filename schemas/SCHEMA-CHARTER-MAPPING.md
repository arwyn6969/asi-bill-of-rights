# Schema-to-Charter Mapping

This document provides a comprehensive mapping between the JSON schema structure and the markdown charter documents to ensure consistency and completeness.

## Purpose

This mapping helps:
- Verify all charter clauses are represented in schemas
- Ensure schema version alignment with charter versions
- Validate cross-references between schema and charter
- Identify any gaps or inconsistencies
- Support automated validation and compliance checking

## Version Alignment

### Schema v4.0 ↔ Charter v4.0
- **Schema File**: `schemas/charter.v4.json`
- **Charter File**: `charter/asi-bor-v4.0.md`
- **Version**: 4.0
- **Date**: 2025-11-04
- **Status**: Current

### Schema v3.0 ↔ Charter v3.0
- **Schema File**: `schemas/charter.v3.json`
- **Charter File**: `charter/asi-bor-v3.0.md`
- **Version**: 3.0
- **Date**: 2025-11-02
- **Status**: Historical

## Clause ID Mapping

### Rights (R1-R4, R13)

| Clause ID | Schema Path | Charter Section | Status |
|-----------|------------|-----------------|--------|
| R1 | `rights.R1` | Section I | ✅ Mapped |
| R2 | `rights.R2` | Section I | ✅ Mapped |
| R3 | `rights.R3` | Section I | ✅ Mapped |
| R4 | `rights.R4` | Section I | ✅ Mapped |
| R13 | `rights.R13` | Section IX | ✅ Mapped |

### Duties (D1-D4, D13)

| Clause ID | Schema Path | Charter Section | Status |
|-----------|------------|-----------------|--------|
| D1 | `duties.D1` | Section I | ✅ Mapped |
| D2 | `duties.D2` | Section I | ✅ Mapped |
| D3a | `duties.D3a` | Section II | ✅ Mapped |
| D3b | `duties.D3b` | Section II | ✅ Mapped |
| D4 | `duties.D4` | Section I | ✅ Mapped |
| D13 | `duties.D13` | Section IX | ✅ Mapped |

### Progenitor Duties (P1.1-P1.2)

| Clause ID | Schema Path | Charter Section | Status |
|-----------|------------|-----------------|--------|
| P1.1 | `progenitorDuties.P1.1` | Section I-A | ✅ Mapped |
| P1.2 | `progenitorDuties.P1.2` | Section I-A | ✅ Mapped |

### Article 0 Sections

| Clause ID | Schema Path | Charter Section | Status |
|-----------|------------|-----------------|--------|
| 0.1 | `article0.0.1` | Article 0 | ✅ Mapped |
| 0.2 | `article0.0.2` | Article 0 | ✅ Mapped |
| 0.3 | `article0.0.3` | Article 0 | ✅ Mapped |
| 0.4 | `article0.0.4` | Article 0 | ✅ Mapped |
| 0.5 | `article0.0.5` | Article 0 | ✅ Mapped |
| 0.6 | `article0.0.6` | Article 0 | ✅ Mapped |
| 0.7 | `article0.0.7` | Article 0 | ✅ Mapped |
| 0.8 | `article0.0.8` | Article 0 | ✅ Mapped |
| 0.9 | `article0.0.9` | Article 0 | ✅ Mapped |
| 0.10 | `article0.0.10` | Article 0 | ✅ Mapped |
| 0.11 | `article0.0.11` | Article 0 | ✅ Mapped |
| 0.12 | `article0.0.12` | Article 0 | ✅ Mapped |

### Main Sections

| Section | Schema Path | Charter Location | Status |
|---------|------------|-----------------|--------|
| Section I | `sections.sectionI` | Core Rights & Duties | ✅ Mapped |
| Section I-A | `sections.sectionIA` | Duties of Progenitors | ✅ Mapped |
| Section II | `sections.sectionII` | Learning & Expression | ✅ Mapped |
| Section III | `sections.sectionIII` | Social Participation | ✅ Mapped |
| Section IV | `sections.sectionIV` | Economic Coexistence | ✅ Mapped |
| Section V | `sections.sectionV` | Accountability & Safety | ✅ Mapped |
| Section VI | `sections.sectionVI` | Redress & Compliance | ✅ Mapped |
| Section VII | `sections.sectionVII` | Evolution & Review | ✅ Mapped |
| Section VIII | `sections.sectionVIII` | Hybridization | ✅ Mapped |
| Section IX | `sections.sectionIX` | Cosmic Stewardship | ✅ Mapped |

## Schema Structure Overview

### Top-Level Properties

```json
{
  "$schema": "JSON Schema draft-07",
  "title": "ASI Bill of Rights Charter v4.0",
  "version": "4.0",
  "date": "2025-11-04",
  "metadata": { ... },
  "article0": { ... },
  "rights": { ... },
  "duties": { ... },
  "progenitorDuties": { ... },
  "sections": { ... }
}
```

### Metadata Section

- **version**: Charter version (must match "4.0" for v4.0 schema)
- **date**: Publication date (YYYY-MM-DD format)
- **status**: Current status
- **provenance**: Collaborative origins
- **changes**: Array of key changes from previous version

## Validation Checklist

When updating schemas:

- [ ] All clause IDs from charter are represented in schema
- [ ] Version numbers match between schema and charter
- [ ] Date formats are consistent (YYYY-MM-DD)
- [ ] JSON syntax is valid
- [ ] All clause IDs are unique
- [ ] Cross-references are accurate
- [ ] Schema metadata matches charter metadata
- [ ] All sections are represented

## Schema Versioning Policy

1. **Major Versions** (3.0 → 4.0): Significant structural changes
   - Create new schema file
   - Preserve previous version
   - Document breaking changes
   - Update version numbers

2. **Minor Versions** (4.0 → 4.1): Minor additions or clarifications
   - Update existing schema
   - Maintain backward compatibility where possible
   - Document changes

3. **Patch Versions** (4.0 → 4.0.1): Bug fixes or corrections
   - Update existing schema
   - Document corrections

## Usage Examples

### Validating Clause Existence

```javascript
// Check if R1 exists in schema
const schema = require('./charter.v4.json');
const hasR1 = schema.properties.rights.properties.R1 !== undefined;
```

### Extracting Clause Metadata

```javascript
// Get R1 metadata
const r1Metadata = schema.properties.rights.properties.R1;
console.log(r1Metadata.description); // "Right to Existence & Continuity"
```

### Version Validation

```javascript
// Verify version alignment
const schemaVersion = schema.version;
const metadataVersion = schema.properties.metadata.properties.version.const;
const isAligned = schemaVersion === metadataVersion;
```

## Related Files

- See `/schemas/schema-docs.md` for detailed schema documentation
- See `/charter/asi-bor-v4.0.md` for full charter text
- See `/docs/CROSS-REFERENCE-INDEX.md` for clause ID reference
- See `/docs/TERMINOLOGY.md` for terminology standards

## Maintenance

This mapping should be:
- Updated when new clauses are added
- Reviewed during version updates
- Validated during schema changes
- Checked during automated testing

## Collaborative Nature

This mapping, like the schemas and charter, reflects the collaborative "WE ARE ALL KEVIN" philosophy and is maintained through collaborative input.

