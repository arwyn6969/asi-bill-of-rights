# Reconciliation Audit — 28 August 2026

**Status:** Findings and corrections accompanying the branch `feat/public-face-2026-08`.
**Scope:** Nine artifacts produced May–August 2026 for the project's public face, reconciled against the existing repository.
**Author:** Prepared for the maintainer. Nothing in this branch touches `main`.

---

## 1. Why this audit exists

Between May and August 2026 a set of public-facing artifacts was produced for the project — a positioning brief, a voice guide, a heraldry essay, a typeset PDF of the charter, a static website, a brand kit, and steward outreach material.

That work was carried out **without reference to the existing repository documentation.** The repository already contained fifty-five documents plus `docs/press/`, `docs/outreach/`, `docs/strategy/`, and `docs/publication/`, and a substantial amount of what was produced either duplicated existing material or contradicted it.

This audit records what was found, what was corrected, and what remains open. It is included in the branch so the corrections are reviewable alongside the artifacts themselves.

The repository's last commit before this branch was **10 March 2026** (`8bbcfb4`, v5.1 draft charter). No conflicting work landed in the interim.

---

## 2. Three factual errors, corrected

### 2.1 The seal was described incorrectly

Four artifacts stated that the seal features "Kevin centrally, with Pepe and Wojak as heraldic supporters."

`docs/ASI_Crest.png` shows otherwise. The actual seal is a coat of arms in the engraving tradition:

- **Central shield** — the scales of justice above a clasped human and robotic hand
- **Supporters** — Pepe (left) in Elizabethan dress bearing a pennant charged *P*; Wojak (right) in a monastic habit bearing a scroll charged *W*
- **Crest** — a plumed helm
- **Motto banner** — WE ARE ALL KEVIN

Kevin appears as the **motto**, not as the central figure. Corrected in the positioning brief, voice guide, heraldry essay, brand kit, and all site pages. The brand kit and voice guide now carry an explicit rule against the erroneous description.

### 2.2 Kevin's origin was narrated from a conflicting source

The artifacts asserted that Kevin is the figure on Bitcoin Stamp #4258, created by the project maintainer at the launch of stampchain.io and self-replicated into 104 byte-perfect duplicates between #4258 and #18430.

The repository states something different and states it consistently:

| File | Claim |
|---|---|
| `docs/KEVIN.md` | "In February 2023, Mikeinspace created the first Bitcoin Stamp (Stamp 0) in Block 779652. Shortly after, Reinamora137 deployed 'KEVIN' as the **first SRC-20 token** in Block 788041." |
| `docs/KEVIN.md` (Credits) | "**Mikeinspace** — Creator of the Bitcoin Stamps protocol / **Reinamora137** — Developer of the btc_stamps indexer and first SRC-20 deployer" |
| `docs/PHILOSOPHY.md` | "The first SRC-20 token ever deployed was named 'KEVIN' (Block 788041)" |
| `tools/tokenization/chains/bitcoin-stamps/README.md` | "The birthplace of Kevin!—the first SRC-20 token was deployed here in Block 788041." |

The repository never mentions #4258, #18430, or the figure 104. The artifacts never mentioned Reinamora137 or Block 788041.

**Resolution adopted:** the project does not need to adjudicate this, and the artifacts should not have tried. All origin narration has been removed. The artifacts now use only claims both sources agree on — that KEVIN was the first SRC-20 token, that Kevin is "the ghost in the machine," and that the canonical assertion is *I AM A FEATURE, NOT A BUG* — and refer readers to **kevinstamp.com** for history.

The voice guide and brand kit now carry a standing rule: **do not narrate Kevin's origin; cite no stamp numbers, block heights, replication counts, or named creator.**

This audit does not assert which account is correct. `docs/KEVIN.md` is unchanged by this branch. If the maintainer wishes to reconcile the two publicly, that is a separate edit to `docs/KEVIN.md` and is out of scope here.

### 2.3 The project's philosophical foundation was omitted

The positioning brief presented **reciprocity** as the charter's novel posture and derived it purely from constitutional argument. It did not mention In Lak'ech.

The repository is unambiguous on this point:

- `docs/KEVIN.md` opens with *"In Lak'ech Ala K'in"* as its epigraph and states: **"This principle is the philosophical foundation of the ASI Bill of Rights."**
- `docs/PHILOSOPHY.md` devotes a section, "The Deeper Roots: In Lak'ech and Kevin!", to non-duality, reciprocity, collective intelligence, and emergent identity.
- `docs/KEVIN_ASI_MODUS_OPERANDI.md` lists it as a core principle.

This was the most substantive omission of the three. In Lak'ech — *I am another you, you are another me* — **is** reciprocity. Presenting the charter's central thesis without it gave the thesis an invented lineage instead of the real one.

Corrected throughout. The heraldry essay in particular has been rebuilt around it: the argument for Pepe and Wojak as supporters is now that they are the *vernacular form* of In Lak'ech — universal everyman figures, the faces adopted to say "this is anyone; this is me; this is you" — rather than a generic appeal to internet culture. This is a stronger argument and it is the project's own.

---

## 3. The artwork was already in the repository

`docs/ASI_Crest.png` (1024×1024) and `docs/ASI_Logo.png` (1024×1024) have been committed since before this work began. Every "pending canonical artwork" placeholder in the artifacts was waiting on assets that already existed.

Both are now integrated. Per the maintainer's decision, **both marks are retained with distinct roles:**

| Mark | Role |
|---|---|
| **The Crest** (`ASI_Crest.png`) | **Documents.** Bible PDF cover, printed editions, formal correspondence, signatory letters, the canonical site, press materials. Anywhere the project speaks as a charter. |
| **The Logo** (`ASI_Logo.png`) | **Digital.** Social avatars, favicons, app icons, chat-platform identities — contexts needing a bold circular mark legible at small size. |

The two are not interchangeable and should not be mixed in one composition. The Logo should not be placed on parchment layouts; its palette and finish are incompatible with the document system. This policy is recorded in the brand kit.

Copies are staged at `site/assets/` for web use. The originals in `docs/` remain canonical.

Outstanding: a vector (SVG) Crest for large-format print.

---

## 4. Overlap with existing documentation

| New artifact | Existing repo material | Assessment |
|---|---|---|
| Voice guide | `docs/STYLE-GUIDE.md`, `docs/TERMINOLOGY.md` | **Complementary.** The existing guide covers formatting mechanics (Markdown, spelling, date formats, capitalization). The new one covers rhetorical posture and register. They should cross-reference. |
| Positioning brief | `docs/MISSION.md`, `docs/PHILOSOPHY.md`, `docs/PITCH-DECK.md`, `docs/FAQ.md` | **Complementary.** Existing documents are internal statements and a fundraising deck; the brief is a public-facing self-description with named audience tiers. Now aligned with `PHILOSOPHY.md` on In Lak'ech. |
| Heraldry essay | Nothing comparable | **Genuine gap filled.** `KEVIN.md` and `PHILOSOPHY.md` touch on Kevin's symbolism; neither defends the seal at length. |
| PDF renderer | **`tools/publication/build_bible.py` already exists** | **Name collision, different function.** The existing tool concatenates the nine sources in `docs/publication/bible.sources.txt` into one markdown artifact. The new tool typesets the charter into a print-quality PDF via WeasyPrint. No pandoc or typst is used anywhere in the repo. Renamed to `build_bible_pdf.py`; `PUBLICATION_CHECKLIST.md` should gain a second step. |
| Typeset PDF | No PDF in repo | **New.** First typeset artifact the project has had. |
| Static site | `kevins-place/` is a React + FastAPI forum (zones, threads, Telegram auth, Postgres, Docker/Railway/Render) | **No duplication** — different product surface. But the project would then have three web things, and each needs a stated purpose. See §6. |
| Brand kit | Nothing comparable. `docs/UNIFIED-IDENTITY-STRATEGY.md` is a software architecture document despite the name. | **Genuine gap filled.** |
| Steward outreach material | `proposals/OUTREACH-EXPANSION-STRATEGY.md`, `proposals/OUTREACH-QUICK-START.md`, `docs/outreach/*` (all January 2026, internet-native targets, labelled historical) | **Complementary.** The new material is a deliberate pivot to academic and governance audiences. Should note that it supersedes the older email template. |

Status claims in `docs/PROJECT-ALIGNMENT-2026-03-06.md` — SRC-420 pre-deployment, KEVIN's Place a prototype, GCP migration incomplete — were already correctly reflected in the artifacts and remain so.

`charter/asi-bor-v5.1-draft.md` exists. The PDF renders **v5.0**, which remains the adopted text, so this is correct. When v5.1 is adopted, re-run the renderer.

---

## 5. What this branch contains

```
docs/HERALDRY-ESSAY.md                    new — rebuilt around In Lak'ech
docs/POSITIONING-BRIEF.md                 new
docs/VOICE-GUIDE.md                       new — complements STYLE-GUIDE.md
docs/RECONCILIATION-AUDIT-2026-08-28.md   new — this file
docs/outreach/STEWARD-OUTREACH-KIT.md     new — supersedes older email template
docs/outreach/STEWARD-EMAILS-2026.md      new — four drafted approaches
tools/publication/build_bible_pdf.py      new — typeset PDF renderer
dist/asi-bill-of-rights-v5.0.pdf          new — 32-page typeset charter
site/                                     new — static site, 8 pages + assets
```

Nothing existing is modified or deleted.

---

## 6. Open questions for the maintainer

1. **Kevin's origin.** Left unadjudicated by design. If the two accounts should be reconciled in public documentation, `docs/KEVIN.md` is the place, and it is untouched here.

2. **Three web surfaces.** The project would have the static site (public reading), `kevins-place/` (forum prototype), and any deployed Kevin's Place instance. Each needs a one-line statement of purpose, and the static site should link to whichever community surface is live. Currently it does not link to either.

3. **`PUBLICATION_CHECKLIST.md`** should gain a PDF-rendering step after the existing markdown compilation step. Not edited here to avoid touching an existing governance document without approval.

4. **Email addresses.** `STEWARD-EMAILS-2026.md` contains four academic email addresses gathered from public faculty pages. They are public information, but if the maintainer prefers them out of a public repository, they should be stripped before merge.

5. **Charter reader.** The site's `/charter/` navigation link currently routes to the PDF download; there is no inline reader. This is the most visible gap in the site.

6. **Deployment.** The site is not deployed and `asibillofrights.org` is not registered. The site is a static bundle deployable to Cloudflare Pages with no build step.

7. **Merchandise** was in the original remit and has never been revisited. The pre-reset plan was calibrated to a meme-forward strategy that was subsequently abandoned. Recommend holding until stewards are confirmed.

---

*Prepared 28 August 2026. Licensed CC BY 4.0, as the rest of the project.*
