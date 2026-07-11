#!/usr/bin/env python3
"""
Duurkracht Kozijnen — automatische blogpost generator
Draait via GitHub Actions op de 1e en 15e van elke maand.
"""
import anthropic
import os
import re
import json
from datetime import datetime
from pathlib import Path

TODAY      = datetime.now().strftime("%Y-%m-%d")
TODAY_NL   = datetime.now().strftime("%-d %B %Y").replace(
    "January","januari").replace("February","februari").replace("March","maart").replace(
    "April","april").replace("May","mei").replace("June","juni").replace(
    "July","juli").replace("August","augustus").replace("September","september").replace(
    "October","oktober").replace("November","november").replace("December","december")
YEAR       = datetime.now().strftime("%Y")
BASE_URL   = "https://www.duurkrachtkozijnen.nl"
SITE_DIR   = Path(".")
BLOG_DIR   = SITE_DIR / "blog"

# ── Bestaande slugs verzamelen ──────────────────────────────────────────────
existing_slugs = sorted([
    d.name for d in BLOG_DIR.iterdir()
    if d.is_dir() and (d / "index.html").exists()
])
print(f"Bestaande blogs ({len(existing_slugs)}): {', '.join(existing_slugs)}")

# ── Twee referentie-posts als HTML-template meegeven ────────────────────────
ref_html = ""
for slug in existing_slugs[:2]:
    path = BLOG_DIR / slug / "index.html"
    ref_html += f"\n\n<!-- REFERENTIE: blog/{slug}/index.html -->\n"
    with open(path, encoding="utf-8") as f:
        ref_html += f.read()

# ── Blog-index en sitemap inlezen ───────────────────────────────────────────
with open(BLOG_DIR / "index.html", encoding="utf-8") as f:
    blog_index_html = f.read()

with open(SITE_DIR / "sitemap.xml", encoding="utf-8") as f:
    sitemap_content = f.read()

# ── Prompt ───────────────────────────────────────────────────────────────────
PROMPT = f"""Je bent de content-marketeer van Duurkracht Kozijnen (duurkrachtkozijnen.nl).
Duurkracht is een specialist in kunststof kozijnen, deuren, schuifpuien en Keralit gevelbekleding,
gevestigd in Hengelo, actief in heel Nederland.

════ OPDRACHT ════
Schrijf een NIEUWE, volledig uitgewerkte SEO-blogpost die:
• Een nog niet behandeld onderwerp behandelt (zie de lijst hieronder)
• Exact dezelfde HTML-structuur, CSS-klassen en meta-tags gebruikt als de referentiebestanden
• Minimaal 900 woorden body-tekst heeft
• Interne links heeft naar /kosten/, /contact/, /faq/ en/of relevante dienst-pagina's

════ REEDS BESTAANDE BLOGPOSTS — kies een NIEUW onderwerp ════
{', '.join(existing_slugs)}

════ SUGGESTIES VOOR NIEUW ONDERWERP (kies de meest waardevolle) ════
- kunststof-kozijnen-jaren-70-80-woning       (veelgezochte doelgroep)
- dakkapel-kozijnen-plaatsen                  (niche, hoog zoekvolume)
- energiebesparing-kozijnen-kwh-besparing     (concrete rekentool)
- ventilatie-kozijnen-combinatie              (technisch advies)
- spouwmuurisolatie-kozijnen-tegelijk         (gecombineerde renovatie)
- schuifpui-maten-standaard-gids             (maatgids, koopintentie)
- kozijnen-woning-verkopen-woningwaarde       (woningmarkt-angle)
- kunststof-kozijnen-kleur-houtlook-folie     (productadvies populair kleur)
- kozijnen-plaatsen-zonder-steigers           (praktische vraag)
- nieuwe-voordeur-kiezen-gids                 (beslissingshelper)

════ VASTE PRIJZEN (exact zo gebruiken) ════
Raamkozijn:  € 2.100 per stuk (all-in)
Achterdeur:  € 3.800 per stuk
Voordeur:    € 4.700 per stuk
Schuifpui:   € 6.400 per stuk
Tuindeuren:  € 7.200 per stuk

════ BEDRIJFSGEGEVENS ════
Naam:        Duurkracht Kozijnen B.V.
Adres:       Hassinkweg 1, 7556 BV Hengelo
Telefoon:    085 073 1660
KvK:         90895312
Product:     uitsluitend Schüco LivIng kozijnen op kunststof stelkozijnen
Garantie:    10 jaar op materiaal én montage
GA4-id:      G-W45QZ8KED5
Clarity-id:  xkjrl7c4vw

════ INTERNE PAGINA'S ════
/ · /diensten/kunststof-kozijnen/ · /diensten/kunststof-deuren/
/diensten/kunststof-schuifpuien/ · /kosten/ · /configurator/
/faq/ · /over-ons/ · /contact/ · /blog/

════ HTML-REFERENTIE (gebruik als EXACTE template) ════
{ref_html[:9000]}

════ VERWACHT ANTWOORD-FORMAAT ════
Zet BOVEN de HTML deze regels (elke op eigen regel):

SLUG: [url-slug zonder slash]
TITLE: [volledige paginatitel, max 60 tekens]
DESCRIPTION: [meta description, 140–155 tekens]
CATEGORY: [bijv. Advies & gids · Prijzen · Productadvies · Onderhoud · Werkwijze]
MINUTES: [leestijd in minuten, getal]
IMAGE: [kies uit: hero-raamkozijnen.jpg · Nieuwe-voordeur-huis.jpg · Voorkant-huis-kozijnen.jpg · diensten-deuren.jpg · dienst-schuifpuien.jpeg · eigenaren-duurkracht-kozijnen.jpg]

Daarna de HTML:
HTML_START
<!DOCTYPE html>
...complete HTML...
</html>
HTML_END

Zorg dat de HTML bevat:
1. Google Analytics snippet (GA4, id G-W45QZ8KED5) vlak na <head>
2. Microsoft Clarity snippet (id xkjrl7c4vw) voor </head>
3. Schema.org Article JSON-LD
4. Schema.org BreadcrumbList JSON-LD
5. Schema.org FAQPage JSON-LD (minimaal 4 Q&A's)
6. Canonical URL: {BASE_URL}/blog/[slug]/
7. article:published_time = {TODAY}
8. Key-takeaways blok (groene checklist, .key-takeaways klasse)
9. Inhoudsopgave (.toc zijbalk)
10. CTA-sectie onderaan naar /contact/
11. exit-intent.js script tag voor </body>: <script src="/js/exit-intent.js" defer></script>
"""

# ── API-aanroep ───────────────────────────────────────────────────────────────
print("Anthropic API aanroepen (claude-opus-4-8)...")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=12000,
    messages=[{"role": "user", "content": PROMPT}]
)

text = message.content[0].text
print(f"Antwoord ontvangen: {len(text)} tekens")

# ── Parsen ────────────────────────────────────────────────────────────────────
def extract(pattern, text, default=""):
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else default

slug_val     = extract(r'^SLUG:\s*(.+)$', text)
title_val    = extract(r'^TITLE:\s*(.+)$', text)
desc_val     = extract(r'^DESCRIPTION:\s*(.+)$', text)
cat_val      = extract(r'^CATEGORY:\s*(.+)$', text, "Advies & gids")
minutes_val  = extract(r'^MINUTES:\s*(\d+)', text, "5")
image_val    = extract(r'^IMAGE:\s*(.+)$', text, "Voorkant-huis-kozijnen.jpg")

html_m = re.search(r'HTML_START\s*\n(<!DOCTYPE[\s\S]+?)\nHTML_END', text)
if not html_m:
    html_m = re.search(r'(<!DOCTYPE html>[\s\S]+</html>)', text)
if not html_m:
    raise ValueError(f"Kon HTML niet vinden in antwoord. Begin: {text[:400]}")

html_val = html_m.group(1).strip()

if not slug_val:
    # Probeer slug uit canonical te halen
    slug_m = re.search(r'/blog/([a-z0-9-]+)/', html_val)
    if slug_m:
        slug_val = slug_m.group(1)
    else:
        raise ValueError("Kon slug niet bepalen")

print(f"Slug: {slug_val}")
print(f"Title: {title_val}")

# ── Blog-post wegschrijven ────────────────────────────────────────────────────
post_dir = BLOG_DIR / slug_val
post_dir.mkdir(parents=True, exist_ok=True)
post_path = post_dir / "index.html"

with open(post_path, "w", encoding="utf-8") as f:
    f.write(html_val)
print(f"Geschreven: {post_path}")

# ── blog/index.html bijwerken ─────────────────────────────────────────────────

# 1. JSON-LD blogPost array — voeg nieuwe post toe aan het begin
new_ld_entry = json.dumps({
    "@type": "Article",
    "@id": f"{BASE_URL}/blog/{slug_val}/#article",
    "headline": title_val,
    "datePublished": TODAY
}, ensure_ascii=False)

blog_index_updated = blog_index_html.replace(
    '"blogPost": [',
    f'"blogPost": [{new_ld_entry},'
)

# 2. Blog-card HTML — invoegen als eerste kaart in blog-grid
img_alt = title_val.replace('"', '\'')
short_desc = desc_val[:110] + "..." if len(desc_val) > 110 else desc_val

new_card = (
    f'\n      <a href="/blog/{slug_val}/" class="blog-card">\n'
    f'        <div class="ph"><img src="/design-assets/images/{image_val}" '
    f'alt="{img_alt}" loading="lazy" /></div>\n'
    f'        <div class="body">\n'
    f'          <div class="cat">{cat_val}</div>\n'
    f'          <div class="date"><time datetime="{TODAY}">{TODAY_NL}</time>'
    f' · {minutes_val} min lezen</div>\n'
    f'          <h2>{title_val}</h2>\n'
    f'          <p>{short_desc}</p>\n'
    f'          <span class="read">Lees artikel <span class="arrow">→</span></span>\n'
    f'        </div>\n'
    f'      </a>'
)

blog_index_updated = blog_index_updated.replace(
    '<div class="blog-grid">',
    '<div class="blog-grid">' + new_card,
    1
)

with open(BLOG_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(blog_index_updated)
print("blog/index.html bijgewerkt")

# ── sitemap.xml bijwerken ─────────────────────────────────────────────────────
new_url_entry = (
    f"\n  <url>\n"
    f"    <loc>{BASE_URL}/blog/{slug_val}/</loc>\n"
    f"    <lastmod>{TODAY}</lastmod>\n"
    f"    <changefreq>monthly</changefreq>\n"
    f"    <priority>0.7</priority>\n"
    f"  </url>"
)

sitemap_updated = sitemap_content.replace("</urlset>", new_url_entry + "\n</urlset>")

with open(SITE_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_updated)
print("sitemap.xml bijgewerkt")

print(f"\n✓ Klaar! Nieuwe blog: {BASE_URL}/blog/{slug_val}/")
