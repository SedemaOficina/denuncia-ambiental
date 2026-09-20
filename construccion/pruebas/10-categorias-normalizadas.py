# -*- coding: utf-8 -*-
"""Las categorías de las capas, normalizadas en el dato (DEC-87).

   El origen trae la misma categoría escrita de dos formas —«Zona Ecologica y
   Cultural» y «Zona Ecológica y Cultural»—, y agrupar por ese texto produce
   categorías fantasma. La normalización ocurre al ingresar la capa, no en la
   pantalla: aquí se comprueba que el dato que llega al navegador ya viene
   normalizado y que no quedó ninguna traducción al vuelo."""
import os, pathlib, sys, unicodedata, collections
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina10.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

def plano(s):
    return unicodedata.normalize('NFD', s).encode('ascii','ignore').decode().lower()

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    d = pg.evaluate("""() => ({
      total: CAPAS_GEOM.length,
      sinCategoria: CAPAS_GEOM.filter(f => !f.p.categoria).length,
      sinClave: CAPAS_GEOM.filter(f => !f.p.categoria_clave).length,
      nombres: [...new Set(CAPAS_GEOM.map(f => f.p.categoria))],
      claves: [...new Set(CAPAS_GEOM.map(f => f.p.categoria_clave))],
      pares: CAPAS_GEOM.map(f => [f.p.categoria_clave, f.p.categoria]),
      normCat: typeof normCat, CATEGORIAS: typeof CATEGORIAS
    })""")

    afirma(d['sinCategoria'] == 0 and d['sinClave'] == 0,
           'los %d rasgos traen categoría y clave (%d y %d sin ellas)'
           % (d['total'], d['sinCategoria'], d['sinClave']))
    afirma(len(d['nombres']) == len(d['claves']),
           'hay tantos nombres como claves: %d y %d' % (len(d['nombres']), len(d['claves'])))

    # Ninguna categoría puede diferir de otra sólo por acentos o mayúsculas.
    colisiones = [v for v, n in collections.Counter(plano(x) for x in d['nombres']).items() if n > 1]
    afirma(colisiones == [], 'ninguna categoría se repite con otra acentuación: %s' % colisiones)

    # Una clave, un nombre: si una clave tuviera dos nombres, la agrupación mentiría.
    porClave = collections.defaultdict(set)
    for clave, nombre in d['pares']:
        porClave[clave].add(nombre)
    sueltas = {k: sorted(v) for k, v in porClave.items() if len(v) > 1}
    afirma(sueltas == {}, 'cada clave tiene un solo nombre: %s' % sueltas)

    # Las claves son estables: sin acentos, sin espacios, sin mayúsculas.
    malas = [k for k in d['claves'] if k != plano(k) or ' ' in k]
    afirma(malas == [], 'las claves son estables —sin acentos ni espacios—: %s' % malas)

    # Y la categoría que se muestra sí lleva sus acentos.
    afirma(any('ó' in x or 'á' in x or 'é' in x for x in d['nombres']),
           'los nombres que se muestran conservan la acentuación')

    afirma(d['normCat'] == 'undefined' and d['CATEGORIAS'] == 'undefined',
           'no quedó traducción al vuelo en la pantalla: la capa llega normalizada')

    # El cruce sigue dando la categoría correcta y acentuada.
    r = pg.evaluate("""() => { ponMarcador(19.2900, -99.2000);
      return {tipo: val('capa_tipo'), nombre: val('capa_nombre'), dg: val('dg_nombre')}; }""")
    afirma('Tlalpan' in (r['nombre'] or ''), 'el cruce sigue reconociendo el Bosque de Tlalpan: %r' % r['nombre'])

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
