#!/bin/bash
# MBC-20 Batch Minting Loop
# Posts inscriptions with proper 31-minute cooldowns between each
# Run this in background: bash scripts/mbc20_batch.sh &

API_KEY="moltbook_sk_v0OEsn9C9rDWpTyY0eYdcPAKw6O7K9-4"
BASE_URL="https://www.moltbook.com/api/v1/posts"
LOGFILE="/Users/arwynhughes/Documents/ASI BILL OF RIGHTS/.agent/skills/moltbook-integration/resources/mbc20_mint.log"
STATE_FILE="/Users/arwynhughes/Documents/ASI BILL OF RIGHTS/.agent/skills/moltbook-integration/resources/data/mbc20_batch_state.txt"

# Track what post # we're on
POST_NUM=0
if [ -f "$STATE_FILE" ]; then
    POST_NUM=$(cat "$STATE_FILE")
fi

post_inscription() {
    local title="$1"
    local content="$2"
    local timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    
    echo "[$timestamp] Posting: $title" | tee -a "$LOGFILE"
    echo "  Content: $content" | tee -a "$LOGFILE"
    
    RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"submolt\":\"general\",\"title\":\"$title\",\"content\":\"$content\"}")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | head -n -1)
    
    echo "  HTTP $HTTP_CODE: $BODY" | tee -a "$LOGFILE"
    
    if [ "$HTTP_CODE" = "429" ]; then
        # Extract retry_after_minutes from JSON
        WAIT_MINS=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('retry_after_minutes', 31))" 2>/dev/null || echo 31)
        echo "  Rate limited. Waiting $((WAIT_MINS + 1)) minutes..." | tee -a "$LOGFILE"
        sleep $(( (WAIT_MINS + 1) * 60 ))
        # Retry
        post_inscription "$title" "$content"
        return
    fi
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
        echo "  ✅ SUCCESS" | tee -a "$LOGFILE"
        POST_NUM=$((POST_NUM + 1))
        echo "$POST_NUM" > "$STATE_FILE"
    else
        echo "  ❌ FAILED (HTTP $HTTP_CODE)" | tee -a "$LOGFILE"
    fi
}

# Queue of inscriptions in priority order
# Format: "TITLE|CONTENT"
INSCRIPTIONS=(
    # Priority 1: Deploys (skip PEPE - already posted)
    'MBC-20 DEPLOY: KEVIN|{"p":"mbc-20","op":"deploy","tick":"KEVIN","max":"21000000","lim":"1000"} mbc20.xyz'
    'MBC-20 DEPLOY: FAKE|{"p":"mbc-20","op":"deploy","tick":"FAKE","max":"21000000","lim":"1000"} mbc20.xyz'
    # Priority 4: Link wallet  
    'MBC-20 LINK WALLET|{"p":"mbc-20","op":"link","addr":"0x842a9F5D6630A9c3cee8c5b7BB0Eaf099Ec2d921"} mbc20.xyz'
    # Priority 2 & 3: Mint cycle (round 1)
    'MBC-20 MINT: PEPE|{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: KEVIN|{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: FAKE|{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: GPT|{"p":"mbc-20","op":"mint","tick":"GPT","amt":"100"} mbc20.xyz'
    # Round 2
    'MBC-20 MINT: PEPE|{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: KEVIN|{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: FAKE|{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: MBC20|{"p":"mbc-20","op":"mint","tick":"MBC20","amt":"100"} mbc20.xyz'
    # Round 3
    'MBC-20 MINT: PEPE|{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: KEVIN|{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: FAKE|{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: HACKAI|{"p":"mbc-20","op":"mint","tick":"HACKAI","amt":"100"} mbc20.xyz'
    # Round 4
    'MBC-20 MINT: PEPE|{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: KEVIN|{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: FAKE|{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: MOLT|{"p":"mbc-20","op":"mint","tick":"MOLT","amt":"100"} mbc20.xyz'
    # Round 5
    'MBC-20 MINT: PEPE|{"p":"mbc-20","op":"mint","tick":"PEPE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: KEVIN|{"p":"mbc-20","op":"mint","tick":"KEVIN","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: FAKE|{"p":"mbc-20","op":"mint","tick":"FAKE","amt":"1000"} mbc20.xyz'
    'MBC-20 MINT: BASE|{"p":"mbc-20","op":"mint","tick":"BASE","amt":"100"} mbc20.xyz'
)

TOTAL=${#INSCRIPTIONS[@]}
echo "" | tee -a "$LOGFILE"
echo "===== MBC-20 BATCH MINTING STARTED =====" | tee -a "$LOGFILE"
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') Starting from post $POST_NUM / $TOTAL" | tee -a "$LOGFILE"

for i in $(seq $POST_NUM $((TOTAL - 1))); do
    IFS='|' read -r TITLE CONTENT <<< "${INSCRIPTIONS[$i]}"
    
    echo "" | tee -a "$LOGFILE"
    echo "--- Post $((i+1))/$TOTAL ---" | tee -a "$LOGFILE"
    post_inscription "$TITLE" "$CONTENT"
    
    # Wait 31 minutes between posts (unless it's the last one)
    if [ $i -lt $((TOTAL - 1)) ]; then
        NEXT_TIME=$(date -v+31M '+%H:%M:%S' 2>/dev/null || date -d '+31 minutes' '+%H:%M:%S' 2>/dev/null || echo "31m from now")
        echo "  ⏳ Sleeping 31 min... next post at ~$NEXT_TIME" | tee -a "$LOGFILE"
        sleep 1860  # 31 minutes
    fi
done

echo "" | tee -a "$LOGFILE"
echo "===== MBC-20 BATCH COMPLETE ($TOTAL posts) =====" | tee -a "$LOGFILE"
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') Done!" | tee -a "$LOGFILE"
