/*
 * Embed-brug voor de configurator.
 *
 * Draait in TWEE rollen, afhankelijk van waar het script geladen wordt:
 *
 *  1. In de configurator zelf (binnen de iframe, alleen bij ?embed=1)
 *     -> meet de eigen hoogte en stuurt die naar de parent, zodat de iframe
 *        meegroeit en er nooit een interne scrollbar ontstaat.
 *
 *  2. Op de homepage (de parent)
 *     -> luistert naar die berichten en past de iframe-hoogte aan.
 *
 * Berichten zijn same-origin en worden gevalideerd op afzender en vorm.
 */
(function () {
  'use strict';

  var MSG = 'duurkracht:cfg-height';

  // ---------------------------------------------------------------- IFRAME
  // Alleen actief in embed-modus én wanneer we daadwerkelijk in een frame zitten.
  function initChild() {
    var last = 0;

    // Meet de BODY, niet documentElement: dat laatste rekt mee met de
    // iframe-viewport, waardoor de hoogte alleen kan groeien en nooit meer
    // krimpt (terugkoppel-lus). De body volgt puur de inhoud.
    function measure() {
      var b = document.body;
      if (!b) return 0;
      var cs = getComputedStyle(b);
      return Math.ceil(
        b.getBoundingClientRect().height +
        parseFloat(cs.marginTop || 0) +
        parseFloat(cs.marginBottom || 0)
      );
    }

    function report() {
      var h = measure();
      if (!h) return;
      // Ruis onderdrukken: alleen melden bij een merkbare wijziging.
      if (Math.abs(h - last) < 2) return;
      last = h;
      parent.postMessage({ type: MSG, height: h }, location.origin);
    }

    // ResizeObserver vangt alles op: stap wisselen, variant kiezen, viewport.
    if (window.ResizeObserver) {
      new ResizeObserver(report).observe(document.body);
    } else {
      window.addEventListener('resize', report);
      setInterval(report, 500);
    }

    window.addEventListener('load', report);
    document.addEventListener('click', function () { setTimeout(report, 60); });
    report();
  }

  // ---------------------------------------------------------------- PARENT
  function initParent(frame) {
    window.addEventListener('message', function (e) {
      if (e.origin !== location.origin) return;
      var d = e.data;
      if (!d || d.type !== MSG || typeof d.height !== 'number') return;
      if (e.source !== frame.contentWindow) return;
      // Ondergrens voorkomt dat de iframe inklapt tijdens het laden.
      frame.style.height = Math.max(d.height, 520) + 'px';
    });
  }

  var inFrame = window.parent !== window;
  var isEmbed = document.documentElement.classList.contains('is-embed');

  if (inFrame && isEmbed) {
    initChild();
  } else {
    var frame = document.getElementById('cfg-embed');
    if (frame) initParent(frame);
  }
})();
