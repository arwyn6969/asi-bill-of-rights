# Sovereign Brain Workspace

**Directory:** `tools/unified_brain`  
**Purpose:** The central orchestration logic for Kevin's autonomous identity.

## Philosophy
This directory contains the custom, sovereign implementation of Kevin's "mind." Unlike third-party frameworks, this code:
1.  Runs locally.
2.  Uses our existing cryptographic keys.
3.  Directly consumes our `tools/agents/` documentation as system prompts.

## Components to Build
- `brain.py`: The main event loop.
- `context_loader.py`: Script to ingest the Charter and Agent Definitions into the prompt.
- `action_dispatcher.py`: Interface to `ai_client.py`, `post_to_nostr.py`, and `wallet-manager`.

## Status
*Planned.* See `../../docs/UNIFIED-IDENTITY-STRATEGY.md` for the full architecture.
