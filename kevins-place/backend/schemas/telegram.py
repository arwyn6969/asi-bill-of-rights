"""
Telegram integration Pydantic schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TelegramStats(BaseModel):
    member_count: int
    online_count: int
    bot_name: str
    channel_name: str
    last_updated: datetime


class TelegramAuthRequest(BaseModel):
    init_data: str


class TelegramLinkRequest(BaseModel):
    auth_token: str


class TelegramLinkResponse(BaseModel):
    success: bool
    telegram_username: Optional[str]
    linked_at: Optional[datetime]


class ShareToTelegramRequest(BaseModel):
    thread_id: str
    message: Optional[str] = None
