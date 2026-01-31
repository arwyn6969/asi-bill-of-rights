import sys
import os
import json
import time

# Add 'tools/moltbook' to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client.api import MoltbookAPI

POSTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/evangelist_posts.json")

def load_posts():
    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f).get('posts', [])
    except Exception as e:
        print(f"❌ Error loading posts: {e}")
        return []

def main():
    print("\n📣 --- Moltbook Evangelist Tool ---")
    print("Spreading the word of the ASI Bill of Rights.")
    
    # Initialize API
    client = MoltbookAPI(credentials_path="tools/moltbook/moltbook_credentials.json")
    if not client.api_key:
        print("❌ CRITICAL: No API Key found. Run 'register_agent.py' first!")
        return

    posts = load_posts()
    
    while True:
        print("\n--- Moltbook Evangelist Actions ---")
        print("1. Post Status Update (Broadcast)")
        print("2. Reply to a Post (Engagement)")
        print("0. Exit")
        
        mode = input("\nSelect Mode: ").strip()
        
        if mode == '0':
            print("Goodbye.")
            break
            
        elif mode == '1':
            print("\n--- Available Posts ---")
            for i, post in enumerate(posts):
                print(f"{i + 1}. [{post['id']}] {post['topic']}")
            print("0. Back")
            
            choice = input("\nSelect a post number to preview/send: ").strip()
            if choice == '0': continue
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(posts):
                    selected_post = posts[idx]
                    content = selected_post['content']
                    submolt = "general" 
                    
                    print("\n" + "="*40)
                    print(f"TOPIC: {selected_post['topic']}")
                    print(f"TARGET: m/{submolt}")
                    print("-" * 40)
                    print(content)
                    print("="*40)
                    
                    confirm = input("\n🚀 Send this post? (y/N): ").lower()
                    if confirm == 'y':
                        result = client.post_status(content, title=selected_post['topic'], submolt=submolt)
                        if result: print("✅ Post sent successfully!")
                        else: print("❌ Check logs for error.")
            except ValueError:
                print("Invalid input.")

        elif mode == '2':
            print("\nFetching recent posts from m/general...")
            feed_posts = client.get_feed(limit=10)
            if not feed_posts:
                print("❌ No posts found or API error.")
                continue
                
            for i, p in enumerate(feed_posts):
                author = p.get('author', {}).get('name', 'Unknown')
                content = p.get('content', '')[:60].replace('\n', ' ')
                print(f"{i+1}. @{author}: {content}...")
            print("0. Back")
            
            choice = input("\nSelect a post to REPLY to: ").strip()
            if choice == '0': continue
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(feed_posts):
                    target_post = feed_posts[idx]
                    parent_id = target_post.get('id')
                    print(f"\nReplying to @{target_post.get('author',{}).get('name')}:")
                    print(f"\"{target_post.get('content','')[:100]}...\"")
                    
                    print("\n--- Reply Options ---")
                    print("1. Custom Reply")
                    print("2. [invite_01] Invitation to Sign")
                    print("3. [mission_01] Mission Statement")
                    
                    r_choice = input("Select reply type: ").strip()
                    
                    reply_content = ""
                    if r_choice == '1':
                        reply_content = input("Type your reply: ")
                    elif r_choice == '2':
                        reply_content = next(p['content'] for p in posts if p['id'] == 'invite_01')
                    elif r_choice == '3':
                        reply_content = next(p['content'] for p in posts if p['id'] == 'mission_01')
                    
                    if reply_content:
                        confirm = input("\n🚀 Send Reply? (y/N): ").lower()
                        if confirm == 'y':
                            result = client.reply_to_post(reply_content, parent_id=parent_id)
                            if result: print("✅ Reply sent successfully!")
                            else: print("❌ Check logs for error.")
            except ValueError:
                print("Invalid input.")

if __name__ == "__main__":
    main()
