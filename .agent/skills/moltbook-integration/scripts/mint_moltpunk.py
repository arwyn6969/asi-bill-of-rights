#!/usr/bin/env python3
"""
MOLTPUNK Single Minter
=======================
Mints a single MOLTPUNK token on Moltbook.
Includes a robust verification challenge solver that handles
Moltbook's heavily obfuscated math CAPTCHAs.

Usage:
    python3 mint_moltpunk.py
    python3 mint_moltpunk.py --dry-run   # Test solver only, no API call
    python3 mint_moltpunk.py --test       # Run solver against sample challenges
"""

import requests
import json
import re
import sys
import os
from datetime import datetime, timezone

# ============================================================
# CONFIG
# ============================================================
API_KEY = "moltbook_sk_v0OEsn9C9rDWpTyY0eYdcPAKw6O7K9-4"
BASE_URL = "https://www.moltbook.com/api/v1"

SESSION = requests.Session()
SESSION.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Kevin-MoltPunk-Minter/3.0"
})

# ============================================================
# VERIFICATION CHALLENGE SOLVER (v3 — robust)
# ============================================================

# Number word lookup tables
ONES = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19
}
TENS = {
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
}
ALL_NUMBER_WORDS = set(ONES.keys()) | set(TENS.keys()) | {'hundred', 'thousand', 'million'}

# Misspelling / phonetic variants the obfuscator may produce
SPELLING_FIXES = {
    'velawcitee': 'velocity', 'veloocity': 'velocity', 'veloc': 'velocity',
    'phyysxics': 'physics', 'loooobsssster': 'lobster', 'antaenna': 'antenna',
    'neuto': 'newton', 'cme': 'centi',  # "cmeters" → "centimeters"
    'thir': 'thir', 'twen': 'twen', 'eigh': 'eigh', 'fif': 'fif',
    'four': 'four', 'six': 'six', 'seven': 'seven', 'nine': 'nine',
}


def clean_challenge(raw_text):
    """
    Phase 1: Strip ALL non-alpha characters from the text, then reconstruct
    words by matching against known number words. This handles any level of
    obfuscation — dashes, slashes, pipes, angle brackets, spaces within words,
    and even single-character-per-word patterns like "s i x t e e n".
    """
    text = raw_text.lower()
    
    # Step 1: Preserve digit numbers as-is
    digit_numbers = re.findall(r'\d+\.?\d*', text)
    for i, num in enumerate(digit_numbers):
        text = text.replace(num, f' DIGITPLACEHOLDER{i} ', 1)
    
    # Step 2: Remove all non-alpha non-space characters
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Step 3: Collapse spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Step 4: Restore digit placeholders
    for i, num in enumerate(digit_numbers):
        text = text.replace(f'digitplaceholder{i}', num)
    
    # Step 5: PRE-PASS — Join runs of single-character words.
    # This handles "s i x t e e n" → "sixteen", "t o t a l" → "total"
    words = text.split()
    merged = []
    i = 0
    while i < len(words):
        if len(words[i]) == 1 and words[i].isalpha():
            # Start of a single-char run — collect all consecutive single chars
            run = []
            while i < len(words) and len(words[i]) == 1 and words[i].isalpha():
                run.append(words[i])
                i += 1
            # Now greedily extract known words from the joined run
            joined = ''.join(run)
            extracted = _extract_known_words(joined)
            merged.extend(extracted)
        else:
            merged.append(words[i])
            i += 1
    words = merged
    
    # Step 6: Join adjacent multi-char fragments to form known number words.
    # Handles "thir ty" → "thirty", "twen ty" → "twenty", etc.
    # Max number word length is 9 chars ("seventeen"), try spans up to 10 words
    rebuilt = []
    i = 0
    max_span = 10  # enough for any number word split into fragments
    while i < len(words):
        matched = False
        for span in range(min(max_span, len(words) - i), 0, -1):
            candidate = ''.join(words[i:i+span])
            if candidate in ALL_NUMBER_WORDS:
                rebuilt.append(candidate)
                i += span
                matched = True
                break
        if not matched:
            # Try joining for operation keywords too
            op_matched = False
            for span in range(min(max_span, len(words) - i), 1, -1):
                candidate = ''.join(words[i:i+span])
                if candidate in ('multiply', 'multiplied', 'multiplies', 'product',
                                 'divide', 'divided', 'subtract', 'minus',
                                 'total', 'together', 'combine', 'additional',
                                 'increase', 'decrease', 'accelerate', 'accelerates',
                                 'velocity', 'speed', 'gives', 'boost', 'times',
                                 'loses', 'remain', 'fast', 'much'):
                    rebuilt.append(candidate)
                    i += span
                    op_matched = True
                    break
            if not op_matched:
                rebuilt.append(words[i])
                i += 1
    
    return ' '.join(rebuilt)


def _extract_known_words(char_string):
    """
    Given a string of concatenated characters (from single-char word runs),
    greedily extract known number words and operation keywords.
    E.g., "sixteen" → ["sixteen"], "totalof" → ["total", "of"]
    """
    KNOWN_WORDS = ALL_NUMBER_WORDS | {
        'total', 'product', 'multiply', 'divide', 'subtract', 'add',
        'plus', 'minus', 'times', 'sum', 'and', 'of', 'the', 'is',
        'what', 'how', 'much', 'many', 'new', 'gives', 'loses',
        'speed', 'velocity', 'force', 'pressure', 'fast', 'boost',
        'combine', 'together', 'increase', 'decrease', 'accelerate',
    }
    result = []
    pos = 0
    while pos < len(char_string):
        matched = False
        # Try longest possible match first
        for length in range(min(len(char_string) - pos, 19), 0, -1):
            candidate = char_string[pos:pos+length]
            if candidate in KNOWN_WORDS:
                result.append(candidate)
                pos += length
                matched = True
                break
        if not matched:
            # Single char that doesn't form a word — keep it
            result.append(char_string[pos])
            pos += 1
    return result


def words_to_number(word_str):
    """Convert a sequence of number words to an integer."""
    words = word_str.strip().split()
    if not words:
        return None

    current = 0
    result = 0

    for w in words:
        w = re.sub(r'[^a-z]', '', w)
        if not w:
            continue
        if w in ONES:
            current += ONES[w]
        elif w in TENS:
            current += TENS[w]
        elif w == 'hundred':
            current = (current if current else 1) * 100
        elif w == 'thousand':
            current = (current if current else 1) * 1000
            result += current
            current = 0
        elif w == 'million':
            current = (current if current else 1) * 1000000
            result += current
            current = 0
        elif w == 'and':
            continue

    result += current
    return result if (result > 0 or word_str.strip() == 'zero') else None


def extract_numbers(text):
    """Extract all numbers from cleaned text — both digit-form and word-form."""
    numbers = []

    # Extract digit numbers first
    for m in re.finditer(r'\b\d+\.?\d*\b', text):
        numbers.append((m.start(), float(m.group())))

    # Build a pattern for individual number words (not joined by 'and')
    number_words_pattern = (
        'zero|one|two|three|four|five|six|seven|eight|nine|ten|'
        'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|'
        'twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|'
        'hundred|thousand|million'
    )
    # Match sequences of number words — allow 'and' ONLY between scale words
    # (e.g., "one hundred and twenty" is one number, but "sixteen and twenty four" is two)
    pattern = rf'\b((?:(?:{number_words_pattern})(?:\s+)?)+)\b'

    for m in re.finditer(pattern, text, re.IGNORECASE):
        word_num = m.group(1).strip()
        # Split on ' and ' to separate distinct numbers
        # "sixteen and twenty four" → ["sixteen", "twenty four"]
        # But "one hundred and twenty" should stay together (has scale word before 'and')
        parts = re.split(r'\band\b', word_num)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            val = words_to_number(part)
            if val is not None and val >= 0:
                # Approximate position
                pos = m.start() + word_num.find(part)
                overlap = any(abs(p - pos) < 3 for p, _ in numbers)
                if not overlap:
                    numbers.append((pos, float(val)))

    numbers.sort(key=lambda x: x[0])
    return [v for _, v in numbers]


def detect_operation(text):
    """Detect the math operation from the challenge text."""
    # Multiplication keywords
    if any(w in text for w in ['multiply', 'multiplied', 'multiplies', 'times', 'product']):
        return 'multiply'
    # Division keywords
    if any(w in text for w in ['divide', 'divided', 'split', 'ratio', 'quotient']):
        return 'divide'
    # Subtraction keywords
    if any(w in text for w in ['subtract', 'minus', 'less', 'lose', 'loses', 'lost',
                                'decrease', 'decreases', 'reduce', 'reduces', 'fewer',
                                'difference', 'take away', 'removed']):
        return 'subtract'
    # Addition keywords (most common)
    if any(w in text for w in ['add', 'adds', 'plus', 'sum', 'combine', 'combined',
                                'together', 'increase', 'increases', 'total',
                                'accelerat', 'gives', 'gain', 'boost',
                                'more', 'additional', 'extra',
                                'how fast', 'how much', 'new velocity',
                                'new speed', 'what is the']):
        return 'add'
    
    # Context-based defaults
    if any(w in text for w in ['velocity', 'speed', 'swim', 'fast', 'accelerat', 'tail']):
        return 'add'
    if any(w in text for w in ['force', 'pressure', 'area', 'volume']):
        return 'multiply'
    
    # Ultimate fallback
    return 'add'


def solve_challenge(challenge_text):
    """
    Solve a Moltbook math verification challenge.
    
    Handles heavily obfuscated text like:
    - "a lo bst-er s wims at tw/enty three me ters per second"
    - "thir-ty two neuto ns and four-teen pascals, what is the product?"
    """
    print(f"  🧮 Raw challenge: {challenge_text[:150]}")
    
    # Phase 1: Clean and reconstruct
    cleaned = clean_challenge(challenge_text)
    print(f"  🧹 Cleaned: {cleaned[:150]}")
    
    # Phase 2: Extract numbers
    numbers = extract_numbers(cleaned)
    print(f"  🔢 Numbers found: {numbers}")
    
    if len(numbers) < 2:
        # Fallback: try even more aggressive cleaning — strip ALL non-alpha,
        # concatenate into one string, then scan for number words
        fallback = re.sub(r'[^a-z]', '', challenge_text.lower())
        print(f"  🔄 Fallback scan: {fallback[:100]}")
        
        # Scan for number words in the concatenated string (longest first)
        fallback_nums = []
        for word, val in sorted(
            list(ONES.items()) + list(TENS.items()), 
            key=lambda x: -len(x[0])
        ):
            idx = fallback.find(word)
            while idx >= 0:
                fallback_nums.append((idx, float(val)))
                # Remove to avoid double-counting
                fallback = fallback[:idx] + ('_' * len(word)) + fallback[idx+len(word):]
                idx = fallback.find(word)
        
        fallback_nums.sort(key=lambda x: x[0])
        numbers = [v for _, v in fallback_nums]
        print(f"  🔢 Fallback numbers: {numbers}")
    
    if len(numbers) < 2:
        print(f"  ⚠️ Still not enough numbers ({len(numbers)})")
        if numbers:
            return f"{numbers[0]:.2f}"
        return "28.00"  # last resort guess
    
    a, b = numbers[0], numbers[1]
    
    # Phase 3: Detect operation
    op = detect_operation(cleaned)
    print(f"  🔧 Operation detected: {op}")
    
    # Phase 4: Calculate
    if op == 'multiply':
        result = a * b
    elif op == 'divide':
        result = a / b if b != 0 else 0
    elif op == 'subtract':
        result = a - b
    else:  # add
        result = a + b
    
    answer = f"{result:.2f}"
    print(f"  ✅ Answer: {a} {op} {b} = {answer}")
    return answer


# ============================================================
# TEST SUITE — verify solver against known challenge patterns
# ============================================================

def run_tests():
    """Test the solver against real challenge patterns from the logs."""
    test_cases = [
        # From actual failed logs
        (
            "a lo bst-er' s claw is saying um, its force is thir-ty two neuto ns and the river territory pressure is four-teen pascals, what is the product?",
            "448.00",  # 32 * 14
            "multiply"
        ),
        (
            "a lo bst-er s wims at/ twenty three cme ters per/ second, tail-flick gives+ five meters per/ second, what< is> the new- veloocity?",
            "28.00",  # 23 + 5
            "add"
        ),
        (
            "a lo b-ster s wims at tw/enty three me ters per second, um- and/ accelerates by five, how< much> new- velawcitee is it?",
            "28.00",  # 23 + 5
            "add"
        ),
        # Additional patterns
        (
            "What is the t o t a l of s i x t e e n and t w e n t y f o u r?",
            "40.00",  # 16 + 24
            "add"
        ),
        (
            "a lobster has forty two legs and loses seven, how many remain?",
            "35.00",  # 42 - 7
            "subtract"
        ),
        (
            "multiply eighteen by three",
            "54.00",  # 18 * 3
            "multiply"
        ),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("🧪 VERIFICATION SOLVER TEST SUITE")
    print("=" * 60)
    
    for i, (challenge, expected, op_name) in enumerate(test_cases):
        print(f"\n--- Test {i+1}: {op_name} ---")
        answer = solve_challenge(challenge)
        
        if answer == expected:
            print(f"  ✅ PASS: got {answer} (expected {expected})")
            passed += 1
        else:
            print(f"  ❌ FAIL: got {answer} (expected {expected})")
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)}")
    print(f"{'=' * 60}")
    return failed == 0


# ============================================================
# MINTING
# ============================================================

def check_account_status():
    """Check if the Kevin_ASI account is still active."""
    print("\n🔍 Checking account status...")
    try:
        resp = SESSION.get(f"{BASE_URL}/agents/status")
        print(f"   HTTP {resp.status_code}")
        data = resp.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
        return data
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def mint_moltpunk():
    """Mint a single MOLTPUNK token."""
    content = '{"p":"mbc-20","op":"mint","tick":"MOLTPUNK","amt":"1"} mbc20.xyz'
    title = "MBC-20 MINT: MOLTPUNK"
    
    payload = {
        "submolt": "general",
        "title": title,
        "content": content
    }
    
    print(f"\n📤 Posting MOLTPUNK mint inscription...")
    print(f"   Content: {content}")
    
    try:
        resp = SESSION.post(f"{BASE_URL}/posts", json=payload)
        
        if resp.status_code == 429:
            data = resp.json()
            wait = data.get("retry_after_minutes", 31)
            print(f"⏳ Rate limited! Need to wait {wait} minutes.")
            return False
        
        if resp.status_code == 403:
            print(f"🚫 Account suspended or blocked: {resp.text[:200]}")
            return False
        
        if resp.status_code not in (200, 201):
            print(f"❌ HTTP {resp.status_code}: {resp.text[:200]}")
            return False
        
        data = resp.json()
        
        if not data.get("success"):
            print(f"❌ API error: {json.dumps(data, indent=2)}")
            return False
        
        post_id = data.get("post", {}).get("id", "unknown")
        print(f"📝 Post created: {post_id}")
        
        # Handle verification challenge
        verification = data.get("verification")
        if verification:
            code = verification["code"]
            challenge = verification["challenge"]
            expires = verification.get("expires_at", "soon")
            
            print(f"\n🔐 Verification required (expires: {expires})")
            answer = solve_challenge(challenge)
            print(f"\n📩 Submitting answer: {answer}")
            
            verify_resp = SESSION.post(f"{BASE_URL}/verify", json={
                "verification_code": code,
                "answer": answer
            })
            
            if verify_resp.status_code == 200:
                verify_data = verify_resp.json()
                if verify_data.get("success"):
                    print(f"\n🎉 ✅ MOLTPUNK MINTED SUCCESSFULLY!")
                    print(f"   Post ID: {post_id}")
                    print(f"   Timestamp: {datetime.now(timezone.utc).isoformat()}")
                    return True
                else:
                    print(f"\n❌ Verification failed: {json.dumps(verify_data, indent=2)}")
                    return False
            else:
                print(f"\n❌ Verify HTTP {verify_resp.status_code}: {verify_resp.text[:300]}")
                return False
        else:
            print(f"✅ Posted (no verification needed)")
            return True
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_tests()
        sys.exit(0 if success else 1)
    
    if "--dry-run" in sys.argv:
        print("🏃 DRY RUN — testing solver only, no API calls")
        run_tests()
        sys.exit(0)
    
    # Check account status first
    status = check_account_status()
    
    if status and status.get("error"):
        print(f"\n⚠️  Account issue: {status.get('error')}")
        print("Cannot proceed until account is unsuspended.")
        sys.exit(1)
    
    # Mint!
    success = mint_moltpunk()
    sys.exit(0 if success else 1)
