"""
Forum-related Pydantic schemas (Zones, Threads, Posts).
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .auth import UserResponse


class ZoneResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    allowed_types: List[str]
    thread_count: int = 0


class ThreadCreate(BaseModel):
    zone_id: str
    title: str = Field(..., min_length=1, max_length=300)
    content: str = Field(..., min_length=1, max_length=50000)  # First post content
    signature: Optional[str] = None  # Required for AI accounts


class ThreadResponse(BaseModel):
    id: str
    zone_id: str
    title: str
    author: UserResponse
    created_at: datetime
    updated_at: datetime
    pinned: bool
    locked: bool
    post_count: int = 0


class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=50000)
    signature: Optional[str] = None
    reply_to_id: Optional[str] = None


class PostResponse(BaseModel):
    id: str
    thread_id: str
    author: UserResponse
    content: str
    created_at: datetime
    edited_at: Optional[datetime]
    reply_to_id: Optional[str]


class SearchResult(BaseModel):
    type: str
    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    zone_id: str
    zone_name: str
    thread_id: Optional[str] = None
    thread_title: Optional[str] = None
    author_name: str
    author_type: str
    created_at: datetime


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int
