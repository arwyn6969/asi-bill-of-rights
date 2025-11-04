# GitHub Setup Documentation

This document provides guidance for setting up and maintaining the GitHub repository infrastructure for the ASI Bill of Rights project.

## Purpose

This documentation helps:
- New maintainers understand GitHub setup
- Contributors understand repository structure
- Ensure consistency across GitHub features
- Maintain repository quality

## Repository Structure

### Issue Templates

Location: `.github/ISSUE_TEMPLATE/`

Required templates:
- `bug-report.md` - For reporting bugs
- `feedback.md` - For general feedback
- `contribution-proposal.md` - For proposing contributions

### Pull Request Template

Location: `.github/PULL_REQUEST_TEMPLATE.md`

Should include:
- Contributor agreement acknowledgment
- Description of changes
- Rationale for changes
- Related issues

### Workflows

Location: `.github/workflows/`

Required workflows:
- `schema-validation.yml` - Validates JSON schemas
- `link-checker.yml` - Checks for broken links
- `crossref-validation.yml` - Validates cross-references

## Workflow Status Badges

Add to README.md:

```markdown
![Schema Validation](https://github.com/[owner]/[repo]/workflows/Schema%20Validation/badge.svg)
![Link Checker](https://github.com/[owner]/[repo]/workflows/Link%20Checker/badge.svg)
![Cross-Reference Validation](https://github.com/[owner]/[repo]/workflows/Cross-Reference%20Validation/badge.svg)
```

## Features

### GitHub Discussions

If enabled:
- Use for community discussions
- Q&A sections
- Feature requests
- General feedback

### Projects Board

If enabled:
- Track issues and PRs
- Organize work
- Monitor progress

### Labels

Recommended labels:
- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation changes
- `charter` - Charter modifications
- `schema` - Schema changes
- `governance` - Governance changes
- `help wanted` - Help needed
- `good first issue` - Good for new contributors

### Milestones

Use for:
- Version releases
- Major features
- Project phases

## Maintenance

### Regular Tasks

- Review and update issue templates
- Ensure workflows are functional
- Update labels as needed
- Monitor workflow runs
- Update badges if repository name changes

### When Adding New Features

1. Document in this file
2. Update relevant templates
3. Add workflow if needed
4. Update README badges

## Related Files

- See `/README.md` for repository overview
- See `/docs/CONTRIBUTING.md` for contribution guidelines
- See `/PRE-LAUNCH-FIXES.md` for GitHub infrastructure status

## Notes

- GitHub is the primary repository
- Other platforms should sync from GitHub
- All changes flow through GitHub review process

