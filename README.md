# Madhesh Next

Website for **Madhesh Next**, a citizen-led, non-partisan campaign to move public
discourse in Madhesh from politics to economy.

Live at **[madheshnext.org](https://madheshnext.org)**

## What is in this repo

- `site/` — the deployable website. This is the Vercel root directory.
- `build.py` — the static site generator. Run `python3 build.py` to rebuild `site/`
- `data.py` — all 8 districts and all 136 local governments, in English and Nepali
- `makelogo.py` — regenerates the whole logo suite: SVGs with the type converted to
  outlines, plus the PNG and favicon exports
- `assets/` — the stylesheet, the JavaScript and the logo sources
- `brand.html` — the brand sheet. Open it in a browser.
- `NOTES.md` — working notes: what broke in the last publish, what changed since

## The site

Bilingual, English and Nepali, with a language toggle in the header. Sixteen pages
covering the founding argument, the 2030–2050 vision, the four campaign modules, all
8 districts of Madhesh Province, all 136 local governments, the team, media, and a
join form.

No frameworks, no build tools, no database. Plain HTML, one stylesheet, one small script.

## Brand

The wordmark is **Poppins SemiBold** converted to outlines, in navy `#0A2C5A`, with the
**left half of the x in "Next" in teal `#009B95`** — a forward chevron, and the only
colour in the mark. The tagline is **Moving Forward** (ने: अगाडि बढ्दै).

| File in `assets/logo/` | Use |
|---|---|
| `madheshnext-logo.svg` | Primary. Site header, documents, anything on white. |
| `madheshnext-logo-reversed.svg` | White version for dark backgrounds. |
| `madheshnext-logo-horizontal.svg` | Wordmark + tagline. Banners, signatures, letterheads. |
| `madheshnext-logo-tagline-reversed.svg` | The same, reversed. |
| `madheshnext-logo-bilingual.svg` | With मधेश नेक्स्ट under a teal rule. |
| `madheshnext-lockup.svg` | Masthead lockup with "Madhesh 2030 · 2040 · 2050". |
| `madheshnext-mark.svg` | MN monogram block. Avatars, social profiles. |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Browser and phone icons. |
| `og-image.png` | 1200×630 social share card. |

Never re-set the type by hand — the SVGs are final. To change the wording, the colours or
the tagline, run `makelogo.py`; the fonts it needs are listed in its docstring.

The pages themselves stay on the near-black-on-white editorial palette; navy and teal
appear in the logo, the monogram blocks and the role labels only. All tokens live in the
`:root` block of `assets/style.css`.

## The team

Only one person is a convener. The rest hold named roles.

| Person | Role |
|---|---|
| Prashant Singh | Mentor |
| Anil Mahaseth | Public Relations Specialist |
| Sanjog Dev | Campaign Convener |
| Ajay Pandey | Campaign Strategist |
| Bala Krishna | Media Specialist |

Edit `TEAM` in `data.py` to change names, roles, Nepali spellings or bios, then rebuild.
The page is `team.html`; `/conveners` and `/conveners.html` redirect to `/team` via
`site/vercel.json`, which `build.py` writes on every build.

### The four modules

| Module | What it holds |
|---|---|
| **Project** | Time-bound interventions with a defined outcome |
| **Program** | Continuing streams of work across years and districts |
| **Poll** | The listening module — surveys, town halls, citizen questions |
| **Publication** | The knowledge module — data, briefs, the manual |

### Districts covered

| District | Local levels | Headquarters | Population (2021) |
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
municipalities. Figures from Nepal's National Population and Housing Census 2021.

## Rebuilding

```bash
python3 build.py
```

Python 3, no packages required. Everything in `site/` is regenerated.

To correct a municipality name or a population figure, edit `data.py`. To change page
content or structure, edit `build.py`.

## Deployment

Pushes to `main` deploy automatically to Vercel. The Vercel project's root directory is
set to `site`, so only the built website is served.

## Copying

Everything Madhesh Next publishes is free to copy, translate, reprint and argue with.
Attribution is welcome but not required.
