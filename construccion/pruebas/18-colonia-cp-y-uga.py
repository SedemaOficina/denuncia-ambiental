# -*- coding: utf-8 -*-
"""La alcaldía y la colonia de la dirección, el código postal y la celda UGA (DEC-117, DEC-118).

   Alcaldía y colonia. La alcaldía de la dirección se elige de un desplegable
   y la colonia sugiere sólo las de esa alcaldía, del catálogo del IECM 2022
   (DEC-118). Lo que se vigila:
   1. Que sea un combobox de verdad: rol, lista enlazada, teclado.
   2. Que la búsqueda ignore acentos y encuentre por cualquier palabra.
   3. Que la alcaldía acote de verdad, y que cambiarla suelte la colonia.
   4. Que la alcaldía escrita NO decida el turnado (DEC-72): si no coincide
      con la del punto, se avisa y el expediente lo marca.
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
      .map(li => ({nom: li.querySelector('.op-nom').textContent, alc: (li.querySelector('.op-alc') || {}).textContent || ''}))""")

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

    # ---------------- la alcaldía de la dirección (DEC-118) ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(400)
    c = pg.evaluate("""() => { const s = document.getElementById('f_alcaldia_dir'), i = document.getElementById('f_colonia');
      const ops = [...s.options].map(o => o.value).filter(Boolean);
      const orden = [...document.querySelectorAll('#app .campo')].map(e => e.id);
      return {ops, primera: ops[0], dis: i.disabled, ph: i.getAttribute('placeholder'),
              antes: orden.indexOf('c_alcaldia_dir') < orden.indexOf('c_colonia'), oblig: esObligatorio('alcaldia_dir')}; }""")
    afirma(len(c['ops']) == 16 and c['primera'] == 'Álvaro Obregón',
           'la alcaldía se elige de un desplegable con las 16, en orden alfabético (%s primero)' % c['primera'])
    afirma(c['antes'] and c['oblig'], 'va antes que la colonia y es obligatoria con dirección')
    afirma(c['dis'] and 'alcaldía' in (c['ph'] or ''), 'sin alcaldía, la colonia está deshabilitada y lo dice: «%s»' % c['ph'])

    def alcaldia(nombre):
        pg.select_option('#f_alcaldia_dir', nombre); pg.wait_for_timeout(120)

    alcaldia('Coyoacán')
    c = pg.evaluate("""() => { const i = document.getElementById('f_colonia'), l = document.getElementById('lista_colonia');
      return {rol: i.getAttribute('role'), ctrl: i.getAttribute('aria-controls'), exp: i.getAttribute('aria-expanded'),
              auto: i.getAttribute('autocomplete'), lista: l && l.getAttribute('role'), oculta: l && l.hidden, dis: i.disabled}; }""")
    afirma(not c['dis'], 'al elegir la alcaldía, la colonia se habilita sin rehacer la pantalla')
    afirma(c['rol'] == 'combobox' and c['ctrl'] == 'lista_colonia' and c['lista'] == 'listbox',
           'la colonia es un combobox enlazado a su lista')
    afirma(c['exp'] == 'false' and c['oculta'], 'la lista empieza cerrada')
    afirma(c['auto'] == 'off', 'el autocompletado del navegador no se encima con el del catálogo')

    escribe(pg, 'c')
    afirma(opciones(pg) == [], 'con una sola letra no se sugiere nada')
    escribe(pg, 'chimal')
    ops = opciones(pg)
    fuera = pg.evaluate("""(noms) => noms.filter(n => !CATALOGO_COLONIAS.filas.some(r => r[0] === n && CATALOGO_COLONIAS.alcaldias[r[1]] === 'Coyoacán'))""",
                        [o['nom'] for o in ops])
    afirma(ops and fuera == [], 'sólo se sugieren colonias de la alcaldía elegida (%d, ninguna de otra)' % len(ops))
    afirma(pg.evaluate("() => document.querySelectorAll('#lista_colonia .op-alc').length") == 0,
           'y sin repetir la alcaldía en cada renglón, porque todas son de la misma')
    afirma(pg.get_attribute('#f_colonia', 'aria-expanded') == 'true', 'al sugerir, el campo anuncia la lista abierta')
    total = pg.evaluate("""() => { guarda('alcaldia_dir',''); const n = sugiereColonias('chimal', 50).length; guarda('alcaldia_dir','Coyoacán'); return n; }""")
    afirma(total > len(ops), 'sin el filtro habría más (%d contra %d): la alcaldía sí acota' % (total, len(ops)))

    # acentos y varias palabras, con la alcaldía de cada caso
    caso = pg.evaluate("""() => { const f = CATALOGO_COLONIAS.filas, A = CATALOGO_COLONIAS.alcaldias;
      const a = f.find(r => /Juárez/.test(r[0])), b = f.find(r => /Pedregal de San Nicolás/.test(r[0]));
      return {a: A[a[1]], b: A[b[1]]}; }""")
    alcaldia(caso['a']); escribe(pg, 'juarez')
    afirma(any('Juárez' in o['nom'] for o in opciones(pg)), 'la búsqueda ignora acentos: «juarez» encuentra «Juárez» (%s)' % caso['a'])
    alcaldia(caso['b']); escribe(pg, 'pedregal nicolas')
    ops = opciones(pg)
    afirma(ops and all('Pedregal' in o['nom'] and 'Nicolás' in o['nom'] for o in ops),
           'y encuentra por varias palabras (%s)' % (ops[0]['nom'] if ops else '—'))
    alcaldia('Coyoacán'); escribe(pg, 'u hab')
    afirma(len(opciones(pg)) > 0, 'también por la abreviatura con que la escribe el IECM')

    # teclado
    escribe(pg, 'chimal')
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(80)
    act = pg.evaluate("() => { const i=document.getElementById('f_colonia'); const id=i.getAttribute('aria-activedescendant'); const li=id&&document.getElementById(id); return {id, sel: li && li.getAttribute('aria-selected'), nom: li && li.querySelector('.op-nom').textContent}; }")
    afirma(act['id'] and act['sel'] == 'true', 'la flecha marca la primera sugerencia sin sacar el foco del campo')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
    el = pg.evaluate("() => ({col: val('colonia'), cve: val('colonia_cve'), alc: val('colonia_alcaldia'), cerr: document.getElementById('lista_colonia').hidden, inp: document.getElementById('f_colonia').value})")
    afirma(el['col'] == act['nom'] and el['inp'] == act['nom'] and el['cve'] and el['alc'] == 'Coyoacán' and el['cerr'],
           'Enter la elige: %s, clave %s, y la lista se cierra' % (el['col'], el['cve']))
    pg.keyboard.type('x'); pg.wait_for_timeout(80)
    afirma(pg.evaluate("() => val('colonia_cve')") == '', 'si se sigue escribiendo, la clave elegida se suelta')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(60)
    afirma(pg.evaluate("() => document.getElementById('lista_colonia').hidden"), 'Escape cierra la lista')

    # clic
    alcaldia('Benito Juárez'); escribe(pg, 'narvarte')
    pg.click('#lista_colonia li[role=option] >> nth=0'); pg.wait_for_timeout(120)
    afirma(pg.evaluate("() => !!val('colonia_cve') && /Narvarte/.test(val('colonia'))"), 'un clic sobre la sugerencia también la elige')

    # cambiar de alcaldía suelta la colonia elegida, no la escrita a mano
    alcaldia('Coyoacán')
    afirma(pg.evaluate("() => val('colonia') === '' && val('colonia_cve') === '' && document.getElementById('f_colonia').value === ''"),
           'cambiar de alcaldía borra la colonia elegida de la otra')
    escribe(pg, 'Colonia Zyxwv Inventada')
    vac = pg.evaluate("() => { const v = document.querySelector('#lista_colonia .combo-vacio'); return v ? v.textContent : ''; }")
    afirma('Coyoacán' in vac and 'como la escribiste' in vac, 'si no hay coincidencias, lo dice con la alcaldía: «%s»' % vac)
    pg.evaluate("() => document.getElementById('f_colonia').blur()"); pg.wait_for_timeout(120)
    fl = pg.evaluate("() => ({col: val('colonia'), cve: val('colonia_cve')})")
    afirma(fl['col'] == 'Colonia Zyxwv Inventada' and fl['cve'] == '', 'y se conserva igual, sin clave')
    alcaldia('Tlalpan')
    afirma(pg.evaluate("() => val('colonia')") == 'Colonia Zyxwv Inventada', 'lo escrito a mano sobrevive al cambio de alcaldía')

    # escrito sin elegir: se reconoce dentro de la alcaldía elegida
    dup = pg.evaluate("""() => { const f = CATALOGO_COLONIAS.filas, A = CATALOGO_COLONIAS.alcaldias, c = {};
      f.forEach(r => { (c[r[0]] = c[r[0]] || []).push(A[r[1]]); });
      const n = Object.keys(c).find(n => c[n].length > 1); return {n, a: c[n][c[n].length-1]}; }""")
    alcaldia(dup['a']); escribe(pg, dup['n'])
    pg.evaluate("() => document.getElementById('f_colonia').blur()"); pg.wait_for_timeout(120)
    rec = pg.evaluate("() => ({cve: val('colonia_cve'), alc: val('colonia_alcaldia')})")
    afirma(rec['cve'] and rec['alc'] == dup['a'],
           'un nombre repetido escrito sin elegir se reconoce en la alcaldía elegida («%s», %s)' % (dup['n'], rec['alc']))

    # ---------------- la alcaldía de la dirección frente a la del punto ----------------
    pg.evaluate(PREP); pg.wait_for_timeout(300)
    alcaldia('Coyoacán')
    pg.evaluate("([a,b]) => ponMarcador(a,b)", list(PUNTO)); pg.wait_for_timeout(400)
    alcP = pg.evaluate("() => val('alcaldia')")
    afirma(alcP == 'Coyoacán', 'el punto de prueba cae en %s' % alcP)
    afirma(pg.evaluate("() => document.getElementById('avisoColonia').textContent.trim()") == '' and
           pg.evaluate("() => val('alcaldia_discrepa')") == '', 'si coinciden, no hay aviso ni marca')
    alcaldia('Tlalpan')
    av = pg.evaluate("() => ({t: document.getElementById('avisoColonia').textContent, alc: val('alcaldia'), m: val('alcaldia_discrepa')})")
    afirma('Tlalpan' in av['t'] and 'Coyoacán' in av['t'], 'si no coinciden, se avisa con las dos alcaldías')
    afirma(av['alc'] == 'Coyoacán', 'y la que decide el turnado sigue siendo la del punto (DEC-72)')
    afirma(av['m'] == 'si', 'el expediente lleva la marca de la diferencia')
    afirma('límite' in av['t'], 'el aviso admite que cerca del límite puede no haber error')
    pg.evaluate("() => valida(2)"); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => !document.querySelector('#c_alcaldia_dir.invalido')"),
           'el aviso no bloquea: al continuar, la alcaldía no se marca como error')
    pg.evaluate("([a,b]) => ponMarcador(a,b)", [19.2600, -99.1900]); pg.wait_for_timeout(300)
    da, pa = pg.evaluate("() => [val('alcaldia_dir'), val('alcaldia')]")
    t = pg.evaluate("() => document.getElementById('avisoColonia').textContent")
    afirma((da == pa) == (t.strip() == ''), 'al mover el punto, el aviso se recalcula (%s / %s)' % (da, pa))

    # la búsqueda de la dirección usa la alcaldía escrita y no los paréntesis
    q = pg.evaluate("""() => { estado = {}; guarda('tiene_direccion','si');
      guarda('calle','Calle 5'); guarda('alcaldia_dir','Coyoacán'); guarda('colonia','Copilco Universidad (Unidad Habitacional)'); guarda('cp','04360');
      return consultaDireccion(); }""")
    afirma('Coyoacán' in q and '(' not in q, 'la búsqueda de la dirección lleva la alcaldía y no los paréntesis: «%s»' % q)

    # los escenarios del panel no se contradicen
    esc = pg.evaluate("""() => ESCENARIOS.filter(e => e.e && e.e.alcaldia_dir && e.e.lat).map(e => {
      const c = consultaCapas(+e.e.lat, +e.e.lon);
      const enCat = CATALOGO_COLONIAS.filas.some(r => r[0] === e.e.colonia && CATALOGO_COLONIAS.alcaldias[r[1]] === e.e.alcaldia_dir);
      return {id: e.id, dir: e.e.alcaldia_dir, punto: c.alcaldia, enCat}; })""")
    malos = [e for e in esc if e['dir'] != e['punto'] or not e['enCat']]
    afirma(len(esc) >= 4 and malos == [], 'los %d escenarios con dirección son coherentes: colonia del catálogo y misma alcaldía que su punto %s' % (len(esc), malos))

    # ---------------- código postal ----------------
    def cp(k, v):
        return pg.evaluate("([k,v]) => { guarda(k,v); avisaFormato(k); return {mal: formatoMal(k), msg: msgFormato(k)}; }", [k, v])
    afirma(not cp('cp', '06010')['mal'], 'un código postal de la Ciudad se acepta (06010)')
    afirma(not cp('cp', '16035')['mal'] and not cp('cp', '01000')['mal'], 'también en los extremos del intervalo (01000, 16035)')
    r = cp('cp', '1234');  afirma(r['mal'] and 'cinco dígitos' in r['msg'], 'cuatro dígitos: «%s»' % r['msg'])
    r = cp('cp', '55000'); afirma(r['mal'] and 'no es de la Ciudad' in r['msg'], 'cinco dígitos de otra entidad: «%s»' % r['msg'])
    r = cp('cp', '00100'); afirma(r['mal'], 'y 00100 tampoco')
    afirma(cp('dom_cp', '55000')['mal'], 'el del domicilio de la persona también debe ser de la Ciudad (DEC-135)')
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
    pg.select_option('#f_alcaldia_dir', 'Iztapalapa'); pg.wait_for_timeout(120)
    escribe(pg, 'unidad habitacional')
    ancho = pg.evaluate("() => { const l = document.getElementById('lista_colonia').getBoundingClientRect(); return {der: l.right, vw: window.innerWidth, doc: document.documentElement.scrollWidth}; }")
    afirma(ancho['der'] <= ancho['vw'] and ancho['doc'] <= ancho['vw'], 'en teléfono la lista cabe en la pantalla (%.0f de %d px)' % (ancho['der'], ancho['vw']))

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
