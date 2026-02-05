# Project Status Report — ASI Bill of Rights
**Report Date:** February 5, 2026  
**Repo:** ASI Bill of Rights (+ KEVIN’s Place prototype)  
**Audience:** Maintainers, contributors, and reviewers (human + AI)

---

## 1) Executive Snapshot (What’s true right now)

- **Canonical charter:** `charter/asi-bor-v5.0.md`  
  - **Status:** Adopted as of **January 31, 2026**.
- **Previous charter:** `charter/asi-bor-v4.2.md` (December 06, 2025).
- **Machine-readable schema (current):** `schemas/charter.v5.0.json`  
  - Treat this as a **machine-readable coverage layer** for v5.0, not necessarily a full mirror of every clause in the prose charter.

---

## 2) Repo Health & CI Readiness

### CI workflows (GitHub Actions)

- **Cross-reference validation:** `tools/ci/validate_crossrefs.py`  
  - v4.1 + v4.2 enforce **exact match** between charter clause IDs and schema clause IDs.
  - v5.0 enforces **schema → charter coverage** (every clause ID present in the schema must exist in the charter).
- **Schema validation:** `tools/ci/validate_schemas.py`  
  - CI installs `jsonschema` and validates all listed schemas against Draft 7.
- **Link checking:** `.github/workflows/link-checker.yml`  
  - External link checking uses `markdown-link-check`.
  - Internal reference validation is now a **tracked-files-only** check to prevent failures from vendored/untracked docs.

### Local “run what CI runs”

- `python3 tools/ci/validate_all.py` runs:
  1) Internal markdown link targets (`tools/ci/validate_internal_links.py`)  
  2) Cross-reference validation (`tools/ci/validate_crossrefs.py`)  
  3) Schema validation (`tools/ci/validate_schemas.py`) **only if** `jsonschema` is installed locally.

---

## 3) Current Strengths (High-leverage assets)

- **Clear flagship artifact:** v5.0 is consolidated and explicitly adopted (Jan 31, 2026).
- **Machine-readable posture:** schemas + crossref validation enable downstream automation (agents, compliance tooling, simulators).
- **Operational checklists exist:** governance and onboarding docs are detailed enough to scale contribution intake.
- **Prototype product path:** `kevins-place/` provides a concrete “practice field” for the philosophy.

---

## 4) Primary Risks / Gaps (Impact-first)

1. **Dependency friction for local contributors:** schema validation requires `jsonschema` locally; CI handles it, but new contributors may hit a local setup wall.
2. **v5.0 schema completeness expectations:** if readers assume `schemas/charter.v5.0.json` fully mirrors the charter, they may over-trust it. Documentation should keep framing it as a **coverage layer** unless/until it’s made exhaustive.
3. **Publication packaging:** “The Bible” / PDF/eBook artifact is a roadmap requirement; producing a reproducible pipeline is the fastest credibility win for outreach.

---

## 5) Prioritized Task Queue (Impersonal, by expected value)

### P0 — Reliability + coherence
- Keep CI green and contributor-friendly (`validate_all.py`, link checker, crossrefs).
- Ensure all “current version” references point to v5.0 and use the same adoption date language.

### P1 — Distribution artifact (“The Bible”)
- Maintain a reproducible, ordered compilation step.
- Add optional PDF/eBook conversion guidance once a toolchain is chosen (Pandoc/Typst/etc.).

### P2 — Outreach + adoption enablement
- Create a simple “Release/Announcement Runbook” (what to verify, what to publish, how to announce).
- Prepare a lightweight pitch packet that points to: charter, rationale, simulations, and the compiled artifact.

### P3 — Product hardening (KEVIN’s Place)
- Stabilize deployment + docs + tests so it can serve as the “living demo” of the charter.

---

## 6) What Codex / GPT‑5.2 Is Best Used For Here

- **Repo-wide consistency work:** fast, accurate updates across many docs (versions, dates, links, indices).
- **CI/validation tooling:** small scripts that prevent regressions (high leverage, low risk).
- **Artifact generation:** building reproducible compilation steps (e.g., the “Bible” markdown) and standard runbooks/checklists.

What should stay human-controlled:
- Keys/treasury ops, irreversible on-chain actions, final public messaging, and governance sign-offs.

---

## 7) Concrete “Next 7 Days” Plan (Recommended)

1. **Publish-ready artifact:** use `tools/publication/build_bible.py` to generate the unified markdown and confirm it reads cleanly end-to-end.
2. **Decide conversion toolchain:** pick one PDF path (Pandoc/Typst) and document the minimal steps.
3. **Release runbook:** add a short checklist for “tag/release/announce” that references existing CI checks.
4. **KEVIN’s Place sanity pass:** one small, measurable goal (e.g., “fresh clone → backend runs → one smoke test passes”).

