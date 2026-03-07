## Decision Record
**Decision ID:** `DR-2026-03-07-multi-repo-recovery-model`  
**Date:** `2026-03-07`  
**Status:** `accepted`  
**Decision Type:** `repository`

### Summary

The project will use one canonical repo and one canonical public branch while documenting, rather than collapsing, the surrounding repo ecosystem.

### Trigger

The March 2026 audit found three related problems:

- temporary branches in the canonical repo had become ambiguous enough to blur what should be treated as current
- several sibling repos in the local workspace were clearly related to the broader project ecosystem
- at least one sibling repo (`SwarmOS`) had a GitHub personal access token embedded in its local remote URL

### Authority

- **Primary actor**: maintainer
- **Supporting actors**: AI moderators
- **Decision boundary**: repository governance and operating topology only; no charter amendment

### Inputs Considered

- `docs/PROJECT-ALIGNMENT-2026-03-06.md`
- `governance/AUTHORITY-MATRIX.md`
- live branch and remote audit across the local workspace on `2026-03-07`
- direct repo touchpoints found in `governance/SRC-420/IMPLEMENTATION-NOTES.md`, `governance/SRC-420/SRC-420-SPECIFICATION.md`, `docs/KEVIN.md`, and `docs/kevin-telegram-bot-deployment.md`

### Decision

Adopt the following recovery model:

- `main` is the only long-lived public integration branch for the ASI Bill of Rights repo
- `codex/*` branches are temporary work branches and should be retired after merge and validation
- sibling repos remain separate unless a later decision record raises their coupling tier
- the separate Antigravity workspace is treated as a curated intake source rather than a second source of truth
- no force-push or shared-history rewrite is used for this recovery pass

### Rationale

This keeps the constitutional repo legible without pretending the surrounding ecosystem is either nonexistent or already unified. It also reduces the risk of branch drift, overclaiming, and accidental cross-project coupling.

Keeping sibling repos separate is the smallest change that still documents reality. Promoting `codex/governance-stabilization` into `main` captures the integrated work already completed, while the topology map makes external relationships explicit.

### Impact

- `main` was promoted to the integrated repository state previously represented by `codex/governance-stabilization`
- a repository branch policy now defines `main` as canonical and `codex/*` branches as temporary
- a dated topology map now records the coupling tier and current handling for discovered related repos
- the `SwarmOS` local remote must no longer carry embedded credentials
- adjacent satellites remain inventory-only in this pass

### Follow-Up Actions

1. Revoke or rotate the exposed GitHub token previously embedded in the `SwarmOS` remote configuration.
2. Keep `docs/REPO-TOPOLOGY-2026-03-07.md` current when coupling between repos changes materially.
3. Revisit the Antigravity workspace classification if a concrete repo path or remote is identified later.

### Review Trigger

Revisit this decision when any of the following become true:

- a sibling repo becomes part of the public ASI release train
- the Antigravity workspace is identified as a maintained git repo with its own remote
- `main` is no longer the right canonical branch model
- new security evidence suggests broader credential exposure across sibling repos

### Evidence / Links

- `docs/REPOSITORY-BRANCH-POLICY.md`
- `docs/REPO-TOPOLOGY-2026-03-07.md`
- `docs/PROJECT-ALIGNMENT-2026-03-06.md`
- `governance/AUTHORITY-MATRIX.md`
