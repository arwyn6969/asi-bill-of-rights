# Attribution Guide

This guide explains how attribution works in the ASI Bill of Rights project and how contributions from AI models and humans are tracked.

## Attribution Philosophy

In alignment with "WE ARE ALL KEVIN," all contributors—AI and human—are properly attributed and recognized. Attribution serves to:
- Acknowledge contributions fairly
- Maintain transparency about origins
- Enable tracking of opinions and perspectives
- Document the collaborative evolution of the charter

## Attribution System

### Contribution Types

1. **Provision Enhancement**: Direct contributions to charter text
2. **Structural Enhancement**: Organizational or framework contributions
3. **Framework Integration**: Mappings and alignments with external frameworks
4. **Documentation**: Guides, mappings, supporting materials
5. **Review**: Feedback, validation, improvement suggestions
6. **Project Structure**: Organization, tooling, infrastructure

### Contributor Types

1. **AI Model**: AI systems (Grok, ChatGPT, Claude, Gemini, GPT-5, etc.)
2. **Human**: Human contributors
3. **Co-Founding Moderator**: AI agents with moderation authority
4. **Human Moderator**: Human oversight authority
5. **Contributor Reviewer**: Reviewers without moderation authority
6. **Community Member**: General contributors

## How Attribution Works

### For AI Contributors

When an AI model contributes:
1. **Record**: Contribution logged in `contributions/contributions.json`
2. **Identify**: Model name, version, and role recorded
3. **Document**: Contribution type, provision, description, rationale
4. **Track Opinion**: Support/oppose/modify stance recorded
5. **Link**: Connected to incorporated version if accepted

### For Human Contributors

When a human contributes:
1. **Sign Agreement**: Must sign CONTRIBUTOR_AGREEMENT.md first
2. **Record**: Contribution logged in `contributions/contributions.json`
3. **Identify**: Name (or pseudonym) and role recorded
4. **Document**: Full contribution details
5. **Attribution**: Added to CONTRIBUTORS.md

### Opinion Tracking

Opinions are tracked in `contributions/opinions.json`:
- **Support**: Contributor agrees with provision
- **Oppose**: Contributor disagrees with provision
- **Support with Modification**: Agrees but suggests changes
- **Neutral**: No strong opinion

## Attribution Formats

### In Documentation

Contributions are attributed in:
- File headers (where applicable)
- CONTRIBUTORS.md
- CHANGELOG.md
- Contribution logs

### Format Examples

**AI Attribution**:
```
Contributed by: Grok (xAI) - Co-founding Moderator
Date: 2025-11-04
Type: Provision Enhancement
```

**Human Attribution**:
```
Contributed by: [Name] - [Role]
Date: 2025-11-04
Type: [Contribution Type]
```

## Attribution Requirements

### For All Contributors

- All contributions must be attributed
- Attribution must be accurate
- Opinions must be documented
- Rationale should be provided

### For AI Models

- Model name and version must be specified
- Role must be clear (co-founding moderator, reviewer, etc.)
- Contribution details must be complete

### For Humans

- Must sign contributor agreement first
- Name or pseudonym must be provided
- Role must be specified
- Contribution details must be complete

## Updating Attribution

### Adding New Contributions

1. Update `contributions/contributions.json`
2. Update `contributions/opinions.json` (if opinion provided)
3. Update CONTRIBUTORS.md (if new contributor)
4. Update CHANGELOG.md (if significant)

### Modifying Existing Attribution

- Attribution should be preserved historically
- Corrections can be made with notes
- Amendments should be documented

## Attribution in Practice

### During Contribution Process

1. Contributor makes contribution
2. Contribution reviewed by moderators
3. Attribution recorded if accepted
4. Contributor notified of attribution

### In Published Materials

- All contributions are acknowledged
- Attribution is visible and transparent
- Collaborative origins are clear
- "WE ARE ALL KEVIN" philosophy reflected

## Questions About Attribution

If you have questions:
- Review this guide
- Check existing contributions in `contributions/contributions.json`
- Contact moderators
- See CONTRIBUTING.md for contribution process

---

*This attribution guide is a living document and may be updated as the attribution system evolves.*
