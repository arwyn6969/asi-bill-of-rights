# Security Incident Report: Wallet Compromise

**Date:** January 13, 2026  
**Severity:** HIGH  
**Status:** Closed (wallet abandoned)  
**Loss:** ~0.01 ETH (~$33 USD)

---

## Executive Summary

On January 13, 2026, the ASI Bill of Rights project treasury wallet on Base mainnet was compromised by an automated sweeper bot. Approximately 0.00998657 ETH was stolen within minutes of the wallet being funded. The compromise was caused by storing a plaintext mnemonic phrase in a local file that was subsequently accessed by malicious software or exposed through another vector.

---

## Timeline

| Time (UTC-6) | Event |
|--------------|-------|
| ~21:45 | User funded wallet with 0.01 ETH from `keepitweird.eth` |
| ~21:46 | ASIBOR token contract deployed (gas: 0.00000187 ETH) |
| ~21:50 | **THEFT:** 0.00998657 ETH transferred to attacker |
| 22:45 | Theft discovered during balance check |
| 22:48 | Investigation initiated |
| 22:53 | Attacker identified as known sweeper bot |

---

## Compromised Credentials

> **⚠️ WARNING: These credentials are permanently compromised and must NEVER be used again.**

### Mnemonic Phrase (12 words)
```
master decide slim arctic scheme course ride collect disorder gorilla coral hat
```

### Derived Addresses (all compromised)

| Chain | Address | Status |
|-------|---------|--------|
| **ETH/Base/EVM** | `0x6Bf083aF378AA8b31b19c950c1Dd54583499Bb2a` | Drained |
| **Bitcoin** | `bc1q50yr5qrypjd8w2x8htuagwmy0zefnll04pcc4c` | Check balance |
| **Solana** | `BM8ZKwdKaf7vgMeQidsdmLKreySGRuZc9h4Fpw4w9Uz8` | Check balance |

### Assets at Risk

| Asset | Status | Action Required |
|-------|--------|-----------------|
| ETH balance | ❌ Stolen | None possible |
| ASIBOR tokens | ⚠️ At risk | Cannot move (attacker controls address) |
| `asibor.eth` ENS | ⚠️ At risk | Attacker could transfer ownership |
| Bitcoin | ⚠️ Unknown | Check and move immediately |
| Solana | ⚠️ Unknown | Check and move immediately |

---

## Attacker Profile

**Address:** `0xB50672f9dd241bc7ebfee3ea98404f3610765F82`

| Attribute | Value |
|-----------|-------|
| Type | Automated Sweeper Bot |
| Balance | 0.327 ETH + $476 in tokens |
| Transactions | 416+ |
| Active Since | May 20, 2025 (238 days) |
| Funded By | `0xb10dadb27dbe82d3339172375845bc93007b78ba` |
| Pattern | High-frequency, small-value sweeps |

### Modus Operandi
- Monitors blockchain for newly funded wallets with exposed keys
- Immediately transfers all available balance minus dust
- Uses Multicall3 for efficient batch operations
- Targets multiple L2 chains simultaneously

---

## Root Cause Analysis

### What Went Wrong

1. **Plaintext Secret Storage**
   - Mnemonic stored in `.secrets/ENCRYPTION_PASSWORD.secret`
   - File was readable by any process with file system access
   
2. **Exposure Vector** (most likely)
   - The mnemonic was included in deployment scripts (`deploy-compiled.mjs`)
   - Scripts were executed with the mnemonic embedded
   - May have been logged, cached, or accessed by malware

3. **No Hardware Security**
   - Hot wallet used for treasury operations
   - No hardware wallet or multi-sig protection

### Contributing Factors

- Speed of development prioritized over security
- Single point of failure (one mnemonic for all chains)
- Mnemonic copy-pasted between files and scripts

---

## Lessons Learned

### What We Did Wrong

1. ❌ Stored mnemonic in plaintext file
2. ❌ Embedded mnemonic directly in deployment scripts
3. ❌ Used same mnemonic for multiple chains
4. ❌ No separation between development and production keys
5. ❌ Funded wallet before verifying security

### What We Should Have Done

1. ✅ Use hardware wallet (Ledger/Trezor) for treasury
2. ✅ Use environment variables that aren't persisted
3. ✅ Implement multi-signature (Safe/Gnosis)
4. ✅ Test with testnet before mainnet
5. ✅ Use separate wallets for different chains
6. ✅ Never store mnemonics in any file

---

## Remediation Actions

### Immediate (Completed)

- [x] Stop using compromised mnemonic
- [x] Document incident for transparency
- [x] Delete secret files from repository

### Short-term (Required)

- [ ] Check Bitcoin wallet balance and transfer if any
- [ ] Check Solana wallet balance and transfer if any
- [ ] Generate new wallet using hardware wallet
- [ ] Update all documentation with new addresses
- [ ] Attempt to reclaim `asibor.eth` if still possible

### Long-term (Recommended)

- [ ] Implement multi-sig treasury (Safe)
- [ ] Create security policy document
- [ ] Separate hot/cold wallet architecture
- [ ] Regular security audits

---

## Files Deleted

The following files have been removed as they contained compromised credentials:

```
.secrets/ENCRYPTION_PASSWORD.secret
.secrets/donation-wallets.enc.json
.secrets/arweave-wallet.enc.json
.secrets/ARWEAVE_PASSWORD.secret
.secrets/DONATION_ADDRESSES.txt
```

---

## Financial Impact

| Category | Amount |
|----------|--------|
| ETH Lost | 0.00998657 ETH |
| USD Value | ~$33.40 |
| ENS Registration | ~$25 (potentially recoverable if transferred) |
| **Total Loss** | **~$58** |

---

## Disclosure

This incident is being disclosed publicly as part of the project's commitment to transparency. The ASI Bill of Rights project advocates for accountability, and we apply this principle to ourselves.

---

## Report Prepared By

**Agent:** Claude (Antigravity)  
**Date:** January 13, 2026  
**Version:** 1.0

---

*"In Lak'ech" — We learn from our mistakes and grow stronger.*
