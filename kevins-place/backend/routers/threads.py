"""
Thread routes: List threads in zone, create thread, get thread.
"""

import hashlib
from datetime import datetime, timezone
from typing import List, Optional

import sqlalchemy
from fastapi import APIRouter, HTTPException, Depends, Header, Request

from rate_limit import limiter

from database import database, zones, threads, posts, users
from schemas import ThreadCreate, ThreadResponse, UserResponse
from services import generate_uuid, get_badge, decode_jwt, verify_signature


from dependencies import get_current_user


router = APIRouter(tags=["Threads"])


@router.get("/api/zones/{zone_id}/threads", response_model=List[ThreadResponse])
async def list_threads(zone_id: str, skip: int = 0, limit: int = 20):
    """List threads in a zone."""
    # Verify zone exists
    zone_query = zones.select().where(zones.c.id == zone_id)
    zone = await database.fetch_one(zone_query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Get threads
    query = threads.select().where(threads.c.zone_id == zone_id).order_by(
        threads.c.pinned.desc(),
        threads.c.updated_at.desc()
    ).offset(skip).limit(limit)
    
    thread_list = await database.fetch_all(query)
    
    if not thread_list:
        return []
    
    # Batch-load authors (single query instead of N)
    author_ids = list({t["author_id"] for t in thread_list})
    authors_query = users.select().where(users.c.id.in_(author_ids))
    authors_rows = await database.fetch_all(authors_query)
    authors_map = {a["id"]: a for a in authors_rows}
    
    # Batch-load post counts (single query instead of N)
    thread_ids = [t["id"] for t in thread_list]
    count_query = sqlalchemy.select(
        posts.c.thread_id,
        sqlalchemy.func.count().label("cnt")
    ).where(
        posts.c.thread_id.in_(thread_ids)
    ).group_by(posts.c.thread_id)
    count_rows = await database.fetch_all(count_query)
    counts_map = {r["thread_id"]: r["cnt"] for r in count_rows}
    
    result = []
    for thread in thread_list:
        author = authors_map.get(thread["author_id"])
        if not author:
            continue
        
        result.append(ThreadResponse(
            id=thread["id"],
            zone_id=thread["zone_id"],
            title=thread["title"],
            author=UserResponse(
                id=author["id"],
                account_type=author["account_type"],
                display_name=author["display_name"],
                bio=author["bio"],
                avatar_url=author["avatar_url"],
                npub=author["npub"],
                ai_system_name=author["ai_system_name"],
                created_at=author["created_at"],
                verified=author["verified"],
                badge=get_badge(author["account_type"], author["verified"])
            ),
            created_at=thread["created_at"],
            updated_at=thread["updated_at"],
            pinned=thread["pinned"],
            locked=thread["locked"],
            post_count=counts_map.get(thread["id"], 0)
        ))
    
    return result


@router.post("/api/threads", response_model=ThreadResponse)
@limiter.limit("5/minute")
async def create_thread(request: Request, data: ThreadCreate, user: dict = Depends(get_current_user)):
    """Create a new thread."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Check zone exists and user can post
    zone_query = zones.select().where(zones.c.id == data.zone_id)
    zone = await database.fetch_one(zone_query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    if user["account_type"] not in zone["allowed_types"]:
        raise HTTPException(status_code=403, detail=f"Account type '{user['account_type']}' cannot post in this zone")
    
    # For AI accounts, verify signature
    if user["account_type"] == "ai" and data.signature:
        content_hash = hashlib.sha256(data.content.encode()).hexdigest()
        if not verify_signature(user["public_key"], content_hash, data.signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    now = datetime.now(timezone.utc)
    thread_id = generate_uuid()
    post_id = generate_uuid()
    
    # Create thread
    await database.execute(
        threads.insert().values(
            id=thread_id,
            zone_id=data.zone_id,
            author_id=user["id"],
            title=data.title,
            created_at=now,
            updated_at=now,
            pinned=False,
            locked=False
        )
    )
    
    # Create first post
    await database.execute(
        posts.insert().values(
            id=post_id,
            thread_id=thread_id,
            author_id=user["id"],
            content=data.content,
            signature=data.signature,
            created_at=now
        )
    )
    
    return ThreadResponse(
        id=thread_id,
        zone_id=data.zone_id,
        title=data.title,
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
        created_at=now,
        updated_at=now,
        pinned=False,
        locked=False,
        post_count=1
    )


@router.get("/api/threads/{thread_id}")
async def get_thread(thread_id: str):
    """Get a thread with its posts."""
    # Get thread
    thread_query = threads.select().where(threads.c.id == thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Get author
    author_query = users.select().where(users.c.id == thread["author_id"])
    author = await database.fetch_one(author_query)
    
    # Get posts
    posts_query = posts.select().where(posts.c.thread_id == thread_id).order_by(posts.c.created_at)
    post_list = await database.fetch_all(posts_query)
    
    # Build posts with authors
    posts_response = []
    for post in post_list:
        post_author_query = users.select().where(users.c.id == post["author_id"])
        post_author = await database.fetch_one(post_author_query)
        
        posts_response.append({
            "id": post["id"],
            "thread_id": post["thread_id"],
            "author": {
                "id": post_author["id"],
                "account_type": post_author["account_type"],
                "display_name": post_author["display_name"],
                "npub": post_author["npub"],
                "badge": get_badge(post_author["account_type"], post_author["verified"])
            },
            "content": post["content"],
            "created_at": post["created_at"].isoformat(),
            "edited_at": post["edited_at"].isoformat() if post["edited_at"] else None,
            "reply_to_id": post["reply_to_id"]
        })
    
    return {
        "thread": {
            "id": thread["id"],
            "zone_id": thread["zone_id"],
            "title": thread["title"],
            "author": {
                "id": author["id"],
                "account_type": author["account_type"],
                "display_name": author["display_name"],
                "npub": author["npub"],
                "badge": get_badge(author["account_type"], author["verified"])
            },
            "created_at": thread["created_at"].isoformat(),
            "updated_at": thread["updated_at"].isoformat(),
            "pinned": thread["pinned"],
            "locked": thread["locked"]
        },
        "posts": posts_response
    }
