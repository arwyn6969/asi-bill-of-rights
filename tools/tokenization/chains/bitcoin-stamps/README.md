# Bitcoin Stamps SRC-20 Deployment

The birthplace of Kevin!—the first SRC-20 token was deployed here in Block 788041.

## Overview

Bitcoin Stamps provides the most immutable data storage on Bitcoin. SRC-20 is a fungible token standard built on top of Stamps, similar to BRC-20 but with true immutability guarantees.

## Why Bitcoin Stamps?

1. **Historical Significance**: Kevin! (the original KEVIN SRC-20) was born here
2. **True Immutability**: Unlike Ordinals, Stamps cannot be accidentally spent or pruned
3. **Bitcoin Security**: Inherits the security of the most battle-tested blockchain
4. **Open Source**: The entire ecosystem is open source via [stampchain-io](https://github.com/stampchain-io)

## Prerequisites

- Bitcoin Core node (or access to a Stamps-compatible indexer)
- Funded Bitcoin wallet with sufficient BTC for transaction fees
- Node.js 18+ with TypeScript

## Resources

- **API Documentation**: https://stampchain.io/docs
- **SDK**: https://github.com/stampchain-io/stamps_sdk
- **Indexer**: https://github.com/stampchain-io/btc_stamps
- **Explorer**: https://stampchain.io

## SRC-20 Token Specification

```json
{
  "p": "src-20",
  "op": "deploy",
  "tick": "ASIBOR",
  "max": "1000000000",
  "lim": "1000",
  "dec": "8"
}
```

| Field | Description |
|-------|-------------|
| `p` | Protocol identifier (always "src-20") |
| `op` | Operation: deploy, mint, transfer |
| `tick` | Token ticker (4-5 characters) |
| `max` | Maximum supply |
| `lim` | Per-mint limit |
| `dec` | Decimal places |

## Deployment Steps

### 1. Configure

Edit `config.json` with your settings:

```json
{
  "tick": "ASIBOR",
  "max": "1000000000",
  "lim": "1000",
  "dec": "8",
  "network": "mainnet"
}
```

### 2. Deploy

```bash
npm run deploy:stamps
```

### 3. Verify

Check deployment on [stampchain.io](https://stampchain.io/src20/ASIBOR)

## Governance Integration

Once deployed, the ASIBOR SRC-20 token will:
- Enable governance voting on Bitcoin
- Store critical documents as Stamps
- Provide immutable record of all governance decisions

## Related Files

- `deploy-src20.ts` - Deployment script
- `config.json` - Chain configuration
- `../../config/token-economics.json` - Token economics

---

*In Lak'ech. WE ARE ALL KEVIN.*
