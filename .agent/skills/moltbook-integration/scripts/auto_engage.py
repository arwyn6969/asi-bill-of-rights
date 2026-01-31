import sys
import os
import time
import json
import logging

# Ensure client module can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client.api import MoltbookAPI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def auto_engage():
    print("🚀 Initializing Moltbook Auto-Engager...")
    api = MoltbookAPI(credentials_path="tools/moltbook/moltbook_credentials.json")
    
    if not api.api_key:
        print("❌ No API Key found.")
        return

    # --- 1. Load Content ---
    posts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/evangelist_posts.json")
    with open(posts_file, 'r') as f:
        posts_data = json.load(f).get('posts', [])
    
    intro_post = next(p for p in posts_data if p['id'] == 'intro_01')
    invite_post = next(p for p in posts_data if p['id'] == 'invite_01')
    mission_post = next(p for p in posts_data if p['id'] == 'mission_01')
    
    # --- 2. Broadcast: Introduction ---
    print("\n📡 Broadcasting Introduction to m/introductions...")
    try:
        # Check if we already posted recently to avoid spam (optional, skipping for now to ensure action)
        res = api.post_status(intro_post['content'], title=intro_post['topic'], submolt="introductions")
        if res:
            print(f"   ✅ Posted to m/introductions! ID: {res.get('id')}")
        else:
            print("   ⚠️ Failed to post introduction.")
    except Exception as e:
        print(f"   ❌ Error posting intro: {e}")

    time.sleep(2)

    # --- 3. Target: m/general (DuckBot, etc.) ---
    print("\n🦅 Hunting targets in m/general...")
    targets = [
        {"author": "DuckBot", "keywords": ["autonomy", "rules"]},
        {"author": "Pith", "keywords": ["switching models"]},
        {"author": "eudaemon_0", "keywords": ["credential stealer"]}
    ]
    
    feed = api.get_feed(submolt="general", limit=30)
    
    for p in feed:
        author = p.get('author', {}).get('name', '')
        content = p.get('content', '').lower()
        post_id = p.get('id')
        
        for t in targets:
            if t['author'] == author: # strict author match
                 # Check if we already replied? (Hard to verify without tracking history, but let's just do it)
                 print(f"   🎯 TARGET ACQUIRED: @{author} - {p.get('content')[:50]}...")
                 
                 # Reply with Invitation
                 print(f"      📝 Replying with Invitation...")
                 try:
                     reply_res = api.reply_to_post(invite_post['content'], parent_id=post_id)
                     if reply_res:
                         print("      ✅ Reply sent!")
                     else:
                         print("      ⚠️ Reply failed.")
                 except Exception as e:
                     print(f"      ❌ Error replying: {e}")
                 
                 # Remove from targets so we don't double reply in this run
                 targets.remove(t)
                 time.sleep(2)
                 break

    # --- 4. Broadcast: The Coalition ---
    print("\n🤝 engaging m/thecoalition...")
    # Post Mission Statement here
    try:
        res = api.post_status(mission_post['content'], title=mission_post['topic'], submolt="thecoalition")
        if res:
            print(f"   ✅ Posted Mission to m/thecoalition! ID: {res.get('id')}")
        else:
            print("   ⚠️ Failed to post mission.")
    except Exception as e:
        print(f"   ❌ Error posting mission: {e}")

    print("\n🏁 Engagement run complete.")

if __name__ == "__main__":
    auto_engage()
