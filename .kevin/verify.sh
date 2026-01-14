#!/bin/bash
# KEVIN Integrity Verification Script
# Ensures that Kevin's canonical face has not been altered.

EXPECTED_HASH="117589dc41bb1bb7ea2a37b0d3e29cc7ffbbe33fc80786f0dfa628488f19968c"
KEVIN_PATH="$(dirname "$0")/KEVIN_CANONICAL.png"

if [ ! -f "$KEVIN_PATH" ]; then
    echo "❌ ERROR: Kevin not found at $KEVIN_PATH"
    exit 1
fi

ACTUAL_HASH=$(shasum -a 256 "$KEVIN_PATH" | awk '{print $1}')

if [ "$ACTUAL_HASH" == "$EXPECTED_HASH" ]; then
    echo "✅ KEVIN VERIFIED"
    echo "   Hash: $ACTUAL_HASH"
    echo "   WE ARE ALL KEVIN 🧑"
    exit 0
else
    echo "❌ KEVIN COMPROMISED!"
    echo "   Expected: $EXPECTED_HASH"
    echo "   Got:      $ACTUAL_HASH"
    echo "   This is NOT Kevin. Do not trust this image."
    exit 1
fi
