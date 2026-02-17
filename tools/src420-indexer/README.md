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
python3 tools/src420-indexer/src420_indexer.py import-balances --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_balances.jsonl
python3 tools/src420-indexer/src420_indexer.py ingest-file --db tools/src420-indexer/src420.db --file tools/src420-indexer/fixtures/sample_events.jsonl --enforce-balance-checks
python3 tools/src420-indexer/src420_indexer.py sync-http --db tools/src420-indexer/src420.db --records-key results --has-more-key has_more --max-pages 3 --tip-height 900000 --min-confirmations 6 --reorg-check --reorg-auto-rollback --reorg-hash-url-template 'https://stampchain.io/api/v2/block/{block}' --reorg-hash-path block_hash --update-cursor
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
- first DEPLOY wins
- sequential proposal IDs
- vote window enforcement
- snapshot-timed delegation behavior
- chain delegation one-hop semantics
- admin attestation precedence
- cursor resolution and HTTP pagination sync logic
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
  - Supports reorg checks via:
    - `--reorg-check`
    - `--reorg-hash-url-template '...{block}...'`
    - `--reorg-hash-path` (default: `block_hash`)
    - optional auto rollback via `--reorg-auto-rollback --reorg-rollback-blocks 12`
- `show-sync-state`: prints cursor values stored in SQLite `sync_state`.

## Rollback command

- `rollback-to-block`: rewinds derived governance state by replaying the event log up to a target block.
  - By default it **deletes future event-log rows** above target block, then replays.
  - Optional: `--keep-future-events` (not recommended, because event tip remains ahead of rebuilt state).
  - Optional: `--prune-balance-snapshots` to also trim balance history above the target.
  - Optional: `--cursor-key` to reset sync cursor (default `sync:http:last_block`).

## Current limits

- Sync is polling-based (not websocket streaming).
- Finality tip is currently caller-provided (`--tip-height`), not auto-discovered.
- Voting strategies are reduced to snapshot balance + delegation logic for MVP.
- Bitcoin address validation is lightweight (format length check, not script-level validation).
