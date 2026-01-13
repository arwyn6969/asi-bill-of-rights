"""
Services package for KEVIN's Place.
"""

from .auth import (
    generate_uuid,
    hash_password,
    verify_password,
    create_jwt,
    decode_jwt,
    get_badge,
)
from .crypto import (
    pubkey_to_npub,
    verify_signature,
    HAS_CRYPTO,
)

__all__ = [
    "generate_uuid",
    "hash_password",
    "verify_password",
    "create_jwt",
    "decode_jwt",
    "get_badge",
    "pubkey_to_npub",
    "verify_signature",
    "HAS_CRYPTO",
]
