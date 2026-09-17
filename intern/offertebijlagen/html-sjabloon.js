/**
 * Bouwt de HTML-versie van een offertebijlage: zeven A4-pagina's die op het
 * scherm te bekijken zijn en via de printfunctie een nette PDF opleveren.
 */
const { GEDEELD } = require('./producten');
const { doorsnedeSvg } = require('./doorsnede');

const esc = (s) => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/**
 * Vinklijst met vetgedrukte kop per punt.
 * De inhoud gaat in één <span>: `ul.vink li` is een flexbox met gap, dus elk
 * los kindelement zou anders als apart flex-item met tussenruimte landen.
 */
const vinkKop = (items) => items
  .map(([kop, rest]) => `<li><span><strong>${esc(kop)}</strong> ${esc(rest)}</span></li>`).join('\n          ');

const streepjes = (items) => items
  .map((x) => `<li>${esc(x)}</li>`).join('\n          ');

const CSS = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  /* Huisstijl Duurkracht: groen als dragende kleur, oranje als accent en lime
     als lichte tint op donkergroen — dezelfde rollen als in /css/site.css. */
  :root {
    --navy: #0B5A2B; --navy-deep: #074120; --navy-mid: #1A7A42; --navy-tint: #E8F0EB;
    --cta: #ED6B06; --cta-tekst: #14100A; --cta-diep: #C4570A;
    --cta-accent: #C4570A; --cta-tekst-licht: #D3CF29;
    --amber-tint: #FDE9D6; --steel: #696960; --steel-soft: #B0BDB4;
    --ink: #0E0E0E; --rule: #EAEAE6; --off: #FAFAFA; --wit: #FFFFFF;
    --sans: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    --serif: 'Fraunces', Georgia, 'Times New Roman', serif;
  }

  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family: var(--sans); font-size: 9.6pt; line-height: 1.6;
         color: var(--ink); background: #8D9A90; padding: 8mm 0; }

  .page { width: 210mm; height: 297mm; background: var(--wit); margin: 0 auto 9mm;
          position: relative; overflow: hidden; box-shadow: 0 3mm 9mm rgba(16,20,24,.28);
          page-break-after: always; break-after: page; }
  .page:last-child { page-break-after: auto; break-after: auto; margin-bottom: 0; }

  @page { size: A4; margin: 0; }
  @media print { body { background: none; padding: 0; } .page { margin: 0; box-shadow: none; } }

  .em-italic { font-family: var(--serif); font-style: italic; font-weight: 400; }

  .kop { display: flex; justify-content: space-between; align-items: center;
         padding: 6mm 14mm 4mm; border-bottom: 1px solid var(--rule); }
  .kop .merk img { height: 7mm; display: block; }
  .kop .doc { font-size: 6.6pt; color: var(--steel); letter-spacing: .06em;
              text-transform: uppercase; font-weight: 600; text-align: right; }

  .voet { position: absolute; bottom: 0; left: 0; right: 0; height: 12mm;
          background: var(--navy); display: flex; justify-content: space-between;
          align-items: center; padding: 0 14mm; }
  .voet span { color: var(--steel-soft); font-size: 6.6pt; }
  .voet strong { color: var(--wit); font-weight: 700; }
  .voet .pg { color: var(--wit); font-size: 6.6pt; font-weight: 700;
              background: rgba(255,255,255,.14); border-radius: 2mm; padding: .8mm 2.6mm; }

  .vlak { padding: 6mm 14mm 14mm; }

  .ey { font-size: 6.8pt; font-weight: 800; text-transform: uppercase;
        letter-spacing: .16em; color: var(--cta-accent); margin-bottom: 2.4mm; }
  .ey.licht { color: var(--cta-tekst-licht); }

  h2 { font-size: 20pt; font-weight: 800; line-height: 1.12; color: var(--navy); letter-spacing: -.012em; }
  h3 { font-size: 11pt; font-weight: 800; color: var(--navy); line-height: 1.3; }
  h4 { font-size: 8.6pt; font-weight: 800; color: var(--navy);
       text-transform: uppercase; letter-spacing: .07em; margin-bottom: 2mm; }

  p { font-size: 9.4pt; line-height: 1.68; color: #4A4A44; }
  p + p { margin-top: 2.6mm; }
  .lood { font-size: 10.6pt; line-height: 1.62; color: #4A4A44; }
  .klein { font-size: 7.8pt; line-height: 1.55; color: var(--steel); }

  .streep { width: 13mm; height: 2.6px; background: var(--cta); border-radius: 2px; margin: 2.6mm 0 3.4mm; }

  .g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
  .g3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 4.5mm; }
  .g4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 3.5mm; }

  .cijfer { background: var(--navy); border-radius: 2.5mm; padding: 3.4mm 4mm; text-align: center; }
  .cijfer .n { font-size: 17pt; font-weight: 800; color: var(--cta-tekst-licht);
               line-height: 1.05; letter-spacing: -.02em; }
  .cijfer .n small { font-size: 9pt; font-weight: 700; }
  .cijfer .l { font-size: 6.8pt; color: var(--steel-soft); margin-top: 1.4mm; line-height: 1.4; }

  ul.vink { list-style: none; display: flex; flex-direction: column; gap: 1.9mm; }
  ul.vink li { display: flex; align-items: flex-start; gap: 2.6mm; font-size: 9pt;
               line-height: 1.55; color: #4A4A44; }
  ul.vink li::before {
    content: ""; flex: 0 0 3.6mm; width: 3.6mm; height: 3.6mm; margin-top: 1.1mm;
    border-radius: 50%; background: var(--cta);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'><path d='M3 6.2l2.1 2.1L9.2 4.2' fill='none' stroke='%2314100A' stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round'/></svg>");
    background-size: 3.6mm 3.6mm; }
  ul.vink.blauw li::before { background-color: var(--navy);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'><path d='M3 6.2l2.1 2.1L9.2 4.2' fill='none' stroke='white' stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round'/></svg>"); }

  ul.streepjes { list-style: none; display: flex; flex-direction: column; gap: 1.4mm; }
  ul.streepjes li { position: relative; padding-left: 4mm; font-size: 8.8pt;
                    line-height: 1.55; color: #4A4A44; }
  ul.streepjes li::before { content: ""; position: absolute; left: 0; top: 1.9mm;
                            width: 2mm; height: 1.4px; background: var(--steel); }

  table.spec { width: 100%; border-collapse: collapse; font-size: 8.6pt; }
  table.spec caption { caption-side: top; text-align: left; font-size: 8.6pt; font-weight: 800;
                       color: var(--navy); text-transform: uppercase; letter-spacing: .07em;
                       padding-bottom: 1.5mm; }
  table.spec th { background: var(--navy); color: var(--wit); text-align: left; font-size: 7.4pt;
                  font-weight: 700; letter-spacing: .07em; text-transform: uppercase; padding: 2.4mm 3.5mm; }
  table.spec td { padding: 1.3mm 3.2mm; line-height: 1.38; border-bottom: 1px solid var(--rule);
                  color: #4A4A44; vertical-align: top; }
  table.spec tr:nth-child(even) td { background: var(--off); }
  table.spec td:first-child { font-weight: 700; color: var(--navy); width: 42%; }
  table.spec tr:last-child td { border-bottom: none; }

  .kader { border: 1px solid var(--rule); border-radius: 2.5mm; padding: 3.6mm 4.6mm; }
  .kader.tint { background: var(--navy-tint); border-color: #CFDDD4; }
  .kader.navy { background: var(--navy); border-color: var(--navy); }
  .kader.navy h4 { color: var(--cta-tekst-licht); }
  .kader.navy p, .kader.navy li { color: var(--steel-soft); }

  .let-op { border-left: 3px solid var(--cta); background: var(--amber-tint);
            border-radius: 0 2mm 2mm 0; padding: 3mm 4.2mm; }
  .let-op p { font-size: 8.4pt; color: #4A3A28; }

  figure { margin: 0; }
  figure img { display: block; width: 100%; object-fit: cover; border-radius: 2.5mm; }
  figcaption { font-size: 7.2pt; color: var(--steel); margin-top: 1.6mm; line-height: 1.45; }

  .stap { display: flex; gap: 4mm; align-items: flex-start; padding: 1.2mm 0; border-bottom: 1px solid var(--rule); }
  .stap:last-child { border-bottom: none; }
  .stap .nr { flex: 0 0 7.5mm; width: 7.5mm; height: 7.5mm; border-radius: 50%;
              background: var(--navy); color: var(--wit); font-size: 8.4pt; font-weight: 800;
              display: flex; align-items: center; justify-content: center; }
  .stap .tx h4 { margin-bottom: 1mm; }
  .stap .tx p { font-size: 8.6pt; }

  /* invulregels op de omslag: label links, schrijfruimte rechts */
  .veld { display: flex; align-items: baseline; gap: 4mm; padding: 2.4mm 0; }
  /* 28 mm, niet 26: "OFFERTENUMMER" is in kapitalen met letterspatiëring
     27,3 mm breed, en een flex-item krimpt niet onder zijn inhoud. Bij 26 mm
     duwde dat ene label zijn invulregel 1,2 mm naar rechts, uit de rooilijn
     van de andere velden. */
  .veld .lb { flex: 0 0 28mm; font-size: 7.2pt; color: var(--steel-soft);
              text-transform: uppercase; letter-spacing: .1em; font-weight: 700;
              white-space: nowrap; }
  .veld .invul { flex: 1 1 auto; height: 4.6mm;
                 border-bottom: 1px dotted rgba(255,255,255,.42); }
  .veld.breed { padding-bottom: 3.2mm; margin-bottom: 1.4mm;
                border-bottom: 1px solid rgba(255,255,255,.14); }
  .veld.breed .lb { flex-basis: 28mm; }
  .veld.breed .invul { height: 6mm; }

  .leg { display: grid; grid-template-columns: repeat(2,1fr); gap: 2mm 5mm; }
  .leg div { display: flex; gap: 2.2mm; align-items: flex-start; font-size: 8pt;
             line-height: 1.45; color: #4A4A44; }
  .leg b { flex: 0 0 4.6mm; width: 4.6mm; height: 4.6mm; border-radius: 50%; background: var(--navy);
           color: var(--wit); font-size: 6.4pt; font-weight: 800; display: flex;
           align-items: center; justify-content: center; margin-top: .3mm; }

  @media screen and (max-width: 230mm) {
    body { padding: 4mm 0; }
    .page { width: 100%; max-width: 210mm; height: auto; min-height: 0; padding-bottom: 14mm; }
    .voet { position: static; height: auto; padding: 4mm 14mm; margin-top: 8mm; }
    .vlak { padding-bottom: 6mm; }
  }
`;

function html(p) {
  const G = GEDEELD;
  const paginaVoet = (n) => `
  <div class="voet">
    <span><strong>${G.bedrijf}</strong> · ${G.payoff}</span>
    <span class="pg">${n}</span>
  </div>`;

  const paginaKop = `
  <div class="kop">
    <div class="merk"><img src="img/logo.png" alt="${G.bedrijf}"></div>
    <div class="doc">Productbijlage · ${esc(p.volledig)}</div>
  </div>`;

  const specTabel = (kop, rijen) => `
    <table class="spec">
      <caption>${esc(kop)}</caption>
      <tbody>
        ${rijen.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('\n        ')}
      </tbody>
    </table>`;

  return `<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(p.volledig)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,600&display=swap" rel="stylesheet">
<style>${CSS}</style>
</head>
<body>

<!-- ══════ 1 · OMSLAG ══════ -->
<div class="page" style="background:var(--navy-deep);">
  <div style="position:absolute;inset:0;">
    <img src="img/cover.jpg" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42;">
    <div style="position:absolute;inset:0;background:linear-gradient(175deg,rgba(7,65,32,.70) 0%,rgba(7,65,32,.88) 52%,rgba(7,65,32,.97) 100%);"></div>
  </div>
  <div style="position:absolute;top:0;left:0;right:0;height:3.2mm;background:linear-gradient(90deg,var(--cta) 0%,var(--cta-diep) 55%,var(--navy-mid) 100%);"></div>

  <!-- De voetbalk hieronder staat absoluut op bottom:0 en telt dus niet mee in
       de kolom. Zonder die 24 mm onderaan schuift het invulpaneel eronder en
       verdwijnen "Adviseur" en "Geldig tot" achter de balk. -->
  <div style="position:relative;height:100%;display:flex;flex-direction:column;padding:16mm 16mm 24mm;">
    <div style="background:var(--wit);border-radius:3mm;padding:6mm 8mm;align-self:flex-start;box-shadow:0 2mm 7mm rgba(0,0,0,.26);">
      <img src="img/logo.png" alt="${G.bedrijf} — ${G.payoff}" style="height:17mm;display:block;">
    </div>

    <div style="margin-top:auto;padding-top:12mm;padding-bottom:6mm;">
      <div class="ey licht" style="margin-bottom:4mm;">Productbijlage bij uw offerte</div>
      <h2 style="color:var(--wit);font-size:34pt;line-height:1.06;letter-spacing:-.022em;">
        ${esc(p.titelRegels[0])}<br>${esc(p.titelRegels[1])}<span style="color:var(--cta-tekst-licht);">${esc(p.titelRegels[2])}</span>
      </h2>
      <div style="width:20mm;height:3px;background:var(--cta);border-radius:2px;margin:6mm 0 5mm;"></div>
      <p style="color:rgba(255,255,255,.90);font-size:12pt;line-height:1.6;max-width:128mm;">
        Kunststof kozijnen met <strong style="color:#fff;">${p.diepte} mm bouwdiepte</strong>,
        een <strong style="color:#fff;">${esc(p.kamersWoord)}</strong> en
        <strong style="color:#fff;">tien jaar garantie</strong> op product én montage.
      </p>
      <p class="em-italic" style="color:var(--cta-tekst-licht);font-size:13pt;margin-top:5mm;">${G.payoff}</p>
    </div>

    <div style="background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);border-radius:3mm;padding:5mm 6mm;">
      ${G.velden.filter((v) => v.breed).map((v) => `
      <div class="veld breed"><span class="lb">${esc(v.label)}</span><span class="invul" data-veld="${v.tag}"></span></div>`).join('')}
      <div class="g2" style="gap:0 9mm;margin-top:1mm;">
        ${G.velden.filter((v) => !v.breed).map((v) => `
        <div class="veld"><span class="lb">${esc(v.label)}</span><span class="invul" data-veld="${v.tag}"></span></div>`).join('')}
      </div>
    </div>
  </div>

  <div style="position:absolute;bottom:0;left:0;right:0;background:rgba(4,40,20,.74);padding:5mm 16mm;display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div style="color:var(--wit);font-size:9.6pt;font-weight:800;">${G.bedrijf} B.V.</div>
      <div style="color:var(--steel-soft);font-size:7.4pt;margin-top:.6mm;">${G.plaats} · werkzaam in heel Nederland</div>
      <div style="color:var(--steel-soft);font-size:7.4pt;">KvK ${G.kvk} · btw ${G.btw}</div>
    </div>
    <div style="text-align:right;color:var(--steel-soft);font-size:7.4pt;line-height:1.75;">
      ${G.telefoon} · ${G.email}<br>${G.web}
    </div>
  </div>
</div>

<!-- ══════ 2 · WAAROM DIT PROFIEL ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak">
    <div class="ey">Waarover deze bijlage gaat</div>
    <h2>Het profiel dat wij<br>voor u hebben gekozen</h2>
    <div class="streep"></div>

    <div class="g2" style="gap:7mm;align-items:start;">
      <div>
        <p class="lood" style="margin-bottom:3mm;">
          In uw offerte staat wát wij leveren en wat het kost. Deze bijlage laat zien
          <span class="em-italic">waaruit</span> uw kozijnen bestaan: het profiel, het glas,
          het hang- en sluitwerk en de garantie die u erop krijgt.
        </p>
        ${p.intro.map((t) => `<p>${esc(t)}</p>`).join('\n        ')}
      </div>
      <figure>
        <img src="img/sfeer-1.jpg" alt="Kunststof kozijnen en voordeur in antraciet" style="height:74mm;">
        <figcaption>Uitgevoerd werk: kozijnen en voordeur in antraciet, geplaatst door onze eigen monteurs.</figcaption>
      </figure>
    </div>

    <div class="g4" style="margin-top:6mm;">
      <div class="cijfer"><div class="n">${p.diepte}<small> mm</small></div><div class="l">Bouwdiepte<br>van het profiel</div></div>
      <div class="cijfer"><div class="n">${p.kamers}</div><div class="l">Kamers<br>in kozijn en vleugel</div></div>
      <div class="cijfer"><div class="n">${p.uf}</div><div class="l">U<sub>f</sub>-waarde<br>W/m²K</div></div>
      <div class="cijfer"><div class="n">10<small> jaar</small></div><div class="l">Garantie op<br>product én montage</div></div>
    </div>

    <div style="margin-top:6mm;" class="g2">
      <div>
        <h4>Wat dit voor u betekent</h4>
        <ul class="vink">
          ${vinkKop(p.voordelen)}
        </ul>
      </div>
      <div class="kader tint">
        <h4>Twee lijnen, één keuze</h4>
        ${p.keuzeKader.map((t) => `<p style="font-size:8.8pt;">${esc(t)}</p>`).join('\n        ')}
        <p class="klein" style="margin-top:3mm;">
          Tot aan het bouwkundig inmeten kunt u nog van profiel wisselen. Vraag ons gerust om een vergelijking.
        </p>
      </div>
    </div>
  </div>
  ${paginaVoet(2)}
</div>

<!-- ══════ 3 · DOORSNEDE ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak">
    <div class="ey">Het profiel van binnen</div>
    <h2>${p.kamers === 6 ? 'Zes' : 'Zeven'} kamers, drie afdichtingen</h2>
    <div class="streep"></div>

    <p style="max-width:150mm;">
      Hieronder ziet u een doorsnede door kozijn en draaiend deel: bovenin de buitenzijde,
      onderin uw woonkamer. De ${p.kamers === 6 ? 'zes' : 'zeven'} kamers, de drievoudige
      afdichting en de versterkingskamer zijn de drie onderdelen die het verschil maken.
    </p>

    <div style="background:var(--off);border:1px solid var(--rule);border-radius:2.5mm;padding:5mm 5mm 3mm;margin:4mm 0 4mm;">
      ${doorsnedeSvg(p)}
      <p class="klein" style="text-align:center;margin-top:1mm;">
        Schematische weergave — bedoeld om de opbouw uit te leggen, niet op schaal en niet maatvoerend.
      </p>
    </div>

    <div class="leg">
      ${G.legenda(p).map(([kop, rest], i) =>
        `<div><b>${i + 1}</b><span><strong>${esc(kop)}</strong> ${esc(rest)}</span></div>`).join('\n      ')}
    </div>

    <div class="let-op" style="margin-top:4.5mm;">
      <p><strong>${esc(p.slotKader[0])}.</strong> ${esc(p.slotKader[1])}</p>
    </div>
  </div>
  ${paginaVoet(3)}
</div>

<!-- ══════ 4 · SPECIFICATIES ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak">
    <div class="ey">Specificaties</div>
    <h2>Technische gegevens</h2>
    <div class="streep"></div>

    ${specTabel('Profielsysteem', G.specRijen(p).map(([a, b]) => [
      a.replace(/^Uf-waarde/, 'U<sub>f</sub>-waarde').replace(/^Uw-waarde/, 'U<sub>w</sub>-waarde'),
      esc(b),
    ]))}

    <div class="g2" style="margin-top:5mm;gap:6mm;align-items:start;">
      <div>
        ${specTabel('Standaard beglazing', [
          ['Type', G.glas.type],
          ['Opbouw', G.glas.opbouw],
          ['U<sub>g</sub>-waarde', G.glas.ug],
          ['Vulling', G.glas.vulling],
          ['Norm', G.glas.norm],
        ])}
        <p class="klein" style="margin-top:2.5mm;">
          Triple beglazing (HR+++), geluidwerend glas, zonwerend glas en veiligheidsglas volgens
          NEN 3569 zijn leverbaar tegen meerprijs. Wat er in úw offerte staat, leest u op het
          offerteblad zelf.
        </p>
      </div>

      <div class="kader navy">
        <h4>Wat de U-waarde betekent</h4>
        <p style="font-size:8.8pt;margin-bottom:2.5mm;">
          De U-waarde zegt hoeveel warmte er per vierkante meter verloren gaat.
          <strong style="color:#fff;">Hoe lager, hoe beter.</strong>
        </p>
        <ul class="streepjes" style="margin-top:1mm;">
          <li style="color:var(--steel-soft);"><strong style="color:#fff;">U<sub>f</sub></strong> — alleen het kozijnprofiel</li>
          <li style="color:var(--steel-soft);"><strong style="color:#fff;">U<sub>g</sub></strong> — alleen het glas</li>
          <li style="color:var(--steel-soft);"><strong style="color:#fff;">U<sub>w</sub></strong> — het complete raam, glas en profiel samen</li>
        </ul>
        <p style="font-size:8.4pt;margin-top:3mm;color:var(--steel-soft);">
          Ter vergelijking: enkel glas in een houten kozijn zit rond de 5,0 W/m²K.
          Uw nieuwe kozijnen met HR++ komen op ongeveer 1,2 — ruim vier keer zo goed.
        </p>
      </div>
    </div>

    <div class="let-op" style="margin-top:4.5mm;">
      <p>
        <strong>Over de opgegeven waarden.</strong> De genoemde U-waarden zijn systeemwaarden van
        de fabrikant, gemeten onder genormeerde omstandigheden. De werkelijke waarde van úw raam
        hangt af van de maat, de indeling en het gekozen glas. De definitieve prestaties leggen we
        vast bij het bouwkundig inmeten.
      </p>
    </div>
  </div>
  ${paginaVoet(4)}
</div>

<!-- ══════ 5 · VEILIGHEID & UITVOERING ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak">
    <div class="ey">Veiligheid, bediening en uitvoering</div>
    <h2>Zoals u hem straks<br>gebruikt</h2>
    <div class="streep"></div>

    <div class="g2" style="gap:6mm;align-items:start;">
      <div>
        <h4>Hang- en sluitwerk</h4>
        <ul class="vink blauw">
          ${G.sluitwerk.map(([a, b, c]) => `<li><span>${esc(a)}<strong>${esc(b)}</strong>${esc(c)}</span></li>`).join('\n          ')}
        </ul>
      </div>
      <figure>
        <img src="img/sfeer-4.jpg" alt="Draai-kiepraam van binnenuit gezien" style="height:52mm;">
        <figcaption>Draai-kiepraam van binnenuit: naar binnen draaiend, met twee ventilatiestanden.</figcaption>
      </figure>
    </div>

    <div class="g2" style="gap:6mm;margin-top:5mm;align-items:start;">
      <div>
        <h4>Kleuren en afwerking</h4>
        <p style="font-size:8.8pt;">
          Standaard leveren wij in <strong>wit RAL 9010</strong>. De ${esc(p.model)} is daarnaast
          leverbaar met gekleurde folie aan de buitenzijde en wit aan de binnenzijde — de meest
          gekozen combinatie in Nederland.
        </p>
        <ul class="streepjes" style="margin-top:3mm;">
          ${streepjes(G.kleuren)}
        </ul>
      </div>
      <div>
        <h4>Afwerking binnen</h4>
        <p style="font-size:8.8pt;">
          Na de montage werken wij de aansluiting tussen kozijn en binnenmuur af met een kunststof
          hoek, zodat u geen stuc- of schilderwerk hoeft te laten doen. Standaardkleuren zijn
          wit RAL 9016 en crème RAL 9001, glad.
        </p>
        <h4 style="margin-top:4mm;">Vensterbanken</h4>
        <p style="font-size:8.8pt;">
          Waar nu een vensterbank zit, plaatsen wij er een terug — tenzij anders afgesproken.
          Onze vensterbanken zijn krasvast, UV-bestendig en ongevoelig voor vocht en warmte.
        </p>
      </div>
    </div>

    <div style="margin-top:5mm;">
      <h4>Uitgevoerd werk</h4>
      <div class="g3" style="margin-top:2.5mm;">
        <figure><img src="img/sfeer-2.jpg" alt="Kunststof kozijnen en deuren in een bakstenen gevel" style="height:40mm;"></figure>
        <figure><img src="img/sfeer-3.jpg" alt="Kunststof schuifpui naar de achtertuin" style="height:40mm;"></figure>
        <figure><img src="img/sfeer-5.jpg" alt="Nieuwe voordeur met zijlicht in antraciet" style="height:40mm;"></figure>
      </div>
      <p class="klein" style="margin-top:2mm;">
        Projecten van ${G.bedrijf}. Uitvoeringen kunnen per woning verschillen; uw eigen indeling,
        kleur en draairichting leggen we vast bij het bouwkundig inmeten.
      </p>
    </div>
  </div>
  ${paginaVoet(5)}
</div>

<!-- ══════ 6 · GARANTIE ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak">
    <div class="ey">Garantiebepalingen</div>
    <h2>Tien jaar, op product<br>én op montage</h2>
    <div class="streep"></div>

    <p style="max-width:152mm;">
      Wij leveren en monteren in eigen beheer. Daardoor hoeft u bij een klacht niet te zoeken wie
      verantwoordelijk is: u meldt het bij ons, en wij lossen het op. Eén aanspreekpunt, voor zowel
      het product als het werk.
    </p>

    <div class="g3" style="margin-top:3.5mm;">
      <div class="cijfer"><div class="n">10<small> jaar</small></div><div class="l">Op het kozijnprofiel<br>in basiskleur</div></div>
      <div class="cijfer"><div class="n">10<small> jaar</small></div><div class="l">Op de montage<br>door onze monteurs</div></div>
      <div class="cijfer"><div class="n">10<small> jaar</small></div><div class="l">Op de beglazing<br>HR++ en HR+++</div></div>
    </div>

    <div class="g2" style="margin-top:3.5mm;gap:6mm;align-items:start;">
      <div>
        <h4>Waarop de garantie geldt</h4>
        <ul class="vink blauw">
          ${vinkKop(G.garantieGeldt)}
        </ul>
      </div>
      <div>
        <h4>Waarop de garantie niet geldt</h4>
        <ul class="streepjes">
          ${streepjes(G.garantieNiet)}
        </ul>
      </div>
    </div>

    <div class="kader tint" style="margin-top:3.5mm;">
      <h4>Voorwaarden waaronder de garantie loopt</h4>
      <div class="g2" style="gap:3mm 6mm;margin-top:1mm;">
        <ul class="streepjes">${streepjes(G.garantieVoorwaarden.slice(0, 3))}</ul>
        <ul class="streepjes">${streepjes(G.garantieVoorwaarden.slice(3))}</ul>
      </div>
    </div>

    <div class="g2" style="margin-top:3mm;gap:6mm;align-items:start;">
      <div class="kader" style="background:var(--amber-tint);border-color:#F6D8BC;">
        <h4>Service melden</h4>
        <p style="font-size:8.6pt;">
          Een gebrek meldt u bij ons kantoor, met foto's en het offerte- of factuurnummer.
          Wij nemen binnen vijf werkdagen contact op om een afspraak te plannen.
        </p>
        <p style="font-size:8.6pt;margin-top:2mm;"><strong>${G.telefoon}</strong> · <strong>${G.email}</strong></p>
      </div>
      <div class="let-op">
        <p>
          <strong>Voorrang van voorwaarden.</strong> Deze bijlage vat de garantie samen en is bedoeld
          om u te informeren. Op al onze leveringen, offertes en overeenkomsten zijn onze algemene
          verkoop- en leveringsvoorwaarden van toepassing. Wijkt de tekst hierboven daarvan af, dan
          gaan de algemene voorwaarden en de offerte zelf voor.
        </p>
      </div>
    </div>
  </div>
  ${paginaVoet(6)}
</div>

<!-- ══════ 7 · MONTAGE & AFSPRAKEN ══════ -->
<div class="page">
  ${paginaKop}
  <div class="vlak" style="padding-bottom:10mm;">
    <div class="ey">Van akkoord tot oplevering</div>
    <h2>Hoe wij het uitvoeren</h2>
    <div class="streep"></div>

    <div class="g2" style="gap:7mm;align-items:start;">
      <div>
        ${G.stappen(p).map(([kop, tekst], i) => `
        <div class="stap">
          <div class="nr">${i + 1}</div>
          <div class="tx"><h4>${esc(kop)}</h4><p>${esc(tekst)}</p></div>
        </div>`).join('')}
      </div>

      <div>
        <figure style="margin-bottom:5mm;">
          <img src="img/montage.jpg" alt="Montage van kunststof kozijnen" style="height:55mm;">
          <figcaption>Montage in eigen beheer — geen onderaannemers.</figcaption>
        </figure>
        <div class="kader tint">
          <h4>Wat wij van u vragen</h4>
          <ul class="streepjes">${streepjes(G.klantvraag)}</ul>
        </div>
      </div>
    </div>

    <div class="g2" style="margin-top:3.5mm;gap:6mm;align-items:start;">
      <div>
        <h4>Standaard inbegrepen</h4>
        <ul class="vink">${streepjes(G.inbegrepen)}</ul>
      </div>
      <div>
        <h4>Niet inbegrepen, tenzij vermeld op de offerte</h4>
        <ul class="streepjes">${streepjes(G.nietInbegrepen)}</ul>
      </div>
    </div>

    <div style="margin-top:4mm;background:var(--navy);border-radius:3mm;padding:5mm 7mm;display:flex;justify-content:space-between;align-items:center;gap:6mm;">
      <div>
        <div class="ey licht" style="margin-bottom:2mm;">Vragen over deze bijlage?</div>
        <p style="color:var(--wit);font-size:11pt;line-height:1.5;font-weight:600;margin-bottom:2mm;">
          Bel of app ons gerust — wij lopen de offerte<br>graag punt voor punt met u door.
        </p>
        <p style="color:var(--steel-soft);font-size:8.4pt;">${G.bedrijf} B.V. · ${G.plaats} · KvK ${G.kvk}</p>
      </div>
      <div style="text-align:right;flex-shrink:0;">
        <div style="color:var(--cta-tekst-licht);font-size:14pt;font-weight:800;">${G.telefoon}</div>
        <div style="color:var(--wit);font-size:9pt;margin-top:1.5mm;">${G.email}</div>
        <div style="color:var(--steel-soft);font-size:9pt;">${G.web}</div>
      </div>
    </div>

    <p class="klein" style="margin-top:2.5mm;text-align:center;">${esc(G.voorbehoud)}</p>
  </div>
  ${paginaVoet(7)}
</div>

</body>
</html>`;
}

module.exports = { html };
