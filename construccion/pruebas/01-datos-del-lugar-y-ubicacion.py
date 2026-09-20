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
        if(!c) return 'ausente';
        const t = c.innerText;
        if(t.toLowerCase().includes('opcional')) return 'DICE OPCIONAL';
        return c.querySelector('.req') ? 'obligatorio' : 'opcional';
      });
      cfg.validar = prev; render();
      return r;
    }""")
    afirma(marcas == ['obligatorio','opcional','opcional'],
           'la calle lleva asterisco y los accesorios no llevan marca: %s' % marcas)

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

    # --- 5. Coordenadas o enlace de mapa pegados (DEC-67, DEC-69) ---
    # La deteccion de ubicacion del dispositivo se retiro por completo: el
    # formulario no debe pedir ese permiso ni tocar esa API. En su lugar, la
    # persona pega lo que ya tiene, y el enlace se LEE aqui, sin salir a la red.
    afirma(pg.locator('button.enlace', has_text='donde estoy ahora').count() == 0,
           'no queda el boton que pedia la ubicacion del dispositivo')
    afirma(pg.evaluate("() => typeof estoyEnElLugar") == 'undefined',
           'la funcion de geolocalizacion se elimino')
    afirma(pg.evaluate("() => document.documentElement.outerHTML.indexOf('navigator.geolocation') < 0"),
           'el codigo ya no menciona la API de geolocalizacion')
    afirma(pg.locator('#f_coord_pegar').count() == 1,
           'existe el campo para pegar coordenadas o un enlace de mapa')

    peticiones = []
    pg.on('request', lambda r: peticiones.append(r.url) if ('google' in r.url or 'goo.gl' in r.url) else None)

    casos = [('19.3579, -99.1610', True), ('19.3579 -99.1610', True),
             ('https://www.google.com/maps/@19.2938,-99.1930,17z', True),
             ('https://www.google.com/maps?q=19.4326,-99.1332', True),
             ('https://www.google.com/maps/place/X/@19.2938,-99.1930,17z/data=!3d19.2938!4d-99.1930', True),
             ('https://maps.app.goo.gl/AbCdEf', False),
             ('Avenida Chapultepec 440', False), ('', False)]
    for t, esperado in casos:
        r = pg.evaluate("t => leeCoordenadas(t)", t)
        afirma((r is not None) == esperado,
               'se %s coordenada en «%s»' % ('lee' if esperado else 'rechaza', (t[:46] or '(vacío)')))

    r = pg.evaluate("""() => { ['lat','lon'].forEach(k=>guarda(k,''));
        guarda('coord_pegar','https://www.google.com/maps/@19.2938,-99.1930,17z'); colocaPorTexto();
        return {lat: val('lat'), capa: val('capa_nombre'), alc: val('alcaldia')}; }""")
    pg.wait_for_timeout(400)
    afirma(r['lat'] != '' and abs(float(r['lat']) - 19.2938) < 0.001,
           'pegar un enlace de Google Maps coloca el punto (lat=%s)' % r['lat'])
    afirma(r['capa'] == 'Bosque de Tlalpan', 'y el cruce con las capas se resuelve sobre ese punto (%s)' % r['capa'])
    afirma(r['alc'] == '', 'el punto pegado NO escribe la alcaldia de la direccion')

    aviso = pg.evaluate("""() => { guarda('coord_pegar','https://maps.app.goo.gl/AbCdEf'); colocaPorTexto();
        return document.getElementById('resBusqueda').innerText.trim(); }""")
    afirma('cortos' in aviso, 'un enlace corto se explica en vez de fallar en silencio')
    afirma(peticiones == [], 'leer el enlace no genera ninguna peticion de red: %s' % peticiones[:2])
    pg.evaluate("guarda('coord_pegar',''); quitaPunto()")

    # --- 5 bis. Confirmacion del punto (DEC-70) ---
    # El punto se arrastra, y un roce basta para moverlo. Se pide confirmarlo, y
    # cualquier movimiento posterior borra la confirmacion: si sobreviviera al
    # movimiento, pedirla no serviria de nada.
    r = pg.evaluate("""() => {
      cfg.validar = true; guarda('tiene_direccion','no'); quitaPunto(); irA(2);
      const sinPunto = !!document.getElementById('f_punto_confirmado');
      guarda('coord_pegar','19.2938, -99.1930'); colocaPorTexto();
      return {sinPunto, conPunto: !!document.getElementById('f_punto_confirmado'),
              marcada: (document.getElementById('f_punto_confirmado')||{}).checked};
    }""")
    pg.wait_for_timeout(400)
    afirma(r['sinPunto'] is False, 'sin punto no se pide confirmarlo')
    afirma(r['conPunto'] is True and r['marcada'] is False,
           'al colocar el punto aparece la casilla, sin marcar')

    r2 = pg.evaluate("""() => {
      guarda('nombre_lugar','Bosque de Tlalpan'); guarda('referencias','Puerta 3');
      const sinConfirmar = valida(2);
      guarda('punto_confirmado','si');
      const confirmado = valida(2);
      ponMarcador(19.31, -99.20);
      const tras = val('punto_confirmado');
      const casilla = (document.getElementById('f_punto_confirmado')||{}).checked;
      const bloquea = valida(2);
      return {sinConfirmar, confirmado, tras, casilla, bloquea};
    }""")
    afirma(r2['sinConfirmar'] is False, 'sin confirmar el punto, el paso no avanza')
    afirma(r2['confirmado'] is True, 'confirmado, el paso avanza')
    afirma(r2['tras'] == '' and r2['casilla'] is False,
           'mover el punto borra la confirmacion y destilda la casilla')
    afirma(r2['bloquea'] is False, 'y vuelve a frenar el paso hasta confirmar de nuevo')
    pg.evaluate("quitaPunto(); guarda('tiene_direccion','si'); guarda('coord_pegar',''); render()")
    pg.wait_for_timeout(250)

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
