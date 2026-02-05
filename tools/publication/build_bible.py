#!/usr/bin/env python3
"""
Builds a single “Bible” markdown file by concatenating selected repo documents.

Inputs are defined in docs/publication/bible.sources.txt (one path per line).
Output defaults to dist/asi-bor-bible-v5.0.md (git-ignored).
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCES = REPO_ROOT / "docs" / "publication" / "bible.sources.txt"
DEFAULT_OUT = REPO_ROOT / "dist" / "asi-bor-bible-v5.0.md"


def iter_sources(path: Path) -> list[Path]:
    sources: list[Path] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        sources.append(REPO_ROOT / line)
    return sources


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ASI BoR Bible markdown")
    parser.add_argument(
        "--sources",
        type=Path,
        default=DEFAULT_SOURCES,
        help="Path to sources list (default: docs/publication/bible.sources.txt)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Output markdown path (default: dist/asi-bor-bible-v5.0.md)",
    )
    args = parser.parse_args()

    sources = iter_sources(args.sources)
    if not sources:
        raise SystemExit(f"✗ No sources found in {args.sources}")

    missing = [src for src in sources if not src.exists()]
    if missing:
        missing_rel = [str(src.relative_to(REPO_ROOT)) for src in missing]
        raise SystemExit(f"✗ Missing source files: {missing_rel}")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = []
    parts.append("# ASI Bill of Rights — Bible (v5.0)\n")
    parts.append(f"_Generated: {generated_at}_\n")
    parts.append("\n## Included Documents\n")
    for src in sources:
        parts.append(f"- `{src.relative_to(REPO_ROOT)}`\n")
    parts.append("\n---\n")

    for src in sources:
        rel = src.relative_to(REPO_ROOT)
        parts.append(f"\n<!-- BEGIN: {rel} -->\n")
        parts.append(src.read_text(encoding="utf-8").rstrip())
        parts.append(f"\n<!-- END: {rel} -->\n")
        parts.append("\n---\n")

    out_path.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"✓ Wrote {out_path.relative_to(REPO_ROOT)} ({len(sources)} sources)")


if __name__ == "__main__":
    main()

