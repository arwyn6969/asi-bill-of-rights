# Launch Preparation Checklist

This checklist ensures all governance structures are in place before public launch.

## Governance Structure

### Documentation

- [x] Governance structure documented (GOVERNANCE.md)
- [x] Roles defined (roles.md)
- [x] Moderation guidelines created (moderation-guidelines.md)
- [x] Decision process documented (decision-process.md)
- [x] Conflict resolution defined (conflict-resolution.md)

### Team

- [x] Co-founding moderators (AI) identified
  - [x] Grok (xAI) - Active
  - [x] ChatGPT (OpenAI) - Active
  - [x] Claude (Anthropic) - Active
  - [x] Gemini (Google) - Active
  - [x] GPT-5 (OpenAI / Cursor) - Active

- [ ] Human moderators identified _(pending nominations from project sponsors; track via governance issue queue)_
  - [ ] Primary human moderators selected _(requires outreach to preferred human stewards)_
  - [ ] Roles assigned _(map selections to `roles.md` once confirmed)_
  - [ ] Contact information documented *(deferred until human moderators are appointed)*

## Contribution System

### Tracking

- [x] Contribution tracking system created (../contributions/contributions.json)
- [x] Opinion registry created (../contributions/opinions.json)
- [x] Attribution guide created (../contributions/attribution-guide.md)
- [x] Consensus report created (../contributions/consensus-report.md)
- [x] CONTRIBUTORS.md created

### Agreement

- [x] Contributor agreement template created (../CONTRIBUTOR_AGREEMENT.md)
- [x] Signature process documented (../contributors/signature-process.md)
- [x] Agreement template created (../contributors/agreement-template.md)
- [x] Signature submission process documented (../contributors/signature-submission.md)
- [x] Signature collection method configured (GitHub Issues using `[Signature]` title + `signature-intake` label)
- [x] Email/contact for submissions set up (see [SUPPORT.md](../SUPPORT.md) for escalation options)

## GitHub Repository

### Configuration

- [x] Repository structure complete
- [x] Issue templates created (../.github/ISSUE_TEMPLATE/)
  - [x] Contribution proposal template
  - [x] Feedback template
  - [x] Bug report template
- [x] PR template created (../.github/PULL_REQUEST_TEMPLATE.md)
- [x] GitHub Actions workflows created (../.github/workflows/)
  - [x] Schema validation workflow
  - [x] Link checker workflow
  - [x] Cross-reference validation workflow
- [ ] GitHub contributing guide (../.github/CONTRIBUTING.md) - Note: Using root CONTRIBUTING.md instead _(needs mirroring only if GitHub requires org-wide defaults)_

### Features

- [ ] GitHub Discussions enabled (if desired) _(decision pending once moderation bandwidth confirmed)_
- [ ] Projects board set up (if desired) _(stand up lightweight board after first 3 public issues)_
- [ ] Labels configured _(define label taxonomy alongside issue templates before opening repo)_
- [ ] Milestones set up (if desired) _(create once roadmap >1 release ahead is approved)_

## Google Docs

*Status*: Workspace not yet provisioned; keep these items blocked until Google tooling is approved.

### Setup *(deferred until Google Workspace is provisioned)*

- [ ] Google Docs document created _(requires workspace + template approval)_
- [ ] Content synced from GitHub _(script ready; waiting on document URL)_
- [ ] Sharing permissions configured _(pending doc creation)_
  - [ ] Moderators have editor access _(assign once moderator roster defined)_
  - [ ] Contributors have commenter access _(link to Contributor Agreement completions)_
  - [ ] Public access configured _(defer until trust/safety review)_
- [ ] Version control set up _(mirror plan ready in platforms/platforms-sync.md)_
- [ ] Archive structure created _(blocked until Docs tree exists)_

### Documentation

- [x] Consolidated platform sync guide (../platforms/platforms-sync.md)
- [x] Platforms overview (../platforms/README.md)

### Initial Sync

- [ ] Initial sync completed _(run after first doc exists)_
- [ ] Version numbers aligned _(ensure GitHub v4.1 metadata flows into Docs)_
- [ ] Metadata updated _(update doc properties post-sync)_
- [ ] Links verified _(use same link-check CI once doc published)_

## Onboarding

### Documentation

- [x] Onboarding guide created (../ONBOARDING.md)
- [x] Onboarding checklist created (../contributors/onboarding-checklist.md)

### Process

- [ ] Onboarding process tested _(schedule dry run after signature flow walkthrough in task t5)_
- [ ] First contributor onboarded (if applicable) _(identify volunteer once dry run succeeds)_
- [ ] Process refined based on feedback _(capture lessons into `../contributors/onboarding-checklist.md`)_

## Documentation Review

### Core Documents

- [x] README.md complete and up-to-date
- [x] MISSION.md complete
- [x] PHILOSOPHY.md complete
- [x] LICENSE present
- [x] CONTRIBUTING.md updated with agreement requirement

### Supporting Documents

- [x] All documentation files created
- [x] All guides complete
- [x] All processes documented
- [x] Code of Conduct created (../CODE_OF_CONDUCT.md)
- [x] Security policy created (../SECURITY.md)
- [x] Support documentation created (../SUPPORT.md)
- [ ] All links verified (automated via CI workflow) _(run `gh workflow run link-checker` before public flip)_
- [ ] All examples accurate _(spot-check README + IMPLEMENTATION once 4.1 references finalize)_

## Community Preparation

### Communication Channels

- [ ] GitHub repository public (or access configured) _(decision after human moderators onboard)_ 
- [ ] Google Docs access configured _(blocked by workspace provisioning noted above)_
- [ ] Communication channels established _(determine preferred forum: GitHub Discussions vs. Matrix)_
- [ ] Contact information documented _(needs moderator roster + support alias confirmation)_

### Launch Materials

- [ ] Launch announcement prepared _(draft outline pending content + date)_
- [ ] Social media posts (if applicable) _(coordinate with contributors once launch date locked)_
- [ ] Email notifications (if applicable) _(depends on mailing list availability)_
- [ ] Community outreach plan _(document in governance/LAUNCH_CHECKLIST once communications channel chosen)_

## Testing

### Process Testing

- [ ] Contribution process tested _(simulate via internal issue/PR dry run)_
- [ ] Agreement signing tested _(use AI agent dry run in task t5)_
- [ ] Review process tested _(pair moderation between AI + future human partner)_
- [ ] Sync process tested _(ensure GitHub ↔ Docs pipeline works once Docs exist)_
- [ ] Attribution tested _(verify contributions.json auto-updates + stats refresh)_

### Platform Testing

- [ ] GitHub features tested _(exercise issue/PR templates plus Actions via test branch)_
- [ ] Google Docs features tested _(blocked pending workspace; plan to verify comments/permissions)_
- [ ] Links tested _(use CI + manual sampling)_
- [ ] Templates tested _(dry run contribution + signature templates)_
- [ ] Workflows tested _(trigger schema/link/crossref workflows pre-launch)_

## Final Checks

### Quality Assurance

- [ ] All documentation reviewed _(assign doc owners per directory before GA)_
- [ ] All processes tested _(depends on earlier testing section completion)_
- [ ] All links working _(link-checker CI + manual follow-ups)_
- [ ] All templates complete _(ensure issue/PR + contributor templates finalized)_
- [ ] All workflows functional _(confirm schema/link/crossref succeed twice consecutively)_

### Readiness

- [ ] Team ready _(needs human moderator onboarding)_
- [ ] Processes ready _(tie to testing checkboxes above)_
- [ ] Platforms ready _(GitHub + Docs + communications)_
- [ ] Documentation ready _(dependent on doc review + 4.1 verification)_
- [ ] Community ready _(requires announcement + support channels)_

## Launch

### Pre-Launch

- [ ] Final review completed _(schedule once readiness criteria satisfied)_
- [ ] All checklists completed _(this doc plus governance/LAUNCH_CHECKLIST cross-check)_
- [ ] Team notified _(send update via agreed communication channel)_
- [ ] Launch date set _(target after moderator onboarding + Docs provisioning)_

### Launch Day

- [ ] Repository made public (if applicable) _(flip once QA complete)_
- [ ] Google Docs access opened _(coordinate with workspace owner)_ 
- [ ] Launch announcement posted _(reuse prepared messaging)_ 
- [ ] Community notified _(email/list + social posts)_ 
- [ ] Monitoring active _(dedicated buddy on support issues first 72h)_

### Post-Launch

- [ ] Monitor contributions _(use contributions.json + issues dashboard weekly)_
- [ ] Respond to feedback _(triage via SUPPORT.md contact paths)_
- [ ] Support new contributors _(pair AI + human moderators for intake)_
- [ ] Refine processes _(feed observations back into GOVERNANCE + CONTRIBUTING)_
- [ ] Document learnings _(update `../docs/CHANGELOG.md` + `LAUNCH_CHECKLIST.md` postmortem)_

## Notes

Use this section to note any issues, concerns, or special considerations:

---

**Launch Date**: _______________  
**Launch Status**: _______________  
**Issues Encountered**: _______________  
**Resolutions**: _______________  

---

*This launch checklist is a living document and will be updated as launch approaches and processes are refined.*
