#!/usr/bin/env bash
# Stage the canonical brand artwork into site/assets/ for deployment.
#
# The originals live in docs/ and are canonical. They are NOT duplicated into
# git under site/assets/ — this script copies them at build/deploy time so
# there is exactly one committed copy of each image in the repository.
#
# Run from the repository root:  bash site/sync-assets.sh
# Or configure it as the Cloudflare Pages build command.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/docs"
DEST="$ROOT/site/assets"

mkdir -p "$DEST"

copy() {
  local from="$SRC/$1" to="$DEST/$2"
  if [[ -f "$from" ]]; then
    cp "$from" "$to"
    echo "  ok  $2"
  else
    echo "  MISSING  $from" >&2
    return 1
  fi
}

echo "Staging brand assets into site/assets/ ..."
copy "ASI_Crest.png"     "asi-crest.png"
copy "ASI_Logo.png"      "asi-logo.png"
copy "THEKEVINSTAMP.png" "kevin-stamp.png"

# The typeset charter PDF, if it has been built.
PDF="$ROOT/dist/asi-bill-of-rights-v5.0.pdf"
if [[ -f "$PDF" ]]; then
  cp "$PDF" "$ROOT/site/asi-bill-of-rights-v5.0.pdf"
  echo "  ok  asi-bill-of-rights-v5.0.pdf"
else
  echo "  note: dist/asi-bill-of-rights-v5.0.pdf not built yet."
  echo "        run: python3 tools/publication/build_bible_pdf.py"
fi

echo "Done."
