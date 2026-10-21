# -*- coding: utf-8 -*-
"""«Atrás» y «Adelante» del navegador recorren los pasos (DEC-241).

   La auditoría del 20 de octubre encontró que «Atrás» salía del formulario
   (C4-01): en el teléfono, el gesto de regreso llevaba a la página anterior.
   Liber Saltijeral decidió que regrese al paso anterior. Se comprueba con los
   botones del navegador:
   1. «Atrás» regresa al paso anterior y «Adelante» vuelve, sin perder lo
      capturado.
   2. Desde el acuse no se regresa a la revisión: la denuncia ya se envió.
   3. Tras recargar la página, «Atrás» lleva a la portada, que ofrece retomar
      el borrador, en lugar de un paso vacío."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina43.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':844}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    donde = lambda: pg.evaluate("() => ({paso: paso, h2: ((document.querySelector('#app .tarjeta h2') || {}).textContent || '').trim()})")
    def atras(): pg.go_back(); pg.wait_for_timeout(250)
    def adelante(): pg.go_forward(); pg.wait_for_timeout(250)

    # ---- 1. Atrás y Adelante entre pasos ----
    pg.evaluate("() => { cargaEscenario('urbano'); irA(1); irA(2); irA(3); }"); pg.wait_for_timeout(300)
    pg.evaluate("() => guarda('hechos', 'Humo negro del taller todas las tardes desde agosto, entra a las casas vecinas.')")
    atras()
    d = donde(); afirma(d['paso'] == 2, '«Atrás» desde el paso 3 regresa al 2: %s' % d)
    atras()
    d = donde(); afirma(d['paso'] == 1, 'y otra vez, al 1: %s' % d)
    adelante(); adelante()
    d = donde(); h = pg.evaluate("() => val('hechos')")
    afirma(d['paso'] == 3 and h.startswith('Humo negro'), '«Adelante» vuelve al 3 sin perder lo capturado: %s' % d)
    foco = pg.evaluate("() => document.activeElement && document.activeElement.tagName")
    afirma(foco == 'H2', 'y el foco va al título del paso, como al avanzar con el botón')

    # ---- 2. Desde el acuse no se regresa ----
    pg.evaluate("() => { cargaEscenario('urbano'); guarda('verificacion','si'); irA(6); enviar(); }"); pg.wait_for_timeout(300)
    folio = pg.evaluate("() => val('folio')")
    atras()
    d = donde(); afirma(d['paso'] == 7 and pg.evaluate("() => val('folio')") == folio,
                        'desde el acuse, «Atrás» no regresa a la revisión: la denuncia ya se envió (%s)' % d)

    # ---- 3. Tras recargar, Atrás lleva a la portada ----
    pg.evaluate("() => { borraBorrador(); cargaEscenario('urbano'); irA(2); irA(3); }"); pg.wait_for_timeout(300)
    pg.reload(); pg.wait_for_timeout(700)
    atras()
    r = pg.evaluate("() => ({paso: paso, franja: document.getElementById('franjaBorrador').innerText, app: document.getElementById('app').innerText.trim().length})")
    afirma(r['paso'] == 0 and 'Tienes una denuncia sin terminar' in r['franja'] and r['app'] > 200,
           'tras recargar, «Atrás» lleva a la portada, que ofrece retomar el borrador: %s' % {k: r[k] for k in ('paso', 'app')})
    pg.evaluate("() => borraBorrador()")

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
