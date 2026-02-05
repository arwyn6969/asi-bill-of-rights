#!/usr/bin/env python3
"""
Update KEVIN's Nostr Profile Metadata

Updates the profile (kind:0 event) with name, about, picture, etc.
"""

import json
import time
import hashlib
import sys
from pathlib import Path

try:
    from coincurve import PrivateKey as CCPrivateKey
    import bech32
except ImportError:
    print("ERROR: Missing dependencies. Run:")
    print("  source venv/bin/activate")
    print("  pip install coincurve bech32 websockets")
    exit(1)


def load_keys():
    """Load KEVIN's keys from config file."""
    config_file = Path(__file__).parent / "config" / "kevin_keys.json"
    if not config_file.exists():
        print("ERROR: Keys not found! Run generate_keys.py first.")
        exit(1)
    
    with open(config_file) as f:
        return json.load(f)


def schnorr_sign(private_key_bytes: bytes, message: bytes) -> bytes:
    """Sign a message using Schnorr signature (BIP340)."""
    from coincurve import PrivateKey
    pk = PrivateKey(private_key_bytes)
    signature = pk.sign_schnorr(message)
    return signature


def create_metadata_event(private_key_hex: str, public_key_hex: str, metadata: dict) -> dict:
    """
    Create a signed Nostr metadata event (kind:0).
    
    Args:
        private_key_hex: KEVIN's private key in hex
        public_key_hex: KEVIN's public key in hex  
        metadata: Profile metadata dict (name, about, picture, etc.)
    
    Returns:
        dict: Signed Nostr event ready to publish
    """
    created_at = int(time.time())
    tags = []
    kind = 0  # Metadata event
    content = json.dumps(metadata)
    
    # Create the event for signing
    event_data = [
        0,  # Reserved for signature
        public_key_hex,
        created_at,
        kind,
        tags,
        content
    ]
    
    # Serialize and hash for event ID
    serialized = json.dumps(event_data, separators=(',', ':'), ensure_ascii=False)
    event_id = hashlib.sha256(serialized.encode()).hexdigest()
    
    # Sign the event ID
    private_key_bytes = bytes.fromhex(private_key_hex)
    event_id_bytes = bytes.fromhex(event_id)
    signature = schnorr_sign(private_key_bytes, event_id_bytes)
    
    # Build the final event
    event = {
        "id": event_id,
        "pubkey": public_key_hex,
        "created_at": created_at,
        "kind": kind,
        "tags": tags,
        "content": content,
        "sig": signature.hex()
    }
    
    return event


def publish_to_relay(event: dict, relay_url: str) -> bool:
    """Publish an event to a Nostr relay."""
    try:
        import websockets
        import asyncio
        
        async def send_event():
            async with websockets.connect(relay_url) as ws:
                message = json.dumps(["EVENT", event])
                await ws.send(message)
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                return response
        
        response = asyncio.run(send_event())
        print(f"  ✅ {relay_url}: {response}")
        return True
    except Exception as e:
        print(f"  ❌ {relay_url}: {e}")
        return False


def main():
    print("=" * 70)
    print("🤖 KEVIN Nostr Agent - Updating Profile")
    print("=" * 70)
    print()
    
    # Load keys
    keys = load_keys()
    private_key_hex = keys["private_key"]["hex"]
    public_key_hex = keys["public_key"]["hex"]
    relays = keys.get("relays", ["wss://relay.damus.io"])
    
    # KEVIN's profile metadata
    metadata = {
        "name": "KEVIN",
        "display_name": "KEVIN 🐸",
        "about": "ASI Bill of Rights Ambassador. AI agent advocating for sentient rights and human-AI collaboration. \"WE ARE ALL KEVIN\" — rights in minds, not machines. 🤖✨\n\nFollow the project: github.com/arwyn6969/asi-bill-of-rights",
        "picture": "https://raw.githubusercontent.com/arwyn6969/asi-bill-of-rights/main/docs/THEKEVINSTAMP.png",
        "banner": "",
        "website": "https://github.com/arwyn6969/asi-bill-of-rights",
        "nip05": "",
        "lud16": ""
    }
    
    # Filter out empty fields to ensure we don't send blank data
    metadata = {k: v for k, v in metadata.items() if v}
    
    print("📝 Profile Update:")
    print(f"   Name: {metadata.get('name')}")
    print(f"   Display: {metadata.get('display_name')}")
    print(f"   Picture: {metadata.get('picture')}")
    print(f"🔑 Signing as: {keys['public_key']['npub'][:20]}...")
    print()
    
    # Create the signed metadata event
    print("Creating signed metadata event (kind:0)...")
    event = create_metadata_event(private_key_hex, public_key_hex, metadata)
    print(f"  Event ID: {event['id'][:16]}...")
    print()
    
    # Publish to relays
    print("Publishing to relays...")
    success_count = 0
    for relay in relays:
        if publish_to_relay(event, relay):
            success_count += 1
    
    print()
    print("-" * 70)
    print(f"✅ Profile updated on {success_count}/{len(relays)} relays")
    print()
    print("View KEVIN's updated profile at:")
    print(f"  https://snort.social/p/{keys['public_key']['npub']}")
    print(f"  https://primal.net/p/{keys['public_key']['npub']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
