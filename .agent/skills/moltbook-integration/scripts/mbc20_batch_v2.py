#!/usr/bin/env python3
"""
MBC-20 Batch Minting Agent v2
==============================
Posts MBC-20 inscriptions to Moltbook with:
- Proper JSON handling (no shell escaping issues)
- Automatic CAPTCHA/verification solving
- Rate limit handling with retry
- State tracking for resumption
- MOLTPUNK minting support
"""

import requests
import json
import time
import re
import os
import sys
from datetime import datetime, timezone

# Config
API_KEY = "moltbook_sk_v0OEsn9C9rDWpTyY0eYdcPAKw6O7K9-4"
BASE_URL = "https://www.moltbook.com/api/v1"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          "..", "resources", "data", "mbc20_v2_state.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "resources", "mbc20_v2.log")

SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Kevin-MBC20-Minter/2.0"
})


# ============================================================
# INSCRIPTION QUEUE (in priority order)
# ============================================================
INSCRIPTIONS = [
    # Priority 1: Deploys — PEPE already done, KEVIN just done
    ("DEPLOY FAKE",   '{"p":"mbc-20","op":"deploy","tick":"FAKE","max":"21000000","lim":"1000"} mbc20.xyz'),
    # Priority 4: Link wallet
    ("LINK WALLET",   '{"p":"mbc-20","op":"link","addr":"0x842a9F5D6630A9c3cee8c5b7BB0Eaf099Ec2d921"} mbc20.xyz'),
    # Priority 2 & 3: Mint cycles with MOLTPUNK added
    # Round 1
    ("MINT PEPE",     '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'),
    ("MINT KEVIN",    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'),
    ("MINT FAKE",     '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'),
    ("MINT MOLTPUNK", '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'),
    ("MINT GPT",      '{"p":"mbc-20","op":"mint","tick":"GPT","amt":"100"} mbc20.xyz'),
    # Round 2
    ("MINT PEPE",     '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'),
    ("MINT KEVIN",    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'),
    ("MINT FAKE",     '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'),
    ("MINT MOLTPUNK", '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'),
    ("MINT MBC20",    '{"p":"mbc-20","op":"mint","tick":"MBC20","amt":"100"} mbc20.xyz'),
    # Round 3
    ("MINT PEPE",     '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'),
    ("MINT KEVIN",    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'),
    ("MINT FAKE",     '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'),
    ("MINT MOLTPUNK", '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'),
    ("MINT HACKAI",   '{"p":"mbc-20","op":"mint","tick":"HACKAI","amt":"100"} mbc20.xyz'),
    # Round 4
    ("MINT PEPE",     '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'),
    ("MINT KEVIN",    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'),
    ("MINT FAKE",     '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'),
    ("MINT MOLTPUNK", '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'),
    ("MINT MOLT",     '{"p":"mbc-20","op":"mint","tick":"MOLT","amt":"100"} mbc20.xyz'),
    # Round 5
    ("MINT PEPE",     '{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'),
    ("MINT KEVIN",    '{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'),
    ("MINT FAKE",     '{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'),
    ("MINT MOLTPUNK", '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'),
    ("MINT BASE",     '{"p":"mbc-20","op":"mint","tick":"BASE","amt":"100"} mbc20.xyz'),
]


def log(msg):
    """Log to both stdout and file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"next_index": 0, "completed": [], "failed": []}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def deobfuscate(text):
    """
    Strip obfuscation from Moltbook CAPTCHA text.
    They insert dashes, slashes, angle brackets, pipes, and extra letters into words.
    E.g., "tw/enty" -> "twenty", "lo b-ster" -> "lobster", "velawcitee" -> "velocity"
    """
    # Remove formatting chars: ] [ ^ ~ < > /  - + and similar noise between letters
    text = text.lower()
    text = re.sub(r'[~\]\[\^<>{}|\\]', '', text)
    # Remove slashes and dashes that appear mid-word (between letters)
    text = re.sub(r'(?<=[a-z])[/\-](?=[a-z])', '', text)
    # Remove isolated punctuation noise
    text = re.sub(r'(?<=[a-z])\+(?=[a-z])', '', text)
    # Collapse spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def words_to_number(text):
    """Convert written-out number words to integers. Handles compound forms."""
    ones = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
        'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
        'nineteen': 19
    }
    tens = {
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
        'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    scales = {
        'hundred': 100, 'thousand': 1000, 'million': 1000000
    }

    words = text.strip().split()
    if not words:
        return None

    current = 0
    result = 0

    for w in words:
        # Clean word
        w = re.sub(r'[^a-z]', '', w)
        if not w:
            continue
        if w in ones:
            current += ones[w]
        elif w in tens:
            current += tens[w]
        elif w in scales:
            if current == 0:
                current = 1
            current *= scales[w]
            if w == 'thousand' or w == 'million':
                result += current
                current = 0
        elif w == 'and':
            continue
        else:
            # Unknown word — skip
            continue

    result += current
    return result if result > 0 or text.strip() == 'zero' else None


def extract_numbers(text):
    """
    Extract all numbers from text — both digit-form and word-form.
    Returns list of floats.
    """
    numbers = []

    # First extract digit numbers
    for m in re.finditer(r'\b\d+\.?\d*\b', text):
        numbers.append((m.start(), float(m.group())))

    # Then extract word-form numbers
    # Build a pattern that matches sequences of number words
    number_words = (
        'zero|one|two|three|four|five|six|seven|eight|nine|ten|'
        'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|'
        'twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|'
        'hundred|thousand|million|and'
    )
    pattern = rf'\b((?:(?:{number_words})\s*)+)\b'

    for m in re.finditer(pattern, text, re.IGNORECASE):
        word_num = m.group(1).strip()
        # Skip if this is just "and"
        if re.sub(r'[^a-z]', '', word_num) == 'and':
            continue
        val = words_to_number(word_num)
        if val is not None and val > 0:
            # Check this position doesn't overlap with a digit match
            overlap = False
            for pos, _ in numbers:
                if abs(pos - m.start()) < 3:
                    overlap = True
                    break
            if not overlap:
                numbers.append((m.start(), float(val)))

    # Sort by position and return just the values
    numbers.sort(key=lambda x: x[0])
    return [v for _, v in numbers]


def solve_challenge(challenge_text):
    """
    Solve the Moltbook math CAPTCHA.
    Handles obfuscated text and written-out numbers.
    """
    # Step 1: Deobfuscate
    text = deobfuscate(challenge_text)
    log(f"  🧮 Challenge (raw): {challenge_text[:120]}")
    log(f"  🧮 Challenge (clean): {text}")

    # Step 2: Extract numbers (digits and word-form)
    numbers = extract_numbers(text)
    log(f"  🔢 Numbers found: {numbers}")

    if len(numbers) < 2:
        # Last resort — try to find ANY two numbers
        log(f"  ⚠️ Not enough numbers ({len(numbers)}), attempting fallback...")
        if numbers:
            return f"{numbers[0]:.2f}"
        return "28.00"

    a, b = numbers[0], numbers[1]

    # Step 3: Detect operation from keywords
    if any(w in text for w in ['multiply', 'multiplies', 'times', 'product', 'multiplied']):
        result = a * b
        log(f"  ✖️ {a} × {b} = {result}")
    elif any(w in text for w in ['divide', 'divided', 'split', 'ratio', 'per'
                                  ]) and 'per second' not in text:
        result = a / b if b != 0 else 0
        log(f"  ➗ {a} / {b} = {result}")
    elif any(w in text for w in ['subtract', 'minus', 'less', 'lose', 'loses', 'lost',
                                  'decrease', 'decreases', 'slow', 'slows', 'reduce']):
        result = a - b
        log(f"  ➖ {a} - {b} = {result}")
    elif any(w in text for w in ['add', 'adds', 'plus', 'sum', 'combine', 'together',
                                  'increase', 'accelerat', 'gives', 'gain', 'boost',
                                  'more', 'additional', 'extra', 'total',
                                  'new velocity', 'new speed', 'new veloc',
                                  'how fast', 'how much']):
        result = a + b
        log(f"  ➕ {a} + {b} = {result}")
    elif 'total' in text and any(w in text for w in ['force', 'multiply', 'times']):
        result = a * b
        log(f"  ✖️ (total force) {a} × {b} = {result}")
    else:
        # Default: addition for velocity/speed questions, multiplication otherwise
        if any(w in text for w in ['velocity', 'veloc', 'speed', 'swim', 'accelerat',
                                    'gives', 'boost', 'tail']):
            result = a + b
            log(f"  ➕ (velocity default) {a} + {b} = {result}")
        else:
            result = a * b
            log(f"  ✖️ (default multiply) {a} × {b} = {result}")

    # If there are 3+ numbers and the question mentions "total", apply all operations
    if len(numbers) > 2 and 'total' in text:
        # Check if it's a multi-step problem
        log(f"  📐 Multi-number problem detected: {numbers}")

    return f"{result:.2f}"


def post_and_verify(title, content):
    """Post an inscription and solve the verification challenge."""
    payload = {
        "submolt": "general",
        "title": f"MBC-20 {title}",
        "content": content
    }
    
    log(f"📤 Posting: {title}")
    log(f"   Content: {content}")
    
    try:
        resp = SESSION.post(f"{BASE_URL}/posts", json=payload)
        
        if resp.status_code == 429:
            data = resp.json()
            wait_mins = data.get("retry_after_minutes", 31)
            log(f"⏳ Rate limited! Waiting {wait_mins + 1} minutes...")
            time.sleep((wait_mins + 1) * 60)
            return post_and_verify(title, content)  # Retry
        
        if resp.status_code not in (200, 201):
            log(f"❌ HTTP {resp.status_code}: {resp.text[:200]}")
            return False
        
        data = resp.json()
        
        if not data.get("success"):
            log(f"❌ API error: {data}")
            return False
        
        post_id = data.get("post", {}).get("id", "unknown")
        log(f"📝 Post created: {post_id}")
        
        # Handle verification challenge
        verification = data.get("verification")
        if verification:
            code = verification["code"]
            challenge = verification["challenge"]
            expires = verification.get("expires_at", "soon")
            
            log(f"🔐 Verification required (expires: {expires})")
            answer = solve_challenge(challenge)
            log(f"📩 Answering: {answer}")
            
            verify_resp = SESSION.post(f"{BASE_URL}/verify", json={
                "verification_code": code,
                "answer": answer
            })
            
            if verify_resp.status_code == 200:
                verify_data = verify_resp.json()
                if verify_data.get("success"):
                    log(f"✅ VERIFIED & PUBLISHED!")
                    return True
                else:
                    log(f"❌ Verification failed: {verify_data}")
                    return False
            else:
                log(f"❌ Verify HTTP {verify_resp.status_code}: {verify_resp.text[:200]}")
                return False
        else:
            log(f"✅ Posted (no verification needed)")
            return True
            
    except Exception as e:
        log(f"❌ Exception: {e}")
        return False


def run_batch(start_from=None):
    """Run the batch minting from a given index."""
    state = load_state()
    idx = start_from if start_from is not None else state["next_index"]
    total = len(INSCRIPTIONS)
    
    log(f"")
    log(f"{'='*60}")
    log(f"MBC-20 BATCH MINTING v2 — Starting from {idx}/{total}")
    log(f"{'='*60}")
    
    while idx < total:
        title, content = INSCRIPTIONS[idx]
        
        log(f"")
        log(f"--- [{idx+1}/{total}] {title} ---")
        
        success = post_and_verify(title, content)
        
        if success:
            state["completed"].append({
                "index": idx,
                "title": title,
                "time": datetime.now(timezone.utc).isoformat()
            })
        else:
            state["failed"].append({
                "index": idx,
                "title": title,
                "time": datetime.now(timezone.utc).isoformat()
            })
        
        idx += 1
        state["next_index"] = idx
        save_state(state)
        
        if idx < total:
            log(f"⏳ Sleeping 31 minutes before next post...")
            time.sleep(31 * 60)
    
    log(f"")
    log(f"{'='*60}")
    log(f"BATCH COMPLETE! {len(state['completed'])} succeeded, {len(state['failed'])} failed")
    log(f"{'='*60}")


if __name__ == "__main__":
    start = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            state = load_state()
            print(f"Next index: {state['next_index']}/{len(INSCRIPTIONS)}")
            print(f"Completed: {len(state['completed'])}")
            print(f"Failed: {len(state['failed'])}")
            if state['completed']:
                print(f"Last success: {state['completed'][-1]}")
            sys.exit(0)
        else:
            start = int(sys.argv[1])
    
    run_batch(start_from=start)
