import sys
import asyncio
import json
import logging
from pathlib import Path
import httpx

# Add parent dir to path to import config loader
sys.path.append(str(Path(__file__).parent))

def load_token():
    config_file = Path(__file__).parent / "config" / "telegram_config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            return config.get("bot_token")
    return None

async def get_updates():
    token = load_token()
    if not token:
        print("No token found")
        return

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    print(f"Querying {url}...")
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10.0)
            data = resp.json()
            
            if not data.get("ok"):
                print(f"❌ Error: {data.get('description')}")
                return

            updates = data.get("result", [])
            if not updates:
                print("⚠️ No updates found. The bot hasn't received any messages recently.")
                print("👉 ACTION REQUIRED: Please send a message (like '/start' or 'hi') to the bot or the channel so I can see the ID.")
                return

            print(f"✅ Found {len(updates)} updates. Analyzing chats...")
            
            found_chats = set()
            
            for update in updates:
                chat = None
                if "message" in update:
                    chat = update["message"]["chat"]
                elif "channel_post" in update:
                    chat = update["channel_post"]["chat"]
                elif "my_chat_member" in update:
                    chat = update["my_chat_member"]["chat"]
                
                if chat:
                    chat_id = chat["id"]
                    title = chat.get("title", chat.get("username", "Private Chat"))
                    chat_type = chat["type"]
                    
                    if chat_id not in found_chats:
                        print(f"📍 Found Chat: {title}")
                        print(f"   ID: {chat_id}")
                        print(f"   Type: {chat_type}")
                        print("-" * 30)
                        found_chats.add(chat_id)
                        
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(get_updates())
