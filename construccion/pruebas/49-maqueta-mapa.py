# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque D, tercera parte: el mapa
   operativo y el mapa del expediente (DEC-247, DEC-251).

   1. Las capas son las del mapa vectorial del formulario, sin copiarlas a
      mano: contorno, alcaldías y suelo de conservación completos; de las
      zonas protegidas, sólo las que tocan las denuncias de prueba.
   2. Cada denuncia con punto está en el mapa, en sus coordenadas, y abre su
      expediente; las que no tienen punto se listan aparte. Abiertas y
      cerradas se distinguen también por la forma, no sólo por el color.
   3. Los filtros —año, mes, materia, estado, área— y el acercamiento a una
      alcaldía funcionan; junto al mapa van las mismas cuentas sin mapa.
   4. El expediente lleva su mapa: la denuncia resaltada, su zona protegida
      si cae en una, y las cercanas; sin punto, no hay mapa.
   5. Nada sale a internet salvo las tipografías; en teléfono no hay
      desplazamiento horizontal."""
import json, math, os, pathlib, re, sys
from collections import Counter
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
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}

datos = json.loads(DATOS.read_text(encoding='utf-8'))
p = PROTO.read_text(encoding='utf-8')
def capa(n): return json.loads(re.search(r'(?m)^var %s=(.*);$' % n, p).group(1))
zonas_usadas = {x['datos'].get('capa_nombre') for x in datos} - {None}
ESPERADO = {'bbox': capa('CDMX_BBOX'), 'borde': capa('CDMX_BORDE'),
            'alcaldias': [{'nombre': f['p']['nombre'], 'g': f['g']} for f in capa('CAPAS_ALCALDIAS')],
            'suelo': [f['g'] for f in capa('CAPAS_SUELO')],
            'zonas': [{'nombre': f['p']['nombre'], 'g': f['g']} for f in capa('CAPAS_GEOM') if f['p']['nombre'] in zonas_usadas]}
def id_de(x): return x['datos']['folio'].replace('SEDEMA/DEN/', '').replace('/', '-')
def metros(a, b):
    r = math.pi / 180
    la1, la2 = float(a['lat']) * r, float(b['lat']) * r
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((float(b['lon']) - float(a['lon'])) * r / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))

PUNTOS = """() => [...document.querySelectorAll(SEL + ' .m-liga')].map(a => { const c = a.querySelector('circle');
  return {href: a.getAttribute('href'), cx: +c.getAttribute('cx'), cy: +c.getAttribute('cy'), clase: c.getAttribute('class'), titulo: c.querySelector('title').textContent}; })"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err, red = [], []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.on('request', lambda r: red.append(r.url) if r.url.startswith('http') and not r.url.startswith(TIPOGRAFIAS) else None)
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(500)

    # ---- 1. Capas ----
    capas = pg.evaluate("() => CAPAS")
    afirma(capas == ESPERADO and len(capas['alcaldias']) == 16 and capas['zonas'] and len(capas['zonas']) < len(capa('CAPAS_GEOM')),
           'las capas son las del formulario: 16 alcaldías, contorno, suelo de conservación y %d zonas protegidas con denuncias' % len(capas['zonas']))
    K = math.cos((capas['bbox'][1] + capas['bbox'][3]) / 2 * math.pi / 180)

    # ---- 2. Mapa operativo ----
    pg.evaluate("() => { cambiaPerfil('consulta'); location.hash = '#/mapa'; }"); pg.wait_for_timeout(250)
    pts = pg.evaluate(PUNTOS.replace('SEL', "'#mapa-cuerpo'"))
    con_punto = [x for x in datos if x['datos'].get('lat')]
    por_href = {q['href']: q for q in pts}
    malos = [x['datos']['folio'] for x in con_punto
             if '#/expediente/' + id_de(x) not in por_href
             or abs(por_href['#/expediente/' + id_de(x)]['cx'] - float(x['datos']['lon']) * K) > 1e-5
             or abs(por_href['#/expediente/' + id_de(x)]['cy'] + float(x['datos']['lat'])) > 1e-5
             or x['datos']['folio'] not in por_href['#/expediente/' + id_de(x)]['titulo']
             or ('m-cerrada' in por_href['#/expediente/' + id_de(x)]['clase']) != (x['tramite']['estado'] in CIERRAN)]
    afirma(len(pts) == len(con_punto) and not malos, 'cada denuncia con punto está en el mapa, en sus coordenadas, con su folio y abierta o cerrada: %s' % malos[:3])
    sin = [x['datos']['folio'] for x in datos if not x['datos'].get('lat')]
    texto = pg.inner_text('#mapa-cuerpo')
    afirma(sin and all(f in texto for f in sin) and ('%d sin punto' % len(sin)) in pg.inner_text('#conteo-mapa'), 'las que no tienen punto se listan aparte')
    afirma(pg.evaluate("() => getComputedStyle(document.querySelector('.m-cerrada')).fill !== getComputedStyle(document.querySelector('.m-punto:not(.m-cerrada)')).fill"),
           'la cerrada es un círculo hueco: se distingue por la forma, no sólo por el color')
    barras = pg.evaluate("""() => { const s = [...document.querySelectorAll('.mapa-lado .indicador')].find(s => s.querySelector('h4').textContent === 'Por alcaldía');
      return Object.fromEntries([...s.querySelectorAll('.barras tr')].map(tr => [tr.querySelector('th').textContent, +tr.querySelector('.num').textContent])); }""")
    afirma(barras == dict(Counter(x['datos'].get('alcaldia') or x['datos'].get('alcaldia_dir') or 'Sin alcaldía' for x in datos)),
           'junto al mapa, la cuenta por alcaldía es la de los datos: el mismo contenido sin mapa')

    # ---- 3. Filtros y acercamiento ----
    pg.select_option('#f-materia', 'impacto'); pg.wait_for_timeout(150)
    n = len(pg.evaluate(PUNTOS.replace('SEL', "'#mapa-cuerpo'")))
    afirma(n == sum(x['datos']['materia'] == 'impacto' and bool(x['datos'].get('lat')) for x in datos), 'el filtro de materia deja sólo sus puntos: %d' % n)
    pg.select_option('#f-materia', '*'); pg.select_option('#f-anio', '2025'); pg.wait_for_timeout(150)
    n = len(pg.evaluate(PUNTOS.replace('SEL', "'#mapa-cuerpo'")))
    def recepcion(x): return x['datos'].get('fecha_recepcion_original') or x['datos']['fecha_acuse']
    afirma(n and n == sum(recepcion(x)[:4] == '2025' and bool(x['datos'].get('lat')) for x in datos), 'el filtro de año deja sólo los puntos de ese año: %d' % n)
    pg.select_option('#f-anio', '*'); pg.select_option('#f-zona', 'Cuauhtémoc'); pg.wait_for_timeout(150)
    vb = [float(v) for v in pg.get_attribute('#mapa-cuerpo svg', 'viewBox').split()]
    alc = next(a for a in capas['alcaldias'] if a['nombre'] == 'Cuauhtémoc')
    xs = [pt[0] * K for pol in ([alc['g']['coordinates']] if alc['g']['type'] == 'Polygon' else alc['g']['coordinates']) for pt in pol[0]]
    afirma(vb[0] <= min(xs) and vb[0] + vb[2] >= max(xs) and vb[2] < 0.2 * (capas['bbox'][2] - capas['bbox'][0]) * K * 3,
           'acercar a una alcaldía encuadra esa alcaldía: %s' % [round(v, 4) for v in vb])

    # ---- 4. Mapa del expediente ----
    malos = []
    for x in datos:
        pg.evaluate("([i, p]) => { cambiaPerfil(p); location.hash = '#/expediente/' + i; }", [id_de(x), 'coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower()]); pg.wait_for_timeout(40)
        hay = pg.locator('.mapa-exp svg').count()
        if not x['datos'].get('lat'):
            if hay or 'Sin punto no hay mapa' not in pg.inner_text('#pantalla'): malos.append(x['datos']['folio'])
            continue
        q = pg.evaluate(PUNTOS.replace('SEL', "'.mapa-exp'"))
        actual = [c for c in q if 'm-actual' in c['clase']]
        cerca = sum(1 for o in datos if o is not x and o['datos'].get('lat') and metros(x['datos'], o['datos']) <= 500)
        sel = pg.evaluate("() => [...document.querySelectorAll('.mapa-exp .m-zona-sel title')].map(t => t.textContent)")
        zona_esperada = [x['datos']['capa_nombre']] if x['datos'].get('capa_nombre') in zonas_usadas else []
        # La actual va encima de las que comparten su punto: es la última de ellas.
        mismos = [c for c in q if actual and c['cx'] == actual[0]['cx'] and c['cy'] == actual[0]['cy']]
        if not hay or len(actual) != 1 or actual[0]['href'] != '#/expediente/' + id_de(x) or len(q) != 1 + cerca \
           or sel != zona_esperada or mismos[-1] is not actual[0]:
            malos.append((x['datos']['folio'], len(actual), len(q), cerca, sel))
    afirma(not malos, 'cada expediente con punto lleva su mapa con la denuncia resaltada, sus cercanas y su zona protegida; sin punto no hay mapa: %s' % malos[:2])

    # ---- 5. Red y teclado ----
    pg.evaluate("() => { cambiaPerfil('consulta'); location.hash = '#/mapa'; }"); pg.wait_for_timeout(200)
    pg.focus('#mapa-cuerpo .m-liga >> nth=0'); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    afirma(pg.evaluate("() => location.hash").startswith('#/expediente/'), 'con teclado, un punto del mapa abre su expediente')
    afirma(not red, 'el mapa no pide nada a internet salvo las tipografías: %s' % red[:3])
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/mapa'); tel.wait_for_timeout(500)
    a = [tel.evaluate("() => document.documentElement.scrollWidth - innerWidth")]
    tel.evaluate("() => { location.hash = '#/expediente/2026-000101-9'; }"); tel.wait_for_timeout(200)
    a.append(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth"))
    afirma(max(a) <= 0, 'a 360 px no hay desplazamiento horizontal, ni en el mapa ni en el expediente: %s' % a)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
