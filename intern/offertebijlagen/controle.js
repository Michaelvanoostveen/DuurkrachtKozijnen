/**
 * Controleert of de inhoud van een pagina binnen de pagina blijft.
 *
 * Elke `.page` is precies 297 mm hoog met `overflow: hidden`, en onderaan staat
 * een voetbalk die absoluut op `bottom: 0` ligt. Wat te lang wordt, verdwijnt
 * dus zonder waarschuwing achter die balk of onder de papierrand — je ziet het
 * pas in de PDF, en alleen als je goed kijkt.
 *
 * Dezelfde aanpak als in pdf-invulvelden.js: de HTML wordt nog een keer door
 * headless Chrome gehaald, het antwoord komt via de paginatitel terug.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

const MEETVENSTER = [1400, 2400];
const PX_PER_MM = 96 / 25.4;

/** Meet per pagina hoe ver de inhoud onder de voetbalk uitkomt. */
const METER = `
(function(){
  var uit = [];
  Array.prototype.forEach.call(document.querySelectorAll('.page'), function(pagina, i){
    var vlak = pagina.querySelector('.vlak');
    var voet = pagina.querySelector('.voet');
    if(!vlak || !voet) return;                      // de omslag heeft geen .vlak
    var grens = voet.getBoundingClientRect().top;
    var onder = 0, dieper = null;
    Array.prototype.forEach.call(vlak.querySelectorAll('*'), function(el){
      var r = el.getBoundingClientRect();
      if(!r.height) return;
      if(r.bottom > onder){ onder = r.bottom; dieper = el; }
    });
    uit.push({
      nr: i + 1,
      over: onder - grens,
      element: dieper ? (dieper.tagName.toLowerCase()
        + (dieper.className ? '.' + String(dieper.className).split(' ').join('.') : '')) : '',
    });
  });
  document.title = 'OVER' + JSON.stringify(uit);
})();
`;

/**
 * @returns {{nr:number, over:number, element:string}[]} pagina's waarvan de
 *   inhoud achter de voetbalk loopt, met de overschrijding in millimeters.
 */
function overloop(htmlPad, chromePad) {
  const bron = fs.readFileSync(htmlPad, 'utf8');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dk-over-'));
  const pagina = path.join(tmp, path.basename(htmlPad));
  fs.writeFileSync(pagina, bron.replace('</body>', `<script>${METER}</script></body>`));

  // Zonder de beeldmap ernaast klapt de opmaak in elkaar en meten we onzin.
  const bronMap = path.join(path.dirname(htmlPad), 'img');
  if (fs.existsSync(bronMap)) fs.symlinkSync(bronMap, path.join(tmp, 'img'));

  try {
    const dom = execFileSync(chromePad, [
      '--headless', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
      `--window-size=${MEETVENSTER[0]},${MEETVENSTER[1]}`,
      '--virtual-time-budget=15000', '--dump-dom', `file://${pagina}`,
    ], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'ignore'] });

    const m = dom.match(/<title>OVER(\[[\s\S]*?\])<\/title>/);
    if (!m) throw new Error('kon de pagina-inhoud niet opmeten in ' + path.basename(htmlPad));

    return JSON.parse(m[1])
      .map((p) => ({ ...p, over: p.over / PX_PER_MM }))
      .filter((p) => p.over > 0.5);                 // een halve millimeter is ruis
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

module.exports = { overloop };
