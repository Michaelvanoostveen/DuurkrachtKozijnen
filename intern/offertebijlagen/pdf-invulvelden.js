/**
 * Zet op de omslag van de PDF echte invulvelden (AcroForm-tekstvelden).
 *
 * Chrome levert een platte PDF af: de stippellijnen op de omslag zijn getekend,
 * niet invulbaar. Hier worden er formuliervelden overheen gelegd, precies op de
 * plek waar die lijnen staan.
 *
 * De uitlijning wordt niet geschat maar gemeten. We laten dezelfde HTML nog een
 * keer door Chrome renderen, lezen daar de vakjes met `data-veld` uit, en
 * rekenen hun plaats om naar PDF-punten. De maatstaf is het `.page`-element van
 * 210 mm breed: de verhouding tussen zijn breedte in pixels en de breedte van de
 * PDF-pagina is de schaalfactor. Zo blijft het kloppen als de opmaak verandert.
 *
 * Let op: de schermweergave moet dan wel gelijk zijn aan de afdruk. Het sjabloon
 * heeft een media query die onder 230 mm de opmaak omgooit, dus we meten in een
 * venster dat ruim breder is.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');
const {
  PDFDocument, PDFName, PDFString, StandardFonts, rgb,
} = require('pdf-lib');

const MEETVENSTER = [1400, 2400];

/** Script dat in de pagina meet en het antwoord in de titel zet. */
const METER = `
(function(){
  var pagina = document.querySelector('.page');
  if(!pagina){ document.title = 'MEET{}'; return; }
  var pr = pagina.getBoundingClientRect();
  var kind = pagina.children;
  var laatste = kind.length ? kind[kind.length - 1].getBoundingClientRect() : null;
  var uit = {
    breedte: pr.width, hoogte: pr.height,
    voetTop: laatste ? laatste.top - pr.top : 0,
    velden: [],
  };
  Array.prototype.forEach.call(pagina.querySelectorAll('[data-veld]'), function(el){
    var r = el.getBoundingClientRect();
    uit.velden.push({
      tag: el.getAttribute('data-veld'),
      x: r.left - pr.left, y: r.top - pr.top, b: r.width, h: r.height,
    });
  });
  document.title = 'MEET' + JSON.stringify(uit);
})();
`;

/** Rendert de HTML nog een keer en leest de plaats van de invulvakken uit. */
function meet(htmlPad, chromePad) {
  const bron = fs.readFileSync(htmlPad, 'utf8');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kk-meet-'));
  const pagina = path.join(tmp, path.basename(htmlPad));
  fs.writeFileSync(pagina, bron.replace('</body>', `<script>${METER}</script></body>`));

  // De afbeeldingen staan met een relatief pad in de HTML; zonder die map
  // ernaast klapt de opmaak in elkaar en meten we de verkeerde plek.
  for (const map of ['img']) {
    const bronMap = path.join(path.dirname(htmlPad), map);
    if (fs.existsSync(bronMap)) fs.symlinkSync(bronMap, path.join(tmp, map));
  }

  try {
    const dom = execFileSync(chromePad, [
      '--headless', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
      `--window-size=${MEETVENSTER[0]},${MEETVENSTER[1]}`,
      '--virtual-time-budget=15000', '--dump-dom', `file://${pagina}`,
    ], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'ignore'] });

    const m = dom.match(/<title>MEET(\{[\s\S]*?\})<\/title>/);
    if (!m) throw new Error('kon de invulvakken niet opmeten in ' + path.basename(htmlPad));
    return JSON.parse(m[1]);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

/**
 * Legt de invulvelden op de eerste pagina van een bestaande PDF.
 * @param {string} pdfPad   het PDF-bestand, wordt ter plekke vervangen
 * @param {string} htmlPad  de HTML waar de PDF uit gemaakt is
 * @param {object[]} velden GEDEELD.velden
 * @param {string} chromePad
 * @returns {{aantal:number, schaal:number}}
 */
async function pasToe(pdfPad, htmlPad, velden, chromePad) {
  const meting = meet(htmlPad, chromePad);
  const perTag = new Map(velden.map((v) => [v.tag, v]));

  const pdf = await PDFDocument.load(fs.readFileSync(pdfPad));
  const omslag = pdf.getPage(0);
  const { width: pdfBreedte, height: pdfHoogte } = omslag.getSize();

  // Eén schaalfactor: de omslag is 210 mm breed, in pixels én in punten.
  const schaal = pdfBreedte / meting.breedte;

  // Uitlijningscontrole: velden die in dezelfde kolom staan horen op dezelfde
  // millimeter te beginnen. Een te smal labelvak duwt er stilletjes eentje uit
  // de rooilijn, en op een omslag valt dat meteen op.
  const scheefOnder = [];
  const kolommen = new Map();
  for (const vak of meting.velden) {
    const sleutel = Math.round(vak.x / 20);      // ruwe indeling in kolommen
    if (!kolommen.has(sleutel)) kolommen.set(sleutel, []);
    kolommen.get(sleutel).push(vak);
  }
  // Loopt er een veld achter de voetbalk? Die staat absoluut onderaan de omslag
  // en overdekt alles wat te laag uitkomt.
  if (meting.voetTop) {
    for (const vak of meting.velden) {
      if (vak.y + vak.h > meting.voetTop) {
        scheefOnder.push(vak.tag + ' loopt '
          + (((vak.y + vak.h) - meting.voetTop) / (96 / 25.4)).toFixed(1)
          + ' mm achter de voetbalk');
      }
    }
  }

  const scheef = scheefOnder.slice();
  for (const groep of kolommen.values()) {
    const links = groep.map((v) => v.x);
    const afwijking = Math.max(...links) - Math.min(...links);
    if (afwijking > 0.5) {                        // een halve pixel is ruis
      scheef.push(groep.map((v) => v.tag).join(', ')
        + ' — ' + (afwijking / (96 / 25.4)).toFixed(2) + ' mm verschil');
    }
  }

  const formulier = pdf.getForm();
  const font = await pdf.embedFont(StandardFonts.Helvetica);

  // In de volgorde van GEDEELD.velden, zodat Tab van boven naar beneden loopt.
  let aantal = 0;
  for (const v of velden) {
    const vak = meting.velden.find((x) => x.tag === v.tag);
    if (!vak) continue;

    // Het vakje in de HTML is de schrijfruimte; de stippellijn is zijn
    // onderrand. Het veld krijgt daarom een paar punten lucht onderaan, zodat
    // de tekst op de lijn staat en er niet doorheen zakt.
    const onderlucht = 1.2;
    const x = vak.x * schaal;
    const breedte = vak.b * schaal;
    const hoogte = vak.h * schaal;
    const y = pdfHoogte - (vak.y + vak.h) * schaal + onderlucht;

    // Géén punt in de naam: in een AcroForm betekent een punt een niveau
    // dieper in de veldboom. 'kk.klantnaam' maakt dan een ouder 'kk' met
    // kinderen eronder, en sommige lezers raken bij het opslaan alles
    // kwijt behalve het veld dat ze zelf hebben aangeraakt.
    const veld = formulier.createTextField('kk_' + v.tag);
    veld.setText('');
    veld.addToPage(omslag, {
      x, y, width: breedte, height: hoogte - onderlucht,
      textColor: rgb(1, 1, 1),                 // omslag is navy
      backgroundColor: undefined,              // stippellijn blijft zichtbaar
      borderWidth: 0,
      font,
    });
    veld.setFontSize(v.breed ? 12 : 9.5);
    veld.enableScrolling();

    // Hulptekst bij het zweven, gelijk aan de hint in het Word-bestand.
    veld.acroField.dict.set(PDFName.of('TU'), PDFString.of(v.hint));
    aantal += 1;
  }

  // pdf-lib schrijft zelf een uiterlijk per veld, met onze witte tekst. Zet hier
  // géén NeedAppearances: die vlag laat de lezer het uiterlijk opnieuw opbouwen
  // met zijn eigen standaard, en dan wordt de tekst zwart op een navy omslag.
  formulier.updateFieldAppearances(font);

  // Een AcroForm hoort zelf ook te zeggen met welk lettertype en welke kleur
  // een veld getekend wordt. Zonder /DA en /DR valt de lezer terug op zijn
  // eigen standaard — zwarte tekst op een navy omslag — en herschrijft hij bij
  // het opslaan het uiterlijk van elk veld.
  const acro = pdf.catalog.lookup(PDFName.of('AcroForm'));
  acro.set(PDFName.of('DA'), PDFString.of('1 1 1 rg /Helv 9.5 Tf'));
  const bronnen = pdf.context.obj({ Font: pdf.context.obj({ Helv: font.ref }) });
  acro.set(PDFName.of('DR'), bronnen);

  fs.writeFileSync(pdfPad, await pdf.save({ useObjectStreams: false }));
  return { aantal, schaal, scheef };
}

module.exports = { pasToe, meet };
