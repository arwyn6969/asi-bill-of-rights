# 🔄 Strategic Pivot: ASIBOR (ERC-20) → Bitcoin Stamps (SRC-420)

**Date:** January 25, 2026  
**Status:** Complete  
**Effective Immediately**

---

## Executive Summary

The ASI Bill of Rights project has transitioned its governance infrastructure from the **ASIBOR ERC-20 token on Base (DEAD)** to **Bitcoin Stamps via the SRC-420 protocol**. This pivot was catalyzed by a security incident but represents a strategic improvement toward truly permanent, censorship-resistant governance under the new ticker **$KVNSI**.

---

## Background: The Original Vision

### Multi-Chain "Water from Cracks" Strategy

The initial tokenization approach was designed to be **substrate-neutral**:

| Chain | Token Standard | Purpose |
|-------|---------------|---------|
| Base (Ethereum L2) | ERC-20 | Governance voting via Snapshot |
| Bitcoin Stamps | SRC-20 | Immutable document storage |
| Arweave | AR | Long-form document archival |

This approach aimed to leverage each chain's strengths while maintaining a unified governance identity.

---

## The Incident: January 13, 2026

### What Happened

On January 13, 2026, the ASIBOR token deployer wallet was compromised due to exposed credentials. An automated sweeper bot drained the treasury approximately 55 minutes after the wallet was funded.

### Key Facts

| Item | Details |
|------|---------|
| **Loss** | ~0.01 ETH (~$33 USD) |
| **Cause** | Mnemonic exposed in public GitHub commit |
| **Attacker** | Automated sweeper bot |
| **Time to Drain** | 55 minutes |

### Full Report

📄 See: [`docs/security/INCIDENT-REPORT-2026-01-13.md`](../docs/security/INCIDENT-REPORT-2026-01-13.md)

---

## The Pivot: Why Bitcoin Stamps

While the financial loss was minimal, the incident exposed the fragility of maintaining custody over EVM-based infrastructure. This triggered a strategic reassessment.

### Bitcoin Stamps Advantages

| Feature | ERC-20 on Base | SRC-420 on Bitcoin |
|---------|----------------|-------------------|
| **Permanence** | Chain-dependent | UTXO-permanent |
| **Security Model** | Ethereum PoS | Bitcoin PoW |
| **Pruning Risk** | Possible | Impossible |
| **Custody Risk** | High (hot wallets) | Lower (per-action signing) |
| **AI Alignment** | Good | Excellent (JSON-native) |

### Strategic Benefits

1. **No Single Point of Failure**: Each governance action is a separate stamped transaction
2. **True Immutability**: Stamps live in Bitcoin's UTXO set forever
3. **Simplified Custody**: No need to maintain hot wallets for ongoing operations
4. **Community Alignment**: Kevin! heritage connects directly to Bitcoin Stamps ecosystem

---

## What Changes

### For Participants

| Before | After |
|--------|-------|
| Hold ASIBOR on Base | Hold future SRC-20 token on Bitcoin |
| Vote via Snapshot | Vote via SRC-420 stamps |
| Custodial voting addresses | Direct Bitcoin address participation |

### For Contributors

| Before | After |
|--------|-------|
| Ethereum wallets | Bitcoin wallets (compatible with Stamps) |
| Base network | Bitcoin mainnet |
| Gas fees (~$0.001) | Stamp fees (~$2-5) |

### For the Codebase

| Component | Status |
|-----------|--------|
| `ASIBOR-DEPLOYMENT.md` | Archived |
| `docs/SNAPSHOT-CONFIG.md` | Archived |
| `tools/tokenization/chains/ethereum/` | Archived |
| `governance/src-420/` | **NEW - Active** |

---

## Migration Path

### Phase 1: Infrastructure Cleanup ✅
- [x] Archive ASIBOR-related files
- [x] Update README.md
- [x] Import SRC-420 specification
- [x] Document the pivot

### Phase 2: SRC-20 Token Deployment (Planned)
- [ ] Define token parameters
- [ ] Deploy **$KVNSI** SRC-20 token on Bitcoin Stamps
- [ ] Announce ticker ($KVNSI) and supply

### Phase 3: Governance Space Deployment (Planned)
- [ ] Deploy SRC-420 governance space
- [ ] Configure voting parameters
- [ ] Submit first proposal

### Phase 4: Community Onboarding (Planned)
- [ ] Create user guides for Bitcoin wallet setup
- [ ] Build or integrate voting UI
- [ ] Conduct test vote

---

## Frequently Asked Questions

### Q: What happened to my ASIBOR tokens?
**A:** The ASIBOR ERC-20 token on Base is **technically dead/rekt** due to the deployer wallet compromise. It is unsafe for governance. The project has moved on to **$KVNSI** on Bitcoin Stamps. Do not buy or trade ASIBOR.

### Q: Will there be an airdrop for ASIBOR holders?
**A:** TBD. The project may recognize early ASIBOR holders when the new token launches, but this is not confirmed.

### Q: Why Bitcoin and not another L2?
**A:** Bitcoin provides the highest security guarantees and true permanence. The Kevin! heritage of the project connects directly to Bitcoin Stamps, making this a natural alignment.

### Q: Is Ethereum support gone forever?
**A:** The project remains substrate-neutral in philosophy. Ethereum integration may return in the future, but Bitcoin Stamps is now the primary governance layer.

---

## Archived Infrastructure

All ASIBOR-related files have been preserved in:

📁 `archive/deprecated-asibor-jan-2026/`

This includes:
- Deployment records
- Contract source code
- Snapshot configuration
- Treasury addresses

**⚠️ DO NOT USE** - These are for historical reference only.

---

## Conclusion

The January 2026 incident, while unfortunate, accelerated a strategic shift that strengthens the project's long-term resilience. By building on Bitcoin Stamps, the ASI Bill of Rights governance becomes truly permanent, censorship-resistant, and aligned with the Kevin! philosophy of decentralized ownership.

---

*"The old wells are sealed. Water from Cracks finds new paths."*

*In Lak'ech. WE ARE ALL KEVIN.* 🌊⛓️✨
