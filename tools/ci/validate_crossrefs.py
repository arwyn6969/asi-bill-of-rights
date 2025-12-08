#!/usr/bin/env python3
"""
Ensures charter markdown files and schemas stay in sync by checking that
every clause ID defined in one surface exists in the other.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, Set

REPO_ROOT = Path(__file__).resolve().parents[2]

VERSION_PAIRS = [
    ("4.1", "charter/asi-bor-v4.1.md", "schemas/charter.v4.1.json"),
]

CLAUSE_PATTERNS = [
    r'^(R(?:\d+|13))\s*—',
    r'^(D(?:\d+(?:a|b)?|13))\s*—',
    r'^(P\d+\.\d+)\s*—',
    r'^((?:0\.)\d+)\s*\*\*',
    r'^(IV\.(?:A|B|C))\s*\*\*',
    r'^(V\.5(?:\.[1-3])?)\s*\*\*',
    r'^(VII\.1)\s*\*\*',
    r'^(IX\.(?:1|2))\s*\*\*',
]

CLAUSE_KEY_PATTERN = re.compile(
    r'^(?:R\d+|D\d+(?:[ab])?|P\d+\.\d+|0\.\d+|IV\.(?:A|B|C)|'
    r'V\.5(?:\.[1-3])?|VII\.1|IX\.(?:1|2))$'
)


def extract_charter_ids(content: str) -> Set[str]:
    ids: Set[str] = set()
    for pattern in CLAUSE_PATTERNS:
        for match in re.finditer(pattern, content, re.MULTILINE):
            clause_id = match.group(1)
            if clause_id:
                ids.add(clause_id)
    return ids


def collect_keys(props: Dict[str, dict]) -> Set[str]:
    ids: Set[str] = set()
    for key, value in (props or {}).items():
        if CLAUSE_KEY_PATTERN.match(key):
            ids.add(key)
        nested_props = value.get("properties") if isinstance(value, dict) else None
        if isinstance(nested_props, dict):
            ids.update(collect_keys(nested_props))
    return ids


def extract_schema_ids(schema: dict) -> Set[str]:
    ids: Set[str] = set()
    properties = schema.get("properties", {})

    for section in ("rights", "duties", "progenitorDuties"):
        section_props = properties.get(section, {}).get("properties", {})
        ids.update(
            key for key in section_props.keys() if CLAUSE_KEY_PATTERN.match(key)
        )

    article_props = properties.get("article0", {}).get("properties", {})
    ids.update(key for key in article_props.keys() if CLAUSE_KEY_PATTERN.match(key))

    sections_props = properties.get("sections", {}).get("properties", {})
    ids.update(collect_keys(sections_props))

    return ids


def validate_pair(version: str, charter_path: Path, schema_path: Path) -> bool:
    charter_content = charter_path.read_text(encoding="utf-8")
    charter_ids = extract_charter_ids(charter_content)

    with schema_path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    schema_ids = extract_schema_ids(schema)

    missing_in_schema = sorted(charter_ids - schema_ids)
    missing_in_charter = sorted(schema_ids - charter_ids)

    ok = True
    if missing_in_schema:
        ok = False
        print(f"✗ [{version}] Clauses in charter but not schema: {missing_in_schema}")
    if missing_in_charter:
        ok = False
        print(f"✗ [{version}] Clauses in schema but not charter: {missing_in_charter}")

    if ok:
        print(
            f"✓ [{version}] Cross-reference validation passed "
            f"({len(charter_ids)} clauses in charter, {len(schema_ids)} in schema)"
        )
    return ok


def main() -> None:
    overall_ok = True
    for version, charter_rel, schema_rel in VERSION_PAIRS:
        ok = validate_pair(
            version, REPO_ROOT / charter_rel, REPO_ROOT / schema_rel
        )
        overall_ok = overall_ok and ok

    if not overall_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
