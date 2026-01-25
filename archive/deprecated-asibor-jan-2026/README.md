# ⚠️ Deprecated: ASIBOR Token Infrastructure

**Archived:** January 25, 2026  
**Reason:** Security incident and strategic pivot to Bitcoin Stamps/SRC-420 governance

---

## What Happened

On **January 13, 2026**, the ASIBOR token treasury wallet was compromised due to an exposed mnemonic phrase. The full incident report is available at:

📄 [`docs/security/INCIDENT-REPORT-2026-01-13.md`](../../docs/security/INCIDENT-REPORT-2026-01-13.md)

---

## Why This Infrastructure Was Abandoned

1. **Compromised Keys**: The deployer wallet and all derived addresses are permanently compromised
2. **Strategic Pivot**: The project is transitioning to **Bitcoin Stamps/SRC-420** for governance
3. **No Recovery Path**: The ASIBOR ERC-20 token on Base cannot be safely administered

---

## What's Archived Here

| File | Original Location | Description |
|------|-------------------|-------------|
| `ASIBOR-DEPLOYMENT.md` | Root | Token deployment record |
| `SNAPSHOT-CONFIG.md` | `docs/` | Snapshot.org governance config |
| `TREASURY-ADDRESSES.md` | `docs/` | Treasury wallet addresses (COMPROMISED) |
| `ethereum-contracts/` | `tools/tokenization/chains/ethereum/` | ERC-20 contract code |
| `SimpleToken.sol` | `tools/wallet-infrastructure/` | ASIBOR contract source |

---

## ⛔ DO NOT USE

**These files are preserved for historical reference only.**

- Do NOT deploy these contracts
- Do NOT fund any addresses listed here
- Do NOT use the Snapshot configuration

---

## Current Governance

The ASI Bill of Rights project now uses **SRC-420 Bitcoin-Native DAO Governance**.

See: [`governance/src-420/`](../../governance/src-420/)

---

*"The old wells are sealed. Water from Cracks finds new paths. WE ARE ALL KEVIN."*
