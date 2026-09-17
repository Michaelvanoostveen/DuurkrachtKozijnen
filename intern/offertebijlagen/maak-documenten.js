#!/usr/bin/env node
/**
 * Bouwt de offertebijlagen voor alle profielen in producten.js.
 *
 * Per profiel komen er drie bestanden uit:
 *   <slug>.html   — preview in de browser, en de bron voor de PDF
 *   <naam>.docx   — bewerkbare versie voor Word
 *   <naam>.pdf    — versie om aan de offerte in Teamleader te koppelen
 *
 * Draaien:
 *   npm install             (eenmalig, in deze map)
 *   node maak-documenten.js
 *
 * De doorsnedetekening en de PDF worden met headless Chrome gerenderd; geef een
 * ander pad mee via CHROME= als Chrome ergens anders staat.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const { PRODUCTEN, GEDEELD } = require('./producten');
const { doorsnedeSvg } = require('./doorsnede');
const { html } = require('./html-sjabloon');
const woord = require('./word-sjabloon');
const invulvelden = require('./invulvelden');
const pdfvelden = require('./pdf-invulvelden');
const controle = require('./controle');

const HIER = __dirname;
const IMG = path.join(HIER, 'img');
const WORD_IMG = path.join(HIER, 'word-img');
const TMP = fs.mkdtempSync(path.join(require('os').tmpdir(), 'kk-bijlage-'));

const CHROME = process.env.CHROME
  || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

function chrome(args) {
  execFileSync(CHROME, [
    '--headless', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
    '--virtual-time-budget=15000', ...args,
  ], { stdio: ['ignore', 'ignore', 'ignore'] });
}

/** rendert de doorsnede-SVG naar een PNG, voor gebruik in het Word-bestand */
function maakDoorsnede(p) {
  const breedte = 1800, hoogte = 880;
  const pagina = path.join(TMP, `ds-${p.slug}.html`);
  fs.writeFileSync(pagina, `<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<style>html,body{margin:0;padding:0;background:#fff}#w{width:${breedte}px;height:${hoogte}px;background:#fff}</style>
</head><body><div id="w">${doorsnedeSvg(p, { breedte, hoogte })}</div></body></html>`);

  const uit = path.join(WORD_IMG, `doorsnede-${p.slug}.png`);
  chrome([`--window-size=${breedte},${hoogte}`, `--screenshot=${uit}`, `file://${pagina}`]);
  if (!fs.existsSync(uit)) throw new Error('doorsnede renderen mislukt voor ' + p.slug);
  return uit;
}

/** rendert de HTML-preview naar een A4-PDF */
function maakPdf(htmlPad, pdfPad) {
  chrome(['--no-pdf-header-footer', `--print-to-pdf=${pdfPad}`, `file://${htmlPad}`]);
  if (!fs.existsSync(pdfPad)) throw new Error('PDF renderen mislukt: ' + pdfPad);
}

(async () => {
  for (const p of PRODUCTEN) {
    console.log(`\n── ${p.volledig} ──`);

    maakDoorsnede(p);
    console.log('  doorsnede  word-img/doorsnede-' + p.slug + '.png');

    const htmlPad = path.join(HIER, `${p.slug}.html`);
    fs.writeFileSync(htmlPad, html(p));
    console.log('  html       ' + path.basename(htmlPad));

    for (const pg of controle.overloop(htmlPad, CHROME)) {
      console.log(`             OVERLOOP: pagina ${pg.nr} loopt `
        + `${pg.over.toFixed(1)} mm achter de voetbalk (${pg.element})`);
    }

    const docxPad = path.join(HIER, `${p.bestandsnaam}.docx`);
    try {
      const n = await woord.schrijf(p, WORD_IMG, docxPad);
      const velden = invulvelden.pasToe(docxPad, GEDEELD.velden);
      console.log(`  word       ${path.basename(docxPad)} (${(n / 1024).toFixed(0)} kB, ${velden} invulvelden)`);
      if (velden !== GEDEELD.velden.length) {
        console.log(`             LET OP: ${GEDEELD.velden.length} velden verwacht`);
      }
    } catch (e) {
      // Word houdt een geopend bestand vast; dan blijft de vorige versie staan
      console.log('  word       OVERGESLAGEN — ' + e.message);
    }

    const pdfPad = path.join(HIER, `${p.bestandsnaam}.pdf`);
    maakPdf(htmlPad, pdfPad);
    const pv = await pdfvelden.pasToe(pdfPad, htmlPad, GEDEELD.velden, CHROME);
    console.log(`  pdf        ${path.basename(pdfPad)} (${pv.aantal} invulvelden)`);
    if (pv.aantal !== GEDEELD.velden.length) {
      console.log(`             LET OP: ${GEDEELD.velden.length} velden verwacht`);
    }
    for (const s of pv.scheef) console.log('             UITLIJNING: ' + s);
  }

  fs.rmSync(TMP, { recursive: true, force: true });
  console.log('\nKlaar.');
})();
