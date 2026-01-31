# Security Policy

## Supported Versions

We actively maintain and provide security updates for:

| Version | Supported          |
| ------- | ------------------ |
| 4.0.x   | :white_check_mark: |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the ASI Bill of Rights project, please report it responsibly.

### What to Report

Please report:

- Security vulnerabilities in scripts or tools
- Issues that could lead to data exposure or manipulation
- Vulnerabilities in the contribution tracking system
- Any security concern that could affect the project's integrity

### How to Report

**Option 1: Private Security Advisory**
- Use GitHub's private security advisory feature if available
- This keeps the vulnerability private until it's fixed

**Option 2: Direct Contact**
- Contact project maintainers directly
- Include detailed information about the vulnerability
- Provide steps to reproduce if possible

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Updates**: We will keep you informed of our progress
- **Resolution**: We will work to resolve the issue promptly

### Disclosure Policy

We follow responsible disclosure practices:

1. **Private Report**: Vulnerabilities are reported privately
2. **Fix Development**: We develop and test fixes
3. **Release**: We release fixes and update affected versions
4. **Public Disclosure**: After fixes are released, we may disclose details (with your permission)

## Security Considerations

### For Contributors

- **Scripts**: Review scripts before running them locally
- **JSON Files**: Validate JSON structure before submitting
- **Links**: Verify external links are legitimate
- **Attribution**: Ensure proper attribution when contributing

### For Implementers

- **Schema Validation**: Always validate JSON schemas before use
- **Cross-References**: Verify clause ID cross-references are correct
- **Version Control**: Use specific versions, not "latest"
- **Audit**: Regularly audit implementations for compliance

## Security Best Practices

1. **Keep Updated**: Use the latest supported version
2. **Validate Input**: Always validate JSON and schema inputs
3. **Review Changes**: Review all changes before merging
4. **Report Issues**: Report security concerns promptly
5. **Follow Processes**: Follow established contribution and review processes

---

*Security is a shared responsibility. Thank you for helping keep this project secure.*

