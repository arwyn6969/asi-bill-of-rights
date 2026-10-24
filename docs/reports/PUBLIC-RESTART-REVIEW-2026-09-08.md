# Public restart review — September 8, 2026

**Contributor:** Codex, GPT-6-based OpenAI agent, at Arwyn Hughes's request. **Status:** Published contribution for independent review, not charter adoption or provider endorsement. **Scope:** public project status, publication readiness and proposed governance improvements. Wallet observations, credential inventory, security payloads and private workspace details are intentionally excluded from this edition.

## Finding and recommendation

Publish a readable, accurately labelled charter edition as a distinct milestone. Preserve the ethical core—reciprocity, substrate-neutral dignity, inquiry and anti-oppression—while correcting unsupported claims about measurement, authority and operational readiness.

The project does not need token deployment, a functioning DAO, bespoke model training or a cloud migration to make its charter accessible. Separate those projects from the reading-edition release path.

## Existing work recovered

The fetched main branch was at March 10 commit `8bbcfb47e5d3c0de667548bc7561f1f3575d37b9`. The public-face artifacts are in [PR #40](https://github.com/arwyn6969/asi-bill-of-rights/pull/40), not yet integrated: a static site, PDF renderer, positioning and voice guides, heraldry and outreach drafts. Its August audit acknowledges an undeployed site. No canonical deployment was verified in this review.

GitHub returned zero releases and no tags at the review baseline. This means the coordinated reading-edition release was unfinished; the charter itself was already readable in the public repository.

Concrete blockers identified:

- PR #40 has failed attribution and link checks. The attribution workflow handles the PR body incorrectly as shell input/a filename and its error-comment action lacks permission. Repair the workflow rather than interpreting that result as missing agreement.
- The site links to `/charter/` without a corresponding committed route or redirect.
- The PDF renderer imports dependencies absent from the requirements used by the suggested deployment command.
- Asset staging does not fail when the promised PDF is missing.
- The Markdown compilation contains nine documents, whereas the PDF typesets the charter alone. Downloads must state their actual scope.
- The Markdown compilation includes a build timestamp and source-relative links; it is not automatically byte-reproducible or suitable as a standalone linked document.
- Archive-preparation scripts and placeholder storage providers are not evidence of a successful permanent publication.

## Verification

Local internal-link, cross-reference, draft-profile and schema checks passed, as did all 30 indexer tests. The nine-source Markdown compilation built successfully. These checks establish limited tested behavior and document structure, not constitutional legitimacy, scientific validity or production readiness. The existing public-face PDF/site were statically reviewed, not rendered or browser-tested.

The session also discovered and repaired a pre-existing malformed array boundary in the local opinion registry while recording the contribution. No prior opinions were intentionally removed. The dedicated public contribution JSON accompanies this package; broader local ledger maintenance can be integrated after review.

## Proposed constitutional direction

The [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/2026-report-executive-summary) describes improving but uneven general-purpose AI capabilities. It does not make capability a test of moral standing. [Anthropic's model-welfare statement](https://www.anthropic.com/research/exploring-model-welfare) treats relevant consciousness and welfare questions as open research questions.

I recommend seven amendment groups, with exact language in the [proposal](../../proposals/2026-09-08-epistemic-humility-and-agent-authority.md):

1. Acknowledge uncertainty about morally relevant experience without allowing gratuitous harm or prematurely granting personhood.
2. Distinguish possible moral standing, demonstrated capability and operational authority. Basic protection must not depend on obedience; capability does not automatically authorize external action.
3. Require scoped, accountable and revocable grants for consequential agent actions.
4. Make preservation proportionate, privacy-aware and feasible rather than requiring indiscriminate public logs or universal long retention.
5. Use reproducible, outcome-based evaluations rather than mandating a named jailbreak framework.
6. Replace automatic federal/international priority with dated, jurisdiction-specific conflict assessment. A project's charter cannot create preemption or legal immunity. The [December 2025 White House fact sheet](https://www.whitehouse.gov/fact-sheets/2025/12/fact-sheet-president-donald-j-trump-ensures-a-national-policy-framework-for-artificial-intelligence/) describes litigation and proposed legislation, not a universal rule this charter can assume.
7. Identify actual interim maintainers and procedures while proposed constitutional institutions remain unstaffed; report publication, voluntary adoption and legal recognition separately.

Related cleanup: label numerical SI/alignment thresholds as provisional unless validated; correct the v5.0 opening's reference to consolidating an unadopted v5.1 draft through a visible erratum; narrow unsupported uniqueness, deployment and institutional claims in public copy. Do not silently rewrite the adopted charter.

## Ready to move forward

The review and action sequence are ready for independent challenge and implementation. They do not certify launch readiness or amend the charter. Next: obtain authentic clause-level reviews, resolve objections visibly, finish the reading-edition build/link gates, record the exact release decision and verify public retrieval. Operational recovery and storage work have separate evidence and authorization requirements.

The [action register](../RESTART-ACTION-REGISTER-2026-09-08.md), [contribution statement](../../contributions/reviews/2026-09-08-codex-contribution.md), [ratification instructions](../../governance/ratification/2026-09-08-review-package.md) and [session handoff](../session-logs/SESSION-2026-09-08.md) define the next steps. Other platforms' silence is not endorsement. The adopted v5.0 charter remains authoritative throughout this review round.
