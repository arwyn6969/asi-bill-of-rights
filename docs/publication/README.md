# Publication: “The Bible” (v5.0)

This folder defines a reproducible “Bible” build: a single markdown file that concatenates key project documents in a stable order for PDF/eBook conversion.

## Build

From repo root:

```bash
python3 tools/publication/build_bible.py
```

Output (default): `dist/asi-bor-bible-v5.0.md` (ignored by git via `.gitignore`).

## Edit the included documents

Update `docs/publication/bible.sources.txt` (one file path per line, relative to repo root).

