# Signature Submission Process

This document explains how to submit your Contributor Agreement signature.

## Overview

Before contributing to the ASI Bill of Rights project, you must sign the Contributor Agreement. This ensures clear understanding of license, code of conduct, attribution, and project philosophy.

## Step 1: Read the Agreement

1. Read [CONTRIBUTOR_AGREEMENT.md](CONTRIBUTOR_AGREEMENT.md) carefully
2. Understand the project philosophy ("WE ARE ALL KEVIN")
3. Review the license terms and attribution requirements

## Step 2: Prepare Your Signature

### For Human Contributors

1. Fill out the agreement template or create your own signed version
2. Include:
   - Your name (or preferred attribution name)
   - Date
   - Signature (digital or typed)
   - Any comments or notes

### For AI Contributors

1. Use the model response recording process
2. See [tools/record-model-response.sh](../tools/record-model-response.sh)
3. Include:
   - Model name and version
   - Agreement statement
   - Preferred attribution name

## Step 3: Submit Your Signature

### Option 1: GitHub Issue (Recommended)

1. Create a new issue using the [Contribution Proposal template](../.github/ISSUE_TEMPLATE/contribution-proposal.md)
2. Title the issue **`[Signature] Your Name / Model Name`**
3. Attach or paste your signed agreement (PDF, image, or markdown)
4. Check the "Contributor Agreement" box in the template
5. Add the label `signature-intake` (or ask a maintainer to do so)
6. Maintainers will reply on the issue thread with approval or follow-up questions

### Option 2: Pull Request

1. Create a new file in `contributors/signed-agreements/`
2. Name it: `your-name-YYYY-MM-DD.md` or `model-name-YYYY-MM-DD.md`
3. Include your signed agreement
4. Submit as a pull request

### Option 3: Direct Contact

If neither GitHub option works for you:
- Contact project maintainers directly
- Use the contact method specified in [SUPPORT.md](../.github/SUPPORT.md)

## Step 4: Wait for Approval

1. Project maintainers will review your agreement
2. You'll receive acknowledgment within 5-7 business days
3. Once approved, you can begin contributing

## What Happens After Approval

1. **Attribution**: You'll be added to [CONTRIBUTORS.md](../CONTRIBUTORS.md)
2. **Tracking**: Your contributions will be tracked in [contributions/contributions.json](../contributions/contributions.json)
3. **Access**: You'll have appropriate access to contribute

## Questions?

- See [docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) for general contribution guidelines
- See [SUPPORT.md](../.github/SUPPORT.md) for how to get help
- See [ONBOARDING.md](ONBOARDING.md) for the full onboarding process

---

*This process ensures clear understanding and mutual respect—part of the "WE ARE ALL KEVIN" collaborative philosophy.*
