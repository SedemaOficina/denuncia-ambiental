# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque D, primera parte: Inicio
   (DEC-245).

   Lo que se espera se calcula aquí, aparte de la maqueta, con las reglas del
   bosquejo (documento 22, §3.1 y §4).

   1. Cada perfil ve sus listas de trabajo: atención y coordinación, cinco
      —atención con «Asignadas», coordinación con «Por asignar»—; captura,
      lo capturado y lo que parece duplicado; administración, el aviso de que
      su inicio llega con el bloque F.
   2. Cada lista tiene las denuncias que dice su regla. Atención ve lo nuevo
      de su área y, en lo demás, lo que tiene a su cargo la persona que simula.
   3. Hay algo en «Por vencer» y en «Vencidas» con los datos de prueba.
   4. Cada denuncia de las listas abre su expediente.
   5. En teléfono no hay desplazamiento horizontal."""
import datetime, json, math, os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
# Lo único que la maqueta pide a internet son las tipografías; si no cargan, no
# es un error de la maqueta. Chrome no pone la dirección en el texto del aviso:
# se lee de su ubicación.
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

datos = json.loads(DATOS.read_text(encoding='utf-8'))
# Plazo que corre en cada estado (documento 22, §4; DEC-84); «suelo»: 93 en la
# DGIVA, 90 en la DGCORENADR.
PLAZOS = {'recibida': 3, 'por_ubicar': 3, 'turnada': 10, 'en_analisis': 10, 'returnada': 5,
          'admitida': 'suelo', 'visita_programada': 'suelo', 'visita_practicada': 'suelo', 'en_procedimiento': 'suelo'}
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}
LISTAS = {'atencion': ['Nuevas', 'Asignadas', 'Por vencer', 'Vencidas', 'Por notificar'],
          'coordinacion': ['Nuevas', 'Por asignar', 'Por vencer', 'Vencidas', 'Por notificar'],
          'captura': ['Capturadas', 'Con posible duplicado']}

def recepcion(x): return x['datos'].get('fecha_recepcion_original') or x['datos']['fecha_acuse']
def dia(iso): return datetime.date(int(iso[:4]), int(iso[5:7]), int(iso[8:10]))
def habiles(desde, hasta):
    d, n = dia(desde), 0
    while d < dia(hasta):
        d += datetime.timedelta(days=1)
        n += d.weekday() < 5
    return n
def metros(a, b):
    r = math.pi / 180
    la1, la2 = float(a['lat']) * r, float(b['lat']) * r
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((float(b['lon']) - float(a['lon'])) * r / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
def abierta(x): return x['tramite']['estado'] not in CIERRAN

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/inicio'); pg.wait_for_timeout(600)
    cat = pg.evaluate("() => ({hoy: HOY, aviso: AVISO_VENCE, umbral: UMBRAL_DUPLICADO, personal: PERSONAL, perfiles: PERFILES})")

    def plazo(x):
        e = x['tramite']['estado']
        if e not in PLAZOS: return None
        total = {'DGIVA': 93, 'DGCORENADR': 90}[x['tramite']['area_actual']] if PLAZOS[e] == 'suelo' else PLAZOS[e]
        return total, habiles(recepcion(x), cat['hoy'])
    def parecida(x):
        u = cat['umbral']
        return abierta(x) and x['datos'].get('lat') and any(
            o is not x and abierta(o) and o['datos'].get('lat') and o['datos']['materia'] == x['datos']['materia']
            and metros(x['datos'], o['datos']) <= u['metros'] and abs((dia(recepcion(x)) - dia(recepcion(o))).days) <= u['dias'] for o in datos)
    REGLA = {
      'Nuevas':        lambda x: x['tramite']['estado'] in ('recibida', 'por_ubicar'),
      'Asignadas':     abierta,
      'Por asignar':   lambda x: x['tramite']['estado'] == 'turnada' and not x['tramite']['asignado'],
      'Por vencer':    lambda x: plazo(x) is not None and plazo(x)[1] <= plazo(x)[0] and plazo(x)[0] - plazo(x)[1] <= cat['aviso'],
      'Vencidas':      lambda x: plazo(x) is not None and plazo(x)[1] > plazo(x)[0],
      'Por notificar': lambda x: x['tramite']['estado'] == 'resuelta',
      'Capturadas':    lambda x: True,
      'Con posible duplicado': parecida}

    malos, total = [], {'Por vencer': 0, 'Vencidas': 0}
    for p in cat['perfiles']:
        if 'inicio' not in p['pantallas']: continue
        pg.evaluate("(id) => { cambiaPerfil(id); location.hash = '#/inicio'; }", p['id']); pg.wait_for_timeout(120)
        vistas = pg.evaluate("""() => [...document.querySelectorAll('.lista-inicio')].map(s => ({
            nom: s.querySelector('h3').textContent.replace(/^\\d+\\s*/, ''), cuenta: +s.querySelector('.cuenta-inicio').textContent,
            folios: [...s.querySelectorAll('li a')].map(a => a.textContent)}))""")
        if p['rol'] == 'administracion':
            texto = pg.inner_text('#pantalla')
            afirma(not vistas and 'llega con el bloque F' in texto, 'administración no tiene listas: su inicio llega con el bloque F')
            continue
        afirma([v['nom'] for v in vistas] == LISTAS[p['rol']], '%s ve sus listas: %s' % (p['id'], [v['nom'] for v in vistas]))
        persona = cat['personal'][p['area']][0] if p['rol'] == 'atencion' else ''
        suyas = [x for x in datos if (not p.get('area') or x['tramite']['area_actual'] in (p['area'], ''))
                 and (not p.get('soloCapturadas') or x['canal'] != 'en_linea')]
        for v in vistas:
            esperado = {x['datos']['folio'] for x in suyas if REGLA[v['nom']](x) and (v['nom'] == 'Nuevas' or not persona or x['tramite']['asignado'] == persona)}
            if set(v['folios']) != esperado or v['cuenta'] != len(esperado): malos.append((p['id'], v['nom'], sorted(v['folios']), sorted(esperado)))
            if v['nom'] in total: total[v['nom']] += v['cuenta']
    afirma(not malos, 'cada lista tiene lo que dice su regla, y atención sólo lo suyo fuera de «Nuevas»: %s' % malos[:1])
    afirma(total['Por vencer'] > 0 and total['Vencidas'] > 0, 'con los datos de prueba hay denuncias por vencer y vencidas: %s' % total)

    pg.evaluate("() => { cambiaPerfil('coordinacion_dgiva'); location.hash = '#/inicio'; }"); pg.wait_for_timeout(120)
    folio = pg.locator('.lista-inicio li a').first.text_content()
    pg.click('.lista-inicio li a >> nth=0'); pg.wait_for_timeout(150)
    afirma(folio in pg.locator('#pantalla h2').text_content() and pg.evaluate("() => location.hash").startswith('#/expediente/'),
           'una denuncia de la lista abre su expediente')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/inicio'); tel.wait_for_timeout(500)
    anchos = []
    for pid in ('atencion_dgiva', 'coordinacion_dgiva', 'captura'):
        tel.evaluate("(id) => { cambiaPerfil(id); location.hash = '#/inicio'; }", pid); tel.wait_for_timeout(100)
        anchos.append(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth"))
    afirma(max(anchos) <= 0, 'a 360 px no hay desplazamiento horizontal: %s' % anchos)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
