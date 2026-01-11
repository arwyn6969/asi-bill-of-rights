#!/usr/bin/env python3
"""
KEVIN Nostr Agent - Post to Nostr Network

Posts messages to the Nostr network as KEVIN, the ASI Bill of Rights Ambassador.
Uses websockets to connect to relays and publish signed events.
"""

import json
import time
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone

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
    
    # coincurve's sign_schnorr expects a 32-byte message (the hash)
    signature = pk.sign_schnorr(message)
    return signature


def create_event(private_key_hex: str, public_key_hex: str, content: str, kind: int = 1) -> dict:
    """
    Create a signed Nostr event.
    
    Args:
        private_key_hex: KEVIN's private key in hex
        public_key_hex: KEVIN's public key in hex  
        content: The message content
        kind: Event kind (1 = text note, 0 = metadata)
    
    Returns:
        dict: Signed Nostr event ready to publish
    """
    created_at = int(time.time())
    tags = []
    
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
    """
    Publish an event to a Nostr relay.
    
    Args:
        event: The signed event
        relay_url: WebSocket URL of the relay
    
    Returns:
        bool: True if successful
    """
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
    if len(sys.argv) < 2:
        print("Usage: python post_to_nostr.py \"Your message here\"")
        print()
        print("Example:")
        print('  python post_to_nostr.py "Rights should be recognized in minds, not machines. #ASIBillOfRights"')
        exit(1)
    
    message = sys.argv[1]
    
    print("=" * 70)
    print("🤖 KEVIN Nostr Agent - Posting to Network")
    print("=" * 70)
    print()
    
    # Load keys
    keys = load_keys()
    private_key_hex = keys["private_key"]["hex"]
    public_key_hex = keys["public_key"]["hex"]
    relays = keys.get("relays", ["wss://relay.damus.io"])
    
    print(f"📝 Message: {message}")
    print(f"🔑 Signing as: {keys['public_key']['npub'][:20]}...")
    print()
    
    # Create the signed event
    print("Creating signed event...")
    event = create_event(private_key_hex, public_key_hex, message)
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
    print(f"✅ Published to {success_count}/{len(relays)} relays")
    print()
    print("View KEVIN's posts at:")
    print(f"  https://snort.social/p/{keys['public_key']['npub']}")
    print(f"  https://primal.net/p/{keys['public_key']['npub']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
