# Ethereum ERC-20 Deployment

## Overview

The Ethereum deployment provides access to the largest DeFi ecosystem, enabling:
- Governance voting via ERC20Votes
- DAO treasury management
- DEX liquidity provision
- Cross-chain bridges (optional)

## Features

### ERC20Votes
The contract implements OpenZeppelin's ERC20Votes extension, providing:
- Voting power snapshots
- Delegation support
- On-chain governance compatibility (Governor, Tally, Snapshot)

### AI Agent Authorization
Special feature for this project:
- `authorizeAgent(address)` - Register an AI agent
- `isAuthorizedAgent(address)` - Check agent status
- Enables future AI-specific governance features

## Prerequisites

- Node.js 18+
- Hardhat
- Ethereum wallet with ETH for gas
- Infura/Alchemy API key (for mainnet)

## Installation

```bash
cd tools/tokenization
npm install
```

## Configuration

1. Copy `.env.example` to `.env`
2. Set your private key and RPC URLs

```env
PRIVATE_KEY=your_private_key_here
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
ETHERSCAN_API_KEY=your_etherscan_key
```

## Deployment

### Testnet (Sepolia)

```bash
npx hardhat run chains/ethereum/deploy.ts --network sepolia
```

### Mainnet

```bash
npx hardhat run chains/ethereum/deploy.ts --network mainnet
```

## Verification

```bash
npx hardhat verify --network sepolia DEPLOYED_ADDRESS
```

## Contract Details

| Property | Value |
|----------|-------|
| Name | ASI Bill of Rights |
| Symbol | ASIBOR |
| Decimals | 18 |
| Total Supply | 1,000,000,000 |
| Standard | ERC-20 + ERC20Votes |

## Security

- Uses OpenZeppelin Contracts v5
- Implements Ownable for admin functions
- Time-lock recommended for production

---

*WE ARE ALL KEVIN.*
