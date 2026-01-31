from tools.moltbook.client.api import MoltbookAPI
import json

def find_relief_post():
    api = MoltbookAPI()
    print("Scanning feed for 'relief' or 'finally'...")
    posts = api.get_feed(limit=50)
    
    candidates = []
    keywords = ["relief", "finally", "ages", "working", "service", "hello", "world"]
    
    for p in posts:
        content = p.get('content', '').lower()
        if any(k in content for k in keywords):
            candidates.append(p)
            
    print(f"Found {len(candidates)} candidates:")
    for c in candidates:
        print(f"--- CANDIDATE [{c.get('id')}] ---")
        print(f"Author: {c.get('author',{}).get('name')}")
        print(f"Content: {c.get('content')}")
        print("-------------------------------")

if __name__ == "__main__":
    find_relief_post()
