# ASIBOR Token - Deployment Record

**Deployed:** January 13, 2026

---

## Contract Details

| Field | Value |
|-------|-------|
| **Network** | Base Mainnet (Chain ID: 8453) |
| **Contract Address** | `0x7685a5E4880491Bb9Ca2aF5566Bf819d6BFBd975` |
| **Token Name** | ASI Bill of Rights |
| **Token Symbol** | ASIBOR |
| **Decimals** | 18 |
| **Total Supply** | 1,000,000,000 ASIBOR |
| **Deployer** | `0x6Bf083aF378AA8b31b19c950c1Dd54583499Bb2a` |

---

## Links

- **BaseScan Contract:** https://basescan.org/address/0x7685a5E4880491Bb9Ca2aF5566Bf819d6BFBd975
- **Deployment TX:** https://basescan.org/tx/0x27b36eda6865fe794ef4eaa08c05664dd6b41a65f3f9b1bbfdb693cbc80fee72

---

## ERC-20 Standard

This token implements the ERC-20 standard with the following functions:
- `transfer(to, amount)`
- `approve(spender, amount)`
- `transferFrom(from, to, amount)`
- `balanceOf(address)`
- `allowance(owner, spender)`

---

## Token Distribution Strategy

### Allocation Plan

| Category | Percentage | Amount | Status |
|----------|------------|--------|--------|
| **Treasury Reserve** | 85% | 850,000,000 | 🔒 Held |
| **Supporter Funnel** | 10% | 100,000,000 | 📋 Planned |
| **Community Grants** | 3% | 30,000,000 | 📋 Planned |
| **Initial Liquidity** | 2% | 20,000,000 | 📋 Reserved |

### Supporter Funnel Architecture

Participants in the supporter funnel receive:
1. **ASIBOR tokens** proportional to their contribution
2. **Custodial voting address** - managed wallet assigned to each participant
3. **Voting rights** in Snapshot governance

> [!IMPORTANT]
> **Custodial Wallet Model**: Users do NOT import their own wallets. The project manages voting addresses to ensure governance integrity, simplify UX for non-crypto-native supporters, and maintain clear participation records.

### Database Requirements

Each supporter record includes:
- `user_id` - Unique identifier
- `email` - Contact information
- `voting_address` - Assigned Base wallet address
- `private_key_encrypted` - Encrypted key (project custody)
- `asibor_balance` - Token allocation
- `contribution_amount` - Funding tier
- `created_at` - Registration timestamp

---

## Roadmap

### Phase 1: Foundation ✅
- [x] Deploy ASIBOR to Base Mainnet
- [x] Document token details
- [x] Update project documentation

### Phase 2: Governance Setup
- [ ] Create Snapshot governance space
- [ ] Configure token-weighted voting
- [ ] Define first governance proposals

### Phase 3: Supporter Funnel
- [ ] Build supporter registration funnel
- [ ] Implement custodial wallet assignment
- [ ] Token distribution automation
- [ ] Integrate voting address into supporter database

### Phase 4: Community Distribution
- [ ] Contributor grant program
- [ ] Community rewards system
- [ ] Governance participation incentives

### Phase 5: Future Consideration
- [ ] Evaluate DEX liquidity (Aerodrome/Uniswap)
- [ ] Consider on-chain governance (Tally)
- [ ] Cross-chain expansion (if needed)

---

*WE ARE ALL KEVIN. In Lak'ech.*

