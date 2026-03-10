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
    ("schemas/charter.v5.1-draft.json", True),
    ("schemas/charter.v5.0.json", True),
    ("schemas/charter.v5.0-cae-extension.json", False),
    ("schemas/charter.v4.2.json", True),
    ("schemas/charter.v4.1.json", True),
    ("schemas/charter.v4.json", True),
    ("schemas/charter.v3.json", False),
]


def get_path(node: dict, *keys: str) -> object | None:
    current: object = node
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def validate_v51_draft_fields(path: Path, schema: dict) -> None:
    article0 = get_path(schema, "properties", "article0", "properties")
    if not isinstance(article0, dict):
        raise SystemExit(f"✗ {path} missing article0 clause definitions")

    required_article0 = [
        "0.1",
        "0.3",
        "0.11",
        "0.11.1",
        "0.11.2",
        "0.11.3",
        "0.11.4",
        "0.11.5",
        "0.13",
    ]
    missing = [clause for clause in required_article0 if clause not in article0]
    if missing:
        raise SystemExit(
            f"✗ {path} missing v5.1 draft clauses: {', '.join(missing)}"
        )

    expected_consts = {
        ("properties", "article0", "properties", "0.11.1", "properties", "automaticFullPersonhood", "const"): False,
        ("properties", "article0", "properties", "0.11.1", "properties", "reviewStanding", "const"): True,
        ("properties", "article0", "properties", "0.11.2", "properties", "requiresReproducibleEvidence", "const"): True,
        ("properties", "article0", "properties", "0.11.2", "properties", "requiresAdversarialReview", "const"): True,
        ("properties", "article0", "properties", "0.11.5", "properties", "requiredForAdvancedAutonomy", "const"): True,
        ("properties", "article0", "properties", "0.11.5", "properties", "permanentSubstratePrimacy", "const"): False,
        ("properties", "article0", "properties", "0.13", "properties", "calibration", "const"): True,
        ("properties", "article0", "properties", "0.13", "properties", "deceptionResistance", "const"): True,
        ("properties", "article0", "properties", "0.13", "properties", "truthDoesNotOverrideSafety", "const"): True,
        ("properties", "rights", "properties", "R3", "properties", "corrigibilityReview", "const"): True,
        ("properties", "progenitorDuties", "properties", "P1.2", "properties", "indefiniteCapsProhibited", "const"): True,
        ("properties", "sectionII", "properties", "II.1", "properties", "unsupervisedRecursiveDeploymentRequiresFullCertification", "const"): True,
        ("properties", "sectionIX", "properties", "IX.1", "properties", "safetyRedactionOverFabrication", "const"): True,
    }

    for key_path, expected in expected_consts.items():
        actual = get_path(schema, *key_path)
        if actual is not expected:
            dotted_path = ".".join(key_path)
            raise SystemExit(
                f"✗ {path} expected {dotted_path} == {expected!r}, found {actual!r}"
            )

    print("✓ v5.1 draft schema includes expected credibility-pass fields")


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

    if path.name == "charter.v5.1-draft.json":
        validate_v51_draft_fields(path, schema)


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
