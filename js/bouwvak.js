/* Bouwvakmelding — sluitingsperiode op één plek beheerd.
 *
 * AANPASSEN VOOR EEN VOLGENDE PERIODE: alleen VAN en TOT hieronder wijzigen.
 * TOT is de eerste werkdag dat we weer open zijn; de melding verdwijnt dan
 * vanzelf. Staat er niets meer te sluiten, zet dan ACTIEF op false.
 *
 * De melding bestaat uit twee delen, allebei gestuurd door dezelfde periode:
 *   1. een balkje in de topbar (site-breed, via tracking.js)
 *   2. een pop-up op de homepage (dit bestand)
 */
(function () {
  'use strict';

  var ACTIEF = true;
  var VAN = '2026-08-07';   // eerste dag gesloten
  var TOT = '2026-08-10';   // eerste dag weer open — melding verdwijnt vanaf deze datum
  var TOT_LABEL = 'maandag 10 augustus';

  // Datum in Nederland, ongeacht de tijdzone van de bezoeker
  function vandaagNL() {
    var p = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'Europe/Amsterdam', year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(new Date());
    function v(t) { return p.find(function (x) { return x.type === t; }).value; }
    return v('year') + '-' + v('month') + '-' + v('day');
  }

  var nu = vandaagNL();
  var loopt = ACTIEF && nu >= VAN && nu < TOT;

  // Beschikbaar voor tracking.js (topbar) en exit-intent.js (niet stapelen)
  window.DKK_BOUWVAK = { loopt: loopt, tot: TOT_LABEL };

  if (!loopt) return;
  if (window.location.pathname !== '/' && !/\/index\.html$/.test(window.location.pathname)) return;
  try { if (sessionStorage.getItem('dkk_bouwvak')) return; } catch (e) {}

  function start() {
    try { sessionStorage.setItem('dkk_bouwvak', '1'); } catch (e) {}

    var css = document.createElement('style');
    css.textContent = [
      '#bv-ov{position:fixed;inset:0;background:rgba(8,20,14,.6);z-index:100000;display:flex;',
        'align-items:center;justify-content:center;padding:20px;animation:bvIn .22s ease}',
      '@keyframes bvIn{from{opacity:0}to{opacity:1}}',
      '@keyframes bvUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}',
      '#bv-box{background:#fff;border-radius:16px;max-width:470px;width:100%;position:relative;',
        'box-shadow:0 24px 70px rgba(0,0,0,.28);overflow:hidden;animation:bvUp .28s ease}',
      '#bv-kop{background:#0B5A2B;color:#fff;padding:26px 30px 22px}',
      '#bv-eyebrow{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:700;',
        'letter-spacing:.13em;text-transform:uppercase;color:#D3CF29;margin:0 0 10px}',
      '#bv-eyebrow::before{content:"";width:7px;height:7px;border-radius:50%;background:#ED6B06}',
      '#bv-kop h2{font-family:Fraunces,Georgia,serif;font-weight:500;font-size:1.6rem;line-height:1.2;',
        'margin:0;color:#fff}',
      '#bv-body{padding:24px 30px 28px}',
      '#bv-body p{font-size:15.5px;line-height:1.6;color:#2a2a2a;margin:0 0 16px}',
      '#bv-body p:last-of-type{margin-bottom:22px}',
      '#bv-datum{background:#e8f0eb;border-left:4px solid #0B5A2B;border-radius:0 10px 10px 0;',
        'padding:13px 16px;margin:0 0 18px;font-size:15px;color:#0E0E0E}',
      '#bv-datum strong{color:#0B5A2B}',
      '#bv-acties{display:flex;flex-direction:column;gap:10px}',
      '#bv-acties a,#bv-sluit{display:flex;align-items:center;justify-content:center;gap:8px;',
        'padding:14px 18px;border-radius:999px;font-size:15px;font-weight:700;font-family:inherit;',
        'text-decoration:none;cursor:pointer;border:none;transition:background .18s,border-color .18s}',
      '#bv-offerte{background:#ED6B06;color:#fff}',
      '#bv-offerte:hover{background:#d45f05}',
      '#bv-sluit{background:#fff;color:#4a4a44;border:1px solid #EAEAE6}',
      '#bv-sluit:hover{border-color:#0B5A2B;color:#0B5A2B}',
      '#bv-x{position:absolute;top:14px;right:16px;background:rgba(255,255,255,.16);border:none;',
        'color:#fff;font-size:20px;line-height:1;cursor:pointer;width:32px;height:32px;border-radius:50%;',
        'display:flex;align-items:center;justify-content:center;transition:background .18s}',
      '#bv-x:hover{background:rgba(255,255,255,.3)}',
      'a:focus-visible,button:focus-visible{outline:2px solid #ED6B06;outline-offset:2px}',
      '@media(max-width:480px){#bv-kop{padding:22px 22px 18px}#bv-body{padding:20px 22px 24px}',
        '#bv-kop h2{font-size:1.35rem}}',
      '@media(prefers-reduced-motion:reduce){#bv-ov,#bv-box{animation:none}}'
    ].join('');
    document.head.appendChild(css);

    var ov = document.createElement('div');
    ov.id = 'bv-ov';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.setAttribute('aria-labelledby', 'bv-titel');
    ov.innerHTML =
      '<div id="bv-box">' +
        '<div id="bv-kop">' +
          '<button id="bv-x" type="button" aria-label="Melding sluiten">&times;</button>' +
          '<p id="bv-eyebrow">Bouwvakvakantie</p>' +
          '<h2 id="bv-titel">We zijn even dicht</h2>' +
        '</div>' +
        '<div id="bv-body">' +
          '<p>Ons kantoor en onze monteurs hebben bouwvakvakantie. Daardoor kunnen we u deze dagen even niet persoonlijk te woord staan.</p>' +
          '<p id="bv-datum">Vanaf <strong>' + TOT_LABEL + '</strong> staan we weer voor u klaar — en helpen we u graag verder.</p>' +
          '<p>Uw aanvraag kunt u gewoon achterlaten. We nemen alles op volgorde van binnenkomst door en nemen direct na de vakantie contact met u op.</p>' +
          '<div id="bv-acties">' +
            '<a id="bv-offerte" href="/offerte-aanvragen/">Vrijblijvend offerte aanvragen&nbsp;&rarr;</a>' +
            '<button id="bv-sluit" type="button">Ik kijk eerst even rond</button>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(ov);

    var terug = document.activeElement;
    var sluitKnop = document.getElementById('bv-sluit');
    if (sluitKnop) sluitKnop.focus();

    function sluit() {
      ov.remove();
      document.removeEventListener('keydown', opToets);
      if (terug && terug.focus) terug.focus();
    }
    function opToets(e) {
      if (e.key === 'Escape') { sluit(); return; }
      if (e.key !== 'Tab') return;
      // focus binnen de dialoog houden
      var f = ov.querySelectorAll('a[href],button');
      if (!f.length) return;
      var eerste = f[0], laatste = f[f.length - 1];
      if (e.shiftKey && document.activeElement === eerste) { e.preventDefault(); laatste.focus(); }
      else if (!e.shiftKey && document.activeElement === laatste) { e.preventDefault(); eerste.focus(); }
    }
    document.addEventListener('keydown', opToets);
    document.getElementById('bv-x').onclick = sluit;
    sluitKnop.onclick = sluit;
    ov.addEventListener('click', function (e) { if (e.target === ov) sluit(); });
    document.getElementById('bv-offerte').addEventListener('click', function () {
      if (window.gtag) gtag('event', 'bouwvak_offerte', { melding: 'bouwvak' });
    });

    if (window.gtag) gtag('event', 'bouwvak_melding_getoond', { tot: TOT });
  }

  // Even wachten zodat de pagina eerst zichtbaar is — een melding die meteen
  // over een lege pagina valt, leest als een storing.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(start, 900); });
  } else {
    setTimeout(start, 900);
  }
})();
