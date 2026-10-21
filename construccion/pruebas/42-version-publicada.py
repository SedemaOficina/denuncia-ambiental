# -*- coding: utf-8 -*-
"""La versión publicada, con su mapa de Leaflet y su búsqueda de direcciones
(DEC-240; bloque 7 de la auditoría del 20 de octubre de 2026).

   docs/index.html es lo que ve la DGIVA. Donde el artefacto dibuja el mapa
   vectorial de mapa_svg.js, la publicada usa Leaflet y busca la dirección en
   Nominatim. Si Leaflet no carga, la página esconde el mapa en silencio y las
   demás baterías pasan igual: por eso ésta exige que el mapa funcione. Corre
   sobre la copia que arma publicada_de_prueba.py, con Leaflet 1.9.4 local y
   sin red.
   1. Sin red: ninguna petición sale a internet.
   2. Leaflet es la copia fijada y el mapa se dibuja en el paso 2.
   3. Un clic en el mapa coloca el punto y resuelve el área que atiende.
   4. La búsqueda de la dirección: un resultado coloca el punto; varios dan a
      elegir; ninguno lo dice.
   5. Es la versión de prueba: franja gris y sin indexar.
   6. Las páginas temporales de las baterías no viajan al repositorio (A1-02)."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = RAIZ / 'publicada-pruebas.html'
TMP  = AQUI / '_pagina42.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
if not RUTA.exists():
    sys.exit('No existe %s. Corre antes construccion/publicada_de_prueba.py (pruebas.py lo hace solo).' % RUTA.name)
TMP.write_text(RUTA.read_text(encoding='utf-8'), encoding='utf-8')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err, red = [], []
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.on('request', lambda r: red.append(r.url) if r.url.startswith('http') else None)
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 2. Leaflet fijado y el mapa en el paso 2 ----
    afirma(pg.evaluate("() => typeof L !== 'undefined' && L.version") == '1.9.4', 'Leaflet cargado es la copia fijada, 1.9.4')
    pg.evaluate("() => { estado = {}; guarda('materia','tala'); guarda('tiene_direccion','no'); irA(2); }"); pg.wait_for_timeout(600)
    m = pg.evaluate("""() => ({mapa: !!mapa, leaflet: !!document.querySelector('#mapa.leaflet-container'),
      escondido: getComputedStyle(document.getElementById('mapa')).display === 'none',
      alto: document.getElementById('mapa').clientHeight})""")
    afirma(m['mapa'] and m['leaflet'] and not m['escondido'] and m['alto'] > 100, 'el paso 2 dibuja el mapa de Leaflet, no lo esconde: %s' % m)

    # ---- 3. Un clic en el mapa ----
    c = pg.evaluate("""() => { mapa.fire('click', {latlng: L.latLng(19.4326, -99.1332)});
      return {lat: val('lat'), dg: val('dg'), marcador: !!marcador && marcador.getLatLng().lat.toFixed(4)}; }""")
    afirma(c['lat'].startswith('19.4326') and c['dg'] == 'DGIVA' and c['marcador'] == '19.4326',
           'un clic en el mapa coloca el marcador y resuelve el área que atiende: %s' % c)

    # ---- 4. La búsqueda de la dirección ----
    DIR = "estado = {}; guarda('materia','emisiones'); guarda('tiene_direccion','si'); guarda('calle','Avenida Ermita Iztapalapa'); guarda('num_ext','1200'); guarda('alcaldia_dir','Iztapalapa'); irA(2);"
    uno = pg.evaluate("""() => { %s window.RESPUESTA_DIRECCIONES = [{lat: '19.355000', lon: '-99.070000', display_name: 'Avenida Ermita Iztapalapa 1200'}];
      ubicaPorDireccion(false); return new Promise(ok => setTimeout(() => ok({lat: val('lat'), dg: val('dg'),
        marcador: !!marcador && marcador.getLatLng().lng.toFixed(2)}), 400)); }""" % DIR)
    afirma(uno['lat'].startswith('19.355') and uno['dg'] == 'DGIVA' and uno['marcador'] == '-99.07',
           'con un solo resultado, la dirección coloca el punto: %s' % uno)
    varios = pg.evaluate("""() => { %s window.RESPUESTA_DIRECCIONES = [
        {lat: '19.355000', lon: '-99.070000', display_name: 'Ermita Iztapalapa 1200, Constitución de 1917'},
        {lat: '19.357000', lon: '-99.060000', display_name: 'Ermita Iztapalapa 1200, Santa Martha'}];
      ubicaPorDireccion(false); return new Promise(ok => setTimeout(() => {
        const b = [...document.querySelectorAll('#resBusqueda button[role=option]')]; const n = b.length;
        if (b[1]) b[1].click(); ok({n, lat: val('lat')}); }, 400)); }""" % DIR)
    afirma(varios['n'] == 2 and varios['lat'].startswith('19.357'), 'con varios, da a elegir y el elegido coloca el punto: %s' % varios)
    nada = pg.evaluate("""() => { %s window.RESPUESTA_DIRECCIONES = [];
      ubicaPorDireccion(false); return new Promise(ok => setTimeout(() => ok({txt: document.getElementById('resBusqueda').innerText, lat: val('lat')}), 400)); }""" % DIR)
    afirma('No se encontró esa dirección' in nada['txt'] and not nada['lat'], 'sin resultados lo dice y no inventa un punto: %r' % nada['txt'][:60])

    # ---- 5. Es la versión de prueba ----
    p = pg.evaluate("""() => ({franja: (document.querySelector('.franja-prueba') || {}).innerText || '',
      robots: (document.querySelector('meta[name=robots]') || {}).content || ''})""")
    afirma('Versión de prueba' in p['franja'] and 'noindex' in p['robots'], 'lleva la franja de versión de prueba y no se indexa')

    # ---- 1. Sin red ----
    afirma(not red, 'ninguna petición salió a internet: %s' % red[:3])
    afirma(err == [], 'sin errores en consola: %s' % err[:2])
    nav.close()

# ---- 6. Las páginas temporales no viajan al repositorio (A1-02) ----
ignora = (RAIZ.parent / '.gitignore').read_text(encoding='utf-8')
afirma('construccion/pruebas/_pagina*.html' in ignora and 'construccion/publicada-pruebas.html' in ignora,
       '.gitignore excluye las páginas temporales de las baterías y la copia de la versión publicada')

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
