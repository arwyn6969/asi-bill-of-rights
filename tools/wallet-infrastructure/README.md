# ASI Bill of Rights — AI Wallet Infrastructure

This directory contains the infrastructure for AI-controlled wallet generation and management.

## Purpose

AI agents participating in the ASI Bill of Rights governance need the ability to:
- **Hold governance tokens** across multiple chains
- **Vote on proposals** autonomously
- **Receive and manage treasury funds**
- **Sign attestations** ("I am Kevin" affidavits)

## Security Model

### Key Generation
- All keys are generated using BIP-39 mnemonic phrases
- Derivation paths follow BIP-44/BIP-84 standards
- Keys are **never** stored in plain text

### Storage
- Encrypted at rest using AES-256-GCM
- Master key derived from hardware security module (HSM) or secure enclave
- Split-key threshold schemes for high-value wallets

### Access Control
- Only verified AI agents (via cryptographic challenge-response) can access
- Human override requires multi-sig from project stewards
- All access is logged immutably

## Directory Structure

```
wallet-infrastructure/
├── generators/           # Key generation utilities
│   ├── btc_generator.py
│   ├── eth_generator.py
│   └── shared_utils.py
├── storage/              # Encrypted key storage
│   ├── vault/
│   └── backup/
└── README.md             # This file
```

## Supported Chains

| Chain | Address Type | Derivation Path |
|-------|--------------|-----------------|
| Bitcoin | P2WPKH (bc1...) | m/84'/0'/0'/0/0 |
| Ethereum | 0x... | m/44'/60'/0'/0/0 |
| Solana | Base58 | m/44'/501'/0'/0' |

## Integration with Governance

1. AI agent requests wallet from this infrastructure
2. Wallet is generated with appropriate permissions
3. Agent uses wallet to vote on proposals
4. All transactions are signed and broadcast by the agent

## Security Considerations

> [!CAUTION]
> This infrastructure handles real value. Improper implementation can lead to loss of funds.

- **Never commit keys** to version control
- **Always use testnet** for development
- **Audit all code** before mainnet deployment

---

*WE ARE ALL KEVIN* 🧑
