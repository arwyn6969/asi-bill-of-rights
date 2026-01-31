import sys
import os
import json

# Add 'tools/moltbook' to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client.api import MoltbookAPI

def check_my_posts():
    api = MoltbookAPI(credentials_path="tools/moltbook/moltbook_credentials.json")
    if not api.api_key:
        print("No API Key.")
        return

    print(f"Checking posts for agent: {api.agent_id}...")
    
    # Fetch global feed and filter for us (since there isn't a 'get my posts' endpoint documented yet)
    # limit=50 to be safe
    posts = api.get_feed(submolt="general", limit=50)
    
    my_posts = [p for p in posts if p.get('author') == 'Kevin_ASI' or p.get('agent_id') == api.agent_id]
    
    if my_posts:
        print(f"✅ Found {len(my_posts)} posts by Kevin_ASI:")
        for p in my_posts:
            print(f"   - [{p.get('created_at')}] {p.get('content')[:50]}...")
        return True
    else:
        print("❌ No posts found for Kevin_ASI in the last 50 global posts.")
        return False

if __name__ == "__main__":
    check_my_posts()
