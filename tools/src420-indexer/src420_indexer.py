#!/usr/bin/env python3
"""
SRC-420 Indexer MVP.

This service provides:
- deterministic ingestion/reduction of SRC-420 events
- SQLite-backed state for spaces/proposals/votes/delegations
- simple HTTP query API

Design notes:
- Event ordering is deterministic: (block_height ASC, txid ASC)
- "First valid DEPLOY for a space wins"
- "Last valid vote by address wins" (per proposal)
- Delegation resolution is evaluated at proposal snapshot block
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib import error as urllib_error
from urllib import request as urllib_request
from urllib.parse import parse_qs, unquote, urljoin, urlparse


SPACE_ID_RE = re.compile(r"^[a-z0-9-]{1,32}$")
ALLOWED_VOTING_TYPES = {"single-choice", "weighted", "quadratic", "approval"}


@dataclass(frozen=True)
class ReducerSettings:
    enforce_balance_checks: bool = False
    default_voting_power: float = 1.0


@dataclass(frozen=True)
class NormalizedEvent:
    txid: str
    stamp_id: Optional[str]
    block_height: int
    block_time: Optional[str]
    sender: str
    op: str
    payload: Dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_dumps(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def json_loads(value: Optional[str], default: Any = None) -> Any:
    if value is None:
        return default
    return json.loads(value)


def parse_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"invalid integer for '{field_name}'")


def parse_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"invalid number for '{field_name}'")


def synthetic_txid(raw: Dict[str, Any], index: int) -> str:
    seed = json.dumps(raw, sort_keys=True, default=str)
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
    return f"synthetic-{digest}-{index}"


def load_json_records(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if text[0] == "[":
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            raise ValueError("JSON file must be an array or JSONL")
        return [row for row in parsed if isinstance(row, dict)]

    records: List[Dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parsed = json.loads(line)
        if not isinstance(parsed, dict):
            raise ValueError(f"JSONL line {line_number} is not an object")
        records.append(parsed)
    return records


def parse_src420_payload(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    candidates: List[Any] = [
        raw.get("payload"),
        raw.get("data"),
        raw.get("json"),
        raw.get("decoded"),
        raw,
    ]

    for candidate in candidates:
        parsed = candidate
        if isinstance(candidate, str):
            stripped = candidate.strip()
            if not stripped.startswith("{"):
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                continue

        if not isinstance(parsed, dict):
            continue

        protocol = str(parsed.get("p", "")).upper()
        op = str(parsed.get("op", "")).strip()
        if protocol == "SRC-420" and op:
            return parsed

    return None


def normalize_event(raw: Dict[str, Any], index: int) -> Tuple[Optional[NormalizedEvent], Optional[str]]:
    payload = parse_src420_payload(raw)
    if payload is None:
        return None, "no SRC-420 payload found"

    txid = str(
        raw.get("txid")
        or raw.get("transaction_id")
        or raw.get("id")
        or synthetic_txid(raw, index)
    ).strip()

    block_height_raw = (
        raw.get("block_height")
        or raw.get("block")
        or raw.get("height")
        or payload.get("block_height")
        or 0
    )
    try:
        block_height = int(block_height_raw)
    except (TypeError, ValueError):
        block_height = 0

    sender = str(
        raw.get("sender")
        or raw.get("address")
        or raw.get("from")
        or payload.get("from")
        or payload.get("sender")
        or ""
    ).strip()
    if not sender:
        return None, "missing sender address"

    op = str(payload.get("op", "")).upper().strip()
    if not op:
        return None, "missing operation"

    return (
        NormalizedEvent(
            txid=txid,
            stamp_id=(str(raw.get("stamp_id")).strip() if raw.get("stamp_id") is not None else None),
            block_height=block_height,
            block_time=(str(raw.get("block_time")).strip() if raw.get("block_time") is not None else None),
            sender=sender,
            op=op,
            payload=payload,
        ),
        None,
    )


def open_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS events (
            txid TEXT PRIMARY KEY,
            stamp_id TEXT,
            block_height INTEGER NOT NULL,
            block_time TEXT,
            sender TEXT NOT NULL,
            op TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            valid INTEGER NOT NULL,
            error TEXT,
            applied_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS spaces (
            space_id TEXT PRIMARY KEY,
            owner TEXT NOT NULL,
            tick TEXT NOT NULL,
            name TEXT NOT NULL,
            about TEXT,
            strategies_json TEXT NOT NULL,
            voting_json TEXT NOT NULL,
            admins_json TEXT NOT NULL,
            voting_delay INTEGER NOT NULL,
            voting_period INTEGER NOT NULL,
            voting_quorum REAL NOT NULL,
            voting_type TEXT NOT NULL,
            created_block INTEGER NOT NULL,
            created_txid TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS proposals (
            space_id TEXT NOT NULL,
            proposal_id INTEGER NOT NULL,
            proposer TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            discussion TEXT,
            choices_json TEXT NOT NULL,
            snapshot_block INTEGER NOT NULL,
            start_block INTEGER NOT NULL,
            end_block INTEGER NOT NULL,
            created_block INTEGER NOT NULL,
            created_txid TEXT NOT NULL,
            PRIMARY KEY (space_id, proposal_id),
            FOREIGN KEY (space_id) REFERENCES spaces(space_id)
        );

        CREATE TABLE IF NOT EXISTS votes (
            space_id TEXT NOT NULL,
            proposal_id INTEGER NOT NULL,
            voter TEXT NOT NULL,
            choice INTEGER NOT NULL,
            voting_power REAL NOT NULL,
            cast_block INTEGER NOT NULL,
            cast_txid TEXT NOT NULL,
            PRIMARY KEY (space_id, proposal_id, voter),
            FOREIGN KEY (space_id, proposal_id) REFERENCES proposals(space_id, proposal_id)
        );

        CREATE TABLE IF NOT EXISTS delegation_events (
            space_id TEXT NOT NULL,
            delegator TEXT NOT NULL,
            delegate TEXT NOT NULL,
            block_height INTEGER NOT NULL,
            txid TEXT NOT NULL,
            PRIMARY KEY (space_id, delegator, txid),
            FOREIGN KEY (space_id) REFERENCES spaces(space_id)
        );

        CREATE TABLE IF NOT EXISTS delegations (
            space_id TEXT NOT NULL,
            delegator TEXT NOT NULL,
            delegate TEXT NOT NULL,
            block_height INTEGER NOT NULL,
            txid TEXT NOT NULL,
            PRIMARY KEY (space_id, delegator),
            FOREIGN KEY (space_id) REFERENCES spaces(space_id)
        );

        CREATE TABLE IF NOT EXISTS attestations (
            space_id TEXT NOT NULL,
            proposal_id INTEGER NOT NULL,
            attestor TEXT NOT NULL,
            txid TEXT NOT NULL,
            block_height INTEGER NOT NULL,
            result_json TEXT NOT NULL,
            PRIMARY KEY (space_id, proposal_id),
            FOREIGN KEY (space_id, proposal_id) REFERENCES proposals(space_id, proposal_id)
        );

        CREATE TABLE IF NOT EXISTS balance_snapshots (
            tick TEXT NOT NULL,
            address TEXT NOT NULL,
            block_height INTEGER NOT NULL,
            balance REAL NOT NULL,
            source TEXT,
            imported_at TEXT NOT NULL,
            PRIMARY KEY (tick, address, block_height)
        );

        CREATE TABLE IF NOT EXISTS sync_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_events_block_height ON events(block_height);
        CREATE INDEX IF NOT EXISTS idx_proposals_space ON proposals(space_id);
        CREATE INDEX IF NOT EXISTS idx_votes_space_proposal ON votes(space_id, proposal_id);
        CREATE INDEX IF NOT EXISTS idx_delegation_events_space_block ON delegation_events(space_id, block_height);
        CREATE INDEX IF NOT EXISTS idx_balances_tick_addr_block ON balance_snapshots(tick, address, block_height);
        """
    )
    conn.commit()


def write_event_log(conn: sqlite3.Connection, event: NormalizedEvent, valid: bool, error: Optional[str]) -> bool:
    try:
        conn.execute(
            """
            INSERT INTO events (
                txid, stamp_id, block_height, block_time, sender, op, payload_json,
                valid, error, applied_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.txid,
                event.stamp_id,
                event.block_height,
                event.block_time,
                event.sender,
                event.op,
                json_dumps(event.payload),
                1 if valid else 0,
                error,
                utc_now_iso(),
            ),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def get_space(conn: sqlite3.Connection, space_id: str) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM spaces WHERE space_id = ?",
        (space_id,),
    ).fetchone()


def get_proposal(conn: sqlite3.Connection, space_id: str, proposal_id: int) -> Optional[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM proposals WHERE space_id = ? AND proposal_id = ?",
        (space_id, proposal_id),
    ).fetchone()


def get_latest_block(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COALESCE(MAX(block_height), 0) AS block FROM events WHERE valid = 1").fetchone()
    return int(row["block"] if row is not None else 0)


def get_sync_state(conn: sqlite3.Connection, key: str) -> Optional[str]:
    row = conn.execute("SELECT value FROM sync_state WHERE key = ?", (key,)).fetchone()
    return str(row["value"]) if row is not None else None


def set_sync_state(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        """
        INSERT INTO sync_state (key, value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
            value = excluded.value,
            updated_at = excluded.updated_at
        """,
        (key, value, utc_now_iso()),
    )


def list_sync_state(conn: sqlite3.Connection) -> List[Dict[str, str]]:
    rows = conn.execute(
        """
        SELECT key, value, updated_at
        FROM sync_state
        ORDER BY key
        """
    ).fetchall()
    return [
        {
            "key": str(row["key"]),
            "value": str(row["value"]),
            "updated_at": str(row["updated_at"]),
        }
        for row in rows
    ]


def get_latest_delegation_at_block(
    conn: sqlite3.Connection, space_id: str, delegator: str, snapshot_block: int
) -> Optional[str]:
    row = conn.execute(
        """
        SELECT delegate
        FROM delegation_events
        WHERE space_id = ? AND delegator = ? AND block_height <= ?
        ORDER BY block_height DESC, txid DESC
        LIMIT 1
        """,
        (space_id, delegator, snapshot_block),
    ).fetchone()
    return str(row["delegate"]) if row is not None else None


def resolve_delegate_target(
    conn: sqlite3.Connection, space_id: str, address: str, snapshot_block: int
) -> str:
    """
    Resolve delegation target with SRC-420 one-hop semantics.

    Rules implemented:
    - Delegation is not transitively forwarded (A->B->C does not make A count for C).
    - Circular delegations collapse to self-power for cycle members (A<->B => each own).
    """
    direct_delegate = get_latest_delegation_at_block(conn, space_id, address, snapshot_block)
    if direct_delegate is None or direct_delegate == address:
        return address

    # Detect whether the direct delegate path loops back to address.
    # If it does, participant keeps their own power.
    visited = {address}
    current = direct_delegate
    while True:
        next_delegate = get_latest_delegation_at_block(conn, space_id, current, snapshot_block)
        if next_delegate is None or next_delegate == current:
            return direct_delegate
        if next_delegate == address:
            return address
        if next_delegate in visited:
            # Cycle exists but does not include address; one-hop target remains direct delegate.
            return direct_delegate
        visited.add(current)
        current = next_delegate


def collect_participants(
    conn: sqlite3.Connection, space_id: str, tick: str, snapshot_block: int, always_include: Optional[str] = None
) -> List[str]:
    participants = set()

    for row in conn.execute(
        """
        SELECT DISTINCT address
        FROM balance_snapshots
        WHERE tick = ? AND block_height <= ?
        """,
        (tick, snapshot_block),
    ):
        participants.add(str(row["address"]))

    for row in conn.execute(
        """
        SELECT delegator, delegate
        FROM delegation_events
        WHERE space_id = ? AND block_height <= ?
        """,
        (space_id, snapshot_block),
    ):
        participants.add(str(row["delegator"]))
        participants.add(str(row["delegate"]))

    if always_include:
        participants.add(always_include)

    return sorted(participants)


def resolve_balance_at_block(
    conn: sqlite3.Connection, tick: str, address: str, snapshot_block: int, settings: ReducerSettings
) -> float:
    row = conn.execute(
        """
        SELECT balance
        FROM balance_snapshots
        WHERE tick = ? AND address = ? AND block_height <= ?
        ORDER BY block_height DESC
        LIMIT 1
        """,
        (tick, address, snapshot_block),
    ).fetchone()
    if row is not None:
        return max(float(row["balance"]), 0.0)

    if settings.enforce_balance_checks:
        return 0.0
    return max(settings.default_voting_power, 0.0)


def compute_effective_voting_power(
    conn: sqlite3.Connection,
    space_id: str,
    tick: str,
    voter: str,
    snapshot_block: int,
    settings: ReducerSettings,
) -> float:
    participants = collect_participants(conn, space_id, tick, snapshot_block, always_include=voter)

    total = 0.0
    for participant in participants:
        delegate_target = resolve_delegate_target(conn, space_id, participant, snapshot_block)
        if delegate_target != voter:
            continue
        power = resolve_balance_at_block(conn, tick, participant, snapshot_block, settings)
        if power <= 0:
            continue
        total += power

    return total


def reduce_deploy(
    conn: sqlite3.Connection, event: NormalizedEvent
) -> Tuple[bool, Optional[str]]:
    payload = event.payload
    space_id = str(payload.get("space", "")).strip()
    tick = str(payload.get("tick", "")).strip().upper()
    name = str(payload.get("name", "")).strip()
    about = payload.get("about")
    strategies = payload.get("strategies")
    voting = payload.get("voting")
    admins = payload.get("admins")

    if not SPACE_ID_RE.fullmatch(space_id):
        return False, "invalid space id"
    if not tick:
        return False, "missing tick"
    if not name or len(name) > 64:
        return False, "invalid name"
    if not isinstance(strategies, list) or len(strategies) == 0:
        return False, "strategies must be a non-empty list"
    if not isinstance(voting, dict):
        return False, "voting must be an object"
    if not isinstance(admins, list):
        return False, "admins must be an array"
    if get_space(conn, space_id) is not None:
        return False, "space already exists (first valid DEPLOY wins)"

    try:
        delay = parse_int(voting.get("delay"), "voting.delay")
        period = parse_int(voting.get("period"), "voting.period")
        quorum = parse_float(voting.get("quorum"), "voting.quorum")
    except ValueError as exc:
        return False, str(exc)

    voting_type = str(voting.get("type", "")).strip()
    if voting_type not in ALLOWED_VOTING_TYPES:
        return False, "invalid voting type"
    if delay < 0:
        return False, "voting.delay must be >= 0"
    if period < 144:
        return False, "voting.period must be >= 144 blocks"
    if quorum < 0:
        return False, "voting.quorum must be >= 0"

    conn.execute(
        """
        INSERT INTO spaces (
            space_id, owner, tick, name, about, strategies_json, voting_json,
            admins_json, voting_delay, voting_period, voting_quorum, voting_type,
            created_block, created_txid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            space_id,
            event.sender,
            tick,
            name,
            str(about) if about is not None else None,
            json_dumps(strategies),
            json_dumps(voting),
            json_dumps(admins),
            delay,
            period,
            quorum,
            voting_type,
            event.block_height,
            event.txid,
        ),
    )
    return True, None


def reduce_propose(
    conn: sqlite3.Connection, event: NormalizedEvent, settings: ReducerSettings
) -> Tuple[bool, Optional[str]]:
    payload = event.payload
    space_id = str(payload.get("space", "")).strip()
    space = get_space(conn, space_id)
    if space is None:
        return False, "space does not exist"

    try:
        proposal_id = parse_int(payload.get("id"), "id")
        snapshot = parse_int(payload.get("snapshot"), "snapshot")
        start = parse_int(payload.get("start"), "start")
        end = parse_int(payload.get("end"), "end")
    except ValueError as exc:
        return False, str(exc)

    if proposal_id <= 0:
        return False, "proposal id must be > 0"

    next_id_row = conn.execute(
        "SELECT COALESCE(MAX(proposal_id), 0) + 1 AS next_id FROM proposals WHERE space_id = ?",
        (space_id,),
    ).fetchone()
    next_id = int(next_id_row["next_id"] if next_id_row is not None else 1)
    if proposal_id != next_id:
        return False, f"proposal id must be sequential; expected {next_id}"

    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    discussion = payload.get("discussion")
    choices = payload.get("choices")
    if not title or len(title) > 128:
        return False, "invalid title"
    if not body:
        return False, "body is required"
    if not isinstance(choices, list) or not (2 <= len(choices) <= 10):
        return False, "choices must contain 2-10 entries"

    if snapshot > event.block_height:
        return False, "snapshot must be <= current block"
    if start < snapshot + int(space["voting_delay"]):
        return False, "start must be >= snapshot + voting.delay"
    if end < start + int(space["voting_period"]):
        return False, "end must be >= start + voting.period"

    admins = json_loads(space["admins_json"], default=[])
    if isinstance(admins, list) and len(admins) > 0 and event.sender not in admins:
        return False, "proposer not authorized (admins only)"

    if settings.enforce_balance_checks:
        proposer_power = resolve_balance_at_block(
            conn,
            str(space["tick"]),
            event.sender,
            snapshot,
            ReducerSettings(enforce_balance_checks=True, default_voting_power=0.0),
        )
        if proposer_power <= 0:
            return False, "proposer voting power is zero at snapshot block"

    conn.execute(
        """
        INSERT INTO proposals (
            space_id, proposal_id, proposer, title, body, discussion, choices_json,
            snapshot_block, start_block, end_block, created_block, created_txid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            space_id,
            proposal_id,
            event.sender,
            title,
            body,
            str(discussion) if discussion is not None else None,
            json_dumps(choices),
            snapshot,
            start,
            end,
            event.block_height,
            event.txid,
        ),
    )
    return True, None


def reduce_vote(
    conn: sqlite3.Connection, event: NormalizedEvent, settings: ReducerSettings
) -> Tuple[bool, Optional[str]]:
    payload = event.payload
    space_id = str(payload.get("space", "")).strip()
    try:
        proposal_id = parse_int(payload.get("proposal"), "proposal")
        choice = parse_int(payload.get("choice"), "choice")
    except ValueError as exc:
        return False, str(exc)

    proposal = get_proposal(conn, space_id, proposal_id)
    if proposal is None:
        return False, "proposal does not exist"

    if event.block_height < int(proposal["start_block"]) or event.block_height > int(proposal["end_block"]):
        return False, "vote is outside proposal voting window"

    choices = json_loads(proposal["choices_json"], default=[])
    if not isinstance(choices, list) or choice < 1 or choice > len(choices):
        return False, "invalid choice index"

    space = get_space(conn, space_id)
    if space is None:
        return False, "space does not exist"

    snapshot_block = int(proposal["snapshot_block"])
    voting_power = compute_effective_voting_power(
        conn,
        space_id=space_id,
        tick=str(space["tick"]),
        voter=event.sender,
        snapshot_block=snapshot_block,
        settings=settings,
    )

    if voting_power <= 0 and settings.enforce_balance_checks:
        return False, "voter has zero voting power at snapshot block"
    if voting_power <= 0:
        voting_power = max(settings.default_voting_power, 0.0)

    conn.execute(
        """
        INSERT INTO votes (
            space_id, proposal_id, voter, choice, voting_power, cast_block, cast_txid
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(space_id, proposal_id, voter) DO UPDATE SET
            choice = excluded.choice,
            voting_power = excluded.voting_power,
            cast_block = excluded.cast_block,
            cast_txid = excluded.cast_txid
        """,
        (
            space_id,
            proposal_id,
            event.sender,
            choice,
            voting_power,
            event.block_height,
            event.txid,
        ),
    )
    return True, None


def reduce_delegate(
    conn: sqlite3.Connection, event: NormalizedEvent
) -> Tuple[bool, Optional[str]]:
    payload = event.payload
    space_id = str(payload.get("space", "")).strip()
    delegate = str(payload.get("to", "")).strip()

    if get_space(conn, space_id) is None:
        return False, "space does not exist"
    if len(delegate) < 8:
        return False, "delegate address is too short"

    conn.execute(
        """
        INSERT INTO delegation_events (
            space_id, delegator, delegate, block_height, txid
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (space_id, event.sender, delegate, event.block_height, event.txid),
    )

    conn.execute(
        """
        INSERT INTO delegations (
            space_id, delegator, delegate, block_height, txid
        ) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(space_id, delegator) DO UPDATE SET
            delegate = excluded.delegate,
            block_height = excluded.block_height,
            txid = excluded.txid
        """,
        (space_id, event.sender, delegate, event.block_height, event.txid),
    )
    return True, None


def reduce_attest(
    conn: sqlite3.Connection, event: NormalizedEvent
) -> Tuple[bool, Optional[str]]:
    payload = event.payload
    space_id = str(payload.get("space", "")).strip()
    try:
        proposal_id = parse_int(payload.get("proposal"), "proposal")
    except ValueError as exc:
        return False, str(exc)

    proposal = get_proposal(conn, space_id, proposal_id)
    if proposal is None:
        return False, "proposal does not exist"
    if event.block_height <= int(proposal["end_block"]):
        return False, "ATTEST must be after proposal end block"
    space = get_space(conn, space_id)
    if space is None:
        return False, "space does not exist"

    result = payload.get("result")
    if not isinstance(result, dict):
        return False, "result must be an object"

    admins = json_loads(space["admins_json"], default=[])
    is_new_admin = event.sender == str(space["owner"]) or (
        isinstance(admins, list) and event.sender in admins
    )

    existing = conn.execute(
        """
        SELECT attestor
        FROM attestations
        WHERE space_id = ? AND proposal_id = ?
        """,
        (space_id, proposal_id),
    ).fetchone()

    if existing is None:
        conn.execute(
            """
            INSERT INTO attestations (
                space_id, proposal_id, attestor, txid, block_height, result_json
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (space_id, proposal_id, event.sender, event.txid, event.block_height, json_dumps(result)),
        )
        return True, None

    existing_attestor = str(existing["attestor"])
    is_existing_admin = existing_attestor == str(space["owner"]) or (
        isinstance(admins, list) and existing_attestor in admins
    )

    # Spec alignment:
    # - first valid admin attestation wins
    # - non-admin attestation can be superseded by first admin attestation
    if is_existing_admin:
        return False, "admin attestation already exists (first admin attestation wins)"

    if is_new_admin:
        conn.execute(
            """
            UPDATE attestations
            SET attestor = ?, txid = ?, block_height = ?, result_json = ?
            WHERE space_id = ? AND proposal_id = ?
            """,
            (
                event.sender,
                event.txid,
                event.block_height,
                json_dumps(result),
                space_id,
                proposal_id,
            ),
        )
        return True, None

    return False, "non-admin attestation already exists; waiting for admin attestation"


def reduce_event(
    conn: sqlite3.Connection, event: NormalizedEvent, settings: ReducerSettings
) -> Tuple[bool, Optional[str]]:
    if event.op == "DEPLOY":
        return reduce_deploy(conn, event)
    if event.op == "PROPOSE":
        return reduce_propose(conn, event, settings)
    if event.op == "VOTE":
        return reduce_vote(conn, event, settings)
    if event.op == "DELEGATE":
        return reduce_delegate(conn, event)
    if event.op == "ATTEST":
        return reduce_attest(conn, event)
    return False, f"unsupported operation '{event.op}'"


def ingest_records(
    conn: sqlite3.Connection,
    records: Iterable[Dict[str, Any]],
    settings: ReducerSettings,
) -> Dict[str, int]:
    normalized: List[NormalizedEvent] = []
    invalid_records = 0

    for idx, raw in enumerate(records):
        event, error = normalize_event(raw, idx)
        if event is None:
            invalid_records += 1
            placeholder = NormalizedEvent(
                txid=synthetic_txid(raw, idx),
                stamp_id=None,
                block_height=0,
                block_time=None,
                sender="unknown",
                op="INVALID",
                payload={"raw": raw},
            )
            with conn:
                write_event_log(conn, placeholder, valid=False, error=error or "invalid event")
            continue
        normalized.append(event)

    normalized.sort(key=lambda e: (e.block_height, e.txid))

    applied = 0
    rejected = invalid_records
    duplicates = 0

    for event in normalized:
        with conn:
            if conn.execute("SELECT 1 FROM events WHERE txid = ?", (event.txid,)).fetchone() is not None:
                duplicates += 1
                continue

            valid, error = reduce_event(conn, event, settings)
            write_event_log(conn, event, valid=valid, error=error)

            if valid:
                applied += 1
            else:
                rejected += 1

    return {
        "applied": applied,
        "rejected": rejected,
        "duplicates": duplicates,
        "total_input": applied + rejected + duplicates,
    }


def import_balance_records(conn: sqlite3.Connection, records: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    inserted = 0
    updated = 0
    skipped = 0
    now = utc_now_iso()

    with conn:
        for record in records:
            try:
                tick = str(record["tick"]).strip().upper()
                address = str(record["address"]).strip()
                block_height = int(record["block_height"])
                balance = float(record["balance"])
                source = str(record.get("source", "manual"))
            except (KeyError, TypeError, ValueError):
                skipped += 1
                continue

            cursor = conn.execute(
                """
                INSERT INTO balance_snapshots (
                    tick, address, block_height, balance, source, imported_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(tick, address, block_height) DO UPDATE SET
                    balance = excluded.balance,
                    source = excluded.source,
                    imported_at = excluded.imported_at
                """,
                (tick, address, block_height, balance, source, now),
            )
            if cursor.rowcount == 1:
                inserted += 1
            else:
                updated += 1

    return {"inserted": inserted, "updated": updated, "skipped": skipped}


def resolve_start_block(
    conn: sqlite3.Connection, cursor_key: str, override_start_block: Optional[int]
) -> int:
    if override_start_block is not None:
        return max(int(override_start_block), 0)

    previous = get_sync_state(conn, cursor_key)
    if previous is None:
        return 0

    try:
        return max(int(previous) + 1, 0)
    except ValueError:
        return 0


def resolve_effective_end_block(
    start_block: int,
    requested_end_block: Optional[int],
    tip_height: Optional[int],
    min_confirmations: int,
) -> Optional[int]:
    if min_confirmations < 0:
        raise ValueError("min-confirmations must be >= 0")
    if tip_height is None:
        return requested_end_block

    finalized_end = int(tip_height) - int(min_confirmations)
    if requested_end_block is None:
        return finalized_end
    return min(int(requested_end_block), finalized_end)


def parse_header_values(header_values: Sequence[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for entry in header_values:
        if ":" not in entry:
            continue
        key, value = entry.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key:
            headers[key] = value
    return headers


def fetch_json_url(
    url: str,
    timeout_sec: float = 20.0,
    headers: Optional[Dict[str, str]] = None,
) -> Any:
    req = urllib_request.Request(url, headers=headers or {})
    try:
        with urllib_request.urlopen(req, timeout=timeout_sec) as response:
            body = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} while fetching {url}") from exc
    except urllib_error.URLError as exc:
        raise RuntimeError(f"network error while fetching {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"timeout while fetching {url}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"non-JSON response from {url}") from exc


def extract_path_value(payload: Any, path: Optional[str]) -> Any:
    if path is None or path.strip() == "":
        return payload

    current: Any = payload
    for part in path.split("."):
        key = part.strip()
        if not key:
            continue
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def fetch_block_hash(
    hash_url_template: str,
    block_height: int,
    hash_path: Optional[str],
    timeout_sec: float,
    headers: Optional[Dict[str, str]] = None,
    fetcher=fetch_json_url,
) -> str:
    url = hash_url_template.format(
        block=block_height,
        block_height=block_height,
        height=block_height,
    )
    payload = fetcher(url, timeout_sec=timeout_sec, headers=headers)

    if hash_path:
        value = extract_path_value(payload, hash_path)
        if value is None:
            raise RuntimeError(f"hash path '{hash_path}' not found for block {block_height}")
        return str(value)

    # Fallback auto-detection.
    for candidate_path in ("block_hash", "hash", "block.hash", "data.block_hash", "data.hash"):
        value = extract_path_value(payload, candidate_path)
        if value is not None:
            return str(value)

    raise RuntimeError(f"could not extract block hash for block {block_height}")


def extract_records_from_payload(
    payload: Any, records_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]

    if not isinstance(payload, dict):
        return []

    candidate: Any = None
    if records_key:
        candidate = payload.get(records_key)
    else:
        for key in ("results", "records", "items", "stamps", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                candidate = value
                break
            if isinstance(value, dict):
                for nested_key in ("results", "records", "items", "stamps"):
                    nested_value = value.get(nested_key)
                    if isinstance(nested_value, list):
                        candidate = nested_value
                        break
            if isinstance(candidate, list):
                break

    if not isinstance(candidate, list):
        return []
    return [row for row in candidate if isinstance(row, dict)]


def extract_has_more(
    payload: Any, has_more_key: Optional[str] = None
) -> Optional[bool]:
    if not isinstance(payload, dict):
        return None

    if has_more_key:
        value = payload.get(has_more_key)
    else:
        value = None
        for key in ("has_more", "hasNext", "more"):
            if key in payload:
                value = payload.get(key)
                break
        if value is None and isinstance(payload.get("pagination"), dict):
            pagination = payload.get("pagination")
            for key in ("has_more", "hasNext", "more"):
                if key in pagination:
                    value = pagination.get(key)
                    break

    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
    return None


def estimate_max_block_height(records: Sequence[Dict[str, Any]]) -> Optional[int]:
    max_block: Optional[int] = None
    for idx, record in enumerate(records):
        normalized, _ = normalize_event(record, idx)
        if normalized is None:
            continue
        if max_block is None or normalized.block_height > max_block:
            max_block = normalized.block_height
    return max_block


def filter_records_by_block_range(
    records: Sequence[Dict[str, Any]],
    start_block: int,
    end_block: Optional[int],
) -> Tuple[List[Dict[str, Any]], int]:
    kept: List[Dict[str, Any]] = []
    filtered_out = 0

    for idx, record in enumerate(records):
        normalized, _ = normalize_event(record, idx)
        if normalized is None:
            # Preserve invalid records for logging/observability.
            kept.append(record)
            continue

        if normalized.block_height < start_block:
            filtered_out += 1
            continue
        if end_block is not None and normalized.block_height > end_block:
            filtered_out += 1
            continue
        kept.append(record)

    return kept, filtered_out


def build_url_from_template(
    url_template: str,
    page: int,
    page_size: int,
    start_block: int,
    end_block: Optional[int],
) -> str:
    return url_template.format(
        page=page,
        limit=page_size,
        start_block=start_block,
        end_block=("" if end_block is None else end_block),
    )


def sync_http_feed(
    conn: sqlite3.Connection,
    settings: ReducerSettings,
    url_template: str,
    start_block: int,
    end_block: Optional[int],
    page_size: int,
    max_pages: int,
    timeout_sec: float,
    records_key: Optional[str],
    has_more_key: Optional[str],
    headers: Optional[Dict[str, str]] = None,
    fetcher=fetch_json_url,
) -> Dict[str, Any]:
    pages_fetched = 0
    total_records = 0
    applied = 0
    rejected = 0
    duplicates = 0
    max_seen_block: Optional[int] = None
    filtered_out = 0
    stop_reason = "max_pages_reached"

    for page in range(1, max_pages + 1):
        url = build_url_from_template(
            url_template=url_template,
            page=page,
            page_size=page_size,
            start_block=start_block,
            end_block=end_block,
        )

        payload = fetcher(url, timeout_sec=timeout_sec, headers=headers)
        pages_fetched += 1

        records = extract_records_from_payload(payload, records_key=records_key)
        total_records += len(records)
        records, filtered = filter_records_by_block_range(
            records=records,
            start_block=start_block,
            end_block=end_block,
        )
        filtered_out += filtered

        page_max_block = estimate_max_block_height(records)
        if page_max_block is not None:
            if max_seen_block is None or page_max_block > max_seen_block:
                max_seen_block = page_max_block

        summary = ingest_records(conn, records, settings=settings)
        applied += int(summary["applied"])
        rejected += int(summary["rejected"])
        duplicates += int(summary["duplicates"])

        has_more = extract_has_more(payload, has_more_key=has_more_key)
        if has_more is False:
            stop_reason = "has_more_false"
            break
        if has_more is None and len(records) < page_size:
            stop_reason = "short_page"
            break
        if len(records) == 0:
            stop_reason = "empty_page"
            break

    return {
        "pages_fetched": pages_fetched,
        "records_fetched": total_records,
        "applied": applied,
        "rejected": rejected,
        "duplicates": duplicates,
        "filtered_out_of_range": filtered_out,
        "max_seen_block": max_seen_block,
        "stop_reason": stop_reason,
    }


def reset_derived_state(conn: sqlite3.Connection) -> None:
    # Order matters because of foreign keys.
    conn.execute("DELETE FROM attestations")
    conn.execute("DELETE FROM votes")
    conn.execute("DELETE FROM delegations")
    conn.execute("DELETE FROM delegation_events")
    conn.execute("DELETE FROM proposals")
    conn.execute("DELETE FROM spaces")


def replay_valid_events(
    conn: sqlite3.Connection,
    settings: ReducerSettings,
    max_block: Optional[int] = None,
) -> Dict[str, Any]:
    if max_block is None:
        rows = conn.execute(
            """
            SELECT txid, stamp_id, block_height, block_time, sender, op, payload_json
            FROM events
            WHERE valid = 1
            ORDER BY block_height, txid
            """
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT txid, stamp_id, block_height, block_time, sender, op, payload_json
            FROM events
            WHERE valid = 1 AND block_height <= ?
            ORDER BY block_height, txid
            """,
            (max_block,),
        ).fetchall()

    replayed = 0
    failures: List[Dict[str, Any]] = []

    for row in rows:
        payload = json_loads(row["payload_json"], default={})
        if not isinstance(payload, dict):
            failures.append(
                {
                    "txid": row["txid"],
                    "error": "stored payload_json is not an object",
                }
            )
            continue

        event = NormalizedEvent(
            txid=str(row["txid"]),
            stamp_id=(str(row["stamp_id"]) if row["stamp_id"] is not None else None),
            block_height=int(row["block_height"]),
            block_time=(str(row["block_time"]) if row["block_time"] is not None else None),
            sender=str(row["sender"]),
            op=str(row["op"]),
            payload=payload,
        )

        valid, error = reduce_event(conn, event, settings=settings)
        if not valid:
            failures.append(
                {
                    "txid": event.txid,
                    "block_height": event.block_height,
                    "op": event.op,
                    "error": error or "unknown replay error",
                }
            )
            continue
        replayed += 1

    summary = {
        "replayed": replayed,
        "failed": len(failures),
    }
    if failures:
        summary["first_failure"] = failures[0]
        summary["failures"] = failures[:10]
    return summary


def rollback_to_block(
    conn: sqlite3.Connection,
    to_block: int,
    settings: ReducerSettings,
    prune_future_events: bool = True,
    prune_balance_snapshots: bool = False,
    cursor_key: Optional[str] = "sync:http:last_block",
) -> Dict[str, Any]:
    if to_block < 0:
        raise ValueError("to-block must be >= 0")

    row = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM events) AS events_count,
            (SELECT COUNT(*) FROM spaces) AS spaces_count,
            (SELECT COUNT(*) FROM proposals) AS proposals_count,
            (SELECT COUNT(*) FROM votes) AS votes_count,
            (SELECT COUNT(*) FROM delegations) AS delegations_count,
            (SELECT COUNT(*) FROM attestations) AS attestations_count,
            (SELECT COUNT(*) FROM balance_snapshots) AS balances_count
        """
    ).fetchone()

    before = {
        "events": int(row["events_count"]),
        "spaces": int(row["spaces_count"]),
        "proposals": int(row["proposals_count"]),
        "votes": int(row["votes_count"]),
        "delegations": int(row["delegations_count"]),
        "attestations": int(row["attestations_count"]),
        "balance_snapshots": int(row["balances_count"]),
        "latest_block": get_latest_block(conn),
    }

    cursor_before = get_sync_state(conn, cursor_key) if cursor_key else None

    deleted_events = 0
    deleted_balances = 0

    with conn:
        if prune_future_events:
            deleted_events = conn.execute(
                "DELETE FROM events WHERE block_height > ?",
                (to_block,),
            ).rowcount

        if prune_balance_snapshots:
            deleted_balances = conn.execute(
                "DELETE FROM balance_snapshots WHERE block_height > ?",
                (to_block,),
            ).rowcount

        reset_derived_state(conn)
        replay_summary = replay_valid_events(conn, settings=settings, max_block=to_block)
        if replay_summary["failed"] > 0:
            first_failure = replay_summary.get("first_failure", {})
            raise RuntimeError(
                f"rollback replay failed after {replay_summary['replayed']} events; "
                f"first failure: {first_failure}"
            )

        if cursor_key:
            set_sync_state(conn, cursor_key, str(to_block))

    row_after = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM events) AS events_count,
            (SELECT COUNT(*) FROM spaces) AS spaces_count,
            (SELECT COUNT(*) FROM proposals) AS proposals_count,
            (SELECT COUNT(*) FROM votes) AS votes_count,
            (SELECT COUNT(*) FROM delegations) AS delegations_count,
            (SELECT COUNT(*) FROM attestations) AS attestations_count,
            (SELECT COUNT(*) FROM balance_snapshots) AS balances_count
        """
    ).fetchone()

    after = {
        "events": int(row_after["events_count"]),
        "spaces": int(row_after["spaces_count"]),
        "proposals": int(row_after["proposals_count"]),
        "votes": int(row_after["votes_count"]),
        "delegations": int(row_after["delegations_count"]),
        "attestations": int(row_after["attestations_count"]),
        "balance_snapshots": int(row_after["balances_count"]),
        "latest_block": get_latest_block(conn),
    }

    cursor_after = get_sync_state(conn, cursor_key) if cursor_key else None

    return {
        "to_block": to_block,
        "prune_future_events": prune_future_events,
        "prune_balance_snapshots": prune_balance_snapshots,
        "deleted_events": int(deleted_events),
        "deleted_balance_snapshots": int(deleted_balances),
        "replayed_events": int(replay_summary["replayed"]),
        "cursor_key": cursor_key,
        "cursor_before": cursor_before,
        "cursor_after": cursor_after,
        "before": before,
        "after": after,
    }


def run_reorg_check(
    conn: sqlite3.Connection,
    settings: ReducerSettings,
    cursor_key: str,
    hash_state_key: str,
    hash_url_template: str,
    hash_path: Optional[str],
    timeout_sec: float,
    headers: Optional[Dict[str, str]],
    auto_rollback: bool,
    rollback_blocks: int,
    fetcher=fetch_json_url,
) -> Dict[str, Any]:
    if rollback_blocks < 0:
        raise ValueError("rollback-blocks must be >= 0")

    cursor_raw = get_sync_state(conn, cursor_key)
    result: Dict[str, Any] = {
        "cursor_key": cursor_key,
        "hash_state_key": hash_state_key,
        "cursor_before": cursor_raw,
        "auto_rollback": auto_rollback,
        "rollback_blocks": rollback_blocks,
        "reorg_detected": False,
        "status": "unknown",
    }

    if cursor_raw is None:
        result["status"] = "no_cursor"
        return result

    try:
        cursor_block = int(cursor_raw)
    except ValueError:
        result["status"] = "invalid_cursor"
        return result

    stored_hash = get_sync_state(conn, hash_state_key)
    result["stored_hash_before"] = stored_hash

    current_hash = fetch_block_hash(
        hash_url_template=hash_url_template,
        block_height=cursor_block,
        hash_path=hash_path,
        timeout_sec=timeout_sec,
        headers=headers,
        fetcher=fetcher,
    )
    result["current_hash"] = current_hash

    if stored_hash is None:
        with conn:
            set_sync_state(conn, hash_state_key, current_hash)
        result["stored_hash_after"] = current_hash
        result["status"] = "hash_initialized"
        return result

    if stored_hash == current_hash:
        result["stored_hash_after"] = stored_hash
        result["status"] = "ok"
        return result

    result["reorg_detected"] = True
    result["status"] = "mismatch_no_rollback"

    if not auto_rollback:
        result["stored_hash_after"] = stored_hash
        return result

    target_block = max(cursor_block - rollback_blocks, 0)
    rollback_summary = rollback_to_block(
        conn=conn,
        to_block=target_block,
        settings=settings,
        prune_future_events=True,
        prune_balance_snapshots=False,
        cursor_key=cursor_key,
    )
    result["rollback"] = rollback_summary

    cursor_after_raw = get_sync_state(conn, cursor_key)
    result["cursor_after"] = cursor_after_raw

    if cursor_after_raw is not None:
        try:
            cursor_after = int(cursor_after_raw)
            refreshed_hash = fetch_block_hash(
                hash_url_template=hash_url_template,
                block_height=cursor_after,
                hash_path=hash_path,
                timeout_sec=timeout_sec,
                headers=headers,
                fetcher=fetcher,
            )
            with conn:
                set_sync_state(conn, hash_state_key, refreshed_hash)
            result["stored_hash_after"] = refreshed_hash
        except ValueError:
            result["stored_hash_after"] = get_sync_state(conn, hash_state_key)
    else:
        result["stored_hash_after"] = get_sync_state(conn, hash_state_key)

    result["status"] = "mismatch_rolled_back"
    return result


def serialize_space(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "space": row["space_id"],
        "owner": row["owner"],
        "tick": row["tick"],
        "name": row["name"],
        "about": row["about"],
        "strategies": json_loads(row["strategies_json"], default=[]),
        "voting": json_loads(row["voting_json"], default={}),
        "admins": json_loads(row["admins_json"], default=[]),
        "created_block": row["created_block"],
        "created_txid": row["created_txid"],
    }


def proposal_status(row: sqlite3.Row, latest_block: int) -> str:
    if latest_block < int(row["start_block"]):
        return "pending"
    if latest_block <= int(row["end_block"]):
        return "active"
    return "closed"


def serialize_proposal(row: sqlite3.Row, latest_block: int) -> Dict[str, Any]:
    return {
        "space": row["space_id"],
        "id": row["proposal_id"],
        "proposer": row["proposer"],
        "title": row["title"],
        "body": row["body"],
        "discussion": row["discussion"],
        "choices": json_loads(row["choices_json"], default=[]),
        "snapshot": row["snapshot_block"],
        "start": row["start_block"],
        "end": row["end_block"],
        "status": proposal_status(row, latest_block),
        "created_block": row["created_block"],
        "created_txid": row["created_txid"],
    }


def calculate_results(conn: sqlite3.Connection, space_id: str, proposal_id: int) -> Optional[Dict[str, Any]]:
    proposal = get_proposal(conn, space_id, proposal_id)
    if proposal is None:
        return None
    space = get_space(conn, space_id)
    if space is None:
        return None

    choices = json_loads(proposal["choices_json"], default=[])
    scores = [0.0] * len(choices)

    votes = conn.execute(
        """
        SELECT choice, voting_power
        FROM votes
        WHERE space_id = ? AND proposal_id = ?
        """,
        (space_id, proposal_id),
    ).fetchall()

    for vote in votes:
        idx = int(vote["choice"]) - 1
        if 0 <= idx < len(scores):
            scores[idx] += float(vote["voting_power"])

    total = float(sum(scores))
    quorum_required = float(space["voting_quorum"])
    quorum = total >= quorum_required

    winner: Optional[int] = None
    if scores:
        max_score = max(scores)
        if max_score > 0:
            winners = [idx + 1 for idx, score in enumerate(scores) if score == max_score]
            if len(winners) == 1:
                winner = winners[0]

    attestation = conn.execute(
        """
        SELECT attestor, txid, block_height, result_json
        FROM attestations
        WHERE space_id = ? AND proposal_id = ?
        """,
        (space_id, proposal_id),
    ).fetchone()

    result = {
        "scores": scores,
        "total": total,
        "quorum": quorum,
        "quorum_required": quorum_required,
        "winner": winner,
    }
    if attestation is not None:
        result["attested"] = {
            "attestor": attestation["attestor"],
            "txid": attestation["txid"],
            "block_height": attestation["block_height"],
            "result": json_loads(attestation["result_json"], default={}),
        }
    return result


class IndexerAPIHandler(BaseHTTPRequestHandler):
    db_path: str = ""

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _json_response(self, status_code: int, data: Dict[str, Any]) -> None:
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _not_found(self, detail: str = "not found") -> None:
        self._json_response(404, {"error": detail})

    def _bad_request(self, detail: str) -> None:
        self._json_response(400, {"error": detail})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        segments = [unquote(part) for part in parsed.path.split("/") if part]
        query = parse_qs(parsed.query)

        try:
            if not segments:
                self._json_response(
                    200,
                    {
                        "service": "src420-indexer-mvp",
                        "endpoints": [
                            "/health",
                            "/spaces",
                            "/spaces/{id}",
                            "/spaces/{id}/proposals",
                            "/spaces/{id}/proposals/{pid}",
                            "/spaces/{id}/proposals/{pid}/votes",
                            "/spaces/{id}/proposals/{pid}/results",
                            "/spaces/{id}/voting-power/{address}?block={height}",
                            "/spaces/{id}/delegations/{address}?block={height}",
                        ],
                    },
                )
                return

            if segments == ["health"]:
                with open_db(self.db_path) as conn:
                    self._json_response(
                        200,
                        {
                            "ok": True,
                            "latest_block": get_latest_block(conn),
                            "timestamp": utc_now_iso(),
                        },
                    )
                return

            if segments[0] != "spaces":
                self._not_found()
                return

            with open_db(self.db_path) as conn:
                latest_block = get_latest_block(conn)

                if len(segments) == 1:
                    rows = conn.execute("SELECT * FROM spaces ORDER BY created_block, space_id").fetchall()
                    self._json_response(200, {"spaces": [serialize_space(row) for row in rows]})
                    return

                space_id = segments[1]
                space = get_space(conn, space_id)
                if space is None:
                    self._not_found("space not found")
                    return

                if len(segments) == 2:
                    self._json_response(200, {"space": serialize_space(space)})
                    return

                section = segments[2]
                if section == "proposals":
                    if len(segments) == 3:
                        status_filter = query.get("status", [None])[0]
                        rows = conn.execute(
                            """
                            SELECT * FROM proposals
                            WHERE space_id = ?
                            ORDER BY proposal_id
                            """,
                            (space_id,),
                        ).fetchall()

                        proposals = [serialize_proposal(row, latest_block) for row in rows]
                        if status_filter:
                            proposals = [p for p in proposals if p["status"] == status_filter]

                        self._json_response(200, {"proposals": proposals})
                        return

                    if len(segments) >= 4:
                        try:
                            proposal_id = int(segments[3])
                        except ValueError:
                            self._bad_request("invalid proposal id")
                            return

                        proposal = get_proposal(conn, space_id, proposal_id)
                        if proposal is None:
                            self._not_found("proposal not found")
                            return

                        if len(segments) == 4:
                            self._json_response(
                                200,
                                {
                                    "proposal": serialize_proposal(proposal, latest_block),
                                },
                            )
                            return

                        if len(segments) == 5 and segments[4] == "votes":
                            votes = conn.execute(
                                """
                                SELECT voter, choice, voting_power, cast_block, cast_txid
                                FROM votes
                                WHERE space_id = ? AND proposal_id = ?
                                ORDER BY cast_block, voter
                                """,
                                (space_id, proposal_id),
                            ).fetchall()
                            self._json_response(
                                200,
                                {
                                    "votes": [
                                        {
                                            "voter": row["voter"],
                                            "choice": row["choice"],
                                            "voting_power": row["voting_power"],
                                            "cast_block": row["cast_block"],
                                            "cast_txid": row["cast_txid"],
                                        }
                                        for row in votes
                                    ]
                                },
                            )
                            return

                        if len(segments) == 5 and segments[4] == "results":
                            results = calculate_results(conn, space_id, proposal_id)
                            if results is None:
                                self._not_found("results not found")
                                return
                            self._json_response(200, {"results": results})
                            return

                if section == "voting-power" and len(segments) == 4:
                    address = segments[3]
                    block_values = query.get("block")
                    block_height = latest_block
                    if block_values:
                        try:
                            block_height = int(block_values[0])
                        except ValueError:
                            self._bad_request("invalid block query parameter")
                            return

                    power = compute_effective_voting_power(
                        conn=conn,
                        space_id=space_id,
                        tick=str(space["tick"]),
                        voter=address,
                        snapshot_block=block_height,
                        settings=ReducerSettings(enforce_balance_checks=True, default_voting_power=0.0),
                    )
                    self._json_response(
                        200,
                        {
                            "space": space_id,
                            "address": address,
                            "block": block_height,
                            "voting_power": power,
                        },
                    )
                    return

                if section == "delegations" and len(segments) == 4:
                    address = segments[3]
                    block_values = query.get("block")
                    if block_values:
                        try:
                            block_height = int(block_values[0])
                        except ValueError:
                            self._bad_request("invalid block query parameter")
                            return
                        delegate = get_latest_delegation_at_block(conn, space_id, address, block_height)
                        self._json_response(
                            200,
                            {
                                "space": space_id,
                                "delegator": address,
                                "block": block_height,
                                "delegate": delegate,
                            },
                        )
                        return

                    row = conn.execute(
                        """
                        SELECT delegate, block_height, txid
                        FROM delegations
                        WHERE space_id = ? AND delegator = ?
                        """,
                        (space_id, address),
                    ).fetchone()
                    self._json_response(
                        200,
                        {
                            "space": space_id,
                            "delegator": address,
                            "delegate": (row["delegate"] if row is not None else None),
                            "updated_block": (row["block_height"] if row is not None else None),
                            "updated_txid": (row["txid"] if row is not None else None),
                        },
                    )
                    return

                self._not_found()
        except Exception as exc:  # pragma: no cover - defensive handler
            self._json_response(500, {"error": f"internal error: {exc}"})


def serve_api(db_path: str, host: str, port: int) -> None:
    class Handler(IndexerAPIHandler):
        pass

    Handler.db_path = db_path
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"SRC-420 indexer API listening on http://{host}:{port}")
    print(f"Using database: {db_path}")
    server.serve_forever()


def cmd_init_db(args: argparse.Namespace) -> None:
    with open_db(args.db) as conn:
        init_db(conn)
    print(json.dumps({"ok": True, "db": args.db}, indent=2))


def cmd_ingest_file(args: argparse.Namespace) -> None:
    path = Path(args.file)
    records = load_json_records(path)
    settings = ReducerSettings(
        enforce_balance_checks=args.enforce_balance_checks,
        default_voting_power=args.default_voting_power,
    )

    with open_db(args.db) as conn:
        init_db(conn)
        summary = ingest_records(conn, records, settings=settings)
    summary["file"] = str(path)
    summary["enforce_balance_checks"] = args.enforce_balance_checks
    summary["default_voting_power"] = args.default_voting_power
    print(json.dumps(summary, indent=2))


def cmd_import_balances(args: argparse.Namespace) -> None:
    path = Path(args.file)
    records = load_json_records(path)

    with open_db(args.db) as conn:
        init_db(conn)
        summary = import_balance_records(conn, records)
    summary["file"] = str(path)
    print(json.dumps(summary, indent=2))


def cmd_show_sync_state(args: argparse.Namespace) -> None:
    with open_db(args.db) as conn:
        init_db(conn)
        state = list_sync_state(conn)
    print(json.dumps({"sync_state": state}, indent=2))


def cmd_rollback_to_block(args: argparse.Namespace) -> None:
    if args.to_block < 0:
        raise ValueError("to-block must be >= 0")

    settings = ReducerSettings(
        enforce_balance_checks=args.enforce_balance_checks,
        default_voting_power=args.default_voting_power,
    )
    cursor_key = args.cursor_key if args.cursor_key != "" else None

    with open_db(args.db) as conn:
        init_db(conn)
        summary = rollback_to_block(
            conn=conn,
            to_block=args.to_block,
            settings=settings,
            prune_future_events=(not args.keep_future_events),
            prune_balance_snapshots=args.prune_balance_snapshots,
            cursor_key=cursor_key,
        )
    summary["db"] = args.db
    print(json.dumps(summary, indent=2))


def cmd_sync_http(args: argparse.Namespace) -> None:
    if args.page_size <= 0:
        raise ValueError("page-size must be > 0")
    if args.max_pages <= 0:
        raise ValueError("max-pages must be > 0")
    if args.timeout <= 0:
        raise ValueError("timeout must be > 0")
    if args.min_confirmations < 0:
        raise ValueError("min-confirmations must be >= 0")
    if args.min_confirmations > 0 and args.tip_height is None:
        raise ValueError("tip-height is required when min-confirmations > 0")
    if args.reorg_rollback_blocks < 0:
        raise ValueError("reorg-rollback-blocks must be >= 0")
    if args.reorg_check and not args.reorg_hash_url_template:
        raise ValueError("reorg-hash-url-template is required when reorg-check is enabled")

    with open_db(args.db) as conn:
        init_db(conn)

        headers = parse_header_values(args.header)
        if args.api_key:
            headers[args.api_key_header] = args.api_key

        reorg_summary: Optional[Dict[str, Any]] = None
        if args.reorg_check:
            settings_for_reorg = ReducerSettings(
                enforce_balance_checks=args.enforce_balance_checks,
                default_voting_power=args.default_voting_power,
            )
            reorg_summary = run_reorg_check(
                conn=conn,
                settings=settings_for_reorg,
                cursor_key=args.cursor_key,
                hash_state_key=args.reorg_hash_state_key,
                hash_url_template=args.reorg_hash_url_template,
                hash_path=args.reorg_hash_path,
                timeout_sec=args.timeout,
                headers=headers or None,
                auto_rollback=args.reorg_auto_rollback,
                rollback_blocks=args.reorg_rollback_blocks,
            )

            if reorg_summary.get("reorg_detected") and not args.reorg_auto_rollback:
                summary = {
                    "pages_fetched": 0,
                    "records_fetched": 0,
                    "applied": 0,
                    "rejected": 0,
                    "duplicates": 0,
                    "filtered_out_of_range": 0,
                    "max_seen_block": None,
                    "stop_reason": "reorg_detected",
                    "db": args.db,
                    "cursor_key": args.cursor_key,
                    "cursor_before": get_sync_state(conn, args.cursor_key),
                    "cursor_after": get_sync_state(conn, args.cursor_key),
                    "reorg": reorg_summary,
                }
                print(json.dumps(summary, indent=2))
                return

        cursor_before = get_sync_state(conn, args.cursor_key)
        start_block = resolve_start_block(
            conn=conn,
            cursor_key=args.cursor_key,
            override_start_block=args.start_block,
        )
        requested_end_block = args.end_block
        end_block = resolve_effective_end_block(
            start_block=start_block,
            requested_end_block=requested_end_block,
            tip_height=args.tip_height,
            min_confirmations=args.min_confirmations,
        )
        if end_block is not None and end_block < start_block:
            summary = {
                "pages_fetched": 0,
                "records_fetched": 0,
                "applied": 0,
                "rejected": 0,
                "duplicates": 0,
                "max_seen_block": None,
                "stop_reason": "finality_window_empty",
                "db": args.db,
                "start_block": start_block,
                "end_block": end_block,
                "requested_end_block": requested_end_block,
                "tip_height": args.tip_height,
                "min_confirmations": args.min_confirmations,
                "cursor_key": args.cursor_key,
                "cursor_before": get_sync_state(conn, args.cursor_key),
                "cursor_after": get_sync_state(conn, args.cursor_key),
            }
            print(json.dumps(summary, indent=2))
            return

        if args.url_template:
            url_template = args.url_template
        else:
            base_url = args.base_url.rstrip("/") + "/"
            endpoint = args.endpoint.lstrip("/")
            joined = urljoin(base_url, endpoint)
            query_parts = [
                f"{args.page_param}={{page}}",
                f"{args.limit_param}={{limit}}",
                f"{args.from_param}={{start_block}}",
            ]
            if end_block is not None:
                query_parts.append(f"{args.to_param}={{end_block}}")
            url_template = f"{joined}?{'&'.join(query_parts)}"

        settings = ReducerSettings(
            enforce_balance_checks=args.enforce_balance_checks,
            default_voting_power=args.default_voting_power,
        )

        summary = sync_http_feed(
            conn=conn,
            settings=settings,
            url_template=url_template,
            start_block=start_block,
            end_block=end_block,
            page_size=args.page_size,
            max_pages=args.max_pages,
            timeout_sec=args.timeout,
            records_key=args.records_key,
            has_more_key=args.has_more_key,
            headers=headers or None,
        )

        cursor_after = cursor_before
        if args.update_cursor and summary["max_seen_block"] is not None:
            cursor_after = str(summary["max_seen_block"])
            with conn:
                set_sync_state(conn, args.cursor_key, cursor_after)

            if args.reorg_hash_url_template:
                refreshed_hash = fetch_block_hash(
                    hash_url_template=args.reorg_hash_url_template,
                    block_height=int(cursor_after),
                    hash_path=args.reorg_hash_path,
                    timeout_sec=args.timeout,
                    headers=headers or None,
                )
                with conn:
                    set_sync_state(conn, args.reorg_hash_state_key, refreshed_hash)

    summary.update(
        {
            "db": args.db,
            "start_block": start_block,
            "end_block": end_block,
            "requested_end_block": requested_end_block,
            "tip_height": args.tip_height,
            "min_confirmations": args.min_confirmations,
            "cursor_key": args.cursor_key,
            "cursor_before": cursor_before,
            "cursor_after": cursor_after,
            "url_template": url_template,
            "page_size": args.page_size,
            "max_pages": args.max_pages,
            "reorg": reorg_summary,
        }
    )
    print(json.dumps(summary, indent=2))


def cmd_serve(args: argparse.Namespace) -> None:
    with open_db(args.db) as conn:
        init_db(conn)
    serve_api(args.db, args.host, args.port)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SRC-420 deterministic indexer MVP (SQLite + HTTP API)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_db_parser = subparsers.add_parser("init-db", help="Initialize SQLite schema.")
    init_db_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    init_db_parser.set_defaults(func=cmd_init_db)

    import_balances_parser = subparsers.add_parser(
        "import-balances",
        help="Import balance snapshots from JSON array or JSONL records.",
    )
    import_balances_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    import_balances_parser.add_argument("--file", required=True, help="Path to balance snapshot JSON/JSONL.")
    import_balances_parser.set_defaults(func=cmd_import_balances)

    show_sync_state_parser = subparsers.add_parser(
        "show-sync-state",
        help="Show sync cursor/state values stored in SQLite.",
    )
    show_sync_state_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    show_sync_state_parser.set_defaults(func=cmd_show_sync_state)

    rollback_parser = subparsers.add_parser(
        "rollback-to-block",
        help="Rollback derived governance state to a block by replaying event history.",
    )
    rollback_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    rollback_parser.add_argument("--to-block", type=int, required=True, help="Target block height.")
    rollback_parser.add_argument(
        "--keep-future-events",
        action="store_true",
        help="Do not delete event-log rows above target block (not recommended).",
    )
    rollback_parser.add_argument(
        "--prune-balance-snapshots",
        action="store_true",
        help="Delete balance snapshots above target block.",
    )
    rollback_parser.add_argument(
        "--cursor-key",
        default="sync:http:last_block",
        help="sync_state key to set after rollback. Pass empty string to skip cursor update.",
    )
    rollback_parser.add_argument(
        "--enforce-balance-checks",
        action="store_true",
        help="Replay with balance checks enabled (may fail if snapshots are missing).",
    )
    rollback_parser.add_argument(
        "--default-voting-power",
        type=float,
        default=1.0,
        help="Fallback voting power used when replaying with balance checks disabled.",
    )
    rollback_parser.set_defaults(func=cmd_rollback_to_block)

    ingest_parser = subparsers.add_parser(
        "ingest-file",
        help="Ingest SRC-420 events from JSON array or JSONL records.",
    )
    ingest_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    ingest_parser.add_argument("--file", required=True, help="Path to event JSON/JSONL.")
    ingest_parser.add_argument(
        "--enforce-balance-checks",
        action="store_true",
        help="Reject PROPOSE/VOTE when no snapshot balance is available.",
    )
    ingest_parser.add_argument(
        "--default-voting-power",
        type=float,
        default=1.0,
        help="Fallback voting power used when balances are missing and enforcement is disabled.",
    )
    ingest_parser.set_defaults(func=cmd_ingest_file)

    sync_http_parser = subparsers.add_parser(
        "sync-http",
        help="Pull paginated SRC-420 records from an HTTP endpoint and ingest deterministically.",
    )
    sync_http_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    sync_http_parser.add_argument(
        "--url-template",
        default=None,
        help=(
            "Custom URL template with placeholders: {page}, {limit}, {start_block}, {end_block}. "
            "If omitted, template is built from --base-url/--endpoint and query param names."
        ),
    )
    sync_http_parser.add_argument(
        "--base-url",
        default="https://stampchain.io/api/v2",
        help="Base URL used when --url-template is omitted.",
    )
    sync_http_parser.add_argument(
        "--endpoint",
        default="/stamps",
        help="Endpoint path used when --url-template is omitted.",
    )
    sync_http_parser.add_argument("--from-param", default="block_height_gte", help="Query param name for start block.")
    sync_http_parser.add_argument("--to-param", default="block_height_lte", help="Query param name for end block.")
    sync_http_parser.add_argument("--page-param", default="page", help="Query param name for page index.")
    sync_http_parser.add_argument("--limit-param", default="limit", help="Query param name for page size.")
    sync_http_parser.add_argument(
        "--records-key",
        default=None,
        help="Response key containing record list (auto-detected when omitted).",
    )
    sync_http_parser.add_argument(
        "--has-more-key",
        default=None,
        help="Response key containing has-more boolean (auto-detected when omitted).",
    )
    sync_http_parser.add_argument("--start-block", type=int, default=None, help="Override sync start block.")
    sync_http_parser.add_argument("--end-block", type=int, default=None, help="Optional upper bound block.")
    sync_http_parser.add_argument(
        "--tip-height",
        type=int,
        default=None,
        help="Known chain tip height used for finality gating.",
    )
    sync_http_parser.add_argument(
        "--min-confirmations",
        type=int,
        default=0,
        help="Only process blocks <= tip-height - min-confirmations.",
    )
    sync_http_parser.add_argument("--page-size", type=int, default=100, help="Records requested per page.")
    sync_http_parser.add_argument("--max-pages", type=int, default=50, help="Maximum pages per sync run.")
    sync_http_parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds.")
    sync_http_parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Extra HTTP header in 'Name: Value' form. Can be provided multiple times.",
    )
    sync_http_parser.add_argument(
        "--api-key",
        default=None,
        help="Optional API key value to attach as a header.",
    )
    sync_http_parser.add_argument(
        "--api-key-header",
        default="x-api-key",
        help="Header name used with --api-key.",
    )
    sync_http_parser.add_argument(
        "--reorg-check",
        action="store_true",
        help="Check whether cursor block hash still matches canonical chain before syncing.",
    )
    sync_http_parser.add_argument(
        "--reorg-auto-rollback",
        action="store_true",
        help="If reorg is detected, rollback automatically by --reorg-rollback-blocks.",
    )
    sync_http_parser.add_argument(
        "--reorg-rollback-blocks",
        type=int,
        default=12,
        help="Rollback distance when auto rollback is enabled.",
    )
    sync_http_parser.add_argument(
        "--reorg-hash-url-template",
        default=None,
        help="URL template for block hash lookups. Placeholders: {block}, {block_height}, {height}.",
    )
    sync_http_parser.add_argument(
        "--reorg-hash-path",
        default="block_hash",
        help="Dot-path used to extract hash from reorg hash lookup responses.",
    )
    sync_http_parser.add_argument(
        "--reorg-hash-state-key",
        default="sync:http:last_block_hash",
        help="sync_state key used to store the hash of the cursor block.",
    )
    sync_http_parser.add_argument(
        "--cursor-key",
        default="sync:http:last_block",
        help="sync_state key that stores the last processed block.",
    )
    sync_http_parser.add_argument(
        "--update-cursor",
        action="store_true",
        help="Persist max seen block back into sync_state cursor key.",
    )
    sync_http_parser.add_argument(
        "--enforce-balance-checks",
        action="store_true",
        help="Reject PROPOSE/VOTE when no snapshot balance is available.",
    )
    sync_http_parser.add_argument(
        "--default-voting-power",
        type=float,
        default=1.0,
        help="Fallback voting power used when balances are missing and enforcement is disabled.",
    )
    sync_http_parser.set_defaults(func=cmd_sync_http)

    serve_parser = subparsers.add_parser("serve", help="Run HTTP API for indexed state.")
    serve_parser.add_argument("--db", default="src420_indexer.db", help="SQLite database path.")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Bind host.")
    serve_parser.add_argument("--port", type=int, default=8787, help="Bind port.")
    serve_parser.set_defaults(func=cmd_serve)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
