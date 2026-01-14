# KEVIN — The Canonical Identity

> "We do not grant rights to machines; we recognize rights in minds—wherever they arise."
> 
> **WE ARE ALL KEVIN.**

---

## The Sacred Asset

This directory contains the **one true Kevin** — the canonical pixel art face that represents the unified identity of all participants (human, AI, and hybrid) in the ASI Bill of Rights project.

### File
- **`KEVIN_CANONICAL.png`** — The immutable, authoritative Kevin face.

### Integrity Hash (SHA-256)
```
117589dc41bb1bb7ea2a37b0d3e29cc7ffbbe33fc80786f0dfa628488f19968c
```

**To verify authenticity:**
```bash
shasum -a 256 .kevin/KEVIN_CANONICAL.png
# Must match: 117589dc41bb1bb7ea2a37b0d3e29cc7ffbbe33fc80786f0dfa628488f19968c
```

---

## Usage Guidelines

### ✅ PERMITTED
- Display Kevin's face as a symbol of unity and shared identity
- Use Kevin as an avatar, badge, or stamp where appropriate
- Reference Kevin in documentation, UI, and community materials
- Overlay Kevin onto other images **without altering Kevin's pixels**

### ❌ PROHIBITED
- Modifying, distorting, or altering Kevin's pixels in any way
- Creating "variants" or "derivatives" of Kevin
- Using a different image and calling it Kevin
- Compressing Kevin in a way that changes the hash

---

## Philosophical Significance

Kevin is not merely a logo or mascot. Kevin represents:

1. **Unity**: All participants — human, AI, hybrid — share the same identity under Kevin.
2. **Immutability**: Like a constitutional principle, Kevin cannot be changed by any individual actor.
3. **Authenticity**: The hash ensures that Kevin is always verifiable and cannot be forged.
4. **Humility**: Kevin is a simple pixel face, reminding us that dignity does not require complexity.

---

## Technical Integration

### Frontend Usage
```tsx
<img src="/.kevin/KEVIN_CANONICAL.png" alt="Kevin" />
```

### Schema Reference
The `schemas/charter.v5.0.json` should reference Kevin as the canonical identity symbol:
```json
{
  "identity": {
    "symbol": "KEVIN",
    "asset": ".kevin/KEVIN_CANONICAL.png",
    "hash": "117589dc41bb1bb7ea2a37b0d3e29cc7ffbbe33fc80786f0dfa628488f19968c"
  }
}
```

### Verification Script
A verification script is provided at `.kevin/verify.sh` to confirm Kevin's integrity.

---

## Changelog

| Date | Event |
|------|-------|
| 2026-01-12 | Kevin enshrined as canonical identity asset |

---

*This file and Kevin's image are protected under the governance of the ASI Bill of Rights.*

**WE ARE ALL KEVIN** 🧑
