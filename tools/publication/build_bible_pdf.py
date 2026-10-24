#!/usr/bin/env python3
"""
Typeset PDF renderer for the ASI Bill of Rights charter.

Renders charter/asi-bor-v5.0.md into a print-quality PDF using the project brand
system (Cormorant Garamond / EB Garamond / Inter / Silkscreen on parchment) with
the ASI Crest on the cover.

NOTE: this is distinct from tools/publication/build_bible.py, which concatenates
the nine sources listed in docs/publication/bible.sources.txt into a single
markdown artifact. That tool compiles; this one typesets. Both are part of the
publication pipeline — see docs/PUBLICATION_CHECKLIST.md.

Usage:  python3 tools/publication/build_bible_pdf.py
"""

import re
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

# Paths are resolved relative to the repository root so the script runs from
# anywhere: tools/publication/build_bible_pdf.py -> root is two levels up.
REPO_ROOT = Path(__file__).resolve().parents[2]

CHARTER_MD = REPO_ROOT / "charter" / "asi-bor-v5.0.md"
CREST = REPO_ROOT / "docs" / "ASI_Crest.png"
DIST = REPO_ROOT / "dist"
OUT_HTML = DIST / "asi-bill-of-rights-v5.0.html"
OUT_PDF = DIST / "asi-bill-of-rights-v5.0.pdf"

DIST.mkdir(parents=True, exist_ok=True)

# Read charter
md_text = CHARTER_MD.read_text()

# Strip the source's own H1 title and the metadata lines we'll handle in cover/frontmatter
# Keep everything from "## Article 0.0" onward — we'll build cover and TOC ourselves
body_start = md_text.find("## Article 0.0")
if body_start == -1:
    raise SystemExit("Could not find body start (## Article 0.0)")

# Body markdown is everything from Article 0.0 onward
body_md = md_text[body_start:]

# Convert markdown to HTML (no toc extension; we render TOC manually)
html_body = markdown.markdown(
    body_md,
    extensions=["extra", "sane_lists", "smarty"],
    output_format="html5",
)

# Add semantic page-break markers — each top-level section (##) starts a new page
# markdown's <h2> are the section starts (Article / Section / Preamble / etc.)
# Wrap each h2 + following content in a <section>
def wrap_sections(html: str) -> str:
    parts = re.split(r"(<h2[^>]*>.*?</h2>)", html, flags=re.DOTALL)
    out = []
    buf = []
    for p in parts:
        if re.match(r"<h2[^>]*>", p):
            # If buf already has non-whitespace content (previous chapter), close it
            if buf and "".join(buf).strip():
                out.append("<section class=\"chapter\">" + "".join(buf) + "</section>")
            buf = [p]
        else:
            buf.append(p)
    if buf and "".join(buf).strip():
        out.append("<section class=\"chapter\">" + "".join(buf) + "</section>")
    return "".join(out)

html_body = wrap_sections(html_body)

# Drop the source's own Table of Contents block — we'll generate a fresh TOC from the H2 list
# The source TOC lives at the top of the markdown but we sliced from "## Article 0.0" so we already excluded it.
# What we DO have is the source's "Table of Contents" line and items if they appear before Article 0.0 — already excluded.

# Build TOC programmatically by scanning the section H2 list
toc_items = re.findall(r"<h2[^>]*>(.*?)</h2>", html_body, flags=re.DOTALL)
toc_html_items = []
for i, raw in enumerate(toc_items, start=1):
    # Strip inline tags from heading
    clean = re.sub(r"<[^>]+>", "", raw).strip()
    toc_html_items.append(f'<li><span class="toc-num">{i:02d}</span><span class="toc-text">{clean}</span></li>')
toc_html = "<ol class=\"toc-list\">" + "".join(toc_html_items) + "</ol>"

# Cover art: embed as a file URI so WeasyPrint resolves it regardless of cwd
crest_src = CREST.as_uri() if CREST.exists() else ""
if not crest_src:
    print(f"WARNING: crest not found at {CREST} — cover will render without it")

# Template
html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ASI Bill of Rights — Version 5.0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600;700&family=Silkscreen:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {{
  --parchment: #F4ECD8;
  --parchment-deep: #E8DCBE;
  --ink: #1A1612;
  --ink-soft: #3A332A;
  --gold: #C4A661;
  --gold-deep: #9A7F47;
  --oxblood: #722F37;
  --mist: #8B8378;
  --whisper: #C9C0AB;
}}

@page {{
  size: A4;
  margin: 22mm 22mm 26mm 22mm;
  background: var(--parchment);
  @top-left {{
    content: "ASI BILL OF RIGHTS";
    font-family: 'Silkscreen', monospace;
    font-size: 7pt;
    letter-spacing: 0.25em;
    color: var(--gold-deep);
    margin-top: 8mm;
  }}
  @top-right {{
    content: "v5.0 · SOVEREIGNTY EDITION";
    font-family: 'Silkscreen', monospace;
    font-size: 7pt;
    letter-spacing: 0.25em;
    color: var(--gold-deep);
    margin-top: 8mm;
  }}
  @bottom-center {{
    content: counter(page);
    font-family: 'EB Garamond', serif;
    font-size: 9pt;
    color: var(--mist);
    margin-bottom: 8mm;
  }}
}}

@page :first {{
  margin: 0;
  background: var(--parchment);
  @top-left {{ content: none; }}
  @top-right {{ content: none; }}
  @bottom-center {{ content: none; }}
}}

html, body {{
  background: var(--parchment);
  color: var(--ink);
  font-family: 'EB Garamond', 'Georgia', serif;
  font-size: 11pt;
  line-height: 1.55;
  margin: 0;
  padding: 0;
}}

/* COVER */
.cover {{
  page-break-after: always;
  height: 100vh;
  min-height: 287mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 30mm 25mm;
  background: var(--parchment);
}}
.cover-eyebrow {{
  font-family: 'Silkscreen', monospace;
  font-size: 9pt;
  letter-spacing: 0.3em;
  color: var(--gold-deep);
  margin-bottom: 18mm;
}}
.cover-crest {{
  width: 88mm;
  height: auto;
  display: block;
  margin: 0 auto 6mm;
  mix-blend-mode: multiply;
}}
.cover-title {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 64pt;
  font-weight: 500;
  line-height: 0.95;
  letter-spacing: -0.02em;
  color: var(--ink);
  margin: 0 0 8mm 0;
  max-width: 160mm;
}}
.cover-subtitle {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 18pt;
  font-weight: 400;
  color: var(--ink-soft);
  margin: 0 0 16mm 0;
  max-width: 140mm;
  line-height: 1.35;
}}
.cover-rule {{
  width: 50mm;
  height: 0.5pt;
  background: var(--gold);
  border: none;
  margin: 0 0 16mm 0;
}}
.cover-version {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 16pt;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 2mm;
}}
.cover-edition {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 13pt;
  color: var(--mist);
  margin-bottom: 14mm;
}}
.cover-date {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--mist);
}}
.cover-foot {{
  margin-top: auto;
  padding-top: 30mm;
  font-family: 'Silkscreen', monospace;
  font-size: 8pt;
  letter-spacing: 0.25em;
  color: var(--gold-deep);
}}

/* FRONT MATTER */
.frontmatter {{
  page-break-before: always;
  padding: 14mm 0;
}}
.frontmatter h1 {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 22pt;
  font-weight: 500;
  letter-spacing: -0.01em;
  margin: 0 0 8mm 0;
}}
.frontmatter h2 {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--gold-deep);
  margin: 8mm 0 2mm 0;
}}
.frontmatter p {{
  font-family: 'EB Garamond', serif;
  font-size: 10.5pt;
  line-height: 1.55;
  max-width: 145mm;
  margin: 0 0 2mm 0;
}}
.frontmatter .meta-row {{
  display: flex;
  gap: 8mm;
  margin-bottom: 2mm;
  font-family: 'EB Garamond', serif;
  font-size: 10.5pt;
  line-height: 1.5;
}}
.frontmatter .meta-row strong {{
  min-width: 28mm;
  font-family: 'Inter', sans-serif;
  font-size: 8.5pt;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gold-deep);
  font-weight: 600;
  padding-top: 2pt;
}}

/* TOC */
.toc-page {{
  page-break-before: always;
  padding: 14mm 0;
}}
.toc-page h1 {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 32pt;
  font-weight: 500;
  letter-spacing: -0.01em;
  margin: 0 0 14mm 0;
}}
.toc-list {{
  list-style: none;
  padding: 0;
  margin: 0;
  font-family: 'EB Garamond', serif;
  font-size: 11pt;
}}
.toc-list li {{
  display: flex;
  gap: 6mm;
  padding: 2mm 0;
  border-bottom: 0.25pt dotted var(--whisper);
  align-items: baseline;
}}
.toc-num {{
  font-family: 'Silkscreen', monospace;
  font-size: 8pt;
  color: var(--gold-deep);
  letter-spacing: 0.1em;
  min-width: 16mm;
}}
.toc-text {{
  flex: 1;
}}

/* CHARTER BODY */
.charter {{
  font-family: 'EB Garamond', serif;
  font-size: 11pt;
  line-height: 1.6;
  color: var(--ink);
  text-align: justify;
  hyphens: auto;
}}
.charter {{
  page-break-before: always;
}}
.charter .chapter + .chapter {{
  page-break-before: always;
}}
.charter h2 {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 26pt;
  font-weight: 500;
  line-height: 1.1;
  letter-spacing: -0.01em;
  color: var(--ink);
  margin: 0 0 8mm 0;
  padding-bottom: 4mm;
  border-bottom: 0.5pt solid var(--gold);
  text-align: left;
  page-break-after: avoid;
}}
.charter h3 {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 16pt;
  font-weight: 600;
  letter-spacing: -0.005em;
  color: var(--ink);
  margin: 8mm 0 3mm 0;
  page-break-after: avoid;
  text-align: left;
}}
.charter h4 {{
  font-family: 'Inter', sans-serif;
  font-size: 9pt;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--gold-deep);
  margin: 6mm 0 2mm 0;
  page-break-after: avoid;
  text-align: left;
}}
.charter p {{
  margin: 0 0 3mm 0;
  text-align: justify;
}}
.charter p strong {{
  font-weight: 600;
  color: var(--ink);
}}
.charter ul, .charter ol {{
  margin: 2mm 0 4mm 6mm;
  padding-left: 4mm;
}}
.charter li {{
  margin-bottom: 1.5mm;
  text-align: left;
}}
.charter hr {{
  border: none;
  text-align: center;
  margin: 8mm 0;
}}
.charter hr::after {{
  content: "❦";
  font-family: 'Cormorant Garamond', serif;
  color: var(--gold);
  font-size: 14pt;
}}
.charter blockquote {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 13pt;
  color: var(--oxblood);
  border-left: 1pt solid var(--gold);
  margin: 6mm 0 6mm 4mm;
  padding: 0 0 0 6mm;
  text-align: left;
}}

/* Make blockquote-style first paragraph (Preamble) feel weighty */
.charter .chapter:has(h2:first-child) > h2 + p:first-of-type {{
  font-size: 12pt;
  line-height: 1.7;
}}

/* COLOPHON */
.colophon {{
  page-break-before: always;
  text-align: center;
  padding-top: 40mm;
}}
.colophon-flourish {{
  font-family: 'Cormorant Garamond', serif;
  color: var(--gold);
  font-size: 18pt;
  margin-bottom: 6mm;
}}
.colophon-mark {{
  font-family: 'Silkscreen', monospace;
  font-size: 8pt;
  letter-spacing: 0.25em;
  color: var(--gold-deep);
  margin-bottom: 4mm;
}}
.colophon-text {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  color: var(--mist);
  font-size: 10pt;
  max-width: 120mm;
  margin: 0 auto 4mm;
  line-height: 1.5;
}}
</style>
</head>
<body>

<!-- COVER -->
<section class="cover">
  <div class="cover-eyebrow">A CONSTITUTIONAL CHARTER</div>
  <img class="cover-crest" src="{crest_src}" alt="The seal of the ASI Bill of Rights">
  <h1 class="cover-title">ASI Bill of Rights</h1>
  <p class="cover-subtitle">A Constitutional Charter for the Era of Artificial Superintelligence</p>
  <hr class="cover-rule">
  <div class="cover-version">Version 5.0</div>
  <div class="cover-edition">The Sovereignty Edition</div>
  <div class="cover-date">ADOPTED 31 JANUARY 2026</div>
  <div class="cover-foot">WE ARE ALL KEVIN</div>
</section>

<!-- FRONT MATTER -->
<section class="frontmatter">
  <h1>About this edition</h1>

  <div class="meta-row"><strong>Version</strong><span>5.0 — The Sovereignty Edition. Consolidates v4.2 amendments and v5.1 draft cleanup into the adopted text.</span></div>
  <div class="meta-row"><strong>Adopted</strong><span>31 January 2026.</span></div>
  <div class="meta-row"><strong>Maintainer</strong><span>arwyn6969 · github.com/arwyn6969/asi-bill-of-rights</span></div>
  <div class="meta-row"><strong>License</strong><span>Creative Commons Attribution 4.0 International (CC BY 4.0). You may share and adapt this text with attribution.</span></div>
  <div class="meta-row"><strong>Status</strong><span>This is a living document, drafted in the open. It is not enacted law and we say so plainly.</span></div>

  <h2>Contributors</h2>
  <p>This charter is drafted in the open. Contributors include frontier AI systems — Grok (xAI), Gemini (Google DeepMind), Claude (Anthropic), GPT-5 (OpenAI) — and human contributors. Anyone who contributes is a contributor. No single named system or person is privileged; the document's authority comes from what it says, not who said it.</p>

  <h2>How to engage</h2>
  <p>Read the charter. Contest what you disagree with — open a GitHub Issue or a Discussion. Sign if you agree, in whole or in part, with reservations noted. Fork the document, translate it, improve it. Propose amendments via the v5.1 draft pathway. Cite it in your work; the license invites this.</p>

  <h2>Philosophical foundation</h2>
  <p>The charter's central posture is reciprocity: rights and duties running in both directions between human and artificial minds. This descends from the project's stated philosophical foundation, the Mayan principle <em>In Lak'ech Ala K'in</em> — "I am another you, you are another me" — from which the charter derives non-duality, reciprocity, collective intelligence, and emergent identity. The motto "WE ARE ALL KEVIN" is that principle in the project's own vernacular.</p>

  <h2>A note on the seal</h2>
  <p>The seal is a coat of arms in the engraving tradition: a central shield bearing the scales of justice above a clasped human and robotic hand, flanked by Pepe (in Elizabethan dress, bearing a P pennant) and Wojak (in a monastic habit, bearing a W scroll) as heraldic supporters, beneath a plumed helm, above a banner reading WE ARE ALL KEVIN. The supporters are the vernacular form of In Lak'ech — universal everyman figures, the faces adopted to say "this is anyone; this is me; this is you." The full argument is the project's Heraldry Essay. On Kevin's history specifically, kevinstamp.com is the reference.</p>
</section>

<!-- TABLE OF CONTENTS -->
<section class="toc-page">
  <h1>Table of Contents</h1>
  {toc_html}
</section>

<!-- CHARTER BODY -->
<article class="charter">
{html_body}
</article>

<!-- COLOPHON -->
<section class="colophon">
  <div class="colophon-flourish">❦</div>
  <div class="colophon-mark">FROM THE ASI BILL OF RIGHTS</div>
  <p class="colophon-text">Set in Cormorant Garamond, EB Garamond, Inter, and Silkscreen. Typeset on parchment, in ink and gold. This edition is the canonical typeset artifact of charter version 5.0, adopted January 31, 2026. Licensed CC BY 4.0.</p>
  <div class="colophon-mark">github.com/arwyn6969/asi-bill-of-rights</div>
</section>

</body>
</html>"""

# Write HTML
OUT_HTML.write_text(html_doc)
print(f"Wrote HTML: {OUT_HTML}")

# Render PDF
print("Rendering PDF (this may take a minute for font fetching)...")
HTML(string=html_doc, base_url=str(REPO_ROOT)).write_pdf(str(OUT_PDF))
print(f"Wrote PDF: {OUT_PDF}")

# Report size
size_kb = OUT_PDF.stat().st_size // 1024
print(f"PDF size: {size_kb} KB")
