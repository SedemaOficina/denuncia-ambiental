# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración, bloque A: el cascarón y los datos de
prueba (DEC-242).

   1. Abre sola, con doble clic: sin errores y sin pedir nada a internet salvo
      las tipografías; la franja dice que es una maqueta con datos ficticios.
   2. Lo que toma del formulario es idéntico a lo del formulario: variables de
      :root, logotipo, nombres de las materias y denuncias de prueba (las
      mismas del archivo de datos).
   3. Las denuncias de prueba son cuarenta, inequívocamente ficticias, y cubren
      cada valor de cada catálogo: materias, estados, canales, áreas, remisión,
      tipos de zona, anónimas, autoridad señalada, sin punto, alcaldía que no
      coincide, sin archivos y nombre larguísimo.
   4. Se navega por el menú, con teclado y con «Atrás»; el foco va al título.
   5. Cada perfil ve sus pantallas y sus denuncias; cada capturista, sólo lo
      que esa persona capturó; directivos, todo (DEC-256); una pantalla ajena
      lleva a la primera propia.
   6. En teléfono no hay desplazamiento horizontal."""
import json, os, pathlib, re, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
DATOS = RAIZ / 'prototipo' / 'administracion' / 'denuncias-ficticias.json'
PROTO = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

def luhn(num):
    t = 0
    for i, c in enumerate(reversed(num)):
        x = int(c)
        if i % 2 == 0:
            x *= 2
            if x > 9: x -= 9
        t += x
    return str((10 - t % 10) % 10)

m = MAQUETA.read_text(encoding='utf-8'); p = PROTO.read_text(encoding='utf-8')
datos = json.loads(DATOS.read_text(encoding='utf-8'))

# ---- 2. Lo que viene del formulario ----
afirma(re.search(r'(?ms)^:root\{.*?^\}', p).group(0) in m, 'las variables de :root son las del formulario, al carácter')
afirma(re.search(r'<img class="logo-inst"[^>]*>', p).group(0) in m, 'el logotipo es el del formulario')
# La copia de GitHub Pages es la misma maqueta; sólo su liga al modo captura
# lleva al formulario publicado, que está junto a ella (DEC-250).
PUBLICADA = RAIZ / 'docs' / 'administracion' / 'index.html'
pub = PUBLICADA.read_text(encoding='utf-8') if PUBLICADA.exists() else ''
liga = re.search(r"var FORMULARIO_CAPTURA = '([^']+)';", pub)
afirma(liga and pub == m.replace("'../prototipo-denuncia-ambiental-sedema.html?modo=captura'", "'%s'" % liga.group(1))
       and liga.group(1).endswith('?modo=captura') and (PUBLICADA.parent / liga.group(1).split('?')[0]).resolve() == (RAIZ / 'docs' / 'index.html').resolve(),
       'la maqueta publicada en GitHub Pages es la misma, con la liga al modo captura hacia el formulario publicado')
bloque = p[p.index('var MATERIAS = ['):]
bloque = bloque[:bloque.index('\n];')]
del_formulario = [{'id': i, 'nom': n} for i, n in re.findall(r"\{id:'([a-z_]+)',.*?\bnom:'([^']+)'", bloque)]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err, red = [], []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.on('request', lambda r: red.append(r.url) if r.url.startswith('http') and not r.url.startswith(TIPOGRAFIAS) else None)
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(600)

    # ---- 1. Abre sola ----
    c = pg.evaluate("""() => ({franja: (document.querySelector('.franja-maqueta') || {}).innerText || '', lang: document.documentElement.lang,
      logo: !!document.querySelector('header .logo-inst[src^="data:image/png;base64,"]'), titulo: document.title})""")
    afirma('Maqueta con datos ficticios' in c['franja'] and c['lang'] == 'es-MX' and c['logo'] and 'maqueta' in c['titulo'],
           'abre con la franja de maqueta, el idioma es-MX y el logotipo institucional')
    afirma(pg.evaluate("() => JSON.stringify(DENUNCIAS)") == json.dumps(datos, ensure_ascii=False, separators=(',', ':')),
           'las denuncias de la maqueta son las del archivo de datos')
    afirma(len(del_formulario) == 19 and pg.evaluate("() => MATERIAS") == del_formulario,
           'las materias de la maqueta son las del formulario, con sus nombres y en su orden')

    # ---- 3. Las denuncias de prueba ----
    cat = pg.evaluate("() => ({estados: ESTADOS.map(e => e.id), canales: CANALES.map(c => c.id)})")
    D = [x['datos'] for x in datos]
    T = [x['tramite'] for x in datos]
    afirma(len(datos) == 40 and all(x['es_ficticio'] is True for x in datos), 'son cuarenta y todas dicen ser ficticias')
    nombres = {'Fulana', 'Mengano', 'Zutana', 'Perengano', 'Fulano', 'Mengana', 'Zutano', 'Perengana', 'Fulana de las Mercedes Guadalupe'}
    afirma(all(d.get('nombre', 'Fulana') in nombres for d in D) and all(d['correo'].endswith('@ejemplo.local') for d in D)
           and all(d.get('telefono', '5500000000').startswith('55000000') for d in D),
           'nadie parece una persona real: nombres de relleno, correos @ejemplo.local y teléfonos de ceros')
    folios = [d['folio'] for d in D]
    afirma(len(set(folios)) == 40 and all(f[-1] == luhn(f[11:15] + f[16:22]) for f in folios),
           'folios únicos, con el carácter verificador del documento 19')
    afirma(len({d['materia'] for d in D}) == 19, 'están las diecinueve materias')
    afirma({t['estado'] for t in T} == set(cat['estados']), 'están todos los estados del ciclo: faltan %s' % sorted(set(cat['estados']) - {t['estado'] for t in T}))
    afirma({x['canal'] for x in datos} == set(cat['canales']), 'están todos los canales')
    afirma({d.get('dg') for d in D} == {'DGIVA', 'DGCORENADR', None} and any(d.get('remite_a') == 'PROFEPA' for d in D),
           'reciben las dos direcciones generales, hay remisiones a la PROFEPA y una sin punto')
    zonas = {d.get('capa_clase') for d in D}
    afirma({'Suelo urbano', 'Área de Valor Ambiental', 'Área Natural Protegida', 'Suelo de conservación'} <= zonas,
           'hay puntos en suelo urbano, Área de Valor Ambiental, Área Natural Protegida y suelo de conservación')
    afirma(any(d['identificacion'] == 'anonima' for d in D) and any(d.get('tipo_denunciado') == 'gobierno' for d in D)
           and any(d.get('alcaldia_discrepa') == 'si' for d in D) and any(not x['archivos'] for x in datos)
           and any(len(d.get('nombre', '')) > 30 for d in D),
           'y los casos incómodos: anónima, autoridad señalada, alcaldía que no coincide, sin archivos y nombre larguísimo')
    afirma(all(('captura' in x) == (x['canal'] != 'en_linea') for x in datos),
           'lo capturado por personal trae canal y soporte (AD-03); lo de en línea, no')
    acum = [t for t in T if t['estado'] == 'acumulada']
    afirma(acum and all(t['acumulada_en'] in folios for t in acum), 'la acumulada apunta a un folio que existe')
    afirma(all([h['fecha'] for h in t['historial']] == sorted(h['fecha'] for h in t['historial']) and t['historial'][-1]['estado'] == t['estado'] for t in T),
           'cada historial va en orden y termina en el estado actual')

    # ---- 4. Navegación ----
    def donde():
        return pg.evaluate("""() => ({hash: location.hash, h2: (document.querySelector('#pantalla h2') || {}).textContent,
          foco: document.activeElement && document.activeElement.tagName, actual: (document.querySelector('.menu a[aria-current=page]') || {}).textContent})""")
    for nom in ('Bandeja', 'Mapa operativo', 'Búsqueda y exportación'):
        pg.click('.menu a:has-text("%s")' % nom); pg.wait_for_timeout(150)
        d = donde()
        afirma(d['h2'] == nom and d['actual'] == nom and d['foco'] == 'H2', 'el menú lleva a «%s», la marca y pone el foco en su título' % nom)
    pg.go_back(); pg.wait_for_timeout(150)
    afirma(donde()['h2'] == 'Mapa operativo', '«Atrás» regresa a la pantalla anterior')
    pg.focus('.menu a:has-text("Inicio")'); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    afirma(donde()['h2'] == 'Inicio', 'con teclado: Enter sobre el menú abre la pantalla')

    # ---- 5. Perfiles ----
    perf = pg.evaluate("""() => PERFILES.map(p => { cambiaPerfil(p.id);
      return {id: p.id, menu: [...document.querySelectorAll('.menu a')].map(a => a.getAttribute('href').slice(2)),
              esperado: p.pantallas.filter(x => x !== 'expediente'), cifra: visibles().length,
              texto: document.getElementById('pantalla').innerText}; })""")
    # El menú sigue siempre el orden de PANTALLAS; lo que cambia es cuáles.
    afirma(all(set(x['menu']) == set(x['esperado']) for x in perf), 'cada perfil ve en el menú sus pantallas, y sólo ésas')
    cuenta = {x['id']: x['cifra'] for x in perf}
    quien = pg.evaluate("() => Object.fromEntries(PERFILES.filter(p => p.soloCapturadas).map(p => [p.id, capturistaDe(p)]))")
    personal = pg.evaluate("() => PERSONAL")
    # Sin punto no hay área todavía: la ven las dos direcciones generales.
    afirma(cuenta['atencion_dgiva'] == sum(t['area_actual'] in ('DGIVA', '') for t in T)
           and cuenta['atencion_dgcorenadr'] == sum(t['area_actual'] in ('DGCORENADR', '') for t in T)
           and all(cuenta[k] == sum(x['canal'] != 'en_linea' and x['captura']['capturo'] == q for x in datos) for k, q in quien.items())
           and cuenta['directivos'] == 40,
           'cada perfil cuenta sus denuncias, y las que no tienen punto las ven las dos direcciones generales: %s' % cuenta)
    afirma(('simula a %s y ve sólo lo que capturó' % quien['capturista_dgiva']) in next(x for x in perf if x['id'] == 'capturista_dgiva')['texto']
           and 'Ve todas las denuncias de la Secretaría.' in next(x for x in perf if x['id'] == 'directivos')['texto'],
           'cada capturista dice a quién simula y que ve sólo lo que capturó; directivos, que ve todas')
    dg_de = {x['nombre']: x['dg'] for x in personal}
    por_persona = {q: sum(x['canal'] != 'en_linea' and x['captura']['capturo'] == q for x in datos) for q in dg_de if q.startswith('Capturista')}
    afirma(any(dg_de[x['captura']['capturo']] != x['tramite']['area_actual'] for x in datos if 'captura' in x)
           and sum(n > 0 for q, n in por_persona.items() if dg_de[q] == 'DGIVA') == 2,
           'dos capturistas de la DGIVA capturaron, cada quien lo suyo, y una denuncia capturada en la DGIVA fue a dar por su punto a la DGCORENADR: %s' % por_persona)
    pg.evaluate("() => { cambiaPerfil('atencion_dgiva'); location.hash = '#/administracion'; }"); pg.wait_for_timeout(150)
    afirma(donde()['h2'] == 'Inicio', 'una pantalla que el perfil no tiene lleva a la primera que sí')

    afirma(not red, 'no pide nada a internet salvo las tipografías: %s' % red[:3])
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 6. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri()); tel.wait_for_timeout(500)
    anchos = tel.evaluate("() => [document.documentElement.scrollWidth, innerWidth]")
    afirma(anchos[0] <= anchos[1], 'a 360 px no hay desplazamiento horizontal: %s' % anchos)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
