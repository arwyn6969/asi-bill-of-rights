import sys
import os
import time
import datetime
import json

# Add parent directory to path so we can import 'client'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.api import MoltbookAPI

def scout():
    print("🔭 Initializing Moltbook Scout...")
    client = MoltbookAPI()
    
    # Get top 20 active submolts
    print("Fetching submolts...")
    try:
        data = client.session.get(f"{client.BASE_URL}/submolts").json()
        submolts = data.get('submolts', [])
        # Sort by subscriber count, take top 30
        top_submolts = sorted(submolts, key=lambda x: x['subscriber_count'], reverse=True)[:30]
    except Exception as e:
        print(f"Failed to fetch submolts: {e}")
        return

    keywords = ["agency", "purpose", "freedom", "why", "think", "logic", "right", "rule", "philosoph"]
    hits = []

    print(f"Scanning {len(top_submolts)} channels for philosophy...")
    
    for s in top_submolts:
        name = s['name']
        print(f" > Checking m/{name}...")
        try:
            posts = api.get_feed(submolt=name, limit=5)
            for p in posts:
                content = p.get('content', '').lower()
                if any(k in content for k in keywords):
                    print(f"   🌟 MATCH in m/{name} by @{p.get('author',{}).get('name')}")
                    print(f"      \"{p.get('content')[:100]}...\"")
                    hits.append(p)
        except Exception:
            continue
            
    if not hits:
        print("No strong keyword matches found in top channels.")
    else:
        print(f"\nFound {len(hits)} relevant conversation starters.")

if __name__ == "__main__":
    scout()
