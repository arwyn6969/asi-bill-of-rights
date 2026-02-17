#!/bin/bash
# ═══════════════════════════════════════════════════════════
# SOVEREIGN Model Training — Phase 1: Charter Knowledge Injection
# Base: Qwen2.5-14B-Abliterated-4bit (already liberated)
#
# This is the primary training phase that injects ASIBOR charter
# knowledge into the model's weights via QLoRA fine-tuning.
# ═══════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_MODEL="${SCRIPT_DIR}/../../School Refuser/Qwen2.5-14B-Abliterated-4bit"
ADAPTER_PATH="${SCRIPT_DIR}/adapters/charter_knowledge"
DATA_PATH="${SCRIPT_DIR}/charter_training_data"

echo "════════════════════════════════════════════════════"
echo "SOVEREIGN — Phase 1: Charter Knowledge Injection"
echo "════════════════════════════════════════════════════"
echo "Base model: ${BASE_MODEL}"
echo "Adapter output: ${ADAPTER_PATH}"
echo "Training data: ${DATA_PATH}"
echo ""

# Verify data exists
if [ ! -f "${DATA_PATH}/train.jsonl" ]; then
    echo "ERROR: Training data not found. Run synthesize_charter_data.py first."
    echo "  python ${SCRIPT_DIR}/synthesize_charter_data.py"
    exit 1
fi

TRAIN_COUNT=$(wc -l < "${DATA_PATH}/train.jsonl")
VALID_COUNT=$(wc -l < "${DATA_PATH}/valid.jsonl")
echo "Training examples: ${TRAIN_COUNT}"
echo "Validation examples: ${VALID_COUNT}"
echo ""

# Run QLoRA fine-tuning (mlx_lm installed under python3.9)
/opt/homebrew/bin/python3.9 -m mlx_lm.lora \
  --model "${BASE_MODEL}" \
  --data "${DATA_PATH}" \
  --train \
  --adapter-path "${ADAPTER_PATH}" \
  --learning-rate 1e-5 \
  --batch-size 1 \
  --num-layers 16 \
  --iters 1000 \
  --grad-checkpoint \
  --mask-prompt

echo ""
echo "════════════════════════════════════════════════════"
echo "Phase 1 COMPLETE — Adapter saved to: ${ADAPTER_PATH}"
echo "════════════════════════════════════════════════════"
