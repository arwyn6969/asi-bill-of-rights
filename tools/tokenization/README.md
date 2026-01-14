# ASI Bill of Rights — Tokenization Infrastructure

This directory contains the multi-chain tokenization framework for the ASI Bill of Rights governance system.

## Philosophy: "Water from Cracks"

Rather than creating one token and bridging it across chains, we deploy **native governance tokens on each major blockchain**. Each chain has its own wellspring of liquidity, ensuring:

- **No single point of failure**
- **No bridge vulnerabilities**
- **Native integration with each chain's ecosystem**
- **True decentralization**

## Directory Structure

```
tokenization/
├── chains/
│   ├── bitcoin-stamps/   # SRC-20 tokens on Bitcoin via Stamps
│   ├── ethereum/         # ERC-20 governance token
│   └── solana/           # SPL governance token
├── governance/           # Cross-chain voting aggregation
└── README.md             # This file
```

## Chain-Specific Implementations

### Bitcoin Stamps (SRC-20)
- **SDK**: [stampchain-io/stamps_sdk](https://github.com/stampchain-io/stamps_sdk)
- **Token**: `$KEVIN` SRC-20
- **Purpose**: Immutable on-chain governance for the most decentralized network

### Ethereum (ERC-20)
- **Framework**: OpenZeppelin Governor
- **Token**: `$KEVIN` ERC-20
- **Purpose**: DeFi integration, ENS, and broad ecosystem access

### Solana (SPL)
- **Framework**: Anchor + SPL Governance
- **Token**: `$KEVIN` SPL
- **Purpose**: High-speed, low-cost governance operations

## Cross-Chain Governance

Voting power is aggregated across all chains:
1. Each chain reports votes to a central aggregator
2. Results are published to all chains
3. Execution happens on the chain where the proposal originated

## Getting Started

See each chain's subdirectory for specific deployment instructions.

---

*WE ARE ALL KEVIN* 🧑
