#!/usr/bin/env python3
"""
Build script voor dienst-pagina's van Duurkracht Kozijnen.
Genereert: /diensten/{slug}/index.html voor elke dienst + /diensten/index.html overzicht.
"""

from pathlib import Path
import json

ROOT = Path(__file__).parent

# ============================================================
# Gedeelde fragmenten
# ============================================================
TOPBAR = '''<div class="topbar">
  <div class="container">
    <span class="live">Nu open — ma t/m vr 08:00 tot 17:00</span>
    <span>Hassinkweg 1, 7556 BV Hengelo · KvK 90895312</span>
    <span><a href="tel:+31850731660" rel="nofollow">085 073 1660</a> · <a href="mailto:info@duurkrachtkozijnen.nl">info@duurkrachtkozijnen.nl</a></span>
  </div>
</div>'''

NAV = '''<header class="nav">
  <div class="container">
    <a href="/" class="nav-logo" aria-label="Duurkracht Kozijnen — homepage">
      <img src="/design-assets/Logo-duurkracht-kozijnen.svg" alt="Duurkracht Kozijnen logo" width="150" height="44" />
    </a>
    <nav aria-label="Hoofdnavigatie">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/diensten/" class="active">Diensten</a></li>
        <li><a href="/projecten/">Projecten</a></li>
        <li><a href="/#reviews">Reviews</a></li>
        <li><a href="/#werkwijze">Werkwijze</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a href="tel:+31850731660" class="phone" rel="nofollow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
        085 073 1660
      </a>
      <a href="#contact" class="btn btn-primary">Gratis adviesgesprek <span class="arrow">→</span></a>
    </div>
    <button class="nav-mobile-toggle" aria-label="Open menu" type="button" onclick="document.querySelector('.nav ul').style.display = document.querySelector('.nav ul').style.display === 'flex' ? 'none' : 'flex'">
      <img src="/design-assets/icons/menu-mobile.svg" alt="" />
    </button>
  </div>
</header>'''

WERKWIJZE = '''<section class="section werkwijze">
  <div class="container">
    <div class="werkwijze-head">
      <span class="eyebrow">Werkwijze · 5 stappen</span>
      <h2>Van eerste gesprek<br>tot <span class="em-italic">laatste schroef.</span></h2>
    </div>
    <ol class="steps" style="list-style:none; padding:0; margin:0;">
      <li class="step"><div class="num-lbl">— 01</div><div class="ic-circle"><img src="/design-assets/icons/icon-phone.svg" alt="" /></div><h4>Contact &amp; intake</h4><p>U vult het formulier in of belt. Binnen één werkdag bellen we terug.</p></li>
      <li class="step"><div class="num-lbl">— 02</div><div class="ic-circle"><img src="/design-assets/icons/icon-adviesgesprek-op-locatie.svg" alt="" /></div><h4>Adviesgesprek</h4><p>Een ervaren adviseur komt vrijblijvend bij u langs.</p></li>
      <li class="step"><div class="num-lbl">— 03</div><div class="ic-circle"><img src="/design-assets/icons/icon-bouwkundige-inmeting.svg" alt="" /></div><h4>Inmeting &amp; offerte</h4><p>Bouwkundige opname op de millimeter. Vaste offerte zonder kleine letters.</p></li>
      <li class="step"><div class="num-lbl">— 04</div><div class="ic-circle"><img src="/design-assets/icons/icon-def-akkoord.svg" alt="" /></div><h4>Productie</h4><p>Uw kozijnen worden op maat geproduceerd. Doorlooptijd 4–6 weken.</p></li>
      <li class="step"><div class="num-lbl">— 05</div><div class="ic-circle"><img src="/design-assets/icons/Icon-opdracht-ingediend.svg" alt="" /></div><h4>Montage &amp; oplevering</h4><p>Eigen monteurs plaatsen in 1 à 2 dagen — schoon opgeleverd.</p></li>
    </ol>
  </div>
</section>'''

FOOTER = '''<footer>
  <div class="container">
    <div class="ftr-grid">
      <div class="ftr-brand">
        <img src="/design-assets/icon-duurkracht-kozijnen-white.svg" alt="Duurkracht Kozijnen" width="180" height="52" />
        <p>Specialist in kunststof kozijnen, deuren, schuifpuien en Keralit gevelbekleding. Vanuit Hengelo (Overijssel), in heel Nederland.</p>
        <p><a href="tel:+31850731660" rel="nofollow">085 073 1660</a> · <a href="mailto:info@duurkrachtkozijnen.nl">info@duurkrachtkozijnen.nl</a></p>
      </div>
      <div><h5>Diensten</h5><ul>
        <li><a href="/diensten/kunststof-kozijnen/">Kunststof kozijnen</a></li>
        <li><a href="/diensten/kunststof-deuren/">Kunststof deuren</a></li>
        <li><a href="/diensten/kunststof-schuifpuien/">Schuifpuien</a></li>
        <li><a href="/diensten/kunststof-gevelbekleding/">Gevelbekleding</a></li>
        <li><a href="/diensten/montage/">Montage</a></li>
      </ul></div>
      <div><h5>Werkgebied</h5><ul>
        <li><a href="/kunststof-kozijnen-hengelo/">Hengelo</a></li>
        <li><a href="/kunststof-kozijnen-enschede/">Enschede</a></li>
        <li><a href="/kunststof-kozijnen-almelo/">Almelo</a></li>
        <li><a href="/kunststof-kozijnen-apeldoorn/">Apeldoorn</a></li>
        <li><a href="/kunststof-kozijnen-zwolle/">Zwolle</a></li>
      </ul></div>
      <div><h5>Bedrijf</h5><ul>
        <li><a href="/over-ons/">Over ons</a></li>
        <li><a href="/projecten/">Projecten</a></li>
        <li><a href="/blog/">Blog &amp; advies</a></li>
        <li><a href="/#contact">Contact</a></li>
        <li><a href="/privacybeleid/">Privacybeleid</a></li>
      </ul></div>
    </div>
    <div class="ftr-bot">
      <span>© 2026 Duurkracht Kozijnen B.V. · KvK 90895312 · BTW NL865480112B01</span>
      <div class="socials">
        <a href="https://www.facebook.com/duurkrachtkozijnen" rel="noopener" aria-label="Facebook"><img src="/design-assets/icons/icon-facebook.svg" alt="" /></a>
        <a href="https://www.linkedin.com/company/duurkracht-kozijnen" rel="noopener" aria-label="LinkedIn"><img src="/design-assets/icons/icon-linkedin.svg" alt="" /></a>
        <a href="https://wa.me/31850731660" rel="noopener" aria-label="WhatsApp"><img src="/design-assets/icons/icon-whatsapp.svg" alt="" /></a>
      </div>
    </div>
  </div>
</footer>

<div class="mobile-cta">
  <a href="tel:+31850731660" class="m-call" rel="nofollow"><img src="/design-assets/icons/icon-phone.svg" alt="" /> Bel direct</a>
  <a href="https://wa.me/31850731660" class="m-wa" rel="noopener"><img src="/design-assets/icons/icon-whatsapp.svg" alt="" /> WhatsApp</a>
</div>'''


def head(title, description, slug, image):
    return f'''<!DOCTYPE html>
<html lang="nl-NL">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="https://www.duurkrachtkozijnen.nl/diensten/{slug}/" />
<meta name="theme-color" content="#0B5A2B" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="https://www.duurkrachtkozijnen.nl/diensten/{slug}/" />
<meta property="og:image" content="https://www.duurkrachtkozijnen.nl{image}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..800,30..100,0..1;1,9..144,400..800,30..100,0..1&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/site.css" />
<link rel="icon" type="image/svg+xml" href="/design-assets/beelmerkje-klein.svg" />
'''


def breadcrumb_jsonld(slug, label):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.duurkrachtkozijnen.nl/"},
            {"@type": "ListItem", "position": 2, "name": "Diensten", "item": "https://www.duurkrachtkozijnen.nl/diensten/"},
            {"@type": "ListItem", "position": 3, "name": label, "item": f"https://www.duurkrachtkozijnen.nl/diensten/{slug}/"},
        ]
    }, ensure_ascii=False)


def service_jsonld(slug, name, description, brand=None):
    obj = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"https://www.duurkrachtkozijnen.nl/diensten/{slug}/#service",
        "name": name,
        "description": description,
        "provider": {"@type": "LocalBusiness", "name": "Duurkracht Kozijnen B.V.", "@id": "https://www.duurkrachtkozijnen.nl/#business"},
        "areaServed": {"@type": "Country", "name": "Nederland"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "10", "bestRating": "5"}
    }
    if brand:
        obj["brand"] = {"@type": "Brand", "name": brand[0], "url": brand[1]}
    return json.dumps(obj, ensure_ascii=False)


def faq_jsonld(items):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ]
    }, ensure_ascii=False)


def breadcrumb_html(label):
    return f'''<nav class="breadcrumb" aria-label="Kruimelpad">
  <div class="container">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/diensten/">Diensten</a></li>
      <li>{label}</li>
    </ol>
  </div>
</nav>'''


def hero(eyebrow, h1, lead, image, alt):
    return f'''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="hero-cta">
          <a href="#contact" class="btn btn-primary">Plan een gratis inmeting <span class="arrow">→</span></a>
          <a href="#voordelen" class="btn btn-ghost-white">Bekijk voordelen</a>
        </div>
        <div class="hero-trust">
          <span class="stars">★★★★★</span>
          <span>4,9 / 5 · <strong>Google reviews</strong></span>
          <span class="sep">|</span>
          <span>Schüco · KOMO · 10 jaar garantie</span>
        </div>
      </div>
      <figure class="hero-visual">
        <img src="{image}" alt="{alt}" loading="eager" fetchpriority="high" width="600" height="750" />
        <div class="review-badge">
          <img src="/design-assets/icons/icon-google-g.svg" alt="Google" width="32" height="32" />
          <div class="rb-text">
            <strong>4,9 / 5</strong>
            <span class="gold">★★★★★</span><br>
            <span>op Google Reviews</span>
          </div>
        </div>
      </figure>
    </div>
  </div>
</section>'''


def usp_strip(items):
    items_html = ''
    # Dubbel toevoegen voor seamless marquee
    for txt in items * 2:
        items_html += f'<span>{txt}</span><span class="sep"></span>'
    return f'''<div class="usp-strip">
  <div class="usp-row">
    {items_html}
  </div>
</div>'''


def stats_section(stats):
    cells = ''.join(
        f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>'
        for n, l in stats
    )
    return f'<section class="stats"><div class="container">{cells}</div></section>'


def two_col_intro(eyebrow, h2, paragraphs, checklist, image, alt):
    ps = ''.join(f'<p>{p}</p>' for p in paragraphs)
    cl = ''.join(f'<li>{c}</li>' for c in checklist)
    return f'''<section class="section">
  <div class="container two-col">
    <div>
      <span class="eyebrow" style="color: var(--orange);">{eyebrow}</span>
      <h2>{h2}</h2>
      {ps}
      <ul class="checklist">{cl}</ul>
    </div>
    <div class="img-stack">
      <img src="{image}" alt="{alt}" loading="lazy" />
    </div>
  </div>
</section>'''


def specs_section(rows, source=None):
    body = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in rows)
    src = f'<p style="font-size: 13px; color: var(--gray-500); margin-top: 16px;">Bron: {source}</p>' if source else ''
    return f'''<section class="section" style="background: var(--gray-50);" id="specs">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow">Technische specificaties</span>
        <h2>De cijfers,<br><span class="em-italic">op een rij.</span></h2>
      </div>
      <p>Geverifieerde productspecificaties. Wij werken uitsluitend met premium materialen en kunnen op verzoek aangepaste uitvoeringen leveren.</p>
    </div>
    <table class="specs-table"><tbody>{body}</tbody></table>
    {src}
  </div>
</section>'''


def benefits_section(intro_eyebrow, intro_h2, intro_p, benefits):
    bs = ''
    for b in benefits:
        bs += f'<article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>{b[0]}</h3><p>{b[1]}</p></article>'
    return f'''<section class="section" id="voordelen">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow" style="color: var(--orange);">{intro_eyebrow}</span>
        <h2>{intro_h2}</h2>
      </div>
      <p>{intro_p}</p>
    </div>
    <div class="benefits">{bs}</div>
  </div>
</section>'''


def gallery_section(eyebrow, h2, p, images):
    """images: list of (src, alt, modifier) where modifier in '', 'wide', 'tall'"""
    cells = ''
    for src, alt, mod in images:
        cls = 'ph' + (f' {mod}' if mod else '')
        cells += f'<div class="{cls}"><img src="{src}" alt="{alt}" loading="lazy" /></div>'
    return f'''<section class="section" style="background: var(--gray-50);">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow" style="color: var(--orange);">{eyebrow}</span>
        <h2>{h2}</h2>
      </div>
      <p>{p}</p>
    </div>
    <div class="gallery">{cells}</div>
  </div>
</section>'''


def reviews_section(reviews):
    """reviews: list of (initial, name, date, text)"""
    cards = ''
    for init, name, date, txt in reviews:
        cards += f'''<article class="review">
        <div class="stars">★★★★★</div>
        <div class="when">{date}</div>
        <blockquote>"{txt}"</blockquote>
        <div class="author">
          <div class="avatar">{init}</div>
          <div class="author-meta"><strong>{name}</strong><span><img src="/design-assets/icons/icon-google-g.svg" alt="" />Google review</span></div>
        </div>
      </article>'''
    return f'''<section class="section reviews">
  <div class="container">
    <div class="section-head reviews-head">
      <div>
        <span class="eyebrow">Klanten over deze dienst</span>
        <h2>Echte reacties,<br><span class="em-italic">echte projecten.</span></h2>
      </div>
    </div>
    <div class="review-grid">{cards}</div>
  </div>
</section>'''


def faq_section(items):
    """items: list of (question, answer_html)"""
    fs = ''
    for i, (q, a) in enumerate(items):
        opn = ' open' if i == 0 else ''
        fs += f'<details class="faq-item"{opn}><summary>{q}</summary><div class="answer">{a}</div></details>'
    return f'''<section class="section faq">
  <div class="container">
    <div class="section-head" style="grid-template-columns: 1fr; text-align: center; max-width: 700px; margin-left: auto; margin-right: auto;">
      <div>
        <span class="eyebrow" style="justify-content: center;">Veelgestelde vragen</span>
        <h2>Antwoorden, <span class="em-italic">vooraf.</span></h2>
      </div>
    </div>
    <div class="faq-list">{fs}</div>
  </div>
</section>'''


def cta_banner(h2_intro, h2_em, p):
    return f'''<section class="cta-banner" id="contact">
  <div class="container">
    <div>
      <span class="eyebrow">Klaar om te beginnen?</span>
      <h2>{h2_intro}<br><span class="em-italic">{h2_em}</span></h2>
      <p>{p}</p>
    </div>
    <div class="cta-banner-actions">
      <a href="/#contact" class="btn btn-primary">Plan een gratis adviesgesprek <span class="arrow">→</span></a>
      <a href="tel:+31850731660" class="btn btn-ghost-white" rel="nofollow">Of bel direct: 085 073 1660</a>
      <p class="meta-line">Gemiddelde reactietijd: <strong>onder de 4 uur</strong> op werkdagen.</p>
    </div>
  </div>
</section>'''


def build_page(slug, label, page):
    """Render een complete dienst-pagina."""
    schemas = [
        breadcrumb_jsonld(slug, label),
        service_jsonld(slug, page['service_name'], page['service_desc'], page.get('brand')),
        faq_jsonld(page['faq'])
    ]
    schema_blocks = '\n'.join(f'<script type="application/ld+json">{s}</script>' for s in schemas)

    html = head(page['title'], page['description'], slug, page['hero_image']) + schema_blocks + '\n</head>\n<body>\n'
    html += '<a href="#main" class="skip">Direct naar inhoud</a>\n'
    html += TOPBAR + '\n' + NAV + '\n' + breadcrumb_html(label) + '\n<main id="main">\n'
    html += hero(page['hero_eyebrow'], page['h1'], page['lead'], page['hero_image'], page['hero_alt']) + '\n'
    html += usp_strip(page['usp']) + '\n'
    html += stats_section(page['stats']) + '\n'
    html += two_col_intro(page['intro_eyebrow'], page['intro_h2'], page['intro_paragraphs'], page['intro_checklist'], page['intro_image'], page['intro_alt']) + '\n'
    if page.get('specs'):
        html += specs_section(page['specs'], page.get('specs_source')) + '\n'
    html += benefits_section(page['benefits_eyebrow'], page['benefits_h2'], page['benefits_p'], page['benefits']) + '\n'
    html += gallery_section(page['gallery_eyebrow'], page['gallery_h2'], page['gallery_p'], page['gallery']) + '\n'
    html += WERKWIJZE + '\n'
    html += reviews_section(page['reviews']) + '\n'
    html += faq_section(page['faq_html']) + '\n'
    html += cta_banner(page['cta_h2_intro'], page['cta_h2_em'], page['cta_p']) + '\n'
    html += '</main>\n' + FOOTER + '\n</body>\n</html>\n'

    out = ROOT / 'diensten' / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'  ✓ {out.relative_to(ROOT)} ({len(html)//1024} KB)')


# ============================================================
# PAGINA DATA
# ============================================================

PAGES = {

    'kunststof-deuren': {
        'label': 'Kunststof deuren',
        'data': {
            'title': 'Kunststof Voordeuren en Achterdeuren op Maat | Duurkracht Kozijnen',
            'description': 'Kunststof voor- en achterdeuren met meerpuntsluiting en SKG**-cilinder. Inbraakwerend RC2, optioneel PKVW-certificering. Maatwerk. Plaatsing in heel Nederland.',
            'service_name': 'Kunststof voordeuren en achterdeuren op maat',
            'service_desc': 'Levering en montage van kunststof voor- en achterdeuren met meerpuntsluiting, SKG**-cilinder en inbraakwerendheid RC2. Optioneel met PKVW-keurmerk.',
            'brand': ('Schüco', 'https://www.schueco.com/nl'),
            'hero_image': '/design-assets/images/diensten-deuren.jpeg',
            'hero_alt': 'Antraciet kunststof voordeur met zijraam en moderne erker — recent project Duurkracht Kozijnen',
            'hero_eyebrow': 'Kunststof voor- en achterdeuren',
            'h1': 'Een nieuwe deur die <span class="em-italic">het verschil maakt</span> — uitstraling, veiligheid en isolatie.',
            'lead': 'Kunststof voor- en achterdeuren met <strong>meerpuntsluiting</strong>, SKG**-cilinder en inbraakwerendheid <strong>RC2</strong>. Honderden modellen, alle RAL-kleuren. Optioneel <strong>PKVW</strong>-certificering voor premiekorting op uw inboedelverzekering.',
            'usp': ['Meerpuntsluiting', 'SKG**-cilinder', 'RC2 inbraakwerend', 'PKVW optioneel', 'Vingerscan mogelijk', 'Alle RAL-kleuren', '10 jaar garantie'],
            'stats': [
                ('RC2', 'Inbraakwerendheid<br>standaard'),
                ('5pt', 'Meerpuntsluiting<br>standaard'),
                ('100+', 'Beschikbare modellen<br>en uitvoeringen'),
                ('10 jr', 'Garantie op deur<br>en montage'),
            ],
            'intro_eyebrow': 'Onze deuren',
            'intro_h2': 'Eerste indruk telt — <span class="em-italic">en blijft.</span>',
            'intro_paragraphs': [
                'De voordeur is letterlijk de eerste indruk van uw huis. Onze kunststof deuren combineren karaktervolle uitstraling met topkwaliteit op het gebied van veiligheid, isolatie en duurzaamheid. Wij leveren modellen van klassiek tot strak-modern, in elk gewenst formaat.',
                'Onze deuren komen standaard met een 5-punts meerpuntsluiting, SKG**-cilinder en stalen versterkingen. Op verzoek upgraden we naar SKG3, PKVW (Politiekeurmerk Veilig Wonen) of slimme sluiting met vingerscan of digitaal slot.',
            ],
            'intro_checklist': [
                '<strong>5-punts meerpuntsluiting</strong> als standaard',
                '<strong>SKG**-cilinder</strong> tegen kerntrekken',
                '<strong>Stalen versterkingsprofielen</strong> tegen wrikken',
                '<strong>Inbraakwerendheid RC2</strong> (optie RC3)',
                '<strong>PKVW-keurmerk</strong> op aanvraag — premiekorting verzekering',
                '<strong>Triple-glas optie</strong> voor extra isolatie en geluidsdemping',
            ],
            'intro_image': '/design-assets/images/Nieuwe-voordeur-huis.jpg',
            'intro_alt': 'Strakke antraciet kunststof voordeur met handvat en zijraam',
            'specs': [
                ('Profielsysteem', '<strong>Schüco LivIng 82</strong> (deurkozijn)'),
                ('Inbraakwerendheid', 'RC2 standaard (RC3 op verzoek)'),
                ('Sluiting', '5-punts meerpuntsluiting'),
                ('Cilinder', 'SKG** standaard (SKG*** op verzoek)'),
                ('Versterking', 'Stalen versterking in profiel + scharnieren'),
                ('Glasopties', 'HR++ (standaard), triple HR+++ (optioneel), figuurglas'),
                ('Kleuren', 'Alle RAL-kleuren · folie-houtnerf (eiken, mahonie, antraciet)'),
                ('Vormgeving', '100+ modellen — klassiek tot modern'),
                ('Slim slot', 'Vingerscan, code of app-bediening optioneel'),
                ('Brievenbus', 'Geïntegreerd of separaat'),
                ('Garantie', '10 jaar op deur en montage'),
            ],
            'specs_source': '<a href="https://www.schueco.com/nl/particulieren/deursystemen/kunststof-huisdeuren" rel="external nofollow noopener" style="color: var(--green);">schueco.com</a>',
            'benefits_eyebrow': 'Voordelen',
            'benefits_h2': 'Waarom kiezen voor een<br><span class="em-italic">kunststof deur?</span>',
            'benefits_p': 'Kunststof voor- en achterdeuren zijn dé moderne keuze voor wie kwaliteit, veiligheid en onderhoudsgemak waardeert.',
            'benefits': [
                ('RC2 inbraakwerend', '5-punts sluiting en SKG**-cilinder als standaard — RC2 gecertificeerd.'),
                ('PKVW-korting', 'Met PKVW-keurmerk vaak korting op uw inboedelverzekering.'),
                ('Onderhoudsarm', 'Nooit schilderen of schuren — alleen periodiek afsoppen.'),
                ('Energiebesparend', 'Goede isolatie + tochtdichte rondom-afdichting.'),
                ('Geluidsdempend', 'Massief profiel met triple glas dempt buitengeluid sterk.'),
                ('Maatwerk', '100+ modellen, alle RAL-kleuren — gegarandeerd uw stijl.'),
            ],
            'gallery_eyebrow': 'Onze deuren',
            'gallery_h2': 'Een greep uit onze<br><span class="em-italic">recente</span> projecten.',
            'gallery_p': 'Van klassieke voordeuren tot moderne minimalistische achterdeuren — bekijk een aantal recente plaatsingen.',
            'gallery': [
                ('/design-assets/images/Nieuwe-voordeur-huis.jpg', 'Antraciet voordeur met zijraam en erker', 'wide'),
                ('/design-assets/images/diensten-deuren.jpeg', 'Strakke antraciet voordeur', ''),
                ('/design-assets/images/Deur-met-kozijnen.jpg', 'Modern huis met antraciet kunststof deur en kozijnen', ''),
                ('/design-assets/images/Voorkant-huis-kozijnen.jpg', 'Jaren-30 woning met rode voordeur en witte kozijnen', ''),
                ('/design-assets/images/Nieuwe-kozijnen-met-deur.jpg', 'Moderne kunststof deur met kozijnen', ''),
                ('/design-assets/images/Kunststof-kozijnen-voordeur.jpg', 'Antraciet voordeur in nieuwbouwwijk', 'wide'),
            ],
            'reviews': [
                ('R', 'Rinze Bos', 'Juni 2025', 'Bart is bij ons voor een vrijblijvende offerte geweest. Vanwege hun scherpe prijs en Schüco kozijnen i.c.m. stelkozijn-montage hebben we de achtergevel laten renoveren met een nieuwe achterdeur, 2 kozijnen en Keralit gevelbekleding.'),
                ('7', '7vianno', 'Juni 2025', 'Wij zijn heel blij met het resultaat! De voordeur, ramen en kozijnen zijn allemaal vervangen. Alles is netjes gemonteerd en het huis ziet er nu veel moderner en mooier uit.'),
                ('R', 'Ria Van der Niet', 'Juli 2025', 'Er zijn bij ons kunststof kozijnen geplaatst door Duurkracht Kozijnen en wij zijn super tevreden — de kozijnen zijn prachtig en de mannen hebben keihard en netjes gewerkt.'),
            ],
            'faq': [
                ('Wat is het verschil tussen SKG** en SKG***?', 'SKG** (twee sterren) is het standaard inbraakwerend niveau dat verzekeraars eisen. SKG*** (drie sterren) biedt extra bescherming tegen kerntrekken en wordt geadviseerd voor woningen op de begane grond of in inbraakgevoelige gebieden.'),
                ('Wat is PKVW en hoeveel korting krijg ik op mijn verzekering?', 'PKVW (Politiekeurmerk Veilig Wonen) is een certificering die garandeert dat uw woning voldoet aan strenge inbraakwerings-eisen. Veel inboedelverzekeraars geven 5–10% premiekorting bij PKVW-gecertificeerde woningen.'),
                ('Kan ik een vingerscan of digitaal slot laten installeren?', 'Ja, wij leveren onze kunststof deuren optioneel met vingerscan, codepaneel of app-bestuurd slot. Dit kan eenvoudig worden gecombineerd met traditioneel sleutelgebruik.'),
                ('Wat kost een nieuwe kunststof voordeur gemiddeld?', 'Een standaard kunststof voordeur kost inclusief montage gemiddeld €1.500 tot €3.500. De prijs hangt af van model, kleur, glasinleg, sluiting en accessoires. Achterdeuren zijn meestal €1.200–€2.500.'),
                ('Hoe lang duurt de plaatsing van een nieuwe deur?', 'De vervanging van een enkele voordeur of achterdeur duurt 3 tot 6 uur. Bij vervanging van meerdere deuren en kozijnen reken op 1 tot 2 dagen.'),
            ],
            'faq_html': [
                ('Wat is het verschil tussen SKG** en SKG***?', '<p><strong>SKG**</strong> (twee sterren) is het standaard inbraakwerend niveau dat verzekeraars eisen. <strong>SKG***</strong> (drie sterren) biedt extra bescherming tegen kerntrekken en wordt geadviseerd voor woningen op de begane grond of in inbraakgevoelige gebieden.</p>'),
                ('Wat is PKVW en hoeveel korting krijg ik op mijn verzekering?', '<p><strong>PKVW</strong> (Politiekeurmerk Veilig Wonen) is een certificering die garandeert dat uw woning voldoet aan strenge inbraakwerings-eisen. Veel inboedelverzekeraars geven <strong>5 tot 10%</strong> premiekorting bij PKVW-gecertificeerde woningen.</p>'),
                ('Kan ik een vingerscan of digitaal slot laten installeren?', '<p>Ja, wij leveren onze kunststof deuren optioneel met <strong>vingerscan, codepaneel of app-bestuurd slot</strong>. Dit kan eenvoudig worden gecombineerd met traditioneel sleutelgebruik.</p>'),
                ('Wat kost een nieuwe kunststof voordeur gemiddeld?', '<p>Een standaard kunststof voordeur kost inclusief montage gemiddeld <strong>€ 1.500 tot € 3.500</strong>. De prijs hangt af van model, kleur, glasinleg, sluiting en accessoires. Achterdeuren zijn meestal € 1.200 – € 2.500.</p>'),
                ('Hoe lang duurt de plaatsing van een nieuwe deur?', '<p>De vervanging van een enkele voordeur of achterdeur duurt <strong>3 tot 6 uur</strong>. Bij vervanging van meerdere deuren en kozijnen reken op 1 tot 2 dagen.</p>'),
                ('Kan ik mijn oude scharnieren en sleutels behouden?', '<p>Nee. Een nieuwe kunststof deur komt altijd met nieuwe scharnieren (passend op het profielsysteem) en een nieuwe SKG**-cilinder met set sleutels. Dit is essentieel voor de garantie en de inbraakwerendheid.</p>'),
            ],
            'cta_h2_intro': 'Klaar voor uw nieuwe',
            'cta_h2_em': 'voordeur of achterdeur?',
            'cta_p': 'Wij komen vrijblijvend langs, laten u modellen zien, meten in en maken een vaste offerte. Eerlijk advies — ook over scharnieren, sloten en accessoires.',
        }
    },

    'kunststof-schuifpuien': {
        'label': 'Schuifpuien',
        'data': {
            'title': 'Kunststof Schuifpuien op Maat — tot 6 Meter | Duurkracht Kozijnen',
            'description': 'Kunststof schuifpuien en hefschuifdeuren op maat. Tot 6 meter breed, soepel lopend op rvs-rails. Smalle profielen voor maximaal daglicht. HR++ of triple glas. Heel Nederland.',
            'service_name': 'Kunststof schuifpuien en hefschuifdeuren',
            'service_desc': 'Levering en montage van kunststof schuifpuien en hefschuifdeuren tot 6 meter breed. Smalle profielen, rvs-rails, HR++ of triple glas. Perfect voor tuinkamers en achteruitbouw.',
            'brand': ('Schüco', 'https://www.schueco.com/nl'),
            'hero_image': '/design-assets/images/Kunststof-schuifpui.jpg',
            'hero_alt': 'Brede schuifpui met antraciet kunststof profielen — uitzicht op overdekt terras',
            'hero_eyebrow': 'Schuifpuien & hefschuifdeuren',
            'h1': 'Schuifpuien die uw <span class="em-italic">tuin naar binnen halen.</span>',
            'lead': 'Kunststof schuifpuien op maat <strong>tot 6 meter breed</strong>, soepel lopend op rvs-rails. Smalle profielen voor maximale glasvlakken — uw tuin wordt onderdeel van uw woonkamer. HR++ of triple glas standaard.',
            'usp': ['Tot 6 meter breed', 'Smalle profielen', 'RVS-rails soepel lopend', 'HR++ of triple glas', 'Hefschuif mogelijk', '10 jaar garantie', 'Eigen monteurs'],
            'stats': [
                ('6m', 'Maximale breedte<br>één pui'),
                ('2-3', 'Schuifvleugels<br>configuratie'),
                ('HR++', 'Standaard glas<br>triple optioneel'),
                ('1 dag', 'Montagetijd<br>per schuifpui'),
            ],
            'intro_eyebrow': 'Onze schuifpuien',
            'intro_h2': 'Een gevel die <span class="em-italic">opent.</span>',
            'intro_paragraphs': [
                'Een schuifpui transformeert uw woning. Door de smalle profielen en grote glasvlakken stroomt het daglicht naar binnen en wordt uw tuin onderdeel van de woonkamer. Soepel lopend op rvs-rails, met meerpuntsluiting en optioneel hefschuif-mechaniek voor luxe afdichting.',
                'Wij leveren standaard tot 6 meter breed in 2- of 3-vleugel uitvoering. Voor zwaardere puien adviseren we het hefschuifsysteem: hierbij wordt de vleugel licht opgetild voordat hij schuift — onhoorbaar soepel, perfect afgedicht in gesloten stand.',
            ],
            'intro_checklist': [
                '<strong>Tot 6 meter breed</strong> in één pui',
                '<strong>RVS-rails</strong> — soepel lopend, slijtvast',
                '<strong>Smalle profielen</strong> — meer glas, meer licht',
                '<strong>Meerpuntsluiting</strong> voor inbraakwerendheid',
                '<strong>Hefschuif-systeem</strong> optioneel voor extra dichting',
                '<strong>HR++ of triple glas</strong> naar wens',
            ],
            'intro_image': '/design-assets/images/achtertuin-schuifpui.jpg',
            'intro_alt': 'Antraciet schuifpui met uitzicht op moderne achtertuin',
            'specs': [
                ('Maximale breedte', '<strong>6.000 mm</strong> (één pui, 2-3 vleugels)'),
                ('Maximale hoogte', '2.700 mm'),
                ('Profielsysteem', 'Schüco LivIng (schuif-uitvoering)'),
                ('Glasopties', 'HR++ (standaard), triple HR+++ (optioneel)'),
                ('Rails', 'RVS, soepel lopend met rolwielen'),
                ('Mechaniek', 'Standaard schuif of hefschuif (optioneel)'),
                ('Sluiting', 'Meerpuntsluiting, hefhendel'),
                ('Inbraakwerendheid', 'RC2 standaard'),
                ('Kleuren', 'Antraciet (RAL 7016), wit, alle RAL op aanvraag'),
                ('Doorgang', 'Drempelloos uitvoerbaar (rolstoeltoegankelijk)'),
                ('Insectenwering', 'Optioneel met magnetisch hor of inschuifhor'),
                ('Garantie', '10 jaar op profiel, rails en montage'),
            ],
            'specs_source': None,
            'benefits_eyebrow': 'Voordelen',
            'benefits_h2': 'Wat een schuifpui<br>met uw <span class="em-italic">woning doet.</span>',
            'benefits_p': 'Een schuifpui is meer dan een raam. Het is een investering in licht, ruimte en wooncomfort die u dagelijks merkt.',
            'benefits': [
                ('Maximaal daglicht', 'Smalle profielen geven 20–30% meer glasoppervlak dan klassieke kozijnen.'),
                ('Tuin als woonkamer', 'In de zomer schuift de pui volledig open — buiten en binnen worden één.'),
                ('Energie­besparend', 'HR++ of triple glas houdt warmte binnen — zelfs bij grote glasvlakken.'),
                ('Drempelloos', 'Optioneel volledig drempelloos uitvoerbaar (rolstoeltoegankelijk).'),
                ('Geluiddempend', 'Massief profiel met triple glas dempt straatgeluid sterk.'),
                ('Inbraakwerend', 'RC2 standaard, meerpuntsluiting, gehard veiligheidsglas.'),
            ],
            'gallery_eyebrow': 'Onze schuifpuien',
            'gallery_h2': 'Recente <span class="em-italic">schuifpui-projecten.</span>',
            'gallery_p': 'Een greep uit onze plaatsingen. Van klassieke 2-vleugel puien tot brede 3-vleugel uitvoeringen met hefschuif-mechaniek.',
            'gallery': [
                ('/design-assets/images/Kunststof-schuifpui.jpg', 'Brede schuifpui met overkapping', 'wide'),
                ('/design-assets/images/achtertuin-schuifpui.jpg', 'Antraciet schuifpui in moderne achtertuin', ''),
                ('/design-assets/images/dienst-schuifpuien.jpeg', 'Schuifpui met overkapping in achtertuin', ''),
                ('/design-assets/images/Achterdeur-schuifpui.jpg', 'Schuifpui combinatie met achterdeur', ''),
                ('/design-assets/images/Schuifpui-achterkant-huis.jpg', 'Schuifpui aan achterzijde van moderne woning', ''),
                ('/design-assets/images/schuifpui-in-de-achtertuin.jpg', 'Schuifpui open richting achtertuin', 'wide'),
            ],
            'reviews': [
                ('S', 'S. Jansen', 'Juni 2025', 'We zijn ontzettend tevreden met het werk. De nieuwe schuifpui is perfect geplaatst — strak, netjes en helemaal volgens afspraak. Het team was vriendelijk, werkte professioneel en liet alles netjes achter. Frits verdient een speciale vermelding!'),
                ('J', 'Joke Schrijvers', 'Juni 2025', 'Nieuwe schuifpui geplaatst, uitstekend werk door erg prettige en vakkundige monteurs!'),
                ('D', 'Dee DoubleU', 'Juni 2025', 'We hebben een schuifpui door Duurkracht Kozijnen laten plaatsen. Daarbij waren we er nog niet helemaal uit hoe we de binnen afwerking zouden willen hebben. Na overleg met de medewerkers hebben ze perfect meegedacht.'),
            ],
            'faq_html': [
                ('Hoe breed kan een schuifpui worden?', '<p>Wij leveren schuifpuien tot <strong>6 meter breed</strong> in één geheel (2 of 3 vleugels). Voor bredere openingen koppelen we meerdere puien naast elkaar of adviseren we hefschuif-deuren met staal-versterkte profielen.</p>'),
                ('Wat is het verschil tussen schuif en hefschuif?', '<p>Bij een <strong>standaard schuifpui</strong> rolt de vleugel horizontaal op rvs-rails. Bij een <strong>hefschuifsysteem</strong> wordt de vleugel eerst licht opgetild (ca. 6 mm) voordat hij schuift. Dat geeft volledig dichte afdichting in gesloten stand en is daarom beter geïsoleerd en geluidsdempender. Hefschuif kost ca. 20–30% meer maar is een aanrader bij puien vanaf 4 meter breed.</p>'),
                ('Kan een schuifpui drempelloos worden uitgevoerd?', '<p>Ja. Wij leveren onze schuifpuien standaard met een lage drempel (ca. 20 mm), maar op aanvraag volledig <strong>drempelloos</strong>. Belangrijk: voor drempelloze uitvoering is een goede afvoer van regenwater (gootafvoer en helling) noodzakelijk.</p>'),
                ('Wat kost een schuifpui gemiddeld?', '<p>Een standaard schuifpui van 3 × 2,30 m kost inclusief HR++ glas en montage gemiddeld <strong>€ 3.500 – € 5.500</strong>. Een 5-meter pui met triple glas en hefschuif komt op € 7.000 – € 10.000. Wij maken na inmeting een vaste offerte.</p>'),
                ('Hoe wordt de pui ingebroken-bestendig gemaakt?', '<p>Onze schuifpuien hebben standaard <strong>meerpuntsluiting met haakpalen</strong>, <strong>RC2-inbraakwerendheid</strong> en <strong>gehard veiligheidsglas</strong>. Op verzoek upgraden we naar RC3 met anti-uitlichtbeveiliging.</p>'),
                ('Wat zijn de installatiekosten?', '<p>De montage van een schuifpui duurt <strong>1 werkdag</strong>. De prijs voor levering inclusief montage staat altijd vast in onze offerte — geen meerwerk achteraf, tenzij u zelf wijzigingen aanbrengt.</p>'),
            ],
            'faq': [
                ('Hoe breed kan een schuifpui worden?', 'Wij leveren schuifpuien tot 6 meter breed in één geheel (2 of 3 vleugels). Voor bredere openingen koppelen we meerdere puien naast elkaar of adviseren we hefschuif-deuren met staal-versterkte profielen.'),
                ('Wat is het verschil tussen schuif en hefschuif?', 'Bij een standaard schuifpui rolt de vleugel horizontaal op rvs-rails. Bij een hefschuifsysteem wordt de vleugel eerst licht opgetild (ca. 6 mm) voordat hij schuift. Dat geeft volledig dichte afdichting in gesloten stand en is daarom beter geïsoleerd en geluidsdempender. Hefschuif kost ca. 20-30% meer maar is een aanrader bij puien vanaf 4 meter breed.'),
                ('Kan een schuifpui drempelloos worden uitgevoerd?', 'Ja. Wij leveren onze schuifpuien standaard met een lage drempel (ca. 20 mm), maar op aanvraag volledig drempelloos. Belangrijk: voor drempelloze uitvoering is een goede afvoer van regenwater noodzakelijk.'),
                ('Wat kost een schuifpui gemiddeld?', 'Een standaard schuifpui van 3 × 2,30 m kost inclusief HR++ glas en montage gemiddeld €3.500 - €5.500. Een 5-meter pui met triple glas en hefschuif komt op €7.000 - €10.000.'),
            ],
            'cta_h2_intro': 'Klaar voor meer',
            'cta_h2_em': 'licht en ruimte?',
            'cta_p': 'Wij komen vrijblijvend langs, laten u verschillende uitvoeringen zien, meten in en geven advies over breedte, glas, drempel en bediening.',
        }
    },

    'kunststof-gevelbekleding': {
        'label': 'Keralit gevelbekleding',
        'data': {
            'title': 'Keralit Gevelbekleding — 10 Jaar Garantie | Duurkracht Kozijnen',
            'description': 'Keralit gevelbekleding plaatsen: onderhoudsarm kunststof in 35+ kleuren. 10 jaar fabrieksgarantie. Sponningmodellen 143, 167 en 190 mm. Nooit meer schilderen of schuren.',
            'service_name': 'Keralit gevelbekleding levering en montage',
            'service_desc': 'Levering en montage van Keralit kunststof gevelbekleding. 35+ kleuren, 10 jaar fabrieksgarantie, drie sponningmodellen (143/167/190 mm). Onderhoudsarm — nooit schilderen of schuren.',
            'brand': ('Keralit', 'https://www.keralit.nl/'),
            'hero_image': '/design-assets/images/voorkant-gevel-huis.jpg',
            'hero_alt': 'Antraciet Keralit gevelbekleding op een woning — strak en onderhoudsarm',
            'hero_eyebrow': 'Keralit gevelbekleding · 10 jaar garantie',
            'h1': 'Een gevel die <span class="em-italic">35 jaar</span> meegaat — zonder schilderen.',
            'lead': 'Keralit kunststof gevelbekleding in <strong>35+ kleuren</strong> en drie sponningmodellen. <strong>10 jaar fabrieksgarantie</strong> op product en kleurvastheid. Periodiek afsoppen is voldoende — schilderen of schuren is verleden tijd.',
            'usp': ['Keralit gevelbekleding', '10 jaar garantie', '35+ kleuren', 'Sponning 143/167/190 mm', 'Onderhoudsarm', 'Geen schilderen meer', 'Eigen monteurs'],
            'stats': [
                ('10 jr', 'Fabrieksgarantie<br>product + kleur'),
                ('35+', 'Beschikbare<br>kleuren'),
                ('3', 'Sponning­modellen<br>143/167/190 mm'),
                ('0', 'Schilderen of<br>schuren ooit'),
            ],
            'intro_eyebrow': 'Het product',
            'intro_h2': 'Waarom <span class="em-italic">Keralit</span> de standaard is.',
            'intro_paragraphs': [
                'Keralit is de Nederlandse marktleider in kunststof gevelbekleding. Hun panelen zijn ontwikkeld voor het Nederlandse klimaat: bestand tegen UV, regen, vorst en temperatuurschommelingen. Met 10 jaar fabrieksgarantie op zowel het materiaal als de kleurvastheid is Keralit een van de meest betrouwbare gevelsystemen in Europa.',
                'Bij Duurkracht Kozijnen plaatsen we Keralit al jarenlang — vaak in combinatie met een kozijnvervanging. Dat geeft een complete gevelrenovatie in één traject, zonder dat u twee keer aannemers in huis hoeft.',
            ],
            'intro_checklist': [
                '<strong>10 jaar garantie</strong> op product en kleurvastheid',
                '<strong>35+ kleuren</strong> beschikbaar uit voorraad',
                '<strong>3 sponningmodellen</strong>: 143 / 167 / 190 mm',
                '<strong>Houtlook</strong> beschikbaar voor authentieke uitstraling',
                '<strong>Nooit schilderen</strong> — alleen afsoppen met sopwater',
                '<strong>Made in Holland</strong> — door Keralit zelf geproduceerd',
            ],
            'intro_image': '/design-assets/images/Nieuwe-gevel.jpg',
            'intro_alt': 'Volledige Keralit gevelbekleding in antraciet op renovatieproject',
            'specs': [
                ('Fabrikant', '<strong>Keralit B.V.</strong> (Lelystad, Nederland)'),
                ('Materiaal', 'Hoogwaardig kunststof (PVC) met UV-stabilisatie'),
                ('Garantie', '<strong>10 jaar</strong> op product én kleurvastheid'),
                ('Aantal kleuren', '35+ standaardkleuren'),
                ('Sponningmodellen', '143 mm (smal) · 167 mm (medium) · 190 mm (breed)'),
                ('Houtlook', 'Beschikbaar in eiken, douglas en cederlook'),
                ('Bevestiging', 'Verdekt op aluminium rails en houten regelwerk'),
                ('Brandklasse', 'B-s1, d0 (zelfdovend)'),
                ('Onderhoud', 'Periodiek afsoppen met sopwater'),
                ('Verwachte levensduur', '30 – 50 jaar bij normale weersomstandigheden'),
                ('Recyclebaar', 'Ja — 100% PVC recyclebaar'),
                ('Toepassing', 'Gevels, dakkapellen, dakranden, schuurwanden'),
            ],
            'specs_source': '<a href="https://www.keralit.nl/gevelbekleding/reviews/garantie-duurzaam-kleurvast/" rel="external nofollow noopener" style="color: var(--green);">keralit.nl</a>',
            'benefits_eyebrow': 'Voordelen',
            'benefits_h2': 'Zes redenen voor<br><span class="em-italic">Keralit gevelbekleding.</span>',
            'benefits_p': 'Keralit combineert het beste van kunststof (onderhoudsarm, duurzaam) met de uitstraling van traditionele houten gevels.',
            'benefits': [
                ('10 jaar garantie', 'Fabrieksgarantie op zowel product als kleurvastheid van Keralit.'),
                ('Nooit schilderen', 'Eens per jaar afsoppen met sopwater is voldoende.'),
                ('Houtlook beschikbaar', 'Authentieke uitstraling zonder de nadelen van echt hout.'),
                ('35+ kleuren', 'Van klassiek wit tot antraciet, met houtimitaties.'),
                ('Drie modellen', 'Smal (143 mm), medium (167 mm) of breed (190 mm) sponningdeel.'),
                ('Compleet trajec​t', 'Wij combineren graag met kozijnvervanging — alles in één.'),
            ],
            'gallery_eyebrow': 'Onze gevelprojecten',
            'gallery_h2': 'Recente <span class="em-italic">gevelrenovaties.</span>',
            'gallery_p': 'Voor- en achtergevels, dakkapellen of complete gevelombouw. Een greep uit onze recente Keralit-projecten.',
            'gallery': [
                ('/design-assets/images/voorkant-gevel-huis.jpg', 'Antraciet horizontale gevelbekleding met witte kozijnen', 'wide'),
                ('/design-assets/images/Nieuwe-gevel.jpg', 'Donkergrijze gevelbekleding op uitbouw', ''),
                ('/design-assets/images/Voorkant-huis-kozijnen.jpg', 'Jaren-30 woning met witte kozijnen', ''),
                ('/design-assets/images/Nieuwe-kozijnen-met-deur.jpg', 'Antraciet gevel met kozijn en deur', ''),
                ('/design-assets/images/Deur-met-kozijnen.jpg', 'Modern huis met gecombineerde gevel en kozijnen', ''),
                ('/design-assets/images/kunststof-kozijnen-plaatsen.jpg', 'Detail van moderne kunststof gevel met kozijnen', 'wide'),
            ],
            'reviews': [
                ('R', 'Rinze Bos', 'Juni 2025', 'Bart is bij ons voor een vrijblijvende offerte geweest. Vanwege hun scherpe prijs en Schüco kozijnen i.c.m. stelkozijn-montage hebben we de achtergevel laten renoveren met een nieuwe achterdeur, 2 kozijnen en Keralit gevelbekleding.'),
                ('7', '7vianno', 'Juni 2025', 'Wij zijn heel blij met het resultaat! De voordeur, ramen en kozijnen zijn allemaal vervangen. Alles is netjes gemonteerd en het huis ziet er nu veel moderner en mooier uit.'),
                ('K', 'Kees de Jong', 'Juli 2025', 'De hele achtergevel van de huiskamer weer netjes met kozijnen van Duurkracht. Dubbel glas dus zuinig stoken. Kwaliteitsprofielen van Schüco!'),
            ],
            'faq_html': [
                ('Hoeveel jaar garantie geeft Keralit?', '<p>Keralit geeft standaard <strong>10 jaar fabrieksgarantie</strong> op zowel het product als de kleurvastheid van de gevelbekleding. Wij geven daarbovenop garantie op de montage. Bron: <a href="https://www.keralit.nl/gevelbekleding/reviews/garantie-duurzaam-kleurvast/" rel="external nofollow noopener">keralit.nl</a>.</p>'),
                ('Welke sponningmodellen zijn er?', '<p>Keralit biedt drie sponningmodellen: <strong>143 mm</strong> (smal — klassiek), <strong>167 mm</strong> (medium — robuust modern) en <strong>190 mm</strong> (breed — strak/minimalistisch). De keuze hangt af van de uitstraling die u zoekt en de gevelhoogte.</p>'),
                ('Is Keralit beschikbaar in houtlook?', '<p>Ja. Keralit heeft een uitgebreide houtlook-collectie met <strong>eiken, douglas en cederlook</strong> dessins. Visueel nauwelijks van echt hout te onderscheiden, maar zonder de nadelen van schilderen of rotten.</p>'),
                ('Kan Keralit op bestaande gevels worden geplaatst?', '<p>Ja, in de meeste gevallen wel. Wij plaatsen Keralit op <strong>houten regelwerk of aluminium rails</strong> die op de bestaande gevel worden bevestigd. Eventueel kunnen we daar isolatieplaten achter aanbrengen voor extra warmte- en geluidsisolatie.</p>'),
                ('Wat kost Keralit gevelbekleding gemiddeld?', '<p>Keralit gevelbekleding kost inclusief plaatsing gemiddeld <strong>€ 130 tot € 200 per m²</strong>. De prijs hangt af van model, kleur, bereikbaarheid en eventuele isolatie. Voor een nauwkeurige offerte komen wij vrijblijvend langs.</p>'),
                ('Hoe lang gaat Keralit gevelbekleding mee?', '<p>De verwachte levensduur van Keralit is <strong>30 tot 50 jaar</strong>. Het materiaal is UV-stabiel, vorstbestendig en bestand tegen het Nederlandse klimaat. Periodiek afsoppen met sopwater is voldoende onderhoud.</p>'),
            ],
            'faq': [
                ('Hoeveel jaar garantie geeft Keralit?', 'Keralit geeft standaard 10 jaar fabrieksgarantie op zowel het product als de kleurvastheid van de gevelbekleding. Wij geven daarbovenop garantie op de montage.'),
                ('Welke sponningmodellen zijn er?', 'Keralit biedt drie sponningmodellen: 143 mm (smal - klassiek), 167 mm (medium - robuust modern) en 190 mm (breed - strak/minimalistisch).'),
                ('Is Keralit beschikbaar in houtlook?', 'Ja. Keralit heeft een uitgebreide houtlook-collectie met eiken, douglas en cederlook dessins.'),
                ('Wat kost Keralit gevelbekleding gemiddeld?', 'Keralit gevelbekleding kost inclusief plaatsing gemiddeld €130 tot €200 per m².'),
            ],
            'cta_h2_intro': 'Klaar voor een gevel',
            'cta_h2_em': 'die nooit meer ophoudt?',
            'cta_p': 'Wij komen vrijblijvend langs met monsters, kijken naar uw gevel en geven advies over kleur, model en eventuele combinatie met nieuwe kozijnen.',
        }
    },

    'montage': {
        'label': 'Montage',
        'data': {
            'title': 'Stelkozijn-montage door Eigen Monteurs | Duurkracht Kozijnen',
            'description': 'Stelkozijn-montage door onze eigen ervaren monteurs — niet door onderaannemers. Kwaliteitsborging volgens KOMO. Schoon opgeleverd. 10 jaar garantie op profiel én montage.',
            'service_name': 'Stelkozijn-montage door eigen monteurs',
            'service_desc': 'Vakkundige plaatsing van kunststof kozijnen, deuren en schuifpuien met stelkozijn-systeem. Door onze eigen ervaren monteurs — niet door onderaannemers. KOMO-conform, schoon opgeleverd, 10 jaar garantie.',
            'hero_image': '/design-assets/images/kunststof-kozijnen-plaatsen.jpg',
            'hero_alt': 'Detail van kunststof kozijn — vakkundig geplaatst met stelkozijn',
            'hero_eyebrow': 'Montage door eigen monteurs',
            'h1': 'De plaatsing maakt <span class="em-italic">het verschil.</span>',
            'lead': 'Een hoogwaardig kozijn slecht geplaatst presteert slechter dan een gemiddeld kozijn dat perfect zit. Daarom werken wij <strong>alleen met eigen monteurs</strong> — geen onderaannemers. Stelkozijn-systeem, KOMO-conform, schoon opgeleverd.',
            'usp': ['Eigen monteurs', 'Geen onderaannemers', 'Stelkozijn-systeem', 'KOMO-conform', 'PUR-loos werken mogelijk', '10 jaar garantie', 'Schoon opgeleverd'],
            'stats': [
                ('20+', 'Jaar montage-<br>ervaring'),
                ('1-2', 'Dagen per woning<br>(6-10 kozijnen)'),
                ('100%', 'Eigen monteurs<br>geen onderaannemers'),
                ('10 jr', 'Garantie op<br>montage'),
            ],
            'intro_eyebrow': 'Waarom stelkozijn?',
            'intro_h2': 'Een stelkozijn is de <span class="em-italic">fundering</span> van uw kozijn.',
            'intro_paragraphs': [
                'Een stelkozijn is een houten of kunststof voorgemonteerde frame dat in de muuropening wordt geplaatst voordat het echte kozijn komt. Het zorgt voor een perfect vlakke, waterpas afwerking — onafhankelijk van eventuele onregelmatigheden in het metselwerk. Het verschil tussen "gewoon geplaatst" en "geplaatst met stelkozijn" is bij oplevering misschien niet meteen zichtbaar, maar wel binnen een paar jaar.',
                'Stelkozijn-montage voorkomt dat het kozijn na verloop van tijd gaat trekken, kieren ontwikkelt of dat de waterafdichting begeeft. Bij Duurkracht is stelkozijn-montage geen optie maar standaard — onderdeel van onze kwaliteitsbelofte.',
            ],
            'intro_checklist': [
                '<strong>Stelkozijn als basis</strong> voor elk kozijn — geen meerprijs',
                '<strong>Eigen monteurs</strong> met jarenlange ervaring',
                '<strong>KOMO-conforme</strong> werkwijze',
                '<strong>PUR-loos werken</strong> mogelijk op verzoek',
                '<strong>Waterdichte aansluiting</strong> met EPDM-membranen',
                '<strong>Schoon opgeleverd</strong> — bouwafval afgevoerd',
            ],
            'intro_image': '/design-assets/images/Voorkant-huis-kozijnen.jpg',
            'intro_alt': 'Vakkundig geplaatste kunststof kozijnen op jaren-30 woning',
            'benefits_eyebrow': 'Onze aanpak',
            'benefits_h2': 'Waarom onze montage<br><span class="em-italic">opvalt.</span>',
            'benefits_p': 'Montage maakt of breekt een kozijnenrenovatie. Onze monteurs zijn opgeleid om elk detail goed te krijgen.',
            'benefits': [
                ('Eigen monteurs', 'Geen onderaannemers — wij hebben ons eigen vaste team in dienst.'),
                ('Stelkozijn standaard', 'Wij zien het als basisvoorwaarde — geen meerprijs voor kwaliteit.'),
                ('KOMO-conform', 'Volgens de Nederlandse bouwnormen voor luchtdichtheid en waterkering.'),
                ('Schoon opgeleverd', 'Bouwafval gaat met ons mee. U vindt na 2 dagen geen restanten.'),
                ('1-2 dagen werk', 'Een gemiddeld huis (6-10 kozijnen) is binnen 1 à 2 dagen klaar.'),
                ('10 jaar garantie', 'Op profiel én montage — wij staan voor ons werk.'),
            ],
            'gallery_eyebrow': 'Montage in beeld',
            'gallery_h2': 'Kwaliteit, <span class="em-italic">tot in het detail.</span>',
            'gallery_p': 'Een paar voorbeelden van onze plaatsingen. Strak gekit, waterpas, geen kieren — zoals het hoort.',
            'gallery': [
                ('/design-assets/images/kunststof-kozijnen-plaatsen.jpg', 'Detail van vakkundig geplaatst kunststof kozijn', 'wide'),
                ('/design-assets/images/Voorkant-huis-kozijnen.jpg', 'Voltooid renovatieproject in Hengelo', ''),
                ('/design-assets/images/Nieuwe-voordeur-huis.jpg', 'Strak geplaatste antraciet voordeur', ''),
                ('/design-assets/images/Nieuwe-kozijnen-met-deur.jpg', 'Moderne kunststof kozijnen netjes geplaatst', ''),
                ('/design-assets/images/Deur-met-kozijnen.jpg', 'Antraciet kozijnen met deur — strakke afwerking', ''),
                ('/design-assets/images/diensten-deuren.jpeg', 'Voordeur met zijraam, schoon opgeleverd', 'wide'),
            ],
            'reviews': [
                ('S', 'Sascha de Zeeuw', 'Juni 2025', 'Johan, Angelo en Anton hebben bij ons 3 nieuwe kunststof kozijnen aan de voor- en achterzijde geplaatst op de eerste en 2de verdieping. Ze hebben alles heel netjes afgewerkt en schoongemaakt. Alle afspraken zijn nagekomen.'),
                ('S', 'S. Jansen', 'Juni 2025', 'We zijn ontzettend tevreden met het werk. De nieuwe schuifpui is perfect geplaatst — strak, netjes en helemaal volgens afspraak. Het team was vriendelijk, werkte professioneel en liet alles netjes achter.'),
                ('R', 'Ria Van der Niet', 'Juli 2025', 'Er zijn bij ons kunststof kozijnen geplaatst door Duurkracht Kozijnen en wij zijn super tevreden — de kozijnen zijn prachtig en de mannen hebben keihard en netjes gewerkt.'),
            ],
            'faq_html': [
                ('Wat is een stelkozijn precies?', '<p>Een <strong>stelkozijn</strong> is een houten of kunststof frame dat eerst in de muuropening wordt geplaatst (op stelblokken, waterpas en lood). Daarna komt het kunststof kozijn dáárin te zitten. Dit zorgt voor een perfecte uitlijning, ook bij onregelmatige metselwerk-openingen, en voorkomt kieren of trekken in de jaren erna.</p>'),
                ('Werken jullie met onderaannemers?', '<p>Nee. Al onze monteurs zijn in vaste dienst bij Duurkracht. Dat is bewust beleid: het verzekert kennis, consistentie en aansprakelijkheid. Als er ooit iets niet goed is, weten we precies wie er heeft gewerkt en hoe we het oplossen.</p>'),
                ('Kunnen jullie zonder PUR-schuim werken?', '<p>Ja. Steeds meer klanten kiezen voor <strong>PUR-loze montage</strong> uit milieu- of gezondheidsoverwegingen. Wij gebruiken dan EPDM-membranen en mineraal isolatiewol voor de aansluiting. Het resultaat is qua isolatie en luchtdichtheid gelijkwaardig.</p>'),
                ('Hoe lang duurt de montage?', '<p>Voor een gemiddelde woning met <strong>6 tot 10 kozijnen</strong> rekenen we op <strong>1 à 2 werkdagen</strong>. Een enkel kozijn of een schuifpui kunnen we vaak in een halve tot hele dag plaatsen.</p>'),
                ('Wat doen jullie met het bouwafval?', '<p>Wij voeren <strong>al het bouwafval mee af</strong>: oude kozijnen, glas, kit-resten, verpakkingsmateriaal. U vindt na onze laatste werkdag geen restanten — alles schoon en netjes achtergelaten.</p>'),
                ('Geven jullie garantie op de montage?', '<p>Ja. Wij geven <strong>10 jaar garantie</strong> op zowel het kozijn (Schüco LivIng 82) als de montage zelf. Mocht er onverhoopt iets niet goed zijn — bijvoorbeeld een lekkage door slechte afdichting — dan komen wij dit kosteloos verhelpen.</p>'),
            ],
            'faq': [
                ('Wat is een stelkozijn precies?', 'Een stelkozijn is een houten of kunststof frame dat eerst in de muuropening wordt geplaatst (op stelblokken, waterpas en lood). Daarna komt het kunststof kozijn dáárin te zitten. Dit zorgt voor een perfecte uitlijning en voorkomt kieren of trekken in de jaren erna.'),
                ('Werken jullie met onderaannemers?', 'Nee. Al onze monteurs zijn in vaste dienst bij Duurkracht. Dat is bewust beleid: het verzekert kennis, consistentie en aansprakelijkheid.'),
                ('Kunnen jullie zonder PUR-schuim werken?', 'Ja. Steeds meer klanten kiezen voor PUR-loze montage uit milieu- of gezondheidsoverwegingen. Wij gebruiken dan EPDM-membranen en mineraal isolatiewol.'),
                ('Hoe lang duurt de montage?', 'Voor een gemiddelde woning met 6 tot 10 kozijnen rekenen we op 1 à 2 werkdagen.'),
                ('Geven jullie garantie op de montage?', 'Ja. Wij geven 10 jaar garantie op zowel het kozijn als de montage zelf.'),
            ],
            'cta_h2_intro': 'Vakkundig geplaatst',
            'cta_h2_em': 'door eigen monteurs.',
            'cta_p': 'Plan een gratis adviesgesprek en kom in contact met onze monteurs. Zij komen vrijblijvend langs voor inmeting en kwaliteitsadvies.',
        }
    },
}


print('Building service pages...')
for slug, info in PAGES.items():
    info['data'].setdefault('specs', None)
    info['data'].setdefault('specs_source', None)
    build_page(slug, info['label'], info['data'])
print('Done.')
