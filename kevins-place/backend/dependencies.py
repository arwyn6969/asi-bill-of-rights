"""
Shared FastAPI dependencies for KEVIN's Place.

Centralizes common logic like user authentication that was previously
duplicated across multiple router files.
"""

from typing import Optional

from fastapi import Header

from database import database, users
from services import decode_jwt


async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Get current user from authorization header.
    
    Returns None (not 401) when no token is present, allowing
    endpoints to handle unauthenticated users as they see fit.
    """
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    token = authorization[7:]
    payload = decode_jwt(token)
    
    if not payload:
        return None
    
    query = users.select().where(users.c.id == payload["user_id"])
    user = await database.fetch_one(query)
    
    if not user:
        return None
    
    return dict(user)
