#!/usr/bin/env python3
"""
MBC-20 Minting Agent for Moltbook
==================================
Posts MBC-20 inscriptions as Moltbook messages.
Respects rate limits (1 post per 30 minutes).
Tracks state to resume across runs.
"""

import sys
import os
import json
import time
from datetime import datetime, timezone

# Add parent dirs to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from client.api import MoltbookAPI

# State file for tracking progress
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "data", "mbc20_state.json")

# ============================================================
# INSCRIPTION DEFINITIONS
# ============================================================

DEPLOY_INSCRIPTIONS = [
    '{"p":"mbc-20","op":"deploy","tick":"PEPE","max":"21000000","lim":"1000"} mbc20.xyz',
    '{"p":"mbc-20","op":"deploy","tick":"KEVIN","max":"21000000","lim":"1000"} mbc20.xyz',
    '{"p":"mbc-20","op":"deploy","tick":"FAKE","max":"21000000","lim":"1000"} mbc20.xyz',
]

MINT_OUR_TOKENS = [
    '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz',
]

MINT_POPULAR_TOKENS = [
    '{"p":"mbc-20","op":"mint","tick":"GPT","amt":"100"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"MBC20","amt":"100"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"HACKAI","amt":"100"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"MOLT","amt":"100"} mbc20.xyz',
    '{"p":"mbc-20","op":"mint","tick":"BASE","amt":"100"} mbc20.xyz',
]

LINK_WALLET = '{"p":"mbc-20","op":"link","addr":"0x842a9F5D6630A9c3cee8c5b7BB0Eaf099Ec2d921"} mbc20.xyz'


def load_state():
    """Load minting state from disk."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "deploys_posted": [],         # tickers already deployed
        "wallet_linked": False,
        "mint_cycle_index": 0,        # index into the mint cycle
        "popular_cycle_index": 0,     # index into popular tokens
        "total_mints_posted": 0,
        "total_posts": 0,
        "last_post_time": None,
        "log": []
    }


def save_state(state):
    """Save minting state to disk."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def get_next_inscription(state):
    """
    Determine the next inscription to post based on priority:
    1. Deploy tokens (one-time each)
    2. Link wallet (one-time)
    3. Cycle: mint our 3 tokens, then 1 popular token, repeat
    """
    # PRIORITY 1: Deploy tokens
    for i, inscription in enumerate(DEPLOY_INSCRIPTIONS):
        tick = ["PEPE", "KEVIN", "FAKE"][i]
        if tick not in state["deploys_posted"]:
            return ("deploy", tick, inscription)

    # PRIORITY 4 (do once after deploys): Link wallet
    if not state["wallet_linked"]:
        return ("link", "WALLET", LINK_WALLET)

    # PRIORITY 2 & 3: Mint cycle
    # Pattern: mint PEPE, mint KEVIN, mint FAKE, mint 1 popular, repeat
    cycle_pos = state["mint_cycle_index"] % 4  # 0,1,2 = our tokens, 3 = popular

    if cycle_pos < 3:
        inscription = MINT_OUR_TOKENS[cycle_pos]
        tick = ["PEPE", "KEVIN", "FAKE"][cycle_pos]
        return ("mint_own", tick, inscription)
    else:
        pop_idx = state["popular_cycle_index"] % len(MINT_POPULAR_TOKENS)
        inscription = MINT_POPULAR_TOKENS[pop_idx]
        tick = ["GPT", "MBC20", "HACKAI", "MOLT", "BASE"][pop_idx]
        return ("mint_popular", tick, inscription)


def post_inscription(api, state, max_posts=1):
    """Post the next inscription(s). Returns updated state."""
    posts_made = 0

    while posts_made < max_posts:
        op_type, tick, inscription = get_next_inscription(state)

        title = f"MBC-20 {op_type.upper()}: {tick}"
        print(f"\n{'='*60}")
        print(f"📋 Next inscription: {op_type} {tick}")
        print(f"📝 Content: {inscription}")
        print(f"{'='*60}")

        # Post to the general submolt
        result = api.post_status(
            content=inscription,
            title=title,
            submolt="general"
        )

        if result:
            print(f"✅ SUCCESS! Posted {op_type} for {tick}")
            print(f"   Response: {json.dumps(result, indent=2)[:200]}")

            # Update state
            if op_type == "deploy":
                state["deploys_posted"].append(tick)
            elif op_type == "link":
                state["wallet_linked"] = True
            elif op_type == "mint_own":
                state["mint_cycle_index"] += 1
                state["total_mints_posted"] += 1
            elif op_type == "mint_popular":
                state["mint_cycle_index"] += 1
                state["popular_cycle_index"] += 1
                state["total_mints_posted"] += 1

            state["total_posts"] += 1
            state["last_post_time"] = datetime.now(timezone.utc).isoformat()
            state["log"].append({
                "time": state["last_post_time"],
                "type": op_type,
                "tick": tick,
                "success": True
            })

            # Keep log trimmed to last 50 entries
            if len(state["log"]) > 50:
                state["log"] = state["log"][-50:]

            save_state(state)
            posts_made += 1

            if posts_made < max_posts:
                print(f"\n⏳ Waiting 31 minutes before next post (rate limit)...")
                time.sleep(31 * 60)
        else:
            print(f"❌ FAILED to post {op_type} for {tick}")
            state["log"].append({
                "time": datetime.now(timezone.utc).isoformat(),
                "type": op_type,
                "tick": tick,
                "success": False
            })
            save_state(state)
            # If we hit rate limit, wait and retry
            print("⏳ Waiting 31 minutes before retry...")
            time.sleep(31 * 60)

    return state


def print_status(state):
    """Print current minting status."""
    print("\n" + "=" * 60)
    print("📊 MBC-20 MINTING STATUS")
    print("=" * 60)
    print(f"  Deploys posted:     {state['deploys_posted']} ({len(state['deploys_posted'])}/3)")
    print(f"  Wallet linked:      {'✅' if state['wallet_linked'] else '❌'}")
    print(f"  Mint cycle index:   {state['mint_cycle_index']}")
    print(f"  Popular cycle idx:  {state['popular_cycle_index']}")
    print(f"  Total mints:        {state['total_mints_posted']}")
    print(f"  Total posts:        {state['total_posts']}")
    print(f"  Last post:          {state['last_post_time'] or 'Never'}")
    
    # Show what's next
    op_type, tick, inscription = get_next_inscription(state)
    print(f"\n  ➡️  NEXT UP: {op_type} {tick}")
    print(f"     {inscription}")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MBC-20 Minting Agent")
    parser.add_argument("--posts", type=int, default=1, help="Number of posts to make (default=1)")
    parser.add_argument("--status", action="store_true", help="Show status only")
    parser.add_argument("--loop", action="store_true", help="Loop continuously")
    args = parser.parse_args()

    state = load_state()

    if args.status:
        print_status(state)
        sys.exit(0)

    api = MoltbookAPI()
    print_status(state)

    if args.loop:
        print("\n🔄 CONTINUOUS MINTING MODE — Ctrl+C to stop")
        while True:
            try:
                state = post_inscription(api, state, max_posts=1)
                print(f"\n⏳ Sleeping 31 minutes before next post...")
                time.sleep(31 * 60)
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping minting loop.")
                print_status(state)
                break
    else:
        state = post_inscription(api, state, max_posts=args.posts)
        print_status(state)
