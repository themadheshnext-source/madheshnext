# Madhesh Next

Website for **Madhesh Next**, a citizen-led, non-partisan campaign to move public
discourse in Madhesh from politics to economy.

Live at **[madheshnext.org](https://madheshnext.org)**

## What is in this repo

- `site/` — the deployable website. This is the Vercel root directory.
- `build.py` — the static site generator. Run `python3 build.py` to rebuild `site/`
- `data.py` — all 8 districts and all 136 local governments, in English and Nepali
- `makelogo.py` — regenerates the logo suite as SVG, with the type converted to outlines
- `rasterize.py` — regenerates the PNG and favicon exports from those SVGs
- `assets/` — the stylesheet, the JavaScript and the logo sources
- `brand.html` — the brand sheet. Open it in a browser.

## The site

Bilingual, English and Nepali, with a language toggle in the header. Sixteen pages
covering the founding argument, the 2030–2050 vision, the four campaign modules, all
8 districts of Madhesh Province, all 136 local governments, the campaign conveners,
media, and a join form.

No frameworks, no build tools, no database. Plain HTML, one stylesheet, one small script.

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
