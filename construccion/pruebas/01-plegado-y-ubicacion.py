# -*- coding: utf-8 -*-
"""Pruebas del bloque B: plegado de campos accesorios, geolocalización
   con encuadre propio, y recorrido completo sin errores de consola."""
import os, pathlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
import json, sys

HTML = '<!doctype html><html lang="es"><head><meta charset="utf-8">' + RUTA.read_text(encoding='utf-8') + '</body></html>'
TMP.write_text(HTML, encoding='utf-8')

fallos, notas = [], []
def afirma(cond, msg):
    (notas if cond else fallos).append(('OK  ' if cond else 'FALLA ') + msg)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width':390,'height':844})
    pg = ctx.new_page()
    errores = []
    EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
    def es_propio(t): return not any(x in t for x in EXTERNO)
    pg.on('console', lambda m: errores.append(m.text) if m.type=='error' and es_propio(m.text) else None)
    pg.on('pageerror', lambda e: errores.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri())
    pg.wait_for_timeout(700)

    # --- Llegar al paso 2 ---
    pg.evaluate("guarda('materia','residuos'); guarda('resp_tipo','desconocido'); guarda('tiene_direccion','si'); irA(2)")
    pg.wait_for_timeout(400)
    afirma(pg.locator('#app').inner_text().find('Dónde') >= 0 or pg.locator('h2').first.inner_text() != '', 'paso 2 renderiza')

    # --- 1. El bloque nace plegado ---
    enc = pg.locator('.enc-opcional')
    afirma(enc.count() == 1, 'existe un solo encabezado plegable')
    afirma(enc.get_attribute('aria-expanded') == 'false', 'el bloque nace plegado (aria-expanded=false)')
    afirma(pg.locator('.cuerpo-opcional').count() == 0, 'plegado: el cuerpo no está en el DOM')
    afirma(pg.locator('#entre_calle1').count() == 0, 'plegado: los campos accesorios no están en el DOM')

    # --- 2. Abre y cierra ---
    enc.click(); pg.wait_for_timeout(300)
    afirma(pg.locator('.enc-opcional').get_attribute('aria-expanded') == 'true', 'abierto: aria-expanded=true')
    afirma(pg.locator('.cuerpo-opcional').count() == 1, 'abierto: el cuerpo aparece')
    for c in ['entre_calle1','entre_calle2','referencias']:
        afirma(pg.locator('#f_'+c).count() == 1, 'abierto: aparece '+c)
    afirma(pg.locator('.cuerpo-opcional .opc:visible').count() == 0, 'dentro del bloque no se repite la palabra «opcional»')

    # la etiqueta del encabezado lo dice una sola vez
    afirma('opcional' in pg.locator('.enc-opcional').inner_text().lower(), 'el encabezado declara que todo es opcional')

    pg.locator('.enc-opcional').click(); pg.wait_for_timeout(300)
    afirma(pg.locator('.cuerpo-opcional').count() == 0, 'vuelve a plegarse')

    # --- 3. Lo plegado conserva su valor ---
    pg.locator('.enc-opcional').click(); pg.wait_for_timeout(250)
    pg.fill('#f_referencias', 'Frente a la escuela primaria')
    pg.locator('.enc-opcional').click(); pg.wait_for_timeout(250)
    pg.locator('.enc-opcional').click(); pg.wait_for_timeout(250)
    afirma(pg.input_value('#f_referencias') == 'Frente a la escuela primaria', 'el dato capturado sobrevive al plegado')
    pg.locator('.enc-opcional').click(); pg.wait_for_timeout(200)

    # --- 4. Ningún campo obligatorio quedó dentro del bloque ---
    envueltos = ['entre_calle1','entre_calle2','fachada','referencias','es_estab','tipo_estab','nombre_estab']
    oblig = pg.evaluate("ks => ks.filter(k => OBLIG[k] && esObligatorio(k))", envueltos)
    afirma(oblig == [], 'ningún campo plegado es obligatorio (obligatorios dentro: %s)' % oblig)

    # --- 4 bis. La red de seguridad: si alguno llegara a ser obligatorio, el bloque se abre ---
    tiene_red = pg.evaluate("() => valida.toString().indexOf('ENVUELTOS_LUGAR') >= 0")
    afirma(tiene_red, 'valida() conserva la red que despliega el bloque si falta un campo de dentro')
    # La obligatoriedad depende del esquema activo (vigente / dgiva): se marcan
    # las dos banderas para que la prueba no dependa de cuál esté seleccionado.
    # Se usa entre_calle1, que vive dentro del bloque y no tiene condicion propia,
    # para que la prueba mida la red y no la condicion de otro campo.
    forzado = pg.evaluate("""() => {
        guarda('tiene_direccion','si'); guarda('mas_lugar','');
        const prev = {v: OBLIG.entre_calle1.vigente, d: OBLIG.entre_calle1.dgiva, validar: cfg.validar};
        OBLIG.entre_calle1.vigente = true; OBLIG.entre_calle1.dgiva = true;
        cfg.validar = true;
        guarda('entre_calle1','');
        const paso = valida(2);
        const abierto = val('mas_lugar');
        OBLIG.entre_calle1.vigente = prev.v; OBLIG.entre_calle1.dgiva = prev.d; cfg.validar = prev.validar;
        return {paso: paso, abierto: abierto, esquema: cfg.esquema};
    }""")
    afirma(forzado['paso'] is False and forzado['abierto'] == 'si',
           'si un campo de dentro fuera obligatorio y faltara, valida() frena y despliega el bloque (%s)' % json.dumps(forzado))
    pg.evaluate("guarda('mas_lugar',''); render()"); pg.wait_for_timeout(200)

    # --- 5. «Los hechos ocurren donde estoy ahora» ---
    enlace = pg.locator('button.enlace', has_text='donde estoy ahora')
    afirma(enlace.count() == 1, 'el enlace de geolocalización está presente')
    afirma(pg.locator('button:has-text("Ubicar en el mapa")').count() == 0,
           'en el artefacto no queda el botón que requiere servicio de geocodificación')

    # degradación: sin permiso de ubicación debe avisar, no romper
    enlace.click(); pg.wait_for_timeout(1200)
    txt = pg.locator('#resBusqueda').inner_text()
    afirma(len(txt.strip()) > 0, 'sin permiso de ubicación se muestra un mensaje, no un vacío: «%s»' % txt.strip()[:70])

    # con permiso concedido: coloca el punto y reencuadra
    ctx2 = nav.new_context(viewport={'width':390,'height':844},
                           geolocation={'latitude':19.3579,'longitude':-99.1610},
                           permissions=['geolocation'], locale='es-MX')
    p2 = ctx2.new_page()
    err2 = []
    p2.on('pageerror', lambda e: err2.append(str(e)))
    p2.on('console', lambda m: err2.append(m.text) if m.type=='error' and es_propio(m.text) else None)
    p2.goto(TMP.as_uri()); p2.wait_for_timeout(700)
    p2.evaluate("guarda('materia','residuos'); guarda('resp_tipo','desconocido'); guarda('tiene_direccion','si'); irA(2)")
    p2.wait_for_timeout(400)
    vista_antes = p2.evaluate("() => VISTA && VISTA.w")
    p2.locator('button.enlace', has_text='donde estoy ahora').click()
    p2.wait_for_timeout(1500)
    lat = p2.evaluate("() => val('lat')")
    vista_dsp = p2.evaluate("() => VISTA && VISTA.w")
    afirma(lat != '' and abs(float(lat) - 19.3579) < 0.001, 'con permiso, el punto queda en la ubicación devuelta (lat=%s)' % lat)
    afirma(vista_dsp is not None and vista_antes is not None and vista_dsp < vista_antes,
           'el mapa vectorial se acerca al punto (ancho %s -> %s)' % (vista_antes, vista_dsp))
    afirma(p2.evaluate("() => val('alcaldia')") == '', 'el punto NO escribe la alcaldía de la dirección')
    afirma(p2.evaluate("() => val('alcaldia_punto')") != '', 'el punto sí registra la alcaldía que le corresponde')
    afirma(err2 == [], 'sin errores en el recorrido con geolocalización: %s' % err2[:3])
    ctx2.close()

    # --- 6. Recorrido completo de los 6 pasos ---
    pg.evaluate("""() => {
      ['materia','resp_tipo'].forEach(k=>guarda(k,''));
      guarda('materia','residuos'); guarda('zona_tipo','urbano'); irA(1);
    }""")
    for n in range(1, 8):
        pg.evaluate("irA(%d)" % n); pg.wait_for_timeout(250)
        afirma(pg.locator('#app').inner_html().strip() != '', 'el paso %d renderiza contenido' % n)

    # --- 7. La barra de progreso navega ---
    pg.evaluate("irA(3)"); pg.wait_for_timeout(250)
    afirma(pg.locator('#progreso [aria-current="step"]').count() == 1, 'la barra marca un solo paso vigente')
    afirma(pg.locator('.barra-fija').count() == 1, 'la barra fija sigue presente')

    afirma(errores == [], 'sin errores de consola en el recorrido principal: %s' % errores[:3])
    nav.close()

print('\n'.join(notas))
print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
