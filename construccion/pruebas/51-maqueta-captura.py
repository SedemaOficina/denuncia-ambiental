# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque E: la captura por personal
   (DEC-248).

   1. La pantalla abre el formulario en su modo captura: la liga lleva
      «?modo=captura» y apunta al prototipo que existe.
   2. Los canales de la maqueta son «En línea» y los del modo captura del
      formulario, sin copiarlos.
   3. Lista lo capturado que ve el perfil, con canal, recepción original,
      folio de origen y soporte, tal como los guardó el formulario.
   4. El expediente de lo capturado dice cómo llegó, con los bloques del
      acuse, y la pantalla deja a la vista las preguntas abiertas CP-1 a CP-5.
   5. En teléfono no hay desplazamiento horizontal."""
import json, os, pathlib, re, sys, urllib.parse
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
PROTO = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
# Lo único que la maqueta pide a internet son las tipografías; si no cargan, no
# es un error de la maqueta. Chrome no pone la dirección en el texto del aviso:
# se lee de su ubicación.
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

datos = json.loads(DATOS.read_text(encoding='utf-8'))
p = PROTO.read_text(encoding='utf-8')
bloque = p[p.index('var CANALES_CAPTURA = ['):]
bloque = bloque[:bloque.index('\n];')]
del_formulario = [{'id': i, 'nom': n} for i, n in re.findall(r"\{id:'([a-z_]+)',\s*nom:'([^']+)'", bloque)]
# El perfil de capturista ve sólo lo que capturó la persona que simula (DEC-256).
capturadas = [x for x in datos if x['canal'] != 'en_linea' and x['captura']['capturo'] == 'Capturista A (DGIVA)']

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(500)
    pg.evaluate("() => { document.getElementById('perfil').value = 'capturista_dgiva'; cambiaPerfil('capturista_dgiva'); location.hash = '#/captura'; }"); pg.wait_for_timeout(200)

    # ---- 1. La liga al modo captura ----
    href = pg.get_attribute('.acciones-captura .boton', 'href')
    destino = (MAQUETA.parent / urllib.parse.unquote(href.split('?')[0])).resolve()
    afirma(href.endswith('?modo=captura') and destino == PROTO.resolve(),
           'la pantalla abre el prototipo del formulario en modo captura: %s' % href)

    # ---- 2. Canales ----
    canales = pg.evaluate("() => CANALES")
    afirma(len(del_formulario) == 4 and canales == [{'id': 'en_linea', 'nom': 'En línea'}] + del_formulario,
           'los canales son «En línea» y los cuatro del modo captura del formulario: %s' % [c['id'] for c in canales])

    # ---- 3. Lo capturado ----
    filas = pg.evaluate("""() => [...document.querySelectorAll('.tabla-chica tbody tr')].map(tr => [...tr.children].map(c => c.textContent))""")
    nombres = {c['id']: c['nom'] for c in canales}
    esperado = {x['datos']['folio']: [nombres[x['canal']], x['datos']['folio_origen'], x['datos']['soporte']] for x in capturadas}
    vistas = {f[0]: [f[1], f[3], f[4]] for f in filas}
    afirma(vistas == esperado and all(x['datos'].get('fecha_recepcion_original') for x in capturadas),
           'lista lo capturado, %d denuncias, con canal, folio de origen y soporte como los guardó el formulario' % len(filas))
    texto = pg.inner_text('#pantalla')
    afirma(all(('CP-%d' % n) in texto for n in range(1, 6)), 'deja a la vista las preguntas abiertas CP-1 a CP-5')

    # ---- 4. El expediente de lo capturado ----
    pg.click('.tabla-chica tbody tr >> nth=0 >> a'); pg.wait_for_timeout(200)
    exp = pg.evaluate("() => [...document.querySelectorAll('.seccion-exp h4')].map(h => h.textContent)")
    afirma(pg.evaluate("() => location.hash").startswith('#/expediente/') and exp and exp[0] == 'Cómo llegó',
           'el expediente de lo capturado empieza su denuncia por «Cómo llegó», como el acuse: %s' % exp[:2])
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/bandeja'); tel.wait_for_timeout(400)
    tel.evaluate("() => { cambiaPerfil('capturista_dgiva'); location.hash = '#/captura'; }"); tel.wait_for_timeout(200)
    afirma(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth") <= 0, 'a 360 px no hay desplazamiento horizontal')
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
