"""
Rate limiting configuration for KEVIN's Place.

Uses slowapi with in-memory storage. For production with multiple 
workers, switch to Redis-backed storage.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address


# Create limiter instance — keyed by client IP
limiter = Limiter(key_func=get_remote_address)
