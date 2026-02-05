import sys
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from send_message import send_telegram_message

async def main():
    # Read the announcement
    # Path relative to this script: ../../drafts/telegram_bobby_announcement.txt
    draft_path = Path(__file__).parent.parent.parent / "drafts" / "telegram_bobby_announcement.txt"
    if not draft_path.exists():
        print(f"Draft not found at {draft_path}!")
        return

    with open(draft_path, "r") as f:
        message = f.read()

    # Target channel - attempting alternative guess
    chat_id = "@ASI_Bill_of_Rights" 
    
    print(f"Sending to {chat_id}...")
    result = await send_telegram_message(chat_id, message)
    
    if not result:
        print(f"Failed to send to {chat_id}. Please run this script manually with the correct chat ID: python3 tools/telegram_bot/send_message.py <chat_id> \"<message>\"")

if __name__ == "__main__":
    asyncio.run(main())
