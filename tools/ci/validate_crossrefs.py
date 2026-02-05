#!/usr/bin/env python3
"""
Ensures charter markdown files and schemas stay in sync by checking that
every clause ID defined in one surface exists in the other.

Notes:
- v4.1/v4.2 schemas are treated as full structural mirrors (exact match).
- v5.0 schema is treated as a partial machine-readable coverage layer, so we
  validate that every clause ID present in the schema exists in the charter.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

VERSION_PAIRS = [
    ("4.1", "charter/asi-bor-v4.1.md", "schemas/charter.v4.1.json", "exact"),
    ("4.2", "charter/asi-bor-v4.2.md", "schemas/charter.v4.2.json", "exact"),
    ("5.0", "charter/asi-bor-v5.0.md", "schemas/charter.v5.0.json", "subset"),
]

CLAUSE_KEY_PATTERN = re.compile(
    r"^(?:"
    r"R\d+|"
    r"D\d+(?:[ab])?|"
    r"P\d+\.\d+|"
    r"0\.\d+(?:\.\d+)?|"
    r"II\.(?:1|2)|"
    r"IV\.(?:A|B|C)|"
    r"V\.5(?:\.[1-3])?|"
    r"VII\.1|"
    r"IX\.(?:1|2|3|4)|"
    r"XI\.(?:1|2|3|4)"
    r")$"
)

CLAUSE_PATTERNS = [
    re.compile(r"^(R\d+)\s*—", re.MULTILINE),
    re.compile(r"^(D\d+(?:a|b)?)\s*—", re.MULTILINE),
    re.compile(r"^(P\d+\.\d+)\s*—", re.MULTILINE),
    re.compile(r"^(0\.\d+(?:\.\d+)?)\s*\*\*", re.MULTILINE),
    re.compile(r"^\*\*(0\.\d+(?:\.\d+)?)\b", re.MULTILINE),
    re.compile(
        r"^((?:II|IV|V|VII|IX|XI)\.(?:\d+|[A-Z])(?:\.\d+)*)\s*\*\*",
        re.MULTILINE,
    ),
    re.compile(
        r"^\*\*((?:II|IV|V|VII|IX|XI)\.(?:\d+|[A-Z])(?:\.\d+)*)\b",
        re.MULTILINE,
    ),
    # Some clause IDs are introduced as markdown headings without bold (e.g., 0.0.1).
    re.compile(r"^###\s*([A-Z0-9]+\.[0-9A-Z.]+)\b", re.MULTILINE),
]


def extract_charter_ids(content: str) -> Set[str]:
    ids: Set[str] = set()
    for pattern in CLAUSE_PATTERNS:
        for match in pattern.finditer(content):
            clause_id = match.group(1)
            if clause_id and CLAUSE_KEY_PATTERN.match(clause_id):
                ids.add(clause_id)
    return ids


def collect_schema_ids(schema: dict) -> Set[str]:
    ids: Set[str] = set()

    def walk(node: object) -> None:
        if not isinstance(node, dict):
            return

        props = node.get("properties")
        if isinstance(props, dict):
            for key, value in props.items():
                if CLAUSE_KEY_PATTERN.match(key):
                    ids.add(key)
                walk(value)

    walk(schema)
    return ids


def diff_summary(
    missing_in_schema: Iterable[str], missing_in_charter: Iterable[str]
) -> Tuple[bool, str]:
    missing_in_schema = sorted(missing_in_schema)
    missing_in_charter = sorted(missing_in_charter)

    ok = True
    lines = []
    if missing_in_schema:
        ok = False
        lines.append(f"✗ Clauses in charter but not schema: {missing_in_schema}")
    if missing_in_charter:
        ok = False
        lines.append(f"✗ Clauses in schema but not charter: {missing_in_charter}")

    return ok, "\n".join(lines)


def validate_pair(
    version: str, charter_path: Path, schema_path: Path, mode: str
) -> bool:
    charter_content = charter_path.read_text(encoding="utf-8")
    charter_ids = extract_charter_ids(charter_content)

    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    schema_ids = collect_schema_ids(schema)

    if mode == "exact":
        missing_in_schema = charter_ids - schema_ids
        missing_in_charter = schema_ids - charter_ids
        ok, details = diff_summary(missing_in_schema, missing_in_charter)
        if not ok:
            print(f"✗ [{version}] Cross-reference validation failed\n{details}")
            return False
        print(
            f"✓ [{version}] Cross-reference validation passed "
            f"({len(charter_ids)} clauses in charter, {len(schema_ids)} in schema)"
        )
        return True

    if mode == "subset":
        missing_in_charter = schema_ids - charter_ids
        ok, details = diff_summary([], missing_in_charter)
        if not ok:
            print(f"✗ [{version}] Schema coverage validation failed\n{details}")
            return False
        print(
            f"✓ [{version}] Schema coverage validation passed "
            f"({len(schema_ids)} schema clauses found in charter)"
        )
        return True

    raise SystemExit(f"Unknown validation mode: {mode!r}")


def main() -> None:
    overall_ok = True
    for version, charter_rel, schema_rel, mode in VERSION_PAIRS:
        ok = validate_pair(
            version, REPO_ROOT / charter_rel, REPO_ROOT / schema_rel, mode
        )
        overall_ok = overall_ok and ok

    if not overall_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
