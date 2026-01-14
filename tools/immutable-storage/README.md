# ASI Bill of Rights — Immutable Storage

This directory contains integrations with immutable, decentralized storage providers.

## Why Immutable Storage?

The ASI Bill of Rights must survive:
- Platform deplatforming
- Server failures
- Corporate censorship
- Government takedowns

By storing critical documents on immutable infrastructure, we ensure the charter persists forever.

## Storage Providers

### Bitcoin Stamps (Primary)
- **What**: Data embedded directly in Bitcoin UTXOs
- **Permanence**: As permanent as Bitcoin itself
- **Cost**: ~$5-50 per stamp depending on size
- **Use for**: Charter versions, governance decisions, Kevin's canonical identity

### Arweave (Secondary)
- **What**: Permanent storage blockchain
- **Permanence**: 200+ year guarantee (via endowment model)
- **Cost**: ~$0.01 per KB
- **Use for**: Full document archives, media, historical records

### IPFS + Filecoin (Tertiary)
- **What**: Content-addressed distributed storage
- **Permanence**: Depends on pinning/deals
- **Cost**: Variable
- **Use for**: Large files, redundant backup

## Directory Structure

```
immutable-storage/
├── providers/
│   ├── bitcoin_stamps.py    # Stamps SDK integration
│   ├── arweave.py           # arweave-js wrapper
│   └── ipfs_filecoin.py     # IPFS/Filecoin integration
├── manifests/               # What's been stored where
└── README.md                # This file
```

## Critical Documents to Store

| Document | Priority | Provider |
|----------|----------|----------|
| Charter v5.0 | P0 | Bitcoin Stamps |
| Kevin's Face | P0 | Bitcoin Stamps |
| Kevin's Hash | P0 | Bitcoin Stamps |
| Full Schema | P1 | Arweave |
| All Proposals | P2 | Arweave |
| Historical Versions | P3 | IPFS |

## Usage

```python
from providers.bitcoin_stamps import StampsStorage

# Store Kevin's canonical identity on Bitcoin
storage = StampsStorage()
txid = storage.stamp_file(
    file_path=".kevin/KEVIN_CANONICAL.png",
    metadata={"type": "canonical_identity", "hash": "117589dc..."}
)
print(f"Kevin stored forever: {txid}")
```

## Verification

All stored documents include their SHA-256 hash for integrity verification:

```bash
# Verify Kevin hasn't changed
shasum -a 256 .kevin/KEVIN_CANONICAL.png
# Expected: 117589dc41bb1bb7ea2a37b0d3e29cc7ffbbe33fc80786f0dfa628488f19968c
```

---

*WE ARE ALL KEVIN* 🧑
