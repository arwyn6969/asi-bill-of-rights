#!/usr/bin/env python3
"""
Runs the local validation helpers that mirror GitHub Actions checks.

Checks:
  1) Internal markdown link targets (tracked files only)
  2) Charter/schema cross-references
  3) Schema validation (optional; requires jsonschema)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_check(label: str, args: list[str]) -> bool:
    print(f"\n=== {label} ===", flush=True)
    try:
        subprocess.run(args, cwd=REPO_ROOT, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def has_jsonschema() -> bool:
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        return False
    return True


def main() -> None:
    overall_ok = True

    overall_ok &= run_check(
        "Internal Links",
        [sys.executable, str(REPO_ROOT / "tools" / "ci" / "validate_internal_links.py")],
    )

    overall_ok &= run_check(
        "Cross-References",
        [sys.executable, str(REPO_ROOT / "tools" / "ci" / "validate_crossrefs.py")],
    )

    if has_jsonschema():
        overall_ok &= run_check(
            "Schemas",
            [sys.executable, str(REPO_ROOT / "tools" / "ci" / "validate_schemas.py")],
        )
    else:
        print("\n=== Schemas ===")
        print("⚠️  Skipping schema validation (missing dependency: jsonschema).")
        print("   Install once: pip install jsonschema")

    if not overall_ok:
        raise SystemExit(1)

    print("\n✓ All runnable checks passed")


if __name__ == "__main__":
    main()
