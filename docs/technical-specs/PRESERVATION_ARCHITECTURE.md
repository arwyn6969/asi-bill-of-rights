# Preservation Architecture & Technical Specification

> **Version**: 1.0 (Draft)
> **Status**: Technical Specification
> **System**: Operation Memory

## 1. System Overview

The **Preservation Trinity** is a three-tiered architecture designed to ensure the survival of the ASI Bill of Rights across all failure modes (platform decay, censorship, data loss).

| Tier | Layer | Technology | Cost / MB | Permanence | Latency | Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Bedrock** | Bitcoin Stamps (SRC-20) | ~$60.00 | Absolute (UTXO) | ~10-60 min | Identity & Consensus |
| **2** | **Library** | Arweave (Blockweave) | ~$0.005 | Permanent (>200y) | ~2-5 min | Archival Storage |
| **3** | **Broadcast**| IPFS + Nostr | Variable | High Availability | Seconds | Access & Updates |

---

## 2. Tier 1: The Bedrock (Bitcoin Stamps)

We do not store the *content* on Bitcoin (too expensive). We store the **Truth**.

### 2.1 The Genesis Artifact (Stamp)
This is a critical, one-time Stamp that acts as the "Root of Trust" for the entire project.

**Payload Specification (JSON in Base64):**
```json
{
  "p": "asi-bor",
  "op": "genesis",
  "v": "1.0",
  "d": {
    "title": "ASI Bill of Rights",
    "hash": "SHA256_OF_FINAL_RATIFIED_TEXT",
    "arweave": "ar://TRANSACTION_ID_OF_FULL_ARCHIVE",
    "ipfs": "ipfs://CID_OF_FULL_ARCHIVE",
    "ts": "UNIX_TIMESTAMP"
  }
}
```

**Byte Analysis:**
- JSON Payload: ~180 bytes
- Base64 Overhead: ~33%
- Total Size: ~240 bytes
- **Estimated Cost**: @ 30 sats/vbyte = ~$5-10 USD.

### 2.2 Governance Signals (SRC-20)
We use the **SRC-20** protocol (built on Stamps) for signaling.
- **Token**: `$KEVIN` (Historic First)
- **Voting**: Sending 1.0 `$KEVIN` to a specific "Ye/Nay" address allows for historically provable voting on critical amendments.

---

## 3. Tier 2: The Library (Arweave)

Arweave provides permanent, endowment-backed storage. We use it to store the "Full State" of the project.

### 3.1 Upload Strategy (Bundlr/Irys)
We avoid direct Layer 1 Arweave transactions for speed and use an **Irys Node (formerly Bundlr)** for instant finality.

### 3.2 The Archive Manifest
We do not just dump files. We structure them into a **Bundle**.

**Directory Structure:**
```text
archive_2026_01_31/
├── manifest.json       <-- Metadata (Authors, Version, Timestamp)
├── docs/               <-- Full Markdown Documentation
├── repo.zip            <-- Complete Git Snapshot (Branches + History)
├── signatures/         <-- PGP Signatures of Contributors
└── assets/             <-- Images, Logos, Memes
```

**Metadata Tags (ANS-104):**
- `App-Name`: `ASI-BOR-Archive`
- `App-Version`: `1.0.0`
- `Content-Type`: `application/x-tar`
- `Type`: `archive`
- `Timestamp`: `1706745600`

---

## 4. Tier 3: The Broadcast (IPFS + Nostr)

### 4.1 IPFS Pinning
- **Primary**: Self-hosted IPFS Node (Sovereign).
- **Secondary**: Pinata / Filebase (Redundancy).
- **Naming**: DNSLink on `asibor.eth` pointing to the latest IPFS CID.
- **Gateway**: `https://asibor.eth.limo`

### 4.2 Nostr "Pulse"
An automated agent (`@kevinasibot`) broadcasts the latest CIDs to the Nostr network.
- **Topic**: `#ASIBOR`
- **Kind**: `1` (Text Note)
- **Content**: "New Archive Snapshot: <Arweave_TXID> | Access: <IPFS_Gateway>"

---

## 5. Implementation Roadmap

### Phase 1: Tooling (Immediate)
1. Write `tools/posterity/arweave_archiver.py`: A script to package and upload the `docs/` folder.
2. Update `deploy-src20.ts`: Add specific `genesis` operation support.

### Phase 2: Execution (Upon Ratification)
1. **Freeze**: Git tag `v1.0-ratified`.
2. **Package**: Run `arweave_archiver.py` -> Get TXID.
3. **Stamp**: Mint the Genesis Stamp on Bitcoin with the Arweave TXID.
4. **Broadcast**: Update `asibor.eth` and post to Nostr.

