"""Zet de Duurkracht-projectfoto's om naar de beeldset van de offertebijlage.

Dezelfde bestandsnamen en dezelfde pixelmaten als de vorige set, zodat de
verhoudingen in word-sjabloon.js blijven kloppen. Alleen het logo heeft een
andere verhouding — die staat in word-sjabloon.js aangepast.
"""
import base64
import io
import re
from PIL import Image
from pathlib import Path

DOEL = Path(__file__).resolve().parent
ASSETS = DOEL.parents[1] / "design-assets"
BRON = ASSETS / "images"
LOGO_SVG = ASSETS / "Logo-duurkracht-kozijnen.svg"

# doel -> (bronbestand, breedte, hoogte, zwaartepunt verticaal, horizontaal, inzoom)
#
# Het zwaartepunt bepaalt wat er overblijft als er bijgesneden moet worden:
# .0 is boven/links, 1 is onder/rechts. Inzoom > 1 snijdt extra weg — gebruikt
# om de rommel op de grond onder de schuifpui buiten beeld te houden.
HTML = {
    "cover.jpg":    ("achtertuin-schuifpui.jpg",        1600,  900, .50, .50, 1.0),
    "sfeer-1.jpg":  ("Kunststof-kozijnen-voordeur.jpg", 1000,  750, .50, .50, 1.0),
    "sfeer-2.jpg":  ("Deur-met-kozijnen.jpg",            604,  423, .45, .50, 1.0),
    "sfeer-3.jpg":  ("hero-home01.jpeg",                1000,  750, .28, .50, 1.3),
    "sfeer-4.jpg":  ("hero-raamkozijnen.jpeg",          1000,  476, .50, .50, 1.0),
    "sfeer-5.jpg":  ("Nieuwe-voordeur-huis.jpg",        1000,  750, .45, .28, 1.0),
    "montage.jpg":  ("kunststof-kozijnen-plaatsen.jpg", 1200, 1600, .50, .50, 1.0),
}

WORD = {
    "cover.jpg":   ("achtertuin-schuifpui.jpg",        1340, 586, .50, .50, 1.0),
    "sfeer-1.jpg": ("Kunststof-kozijnen-voordeur.jpg",  660, 495, .50, .50, 1.0),
    "sfeer-2.jpg": ("Deur-met-kozijnen.jpg",            430, 430, .45, .50, 1.0),
    "sfeer-3.jpg": ("hero-home01.jpeg",                 430, 430, .28, .50, 1.3),
    "sfeer-4.jpg": ("hero-raamkozijnen.jpeg",           660, 371, .50, .50, 1.0),
    "sfeer-5.jpg": ("Nieuwe-voordeur-huis.jpg",         430, 430, .45, .28, 1.0),
    "montage.jpg": ("kunststof-kozijnen-plaatsen.jpg",  660, 495, .50, .50, 1.0),
}


def vul(bron: Path, bw: int, bh: int, vfocus: float, hfocus: float, zoom: float) -> Image.Image:
    """Schaalt bij en snijdt bij tot exact bw x bh, zonder vervorming."""
    im = Image.open(bron).convert("RGB")
    schaal = max(bw / im.width, bh / im.height) * zoom
    im = im.resize((round(im.width * schaal), round(im.height * schaal)), Image.LANCZOS)
    links = round((im.width - bw) * hfocus)
    boven = round((im.height - bh) * vfocus)
    return im.crop((links, boven, links + bw, boven + bh))


for map_, spec, kwal in ((DOEL / "img", HTML, 86), (DOEL / "word-img", WORD, 82)):
    map_.mkdir(parents=True, exist_ok=True)
    for naam, (bestand, bw, bh, *hoe) in spec.items():
        vul(BRON / bestand, bw, bh, *hoe).save(map_ / naam, quality=kwal, optimize=True)
        print(f"  {map_.name}/{naam}  {bw}x{bh}  ← {bestand}")

# Het logo zit als PNG met doorzichtige achtergrond in de SVG. Hier eruit
# gehaald en bijgeschaald; op de donkergroene omslag staat het op een wit vlak,
# want het is een donker logo.
ingebed = re.search(r'xlink:href="data:image/png;base64,([A-Za-z0-9+/=]+)"', LOGO_SVG.read_text())
logo = Image.open(io.BytesIO(base64.b64decode(ingebed.group(1))))
for map_, breedte, naam in ((DOEL / "img", 900, "logo.png"),
                            (DOEL / "word-img", 760, "logo-groot.png"),
                            (DOEL / "word-img", 380, "logo-klein.png")):
    h = round(breedte * logo.height / logo.width)
    logo.resize((breedte, h), Image.LANCZOS).save(map_ / naam, optimize=True)
    print(f"  {map_.name}/{naam}  {breedte}x{h}")
print(f"\nlogo-verhouding: {logo.height}/{logo.width} = {logo.height/logo.width:.4f}")
