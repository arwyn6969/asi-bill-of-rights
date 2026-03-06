# Pull Request: SRC-420 Indexer Hardening and Protocol-Surface Expansion

## Summary

This change moves the local SRC-420 indexer closer to production-grade research infrastructure before first deployment.

It addresses three protocol risks that were still open after the first hardening pass:

1. `DEPLOY` can now be enforced against a local canonical SRC-20 tick registry.
2. Same-block replay now preserves explicit upstream ordering metadata when the feed exposes it.
3. The reducer and tally engine now support `approval` and `weighted` ballots instead of rejecting the entire non-single-choice surface.

The branch remains intentionally conservative. `quadratic` voting and multi-strategy power are still deferred because the current spec does not define them tightly enough to implement without guesswork.

## Main Changes

- Added `token_registry` storage plus `import-tick-registry`.
- Added `--enforce-tick-registry` to `ingest-file`, `sync-http`, and `rollback-to-block`.
- Persisted event `order_index` metadata in the event log for replay-safe same-block ordering.
- Applied same-block ordering metadata to delegation history lookups and replay ordering.
- Added canonical ballot storage on votes (`ballot_type`, `ballot_json`, `cast_order_index`).
- Implemented `approval` ballots with equal split across selected choices.
- Implemented `weighted` ballots with explicit 100% allocation checks.
- Updated the operator wrapper so it can preload a tick registry file before sync.
- Added fixture, docs, and issue tracking updates.

## Validation

Executed locally:

```bash
python3 -m py_compile tools/src420-indexer/src420_indexer.py tools/src420-indexer/validate_mvp.py
python3 tools/src420-indexer/validate_mvp.py
python3 tools/src420-indexer/src420_indexer.py sync-http --help
bash -n tools/src420-indexer/run_stampchain_sync.sh
python3 tools/ci/validate_all.py
```

Current regression result: `30/30` tests passing.

## Scope Boundary

Implemented now:

- `single-choice`
- `approval`
- `weighted`
- `src20-balance`
- replay-safe same-block ordering when upstream metadata exists
- operator-managed canonical tick registry enforcement

Still deferred:

- `quadratic` ballot semantics
- multi-strategy power
- strict Bitcoin address decoding
- trustless or upstream-canonical SRC-20 registry discovery
- ASI addendum operations

## Related Tracking

- Issue: `docs/issues/ISSUE-SRC420-INDEXER-PRODUCTION-READINESS.md`
