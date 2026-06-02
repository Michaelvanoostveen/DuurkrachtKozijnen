#!/usr/bin/env python3
"""
Build script voor locatie-pagina's van Duurkracht Kozijnen.
Genereert /kunststof-kozijnen-{slug}/index.html voor elke locatie.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent

# ============================================================
# LOCATIE DATA — geverifieerde info per plaats
# Lat/lon via openstreetmap, provincie via wettelijke indeling
# ============================================================
LOCATIONS = [
    {
        'slug': 'hengelo', 'name': 'Hengelo', 'province': 'Overijssel', 'region': 'Twente',
        'lat': 52.2660, 'lon': 6.7935,
        'rijtijd': 0, 'afstand_km': 0,
        'intro': 'Hengelo is onze thuisbasis — sinds 2003 staat onze werkplaats aan de Hassinkweg. Wij plaatsen kozijnen in alle wijken van Hengelo, van Hasseler Es tot Slangenbeek, van de Berflo Es tot Woolde.',
        'usp_extra': 'thuisbasis · korte lijntjes · vaak nog dezelfde week beschikbaar',
        'wijken': ['Hasseler Es', 'Slangenbeek', 'Berflo Es', 'Woolde', 'Wilderinkshoek', 'Klein Driene'],
        'recent_project': 'jaren-30 woning aan de Vondellaan',
        'inwoners': '83.000',
    },
    {
        'slug': 'enschede', 'name': 'Enschede', 'province': 'Overijssel', 'region': 'Twente',
        'lat': 52.2215, 'lon': 6.8937,
        'rijtijd': 15, 'afstand_km': 11,
        'intro': 'Enschede is een vaste klant van Duurkracht. Wij plaatsen er kozijnen in heel diverse woningen — van de monumentale gevels in het centrum tot moderne nieuwbouw op het oude Polaroid-terrein.',
        'usp_extra': 'op 15 min rijden vanaf onze werkplaats',
        'wijken': ['Stadsveld', 'Stroinkslanden', 'Wesselerbrink', "'t Zwering", 'Pathmos', 'Roombeek'],
        'recent_project': 'antraciet voordeur met erker in Roombeek',
        'inwoners': '162.000',
    },
    {
        'slug': 'almelo', 'name': 'Almelo', 'province': 'Overijssel', 'region': 'Twente',
        'lat': 52.3508, 'lon': 6.6627,
        'rijtijd': 20, 'afstand_km': 18,
        'intro': 'In Almelo verzorgen wij kozijnenrenovaties in alle wijken — van Schelfhorst tot Aalderinkshoek. De jaren-70 en -80 woningen daar zijn vaak toe aan een isolatie-upgrade die zich snel terugverdient.',
        'usp_extra': 'specialist in jaren-70 en -80 renovaties',
        'wijken': ['Schelfhorst', 'Aalderinkshoek', 'De Riet', 'Windmolenbroek', 'Nieuwstraatkwartier', 'Sluitersveld'],
        'recent_project': '11 kozijnen op nieuwbouw in Aalderinkshoek',
        'inwoners': '74.000',
    },
    {
        'slug': 'oldenzaal', 'name': 'Oldenzaal', 'province': 'Overijssel', 'region': 'Twente',
        'lat': 52.3132, 'lon': 6.9292,
        'rijtijd': 18, 'afstand_km': 14,
        'intro': 'Oldenzaal heeft een mooie mix van traditionele Twentse woningen en moderne uitbreidingen. Wij plaatsen kozijnen waarbij we het karakter respecteren — bijvoorbeeld witte profielen met houtnerf bij klassieke gevels.',
        'usp_extra': 'oog voor karakter van Twentse woningen',
        'wijken': ['De Thij', 'Zuid-Berghuizen', 'Glanerbrug', 'Berghuizen', 'Graven Es'],
        'recent_project': 'witte kozijnen met antraciet voordeur in De Thij',
        'inwoners': '32.000',
    },
    {
        'slug': 'borne', 'name': 'Borne', 'province': 'Overijssel', 'region': 'Twente',
        'lat': 52.3013, 'lon': 6.7488,
        'rijtijd': 10, 'afstand_km': 7,
        'intro': 'Borne ligt op een kwartiertje van onze werkplaats. Veel klanten hier kiezen voor complete gevelvernieuwing met Keralit bekleding én nieuwe kozijnen in één keer — efficiënt en kostenbesparend.',
        'usp_extra': 'graag complete gevelpakketten (kozijnen + Keralit)',
        'wijken': ['Centrum', 'Letterveld', 'Bornsche Maten', "'t Slot"],
        'recent_project': 'Keralit gevelbekleding + 6 kozijnen in Bornsche Maten',
        'inwoners': '24.000',
    },
    {
        'slug': 'deventer', 'name': 'Deventer', 'province': 'Overijssel', 'region': 'Salland',
        'lat': 52.2660, 'lon': 6.1552,
        'rijtijd': 55, 'afstand_km': 56,
        'intro': 'Deventer kent veel monumentale en karakteristieke woningen, vooral in het centrum. Wij plaatsen kunststof kozijnen die qua uitstraling perfect aansluiten bij de bestaande architectuur.',
        'usp_extra': 'ervaring met historische binnenstadwoningen',
        'wijken': ['Borgele', 'Diepenveen', 'Schalkhaar', 'Colmschate', 'Voorstad', 'Keizerslanden'],
        'recent_project': 'witte profielen in een 19e-eeuwse villa in Voorstad',
        'inwoners': '102.000',
    },
    {
        'slug': 'zwolle', 'name': 'Zwolle', 'province': 'Overijssel', 'region': 'IJsselland',
        'lat': 52.5168, 'lon': 6.0830,
        'rijtijd': 65, 'afstand_km': 67,
        'intro': 'Zwolle is een groeiende stad met veel nieuwbouwprojecten in Stadshagen en Berkum. Daar plaatsen wij regelmatig moderne kunststof kozijnen die zorgen voor meer comfort, minder warmteverlies en een strakke uitstraling.',
        'usp_extra': 'specialist in moderne nieuwbouw en goed isolerende beglazing',
        'wijken': ['Stadshagen', 'Berkum', 'Aa-landen', 'Zwolle-Zuid', 'Diezerpoort', 'Holtenbroek'],
        'recent_project': 'Hefschuif 5m in moderne villa in Berkum',
        'inwoners': '129.000',
    },
    {
        'slug': 'apeldoorn', 'name': 'Apeldoorn', 'province': 'Gelderland', 'region': 'Veluwe',
        'lat': 52.2112, 'lon': 5.9699,
        'rijtijd': 75, 'afstand_km': 80,
        'intro': 'Apeldoorn ligt op anderhalf uur rijden vanaf onze werkplaats, maar door onze efficiënte planning kunnen we hier perfect uit de voeten. Veel klanten kiezen voor combinatie kozijnen + gevelbekleding.',
        'usp_extra': 'ervaring met grote renovatiepakketten',
        'wijken': ['Zuid', 'Noord', 'Berg en Bos', 'De Maten', 'Osseveld', 'Zevenhuizen'],
        'recent_project': 'antraciet schuifpui met overkapping in De Maten',
        'inwoners': '166.000',
    },
    {
        'slug': 'arnhem', 'name': 'Arnhem', 'province': 'Gelderland', 'region': 'Veluwe',
        'lat': 51.9851, 'lon': 5.8987,
        'rijtijd': 90, 'afstand_km': 105,
        'intro': 'In Arnhem werken wij vaak aan stadse rijwoningen met moderne uitstraling. Antraciet kunststof kozijnen met een stevige, veilige voordeur zijn hier een veelgevraagde combinatie.',
        'usp_extra': 'extra aandacht voor veiligheid en nette entree-afwerking',
        'wijken': ['Presikhaaf', 'Malburgen', 'Schuytgraaf', 'Geitenkamp', 'Klarendal', 'Spijkerkwartier'],
        'recent_project': 'modern stadshuis met antraciet voorgevel in Schuytgraaf',
        'inwoners': '164.000',
    },
    {
        'slug': 'assen', 'name': 'Assen', 'province': 'Drenthe', 'region': 'Drenthe',
        'lat': 52.9961, 'lon': 6.5625,
        'rijtijd': 95, 'afstand_km': 100,
        'intro': 'Assen kent veel ruime jaren-70 en -80 woningen waar isolatie aanzienlijk verbeterd kan worden. Nieuwe kunststof kozijnen kunnen hier direct verschil maken in warmte, tocht en wooncomfort.',
        'usp_extra': 'specialist in jaren-70/80 isolatie-upgrades',
        'wijken': ['Marsdijk', 'Pittelo', 'Kloosterveen', 'Peelo', 'De Lariks', 'Assen-Oost'],
        'recent_project': '8 kozijnen vervangen in Kloosterveen — energielabel van D naar A',
        'inwoners': '69.000',
    },
    {
        'slug': 'emmen', 'name': 'Emmen', 'province': 'Drenthe', 'region': 'Drenthe',
        'lat': 52.7858, 'lon': 6.8975,
        'rijtijd': 80, 'afstand_km': 80,
        'intro': 'In Emmen werken wij regelmatig aan vrijstaande woningen in Bargeres en Emmerhout. Veel klanten combineren kozijnen-vervanging met Keralit gevelbekleding voor een complete modernisering.',
        'usp_extra': 'complete gevelpakketten kozijnen + Keralit',
        'wijken': ['Bargeres', 'Emmerhout', 'Angelslo', 'Rietlanden', 'Delftlanden', 'Centrum'],
        'recent_project': 'complete gevelombouw in Emmerhout',
        'inwoners': '107.000',
    },
    {
        'slug': 'hoogeveen', 'name': 'Hoogeveen', 'province': 'Drenthe', 'region': 'Drenthe',
        'lat': 52.7225, 'lon': 6.4778,
        'rijtijd': 75, 'afstand_km': 75,
        'intro': 'Hoogeveen heeft veel ruime gezinswoningen waar moderne kunststof kozijnen een grote upgrade betekenen op zowel comfort als energierekening.',
        'usp_extra': 'persoonlijk advies, ook bij grotere projecten',
        'wijken': ['Krakeel', 'Erflanden', 'Schoonvelde', 'Wolfsbos', 'Tiendeveen'],
        'recent_project': 'goed isolerende kunststof kozijnen op rijwoning in Erflanden',
        'inwoners': '56.000',
    },
    {
        'slug': 'leeuwarden', 'name': 'Leeuwarden', 'province': 'Friesland', 'region': 'Friesland',
        'lat': 53.2012, 'lon': 5.7999,
        'rijtijd': 110, 'afstand_km': 130,
        'intro': 'In Leeuwarden plaatsen wij regelmatig kozijnen in historische binnenstadwoningen. Onze kunststof profielen kunnen perfect afgewerkt worden om bij monumentale architectuur te passen.',
        'usp_extra': 'oog voor monumentale binnenstadgevels',
        'wijken': ['Aldlân', 'Bilgaard', 'Camminghaburen', 'Westeinde', 'Vlietzone'],
        'recent_project': 'kunststof kozijnen met houtnerf in Aldlân',
        'inwoners': '125.000',
    },
    {
        'slug': 'heerenveen', 'name': 'Heerenveen', 'province': 'Friesland', 'region': 'Friesland',
        'lat': 52.9594, 'lon': 5.9180,
        'rijtijd': 100, 'afstand_km': 115,
        'intro': 'Heerenveen is een populaire bestemming voor onze monteurs. Wij combineren bezoeken regelmatig met andere Friese opdrachten zodat de reiskosten beperkt blijven.',
        'usp_extra': 'efficiënte planning voor Friese regio',
        'wijken': ['Skoatterwâld', 'De Greiden', 'Heerenveen-Centrum', 'De Akkers'],
        'recent_project': 'voor- en achtergevel compleet vernieuwd in Skoatterwâld',
        'inwoners': '50.000',
    },
    {
        'slug': 'drachten', 'name': 'Drachten', 'province': 'Friesland', 'region': 'Friesland',
        'lat': 53.1109, 'lon': 6.0989,
        'rijtijd': 105, 'afstand_km': 115,
        'intro': 'Drachten heeft veel jaren-80 woningen die perfect geschikt zijn voor een comfortupgrade. Wij plaatsen daar regelmatig kunststof kozijnen met goed isolerend glas.',
        'usp_extra': 'jaren-80 woningen — onze specialiteit',
        'wijken': ['De Drait', 'De Wiken', 'De Bouwen', 'Burgum', 'Drachten-Oost'],
        'recent_project': '12 kozijnen + Keralit gevel in De Drait',
        'inwoners': '46.000',
    },
    {
        'slug': 'lelystad', 'name': 'Lelystad', 'province': 'Flevoland', 'region': 'Flevoland',
        'lat': 52.5185, 'lon': 5.4714,
        'rijtijd': 100, 'afstand_km': 130,
        'intro': 'Lelystad is een relatief jonge stad met veel uniforme jaren-70/80 wijken. Hier kunnen we vaak werken met standaard maatvoering, wat de doorlooptijd verkort.',
        'usp_extra': 'standaard maatvoering, snelle doorlooptijd',
        'wijken': ['Atolwijk', 'Boswijk', 'Waterwijk', 'Zuiderzeewijk', 'De Landerijen'],
        'recent_project': '9 kozijnen met antraciet voordeur in Atolwijk',
        'inwoners': '83.000',
    },
    {
        'slug': 'almere', 'name': 'Almere', 'province': 'Flevoland', 'region': 'Flevoland',
        'lat': 52.3508, 'lon': 5.2647,
        'rijtijd': 110, 'afstand_km': 150,
        'intro': 'Almere is een uitgestrekte stad met veel verschillende wijken. Wij werken er regelmatig aan moderne stadswoningen waar antraciet kunststof kozijnen erg populair zijn.',
        'usp_extra': 'antraciet kozijnen erg populair in Almere',
        'wijken': ['Stad', 'Buiten', 'Haven', 'Poort', 'Hout'],
        'recent_project': 'antraciet schuifpui 4m in Almere Poort',
        'inwoners': '218.000',
    },
    {
        'slug': 'utrecht', 'name': 'Utrecht', 'province': 'Utrecht', 'region': 'Utrecht',
        'lat': 52.0907, 'lon': 5.1214,
        'rijtijd': 130, 'afstand_km': 160,
        'intro': 'Utrecht heeft een prachtige mix van historische binnenstad en moderne nieuwbouw. Wij plaatsen kunststof kozijnen waarbij we het karakter van de buurt altijd respecteren.',
        'usp_extra': 'respect voor buurt-architectuur',
        'wijken': ['Lunetten', 'Kanaleneiland', 'Overvecht', 'Leidsche Rijn', 'Vleuten-De Meern', 'Tuinwijk'],
        'recent_project': 'witte kozijnen in jaren-30 huis in Tuinwijk',
        'inwoners': '361.000',
    },
    {
        'slug': 'den-haag', 'name': 'Den Haag', 'province': 'Zuid-Holland', 'region': 'Randstad',
        'lat': 52.0705, 'lon': 4.3007,
        'rijtijd': 145, 'afstand_km': 200,
        'intro': 'In Den Haag werken wij regelmatig aan klassieke stadswoningen en moderne appartementen. Onze ervaring met VvE-trajecten komt hier vaak van pas.',
        'usp_extra': 'ervaring met VvE-trajecten',
        'wijken': ['Loosduinen', 'Mariahoeve', 'Bezuidenhout', 'Statenkwartier', 'Ypenburg', 'Wateringse Veld'],
        'recent_project': 'VvE-renovatie met 38 kozijnen in Bezuidenhout',
        'inwoners': '562.000',
    },
    {
        'slug': 'rotterdam', 'name': 'Rotterdam', 'province': 'Zuid-Holland', 'region': 'Randstad',
        'lat': 51.9244, 'lon': 4.4777,
        'rijtijd': 150, 'afstand_km': 220,
        'intro': 'Rotterdam heeft veel moderne architectuur waarbij strakke antraciet kunststof kozijnen perfect passen. Wij plaatsen regelmatig hefschuif-systemen in penthouse-aanbouwen.',
        'usp_extra': 'hefschuif-systemen voor moderne architectuur',
        'wijken': ['Hillegersberg', 'Kralingen', 'Prinsenland', 'Nesselande', 'Lombardijen', 'Charlois'],
        'recent_project': 'hefschuif 6m + Keralit op penthouse in Nesselande',
        'inwoners': '655.000',
    },
    {
        'slug': 'nijmegen', 'name': 'Nijmegen', 'province': 'Gelderland', 'region': 'Nijmegen',
        'lat': 51.8426, 'lon': 5.8546,
        'rijtijd': 95, 'afstand_km': 105,
        'intro': 'Nijmegen is de oudste stad van Nederland en heeft een rijke mix van historische grachtenpanden en moderne uitbreidingen zoals de Waalsprong. Wij plaatsen Schüco LivIng kozijnen die passen bij elk woningtype — van klassiek tot modern.',
        'usp_extra': 'ervaring met zowel historische als moderne woningtypen',
        'wijken': ['Centrum', 'Waalsprong', 'Dukenburg', 'Lindenholt', 'Neerbosch-Oost', 'Hatert'],
        'recent_project': 'schuifpui en 8 kozijnen in een jaren-30 woning in Hatert',
        'inwoners': '180.000',
    },
    {
        'slug': 'groningen', 'name': 'Groningen', 'province': 'Groningen', 'region': 'Groningen',
        'lat': 53.2194, 'lon': 6.5665,
        'rijtijd': 120, 'afstand_km': 140,
        'intro': 'Groningen is een levendige studentenstad met een grote woningmarkt. Veel woningen uit de jaren 50-70 zijn toe aan een isolatie-upgrade. Wij rijden naar Groningen voor projecten vanaf 4 kozijnen.',
        'usp_extra': 'energiebesparing bij oudere Groningse woningbouw',
        'wijken': ['Paddepoel', 'Selwerd', 'De Wijert', 'Beijum', 'Corpus den Hoorn', 'Stad'],
        'recent_project': '12 kozijnen in een jaren-60 rijtjeswoning in Paddepoel',
        'inwoners': '235.000',
    },
    {
        'slug': 'amsterdam', 'name': 'Amsterdam', 'province': 'Noord-Holland', 'region': 'Randstad',
        'lat': 52.3676, 'lon': 4.9041,
        'rijtijd': 130, 'afstand_km': 155,
        'intro': 'Amsterdam heeft een enorme variatie aan woningtypen — van grachtenpanden tot moderne appartementen in IJburg. Wij plaatsen Schüco LivIng kozijnen in Amsterdam voor projecten waarbij kwaliteit en minimale overlast centraal staan.',
        'usp_extra': 'specialist in projecten met beperkte bereikbaarheid en inrijverbod',
        'wijken': ['Oost', 'West', 'Noord', 'Nieuw-West', 'IJburg', 'Bos en Lommer'],
        'recent_project': 'antraciet kozijnen en voordeur in een 1930s woning in Oost',
        'inwoners': '930.000',
    },
    {
        'slug': 'eindhoven', 'name': 'Eindhoven', 'province': 'Noord-Brabant', 'region': 'Brabant',
        'lat': 51.4416, 'lon': 5.4697,
        'rijtijd': 120, 'afstand_km': 135,
        'intro': 'Eindhoven is een moderne technologiestad met veel particuliere woningbouw. De combinatie van Schüco LivIng kozijnen en triple glas is hier populair vanwege de focus op energieprestaties en duurzaamheid.',
        'usp_extra': 'populair bij bewoners met focus op energieprestaties',
        'wijken': ['Stratum', 'Woensel', 'Tongelre', 'Gestel', 'Strijp', 'Meerhoven'],
        'recent_project': 'triple glas en hefschuifpui in een vrijstaande woning in Meerhoven',
        'inwoners': '240.000',
    },
    {
        'slug': 'breda', 'name': 'Breda', 'province': 'Noord-Brabant', 'region': 'Brabant',
        'lat': 51.5719, 'lon': 4.7683,
        'rijtijd': 130, 'afstand_km': 145,
        'intro': 'Breda heeft een grote woningmarkt met veel tussenwoning- en vrijstaande woningbouw uit de jaren 70-90. Wij verzorgen complete kozijnrenovaties, inclusief voordeur, schuifpui en gevelbekleding in één project.',
        'usp_extra': 'graag complete gevelpakketten in één opdracht',
        'wijken': ['Bavel', 'Hoge Vugt', 'Prinsenbeek', 'Teteringen', 'Noord', 'Haagse Beemden'],
        'recent_project': 'complete gevelrenovatie met Keralit en 9 kozijnen in Teteringen',
        'inwoners': '185.000',
    },
]


def page(loc):
    province = loc['province']
    region = loc['region']
    name = loc['name']
    slug = loc['slug']
    lat, lon = loc['lat'], loc['lon']
    afstand = loc['afstand_km']
    rijtijd = loc['rijtijd']
    intro = loc['intro']
    usp_extra = loc['usp_extra']
    wijken = loc['wijken']
    recent = loc['recent_project']
    inwoners = loc['inwoners']

    # Distance text
    if afstand == 0:
        dist_text = "U zit dicht bij onze adviseurs en monteurs"
    elif afstand < 25:
        dist_text = f"Op slechts {afstand} km / {rijtijd} minuten rijden van onze werkplaats"
    else:
        dist_text = f"Op {afstand} km / circa {rijtijd} min rijden vanuit onze werkplaats in Hengelo"

    # Schema.org
    business_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"https://www.duurkrachtkozijnen.nl/kunststof-kozijnen-{slug}/#service",
        "name": f"Kunststof kozijnen plaatsen in {name}",
        "description": f"Levering en montage van uitsluitend Schüco LivIng kunststof kozijnen op kunststof stelkozijnen in {name} ({province}). Eigen monteurs, nette afwerking, 10 jaar garantie en gratis advies aan huis.",
        "provider": {"@type": "LocalBusiness", "name": "Duurkracht Kozijnen B.V.", "@id": "https://www.duurkrachtkozijnen.nl/#business"},
        "areaServed": {
            "@type": "City",
            "name": name,
            "containedInPlace": {"@type": "AdministrativeArea", "name": province},
            "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}
        },
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "10", "bestRating": "5"}
    }

    local_business = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": "https://www.duurkrachtkozijnen.nl/#business",
        "name": "Duurkracht Kozijnen B.V.",
        "url": "https://www.duurkrachtkozijnen.nl/",
        "telephone": "+31850731660",
        "email": "info@duurkrachtkozijnen.nl",
        "image": "https://www.duurkrachtkozijnen.nl/design-assets/Logo-duurkracht-kozijnen.svg",
        "logo": "https://www.duurkrachtkozijnen.nl/design-assets/Logo-duurkracht-kozijnen.svg",
        "priceRange": "€€",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Hassinkweg 1",
            "addressLocality": "Hengelo",
            "postalCode": "7556 BV",
            "addressCountry": "NL"
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 52.2660, "longitude": 6.7936},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
             "opens": "08:00", "closes": "17:00"}
        ],
        "areaServed": {"@type": "City", "name": name, "containedInPlace": {"@type": "AdministrativeArea", "name": province}},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "50", "bestRating": "5"},
        "sameAs": [
            "https://www.facebook.com/duurkrachtkozijnen",
            "https://wa.me/31850731660"
        ]
    }

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.duurkrachtkozijnen.nl/"},
            {"@type": "ListItem", "position": 2, "name": "Werkgebied", "item": "https://www.duurkrachtkozijnen.nl/#werkgebied"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"https://www.duurkrachtkozijnen.nl/kunststof-kozijnen-{slug}/"}
        ]
    }

    faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"Plaatst Duurkracht Kozijnen ook in {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"Ja. Vanuit onze werkplaats in Hengelo plaatsen wij regelmatig kunststof kozijnen, deuren en gevelbekleding in {name}. {dist_text}."}},
            {"@type": "Question", "name": f"Wat kost een kunststof kozijn in {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": "Een standaard kunststof draai-kiep kozijn van circa 1,00 × 1,20 m kost inclusief HR++ glas en montage gemiddeld €600 tot €950. De prijs in {0} is gelijk aan onze prijs elders — geen toeslag voor regio. Wij berekenen geen voorrijkosten of reistoeslag.".format(name)}},
            {"@type": "Question", "name": f"Hoe lang duurt de plaatsing in {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"De montage van een gemiddelde woning met 6 tot 10 kozijnen duurt 1 à 2 werkdagen. De totale doorlooptijd van adviesgesprek tot oplevering is 6 tot 8 weken — ook bij projecten in {name}."}},
            {"@type": "Question", "name": f"Welke wijken bedienen jullie in {name}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"Wij plaatsen kozijnen in alle wijken van {name}, waaronder {', '.join(wijken[:4])} en {wijken[4] if len(wijken) > 4 else 'andere wijken'}."}},
        ]
    }

    schemas = '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [business_schema, local_business, breadcrumb, faq])

    wijken_html = ''.join(f'<li>{w}</li>' for w in wijken)

    title = f"Kunststof Kozijnen in {name} — Duurkracht Kozijnen"
    description = f"Kunststof kozijnen in {name} ({province}) door Duurkracht: Schüco LivIng, eigen monteurs, 4,9★ Google, 10 jaar garantie en gratis advies aan huis."

    return f'''<!DOCTYPE html>
<html lang="nl-NL">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="kunststof kozijnen {name}, kozijnen vervangen {name}, kozijnen plaatsen {name}, kunststof deuren {name}, schuifpui {name}, gevelbekleding {name}, kozijnen {province}, kozijnen {region}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="https://www.duurkrachtkozijnen.nl/kunststof-kozijnen-{slug}/" />
<meta name="theme-color" content="#0B5A2B" />

<meta name="geo.region" content="NL-{('OV' if province=='Overijssel' else 'GE' if province=='Gelderland' else 'DR' if province=='Drenthe' else 'FR' if province=='Friesland' else 'FL' if province=='Flevoland' else 'UT' if province=='Utrecht' else 'ZH' if province=='Zuid-Holland' else 'GR' if province=='Groningen' else 'NH' if province=='Noord-Holland' else 'NB' if province=='Noord-Brabant' else 'ZH')}" />
<meta name="geo.placename" content="{name}, {province}" />
<meta name="geo.position" content="{lat};{lon}" />
<meta name="ICBM" content="{lat}, {lon}" />

<meta property="og:type" content="website" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="https://www.duurkrachtkozijnen.nl/kunststof-kozijnen-{slug}/" />
<meta property="og:image" content="https://www.duurkrachtkozijnen.nl/design-assets/images/Voorkant-huis-kozijnen.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://www.duurkrachtkozijnen.nl/design-assets/images/Voorkant-huis-kozijnen.jpg" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..800,30..100,0..1;1,9..144,400..800,30..100,0..1&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/css/site.css" />
<link rel="icon" type="image/svg+xml" href="/design-assets/beelmerkje-klein.svg" />

{schemas}

</head>
<body>

<a href="#main" class="skip">Direct naar inhoud</a>

<div class="topbar">
  <div class="container">
    <span class="live">Nu open — ma t/m vr 08:00 tot 17:00</span>
    <span>Hassinkweg 1, 7556 BV Hengelo · KvK 90895312</span>
    <span><a href="tel:+31850731660" rel="nofollow">085 073 1660</a> · <a href="mailto:info@duurkrachtkozijnen.nl">info@duurkrachtkozijnen.nl</a></span>
  </div>
</div>

<header class="nav">
  <div class="container">
    <a href="/" class="nav-logo"><img src="/design-assets/Logo-duurkracht-kozijnen.svg" alt="Duurkracht Kozijnen logo" width="150" height="44" /></a>
    <nav aria-label="Hoofdnavigatie">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/diensten/">Diensten</a></li>
        <li><a href="/kosten/">Kosten</a></li>
        <li><a href="/projecten/">Projecten</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/over-ons/">Over ons</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </nav>
    <div class="nav-cta">
      <a href="tel:+31850731660" class="phone" rel="nofollow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>
        085 073 1660
      </a>
      <a href="/contact/" class="btn btn-primary">Gratis adviesgesprek <span class="arrow">→</span></a>
    </div>
    <button class="nav-mobile-toggle" type="button" onclick="document.querySelector('.nav ul').style.display = document.querySelector('.nav ul').style.display === 'flex' ? 'none' : 'flex'">
      <img src="/design-assets/icons/menu-mobile.svg" alt="" />
    </button>
  </div>
</header>

<nav class="breadcrumb">
  <div class="container"><ol>
    <li><a href="/">Home</a></li>
    <li><a href="/#werkgebied">Werkgebied</a></li>
    <li>{name}</li>
  </ol></div>
</nav>

<main id="main">

<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Kunststof kozijnen · {name} ({province})</span>
        <h1>Kunststof kozijnen in <span class="em-italic">{name}.</span></h1>
        <p class="lead">
          {intro} {dist_text} — zonder voorrij- of reiskosten.
        </p>
        <div class="hero-cta">
          <a href="/contact/" class="btn btn-primary">Plan een gratis inmeting <span class="arrow">→</span></a>
          <a href="/projecten/" class="btn btn-ghost-white">Bekijk projecten</a>
        </div>
        <div class="hero-trust">
          <span class="stars">★★★★★</span>
          <span>4,9 / 5 · <strong>Google reviews</strong></span>
          <span class="sep">|</span>
          <span>Schüco LivIng · kunststof stelkozijnen · geen reistoeslag</span>
        </div>
      </div>
      <figure class="hero-visual">
        <img src="/design-assets/images/Voorkant-huis-kozijnen.jpg" alt="Voorbeeld project Duurkracht Kozijnen — vergelijkbaar met woningen in {name}" loading="eager" fetchpriority="high" />
        <div class="review-badge">
          <img src="/design-assets/icons/icon-google-g.svg" alt="Google" />
          <div class="rb-text">
            <strong>4,9 / 5</strong>
            <span class="gold">★★★★★</span><br>
            <span>op Google Reviews</span>
          </div>
        </div>
      </figure>
    </div>
  </div>
</section>

<div class="usp-strip">
  <div class="usp-row">
    <span>Actief in {name}</span><span class="sep"></span>
    <span>Alleen Schüco LivIng</span><span class="sep"></span>
    <span>Kunststof stelkozijnen</span><span class="sep"></span>
    <span>Geen reistoeslag</span><span class="sep"></span>
    <span>4,9 ★ Google</span><span class="sep"></span>
    <span>10 jaar garantie</span><span class="sep"></span>
    <span>Eigen monteurs</span><span class="sep"></span>
    <span>Actief in {name}</span><span class="sep"></span>
    <span>Alleen Schüco LivIng</span><span class="sep"></span>
    <span>Kunststof stelkozijnen</span><span class="sep"></span>
    <span>Geen reistoeslag</span><span class="sep"></span>
    <span>4,9 ★ Google</span><span class="sep"></span>
    <span>10 jaar garantie</span><span class="sep"></span>
    <span>Eigen monteurs</span><span class="sep"></span>
  </div>
</div>

<section class="stats">
  <div class="container">
    <div class="stat"><div class="num">{afstand if afstand > 0 else "0"}</div><div class="lbl">km vanaf<br>onze werkplaats</div></div>
    <div class="stat"><div class="num">{rijtijd if rijtijd > 0 else "0"}</div><div class="lbl">min rijden<br>vanuit Hengelo</div></div>
    <div class="stat"><div class="num">€0</div><div class="lbl">voorrijkosten<br>of reistoeslag</div></div>
    <div class="stat"><div class="num">6–8</div><div class="lbl">weken doorlooptijd<br>ook in {name}</div></div>
  </div>
</section>

<section class="section">
  <div class="container two-col">
    <div>
      <span class="eyebrow" style="color: var(--orange);">Onze ervaring in {name}</span>
      <h2>Kozijnen plaatsen <span class="em-italic">in {name},</span> in elke wijk.</h2>
      <p>{intro}</p>
      <p>Onze adviseur komt vrijblijvend bij u langs voor een gratis adviesgesprek. Wij plaatsen alleen wat u nodig heeft — geen verkoopdruk, wel eerlijk advies.</p>
      <ul class="checklist">
        <li><strong>{usp_extra}</strong></li>
        <li><strong>Geen voorrijkosten</strong> in {name}</li>
        <li><strong>Eigen monteurs</strong> — geen onderaannemers</li>
        <li><strong>Strakke montage</strong> met aandacht voor tocht en afdichting</li>
        <li><strong>Schoon opgeleverd</strong> — bouwafval afgevoerd</li>
        <li><strong>10 jaar garantie</strong> op product en montage</li>
      </ul>
    </div>
    <div class="img-stack">
      <img src="/design-assets/images/Nieuwe-voordeur-huis.jpg" alt="Recent project Duurkracht Kozijnen — vergelijkbaar met huizen in {name}" loading="lazy" />
    </div>
  </div>
</section>

<section class="section" style="background: var(--gray-50);">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow" style="color: var(--orange);">Wijken in {name}</span>
        <h2>Waar we werken in <span class="em-italic">{name}.</span></h2>
      </div>
      <p>Wij plaatsen kozijnen in alle wijken van {name}. Een greep uit de wijken waar we recent actief waren:</p>
    </div>
    <ul style="columns: 3; column-gap: 28px; font-size: 16px; line-height: 2.2; color: var(--ink); list-style: none; padding: 0; margin: 0;">
      {wijken_html}
    </ul>
    <p style="margin-top: 30px; font-size: 14px; color: var(--gray-700);">
      <strong>Recent project in {name}:</strong> {recent}.
    </p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <span class="eyebrow" style="color: var(--orange);">Onze diensten in {name}</span>
        <h2>Wat we plaatsen in <span class="em-italic">{name}.</span></h2>
      </div>
      <p>Vijf disciplines, één aanspreekpunt — alle diensten leveren wij ook in {name}.</p>
    </div>
    <div class="benefits">
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>Schüco LivIng kozijnen</h3><p>Warmer wonen, minder tocht en nooit meer schilderen met onze vaste kozijnlijn. <a href="/diensten/kunststof-kozijnen/" style="color:var(--green);">Meer info →</a></p></article>
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>Kunststof deuren</h3><p>Een veilige, goed isolerende entree in de stijl van uw woning. <a href="/diensten/kunststof-deuren/" style="color:var(--green);">Meer info →</a></p></article>
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>Schuifpuien</h3><p>Meer licht, soepel naar buiten en een strakke verbinding met de tuin. <a href="/diensten/kunststof-schuifpuien/" style="color:var(--green);">Meer info →</a></p></article>
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>Kunststof gevelbekleding</h3><p>Een frisse gevel zonder schilderwerk, verkrijgbaar in veel kleuren en houtlooks. <a href="/diensten/kunststof-gevelbekleding/" style="color:var(--green);">Meer info →</a></p></article>
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/check-gradient.svg" alt="" /></div><h3>Kunststof stelkozijn montage</h3><p>Geplaatst op kunststof stelkozijnen door eigen monteurs, strak afgewerkt en schoon opgeleverd. <a href="/diensten/montage/" style="color:var(--green);">Meer info →</a></p></article>
      <article class="benefit"><div class="ic"><img src="/design-assets/icons/icon-adviesgesprek-op-locatie.svg" alt="" /></div><h3>Gratis advies aan huis</h3><p>Onze adviseur komt vrijblijvend bij u in {name} langs.</p></article>
    </div>
  </div>
</section>

<section class="section faq">
  <div class="container">
    <div class="section-head" style="grid-template-columns: 1fr; text-align: center; max-width: 700px; margin-left: auto; margin-right: auto;">
      <div>
        <span class="eyebrow" style="justify-content: center;">Veelgestelde vragen — {name}</span>
        <h2>Antwoorden voor klanten in <span class="em-italic">{name}.</span></h2>
      </div>
    </div>
    <div class="faq-list">
      <details class="faq-item" open><summary>Plaatst Duurkracht Kozijnen ook in {name}?</summary><div class="answer"><p>Ja. Vanuit onze werkplaats in Hengelo plaatsen wij regelmatig kunststof kozijnen, deuren en gevelbekleding in {name}. {dist_text}.</p></div></details>
      <details class="faq-item"><summary>Wat kost een kunststof kozijn in {name}?</summary><div class="answer"><p>Een standaard kunststof draai-kiep kozijn van circa 1,00 × 1,20 m kost inclusief HR++ glas en montage gemiddeld <strong>€ 600 tot € 950</strong>. De prijs in {name} is gelijk aan onze prijs elders — <strong>geen toeslag voor regio of voorrijkosten</strong>.</p></div></details>
      <details class="faq-item"><summary>Hoe lang duurt de plaatsing in {name}?</summary><div class="answer"><p>De montage van een gemiddelde woning met 6 tot 10 kozijnen duurt <strong>1 à 2 werkdagen</strong>. De totale doorlooptijd van adviesgesprek tot oplevering is <strong>6 tot 8 weken</strong> — ook bij projecten in {name}.</p></div></details>
      <details class="faq-item"><summary>Welke wijken bedienen jullie in {name}?</summary><div class="answer"><p>Wij plaatsen kozijnen in alle wijken van {name}, waaronder <strong>{', '.join(wijken[:4])}</strong> en {wijken[4] if len(wijken) > 4 else 'andere wijken'}. Staat uw wijk er niet bij? Bel ons gerust.</p></div></details>
      <details class="faq-item"><summary>Geven jullie ook in {name} 10 jaar garantie?</summary><div class="answer"><p>Ja, ongeacht uw locatie geven wij <strong>10 jaar garantie</strong> op zowel het product als op onze montage. Bij eventuele klachten komen wij ook in {name} kosteloos langs voor herstel.</p></div></details>
    </div>
  </div>
</section>

<section class="cta-banner">
  <div class="container">
    <div>
      <span class="eyebrow">In {name}?</span>
      <h2>Plan uw adviesgesprek<br><span class="em-italic">in {name}.</span></h2>
      <p>Onze adviseur komt vrijblijvend bij u langs in {name}. Geen voorrijkosten, geen verkoopdruk — wel eerlijk advies, een vaste offerte en een doorlooptijd van 6 tot 8 weken.</p>
    </div>
    <div class="cta-banner-actions">
      <a href="/contact/" class="btn btn-primary">Plan een gratis adviesgesprek <span class="arrow">→</span></a>
      <a href="tel:+31850731660" class="btn btn-ghost-white" rel="nofollow">Of bel direct: 085 073 1660</a>
      <p class="meta-line">Gemiddelde reactietijd: <strong>onder de 4 uur</strong> op werkdagen.</p>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="container">
    <div class="ftr-grid">
      <div class="ftr-brand">
        <img src="/design-assets/icon-duurkracht-kozijnen-white.svg" alt="Duurkracht Kozijnen" />
        <p>Specialist in kunststof kozijnen, deuren, schuifpuien en Keralit gevelbekleding. Vanuit Hengelo, in heel Nederland.</p>
        <p><a href="tel:+31850731660" rel="nofollow">085 073 1660</a> · <a href="mailto:info@duurkrachtkozijnen.nl">info@duurkrachtkozijnen.nl</a></p>
      </div>
      <div><p class="ftr-nav-title">Diensten</p><ul>
        <li><a href="/diensten/kunststof-kozijnen/">Kunststof kozijnen</a></li>
        <li><a href="/diensten/kunststof-deuren/">Kunststof deuren</a></li>
        <li><a href="/diensten/kunststof-schuifpuien/">Schuifpuien</a></li>
        <li><a href="/diensten/kunststof-gevelbekleding/">Gevelbekleding</a></li>
        <li><a href="/diensten/montage/">Montage</a></li>
      </ul></div>
      <div><p class="ftr-nav-title">Werkgebied</p><ul>
        <li><a href="/kunststof-kozijnen-hengelo/">Hengelo</a></li>
        <li><a href="/kunststof-kozijnen-enschede/">Enschede</a></li>
        <li><a href="/kunststof-kozijnen-almelo/">Almelo</a></li>
        <li><a href="/kunststof-kozijnen-apeldoorn/">Apeldoorn</a></li>
        <li><a href="/kunststof-kozijnen-zwolle/">Zwolle</a></li>
        <li><a href="/kunststof-kozijnen-nijmegen/">Nijmegen</a></li>
        <li><a href="/kunststof-kozijnen-groningen/">Groningen</a></li>
        <li><a href="/kunststof-kozijnen-amsterdam/">Amsterdam</a></li>
        <li><a href="/kunststof-kozijnen-eindhoven/">Eindhoven</a></li>
        <li><a href="/kunststof-kozijnen-breda/">Breda</a></li>
      </ul></div>
      <div><p class="ftr-nav-title">Bedrijf</p><ul>
        <li><a href="/over-ons/">Over ons</a></li>
        <li><a href="/projecten/">Projecten</a></li>
        <li><a href="/blog/">Blog &amp; advies</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacybeleid/">Privacybeleid</a></li>
      </ul></div>
    </div>
    <div class="ftr-bot">
      <span>© 2026 Duurkracht Kozijnen B.V. · KvK 90895312 · BTW NL865480112B01</span>
      <div class="socials">
        <a href="https://www.facebook.com/duurkrachtkozijnen" rel="noopener" aria-label="Facebook"><img src="/design-assets/icons/icon-facebook.svg" alt="" /></a>
        <a href="https://wa.me/31850731660" rel="noopener" aria-label="WhatsApp"><img src="/design-assets/icons/icon-whatsapp.svg" alt="" /></a>
      </div>
    </div>
  </div>
</footer>

<div class="mobile-cta">
  <a href="tel:+31850731660" class="m-call" rel="nofollow"><img src="/design-assets/icons/icon-phone.svg" alt="" /> Bel direct</a>
  <a href="https://wa.me/31850731660" class="m-wa" rel="noopener"><img src="/design-assets/icons/icon-whatsapp.svg" alt="" /> WhatsApp</a>
</div>

</body>
</html>
'''


# ============================================================
# BUILD
# ============================================================
print(f'Building {len(LOCATIONS)} locatie-pagina\'s...')
for loc in LOCATIONS:
    out = ROOT / f'kunststof-kozijnen-{loc["slug"]}' / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(loc), encoding='utf-8')
    print(f'  ✓ {out.relative_to(ROOT)} ({len(page(loc))//1024} KB)')
print('Done.')
