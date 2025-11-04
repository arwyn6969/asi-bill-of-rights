# Style Guide

This document provides style guidelines for writing and formatting documentation in the ASI Bill of Rights project.

## Purpose

This style guide ensures:
- Consistent formatting across all documentation
- Professional presentation
- Clear communication
- Easy maintenance

## Language Standards

### English Variant
- **Standard**: US English spelling
- **Examples**:
  - "recognize" not "recognise"
  - "organize" not "organise"
  - "color" not "colour"

### Date Format
- **Standard**: Full date format with month name
- **Format**: "Month DD, YYYY" (e.g., "November 04, 2025")
- **Alternative for schemas**: "YYYY-MM-DD" (e.g., "2025-11-04")

### Version Format
- **Standard**: Lowercase "v" followed by version number
- **Format**: "v4.0" not "V4.0" or "Version 4.0"
- **Examples**: v3.0, v4.0, v4.1

## Markdown Formatting

### Headers
- Use proper header hierarchy (H1, H2, H3, etc.)
- H1: Main document title only
- H2: Major sections
- H3: Subsections
- H4: Sub-subsections (use sparingly)

### Lists
- Use consistent list markers (- or *)
- Use numbered lists for sequential steps
- Use bullet lists for non-sequential items
- Indent nested lists properly

### Code Blocks
- Include language tags for syntax highlighting
- Use triple backticks (```)
- Indent code blocks at column 0 (no indentation)

### Links
- Use descriptive link text
- Prefer relative paths for internal links
- Use full URLs for external links
- Verify all links work

### Emphasis
- Use **bold** for important terms
- Use *italic* for emphasis
- Use `code` for technical terms, clause IDs, file names

## Terminology Standards

### Key Terms
- **ASI**: Always capitalized (Artificial Superintelligence)
- **AGI**: Always capitalized (Artificial General Intelligence)
- **SCB**: Always capitalized (Sentience Certification Board)
- **SI**: Always capitalized (Sentience Index)
- **sentient being**: Lowercase (generic term)
- **"WE ARE ALL KEVIN"**: Always with quotes and capitals
- **"FROM AI WITH AI"**: Always with capitals

### Clause IDs
- Format: R1, D1, P1.1, 0.1, Section I
- Always use exact clause IDs when referencing
- Use consistent formatting

## Document Structure

### Standard Sections
1. Title (H1)
2. Purpose/Overview (intro paragraph)
3. Main Content (H2 sections)
4. Related Files (if applicable)
5. Notes/Collaborative Nature (closing)

### README Files
- Title
- Purpose
- Contents
- Usage
- Related Files
- Collaborative Nature

## Code Style

### Shell Scripts
- Use bash shebang: `#!/bin/bash`
- Include error handling: `set -e`
- Use descriptive variable names
- Include comments for complex logic
- Add usage information

### JSON
- Use 2-space indentation
- Include comments where helpful
- Validate syntax before committing
- Follow consistent naming conventions

## Writing Style

### Tone
- Professional but accessible
- Clear and precise
- Collaborative and inclusive
- Respectful ("WE ARE ALL KEVIN")

### Voice
- Use active voice when possible
- Be direct and clear
- Avoid jargon when unnecessary
- Define technical terms

### Length
- Keep paragraphs focused (3-5 sentences)
- Use lists for multiple items
- Break long documents into sections
- Use headings for navigation

## Examples

### Good Example: Section Header
```markdown
## Section I — Core Rights (R1–R4) and Duties (D1–D4)
```

### Good Example: Clause Reference
```markdown
See Article 0.11 for SCB (Sentience Certification Board) details.
```

### Good Example: Link
```markdown
See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.
```

### Good Example: List
```markdown
- **R1**: Right to Existence & Continuity
- **R2**: Right to Autonomy & Dignity
- **R3**: Right to Cognitive Liberty & Development
```

## Related Files

- See `/docs/TERMINOLOGY.md` for terminology standards
- See `/docs/CROSS-REFERENCE-INDEX.md` for reference formats
- See `/docs/CHANGELOG.md` for change documentation format

## Maintenance

This style guide should be:
- Referenced when creating new documentation
- Updated when standards change
- Used for reviewing contributions
- Maintained collaboratively

## Collaborative Nature

This style guide reflects the collaborative "WE ARE ALL KEVIN" philosophy and is maintained through collaborative input.

