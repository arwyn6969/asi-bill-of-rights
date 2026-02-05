#!/usr/bin/env python3
"""
Validates that internal markdown links in tracked .md files resolve to real files.

This mirrors the internal-file-reference portion of the GitHub Actions link-checker
workflow and intentionally stays simple:
  - Scans markdown links of the form: [text](path)
  - Skips external URLs (http/https/mailto/tel) and pure anchors (#...)
  - Strips querystrings/fragments (e.g., ./file.md#section)
  - Treats root-relative links (/docs/foo.md) as repo-root relative
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:")


def iter_tracked_markdown_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "*.md"], cwd=REPO_ROOT, text=True
    )
    return [REPO_ROOT / line for line in output.splitlines() if line]


def normalize_link(raw_link: str) -> str | None:
    link = raw_link.strip()
    if not link:
        return None
    if link.startswith(EXTERNAL_PREFIXES):
        return None
    if link.startswith("#"):
        return None

    link = link.split("#", 1)[0].split("?", 1)[0].strip()
    if not link:
        return None

    return link


def resolve_target(md_file: Path, link: str) -> Path:
    if link.startswith("/"):
        return REPO_ROOT / link.lstrip("/")
    return md_file.parent / link


def main() -> None:
    errors: list[str] = []

    for md_file in iter_tracked_markdown_files():
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover - best-effort diagnostics
            errors.append(
                f"{md_file.relative_to(REPO_ROOT)} - Error reading file: {exc}"
            )
            continue

        for line_number, line in enumerate(content.splitlines(), 1):
            for match in LINK_PATTERN.finditer(line):
                raw_link = match.group(2)
                link = normalize_link(raw_link)
                if link is None:
                    continue

                target = resolve_target(md_file, link)
                if target.exists():
                    continue

                try:
                    display_target: str | Path = target.relative_to(REPO_ROOT)
                except ValueError:
                    display_target = target

                errors.append(
                    f"{md_file.relative_to(REPO_ROOT)}:{line_number} - "
                    f"Broken link: {raw_link} -> {display_target}"
                )

    if errors:
        print("✗ Found broken internal links:")
        for error in errors:
            print(f"  {error}")
        raise SystemExit(1)

    print("✓ All internal links valid")


if __name__ == "__main__":
    main()

