#!/usr/bin/env python3
"""
Build blog landing + 6 SEO-geoptimaliseerde artikelen.
Genereert /blog/index.html + /blog/{slug}/index.html voor elke post.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
BLOG = ROOT / 'blog'

# ============================================================
# GEDEELDE COMPONENTEN
# ============================================================

def topbar():
    return '''<div class="topbar"><div class="container">
    <span class="live">Nu open — ma t/m vr 08:00 tot 17:00</span>
    <span>Hassinkweg 1, 7556 BV Hengelo · KvK 90895312</span>
    <span><a href="tel:+31850731660" rel="nofollow">085 073 1660</a> · <a href="mailto:info@duurkrachtkozijnen.nl">info@duurkrachtkozijnen.nl</a></span>
  </div></div>'''

def nav(active='blog'):
    items = [('Home','/','home'),('Diensten','/diensten/','diensten'),('Projecten','/projecten/','projecten'),('Blog','/blog/','blog'),('FAQ','/faq/','faq'),('Over ons','/over-ons/','over-ons'),('Contact','/contact/','contact')]
    parts = []
    for l, u, k in items:
        cls = ' class="active"' if k == active else ''
        parts.append('<li><a href="' + u + '"' + cls + '>' + l + '</a></li>')
    lis = ''.join(parts)
    return f'''<header class="nav"><div class="container">
    <a href="/" class="nav-logo"><img src="/design-assets/Logo-duurkracht-kozijnen.svg" alt="Duurkracht Kozijnen logo" width="150" height="44" /></a>
    <nav><ul>{lis}</ul></nav>
    <div class="nav-cta">
      <a href="tel:+31850731660" class="phone" rel="nofollow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>085 073 1660</a>
      <a href="/contact/" class="btn btn-primary">Gratis adviesgesprek <span class="arrow">→</span></a>
    </div>
    <button class="nav-mobile-toggle" type="button" onclick="document.querySelector('.nav ul').style.display = document.querySelector('.nav ul').style.display === 'flex' ? 'none' : 'flex'"><img src="/design-assets/icons/menu-mobile.svg" alt="" /></button>
  </div></header>'''

def footer():
    return '''<footer><div class="container">
    <div class="ftr-grid">
      <div class="ftr-brand">
        <img src="/design-assets/icon-duurkracht-kozijnen-white.svg" alt="Duurkracht Kozijnen" />
        <p>Specialist in kunststof kozijnen, deuren, schuifpuien en Keralit gevelbekleding. Vanuit Hengelo, in heel Nederland.</p>
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
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/contact/">Contact</a></li>
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
  </div></footer>

<div class="mobile-cta">
  <a href="tel:+31850731660" class="m-call" rel="nofollow"><img src="/design-assets/icons/icon-phone.svg" alt="" /> Bel direct</a>
  <a href="https://wa.me/31850731660" class="m-wa" rel="noopener"><img src="/design-assets/icons/icon-whatsapp.svg" alt="" /></a>
</div>'''


BLOG_CSS = '''<style>
.blog-hero{ background: var(--green); color: white; padding: 80px 0 60px; position: relative; overflow: hidden; }
.blog-hero::before{ content: ""; position: absolute; right: -120px; top: -100px; width: 500px; height: 500px; background-image: url("/design-assets/watermark-waarom-transparant.svg"); background-size: contain; background-repeat: no-repeat; opacity: .07; }
.blog-hero .container{ position: relative; z-index: 2; max-width: 800px; }
.blog-hero .eyebrow{ color: var(--lime); }
.blog-hero h1{ color: white; margin-bottom: 18px; }
.blog-hero p.lead{ color: #d6e3da; font-size: 18px; max-width: 600px; }

.post-meta-bar{ background: var(--gray-50); padding: 14px 0; border-bottom: 1px solid var(--gray-200); font-size: 13px; color: var(--gray-700); }
.post-meta-bar .container{ display: flex; gap: 20px; flex-wrap: wrap; align-items: center; justify-content: space-between; }
.post-meta-bar .crumb{ color: var(--gray-500); }
.post-meta-bar .meta-right{ display: flex; gap: 18px; align-items: center; }
.post-meta-bar .meta-right span::before{ content: "·"; margin-right: 14px; color: var(--gray-300); }
.post-meta-bar .meta-right span:first-child::before{ display: none; }

.article-layout{ display: grid; grid-template-columns: 1fr 280px; gap: 60px; padding: 60px 0; max-width: 1100px; margin: 0 auto; }
@media (max-width: 980px){ .article-layout{ grid-template-columns: 1fr; gap: 30px; } .toc{ position: static !important; max-height: none !important; } }

.toc{ position: sticky; top: 100px; max-height: calc(100vh - 120px); overflow-y: auto; background: var(--gray-50); padding: 24px; border-radius: var(--radius); border: 1px solid var(--gray-200); }
.toc h4{ font-size: 11.5px; letter-spacing: .15em; text-transform: uppercase; color: var(--gray-500); margin: 0 0 14px; font-weight: 600; }
.toc ul{ list-style: none; padding: 0; margin: 0; font-size: 14px; }
.toc li{ margin-bottom: 8px; line-height: 1.4; }
.toc a{ color: var(--gray-700); text-decoration: none; padding-left: 12px; border-left: 2px solid var(--gray-200); display: block; transition: all .2s; }
.toc a:hover{ color: var(--green); border-left-color: var(--green); }

.article-body{ max-width: 720px; }
.article-body h2{ font-size: clamp(1.5rem, 2.5vw, 2rem); margin: 60px 0 16px; scroll-margin-top: 90px; letter-spacing: -0.02em; }
.article-body h2:first-of-type{ margin-top: 0; }
.article-body h3{ font-size: 1.25rem; margin: 32px 0 12px; }
.article-body p{ color: var(--ink-soft); font-size: 17px; line-height: 1.7; margin: 0 0 18px; }
.article-body strong{ color: var(--ink); }
.article-body a{ color: var(--green); text-decoration: underline; }
.article-body ul, .article-body ol{ padding-left: 22px; margin: 18px 0; }
.article-body li{ color: var(--ink-soft); font-size: 17px; line-height: 1.7; margin-bottom: 10px; }
.article-body blockquote{ background: var(--green-tint); border-left: 4px solid var(--green); padding: 20px 24px; margin: 24px 0; border-radius: 0 var(--radius) var(--radius) 0; font-style: normal; }
.article-body blockquote p{ margin: 0; color: var(--ink); }
.article-body table{ width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 15px; }
.article-body table th{ background: var(--gray-50); text-align: left; padding: 12px 16px; font-weight: 600; border-bottom: 2px solid var(--gray-300); }
.article-body table td{ padding: 12px 16px; border-bottom: 1px solid var(--gray-200); }

.article-cta{ background: var(--orange-tint); border-radius: var(--radius); padding: 28px 32px; margin: 36px 0; display: flex; gap: 24px; align-items: center; flex-wrap: wrap; }
.article-cta .ic{ width: 48px; height: 48px; background: var(--orange); border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.article-cta .ic img{ width: 24px; height: 24px; filter: brightness(0) invert(1); }
.article-cta .text{ flex: 1; min-width: 240px; }
.article-cta strong{ display: block; color: var(--ink); font-size: 16px; }
.article-cta p{ margin: 4px 0 0 !important; font-size: 14px !important; color: var(--ink-soft); }
.article-cta .btn{ flex-shrink: 0; }

.author-card{ display: flex; gap: 16px; align-items: center; padding: 24px; background: var(--gray-50); border-radius: var(--radius); margin-top: 60px; }
.author-card .avatar{ width: 56px; height: 56px; background: var(--green); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 22px; flex-shrink: 0; }
.author-card .info strong{ display: block; font-size: 15px; }
.author-card .info span{ color: var(--gray-500); font-size: 13px; }

.blog-grid{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 50px; }
@media (max-width: 980px){ .blog-grid{ grid-template-columns: 1fr 1fr; } }
@media (max-width: 640px){ .blog-grid{ grid-template-columns: 1fr; } }
.blog-card{ background: white; border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; text-decoration: none; color: inherit; transition: all .3s; display: flex; flex-direction: column; }
.blog-card:hover{ transform: translateY(-4px); border-color: var(--green-mid); box-shadow: 0 16px 40px -16px rgba(11,90,43,.25); }
.blog-card .ph{ aspect-ratio: 16/9; overflow: hidden; background: var(--green); display: flex; align-items: center; justify-content: center; color: white; padding: 30px; text-align: center; font-family: "Fraunces", serif; font-style: italic; font-size: 22px; font-variation-settings:"opsz" 96, "SOFT" 80, "WONK" 1; }
.blog-card .ph img{ width: 100%; height: 100%; object-fit: cover; }
.blog-card .body{ padding: 24px; flex: 1; display: flex; flex-direction: column; }
.blog-card .cat{ font-size: 11px; letter-spacing: .15em; text-transform: uppercase; color: var(--orange); font-weight: 600; margin-bottom: 10px; }
.blog-card h3{ font-size: 19px; font-weight: 600; line-height: 1.3; margin: 0 0 10px; letter-spacing: -0.01em; }
.blog-card p{ font-size: 14px; color: var(--gray-700); margin: 0 0 16px; flex: 1; line-height: 1.55; }
.blog-card .read{ font-size: 13px; color: var(--green); font-weight: 600; display: inline-flex; align-items: center; gap: 8px; }
.blog-card .read .arrow{ transition: transform .25s; }
.blog-card:hover .read .arrow{ transform: translateX(4px); }
.blog-card .date{ font-size: 12px; color: var(--gray-500); margin-bottom: 10px; }

.related-posts{ background: var(--gray-50); padding: 80px 0; margin-top: 60px; }
.related-posts h3{ margin-bottom: 30px; }
</style>'''


# ============================================================
# BLOG POSTS DATA
# ============================================================

POSTS = [
    {
        'slug': 'kunststof-kozijnen-kosten',
        'title': 'Kunststof kozijnen kosten in 2026: complete prijsgids',
        'meta_desc': 'Wat kosten kunststof kozijnen in 2026? Complete prijsgids: per kozijn, per huis, inclusief montage, glas en kleur. Plus ISDE-subsidie tips.',
        'category': 'Prijzen & advies',
        'date': '2026-05-20',
        'modified': '2026-05-24',
        'reading_time': 7,
        'intro_image': 'Voorkant-huis-kozijnen',
        'lead': "Wat kosten kunststof kozijnen in 2026? In dit artikel zetten we alle prijscomponenten op een rij — van standaard draai-kiep tot complete gevelrenovatie. Inclusief actuele ISDE-subsidies en concrete prijsvoorbeelden.",
        'sections': [
            {'id': 'gemiddelde-prijs', 'h2': 'Wat kost een kunststof kozijn gemiddeld?', 'body': """
<p>Een standaard kunststof draai-kiep kozijn van circa <strong>1,00 × 1,20 m</strong> kost inclusief HR++ glas en montage gemiddeld <strong>€ 600 tot € 950</strong>. Voor een rijwoning met 6 tot 10 kozijnen kom je daarmee uit op <strong>€ 4.500 tot € 9.000</strong> totaal.</p>
<p>De definitieve prijs hangt af van een handvol factoren die we hieronder per stuk behandelen.</p>
"""},
        {'id': 'prijsfactoren', 'h2': 'Welke factoren bepalen de prijs?', 'body': """
<p>De prijs van een kunststof kozijn wordt bepaald door zeven hoofdfactoren:</p>
<ol>
<li><strong>Afmeting:</strong> grotere kozijnen kosten meer per stuk, maar minder per vierkante meter</li>
<li><strong>Type:</strong> vast glas is goedkoper dan draai-kiep, hefschuif is duurder dan standaard schuif</li>
<li><strong>Profielsysteem:</strong> wij werken uitsluitend met Schüco LivIng (premium)</li>
<li><strong>Glassoort:</strong> HR++ is standaard, triple glas (HR+++) is ~30% duurder</li>
<li><strong>Kleur:</strong> standaard wit is goedkoopst; folie-uitvoering (antraciet, eikenhout) ~15-25% meerprijs</li>
<li><strong>Inbraakwering:</strong> RC2 is standaard; RC3 of PKVW ~10-15% meerprijs</li>
<li><strong>Bereikbaarheid:</strong> begane grond goedkoper dan derde verdieping (steiger nodig)</li>
</ol>
"""},
        {'id': 'voorbeelden', 'h2': 'Concrete prijsvoorbeelden voor 2026', 'body': """
<table>
<thead><tr><th>Type / afmeting</th><th>Glas</th><th>Inclusief montage</th></tr></thead>
<tbody>
<tr><td>Vast glas kozijn 80×100 cm</td><td>HR++</td><td>€ 350 – € 500</td></tr>
<tr><td>Draai-kiep kozijn 100×120 cm</td><td>HR++</td><td>€ 600 – € 950</td></tr>
<tr><td>Draai-kiep kozijn 100×120 cm</td><td>Triple</td><td>€ 850 – € 1.250</td></tr>
<tr><td>Stolpraam 150×140 cm</td><td>HR++</td><td>€ 900 – € 1.400</td></tr>
<tr><td>Voordeur kunststof (standaard)</td><td>HR++</td><td>€ 1.500 – € 3.500</td></tr>
<tr><td>Achterdeur kunststof</td><td>HR++</td><td>€ 1.200 – € 2.500</td></tr>
<tr><td>Schuifpui 3 × 2,30 m</td><td>HR++</td><td>€ 3.500 – € 5.500</td></tr>
<tr><td>Schuifpui 5 m + hefschuif</td><td>Triple</td><td>€ 7.000 – € 10.000</td></tr>
</tbody>
</table>
<blockquote><p><strong>Tip:</strong> alle bovenstaande prijzen zijn inclusief Schüco LivIng profiel, 21% btw en montage op kunststof stelkozijn. Geen verborgen kosten.</p></blockquote>
"""},
        {'id': 'compleet-huis', 'h2': 'Wat kost een compleet huis aan kozijnen?', 'body': """
<p>Voor concrete oriëntatie — gemiddelde prijzen voor complete vervanging in 2026:</p>
<ul>
<li><strong>Hoekwoning, 6 kozijnen:</strong> € 4.500 – € 7.500</li>
<li><strong>Tussenwoning, 8 kozijnen:</strong> € 6.000 – € 9.500</li>
<li><strong>Vrijstaande woning, 12-15 kozijnen:</strong> € 9.000 – € 16.000</li>
<li><strong>Bovenstaand + voordeur + schuifpui:</strong> € 13.000 – € 25.000</li>
</ul>
<p>Met de huidige ISDE-subsidies kun je daar nog € 500 tot € 2.500 van aftrekken (zie volgende sectie).</p>
"""},
        {'id': 'subsidie', 'h2': 'Welke ISDE-subsidie krijg je in 2026?', 'body': """
<p>De Investeringssubsidie Duurzame Energie (ISDE) is in 2026 fors:</p>
<ul>
<li><strong>HR++ glas:</strong> € 25 per m² basis, tot <strong>€ 50/m²</strong> bij combinatie met andere isolatiemaatregel</li>
<li><strong>Triple glas:</strong> € 111 per m² basis, tot <strong>€ 222/m²</strong> bij combinatie</li>
</ul>
<p>De combinatiemaatregel betekent dat je binnen 24 maanden minimaal twee verduurzamingsmaatregelen uitvoert (bijvoorbeeld: kozijnen + spouwmuurisolatie, of kozijnen + warmtepomp).</p>
<p>De voorwaarden voor 2026:</p>
<ul>
<li>Minimum oppervlakte: <strong>3 m²</strong></li>
<li>Maximum oppervlakte: <strong>45 m²</strong> per woning</li>
<li>Geen Uf-eis meer voor kozijnen (sinds 2026)</li>
<li>Aanvragen binnen 24 maanden na plaatsing</li>
</ul>
<p>Bron: <a href="https://www.rvo.nl/subsidies-financiering/isde/woningeigenaren/isolatiemaatregelen" rel="external nofollow noopener">RVO — ISDE 2026</a>. Wij helpen u kosteloos bij de aanvraag.</p>
"""},
        {'id': 'besparing', 'h2': 'Hoeveel bespaart u jaarlijks op energie?', 'body': """
<p>De terugverdientijd van nieuwe kozijnen hangt af van wat u nu heeft:</p>
<table>
<thead><tr><th>Huidige situatie</th><th>Nieuw (HR++)</th><th>Besparing/jaar</th></tr></thead>
<tbody>
<tr><td>Enkel glas</td><td>HR++ glas</td><td>€ 450 – € 700</td></tr>
<tr><td>Oud dubbelglas (1990-2000)</td><td>HR++ glas</td><td>€ 200 – € 400</td></tr>
<tr><td>HR+ glas</td><td>Triple glas (HR+++)</td><td>€ 80 – € 180</td></tr>
<tr><td>Enkel glas</td><td>Triple glas</td><td>€ 600 – € 850</td></tr>
</tbody>
</table>
<p>Combineer dit met de eenmalige ISDE-subsidie en de terugverdientijd komt vaak op <strong>7 tot 12 jaar</strong> — terwijl de kozijnen 40+ jaar meegaan.</p>
"""},
        {'id': 'wanneer-vervangen', 'h2': 'Wanneer is vervanging zinvol?', 'body': """
<p>Een kozijn vervangen is een investering. Het is meestal zinvol als:</p>
<ul>
<li><strong>Uw kozijnen ouder zijn dan 30 jaar</strong> (vooral hout)</li>
<li><strong>U last heeft van tocht of condensvorming</strong> tussen het glas</li>
<li><strong>Uw energielabel onder C zit</strong> — vervanging tilt het vaak twee labels omhoog</li>
<li><strong>U toch al gaat verbouwen of stukadoren</strong> — combineer dan</li>
<li><strong>Uw houten kozijnen verzakt of verrot zijn</strong></li>
</ul>
"""},
        ],
        'faq': [
            ('Wat kost een kunststof draai-kiep kozijn van 100×120 cm?', 'Een standaard draai-kiep kozijn van die afmeting kost inclusief HR++ glas en montage gemiddeld € 600 tot € 950. Met triple glas € 850 tot € 1.250.'),
            ('Hoeveel ISDE-subsidie krijg ik op nieuwe kozijnen?', 'Voor HR++ glas € 25-50 per m². Voor triple glas € 111-222 per m². De hogere bedragen gelden bij combinatie met een tweede isolatiemaatregel binnen 24 maanden.'),
            ('Wat is goedkoper: kunststof of aluminium kozijnen?', 'Kunststof kozijnen (Schüco LivIng) zijn ongeveer 30-60% goedkoper dan aluminium met vergelijkbare isolatiewaarde. Aluminium is alleen voordeliger bij zeer grote afmetingen (>3m).'),
            ('Kan ik subsidie krijgen op alleen kozijnen vervangen?', 'Alleen op het glasoppervlak (HR++ of triple), niet op het kozijnprofiel zelf. De ISDE-subsidie wordt berekend over de vierkante meters glasoppervlak die u vervangt.'),
            ('Krijg ik mijn investering ooit terug?', 'Ja. Bij vervanging van enkel glas door HR++ verdient u de investering meestal in 7-12 jaar terug via lagere stookkosten. Kozijnen gaan 40-50 jaar mee, dus de winst loopt door tientallen jaren door.'),
        ],
        'cta_inline_after_h2_index': 3,  # na "compleet huis" sectie
        'cta_inline_text': '<strong>Een vaste prijs voor uw woning?</strong><p>Onze adviseur komt vrijblijvend langs, meet uw kozijnen in en maakt een vaste offerte zonder verrassingen.</p>',
        'related': ['hr-plus-plus-of-triple-glas', 'isde-subsidie-kozijnen-2026', 'schueco-living-82-review'],
    },

    {
        'slug': 'hr-plus-plus-of-triple-glas',
        'title': 'HR++ of triple glas: welke kies je voor je nieuwe kozijnen?',
        'meta_desc': 'HR++ of triple glas? Wij vergelijken U-waarde, prijs, geluidsdemping en ISDE-subsidie. Praktisch advies voor uw kozijnenkeuze.',
        'category': 'Productadvies',
        'date': '2026-05-18',
        'modified': '2026-05-24',
        'reading_time': 6,
        'intro_image': 'hero-raamkozijnen',
        'lead': "HR++ of triple glas? Een keuze die jaarlijks honderden euro's verschil kan maken — én duizenden euro's bij de aanschaf. Wij vergelijken eerlijk en geven praktisch advies per woningtype.",
        'sections': [
            {'id': 'wat-is-hr', 'h2': 'Wat is HR++ glas eigenlijk?', 'body': """
<p>HR++ staat voor <strong>Hoog Rendement (++)</strong>. Het is een isolatieglas dat bestaat uit:</p>
<ul>
<li><strong>2 glasplaten</strong> (meestal beide 4 mm dik)</li>
<li><strong>1 spouw</strong> van 14-16 mm tussen de platen</li>
<li><strong>Argon-gas</strong> in plaats van lucht in de spouw (beter isolerend)</li>
<li><strong>Low-E coating</strong> op één van de glasplaten die warmte naar binnen reflecteert</li>
</ul>
<p>De isolatiewaarde (U-waarde, lager = beter) ligt rond de <strong>Ug = 1,1 W/m²K</strong>. Ter vergelijking: enkel glas zit op 5,8 en oud dubbel glas op 2,7.</p>
"""},
        {'id': 'wat-is-triple', 'h2': 'En wat is triple glas (HR+++)?', 'body': """
<p>Triple glas heeft <strong>drie glasplaten en twee spouwen</strong>, beide gevuld met argon-gas. Specs:</p>
<ul>
<li><strong>3 glasplaten</strong> (vaak 4 mm + 4 mm + 4 mm)</li>
<li><strong>2 spouwen</strong> van elk 12-14 mm</li>
<li><strong>2x argon-gas</strong></li>
<li><strong>2x Low-E coating</strong></li>
</ul>
<p>U-waarde: <strong>Ug = 0,5 – 0,7 W/m²K</strong>. Dat is bijna passiefhuis-niveau.</p>
<p>Wel: triple glas is veel zwaarder (~30 kg/m² i.p.v. 20). Daardoor heb je sterkere profielen nodig — gelukkig is Schüco LivIng dat standaard al.</p>
"""},
        {'id': 'vergelijk', 'h2': 'HR++ vs triple: directe vergelijking', 'body': """
<table>
<thead><tr><th>Eigenschap</th><th>HR++</th><th>Triple (HR+++)</th></tr></thead>
<tbody>
<tr><td>U-waarde (Ug)</td><td>±1,1 W/m²K</td><td>0,5 – 0,7 W/m²K</td></tr>
<tr><td>Aantal glasplaten</td><td>2</td><td>3</td></tr>
<tr><td>Gewicht per m²</td><td>~20 kg</td><td>~30 kg</td></tr>
<tr><td>Geluidsdemping</td><td>32-35 dB</td><td>38-42 dB</td></tr>
<tr><td>Prijs (indicatie meerprijs)</td><td>Standaard</td><td>+ 30-40%</td></tr>
<tr><td>ISDE-subsidie 2026 (basis)</td><td>€ 25/m²</td><td>€ 111/m²</td></tr>
<tr><td>ISDE-subsidie (met combi)</td><td>€ 50/m²</td><td>€ 222/m²</td></tr>
<tr><td>Verwachte levensduur</td><td>25-30 jaar</td><td>25-30 jaar</td></tr>
<tr><td>Energiebesparing vs enkel glas</td><td>~€ 500/jaar</td><td>~€ 700/jaar</td></tr>
</tbody>
</table>
"""},
        {'id': 'wanneer-welk', 'h2': 'Wanneer kies je welke?', 'body': """
<p>Geen one-size-fits-all — onze pragmatische adviezen per situatie:</p>
<h3>Kies HR++ als...</h3>
<ul>
<li>U een <strong>bestaande woning renoveert</strong> en al een redelijk gezond energielabel heeft (C of beter)</li>
<li>U <strong>budget-bewust</strong> bent en al een mooie ISDE-subsidie pakt</li>
<li>De woning <strong>niet aan een drukke straat</strong> staat (geluidsisolatie minder kritisch)</li>
<li>U <strong>kleinere kozijnen</strong> vervangt</li>
</ul>
<h3>Kies triple glas als...</h3>
<ul>
<li>U <strong>nieuwbouw</strong> heeft of een complete renovatie naar BENG/passiefhuis-niveau</li>
<li>De woning <strong>aan een drukke weg of vliegroute</strong> staat — geluidsdemping is ~5-8 dB beter</li>
<li>U <strong>grote glaspartijen</strong> heeft (schuifpuien, grote raampartijen) waar warmteverlies groot is</li>
<li>U op <strong>energielabel A+++</strong> wil komen</li>
<li>U van plan bent <strong>>10 jaar in de woning te blijven</strong> (langere terugverdientijd)</li>
</ul>
"""},
        {'id': 'terugverdienen', 'h2': 'Hoe snel verdient triple glas zich terug?', 'body': """
<p>Triple glas kost ~30-40% meer dan HR++. Maar bespaart ook ~30-40% méér op stookkosten. Ruwe schatting voor een gemiddelde rijwoning (80 m² gevel, 15 m² glasoppervlak):</p>
<ul>
<li>Meerkosten triple glas vs HR++: <strong>€ 1.500 – € 2.500</strong></li>
<li>Extra ISDE-subsidie (basis): <strong>€ 1.300</strong> (€ 86 × 15 m²)</li>
<li>Extra ISDE-subsidie (met combi): <strong>€ 2.580</strong> (€ 172 × 15 m²)</li>
<li>Extra besparing op stookkosten: <strong>€ 150-200/jaar</strong></li>
</ul>
<p>Met de combi-subsidie verdient u het meerwerk vrijwel direct terug. Zonder combi: 5-10 jaar.</p>
"""},
        {'id': 'advies', 'h2': 'Ons advies in één zin', 'body': """
<blockquote><p><strong>Gaat u verbouwen en pakt u sowieso een tweede maatregel mee (spouwisolatie, warmtepomp)?</strong> Kies triple glas — de combi-subsidie maakt het bijna gratis. <strong>Geen combi?</strong> HR++ is een prima keuze, vooral op bestaande woningen.</p></blockquote>
"""},
        ],
        'faq': [
            ('Is triple glas altijd beter dan HR++?', 'Technisch wel (lagere U-waarde, betere geluidsdemping). Financieel hangt het af van of u de combi-subsidie kunt pakken. Zonder combi is HR++ vaak voldoende.'),
            ('Kan triple glas in elk kozijn?', 'Niet in oude houten kozijnen (te zwaar). In onze Schüco LivIng profielen wel — die zijn standaard geschikt voor triple glas.'),
            ('Hoeveel decibel scheelt triple glas?', 'Triple glas dempt 5 tot 8 decibel meer dan HR++. Dat klinkt klein, maar elke 10 dB wordt door het menselijk oor als half zo luid ervaren. Bij verkeer/vliegroute aanrader.'),
            ('Geeft triple glas problemen met condens?', 'Nee, bij goede montage niet. De binnenkant is door de extra isolatie juist minder koud, dus minder kans op binnencondens. Buitencondens (op koude ochtenden) kan wel voorkomen — dat is een teken dat het glas perfect isoleert.'),
            ('Kan ik HR++ later upgraden naar triple?', 'Theoretisch wel (glas wisselen in hetzelfde kozijn), maar in de praktijk vaak niet zinvol. Het meeste werk zit in de montage, niet in het glas. Beter direct triple plaatsen als u dat wil.'),
        ],
        'cta_inline_after_h2_index': 2,
        'cta_inline_text': '<strong>Onzeker over HR++ of triple?</strong><p>Onze adviseur kijkt naar uw woning, energielabel en wensen — en geeft eerlijk advies. Geen verkoopdruk.</p>',
        'related': ['kunststof-kozijnen-kosten', 'isde-subsidie-kozijnen-2026', 'schueco-living-82-review'],
    },

    {
        'slug': 'isde-subsidie-kozijnen-2026',
        'title': 'ISDE-subsidie voor kozijnen in 2026: complete gids',
        'meta_desc': 'Krijg in 2026 tot €222 per m² ISDE-subsidie op triple glas. Voorwaarden, aanvraag-stappen en valkuilen — alles in één gids.',
        'category': 'Subsidie',
        'date': '2026-05-15',
        'modified': '2026-05-24',
        'reading_time': 5,
        'intro_image': 'Nieuwe-voordeur-huis',
        'lead': "De ISDE-subsidie is in 2026 hoger dan ooit voor isolatieglas. In deze gids leggen we precies uit hoeveel u krijgt, wanneer u aanspraak maakt en hoe u de aanvraag indient — zonder de bekende valkuilen.",
        'sections': [
            {'id': 'wat-is-isde', 'h2': 'Wat is de ISDE-subsidie?', 'body': """
<p>De <strong>Investeringssubsidie Duurzame Energie en Energiebesparing (ISDE)</strong> is een subsidieregeling van het Rijk, uitgevoerd door <a href="https://www.rvo.nl/subsidies-financiering/isde" rel="external nofollow noopener">RVO.nl</a>. Het doel: verduurzaming van Nederlandse woningen stimuleren.</p>
<p>Voor woningeigenaren is er subsidie beschikbaar op:</p>
<ul>
<li>Warmtepompen</li>
<li>Zonneboilers</li>
<li>Isolatiemaatregelen (waaronder <strong>HR++ en triple glas</strong>)</li>
<li>Aansluiting op een warmtenet</li>
</ul>
"""},
        {'id': 'hoeveel', 'h2': 'Hoeveel subsidie krijgt u in 2026?', 'body': """
<p>Voor isolatieglas geldt in 2026:</p>
<table>
<thead><tr><th>Type glas</th><th>Subsidie per m²</th><th>Bij combi-maatregel</th></tr></thead>
<tbody>
<tr><td><strong>HR++ glas</strong></td><td>€ 25</td><td>€ 50</td></tr>
<tr><td><strong>Triple glas (HR+++)</strong></td><td>€ 111</td><td>€ 222</td></tr>
</tbody>
</table>
<p>De <strong>combi-maatregel</strong> betekent dat u binnen <strong>24 maanden</strong> minimaal twee verschillende verduurzamingsmaatregelen uitvoert. Bijvoorbeeld:</p>
<ul>
<li>Triple glas + spouwmuurisolatie</li>
<li>Triple glas + warmtepomp</li>
<li>HR++ glas + dakisolatie</li>
<li>Triple glas + vloerisolatie</li>
</ul>
<blockquote><p><strong>Praktisch voorbeeld:</strong> bij 15 m² triple glas met combi-maatregel = <strong>€ 3.330 subsidie</strong>. Op een totale glasinvestering van bijvoorbeeld € 9.000 is dat ~37% van de kosten.</p></blockquote>
"""},
        {'id': 'voorwaarden', 'h2': 'De voorwaarden in 2026', 'body': """
<p>Om voor ISDE-subsidie in aanmerking te komen moet u voldoen aan:</p>
<ul>
<li><strong>Minimum oppervlakte:</strong> 3 m² per glasvervanging</li>
<li><strong>Maximum oppervlakte:</strong> 45 m² per woning per subsidieperiode</li>
<li><strong>Eigenaar-bewoner:</strong> u woont zelf in de woning (of komt er wonen)</li>
<li><strong>Bestaande woning:</strong> niet voor nieuwbouw vanaf 2024</li>
<li><strong>Vakkundige installatie:</strong> uitgevoerd door een bouwbedrijf</li>
<li><strong>Aanvraag binnen 24 maanden</strong> na plaatsing</li>
</ul>
<p>Goed om te weten: vanaf 2026 is de <strong>Uf-eis voor kozijnen vervallen</strong>. Vroeger moest het kozijnprofiel ook aan strenge eisen voldoen — dat is nu losgelaten. Alleen het glas moet aan de specs voldoen.</p>
"""},
        {'id': 'aanvragen', 'h2': 'Hoe vraagt u ISDE aan? Stap-voor-stap', 'body': """
<ol>
<li><strong>Laat het werk uitvoeren</strong> door een geregistreerd bouwbedrijf (zoals Duurkracht Kozijnen)</li>
<li><strong>Bewaar de eindfactuur</strong> — met daarop apart de glaskosten en het aantal m²</li>
<li><strong>Bewaar het betaalbewijs</strong> (bankafschrift)</li>
<li><strong>Ga naar mijn.rvo.nl</strong> en log in met DigiD</li>
<li><strong>Selecteer "ISDE-subsidie aanvragen"</strong> en kies "Isolatiemaatregelen"</li>
<li><strong>Vul de gegevens in</strong>: glassoort, aantal m², factuurbedrag, bedrijfsgegevens</li>
<li><strong>Upload factuur en betaalbewijs</strong> als PDF</li>
<li><strong>Wacht 8-13 weken</strong> op uitbetaling</li>
</ol>
<p>RVO betaalt de subsidie rechtstreeks op uw bankrekening uit — niet via het bouwbedrijf.</p>
"""},
        {'id': 'valkuilen', 'h2': 'Vijf valkuilen om te vermijden', 'body': """
<ol>
<li><strong>Te lang wachten met aanvragen.</strong> De deadline is 24 maanden na uitvoering. Vraag liefst binnen 6 maanden aan.</li>
<li><strong>Te kleine oppervlakte.</strong> Onder de 3 m² geen subsidie. Combineer eventueel met de buurman of plan ergens anders glas mee.</li>
<li><strong>Vergeten te factureren als "isolatieglas".</strong> Op de factuur moet duidelijk staan: glassoort, aantal m², per project. Wij regelen dit standaard.</li>
<li><strong>Combi-maatregel verkeerd inplannen.</strong> Beide maatregelen moeten binnen 24 maanden plaatsvinden, en u moet ze in één keer aanvragen.</li>
<li><strong>Geen DigiD.</strong> Geen DigiD = geen aanvraag. Vraag op tijd aan op www.digid.nl.</li>
</ol>
"""},
        {'id': 'helpen', 'h2': 'Wij helpen u kosteloos bij de aanvraag', 'body': """
<p>Bij Duurkracht Kozijnen zorgen we voor:</p>
<ul>
<li>Een correcte factuur met alle specificaties voor ISDE</li>
<li>Advies over welke combi-maatregel het best bij uw situatie past</li>
<li>Een rekenvoorbeeld bij uw offerte (hoeveel subsidie verwacht)</li>
<li>Hulp bij het invullen van de aanvraag op mijn.rvo.nl als u dat wil</li>
</ul>
<p>Dit zit standaard bij onze service inbegrepen — geen extra kosten.</p>
"""},
        ],
        'faq': [
            ('Kan ik ISDE krijgen op alleen kozijnen vervangen?', 'Alleen op het glasoppervlak (HR++ of triple glas), niet op het kozijnprofiel. De subsidie is afhankelijk van vierkante meters glas, niet van het aantal kozijnen.'),
            ('Wat is een combi-maatregel?', 'Een tweede verduurzamingsmaatregel die u binnen 24 maanden uitvoert. Bijvoorbeeld: spouwmuurisolatie, dakisolatie, warmtepomp of vloerisolatie. De combi geeft 2x zo veel subsidie per m² glas.'),
            ('Geldt ISDE ook voor nieuwbouw?', 'Nee. De ISDE is alleen voor bestaande woningen die zijn gebouwd vóór 2024.'),
            ('Hoe lang duurt de uitbetaling?', 'RVO streeft naar uitbetaling binnen 8 tot 13 weken na een complete aanvraag. Bij ontbrekende gegevens kan het langer duren.'),
            ('Moet ik ISDE aanvragen vóór of na de plaatsing?', 'Na plaatsing — u heeft de eindfactuur en het betaalbewijs nodig. Maar de subsidieregeling moet wel beschikbaar zijn op het moment van plaatsing.'),
        ],
        'cta_inline_after_h2_index': 3,
        'cta_inline_text': '<strong>Maximale subsidie + zekerheid?</strong><p>Wij berekenen vooraf precies hoeveel ISDE-subsidie u krijgt en helpen kosteloos met de aanvraag. Geen verrassingen.</p>',
        'related': ['kunststof-kozijnen-kosten', 'hr-plus-plus-of-triple-glas', 'schueco-living-82-review'],
    },

    {
        'slug': 'schueco-living-82-review',
        'title': 'Schüco LivIng review: het beste kunststof kozijn van 2026?',
        'meta_desc': 'Onafhankelijke review van Schüco LivIng: 7-kamer, Uf 0,92, RC2. Specs, voor- en nadelen, vergelijking met concurrenten.',
        'category': 'Product review',
        'date': '2026-05-12',
        'modified': '2026-05-24',
        'reading_time': 8,
        'intro_image': 'kunststof-kozijnen-plaatsen',
        'lead': "Schüco LivIng is ons enige kozijnprofiel. Maar waarom? In deze review leggen we eerlijk uit waar het systeem in uitblinkt, wat de nadelen zijn, en hoe het zich verhoudt tot concurrenten als Aluplast, Veka en Deceuninck.",
        'sections': [
            {'id': 'wat-is-living-82', 'h2': 'Wat is Schüco LivIng?', 'body': """
<p>Schüco LivIng is een premium kunststof kozijnprofielsysteem van de Duitse fabrikant <strong>Schüco International KG</strong>, opgericht in 1951 en gevestigd in Bielefeld. Schüco is wereldwijd marktleider in raam-, deur- en gevelsystemen.</p>
<p>De "82" verwijst naar de <strong>bouwdiepte van 82 mm</strong> — dat is breder dan veel concurrenten (vaak 70-76 mm), wat ruimte biedt voor meer luchtkamers en betere isolatie.</p>
"""},
        {'id': 'specs', 'h2': 'Belangrijkste specificaties', 'body': """
<table>
<thead><tr><th>Eigenschap</th><th>Waarde</th></tr></thead>
<tbody>
<tr><td><strong>Aantal kamers</strong></td><td>7 luchtkamers in profieldoorsnede</td></tr>
<tr><td><strong>Bouwdiepte</strong></td><td>82 mm</td></tr>
<tr><td><strong>Uf-waarde (frame)</strong></td><td>0,92 W/m²K</td></tr>
<tr><td><strong>Inbraakwerendheid</strong></td><td>RC2 standaard (RC3 op verzoek)</td></tr>
<tr><td><strong>Afdichting</strong></td><td>EPDM, lasbaar (eerste in industrie)</td></tr>
<tr><td><strong>Versterking</strong></td><td>Stalen versterkingsprofielen</td></tr>
<tr><td><strong>Glasdikte</strong></td><td>HR++ (24 mm) tot triple (52 mm)</td></tr>
<tr><td><strong>Kleurmogelijkheden</strong></td><td>Wit, folie houtnerf, alle RAL-kleuren</td></tr>
<tr><td><strong>Productieland</strong></td><td>Duitsland (Bielefeld)</td></tr>
<tr><td><strong>Garantie</strong></td><td>10 jaar fabrieksgarantie</td></tr>
</tbody>
</table>
<p>Bron: <a href="https://www.schueco.com/nl/architecten/producten/kozijnen-en-beslagen/kunststof/living82" rel="external nofollow noopener">schueco.com — LivIng</a></p>
"""},
        {'id': 'voordelen', 'h2': 'De vijf grootste pluspunten', 'body': """
<h3>1. Top-isolatie</h3>
<p>Met Uf = 0,92 W/m²K zit LivIng in de top-3 van kunststof kozijnen wereldwijd. Combineer met triple glas en je haalt passiefhuis-niveau (Uw < 0,8) zonder dat je naar aluminium of hout hoeft.</p>
<h3>2. Lasbare EPDM-afdichting</h3>
<p>Schüco was de eerste fabrikant die kunststof EPDM-afdichtingen kon lassen. Resultaat: <strong>geen zichtbare hoekverbindingen</strong> in de rubbers, geen waterlek, esthetisch strakker.</p>
<h3>3. RC2 standaard</h3>
<p>De meeste fabrikanten leveren RC1 of "inbraakvertragend" als standaard. Schüco LivIng voldoet standaard aan RC2 — gelijkwaardig aan SKG**.</p>
<h3>4. Beschikbaarheid en levertijd</h3>
<p>Schüco produceert in Duitsland en heeft een grote voorraad. Onze gemiddelde levertijd is 4-6 weken — bij concurrenten vaak 10-14 weken.</p>
<h3>5. 40+ jaar levensduur</h3>
<p>Door de stabiele PVC-formule en UV-bestendigheid hebben deze kozijnen een verwachte levensduur van 40 tot 50 jaar. Goedkope concurrenten zitten op 20-25 jaar.</p>
"""},
        {'id': 'nadelen', 'h2': 'Eerlijke nadelen', 'body': """
<p>Geen product is perfect — ook Schüco LivIng niet:</p>
<h3>1. Niet de goedkoopste keuze</h3>
<p>Schüco zit in het premium segment. Een Duits premium Schüco-kozijn kost 15-30% meer dan een Pools of Turks no-name kozijn. Voor wie puur op aanschafprijs koopt, niet de eerste keuze.</p>
<h3>2. Bouwdiepte 82 mm</h3>
<p>Bij smalle muuropeningen (denk: oude binnenstadwoningen met dikke muren maar smalle dagmaten) kan 82 mm bouwdiepte krap zijn. In ~5% van de projecten kiezen we daarom voor een dunner alternatief.</p>
<h3>3. Strakke uitstraling</h3>
<p>De profielen zijn relatief breed in vergelijking met aluminium. Voor de meest minimalistische look (grote glasvlakken, zeer smalle randen) kies je beter voor Schüco's aluminium-lijn — duurder.</p>
"""},
        {'id': 'vergelijk', 'h2': 'Hoe verhoudt het zich tot concurrenten?', 'body': """
<table>
<thead><tr><th>Systeem</th><th>Bouwdiepte</th><th>Kamers</th><th>Uf-waarde</th><th>Prijs-index</th></tr></thead>
<tbody>
<tr><td><strong>Schüco LivIng</strong></td><td>82 mm</td><td>7</td><td>0,92</td><td>100 (referentie)</td></tr>
<tr><td>Veka Softline 82</td><td>82 mm</td><td>6</td><td>1,0</td><td>95</td></tr>
<tr><td>Deceuninck Zendow 70</td><td>70 mm</td><td>5</td><td>1,3</td><td>80</td></tr>
<tr><td>Aluplast Ideal 7000</td><td>85 mm</td><td>7</td><td>0,95</td><td>92</td></tr>
<tr><td>Kömmerling 76</td><td>76 mm</td><td>5</td><td>1,1</td><td>88</td></tr>
</tbody>
</table>
<p>Schüco LivIng zit qua prijs in het bovensegment maar levert ook bovengemiddelde prestaties. Voor wie het beste van twee werelden wil (kwaliteit + redelijke prijs) is dit ons advies.</p>
"""},
        {'id': 'wanneer', 'h2': 'Wanneer is LivIng de juiste keuze?', 'body': """
<p>Schüco LivIng past goed bij:</p>
<ul>
<li><strong>Renovaties</strong> waar u 25+ jaar in de woning wil blijven</li>
<li><strong>Energie-bewuste huiseigenaren</strong> die naar label A of hoger willen</li>
<li><strong>Inbraakgevoelige locaties</strong> waar RC2/RC3 belangrijk is</li>
<li><strong>Klassieke woningen</strong> waar witte profielen mooi staan</li>
<li><strong>Mensen die kwaliteit boven prijs stellen</strong></li>
</ul>
<p>Minder geschikt voor: zeer beperkt budget (kies dan een goedkoper merk) of wanneer u zeer smalle profielen wenst (kies dan aluminium).</p>
"""},
        ],
        'faq': [
            ('Is Schüco LivIng echt het beste kunststof kozijn?', 'Het zit in de absolute top-3 wereldwijd, samen met Aluplast Ideal 7000 en Veka Softline 82. Welke "de beste" is hangt af van uw prioriteiten (prijs, isolatie, look). Voor de Nederlandse markt vinden wij LivIng de beste balans.'),
            ('Waarom kiest Duurkracht voor Schüco?', 'Drie redenen: bewezen kwaliteit (Schüco kwaliteit sinds 1951), beste isolatie- en inbraakwerendheidswaarden in zijn klasse, en betrouwbare leverbetrouwbaarheid (4-6 weken levertijd).'),
            ('Wat is het verschil tussen LivIng en LivIng MD?', 'LivIng MD is een nog premiumere variant met middelafdichting (3 afdichtingen i.p.v. 2). Iets betere isolatie en geluidsdemping, maar 15-20% duurder. Voor 95% van de woningen volstaat standaard LivIng.'),
            ('Krijg ik kortingsbon van Schüco?', 'Schüco werkt niet met consumentenkortingen — alle leveringen lopen via gecertificeerde dealers zoals wij. Wel hebben wij scherpe inkoop-prijzen door volume.'),
            ('Kan ik Schüco-kozijnen ook in een andere kleur dan wit?', 'Ja. Alle RAL-kleuren zijn mogelijk via folie-coating. Antraciet (RAL 7016) en houtnerf-eiken zijn meest gevraagd. Folie geeft 10-25% meerprijs en heeft een eigen 10-jaar garantie.'),
        ],
        'cta_inline_after_h2_index': 3,
        'cta_inline_text': '<strong>Schüco LivIng voor uw woning?</strong><p>Vraag een vaste offerte aan. Onze adviseur laat u monsters zien en bespreekt opties zoals kleur, glas en sluiting.</p>',
        'related': ['hr-plus-plus-of-triple-glas', 'inbraakwerend-kozijn-rc2-rc3', 'kunststof-kozijnen-kosten'],
    },

    {
        'slug': 'inbraakwerend-kozijn-rc2-rc3',
        'title': 'Inbraakwerend kozijn: alles over RC2, RC3, SKG en PKVW',
        'meta_desc': 'Wat betekenen RC2, RC3, SKG** en PKVW? Inbraakwerendheid van kunststof kozijnen uitgelegd, plus tips voor maximale veiligheid.',
        'category': 'Veiligheid',
        'date': '2026-05-08',
        'modified': '2026-05-24',
        'reading_time': 6,
        'intro_image': 'diensten-deuren',
        'lead': "RC2? SKG**? PKVW? Een wirwar aan termen rond inbraakwerendheid van kozijnen. In deze gids leggen we ze één voor één uit — en geven we praktisch advies over welk niveau u nodig heeft.",
        'sections': [
            {'id': 'wat-is-rc', 'h2': 'Wat zijn de RC-klassen?', 'body': """
<p>De Europese norm <strong>EN 1627</strong> deelt inbraakwerendheid in zes klassen, RC1 tot RC6. Voor woningen zijn vooral RC1 t/m RC3 relevant:</p>
<table>
<thead><tr><th>Klasse</th><th>Bestand tegen</th><th>Toepassing</th></tr></thead>
<tbody>
<tr><td>RC1</td><td>Geweld zonder gereedschap</td><td>Minimum bouwbesluit</td></tr>
<tr><td><strong>RC2</strong></td><td>Inbraak met simpel gereedschap (5 min)</td><td>Standaard woning</td></tr>
<tr><td><strong>RC3</strong></td><td>Inbraak met breekijzer (5 min)</td><td>Inbraakgevoelig gebied</td></tr>
<tr><td>RC4</td><td>Ervaren dief met zwaar gereedschap</td><td>Juwelier, museum</td></tr>
<tr><td>RC5</td><td>Aanval met elektrisch gereedschap</td><td>Bank, kluis</td></tr>
<tr><td>RC6</td><td>Aanval met zware elektrische werktuigen</td><td>Hoogveiligheid</td></tr>
</tbody>
</table>
<blockquote><p>Voor de gemiddelde Nederlandse woning is <strong>RC2</strong> het juiste niveau. In inbraakgevoelige wijken of begane-grond woningen is <strong>RC3</strong> aan te raden.</p></blockquote>
"""},
        {'id': 'wat-is-skg', 'h2': 'En wat is SKG dan?', 'body': """
<p>SKG is de Nederlandse keuringsorganisatie voor inbraakwerendheid. Hun keuringen worden uitgedrukt in <strong>sterren</strong>:</p>
<ul>
<li><strong>SKG*</strong> (1 ster) — basis inbraakwering</li>
<li><strong>SKG**</strong> (2 sterren) — vergelijkbaar met RC2, standaard voor woningen</li>
<li><strong>SKG***</strong> (3 sterren) — vergelijkbaar met RC3, hoogwaardig</li>
</ul>
<p>SKG-sterren worden vaak gebruikt voor <strong>cilinders en sloten</strong>; RC-klassen voor <strong>complete kozijnen of deuren</strong>. In de praktijk wordt vaak gecombineerd: een RC2-kozijn met een SKG**-cilinder.</p>
"""},
        {'id': 'wat-is-pkvw', 'h2': 'En PKVW dan?', 'body': """
<p><strong>PKVW</strong> staat voor <strong>Politiekeurmerk Veilig Wonen</strong>. Dit is een totaalkeurmerk van de Nederlandse politie dat eisen stelt aan:</p>
<ul>
<li>Inbraakwerendheid van kozijnen, ramen, deuren (minimaal SKG**)</li>
<li>Verlichting buiten</li>
<li>Zicht vanuit huis op straat (geen "donkere hoeken")</li>
<li>Hang- en sluitwerk</li>
</ul>
<p>Een woning met <strong>PKVW-certificering</strong> wordt door inbrekers significant vaker overgeslagen. Bonus: veel inboedelverzekeraars geven <strong>5-10% premiekorting</strong> bij PKVW-certificering.</p>
"""},
        {'id': 'onze-kozijnen', 'h2': 'Hoe inbraakwerend zijn onze kozijnen?', 'body': """
<p>Onze Schüco LivIng kozijnen voldoen <strong>standaard aan RC2</strong>. Dat betekent inbegrepen:</p>
<ul>
<li><strong>Stalen versterkingsprofielen</strong> in het kunststof</li>
<li><strong>Meerpuntsluiting</strong> (5 punten op deuren, 2-4 op ramen)</li>
<li><strong>SKG**-cilinders</strong> tegen kerntrekken</li>
<li><strong>Glaslatten aan de binnenkant</strong> — kunnen niet van buiten gewipt worden</li>
<li><strong>Anti-uitlichtbeveiliging</strong> op draai-kiep mechaniek</li>
<li><strong>Verstevigde scharnieren</strong></li>
</ul>
<p>Voor extra zekerheid bieden we:</p>
<ul>
<li>Upgrade naar <strong>RC3</strong> met dikkere staalversterking en zware SKG***-cilinder</li>
<li>Volledige <strong>PKVW-certificering</strong> voor verzekeringskorting</li>
<li><strong>Inbraakwerend glas</strong> (P4A) op begane grond</li>
<li><strong>Smart-locks</strong> met vingerscan of code</li>
</ul>
"""},
        {'id': 'welk-niveau', 'h2': 'Welk niveau heeft u nodig?', 'body': """
<p>Onze pragmatische adviezen:</p>
<h3>RC2 is voldoende voor:</h3>
<ul>
<li>Eerste verdieping en hoger</li>
<li>Woningen op rustige plekken</li>
<li>Buurten met laag inbraakcijfer (check politie.nl/buurtinfo)</li>
</ul>
<h3>RC3 of PKVW is aan te raden voor:</h3>
<ul>
<li>Begane grond met directe straat-toegang</li>
<li>Woningen waar al eens is ingebroken</li>
<li>Wijken met verhoogd inbraakcijfer</li>
<li>Tweede woning of vakantiewoning</li>
<li>Mensen die graag korting op de inboedelverzekering willen</li>
</ul>
<p>Voor de meeste Nederlandse rijwoningen is RC2 voldoende. PKVW is een mooie extra die zichzelf vaak terugverdient via verzekeringskorting.</p>
"""},
        {'id': 'meer-doen', 'h2': 'Wat kunt u verder zelf doen?', 'body': """
<p>Een inbraakwerend kozijn is goud waard, maar werkt het best in combinatie met:</p>
<ul>
<li><strong>Buitenverlichting met bewegingssensor</strong> — schrikt 70% van de dieven af</li>
<li><strong>Slot op alle hang-/dakraampjes</strong> — vaak vergeten</li>
<li><strong>Geen sleutels in zicht</strong> (niet in dichtbije auto, niet onder mat)</li>
<li><strong>Tijdschakelaars op binnenverlichting</strong> tijdens vakantie</li>
<li><strong>Aansluiten op alarm</strong> (Verisure, Vivat, ADT)</li>
</ul>
<p>Volgens politiestatistieken vermindert PKVW-certificering de inbraakkans met <strong>~70%</strong> in vergelijking met niet-gecertificeerde woningen.</p>
"""},
        ],
        'faq': [
            ('Wat is het verschil tussen RC2 en SKG**?', 'In de praktijk vergelijkbaar — beide bieden bescherming tegen inbraak met simpel gereedschap (~5 minuten weerstand). RC is een Europese norm voor kozijnen, SKG een Nederlandse keuring voor cilinders en sloten.'),
            ('Hoeveel korting krijg ik op verzekering met PKVW?', 'Tussen 5% en 10% bij de meeste inboedelverzekeraars. Bij Centraal Beheer, Univé, Interpolis, ASR en Nationale-Nederlanden is dit standaard beleid.'),
            ('Kost RC3 veel meer dan RC2?', 'Ongeveer 10-15% meerprijs op het kozijn. Voor PKVW-certificering komt daar een keuringskostje bij van ~€ 250-500 per woning.'),
            ('Heb ik PKVW nodig in een rustige wijk?', 'Niet strikt nodig, maar wel verstandig als u korting op uw inboedelverzekering wil. De terugverdientijd op PKVW-certificering is meestal 4-7 jaar via verzekeringskorting.'),
            ('Werkt inbraakwering ook tegen woninginbraak met breekijzer?', 'RC2 niet — die is op breekijzer-niveau niet bestand. RC3 wel: bestand tegen 5 minuten breekijzer-aanval. Voor begane grond raden we daarom RC3 aan.'),
        ],
        'cta_inline_after_h2_index': 3,
        'cta_inline_text': '<strong>PKVW-certificering voor uw woning?</strong><p>Onze adviseur kijkt naar uw situatie en buurt, en geeft eerlijk advies of RC2 voldoende is of dat RC3/PKVW slim is.</p>',
        'related': ['schueco-living-82-review', 'kunststof-kozijnen-kosten', 'kunststof-kozijnen-onderhoud'],
    },

    {
        'slug': 'kunststof-kozijnen-onderhoud',
        'title': 'Kunststof kozijnen onderhouden: zo simpel is het',
        'meta_desc': 'Hoe onderhoudt u kunststof kozijnen? Stap-voor-stap gids: schoonmaken, scharnieren, rubbers, kleine reparaties. Niets schilderen, niets schuren.',
        'category': 'Onderhoud',
        'date': '2026-05-04',
        'modified': '2026-05-24',
        'reading_time': 5,
        'intro_image': 'hero-raamkozijnen',
        'lead': "De grote belofte van kunststof kozijnen: onderhoudsarm. Klopt dat ook? Ja — maar 'onderhoudsarm' is niet 'onderhoudsvrij'. In deze gids: precies wat u jaarlijks moet doen om uw kozijnen 40+ jaar in topconditie te houden.",
        'sections': [
            {'id': 'algemeen', 'h2': 'Het 30-seconden overzicht', 'body': """
<p>Kunststof kozijnen vragen verrassend weinig aandacht. De jaarlijkse onderhoudslijst:</p>
<ul>
<li><strong>1x per jaar:</strong> kozijnen en glas grondig schoonmaken (lente)</li>
<li><strong>1x per jaar:</strong> rubbers controleren en eventueel invetten met siliconen-spray</li>
<li><strong>1x per jaar:</strong> scharnieren en sluitwerk smeren met krijt-vet of WD-40 dry</li>
<li><strong>1x per 5 jaar:</strong> grondige controle van kit en afdichting (door uzelf of vakman)</li>
</ul>
<p>Verder: <strong>niet schilderen</strong>, <strong>niet schuren</strong>, <strong>geen agressieve middelen</strong>. Dat is alles.</p>
"""},
        {'id': 'schoonmaken', 'h2': 'Het kozijn schoonmaken (jaarlijks)', 'body': """
<p>Voorjaar is het ideale moment. Wat u nodig heeft:</p>
<ul>
<li>Emmer warm water</li>
<li>Klein scheutje afwasmiddel of allesreiniger (pH-neutraal)</li>
<li>Zachte microvezeldoek</li>
<li>Zachte borstel voor hoeken en groeven</li>
</ul>
<p><strong>Werkwijze:</strong></p>
<ol>
<li>Veeg eerst los stof en spinnenwebben weg met een droge doek</li>
<li>Maak het sopje en sop het kozijn af</li>
<li>Gebruik de zachte borstel voor groeven, rubbers en sponningen</li>
<li>Veeg na met een schone doek</li>
<li>Vergeet het glas niet — gebruik daarvoor glazenwasser of azijn-water</li>
</ol>
<blockquote><p><strong>Niet doen:</strong> harde sponzen, scheuvies, schuurmiddelen, agressieve oplosmiddelen (aceton, terpentine, ammonia). Die kunnen de kunststof beschadigen.</p></blockquote>
"""},
        {'id': 'rubbers', 'h2': 'Rubbers en afdichtingen', 'body': """
<p>De EPDM-rubbers rondom uw kozijnen zorgen voor luchtdichtheid en waterkering. Bij onze Schüco LivIng zijn deze rubbers lasbaar — dus zonder zichtbare hoeknaden — wat ze duurzamer maakt.</p>
<p>Wat u jaarlijks doet:</p>
<ol>
<li>Inspecteer de rubbers op uitdroging, scheuren of vervorming</li>
<li>Maak ze schoon met een vochtige doek</li>
<li>Sprayed eens per 2-3 jaar een dun laagje <strong>siliconen-spray</strong> op de rubbers</li>
<li>Niet smeren met vet of olie — die tasten de rubber aan</li>
</ol>
<p>Goed onderhouden rubbers gaan <strong>20+ jaar</strong> mee. Vervangen kan altijd later — kost ca. € 50-100 per kozijn.</p>
"""},
        {'id': 'beslag', 'h2': 'Scharnieren en sluitwerk', 'body': """
<p>Het beslag (scharnieren, kruk-mechaniek, meerpuntsluiting) zorgt voor de soepele werking. Onderhoud:</p>
<ol>
<li><strong>Smeer 1x per jaar</strong> met krijt-vet, slot-spray (WD-40 specialist), of een tandwielspray</li>
<li><strong>Niet smeren</strong> met gewone WD-40 (te dun, trekt vuil aan) of plantaardige olie</li>
<li>Spuit kort op het mechaniek, beweeg het slot enkele keren heen en weer</li>
<li>Veeg overtollig vet af</li>
</ol>
<p>Doet uw kruk stroef, of valt het slot niet meer goed in? Vaak gewoon een kwestie van schoonmaken en smeren. Helpt niet? Bel ons — vaak een kleine reparatie.</p>
"""},
        {'id': 'kleur', 'h2': 'Kleurvastheid: gaat antraciet niet verbleken?', 'body': """
<p>Een veelgehoorde zorg over kunststof kozijnen: <strong>verbleekt antraciet niet onder de zon?</strong> Vroeger soms wel — bij oudere PVC-formuleringen. Bij Schüco LivIng niet, want:</p>
<ul>
<li>De folie-laag is <strong>UV-stabiel tot 25 jaar</strong> (10 jaar fabrieksgarantie van Schüco)</li>
<li>Bij witte kozijnen geen probleem (wit blijft wit)</li>
<li>Bij folie-kleuren (antraciet, eikenhout): minimaal kleurverlies van &lt;5% in 20 jaar</li>
</ul>
<p>Op dakkapellen of in volle zon: maak ze 2x per jaar schoon — dan zien ze er over 20 jaar nog steeds top uit.</p>
"""},
        {'id': 'reparatie', 'h2': 'Kleine schade zelf repareren', 'body': """
<p>Lichte schade kun je vaak zelf oplossen:</p>
<h3>Krassen</h3>
<p>Hele lichte krasjes (alleen in folie-laag) kunnen weg met een speciale kunststof-polish (te koop bij bouwmarkt). Diepere krassen blijven zichtbaar; vervangen van het paneel is dan de enige optie.</p>
<h3>Verkleuring</h3>
<p>Hardnekkige vlekken (vet, nicotine) gaan vaak weg met een mild kunststof-reiniger. Bij wit ook geel-verkleuring? Probeer waterstofperoxide (3%) — een wattenpadje 30 minuten erop laten zitten.</p>
<h3>Slot werkt niet meer</h3>
<p>Vaak schoonmaken + smeren. Werkt het nog niet? Bel onze service.</p>
<h3>Vochtige plekken binnen het glas</h3>
<p>Dit is condens binnenin de spouw — een teken dat de glasafdichting kapot is. Vervanging van het glaspakket is dan nodig (~€ 200-400 per ruit).</p>
"""},
        ],
        'faq': [
            ('Hoe vaak moet ik kunststof kozijnen schoonmaken?', '1x per jaar grondig (lente), eventueel 2x bij dakkapellen of zon-exposed zijde. Dagelijks schoonpoetsen is niet nodig.'),
            ('Mag ik schoonmaakmiddelen met chloor gebruiken?', 'Liever niet — chloor kan de kunststof aantasten over tijd. Gebruik een mild allesreiniger of pH-neutraal sopje.'),
            ('Moet ik de rubbers vervangen?', 'Pas na 20+ jaar of bij zichtbare schade (scheuren, uitdroging). Onderhoud (siliconen-spray) verlengt de levensduur.'),
            ('Wat doe ik bij scheurtjes in het kozijn?', 'Bij kleine oppervlakkige scheurtjes is dat meestal cosmetisch. Bij diepe scheuren in het profiel: meld bij ons binnen garantietermijn (10 jaar).'),
            ('Hoe weet ik of mijn glasafdichting nog goed is?', 'Geen condens binnen het glas, geen tocht voelbaar bij geluiden van wind. Bij condens binnenin: glas vervangen.'),
        ],
        'cta_inline_after_h2_index': 3,
        'cta_inline_text': '<strong>Service nodig op bestaande Duurkracht-kozijnen?</strong><p>Bel ons op 085 073 1660. Binnen garantietermijn (10 jaar) komen wij kosteloos langs voor onderhoud of reparatie.</p>',
        'related': ['schueco-living-82-review', 'kunststof-kozijnen-kosten', 'inbraakwerend-kozijn-rc2-rc3'],
    },
]


# ============================================================
# RENDER ARTIKEL
# ============================================================

def render_article(post):
    slug = post['slug']
    title = post['title']
    meta_desc = post['meta_desc']
    cat = post['category']
    date = post['date']
    modified = post['modified']
    reading_time = post['reading_time']
    lead = post['lead']
    intro_img = post['intro_image']

    # JSON-LD Article schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": f"https://www.duurkrachtkozijnen.nl/blog/{slug}/#article",
        "headline": title,
        "description": meta_desc,
        "image": f"https://www.duurkrachtkozijnen.nl/design-assets/images/{intro_img}.jpg",
        "datePublished": date,
        "dateModified": modified,
        "author": {"@type": "Organization", "name": "Duurkracht Kozijnen B.V.", "@id": "https://www.duurkrachtkozijnen.nl/#organization"},
        "publisher": {"@type": "Organization", "name": "Duurkracht Kozijnen B.V.", "@id": "https://www.duurkrachtkozijnen.nl/#organization", "logo": {"@type":"ImageObject","url":"https://www.duurkrachtkozijnen.nl/design-assets/Logo-duurkracht-kozijnen.svg"}},
        "mainEntityOfPage": {"@type":"WebPage","@id":f"https://www.duurkrachtkozijnen.nl/blog/{slug}/"},
        "articleSection": cat,
        "inLanguage": "nl-NL",
        "wordCount": sum(len(s['body'].split()) for s in post['sections'])
    }

    breadcrumb_schema = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://www.duurkrachtkozijnen.nl/"},
            {"@type":"ListItem","position":2,"name":"Blog","item":"https://www.duurkrachtkozijnen.nl/blog/"},
            {"@type":"ListItem","position":3,"name":title,"item":f"https://www.duurkrachtkozijnen.nl/blog/{slug}/"}
        ]
    }

    faq_schema = {
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in post['faq']]
    }

    schemas = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [article_schema, breadcrumb_schema, faq_schema])

    # TOC
    toc_items = ''.join(f'<li><a href="#{s["id"]}">{s["h2"]}</a></li>' for s in post['sections'])
    toc_items += '<li><a href="#faq-section">Veelgestelde vragen</a></li>'

    # Body sections
    body_html = ''
    inline_cta_idx = post.get('cta_inline_after_h2_index', -1)
    for i, s in enumerate(post['sections']):
        body_html += f'<h2 id="{s["id"]}">{s["h2"]}</h2>\n{s["body"]}\n'
        if i == inline_cta_idx:
            body_html += f'''<div class="article-cta">
  <div class="ic"><img src="/design-assets/icons/icon-adviesgesprek-op-locatie.svg" alt="" /></div>
  <div class="text">{post["cta_inline_text"]}</div>
  <a href="/contact/" class="btn btn-primary">Plan afspraak <span class="arrow">→</span></a>
</div>'''

    # FAQ
    faq_html = '<h2 id="faq-section">Veelgestelde vragen</h2>\n<div class="faq-list" style="border-top: 1px solid var(--ink); margin-top: 16px;">\n'
    for i, (q, a) in enumerate(post['faq']):
        opn = ' open' if i == 0 else ''
        faq_html += f'<details class="faq-item"{opn}><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>\n'
    faq_html += '</div>'

    # Related posts
    related_html = ''
    related_lookup = {p['slug']: p for p in POSTS}
    if post.get('related'):
        for r_slug in post['related']:
            if r_slug in related_lookup:
                r = related_lookup[r_slug]
                related_html += f'''<a href="/blog/{r["slug"]}/" class="blog-card">
        <div class="ph">"{r["title"]}"</div>
        <div class="body">
          <div class="cat">{r["category"]}</div>
          <h3>{r["title"]}</h3>
          <p>{r["meta_desc"][:120]}...</p>
          <span class="read">Lees artikel <span class="arrow">→</span></span>
        </div>
      </a>'''

    return f'''<!DOCTYPE html>
<html lang="nl-NL">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>{title} | Duurkracht Kozijnen</title>
<meta name="description" content="{meta_desc}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="https://www.duurkrachtkozijnen.nl/blog/{slug}/" />
<meta name="theme-color" content="#0B5A2B" />
<meta name="author" content="Duurkracht Kozijnen B.V." />

<meta property="og:type" content="article" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="https://www.duurkrachtkozijnen.nl/blog/{slug}/" />
<meta property="og:image" content="https://www.duurkrachtkozijnen.nl/design-assets/images/{intro_img}.jpg" />
<meta property="article:published_time" content="{date}" />
<meta property="article:modified_time" content="{modified}" />
<meta property="article:section" content="{cat}" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..800,30..100,0..1;1,9..144,400..800,30..100,0..1&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/site.css" />
<link rel="icon" type="image/svg+xml" href="/design-assets/beelmerkje-klein.svg" />

{schemas}
{BLOG_CSS}

</head>
<body>

<a href="#main" class="skip">Direct naar inhoud</a>

{topbar()}
{nav('blog')}

<div class="post-meta-bar">
  <div class="container">
    <span class="crumb"><a href="/" style="color:var(--green);">Home</a> › <a href="/blog/" style="color:var(--green);">Blog</a> › {cat}</span>
    <div class="meta-right">
      <span>Gepubliceerd: {date}</span>
      <span>Laatst bijgewerkt: {modified}</span>
      <span>{reading_time} min lezen</span>
    </div>
  </div>
</div>

<main id="main">

<section class="blog-hero">
  <div class="container">
    <span class="eyebrow">{cat} · {reading_time} min lezen</span>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>

<div class="container">
<div class="article-layout">

  <aside class="toc" aria-label="Inhoudsopgave">
    <h4>Inhoud</h4>
    <ul>{toc_items}</ul>
  </aside>

  <article class="article-body">
    {body_html}
    {faq_html}

    <div class="author-card">
      <div class="avatar">D</div>
      <div class="info">
        <strong>Duurkracht Kozijnen B.V.</strong>
        <span>Specialist sinds 2003 · Hassinkweg 1, Hengelo</span>
      </div>
    </div>
  </article>

</div>
</div>

{f'<section class="related-posts"><div class="container"><h3>Verwante artikelen</h3><div class="blog-grid">{related_html}</div></div></section>' if related_html else ''}

<section class="cta-banner">
  <div class="container">
    <div>
      <span class="eyebrow">Vragen na het lezen?</span>
      <h2>Plan een gratis<br><span class="em-italic">adviesgesprek aan huis.</span></h2>
      <p>Onze adviseur komt vrijblijvend langs, beantwoordt al uw vragen over kozijnen en geeft een vaste offerte.</p>
    </div>
    <div class="cta-banner-actions">
      <a href="/contact/" class="btn btn-primary">Plan afspraak <span class="arrow">→</span></a>
      <a href="tel:+31850731660" class="btn btn-ghost-white" rel="nofollow">Of bel: 085 073 1660</a>
      <p class="meta-line">Gemiddelde reactietijd: <strong>onder de 4 uur</strong> op werkdagen.</p>
    </div>
  </div>
</section>

</main>

{footer()}

</body>
</html>
'''


def render_landing():
    """Blog overzicht pagina"""
    cards = ''
    for p in sorted(POSTS, key=lambda x: x['date'], reverse=True):
        cards += f'''<a href="/blog/{p["slug"]}/" class="blog-card">
        <div class="ph"><img src="/design-assets/images/{p["intro_image"]}.jpg" alt="{p["title"]}" loading="lazy" /></div>
        <div class="body">
          <div class="cat">{p["category"]}</div>
          <div class="date">{p["date"]} · {p["reading_time"]} min lezen</div>
          <h3>{p["title"]}</h3>
          <p>{p["meta_desc"][:120]}...</p>
          <span class="read">Lees artikel <span class="arrow">→</span></span>
        </div>
      </a>'''

    blog_schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": "https://www.duurkrachtkozijnen.nl/blog/#blog",
        "name": "Duurkracht Kozijnen Blog",
        "description": "Praktisch advies over kunststof kozijnen, deuren, schuifpuien en gevelbekleding.",
        "publisher": {"@type":"Organization","name":"Duurkracht Kozijnen B.V.","@id":"https://www.duurkrachtkozijnen.nl/#organization"},
        "blogPost": [{"@type":"BlogPosting","@id":f"https://www.duurkrachtkozijnen.nl/blog/{p['slug']}/#article","headline":p['title'],"datePublished":p['date']} for p in POSTS]
    }

    breadcrumb = {
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://www.duurkrachtkozijnen.nl/"},
            {"@type":"ListItem","position":2,"name":"Blog","item":"https://www.duurkrachtkozijnen.nl/blog/"}
        ]
    }

    schemas = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [blog_schema, breadcrumb])

    return f'''<!DOCTYPE html>
<html lang="nl-NL">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>Blog & Advies — Praktisch over kunststof kozijnen | Duurkracht Kozijnen</title>
<meta name="description" content="Praktisch advies over kunststof kozijnen, deuren, schuifpuien en gevelbekleding. Prijzen, subsidies, productadvies en onderhoudstips." />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="https://www.duurkrachtkozijnen.nl/blog/" />
<meta name="theme-color" content="#0B5A2B" />

<meta property="og:type" content="website" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:title" content="Blog & Advies — Duurkracht Kozijnen" />
<meta property="og:description" content="Praktische gidsen over kozijnen, glas, subsidies en onderhoud." />
<meta property="og:url" content="https://www.duurkrachtkozijnen.nl/blog/" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..800,30..100,0..1;1,9..144,400..800,30..100,0..1&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/site.css" />
<link rel="icon" type="image/svg+xml" href="/design-assets/beelmerkje-klein.svg" />

{schemas}
{BLOG_CSS}

</head>
<body>

<a href="#main" class="skip">Direct naar inhoud</a>

{topbar()}
{nav('blog')}

<nav class="breadcrumb"><div class="container"><ol><li><a href="/">Home</a></li><li>Blog</li></ol></div></nav>

<main id="main">

<section class="blog-hero">
  <div class="container">
    <span class="eyebrow">Blog &amp; Advies</span>
    <h1>Praktisch advies <span class="em-italic">over kozijnen,</span> glas en subsidies.</h1>
    <p class="lead">
      Verdieping op {len(POSTS)} onderwerpen rond kunststof kozijnen — geschreven door onze vakmensen op basis van 20+ jaar ervaring en geverifieerde productinformatie van Schüco, Keralit en RVO.
    </p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="blog-grid">
      {cards}
    </div>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <div>
      <span class="eyebrow">Mist u een onderwerp?</span>
      <h2>Stel uw vraag <span class="em-italic">direct.</span></h2>
      <p>Heeft u een specifieke vraag die u in een artikel zou willen lezen? Of wilt u persoonlijk advies? Bel ons of plan een gratis adviesgesprek.</p>
    </div>
    <div class="cta-banner-actions">
      <a href="/contact/" class="btn btn-primary">Stel uw vraag <span class="arrow">→</span></a>
      <a href="tel:+31850731660" class="btn btn-ghost-white" rel="nofollow">Of bel: 085 073 1660</a>
    </div>
  </div>
</section>

</main>

{footer()}

</body>
</html>
'''


# ============================================================
# BUILD
# ============================================================

print(f'Building blog ({len(POSTS)} artikelen + landing)...')
(BLOG / 'index.html').write_text(render_landing(), encoding='utf-8')
print(f'  ✓ blog/index.html')

for post in POSTS:
    out = BLOG / post['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_article(post), encoding='utf-8')
    words = sum(len(s['body'].split()) for s in post['sections'])
    print(f'  ✓ blog/{post["slug"]}/  ({words} woorden, {post["reading_time"]} min)')

print('Done.')
