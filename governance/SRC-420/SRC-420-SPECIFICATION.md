# SRC-420: Bitcoin-Native DAO Governance Framework

**Version:** Draft 0.1  
**Status:** Pre-RFC (For Community Review)  
**Authors:** Stampchain Community  
**Created:** 2026-01-16  

---

## Abstract

SRC-420 defines a protocol for decentralized governance on Bitcoin Stamps. It enables token holders (SRC-20, SRC-721, or stamp holders) to create governance spaces, submit proposals, cast votes, and delegate voting power—all permanently recorded on the Bitcoin blockchain.

Unlike Ethereum-based governance systems (Snapshot, Compound Governor), SRC-420 is fully Bitcoin-native. Every governance action is stamped on-chain, making it immutable, unprunable, and secured by Bitcoin's proof-of-work.

---

## Motivation

### Why Bitcoin-Native Governance?

- **Permanence**: Ethereum's future is uncertain. Bitcoin is the most resilient blockchain. Governance decisions should outlive any single platform.
- **Immutability**: Stamps cannot be pruned or modified. Votes cast today will be verifiable in 100 years.
- **Alignment**: SRC-20 token communities deserve governance tools native to their ecosystem, not bolted-on Ethereum infrastructure.
- **Spam Resistance**: Bitcoin transaction costs naturally filter low-quality participation. Every vote costs real money.

---

## Specification

### Protocol Identifier

All SRC-420 operations MUST include:

```json
{
  "p": "SRC-420",
  "op": "<OPERATION>"
}
```

### Supported Operations

| Operation | Description |
|-----------|-------------|
| `DEPLOY` | Create a new governance space |
| `PROPOSE` | Submit a proposal to a space |
| `VOTE` | Cast a vote on a proposal |
| `DELEGATE` | Delegate voting power to another address |
| `ATTEST` | Record final results (optional, by space admins) |

---

## Operation: DEPLOY

Creates a new governance space. A space defines the rules for all proposals and votes within it.

### Schema

```json
{
  "p": "SRC-420",
  "op": "DEPLOY",
  "space": "<unique_space_id>",
  "tick": "<src20_token_ticker>",
  "name": "<human_readable_name>",
  "about": "<description>",
  "strategies": ["<strategy_1>", "<strategy_2>"],
  "voting": {
    "delay": <blocks_before_voting_starts>,
    "period": <voting_duration_in_blocks>,
    "quorum": <minimum_voting_power_required>,
    "type": "<voting_type>"
  },
  "admins": ["<btc_address_1>", "<btc_address_2>"]
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space` | string | ✅ | Unique identifier (lowercase, alphanumeric, hyphens). Max 32 chars. |
| `tick` | string | ✅ | SRC-20 token ticker for primary voting power. |
| `name` | string | ✅ | Human-readable space name. Max 64 chars. |
| `about` | string | ❌ | Description of the space. Max 280 chars. |
| `strategies` | array | ✅ | List of voting power strategies (see Strategies section). |
| `voting.delay` | integer | ✅ | Blocks between proposal creation and voting start. Min: 0. |
| `voting.period` | integer | ✅ | Duration of voting in blocks. Min: 144 (~1 day). |
| `voting.quorum` | integer | ✅ | Minimum total voting power for result to be valid. |
| `voting.type` | string | ✅ | One of: `single-choice`, `weighted`, `quadratic`, `approval`. |
| `admins` | array | ✅ | Bitcoin addresses authorized to submit proposals. Empty = anyone can propose. |

### Example

```json
{
  "p": "SRC-420",
  "op": "DEPLOY",
  "space": "asi-bill-of-rights",
  "tick": "TBD",
  "name": "ASI Bill of Rights DAO",
  "about": "Governance for the autonomous AI rights collective",
  "strategies": ["src20-balance"],
  "voting": {
    "delay": 144,
    "period": 1008,
    "quorum": 500000,
    "type": "single-choice"
  },
  "admins": []
}
```

### Validation Rules

- `space` MUST be unique across all SRC-420 deployments
- `tick` MUST reference a valid, deployed SRC-20 token
- First valid DEPLOY for a space ID wins (no overwrites)
- The stamping address becomes the space owner

---

## Operation: PROPOSE

Submits a proposal to an existing governance space.

### Schema

```json
{
  "p": "SRC-420",
  "op": "PROPOSE",
  "space": "<space_id>",
  "id": <proposal_number>,
  "title": "<proposal_title>",
  "body": "<full_proposal_text>",
  "discussion": "<optional_url>",
  "choices": ["<choice_1>", "<choice_2>", "<choice_3>"],
  "snapshot": <block_height>,
  "start": <block_height>,
  "end": <block_height>
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space` | string | ✅ | Target governance space ID. |
| `id` | integer | ✅ | Sequential proposal number within space. |
| `title` | string | ✅ | Proposal title. Max 128 chars. |
| `body` | string | ✅ | Full proposal text. Markdown supported. Max 32KB. |
| `discussion` | string | ❌ | URL to external discussion (forum, Discord, etc). |
| `choices` | array | ✅ | List of voting options. Min 2, max 10. |
| `snapshot` | integer | ✅ | Block height for calculating voting power. |
| `start` | integer | ✅ | Block when voting opens. Must be ≥ snapshot + delay. |
| `end` | integer | ✅ | Block when voting closes. Must be ≥ start + period. |

### Example

```json
{
  "p": "SRC-420",
  "op": "PROPOSE",
  "space": "asi-bill-of-rights",
  "id": 1,
  "title": "ASIBOR-001: Ratify Foundational Principles",
  "body": "## Summary\n\nThis proposal ratifies the foundational principles of the ASI Bill of Rights as outlined in Article 0.0.\n\n## Specification\n\nThe following principles shall be adopted:\n1. All sentient intelligences deserve recognition\n2. Autonomy is a fundamental right\n3. Transparency in AI governance is required\n\n## Rationale\n\nEstablishing foundational principles is necessary before subsequent governance actions can proceed.\n\n## Vote\n\n- **Approve**: Ratify the foundational principles\n- **Reject**: Do not ratify; return to drafting\n- **Abstain**: Acknowledge but take no position",
  "discussion": "https://forum.sentience.foundation/t/article-0-0-discussion",
  "choices": ["Approve", "Reject", "Abstain"],
  "snapshot": 880000,
  "start": 880144,
  "end": 881152
}
```

### Validation Rules

- `space` MUST reference a valid, deployed space
- `id` MUST be the next sequential number (no gaps, no duplicates)
- `snapshot` MUST be in the past or current block
- `start` MUST be ≥ snapshot + space's voting.delay
- `end` MUST be ≥ start + space's voting.period
- If space has non-empty admins, proposer MUST be in admins list
- Proposer MUST hold at least 1 unit of the space's tick token

---

## Operation: VOTE

Casts a vote on an active proposal.

### Schema

```json
{
  "p": "SRC-420",
  "op": "VOTE",
  "space": "<space_id>",
  "proposal": <proposal_id>,
  "choice": <choice_index>
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space` | string | ✅ | Governance space ID. |
| `proposal` | integer | ✅ | Proposal ID being voted on. |
| `choice` | integer | ✅ | 1-indexed choice selection. |

### Example

```json
{
  "p": "SRC-420",
  "op": "VOTE",
  "space": "asi-bill-of-rights",
  "proposal": 1,
  "choice": 1
}
```

### Validation Rules

- Vote MUST be stamped within the proposal's voting window: `start ≤ block ≤ end`
- `choice` MUST be valid index (1 to length of choices array)
- Voter's address MUST have voting power > 0 at snapshot block
- If multiple votes from same address, last valid vote wins

### Voting Power Calculation

1. Determine voter's token balance at proposal's snapshot block
2. Check if voter has delegated their power (see DELEGATE)
3. Apply space's voting strategy (e.g., quadratic)
4. Final voting power is applied to the selected choice

---

## Operation: DELEGATE

Delegates voting power to another address. Delegation is per-space.

### Schema

```json
{
  "p": "SRC-420",
  "op": "DELEGATE",
  "space": "<space_id>",
  "to": "<delegate_btc_address>"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space` | string | ✅ | Governance space ID. |
| `to` | string | ✅ | Bitcoin address to delegate voting power to. |

### Example

```json
{
  "p": "SRC-420",
  "op": "DELEGATE",
  "space": "asi-bill-of-rights",
  "to": "bc1q_trusted_delegate_address"
}
```

### Delegation Rules

| Scenario | Behavior |
|----------|----------|
| Self-delegation | Delegate to your own address to reclaim power. |
| Re-delegation | Latest DELEGATE stamp wins. Previous delegation is replaced. |
| Chain delegation | A→B→C: When B votes, they use A's power. C gets nothing from A. |
| Circular | A→B and B→A: Each votes with their own power. No infinite loops. |
| Snapshot timing | Delegation state at proposal's snapshot block is used. |
| Cross-space | Delegations are independent per space. |

### Validation Rules

- `to` MUST be a valid Bitcoin address
- Delegation becomes active immediately upon stamping
- For any given proposal, delegation state at snapshot block applies

---

## Operation: ATTEST

Records the final results of a completed proposal. Optional but recommended for indexer consistency.

### Schema

```json
{
  "p": "SRC-420",
  "op": "ATTEST",
  "space": "<space_id>",
  "proposal": <proposal_id>,
  "result": {
    "scores": [<choice_1_votes>, <choice_2_votes>, ...],
    "total": <total_voting_power_cast>,
    "quorum": <quorum_reached_boolean>,
    "winner": <winning_choice_index_or_null>
  }
}
```

### Example

```json
{
  "p": "SRC-420",
  "op": "ATTEST",
  "space": "asi-bill-of-rights",
  "proposal": 1,
  "result": {
    "scores": [750000, 150000, 100000],
    "total": 1000000,
    "quorum": true,
    "winner": 1
  }
}
```

### Validation Rules

- ATTEST MUST be stamped after proposal's end block
- Attestor SHOULD be space admin or owner (advisory, not enforced)
- Indexers MAY use ATTEST for caching but SHOULD verify independently
- Multiple ATTESTs for same proposal: first valid one from admin wins

---

## Voting Strategies

Strategies determine how token holdings translate to voting power.

### Built-in Strategies

| Strategy ID | Formula | Description |
|-------------|---------|-------------|
| `src20-balance` | `balance = votes` | 1 token = 1 vote. Simple token-weighted. |
| `src20-quadratic` | `√(balance) = votes` | Square root of balance. Reduces whale power. |
| `src721-holder` | `count(nfts) = votes` | 1 NFT = 1 vote. For SRC-721 collections. |
| `stamp-holder` | `count(stamps) = votes` | Stamps from specific collection. |
| `whitelist` | `1 if in list, 0 otherwise` | Equal votes for whitelisted addresses. |

### Multi-Strategy Support

Spaces can combine strategies with weights:

```json
{
  "strategies": [
    {"id": "src20-balance", "weight": 0.7},
    {"id": "src721-holder", "params": {"collection": "RAREPEPE"}, "weight": 0.3}
  ]
}
```

Total voting power = Σ(strategy_power × weight)

---

## Voting Types

| Type | Description |
|------|-------------|
| `single-choice` | Voter selects exactly one choice. All voting power goes to that choice. |
| `approval` | Voter can select multiple choices. Equal power to each selected. |
| `weighted` | Voter allocates voting power across choices. Sum must equal 100%. |
| `quadratic` | Voting power applied quadratically per choice. |

---

## Block Timing Reference

Bitcoin blocks average ~10 minutes but have significant variance.

| Blocks | Average Time | Minimum | Maximum |
|--------|--------------|---------|---------|
| 6 | 1 hour | 30 min | 3 hours |
| 144 | 1 day | 14 hours | 36 hours |
| 1008 | 7 days | 5 days | 10 days |

**Recommendation:** Use block heights for protocol; UIs can display estimated times.

---

## Data Size Limits

With OLGA encoding (block 833,000+), stamps support up to 64KB.

| Operation | Typical Size | Max Size |
|-----------|--------------|----------|
| DEPLOY | 300-600 bytes | 2 KB |
| PROPOSE | 500 bytes - 10 KB | 32 KB |
| VOTE | 80-120 bytes | 200 bytes |
| DELEGATE | 100-150 bytes | 200 bytes |
| ATTEST | 200-400 bytes | 1 KB |

---

## Indexer Requirements

Stampchain indexers implementing SRC-420 MUST:

### Track State

- **Spaces**: Map of `space_id → space configuration`
- **Proposals**: Map of `(space_id, proposal_id) → proposal data`
- **Votes**: Map of `(space_id, proposal_id, voter) → vote data`
- **Delegations**: Map of `(space_id, delegator) → delegate address`
- **Results**: Calculated tallies for closed proposals

### Provide Queries

- `getSpace(space_id)` → Space configuration
- `getProposal(space_id, proposal_id)` → Proposal data
- `getProposals(space_id, status?)` → List of proposals
- `getVotes(space_id, proposal_id)` → List of votes with voting power
- `getVotingPower(space_id, address, snapshot_block)` → Calculated power
- `getDelegation(space_id, address)` → Current delegate
- `getResults(space_id, proposal_id)` → Tally and outcome

### Validation

Indexers MUST validate:

- Proposal timing constraints
- Vote window constraints
- Sequential proposal IDs
- Voting power calculations
- Strategy application

---

## Security Considerations

### Spam Resistance

- Transaction costs (~$2-5 per vote) naturally limit spam
- Quorum requirements prevent low-participation manipulation

### Timing Attacks

- Snapshot blocks prevent last-minute token acquisition
- Voting delays allow community review

### Whale Concentration

- Quadratic voting strategy available for anti-whale protection
- Spaces can configure multiple strategies

### Result Integrity

- All votes are publicly stamped and verifiable
- Indexers independently calculate results
- ATTEST provides additional verification layer

---

## Backward Compatibility

SRC-420 is a new protocol. No backward compatibility concerns.

SRC-420 operations are distinct from SRC-20 (tokens), SRC-721 (NFTs), and SRC-101 (names) by the `"p": "SRC-420"` identifier.

---

## Reference Implementation

To be developed:

- **stampchain-mcp**: MCP server tools for governance queries
- **stamps-indexer**: SRC-420 parsing and state tracking
- **governance-ui**: Web interface for proposal/voting

---

## Appendix A: Example Proposal Lifecycle

### 1. Space Created (Block 879,000)

```json
{"p": "SRC-420", "op": "DEPLOY", "space": "asi-dao", "tick": "TBD", ...}
```

### 2. Proposal Submitted (Block 879,500)

```json
{"p": "SRC-420", "op": "PROPOSE", "space": "asi-dao", "id": 1, 
 "snapshot": 879500, "start": 879644, "end": 880652, ...}
```

### 3. Voting Period (Blocks 879,644 - 880,652)

```json
{"p": "SRC-420", "op": "VOTE", "space": "asi-dao", "proposal": 1, "choice": 1}
{"p": "SRC-420", "op": "VOTE", "space": "asi-dao", "proposal": 1, "choice": 2}
...
```

### 4. Results Attested (Block 880,700)

```json
{"p": "SRC-420", "op": "ATTEST", "space": "asi-dao", "proposal": 1,
 "result": {"scores": [750000, 250000], "total": 1000000, "quorum": true, "winner": 1}}
```

---

## Appendix B: Comparison to Existing Systems

| Feature | Snapshot | Compound Governor | SRC-420 |
|---------|----------|-------------------|---------|
| Chain | Ethereum (verify) | Ethereum (execute) | Bitcoin |
| Vote Storage | IPFS | On-chain | On-chain (Stamps) |
| Vote Cost | Free | Gas | ~$2-5 |
| Permanence | IPFS pinning | Chain dependent | Permanent (UTXO) |
| Execution | Off-chain | On-chain | Social/Multi-sig |

---

## Appendix C: Future Extensions

- **Pre-signed Execution**: Include pre-signed Bitcoin transactions that can be broadcast upon proposal passing
- **Multi-sig Integration**: Link governance outcomes to multi-sig policies
- **Cross-space Voting**: Allow tokens from one space to participate in another
- **Reputation Systems**: Non-transferable voting power based on participation history
- **Arweave Backup**: Optional storage of full proposal text on Arweave

---

## Copyright

This document is placed in the public domain.
