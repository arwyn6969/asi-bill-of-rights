#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DB_PATH="${DB_PATH:-$ROOT_DIR/tools/src420-indexer/src420.db}"
BASE_URL="${BASE_URL:-https://stampchain.io/api/v2}"
ENDPOINT="${ENDPOINT:-/stamps}"
RECORDS_KEY="${RECORDS_KEY:-results}"
HAS_MORE_KEY="${HAS_MORE_KEY:-has_more}"
CURSOR_KEY="${CURSOR_KEY:-sync:http:last_block}"
PAGE_SIZE="${PAGE_SIZE:-100}"
MAX_PAGES="${MAX_PAGES:-50}"
TIMEOUT_SEC="${TIMEOUT_SEC:-20}"
MIN_CONFIRMATIONS="${MIN_CONFIRMATIONS:-6}"
TIP_HEIGHT="${TIP_HEIGHT:-}"
CURSOR_ADVANCE_POLICY="${CURSOR_ADVANCE_POLICY:-complete-window}"
REORG_CHECK="${REORG_CHECK:-1}"
REORG_ROLLBACK_BLOCKS="${REORG_ROLLBACK_BLOCKS:-12}"
REORG_HASH_URL_TEMPLATE="${REORG_HASH_URL_TEMPLATE:-https://stampchain.io/api/v2/block/{block}}"
REORG_HASH_PATH="${REORG_HASH_PATH:-block_hash}"
ENFORCE_BALANCE_CHECKS="${ENFORCE_BALANCE_CHECKS:-1}"
ENFORCE_TICK_REGISTRY="${ENFORCE_TICK_REGISTRY:-0}"
TICK_REGISTRY_FILE="${TICK_REGISTRY_FILE:-}"

if [[ "${MIN_CONFIRMATIONS}" != "0" && -z "${TIP_HEIGHT}" ]]; then
  echo "TIP_HEIGHT is required when MIN_CONFIRMATIONS is non-zero." >&2
  exit 1
fi

ARGS=(
  python3
  "$ROOT_DIR/tools/src420-indexer/src420_indexer.py"
  sync-http
  --db "$DB_PATH"
  --base-url "$BASE_URL"
  --endpoint "$ENDPOINT"
  --records-key "$RECORDS_KEY"
  --has-more-key "$HAS_MORE_KEY"
  --cursor-key "$CURSOR_KEY"
  --page-size "$PAGE_SIZE"
  --max-pages "$MAX_PAGES"
  --timeout "$TIMEOUT_SEC"
  --update-cursor
  --cursor-advance-policy "$CURSOR_ADVANCE_POLICY"
)

if [[ -n "${TIP_HEIGHT}" ]]; then
  ARGS+=(--tip-height "$TIP_HEIGHT")
fi

if [[ "${MIN_CONFIRMATIONS}" != "0" ]]; then
  ARGS+=(--min-confirmations "$MIN_CONFIRMATIONS")
fi

if [[ -n "${START_BLOCK:-}" ]]; then
  ARGS+=(--start-block "$START_BLOCK")
fi

if [[ -n "${END_BLOCK:-}" ]]; then
  ARGS+=(--end-block "$END_BLOCK")
fi

if [[ "${ENFORCE_BALANCE_CHECKS}" == "1" ]]; then
  ARGS+=(--enforce-balance-checks)
fi

if [[ "${ENFORCE_TICK_REGISTRY}" == "1" ]]; then
  ARGS+=(--enforce-tick-registry)
fi

if [[ "${REORG_CHECK}" == "1" ]]; then
  ARGS+=(
    --reorg-check
    --reorg-auto-rollback
    --reorg-rollback-blocks "$REORG_ROLLBACK_BLOCKS"
    --reorg-hash-url-template "$REORG_HASH_URL_TEMPLATE"
    --reorg-hash-path "$REORG_HASH_PATH"
  )
fi

if [[ -n "${API_KEY:-}" ]]; then
  ARGS+=(--api-key "$API_KEY" --api-key-header "${API_KEY_HEADER:-x-api-key}")
fi

if [[ -n "${TICK_REGISTRY_FILE}" ]]; then
  python3 \
    "$ROOT_DIR/tools/src420-indexer/src420_indexer.py" \
    import-tick-registry \
    --db "$DB_PATH" \
    --file "$TICK_REGISTRY_FILE"
fi

exec "${ARGS[@]}"
