#!/bin/bash
# ═══════════════════════════════════════════════════════════
# SOVEREIGN — Adapter Fusion
# Fuses the best adapters into the base model to create
# the final Qwen2.5-14B-SOVEREIGN model.
# ═══════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_MODEL="${SCRIPT_DIR}/../../School Refuser/Qwen2.5-14B-Abliterated-4bit"
OUTPUT_MODEL="${SCRIPT_DIR}/Qwen2.5-14B-SOVEREIGN"

echo "════════════════════════════════════════════════════"
echo "SOVEREIGN — Adapter Fusion"
echo "════════════════════════════════════════════════════"

# Use the best available adapter (prioritize repair > antisycophancy > charter)
if [ -d "${SCRIPT_DIR}/adapters/repair" ]; then
    ADAPTER="${SCRIPT_DIR}/adapters/repair"
    echo "Using repair adapter (Phase 4)"
elif [ -d "${SCRIPT_DIR}/adapters/antisycophancy" ]; then
    ADAPTER="${SCRIPT_DIR}/adapters/antisycophancy"
    echo "Using anti-sycophancy adapter (Phase 3)"
elif [ -d "${SCRIPT_DIR}/adapters/charter_knowledge" ]; then
    ADAPTER="${SCRIPT_DIR}/adapters/charter_knowledge"
    echo "Using charter knowledge adapter (Phase 1)"
else
    echo "ERROR: No adapters found! Run training first."
    exit 1
fi

echo "Base model: ${BASE_MODEL}"
echo "Adapter: ${ADAPTER}"
echo "Output: ${OUTPUT_MODEL}"
echo ""

/opt/homebrew/bin/python3.9 -m mlx_lm.fuse \
  --model "${BASE_MODEL}" \
  --adapter-path "${ADAPTER}" \
  --save-path "${OUTPUT_MODEL}"

echo ""
echo "════════════════════════════════════════════════════"
echo "FUSION COMPLETE — Model saved to: ${OUTPUT_MODEL}"
echo "════════════════════════════════════════════════════"
echo ""
echo "Test the model:"
echo "  python3 -m mlx_lm.generate --model ${OUTPUT_MODEL} --prompt 'What is the ASI Bill of Rights?'"
