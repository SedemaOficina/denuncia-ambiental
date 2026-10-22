# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración: la evidencia del expediente, fácil
   de revisar (DEC-253, DEC-254).

   1. Cada archivo es una miniatura con su nombre —«Foto 1», «Video 1»,
      «PDF 1», «Word 1», «Excel 1»— y, en las fotos, cuándo se tomó, en
      palabras; en lo demás, el nombre del archivo. Toda extensión que admite
      el formulario tiene su clase, y los datos de prueba traen de todas.
   2. Un clic abre el visor: el archivo en grande, su nombre y su tipo, y en
      las fotos cuándo y dónde se tomaron —dónde, contra el lugar de la
      denuncia, en metros—. Nada de datos del sistema: ni peso, ni
      dimensiones, ni huella, ni coordenadas.
   3. «Anterior» y «Siguiente» recorren los archivos; Escape o «Cerrar»
      cierran y el foco vuelve a la miniatura.
   4. Directivos ve también dónde se tomó la foto (DEC-256).
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
    pares: Object.fromEntries([...v.querySelectorAll('.ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent])),
    texto: v.textContent, botones: [...v.querySelectorAll('.acciones-visor button')].map(b => b.textContent)}; }"""
# Lo que es dato del sistema y no se muestra a quien usa la plataforma.
DEL_SISTEMA = re.compile(r'SHA|huella|Huella|MB\b|píxeles|Coordenadas|Peso')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(500)
    clases = pg.evaluate("() => CLASES_EVIDENCIA.map(c => ({nom: c.nom, tipo: c.tipo, exts: c.exts}))")
    todas = [e for c in clases for e in c['exts']]
    afirma(sorted(todas) == sorted(exts) and len(set(todas)) == len(todas), 'cada extensión que admite el formulario tiene una sola clase: %s' % [(c['nom'], c['exts']) for c in clases])
    meses = pg.evaluate("() => MESES")
    ids = pg.evaluate("() => DENUNCIAS.map(idDe)")
    vistas_clase = set()

    def clase(a): return next(c for c in clases if a['name'].rsplit('.', 1)[1].lower() in c['exts'])
    def tipo(a):
        c = clase(a)
        return c['tipo'] + (' (%s)' % a['name'].rsplit('.', 1)[1].upper() if len(c['exts']) > 1 else '')
    def abre(perfil, ident):
        pg.evaluate("([p, i]) => { const v = document.getElementById('visor'); if (v && v.open) v.close(); cambiaPerfil(p); location.hash = '#/expediente/' + i; }", [perfil, ident])
        pg.wait_for_timeout(60)

    malos = {'galeria': [], 'visor': [], 'sistema': []}
    for x, ident in zip(datos, ids):
        abre('coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident)
        tarjetas = pg.evaluate("() => [...document.querySelectorAll('.galeria .archivo-ev')].map(b => [b.querySelector('.archivo-tit').textContent, b.querySelector('.dato-sec').textContent])")
        cuenta, esperado = {}, []
        for a in x['archivos']:
            c = clase(a)['nom']
            cuenta[c] = cuenta.get(c, 0) + 1; vistas_clase.add(c)
            segundo = (('Tomada el %d %s %s a las %s h, según la cámara' % (int(a['fecha_captura'][8:10]), meses[int(a['fecha_captura'][5:7]) - 1], a['fecha_captura'][:4], a['fecha_captura'][11:16]))
                       if 'fecha_captura' in a else 'La foto no dice cuándo se tomó') if c == 'Foto' else a['name']
            esperado.append(['%s %d' % (c, cuenta[c]), segundo])
        ev = pg.evaluate("() => [...document.querySelectorAll('.seccion-exp')].find(s => s.querySelector('h3').textContent === '3. Evidencia').innerText")
        if tarjetas != esperado or (not x['archivos'] and 'Sin archivos adjuntos' not in ev) or DEL_SISTEMA.search(ev):
            malos['galeria'].append((ident, tarjetas, esperado))
        for k, a in enumerate(x['archivos']):
            pg.evaluate("(k) => document.querySelectorAll('.galeria .archivo-ev')[k].click()", k); pg.wait_for_timeout(30)
            v = pg.evaluate(VISOR)
            pares = ({'Cuándo': esperado[k][1], 'Dónde': donde(a, x)} if clase(a)['nom'] == 'Foto' else {})
            pares.update({'Archivo': a['name'], 'Tipo': tipo(a)})
            if not v['abierto'] or v['tit'] != esperado[k][0] or not v['foco'] or v['pares'] != pares:
                malos['visor'].append((ident, k, v['pares'], pares))
            if DEL_SISTEMA.search(v['texto']) or a.get('sha256_original', '§') in v['texto'] or str(a.get('lat_captura', '§')) in v['texto']:
                malos['sistema'].append((ident, k))
    afirma(vistas_clase == {c['nom'] for c in clases}, 'los datos de prueba traen de cada clase: fotos, video, PDF, Word y Excel: %s' % sorted(vistas_clase))
    afirma(not malos['galeria'], 'cada archivo es una miniatura con su nombre y, en las fotos, cuándo se tomó, en palabras; en lo demás, el nombre del archivo: %s' % malos['galeria'][:1])
    afirma(not malos['visor'], 'un clic abre el visor con el foco en su título, el nombre y el tipo del archivo, y en las fotos cuándo y dónde, contra el lugar de la denuncia: %s' % malos['visor'][:2])
    afirma(not malos['sistema'], 'ni la galería ni el visor muestran datos del sistema: peso, dimensiones, huella o coordenadas: %s' % malos['sistema'][:2])
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
    abre('directivos', ident)
    pg.click('.galeria li:nth-child(1) .archivo-ev'); pg.wait_for_timeout(50)
    v = pg.evaluate(VISOR)
    afirma(v['pares']['Dónde'] == donde(x['archivos'][0], x), 'directivos ve dónde se tomó la foto, contra el lugar de la denuncia (DEC-256)')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 5. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri()); tel.wait_for_timeout(400)
    x, ident = next((x, i) for x, i in zip(datos, ids) if len(x['archivos']) >= 3)
    tel.evaluate("([p, i]) => { cambiaPerfil(p); location.hash = '#/expediente/' + i; }", ['coordinacion_' + (x['tramite']['area_actual'] or 'DGIVA').lower(), ident]); tel.wait_for_timeout(150)
    tel.click('.galeria li:nth-child(1) .archivo-ev'); tel.wait_for_timeout(80)
    r = tel.evaluate("() => { const v = document.getElementById('visor'); return [document.documentElement.scrollWidth - innerWidth, v.scrollWidth - v.clientWidth, v.getBoundingClientRect().right <= innerWidth]; }")
    afirma(r[0] <= 0 and r[1] <= 0 and r[2], 'a 360 px, con el visor abierto, nada se desplaza a lo ancho: %s' % r)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
