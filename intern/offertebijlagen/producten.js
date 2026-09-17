/**
 * Productgegevens voor de offertebijlagen.
 *
 * Eén bron voor zowel de HTML-preview als het Word-bestand. Pas hier een
 * specificatie aan en draai `node maak-documenten.js` om beide documenten van
 * beide profielen opnieuw te bouwen.
 *
 * De cijfers komen van de fabrikant. Zie NOTITIES.md voor de vindplaats per
 * waarde en voor de punten die nog bevestigd moeten worden.
 */

// Tekst die voor beide profielen identiek is, staat onderaan in GEDEELD.

const ALUPLAST = {
  slug: 'aluplast-ideal-7000-nl',
  bestandsnaam: 'Productbijlage-Aluplast-Ideal-7000-NL',
  merk: 'Aluplast',
  model: 'Ideal 7000 NL',
  volledig: 'Aluplast Ideal 7000 NL',
  // omslagtitel, in twee regels; het derde deel krijgt de accentkleur
  titelRegels: ['Aluplast', 'Ideal 7000 ', 'NL'],

  kamers: 6,
  kamersWoord: 'zeskamerprofiel',
  kamersWoordKap: 'Zeskamerprofiel',
  kamersTekst: 'Zeskamersysteem in kozijn en vleugel',
  diepte: 85,
  inbouwdiepte: 120,
  uf: '1,1',
  uwBest: '0,70',
  glasMax: 51,
  geluid: 46,
  levertijd: '3 tot 4 weken',
  levertijdKort: '3–4 weken',
  herkomst: 'Aluplast GmbH, Karlsruhe (Duitsland)',
  typeOmschrijving: 'Verdiept profiel, ontwikkeld voor de Nederlandse renovatiemarkt',
  versterking: 'Verzinkt staal in de versterkingskamer; Powerdur-versterking optioneel',
  versterkingKort: 'Verzinkt staal (of Powerdur-versterking)',

  // extra regels die alleen dit profiel heeft
  extraSpecs: [],

  intro: [
    'Wij monteren de Aluplast Ideal 7000 NL: een Duits kunststof profielsysteem dat speciaal is ontwikkeld voor de Nederlandse renovatiemarkt. Het heeft een bouwdiepte van 85 mm en een zeskamerconstructie — meer kamers betekent meer stilstaande lucht in het profiel, en stilstaande lucht isoleert.',
    'De NL-uitvoering is een verdiept profiel met een inbouwdiepte van 120 mm. Dat is precies de maat die in Nederlandse gevels past, waardoor uw nieuwe kozijn dezelfde schaduwwerking en diepte houdt als het kozijn dat eruit gaat. Uw gevel blijft er dus uitzien zoals u gewend bent — alleen beter geïsoleerd, stiller en zonder onderhoud.',
  ],

  voordelen: [
    ['Warmer in huis.', 'Minder warmteverlies langs het kozijn, en geen koudestraling meer langs het raam.'],
    ['Stiller.', 'De drievoudige afdichting en het zware glaspakket dempen verkeers- en buitengeluid.'],
    ['Geen onderhoud.', 'Nooit meer schilderen; het profiel blijft kleurvast en vraagt alleen af en toe schoonmaken.'],
    ['Snel te leveren.', 'Drie tot vier weken productietijd na het inmeten — de kortste levertijd van onze twee lijnen.'],
  ],

  // het kaderblok waarin de twee lijnen naast elkaar worden gezet
  keuzeKader: [
    'Duurkracht Kozijnen werkt bewust met twee profielsystemen: Aluplast Ideal 7000 NL en Schüco LivIng 82. Allebei Duits, allebei KOMO-gecertificeerd.',
    'Voor uw woning adviseren wij de Aluplast Ideal 7000 NL. Naast de prestaties speelt de levertijd mee: 3 tot 4 weken voor Aluplast, tegenover 6 tot 8 weken voor Schüco LivIng.',
  ],

  // uitleg onder de doorsnede
  slotKader: [
    'Waarom die middendichting telt',
    'Veel goedkopere kozijnen hebben twee afdichtingen. De Ideal 7000 NL heeft er drie. De extra dichting houdt de sponning droog, waardoor er minder koude lucht tot in het profiel komt. U merkt dat aan de tocht die wegblijft en aan het geluid dat buiten blijft.',
  ],

  productieRegel: 'Uw kozijnen gaan op maat in productie bij Aluplast. Reken op een levertijd van 3 tot 4 weken.',
};

const SCHUCO = {
  slug: 'schueco-living-82',
  bestandsnaam: 'Productbijlage-Schuco-LivIng-82',
  merk: 'Schüco',
  model: 'LivIng 82',
  volledig: 'Schüco LivIng 82',
  titelRegels: ['Schüco', 'LivIng ', '82'],

  kamers: 7,
  kamersWoord: 'zevenkamerprofiel',
  kamersWoordKap: 'Zevenkamerprofiel',
  kamersTekst: 'Zevenkamersysteem in kozijn en vleugel',
  diepte: 82,
  inbouwdiepte: 120,
  uf: '0,96',
  uwBest: '0,70',
  glasMax: 52,
  geluid: 47,
  levertijd: '6 tot 8 weken',
  levertijdKort: '6–8 weken',
  herkomst: 'Schüco Polymer Technologies, Weißenfels (Duitsland)',
  typeOmschrijving: 'Uitvoering MD met middendichting, geleverd als verdiept Hollands profiel met vaste aanslag',
  versterking: 'Verzinkt staal in de versterkingskamer; schuimvulling optioneel',
  versterkingKort: 'Verzinkt staal (of een geschuimde versterking)',

  extraSpecs: [
    ['Luchtdoorlatendheid', 'Klasse 4 — de hoogste klasse volgens NEN-EN 12207'],
    ['Waterdichtheid', 'Klasse 9A volgens NEN-EN 12208'],
    ['Hoekafdichting', 'Ingelaste middendichting, zonder harde hoekstukken'],
  ],

  intro: [
    'Wij monteren de Schüco LivIng 82: het kunststof profielsysteem van Schüco, een van de bekendste Duitse merken in de gevelbouw. Het heeft een bouwdiepte van 82 mm en een zevenkamerconstructie — meer kamers betekent meer stilstaande lucht in het profiel, en stilstaande lucht isoleert.',
    'Wij leveren de LivIng als verdiept Hollands profiel met een inbouwdiepte van 120 mm en een vaste aanslag. Dat is precies de maat die in Nederlandse gevels past, waardoor uw nieuwe kozijn dezelfde schaduwwerking en diepte houdt als het kozijn dat eruit gaat. Uw gevel blijft er dus uitzien zoals u gewend bent — alleen beter geïsoleerd, stiller en zonder onderhoud.',
  ],

  voordelen: [
    ['Warmer in huis.', 'Met een U-waarde van 0,96 W/m²K voor het profiel is dit het best isolerende systeem dat wij leveren.'],
    ['Stiller.', 'Geluidsisolatie tot 47 dB, en luchtdichtheid in klasse 4 — de hoogste klasse die er is.'],
    ['Geen onderhoud.', 'Nooit meer schilderen; het profiel blijft kleurvast en vraagt alleen af en toe schoonmaken.'],
    ['Strakke hoeken.', 'De middendichting wordt ingelast in plaats van geplakt, dus geen zichtbare hoekstukjes in de sponning.'],
  ],

  keuzeKader: [
    'Duurkracht Kozijnen werkt bewust met twee profielsystemen: Schüco LivIng 82 en Aluplast Ideal 7000 NL. Allebei Duits, allebei KOMO-gecertificeerd.',
    'Voor uw woning adviseren wij de Schüco LivIng 82. Het isoleert een slag beter dan de Aluplast en presteert hoger op geluid en luchtdichtheid. Daar staat een langere levertijd tegenover: 6 tot 8 weken, tegenover 3 tot 4 weken voor Aluplast.',
  ],

  slotKader: [
    'Waarom die ingelaste dichting telt',
    'Bij de meeste kozijnen wordt de middendichting als rubber in de sponning gedrukt en in de hoeken op maat geknipt. Schüco last de dichting in één doorlopend geheel mee. Daardoor zit er in de hoek — precies waar tocht en lekkage normaal beginnen — geen naad. Dat is de reden dat dit systeem klasse 4 haalt op luchtdoorlatendheid.',
  ],

  productieRegel: 'Uw kozijnen gaan op maat in productie bij Schüco. Reken op een levertijd van 6 tot 8 weken.',
};

// ───────────────────────  gedeelde teksten  ───────────────────────
const GEDEELD = {
  bedrijf: 'Duurkracht Kozijnen',
  payoff: 'Stiller, warmer, lichter wonen.',
  plaats: 'Hassinkweg 1, 7556 BV Hengelo',
  plaatsKort: 'Hengelo (Ov.)',
  telefoon: '085 073 1660',
  email: 'info@duurkrachtkozijnen.nl',
  web: 'www.duurkrachtkozijnen.nl',
  kvk: '90895312',
  btw: 'NL865489725B01',

  /**
   * De velden op de omslag die per klant worden ingevuld.
   * In het Word-bestand worden dit echte invulvelden (inhoudsbesturingselementen):
   * klikken selecteert de hele grijze hint, typen vervangt hem.
   * `breed: true` zet het veld over de volle breedte.
   */
  velden: [
    { tag: 'klantnaam', label: 'Opgesteld voor', hint: 'Naam van de klant', breed: true },
    { tag: 'offertenummer', label: 'Offertenummer', hint: 'Offertenummer' },
    { tag: 'datum', label: 'Datum', hint: 'Datum' },
    { tag: 'adviseur', label: 'Adviseur', hint: 'Naam adviseur' },
    { tag: 'geldigtot', label: 'Geldig tot', hint: 'Vervaldatum' },
  ],

  glas: {
    type: 'HR++ isolatieglas',
    opbouw: '4 – 16 – 4 mm, totaal 24 mm',
    ug: '1,1 W/m²K',
    vulling: 'Argon, met warme afstandhouder',
    norm: 'NEN 2608, KOMO-keurmerk',
  },

  garantieGeldt: [
    ['Profiel.', 'Materiaal- en fabricagefouten, vormvastheid en kleurvastheid van het profiel in basiskleur.'],
    ['Beglazing.', 'Lekkage van de isolerende beglazing — het beslaan tussen de ruiten door een defecte randafdichting.'],
    ['Hang- en sluitwerk.', 'Goede werking van scharnieren, sluitingen en bediening bij normaal gebruik.'],
    ['Montage.', 'De plaatsing, de aansluiting op het metselwerk en de waterdichtheid van die aansluiting.'],
  ],

  garantieNiet: [
    'Schade door geweld van buitenaf, inbraak, storm, brand of andere calamiteiten',
    'Glasbreuk anders dan door een aantoonbaar materiaalgebrek',
    'Krassen en beschadigingen die bij oplevering niet zijn gemeld',
    'Gebreken door verkeerd gebruik, eigen aanpassingen of reparaties door derden',
    'Normale slijtage van bewegende delen en afdichtingsrubbers',
    'Thermische breuk van glas door afplakken, beschilderen of het plaatsen van folie',
    'Verkleuring van niet-basiskleuren buiten de door de folieleverancier gestelde termijn',
    'Werk van derden dat op onze kozijnen aansluit, zoals stuc-, schilder- of metselwerk',
  ],

  garantieVoorwaarden: [
    'De garantietermijn gaat in op de datum van oplevering',
    'De factuur is volledig voldaan volgens de overeengekomen betalingsvoorwaarden',
    'De kozijnen zijn normaal gebruikt en onderhouden — schoonmaken met water en een mild middel, geen schuurmiddelen',
    'Gebreken worden binnen redelijke termijn na ontdekking schriftelijk bij ons gemeld',
    'Wij krijgen de gelegenheid het gebrek zelf te onderzoeken en te herstellen',
    'De garantie is gekoppeld aan het adres en gaat bij verkoop van de woning over op de nieuwe eigenaar',
  ],

  sluitwerk: [
    ['Alle draai-kiepramen en deuren krijgen standaard ', 'SKG**-beslag', ' met meerpuntsluiting en stalen versterking.'],
    ['Daarmee voldoen uw ramen en deuren standaard aan ', 'weerstandsklasse RC2', ' volgens NEN 5096.'],
    ['Op verzoek uit te voeren op ', 'PKVW-niveau', ' — het Politiekeurmerk Veilig Wonen, waar veel inboedelverzekeraars premiekorting voor geven.'],
    ['Draai-kiepramen zijn in ', 'twee ventilatiestanden', ' te zetten en draaien altijd naar binnen open.'],
    ['Voor- en achterdeur hebben een ', 'driepuntssluiting', ' met automatisch slot, cilinderslot en kerntrekbeveiliging.'],
    ['Voor- en achterdeur worden geleverd met een onderdorpel van ', 'Isostone', '.'],
  ],

  kleuren: [
    'Veelgekozen buitenkleuren: antracietgrijs RAL 7016 (nerf), zwart RAL 9005 (nerf), crème RAL 9001',
    'Houtnerfdecors zoals Golden Oak en Noten voor woningen met een klassieke gevel',
    'Binnenzijde standaard wit RAL 9016 glad, of in dezelfde kleur als buiten',
    'Kleurvast en UV-bestendig; nooit meer schilderen',
  ],

  inbegrepen: [
    'Levering en montage van de kozijnen, inclusief het plaatsen van het glas',
    'Kunststof stelkozijnen als montagebasis',
    'Demontage van de bestaande kozijnen en afvoer van het bouwafval',
    'Binnenafwerking met kunststof hoeklijst',
    'Terugplaatsen van vensterbanken waar die nu zitten',
  ],

  nietInbegrepen: [
    'Demontage en montage van rolluiken, screens, radiatoren en elektra',
    'Stuc-, metsel-, schilder- en loodgieterswerk',
    'Steigerwerk, tenzij dat op de offerte staat',
    'Afvoer van asbesthoudend of chemisch afval',
    'Het afdekken van meubilair en het aanvragen van vergunningen',
    'Veiligheidsbeglazing volgens NEN 3569 — wel leverbaar tegen meerprijs',
  ],

  klantvraag: [
    'Rondom de werkplekken circa 1,5 meter ruimte vrijmaken',
    'Ramen en vensterbanken leeg, gordijnen en raamdecoratie verwijderd',
    'Een parkeerplek voor de bus in de buurt van de woning',
    'Toegang tot water en elektra tijdens de werkdag',
  ],

  voorbehoud:
    'Deze productbijlage hoort bij de offerte waaraan hij is gekoppeld en bevat geen prijzen. ' +
    'Prijzen, aantallen en posities staan op het offerteblad zelf. Aan deze bijlage kunnen geen ' +
    'rechten worden ontleend voor zover zij afwijkt van de offerte of van onze algemene ' +
    'verkoop- en leveringsvoorwaarden.',
};

/** stappen van akkoord tot oplevering — de productieregel verschilt per profiel */
GEDEELD.stappen = (prod) => [
  ['Akkoord op de offerte', 'U tekent de offerte. Binnen twee weken bellen wij u voor de afspraak voor het bouwkundig inmeten.'],
  ['Bouwkundig inmeten', 'Onze bouwkundige komt langs en legt maatvoering, kleuren en draairichtingen definitief vast. Tot dat moment kunt u nog wijzigen.'],
  ['Productie', prod.productieRegel],
  ['Montage', 'Onze eigen monteurs demonteren de oude kozijnen en plaatsen de nieuwe op kunststof stelkozijnen, inclusief beglazing en binnenafwerking.'],
  ['Oplevering', 'Wij lopen het werk met u na, leveren schoon op en voeren het bouwafval af. Vanaf die datum loopt uw garantie.'],
];

/** de regels van de grote specificatietabel, opgebouwd uit de productgegevens */
GEDEELD.specRijen = (p) => [
  ['Merk en type', `${p.volledig} — ${p.typeOmschrijving}`],
  ['Herkomst', p.herkomst],
  ['Bouwdiepte profiel', `${p.diepte} mm`],
  ['Inbouwdiepte (NL, verdiept)', `${p.inbouwdiepte} mm, met vaste aanslag`],
  ['Kamerindeling', p.kamersTekst],
  ['Afdichting', 'Drievoudig, met doorlopende middendichting'],
  ['Uf-waarde profiel', `${p.uf} W/m²K`],
  ['Uw-waarde raam', `Vanaf 1,2 W/m²K met HR++; met triple beglazing tot ${p.uwBest} W/m²K haalbaar`],
  ['Maximale glasdikte', `Tot ${p.glasMax} mm — ruimte voor HR++, triple en geluidwerend glas`],
  ['Versterking', p.versterking],
  ['Hoekverbinding', 'Diagonale verstekverbinding, machinaal gelast'],
  ['Geluidsisolatie', `Tot ${p.geluid} dB, afhankelijk van de gekozen beglazing`],
  ...p.extraSpecs,
  ['Certificering', 'KOMO-gecertificeerd, SKG-getest hang- en sluitwerk; glasopbouw conform NEN 2608'],
  ['Levertijd productie', `${p.levertijd} na bouwkundig inmeten`],
];

/** legenda onder de doorsnedetekening */
GEDEELD.legenda = (p) => [
  [p.kamersWoordKap + '.', `Gescheiden luchtkamers in kozijn én vleugel remmen de warmtestroom van binnen naar buiten.`],
  ['Versterkingskamer.', `${p.versterkingKort} houdt het kozijn kaarsrecht, ook bij grote maten.`],
  ['Middendichting.', 'De derde afdichting scheidt de natte buitenzone van de droge binnenzone — winst op isolatie én geluid.'],
  [`Vleugel, ${p.diepte} mm.`, 'Even diep als het kozijn, met dezelfde kamerindeling en versterking.'],
  ['Glaslat.', 'Aan de binnenzijde gemonteerd: het glas is van buitenaf niet uit te nemen.'],
  [`Beglazing tot ${p.glasMax} mm.`, 'Ruimte voor HR++, triple of geluidwerend glas — nu of bij een latere upgrade.'],
];

module.exports = { ALUPLAST, SCHUCO, GEDEELD, PRODUCTEN: [ALUPLAST, SCHUCO] };
