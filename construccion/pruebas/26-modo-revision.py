# -*- coding: utf-8 -*-
"""Modo revisión para la DGIVA (DEC-153, DEC-155).

   Una sola liga, ?revision=<palabra>, abre un panel para dejar observaciones
   que llegan a una hoja de Google por su Apps Script. Cada quien escribe su
   nombre la primera vez. Se vigila que:
   1. Sin la liga de revisión no se pinta nada.
   2. Con ella aparece «Observar»; pide el nombre antes de todo y lo recuerda.
   3. Se señala un elemento o un texto seleccionado y la observación
      registra quién, pantalla, sección y texto.
   4. Sin la hoja se guarda en el navegador, sobrevive a recargar y se
      descarga en CSV.
   5. Conectada, manda a la hoja lo que el Apps Script espera, muestra las
      observaciones de todo el equipo con su estado y su respuesta, y filtra
      las propias; si la hoja falla, no se pierde nada.
   6. El Apps Script (revision/Codigo.gs) valida la palabra de la liga, exige
      nombre, no duplica un reintento y neutraliza fórmulas.
   La hoja real nunca se toca: toda llamada a script.google.com se intercepta."""
import os, pathlib, sys, json, subprocess, shutil, re
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina26.html'
GS   = RAIZ.parent / 'revision' / 'Codigo.gs'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
FUENTE = RUTA.read_text(encoding='utf-8')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' + FUENTE + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
LIGA = '?revision=k7pmq4xz2abc'
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

m = re.search(r"endpoint: '([^']*)'", FUENTE)
afirma(bool(m) and (m.group(1) == '' or bool(re.match(r'^https://script\.google\.com/macros/s/[\w-]+/exec$', m.group(1)))),
       'la URL de la hoja es la de un Apps Script o está vacía')
afirma('PALABRA' not in FUENTE and 'k7pmq4xz2abc' not in FUENTE, 'la palabra de la liga no está escrita en el formulario')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width':1200,'height':900}, accept_downloads=True)
    modo = {'hoja': 'caida'}
    recibidos = []
    def hoja(route):
        req = route.request
        if modo['hoja'] == 'caida': return route.abort()
        if modo['hoja'] == 'vencida':
            return route.fulfill(status=200, content_type='application/json', body='{"ok":false,"error":"clave"}')
        if req.method == 'POST':
            d = json.loads(req.post_data); recibidos.append(d)
            return route.fulfill(status=200, content_type='application/json',
                                 body=json.dumps({'ok': True, 'id': 'OBS-%04d' % len(recibidos)}))
        return route.fulfill(status=200, content_type='application/json',
            body=json.dumps({'ok': True, 'observaciones': [
              {'id': 'OBS-0009', 'creada': '2026-09-30T18:00:00Z', 'revisor': 'Luis Colega', 'pantalla': 'Paso 2 · Dónde ocurrió',
               'seccion': 'Dirección', 'texto': 'Colonia', 'tipo': 'Duda', 'observacion': '¿Acepta colonias nuevas?',
               'propuesta': '', 'estado': 'Atendida', 'respuesta': 'Sí, con texto libre.'},
              {'id': 'OBS-0010', 'creada': '2026-09-30T18:05:00Z', 'revisor': 'ana prueba', 'pantalla': 'Portada',
               'seccion': '', 'texto': '', 'tipo': 'Otro', 'observacion': 'Una mía de antes', 'propuesta': '',
               'estado': 'Pendiente', 'respuesta': ''}]}))
    ctx.route('https://script.google.com/**', hoja)
    pg = ctx.new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))

    # ---- 1. Sin liga, nada ----
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    afirma(pg.evaluate("() => !document.getElementById('revision') && REVISION.palabra === ''"), 'sin ?revision= no aparece el modo revisión')
    pg.goto(TMP.as_uri() + '?revision=abc'); pg.wait_for_timeout(500)
    afirma(pg.evaluate("() => !document.getElementById('revision')"), 'una palabra de menos de cuatro caracteres no lo abre')

    # ---- 2. Con la liga: primero el nombre ----
    pg.goto(TMP.as_uri() + LIGA); pg.wait_for_timeout(700)
    pg.evaluate("""() => { try{ localStorage.removeItem('sedema.revision.obs'); localStorage.removeItem('sedema.revision.quien'); }catch(e){}
      REVISION.obs = []; REVISION.nombre = ''; REVISION.endpoint = ''; pintaRevision(); }""")
    afirma(pg.is_visible('#revision .rev-toggle'), 'con ?revision= aparece el botón «Observar»')
    afirma(pg.evaluate("() => REVISION.palabra") == 'k7pmq4xz2abc', 'la palabra de la liga se toma tal cual')
    caja = pg.evaluate("() => { const b = document.querySelector('#revision .rev-toggle').getBoundingClientRect(); const p = document.querySelector('#panel .toggle').getBoundingClientRect(); return {b: [b.left, b.right], p: [p.left, p.right]}; }")
    afirma(caja['b'][1] < caja['p'][0], 'no se encima con el botón del panel de validación')
    pg.click('#revision .rev-toggle'); pg.wait_for_timeout(150)
    afirma(pg.is_visible('#revNombre') and not pg.is_visible('#revObs'), 'antes de observar pide el nombre')
    pg.click('text=Empezar a revisar'); pg.wait_for_timeout(100)
    afirma(pg.is_visible('#revNombre') and 'Escribe tu nombre' in pg.inner_text('#revMsg'), 'sin nombre no deja empezar')
    pg.fill('#revNombre', '  Ana   Prueba '); pg.fill('#revArea', 'DGIVA')
    pg.click('text=Empezar a revisar'); pg.wait_for_timeout(150)
    t = pg.inner_text('#revCuerpo')
    afirma('Ana Prueba · DGIVA' in t and pg.is_visible('#revObs'), 'con el nombre abre la observación y lo muestra: «%s»' % t[:60])
    afirma('Portada' in t and 'Toda la pantalla' in t, 'el panel dice la pantalla y que no hay parte señalada')
    afirma('aún no está conectada' in t, 'y avisa que, sin hoja, se guarda en el navegador')

    # ---- 3. Señalar ----
    pg.click('text=Señalar en pantalla'); pg.wait_for_timeout(150)
    afirma(pg.is_visible('#revAviso') and not pg.is_visible('#revCuerpo'), 'al señalar se cierra el panel y aparece la indicación')
    pg.hover('text=¿Qué necesitas?'); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => !!document.querySelector('.rev-foco')"), 'lo que está bajo el puntero se resalta')
    pag0 = pg.evaluate("() => paso")
    pg.click('text=¿Qué necesitas?'); pg.wait_for_timeout(200)
    afirma(pg.evaluate("() => paso") == pag0 and pg.is_visible('#revCuerpo'), 'el clic de señalar no activa nada del formulario y reabre el panel')
    s = pg.evaluate("() => REVISION.senal")
    afirma(bool(s) and s['texto'] == '¿Qué necesitas?' and 'h2' in s['elemento'] and 'div#app' in s['elemento'],
           'registra el texto y el elemento señalados: %s' % s)
    afirma(not pg.evaluate("() => !!document.querySelector('.rev-foco, #revAviso')"), 'y limpia el resaltado')
    pg.click('.rev-tipos button:has-text("Quitar")'); pg.wait_for_timeout(100)
    pg.fill('#revObs', 'Sobra el signo; revisar el tono.')
    pg.fill('#revProp', '¿Qué necesitas para denunciar?')
    pg.click('text=Guardar observación'); pg.wait_for_timeout(200)
    o = pg.evaluate("() => REVISION.obs[0]")
    afirma(bool(o) and o['revisor'] == 'Ana Prueba' and o['area'] == 'DGIVA' and o['pantalla'] == 'Portada' and o['tipo'] == 'Quitar'
           and o['texto'] == '¿Qué necesitas?' and o['propuesta'] == '¿Qué necesitas para denunciar?' and o['version'].startswith('DEC-'),
           'la observación guarda quién, pantalla, tipo, texto señalado, propuesta y versión')
    afirma(bool(o) and o['estado'] == 'Guardada en este navegador' and 'Guardada en este navegador' in pg.inner_text('#revMsg'),
           'sin hoja queda «Guardada en este navegador»')
    afirma(pg.inner_text('#revCuenta').strip() == '· 1', 'el botón cuenta las observaciones propias')
    afirma(pg.evaluate("() => REVISION.borrador.obs === '' && REVISION.senal === null"), 'y el formulario de observación queda limpio')
    pg.click('text=Guardar observación'); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => REVISION.obs.length") == 1 and 'Escribe la observación' in pg.inner_text('#revMsg'), 'sin texto no se guarda')

    pg.evaluate("() => { cargaEscenario('urbano'); irA(3); }"); pg.wait_for_timeout(300)
    pg.evaluate("""() => { const h = [...document.querySelectorAll('#app h3')].find(x => x.textContent.indexOf('Quién lo está haciendo') >= 0);
      const r = document.createRange(); r.selectNodeContents(h); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }""")
    pg.wait_for_timeout(100)
    pg.click('#revision .rev-toggle'); pg.wait_for_timeout(100)
    pg.click('#revision .rev-toggle'); pg.wait_for_timeout(150)
    t = pg.inner_text('#revCuerpo')
    afirma('Paso 3' in t and '¿Quién lo está haciendo?' in t, 'un texto seleccionado se toma como la parte señalada, con su paso')
    pg.fill('#revObs', 'Con «=» al inicio: =HYPERLINK("x")')
    pg.click('text=Guardar observación'); pg.wait_for_timeout(150)
    pg.evaluate("() => abrePrivacidad()"); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => revPantalla()") == 'Ventana · Aviso de privacidad', 'si hay una ventana abierta, la pantalla es esa ventana')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

    # ---- 4. Persiste y se descarga ----
    pg.reload(); pg.wait_for_timeout(700)
    pg.evaluate("() => { REVISION.endpoint = ''; pintaRevision(); }")
    afirma(pg.evaluate("() => REVISION.obs.length") == 2, 'lo guardado en el navegador sobrevive a recargar')
    afirma(pg.evaluate("() => REVISION.nombre") == 'Ana Prueba', 'y el nombre también: no se vuelve a pedir')
    pg.click('#revision .rev-toggle'); pg.click('.rev-pestanas button:has-text("Observaciones")'); pg.wait_for_timeout(150)
    lista = pg.inner_text('#revCuerpo')
    afirma('Sin enviar' in lista and 'Sobra el signo' in lista and 'Ana Prueba' in lista, '«Observaciones» las muestra con su autora')
    with pg.expect_download() as d:
        pg.click('text=Descargar en CSV')
    ruta = AQUI / '_observaciones26.csv'; d.value.save_as(ruta)
    csv = ruta.read_text(encoding='utf-8-sig'); ruta.unlink()
    afirma(d.value.suggested_filename == 'observaciones-revision.csv', 'el CSV se descarga')
    afirma(csv.startswith('"ID","Fecha","Revisor"') and 'Sobra el signo' in csv and 'Ana Prueba' in csv, 'y trae encabezados, autora y observaciones')

    # ---- 5. Conectada a una hoja simulada ----
    modo['hoja'] = 'viva'
    pg.evaluate("() => { REVISION.endpoint = 'https://script.google.com/macros/s/PRUEBA/exec'; return revConecta(); }"); pg.wait_for_timeout(600)
    afirma(len(recibidos) == 2 and all(r['accion'] == 'guardar' and r['palabra'] == 'k7pmq4xz2abc' for r in recibidos),
           'al conectarse manda a la hoja lo que estaba en el navegador, con la palabra de la liga (%d)' % len(recibidos))
    afirma(bool(recibidos) and all(k in recibidos[0]['obs'] for k in ('uid','revisor','area','pantalla','seccion','texto','tipo','observacion','propuesta','version','paso')),
           'con los campos que el Apps Script espera')
    afirma(pg.evaluate("() => { try{ return JSON.parse(localStorage.getItem('sedema.revision.obs')).length; }catch(e){ return -1; } }") == 0,
           'y ya enviadas, el navegador deja de guardarlas')
    pg.click('.rev-pestanas button:has-text("Observaciones")'); pg.wait_for_timeout(150)
    lista = pg.inner_text('#revCuerpo')
    afirma('se guardan en la hoja' in lista, 'dice que está conectada')
    afirma('Luis Colega' in lista and 'Atendida' in lista and 'Sí, con texto libre.' in lista, 'muestra las del equipo, con estado y respuesta de la Secretaría')
    afirma(pg.evaluate("() => document.querySelector('.rev-edo-ok') !== null"), 'la atendida lleva su color')
    pg.check('.rev-filtro input'); pg.wait_for_timeout(100)
    lista = pg.inner_text('#revCuerpo')
    afirma('Luis Colega' not in lista and 'Una mía de antes' in lista, '«Sólo las mías» filtra por nombre, sin importar mayúsculas')

    pg.click('text=Nueva observación'); pg.fill('#revObs', 'Una más'); pg.click('text=Guardar observación'); pg.wait_for_timeout(400)
    afirma(len(recibidos) == 3 and 'OBS-0003' in pg.inner_text('#revMsg'), 'una nueva se envía al momento y dice su ID')

    modo['hoja'] = 'caida'
    pg.fill('#revObs', 'Sin red'); pg.click('text=Guardar observación'); pg.wait_for_timeout(400)
    afirma('No se pudo enviar' in pg.inner_text('#revMsg') and
           pg.evaluate("() => JSON.parse(localStorage.getItem('sedema.revision.obs')).length") == 1,
           'si la hoja no responde, la observación se queda en el navegador')
    modo['hoja'] = 'vencida'
    pg.evaluate("() => revConecta()"); pg.wait_for_timeout(400)
    afirma('ya no está vigente' in pg.inner_text('#revCuerpo'), 'una liga reemplazada se avisa')

    pg.click('.rev-cab .rev-link'); pg.wait_for_timeout(100)
    afirma(pg.is_visible('#revNombre'), '«Cambiar» vuelve a pedir el nombre')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    afirma(not pg.is_visible('#revCuerpo'), 'Escape cierra el panel')

    # ---- Teléfono ----
    ph = ctx.new_page(); ph.set_viewport_size({'width': 390, 'height': 800})
    ph.goto(TMP.as_uri() + LIGA); ph.wait_for_timeout(600)
    ph.click('#revision .rev-toggle'); ph.wait_for_timeout(150)
    bx = ph.evaluate("() => { const r = document.getElementById('revCuerpo').getBoundingClientRect(); return [r.left, r.right, document.documentElement.scrollWidth]; }")
    afirma(bx[0] >= 0 and bx[1] <= 390 and bx[2] <= 390, 'en teléfono el panel cabe en la pantalla: %s' % bx)

    afirma(not err, 'sin errores propios en consola: %s' % err[:3])
    nav.close()

# ---- 6. El Apps Script, contra una hoja simulada ----
NODE = shutil.which('node')
if not GS.exists():
    afirma(False, 'existe revision/Codigo.gs')
elif not NODE:
    notas.append('NOTA sin node: no se simula el Apps Script')
else:
    SIM = r"""
const fs = require('fs'); const vm = require('vm');
function Hoja(){ this.d = []; }
Hoja.prototype.getLastRow = function(){ return this.d.length; };
Hoja.prototype.appendRow = function(f){ this.d.push(f.slice()); };
Hoja.prototype.getRange = function(r, c, nr, nc){ const h = this; return {
  getValues(){ return h.d.slice(r-1, r-1+nr).map(f => f.slice(c-1, c-1+nc).map(v => v === undefined ? '' : v)); },
  getValue(){ return h.d[r-1][c-1]; },
  createTextFinder(t){ return { matchEntireCell(){ return this; }, findNext(){
    for(let i = 0; i < nr; i++) if(String(h.d[r-1+i][c-1]) === t) return { getRow(){ return r+i; } }; return null; } }; } }; };
const obs = new Hoja(); obs.d = [['ID']];
const props = {};
const ctx = {
  SpreadsheetApp: { getActive: () => ({ getSheetByName: n => n === 'Observaciones' ? obs : null }) },
  PropertiesService: { getScriptProperties: () => ({ getProperty: k => props[k] || null, setProperty: (k, v) => { props[k] = v; } }) },
  LockService: { getScriptLock: () => ({ waitLock(){}, releaseLock(){} }) },
  Utilities: { formatDate: (d) => d.toISOString().slice(0,10).replace(/-/g,'') },
  ContentService: { MimeType: { JSON: 'json' }, createTextOutput: t => ({ setMimeType(){ return t; } }) },
  Logger: { log(){} }, console
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], 'utf8'), ctx);
const post = o => JSON.parse(ctx.doPost({ postData: { contents: JSON.stringify(o) } }));
const get = p => JSON.parse(ctx.doGet({ parameter: p }));
const r = {};
r.sinLiga = post({ accion: 'guardar', palabra: '', obs: { revisor: 'Ana', observacion: 'x' } });
props.PALABRA = 'k7pmq4xz2abc';
r.malaPalabra = post({ accion: 'guardar', palabra: 'otra-palabra', obs: { revisor: 'Ana', observacion: 'x' } });
r.sinNombre = post({ accion: 'guardar', palabra: 'k7pmq4xz2abc', obs: { revisor: ' ', observacion: 'x' } });
r.vacia = post({ accion: 'guardar', palabra: 'k7pmq4xz2abc', obs: { revisor: 'Ana Prueba', observacion: '  ' } });
r.uno = post({ accion: 'guardar', palabra: 'k7pmq4xz2abc', obs: { uid: 'u1', revisor: '  Ana   Prueba ', area: 'DGIVA', observacion: '=HYPERLINK("x")', tipo: 'Quitar', pantalla: 'Portada' } });
r.repetida = post({ accion: 'guardar', palabra: 'k7pmq4xz2abc', obs: { uid: 'u1', revisor: 'Ana Prueba', observacion: 'otra vez' } });
r.dos = post({ accion: 'guardar', palabra: 'k7pmq4xz2abc', obs: { uid: 'u2', revisor: 'Luis', observacion: 'De otro' } });
r.filas = obs.d.length - 1;
r.formula = obs.d[1][11];
r.estado = obs.d[1][15];
r.revisor = obs.d[1][2];
r.lista = get({ accion: 'lista', palabra: 'k7pmq4xz2abc' });
r.listaMala = get({ accion: 'lista', palabra: 'nada' });
r.accion = get({});
console.log(JSON.stringify(r));
"""
    sim = AQUI / '_simula26.js'; sim.write_text(SIM, encoding='utf-8')
    p = subprocess.run([NODE, str(sim), str(GS)], capture_output=True, text=True, timeout=30)
    sim.unlink()
    if p.returncode != 0:
        afirma(False, 'el Apps Script corre en la simulación: %s' % p.stderr[-400:])
    else:
        r = json.loads(p.stdout)
        afirma(r['sinLiga']['error'] == 'clave', 'Apps Script: sin liga generada no acepta nada')
        afirma(r['malaPalabra'] == {'ok': False, 'error': 'clave'}, 'Apps Script: rechaza una liga que no es la vigente')
        afirma(r['sinNombre']['error'] == 'nombre' and r['vacia']['error'] == 'vacia', 'Apps Script: exige nombre y observación')
        afirma(r['uno'] == {'ok': True, 'id': 'OBS-0001'} and r['dos']['id'] == 'OBS-0002', 'Apps Script: numera OBS-0001, OBS-0002')
        afirma(r['repetida'].get('repetida') and r['repetida']['id'] == 'OBS-0001' and r['filas'] == 2, 'Apps Script: un reintento con el mismo uid no se duplica')
        afirma(r['formula'].startswith("'="), 'Apps Script: un texto que empieza con = no se vuelve fórmula')
        afirma(r['estado'] == 'Pendiente' and r['revisor'] == 'Ana Prueba', 'Apps Script: la fila nace Pendiente y con el nombre limpio')
        afirma(len(r['lista']['observaciones']) == 2 and 'uid' not in r['lista']['observaciones'][0], 'Apps Script: lista las de todo el equipo, sin el identificador interno')
        afirma(r['listaMala']['error'] == 'clave' and r['accion']['error'] == 'accion', 'Apps Script: sin la liga vigente o sin acción no entrega nada')

TMP.unlink(missing_ok=True)
print('\n'.join(notas))
if fallos:
    print('\n'.join(fallos)); print('\n%d FALLAS' % len(fallos)); sys.exit(1)
print('\nTODAS LAS PRUEBAS PASAN (%d)' % len(notas))
