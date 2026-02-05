import sys
import asyncio
import os
import json
from pathlib import Path

# Add parent dir to path to import config loader
sys.path.append(str(Path(__file__).parent))

try:
    from telegram import Bot
    from telegram.error import TelegramError
except ImportError:
    print("python-telegram-bot not installed")
    sys.exit(1)

def load_token():
    config_file = Path(__file__).parent / "config" / "telegram_config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            return config.get("bot_token")
    return os.getenv("TELEGRAM_BOT_TOKEN")

async def check_chat(chat_id):
    token = load_token()
    if not token:
        print("No token found")
        return

    bot = Bot(token=token)
    print(f"Checking access to {chat_id}...")
    
    try:
        chat = await bot.get_chat(chat_id)
        print(f"✅ FOUND CHAT: {chat.title} (ID: {chat.id})")
        print(f"   Type: {chat.type}")
        
        # Check bot status
        me = await bot.get_me()
        try:
            member = await bot.get_chat_member(chat_id, me.id)
            print(f"   Bot Status: {member.status}")
            print(f"   Can Post: {member.can_post_messages if hasattr(member, 'can_post_messages') else 'Unknown'}")
        except Exception as e:
            print(f"   ❌ Could not get member status: {e}")
            
    except TelegramError as e:
        print(f"❌ Error accessing {chat_id}: {e}")

async def main():
    chats_to_check = [
        "@ASIBillOfRights", 
        "@asibillofrights", 
        "@ASI_Bill_of_Rights",
        "@asi_bill_of_rights"
    ]
    
    for chat in chats_to_check:
        await check_chat(chat)
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
