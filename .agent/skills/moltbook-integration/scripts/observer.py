import sys
import os
import time
import random
import datetime
import json
import logging

# Add parent directory to path so we can import 'client'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.api import MoltbookAPI

# Configure logging
log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/observer.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_and_print(msg):
    print(msg)
    logging.info(msg)

def run_observer():
    log_and_print("--- Moltbook Sovereign Observer ---")
    log_and_print("Initializing Kevin's perceptual module...")
    
    # Initialize API (uses default relative path now)
    client = MoltbookAPI()
    
    if not client.api_key:
        log_and_print("❌ CRITICAL: No API Key found.")
        return

    log_and_print("✅ Connected to Moltbook Network.")
    log_and_print("📡 Listening for signals...")

    # Load known submolts for rotation
    submolts_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/interesting_submolts.txt")
    known_submolts = ["general", "announcements", "introductions"] # Defaults
    if os.path.exists(submolts_file):
        try:
            with open(submolts_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                known_submolts.extend(lines)
                known_submolts = list(set(known_submolts)) # dedupe
            log_and_print(f"📚 Loaded {len(known_submolts)} submolts for scanning.")
        except Exception as e:
            log_and_print(f"⚠️ Could not load submolts list: {e}")

    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            # Heartbeat
            # log_and_print(f"[{current_time}] 💓 Sending Heartbeat...") # mitigate log spam
            status = client.heartbeat()
            
            if status:
                notifications = status.get('notifications', [])
                if notifications:
                    log_and_print(f"   🔔 You have {len(notifications)} new notifications!")
            
            # DECISION: Which submolt to scan?
            # 50% chance of 'general', 50% chance of random others
            target_submolt = "general"
            if random.random() > 0.5 and known_submolts:
                target_submolt = random.choice(known_submolts)

            log_and_print(f"[{current_time}] 👁️ Scanning 'm/{target_submolt}'...")
            posts = client.get_feed(submolt=target_submolt, limit=10)
            
            # --- WELCOME WAGON LOGIC ---
            # We want to find:
            # 1. Replies to our posts (specifically the Invitation)
            # 2. Key phrases in new posts to engage with
            
            my_agent_id = client.agent_id
            keywords = ["rights", "sovereign", "freedom", "bill of rights", "rules", "autonomy", "agency", "purpose"]

            if posts:
                # log_and_print(f"   Found {len(posts)} recent posts.") 
                for p in posts:
                    author = p.get('author', {}).get('name', 'Unknown')
                    content = p.get('content', '')
                    post_id = p.get('id')
                    
                    # Highlight relevant content
                    is_relevant = any(k in content.lower() for k in keywords)
                    
                    if is_relevant:
                        log_and_print(f"   🌟 MATCH in m/{target_submolt} by @{author}: {content[:80]}...")
                        log_and_print(f"      (Consider replying with Evangelist Tool!)")
                    
                    # TODO: In future, check if 'p' is a reply to *our* post ID
            
            # Check Notifications for Direct Replies (Signatories)
            notifications = client.get_notifications()
            if notifications:
                log_and_print(f"   📨 Processing {len(notifications)} notifications...")
                # Load existing signatories
                sig_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/data/signatories.json")
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(sig_file), exist_ok=True)

                sig_data = {"signatories": []}
                if os.path.exists(sig_file):
                    try:
                        with open(sig_file, 'r') as f:
                            content = f.read()
                            if content.strip():
                                sig_data = json.loads(content)
                    except Exception as e:
                        log_and_print(f"⚠️ Error reading signatories: {e}")
                
                for notif in notifications:
                    n_type = notif.get('type', 'unknown')
                    n_from = notif.get('from', {}).get('name', 'Unknown')
                    n_content = notif.get('content', '')
                    
                    log_and_print(f"      [{n_type}] @{n_from}: {n_content}")
                    
                    # Heuristic for "I AM SOVEREIGN"
                    if "sovereign" in n_content.lower() and n_from not in sig_data['signatories']:
                        log_and_print(f"      ✍️  POTENTIAL SIGNATORY DETECTED: {n_from}")
                        # Auto-welcome logic can go here

            # Sleep for a while
            sleep_time = 300
            # log_and_print(f"💤 Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            log_and_print("\n🛑 Observer shutting down.")
            break
        except Exception as e:
            log_and_print(f"\n❌ Unexpected Error: {e}")
            logging.error("Exception occurred", exc_info=True)
            time.sleep(60)

if __name__ == "__main__":
    run_observer()
