# Repository Branch Policy

**Status:** Active as of 2026-03-07

## Purpose

This policy defines how repository branches and sibling workspaces should be handled after the March 2026 multi-repo recovery pass.

It exists to prevent ambiguity about:

- which branch is canonical
- which branches are temporary
- how sibling repositories relate to this repo
- how local-only workspaces such as Antigravity should be imported

## Canonical Rule

- `main` is the only long-lived public integration branch for the ASI Bill of Rights repository.
- The canonical repository remains `/Users/arwynhughes/Documents/ASI BILL OF RIGHTS`.
- Repository-level truth still follows the source order defined in `docs/PROJECT-ALIGNMENT-2026-03-06.md`.

## Temporary Branch Rules

- `codex/*` branches are temporary implementation branches tied to one bounded workstream.
- Temporary branches should be deleted locally and remotely after:
  - their work is integrated into `main`
  - validation confirms they contain no unique unintegrated commits
  - the resulting `main` state has been pushed successfully
- Temporary branches should not become substitute sources of truth for repository posture.

## Shared-History Safety

- Do not rewrite shared remote history for this repo as part of ordinary stabilization work.
- Prefer fast-forward promotion where possible.
- If fast-forward is no longer possible, create a new recovery branch from the latest `origin/main`, merge there, validate, and then merge back without force-push.

## External Repository Rules

- Sibling repositories keep their own release trains, default branches, and local branch policies unless explicitly documented otherwise.
- Being referenced in ASI Bill of Rights docs does not automatically make a sibling repo part of the ASI release train.
- Cross-repo relationships should be recorded in `docs/REPO-TOPOLOGY-2026-03-07.md`.

## Workspace Intake Rules

- Non-repo workspaces or local-only sources, including the separate Antigravity workspace described during the audit, are intake sources rather than canonical repos.
- Import from those workspaces must be curated by artifact:
  - identify the source path
  - record the owner or model attribution
  - choose a canonical destination in this repo
  - classify each item as import, defer, or archive
- Do not bulk-copy an external workspace into this repo without a separate decision record.

## Dirty-State Handling

- Preserve local feature work in sibling repos.
- Separate runtime state from source changes before using dirty-state as a signal for cleanup decisions.
- Runtime artifacts such as local databases should not silently define product scope or repo coupling.

## Retirement Procedure For Temporary Branches

1. Promote validated work to `main` without rewriting shared history.
2. Verify the temporary branch contributes no unique unintegrated commits.
3. Push `main`.
4. Delete the temporary branch locally and remotely.
5. Record the decision or topology update if the cleanup changes repository posture.
