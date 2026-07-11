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
- **Hosting:** Vercel (https://duurkrachtkozijnen.nl)
- **Repo:** https://github.com/Michaelvanoostveen/DuurkrachtKozijnen
- **Type:** Statische HTML-site, geen CMS
- **CSS:** /css/site.css (design system met CSS-variabelen: --green, --orange, --lime, --ink)
- **Fonts:** Fraunces (koppen) + Manrope (body)
- **Analytics:** Google Analytics 4 (G-W45QZ8KED5)
- **Heatmaps:** Microsoft Clarity (project ID: xkjrl7c4vw)
- **Deploy:** `vercel deploy --prod --yes`

## Sitemap / pagina-overzicht
- `/` — homepage (hero, calculator, postcode-check, reviews, contact)
- `/diensten/kunststof-kozijnen/` · `/kunststof-deuren/` · `/kunststof-schuifpuien/`
- `/kosten/` — prijspagina met calculator
- `/configurator/` — kozijn-configurator (63 presets, 6 categorieën)
- `/blog/` — 15 blogposts (zie hieronder)
- `/faq/` — veelgestelde vragen
- `/over-ons/` · `/eigenaren/` · `/contact/` · `/bedankt/`
- 25 locatiepagina's: `/kunststof-kozijnen-[stad]/`
- Nieuwe landingspagina's: `/aluminium-vs-kunststof-kozijnen/` · `/kunststof-voordeur/` · `/kunststof-kozijnen-antraciet/`

## Bestaande blogposts (/blog/)
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

## Blog-automatie
- GitHub Actions genereert automatisch een nieuwe SEO-blogpost op de **1e en 15e van elke maand**
- Bestand: `.github/workflows/blog-auto.yml` + `.github/scripts/gen_blog.py`
- Gebruikt model `claude-opus-4-8` via Anthropic API
- Commit & deploy volledig automatisch — geen handmatige actie nodig
- Michael heeft permanente toestemming gegeven voor dit proces

## Lead generatie (geïmplementeerd juli 2026)
- **Exit-intent popup** (`/js/exit-intent.js`): verschijnt bij muisverlating (desktop) of na 50s (mobiel). Tekst: "Ben belt u terug". Opens WhatsApp met prefilled bericht.
- **Hero reviews**: 2 Google-citaten direct onder de CTA-knoppen
- **Calculator WhatsApp CTA**: groene WhatsApp-knop naast "Offerte aanvragen" op homepage en kostenpagina
- **Postcode → terugbelformulier**: na positief postcode-resultaat verschijnt telefooninvoer + "Ben belt terug →" WhatsApp-knop
- **Bedankt-pagina**: "Ben belt u binnen 4 uur terug" (niet meer Romin)

## Design-systeem (CSS-variabelen)
```
--green: #0B5A2B    (primaire kleur, headers, knoppen)
--orange / --accent: #E8612C  (CTA-knoppen, highlights)
--lime: #B5D96B     (eyebrow-tekst, accenten)
--ink: #0D1F18      (bodytekst)
--radius: 12px
```

## Werkwijze & afspraken
- Directe implementatie zonder lang overleg
- Visueel controleren in browser na elke wijziging
- Alle prijzen zijn vaste all-in prijzen (geen verborgen kosten)
- Alle HTML-bestanden hebben Google Analytics + Microsoft Clarity snippets
- Schema.org JSON-LD op alle pagina's (Article, Product, FAQPage, BreadcrumbList)
- Sitemap.xml bijhouden bij nieuwe pagina's

## Openstaande punten / toekomstige ideeën
- Google Ads / retargeting campagne (nog niet opgepakt)
- Kortere offerte-aanvraag (max 4-5 velden, nog controleren)
- WhatsApp als primaire CTA testen op mobiel
