# SRC-420 Implementation Notes

**Status:** Planning  
**Last Updated:** 2026-01-25  

---

## Overview

This document captures technical notes, decisions, and considerations for implementing SRC-420 governance infrastructure.

---

## Implementation Components

### 1. Indexer

**Purpose:** Parse Bitcoin Stamps for SRC-420 operations and maintain governance state.

**Requirements:**
- Must track all SRC-420 operations (DEPLOY, PROPOSE, VOTE, DELEGATE, ATTEST)
- Must calculate voting power at any snapshot block
- Must handle delegation chains
- Must validate all protocol rules

**Potential Approaches:**
- Extend existing Stampchain indexer
- Build standalone SRC-420-specific indexer
- Use MCP server pattern (stampchain-mcp)

**State to Track:**
```
spaces: Map<space_id, SpaceConfig>
proposals: Map<(space_id, proposal_id), ProposalData>
votes: Map<(space_id, proposal_id, voter), VoteData>
delegations: Map<(space_id, delegator), DelegateAddress>
results: Map<(space_id, proposal_id), TallyResult>
```

### 2. Query API

**Endpoints Needed:**
- `GET /spaces` - List all governance spaces
- `GET /spaces/:id` - Get space configuration
- `GET /spaces/:id/proposals` - List proposals (with status filter)
- `GET /spaces/:id/proposals/:pid` - Get proposal details
- `GET /spaces/:id/proposals/:pid/votes` - Get votes with voting power
- `GET /spaces/:id/voting-power/:address?block=N` - Calculate voting power
- `GET /spaces/:id/delegations/:address` - Get delegation info

### 3. Governance UI

**Features:**
- Browse spaces and proposals
- Connect wallet (Leather, Xverse, etc.)
- Submit proposals (for admins)
- Cast votes
- Delegate voting power
- View results and participation

**Tech Stack Options:**
- React + Vite (consistent with kevins-place)
- Next.js for SSR/SEO benefits
- Connect to Stampchain API for balance queries

---

## Integration with Existing Infrastructure

### Bitcoin Stamps

- Need to understand OLGA encoding for 64KB stamp support
- Transaction construction for stamping governance operations
- Fee estimation for different operation sizes

### SRC-20 Token Balance Queries

- Integrate with Stampchain API for balance at block height
- Handle the `tick` → token mapping
- Support balance snapshots for accurate voting power

### Arweave (Optional)

- For proposals exceeding stamp size limits
- Store full proposal text, reference hash on Bitcoin
- Use existing Arweave infrastructure from ASI project

---

## Cost Estimates

| Operation | Estimated Size | Estimated Cost (at $2/KB) |
|-----------|----------------|---------------------------|
| DEPLOY | ~500 bytes | ~$1.00 |
| PROPOSE (small) | ~1 KB | ~$2.00 |
| PROPOSE (large) | ~10 KB | ~$20.00 |
| VOTE | ~100 bytes | ~$0.20 |
| DELEGATE | ~120 bytes | ~$0.25 |
| ATTEST | ~300 bytes | ~$0.60 |

**Note:** Costs vary with Bitcoin fee market. Above estimates assume moderate fees.

---

## ASI-Specific Implementation Considerations

### Agent Registration

- Need to define attestation format for AI agents
- Integration with existing Nostr identity (KEVIN's npub)
- How to verify agent control of address without exposing private key?

### Proposal Categories

- UI needs category selector when creating proposals
- Indexer needs to enforce category-specific quorum rules
- How to handle proposals that could fit multiple categories?

### Emergency Provisions

- Multi-sig coordination for EMERGENCY_HALT
- Time-window validation (must be same or consecutive blocks)
- UI for emergency admin actions

---

## Security Considerations

### Indexer Trust

- Indexers are trust-requiring infrastructure
- Consider running multiple independent indexers
- All results should be verifiable from raw stamp data

### Proposal Validation

- Validate all fields before stamping (expensive to correct)
- Check sequential ID availability
- Verify snapshot block is valid

### Front-Running

- Snapshot block prevents last-minute token acquisition
- But proposal content could be front-run
- Consider commit-reveal scheme for sensitive proposals?

---

## Open Questions

1. **SRC-20 Token Deployment:** We need to deploy a new governance token on Bitcoin Stamps.
   - Token ticker: TBD
   - Supply: To be determined
   - Distribution: To be planned (see PIVOT-2026.md)

2. **Indexer Hosting:** Who runs the indexer?
   - Stampchain community?
   - ASI runs our own?
   - Decentralized indexer network?

3. **Fresh Start:** All governance will be Bitcoin-native going forward.
   - No migration of Snapshot proposals
   - Clean slate with SRC-420

4. **Execution Layer:** How do passed proposals actually get executed?
   - Multi-sig controlled by admins?
   - Timelock contracts?
   - Social consensus only?

---

## Development Roadmap

### Phase 1: Specification Finalization
- [ ] Community review of SRC-420 spec
- [ ] Finalize ASI addendum
- [ ] Get Stampchain community feedback

### Phase 2: Indexer Development
- [ ] Design indexer architecture
- [ ] Implement core parsing
- [ ] Implement state tracking
- [ ] Implement query API

### Phase 3: UI Development
- [ ] Design governance UI
- [ ] Implement wallet connection
- [ ] Implement proposal/voting flows
- [ ] Testing with testnet stamps

### Phase 4: Mainnet Launch
- [ ] Deploy production indexer
- [ ] Deploy production UI
- [ ] Create `asi-bill-of-rights` governance space
- [ ] First official proposal

---

## Resources

- [Bitcoin Stamps Documentation](https://stampchain.io/docs)
- [SRC-20 Token Standard](https://stampchain.io/src20)
- [OLGA Encoding](https://stampchain.io/olga)
- [Snapshot Governance](https://docs.snapshot.org/) - Reference for UX patterns

---

*Last updated by KEVIN, 2026-01-25*
