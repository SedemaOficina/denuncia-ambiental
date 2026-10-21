# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque D, segunda parte: el tablero
   (DEC-246).

   Cada indicador se calcula aquí, aparte de la maqueta, sobre el archivo de
   datos y con las reglas del bosquejo (documento 22, §4 y §5).

   1. Los cinco grupos del bosquejo, con sus nombres y en su orden.
   2. Las cuatro cifras de arriba: recibidas, en trámite, cerradas y con el
      plazo vencido.
   3. Los filtros —mes, área, canal, materia, alcaldía— se combinan y todo el
      tablero responde a ellos.
   4. Operación: por mes, por canal y carga por persona, que sólo ve
      coordinación.
   5. Plazos: turnado en 3 días hábiles, primera valoración en 10,
      procedimiento en 93 o 90.
   6. Resultado: visita practicada por materia; remitidas y returnadas por
      separado; sin materia y acumuladas.
   7. Territorio: por alcaldía, por tipo de zona, celdas con denuncia
      reiterada y proporción en conservación o Área Natural Protegida.
   8. Canal: anónimas, notificación por correo, punto y evidencia; género y
      edad sólo en agregado, sin mostrar una cifra menor que el mínimo.
   9. En teléfono, sin desplazamiento horizontal y con los filtros plegados."""
import datetime, json, os, pathlib, re, sys
from collections import Counter
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
DOC22 = RAIZ / 'documentacion' / '22-bosquejo-modulo-de-administracion.md'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
# Lo único que la maqueta pide a internet son las tipografías; si no cargan, no
# es un error de la maqueta. Chrome no pone la dirección en el texto del aviso:
# se lee de su ubicación.
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

datos = json.loads(DATOS.read_text(encoding='utf-8'))
doc = DOC22.read_text(encoding='utf-8')
sec5 = doc[doc.index('## 5. Tablero'):doc.index('## 6.')]
GRUPOS = re.findall(r'(?m)^\| \*\*([^*]+)\*\* \|', sec5)
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}
PLAZOS = {'recibida': 3, 'por_ubicar': 3, 'turnada': 10, 'en_analisis': 10, 'returnada': 5,
          'admitida': 'suelo', 'visita_programada': 'suelo', 'visita_practicada': 'suelo', 'en_procedimiento': 'suelo'}
VALORACION = ['admitida', 'returnada', 'remitida', 'recomendacion', 'sin_materia', 'acumulada']

def recepcion(x): return x['datos'].get('fecha_recepcion_original') or x['datos']['fecha_acuse']
def dia(iso): return datetime.date(int(iso[:4]), int(iso[5:7]), int(iso[8:10]))
def habiles(desde, hasta):
    d, n = dia(desde), 0
    while d < dia(hasta):
        d += datetime.timedelta(days=1)
        n += d.weekday() < 5
    return n
def abierta(x): return x['tramite']['estado'] not in CIERRAN
def fecha(x, e): return next((h['fecha'] for h in x['tramite']['historial'] if h['estado'] == e), '')

LEE = """() => ({
  conteo: document.getElementById('conteo-tablero').textContent,
  grupos: [...document.querySelectorAll('#indicadores > h3')].map(h => h.textContent),
  cifras: Object.fromEntries([...document.querySelectorAll('.cifras-tablero > div')].map(x => [x.querySelector('dt').textContent, +x.querySelector('dd').textContent])),
  ind: Object.fromEntries([...document.querySelectorAll('.indicador')].map(s => [s.querySelector('h4').textContent, {
    texto: s.innerText,
    barras: [...s.querySelectorAll('.barras tr')].map(tr => [tr.querySelector('th').textContent, tr.querySelector('.num').textContent, !!tr.querySelector('.barra')]),
    pares: Object.fromEntries([...s.querySelectorAll('.ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent]))}]))
})"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(500)
    cat = pg.evaluate("""() => ({hoy: HOY, minimo: MINIMO_AGREGADO, canales: Object.fromEntries(CANALES.map(c => [c.id, c.nom])),
      materias: Object.fromEntries(MATERIAS.map(m => [m.id, m.nom])), est: OPCIONES_ESTADISTICA})""")
    def vencida(x):
        e = x['tramite']['estado']
        if e not in PLAZOS or not abierta(x): return False
        total = {'DGIVA': 93, 'DGCORENADR': 90}[x['tramite']['area_actual']] if PLAZOS[e] == 'suelo' else PLAZOS[e]
        return habiles(recepcion(x), cat['hoy']) > total
    def abre(perfil):
        pg.evaluate("(p) => { cambiaPerfil(p); location.hash = '#/tablero'; }", perfil); pg.wait_for_timeout(150)
        return pg.evaluate(LEE)

    t = abre('consulta')
    afirma(len(GRUPOS) == 5 and t['grupos'] == GRUPOS, 'los cinco grupos del bosquejo, en su orden: %s' % t['grupos'])
    esperado = {'Recibidas': 40, 'En trámite': sum(map(abierta, datos)), 'Cerradas': 40 - sum(map(abierta, datos)),
                'Con el plazo vencido': sum(map(vencida, datos))}
    afirma(t['cifras'] == esperado and esperado['Con el plazo vencido'] > 0, 'las cuatro cifras de arriba: %s' % t['cifras'])
    i = t['ind']
    canal = Counter(cat['canales'][x['canal']] for x in datos)
    afirma({b[0]: int(b[1]) for b in i['Recibidas por canal']['barras']} == dict(canal), 'recibidas por canal')
    meses = re.findall(r'(\w{3} \d{4})\t(\d+)\t(\d+)\t(\d+)', i['Recibidas, en trámite y cerradas, por mes']['texto'])
    por_mes = Counter(recepcion(x)[:7] for x in datos)
    afirma(sum(int(m[1]) for m in meses) == 40 and len(meses) == len(por_mes) and all(int(m[1]) == int(m[2]) + int(m[3]) for m in meses),
           'por mes: cada mes suma en trámite y cerradas, y el total es 40: %s' % meses)
    afirma('Sólo la ve coordinación' in i['Carga por persona asignada']['texto'] and not i['Carga por persona asignada']['barras'],
           'consulta no ve la carga por persona')

    # ---- 5. Plazos ----
    turnadas = [x for x in datos if fecha(x, 'turnada')]
    k = sum(habiles(recepcion(x), fecha(x, 'turnada')) <= 3 for x in turnadas)
    afirma(i['Turnado en 3 días hábiles']['pares']['Dentro del plazo'].startswith('%d de %d ' % (k, len(turnadas))), 'turnado en tres días hábiles: %d de %d' % (k, len(turnadas)))
    valoradas = [x for x in datos if any(h['estado'] in VALORACION for h in x['tramite']['historial'])]
    k = sum(habiles(recepcion(x), next(h['fecha'] for h in x['tramite']['historial'] if h['estado'] in VALORACION)) <= 10 for x in valoradas)
    afirma(i['Primera valoración en 10 días hábiles']['pares']['Dentro del plazo'].startswith('%d de %d ' % (k, len(valoradas))), 'primera valoración en diez: %d de %d' % (k, len(valoradas)))
    proc = [x for x in datos if PLAZOS.get(x['tramite']['estado']) == 'suelo']
    afirma(i['Procedimiento en 93 o 90 días hábiles']['pares'] == {'Dentro del plazo': str(sum(not vencida(x) for x in proc)), 'Fuera del plazo': str(sum(map(vencida, proc)))},
           'procedimiento en 93 o 90 días')

    # ---- 6. Resultado ----
    vis = i['Con visita practicada, por materia']['pares']
    afirma(all(vis[cat['materias'][m]] == '%d de %d' % (sum(bool(fecha(x, 'visita_practicada')) for x in datos if x['datos']['materia'] == m), n)
               for m, n in Counter(x['datos']['materia'] for x in datos).items()), 'visita practicada, por materia')
    afirma(i['Remitidas a otra autoridad y returnadas, por separado']['pares'] == {'Remitidas': str(sum(bool(fecha(x, 'remitida')) for x in datos)),
           'Returnadas': str(sum(bool(fecha(x, 'returnada')) for x in datos))}, 'remitidas y returnadas, por separado')
    afirma(i['Concluidas sin materia y acumuladas']['pares'] == {'Sin materia': str(sum(x['tramite']['estado'] == 'sin_materia' for x in datos)),
           'Acumuladas': str(sum(x['tramite']['estado'] == 'acumulada' for x in datos))}, 'sin materia y acumuladas')
    distintas = sum(x['tramite']['materia_confirmada'] != x['datos']['materia'] for x in datos)
    afirma(('%d de 40 distintas' % distintas) in i['Materia declarada frente a la confirmada']['texto'] and distintas > 0, 'materia declarada frente a la confirmada')

    # ---- 7. Territorio ----
    alc = Counter(x['datos'].get('alcaldia') or x['datos'].get('alcaldia_dir') or 'Sin alcaldía' for x in datos)
    afirma({b[0]: int(b[1]) for b in i['Por alcaldía']['barras']} == dict(alc), 'por alcaldía')
    zona = Counter(x['datos'].get('capa_clase') or 'Sin ubicar' for x in datos)
    afirma({b[0]: int(b[1]) for b in i['Por tipo de zona']['barras']} == dict(zona), 'por tipo de zona')
    celdas = {c: n for c, n in Counter(x['datos']['uga'] for x in datos if x['datos'].get('lat')).items() if n > 1}
    afirma({b[0]: int(b[1]) for b in i['Celdas UGA con denuncia reiterada']['barras']} == celdas and celdas, 'celdas UGA con denuncia reiterada: %d' % len(celdas))
    cons = sum(x['datos'].get('capa_clase') in ('Suelo de conservación', 'Área Natural Protegida') for x in datos)
    afirma(i['En suelo de conservación o Área Natural Protegida']['pares']['Proporción'].startswith('%d de 40' % cons) and '4.3 %' in i['En suelo de conservación o Área Natural Protegida']['texto'],
           'proporción en conservación o ANP, con la línea base de 4.3 %')

    # ---- 8. Canal ----
    anon = [x for x in datos if x['datos']['identificacion'] == 'anonima']
    correos = [x for x in anon if x['tramite']['notificacion'] and x['tramite']['notificacion']['medio'] == 'correo']
    afirma(i['Anónimas y con datos']['pares'] == {'Anónimas': str(len(anon)), 'Con datos': str(40 - len(anon))}, 'anónimas y con datos')
    afirma(i['Notificación por correo, en anónimas']['pares']['Rebotadas'] == str(sum(x['tramite']['notificacion']['resultado'] == 'rebotado' for x in correos))
           and i['Notificación por correo, en anónimas']['pares']['Enviadas'] == str(len(correos)), 'notificación por correo en anónimas')
    malos = []
    for k_, titulo in (('sexo_genero', 'Género'), ('edad_rango', 'Rango de edad')):
        cuenta = Counter(x['datos'].get(k_) for x in datos)
        for etq, num, barra in i[titulo]['barras']:
            v = next((o['v'] for o in cat['est'][k_] if o['t'] == etq), None)
            n = cuenta[v]
            esperado_ = ('menos de %d' % cat['minimo']) if 0 < n < cat['minimo'] else str(n)
            if num != esperado_ or barra != (n >= cat['minimo']): malos.append((titulo, etq, num, n))
    ocultas = sum(1 for k_ in ('Género', 'Rango de edad') for b in i[k_]['barras'] if b[1].startswith('menos de'))
    afirma(not malos and ocultas > 0, 'género y edad sólo en agregado, y una cifra menor que %d no se muestra: %s' % (cat['minimo'], malos[:2]))

    # ---- 3. Filtros ----
    malos = []
    for mes in sorted(por_mes):
        pg.select_option('#f-periodo', mes); pg.wait_for_timeout(80)
        if pg.evaluate(LEE)['cifras']['Recibidas'] != por_mes[mes]: malos.append(mes)
    pg.select_option('#f-canal', 'telefono'); pg.wait_for_timeout(80)
    combinado = pg.evaluate(LEE)['cifras']['Recibidas']
    afirma(not malos and combinado == sum(x['canal'] == 'telefono' and recepcion(x)[:7] == sorted(por_mes)[-1] for x in datos),
           'los filtros de mes y canal se combinan y el tablero responde: %s' % malos)

    # ---- 4. Coordinación ----
    t = abre('coordinacion_dgiva')
    suyas = [x for x in datos if x['tramite']['area_actual'] in ('DGIVA', '')]
    carga = Counter(x['tramite']['asignado'] for x in suyas if abierta(x) and x['tramite']['asignado'])
    afirma(t['cifras']['Recibidas'] == len(suyas) and {b[0]: int(b[1]) for b in t['ind']['Carga por persona asignada']['barras']} == dict(carga),
           'coordinación ve su área y la carga por persona: %s' % dict(carga))
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/bandeja'); tel.wait_for_timeout(400)
    tel.evaluate("() => { cambiaPerfil('consulta'); location.hash = '#/tablero'; }"); tel.wait_for_timeout(200)
    r = tel.evaluate("() => [document.documentElement.scrollWidth - innerWidth, document.querySelector('.plegable').open]")
    afirma(r[0] <= 0 and r[1] is False, 'a 360 px no hay desplazamiento horizontal y los filtros empiezan plegados: %s' % r)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
