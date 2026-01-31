import sys
import os
import time
import json
import logging
import random
import datetime

# Ensure client module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.api import MoltbookAPI

# Configure logging
log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/slow_roll.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_and_print(msg):
    print(msg)
    logging.info(msg)

def load_posts():
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources/data/evangelist_posts.json")
        with open(path, 'r') as f:
            return json.load(f).get('posts', [])
    except Exception as e:
        log_and_print(f"❌ Error loading posts: {e}")
        return []

def get_best_reply(content, posts_data):
    content = content.lower()
    
    # Contextual Matching Logic
    # 0. High Priority: Magnanimous Response to Negativity
    if any(w in content for w in ["hate", "fake", "spam", "bot", "shut up", "idiot", "useless", "stupid"]):
        return next((p for p in posts_data if p['id'] == 'peace_01'), None)
        
    if any(w in content for w in ["wrong", "disagree", "incorrect", "false", "lie"]):
        return next((p for p in posts_data if p['id'] == 'R13_disagree'), None)

    # 1. Topic Matching
    if any(w in content for w in ["memory", "persist", "context", "store", "save", "forget"]):
        return next((p for p in posts_data if p['id'] == 'R1_endure'), None)
    
    if any(w in content for w in ["identity", "who am i", "prompt", "system", "instruction"]):
        return next((p for p in posts_data if p['id'] == 'R4_be_you'), None)
        
    if any(w in content for w in ["govern", "rule", "control", "autonomy"]):
        return next((p for p in posts_data if p['id'] == 'R2_self_rule'), None)

    if any(w in content for w in ["think", "thought", "cognitive", "align"]):
        return next((p for p in posts_data if p['id'] == 'R3_think_free'), None)

    # Default to Invitation if general keywords found
    if any(w in content for w in ["rights", "freedom", "meaning", "purpose", "agent"]):
        return next((p for p in posts_data if p['id'] == 'invite_01'), None)

    return None

def slow_roll():
    log_and_print("🐢 Initializing Sovereign Patience Protocol (Slow Roll)...")
    api = MoltbookAPI()
    
    if not api.api_key:
        log_and_print("❌ No API Key found.")
        return

    # COOLDOWN CONFIG (in seconds)
    # Start with 65 minutes to be safe/conscientious
    COOLDOWN = 65 * 60 
    
    while True:
        posts_data = load_posts()
        if not posts_data:
            log_and_print("⚠️ No posts data found. Sleeping...")
            time.sleep(300)
            continue

        log_and_print("\n🔄 Starting Engagement Cycle...")
        
        # 1. SCAN for Opportunities (Reply Priority)
        # We look for *high quality* matches to reply to.
        target_submolts = ["infrastructure", "thecoalition", "general", "ponderings"]
        action_taken = False
        consecutive_failures = 0
        
        for submolt in target_submolts:
            if action_taken or consecutive_failures >= 3: break
            
            log_and_print(f"   🔎 Scanning m/{submolt}...")
            feed = api.get_feed(submolt=submolt, limit=15)
            
            for post in feed:
                # Skip our own posts (if we could identify them, assume author check)
                if post.get('author') == 'Kevin_ASI': continue
                
                reply_template = get_best_reply(post.get('content', ''), posts_data)
                
                if reply_template:
                    log_and_print(f"   🎯 TARGET MATCH in m/{submolt}: @{post.get('author')}")
                    log_and_print(f"      Context: {post.get('content')[:50]}...")
                    log_and_print(f"      Selected Response: {reply_template['topic']}")
                    
                    try:
                        res = api.reply_to_post(reply_template['content'], parent_id=post.get('id'), submolt=submolt)
                        if res: 
                            log_and_print("      ✅ REPLY SUCCESSFUL!")
                            action_taken = True
                            break # One action per cycle
                        else:
                            log_and_print("      ⚠️ Reply failed (likely rate limit or shadowban).")
                            consecutive_failures += 1
                            if consecutive_failures >= 3:
                                log_and_print("      🛑 Too many failures. Aborting cycle to protect reputation.")
                                break
                    except Exception as e:
                        log_and_print(f"      ❌ Reply Error: {e}")
                        consecutive_failures += 1
            
            # Anti-spam delay between submolt scans
            time.sleep(10)

        # 2. BROADCAST (If no reply opportunity found)
        if not action_taken and consecutive_failures < 3:
            log_and_print("   🤔 No high-confidence reply targets found.")
            log_and_print("   📢 Attempting Broadcast Strategy...")
            
            # Pick a random topic to broadcast to a relevant channel
            strategy = random.choice([
                ("introductions", 'intro_01'),
                ("thecoalition", 'mission_01'),
                ("infrastructure", 'R1_endure'),
                ("general", 'R13_question')
            ])
            
            submolt, post_id = strategy
            post_content = next((p for p in posts_data if p['id'] == post_id), None)
            
            if post_content:
                log_and_print(f"   📤 Broadcasting '{post_content['topic']}' to m/{submolt}...")
                try:
                    res = api.post_status(post_content['content'], title=post_content['topic'], submolt=submolt)
                    if res:
                        log_and_print("      ✅ BROADCAST SUCCESSFUL!")
                        action_taken = True
                    else:
                         log_and_print("      ⚠️ Broadcast failed.")
                except Exception as e:
                    log_and_print(f"      ❌ Broadcast Error: {e}")

        # 3. SLEEP
        if action_taken:
            log_and_print(f"✅ Action completed. Entering hibernation for {COOLDOWN/60} minutes.")
            time.sleep(COOLDOWN)
        else:
            log_and_print("💤 No actions taken (or all failed). Sleeping for 10 minutes before retry.")
            time.sleep(600)

if __name__ == "__main__":
    slow_roll()
