# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque B: la bandeja (DEC-243).

   Lo que se espera se calcula aquí, aparte, con las reglas del bosquejo
   (documento 22, §3.2 y §4) sobre el archivo de datos; la maqueta tiene que
   dar lo mismo.

   1. Columnas y vistas son las del bosquejo, en su orden; cada vista tiene al
      menos una denuncia de prueba y cuenta lo mismo que la regla, por perfil.
   2. Los estados que cierran el trámite son los finales del ciclo, y la
      pantalla dice que los estados son una propuesta por acordar.
   3. Días hábiles desde la recepción original —en lo capturado, la del
      escrito o la llamada— hasta hoy o hasta el cierre, sin sábados ni
      domingos.
   4. El área y la remisión van en columnas distintas.
   5. Filtros combinables y búsqueda por folio, establecimiento, calle y
      hechos, con o sin acentos; sin resultados lo dice y ofrece quitar
      filtros; el foco se queda en el control.
   6. Orden y páginas de quince.
   7. Vistas y folios cambian la dirección: «Atrás» regresa y la bandeja
      conserva los filtros.
   8. Ningún perfil ve en la bandeja nombre, correo ni teléfono de quien
      denuncia.
   9. En teléfono, fichas con etiqueta, filtros plegados y sin desplazamiento
      horizontal."""
import datetime, json, math, os, pathlib, re, sys, unicodedata
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
tabla = doc[doc.index('| Vista | Qué reúne | Origen |'):]
VISTAS_DOC = re.findall(r'(?m)^\| ([^|]+?) \| [^|]+ \| [^|]+ \|$', tabla[:tabla.index('\n\n')])[1:]
COLUMNAS_DOC = ['Folio', 'Recepción', 'Canal', 'Materia', 'Alcaldía', 'Tipo de zona', 'Área que recibe', 'Remisión',
                'Estado', 'Persona asignada', 'Días hábiles']
# Los que terminan el trámite en la Secretaría: los finales del ciclo y la remisión.
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}

def recepcion(x): return x['datos'].get('fecha_recepcion_original') or x['datos']['fecha_acuse']
def dia(iso): return datetime.date(int(iso[:4]), int(iso[5:7]), int(iso[8:10]))
def habiles(x, hoy):
    fin = dia(x['tramite']['historial'][-1]['fecha'] if x['tramite']['estado'] in CIERRAN else hoy)
    d, n = dia(recepcion(x)), 0
    while d < fin:
        d += datetime.timedelta(days=1)
        n += d.weekday() < 5
    return n
def metros(a, b):
    r = math.pi / 180
    la1, la2 = float(a['lat']) * r, float(b['lat']) * r
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((float(b['lon']) - float(a['lon'])) * r / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))
def normaliza(t):
    return ''.join(c for c in unicodedata.normalize('NFD', (t or '').lower()) if unicodedata.category(c) != 'Mn')
def abierta(x): return x['tramite']['estado'] not in CIERRAN

def reglas(umbral):
    def parecidas(x):
        if not abierta(x) or not x['datos'].get('lat'): return []
        return [o for o in datos if o is not x and abierta(o) and o['datos'].get('lat') and o['datos']['materia'] == x['datos']['materia']
                and metros(x['datos'], o['datos']) <= umbral['metros'] and abs((dia(recepcion(x)) - dia(recepcion(o))).days) <= umbral['dias']]
    return {
      'todas':         lambda x: True,
      'por_turnar':    lambda x: x['tramite']['estado'] == 'recibida',
      'por_ubicar':    lambda x: x['tramite']['estado'] == 'por_ubicar',
      'en_analisis':   lambda x: x['tramite']['estado'] in ('turnada', 'en_analisis'),
      'por_remitir':   lambda x: x['datos'].get('remite_a') == 'PROFEPA' and abierta(x),
      'duplicado':     lambda x: bool(parecidas(x)),
      'revision':      lambda x: bool(x['tramite']['marcas']),
      'alcaldia':      lambda x: x['datos'].get('alcaldia_discrepa') == 'si',
      'autoridad':     lambda x: x['datos'].get('tipo_denunciado') == 'gobierno',
      'anonimas':      lambda x: x['datos']['identificacion'] == 'anonima',
      'por_notificar': lambda x: x['tramite']['estado'] == 'resuelta'}, parecidas

def ve(perfil, x):
    if perfil.get('soloCapturadas'): return x['canal'] != 'en_linea' and x['captura']['capturo'] == perfil['quien']
    return not perfil.get('area') or x['tramite']['area_actual'] in (perfil['area'], '')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri() + '#/bandeja'); pg.wait_for_timeout(600)
    pg.evaluate("() => { document.getElementById('perfil').value = 'directivos'; cambiaPerfil('directivos'); }")
    cat = pg.evaluate("""() => ({hoy: HOY, umbral: UMBRAL_DUPLICADO, perfiles: PERFILES.map(p => Object.assign({quien: capturistaDe(p)}, p)), vistas: VISTAS.map(v => ({id: v.id, nom: v.nom})),
      cierran: ESTADOS.filter(e => e.cierra).map(e => e.id)})""")
    REGLA, parecidas = reglas(cat['umbral'])
    folio_de = {x['datos']['folio']: x for x in datos}

    # ---- 1 y 2. Columnas, vistas y estados que cierran ----
    def encabezados(): return pg.evaluate("() => [...document.querySelectorAll('.tabla-bandeja th')].map(t => t.textContent)")
    afirma(encabezados() == COLUMNAS_DOC, 'las columnas son las del bosquejo, en su orden: %s' % encabezados())
    afirma([v['nom'] for v in cat['vistas']] == ['Todas'] + VISTAS_DOC,
           'las vistas son «Todas» y las diez del bosquejo, con sus nombres y en su orden')
    afirma(set(cat['cierran']) == CIERRAN, 'cierran el trámite los estados finales y la remisión: %s' % sorted(cat['cierran']))
    afirma('Los estados son una propuesta por acordar con la DGIVA y la DGCORENADR' in pg.inner_text('#pantalla'),
           'la bandeja dice en pantalla que los estados son una propuesta por acordar (MA-07, P-14)')
    afirma(all(any(REGLA[v['id']](x) for x in datos) for v in cat['vistas']),
           'cada vista tiene al menos una denuncia de prueba: %s' % [v['id'] for v in cat['vistas'] if not any(REGLA[v['id']](x) for x in datos)])
    malos = []
    for p in cat['perfiles']:
        if 'bandeja' not in p['pantallas']: continue
        pg.evaluate("(id) => cambiaPerfil(id)", p['id'])
        chips = pg.evaluate("() => Object.fromEntries([...document.querySelectorAll('.vistas a')].map(a => [a.getAttribute('href').split('/')[2], +a.querySelector('.cuenta').textContent]))")
        esperado = {v: sum(1 for x in datos if ve(p, x) and REGLA[v](x)) for v in REGLA}
        if chips != esperado: malos.append((p['id'], chips, esperado))
    afirma(not malos, 'en cada perfil, cada vista cuenta lo que dice su regla: %s' % malos[:1])
    pares = [(x['datos']['folio'], [o['datos']['folio'] for o in parecidas(x)]) for x in datos if parecidas(x)]
    afirma(len(pares) >= 2, 'hay al menos un par de posibles duplicados en los datos de prueba: %s' % pares)

    # ---- Lectura de todas las páginas de la vista ----
    def filas():
        return pg.evaluate("""() => [...document.querySelectorAll('.tabla-bandeja tbody tr')].map(tr =>
          Object.fromEntries([...tr.cells].map(td => [td.dataset.etiqueta, td.innerText.trim()])))""")
    def todas_las_filas():
        out = filas()
        while pg.locator('.paginacion button:has-text("Siguiente"):not([disabled])').count():
            pg.click('.paginacion button:has-text("Siguiente")'); out += filas()
        return out

    pg.evaluate("() => cambiaPerfil('directivos')")
    pg.evaluate("() => { location.hash = '#/bandeja/todas'; }"); pg.wait_for_timeout(150)
    paginas = pg.evaluate("() => document.querySelectorAll('.tabla-bandeja tbody tr').length")
    def rebasa(): return pg.evaluate("() => { const m = document.querySelector('.tabla-marco'); return m.scrollWidth - m.clientWidth; }")
    exceso = [rebasa()]
    F = filas()
    while pg.locator('.paginacion button:has-text("Siguiente"):not([disabled])').count():
        pg.click('.paginacion button:has-text("Siguiente")'); F += filas(); exceso.append(rebasa())
    afirma(max(exceso) <= 0, 'a 1280 px las once columnas caben sin desplazar la tabla, en todas las páginas: %s' % exceso)
    afirma(pg.evaluate("() => { const m = document.querySelector('.tabla-marco'); return m.tabIndex === 0 && m.getAttribute('role') === 'region' && !!m.getAttribute('aria-label'); }"),
           'si la pantalla es más angosta, el marco de la tabla se recorre con el teclado')
    afirma(paginas == 15 and len(F) == 40 and len({f['Folio'].split('\n')[0] for f in F}) == 40,
           'en páginas de quince, las cuarenta aparecen una sola vez: %d en la primera, %d en total' % (paginas, len(F)))

    # ---- 3. Días hábiles y fecha de recepción ----
    malos = []
    for f in F:
        x = folio_de[f['Folio'].split('\n')[0]]
        n = habiles(x, cat['hoy'])
        texto = str(n) + ('\nal cierre' if not abierta(x) else '')
        r = recepcion(x)
        fecha = '%d %s %s\n%s h' % (int(r[8:10]), 'ene feb mar abr may jun jul ago sep oct nov dic'.split()[int(r[5:7]) - 1], r[:4], r[11:16])
        if f['Días hábiles'] != texto or f['Recepción'] != fecha: malos.append((x['datos']['folio'], f['Días hábiles'], texto, f['Recepción'], fecha))
    afirma(not malos, 'días hábiles sin sábados ni domingos, hasta hoy o hasta el cierre, desde la recepción original: %s' % malos[:2])
    capt = [f for f in F if 'captura' in folio_de[f['Folio'].split('\n')[0]]]
    afirma(capt and all(f['Recepción'].startswith(str(int(folio_de[f['Folio'].split('\n')[0]]['datos']['fecha_recepcion_original'][8:10])) + ' ') for f in capt),
           'en lo capturado por personal, la fecha es la de recepción original, no la de captura')

    # ---- 4. Área y remisión ----
    prof = [f for f in F if folio_de[f['Folio'].split('\n')[0]]['datos'].get('remite_a') == 'PROFEPA']
    afirma(prof and all(f['Área que recibe'] == 'DGCORENADR' and f['Remisión'] == 'PROFEPA' for f in prof)
           and not any(f['Área que recibe'] == 'PROFEPA' for f in F),
           'las de la PROFEPA las recibe la DGCORENADR y la remisión va en su propia columna (DEC-235)')
    dup = [f for f in F if f['Folio'].split('\n')[0] in dict(pares)]
    afirma(dup and all(any(('Posible duplicado: ' + o[-8:]) in f['Folio'] for o in dict(pares)[f['Folio'].split('\n')[0]]) for f in dup),
           'cada posible duplicado dice con cuál se parece')

    # ---- 5. Filtros y búsqueda ----
    def cuenta(): return pg.evaluate("() => document.querySelectorAll('.tabla-bandeja tbody tr').length ? +document.getElementById('conteo').textContent.split(' ')[0] : 0")
    pg.focus('#f-materia'); pg.evaluate("() => { window.listaAntes = document.getElementById('f-materia'); }")
    pg.select_option('#f-materia', 'impacto')
    c1, foco = cuenta(), pg.evaluate("() => document.activeElement === window.listaAntes ? 'f-materia' : document.activeElement.id")
    pg.select_option('#f-estado', 'recibida')
    c2 = cuenta()
    afirma(c1 == sum(x['datos']['materia'] == 'impacto' for x in datos) and c2 == sum(x['datos']['materia'] == 'impacto' and x['tramite']['estado'] == 'recibida' for x in datos)
           and foco == 'f-materia', 'los filtros se combinan y el foco se queda en la lista: %d y %d' % (c1, c2))
    opciones = pg.evaluate("() => [...document.querySelectorAll('#f-asignado option')].map(o => o.textContent)")
    afirma(opciones[0] == 'Todas' and 'Sin asignar' in opciones and len(opciones) == 1 + len({x['tramite']['asignado'] for x in datos}),
           '«Sin asignar» es una opción y no hay opciones que den cero')
    pg.click('#pantalla .limpiar-filtros'); pg.wait_for_timeout(100)
    def busca(t):
        pg.fill('#f-texto', t)
        palabras = normaliza(t).split()
        return cuenta(), sum(all(p in normaliza(' '.join(str(x['datos'].get(k) or '') for k in ('folio', 'nombre_estab', 'calle', 'hechos'))) for p in palabras) for x in datos)
    casos = {t: busca(t) for t in ('000105', 'Negocio Ficticio 7', 'chapultepec', 'JARDIN', 'basura negocio')}
    afirma(all(a == b and a > 0 for a, b in casos.values()), 'la búsqueda va por folio, establecimiento, calle y hechos, sin importar acentos ni mayúsculas: %s' % casos)
    busca('zzzz')
    vacio = pg.evaluate("() => (document.querySelector('.sin-resultados') || {}).textContent || ''")
    afirma('Ninguna denuncia cumple' in vacio, 'sin resultados lo dice')
    pg.click('#pantalla .limpiar-filtros'); pg.wait_for_timeout(100)
    q = pg.evaluate("() => ({n: document.querySelectorAll('.tabla-bandeja tbody tr').length, foco: document.activeElement.id, t: document.getElementById('f-texto').value, boton: document.querySelector('#pantalla .limpiar-filtros').textContent})")
    afirma(q == {'n': 15, 'foco': 'f-texto', 't': '', 'boton': 'Limpiar filtros y búsqueda'},
           '«Limpiar filtros y búsqueda» está siempre a la vista, regresa todo y lleva el foco a la búsqueda (DEC-258): %s' % q)

    # ---- 6. Orden y páginas ----
    primero = lambda: folio_de[filas()[0]['Folio'].split('\n')[0]]
    orden = sorted(datos, key=recepcion)
    a = primero()
    pg.select_option('#f-orden', 'antiguas'); b = primero()
    afirma(a is orden[-1] and b is orden[0], 'ordena por recepción: más recientes o más antiguas primero')
    pg.click('.paginacion button:has-text("Siguiente")')
    p2 = pg.evaluate("() => ({c: document.getElementById('conteo').textContent, foco: document.activeElement.className})")
    pg.select_option('#f-canal', 'telefono')
    p1 = pg.evaluate("() => document.getElementById('conteo').textContent")
    afirma('Página 2 de 3' in p2['c'] and p2['foco'] == 'titulo-resultados' and 'Página' not in p1,
           'al cambiar de página el foco va al título del listado; al filtrar, vuelve a la primera: %s · %s' % (p2, p1))

    # ---- 7. Dirección y «Atrás» ----
    pg.click('.vistas a:has-text("Por turnar")'); pg.wait_for_timeout(150)
    v = pg.evaluate("() => ({hash: location.hash, actual: document.querySelector('.vistas a[aria-current=page]').textContent, foco: document.activeElement.textContent, filtro: document.getElementById('f-canal').value})")
    afirma(v['hash'] == '#/bandeja/por_turnar' and v['actual'].startswith('Por turnar') and v['foco'] == 'Por turnar' and v['filtro'] == 'telefono',
           'una vista cambia la dirección, se marca, lleva el foco a su título y conserva los filtros: %s' % v)
    pg.click('.tabla-bandeja a.folio'); pg.wait_for_timeout(150)
    e = pg.evaluate("() => ({hash: location.hash, texto: document.getElementById('pantalla').innerText})")
    folio = pg.evaluate("() => DENUNCIAS.filter(d => idDe(d) === location.hash.split('/')[2])[0].datos.folio")
    afirma(e['hash'].startswith('#/expediente/') and folio in e['texto'], 'el folio abre el expediente de esa denuncia: %s' % e['hash'])
    pg.go_back(); pg.wait_for_timeout(150)
    v = pg.evaluate("() => ({hash: location.hash, filtro: document.getElementById('f-canal').value, n: document.querySelectorAll('.tabla-bandeja tbody tr').length})")
    afirma(v['hash'] == '#/bandeja/por_turnar' and v['filtro'] == 'telefono' and v['n'] == sum(x['canal'] == 'telefono' and REGLA['por_turnar'](x) for x in datos),
           '«Atrás» regresa del expediente a la bandeja como estaba: %s' % v)
    pg.go_back(); pg.wait_for_timeout(150)
    afirma(pg.evaluate("() => location.hash") == '#/bandeja/todas', '«Atrás» regresa a la vista anterior')

    # ---- 8. Datos personales ----
    personales = {x['datos'][k] for x in datos for k in ('nombre', 'apellido_paterno', 'correo', 'telefono', 'dom_calle') if x['datos'].get(k)}
    malos = []
    for p in cat['perfiles']:
        if 'bandeja' not in p['pantallas']: continue
        pg.evaluate("(id) => { cambiaPerfil(id); location.hash = '#/bandeja/todas'; }", p['id']); pg.wait_for_timeout(100)
        texto = ' '.join(' '.join(f.values()) for f in todas_las_filas())
        malos += [(p['id'], t) for t in personales if re.search(r'(?<!\w)' + re.escape(t) + r'(?!\w)', texto)]
    afirma(not malos, 'ningún perfil ve en la bandeja nombre, correo, teléfono ni domicilio de quien denuncia: %s' % malos[:3])
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 9. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri() + '#/bandeja/todas'); tel.wait_for_timeout(500)
    t = tel.evaluate("""() => ({anchos: [document.documentElement.scrollWidth, innerWidth], abiertos: document.querySelector('.plegable').open,
      etiqueta: getComputedStyle(document.querySelector('.tabla-bandeja td'), '::before').content,
      fichas: [...document.querySelectorAll('.tabla-bandeja tbody tr')].every(tr => tr.scrollWidth <= tr.clientWidth + 1)})""")
    afirma(t['anchos'][0] <= t['anchos'][1] and t['fichas'], 'a 360 px no hay desplazamiento horizontal y cada ficha cabe: %s' % t['anchos'])
    afirma(t['etiqueta'] == '"Folio"' and t['abiertos'] is False, 'en teléfono cada dato lleva su etiqueta y los filtros empiezan plegados')
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
