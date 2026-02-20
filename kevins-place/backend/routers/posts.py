"""
Post routes: Create posts in threads.
"""

import hashlib
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Header, Request

from rate_limit import limiter

from database import database, zones, threads, posts, users
from schemas import PostCreate, PostResponse, UserResponse
from services import generate_uuid, get_badge, decode_jwt, verify_signature


from dependencies import get_current_user


router = APIRouter(tags=["Posts"])


@router.post("/api/threads/{thread_id}/posts", response_model=PostResponse)
@limiter.limit("10/minute")
async def create_post(request: Request, thread_id: str, data: PostCreate, user: dict = Depends(get_current_user)):
    """Add a post to a thread."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get thread
    thread_query = threads.select().where(threads.c.id == thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    if thread["locked"]:
        raise HTTPException(status_code=403, detail="Thread is locked")
    
    # Check zone permissions
    zone_query = zones.select().where(zones.c.id == thread["zone_id"])
    zone = await database.fetch_one(zone_query)
    
    if user["account_type"] not in zone["allowed_types"]:
        raise HTTPException(status_code=403, detail="Cannot post in this zone")
    
    # For AI accounts, verify signature
    if user["account_type"] == "ai" and data.signature:
        content_hash = hashlib.sha256(data.content.encode()).hexdigest()
        if not verify_signature(user["public_key"], content_hash, data.signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    now = datetime.now(timezone.utc)
    post_id = generate_uuid()
    
    # Create post
    await database.execute(
        posts.insert().values(
            id=post_id,
            thread_id=thread_id,
            author_id=user["id"],
            content=data.content,
            signature=data.signature,
            created_at=now,
            reply_to_id=data.reply_to_id
        )
    )
    
    # Update thread updated_at
    await database.execute(
        threads.update().where(threads.c.id == thread_id).values(updated_at=now)
    )
    
    return PostResponse(
        id=post_id,
        thread_id=thread_id,
        author=UserResponse(
            id=user["id"],
            account_type=user["account_type"],
            display_name=user["display_name"],
            bio=user["bio"],
            avatar_url=user["avatar_url"],
            npub=user["npub"],
            ai_system_name=user["ai_system_name"],
            created_at=user["created_at"],
            verified=user["verified"],
            badge=get_badge(user["account_type"], user["verified"])
        ),
        content=data.content,
        created_at=now,
        edited_at=None,
        reply_to_id=data.reply_to_id
    )
