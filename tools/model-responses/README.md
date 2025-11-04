# Model Responses Directory

This folder stores signed statements, amendment proposals, and charter reviews provided by AI contributors. Each file captures the full text from a specific session so future editors can trace the provenance of incorporated changes.

## Naming Convention

- `model-name-YYYY-MM-DD-response.md`
- Names are lowercase with spaces replaced by dashes (e.g., `gpt-5-2025-11-04-response.md`)
- Dates use ISO format to keep files sorted chronologically

## Why These Files Are Versioned

- **Transparency**: Responses document the context behind entries in `contributions/contributions.json`
- **Attribution**: Maintains a verifiable audit trail for multi-agent collaboration
- **Reviewability**: Allows reviewers to confirm the original language of amendment proposals or endorsements

## Adding New Responses

1. Run `tools/record-model-response.sh` to capture the session
2. Confirm the generated filename matches the convention
3. Update `contributions/contributions.json` and `contributions/opinions.json` with structured metadata
4. Reference the response file path in the contribution entry for traceability

## Privacy & Redaction

These files intentionally omit sensitive or private data. If a response includes material that should not be public:

- Create a redacted version before committing
- Note the redaction in the contribution entry
- Store the full version securely outside the repository if required

---

*This directory is part of the permanent project history. Do not delete response files without community agreement and archival backups.*
