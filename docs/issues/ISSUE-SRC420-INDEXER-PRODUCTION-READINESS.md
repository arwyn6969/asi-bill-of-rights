## SRC-420 Indexer Production Readiness

### Priority: High
### Type: Infrastructure / Protocol Hardening
### Date: March 5, 2026

---

### Summary

The local SRC-420 indexer MVP is now hardened enough for continued research, but it is still not the full SRC-420 protocol surface. This issue tracks the gap between the current safe MVP and a production-ready, community-runnable indexer.

### What Was Fixed In This Hardening Pass

- Invalid events now fail closed when `block_height` is missing or malformed.
- The indexer now supports `approval` and `weighted` ballots and still rejects unsupported `quadratic` semantics instead of silently mis-scoring them.
- `sync-http` now stages records across fetched pages and sorts globally before reduction, preventing page-order corruption.
- Previously invalid dependency-ordered events can now be retried and recovered.
- Proposal status can now use the last known chain tip rather than only the latest indexed governance event.
- Same-block replay can now preserve upstream ordering metadata when the feed provides transaction/stamp position fields.
- DEPLOY can now be enforced against a local SRC-20 tick registry.
- Regression coverage was expanded around malformed input, unsupported modes, dependency replay, same-block ordering, tick enforcement, weighted/approval tallies, out-of-order pages, and status reference behavior.

### Current Safe Scope

- Voting types: `single-choice`, `approval`, `weighted`
- Strategy: `src20-balance`
- Operations: `DEPLOY`, `PROPOSE`, `VOTE`, `DELEGATE`, `ATTEST`
- Optional local SRC-20 tick registry enforcement
- Reorg handling: rollback + cursor/hash checks
- Query API: research/operator use

### Deferred Full-Spec Work

- Define and implement a canonical `quadratic` ballot schema and tally rule.
- Implement multi-strategy voting power calculation beyond `src20-balance`.
- Replace operator-imported tick registry checks with a canonical trustable upstream or verifiable on-chain SRC-20 registry path.
- Upgrade Bitcoin address validation from prefix/shape checks to canonical decoding/verification.
- Decide whether partial same-block metadata should be accepted, warned on, or rejected in strict mode.
- Decide whether ASI addendum operations are launch requirements or post-MVP extensions.
- Add production sync guarantees around very large windows, partial fetches, and cursor advancement strategy.

### Difficulty Split

- `4/10` Canonical tick registry / token existence checks
- `5/10` Full address decoding validation
- `6/10` Explicit chain-tip ingestion/discovery path
- `7/10` Canonical quadratic vote schema + reducer support
- `7/10` Multi-strategy power engine
- `7/10` Addendum launch-scope decision and protocol boundary cleanup

### Recommended Next Steps

- [ ] Decide whether launch scope is strict MVP or broader SRC-420 compatibility.
- [ ] Decide whether strict mode should require same-block ordering metadata on colliding blocks.
- [ ] Add a production sync profile against the intended upstream endpoint.
- [ ] Add larger replay/sync fixtures that simulate real feed disorder and restart behavior.
- [ ] Define execution-layer expectations for passed proposals.

### Labels

`src-420`, `indexer`, `infrastructure`, `hardening`, `governance`
