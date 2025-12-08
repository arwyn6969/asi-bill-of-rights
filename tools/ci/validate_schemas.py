#!/usr/bin/env python3
"""
Validates charter schemas and contribution metadata to mirror the CI workflow.
Run locally before opening a PR to catch issues the schema-validation
GitHub Action would flag.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError as exc:  # pragma: no cover - dependency hint for local runs
    print("✗ jsonschema is required. Install with `pip install jsonschema`.")
    raise SystemExit(1) from exc

REPO_ROOT = Path(__file__).resolve().parents[2]

SCHEMAS = [
    ("schemas/charter.v4.1.json", True),
    ("schemas/charter.v4.json", True),
    ("schemas/charter.v3.json", False),
]


def validate_schema(path: Path, enforce_required: bool) -> None:
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)

    Draft7Validator.check_schema(schema)
    print(f"✓ {path} is valid JSON Schema Draft 7")

    if enforce_required:
        required_fields = ["metadata", "article0", "rights", "duties"]
        properties = schema.get("properties", {})
        missing = [field for field in required_fields if field not in properties]
        if missing:
            raise SystemExit(
                f"✗ {path} missing required top-level fields: {', '.join(missing)}"
            )
        print(f"✓ {path} includes required fields: {', '.join(required_fields)}")


def validate_contributions(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if "contributions" not in data or "statistics" not in data:
        raise SystemExit("✗ contributions.json missing `contributions` or `statistics`")

    contributions = data["contributions"]
    stats_total = data["statistics"].get("total_contributions")

    if stats_total != len(contributions):
        raise SystemExit(
            f"✗ contributions.json mismatch: {len(contributions)} entries "
            f"but statistics.total_contributions={stats_total}"
        )

    print(
        f"✓ contributions.json structure valid ({len(contributions)} contributions tracked)"
    )


def main() -> None:
    for rel_path, enforce_required in SCHEMAS:
        validate_schema(REPO_ROOT / rel_path, enforce_required)

    validate_contributions(REPO_ROOT / "contributions" / "contributions.json")
    print("✓ Schema validation completed successfully")


if __name__ == "__main__":
    main()
