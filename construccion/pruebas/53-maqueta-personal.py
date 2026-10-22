# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración: el personal que da de alta y de baja
   cada coordinación (DEC-252).

   1. Sólo coordinación tiene la pantalla «Personal», y cada coordinación ve
      sólo a la gente de su dirección general; administración ve a las dos,
      sin poder cambiar nada.
   2. Se piden nombre, área de la que depende, cargo, correo institucional y
      perfil, cada uno con su etiqueta; los perfiles que se dan son captura,
      atención y coordinación, ni consulta ni administración.
   3. Sin un dato, o con un correo que no es correo, no hay alta: el aviso
      dice cuál falta y el foco va a ese campo. Dos personas activas no
      comparten correo.
   4. El alta queda en la dirección general de quien la da, en la tabla, en
      la de administración y en la bitácora; si es de atención, ya cuenta
      entre las personas activas de su área.
   5. La baja no borra: la persona queda «De baja», sigue en la lista y en la
      bitácora, y se avisa lo que tenía abierto. Una dirección general no se
      queda sin coordinación activa.
   6. En teléfono no hay desplazamiento horizontal; sin errores en consola."""
import json, os, pathlib, sys
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
CIERRAN = {'remitida', 'concluida', 'acumulada', 'sin_materia', 'recomendacion'}
datos = json.loads(DATOS.read_text(encoding='utf-8'))

LEE = """() => ({
  h2: (document.querySelector('#pantalla h2') || {}).textContent,
  filas: [...document.querySelectorAll('#pantalla tbody tr')].map(tr => [...tr.children].map(c => c.innerText.trim())),
  aviso: (document.getElementById('aviso-personal') || {}).textContent,
  foco: document.activeElement && document.activeElement.id,
  n: PERSONAL.length})"""

def llena(pg, nombre='Fulana de Prueba Alta', area='Área de prueba nueva', cargo='Cargo de prueba nuevo', correo='fulana.alta@ejemplo.local', perfil='atencion'):
    for k, v in (('nombre', nombre), ('area', area), ('cargo', cargo), ('correo', correo)):
        pg.fill('#a-' + k, v)
    pg.select_option('#a-perfil', perfil)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(500)
    inicial = pg.evaluate("() => JSON.parse(JSON.stringify(PERSONAL))")

    # ---- 1. Quién la tiene ----
    tienen = pg.evaluate("() => PERFILES.filter(p => p.pantallas.indexOf('personal') >= 0).map(p => p.rol)")
    afirma(tienen == ['coordinacion', 'coordinacion'], 'sólo las dos coordinaciones tienen la pantalla «Personal»: %s' % tienen)
    def abre(perfil):
        pg.evaluate("(p) => { cambiaPerfil(p); location.hash = '#/personal'; }", perfil); pg.wait_for_timeout(150)
        return pg.evaluate(LEE)
    vistas = {}
    for dg in ('DGIVA', 'DGCORENADR'):
        t = abre('coordinacion_' + dg.lower())
        vistas[dg] = [f[0] for f in t['filas']]
    afirma(t['h2'] == 'Personal' and all(vistas[dg] == [x['nombre'] for x in inicial if x['dg'] == dg] and vistas[dg] for dg in vistas),
           'cada coordinación ve sólo a la gente de su dirección general: %s' % vistas)
    pg.evaluate("() => { cambiaPerfil('atencion_dgiva'); location.hash = '#/personal'; }"); pg.wait_for_timeout(150)
    afirma(pg.evaluate(LEE)['h2'] != 'Personal', 'atención no entra a «Personal»: la dirección lleva a su primera pantalla')

    # ---- 2. El formulario ----
    t = abre('coordinacion_dgiva')
    etiquetas = pg.evaluate("""() => ['nombre', 'area', 'cargo', 'correo', 'perfil'].map(k => {
      const el = document.getElementById('a-' + k); return el && el.labels.length ? el.labels[0].textContent : null; })""")
    afirma(etiquetas == ['Nombre completo', 'Área de la que depende', 'Cargo', 'Correo institucional', 'Perfil'],
           'pide nombre, área de la que depende, cargo, correo institucional y perfil, cada uno con su etiqueta: %s' % etiquetas)
    perfiles = pg.evaluate("() => [...document.querySelectorAll('#a-perfil option')].filter(o => o.value).map(o => o.value)")
    afirma(perfiles == ['capturista', 'atencion', 'coordinacion'], 'da perfiles de capturista, atención y coordinación, ni directivos ni administración: %s' % perfiles)

    # ---- 3. Sin un dato no hay alta ----
    malos = []
    for k, etq in (('nombre', 'Nombre completo'), ('area', 'Área de la que depende'), ('cargo', 'Cargo'), ('correo', 'Correo institucional')):
        abre('coordinacion_dgiva'); llena(pg); pg.fill('#a-' + k, '')
        pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(80)
        r = pg.evaluate(LEE)
        if r['n'] != len(inicial) or etq not in r['aviso'] or r['foco'] != 'a-' + k or pg.get_attribute('#a-' + k, 'aria-invalid') != 'true':
            malos.append((k, r['aviso'], r['foco']))
    abre('coordinacion_dgiva'); llena(pg); pg.select_option('#a-perfil', '')
    pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(80)
    r = pg.evaluate(LEE)
    if r['n'] != len(inicial) or 'Perfil' not in r['aviso'] or r['foco'] != 'a-perfil': malos.append(('perfil', r['aviso'], r['foco']))
    afirma(not malos, 'sin un dato no hay alta: el aviso dice cuál y el foco va a ese campo: %s' % malos)
    abre('coordinacion_dgiva'); llena(pg, correo='esto no es correo')
    pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(80)
    r = pg.evaluate(LEE)
    afirma(r['n'] == len(inicial) and 'no es válido' in r['aviso'] and r['foco'] == 'a-correo', 'un correo que no es correo no pasa: %s' % r['aviso'])
    abre('coordinacion_dgiva'); llena(pg, correo=inicial[1]['correo'].upper())
    pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(80)
    r = pg.evaluate(LEE)
    afirma(r['n'] == len(inicial) and 'Ya hay una persona activa con ese correo' in r['aviso'], 'dos personas activas no comparten correo, sin importar mayúsculas')

    # ---- 4. El alta ----
    abre('coordinacion_dgiva'); llena(pg)
    pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(100)
    r = pg.evaluate(LEE)
    nueva = pg.evaluate("() => PERSONAL[PERSONAL.length - 1]")
    afirma(r['n'] == len(inicial) + 1 and nueva == {'nombre': 'Fulana de Prueba Alta', 'dg': 'DGIVA', 'area': 'Área de prueba nueva', 'cargo': 'Cargo de prueba nuevo',
                                                     'correo': 'fulana.alta@ejemplo.local', 'perfil': 'atencion', 'activa': True},
           'el alta queda en la dirección general de quien la da, con sus datos: %s' % nueva)
    afirma(['Fulana de Prueba Alta', 'Área de prueba nueva', 'Cargo de prueba nuevo', 'fulana.alta@ejemplo.local', 'Atención', 'Activa', 'Dar de baja'] in r['filas']
           and 'Se dio de alta a Fulana de Prueba Alta' in r['aviso'] and r['foco'] == 'a-nombre',
           'aparece en la tabla, el aviso lo dice y el foco vuelve al nombre para la siguiente')
    afirma(pg.evaluate("() => activas('DGIVA', 'atencion').map(x => x.nombre).indexOf('Fulana de Prueba Alta') >= 0 && bitacora[0].que.indexOf('Da de alta a Fulana de Prueba Alta (Atención, DGIVA)') === 0"),
           'ya cuenta entre las personas de atención activas de la DGIVA, y la bitácora lo registra')
    t = abre('coordinacion_dgcorenadr')
    afirma('Fulana de Prueba Alta' not in [f[0] for f in t['filas']], 'la otra coordinación no la ve')

    # ---- 5. La baja ----
    t = abre('coordinacion_dgiva')
    b = next(x for x in inicial if x['dg'] == 'DGIVA' and x['perfil'] == 'atencion' and x['nombre'].endswith('B (DGIVA)'))
    abiertas = sum(x['tramite']['asignado'] == b['nombre'] and x['tramite']['estado'] not in CIERRAN for x in datos)
    pg.click('button[aria-label="Dar de baja a %s"]' % b['nombre']); pg.wait_for_timeout(100)
    r = pg.evaluate(LEE)
    fila = next(f for f in r['filas'] if f[0] == b['nombre'])
    afirma(r['n'] == len(inicial) + 1 and fila[5] == 'De baja' and fila[6] == '' and abiertas > 0 and ('Tenía %d denuncias abiertas asignadas' % abiertas) in r['aviso'],
           'la baja no borra: queda «De baja», sin botón, y avisa las %d denuncias abiertas que hay que reasignar' % abiertas)
    afirma(pg.evaluate("(n) => activas('DGIVA', 'atencion').every(x => x.nombre !== n) && bitacora[0].que.indexOf('Da de baja a ' + n) === 0", b['nombre']),
           'deja de contar entre las activas y la bitácora lo registra')
    coord = next(x for x in inicial if x['dg'] == 'DGIVA' and x['perfil'] == 'coordinacion')
    pg.click('button[aria-label="Dar de baja a %s"]' % coord['nombre']); pg.wait_for_timeout(100)
    r = pg.evaluate(LEE)
    afirma(next(f for f in r['filas'] if f[0] == coord['nombre'])[5] == 'Activa' and 'sin coordinación activa' in r['aviso'],
           'la única coordinación activa no se puede dar de baja')
    abre('coordinacion_dgiva'); llena(pg, nombre='Otra Coordinación de Prueba', correo='otra.coordinacion@ejemplo.local', perfil='coordinacion')
    pg.click('button:has-text("Dar de alta")'); pg.wait_for_timeout(100)
    pg.click('button[aria-label="Dar de baja a %s"]' % coord['nombre']); pg.wait_for_timeout(100)
    r = pg.evaluate(LEE)
    afirma(next(f for f in r['filas'] if f[0] == coord['nombre'])[5] == 'De baja', 'con otra coordinación activa, la primera sí se puede dar de baja')

    # ---- 1. Administración ve todo, sin cambiar nada ----
    pg.evaluate("() => { cambiaPerfil('administracion'); location.hash = '#/administracion'; }"); pg.wait_for_timeout(150)
    adm = pg.evaluate("""() => { const h = [...document.querySelectorAll('#pantalla h3')].find(x => x.textContent === 'Personal de las direcciones generales');
      const t = h.nextElementSibling; return {filas: [...t.querySelectorAll('tbody tr')].map(tr => [...tr.children].map(c => c.innerText.trim())),
      botones: t.querySelectorAll('button').length}; }""")
    afirma(len(adm['filas']) == pg.evaluate("() => PERSONAL.length") and adm['botones'] == 0
           and ['Fulana de Prueba Alta', 'DGIVA', 'Área de prueba nueva', 'Cargo de prueba nuevo', 'fulana.alta@ejemplo.local', 'Atención', 'Activa'] in adm['filas'],
           'administración ve al personal de las dos direcciones generales, con lo dado de alta, y sin botones')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 6. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri()); tel.wait_for_timeout(400)
    tel.evaluate("() => { cambiaPerfil('coordinacion_dgiva'); location.hash = '#/personal'; }"); tel.wait_for_timeout(200)
    afirma(tel.evaluate("() => document.documentElement.scrollWidth - innerWidth") <= 0, 'a 360 px no hay desplazamiento horizontal')
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
