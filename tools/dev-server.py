#!/usr/bin/env python3
"""Lokale server die vercel.json nabootst: cleanUrls, trailingSlash en
redirects. Zo test je welk bestand Vercel écht uitserveert op een URL —
inclusief 308-redirects, ook meerdere sprongen na elkaar — zonder de live
site te hoeven benaderen. Handig omdat deze omgeving geen netwerktoegang
heeft tot duurkrachtkozijnen.nl.

Gebruik:  python3 tools/dev-server.py [poort]   (standaard 7799)

Voorbeeld — een redirect-keten volgen zonder dat een browser dat verbergt
(let op: gebruik http.client of curl -I, want de meeste HTTP-clients volgen
redirects automatisch en laten je dan alleen de eind-200 zien):

    curl -sI --noproxy '*' http://127.0.0.1:7799/locaties/hengelo

Dit script heeft eerder de dubbele-redirectketens (308 → 308 → 200) in
vercel.json blootgelegd die Google Search Console als "Pagina's met
omleiding" rapporteerde — zie de commit die tegelijk met dit bestand is
toegevoegd.
"""
import json, os, re, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CFG = json.load(open("vercel.json", encoding="utf-8"))
CLEAN = CFG.get("cleanUrls", False)
TRAIL = CFG.get("trailingSlash", False)

def naar_regex(bron):
    """Vercel-pad met :param en (.*) → regex."""
    r = re.escape(bron)
    r = r.replace(r"\(\.\*\)", "(.*)").replace(r"\(\[\^/\]\+\)", "([^/]+)")
    r = re.sub(r"\\:([A-Za-z0-9_]+)\\\*", r"(?P<\1>.*)", r)
    r = re.sub(r"\\:([A-Za-z0-9_]+)", r"(?P<\1>[^/]+)", r)
    return re.compile("^" + r + "$")

REDIRECTS = [(naar_regex(x["source"]), x["destination"],
              308 if x.get("permanent") else 307) for x in CFG.get("redirects", [])]

class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

    def stuur_redirect(self, naar, code):
        self.send_response(code); self.send_header("Location", naar)
        self.end_headers()
        print(f"  {self.path}  →  {code}  {naar}")

    def do_GET(self, kop_alleen=False):
        pad = urlsplit(self.path).path

        # 1. expliciete redirects uit vercel.json
        for rx, dest, code in REDIRECTS:
            m = rx.match(pad)
            if m:
                d = dest
                for k, v in (m.groupdict() or {}).items():
                    d = d.replace(f":{k}", v)
                for i, g in enumerate(m.groups() or [], 1):
                    if g is not None: d = d.replace(f"${i}", g)
                return self.stuur_redirect(d, code)

        # 2. cleanUrls: /pad.html → redirect naar /pad
        if CLEAN and pad.endswith(".html"):
            kaal = pad[:-5]
            if kaal.endswith("/index"): kaal = kaal[:-6] or "/"
            return self.stuur_redirect(kaal + ("/" if TRAIL and kaal != "/" else ""), 308)

        # 3. trailingSlash
        if TRAIL and pad != "/" and not pad.endswith("/") and "." not in os.path.basename(pad):
            return self.stuur_redirect(pad + "/", 308)
        if not TRAIL and pad != "/" and pad.endswith("/"):
            return self.stuur_redirect(pad.rstrip("/"), 308)

        # 4. welk bestand hoort hierbij?
        rel = pad.strip("/")
        for kandidaat in ([rel + "/index.html", rel + ".html"] if rel else ["index.html"]):
            if os.path.isfile(kandidaat):
                self.gevonden = kandidaat
                data = open(kandidaat, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("X-Serveert-Bestand", kandidaat)   # handig bij testen
                self.end_headers()
                if not kop_alleen: self.wfile.write(data)
                print(f"  {pad}  →  200  {kandidaat}")
                return
        if os.path.isfile(rel):
            return SimpleHTTPRequestHandler.do_GET(self)
        self.send_error(404, f"geen bestand voor {pad}")
        print(f"  {pad}  →  404")

    def do_HEAD(self): self.do_GET(kop_alleen=True)

poort = int(sys.argv[1]) if len(sys.argv) > 1 else 7799
print(f"vercel.json nagebootst op http://127.0.0.1:{poort}"
      f"  (cleanUrls={CLEAN}, trailingSlash={TRAIL}, {len(REDIRECTS)} redirects)")
ThreadingHTTPServer(("127.0.0.1", poort), H).serve_forever()
