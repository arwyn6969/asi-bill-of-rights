#!/usr/bin/env python3
"""
Validation suite for SRC-420 indexer MVP.

Runs protocol-focused regression checks so we can prove behavior instead of
assuming correctness.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List


def load_indexer_module():
    here = Path(__file__).resolve().parent
    module_path = here / "src420_indexer.py"
    spec = importlib.util.spec_from_file_location("src420_indexer", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["src420_indexer"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


IDX = load_indexer_module()


def deploy_event(sender: str, space: str = "s1") -> Dict:
    return {
        "txid": "d1",
        "block_height": 1,
        "sender": sender,
        "payload": {
            "p": "SRC-420",
            "op": "DEPLOY",
            "space": space,
            "tick": "KVNSI",
            "name": "Test Space",
            "strategies": ["src20-balance"],
            "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
            "admins": [],
        },
    }


class Src420IndexerValidation(unittest.TestCase):
    def setUp(self) -> None:
        fd, self.db_path = tempfile.mkstemp(prefix="src420-validate-", suffix=".db")
        os.close(fd)
        self.conn = IDX.open_db(self.db_path)
        IDX.init_db(self.conn)

    def tearDown(self) -> None:
        self.conn.close()
        os.remove(self.db_path)

    def ingest(self, events: List[Dict], enforce: bool = True) -> Dict[str, int]:
        return IDX.ingest_records(
            self.conn,
            events,
            settings=IDX.ReducerSettings(
                enforce_balance_checks=enforce,
                default_voting_power=1.0,
            ),
        )

    def import_balances(self, rows: List[Dict]) -> None:
        IDX.import_balance_records(self.conn, rows)

    def test_basic_flow_results(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_alice", "block_height": 100, "balance": 40},
                {"tick": "KVNSI", "address": "bc1p_bob", "block_height": 100, "balance": 60},
                {"tick": "KVNSI", "address": "bc1p_charlie", "block_height": 100, "balance": 30},
            ]
        )
        events = [
            {
                "txid": "d1",
                "block_height": 90,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "asi-bill-of-rights",
                    "tick": "KVNSI",
                    "name": "DAO",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 2, "period": 144, "quorum": 80, "type": "single-choice"},
                    "admins": [],
                },
            },
            {
                "txid": "g1",
                "block_height": 99,
                "sender": "bc1p_alice",
                "payload": {
                    "p": "SRC-420",
                    "op": "DELEGATE",
                    "space": "asi-bill-of-rights",
                    "to": "bc1p_bob",
                },
            },
            {
                "txid": "p1",
                "block_height": 100,
                "sender": "bc1p_alice",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "asi-bill-of-rights",
                    "id": 1,
                    "title": "T1",
                    "body": "B",
                    "choices": ["Yes", "No"],
                    "snapshot": 100,
                    "start": 102,
                    "end": 246,
                },
            },
            {
                "txid": "v1",
                "block_height": 120,
                "sender": "bc1p_bob",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "asi-bill-of-rights", "proposal": 1, "choice": 1},
            },
            {
                "txid": "v2",
                "block_height": 121,
                "sender": "bc1p_charlie",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "asi-bill-of-rights", "proposal": 1, "choice": 2},
            },
            {
                "txid": "v3",
                "block_height": 122,
                "sender": "bc1p_bob",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "asi-bill-of-rights", "proposal": 1, "choice": 2},
            },
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["applied"], 6)
        self.assertEqual(summary["rejected"], 0)

        results = IDX.calculate_results(self.conn, "asi-bill-of-rights", 1)
        self.assertEqual(results["winner"], 2)
        self.assertAlmostEqual(results["total"], 130.0)

    def test_idempotent_ingestion(self) -> None:
        summary1 = self.ingest([deploy_event("bc1p_addr_a")], enforce=False)
        summary2 = self.ingest([deploy_event("bc1p_addr_a")], enforce=False)
        self.assertEqual(summary1["applied"], 1)
        self.assertEqual(summary2["duplicates"], 1)

    def test_first_deploy_wins(self) -> None:
        events = [
            deploy_event("bc1p_addr_a"),
            {
                **deploy_event("bc1p_addr_b"),
                "txid": "d2",
                "block_height": 2,
                "payload": {**deploy_event("bc1p_addr_b")["payload"], "name": "Other Name"},
            },
        ]
        summary = self.ingest(events, enforce=False)
        self.assertEqual(summary["applied"], 1)
        self.assertEqual(summary["rejected"], 1)

    def test_vote_window_enforced(self) -> None:
        self.import_balances([{"tick": "KVNSI", "address": "bc1p_addr_a", "block_height": 10, "balance": 10}])
        events = [
            {
                **deploy_event("bc1p_addr_a"),
                "payload": {**deploy_event("bc1p_addr_a")["payload"], "voting": {"delay": 2, "period": 144, "quorum": 1, "type": "single-choice"}},
            },
            {
                "txid": "p1",
                "block_height": 10,
                "sender": "bc1p_addr_a",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 10,
                    "start": 12,
                    "end": 156,
                },
            },
            {
                "txid": "vbad",
                "block_height": 11,
                "sender": "bc1p_addr_a",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["applied"], 2)
        self.assertEqual(summary["rejected"], 1)

    def test_sequential_proposal_ids(self) -> None:
        self.import_balances([{"tick": "KVNSI", "address": "bc1p_addr_a", "block_height": 10, "balance": 10}])
        events = [
            deploy_event("bc1p_addr_a"),
            {
                "txid": "p2",
                "block_height": 10,
                "sender": "bc1p_addr_a",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 2,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 10,
                    "start": 10,
                    "end": 154,
                },
            },
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["applied"], 1)
        self.assertEqual(summary["rejected"], 1)

    def test_snapshot_timing_for_delegation(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_addr_a", "block_height": 100, "balance": 40},
                {"tick": "KVNSI", "address": "bc1p_addr_b", "block_height": 100, "balance": 60},
            ]
        )
        events = [
            deploy_event("bc1p_addr_a"),
            {
                "txid": "p1",
                "block_height": 100,
                "sender": "bc1p_addr_a",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 100,
                    "start": 100,
                    "end": 244,
                },
            },
            {
                "txid": "g_late",
                "block_height": 101,
                "sender": "bc1p_addr_a",
                "payload": {"p": "SRC-420", "op": "DELEGATE", "space": "s1", "to": "bc1p_addr_b"},
            },
            {
                "txid": "vb",
                "block_height": 120,
                "sender": "bc1p_addr_b",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["rejected"], 0)

        row = self.conn.execute(
            "SELECT voting_power FROM votes WHERE space_id = 's1' AND proposal_id = 1 AND voter = 'bc1p_addr_b'"
        ).fetchone()
        self.assertAlmostEqual(float(row["voting_power"]), 60.0)

    def test_chain_delegation_is_one_hop(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_addr_a", "block_height": 100, "balance": 40},
                {"tick": "KVNSI", "address": "bc1p_addr_b", "block_height": 100, "balance": 60},
                {"tick": "KVNSI", "address": "bc1p_addr_c", "block_height": 100, "balance": 30},
            ]
        )
        events = [
            deploy_event("bc1p_addr_a"),
            {"txid": "g1", "block_height": 99, "sender": "bc1p_addr_a", "payload": {"p": "SRC-420", "op": "DELEGATE", "space": "s1", "to": "bc1p_addr_b"}},
            {"txid": "g2", "block_height": 99, "sender": "bc1p_addr_b", "payload": {"p": "SRC-420", "op": "DELEGATE", "space": "s1", "to": "bc1p_addr_c"}},
            {
                "txid": "p1",
                "block_height": 100,
                "sender": "bc1p_addr_a",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 100,
                    "start": 100,
                    "end": 244,
                },
            },
            {"txid": "vc", "block_height": 120, "sender": "bc1p_addr_c", "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1}},
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["rejected"], 0)

        row = self.conn.execute(
            "SELECT voting_power FROM votes WHERE space_id = 's1' AND proposal_id = 1 AND voter = 'bc1p_addr_c'"
        ).fetchone()
        # One-hop semantics: C should get B + C, but not A.
        self.assertAlmostEqual(float(row["voting_power"]), 90.0)

    def test_admin_attestation_precedence(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_admin", "block_height": 10, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_user1", "block_height": 10, "balance": 10},
            ]
        )

        events = [
            {
                "txid": "d1",
                "block_height": 1,
                "sender": "bc1p_admin",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "s1",
                    "tick": "KVNSI",
                    "name": "N",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                    "admins": ["bc1p_admin"],
                },
            },
            {
                "txid": "p1",
                "block_height": 10,
                "sender": "bc1p_admin",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 10,
                    "start": 10,
                    "end": 154,
                },
            },
            {"txid": "v1", "block_height": 20, "sender": "bc1p_user1", "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1}},
            {"txid": "a-non", "block_height": 200, "sender": "bc1p_user1", "payload": {"p": "SRC-420", "op": "ATTEST", "space": "s1", "proposal": 1, "result": {"scores": [10, 0], "total": 10, "quorum": True, "winner": 1}}},
            {"txid": "a-admin", "block_height": 201, "sender": "bc1p_admin", "payload": {"p": "SRC-420", "op": "ATTEST", "space": "s1", "proposal": 1, "result": {"scores": [10, 0], "total": 10, "quorum": True, "winner": 1}}},
        ]
        summary = self.ingest(events, enforce=True)
        self.assertEqual(summary["rejected"], 0)

        row = self.conn.execute(
            "SELECT attestor, txid FROM attestations WHERE space_id = 's1' AND proposal_id = 1"
        ).fetchone()
        self.assertEqual(row["attestor"], "bc1p_admin")
        self.assertEqual(row["txid"], "a-admin")

    def test_cursor_resolution(self) -> None:
        start = IDX.resolve_start_block(self.conn, "sync:http:last_block", None)
        self.assertEqual(start, 0)

        IDX.set_sync_state(self.conn, "sync:http:last_block", "101")
        start = IDX.resolve_start_block(self.conn, "sync:http:last_block", None)
        self.assertEqual(start, 102)

        start = IDX.resolve_start_block(self.conn, "sync:http:last_block", 33)
        self.assertEqual(start, 33)

    def test_sync_http_feed_pagination(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 50, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 50, "balance": 20},
            ]
        )

        payloads = {
            1: {
                "results": [
                    {
                        "txid": "d1",
                        "block_height": 10,
                        "sender": "bc1p_founder",
                        "payload": {
                            "p": "SRC-420",
                            "op": "DEPLOY",
                            "space": "s1",
                            "tick": "KVNSI",
                            "name": "N",
                            "strategies": ["src20-balance"],
                            "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                            "admins": [],
                        },
                    },
                    {
                        "txid": "p1",
                        "block_height": 50,
                        "sender": "bc1p_founder",
                        "payload": {
                            "p": "SRC-420",
                            "op": "PROPOSE",
                            "space": "s1",
                            "id": 1,
                            "title": "T",
                            "body": "B",
                            "choices": ["Y", "N"],
                            "snapshot": 50,
                            "start": 50,
                            "end": 194,
                        },
                    },
                ],
                "has_more": True,
            },
            2: {
                "results": [
                    {
                        "txid": "v1",
                        "block_height": 60,
                        "sender": "bc1p_voter",
                        "payload": {
                            "p": "SRC-420",
                            "op": "VOTE",
                            "space": "s1",
                            "proposal": 1,
                            "choice": 1,
                        },
                    }
                ],
                "has_more": False,
            },
        }

        seen_urls = []

        def fake_fetcher(url: str, timeout_sec: float, headers=None):
            seen_urls.append(url)
            if "page=1" in url:
                return payloads[1]
            if "page=2" in url:
                return payloads[2]
            return {"results": [], "has_more": False}

        summary = IDX.sync_http_feed(
            conn=self.conn,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            url_template="https://example.test/stamps?page={page}&limit={limit}&from={start_block}",
            start_block=0,
            end_block=None,
            page_size=2,
            max_pages=5,
            timeout_sec=1.0,
            records_key="results",
            has_more_key="has_more",
            headers={"x-test": "1"},
            fetcher=fake_fetcher,
        )

        self.assertEqual(summary["pages_fetched"], 2)
        self.assertEqual(summary["records_fetched"], 3)
        self.assertEqual(summary["applied"], 3)
        self.assertEqual(summary["rejected"], 0)
        self.assertEqual(summary["filtered_out_of_range"], 0)
        self.assertEqual(summary["max_seen_block"], 60)
        self.assertTrue(any("page=1" in url for url in seen_urls))
        self.assertTrue(any("page=2" in url for url in seen_urls))

    def test_sync_http_feed_filters_out_of_range_blocks(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 50, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 50, "balance": 20},
            ]
        )

        payload = {
            "results": [
                {
                    "txid": "d1",
                    "block_height": 10,
                    "sender": "bc1p_founder",
                    "payload": {
                        "p": "SRC-420",
                        "op": "DEPLOY",
                        "space": "s1",
                        "tick": "KVNSI",
                        "name": "N",
                        "strategies": ["src20-balance"],
                        "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                        "admins": [],
                    },
                },
                {
                    "txid": "p1",
                    "block_height": 50,
                    "sender": "bc1p_founder",
                    "payload": {
                        "p": "SRC-420",
                        "op": "PROPOSE",
                        "space": "s1",
                        "id": 1,
                        "title": "T",
                        "body": "B",
                        "choices": ["Y", "N"],
                        "snapshot": 50,
                        "start": 50,
                        "end": 194,
                    },
                },
                {
                    "txid": "v1",
                    "block_height": 60,
                    "sender": "bc1p_voter",
                    "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
                },
            ],
            "has_more": False,
        }

        def fake_fetcher(url: str, timeout_sec: float, headers=None):
            return payload

        summary = IDX.sync_http_feed(
            conn=self.conn,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            url_template="https://example.test/stamps?page={page}&limit={limit}&from={start_block}&to={end_block}",
            start_block=0,
            end_block=55,
            page_size=100,
            max_pages=1,
            timeout_sec=1.0,
            records_key="results",
            has_more_key="has_more",
            headers=None,
            fetcher=fake_fetcher,
        )

        # Vote at block 60 is filtered out by end_block=55.
        self.assertEqual(summary["filtered_out_of_range"], 1)
        self.assertEqual(summary["applied"], 2)
        self.assertEqual(summary["max_seen_block"], 50)

    def test_finality_end_block_resolution(self) -> None:
        self.assertEqual(
            IDX.resolve_effective_end_block(
                start_block=100,
                requested_end_block=None,
                tip_height=220,
                min_confirmations=6,
            ),
            214,
        )

    def test_rollback_to_block_prunes_and_replays(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 20, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 20, "balance": 50},
            ]
        )
        events = [
            {
                "txid": "d1",
                "block_height": 10,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "s1",
                    "tick": "KVNSI",
                    "name": "N",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                    "admins": [],
                },
            },
            {
                "txid": "p1",
                "block_height": 20,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 20,
                    "start": 20,
                    "end": 164,
                },
            },
            {
                "txid": "v1",
                "block_height": 30,
                "sender": "bc1p_voter",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
            {
                "txid": "a1",
                "block_height": 200,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "ATTEST",
                    "space": "s1",
                    "proposal": 1,
                    "result": {"scores": [50, 0], "total": 50, "quorum": True, "winner": 1},
                },
            },
        ]
        summary_before = self.ingest(events, enforce=True)
        self.assertEqual(summary_before["applied"], 4)
        IDX.set_sync_state(self.conn, "sync:http:last_block", "200")

        rollback_summary = IDX.rollback_to_block(
            conn=self.conn,
            to_block=25,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            prune_future_events=True,
            prune_balance_snapshots=False,
            cursor_key="sync:http:last_block",
        )

        self.assertEqual(rollback_summary["deleted_events"], 2)
        self.assertEqual(rollback_summary["replayed_events"], 2)
        self.assertEqual(rollback_summary["after"]["spaces"], 1)
        self.assertEqual(rollback_summary["after"]["proposals"], 1)
        self.assertEqual(rollback_summary["after"]["votes"], 0)
        self.assertEqual(rollback_summary["after"]["attestations"], 0)
        self.assertEqual(rollback_summary["after"]["latest_block"], 20)
        self.assertEqual(rollback_summary["cursor_after"], "25")

    def test_rollback_keep_future_events_leaves_event_tip(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 20, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 20, "balance": 50},
            ]
        )
        events = [
            {
                "txid": "d1",
                "block_height": 10,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "s1",
                    "tick": "KVNSI",
                    "name": "N",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                    "admins": [],
                },
            },
            {
                "txid": "p1",
                "block_height": 20,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 20,
                    "start": 20,
                    "end": 164,
                },
            },
            {
                "txid": "v1",
                "block_height": 30,
                "sender": "bc1p_voter",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
        ]
        summary_before = self.ingest(events, enforce=True)
        self.assertEqual(summary_before["applied"], 3)

        rollback_summary = IDX.rollback_to_block(
            conn=self.conn,
            to_block=25,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            prune_future_events=False,
            prune_balance_snapshots=False,
            cursor_key=None,
        )

        # State is replayed to target block, but event log tip remains at 30 if future events are retained.
        self.assertEqual(rollback_summary["deleted_events"], 0)
        self.assertEqual(rollback_summary["after"]["votes"], 0)
        self.assertEqual(rollback_summary["after"]["latest_block"], 30)

    def test_reorg_check_detects_mismatch_without_rollback(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 20, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 20, "balance": 50},
            ]
        )
        events = [
            {
                "txid": "d1",
                "block_height": 10,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "s1",
                    "tick": "KVNSI",
                    "name": "N",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                    "admins": [],
                },
            },
            {
                "txid": "p1",
                "block_height": 20,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 20,
                    "start": 20,
                    "end": 164,
                },
            },
            {
                "txid": "v1",
                "block_height": 30,
                "sender": "bc1p_voter",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
        ]
        summary_before = self.ingest(events, enforce=True)
        self.assertEqual(summary_before["applied"], 3)

        IDX.set_sync_state(self.conn, "sync:http:last_block", "30")
        IDX.set_sync_state(self.conn, "sync:http:last_block_hash", "old-hash")

        def fake_fetcher(url: str, timeout_sec: float, headers=None):
            return {"block_hash": "new-hash"}

        result = IDX.run_reorg_check(
            conn=self.conn,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            cursor_key="sync:http:last_block",
            hash_state_key="sync:http:last_block_hash",
            hash_url_template="https://example.test/block/{block}",
            hash_path="block_hash",
            timeout_sec=1.0,
            headers=None,
            auto_rollback=False,
            rollback_blocks=12,
            fetcher=fake_fetcher,
        )

        self.assertTrue(result["reorg_detected"])
        self.assertEqual(result["status"], "mismatch_no_rollback")
        row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM votes WHERE space_id = 's1' AND proposal_id = 1"
        ).fetchone()
        self.assertEqual(int(row["c"]), 1)

    def test_reorg_check_auto_rollback(self) -> None:
        self.import_balances(
            [
                {"tick": "KVNSI", "address": "bc1p_founder", "block_height": 20, "balance": 10},
                {"tick": "KVNSI", "address": "bc1p_voter", "block_height": 20, "balance": 50},
            ]
        )
        events = [
            {
                "txid": "d1",
                "block_height": 10,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "DEPLOY",
                    "space": "s1",
                    "tick": "KVNSI",
                    "name": "N",
                    "strategies": ["src20-balance"],
                    "voting": {"delay": 0, "period": 144, "quorum": 1, "type": "single-choice"},
                    "admins": [],
                },
            },
            {
                "txid": "p1",
                "block_height": 20,
                "sender": "bc1p_founder",
                "payload": {
                    "p": "SRC-420",
                    "op": "PROPOSE",
                    "space": "s1",
                    "id": 1,
                    "title": "T",
                    "body": "B",
                    "choices": ["Y", "N"],
                    "snapshot": 20,
                    "start": 20,
                    "end": 164,
                },
            },
            {
                "txid": "v1",
                "block_height": 30,
                "sender": "bc1p_voter",
                "payload": {"p": "SRC-420", "op": "VOTE", "space": "s1", "proposal": 1, "choice": 1},
            },
        ]
        summary_before = self.ingest(events, enforce=True)
        self.assertEqual(summary_before["applied"], 3)

        IDX.set_sync_state(self.conn, "sync:http:last_block", "30")
        IDX.set_sync_state(self.conn, "sync:http:last_block_hash", "old-hash")

        def fake_fetcher(url: str, timeout_sec: float, headers=None):
            if url.endswith("/30"):
                return {"block_hash": "new-hash-at-30"}
            if url.endswith("/18"):
                return {"block_hash": "canonical-hash-18"}
            if url.endswith("/20"):
                return {"block_hash": "canonical-hash-20"}
            return {"block_hash": "fallback"}

        result = IDX.run_reorg_check(
            conn=self.conn,
            settings=IDX.ReducerSettings(enforce_balance_checks=True, default_voting_power=1.0),
            cursor_key="sync:http:last_block",
            hash_state_key="sync:http:last_block_hash",
            hash_url_template="https://example.test/block/{block}",
            hash_path="block_hash",
            timeout_sec=1.0,
            headers=None,
            auto_rollback=True,
            rollback_blocks=12,
            fetcher=fake_fetcher,
        )

        self.assertTrue(result["reorg_detected"])
        self.assertEqual(result["status"], "mismatch_rolled_back")
        self.assertEqual(IDX.get_sync_state(self.conn, "sync:http:last_block"), "18")
        self.assertEqual(IDX.get_sync_state(self.conn, "sync:http:last_block_hash"), "canonical-hash-18")

        row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM votes WHERE space_id = 's1' AND proposal_id = 1"
        ).fetchone()
        self.assertEqual(int(row["c"]), 0)
        self.assertEqual(
            IDX.resolve_effective_end_block(
                start_block=100,
                requested_end_block=180,
                tip_height=220,
                min_confirmations=6,
            ),
            180,
        )
        self.assertEqual(
            IDX.resolve_effective_end_block(
                start_block=100,
                requested_end_block=230,
                tip_height=220,
                min_confirmations=6,
            ),
            214,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
