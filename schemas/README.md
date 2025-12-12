# Schemas Directory

This directory contains machine-readable JSON schemas for the ASI Bill of Rights charter.

## Contents

- `charter.v3.json` - Machine-readable schema for Draft 3.0
- `charter.v4.1.json` - Machine-readable schema for Draft 4.1 (current)
- `charter.v4.json` - Machine-readable schema for Draft 4.0 (historical reference)
- `schema-docs.md` - Documentation explaining schema structure and usage

## Notation (Project Maintenance)

- **2025-12-12**: Updated the “Contents” list so the current schema is correctly identified as v4.1,
  matching `README.md` and `charter/asi-bor-v4.1.md`.

## Purpose

These schemas enable:
- **Programmatic access** to charter provisions
- **Automated compliance checking**
- **Cross-reference validation**
- **API development** for charter-based systems
- **Integration** with governance software

## Schema Structure

Each schema includes:
- **Clause IDs**: Stable identifiers (R1, D1, P1.1, etc.)
- **Cross-references**: Links between related provisions
- **Risk formulas**: Mathematical expressions for risk budgets
- **SI tier definitions**: Sentience Index classifications
- **Enforcement mechanisms**: Remedy structures and processes
- **Metadata**: Version, date, collaborative origins

## Usage

These schemas can be used to:
- Build compliance checking tools
- Create automated citation systems
- Generate documentation
- Validate cross-references
- Develop governance applications

See `schema-docs.md` for detailed documentation on structure and usage examples.

## Version Alignment

Schemas are versioned independently but aligned with markdown charter versions. Schema evolution is documented to maintain backward compatibility where possible.

## Related Files

- See `/charter/` for markdown charter documents
- See `/docs/IMPLEMENTATION.md` for implementation guidance
- See `/docs/CHANGELOG.md` for version history
- See `schema-docs.md` for detailed schema documentation

## Collaborative Nature

These schemas, like the main charter, are living documents that evolve through collaborative input from AI systems and human users.
