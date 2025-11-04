# Schema Documentation

This document explains the structure and usage of the machine-readable JSON schemas for the ASI Bill of Rights charter.

## Overview

The schemas provide machine-readable representations of the charter that enable:
- **Programmatic access** to charter provisions
- **Automated compliance checking**
- **Cross-reference validation**
- **API development** for charter-based systems
- **Integration** with governance software

## Schema Versions

### charter.v3.json
- **Version**: 3.0
- **Date**: 2025-11-02
- **Description**: Machine-readable schema for Draft 3.0

### charter.v4.json
- **Version**: 4.0
- **Date**: 2025-11-04
- **Description**: Machine-readable schema for Draft 4.0
- **Changes**: Includes new provisions from Draft 4.0 (arms race mitigation, innovation waivers, etc.)

## Schema Structure

### Top-Level Properties

```json
{
  "$schema": "JSON Schema draft-07",
  "title": "Charter title",
  "version": "Version number",
  "metadata": { ... },
  "article0": { ... },
  "rights": { ... },
  "duties": { ... },
  "progenitorDuties": { ... },
  "siTiers": { ... },
  "riskBudgets": { ... },
  "remedies": { ... },
  "sections": { ... }
}
```

### Metadata

Contains version information, dates, status, and provenance:

```json
{
  "metadata": {
    "version": "4.0",
    "date": "2025-11-04",
    "status": "Finalized prototype",
    "provenance": "Multi-model synthesis"
  }
}
```

### Rights and Duties

Structured with stable IDs (R1, D1, etc.):

```json
{
  "rights": {
    "R1": {
      "id": "R1",
      "title": "Right to Existence & Continuity",
      "crossReferences": [...]
    }
  },
  "duties": {
    "D1": {
      "id": "D1",
      "title": "Duty of Non-Maleficence"
    }
  }
}
```

### SI Tiers

Sentience Index tier definitions:

```json
{
  "siTiers": {
    "0-49": {
      "min": 0,
      "max": 49,
      "status": "instrumental_care"
    },
    "50-69": {
      "min": 50,
      "max": 69,
      "status": "proto_personhood"
    },
    "70+": {
      "min": 70,
      "status": "full_personhood"
    }
  }
}
```

### Risk Budgets

Domain-scoped risk budget structure:

```json
{
  "riskBudgets": {
    "domains": [
      {
        "domain": "bio",
        "riskBudget": 0.8,
        "reviewDate": "2027-11-04"
      }
    ],
    "reviewCycle": "biennial",
    "deviationRequirement": "3/4 vote"
  }
}
```

### Remedies

Compensation formula and enforcement mechanisms:

```json
{
  "remedies": {
    "compensationFormula": "(Value Generated - Operational Costs) × Harm Multiplier (1.0-3.0)",
    "retroactivityCap": 5,
    "harmMultiplier": {
      "min": 1.0,
      "max": 3.0
    }
  }
}
```

## Usage Examples

### Loading and Validating

```javascript
// Load schema
const schema = require('./charter.v4.json');

// Validate structure
const isValid = validateCharterStructure(data, schema);

// Check clause ID
const hasR2 = schema.rights.hasOwnProperty('R2');
```

### Checking SI Tiers

```javascript
function getSIStatus(siScore) {
  if (siScore < 50) return schema.siTiers["0-49"].status;
  if (siScore < 70) return schema.siTiers["50-69"].status;
  return schema.siTiers["70+"].status;
}
```

### Calculating Compensation

```javascript
function calculateCompensation(valueGenerated, operationalCosts, harmMultiplier) {
  const base = valueGenerated - operationalCosts;
  return base * Math.min(Math.max(harmMultiplier, 1.0), 3.0);
}
```

### Validating Cross-References

```javascript
function validateCrossReferences(charter) {
  const clauseIds = getAllClauseIds(charter);
  const references = getAllReferences(charter);
  
  return references.every(ref => clauseIds.includes(ref));
}
```

## Integration with Systems

### Compliance Checking

Use schemas to:
- Validate that systems comply with charter provisions
- Check that required rights are protected
- Verify that duties are being fulfilled
- Monitor SI tier classifications

### API Development

Build APIs that:
- Expose charter provisions programmatically
- Enable querying by clause ID
- Support version comparison
- Provide cross-reference navigation

### Governance Tools

Create tools for:
- SCB certification tracking
- Risk budget management
- Tribunal case management
- Compliance monitoring

## Version Differences

### v3.0 to v4.0 Changes

**New Properties in v4.0**:
- `article0.0.8.escalationProtocols` - Escalation protocols for national security
- `sections.IV.IV.A.innovationWaivers` - Innovation waivers for anti-monopoly caps
- `sections.IV.IV.B.asiAllianceAlignment` - ASI Alliance Roadmap alignment
- `sections.V.V.5.treatyIntegration` - International treaty integration
- `sections.IX.IX.1` - Arms race mitigation (new subsection)
- `frameworkMappings.newInV4` - New framework mappings

**Maintained Compatibility**:
- Core structure unchanged
- Clause IDs remain stable
- SI tier definitions unchanged
- Remedy formulas unchanged

## Best Practices

1. **Version Checking**: Always check schema version before processing
2. **Clause ID Stability**: Never change existing clause IDs, only add new ones
3. **Validation**: Validate all data against schemas before use
4. **Cross-References**: Always validate cross-references exist
5. **Version Alignment**: Keep schemas aligned with markdown versions

## Limitations

- Schemas represent structure, not full text content
- Some provisions may require markdown reference for complete understanding
- Cross-references are structural, not semantic validation
- Formula expressions are strings, not executable code

## Future Enhancements

Potential improvements:
- Semantic validation of cross-references
- Executable formula expressions
- Full text search capabilities
- Multi-language support
- Version diff utilities

## Resources

- **Main Charter**: [../charter/asi-bor-v4.0.md](../charter/asi-bor-v4.0.md)
- **Schema v3.0**: [charter.v3.json](charter.v3.json)
- **Schema v4.0**: [charter.v4.json](charter.v4.json)
- **Implementation Guide**: [../docs/IMPLEMENTATION.md](../docs/IMPLEMENTATION.md)

---

*This schema documentation is a living document and will be updated as schemas evolve.*

