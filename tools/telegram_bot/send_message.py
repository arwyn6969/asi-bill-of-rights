#!/usr/bin/env python3
"""
Send a message to a Telegram chat using the Bot API.

Usage:
    python3 send_message.py <chat_id> "<message>"

Or import and use programmatically:
    from send_message import send_telegram_message
    send_telegram_message(chat_id, "Hello!")
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Check for required packages
try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx")
    sys.exit(1)


def load_token():
    """Load bot token from env or config file."""
    # 1. Try environment variable
    env_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if env_token:
        return env_token
    
    # 2. Try config file
    config_file = Path(__file__).parent / "config" / "telegram_config.json"
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
            return config.get("bot_token")
    
    print("ERROR: Bot token not found!")
    print("Set TELEGRAM_BOT_TOKEN env var or create config/telegram_config.json")
    sys.exit(1)


async def send_telegram_message(chat_id: str, message: str, parse_mode: str = "HTML"):
    """Send a message to a Telegram chat."""
    token = load_token()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode
        })
        
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Message sent to {chat_id}")
            print(f"   Message ID: {result['result']['message_id']}")
            return result
        else:
            print(f"❌ Failed to send message: {result.get('description', 'Unknown error')}")
            return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_message.py <chat_id> \"<message>\"")
        print()
        print("Examples:")
        print("  python3 send_message.py -1001234567890 \"Hello group!\"")
        print("  python3 send_message.py @channelname \"Hello channel!\"")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    message = sys.argv[2]
    
    print(f"📤 Sending message to {chat_id}...")
    asyncio.run(send_telegram_message(chat_id, message))


if __name__ == "__main__":
    main()
