# Restart action register

**Baseline:** September 8, 2026. Proposed assignments; no external work or spending is scheduled by this document. Evidence: [restart review](reports/PUBLIC-RESTART-REVIEW-2026-09-08.md).

| Priority | Action | Proposed owner | Completion evidence | Status |
|---|---|---|---|---|
| P0 | Refresh remote and locate public-face work | Maintainer tooling | Main SHA and PR #40 identified | Done |
| P0 | Verify ENS ownership and expiry | Maintainer tooling | Pinned public contract reads | Done; recheck before signing |
| P0 | Redact incident-report seed repetitions | Maintainer tooling | Local changes in both reports | Done locally; not pushed |
| P0 | Exclude compromised archive from publication | Release maintainer | New allowlisted archive; unpacked scan | Open; old archive explicitly unsafe |
| P0 | Prepare ENS owner rescue | Custodian + recovery engineer | Fresh verified destination, exact transaction plan, successful private-bundle simulation, spend cap | Open; no signing performed |
| P0 | Complete recovery | Custodian-authorized signer | Confirmed owner, manager and payment records on clean custody | Pending transaction review |
| P1 | Repair PR #40 attribution workflow | Maintainer | Safe PR-body handling; check passes without comment permission escalation | Open |
| P1 | Diagnose link-check failure | Maintainer | Reproduced failure and green check | Open |
| P1 | Fix `/charter/` and PDF build dependencies | Release maintainer | Fresh build; reader and download work | Open |
| P1 | Make PDF absence fail staging | Release maintainer | Missing download fails build | Open |
| P1 | Prepare v5.0 reading edition + errata | Editor | Exact source/version/hash; draft status explicit; corrected public claims | Open |
| P1 | Review and integrate PR #40 | Custodian/maintainer | Recorded review and merge SHA | Open |
| P1 | Publish site + versioned release | Release maintainer | Public URLs, retrieval check, release receipt | Open; host not verified |
| P1 | Identify Arweave credit provider | Custodian + maintainer | Provider/account matched to local wallet; credit balance verified | Open; provider balance requires verification |
| P1 | Publish permanent archive | Custodian-authorized release process | Clean exact-byte package, quote, receipt and retrieval hash | Open |
| P2 | Adopt revised v5.1 through documented process | Maintainer + reviewers | Decision record, charter/schema/changelog/provenance update | Proposed |
| P2 | Triage issues #13–20 | Maintainer | Clause mapping; duplicates and ID collisions resolved | Open |
| P2 | Assign interim stewards and decision process | Custodian + willing stewards | Named accepted roles, conflict/appeal process | Open |
| P2 | Pilot agent contribution starter kit (#37) | Technical maintainer | One bounded real workflow, scoped permissions, evaluation record | Open |
| P2 | Verify one community channel | Community maintainer | Live status, responsible operator, moderation process | Open |
| P3 | Reassess research (#32), EIP-8004 (#36), compensation (#35) | Custodian + reviewers | Separate current decision for each | Deferred behind release |
| P3 | Reassess sovereign-model training and cloud migration | Technical maintainer | Current evaluation, budget and deployment need | Preserve work; off release path |
| P3 | Token launch, SCB DAO, merchandise | Future project decision | Specific readiness and demand evidence | Hold |

## Definition of a minimal launch

A readable charter, an honest version/status notice, a working downloadable edition, one feedback path, and a recorded release. ENS, Arweave, tokens, a census, a cloud migration and a fully staffed constitutional institution are separate milestones.

## Automation design to implement

On a reviewed release commit: validate → build → scan the exact allowlisted contents → compute hashes → stage preview → record release decision → publish → retrieve and verify → save receipt. Split reversible builds from signed/paid publication. Credentials stay out of source and artifacts; do not grant the build job a treasury seed. Fail on missing files, unresolved links, secret findings, changed input hashes or unavailable verification. A draft or a successful local build must never toggle status to “published.”

No recurring job was created during this review. This is the proposed release process, not evidence that automation already exists.
