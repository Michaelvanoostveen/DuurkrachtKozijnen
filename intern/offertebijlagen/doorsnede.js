/**
 * Tekent de schematische doorsnede van een kozijnprofiel.
 *
 * De diepterichting loopt verticaal: bovenin de buitenzijde, onderin de
 * binnenzijde. De maatlijn links geeft de bouwdiepte. Het aantal luchtkamers
 * is telbaar — 6 of 7 — zodat de tekening klopt met de tekst ernaast.
 */

const NAVY = '#0B5A2B', NAVY_MID = '#1A7A42', CTA = '#ED6B06', CTA_ACCENT = '#C4570A';
const STEEL = '#696960', LIJN = '#D5D5CF', KAMER = '#F1F5F2', OFF = '#FAFAFA';

// verticale banden binnen het profiel; de derde band is de versterkingskamer
const BANDEN = [
  { y: 74,  h: 64 },
  { y: 146, h: 64 },
  { y: 218, h: 76, versterking: true },
  { y: 302, h: 64 },
];

/**
 * Verdeelt het aantal kamers over de banden.
 * 6 kamers → 1 + 2 + [versterking] + 2
 * 7 kamers → 2 + 2 + [versterking] + 2
 */
function verdeling(kamers) {
  const rest = kamers - 1;                 // de versterkingskamer telt als één
  if (rest === 5) return [1, 2, null, 2];
  if (rest === 6) return [2, 2, null, 2];
  throw new Error('onverwacht aantal kamers: ' + kamers);
}

/** tekent de kamerblokjes van één profieldeel */
function profiel(x, breedte, kamers) {
  const verd = verdeling(kamers);
  const marge = 16;
  let uit = `<rect x="${x}" y="58" width="${breedte}" height="324" rx="7" fill="#FFFFFF" stroke="${NAVY}" stroke-width="3.4"/>`;

  BANDEN.forEach((band, i) => {
    if (band.versterking) {
      uit += `<rect x="${x + marge + 14}" y="${band.y}" width="${breedte - 2 * marge - 28}" height="${band.h}" rx="4" fill="url(#staal)" stroke="${NAVY}" stroke-width="3"/>`;
      return;
    }
    const n = verd[i];
    const gap = 12;
    const bin = breedte - 2 * marge;
    const w = (bin - gap * (n - 1)) / n;
    for (let k = 0; k < n; k++) {
      uit += `<rect x="${(x + marge + k * (w + gap)).toFixed(1)}" y="${band.y}" width="${w.toFixed(1)}" height="${band.h}" rx="3" fill="${KAMER}" stroke="${NAVY_MID}" stroke-width="2"/>`;
    }
  });
  return uit;
}

/** cirkel met wit nummer erin */
const nummer = (cx, cy, n, vulling = NAVY, tekst = '#FFFFFF') =>
  `<circle cx="${cx}" cy="${cy}" r="15" fill="${vulling}"/>` +
  `<text x="${cx}" y="${cy + 5}" font-family="Manrope,Arial,sans-serif" font-size="13" font-weight="800" fill="${tekst}" text-anchor="middle">${n}</text>`;

/**
 * @param {object} p  productdefinitie uit producten.js
 * @param {object} opts  { breedte, hoogte } voor een losstaande SVG
 */
function doorsnedeSvg(p, opts = {}) {
  const maat = opts.breedte
    ? ` width="${opts.breedte}" height="${opts.hoogte}"`
    : ' style="width:100%;height:auto;display:block;"';

  return `<svg viewBox="0 0 900 440"${maat} xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Schematische doorsnede van het ${p.volledig} profiel">
  <defs>
    <pattern id="staal" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="7" height="7" fill="#B0BDB4"/>
      <line x1="0" y1="0" x2="0" y2="7" stroke="#6E7E90" stroke-width="2.4"/>
    </pattern>
    <linearGradient id="glasv" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#CFE3E6"/><stop offset="1" stop-color="#AFCBD2"/>
    </linearGradient>
  </defs>

  <!-- buiten boven, binnen onder -->
  <text x="150" y="34" font-family="Manrope,Arial,sans-serif" font-size="15" font-weight="800" fill="${STEEL}" letter-spacing="2.4">BUITEN</text>
  <text x="150" y="422" font-family="Manrope,Arial,sans-serif" font-size="15" font-weight="800" fill="${STEEL}" letter-spacing="2.4">BINNEN</text>
  <line x1="232" y1="29" x2="470" y2="29" stroke="${LIJN}" stroke-width="2"/>
  <line x1="232" y1="417" x2="470" y2="417" stroke="${LIJN}" stroke-width="2"/>

  <!-- maatlijn bouwdiepte -->
  <line x1="112" y1="58" x2="112" y2="382" stroke="${CTA_ACCENT}" stroke-width="2.4"/>
  <line x1="104" y1="58" x2="120" y2="58" stroke="${CTA_ACCENT}" stroke-width="2.4"/>
  <line x1="104" y1="382" x2="120" y2="382" stroke="${CTA_ACCENT}" stroke-width="2.4"/>
  <rect x="98" y="194" width="28" height="52" rx="4" fill="${OFF}"/>
  <text x="112" y="220" font-family="Manrope,Arial,sans-serif" font-size="14" font-weight="800" fill="${CTA_ACCENT}" text-anchor="middle" transform="rotate(-90 112 220)">${p.diepte} mm</text>

  <!-- kozijn en vleugel -->
  ${profiel(150, 196, p.kamers)}
  ${profiel(386, 180, p.kamers)}

  <!-- afdichtingen: buiten, midden (accent), binnen -->
  <circle cx="366" cy="92" r="15" fill="#101418"/>
  <circle cx="366" cy="220" r="17" fill="${CTA}"/>
  <circle cx="366" cy="348" r="15" fill="#101418"/>

  <!-- glasaanslag buiten, glaspakket, glaslat binnen -->
  <rect x="566" y="128" width="40" height="46" rx="3" fill="#FFFFFF" stroke="${NAVY}" stroke-width="3"/>
  <rect x="566" y="174" width="284" height="15" fill="url(#glasv)" stroke="#6E8F98" stroke-width="1.6"/>
  <rect x="566" y="189" width="284" height="62" fill="#F2F7F8" stroke="#C6D6DA" stroke-width="1.2"/>
  <rect x="566" y="251" width="284" height="15" fill="url(#glasv)" stroke="#6E8F98" stroke-width="1.6"/>
  <rect x="566" y="174" width="284" height="92" fill="none" stroke="${NAVY}" stroke-width="2.6"/>
  <text x="726" y="226" font-family="Manrope,Arial,sans-serif" font-size="13" font-weight="700" fill="${NAVY_MID}" text-anchor="middle">4 &#8211; 16 &#8211; 4 mm</text>
  <rect x="566" y="266" width="40" height="46" rx="3" fill="#FFFFFF" stroke="${NAVY}" stroke-width="3"/>

  <!-- nummers -->
  ${nummer(289, 109, 1)}
  ${nummer(250, 220, 2)}
  <line x1="366" y1="243" x2="366" y2="282" stroke="${CTA_ACCENT}" stroke-width="2"/>
  ${nummer(366, 298, 3, CTA, '#14100A')}
  ${nummer(476, 220, 4)}
  <line x1="586" y1="312" x2="586" y2="344" stroke="${NAVY}" stroke-width="2"/>
  ${nummer(586, 360, 5)}
  <line x1="790" y1="174" x2="790" y2="140" stroke="${NAVY}" stroke-width="2"/>
  ${nummer(790, 124, 6)}

  <text x="620" y="300" font-family="Manrope,Arial,sans-serif" font-size="12" font-weight="600" fill="${STEEL}">HR++ isolatieglas, 24 mm</text>
  <text x="620" y="318" font-family="Manrope,Arial,sans-serif" font-size="12" font-weight="600" fill="${STEEL}">U<tspan dy="3" font-size="9">g</tspan><tspan dy="-3"> 1,1 W/m&#178;K</tspan></text>
</svg>`;
}

module.exports = { doorsnedeSvg };
