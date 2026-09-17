/**
 * Bouwt de bewerkbare Word-versie van een offertebijlage.
 *
 * Bewust Calibri in plaats van de huisstijlfonts Manrope/Fraunces: die staan
 * niet standaard op een Windows- of Mac-werkplek, en een ontbrekend lettertype
 * maakt van een nette offerte een rommelige. Wie Manrope wél installeert, zet
 * het document in Word in één keer om via de stijlen.
 */
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, HeadingLevel, PageBreak,
  Header, Footer, PageNumber, VerticalAlign, LevelFormat, convertMillimetersToTwip,
} = require('docx');
const { GEDEELD } = require('./producten');
const { MARKERING } = require('./invulvelden');

// Huisstijl Duurkracht; NAVY heet zo om historische redenen en is het groen.
const NAVY = '0B5A2B', CTA = 'ED6B06', CTA_ACCENT = 'C4570A', CTA_LICHT = 'D3CF29';
const STEEL = '696960', STEEL_SOFT = 'B0BDB4', NAVY_TINT = 'E8F0EB', AMBER_TINT = 'FDE9D6';
const INK = '4A4A44', RULE = 'EAEAE6', OFF = 'FAFAFA', WIT = 'FFFFFF';
const FONT = 'Calibri';

const CONTENT = convertMillimetersToTwip(178);

function bouw(p, IMG) {
  const G = GEDEELD;
  const img = (f) => fs.readFileSync(path.join(IMG, f));

  // ── kleine bouwstenen ──
  const t = (text, o = {}) => new TextRun({ text, font: FONT, ...o });

  const par = (text, o = {}) => new Paragraph({
    spacing: { after: 120, line: 276, ...(o.spacing || {}) },
    alignment: o.alignment,
    children: [t(text, { size: o.size || 20, color: o.color || INK, bold: o.bold, italics: o.italics })],
  });

  const rich = (runs, o = {}) => new Paragraph({
    spacing: { after: 120, line: 276, ...(o.spacing || {}) },
    alignment: o.alignment,
    children: runs,
  });

  const eyebrow = (text) => new Paragraph({
    spacing: { after: 60 },
    children: [t(text.toUpperCase(), { size: 15, bold: true, color: CTA_ACCENT, characterSpacing: 60 })],
  });

  const titel = (text) => [
    new Paragraph({
      heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 80 },
      children: [t(text, { size: 34, bold: true, color: NAVY })],
    }),
    new Paragraph({
      spacing: { after: 200 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: CTA, space: 1 } },
      indent: { right: convertMillimetersToTwip(155) },
      children: [t('', { size: 2 })],
    }),
  ];

  const subkop = (text) => new Paragraph({
    heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 90 },
    children: [t(text.toUpperCase(), { size: 17, bold: true, color: NAVY, characterSpacing: 30 })],
  });

  const kleineTekst = (text) => par(text, { size: 15, color: STEEL, spacing: { after: 80 } });

  const bullet = (runs, ref = 'vink') => new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { after: 70, line: 264 },
    children: runs,
  });
  const bul = (text, ref = 'vink', size = 19) => bullet([t(text, { size, color: INK })], ref);
  const bulKop = (kop, rest, ref = 'vink') => bullet([
    t(kop, { size: 19, bold: true, color: NAVY }),
    t(' ' + rest, { size: 19, color: INK }),
  ], ref);

  const afb = (file, w, ratio, o = {}) => new Paragraph({
    alignment: o.alignment || AlignmentType.LEFT,
    spacing: { after: o.after === undefined ? 100 : o.after },
    children: [new ImageRun({
      data: img(file), type: file.endsWith('.png') ? 'png' : 'jpg',
      transformation: { width: w, height: Math.round(w * ratio) },
    })],
  });

  const bijschrift = (text) => par(text, { size: 14, color: STEEL, italics: true, spacing: { after: 160 } });
  const ruimte = (na = 160) => new Paragraph({ spacing: { after: na }, children: [t('', { size: 4 })] });

  const NOBORDER = ['top', 'bottom', 'left', 'right', 'insideHorizontal', 'insideVertical']
    .reduce((o, k) => (o[k] = { style: BorderStyle.NONE, size: 0, color: 'auto' }, o), {});
  const lijn = (color = RULE) => ({ style: BorderStyle.SINGLE, size: 4, color });

  // ── specificatietabel ──
  function specTabel(kop, rijen) {
    const c1 = Math.round(CONTENT * 0.40), c2 = CONTENT - c1;
    const kopcel = (txt) => new TableCell({
      width: { size: txt ? c1 : c2, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
      margins: { top: 90, bottom: 90, left: 140, right: 140 },
      children: [new Paragraph({ children: [t(txt, { size: 15, bold: true, color: WIT, characterSpacing: 30 })] })],
    });
    const rows = [new TableRow({ tableHeader: true, children: [kopcel(kop.toUpperCase()), kopcel('')] })];

    rijen.forEach(([links, rechts], i) => {
      const fill = i % 2 ? OFF : WIT;
      rows.push(new TableRow({ children: [
        new TableCell({ width: { size: c1, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
          margins: { top: 80, bottom: 80, left: 140, right: 140 },
          children: [new Paragraph({ children: [t(links, { size: 18, bold: true, color: NAVY })] })] }),
        new TableCell({ width: { size: c2, type: WidthType.DXA },
          shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
          margins: { top: 80, bottom: 80, left: 140, right: 140 },
          children: [new Paragraph({ children: [t(rechts, { size: 18, color: INK })] })] }),
      ] }));
    });

    return new Table({
      columnWidths: [c1, c2], width: { size: CONTENT, type: WidthType.DXA },
      borders: { top: lijn(NAVY), bottom: lijn(), left: lijn(), right: lijn(),
                 insideHorizontal: lijn(), insideVertical: lijn() },
      rows,
    });
  }

  // ── gekleurd kaderblok ──
  function kader(kinderen, fill = NAVY_TINT, randkleur = null) {
    const borders = randkleur
      ? { ...NOBORDER, left: { style: BorderStyle.SINGLE, size: 18, color: randkleur } }
      : NOBORDER;
    return new Table({
      columnWidths: [CONTENT], width: { size: CONTENT, type: WidthType.DXA }, borders,
      rows: [new TableRow({ children: [new TableCell({
        width: { size: CONTENT, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
        margins: { top: 170, bottom: 170, left: 220, right: 220 },
        children: kinderen,
      })] })],
    });
  }

  const kaderKop = (tekst, kleur = NAVY) => new Paragraph({
    spacing: { after: 90 },
    children: [t(tekst.toUpperCase(), { size: 16, bold: true, color: kleur, characterSpacing: 30 })],
  });

  // ── rij met kerncijfers ──
  function cijferRij(items) {
    const w = Math.floor(CONTENT / items.length);
    const wit = { style: BorderStyle.SINGLE, size: 12, color: WIT };
    return new Table({
      columnWidths: items.map(() => w), width: { size: w * items.length, type: WidthType.DXA },
      borders: { top: wit, bottom: wit, left: wit, right: wit, insideHorizontal: wit, insideVertical: wit },
      rows: [new TableRow({ children: items.map(([groot, klein]) => new TableCell({
        width: { size: w, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
        margins: { top: 150, bottom: 150, left: 80, right: 80 },
        verticalAlign: VerticalAlign.CENTER,
        children: [
          new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
            children: [t(groot, { size: 30, bold: true, color: CTA_LICHT })] }),
          new Paragraph({ alignment: AlignmentType.CENTER,
            children: [t(klein, { size: 14, color: STEEL_SOFT })] }),
        ],
      })) })],
    });
  }

  // ── twee kolommen ──
  function tweeKolommen(links, rechts, verhouding = 0.5) {
    const c1 = Math.round(CONTENT * verhouding), c2 = CONTENT - c1;
    return new Table({
      columnWidths: [c1, c2], width: { size: CONTENT, type: WidthType.DXA }, borders: NOBORDER,
      rows: [new TableRow({ children: [
        new TableCell({ width: { size: c1, type: WidthType.DXA }, margins: { right: 200 }, children: links }),
        new TableCell({ width: { size: c2, type: WidthType.DXA }, margins: { left: 200 }, children: rechts }),
      ] })],
    });
  }

  function fotoRij(bestanden) {
    const w = Math.floor(CONTENT / 3);
    return new Table({
      columnWidths: [w, w, w], width: { size: w * 3, type: WidthType.DXA }, borders: NOBORDER,
      rows: [new TableRow({ children: bestanden.map((f) => new TableCell({
        width: { size: w, type: WidthType.DXA }, margins: { right: 90, left: 90 },
        children: [afb(f, 178, 1, { after: 0 })],
      })) })],
    });
  }

  /**
   * Invulblok op de omslag. De waarderegel bevat een markering die na het
   * bouwen wordt omgezet naar een echt invulveld — zie invulvelden.js.
   */
  function omslagVelden() {
    const breed = G.velden.filter((v) => v.breed);
    const smal = G.velden.filter((v) => !v.breed);
    const halve = Math.round(CONTENT / 2);

    const cel = (veld, breedte, fill) => new TableCell({
      width: { size: breedte, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
      margins: { top: 130, bottom: 130, left: 180, right: 180 },
      children: [
        new Paragraph({ spacing: { after: 40 },
          children: [t(veld.label.toUpperCase(), { size: 13, bold: true, color: STEEL, characterSpacing: 40 })] }),
        new Paragraph({ children: [t(MARKERING(veld.tag), { size: 20, bold: true, color: NAVY })] }),
      ],
    });

    const rijen = [];
    breed.forEach((v) => rijen.push(new TableRow({
      children: [new TableCell({
        width: { size: CONTENT, type: WidthType.DXA },
        columnSpan: 2,
        shading: { type: ShadingType.CLEAR, fill: WIT, color: 'auto' },
        margins: { top: 130, bottom: 130, left: 180, right: 180 },
        children: [
          new Paragraph({ spacing: { after: 40 },
            children: [t(v.label.toUpperCase(), { size: 13, bold: true, color: STEEL, characterSpacing: 40 })] }),
          new Paragraph({ children: [t(MARKERING(v.tag), { size: 24, bold: true, color: NAVY })] }),
        ],
      })],
    })));

    for (let i = 0; i < smal.length; i += 2) {
      const fill = (i / 2) % 2 === 0 ? OFF : WIT;
      const paar = smal.slice(i, i + 2);
      rijen.push(new TableRow({
        children: paar.length === 2
          ? [cel(paar[0], halve, fill), cel(paar[1], CONTENT - halve, fill)]
          : [new TableCell({
              width: { size: CONTENT, type: WidthType.DXA }, columnSpan: 2,
              shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
              margins: { top: 130, bottom: 130, left: 180, right: 180 },
              children: [
                new Paragraph({ spacing: { after: 40 },
                  children: [t(paar[0].label.toUpperCase(), { size: 13, bold: true, color: STEEL, characterSpacing: 40 })] }),
                new Paragraph({ children: [t(MARKERING(paar[0].tag), { size: 20, bold: true, color: NAVY })] }),
              ],
            })],
      }));
    }

    return new Table({
      columnWidths: [halve, CONTENT - halve], width: { size: CONTENT, type: WidthType.DXA },
      borders: { top: lijn(), bottom: lijn(), left: lijn(), right: lijn(),
                 insideHorizontal: lijn(), insideVertical: lijn() },
      rows: rijen,
    });
  }

  const paginaEinde = () => new Paragraph({ children: [new PageBreak()] });
  const doorsnedeBestand = `doorsnede-${p.slug}.png`;

  // ─────────────────────  document  ─────────────────────
  return new Document({
    creator: G.bedrijf,
    title: `Productbijlage ${p.volledig}`,
    description: `Productbijlage bij de offerte van ${G.bedrijf} — ${p.volledig}`,
    styles: {
      default: { document: { run: { font: FONT, size: 20, color: INK }, paragraph: { spacing: { line: 276 } } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: FONT, size: 34, bold: true, color: NAVY },
          paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: FONT, size: 17, bold: true, color: NAVY },
          paragraph: { spacing: { before: 200, after: 90 }, outlineLevel: 1 } },
      ],
    },
    numbering: { config: [
      { reference: 'vink', levels: [{ level: 0, format: LevelFormat.BULLET, text: '▪',
        alignment: AlignmentType.LEFT,
        style: { run: { color: CTA, size: 20 }, paragraph: { indent: { left: 300, hanging: 200 } } } }] },
      { reference: 'streep', levels: [{ level: 0, format: LevelFormat.BULLET, text: '–',
        alignment: AlignmentType.LEFT,
        style: { run: { color: STEEL, size: 20 }, paragraph: { indent: { left: 300, hanging: 200 } } } }] },
      { reference: 'stap', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.',
        alignment: AlignmentType.LEFT,
        style: { run: { color: NAVY, bold: true, size: 20 }, paragraph: { indent: { left: 340, hanging: 340 } } } }] },
    ] },
    sections: [{
      properties: {
        titlePage: true,
        page: { margin: {
          top: convertMillimetersToTwip(16), bottom: convertMillimetersToTwip(16),
          left: convertMillimetersToTwip(16), right: convertMillimetersToTwip(16),
          header: convertMillimetersToTwip(10), footer: convertMillimetersToTwip(10),
        } },
      },
      headers: {
        first: new Header({ children: [new Paragraph({ children: [] })] }),
        default: new Header({ children: [
          new Table({
            columnWidths: [Math.round(CONTENT * 0.45), Math.round(CONTENT * 0.55)],
            width: { size: CONTENT, type: WidthType.DXA },
            borders: { ...NOBORDER, bottom: lijn() },
            rows: [new TableRow({ children: [
              new TableCell({ width: { size: Math.round(CONTENT * 0.45), type: WidthType.DXA },
                margins: { bottom: 90 }, verticalAlign: VerticalAlign.CENTER,
                children: [afb('logo-klein.png', 70, 220 / 380, { after: 0 })] }),
              new TableCell({ width: { size: Math.round(CONTENT * 0.55), type: WidthType.DXA },
                margins: { bottom: 90 }, verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({ alignment: AlignmentType.RIGHT,
                  children: [t(`PRODUCTBIJLAGE · ${p.volledig.toUpperCase()}`,
                    { size: 13, bold: true, color: STEEL, characterSpacing: 30 })] })] }),
            ] })],
          }),
          new Paragraph({ spacing: { after: 120 }, children: [t('', { size: 6 })] }),
        ] }),
      },
      footers: {
        first: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
          children: [t(`${G.bedrijf} B.V. · ${G.plaats} · ${G.telefoon} · ${G.email} · ${G.web} · KvK ${G.kvk}`,
            { size: 14, color: STEEL })] })] }),
        default: new Footer({ children: [
          new Paragraph({ border: { top: lijn() }, spacing: { before: 60 }, children: [t('', { size: 4 })] }),
          new Table({
            columnWidths: [Math.round(CONTENT * 0.75), Math.round(CONTENT * 0.25)],
            width: { size: CONTENT, type: WidthType.DXA }, borders: NOBORDER,
            rows: [new TableRow({ children: [
              new TableCell({ width: { size: Math.round(CONTENT * 0.75), type: WidthType.DXA },
                children: [new Paragraph({ children: [t(`${G.bedrijf} · ${G.payoff}`, { size: 14, color: STEEL })] })] }),
              new TableCell({ width: { size: Math.round(CONTENT * 0.25), type: WidthType.DXA },
                children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
                  t('Pagina ', { size: 14, color: STEEL }),
                  new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 14, bold: true, color: NAVY }),
                  t(' van ', { size: 14, color: STEEL }),
                  new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 14, color: STEEL }),
                ] })] }),
            ] })],
          }),
        ] }),
      },

      children: [
        // ══ 1 · OMSLAG ══
        afb('logo-groot.png', 150, 440 / 760, { after: 360 }),
        eyebrow('Productbijlage bij uw offerte'),
        new Paragraph({ spacing: { after: 60 },
          children: [t(p.volledig, { size: 52, bold: true, color: NAVY })] }),
        new Paragraph({ spacing: { after: 220 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 22, color: CTA, space: 1 } },
          indent: { right: convertMillimetersToTwip(150) }, children: [t('', { size: 2 })] }),
        rich([
          t('Kunststof kozijnen met ', { size: 24 }),
          t(`${p.diepte} mm bouwdiepte`, { size: 24, bold: true, color: NAVY }),
          t(', een ', { size: 24 }),
          t(p.kamersWoord, { size: 24, bold: true, color: NAVY }),
          t(' en ', { size: 24 }),
          t('tien jaar garantie', { size: 24, bold: true, color: NAVY }),
          t(' op product én montage.', { size: 24 }),
        ], { spacing: { after: 260 } }),
        afb('cover.jpg', 660, 586 / 1340, { after: 260 }),
        omslagVelden(),
        new Paragraph({ spacing: { before: 300, after: 60 },
          children: [t(G.payoff, { size: 22, italics: true, color: CTA_ACCENT })] }),
        par(`${G.bedrijf} B.V. · ${G.plaats} · werkzaam in heel Nederland · KvK ${G.kvk}`,
          { size: 16, color: STEEL, spacing: { after: 0 } }),

        paginaEinde(),

        // ══ 2 · WAAROM DIT PROFIEL ══
        eyebrow('Waarover deze bijlage gaat'),
        ...titel('Het profiel dat wij voor u hebben gekozen'),
        rich([
          t('In uw offerte staat wát wij leveren en wat het kost. Deze bijlage laat zien ', { size: 22 }),
          t('waaruit', { size: 22, italics: true, bold: true, color: NAVY }),
          t(' uw kozijnen bestaan: het profiel, het glas, het hang- en sluitwerk en de garantie die u erop krijgt.', { size: 22 }),
        ], { spacing: { after: 180 } }),

        tweeKolommen(
          p.intro.map((x) => par(x)),
          [afb('sfeer-1.jpg', 300, 495 / 660, { after: 60 }),
           bijschrift('Uitgevoerd werk: kozijnen en voordeur in antraciet, geplaatst door onze eigen monteurs.')],
          0.54,
        ),

        ruimte(),
        cijferRij([
          [`${p.diepte} mm`, 'Bouwdiepte van het profiel'],
          [String(p.kamers), 'Kamers in kozijn en vleugel'],
          [p.uf, 'Uf-waarde in W/m²K'],
          ['10 jaar', 'Garantie op product én montage'],
        ]),

        subkop('Wat dit voor u betekent'),
        ...p.voordelen.map(([kop, rest]) => bulKop(kop, rest)),

        ruimte(),
        kader([
          kaderKop('Twee lijnen, één keuze'),
          ...p.keuzeKader.map((x) => par(x, { size: 19 })),
          par('Tot aan het bouwkundig inmeten kunt u nog van profiel wisselen. Vraag ons gerust om een vergelijking.',
            { size: 16, color: STEEL, spacing: { after: 0 } }),
        ]),

        paginaEinde(),

        // ══ 3 · DOORSNEDE ══
        eyebrow('Het profiel van binnen'),
        ...titel(`${p.kamers === 6 ? 'Zes' : 'Zeven'} kamers, drie afdichtingen`),
        par(`Hieronder ziet u een doorsnede door kozijn en draaiend deel: bovenin de buitenzijde, onderin uw woonkamer. De ${p.kamers === 6 ? 'zes' : 'zeven'} kamers, de drievoudige afdichting en de versterkingskamer zijn de drie onderdelen die het verschil maken.`,
          { size: 21, spacing: { after: 180 } }),

        afb(doorsnedeBestand, 660, 655 / 1340, { after: 60 }),
        kleineTekst('Schematische weergave — bedoeld om de opbouw uit te leggen, niet op schaal en niet maatvoerend.'),

        ruimte(120),
        ...G.legenda(p).map(([kop, rest], i) => bulKop(`${i + 1} · ${kop}`, rest)),

        ruimte(),
        kader([
          new Paragraph({ spacing: { after: 70 },
            children: [t(p.slotKader[0], { size: 19, bold: true, color: NAVY })] }),
          par(p.slotKader[1], { size: 19, spacing: { after: 0 } }),
        ], AMBER_TINT, CTA),

        paginaEinde(),

        // ══ 4 · SPECIFICATIES ══
        eyebrow('Specificaties'),
        ...titel('Technische gegevens'),
        specTabel('Profielsysteem', G.specRijen(p)),

        ruimte(200),
        specTabel('Standaard beglazing', [
          ['Type', G.glas.type], ['Opbouw', G.glas.opbouw], ['Ug-waarde', G.glas.ug],
          ['Vulling', G.glas.vulling], ['Norm', G.glas.norm],
        ]),
        kleineTekst('Triple beglazing (HR+++), geluidwerend glas, zonwerend glas en veiligheidsglas volgens NEN 3569 zijn leverbaar tegen meerprijs. Wat er in úw offerte staat, leest u op het offerteblad zelf.'),

        ruimte(),
        kader([
          kaderKop('Wat de U-waarde betekent'),
          par('De U-waarde zegt hoeveel warmte er per vierkante meter verloren gaat. Hoe lager, hoe beter.', { size: 19 }),
          bullet([t('Uf', { size: 19, bold: true, color: NAVY }), t(' — alleen het kozijnprofiel', { size: 19 })], 'streep'),
          bullet([t('Ug', { size: 19, bold: true, color: NAVY }), t(' — alleen het glas', { size: 19 })], 'streep'),
          bullet([t('Uw', { size: 19, bold: true, color: NAVY }), t(' — het complete raam, glas en profiel samen', { size: 19 })], 'streep'),
          par('Ter vergelijking: enkel glas in een houten kozijn zit rond de 5,0 W/m²K. Uw nieuwe kozijnen met HR++ komen op ongeveer 1,2 — ruim vier keer zo goed.',
            { size: 18, spacing: { before: 80, after: 0 } }),
        ]),

        ruimte(),
        kader([
          new Paragraph({ spacing: { after: 70 },
            children: [t('Over de opgegeven waarden', { size: 19, bold: true, color: NAVY })] }),
          par('De genoemde U-waarden zijn systeemwaarden van de fabrikant, gemeten onder genormeerde omstandigheden. De werkelijke waarde van úw raam hangt af van de maat, de indeling en het gekozen glas. De definitieve prestaties leggen we vast bij het bouwkundig inmeten.',
            { size: 19, spacing: { after: 0 } }),
        ], AMBER_TINT, CTA),

        paginaEinde(),

        // ══ 5 · VEILIGHEID & UITVOERING ══
        eyebrow('Veiligheid, bediening en uitvoering'),
        ...titel('Zoals u hem straks gebruikt'),
        subkop('Hang- en sluitwerk'),
        ...G.sluitwerk.map(([a, b, c]) => bullet([
          t(a, { size: 19 }), t(b, { size: 19, bold: true, color: NAVY }), t(c, { size: 19 }),
        ])),

        ruimte(140),
        afb('sfeer-4.jpg', 440, 371 / 660, { after: 60 }),
        bijschrift('Draai-kiepraam van binnenuit: naar binnen draaiend, met twee ventilatiestanden.'),

        tweeKolommen(
          [
            subkop('Kleuren en afwerking'),
            par(`Standaard leveren wij in wit RAL 9010. De ${p.model} is daarnaast leverbaar met gekleurde folie aan de buitenzijde en wit aan de binnenzijde — de meest gekozen combinatie in Nederland.`, { size: 19 }),
            ...G.kleuren.map((x) => bul(x, 'streep', 18)),
          ],
          [
            subkop('Afwerking binnen'),
            par('Na de montage werken wij de aansluiting tussen kozijn en binnenmuur af met een kunststof hoek, zodat u geen stuc- of schilderwerk hoeft te laten doen. Standaardkleuren zijn wit RAL 9016 en crème RAL 9001, glad.', { size: 19 }),
            subkop('Vensterbanken'),
            par('Waar nu een vensterbank zit, plaatsen wij er een terug — tenzij anders afgesproken. Onze vensterbanken zijn krasvast, UV-bestendig en ongevoelig voor vocht en warmte.', { size: 19 }),
          ],
        ),

        subkop('Uitgevoerd werk'),
        fotoRij(['sfeer-2.jpg', 'sfeer-3.jpg', 'sfeer-5.jpg']),
        kleineTekst(`Projecten van ${G.bedrijf}. Uitvoeringen kunnen per woning verschillen; uw eigen indeling, kleur en draairichting leggen we vast bij het bouwkundig inmeten.`),

        paginaEinde(),

        // ══ 6 · GARANTIE ══
        eyebrow('Garantiebepalingen'),
        ...titel('Tien jaar, op product én op montage'),
        par('Wij leveren en monteren in eigen beheer. Daardoor hoeft u bij een klacht niet te zoeken wie verantwoordelijk is: u meldt het bij ons, en wij lossen het op. Eén aanspreekpunt, voor zowel het product als het werk.',
          { size: 21, spacing: { after: 180 } }),

        cijferRij([
          ['10 jaar', 'Op het kozijnprofiel in basiskleur'],
          ['10 jaar', 'Op de montage door onze monteurs'],
          ['10 jaar', 'Op de beglazing HR++ en HR+++'],
        ]),

        subkop('Waarop de garantie geldt'),
        ...G.garantieGeldt.map(([kop, rest]) => bulKop(kop, rest)),

        subkop('Waarop de garantie niet geldt'),
        ...G.garantieNiet.map((x) => bul(x, 'streep')),

        ruimte(),
        kader([
          kaderKop('Voorwaarden waaronder de garantie loopt'),
          ...G.garantieVoorwaarden.map((x) => bul(x, 'streep')),
        ]),

        ruimte(),
        tweeKolommen(
          [
            new Paragraph({ spacing: { after: 70 },
              children: [t('Service melden', { size: 19, bold: true, color: NAVY })] }),
            par('Een gebrek meldt u bij ons kantoor, met foto’s en het offerte- of factuurnummer. Wij nemen binnen vijf werkdagen contact op om een afspraak te plannen.', { size: 18 }),
            rich([t(G.telefoon, { size: 18, bold: true, color: NAVY }),
                  t('  ·  ', { size: 18, color: STEEL }),
                  t(G.email, { size: 18, bold: true, color: NAVY })], { spacing: { after: 0 } }),
          ],
          [
            new Paragraph({ spacing: { after: 70 },
              children: [t('Voorrang van voorwaarden', { size: 19, bold: true, color: NAVY })] }),
            par('Deze bijlage vat de garantie samen en is bedoeld om u te informeren. Op al onze leveringen, offertes en overeenkomsten zijn onze algemene verkoop- en leveringsvoorwaarden van toepassing. Wijkt de tekst hierboven daarvan af, dan gaan de algemene voorwaarden en de offerte zelf voor.',
              { size: 18, spacing: { after: 0 } }),
          ],
        ),

        paginaEinde(),

        // ══ 7 · MONTAGE & AFSPRAKEN ══
        eyebrow('Van akkoord tot oplevering'),
        ...titel('Hoe wij het uitvoeren'),
        ...G.stappen(p).map(([kop, tekst]) => bullet([
          t(kop + '  ', { size: 19, bold: true, color: NAVY }),
          t(tekst, { size: 19, color: INK }),
        ], 'stap')),

        ruimte(),
        tweeKolommen(
          [afb('montage.jpg', 290, 495 / 660, { after: 60 }),
           bijschrift('Montage in eigen beheer — geen onderaannemers.')],
          [kaderKop('Wat wij van u vragen'), ...G.klantvraag.map((x) => bul(x, 'streep', 18))],
          0.46,
        ),

        subkop('Standaard inbegrepen'),
        ...G.inbegrepen.map((x) => bul(x)),

        subkop('Niet inbegrepen, tenzij vermeld op de offerte'),
        ...G.nietInbegrepen.map((x) => bul(x, 'streep')),

        ruimte(200),
        kader([
          kaderKop('Vragen over deze bijlage?', CTA_LICHT),
          new Paragraph({ spacing: { after: 120 },
            children: [t('Bel of app ons gerust — wij lopen de offerte graag punt voor punt met u door.',
              { size: 24, bold: true, color: WIT })] }),
          rich([t(G.telefoon, { size: 26, bold: true, color: CTA_LICHT }),
                t(`     ${G.email}     ${G.web}`, { size: 18, color: WIT })], { spacing: { after: 60 } }),
          par(`${G.bedrijf} B.V. · ${G.plaats} · KvK ${G.kvk}`,
            { size: 16, color: STEEL_SOFT, spacing: { after: 0 } }),
        ], NAVY),

        new Paragraph({ spacing: { before: 220 }, alignment: AlignmentType.CENTER,
          children: [t(G.voorbehoud, { size: 14, color: STEEL })] }),
      ],
    }],
  });
}

async function schrijf(p, IMG, uitPad) {
  const doc = bouw(p, IMG);
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(uitPad, buf);
  return buf.length;
}

module.exports = { schrijf };
