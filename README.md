# Madhesh Next

Website for Madhesh Next, a citizen-led, non-partisan campaign to move public discourse in Madhesh from politics to economy.

Live at madheshnext.org

## What is in this repo

- site/ is the deployable website. This is the Vercel root directory.
- - build.py is the static site generator. Run python3 build.py to rebuild site/
  - - data.py holds all 8 districts and all 136 local governments, in English and Nepali
    - - makelogo.py regenerates the logo suite as SVG with the type converted to outlines
      - - assets/ holds the stylesheet, the JavaScript and the logo sources
       
        - ## The site
       
        - Bilingual, English and Nepali, with a language toggle in the header. Sixteen pages covering the founding argument, the 2030 to 2050 vision, the four campaign modules, all 8 districts of Madhesh Province, all 136 local governments, the campaign conveners, media and a join form.
       
        - No frameworks, no build tools, no database. Plain HTML, one stylesheet, one small script.
       
        - ## Rebuilding
       
        - Run python3 build.py. It needs Python 3 and no packages. Everything in site/ is regenerated.
       
        - ## Copying
       
        - Everything Madhesh Next publishes is free to copy, translate, reprint and argue with. Attribution is welcome but not required.
        - 
