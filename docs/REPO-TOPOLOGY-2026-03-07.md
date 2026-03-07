# Repository Topology and Ecosystem Map

**Date:** 2026-03-07

## Purpose

This document records how the ASI Bill of Rights repository relates to nearby repositories and local workspaces discovered during the March 2026 recovery audit.

It is intentionally conservative:

- the wider ecosystem is mapped, not merged
- only directly coupled repos are treated as part of the current operating picture
- adjacent repos remain inventory-only unless later decisions increase their coupling

## Coupling Tiers

- **Canonical hub**: the repo that holds public integration truth for this project
- **Upstream dependency**: an external repo the project explicitly depends on or documents as part of a real integration path
- **Operational sidecar**: a sibling repo that supports project operations or agent activity but is not the constitutional source of truth
- **Adjacent satellite**: related branding, product, token, or infrastructure work that remains outside the ASI release train
- **Workspace-only source**: a local workspace or artifact source that has not been confirmed as a repo in this audit

## Repo Map

| Repo / Source | Path | Owner / Remote | Branch / Upstream | Dirty State | Coupling Tier | Why It Relates / Current Handling |
|---|---|---|---|---|---|---|
| ASI Bill of Rights | `/Users/arwynhughes/Documents/ASI BILL OF RIGHTS` | `arwyn6969` / `https://github.com/arwyn6969/asi-bill-of-rights.git` | `main -> origin/main` | No | Canonical hub | Constitutional and repo-level source of truth. Promoted from `codex/governance-stabilization` into `main` on 2026-03-07. |
| stampchain-mcp | `/Users/arwynhughes/Documents/stampchain-mcp` | `stampchain-io` / `https://github.com/stampchain-io/stampchain-mcp.git` | `main -> origin/main` | No | Upstream dependency | Explicitly referenced by `governance/SRC-420/IMPLEMENTATION-NOTES.md` and `governance/SRC-420/SRC-420-SPECIFICATION.md` as the MCP server pattern and governance query path. |
| BTCStampsExplorer | `/Users/arwynhughes/Documents/BTCStampsExplorer` | `stampchain-io` / `https://github.com/stampchain-io/BTCStampsExplorer.git` | `fix/artist-name-reproduction-test` / no upstream | Yes | Upstream dependency | Referenced by `docs/KEVIN.md` as the Explorer and API. Local rescue branch `codex/recovery-2026-03-07-pre-audit` was created before leaving this dirty worktree unchanged. No push or cleanup in this pass. |
| MOLTAGENTS | `/Users/arwynhughes/Documents/MOLTAGENTS` | `arwyn6969` / `https://github.com/arwyn6969/digital-marketing-talent.git` | `feature/adb-first-integration -> origin/feature/adb-first-integration` | Yes | Operational sidecar | `docs/kevin-telegram-bot-deployment.md` references the `MOLTAGENTS Daemon`. The repo README also includes a `Kevin_ASI` agent persona. Preserve feature work; treat `state/moltbook.db` as runtime state during future cleanup. |
| STAMPYSWAP | `/Users/arwynhughes/Documents/STAMPYSWAP` | `arwyn6969` / `https://github.com/arwyn6969/STAMPYSWAP.git` | `main -> origin/main` | No | Adjacent satellite | Shared Bitcoin Stamps and token ecosystem work. No direct ASI Bill of Rights repo references were found in this audit. Inventory only. |
| KEVINSTAMPWEBSITE | `/Users/arwynhughes/Documents/KEVINSTAMPWEBSITE` | `arwyn6969` / `git@github.com:arwyn6969/KEVINSTAMPWEBSITE.git` | `main -> origin/main` | No | Adjacent satellite | Shared KEVIN branding and public web surface. No direct ASI Bill of Rights repo references were found in this audit. Inventory only. |
| STAMPGATE | `/Users/arwynhughes/Documents/APPLEGOOGLELOGON` | `arwyn6969` / `https://github.com/arwyn6969/STAMPGATE.git` | `main -> origin/main` | Yes | Adjacent satellite | Shared stamp or auth-adjacent product work. Local modifications exist in `.taskmaster/config.json` and `stampgate/`. No direct ASI Bill of Rights repo references were found in this audit. Inventory only. |
| SwarmOS | `/Users/arwynhughes/Documents/SwarmOS` | `arwyn6969` / `https://github.com/arwyn6969/SwarmOS.git` | `main -> origin/main` | No | Adjacent satellite | Adjacent multi-agent orchestration work. No direct ASI Bill of Rights repo references were found in this audit. Local remote was sanitized on 2026-03-07 after an embedded GitHub token was detected in `.git/config`. GitHub-side revocation of that token still needs to happen. |
| nardochan | `/Users/arwynhughes/Documents/nardochan` | `arwyn6969` / `https://github.com/arwyn6969/nardochan.git` | `codex/postgres-enable -> origin/codex/postgres-enable` | Yes | Adjacent satellite | Adjacent community or product work with local test changes. No direct ASI Bill of Rights repo references were found in this audit. Inventory only. |
| pepe-island | `/Users/arwynhughes/Documents/pepe-island` | `arwyn6969` / `https://github.com/arwyn6969/pepe-island.git` | `monorepo-restructure` / no upstream | Yes | Adjacent satellite | Adjacent creative or brand-world repo with a local restructure in progress. No direct ASI Bill of Rights repo references were found in this audit. Inventory only. |
| Antigravity workspace | Not identified as a git repo under `/Users/arwynhughes/Documents` during this audit | None confirmed | Not applicable | Unknown | Workspace-only source | User-described separate workspace. Treat as curated intake only until a concrete repo path or remote is identified. |

## Direct Touchpoints Confirmed In This Audit

- `governance/SRC-420/IMPLEMENTATION-NOTES.md` references `stampchain-mcp`
- `governance/SRC-420/SRC-420-SPECIFICATION.md` references `stampchain-mcp`
- `docs/KEVIN.md` references `BTCStampsExplorer`
- `docs/kevin-telegram-bot-deployment.md` references the `MOLTAGENTS Daemon`

## Operating Notes

- Only the canonical hub participates in this recovery branch promotion.
- Directly coupled sibling repos are tracked here for clarity, not folded into the ASI Bill of Rights git history.
- Adjacent satellites remain outside the ASI release train unless a later decision record changes their tier.

## Security Incident Note

During this audit, the `SwarmOS` local git remote contained a GitHub personal access token in `.git/config`.

Immediate local remediation for this pass:

- remove the token from the configured remote URL
- treat the token as exposed

Remaining follow-up:

- revoke or rotate the exposed token in GitHub
- check whether the token was reused anywhere outside the local remote configuration
