# -*- coding: utf-8 -*-
"""Datos accesorios del lugar, geolocalizacion con encuadre propio y recorrido
   completo sin errores de consola.

   El bloque nació plegado (DEC-44) y dejó de estarlo (DEC-51): al fundirse los
   dos campos de referencias en uno, bajó de siete campos a tres, y a ese tamaño
   esconderlos costaba más de lo que ahorraba. Lo que se conserva de aquella
   decisión es que «opcional» se dice una vez en el encabezado y no campo por
   campo. Estas comprobaciones siguen el cambio; no se borran."""
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

    # --- 1. Los campos accesorios son parte de la direccion ---
    pos = pg.evaluate("""() => {
      const yy = id => { const e=document.getElementById(id); return e? Math.round(e.getBoundingClientRect().top+window.scrollY):null; };
      const m = document.getElementById('mapa');
      return {cp: yy('f_cp'), e1: yy('f_entre_calle1'), refs: yy('f_referencias'),
              mapa: m ? Math.round(m.getBoundingClientRect().top+window.scrollY) : null,
              cajas: document.querySelectorAll('.bloque-opcional, .enc-opcional, .cuerpo-opcional').length,
              campos: ['entre_calle1','entre_calle2','referencias'].map(k=>!!document.getElementById('f_'+k))};
    }""")
    afirma(all(pos['campos']), 'los tres campos accesorios estan a la vista: %s' % pos['campos'])
    afirma(pos['cajas'] == 0, 'no quedan cajas ni encabezados de bloque plegable (%d)' % pos['cajas'])
    afirma(pos['cp'] < pos['e1'] < pos['refs'] < pos['mapa'],
           'van despues del codigo postal y antes del mapa: CP %s < entre calles %s < como se reconoce %s < mapa %s'
           % (pos['cp'], pos['e1'], pos['refs'], pos['mapa']))

    # --- 2. Aqui «opcional» si distingue, y por eso se marca ---
    marcas = pg.evaluate("""() => {
      const prev = cfg.validar; cfg.validar = true; render();
      const r = ['calle','entre_calle1','referencias'].map(k => {
        const c = document.getElementById('c_'+k);
        return c ? (c.innerText.toLowerCase().includes('opcional') ? 'opcional' : 'obligatorio') : 'ausente';
      });
      cfg.validar = prev; render();
      return r;
    }""")
    afirma(marcas == ['obligatorio','opcional','opcional'],
           'la calle se pide y los accesorios se marcan opcionales: %s' % marcas)

    # --- 3. Lo capturado se conserva al volver al paso ---
    pg.fill('#f_referencias', 'Frente a la escuela primaria')
    pg.evaluate("irA(1)"); pg.wait_for_timeout(250)
    pg.evaluate("irA(2)"); pg.wait_for_timeout(300)
    afirma(pg.input_value('#f_referencias') == 'Frente a la escuela primaria',
           'el dato capturado sobrevive a salir y volver al paso')

    # --- 4. Ninguno es obligatorio cuando hay direccion ---
    oblig = pg.evaluate("ks => ks.filter(k => OBLIG[k] && esObligatorio(k))",
                        ['entre_calle1','entre_calle2','referencias'])
    afirma(oblig == [], 'con direccion, ninguno es obligatorio (lo son: %s)' % oblig)

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
