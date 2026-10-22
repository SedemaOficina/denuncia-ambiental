# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración: la evidencia del expediente, fácil
   de revisar (DEC-253).

   1. Cada archivo es una miniatura con su nombre —«Foto 1», «Video 1»,
      «Documento 1»— y, en las fotos, cuándo se tomó, en palabras. Toda
      extensión que admite el formulario tiene su clase.
   2. Un clic abre el visor: el archivo en grande, cuándo y dónde se tomó
      —dónde, contra el lugar de la denuncia, en metros—, y lo técnico
      plegado: nombre, peso, huella y coordenadas.
   3. «Anterior» y «Siguiente» recorren los archivos; Escape o «Cerrar»
      cierran y el foco vuelve a la miniatura.
   4. Quien no ve datos personales no ve dónde se tomó la foto ni sus
      coordenadas.
   5. En teléfono, con el visor abierto, no hay desplazamiento horizontal; sin
      errores en consola."""
import json, math, os, pathlib, re, sys
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
exts = re.findall(r"'(\w+)'", re.search(r"exts:\s*\[([^\]]*)\]", PROTO.read_text(encoding='utf-8')).group(1))

def metros(a, b):
    r = math.pi / 180
    la1, la2 = float(a['lat']) * r, float(b['lat']) * r
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((float(b['lon']) - float(a['lon'])) * r / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
def donde(a, x):
    if 'lat_captura' not in a: return 'La foto no dice dónde se tomó.'
    if not x['datos'].get('lat'): return 'La foto trae su lugar, pero la denuncia no tiene punto para compararlo.'
    m = metros({'lat': a['lat_captura'], 'lon': a['lon_captura']}, x['datos'])
    return ('En el lugar de la denuncia: a menos de 50 metros.' if m < 50 else 'A unos %d metros del lugar de la denuncia.' % (round(m / 10) * 10) if m < 1000
            else 'A %.1f km del lugar de la denuncia: conviene revisar si es el mismo sitio.' % (m / 1000))

VISOR = """() => { const v = document.getElementById('visor');
  return {abierto: v.open, tit: v.querySelector('h4').textContent, foco: document.activeElement === v.querySelector('h4'),
    pares: Object.fromEntries([...v.querySelectorAll(':scope > .ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent])),
    tecnico: [...v.querySelectorAll('.detalle-tecnico .ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent]),
    plegado: !v.querySelector('details').open, botones: [...v.querySelectorAll('.acciones-visor button')].map(b => b.textContent)}; }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(500)
    clases = pg.evaluate("() => CLASES_EVIDENCIA.map(c => [c.nom, c.exts])")
    todas = [e for _, es in clases for e in es]
    afirma(sorted(todas) == sorted(exts) and len(set(todas)) == len(todas), 'cada extensión que admite el formulario tiene una sola clase: %s' % clases)
    ids = pg.evaluate("() => DENUNCIAS.map(idDe)")
    vistas_clase = set()

    def abre(perfil, ident):
        pg.evaluate("([p, i]) => { const v = document.getElementById('visor'); if (v && v.open) v.close(); cambiaPerfil(p); location.hash = '#/expediente/' + i; }", [perfil, ident])
        pg.wait_for_timeout(60)

    malos = {'galeria': [], 'visor': [], 'tecnico': []}
    for x, ident in zip(datos, ids):
        abre('coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident)
        tarjetas = pg.evaluate("() => [...document.querySelectorAll('.galeria .archivo-ev')].map(b => [b.querySelector('.archivo-tit').textContent, b.querySelector('.dato-sec').textContent])")
        cuenta, esperado = {}, []
        for a in x['archivos']:
            c = next(n for n, es in clases if a['name'].rsplit('.', 1)[1].lower() in es)
            cuenta[c] = cuenta.get(c, 0) + 1; vistas_clase.add(c)
            cuando = (('Tomada el %d %s %s a las %s h, según la cámara' % (int(a['fecha_captura'][8:10]), pg.evaluate("() => MESES")[int(a['fecha_captura'][5:7]) - 1], a['fecha_captura'][:4], a['fecha_captura'][11:16]))
                      if 'fecha_captura' in a else 'La foto no dice cuándo se tomó') if c == 'Foto' else None
            esperado.append(['%s %d' % (c, cuenta[c]), cuando])
        if [[t, d if e[1] else None] for (t, d), e in zip(tarjetas, esperado)] != esperado or (not x['archivos'] and 'Sin archivos adjuntos' not in pg.inner_text('#pantalla')):
            malos['galeria'].append((ident, tarjetas, esperado))
        for k, a in enumerate(x['archivos']):
            pg.evaluate("(k) => document.querySelectorAll('.galeria .archivo-ev')[k].click()", k); pg.wait_for_timeout(30)
            v = pg.evaluate(VISOR)
            foto = esperado[k][1] is not None
            if not v['abierto'] or v['tit'] != esperado[k][0] or not v['foco'] or not v['plegado'] or \
               (foto and v['pares'] != {'Cuándo': esperado[k][1], 'Dónde': donde(a, x)}):
                malos['visor'].append((ident, k, v['pares'], donde(a, x)))
            tec = dict(v['tecnico'])
            if tec.get('Archivo') != a['name'] or (a.get('sha256_original') and tec.get('Huella SHA-256 del original') != a['sha256_original']) \
               or (('lat_captura' in a) != ('Coordenadas de la cámara' in tec)):
                malos['tecnico'].append((ident, k))
    afirma(vistas_clase == {'Foto', 'Video', 'Documento'}, 'los datos de prueba traen fotos, un video y un documento: %s' % sorted(vistas_clase))
    afirma(not malos['galeria'], 'cada archivo es una miniatura con su nombre y, en las fotos, cuándo se tomó, en palabras: %s' % malos['galeria'][:1])
    afirma(not malos['visor'], 'un clic abre el visor con el foco en su título, cuándo y dónde en palabras —dónde, contra el lugar de la denuncia— y lo técnico plegado: %s' % malos['visor'][:2])
    afirma(not malos['tecnico'], 'lo técnico trae nombre, huella y coordenadas de la cámara cuando las hay: %s' % malos['tecnico'][:2])
    lejos = [donde(a, x) for x in datos for a in x['archivos'] if 'lat_captura' in a]
    afirma(any(s.startswith('En el lugar') for s in lejos) and any('conviene revisar' in s for s in lejos),
           'hay fotos tomadas en el lugar de la denuncia y una lejos, con el aviso de revisarla: %s' % sorted(set(lejos)))

    # ---- 3. Recorrer y cerrar ----
    x, ident = next((x, i) for x, i in zip(datos, ids) if len(x['archivos']) >= 3)
    abre('coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident)
    pg.click('.galeria li:nth-child(2) .archivo-ev'); pg.wait_for_timeout(50)
    b = pg.evaluate(VISOR)['botones']
    pg.click('.acciones-visor button:has-text("Siguiente")'); pg.wait_for_timeout(50)
    t3 = pg.evaluate(VISOR)
    pg.click('.acciones-visor button:has-text("Anterior")'); pg.click('.acciones-visor button:has-text("Anterior")'); pg.wait_for_timeout(50)
    t1 = pg.evaluate(VISOR)
    afirma(b == ['Anterior', 'Siguiente', 'Cerrar'] and 'Siguiente' not in t3['botones'] and 'Anterior' not in t1['botones'] and t1['foco'] and t3['foco'],
           'Anterior y Siguiente recorren los archivos y el foco va al título de cada uno: %s' % [b, t3['tit'], t1['tit']])
    pg.keyboard.press('Escape'); pg.wait_for_timeout(50)
    r = pg.evaluate("() => [document.getElementById('visor').open, document.activeElement.classList.contains('archivo-ev'), [...document.querySelectorAll('.archivo-ev')].indexOf(document.activeElement)]")
    afirma(r == [False, True, 1], 'Escape cierra el visor y el foco vuelve a la miniatura desde la que se abrió: %s' % r)
    pg.click('.galeria li:nth-child(1) .archivo-ev'); pg.click('.acciones-visor button:has-text("Cerrar")'); pg.wait_for_timeout(50)
    afirma(pg.evaluate("() => !document.getElementById('visor').open && [...document.querySelectorAll('.archivo-ev')].indexOf(document.activeElement) === 0"),
           '«Cerrar» también cierra y regresa el foco')

    # ---- 4. Sin datos personales ----
    x, ident = next((x, i) for x, i in zip(datos, ids) if any('lat_captura' in a for a in x['archivos']))
    abre('consulta', ident)
    pg.click('.galeria li:nth-child(1) .archivo-ev'); pg.wait_for_timeout(50)
    v = pg.evaluate(VISOR); texto = pg.evaluate("() => document.getElementById('visor').textContent")
    a = x['archivos'][0]
    afirma(v['pares']['Dónde'].startswith('Este perfil no lo ve') and str(a['lat_captura']) not in texto and 'Coordenadas' not in texto,
           'consulta no ve dónde se tomó la foto ni sus coordenadas')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 5. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri()); tel.wait_for_timeout(400)
    x, ident = next((x, i) for x, i in zip(datos, ids) if len(x['archivos']) >= 3)
    tel.evaluate("([p, i]) => { cambiaPerfil(p); location.hash = '#/expediente/' + i; }", ['coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident]); tel.wait_for_timeout(150)
    tel.click('.galeria li:nth-child(1) .archivo-ev'); tel.wait_for_timeout(80)
    tel.click('.visor summary'); tel.wait_for_timeout(50)
    r = tel.evaluate("() => { const v = document.getElementById('visor'); return [document.documentElement.scrollWidth - innerWidth, v.scrollWidth - v.clientWidth, v.getBoundingClientRect().right <= innerWidth]; }")
    afirma(r[0] <= 0 and r[1] <= 0 and r[2], 'a 360 px, con el visor abierto y lo técnico desplegado, nada se desplaza a lo ancho: %s' % r)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
