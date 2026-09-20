# -*- coding: utf-8 -*-
"""La pantalla de inicio (DEC-53).

   Tenia 232 palabras en cuatro cajas identicas y el boton de empezar a 1 268 px:
   casi dos pantallas de desplazamiento antes de poder hacer nada. Ademas repetia
   el titulo y la bajada que ya estan en el encabezado institucional de la pagina.
   Estas comprobaciones fijan lo que no debe volver a crecer."""
import os, pathlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
import sys

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho, alto, nom in [(390, 760, 'teléfono'), (1100, 800, 'escritorio')]:
        pg = nav.new_context(viewport={'width':ancho,'height':alto}).new_page()
        err = []
        pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
        pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

        r = pg.evaluate("""() => {
          const a = document.getElementById('app');
          const t = a.innerText.replace(/\\s+/g,' ').trim();
          const b = [...a.querySelectorAll('button')].find(x => x.textContent.includes('Iniciar'));
          const enc = document.querySelector('.titulo h1, .titulo');
          return {
            palabras: t.split(' ').length,
            botonY: b ? Math.round(b.getBoundingClientRect().top + window.scrollY) : null,
            cajas: a.querySelectorAll('.aviso').length,
            datos: a.querySelectorAll('.dato').length,
            pasos: a.querySelectorAll('.despues li').length,
            chips: a.querySelectorAll('.tener span').length,
            encabezado: enc ? enc.innerText.replace(/\\s+/g,' ').trim() : '',
            tarjeta: t,
            desborde: document.documentElement.scrollWidth > window.innerWidth
          };
        }""")

        afirma(r['palabras'] <= 140, '%s: la portada cabe en %d palabras (tope 140)' % (nom, r['palabras']))
        afirma(r['botonY'] is not None and r['botonY'] < alto,
               '%s: el botón de iniciar se ve sin desplazar (a %s px de %d)' % (nom, r['botonY'], alto))
        afirma(r['cajas'] == 0, '%s: no quedan cajas de aviso apiladas (%d)' % (nom, r['cajas']))
        afirma(r['datos'] == 3 and r['pasos'] == 4 and r['chips'] == 3,
               '%s: tres datos, cuatro pasos y tres etiquetas' % nom)
        afirma(not r['desborde'], '%s: sin desbordamiento horizontal' % nom)

        # El encabezado de la pagina ya titula y describe: la tarjeta no lo repite.
        afirma('Denuncia Ambiental en línea' not in r['tarjeta'],
               '%s: la tarjeta no repite el título del encabezado' % nom)
        afirma('dañan el ambiente en la Ciudad de México' not in r['tarjeta'],
               '%s: la tarjeta no repite la bajada del encabezado' % nom)

        # El texto de cada paso ocupa su propia celda: una linea, no una palabra por linea.
        anchos = pg.evaluate("""() => [...document.querySelectorAll('.despues span')]
            .map(e => Math.round(e.getBoundingClientRect().width))""")
        afirma(min(anchos) > 150, '%s: el texto de los pasos no se parte por palabra (mínimo %d px)' % (nom, min(anchos)))

        afirma(err == [], '%s: sin errores propios en consola: %s' % (nom, err[:2]))
        pg.close()
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
