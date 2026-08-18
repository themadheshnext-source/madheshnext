# Madhesh Next — working notes

## What went wrong in the last task (12 Aug 2026)

**Publish never completed from the local machine.**

- `~/Documents/MadheshNext/madheshnext-repo` was `git init`-ed and pointed at
  `https://github.com/themadheshnext-source/madheshnext.git`, but the `git add` run was
  interrupted. It left behind `.git/index.lock` and several `.git/objects/**/tmp_obj_*`
  stubs, and the branch `main` still has **no commits**. Every later git command in that
  folder fails with `Unable to create '.git/index.lock': File exists`.
- Because the push failed, the site files reached GitHub only through the web UI — the
  history is a run of "Add files via upload" commits, not real commits from the working
  copy. The local folder and the repo can therefore drift apart silently.
- `madheshnext.org` is live on Vercel from that repo. **`madheshnext.com` is still
  parked on a Squarespace "Coming Soon" page** — the domain has never been pointed at
  the Vercel deployment. Outstanding, separate from this task.

**Fix before the next local push:** delete `madheshnext-repo/.git/index.lock` and the
`tmp_obj_*` files, then `git add -A && git commit` again. Or re-clone the repo fresh —
the local folder has nothing the repo does not already have.

## Required edits — this round (18 Aug 2026)

1. **New logo.** Replace the black stacked wordmark with the new single-line
   *Madhesh Next* wordmark: Poppins SemiBold, navy `#0A2C5A`, with the left half of the
   **x** in *Next* in teal `#009B95` (the chevron). Regenerate the whole asset suite —
   primary, reversed, horizontal, bilingual, lockup, MN mark, favicons, OG image.

2. **Tagline.** *Moving Forward* (ने: अगाडि बढ्दै) becomes the campaign tagline. It sits
   under the wordmark in the horizontal/lockup logos, in the site header beside the
   brand, and in the footer.

3. **One convener, not five.** The five people keep their places but only Sanjog Dev is
   a convener. New roles:

   | Person | Role (EN) | Role (ने) |
   |---|---|---|
   | Prashant Singh | Mentor | मार्गदर्शक |
   | Anil Mahaseth | Public Relations Specialist | जनसम्पर्क विज्ञ |
   | Sanjog Dev | Campaign Convener | अभियान संयोजक |
   | Ajay Pandey | Campaign Strategist | अभियान रणनीतिकार |
   | Bala Krishna | Media Specialist | सञ्चार विज्ञ |

   Bios updated to match — Sanjog Dev's now covers technology, data and digital
   infrastructure **plus** civic organisation, district chapters and community.

4. **`conveners.html` → `team.html`.** The page name, nav label, headings and lede no
   longer work with a single convener. `/conveners` redirects to `/team` in
   `vercel.json` so old links keep working. The "district conveners wanted"
   recruitment section stays — that is still about conveners.

## Publishing

Vercel builds `site/` from the `main` branch of
`themadheshnext-source/madheshnext` and serves it at madheshnext.org. Pushing to `main`
is the deploy.
