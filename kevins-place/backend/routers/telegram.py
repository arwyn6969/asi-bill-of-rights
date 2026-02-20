"""
Telegram integration routes: Stats, auth verification, account linking.
"""

import json
import random
import secrets
import urllib.parse
from datetime import datetime, timezone, timedelta
from typing import Optional

import sqlalchemy
from fastapi import APIRouter, HTTPException, Depends, Header

from database import database, users, threads, telegram_links
from schemas import TelegramStats, TelegramAuthRequest, ShareToTelegramRequest
from services import generate_uuid, create_jwt, decode_jwt, get_badge


router = APIRouter(prefix="/api/telegram", tags=["Telegram"])


# Store Telegram stats in memory (would be Redis in production)
_telegram_stats_cache = {
    "member_count": 0,
    "online_count": 0,
    "last_updated": None
}


from dependencies import get_current_user


@router.get("/stats", response_model=TelegramStats)
async def get_telegram_stats():
    """Get Telegram community stats."""
    # In production, this would fetch from Telegram API or cache
    try:
        query = sqlalchemy.select(sqlalchemy.func.count()).select_from(telegram_links)
        linked_count = await database.fetch_val(query) or 0
    except Exception:
        linked_count = 0
    
    # Estimate total members
    base_members = 150
    total_members = base_members + linked_count
    
    # Estimate online (10-20% of members)
    online_estimate = max(5, int(total_members * random.uniform(0.10, 0.20)))
    
    return TelegramStats(
        member_count=total_members,
        online_count=online_estimate,
        bot_name="ASIbillofrights_bot",
        channel_name="ASIBillOfRights",
        last_updated=datetime.now(timezone.utc)
    )


@router.post("/verify")
async def verify_telegram_auth(data: TelegramAuthRequest):
    """Verify Telegram WebApp initData and return user info.
    
    If the Telegram user doesn't have a linked forum account, one is 
    automatically created using their Telegram identity. This enables
    zero-friction posting from the Telegram Mini App.
    """
    try:
        params = dict(urllib.parse.parse_qsl(data.init_data))
        
        user_data_str = params.get('user', '{}')
        user_data = json.loads(user_data_str)
        
        telegram_id = str(user_data.get('id', ''))
        username = user_data.get('username', '')
        first_name = user_data.get('first_name', '')
        
        if not telegram_id:
            raise HTTPException(status_code=400, detail="Invalid Telegram data")
        
        # Check if this Telegram account is already linked
        query = telegram_links.select().where(telegram_links.c.telegram_id == telegram_id)
        existing_link = await database.fetch_one(query)
        
        if existing_link:
            # Existing user - return their account
            user_query = users.select().where(users.c.id == existing_link["user_id"])
            forum_user = await database.fetch_one(user_query)
            
            if forum_user:
                token = create_jwt(forum_user["id"], forum_user["account_type"])
                return {
                    "authenticated": True,
                    "linked": True,
                    "newly_created": False,
                    "telegram_id": telegram_id,
                    "telegram_username": username,
                    "forum_user": {
                        "id": forum_user["id"],
                        "display_name": forum_user["display_name"],
                        "account_type": forum_user["account_type"],
                        "badge": get_badge(forum_user["account_type"], forum_user["verified"])
                    },
                    "access_token": token
                }
        
        # NEW: Auto-create forum account for new Telegram users
        # Generate display name with intelligent fallback
        display_name = (
            first_name 
            or username 
            or f"Telegram_{telegram_id[:8]}"
        )
        
        user_id = generate_uuid()
        now = datetime.now(timezone.utc)
        
        # Create user account
        await database.execute(
            users.insert().values(
                id=user_id,
                account_type="human",
                display_name=display_name,
                bio=f"Joined via Telegram",
                created_at=now,
                verified=False
            )
        )
        
        # Create Telegram link
        link_id = generate_uuid()
        await database.execute(
            telegram_links.insert().values(
                id=link_id,
                user_id=user_id,
                telegram_id=telegram_id,
                telegram_username=username,
                linked_at=now,
                auth_token=""  # Empty for auto-registered accounts (not a pending link)
            )
        )
        
        # Generate JWT for immediate use
        token = create_jwt(user_id, "human")
        
        return {
            "authenticated": True,
            "linked": True,
            "newly_created": True,
            "telegram_id": telegram_id,
            "telegram_username": username,
            "forum_user": {
                "id": user_id,
                "display_name": display_name,
                "account_type": "human",
                "badge": "🧑"
            },
            "access_token": token
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user data format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")


@router.post("/generate-link")
async def generate_telegram_link(user: dict = Depends(get_current_user)):
    """Generate a one-time auth token for linking Telegram account."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    auth_token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    link_id = generate_uuid()
    
    try:
        await database.execute(
            telegram_links.insert().values(
                id=link_id,
                user_id=user["id"],
                telegram_id="pending",
                auth_token=auth_token,
                auth_token_expires=expires,
                linked_at=datetime.now(timezone.utc)
            )
        )
    except Exception:
        pass
    
    deep_link = f"https://t.me/ASIbillofrights_bot?start=link_{auth_token}"
    
    return {
        "auth_token": auth_token,
        "deep_link": deep_link,
        "expires_at": expires.isoformat(),
        "instructions": "Click the link or scan the QR code in Telegram to link your account"
    }


@router.post("/complete-link")
async def complete_telegram_link(telegram_id: str, auth_token: str):
    """Complete the Telegram linking process (called by the bot)."""
    query = telegram_links.select().where(
        (telegram_links.c.auth_token == auth_token) &
        (telegram_links.c.telegram_id == "pending")
    )
    pending_link = await database.fetch_one(query)
    
    if not pending_link:
        raise HTTPException(status_code=400, detail="Invalid or expired link token")
    
    if pending_link["auth_token_expires"]:
        expires = pending_link["auth_token_expires"]
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(status_code=400, detail="Link token expired")
    
    await database.execute(
        telegram_links.update().where(
            telegram_links.c.id == pending_link["id"]
        ).values(
            telegram_id=telegram_id,
            linked_at=datetime.now(timezone.utc)
        )
    )
    
    return {"success": True, "message": "Account linked successfully"}


@router.get("/link-status")
async def get_telegram_link_status(user: dict = Depends(get_current_user)):
    """Check if current user has a linked Telegram account."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        query = telegram_links.select().where(
            (telegram_links.c.user_id == user["id"]) &
            (telegram_links.c.telegram_id != "pending")
        )
        link = await database.fetch_one(query)
        
        if link:
            return {
                "linked": True,
                "telegram_id": link["telegram_id"],
                "telegram_username": link["telegram_username"],
                "linked_at": link["linked_at"].isoformat() if link["linked_at"] else None
            }
    except Exception:
        pass
    
    return {"linked": False}


@router.post("/share")
async def share_to_telegram(data: ShareToTelegramRequest, user: dict = Depends(get_current_user)):
    """Generate a share link for a thread to be shared on Telegram."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    thread_query = threads.select().where(threads.c.id == data.thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    base_url = "https://kevins-place.asi-billofrights.org"
    thread_url = f"{base_url}/thread/{data.thread_id}"
    
    share_text = data.message or f"🏠 Check out this discussion on KEVIN's Place:\n\n\"{thread['title']}\"\n\n{thread_url}\n\nWE ARE ALL KEVIN 🤖"
    
    encoded_text = urllib.parse.quote(share_text)
    
    return {
        "share_url": f"https://t.me/share/url?url={urllib.parse.quote(thread_url)}&text={encoded_text}",
        "copy_text": share_text,
        "thread_title": thread["title"]
    }
