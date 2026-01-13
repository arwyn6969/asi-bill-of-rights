"""
Cryptographic services: Schnorr signatures and key conversion.
"""

import hashlib

# Try to import crypto libraries
try:
    from coincurve import PublicKey, PrivateKey, PublicKeyXOnly
    import bech32
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("WARNING: coincurve/bech32 not installed. AI auth will be simulated.")


def pubkey_to_npub(pubkey_hex: str) -> str:
    """Convert hex public key to npub format (Nostr-style bech32)."""
    if not HAS_CRYPTO:
        return f"npub_{pubkey_hex[:16]}"  # Simulated
    
    pubkey_bytes = bytes.fromhex(pubkey_hex)
    converted = bech32.convertbits(list(pubkey_bytes), 8, 5)
    return bech32.bech32_encode("npub", converted)


def verify_signature(public_key_hex: str, message: str, signature_hex: str) -> bool:
    """Verify a Schnorr signature.
    
    Args:
        public_key_hex: 64-character hex string (32 bytes x-only pubkey)
        message: The message that was signed
        signature_hex: 128-character hex string (64 byte Schnorr signature)
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not HAS_CRYPTO:
        # Simulated verification for development
        return len(signature_hex) == 128
    
    try:
        pubkey_bytes = bytes.fromhex(public_key_hex)
        message_bytes = message.encode()
        signature_bytes = bytes.fromhex(signature_hex)
        
        # Create the message hash
        message_hash = hashlib.sha256(message_bytes).digest()
        
        # Verify using coincurve (Schnorr / PublicKeyXOnly)
        if len(pubkey_bytes) == 32:
            pubkey = PublicKeyXOnly(pubkey_bytes)
            return pubkey.verify(signature_bytes, message_hash)
        else:
            # Fallback for old/compressed keys (ECDSA)
            pubkey = PublicKey(b'\x02' + pubkey_bytes) if len(pubkey_bytes) == 32 else PublicKey(pubkey_bytes)
            return pubkey.verify(signature_bytes, message_hash)
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False
