# Claude Code Handoff - Duurkracht Kozijnen

```yaml
handoff_type: codex_to_claude_code
project: Duurkracht Kozijnen
cwd: /Users/michaelvanoostveen/Duurkracht Kozijnen
date: 2026-05-24
status: deployed_to_vercel_production
live_url_requested: https://duurkracht-kozijnen.vercel.app
live_url_auto_alias: https://duurkrachtkozijnen.vercel.app
deployment_url: https://duurkrachtkozijnen-hoo13o3vd-michaelvanoostveen1985-s-projects.vercel.app
deployment_id: dpl_6czHDLrtvEQ9yHX6GvnmaQVRWHRu
vercel_project: duurkrachtkozijnen
vercel_project_id: prj_VmroHJNqBgMLvcOFPCEztzoAQy3b
vercel_org_id: team_N6hKf8FooSD2zO5MrycFtZmA
```

## Intent

The user asked to continue from the existing Claude Code/Vercel setup and improve the website content for consumer readability. The content should remain technically credible, but not lead with jargon. Main communication strategy now:

- Lead with homeowner outcomes: warmer living, less draft, less noise, less maintenance, clear planning, neat installation.
- Keep technical proof only where useful: A-brand materials, isolating glass, safe hardware, own installers, 10 year warranty.
- Avoid prominent jargon in hero sections, service cards, stats and FAQs unless translated into practical value.

## Work Completed

### Latest visual update - werkwijze steps

The user provided a screenshot of the "Van eerste gesprek tot laatste schroef" process section and asked to make the process steps more graphical with matching photos/images.

Completed:

- Reworked the step cards on `index.html` from icon-only cards into photo-led cards.
- Added matching process visuals:
  - Step 01 Contact & intake: `/design-assets/images/hero-contact.jpeg`
  - Step 02 Adviesgesprek: `/design-assets/images/hero-over-ons.jpeg`
  - Step 03 Inmeting & offerte: `/design-assets/images/kunststof-kozijnen-plaatsen.jpg`
  - Step 04 Productie: `/design-assets/images/Nieuwe-kozijnen-met-deur.jpg`
  - Step 05 Montage & oplevering: `/design-assets/images/Voorkant-huis-kozijnen.jpg`
- Added `.step-visual`, `.step-photo`, `.step-content` styling in both:
  - `index.html` inline CSS
  - `css/site.css`
- Applied the same updated werkwijze markup to reused service pages:
  - `diensten/index.html`
  - `diensten/kunststof-kozijnen/index.html`
  - `diensten/kunststof-deuren/index.html`
  - `diensten/kunststof-schuifpuien/index.html`
  - `diensten/kunststof-gevelbekleding/index.html`
  - `diensten/montage/index.html`
- Browser-checked the homepage section locally at `http://localhost:4173/?steps=visual2#werkwijze`.
- Verified all new process images resolve and all new image tags have alt text.

### Content rewrite

Updated consumer-facing text on:

- `index.html`
- `diensten/index.html`
- `diensten/kunststof-kozijnen/index.html`
- `diensten/kunststof-deuren/index.html`
- `diensten/kunststof-schuifpuien/index.html`
- `diensten/kunststof-gevelbekleding/index.html`
- `diensten/montage/index.html`
- `projecten/index.html`
- `over-ons/index.html`
- `blog/index.html`

Main rewrite pattern:

```text
Before: Schüco LivIng, Uf 0,92, RC2, KOMO, stelkozijn as leading message.
After: less draft, better closing, warmer home, safer feeling, neat delivery, own installers.
Technical terms remain only in specification/proof contexts.
```

### Location pages

Updated `build_location_pages.py` and regenerated all 20 generated location pages:

- `kunststof-kozijnen-hengelo/index.html`
- `kunststof-kozijnen-enschede/index.html`
- `kunststof-kozijnen-almelo/index.html`
- `kunststof-kozijnen-oldenzaal/index.html`
- `kunststof-kozijnen-borne/index.html`
- `kunststof-kozijnen-deventer/index.html`
- `kunststof-kozijnen-zwolle/index.html`
- `kunststof-kozijnen-apeldoorn/index.html`
- `kunststof-kozijnen-arnhem/index.html`
- `kunststof-kozijnen-assen/index.html`
- `kunststof-kozijnen-emmen/index.html`
- `kunststof-kozijnen-hoogeveen/index.html`
- `kunststof-kozijnen-leeuwarden/index.html`
- `kunststof-kozijnen-heerenveen/index.html`
- `kunststof-kozijnen-drachten/index.html`
- `kunststof-kozijnen-lelystad/index.html`
- `kunststof-kozijnen-almere/index.html`
- `kunststof-kozijnen-utrecht/index.html`
- `kunststof-kozijnen-den-haag/index.html`
- `kunststof-kozijnen-rotterdam/index.html`

Generator command used:

```bash
python3 build_location_pages.py
```

### Compatibility route files

The following lightweight redirect/noindex HTML compatibility pages exist as untracked files from the route compatibility work:

- `blog/kosten-kunststof-kozijnen.html`
- `diensten/gevelbekleding.html`
- `diensten/kunststof-deuren.html`
- `diensten/kunststof-kozijnen.html`
- `diensten/montage.html`
- `diensten/schuifpuien.html`

These preserve old `.html` URL compatibility and redirect to the clean current URLs.

### Vercel config

`vercel.json` contains redirect aliases for older service/location paths and cache/security headers. It was already adjusted to support old URLs such as:

- `/diensten/schuifpuien` -> `/diensten/kunststof-schuifpuien`
- `/diensten/gevelbekleding` -> `/diensten/kunststof-gevelbekleding`
- `/locaties/hengelo` -> `/kunststof-kozijnen-hengelo`

## Validation Completed

### Static validation

Active HTML files, excluding `_extracted` and `preview.html`, were checked.

Results:

```yaml
html_files_checked_for_schema_assets_alt: 51
json_ld_parse_errors: 0
missing_local_images: 0
missing_img_alt_attributes: 0

html_files_checked_for_internal_links: 50
missing_internal_links: 0
```

Validation used Node one-liners that:

- parse every `<script type="application/ld+json">`
- verify local `/...` image paths exist
- verify all `<img>` tags have `alt`
- verify internal local links resolve to files, generated directories or `vercel.json` redirects

### Browser/Vercel preview validation

Local Vercel dev server was running at:

```text
http://localhost:4173/
```

Routes checked in browser:

- `/`
- `/diensten/`
- `/diensten/montage/`
- `/kunststof-kozijnen-hengelo/`
- `/projecten/`
- `/blog/`

No browser console errors were found on the checked route.

### Production deploy

Production deploy command used:

```bash
vercel deploy --prod --yes
```

Alias command used:

```bash
vercel alias set duurkrachtkozijnen-hoo13o3vd-michaelvanoostveen1985-s-projects.vercel.app duurkracht-kozijnen.vercel.app
```

Live check:

```bash
curl -I https://duurkracht-kozijnen.vercel.app
```

Result:

```yaml
http_status: 200
server: Vercel
content_type: text/html; charset=utf-8
```

## Current Git State Notes

Expected modified files include:

- `blog/index.html`
- `build_location_pages.py`
- `contact/index.html`
- `diensten/index.html`
- all main service pages under `diensten/*/index.html`
- generated `kunststof-kozijnen-* /index.html` pages
- `index.html`
- `over-ons/index.html`
- `projecten/index.html`
- `vercel.json`

Expected untracked compatibility files:

- `blog/kosten-kunststof-kozijnen.html`
- `diensten/gevelbekleding.html`
- `diensten/kunststof-deuren.html`
- `diensten/kunststof-kozijnen.html`
- `diensten/montage.html`
- `diensten/schuifpuien.html`

Do not delete these unless the user explicitly wants to remove old `.html` compatibility URLs.

## Important Guidance For Next Agent

1. If editing location pages, edit `build_location_pages.py` first, then regenerate pages with `python3 build_location_pages.py`.
2. Keep consumer readability as the default. Avoid making hero sections, cards and FAQs read like product spec sheets.
3. Keep technical differentiation present, but mostly in proof/spec sections.
4. Current product/montage positioning: Duurkracht works only with Schüco LivIng kozijnen and uses kunststof stelkozijnen as the fixed montage basis. Keep this wording consistent; avoid generic "A-merk" as the primary claim.
5. Added SEO blog route: `/blog/compriband-vs-kunststof-stelkozijn-montage/`. Blog index and sitemap have been updated.
6. If deploying again, use the linked Vercel project already present in `.vercel/project.json`.
7. The requested public URL is `https://duurkracht-kozijnen.vercel.app`, but Vercel also has `https://duurkrachtkozijnen.vercel.app`.

## Suggested Next Checks

```bash
git status --short
vercel inspect duurkrachtkozijnen-hoo13o3vd-michaelvanoostveen1985-s-projects.vercel.app
curl -I https://duurkracht-kozijnen.vercel.app
```
