# SRC-420 Indexer MVP

Deterministic local indexer for SRC-420 governance events.

Location: `/Users/arwynhughes/Documents/ASI BILL OF RIGHTS/tools/src420-indexer/src420_indexer.py`

## What this MVP does

- Ingests SRC-420 events from JSON or JSONL.
- Applies protocol reduction rules into SQLite state:
  - `spaces`
  - `proposals`
  - `votes` (last valid vote wins)
  - `delegations`
  - `attestations`
- Computes proposal tallies and winners.
- Serves a query API for spaces/proposals/votes/results/voting power.

## Current MVP scope

- Supported voting types: `single-choice`, `approval`, `weighted`
- Supported strategy: `src20-balance`
- Optional local SRC-20 tick registry enforcement via `import-tick-registry` + `--enforce-tick-registry`
- Same-block ordering prefers upstream ordering metadata (`tx_index`, `transaction_index`, `tx_position`, `stamp_index`, `stamp_number`) when present, then falls back to `txid`.
- Sync batches records across fetched pages, then sorts globally before reduction.
- Proposal status uses the last known chain tip when `sync-http --tip-height` has been provided; otherwise it falls back to the latest indexed governance block.

## Difficulty-Split Build (<= 7/10 tasks)

- `3/10` Schema and DB bootstrapping
- `5/10` Deterministic event normalization/order
- `6/10` Protocol reducers (`DEPLOY`, `PROPOSE`, `VOTE`, `DELEGATE`, `ATTEST`)
- `6/10` Voting power resolution at snapshot block with delegation chaining
- `4/10` Read API endpoints for operators/UI
- `6/10` HTTP sync + cursor state management
- `2/10` Fixtures and runbook for local validation

Everything above `7/10` was split before implementation.

## Quick start

From repo root:

```bash
python3 tools/src420-indexer/src420_indexer.py init-db --db tools/src420-indexer/src420.db
python3 tools/src420-indexer/src420_indexer.py import-tick-registry --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_tick_registry.jsonl
python3 tools/src420-indexer/src420_indexer.py import-balances --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_balances.jsonl
python3 tools/src420-indexer/src420_indexer.py ingest-file --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_events.jsonl --enforce-balance-checks --enforce-tick-registry
python3 tools/src420-indexer/src420_indexer.py sync-http --db tools/src420-indexer/src420.db --records-key results --has-more-key has_more --max-pages 3 --tip-height 900000 --min-confirmations 6 --reorg-check --reorg-auto-rollback --reorg-hash-url-template 'https://stampchain.io/api/v2/block/{block}' --reorg-hash-path block_hash --update-cursor --enforce-tick-registry
python3 tools/src420-indexer/src420_indexer.py rollback-to-block --db tools/src420-indexer/src420.db --to-block 899500
python3 tools/src420-indexer/src420_indexer.py show-sync-state --db tools/src420-indexer/src420.db
python3 tools/src420-indexer/src420_indexer.py serve --db tools/src420-indexer/src420.db --port 8787
```

Then query:

```bash
curl http://127.0.0.1:8787/health
curl http://127.0.0.1:8787/spaces
curl http://127.0.0.1:8787/spaces/asi-bill-of-rights/proposals
curl http://127.0.0.1:8787/spaces/asi-bill-of-rights/proposals/1/results
curl "http://127.0.0.1:8787/spaces/asi-bill-of-rights/voting-power/bc1p_bob?block=100"
```

## Validation (proof checklist)

Run the regression suite:

```bash
python3 tools/src420-indexer/validate_mvp.py
python3 tools/ci/validate_all.py
```

This covers:
- deterministic ingestion/idempotency
- missing block height rejection
- unsupported strategy/quadratic rejection
- tick registry enforcement
- first DEPLOY wins
- sequential proposal IDs
- vote window enforcement
- approval and weighted tally behavior
- snapshot-timed delegation behavior
- chain delegation one-hop semantics
- admin attestation precedence
- retrying previously invalid events after dependencies arrive
- same-block order metadata surviving replay/rollback
- cursor resolution and HTTP pagination sync logic
- cross-page out-of-order sync correction
- status reference block behavior
- finality range filtering and rollback replay
- reorg detection + auto rollback behavior

CI also runs this suite in `.github/workflows/src420-indexer-validation.yml` when files under `tools/src420-indexer/` change.

## Event input format

Supports either:

- JSON array of objects
- JSONL (one object per line)

Each record should provide at least:

- `txid`
- `block_height`
- optional same-block ordering metadata such as `tx_index`, `transaction_index`, `tx_position`, `stamp_index`, or `stamp_number`
- `sender` (or `address`)
- a payload object or JSON string containing:
  - `"p": "SRC-420"`
  - `"op": "<OPERATION>"`

Example JSONL record:

```json
{"txid":"abc123","block_height":100,"sender":"bc1p_x","payload":{"p":"SRC-420","op":"DEPLOY","space":"demo","tick":"KVNSI","name":"Demo","strategies":["src20-balance"],"voting":{"delay":1,"period":144,"quorum":10,"type":"single-choice"},"admins":[]}}
```

## Balance snapshot format

JSON/JSONL records with:

- `tick` (e.g. `KVNSI`)
- `address`
- `block_height`
- `balance`
- optional `source`

## Tick registry format

Optional JSON/JSONL records with:

- `tick`
- optional `protocol` (default: `SRC-20`)
- optional `block_height` / `deployed_block`
- optional `txid` / `deployment_txid`
- optional `metadata`
- optional `source`

If you want strict `DEPLOY` validation against canonical SRC-20 ticks, import registry rows first and run with `--enforce-tick-registry`.

## Vote payload formats

- `single-choice`

```json
{"p":"SRC-420","op":"VOTE","space":"demo","proposal":1,"choice":1}
```

- `approval`

```json
{"p":"SRC-420","op":"VOTE","space":"demo","proposal":1,"choices":[1,3]}
```

- `weighted`

```json
{"p":"SRC-420","op":"VOTE","space":"demo","proposal":1,"weights":{"1":60,"2":40}}
```

## API surface

- `GET /health`
- `GET /spaces`
- `GET /spaces/{id}`
- `GET /spaces/{id}/proposals?status=pending|active|closed`
- `GET /spaces/{id}/proposals/{pid}`
- `GET /spaces/{id}/proposals/{pid}/votes`
- `GET /spaces/{id}/proposals/{pid}/results`
- `GET /spaces/{id}/voting-power/{address}?block={height}`
- `GET /spaces/{id}/delegations/{address}?block={height}`

## HTTP sync commands

- `sync-http`: pulls paginated records from an HTTP endpoint and ingests them.
  - Supports either:
    - `--url-template` with placeholders `{page}`, `{limit}`, `{start_block}`, `{end_block}`
    - or auto template via `--base-url` + `--endpoint` + query param names
  - Supports finality gating via `--tip-height` and `--min-confirmations`
  - Supports optional tick enforcement via `--enforce-tick-registry`
  - Supports cursor policies via `--cursor-advance-policy no-rejections|complete-window|always`
  - Supports reorg checks via:
    - `--reorg-check`
    - `--reorg-hash-url-template '...{block}...'`
    - `--reorg-hash-path` (default: `block_hash`)
    - optional auto rollback via `--reorg-auto-rollback --reorg-rollback-blocks 12`
- `import-tick-registry`: imports canonical SRC-20 tick metadata used by `--enforce-tick-registry`.
- `show-sync-state`: prints cursor values stored in SQLite `sync_state`.

## Production sync profile

For live operator runs, use the wrapper script:

```bash
TIP_HEIGHT=900000 \
TICK_REGISTRY_FILE=tools/src420-indexer/fixtures/sample_tick_registry.jsonl \
ENFORCE_TICK_REGISTRY=1 \
MIN_CONFIRMATIONS=6 \
bash tools/src420-indexer/run_stampchain_sync.sh
```

Recommended defaults in that wrapper:

- `--update-cursor`
- `--cursor-advance-policy complete-window`
- `--reorg-check --reorg-auto-rollback`
- `--enforce-balance-checks`
- optional pre-sync `import-tick-registry` when `TICK_REGISTRY_FILE` is set
- optional `--enforce-tick-registry` when `ENFORCE_TICK_REGISTRY=1`

Why this profile exists:

- It refuses to advance the cursor when a run contains rejected records.
- It can also refuse cursor advancement when the run stopped because `--max-pages` was exhausted.
- It persists the supplied chain tip so proposal status can be evaluated against the last known tip instead of only the latest indexed governance event.
- It can enforce canonical tick presence when you maintain a local SRC-20 registry file.

## Rollback command

- `rollback-to-block`: rewinds derived governance state by replaying the event log up to a target block.
  - By default it **deletes future event-log rows** above target block, then replays.
  - Optional: `--keep-future-events` (not recommended, because event tip remains ahead of rebuilt state).
  - Optional: `--prune-balance-snapshots` to also trim balance history above the target.
  - Optional: `--cursor-key` to reset sync cursor (default `sync:http:last_block`).

## Current limits

- Sync is polling-based (not websocket streaming).
- Finality tip is currently caller-provided (`--tip-height`), not auto-discovered.
- `quadratic` voting type is still intentionally rejected because the spec does not yet define a stable ballot schema or tally rule.
- Multi-strategy voting power beyond `src20-balance` is still intentionally rejected.
- Bitcoin address validation is still lightweight (prefix/shape checks, not full script-level validation).
- Canonical tick verification depends on the operator importing a local SRC-20 registry; without that, only ticker format is enforced.
