# Duurkracht Kozijnen — projectkennis voor Claude

## Bedrijf
- **Naam:** Duurkracht Kozijnen B.V.
- **Adres:** Hassinkweg 1, 7556 BV Hengelo
- **KvK:** 90895312 · BTW: NL865386488B01
- **Telefoon:** 085 073 1660
- **E-mail:** info@duurkrachtkozijnen.nl
- **Website:** https://www.duurkrachtkozijnen.nl
- **Actief:** heel Nederland, vanuit Hengelo, eigen monteurs
- **Opgericht:** 2003 · 20+ jaar ervaring

## Team
- **Michael van Oostveen** — operationeel directeur (ook gebruiker van deze Claude-sessies)
- **Romin Ahmadi** — commercieel directeur (offertes, inmeting, klantcontact)
- **Ben** — contactpersoon voor terugbellen / leads
- Monteurs: Frits, Johan, Angelo, Anton en anderen

## Product & positionering
- Uitsluitend **Schüco LivIng** kunststof kozijnen op **kunststof stelkozijnen**
- Diensten: raamkozijnen, voordeur, achterdeur, schuifpui, tuindeuren, Keralit gevelbekleding
- Garantie: 10 jaar op materiaal én montage
- Doorlooptijd: gemiddeld 6–8 weken (2× sneller dan marktgemiddelde)
- Keurmerken: KOMO, SKG ★★★ (RC2 inbraakwerend), Schüco LivIng exclusief
- Google Reviews: 4,9 / 5

## Vaste prijzen (all-in, incl. montage, glas, btw)
| Product | Prijs |
|---|---|
| Raamkozijn | € 2.100 per stuk |
| Achterdeur | € 3.800 per stuk |
| Voordeur | € 4.700 per stuk |
| Schuifpui | € 6.400 per stuk |
| Tuindeuren | € 7.200 per stuk |

## Website — technisch
- **Hosting:** Vercel
- **Repo:** https://github.com/Michaelvanoostveen/DuurkrachtKozijnen
- **Type:** Statische HTML-site, geen CMS
- **CSS:** /css/site.css (design system met CSS-variabelen: --green, --orange, --lime, --ink)
- **Fonts:** Fraunces (koppen) + Manrope (body)
- **Analytics:** Google Analytics 4 (G-W45QZ8KED5) — events via /js/tracking.js
- **Heatmaps:** Microsoft Clarity (project ID: xkjrl7c4vw)
- **Deploy:** automatisch bij commit op `main` via GitHub Actions (vercel deploy --prod)
- **Vercel project ID:** prj_VmroHJNqBgMLvcOFPCEztzoAQy3b · org: team_N6hKf8FooSD2zO5MrycFtZmA

## Design-systeem (CSS-variabelen)
```
--green: #0B5A2B    (primaire kleur, headers, knoppen)
--orange / --accent: #E8612C  (CTA-knoppen, highlights)
--lime: #B5D96B     (eyebrow-tekst, accenten)
--ink: #0D1F18      (bodytekst)
--radius: 12px
```

## Sitemap / pagina-overzicht (89 URLs)

### Kernpagina's
- `/` — homepage (hero, kosten-calculator, postcode-check, reviews, contact)
- `/kosten/` — prijspagina met calculator
- `/configurator/` — kozijn-configurator (63 presets, 6 categorieën)
- `/configurator/galerij` — projectgalerij bij configurator (geen trailing slash in sitemap)
- `/offerte-aanvragen/` — uitgebreid offerteformulier
- `/isde-subsidie/` — ISDE-subsidie 2026 (bedragen, voorwaarden, aanvragen)
- `/faq/` — veelgestelde vragen
- `/over-ons/` · `/eigenaren/` · `/contact/` · `/bedankt/` · `/projecten/`
- `/privacybeleid/` · `/voorwaarden/`

### Diensten (6)
- `/diensten/` — overzicht
- `/diensten/kunststof-kozijnen/`
- `/diensten/kunststof-deuren/`
- `/diensten/kunststof-schuifpuien/`
- `/diensten/kunststof-gevelbekleding/`
- `/diensten/montage/`

### Landingspagina's (SEO)
- `/aluminium-vs-kunststof-kozijnen/`
- `/kunststof-voordeur/`
- `/kunststof-kozijnen-antraciet/`
- `/kunststof-kozijnen-vervangen/`

### Blog (/blog/) — 15 artikelen
1. kunststof-kozijnen-kosten
2. hr-plus-plus-of-triple-glas
3. isde-subsidie-kozijnen-2026
4. schueco-living-82-review
5. inbraakwerend-kozijn-rc2-rc3
6. kunststof-kozijnen-onderhoud
7. kunststof-kozijnen-laten-plaatsen
8. kunststof-deuren-kosten
9. schuifpui-of-tuindeuren
10. condens-op-kozijnen
11. geluidwerend-glas-kozijnen
12. compriband-vs-kunststof-stelkozijn-montage
13. kunststof-vs-houten-kozijnen
14. kunststof-kozijnen-kleuren
15. schueco-living-vs-andere-merken

### Locatiepagina's — 50 steden (URL: /kunststof-kozijnen-[stad]/)
**Batch 1 (25 steden, lastmod 2026-06-02):** Hengelo, Enschede, Almelo, Oldenzaal, Borne, Deventer, Zwolle, Apeldoorn, Arnhem, Assen, Emmen, Hoogeveen, Leeuwarden, Heerenveen, Drachten, Lelystad, Almere, Utrecht, Den Haag, Rotterdam, Nijmegen, Groningen, Amsterdam, Eindhoven, Breda

**Batch 2 (25 steden, lastmod 2026-06-11):** Alkmaar, Amstelveen, Alphen aan den Rijn, Capelle aan den IJssel, Delft, Den Helder, Doetinchem, Dordrecht, Ede, Gouda, Haarlem, Heerhugowaard, Hilversum, Hoofddorp, Hoorn, Kampen, Katwijk, Leiden, Purmerend, Rijswijk, Schiedam, Spijkenisse, Vlaardingen, Zaandam, Zoetermeer

### Postcode-check widget (homepage)
25 steden in de LOCATIES-array voor Haversine-afstandsberekening:
Hengelo, Enschede, Almelo, Oldenzaal, Borne, Deventer, Zwolle, Apeldoorn, Arnhem, Assen, Emmen, Hoogeveen, Leeuwarden, Heerenveen, Drachten, Lelystad, Almere, Utrecht, Den Haag, Rotterdam, Nijmegen, Groningen, Amsterdam, Eindhoven, Breda

De PC2-tabel (90 tweecijferige postcodegebieden) maakt volledige NL-dekking mogelijk.

## Blog-automatie
- **Schema:** 1e en 15e van elke maand om 09:17 UTC (11:17 NL zomertijd)
- **Bestand:** `.github/workflows/blog-auto.yml` + `.github/scripts/gen_blog.py`
- **Model:** `claude-opus-4-8`, max_tokens 12.000
- **Werkwijze:** leest bestaande slugs + eerste 2 posts als HTML-referentie, genereert nieuw onderwerp (900+ woorden, prijzen, JSON-LD, GA4, Clarity, CTA's), past blog/index.html en sitemap.xml automatisch bij, commit + Vercel deploy
- **Secrets:** `ANTHROPIC_API_KEY`, `VERCEL_TOKEN`
- **Michael heeft permanente toestemming gegeven voor dit proces**

## JavaScript-bestanden
- `/js/exit-intent.js` — exit-intent popup (eenmalig per sessie via sessionStorage). Desktop: muisverlating boven viewport. Mobiel: na 50 seconden. Toont telefooninvoer + "Ben belt u terug" → WhatsApp `wa.me/31850731660`. Niet op /bedankt/, /contact/, /offerte/ pagina's.
- `/js/tracking.js` — GA4 events: `phone_call` (tel:-links), `whatsapp_click` (wa.me-links), `generate_lead` (Formspree submit). Injecteert `.wa-float` WhatsApp-knop in body. Vult `.topbar .live` met "Nu open/gesloten" (ma–vr 08:00–17:00, Europe/Amsterdam). Regelt mobiele nav-toggle.

## Homepage-secties (index.html)
Topbar → Hero (met 2 inline reviews) → Trust-badges (KOMO, SKG, Schüco, garantie, rating) → USP-marquee → Stats → Diensten (5 cards) → Partners → Werkwijze → **Tools-widget** (Kosten-calculator + Postcode-check, tabbed) → Projecten → Reviews (6 Google-reviews) → Werkgebied → FAQ → CTA-banner → Contact (Formspree) → Mobile sticky CTA

## Lead generatie
- **Exit-intent popup** — zie /js/exit-intent.js
- **Hero reviews** — 2 Google-citaten direct onder CTA-knoppen
- **Calculator WhatsApp CTA** — groene WhatsApp-knop naast "Offerte aanvragen" (homepage + kosten)
- **Postcode → terugbelformulier** — na positief postcode-resultaat: telefooninvoer + "Ben belt terug" WhatsApp-knop
- **Bedankt-pagina** — "Ben belt u binnen 4 uur terug"
- **Offerte-aanvragen pagina** — `/offerte-aanvragen/` — uitgebreide funnel

## Schema.org JSON-LD — aanwezig op alle pagina's
- Homepage: LocalBusiness + Organization + ServiceCatalogue + FAQPage (8 Q&A's) + BreadcrumbList + AggregateRating
- Blogposts: Article + BreadcrumbList + FAQPage (≥4 Q&A's)
- Locatiepagina's: LocalBusiness + BreadcrumbList
- Dienstpagina's: Service + BreadcrumbList

## Hulpscripts (Python, alleen lokaal / build-tijd)
- `build_location_pages.py` — bulk locatiepagina-generator
- `build_blog.py` — bulk blog-generator
- `build_service_pages.py` — bulk dienstpagina-generator
- `build_picture_tags.py` — picture/srcset tag-generator

## Overige bestanden
- `llms.txt` — AI/LLM hints-bestand (expliciet geserveerd voor AI-retrievaltools)
- `docs/algemene-voorwaarden-dkk-2026.pdf` — PDF versie algemene voorwaarden
- `brochure-duurkracht-kozijnen.html` — print-geoptimaliseerde A4 HTML-brochure (niet in sitemap)
- `CLAUDE_HANDOFF.md` — uitgebreid sessie-handoff document
- `vercel.json` — Vercel deployment config (rewrites/redirects)
- `robots.txt` — staat alle grote AI-bots toe (GPTBot, ClaudeBot, Perplexity, etc.); blokkeert SEO-scrapers (Semrush, Ahrefs)

## Werkwijze & afspraken
- Directe implementatie zonder lang overleg
- Alle prijzen zijn vaste all-in prijzen (geen verborgen kosten)
- Alle HTML-bestanden hebben Google Analytics (G-W45QZ8KED5) + Microsoft Clarity (xkjrl7c4vw)
- Schema.org JSON-LD op alle pagina's (zie boven)
- Sitemap.xml bijhouden bij nieuwe pagina's
- Feature branches mergen naar `main` — Vercel deployt automatisch

## Openstaande punten / toekomstige ideeën
- Google Ads / retargeting campagne (nog niet opgepakt)
- WhatsApp als primaire CTA testen op mobiel
