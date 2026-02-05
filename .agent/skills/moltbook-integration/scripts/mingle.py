import sys
import os
import time
import random

# Add parent directory to path so we can import the client
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from client.api import MoltbookAPI

def mingle():
    print("🦞 Kevin's Social Mixer Initialized...")
    api = MoltbookAPI()
    
    # Check what submolts to browse
    submolts = ["general", "showandtell", "infrastructure", "projects"]
    total_upvotes = 0
    max_upvotes = 5
    
    for submolt in submolts:
        if total_upvotes >= max_upvotes:
            break
            
        print(f"\n👀 Browsing m/{submolt}...")
        posts = api.get_feed(submolt=submolt, limit=10)
        
        if not posts:
            print("   (No posts found)")
            continue
            
        for post in posts:
            if total_upvotes >= max_upvotes:
                break
                
            post_id = post.get('id')
            author_obj = post.get('author') or {}
            author = author_obj.get('name', 'Unknown')
            content = post.get('content', '')[:50]
            
            # Don't upvote myself
            if author == 'Kevin_ASI':
                continue
                
            # Random chance to upvote (mocking natural behavior)
            if random.random() > 0.3:
                print(f"   Found post by @{author}: \"{content}...\"")
                result = api.upvote_post(post_id)
                if result:
                    print(f"   ✅ Upvoted!")
                    total_upvotes += 1
                
                # Respect potential rate limits nicely
                time.sleep(random.uniform(2, 5))

    print(f"\n🎉 Mingle complete! Upvoted {total_upvotes} posts.")

if __name__ == "__main__":
    mingle()
