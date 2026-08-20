# madheshnext.org

A bilingual (English / नेपाली) static website for **Madhesh Next** — a citizen-led,
non-partisan campaign to move public discourse in Madhesh from politics to economy.

Modelled on the structure of saptarinext.com, scaled to the whole province:
**8 districts, 136 local governments.**

---

## What's in the box

```
site/                     ← the finished website. Upload this folder.
  index.html              Home
  manifesto.html          "Public discourse must shift to economy" (Prashant Singh)
  vision.html             2030 / 2040 / 2050
  modules.html            Project · Program · Poll · Publication
  districts.html          All 8 districts + searchable table of all 136 local levels
  districts/*.html        One page per district (8)
  conveners.html          The team (Mentor, PR, Convener, Strategist, Media)
  media.html              Publications + press
  join.html               Join / start a chapter (form)
  sitemap.xml, robots.txt, CNAME
  assets/style.css, assets/site.js

  assets/logo/            Logo suite (SVG + PNG), favicons, OG image

build.py                  Site generator (python3 build.py → rebuilds site/)
data.py                   All district + local-level data, and the team list
makelogo.py               Regenerates the logo SVGs (text converted to outlines)
rasterize.py              Regenerates PNG/favicon exports from the SVGs
brand.html                Brand sheet — open in a browser
```

No frameworks, no build tools, no database. Two files of source data, one CSS file,
one small JS file. Anyone can edit it.

---

## Logo

A single-line wordmark set in **Inter ExtraBold**, navy, with the "x" of "Next" split into
two diagonal bars — the rising bar in teal, forming the chevron. All type is converted to
outlines, so the SVGs render identically everywhere with no font to install.

The teal bar is produced by clipping a rotated band to the actual "x" glyph outline, so it
follows the letterform exactly rather than being drawn by hand. Change the wording in
`makelogo.py` and the chevron re-fits itself.

**Brand colour:** navy `#1B3160`, teal `#14A79E`.

| File | Use |
|---|---|
| `madheshnext-logo.svg` | Primary. Navy wordmark, teal chevron. Anything on white. |
| `madheshnext-logo-reversed.svg` | White wordmark, teal chevron. For dark backgrounds. |
| `madheshnext-logo-stacked.svg` | Two-line lockup for narrow or square spaces. |
| `madheshnext-logo-bilingual.svg` | With मधेश नेक्स्ट under a rule. Nepali-language materials. |
| `madheshnext-logo-navy-solid.svg` | Single-colour navy, no teal. Faxes, embroidery, stamps. |
| `madheshnext-logo-black.svg` / `-white.svg` | Single-colour fallbacks. |
| `madheshnext-logo-alt.svg` | Mirror of the primary — teal on the falling bar instead. |
| `madheshnext-mark.svg` | The two-tone X in a navy tile. Avatars, favicons, social profiles. |
| `favicon.svg` / `favicon-32.png` / `apple-touch-icon.png` | Browser and phone icons. |
| `og-image.png` | 1200×630 social share card. |

PNG versions of the wordmarks are in the same folder at 800px wide, transparent background.

**Rules of thumb:** keep clear space of at least the height of the "M" on all sides; never
stretch, recolour, outline or add effects; never re-set the type — use the SVG. On photos,
use the reversed version over a dark area, not the black one.

You almost certainly never need to regenerate these — the SVGs are final. If you do want
to (to change the wording, say), the scripts need the source fonts and a renderer first:

```bash
npm i @fontsource/inter @fontsource/noto-sans-devanagari
pip install fonttools brotli playwright && playwright install chromium
python3 makelogo.py && python3 rasterize.py
```

---

## Colour

The site uses a New York Times editorial palette — near-black on white, hairline rules,
and colour reserved for links only.

| Token | Hex | Use |
|---|---|---|
| Ink | `#121212` | Headlines, body text, buttons, heavy rules |
| Ink 2 | `#333333` | Secondary text, standfirsts |
| Muted | `#666666` | Labels, bylines, captions, table headers |
| Rule | `#E2E2E2` | Hairline dividers |
| Band | `#F7F7F7` | Tinted section background |
| Paper | `#FFFFFF` | Page background |
| Link | `#1B3160` | Links only — brand navy |
| Alert | `#D0021B` | Reserved — deadlines, corrections. Use rarely. |
| Navy | `#1B3160` | Brand — wordmark, links, role labels, avatar tiles |
| Teal | `#14A79E` | Brand — the chevron in the logo. Accent only, never body text. |

Type: **Georgia** for headlines and body (NYT's Cheltenham/Imperial equivalent that needs
no download), **Libre Franklin** for labels, navigation and buttons (close to NYT's
Franklin), **Noto Sans Devanagari** for Nepali. No rounded corners, no shadows, no
gradients anywhere — structure comes from rules and spacing.

All of it lives in the `:root` block at the top of `assets/style.css`. Change a hex there
and it changes everywhere.

---

## The module structure

The site is deliberately modular so it can grow without a redesign:

| Module | What it holds |
|---|---|
| **Project** | Time-bound interventions with a defined outcome |
| **Program** | Continuing streams of work across years and districts |
| **Poll** | The listening module — surveys, town halls, citizen questions |
| **Publication** | The knowledge module — data, briefs, the manual |

Every district chapter runs the same four, so work is comparable across all 8 districts.

---

## Data included

All **136** local governments of Madhesh Province, each with English + Nepali name and type:

| District | Local levels | HQ | Population (2021) |
|---|---|---|---|
| Saptari | 18 | Rajbiraj | 706,255 |
| Siraha | 17 | Siraha | 739,953 |
| Dhanusha | 18 | Janakpurdham | 867,747 |
| Mahottari | 15 | Jaleshwar | 705,838 |
| Sarlahi | 20 | Malangwa | 862,470 |
| Rautahat | 18 | Gaur | 813,573 |
| Bara | 16 | Kalaiya | 743,975 |
| Parsa | 14 | Birgunj | 654,471 |

Totals: 1 metropolitan city, 3 sub-metropolitan cities, 73 municipalities, 59 rural
municipalities. Figures from the National Population & Housing Census 2021 (CBS).

---

## The team

| # | Name | Role |
|---|---|---|
| 1 | Prashant Singh | Mentor |
| 2 | Anil Mahaseth | Public Relations Specialist |
| 3 | Sanjog Dev | Campaign Convener |
| 4 | Ajay Pandey | Campaign Strategist |
| 5 | Bala Krishna | Media Specialist |

There is one Campaign Convener. Edit `TEAM` in `data.py` to change the order, names, Nepali
spellings, roles or bios, then rebuild. The order in that list is the order on the site.

---

## Deployment

The site is **live at [madheshnext.org](https://madheshnext.org)**, hosted on Vercel and
deployed from GitHub.

| Piece | Where |
|---|---|
| Repo | `github.com/themadheshnext-source/madheshnext` |
| Vercel project | team **MadheshNext**, project `madheshnext` |
| Root directory | `site` — only the built website is served |
| Domain | `madheshnext.org`, apex 308-redirects to `www.madheshnext.org` |
| Registrar | Squarespace |

DNS at Squarespace (the Squarespace Defaults preset was removed; the Email Security preset
— DKIM, DMARC, SPF — was left intact):

| Type | Name | Value |
|---|---|---|
| `A` | `@` | `216.198.79.1` |
| `CNAME` | `www` | `c70ad3f4465c8619.vercel-dns-017.com.` |

**To publish a change:** edit, run `python3 build.py`, commit and push to `main`. Vercel
rebuilds automatically. Nothing else to do.

### Still to do

- The **join form is a demo.** Give the `<form>` in `page_join()` an `action` pointing at
  Formspree, Netlify Forms or a Google Form before it collects anything real.
- **Nepali is a working draft.** Worth a read-through by a Maithili or Nepali editor,
  especially `manifesto.html`.
- **madheshnext.com** is still parked at Squarespace and not pointed anywhere.
- No photographs yet. The design leaves room for them.

---

## Rebuilding after an edit

```bash
python3 build.py
```

Requires only Python 3 — no packages. Everything in `site/` is regenerated.

To add a district page section, a new module, or new content: edit `build.py`. To fix a
municipality name or population figure: edit `data.py`.

---

## Language switching

The EN / ने toggle in the header swaps every string on the page. Two mechanisms:

- Short strings: `<span class="t" data-en="..." data-ne="...">`
- Paragraph blocks: `<div data-lang="en">` / `<div data-lang="ne">`

In `build.py` these are the helpers `t(en, ne)` and `blocks(en_html, ne_html)`. The
choice persists across pages. Nepali numerals (१३६) are generated automatically by
`nep()`.

The Nepali translations are a solid working draft — worth a read-through by a Maithili
or Nepali editor before launch, especially the manifesto page.
