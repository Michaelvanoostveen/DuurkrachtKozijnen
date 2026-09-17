/**
 * Maakt van de omslagvelden echte invulvelden in het Word-bestand.
 *
 * docx-js kan geen inhoudsbesturingselementen (content controls) schrijven, dus
 * bouwen we het document eerst normaal op met een markering als tekst —
 * {{veld:klantnaam}} — en vervangen die markering hier door een <w:sdt>-blok.
 *
 * Wat de gebruiker daarvan merkt: op de omslag staat grijze hinttekst, één klik
 * selecteert die helemaal, en typen vervangt hem. Tabben springt naar het
 * volgende veld. De opmaak van de oorspronkelijke run blijft behouden.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const os = require('os');

// Het vaste id dat Word zelf gebruikt voor "klik hier om tekst in te voeren".
const PLACEHOLDER = 'DefaultPlaceholder_-1854013440';

/**
 * Bouwt het <w:sdt>-blok.
 * @param {string} rPr    de <w:rPr>…</w:rPr> van de oorspronkelijke run, of ''
 * @param {object} veld   { tag, label, hint }
 * @param {number} id     uniek nummer binnen het document
 */
function sdt(rPr, veld, id) {
  const hint = veld.hint
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return '<w:sdt>'
    + '<w:sdtPr>'
      + rPr
      + `<w:alias w:val="${veld.label}"/>`
      + `<w:tag w:val="${veld.tag}"/>`
      + `<w:id w:val="${id}"/>`
      + `<w:placeholder><w:docPart w:val="${PLACEHOLDER}"/></w:placeholder>`
      + '<w:showingPlcHdr/>'
      + '<w:text/>'
    + '</w:sdtPr>'
    + '<w:sdtContent>'
      + `<w:r>${rPr}<w:t xml:space="preserve">${hint}</w:t></w:r>`
    + '</w:sdtContent>'
  + '</w:sdt>';
}

/**
 * Vervangt elke {{veld:tag}}-markering in document.xml door een invulveld.
 * @returns {number} aantal omgezette velden
 */
function zetOm(documentXml, velden) {
  const perTag = new Map(velden.map((v) => [v.tag, v]));
  let id = 90100000;
  let aantal = 0;

  // Eén hele <w:r> waarin de markering staat, inclusief de eigen opmaak.
  const runMetMarkering = /<w:r>((?:(?!<w:r>)[\s\S])*?)<w:t(?:\s[^>]*)?>\{\{veld:([a-z]+)\}\}<\/w:t>([\s\S]*?)<\/w:r>/g;

  const uit = documentXml.replace(runMetMarkering, (heel, voor, tag) => {
    const veld = perTag.get(tag);
    if (!veld) return heel;                       // onbekende markering blijft staan
    const rPr = (voor.match(/<w:rPr>[\s\S]*?<\/w:rPr>/) || [''])[0];
    aantal++;
    return sdt(rPr, veld, id++);
  });

  return { xml: uit, aantal };
}

/**
 * Past een bestaand .docx-bestand ter plekke aan.
 * Gebruikt de zip/unzip van het systeem, zodat er geen extra pakket bij hoeft.
 */
function pasToe(docxPad, velden) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kk-sdt-'));
  try {
    execFileSync('unzip', ['-q', docxPad, '-d', tmp], { stdio: 'ignore' });

    const docPad = path.join(tmp, 'word', 'document.xml');
    const { xml, aantal } = zetOm(fs.readFileSync(docPad, 'utf8'), velden);
    if (aantal === 0) return 0;
    fs.writeFileSync(docPad, xml);

    fs.rmSync(docxPad, { force: true });
    execFileSync('zip', ['-Xqr', docxPad, '.'], { cwd: tmp, stdio: 'ignore' });
    return aantal;
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

module.exports = { pasToe, zetOm, MARKERING: (tag) => `{{veld:${tag}}}` };
