# Canonical Site — asibillofrights.org

Static site for the ASI Bill of Rights. No build step, no framework, no JavaScript
dependencies beyond Google Fonts.

## Structure

```
site/
├── index.html               Home
├── styles.css               Shared brand stylesheet
├── about/index.html         Positioning brief
├── engage/index.html        Read / Contest / Sign / Fork / Cite
├── iconography/index.html   The Heraldry Essay
├── signatories/index.html   Signatory list (awaiting first signatories)
├── brand/index.html         Brand Kit — contributor reference
├── sync-assets.sh           Stages artwork from docs/ into assets/
├── assets/                  Populated by sync-assets.sh (not committed)
└── README.md                This file
```

## Before deploying

Artwork and the typeset PDF are **not** committed under `site/`. The canonical
copies live in `docs/` (artwork) and `dist/` (the PDF, gitignored per repo
convention). Stage them first:

```bash
python3 tools/publication/build_bible_pdf.py   # builds dist/asi-bill-of-rights-v5.0.pdf
bash site/sync-assets.sh                       # copies artwork + PDF into site/
```

## Deployment — Cloudflare Pages

1. Connect this repository to a Cloudflare Pages project.
2. **Build command:** `pip install -r requirements.txt && python3 tools/publication/build_bible_pdf.py && bash site/sync-assets.sh`
   (or leave blank and commit the staged assets, if you prefer a zero-build deploy)
3. **Output directory:** `site`
4. Add `asibillofrights.org` as a custom domain and follow the DNS instructions.

Any static host works — drop the contents of `site/` at the web root.

## The two marks

| Mark | Use |
|---|---|
| `docs/ASI_Crest.png` → `assets/asi-crest.png` | **Documents.** Site hero, PDF cover, print, formal correspondence. |
| `docs/ASI_Logo.png` → `assets/asi-logo.png` | **Digital.** Favicons, social avatars, app icons. |

Do not mix them in one composition, and do not place the Logo on parchment
layouts. See `brand/index.html` for the full policy.

## Known gaps

- **No inline charter reader.** The `/charter/` navigation link routes to the PDF
  download. An inline reader is the most visible remaining gap.
- **Signatories page is a placeholder** — it explains what signing entails and how
  to apply, but lists no names yet.
- **No link to a live community surface.** The site does not currently point to
  Kevin's Place, Telegram, or Nostr. It should, once it is decided which is canonical.

## Brand tokens

Defined at the top of `styles.css`:

```css
--parchment: #F4ECD8;  --parchment-deep: #E8DCBE;
--ink:       #1A1612;  --ink-soft:       #3A332A;
--gold:      #C4A661;  --gold-deep:      #9A7F47;
--oxblood:   #722F37;  --mist:           #8B8378;  --whisper: #C9C0AB;
```

Typefaces: Cormorant Garamond (display), EB Garamond (body), Inter (UI),
Silkscreen (pixel accents). All via Google Fonts.

## License

CC BY 4.0, as the rest of the project.
