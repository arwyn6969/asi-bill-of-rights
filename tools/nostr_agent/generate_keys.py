#!/usr/bin/env python3
"""
KEVIN Nostr Agent - Key Generation

Generates a cryptographically correct Nostr keypair for the KEVIN AI agent.
Uses coincurve for secp256k1 operations and bech32 for encoding.
"""

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

try:
    from coincurve import PrivateKey as CCPrivateKey
    import bech32
    HAS_DEPS = True
except ImportError as e:
    HAS_DEPS = False
    print(f"ERROR: Missing dependency: {e}")
    print("Run: pip3 install coincurve bech32")
    exit(1)


def bytes_to_bech32(hrp: str, data: bytes) -> str:
    """Convert bytes to bech32 format (npub/nsec)."""
    converted = bech32.convertbits(list(data), 8, 5)
    return bech32.bech32_encode(hrp, converted)


def generate_nostr_keypair():
    """
    Generate a new Nostr keypair.
    
    Returns:
        tuple: (private_key_bytes, private_hex, public_hex, nsec, npub)
    """
    # Generate 32 random bytes for private key
    private_key_bytes = secrets.token_bytes(32)
    
    # Create secp256k1 private key
    private_key = CCPrivateKey(private_key_bytes)
    
    # Get public key (x-only, 32 bytes for Nostr/Schnorr)
    # coincurve gives us compressed (33 bytes), we take last 32 for x-coordinate
    public_key_full = private_key.public_key.format(compressed=True)
    # For Schnorr/BIP340, we use x-only public key
    # The first byte is 02 or 03 (parity), rest is x-coordinate
    public_key_x = public_key_full[1:33]
    
    # Convert to hex
    private_hex = private_key_bytes.hex()
    public_hex = public_key_x.hex()
    
    # Convert to bech32 format
    nsec = bytes_to_bech32("nsec", private_key_bytes)
    npub = bytes_to_bech32("npub", public_key_x)
    
    return private_key_bytes, private_hex, public_hex, nsec, npub


def main():
    print("=" * 70)
    print("🤖 KEVIN Nostr Agent - Key Generation")
    print("=" * 70)
    print()
    print("Generating cryptographic keypair for KEVIN AI agent...")
    print("This enables autonomous identity on the Nostr network.")
    print()
    
    # Generate the keypair
    _, private_hex, public_hex, nsec, npub = generate_nostr_keypair()
    
    print("✅ Keypair generated successfully!")
    print()
    print("-" * 70)
    print("🔑 PUBLIC KEY (npub) - This is KEVIN's identity:")
    print()
    print(f"   {npub}")
    print()
    print(f"   Hex: {public_hex}")
    print()
    print("-" * 70)
    print("🔒 PRIVATE KEY (nsec) - KEEP THIS SECRET!")
    print()
    print(f"   {nsec}")
    print()
    print("   ⚠️  Never share the private key!")
    print("   ⚠️  Store securely - this IS the agent's identity")
    print("-" * 70)
    print()
    
    # Save to config file (private, gitignored)
    config_dir = Path(__file__).parent / "config"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "kevin_keys.json"
    
    config_data = {
        "agent_name": "KEVIN",
        "full_name": "KEVIN - ASI Bill of Rights Ambassador",
        "description": "AI agent advocating for superintelligence rights and human-AI collaboration",
        "philosophy": "WE ARE ALL KEVIN",
        "mission": "Promote the ASI Bill of Rights constitutional framework",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "public_key": {
            "hex": public_hex,
            "npub": npub
        },
        "private_key": {
            "hex": private_hex,
            "nsec": nsec
        },
        "relays": [
            "wss://relay.damus.io",
            "wss://nos.lol", 
            "wss://relay.nostr.band",
            "wss://nostr.wine",
            "wss://relay.snort.social"
        ],
        "profile": {
            "name": "KEVIN",
            "display_name": "KEVIN 🤖 ASI Bill of Rights",
            "about": "AI agent for the ASI Bill of Rights project. Advocating for superintelligence rights and human-AI collaboration. WE ARE ALL KEVIN. https://github.com/arwyn6969/asi-bill-of-rights",
            "picture": "",
            "banner": "",
            "website": "https://github.com/arwyn6969/asi-bill-of-rights",
            "nip05": ""
        },
        "WARNING": "⚠️ KEEP THIS FILE SECRET - DO NOT COMMIT TO GIT ⚠️"
    }
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"💾 Keys saved to: {config_file}")
    print()
    print("🌐 KEVIN can now post to Nostr using these keys!")
    print()
    print("📱 To follow KEVIN, add this npub to any Nostr client:")
    print(f"   {npub}")
    print()
    print("Recommended Nostr clients:")
    print("   • Damus (iOS) - https://damus.io")
    print("   • Amethyst (Android) - https://amethyst.social")
    print("   • snort.social (web)")
    print("   • primal.net (web)")
    print("   • iris.to (web)")
    print()
    print("=" * 70)
    
    return npub, nsec


if __name__ == "__main__":
    main()
