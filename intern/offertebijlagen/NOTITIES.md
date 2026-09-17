# Offertebijlagen — herkomst van de gegevens en openstaande punten

Productbijlagen die je aan een offerte koppelt. Eén per profielsysteem, zeven
pagina's, zonder prijzen — die staan op het offerteblad.

## Bouwen

```bash
cd "intern/offertebijlagen" && npm install && node maak-documenten.js
```

`npm install` is eenmalig — het haalt `docx` en `pdf-lib` op. Het renderen
gebeurt met headless Chrome; staat Chrome ergens anders, geef dan `CHROME=` mee.

Per profiel komen eruit:

| Bestand | Waarvoor |
|---|---|
| `<slug>.html` | preview in de browser; ook de bron voor de PDF |
| `Productbijlage-*.docx` | bewerkbare versie voor Word |
| `Productbijlage-*.pdf` | het bestand dat aan de offerte gekoppeld wordt |

De map ligt onder `intern/`, en dat pad staat in `robots.txt` op `Disallow`.

## Publiceren op /downloads/

De PDF's staan publiek op `www.duurkrachtkozijnen.nl/downloads/`. Die pagina is
`downloads/index.html`; de bestanden zelf liggen in `docs/`. Na een build gaan de
nieuwe versies er zo heen:

```bash
cp Productbijlage-Schuco-LivIng-82.pdf        ../../docs/productbijlage-schuco-living-82.pdf
cp Productbijlage-Aluplast-Ideal-7000-NL.pdf  ../../docs/productbijlage-aluplast-ideal-7000-nl.pdf
```

De bestandsnamen in `docs/` zijn kleingeletterd en met koppeltekens, zoals de
rest van de site. Wijzig ze niet zonder ook `downloads/index.html`, `sitemap.xml`
en de JSON-LD op die pagina bij te werken — daar staan ze met volledige URL in.

De PDF's in déze map staan in `.gitignore`: ze zijn identiek aan die in `docs/`
en zouden anders bij elke build dubbel in de geschiedenis belanden. De `.docx`
blijft wél in git, want die is voor Romin de bewerkbare versie.

Staat op `/downloads/` een kental (bouwdiepte, U-waarde, levertijd), dan staat
datzelfde getal ook in `producten.js`. Pas ze samen aan.

## Beeldmateriaal

`beelden.py` (Pillow) maakt de beeldset uit `design-assets/`: het logo komt uit
`Logo-duurkracht-kozijnen.svg` — daar zit het als PNG met doorzichtige
achtergrond in — en de foto's uit `design-assets/images/`. Per bestand staat
erbij op welk punt er bijgesneden wordt, want de bronfoto's zijn staand en
liggend door elkaar. Draai het alleen opnieuw als je van foto wisselt:

```bash
python3 beelden.py
```

De maten in `word-img/` liggen vast: `word-sjabloon.js` noemt per afbeelding een
hoogte-breedteverhouding. Wijzig je een maat daar, wijzig dan ook die verhouding.

## Per klant invullen

De omslag heeft vijf invulvelden: **Opgesteld voor** (klantnaam), **Offertenummer**,
**Datum**, **Adviseur** en **Geldig tot**. Ze staan in `producten.js` onder
`GEDEELD.velden`.

In het **Word-bestand** zijn het invulvelden (inhoudsbesturingselementen).
Eén klik selecteert de grijze hinttekst, typen vervangt hem, en Tab springt naar
het volgende veld. De rest van het document kun je met rust laten. Werkwijze:
open het .docx, vul de vijf velden in, en sla op als PDF om aan de offerte te
koppelen. Wie liever rechtstreeks in de PDF werkt, kan dat ook — zie hieronder.

`invulvelden.js` maakt die velden. docx-js kan ze niet schrijven, dus het
document wordt eerst gebouwd met `{{veld:tag}}` als tekst; die markering wordt
daarna in `word/document.xml` vervangen door een `<w:sdt>`-blok. Voeg je een
veld toe aan `GEDEELD.velden`, dan komt het er vanzelf bij — de build meldt het
als het aantal omgezette velden niet klopt.

In de **PDF** zijn het sinds kort ook echte invulvelden (AcroForm). Open het
bestand in Voorvertoning, Acrobat of de browser, klik op de regel achter
*Opgesteld voor* en typ; Tab springt naar het volgende veld. De tekst is wit,
want de omslag is donker — in macOS Voorvertoning zie je tijdens het typen een
lichtgrijs vakje met donkere letters, dat is de bewerkingsweergave van het
programma. Bij opslaan en afdrukken staat er wit op groen.

`pdf-invulvelden.js` legt die velden erop. De uitlijning wordt niet geschat: na
het renderen meet het script dezelfde HTML nog een keer met headless Chrome,
leest de vakjes met `data-veld` uit en rekent hun plaats om naar PDF-punten. De
maatstaf is het `.page`-element van 210 mm. Het script waarschuwt als velden in
dezelfde kolom niet op dezelfde millimeter beginnen, of als er eentje achter de
voetbalk zou verdwijnen.

## Teksten aanpassen

Alle teksten en specificaties staan in `producten.js`. Pas ze daar aan en draai
het script opnieuw — dan blijven de HTML, de Word- en de PDF-versie van beide
profielen gelijk. Handmatig in het Word-bestand knippen kan ook, maar die
wijziging is bij de volgende build weg.

De huisstijlkleuren staan op drie plekken, één per uitvoer: bovenin de `:root`
van `html-sjabloon.js`, bovenin `word-sjabloon.js` en bovenin `doorsnede.js`.
Ze dragen nog hun oude namen — `NAVY` is het groen `#0B5A2B` — omdat die namen
de rol beschrijven en niet de kleur.

## Waar de cijfers vandaan komen

**Aluplast Ideal 7000 NL** — fabrikantopgave via aluplast.net:
85 mm bouwdiepte, zeskamerprofiel, U<sub>f</sub> 1,1 W/m²K, beglazing tot 51 mm,
tot RC2, geluidsisolatie tot 46 dB, U<sub>w</sub> tot 0,70 W/m²K met triple glas.
De inbouwdiepte van 120 mm (verdiepte NL-uitvoering) komt van Nederlandse
dealers, niet van aluplast zelf.

**Schüco LivIng 82** — fabrikantopgave en ift Rosenheim:
82 mm bouwdiepte, zevenkamerprofiel, U<sub>f</sub> 0,96 W/m²K voor de
MD-uitvoering met middendichting, beglazing tot 52 mm, tot RC2, geluidsisolatie
tot 47 dB (R<sub>w</sub>), luchtdoorlatendheid klasse 4, waterdichtheid 9A.

**Garantie** — 10 jaar op product én montage, conform wat op
duurkrachtkozijnen.nl staat. Het glas is in de bijlage op dezelfde termijn gezet.

**Inbraakwerendheid** — de site belooft standaard RC2 (SKG\*\*) en PKVW op
verzoek. De bijlage zegt hetzelfde; wijkt er één af, pas dan allebei aan.

**U<sub>f</sub> Schüco 0,96, niet 0,92.** De site noemde overal 0,92; dat is op
17 september 2026 rechtgezet naar de fabrikant- en ift-opgave voor de
MD-uitvoering die wij leveren. Staat er ergens weer 0,92, dan is dat de oude
waarde. `build_blog.py` is meegegaan, zodat nieuwe blogs het goed hebben.

## Nog te controleren vóór dit naar klanten gaat

1. **Glasopbouw 4–16–4.** Dat is de gangbare 24 mm-opbouw, maar controleer wat
   onze glasleverancier daadwerkelijk levert — 4–15–4 of 5–15–4 met een dikkere
   spouwvulling komt ook voor.

2. **Garantie op glas.** De bijlage geeft 10 jaar op HR++/HR+++. Controleer of
   dat de termijn van de glasleverancier is.

3. **Algemene voorwaarden.** De bijlage verwijst ernaar en geeft ze voorrang.
   Zorg dat ze als bijlage bij de offerte zitten —
   `docs/algemene-voorwaarden-dkk-2026.pdf`.

4. **Levertijd Aluplast.** De bijlage en de configurator zeggen allebei 3 à 4
   weken, tegenover 6 tot 8 voor Schüco. Verandert dat, pas dan `producten.js`
   én `configurator/index.html` aan.

## Keuzes die zijn gemaakt

- **Geen prijzen.** De bijlage beschrijft het product; de offerte rekent. Dat
  scheelt een tweede plek waar bedragen kunnen verouderen.
- **Calibri in het Word-bestand**, niet Manrope. De huisstijlfonts staan niet op
  een doorsnee werkplek, en een ontbrekend lettertype maakt het document
  rommelig. De HTML- en PDF-versie gebruiken wél Manrope en Fraunces.
- **De doorsnedetekening is getekend, geen foto.** `doorsnede.js` genereert hem
  uit de productgegevens, zodat het aantal kamers en de bouwdiepte altijd
  kloppen met de tekst. Hij is schematisch en dat staat er ook bij — het is geen
  maatvoerende detailtekening van de fabrikant.
- **Foto's zijn eigen projectfoto's** uit `design-assets/images/`. Er zitten geen
  productfoto's van Aluplast of Schüco in; die zijn auteursrechtelijk van de
  fabrikant. Wil je die erin, vraag dan het beeldmateriaal op bij de leverancier.
- **Het logo** komt uit `design-assets/Logo-duurkracht-kozijnen.svg`, waar het
  als PNG met doorzichtige achtergrond in zit. Op de donkergroene omslag staat
  het op een wit vlak: het is een donker logo en dat valt op groen weg.

## Twee uitlijningsfouten die bij het invulbaar maken boven water kwamen

Allebei zaten ze al in de omslag; ze vielen pas op toen de velden op de
millimeter werden nagemeten.

1. **`OFFERTENUMMER` stond 1,2 mm uit de rooilijn.** Het labelvak had
   `flex: 0 0 26mm`, maar dat label is in kapitalen met letterspatiëring 27,3 mm
   breed. Een flex-item krimpt niet onder zijn inhoud, dus dat ene label duwde
   zijn invulregel naar rechts terwijl de andere drie wél op 26 mm bleven staan.
   De basis staat nu op 28 mm.

2. **`Adviseur` en `Geldig tot` verdwenen achter de voetbalk.** Die balk staat
   absoluut op `bottom: 0` en telt dus niet mee in de kolom erboven. Het paneel
   liep er 12,2 mm achter. De kolom reserveert nu 24 mm onderaan.

De build controleert sindsdien allebei en meldt het als het weer misgaat.

## Pagina's die stilletjes overliepen

Dezelfde val, maar dan voor de inhoud in plaats van de invulvelden: elke `.page`
is precies 297 mm hoog met `overflow: hidden`, en de voetbalk ligt er absoluut
overheen. Wat niet paste, verdween zonder foutmelding. Op pagina 4 was daardoor
het hele blok "Over de opgegeven waarden" weg, op pagina 6 de kaders *Service
melden* en *Voorrang van voorwaarden*, en op pagina 7 het voorbehoud onderaan —
in beide profielen, en het viel niemand op omdat een PDF er nu eenmaal
afgemaakt uitziet.

De opmaak is daarom een slag dichter gezet: krappere celopvulling en regelhoogte
in de specificatietabel (dat scheelde het meest — zestien regels à ruim 2 mm),
kleinere tussenruimtes in de lijsten en kaders, en minder marge tussen de
blokken. `controle.js` meet nu na elke build per pagina hoe ver de onderste
inhoud onder de voetbalk uitkomt, en `maak-documenten.js` meldt het met
`OVERLOOP`. Verschijnt die regel, dan is er iets bijgekomen dat er niet meer bij
past — inkorten, niet negeren.

Let op bij het toevoegen van tekst: de Schüco-bijlage heeft drie specificatie-
regels meer dan de Aluplast (luchtdoorlatendheid, waterdichtheid, hoekafdichting)
en zit dus krapper. Wat bij Aluplast nog past, hoeft dat bij Schüco niet te doen.
