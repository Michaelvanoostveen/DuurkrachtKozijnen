(function () {
  if (sessionStorage.getItem('eidkk')) return;

  // Niet tonen op bedankt-, contact- en offerte-pagina's
  if (/\/(bedankt|contact|offerte)/.test(window.location.pathname)) return;

  var triggered = false;

  var WA = 'https://wa.me/31850731660';
  var WA_MSG = encodeURIComponent('Ik wil graag een gratis adviesgesprek aanvragen over kozijnen.');

  var CSS = [
    '#ei-ov{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:99999;display:flex;align-items:center;justify-content:center;padding:20px;animation:eiFade .22s ease;}',
    '@keyframes eiFade{from{opacity:0}to{opacity:1}}',
    '#ei-box{background:#fff;border-radius:16px;padding:40px 32px 32px;max-width:440px;width:100%;position:relative;box-shadow:0 20px 60px rgba(0,0,0,.22);}',
    '#ei-close{position:absolute;top:14px;right:18px;background:none;border:none;font-size:24px;line-height:1;cursor:pointer;color:#999;padding:4px 8px;}',
    '#ei-close:hover{color:#333}',
    '#ei-box h2{font-family:Fraunces,serif;font-size:1.55rem;color:#0b2218;margin:0 0 8px;line-height:1.2;}',
    '#ei-box p{font-size:15px;color:#555;margin:0 0 20px;line-height:1.55;}',
    '#ei-tel{width:100%;padding:14px 16px;border:2px solid #d0d5cc;border-radius:10px;font-size:16px;font-family:inherit;box-sizing:border-box;margin-bottom:10px;outline:none;transition:border-color .2s;}',
    '#ei-tel:focus{border-color:#0B5A2B;}',
    '#ei-cta{width:100%;padding:15px;background:#E8612C;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .2s;}',
    '#ei-cta:hover{background:#cf5225;}',
    '#ei-or{text-align:center;font-size:13px;color:#bbb;margin:14px 0 10px;}',
    '#ei-wa{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:13px;background:#25D366;color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;text-decoration:none;transition:background .2s;}',
    '#ei-wa:hover{background:#1ebe5a;}',
    '#ei-note{font-size:11.5px;color:#bbb;text-align:center;margin:14px 0 0;}',
  ].join('');

  var WA_ICON = '<svg width="20" height="20" fill="white" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';

  function show() {
    if (triggered) return;
    triggered = true;
    sessionStorage.setItem('eidkk', '1');

    var s = document.createElement('style');
    s.textContent = CSS;
    document.head.appendChild(s);

    var ov = document.createElement('div');
    ov.id = 'ei-ov';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.setAttribute('aria-label', 'Gratis adviesgesprek aanvragen');
    ov.innerHTML =
      '<div id="ei-box">' +
        '<button id="ei-close" aria-label="Sluiten">×</button>' +
        '<h2>Even twijfelen?</h2>' +
        '<p>Laat uw telefoonnummer achter. <strong>Ben belt u terug</strong> voor een gratis adviesgesprek — geen verplichtingen.</p>' +
        '<input id="ei-tel" type="tel" placeholder="Uw telefoonnummer" autocomplete="tel" />' +
        '<button id="ei-cta" type="button">Ben belt u terug →</button>' +
        '<div id="ei-or">of direct contact</div>' +
        '<a id="ei-wa" href="' + WA + '?text=' + WA_MSG + '" target="_blank" rel="noopener">' + WA_ICON + ' WhatsApp ons</a>' +
        '<p id="ei-note">Geen spam. Uw nummer wordt niet gedeeld.</p>' +
      '</div>';
    document.body.appendChild(ov);

    function close() { ov.remove(); }
    document.getElementById('ei-close').onclick = close;
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
    document.addEventListener('keydown', function h(e) {
      if (e.key === 'Escape') { close(); document.removeEventListener('keydown', h); }
    });

    document.getElementById('ei-cta').onclick = function () {
      var ph = (document.getElementById('ei-tel').value || '').trim();
      var msg = ph
        ? 'Wilt u mij terugbellen op ' + ph + ' voor een gratis adviesgesprek over kozijnen?'
        : 'Ik wil graag een gratis adviesgesprek aanvragen over kozijnen.';
      window.open(WA + '?text=' + encodeURIComponent(msg), '_blank');
      close();
    };

    document.getElementById('ei-tel').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') document.getElementById('ei-cta').click();
    });
  }

  // Desktop: muiscursor verlaat bovenkant pagina
  document.addEventListener('mouseleave', function (e) {
    if (e.clientY <= 10) show();
  });

  // Mobiel: na 20 seconden (gem. sessieduur is 32s, 50s was te laat)
  var mobileDelay = setTimeout(function () {
    if (/Mobi|Android|iPhone|iPad/i.test(navigator.userAgent)) show();
  }, 20000);

})();
