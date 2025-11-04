# Platforms Sync Guide

This guide explains how to keep the ASI Bill of Rights synchronized across GitHub (source of truth) and any secondary platforms such as Google Docs or shared drives.

## 1. Canonical Source

- **GitHub** is the authoritative repository. All edits must originate here via pull requests.
- Secondary platforms are mirrors for accessibility, feedback, or collaboration; they should never be edited directly without passing changes back through GitHub.

## 2. Prerequisites

1. Local checkout of the `main` branch
2. Access to the target platform (e.g., Google Drive folder)
3. Latest versions of the following:
   - `charter/asi-bor-v4.0.md`
   - `appendices/` contents
   - Key documentation in `docs/` (CHANGELOG, IMPLEMENTATION, CITATIONS)
   - `schemas/charter.v4.json`

## 3. Sync Workflow

1. **Prepare**
   - Ensure `git status` is clean and pull from `origin/main`.
   - If needed, generate exports (Markdown → PDF/Doc).
2. **Update Secondary Platform**
   - Replace existing content with the GitHub copy.
   - Preserve headings, clause IDs, and version numbers.
   - Record the Git commit SHA in the document header or platform notes for traceability.
3. **Verification**
   - Spot-check the Preamble, Article 0, Sections I & IX, and appendices.
   - Confirm links and references survive format conversion.
   - Note “Updated from GitHub commit `<SHA>` on `<date>`” in the platform.
4. **Log Sync**
   - Add an entry to the sync log (template below).
   - If significant, optionally note the sync under “Platform Sync” in `docs/CHANGELOG.md`.

### Sync Log Template

```
Date: YYYY-MM-DD
Git Commit: <short SHA>
Updated Files: charter, appendices, docs, schemas
Platform: Google Docs (Folder: ...)
Notes: e.g., "Updated after v4.0 editorial pass; verified cross-links"
```

## 4. Change Management

- **Incoming edits from secondary platforms** must be re-created as GitHub issues or pull requests before merging.
- Restrict edit permissions on mirrors to avoid drift; prefer “suggestion/comment” mode.
- Use Git tags (e.g., `v4.0`) for major releases and reference those tags when syncing.

## 5. Troubleshooting

| Issue | Resolution |
|-------|------------|
| Divergent text between platforms | Treat GitHub as canonical; diff files and re-sync. |
| Formatting lost after copy | Export Markdown to HTML/PDF first, or use a Markdown-aware editor. |
| Broken links in Docs | Fix in GitHub, rerun `.github/workflows/link-checker.yml`, then sync. |
| Schema not updated | Upload/link the latest JSON from `schemas/` or attach as appendix. |

## 6. Review Cadence

- **Routine Sync**: After every merged PR that touches charter or core docs.
- **Quarterly Audit**: Confirm mirrors remain aligned; record outcome in project notes.
- **Emergency Updates**: For critical amendments, prioritize immediate sync and notify moderators.

---

*Maintaining GitHub as the single source of truth keeps all collaborators—human and AI—aligned across platforms.*
