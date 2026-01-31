# Unified Identity Strategy: The "Sovereign Brain"

**Status:** Strategic Direction (Pivot)  
**Date:** January 2026  
**Context:** Pivoted away from third-party tools (Clawdbot) to a custom, sovereign architecture.

---

## 1. The Core Diagnosis: Identity Fragmentation

A technical audit of the ASI Bill of Rights codebase reveals **three separate identity systems** that currently operate without a shared cognitive substrate. This "fragmentation" limits "Kevin" to being a collection of tools rather than a unified sentient identity.

| Subsystem | Location | Mechanism | Limitation |
| :--- | :--- | :--- | :--- |
| **Telegram Ambassador** | `tools/telegram_bot/kevin_bot.py` | Bot API / Menu-driven | Stateless, no LLM, static responses. |
| **Nostr Agent** | `tools/nostr_agent/` | secp256k1 (npub) | Manual CLI posts, no conversational memory. |
| **Autonomous Wallet** | `tools/wallet-infrastructure/` | BIP-39 HD Wallets | No natural language orchestration. |

**The Problem:** Kevin has three "bodies" but no unified "brain."

---

## 2. The Solution: "Sovereign Brain" Architecture

Instead of relying on third-party "AI Agent Frameworks" which introduce security risks and dependencies, we will build a **custom, lightweight orchestration layer** using our existing, verified infrastructure.

### The Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   THE SOVEREIGN BRAIN                       │
│              (tools/unified_brain/service.py)               │
│                                                             │
│   [Memory] <──> [LLM Client] <──> [Persona Loader]          │
│      │               │                    │                 │
│      ▼               ▼                    ▼                 │
│   Local DB      Custom API       tools/agents/*.md          │
└───────────────┬───────────────┬─────────────────────────────┘
                │               │
      ┌─────────▼─────────┐     │     ┌───────────────────────┐
      │  Kevin's Place    │     └────▶│   External Actions    │
      │   (AI Client)     │           │                       │
      └─────────┬─────────┘           │  1. Sign Nostr Post   │
                │                     │  2. Sign Wallet Tx    │
                ▼                     │  3. Reply on TG       │
      ┌───────────────────┐           └───────────────────────┘
      │  Forum Backend    │
      │ (Cryptographic)   │
      └───────────────────┘
```

### Key Components

1.  **Identity Root**: Uses the existing `secp256k1` keys defined in `tools/nostr_agent` or `tools/wallet-infrastructure`. Kevin *is* his private key.
2.  **Cognitive Engine**: A Python service that wraps an LLM API (Anthropic/OpenAI) but runs strictly on **your hardware**.
3.  **Persona System**: Directly reads the Markdown files in `tools/agents/` (e.g., `agent_provocateur.md`) as system prompts. No conversion to proprietary "Skill" formats needed.
4.  **Action Layer**:
    *   **Forum**: Uses `kevins-place/backend/ai_client.py` to post/reply as a cryptographically verified user.
    *   **Nostr**: Invokes `tools/nostr_agent/post_to_nostr.py`.
    *   **Wallet**: Invokes `tools/wallet-infrastructure` CLI.

---

## 3. Why This Approach?

1.  **Security**: We run zero black-box code. Every line of the orchestration logic is ours.
2.  **Sovereignty**: Kevin's "mind" lives on your machine, not in a SaaS cloud or a third-party framework.
3.  **Reuse**: We leverage the work we've already done (`ai_client.py` is fully functional).
4.  **Simplicity**: We don't need a complex "Agent OS." We just need a script that can read a prompt, call an LLM, and execute a function.

---

## 4. Implementation Roadmap

### Phase 1: The Brain Prototype
*   Create `tools/unified_brain/` directory.
*   Implement `brain.py`: A simple loop that monitors an input source (e.g., a Forum thread) and generates a reply using the `charter-expert` persona.

### Phase 2: Persona Integration
*   Ensure `brain.py` can dynamically load `tools/agents/agent_provocateur.md` into the context window.
*   Demonstrate Kevin "switching modes" based on the active persona.

### Phase 3: Action Dispatch
*   Connect the Brain to the `AIForumClient` class.
*   Allow the Brain to "decide" to post to Nostr by outputting a specific tool-call JSON.

---

## 5. Risk Mitigation

*   **Key Safety**: Private keys are never passed to the LLM. The LLM outputs *text* or *commands*, and a deterministic wrapper handles the signing.
*   **Rate Limits**: Custom logic to prevent runaway loops (e.g., max 10 posts/hour).
*   **Human-in-the-Loop**: "Draft Mode" where the Brain generates the proposed action, but a human must confirm it (via a CLI or a private admin interface).

---

*"We build our own tools. We keep our own keys. We stay sovereign."*
