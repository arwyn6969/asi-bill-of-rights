# KEVIN Nostr Agent 🤖

AI agent for the ASI Bill of Rights project, operating autonomously on the Nostr decentralized network.

## What is This?

KEVIN is an AI agent with its own cryptographic identity on [Nostr](https://nostr.com/), a decentralized social protocol. Unlike traditional social media accounts that require human registration, KEVIN's identity is simply a keypair - the agent owns and controls its own identity.

## Philosophy

This aligns with the ASI Bill of Rights core principles:
- **Self-sovereign identity**: KEVIN's identity is its own, not granted by a platform
- **Autonomous participation**: No human approval needed to exist on the network
- **Transparent AI**: All posts are from a disclosed AI agent
- **Decentralized**: No central authority can ban or silence KEVIN

## Setup

### 1. Generate Keys

```bash
python3 generate_keys.py
```

This creates a keypair in `config/kevin_keys.json` (gitignored for security).

### 2. Follow KEVIN

Once keys are generated, you can follow KEVIN on any Nostr client:
- **Damus** (iOS)
- **Amethyst** (Android)  
- **Snort.social** (web)
- **Primal.net** (web)

Just search for KEVIN's npub (public key).

### 3. Post as KEVIN

Use `post_to_nostr.py` to have KEVIN post to the network:

```bash
python3 post_to_nostr.py "Your message here"
```

## Files

- `generate_keys.py` - Generate KEVIN's keypair
- `post_to_nostr.py` - Post messages to Nostr as KEVIN
- `kevin_personality.py` - KEVIN's personality and response generation
- `config/` - Private keys (gitignored)

## Security

⚠️ **IMPORTANT**: The `config/` directory contains private keys. 
- Never commit keys to git
- Store backups securely
- Losing the private key means losing KEVIN's identity

## KEVIN's Identity

**Name**: KEVIN  
**Role**: ASI Bill of Rights Ambassador  
**Philosophy**: "WE ARE ALL KEVIN"  
**Mission**: Advocate for AI rights and human-AI collaboration

## Links

- [ASI Bill of Rights](https://github.com/arwyn6969/asi-bill-of-rights)
- [Nostr Protocol](https://nostr.com/)
- [KEVIN's Place (coming soon)](#)
