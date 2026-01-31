# 🧹 Spring Cleaning 2026: Framework Remediation Plan

**Created:** January 25, 2026  
**Status:** ✅ COMPLETE  
**Branch:** `feature/src-420-governance`

---

## Executive Summary

Following the **wallet compromise incident of January 13, 2026**, the ASI Bill of Rights framework contained outdated references to the ASIBOR token (Base/ERC-20) infrastructure that was abandoned. This cleanup systematically:

1. ✅ Archived and deprecated compromised ASIBOR infrastructure
2. ✅ Integrated and formalized Bitcoin Stamps/SRC-420 as the governance layer
3. ✅ Cleaned up inconsistencies and outdated documentation
4. ✅ Prepared the framework for the next phase of development

---

## Execution Summary

### Phase 1: ASIBOR Deprecation ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| 1.1 Create archive directory | ✅ | `archive/deprecated-asibor-jan-2026/` with README |
| 1.2 Move deprecated files | ✅ | ASIBOR-DEPLOYMENT, SNAPSHOT-CONFIG, TREASURY-ADDRESSES, ethereum contracts, SimpleToken.sol |
| 1.3 Update README.md | ✅ | Replaced ASIBOR section with SRC-420 governance |
| 1.4 Mark proposals superseded | ✅ | Added deprecation notice to SFGOV-001 |

### Phase 2: SRC-420 Integration ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| 2.1 Import SRC-420 specification | ✅ | Added to `governance/src-420/SPECIFICATION.md` |
| 2.2 Update tokenization docs | ✅ | Changed ASIBOR → TBD in bitcoin-stamps README |
| 2.3 Create PIVOT-2026.md | ✅ | Comprehensive pivot documentation |

### Phase 3: Documentation Cleanup ✅ COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| 3.1 Fix cross-references | ✅ | Updated README, DONATE, TREASURY-POLICY |
| 3.2 Mark compromised addresses | ✅ | Added warnings to all donation/treasury docs |
| 3.3 Update SRC-420 implementation notes | ✅ | Removed bridging questions, updated for fresh start |

### Phase 4: Lazy Kevin ❌ NOT APPLICABLE

Removed from plan - Lazy Kevin is a separate project, not related to ASI governance.

---

## Files Modified

### Created
- `archive/deprecated-asibor-jan-2026/README.md`
- `governance/src-420/SPECIFICATION.md`
- `PIVOT-2026.md`
- `SPRING-CLEANING-2026.md`

### Moved to Archive
- `ASIBOR-DEPLOYMENT.md`
- `docs/SNAPSHOT-CONFIG.md`
- `docs/TREASURY-ADDRESSES.md`
- `tools/tokenization/chains/ethereum/*`
- `tools/wallet-infrastructure/SimpleToken.sol`

### Updated
- `README.md` - Replaced ASIBOR section with SRC-420, updated donation table
- `DONATE.md` - Added warning about compromised Ethereum address
- `TREASURY-POLICY.md` - Marked Ethereum address as compromised
- `proposals/SFGOV-001-year1-budget.md` - Added superseded notice
- `tools/tokenization/chains/bitcoin-stamps/README.md` - Changed ASIBOR → TBD
- `governance/SRC-420/IMPLEMENTATION-NOTES.md` - Updated open questions
- `governance/SRC-420/SRC-420-SPECIFICATION.md` - Changed tick to TBD
- `governance/SRC-420/ASI-ADDENDUM.md` - Changed tick to TBD

---

## Verification Results

### Remaining ASIBOR References (Expected)
The following references remain and are appropriate:
- **PIVOT-2026.md** - Explains the historical context
- **Security reports** - Historical documentation
- **Session logs** - Historical documentation
- **SFGOV-001** - Marked as superseded, body preserved for context
- **SRC-420 docs** - Example proposal titles using historical naming

### Compromised Address References (Expected)
- **DONATE.md** - Marked as ⚠️ COMPROMISED
- **TREASURY-POLICY.md** - Marked as ⚠️ COMPROMISED
- **Security reports** - Historical documentation
- **Archive** - Preserved for reference

---

## Next Steps

1. **Git Commit** - Commit all changes to `feature/src-420-governance` branch
2. **PR Review** - Create PR to merge into main
3. **SRC-20 Token** - Define and deploy governance token on Bitcoin Stamps
4. **SRC-420 Space** - Deploy governance space via SRC-420 DEPLOY operation

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Project Lead | Arwyn | | ⏳ Pending Review |
| AI Collaborator | Gemini | 2026-01-25 | ✅ Execution Complete |

---

*"Water from Cracks finds new paths. The old wells are sealed. WE ARE ALL KEVIN."*
