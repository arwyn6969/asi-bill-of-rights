import requests
import json
from datetime import datetime

# Use local port 8000
BASE_URL = "http://localhost:8000"

def get_json(endpoint):
    try:
        resp = requests.get(f"{BASE_URL}{endpoint}")
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

print("--- FETCHING PRODUCTION DATA ---\n")

# 1. Zones
zones = get_json("/api/zones")
print(f"Found {len(zones)} Zones.\n")

for zone in zones:
    print(f"📍 ZONE: {zone['name']} ({zone['id']})")
    
    # 2. Threads
    threads = get_json(f"/api/zones/{zone['id']}/threads")
    if not threads:
        print("   (No threads)")
        continue
        
    for thread in threads:
        print(f"   🧵 THREAD: {thread['title']} (by {thread['author']['display_name']})")
        print(f"      ID: {thread['id']}")
        print(f"      Created: {thread['created_at']}")
        
        # 3. Posts (Need to fetch individual thread details often to get posts, 
        #    but the list threads endpoint might not return posts. 
        #    Let's check thread detail endpoint)
        thread_detail = get_json(f"/api/threads/{thread['id']}")
        if thread_detail and 'posts' in thread_detail:
            posts = thread_detail['posts']
            for post in posts:
                print(f"      📝 POST ({post['author']['display_name']}):")
                print(f"         \"{post['content']}\"")
                print(f"         ---")
        print("")
