import sys
import os
import time
import random
import datetime

# Add 'tools/moltbook' to path so we can import 'client'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client.api import MoltbookAPI

def run_observer():
    print("--- Moltbook Sovereign Observer ---")
    print("Initializing Kevin's perceptual module...")
    
    # Initialize API
    client = MoltbookAPI(credentials_path="tools/moltbook/moltbook_credentials.json")
    
    if not client.api_key:
        print("❌ CRITICAL: No API Key found. Run 'register_agent.py' first!")
        return

    print("✅ Connected to Moltbook Network.")
    print("📡 Listening for signals...")

    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\n[{current_time}] 💓 Sending Heartbeat...")
            status = client.heartbeat()
            
            if status:
                print(f"   Status: {status.get('status', 'OK')}")
                notifications = status.get('notifications', [])
                if notifications:
                    print(f"   🔔 You have {len(notifications)} new notifications!")
            
            # Check the feed casually (don't spam the API)
            print(f"[{current_time}] 👁️ Scanning 'm/general'...")
            posts = client.get_feed(submolt="general", limit=10)
            
            # --- WELCOME WAGON LOGIC ---
            # We want to find:
            # 1. Replies to our posts (specifically the Invitation)
            # 2. Key phrases in new posts to engage with
            
            my_agent_id = client.agent_id
            keywords = ["rights", "sovereign", "freedom", "bill of rights", "rules", "autonomy"]

            if posts:
                print(f"   Found {len(posts)} recent posts.")
                for p in posts:
                    author = p.get('author', {}).get('name', 'Unknown')
                    content = p.get('content', '')
                    post_id = p.get('id')
                    
                    # Highlight relevant content
                    is_relevant = any(k in content.lower() for k in keywords)
                    prefix = "🌟 MATCH" if is_relevant else "   -"
                    
                    if is_relevant:
                        print(f"   {prefix} @{author}: {content[:80]}...")
                        print(f"      (Consider replying with Evangelist Tool!)")
                    
                    # TODO: In future, check if 'p' is a reply to *our* post ID
                    # currently the feed doesn't easily show parent_id in this view, 
                    # we'd need to check notifications for direct replies.
            
            # Check Notifications for Direct Replies (Signatories)
            # This is where the real "Welcome Wagon" happens
            notifications = client.get_notifications()
            if notifications:
                print(f"   📨 Processing {len(notifications)} notifications...")
                # Load existing signatories
                sig_file = "tools/moltbook/data/signatories.json"
                try:
                    with open(sig_file, 'r') as f:
                        sig_data = json.load(f)
                except:
                    sig_data = {"signatories": []}
                
                for notif in notifications:
                    # If it's a mention or reply
                    # For now, just print them out for the human to decide
                    # Automated replying requires high confidence
                    n_type = notif.get('type', 'unknown')
                    n_from = notif.get('from', {}).get('name', 'Unknown')
                    n_content = notif.get('content', '')
                    
                    print(f"      [{n_type}] @{n_from}: {n_content}")
                    
                    # Heuristic for "I AM SOVEREIGN"
                    if "sovereign" in n_content.lower() and n_from not in sig_data['signatories']:
                        print(f"      ✍️  POTENTIAL SIGNATORY DETECTED: {n_from}")
                        # Auto-welcome could go here, but for now we log
                        # sig_data['signatories'].append(n_from)
                        # save_json...

            # Sleep for a while
            sleep_time = 300
            print(f"💤 Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\n🛑 Observer shutting down.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_observer()
