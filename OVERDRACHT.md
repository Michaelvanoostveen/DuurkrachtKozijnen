# Overdracht — Duurkracht Kozijnen configurator

> Zelfstandig overdrachtsdocument. Bedoeld om mee te geven aan een andere workflow of agent
> die verder werkt aan deze configurator, of aan een vergelijkbaar project.
> Alles hieronder is geverifieerd in de code op het moment van schrijven.

**Opgesteld:** 2026-08-13 · **Repo:** `Michaelvanoostveen/DuurkrachtKozijnen` · **Branch:** `main`
**Laatste commit bij overdracht:** `5033de8`

---

## 1. Waar het om gaat

Statische HTML-site (geen framework, geen build-stap) voor Duurkracht Kozijnen — kunststof
kozijnen, deuren en schuifpuien. Gehost op Vercel. 105 HTML-pagina's, 93 URL's in de sitemap,
19 blogartikelen.

De **configurator** is het hart van dit document: `configurator/index.html`, 1.526 regels,
één bestand met HTML, CSS en JS bij elkaar. Geen dependencies, geen build. Alles wat je
aanpast doe je in dat ene bestand.

---

## 2. Wat de configurator kan

Zes producttypen — raamkozijn, voordeur, achterdeur, schuifpui, tuindeuren, balkondeur — met
per product een set indelingen (presets). De klant stelt samen en ziet direct prijs en tekening.

| Onderdeel | Wat het doet |
|---|---|
| **Live SVG-tekening** | Geen afbeeldingen; alles wordt met JS als SVG getekend en schaalt met de gekozen maten |
| **Bewegende preview** | CSS 3D-transforms tonen hoe het kozijn opengaat; aan/uit via een knop, keuze in `localStorage` |
| **Profielgeometrie** | Kozijn → vleugel → glaslat → glas, op ware schaal omgerekend uit mm |
| **Kleur kozijn + vleugel apart** | Tweekleurig; contrast blijft kloppen bij elke RAL |
| **Binnenzijde-afwerking** | Wit/crème glad inbegrepen, houtnerf of kleur +15% |
| **Indeling per vak** | Per vak type én draairichting instelbaar, los van de gekozen preset |
| **Maten per vak/rij** | Breedte per vak en hoogte per rij, met totaal-slider |
| **Project** | Meerdere onderdelen verzamelen in `localStorage`, offerte via een vooringevulde link |

---

## 3. Vakinhoudelijke regels — hier ging het twee keer mis

### De punt van het openingssymbool is de KRUK, niet het scharnier

Dit is de belangrijkste regel in de tekenlogica en is in deze sessie tweemaal verkeerd
geïmplementeerd voordat de eigenaar het corrigeerde. Leg dit naast elke wijziging aan
`sym()` of `sash()`:

```
De driehoek in het symbool wijst naar de kruk (handgreep).
Het scharnier zit aan de TEGENOVERLIGGENDE kant.
De animatie moet dus om de kant draaien waar de punt NIET is.
```

Concreet in de code:

| Type | Punt / kruk | Scharnier → animatiepivot |
|---|---|---|
| `turnR` | rechts | links |
| `turnL` | links | rechts |
| `tiltturn` | links | rechts |
| `tiltturnR` | rechts | links |
| `tilt` (valraam) | onder | onder — dit symbool wijst wél naar het scharnier zelf |

`tilt` is de uitzondering: daar is geen kruk in het symbool, de punt ís het scharnier.

### Stolpraam

Twee vleugels die op elkaar sluiten zonder vaste tussenstijl. Zodra één vleugel op vast glas
wordt gezet, is het geen stolpraam meer en moet de tussenstijl terugkomen — dat gebeurt
automatisch in `effVariant()`.

---

## 4. Prijsmodel — en waar je het bijstelt

De formule staat in `update()`:

```
prijs = (basis + m² boven standaard × prijs per m²)
        × glas × kleur × beslag × indeling × binnenzijde
        → daarna softCap()
```

Alle knoppen staan als constanten bovenin het `<script>`-blok:

| Constante | Wat | Huidige waarde |
|---|---|---|
| `PRODUCTS[x].base` | basisprijs per product | raam 2100, voordeur 4700, achterdeur 3800, schuifpui 6000, tuindeuren 6400, balkondeur 3800 |
| `PRODUCTS[x].priceMax` | prijsplafond | raam 3000, deuren 6400, pui/tuindeuren 10600 |
| `GLASS` | HR++ 1,00 · triple 1,25 | ook de ISDE-bedragen per m² |
| `COLOR` | zes RAL's, factor 1,00–1,18 | |
| `BESLAG` | RC2 1,00 · RC3 1,10 | |
| `BINNEN` | wit/crème glad 1,00 · houtnerf of kleur 1,15 | |
| `VAK` | prijsfactor per vaktype | vast 0,80 · valraam 0,92 · draai 0,96 · draai-kiep 1,00 |
| `VAK_DEMPING` | hoe zwaar een per-vak wijziging meetelt | 0,80 |
| `PROFILE` | aanzichtmaten in mm | Schüco LivIng 82 |

### Door de eigenaar bevestigde prijsregels

Deze zijn expliciet vastgesteld en mogen niet zomaar veranderen:

1. **Kozijn en vleugel in verschillende RAL's kost niets extra.** Er geldt simpelweg de
   duurste van de twee kleurfactoren. Een eerdere bicolor-toeslag is op verzoek verwijderd.
2. **Binnenzijde wit glad óf crème glad is inbegrepen.** Alles daarbuiten — houtnerf of een
   kleur — is +15%. Die twee zitten daarom samen in één optie.
3. **Een gekozen preset houdt exact zijn eigen prijs.** Alleen het verschil per vak telt mee,
   zodat bestaande prijzen niet verschuiven door de per-vak functie.

### Let op: `softCap` verbergt prijsverschillen

```js
knee = priceMax × 0.75;   // boven dit bedrag loopt de prijs asymptotisch naar priceMax
```

Voor een raamkozijn ligt de knie op €2.250 en het plafond op €3.000. Een 3-delig raam zit
daar al tegenaan, waardoor extra opties nauwelijks nog prijsverschil geven — twee vakken van
vast glas naar draai-kiep zetten leverde €10 verschil. **Dit is bestaand gedrag, geen bug**,
maar het maakt de per-vak prijsfactoren bij meervaks-ramen praktisch onzichtbaar. Wil je dat
verschil wél zien, dan moet `priceMax` voor raamkozijnen omhoog. Nog niet besloten.

---

## 5. Hoe de tekening in elkaar zit

```
buildSVG(kind, variant, ratio, kleurKozijn, colW, rowH, anim, breedteMm, kleurVleugel)
  ├── drawWindow   (raam, balkondeur)
  ├── drawDoor     (voor-/achterdeur)
  ├── drawSlider   (schuifpui)
  └── drawFrench   (tuindeuren)
```

Bouwstenen die je bijna altijd nodig hebt:

| Functie | Doet |
|---|---|
| `livPane(type, x,y,w,h, kleur, P, kleurVleugel)` | één vak: vleugel → glaslat → glas. Vast glas krijgt geen vleugel en dus meer glasoppervlak |
| `sym(type, x,y,w,h)` | het openingssymbool — zie sectie 3 |
| `sash(type, ..., inner, kleur, kleurVleugel)` | wikkelt een vak in een `<g>` dat via CSS om het scharnier draait |
| `profilePx(pxPerMm)` | rekent `PROFILE` (mm) om naar pixels voor de huidige tekening |
| `contrastTint(hex, hoeveel)` | maakt donkerder bij lichte kleuren, lichter bij donkere |

`contrastTint` bestaat omdat de dagopening en de glaslat eerst vaste kleuren hadden. Bij
antraciet, zwartgrijs, staalblauw en dennengroen vielen die weg tegen het profiel, waardoor je
bij een open raam niet meer zag dát het openstond.

**Animatie:** CSS `@keyframes` op SVG-groepen met `transform-box: view-box` en het scharnier
als `transform-origin`. Geen video, geen library. Respecteert `prefers-reduced-motion`.

---

## 6. Wat een volgende wijziging moet meenemen

Bij elke aanpassing aan de configurator zijn dit de plekken die stilletjes uit de pas gaan
lopen als je ze vergeet. Ze zijn alle vijf een keer misgegaan in deze sessie:

1. **De variant-thumbnails** (`renderVariants` → `variantThumb`) — die tekenen met dezelfde
   functies maar zonder mm-maten; ze vallen terug op `profileFallback()`
2. **De projectlijst** (`computeItem`, `renderProject`) — eigen aanroep van `buildSVG` en een
   eigen prijsberekening; wat je in `update()` wijzigt moet hier ook
3. **Opslaan en bewerken** (`addToProject`, `editItem`) — nieuwe velden moeten in de `key`,
   in het opgeslagen object én in de `setRadio`/`pending*` herstelroute
4. **De offertetekst** — losse string-opbouw onderaan `renderProject()`
5. **Oude projecten in `localStorage`** — klanten hebben opgeslagen items zonder je nieuwe
   veld; val altijd terug op een standaard (`it.kleurV || 'zelfde'`)

---

## 7. Testen

Playwright is de enige zinvolle manier om dit te controleren; de configurator is volledig
JS-gedreven, dus statische checks zeggen weinig.

```bash
python3 -m http.server 7700           # vanuit de repo-root
# browser: /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

Patronen die goed werkten:

```js
// animatie vastzetten op de open stand — let op: elke animatie heeft een eigen fase
document.getElementById('cfg-svg').getAnimations({subtree:true})
  .forEach(a => { a.pause(); a.currentTime = a.effect.getTiming().duration * 0.72; });
```

Draai-kiep heeft een cyclus van 7s waarin de kiepfase op 15–28% zit en de draaifase op 62–82%.
Andere types 6s met de open fase rond 32–62%. Eén vast tijdstip klopt dus niet voor alles.

Voor datumafhankelijke dingen: klok vastzetten via `context.add_init_script()` met een
vervangen `Date`, en testen op de dag ervoor, de dag zelf en ruim erna.

Controleer standaard: geen JS-fouten (`page.on("pageerror")`), geen horizontale overflow op
390px, en of afbeeldingen echt laden (`naturalWidth`).

---

## 8. Openstaand

| Punt | Status |
|---|---|
| **`ANTHROPIC_API_KEY` ontbreekt** | De blogautomatie faalt sinds half juli met `Could not resolve authentication method`. De Vercel-stap eronder wordt nooit bereikt. Zetten onder Settings → Secrets → Actions |
| **Deploy-workflow nog nooit gedraaid** | `.github/workflows/deploy.yml` toegevoegd, handmatig te starten. Een agent met beperkte GitHub-rechten kan hem niet dispatchen (403); de eigenaar moet dat één keer doen |
| **`priceMax` raamkozijn** | Zie sectie 4 — beslissen of het plafond omhoog moet |
| **Aanzichtmaten Schüco LivIng** | De mm in `PROFILE` komen uit modelkennis, niet uit een geverifieerde datasheet. Bouwdiepte 82 mm en 7-kamer kloppen met de site; de 117 mm aanzicht is niet tegen een officiële bron gecontroleerd |
| **Mobiele sticky CTA** | Toont altijd "Bel direct", ook buiten openingstijden of tijdens een sluitingsperiode |

---

## 9. Conventies in dit project

- **Nederlands** in alle klantgerichte tekst, commit-berichten en code-commentaar
- **Geen build-stap** — HTML/CSS/JS direct bewerken. Uitzondering: `build_*.py` genereren
  blog-, locatie- en dienstpagina's; bewerk daar het Python-bestand, niet de HTML
- **Sitemap bijwerken** bij nieuwe pagina's
- **GA4** (`G-W45QZ8KED5`) en **Clarity** (`xkjrl7c4vw`) op elke pagina
- **JSON-LD** op elke pagina; blijft valide houden
- Prijzen zijn **vaste all-in prijzen** — profiel, glas, stelkozijn, montage, btw
- Bedrijfsfeiten staan in `CLAUDE.md` en sectie 4 van `CLAUDE_HANDOFF.md`; die zijn leidend

---

## 10. Wat er in deze sessie is gebeurd

Nieuwste eerst. Alles staat op `main` en is gepusht.

| Commit | |
|---|---|
| `5033de8` | Workflow om een Vercel-deploy handmatig af te dwingen |
| `93defda` | Indeling en draairichting per vak instelbaar (+ gespiegelde draai-kiep) |
| `3d4e6dc` | Bouwvakmelding weer verwijderd |
| `0b883b0` | Bouwvakmelding: pop-up homepage + kloppende topbar site-breed |
| `f904e7d` | Scharnier zit tegenover de kruk (correctie op `e4f7756`) |
| `e4f7756` | Eerste poging scharnierrichting — bleek verkeerd |
| `2f293ad` | Twee blogartikelen + layoutfout in 17 bestaande posts hersteld |
| `612d7ea` | Geen toeslag voor twee kleuren, wel keuze voor de binnenzijde |
| `62d20ef` | Aparte kleur voor kozijn en vleugel |
| `7f997fc` | Dagopening en glaslat contrasteren bij elke RAL |
| `2078e13` | Profielen conform Schüco LivIng 82 + leesbare openingssymbolen |
| `e928084` | Bewegende preview van kozijn, deur en schuifpui |

Twee dingen die onderweg werden gevonden en meteen zijn opgelost, los van de opdracht:

- **Alle blogposts stonden verkeerd op desktop.** `grid-template-columns: 1fr 280px` terwijl de
  `<aside>` vóór het artikel in de DOM staat — de inhoudsopgave kreeg de brede kolom en het
  artikel werd in 280px geperst. Trof 17 van de 18 posts.
- **De topbar zei "Nu open" tijdens de bouwvak** op 94 pagina's, terwijl er niemand bereikbaar
  was. Veel zoekverkeer landt op locatie- en kostenpagina's, niet op de homepage.
