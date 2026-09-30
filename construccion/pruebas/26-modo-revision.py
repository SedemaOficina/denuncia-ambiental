# -*- coding: utf-8 -*-
"""Modo revisión para la DGIVA (DEC-153).

   Una liga con ?revision=CLAVE abre un panel para dejar observaciones que
   llegan a una hoja de Google por su Apps Script. Se vigila que:
   1. Sin la clave en la liga no se pinta nada.
   2. Con la clave aparece «Observar»; se señala un elemento o un texto
      seleccionado y la observación registra pantalla, sección y texto.
   3. Sin la hoja conectada se guarda en el navegador, sobrevive a recargar
      y se descarga en CSV.
   4. Conectada, manda a la hoja lo que el Apps Script espera y muestra el
      estado y la respuesta que la hoja devuelve; si la hoja falla, no se
      pierde nada.
   5. El Apps Script (revision/Codigo.gs) valida la clave, no duplica un
      reintento, neutraliza fórmulas y sólo lista lo de cada quien."""
import os, pathlib, sys, json, subprocess, shutil
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
FALSO = 'https://script.google.com/macros/s/PRUEBA/exec'
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

afirma("endpoint: ''" in FUENTE or 'endpoint: \'https://script.google.com/' in FUENTE,
       'la URL de la hoja es la del Apps Script o está vacía')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width':1200,'height':900}, accept_downloads=True)
    pg = ctx.new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))

    # ---- 1. Sin clave, nada ----
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    afirma(pg.evaluate("() => !document.getElementById('revision') && REVISION.clave === ''"), 'sin ?revision= no aparece el modo revisión')
    pg.goto(TMP.as_uri() + '?revision=abc'); pg.wait_for_timeout(500)
    afirma(pg.evaluate("() => !document.getElementById('revision')"), 'una clave de menos de cuatro caracteres no lo abre')

    # ---- 2. Con clave, sin hoja ----
    pg.goto(TMP.as_uri() + '?revision=k7pm-4xq2'); pg.wait_for_timeout(700)
    pg.evaluate("() => { try{ localStorage.removeItem('sedema.revision.K7PM-4XQ2'); }catch(e){} REVISION.obs = []; pintaRevision(); }")
    afirma(pg.is_visible('#revision .rev-toggle'), 'con ?revision= aparece el botón «Observar»')
    afirma(pg.evaluate("() => REVISION.clave") == 'K7PM-4XQ2', 'la clave se toma en mayúsculas')
    caja = pg.evaluate("() => { const b = document.querySelector('#revision .rev-toggle').getBoundingClientRect(); const p = document.querySelector('#panel .toggle').getBoundingClientRect(); return {b: [b.left, b.right], p: [p.left, p.right]}; }")
    afirma(caja['b'][1] < caja['p'][0], 'no se encima con el botón del panel de validación')
    pg.click('#revision .rev-toggle'); pg.wait_for_timeout(150)
    t = pg.inner_text('#revCuerpo')
    afirma('Portada' in t and 'Toda la pantalla' in t, 'el panel dice la pantalla y que no hay parte señalada')
    afirma('aún no está conectada' in t, 'y avisa que, sin hoja, se guarda en el navegador')

    # Señalar un elemento de la portada
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
    pg.click('#revCuerpo button:has-text("Quitar")'); pg.wait_for_timeout(100)
    pg.fill('#revObs', 'Sobra el signo; revisar el tono.')
    pg.fill('#revProp', '¿Qué necesitas para denunciar?')
    pg.click('text=Guardar observación'); pg.wait_for_timeout(200)
    o = pg.evaluate("() => REVISION.obs[0]")
    afirma(o and o['pantalla'] == 'Portada' and o['tipo'] == 'Quitar' and o['texto'] == '¿Qué necesitas?'
           and o['propuesta'] == '¿Qué necesitas para denunciar?' and o['version'].startswith('DEC-'),
           'la observación guarda pantalla, tipo, texto señalado, propuesta y versión')
    afirma(o and o['estado'] == 'Guardada en este navegador' and 'Guardada en este navegador' in pg.inner_text('#revMsg'),
           'sin hoja queda «Guardada en este navegador»')
    afirma(pg.inner_text('#revCuenta').strip() == '· 1', 'el botón cuenta las observaciones')
    afirma(pg.evaluate("() => REVISION.borrador.obs === '' && REVISION.senal === null"), 'y el formulario de observación queda limpio')

    # Vacía no se guarda
    pg.click('text=Guardar observación'); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => REVISION.obs.length") == 1 and 'Escribe la observación' in pg.inner_text('#revMsg'), 'sin texto no se guarda')

    # Texto seleccionado en un campo del paso 3
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

    # Ventana del aviso de privacidad
    pg.evaluate("() => abrePrivacidad()"); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => revPantalla()") == 'Ventana · Aviso de privacidad', 'si hay una ventana abierta, la pantalla es esa ventana')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

    # ---- 3. Persiste y se descarga ----
    pg.reload(); pg.wait_for_timeout(700)
    afirma(pg.evaluate("() => REVISION.obs.length") == 2, 'lo guardado en el navegador sobrevive a recargar')
    pg.click('#revision .rev-toggle'); pg.click('text=Mis observaciones'); pg.wait_for_timeout(150)
    lista = pg.inner_text('#revCuerpo')
    afirma('Sin enviar' in lista and 'Sobra el signo' in lista, '«Mis observaciones» las muestra')
    with pg.expect_download() as d:
        pg.click('text=Descargar en CSV')
    ruta = AQUI / '_observaciones26.csv'; d.value.save_as(ruta)
    csv = ruta.read_text(encoding='utf-8-sig'); ruta.unlink()
    afirma(d.value.suggested_filename == 'observaciones-K7PM-4XQ2.csv', 'el CSV lleva la clave en el nombre')
    afirma(csv.startswith('"ID","Fecha"') and 'Sobra el signo' in csv, 'y trae encabezados y observaciones')
    afirma('"Con «=» al inicio' in csv, 'un texto que no empieza con signo se deja igual')

    # ---- 4. Conectada a una hoja simulada ----
    recibidos = []
    def hoja(route):
        req = route.request
        if req.method == 'POST':
            d = json.loads(req.post_data); recibidos.append(d)
            route.fulfill(status=200, content_type='application/json',
                          body=json.dumps({'ok': True, 'id': 'OBS-%04d' % len(recibidos)}))
        else:
            route.fulfill(status=200, content_type='application/json', headers={'Access-Control-Allow-Origin': '*'},
                          body=json.dumps({'ok': True, 'revisor': {'nombre': 'Ana Prueba', 'area': 'DGIVA', 'veTodas': False},
                                           'observaciones': [{'id': 'OBS-0009', 'creada': '2026-09-30T18:00:00Z', 'pantalla': 'Paso 2 · Dónde ocurrió',
                                                              'seccion': 'Dirección', 'texto': 'Colonia', 'tipo': 'Duda', 'observacion': '¿Acepta colonias nuevas?',
                                                              'propuesta': '', 'estado': 'Atendida', 'respuesta': 'Sí, con texto libre.'}]}))
    pg.route(FALSO + '**', hoja)
    pg.evaluate("(u) => { REVISION.endpoint = u; return revConecta(); }", FALSO); pg.wait_for_timeout(600)
    afirma(len(recibidos) == 2 and all(r['accion'] == 'guardar' and r['clave'] == 'K7PM-4XQ2' for r in recibidos),
           'al conectarse manda a la hoja lo que estaba en el navegador (%d)' % len(recibidos))
    afirma(recibidos and all(k in recibidos[0]['obs'] for k in ('uid','pantalla','seccion','texto','tipo','observacion','propuesta','version','paso')),
           'con los campos que el Apps Script espera')
    afirma(pg.evaluate("() => { try{ return JSON.parse(localStorage.getItem('sedema.revision.K7PM-4XQ2')).length; }catch(e){ return -1; } }") == 0,
           'y ya enviadas, el navegador deja de guardarlas')
    pg.click('text=Mis observaciones'); pg.wait_for_timeout(150)
    lista = pg.inner_text('#revCuerpo')
    afirma('Ana Prueba' in lista and 'se guardan en la hoja' in lista, 'muestra quién revisa y que está conectada')
    afirma('Atendida' in lista and 'Sí, con texto libre.' in lista, 'y el estado y la respuesta que puso la Secretaría')
    afirma(pg.evaluate("() => document.querySelector('.rev-edo-ok') !== null"), 'la atendida lleva su color')

    pg.click('text=Nueva observación'); pg.fill('#revObs', 'Una más'); pg.click('text=Guardar observación'); pg.wait_for_timeout(400)
    afirma(len(recibidos) == 3 and 'OBS-0003' in pg.inner_text('#revMsg'), 'una nueva se envía al momento y dice su ID')

    pg.unroute(FALSO + '**')
    pg.route(FALSO + '**', lambda r: r.abort())
    pg.fill('#revObs', 'Sin red'); pg.click('text=Guardar observación'); pg.wait_for_timeout(400)
    afirma('No se pudo enviar' in pg.inner_text('#revMsg') and
           pg.evaluate("() => JSON.parse(localStorage.getItem('sedema.revision.K7PM-4XQ2')).length") == 1,
           'si la hoja no responde, la observación se queda en el navegador')
    pg.unroute(FALSO + '**')
    pg.route(FALSO + '**', lambda r: r.fulfill(status=200, content_type='application/json', body='{"ok":false,"error":"clave"}'))
    pg.evaluate("() => revConecta()"); pg.wait_for_timeout(400)
    afirma('no está registrada o fue desactivada' in pg.inner_text('#revCuerpo'), 'una clave desactivada se avisa')

    # Escape cierra el panel
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    afirma(not pg.is_visible('#revCuerpo'), 'Escape cierra el panel')

    # ---- Teléfono ----
    ph = ctx.new_page(); ph.set_viewport_size({'width': 390, 'height': 800})
    ph.goto(TMP.as_uri() + '?revision=K7PM-4XQ2'); ph.wait_for_timeout(600)
    ph.click('#revision .rev-toggle'); ph.wait_for_timeout(150)
    bx = ph.evaluate("() => { const r = document.getElementById('revCuerpo').getBoundingClientRect(); return [r.left, r.right, document.documentElement.scrollWidth]; }")
    afirma(bx[0] >= 0 and bx[1] <= 390 and bx[2] <= 390, 'en teléfono el panel cabe en la pantalla: %s' % bx)

    afirma(not err, 'sin errores propios en consola: %s' % err[:3])
    nav.close()

# ---- 5. El Apps Script, contra una hoja simulada ----
NODE = shutil.which('node')
if not GS.exists():
    afirma(False, 'existe revision/Codigo.gs')
elif not NODE:
    notas.append('NOTA sin node: no se simula el Apps Script')
else:
    SIM = r"""
const fs = require('fs'); const vm = require('vm');
function Hoja(nombre){ this.nombre = nombre; this.d = []; }
Hoja.prototype.getLastRow = function(){ return this.d.length; };
Hoja.prototype.appendRow = function(f){ this.d.push(f.slice()); };
Hoja.prototype.getRange = function(r, c, nr, nc){ const h = this; return {
  getValues(){ return h.d.slice(r-1, r-1+nr).map(f => f.slice(c-1, c-1+nc).map(v => v === undefined ? '' : v)); },
  getValue(){ return h.d[r-1][c-1]; },
  createTextFinder(t){ return { matchEntireCell(){ return this; }, findNext(){
    for(let i = 0; i < nr; i++) if(String(h.d[r-1+i][c-1]) === t) return { getRow(){ return r+i; } }; return null; } }; } }; };
const libro = { Observaciones: new Hoja('Observaciones'), Revisores: new Hoja('Revisores') };
libro.Revisores.d = [['Clave','Nombre','Área','Activa','Ve todas','Liga'],
  ['K7PM-4XQ2','Ana Prueba','DGIVA','Sí','No',''], ['AB12-CD34','Luis Baja','DGIVA','No','No',''], ['ZZZZ-9999','Coord','DGIVA','Sí','Sí','']];
libro.Observaciones.d = [['ID']];
const ctx = {
  SpreadsheetApp: { getActive: () => ({ getSheetByName: n => libro[n] }) },
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
r.malaClave = post({ accion: 'guardar', clave: 'NO00-0000', obs: { observacion: 'x' } });
r.inactiva = post({ accion: 'guardar', clave: 'AB12-CD34', obs: { observacion: 'x' } });
r.vacia = post({ accion: 'guardar', clave: 'K7PM-4XQ2', obs: { observacion: '  ' } });
r.uno = post({ accion: 'guardar', clave: 'k7pm-4xq2', obs: { uid: 'u1', observacion: '=HYPERLINK("x")', tipo: 'Quitar', pantalla: 'Portada' } });
r.repetida = post({ accion: 'guardar', clave: 'K7PM-4XQ2', obs: { uid: 'u1', observacion: 'otra vez' } });
r.dos = post({ accion: 'guardar', clave: 'ZZZZ-9999', obs: { uid: 'u2', observacion: 'De coordinación' } });
r.filas = libro.Observaciones.d.length - 1;
r.formula = libro.Observaciones.d[1][12];
r.estado = libro.Observaciones.d[1][16];
r.revisor = libro.Observaciones.d[1][3];
r.listaAna = get({ accion: 'lista', clave: 'K7PM-4XQ2' });
r.listaCoord = get({ accion: 'lista', clave: 'ZZZZ-9999' });
r.listaMala = get({ accion: 'lista', clave: 'NO00-0000' });
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
        afirma(r['malaClave'] == {'ok': False, 'error': 'clave'} and r['inactiva']['error'] == 'clave', 'Apps Script: rechaza una clave inexistente o desactivada')
        afirma(r['vacia']['error'] == 'vacia', 'Apps Script: rechaza una observación vacía')
        afirma(r['uno'] == {'ok': True, 'id': 'OBS-0001'} and r['dos']['id'] == 'OBS-0002', 'Apps Script: numera OBS-0001, OBS-0002')
        afirma(r['repetida'].get('repetida') and r['repetida']['id'] == 'OBS-0001' and r['filas'] == 2, 'Apps Script: un reintento con el mismo uid no se duplica')
        afirma(r['formula'].startswith("'="), 'Apps Script: un texto que empieza con = no se vuelve fórmula')
        afirma(r['estado'] == 'Pendiente' and r['revisor'] == 'Ana Prueba', 'Apps Script: la fila nace Pendiente y con el nombre del revisor, no el que mande el navegador')
        afirma(len(r['listaAna']['observaciones']) == 1 and r['listaAna']['revisor']['nombre'] == 'Ana Prueba', 'Apps Script: cada quien ve sólo lo suyo')
        afirma(len(r['listaCoord']['observaciones']) == 2 and r['listaCoord']['revisor']['veTodas'], 'Apps Script: quien «ve todas» ve las de todos')
        afirma(r['listaMala']['error'] == 'clave' and r['accion']['error'] == 'accion', 'Apps Script: sin clave válida o sin acción no entrega nada')

TMP.unlink(missing_ok=True)
print('\n'.join(notas))
if fallos:
    print('\n'.join(fallos)); print('\n%d FALLAS' % len(fallos)); sys.exit(1)
print('\nTODAS LAS PRUEBAS PASAN (%d)' % len(notas))
