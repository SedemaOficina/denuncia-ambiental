# -*- coding: utf-8 -*-
"""El codigo plus y el enlace corto de Google Maps (DEC-82).

   Un enlace `maps.app.goo.gl` no lleva la coordenada dentro y el navegador no
   puede canjearlo. El codigo plus si la lleva y se decodifica con aritmetica,
   sin red. Estas comprobaciones fijan que el decodificador es correcto contra
   los ejemplos publicados de la especificacion, que la recuperacion de un
   codigo corto funciona en toda la Ciudad —incluido el sureste, donde cambia
   el bloque de un grado— y que el enlace corto deja de ser un callejon."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina07.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# Ejemplos publicados de la especificacion Open Location Code.
PATRON = [('8FVC2222+22', 47.0000625, 8.0000625),
          ('796RWF8Q+WF', 14.9173125, -23.5113125)]
# Cuatro puntos de la Ciudad, uno en cada rumbo. El de Milpa Alta cae en otro
# bloque de un grado que el centro, que es donde falla una recuperacion ingenua.
CIUDAD = [(19.4326, -99.1332, 'Zócalo'), (19.2900, -99.2000, 'Bosque de Tlalpan'),
          (19.5900, -99.0300, 'norte de Gustavo A. Madero'), (19.1000, -98.9500, 'sureste de Milpa Alta')]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. El decodificador, contra los ejemplos publicados ----
    for codigo, la, lo in PATRON:
        r = pg.evaluate("(c)=>descifraPlus(c)", codigo)
        ok = r and abs(r['lat']-la) < 1e-6 and abs(r['lon']-lo) < 1e-6
        afirma(ok, '%s decodifica a %s, %s como manda la especificación' % (codigo, la, lo))

    # ---- 2. La recuperacion del codigo corto, en los cuatro rumbos ----
    for lat, lon, nom in CIUDAD:
        pref = pg.evaluate("([a,b])=>cifraPlus(a,b)", [lat, lon])
        ida  = pg.evaluate("(c)=>descifraPlus(c)", pref)
        rec  = pg.evaluate("(c)=>recuperaPlus(c,19.36,-99.13)", pref[4:]+'+22')
        cerca = rec and abs(rec['lat']-ida['lat']) < 0.01 and abs(rec['lon']-ida['lon']) < 0.01
        afirma(cerca, 'un código corto del %s se recupera en su sitio (%s)' % (nom, pref))

    # ---- 3. Lo que el campo acepta ----
    casos = [
      ("19.3579, -99.1610", True,  'coordenadas sueltas'),
      ("76F2CVM8+22",       True,  'código plus completo'),
      ("CVM8+22 Ciudad de México", True, 'código plus corto con la localidad detrás'),
      ("https://www.google.com/maps/@19.3579,-99.1610,17z", True, 'enlace largo de Google Maps'),
      ("https://maps.app.goo.gl/4iwJgrZVKKrEHH2u8?g_st=ic", False, 'enlace corto, que no la trae'),
      ("por el taller de la esquina", False, 'texto cualquiera'),
    ]
    for texto, esperado, nom in casos:
        r = pg.evaluate("(t)=>leeCoordenadas(t)", texto)
        afirma((r is not None) == esperado, 'se reconoce lo que debe: %s' % nom)
        if r and esperado:
            afirma(-90 <= r['lat'] <= 90 and -180 <= r['lon'] <= 180,
                   'y la coordenada que devuelve es válida: %s' % nom)

    # ---- 4. El enlace corto no es un callejon sin salida ----
    r = pg.evaluate("""() => {
      cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','no'); irA(2);
      guarda('coord_pegar','https://maps.app.goo.gl/4iwJgrZVKKrEHH2u8?g_st=ic');
      colocaPorTexto();
      const c = document.getElementById('resBusqueda');
      const a = c ? c.querySelector('a[target="_blank"]') : null;
      return {texto: c ? c.innerText.replace(/\\s+/g,' ') : '',
              abre: !!a, destino: a ? a.getAttribute('href') : '',
              rel: a ? a.getAttribute('rel') : '',
              demo: !!(c && [...c.querySelectorAll('button')].some(b => b.textContent.indexOf('funcionará') >= 0)),
              pasos: c ? c.querySelectorAll('ol li').length : 0};
    }""")
    afirma('No lleva la coordenada dentro' in r['texto'],
           'el aviso explica por qué ese enlace no sirve todavía')
    afirma('servidor de la Secretaría' in r['texto'],
           'y dice quién lo va a resolver, en vez de culpar a la persona')
    afirma('sin que tu navegador hable con Google' in r['texto'],
           'y que resolverlo ahí evita que Google sepa que alguien denuncia (DEC-88)')
    afirma(r['abre'] and r['destino'].startswith('https://maps.app.goo.gl/'),
           'ofrece abrir el propio enlace que se pegó')
    afirma('noopener' in r['rel'], 'la pestaña nueva se abre sin dar control sobre la nuestra')
    afirma(r['pasos'] == 2, 'la salida son dos pasos, no un párrafo')
    afirma(r['demo'], 'y se puede ver cómo funcionará, a petición')

    # La demostración coloca un punto fijo: no puede hacerlo sin avisarlo, o
    # alguien dará por buena una coordenada inventada.
    d = pg.evaluate("""() => {
      demoEnlace();
      const c = document.getElementById('resBusqueda');
      return {texto: c ? c.innerText.replace(/\\s+/g,' ') : '',
              lat: val('lat'), chip: c ? c.querySelectorAll('.pendiente').length : 0};
    }""")
    afirma(d['lat'] != '', 'la demostración coloca el punto')
    afirma('no se resolvió de verdad' in d['texto'],
           'y advierte que la coordenada es de demostración')
    afirma(d['chip'] >= 1, 'con la marca de pendiente, como el resto de lo simulado')

    # ---- 5. Un codigo plus pegado coloca el punto ----
    r = pg.evaluate("""() => {
      guarda('coord_pegar','76F2CVM8+22'); colocaPorTexto();
      return {lat: val('lat'), lon: val('lon'), alcaldia: val('alcaldia')};
    }""")
    afirma(r['lat'] != '' and r['lon'] != '', 'un código plus coloca el punto en el mapa')
    afirma(r['alcaldia'] != '', 'y el cruce con las capas responde: %s' % r['alcaldia'])

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
