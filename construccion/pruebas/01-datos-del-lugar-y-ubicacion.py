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
      return {cp: yy('f_cp'), e1: yy('f_entre_calles'), refs: yy('f_referencias'),
              mapa: m ? Math.round(m.getBoundingClientRect().top+window.scrollY) : null,
              cajas: document.querySelectorAll('.bloque-opcional, .enc-opcional, .cuerpo-opcional').length,
              campos: ['entre_calles','referencias'].map(k=>!!document.getElementById('f_'+k))};
    }""")
    afirma(all(pos['campos']), 'los tres campos accesorios estan a la vista: %s' % pos['campos'])
    afirma(pos['cajas'] == 0, 'no quedan cajas ni encabezados de bloque plegable (%d)' % pos['cajas'])
    afirma(pos['cp'] < pos['e1'] < pos['refs'] < pos['mapa'],
           'van despues del codigo postal y antes del mapa: CP %s < entre calles %s < como se reconoce %s < mapa %s'
           % (pos['cp'], pos['e1'], pos['refs'], pos['mapa']))

    # --- 2. Aqui «opcional» si distingue, y por eso se marca ---
    marcas = pg.evaluate("""() => {
      const prev = cfg.validar; cfg.validar = true; render();
      const r = ['calle','entre_calles','referencias'].map(k => {
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
                        ['entre_calles','referencias'])
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
    # DEC-72 invierte la regla anterior: la alcaldia ya no se escribe, la
    # determina el punto. Antes habia dos -la escrita y la calculada-, el
    # turnado usaba una y el acuse mostraba la otra, y podia enviarse una
    # denuncia que dijera Coyoacan y se turnara como Tlalpan.
    afirma(r['alc'] == 'Tlalpan', 'el punto determina la alcaldia (%s)' % r['alc'])
    coherente = pg.evaluate("""() => {
      guarda('calle','Av. Mexico'); guarda('num_ext','10');
      guarda('colonia','Del Carmen'); guarda('cp','04100');
      guarda('tiene_direccion','si');
      ponMarcador(19.2938, -99.1930);
      irA(6);
      const dts = [...document.querySelectorAll('.resumen dt')].map(e => e.textContent.replace('Editar','').trim());
      const dds = [...document.querySelectorAll('.resumen dd')].map(e => e.textContent.trim());
      const o = {}; dts.forEach((k,i) => o[k] = dds[i]);
      irA(2);
      return {lugar: o['Lugar de los hechos'], alc: val('alcaldia'),
              hayCampoAlcaldia: !!document.getElementById('f_alcaldia')};
    }""")
    pg.wait_for_timeout(300)
    afirma(not coherente['hayCampoAlcaldia'], 'la alcaldia ya no se pregunta')
    afirma(coherente['alc'] in coherente['lugar'],
           'el resumen usa la MISMA alcaldia con la que se turna: «%s» contiene «%s»'
           % (coherente['lugar'], coherente['alc']))

    aviso = pg.evaluate("""() => { guarda('coord_pegar','https://maps.app.goo.gl/AbCdEf'); colocaPorTexto();
        return document.getElementById('resBusqueda').innerText.trim(); }""")
    # El aviso cambio con DEC-82: ya no solo explica el problema, ofrece la
    # salida. Lo que no puede perderse es que el enlace no trae la coordenada.
    afirma('No lleva la coordenada dentro' in aviso,
           'un enlace corto se explica en vez de fallar en silencio')
    afirma('servidor de la Secretar\u00eda' in aviso,
           'y dice qui\u00e9n lo resolver\u00e1, en vez de dejar ah\u00ed a la persona')
    afirma(peticiones == [], 'leer el enlace no genera ninguna peticion de red: %s' % peticiones[:2])
    pg.evaluate("guarda('coord_pegar',''); guarda('lat',''); guarda('lon',''); render()")

    # --- 5 bis. Pegar la ubicacion coloca el punto (DEC-92) ---
    # Habia un boton «Colocar ese punto»: pegar ya es el gesto de «coloca
    # esto», y pedir despues un clic era pedir dos veces lo mismo.
    r = pg.evaluate("""() => {
      cfg.validar = true; guarda('tiene_direccion','no'); guarda('lat',''); guarda('lon',''); irA(2);
      const boton = [...document.querySelectorAll('#app button')]
                      .some(b => b.textContent.indexOf('Colocar ese punto') >= 0);
      guarda('coord_pegar','19.2938, -99.1930'); colocaPorTexto();
      return {boton, lat: val('lat'), lon: val('lon'), alcaldia: val('alcaldia')};
    }""")
    pg.wait_for_timeout(400)
    afirma(r['boton'] is False, 'ya no hay boton de colocar el punto')
    afirma(r['lat'] != '' and r['lon'] != '', 'pegar la ubicacion coloca el punto')
    afirma('Tlalpan' in (r['alcaldia'] or ''), 'y el cruce responde solo: %s' % r['alcaldia'])

    # Lo que no se reconoce no se reprocha: el aviso desaparece (DEC-93).
    r = pg.evaluate("""() => {
      guarda('coord_pegar','no se que poner aqui'); colocaPorTexto();
      const c = document.getElementById('resBusqueda');
      return {texto: c ? c.innerText.trim() : null};
    }""")
    afirma(r['texto'] == '', 'lo que no se reconoce no deja aviso: %r' % r['texto'])

    # La casilla de confirmacion se retiro por ruido (DEC-93). Lo que no puede
    # perderse es lo que ella decia: que al mover el punto la persona vea, sin
    # hacer nada, a que alcaldia y a que area acaba de mandar su denuncia.
    r3 = pg.evaluate("""() => {
      guarda('tiene_direccion','si'); irA(2); ponMarcador(19.2938, -99.1930);
      const uno = (document.getElementById('panelCapas')||{}).innerText || '';
      ponMarcador(19.4326, -99.1332);
      const dos = (document.getElementById('panelCapas')||{}).innerText || '';
      return {uno: uno.replace(/\\s+/g,' '), dos: dos.replace(/\\s+/g,' '),
              casilla: !!document.getElementById('c_punto_confirmado')};
    }""")
    pg.wait_for_timeout(400)
    afirma(not r3['casilla'], 'ya no se pide confirmar el punto con una casilla')
    afirma('Tlalpan' in r3['uno'], 'la ficha del cruce dice donde cayo el punto: «%s»' % r3['uno'][:70])
    afirma(r3['dos'] != r3['uno'], 'y se actualiza sola al mover el punto')
    afirma('Cuauht' in r3['dos'] or 'Cuauhtémoc' in r3['dos'],
           'con la alcaldia nueva: «%s»' % r3['dos'][:70])
    pg.evaluate("guarda('lat',''); guarda('lon',''); guarda('tiene_direccion','si'); guarda('coord_pegar',''); render()")
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
