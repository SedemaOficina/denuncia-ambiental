# -*- coding: utf-8 -*-
"""Jerarquia visual: paso, seccion, subseccion, pregunta, respuesta y ayuda.

   Antes de DEC-64 el titulo del paso y el de seccion eran identicos -20 px,
   Cabin 600, guinda- y la respuesta se veia MAS GRANDE que la pregunta. Esta
   bateria fija la regla: cada nivel se distingue del contiguo por al menos dos
   rasgos, y la pregunta nunca es menor que su respuesta."""
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

MEDIR = """(sel) => {
  const e = document.querySelector(sel); if(!e) return null;
  const c = getComputedStyle(e);
  return {px: parseFloat(c.fontSize), peso: c.fontWeight,
          fam: c.fontFamily.split(',')[0].replace(/['"]/g,''),
          color: c.color, may: c.textTransform,
          borde: c.borderTopWidth !== '0px'};
}"""
def rasgos(a, b):
    return [k for k in ['px','peso','fam','color','may','borde'] if a.get(k) != b.get(k)]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1000,'height':1000}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    pg.evaluate("cfg.validar=true; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(3)")
    pg.wait_for_timeout(450)
    paso    = pg.evaluate(MEDIR, '.tarjeta h2')
    seccion = pg.evaluate(MEDIR, '.sub-seccion')
    pregunta= pg.evaluate(MEDIR, '.campo label')
    respuesta=pg.evaluate(MEDIR, '#f_hechos')
    ayuda   = pg.evaluate(MEDIR, '.campo .ayuda')
    pg.evaluate("guarda('folio','X'); irA(7)"); pg.wait_for_timeout(400)
    subseccion = pg.evaluate(MEDIR, '.sub-seccion-sm')

    for nom, x in [('paso',paso),('sección',seccion),('subsección',subseccion),
                   ('pregunta',pregunta),('respuesta',respuesta),('ayuda',ayuda)]:
        afirma(x is not None, 'se encuentra el nivel «%s»' % nom)

    # Cada nivel contiguo se separa por dos rasgos o mas.
    for a, b, na, nb in [(paso,seccion,'paso','sección'), (seccion,subseccion,'sección','subsección'),
                         (subseccion,pregunta,'subsección','pregunta'), (pregunta,respuesta,'pregunta','respuesta'),
                         (respuesta,ayuda,'respuesta','ayuda')]:
        if a and b:
            r = rasgos(a, b)
            afirma(len(r) >= 2, '%s y %s se distinguen por %d rasgos: %s' % (na, nb, len(r), r))

    # Ninguna respuesta puede verse mas grande que su pregunta.
    afirma(pregunta['px'] >= respuesta['px'],
           'la pregunta no es menor que la respuesta (%s vs %s px)' % (pregunta['px'], respuesta['px']))
    afirma(paso['px'] > seccion['px'] > pregunta['px'],
           'la escala baja del paso a la sección y de ahí a la pregunta (%s > %s > %s)'
           % (paso['px'], seccion['px'], pregunta['px']))
    afirma(ayuda['px'] < pregunta['px'], 'la ayuda es menor que la pregunta')

    # --- Peso de las acciones: avanzar, retroceder y responder ---
    # El acuse no tiene ninguno de los tres: se mide en un paso del formulario.
    pg.evaluate("irA(3)"); pg.wait_for_timeout(350)
    acc = pg.evaluate("""() => {
      const NEUTRO = ['rgba(0, 0, 0, 0)', 'transparent', 'rgb(255, 255, 255)'];
      const g = e => { if(!e) return null; const c = getComputedStyle(e);
        return {borde: c.borderTopWidth !== '0px',
                relleno: NEUTRO.indexOf(c.backgroundColor) < 0, fondo: c.backgroundColor}; };
      return {atras: g(document.querySelector('.btn-atras')),
              continuar: g([...document.querySelectorAll('.btn-primario')].pop()),
              sino: g(document.querySelector('.btn-sn'))};
    }""")
    afirma(acc['atras'] is not None, 'el control de retroceso existe')
    afirma(acc['atras'] and not acc['atras']['borde'] and not acc['atras']['relleno'],
           'retroceder no lleva borde ni relleno: es navegación, no una respuesta')
    afirma(acc['sino'] and acc['sino']['borde'] and not acc['sino']['relleno'],
           'responder lleva borde y fondo neutro (%s)' % (acc['sino'] and acc['sino']['fondo']))
    afirma(acc['continuar'] and acc['continuar']['relleno'],
           'avanzar es lo único con relleno de color: una acción principal por pantalla (%s)'
           % (acc['continuar'] and acc['continuar']['fondo']))
    alto = pg.evaluate("() => Math.round(document.querySelector('.btn-atras').getBoundingClientRect().height)")
    afirma(alto >= 44, 'retroceder conserva el blanco táctil de 44 px (%d)' % alto)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
