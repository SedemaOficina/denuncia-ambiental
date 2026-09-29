# -*- coding: utf-8 -*-
"""La colonia con catálogo, el código postal de la Ciudad y la celda UGA (DEC-117).

   Colonia. El campo sugiere del catálogo del IECM 2022 mientras se escribe, y
   cada sugerencia lleva su alcaldía, porque hay nombres repetidos. Lo que se
   vigila:
   1. Que sea un combobox de verdad: rol, lista enlazada, teclado.
   2. Que la búsqueda ignore acentos y encuentre por cualquier palabra.
   3. Que, con punto, las colonias de la alcaldía del punto vayan primero.
   4. Que la colonia NO corrija la alcaldía (DEC-72): si no coinciden, avisa.
   5. Que el catálogo sugiera sin obligar: lo que no está se conserva igual.
   6. Que lo escrito sin elegir se reconozca sólo cuando no hay duda.

   Código postal. Se escribe a mano. El del lugar tiene que ser de la Ciudad,
   del 01000 al 16999; el del domicilio de la persona, no.

   UGA. La asigna el punto, no se muestra, y coincide con el polígono que lo
   contiene en la capa completa del SIA."""
import os, pathlib, sys, json, random
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
UGA  = RAIZ.parent / 'capas' / 'originales' / 'UGA_CDMX.geojson'
TMP  = AQUI / '_pagina18.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

PREP = """() => { estado = {}; archivos = []; cfg.validar = true;
  guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2); }"""
PUNTO = (19.3500, -99.1620)

def escribe(pg, texto):
    pg.fill('#f_colonia', '')
    pg.type('#f_colonia', texto, delay=10)
    pg.wait_for_timeout(120)

def opciones(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#lista_colonia li[role=option]')]
      .map(li => ({nom: li.querySelector('.op-nom').textContent, alc: li.querySelector('.op-alc').textContent}))""")

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---------------- el catálogo ----------------
    cat = pg.evaluate("""() => ({n: CATALOGO_COLONIAS.filas.length, a: CATALOGO_COLONIAS.alcaldias.length,
      unicas: new Set(CATALOGO_COLONIAS.filas.map(r => r[2])).size,
      alcOk: CATALOGO_COLONIAS.alcaldias.every(a => CAPAS_ALCALDIAS.some(f => f.p.nombre === a)),
      mayus: CATALOGO_COLONIAS.filas.filter(r => r[0] === r[0].toUpperCase() && /[A-Z]{4}/.test(r[0])).length})""")
    afirma(cat['n'] == 1837 and cat['unicas'] == 1837, 'el catálogo trae las 1 837 colonias del IECM, cada una con su clave (%d)' % cat['n'])
    afirma(cat['a'] == 16 and cat['alcOk'], 'y sus 16 alcaldías se llaman igual que en la capa del punto')
    afirma(cat['mayus'] == 0, 'ningún nombre se muestra en mayúsculas sostenidas (%d)' % cat['mayus'])

    # ---------------- el control ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(400)
    c = pg.evaluate("""() => { const i = document.getElementById('f_colonia'), l = document.getElementById('lista_colonia');
      return {rol: i.getAttribute('role'), ctrl: i.getAttribute('aria-controls'), exp: i.getAttribute('aria-expanded'),
              auto: i.getAttribute('autocomplete'), lista: l && l.getAttribute('role'), oculta: l && l.hidden}; }""")
    afirma(c['rol'] == 'combobox' and c['ctrl'] == 'lista_colonia' and c['lista'] == 'listbox',
           'la colonia es un combobox enlazado a su lista')
    afirma(c['exp'] == 'false' and c['oculta'], 'la lista empieza cerrada')
    afirma(c['auto'] == 'off', 'el autocompletado del navegador no se encima con el del catálogo')

    escribe(pg, 'c')
    afirma(opciones(pg) == [], 'con una sola letra no se sugiere nada')
    escribe(pg, 'chimal')
    ops = opciones(pg)
    alcs = sorted(set(o['alc'] for o in ops if o['nom'] == 'Chimalistac'))
    afirma(len(alcs) >= 2, '«Chimalistac» aparece una vez por alcaldía, cada una con la suya: %s' % alcs)
    afirma(all(o['alc'] for o in ops) and 0 < len(ops) <= 8, 'toda sugerencia lleva alcaldía, y son ocho como máximo (%d)' % len(ops))
    afirma(pg.get_attribute('#f_colonia', 'aria-expanded') == 'true', 'al sugerir, el campo anuncia la lista abierta')

    escribe(pg, 'juarez')
    ops = opciones(pg)
    afirma(any('Juárez' in o['nom'] for o in ops), 'la búsqueda ignora acentos: «juarez» encuentra «Juárez»')
    escribe(pg, 'pedregal nicolas')
    ops = opciones(pg)
    afirma(ops and all('Pedregal' in o['nom'] and 'Nicolás' in o['nom'] for o in ops),
           'y encuentra por varias palabras en cualquier orden (%s)' % (ops[0]['nom'] if ops else '—'))
    escribe(pg, 'u hab')
    afirma(len(opciones(pg)) > 0, 'también por la abreviatura con que la escribe el IECM')

    # teclado
    escribe(pg, 'chimal')
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(80)
    act = pg.evaluate("() => { const i=document.getElementById('f_colonia'); const id=i.getAttribute('aria-activedescendant'); const li=id&&document.getElementById(id); return {id, sel: li && li.getAttribute('aria-selected'), nom: li && li.querySelector('.op-nom').textContent, alc: li && li.querySelector('.op-alc').textContent}; }")
    afirma(act['id'] and act['sel'] == 'true', 'la flecha marca la primera sugerencia sin sacar el foco del campo')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
    el = pg.evaluate("() => ({col: val('colonia'), cve: val('colonia_cve'), alc: val('colonia_alcaldia'), cerr: document.getElementById('lista_colonia').hidden, inp: document.getElementById('f_colonia').value})")
    afirma(el['col'] == act['nom'] and el['inp'] == act['nom'] and el['cve'] and el['alc'] == act['alc'] and el['cerr'],
           'Enter la elige: nombre, clave %s y alcaldía %s, y la lista se cierra' % (el['cve'], el['alc']))
    pg.keyboard.type('x'); pg.wait_for_timeout(80)
    afirma(pg.evaluate("() => val('colonia_cve')") == '', 'si se sigue escribiendo, la clave elegida se suelta')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(60)
    afirma(pg.evaluate("() => document.getElementById('lista_colonia').hidden"), 'Escape cierra la lista')

    # clic: la elección no dispara la salida del campo antes de tiempo
    escribe(pg, 'narvarte')
    pg.click('#lista_colonia li[role=option] >> nth=0'); pg.wait_for_timeout(120)
    afirma(pg.evaluate("() => !!val('colonia_cve') && /Narvarte/.test(val('colonia'))"), 'un clic sobre la sugerencia también la elige')

    # ---------------- con punto: prioridad y aviso ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(300)
    pg.evaluate("([a,b]) => ponMarcador(a,b)", list(PUNTO)); pg.wait_for_timeout(400)
    alcP = pg.evaluate("() => val('alcaldia')")
    afirma(bool(alcP), 'el punto de prueba cae en %s' % alcP)
    # un nombre repetido que exista en la alcaldía del punto
    dup = pg.evaluate("""(alc) => { const f = CATALOGO_COLONIAS.filas, A = CATALOGO_COLONIAS.alcaldias, c = {};
      f.forEach(r => { (c[r[0]] = c[r[0]] || []).push(A[r[1]]); });
      return Object.keys(c).find(n => c[n].length > 1 && c[n].indexOf(alc) >= 0 && c[n][0] !== alc) ||
             Object.keys(c).find(n => c[n].length > 1 && c[n].indexOf(alc) >= 0); }""", alcP)
    escribe(pg, dup)
    ops = opciones(pg)
    afirma(ops and ops[0]['alc'] == alcP, 'con punto, la colonia de su alcaldía va primero: «%s · %s»' % (ops[0]['nom'], ops[0]['alc']) if ops else 'sin opciones')
    pg.evaluate("() => document.getElementById('f_colonia').blur()"); pg.wait_for_timeout(120)
    rec = pg.evaluate("() => ({cve: val('colonia_cve'), alc: val('colonia_alcaldia')})")
    afirma(rec['cve'] and rec['alc'] == alcP, 'escrito sin elegir, un nombre repetido se reconoce por la alcaldía del punto (%s)' % rec['cve'])
    afirma(pg.evaluate("() => document.getElementById('avisoColonia').textContent.trim()") == '', 'si coinciden, no hay aviso')

    otra = pg.evaluate("""(alc) => CATALOGO_COLONIAS.filas.findIndex(r => CATALOGO_COLONIAS.alcaldias[r[1]] !== alc)""", alcP)
    pg.evaluate("(i) => eligeColonia(i)", otra); pg.wait_for_timeout(120)
    av = pg.evaluate("() => ({t: document.getElementById('avisoColonia').textContent, alc: val('alcaldia'), ca: val('colonia_alcaldia')})")
    afirma(av['ca'] in av['t'] and alcP in av['t'], 'si no coinciden, se avisa con las dos alcaldías')
    afirma(av['alc'] == alcP, 'y la alcaldía sigue siendo la del punto: la colonia no la corrige (DEC-72)')
    afirma('límite' in av['t'], 'el aviso admite que cerca del límite puede no haber error')
    pg.evaluate("() => valida(2)"); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => !document.querySelector('#c_colonia.invalido')"),
           'el aviso no bloquea: al continuar, la colonia no se marca como error')
    # el aviso sigue al punto
    pg.evaluate("([a,b]) => ponMarcador(a,b)", [19.2000, -99.0300]); pg.wait_for_timeout(300)
    ca, pa = pg.evaluate("() => [val('colonia_alcaldia'), val('alcaldia')]")
    t = pg.evaluate("() => document.getElementById('avisoColonia').textContent")
    afirma((ca == pa) == (t.strip() == ''), 'al mover el punto, el aviso se recalcula (%s / %s)' % (ca, pa))

    # ---------------- lo que no está en el catálogo ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(300)
    escribe(pg, 'Colonia Zyxwv Inventada')
    vac = pg.evaluate("() => { const v = document.querySelector('#lista_colonia .combo-vacio'); return v ? v.textContent : ''; }")
    afirma('como la escribiste' in vac, 'si no hay coincidencias, se dice que se conserva como se escribió')
    pg.evaluate("() => document.getElementById('f_colonia').blur()"); pg.wait_for_timeout(120)
    fl = pg.evaluate("() => ({col: val('colonia'), cve: val('colonia_cve')})")
    afirma(fl['col'] == 'Colonia Zyxwv Inventada' and fl['cve'] == '', 'y se conserva igual, sin clave')

    # ---------------- código postal ----------------
    def cp(k, v):
        return pg.evaluate("([k,v]) => { guarda(k,v); avisaFormato(k); return {mal: formatoMal(k), msg: msgFormato(k)}; }", [k, v])
    afirma(not cp('cp', '06010')['mal'], 'un código postal de la Ciudad se acepta (06010)')
    afirma(not cp('cp', '16035')['mal'] and not cp('cp', '01000')['mal'], 'también en los extremos del intervalo (01000, 16035)')
    r = cp('cp', '1234');  afirma(r['mal'] and 'cinco dígitos' in r['msg'], 'cuatro dígitos: «%s»' % r['msg'])
    r = cp('cp', '55000'); afirma(r['mal'] and 'no es de la Ciudad' in r['msg'], 'cinco dígitos de otra entidad: «%s»' % r['msg'])
    r = cp('cp', '00100'); afirma(r['mal'], 'y 00100 tampoco')
    afirma(not cp('dom_cp', '55000')['mal'], 'el del domicilio de la persona sí puede ser de otra entidad')
    pg.evaluate("() => { guarda('cp',''); guarda('dom_cp',''); }")

    # ---------------- UGA ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(300)
    pg.evaluate("([a,b]) => ponMarcador(a,b)", list(PUNTO)); pg.wait_for_timeout(300)
    u = pg.evaluate("() => ({uga: val('uga'), ver: val('uga_version')})")
    import re
    afirma(re.match(r'^[A-Z]{3}-\d{3}$', u['uga'] or '') is not None and u['ver'], 'el punto asigna la celda UGA %s (%s)' % (u['uga'], u['ver']))
    vis2 = pg.evaluate("(c) => document.body.innerText.indexOf(c) >= 0 || /\\bUGA\\b/.test(document.body.innerText)", u['uga'])
    afirma(not vis2, 'la celda no se muestra en el paso 2')
    pg.evaluate("() => { guarda('hechos','Tiran escombro en la esquina desde hace dos semanas, por las noches.'); guarda('identificacion','anonima'); irA(6); alternaDetalleRevision(); }")
    pg.wait_for_timeout(300)
    vis6 = pg.evaluate("(c) => document.body.innerText.indexOf(c) >= 0 || /\\bUGA\\b/.test(document.body.innerText)", u['uga'])
    afirma(not vis6, 'ni en la revisión que ve la persona')
    pg.evaluate("() => irA(2)"); pg.wait_for_timeout(300)
    pg.evaluate("() => ponMarcador(19.6500, -99.4000)"); pg.wait_for_timeout(300)
    afirma(pg.evaluate("() => val('uga')") == '', 'fuera de la Ciudad no hay celda')

    if UGA.exists():
        try:
            from shapely.geometry import shape, Point
            d = json.load(open(UGA, encoding='utf-8'))
            polis = [(f['properties']['clave'], shape(f['geometry'])) for f in d['features']]
            random.seed(7); pts = []
            while len(pts) < 150:
                cl, g = random.choice(polis)
                x0, y0, x1, y1 = g.bounds
                p = Point(random.uniform(x0, x1), random.uniform(y0, y1))
                if g.contains(p) and g.exterior.distance(p) > 0.00002:   # a más de ~2 m del borde
                    pts.append((p.y, p.x, cl))
            js = pg.evaluate("(pts) => pts.map(p => celdaUga(p[0], p[1]))", pts)
            buenos = sum(1 for a, b in zip(js, pts) if a == b[2])
            afirma(buenos == len(pts), 'la celda coincide con el polígono de la capa completa en %d de %d puntos' % (buenos, len(pts)))
        except ImportError:
            notas.append('OK  (sin shapely: se omite el cotejo contra los polígonos)')

    # ---------------- teléfono: la lista no desborda ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(300)
    escribe(pg, 'unidad habitacional')
    ancho = pg.evaluate("() => { const l = document.getElementById('lista_colonia').getBoundingClientRect(); return {der: l.right, vw: window.innerWidth, doc: document.documentElement.scrollWidth}; }")
    afirma(ancho['der'] <= ancho['vw'] and ancho['doc'] <= ancho['vw'], 'en teléfono la lista cabe en la pantalla (%.0f de %d px)' % (ancho['der'], ancho['vw']))

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
