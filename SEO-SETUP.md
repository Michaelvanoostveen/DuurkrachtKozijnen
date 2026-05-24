# SEO Setup — Duurkracht Kozijnen

Deze handleiding loopt door alle externe SEO-tools die je éénmalig zelf moet activeren (ze vereisen jouw browser-login en eigenaarschap-verificatie). De code-kant is al volledig voorbereid.

---

## 1. Google Search Console (15 minuten)

GSC laat je zien hoe Google de site indexeert, welke zoekopdrachten clicks opleveren, en waar fouten zitten. Onmisbaar.

### Stap 1.1 — Property aanmaken
1. Ga naar https://search.google.com/search-console
2. Log in met je Google-account (of maak er een aan)
3. Klik **"Property toevoegen"** rechtsboven
4. Kies **"URL-voorvoegsel"** (rechter optie) — eenvoudiger dan domein-verificatie
5. Vul in: `https://duurkrachtkozijnen.vercel.app/` (later vervangen door eigen domein)
6. Klik **"Doorgaan"**

### Stap 1.2 — Verifiëren (HTML-tag methode)
1. In het verificatiescherm kies je **"HTML-tag"**
2. Je krijgt een meta-tag te zien zoals:
   ```html
   <meta name="google-site-verification" content="ABCdef123XYZ..." />
   ```
3. **Kopieer de hele tag** en stuur naar mij — ik plaats hem in `index.html` `<head>`
4. Na deploy klik je op **"Verifiëren"** in GSC

> **Alternatief:** als je weet wat je doet en het eigen domein al koppelt, gebruik dan **DNS-verificatie** (domain property). Dat verifieert alle subdomeinen automatisch.

### Stap 1.3 — Sitemap indienen
1. In GSC-menu links: klik **"Sitemaps"**
2. Vul in: `sitemap.xml` (dus alleen het einde van de URL)
3. Klik **"Indienen"**
4. Google start binnen 24 uur met crawlen

### Stap 1.4 — Eerste week monitoren
- Na 3-7 dagen verschijnen er data in "Prestaties" en "Dekking"
- Check **"Dekking"** voor crawl-fouten
- Check **"Pagina-ervaring"** voor Core Web Vitals

---

## 2. Bing Webmaster Tools (5 minuten)

Bing krijgt ~10% van Nederlandse zoekopdrachten, en ChatGPT/Copilot zoeken via Bing. Dus belangrijk.

1. Ga naar https://www.bing.com/webmasters
2. Log in met Microsoft-account
3. Klik **"Sites toevoegen"** → **"URL-voorvoegsel"**
4. Vul in: `https://duurkrachtkozijnen.vercel.app/`
5. Kies **"Meta-tag"** verificatie
6. Stuur de meta-tag naar mij — ik plaats hem in `index.html`
7. Na deploy verifieer je via Bing dashboard
8. Onder **"Sitemaps"** voeg toe: `https://duurkrachtkozijnen.vercel.app/sitemap.xml`

> **Bonus:** Bing Webmaster Tools heeft een handige optie **"Importeer vanuit Google Search Console"** — bespaart configuratiewerk.

---

## 3. Google Business Profile (10 minuten)

Voor lokale SEO en Google Maps-zichtbaarheid is dit verreweg het belangrijkste — vaak meer impact dan een SEO-website.

1. Ga naar https://business.google.com
2. Zoek of jullie bedrijf al een listing heeft (Duurkracht Kozijnen Hengelo)
3. **Als wel:** claim het bedrijf en verifieer per post (briefkaart met code)
4. **Als niet:** maak een nieuwe listing met:
   - Naam: `Duurkracht Kozijnen B.V.`
   - Categorie: **Aannemer / Bouwbedrijf**
   - Adres: Hassinkweg 1, 7556 BV Hengelo
   - Telefoon: 085 073 1660
   - Website: https://duurkrachtkozijnen.vercel.app/ (of eigen domein)
   - Openingstijden: ma-vr 08:00-17:00
5. Upload **15-20 foto's** uit de `design-assets/images/` folder
6. Vraag tevreden klanten om een **Google review** te plaatsen (de huidige 10 reviews zijn al lovend — bouw uit)

> **Kritiek:** zorg dat de naam, adres en telefoon (NAP) **exact overeenkomen** met wat in de website JSON-LD staat. Anders denkt Google dat het twee verschillende bedrijven zijn.

---

## 4. Eigen domein koppelen (DNS) — optioneel

Zolang je site op `duurkrachtkozijnen.vercel.app` draait werkt alles, maar `www.duurkrachtkozijnen.nl` is professioneler en SEO-beter.

### Vercel-kant
1. Vercel dashboard → Project `duurkrachtkozijnen` → **Settings** → **Domains**
2. Klik **"Add Domain"**
3. Vul in: `duurkrachtkozijnen.nl`
4. Vercel toont je de DNS-records die je moet zetten

### Bij je domeinregistrar (TransIP, Mijndomein, Hostnet, etc.)
1. Log in bij je registrar
2. Ga naar DNS-beheer van `duurkrachtkozijnen.nl`
3. Voeg deze records toe:
   - **A-record:** `@` → `76.76.21.21` (root domain)
   - **CNAME:** `www` → `cname.vercel-dns.com` (www subdomain)
4. Wacht **1-24 uur** voor DNS-propagatie
5. Vercel regelt automatisch het SSL-certificaat

> **Belangrijk:** als de huidige `duurkrachtkozijnen.nl` ergens anders draait (WordPress hosting), gaat die DAN offline. Plan een moment waarop je daadwerkelijk wil overzetten.

### Na DNS-koppeling: update interne URLs
Alle JSON-LD, canonical URLs en sitemap staan al ingesteld op `https://www.duurkrachtkozijnen.nl/`. Zodra DNS werkt, werkt alles automatisch correct.

---

## 5. Andere lokale platforms (optioneel maar waardevol)

### Solvari
Jullie staan al op https://www.solvari.nl/bedrijven-overzicht/duurkracht-kozijnen-bv  
→ Check of het profiel volledig is en foto's heeft

### Slimster
https://slimster.nl/bedrijf/duurkracht-kozijnen/  
→ Idem: profiel up-to-date houden

### Trustoo
https://trustoo.nl/overijssel/enter/kozijnen/duurkracht-kozijnen-bv/  
→ De Trustoo-score (nu 8.0) actief verhogen door reviews te vragen

### Werkspot, KlusOffertes, Bouwoffertes
Als jullie nieuwe leads willen via offerte-aanvragen, registreer dan op deze platforms. Reviews die daar komen zijn ook waardevol voor je hoofdsite-reputatie.

---

## 6. Monitoring & analytics

### Plausible of Google Analytics 4
Op dit moment heeft de site **geen tracking**. Aanrader:
- **Plausible** (privacy-vriendelijk, €9/mnd, geen cookie-banner nodig): https://plausible.io
- **GA4** (gratis, complex, vereist cookie-banner): https://analytics.google.com

Wat je wil tracken:
- Bezoekers per pagina
- Conversie: form-submits, telefoon-clicks, WhatsApp-clicks
- Verkeersbronnen (Google, direct, social)

Laat weten als je deze geïmplementeerd wilt hebben — ik plaats de tracking-code.

---

## 7. Wat is er al geregeld op de site

- ✅ Volledige **JSON-LD structured data** (LocalBusiness, Reviews, FAQ, Services, etc.)
- ✅ **`robots.txt`** met 18 AI-bots expliciet toegestaan
- ✅ **`sitemap.xml`** met alle 31 pagina's
- ✅ **`llms.txt`** met geverifieerde feiten voor AI-tools
- ✅ **Open Graph** + Twitter Card meta tags
- ✅ **Geo meta tags** (geo.region, ICBM)
- ✅ **Canonical URLs** op elke pagina
- ✅ **HTTPS + HSTS** via Vercel
- ✅ **WebP-foto's** met JPG-fallback (34% kleiner)
- ✅ **Mobile-first** responsive design
- ✅ **Core Web Vitals**: LCP <1s, CLS=0 (gemeten)
- ✅ **Skip-link** en ARIA labels voor accessibility

## Volgorde van prioriteit (mijn advies)

1. **Google Business Profile** — meeste lokale impact (#3 hierboven)
2. **Google Search Console** — onmisbaar voor indexatie-monitoring (#1)
3. **Eigen domein koppelen** — professioneel + SEO-voordeel (#4)
4. **Bing Webmaster Tools** — quick win, 10% extra zichtbaarheid (#2)
5. **Analytics installeren** — pas zinvol als er verkeer is (#6)
