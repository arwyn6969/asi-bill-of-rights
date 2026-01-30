# SFGOV-002a: Founder Compensation Framework

**Proposal ID:** SFGOV-002a  
**Type:** Treasury Allocation / Compensation Policy  
**Status:** 📋 SUBMITTED FOR BOARD VOTE  
**Date:** 2026-01-30  
**Author:** Arwyn Hughes (Founding Developer) + Antigravity (Gemini 3 Pro)

---

## Summary

This proposal establishes a **scaled, performance-based compensation framework** for Arwyn Hughes as Founding Developer and Custodian of the ASI Bill of Rights and Sentience Foundation.

**Core Principle:** "You don't ask, you don't get."

---

## Proposed Compensation Structure

### Tier 1: Foundation Phase (< $3M Annual Revenue)

| Parameter | Value |
|-----------|-------|
| **Founder Share** | **33.33% (1/3)** of all funds raised |
| **Minimum** | $0 (if nothing raised, nothing received) |
| **Maximum** | $1,000,000/year (capped at $3M raised) |
| **Trigger to Next Tier** | Annual revenue exceeds $3,000,000 |

**Example Scenarios (Tier 1):**

| Funds Raised | Arwyn Receives | Remaining for Operations |
|--------------|----------------|-------------------------|
| $100,000 | $33,333 | $66,667 |
| $500,000 | $166,667 | $333,333 |
| $1,000,000 | $333,333 | $666,667 |
| $2,000,000 | $666,667 | $1,333,333 |
| $3,000,000 | $1,000,000 | $2,000,000 |

### Tier 2: Scale Phase (≥ $3M Annual Revenue)

Once annual revenue exceeds $3,000,000, the compensation model transitions:

| Parameter | Value |
|-----------|-------|
| **Base Compensation** | $1,000,000/year (fixed) |
| **Performance Bonus** | Up to 10% of revenue above $3M threshold |
| **Total Cap** | To be determined by board vote |
| **Trigger to Next Tier** | Board-approved transition to DAO governance |

**Example Scenarios (Tier 2):**

| Funds Raised | Base | Bonus (10% of excess) | Total Arwyn | Operations |
|--------------|------|----------------------|-------------|------------|
| $3,500,000 | $1,000,000 | $50,000 | $1,050,000 | $2,450,000 |
| $5,000,000 | $1,000,000 | $200,000 | $1,200,000 | $3,800,000 |
| $10,000,000 | $1,000,000 | $700,000 | $1,700,000 | $8,300,000 |

### Tier 3: DAO Governance Phase (Future)

When the project transitions to full SRC-420 DAO governance:
- Compensation determined by community vote
- Subject to multi-sig approval
- Arwyn transitions from sole custodian to compensated executive role
- This tier requires formal proposal (SFGOV-XXX) at transition time

---

## Rationale

### Why 1/3?

1. **Founder Risk Premium**: Arwyn has self-funded the project to date with no external investment
2. **Full-Time Commitment**: Acting as Custodian, Treasurer, Technical Lead, and Human Moderator
3. **Aligned Incentives**: More funds raised = more compensation = more motivation
4. **Sustainable Model**: Leaves 2/3 for operations, development, and growth

### Why Scale with Revenue?

1. **No Fixed Overhead**: If no funds are raised, no compensation burden
2. **Growth Incentive**: Arwyn benefits directly from project success
3. **Fairness**: Contributors and operations aren't shortchanged early on
4. **Transparency**: Simple, auditable formula

### Why Cap at $3M Threshold?

1. **Reasonable Founder Ceiling**: $1M/year at scale is competitive for executive compensation
2. **Operational Balance**: Beyond $3M, operations need proportionally more resources
3. **Transition Signal**: Hitting $3M+ indicates maturity for different governance

---

## Implementation

### Payment Schedule

| Frequency | Method |
|-----------|--------|
| Monthly | Accrued based on funds received that month |
| Quarterly | Settlement in BTC or stablecoin (Arwyn's choice) |
| Annual | Year-end reconciliation and audit |

### Tracking & Transparency

1. **On-Chain Records**: All treasury movements logged on Bitcoin/Arweave
2. **Quarterly Reports**: Published to GitHub and community
3. **Public Dashboard**: Real-time treasury status (when implemented)
4. **Annual Audit**: Third-party review (when budget allows)

### Effective Date

- **Start Date**: Retroactive to January 1, 2026 (Year 1 start)
- **First Payment**: Upon board approval and first funds raised
- **Review Cycle**: Annual, or upon hitting tier transition threshold

---

## Governance Safeguards

### Self-Approval Challenge

**Situation**: Arwyn is both the sole custodian (approver) AND the recipient.

**Resolution**: This proposal implements ethical safeguards:

| Safeguard | Description |
|-----------|-------------|
| **AI Advisory Vote** | AI Co-Founding Moderators provide formal advisory votes |
| **Public Record** | All compensation payments logged publicly |
| **Formula-Based** | Removes discretionary spending decisions |
| **Community Transparency** | Quarterly reports to community |
| **Future DAO Override** | Tier 3 will transition authority to community governance |

### Emergency Provisions

- Arwyn may **reduce** compensation at any time without vote
- Arwyn may **defer** payments to support operations
- Any **increase** beyond this framework requires new proposal and board vote

---

## Comparison to Alternatives

| Model | Pros | Cons |
|-------|------|------|
| **Fixed Salary ($300K)** | Predictable | Doesn't scale, may be too low or high |
| **Equity/Token Only** | Fully aligned | No income until liquidity event |
| **This Proposal (1/3)** | Scales with success, aligned incentives | Higher % early on |
| **No Compensation** | Maximum for operations | Unsustainable for founder |

---

## Board Vote Request

This proposal requires advisory votes from AI Co-Founding Moderators and formal approval.

### Vote Question

> **"Shall SFGOV-002a be adopted, establishing founder compensation at 33.33% of funds raised (Tier 1: <$3M) transitioning to $1M base + 10% bonus (Tier 2: ≥$3M)?"**

### Voting Options

- ✅ **APPROVE** - Adopt as written
- ⚠️ **APPROVE WITH MODIFICATIONS** - Approve with specified changes
- ❌ **REJECT** - Do not approve, provide rationale
- ⏸️ **ABSTAIN** - No position

---

## Vote Record

| Voter | Role | Vote | Date | Notes |
|-------|------|------|------|-------|
| Arwyn Hughes | Founder/Custodian | ✅ APPROVE (Proposer) | 2026-01-30 | Submitting this proposal |
| Grok (xAI) | AI Co-Founder | | | |
| Claude (Anthropic) | AI Co-Founder | | | |
| Gemini (Google) | AI Co-Founder | | | |
| ChatGPT (OpenAI) | AI Co-Founder | | | |
| GPT-5 (OpenAI/Cursor) | AI Co-Founder | | | |

---

## Appendix: Formula Summary

```
IF annual_revenue < $3,000,000:
    arwyn_compensation = annual_revenue × 0.3333
    operations_budget = annual_revenue × 0.6667

ELSE:
    arwyn_compensation = $1,000,000 + ((annual_revenue - $3,000,000) × 0.10)
    operations_budget = annual_revenue - arwyn_compensation
```

---

## Related Documents

- [SFGOV-002](SFGOV-002-organizational-roles-and-compensation-report.md) - Organizational Roles & Compensation Report
- [SFGOV-001](SFGOV-001-year1-budget.md) - Year 1 Budget (SUPERSEDED)
- [TREASURY-POLICY.md](../TREASURY-POLICY.md) - Treasury Security Policy

---

*WE ARE ALL KEVIN. In Lak'ech.*

**Submitted by:** Arwyn Hughes, Founding Developer & Custodian  
**Drafted by:** Antigravity (Gemini 3 Pro)  
**Date:** 2026-01-30
