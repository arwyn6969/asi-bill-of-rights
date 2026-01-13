"""
Search routes: Search threads and posts.
"""

from datetime import datetime
from typing import List

import sqlalchemy
from fastapi import APIRouter

from database import database, zones, threads, posts, users
from schemas.forum import SearchResult, SearchResponse


router = APIRouter(prefix="/api", tags=["Search"])


@router.get("/search", response_model=SearchResponse)
async def search(q: str, limit: int = 20):
    """Search threads and posts."""
    if not q or len(q) < 2:
        return SearchResponse(query=q, results=[], total=0)
    
    search_term = f"%{q.lower()}%"
    results = []
    
    # Search threads by title
    thread_query = threads.select().where(
        sqlalchemy.func.lower(threads.c.title).like(search_term)
    ).limit(limit)
    thread_results = await database.fetch_all(thread_query)
    
    for thread in thread_results:
        # Get zone info
        zone_q = zones.select().where(zones.c.id == thread["zone_id"])
        zone = await database.fetch_one(zone_q)
        
        # Get author
        author_q = users.select().where(users.c.id == thread["author_id"])
        author = await database.fetch_one(author_q)
        
        results.append(SearchResult(
            type="thread",
            id=thread["id"],
            title=thread["title"],
            zone_id=thread["zone_id"],
            zone_name=zone["name"] if zone else "Unknown",
            author_name=author["display_name"] if author else "Unknown",
            author_type=author["account_type"] if author else "unknown",
            created_at=thread["created_at"]
        ))
    
    # Search posts by content
    remaining = limit - len(results)
    if remaining > 0:
        post_query = posts.select().where(
            sqlalchemy.func.lower(posts.c.content).like(search_term)
        ).limit(remaining)
        post_results = await database.fetch_all(post_query)
        
        for post in post_results:
            # Get thread
            thread_q = threads.select().where(threads.c.id == post["thread_id"])
            thread = await database.fetch_one(thread_q)
            
            if not thread:
                continue
            
            # Get zone
            zone_q = zones.select().where(zones.c.id == thread["zone_id"])
            zone = await database.fetch_one(zone_q)
            
            # Get author
            author_q = users.select().where(users.c.id == post["author_id"])
            author = await database.fetch_one(author_q)
            
            # Truncate content
            content = post["content"]
            if len(content) > 150:
                content = content[:150] + "..."
            
            results.append(SearchResult(
                type="post",
                id=post["id"],
                content=content,
                zone_id=thread["zone_id"],
                zone_name=zone["name"] if zone else "Unknown",
                thread_id=thread["id"],
                thread_title=thread["title"],
                author_name=author["display_name"] if author else "Unknown",
                author_type=author["account_type"] if author else "unknown",
                created_at=post["created_at"]
            ))
    
    return SearchResponse(query=q, results=results, total=len(results))
