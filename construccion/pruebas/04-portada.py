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

        # El tope subio de 140 a 180 al recuperar el texto de presentacion, que
        # es contenido pedido y no relleno (DEC-57). Sigue habiendo tope: la
        # version que motivo todo esto tenia 232 palabras.
        afirma(r['palabras'] <= 180, '%s: la portada cabe en %d palabras (tope 180)' % (nom, r['palabras']))
        intro = pg.evaluate("""() => {
          const i = document.querySelector('.portada-intro'), d = document.querySelector('.dato');
          if(!i || !d) return null;
          return {texto: i.innerText.trim().length,
                  alineado: Math.abs(i.getBoundingClientRect().left - d.getBoundingClientRect().left) < 2};
        }""")
        afirma(intro is not None and intro['texto'] > 80, '%s: hay texto de presentación' % nom)
        afirma(intro and intro['alineado'], '%s: la presentación alinea con las tarjetas de datos' % nom)
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
        afirma(min(anchos) > 80, '%s: el texto de los pasos no cae en la columna del número (mínimo %d px)' % (nom, min(anchos)))
        filas = pg.evaluate("""() => {
          const li=[...document.querySelectorAll('.despues li')];
          return [...new Set(li.map(e=>Math.round(e.getBoundingClientRect().top)))].length;
        }""")
        esperado = 1 if ancho >= 620 else 2
        afirma(filas == esperado, '%s: los cuatro momentos van en %d fila(s), como corresponde al ancho' % (nom, filas))

        # El aviso de denuncia sin terminar puede acortarse, pero NUNCA puede
        # perder que aun no se ha presentado: sin esa frase alguien cierra el
        # navegador creyendo que ya denuncio (DEC-54).
        av = pg.evaluate("""() => {
          localStorage.setItem(CLAVE_BORRADOR, JSON.stringify(
            {estado:{materia:'ava', hechos:'x'.repeat(60)}, paso:3, t:Date.now()}));
          irA(0);
          const a = document.querySelector('.franja');
          const r = a ? {t: a.innerText.replace(/\\s+/g,' ').trim(),
                         botones: [...a.querySelectorAll('button')].length} : null;
          localStorage.removeItem(CLAVE_BORRADOR);
          return r;
        }""")
        afirma(av is not None, '%s: con un borrador guardado aparece el aviso' % nom)
        if av:
            afirma('no se ha presentado' in av['t'],
                   '%s: el aviso conserva que la denuncia aún no se ha presentado' % nom)
            afirma(av['botones'] == 2, '%s: el aviso ofrece continuar y descartar' % nom)
            fuera = pg.evaluate("""() => {
              localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado:{materia:'ava'}, paso:3, t:Date.now()}));
              irA(0);
              const f = document.querySelector('.franja'), app = document.getElementById('app');
              const r = {dentro: !!(f && app.contains(f)),
                         antes: !!(f && f.getBoundingClientRect().top < app.getBoundingClientRect().top)};
              irA(1);
              r.enElPaso1 = !!document.querySelector('.franja');
              irA(0);
              localStorage.removeItem(CLAVE_BORRADOR);
              return r;
            }""")
            afirma(not fuera['dentro'], '%s: el aviso vive fuera del formulario' % nom)
            afirma(fuera['antes'], '%s: y encima de la tarjeta, como franja de sistema' % nom)
            afirma(not fuera['enElPaso1'], '%s: dentro del formulario ya no aparece' % nom)
            peso = pg.evaluate("""() => {
              localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado:{materia:'ava'}, paso:3, t:Date.now()}));
              irA(0);
              const ini = [...document.querySelectorAll('#app button')].find(b => b.textContent.includes('Iniciar'));
              const con = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Continuar donde'));
              if(!ini || !con) return null;
              const r = {iniRelleno: getComputedStyle(ini).backgroundColor,
                         conRelleno: getComputedStyle(con).backgroundColor};
              localStorage.removeItem(CLAVE_BORRADOR);
              return r;
            }""")
            afirma(peso is not None and peso['iniRelleno'] != peso['conRelleno'] and 'rgb(255, 255, 255)' in peso['conRelleno'],
                   '%s: continuar es secundario y no compite con iniciar (%s vs %s)'
                   % (nom, peso and peso['conRelleno'], peso and peso['iniRelleno']))
            afirma(len(av['t'].split(' ')) <= 26,
                   '%s: el aviso se mantiene breve (%d palabras, tope 26)' % (nom, len(av['t'].split(' '))))
        pg.evaluate("irA(0)"); pg.wait_for_timeout(200)

        afirma(err == [], '%s: sin errores propios en consola: %s' % (nom, err[:2]))
        pg.close()
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
