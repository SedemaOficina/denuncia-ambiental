# -*- coding: utf-8 -*-
"""Pegar la ubicación: ayuda para quien no sabe sacar coordenadas y los
   formatos que el campo reconoce (DEC-122).

   Los tres primeros casos son los que mandó Liber Saltijeral, tal cual:
   un enlace completo de ficha de lugar, unas coordenadas con muchos
   decimales y un enlace corto de «Compartir».
   Lo que se vigila:
   1. En el enlace de ficha se toma el LUGAR (!3d…!4d), no el centro de la
      vista (@), que puede quedar a cientos de metros.
   2. Coordenadas en grados, minutos y segundos, con N/S y W/O.
   3. La longitud sin signo, dentro de la Ciudad, se corrige; fuera no.
   4. El enlace corto no se lee, y se dice qué hacer.
   5. La ayuda está plegada bajo el campo y enumera los mismos formatos."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina21.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

FICHA = ('https://www.google.com/maps/place/C.+Ahuacatitla,+Cd.+de+M%C3%A9xico/@19.2089226,-99.1665394,1603m/'
         'data=!3m1!1e3!4m15!1m8!3m7!1s0x85ce0705100fa113:0x44ccdfd73712af9b!2sC.+Ahuacatitla,+Cd.+de+M%C3%A9xico!3b1'
         '!8m2!3d19.2089176!4d-99.1639645!16s%2Fg%2F1tj1mvyn!3m5!1s0x85ce0705100fa113:0x44ccdfd73712af9b!8m2'
         '!3d19.2089176!4d-99.1639645!16s%2Fg%2F1tj1mvyn?entry=ttu&g_ep=EgoyMDI2MDkyNy4xIKXMDSoASAFQAw%3D%3D')
CASOS = [
  (FICHA, (19.2089176, -99.1639645), 'enlace de ficha de lugar (se toma el lugar, no el centro de la vista)'),
  ('19.209069554604078, -99.16396450220994', (19.209069554604078, -99.16396450220994), 'coordenadas con muchos decimales'),
  ('19°25\'57.4"N 99°07\'59.5"W', (19.432611, -99.133194), 'grados, minutos y segundos'),
  ('19° 25′ 57.4″ N, 99° 07′ 59.5″ O', (19.432611, -99.133194), 'con espacios, comillas tipográficas y O por oeste'),
  ('19.4326, 99.1332', (19.4326, -99.1332), 'longitud sin signo dentro de la Ciudad: se corrige'),
  ('https://www.google.com/maps/@19.2938,-99.1930,17z', (19.2938, -99.1930), 'enlace de vista de mapa (@)'),
]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    for texto, (la, lo), nombre in CASOS:
        r = pg.evaluate("t => leeCoordenadas(t)", texto)
        ok = r and abs(r['lat'] - la) < 1e-5 and abs(r['lon'] - lo) < 1e-5
        afirma(ok, '%s → %s' % (nombre, r))
    fuera = pg.evaluate("t => leeCoordenadas(t)", '40.4168, 3.7038')
    afirma(fuera and fuera['lon'] > 0, 'fuera de la Ciudad no se adivina el signo (%s)' % fuera)

    # enlace corto de Compartir: no se lee y se explica
    pg.evaluate("() => { estado={}; guarda('materia','rsu'); guarda('tiene_direccion','no'); irA(2); }"); pg.wait_for_timeout(300)
    corto = pg.evaluate("""() => { guarda('coord_pegar','https://maps.app.goo.gl/bxEUL12FPAbcRFq1A https://maps.app.goo.gl/bxEUL12FPAbcRFq1A');
      colocaPorTexto(); return {lee: leeCoordenadas(val('coord_pegar')), lat: val('lat'), txt: document.getElementById('resBusqueda').innerText}; }""")
    afirma(corto['lee'] is None and not corto['lat'], 'el enlace corto de Compartir no coloca un punto inventado')
    afirma('todavía no se puede resolver' in corto['txt'] and 'Abre el enlace' in corto['txt'], 'y dice qué hacer mientras tanto')

    # el enlace de ficha coloca el punto en el lugar
    fi = pg.evaluate("""(u) => { guarda('coord_pegar', u); colocaPorTexto(); return [val('lat'), val('lon')]; }""", FICHA)
    afirma(fi and abs(float(fi[0]) - 19.2089176) < 1e-5 and abs(float(fi[1]) + 99.1639645) < 1e-5,
           'pegado en el campo, el enlace de ficha coloca el punto en el lugar (%s)' % fi)

    # enlace de vista (solo «@»): coloca el punto y avisa que es el centro de la pantalla
    VISTA = 'https://www.google.com/maps/@19.2089226,-99.1665394,1603m/data=!3m1!1e3?entry=ttu&g_ep=EgoyMDI2MDkyNy4xIKXMDSoASAFQAw%3D%3D'
    vi = pg.evaluate("""(u) => { guarda('lat',''); guarda('coord_pegar', u); colocaPorTexto();
      return {lat: val('lat'), lon: val('lon'), txt: document.getElementById('resBusqueda').innerText}; }""", VISTA)
    afirma(abs(float(vi['lat']) - 19.2089226) < 1e-5 and abs(float(vi['lon']) + 99.1665394) < 1e-5,
           'el enlace de vista coloca el punto en el centro de la pantalla (%s, %s)' % (vi['lat'], vi['lon']))
    afirma('centro de la pantalla' in vi['txt'], 'y avisa que no es un lugar: hay que revisar el punto')
    fi2 = pg.evaluate("""(u) => { guarda('coord_pegar', u); colocaPorTexto(); return document.getElementById('resBusqueda').innerText; }""", FICHA)
    afirma('centro de la pantalla' not in fi2, 'con el enlace de ficha de lugar no hace falta ese aviso')

    # la ayuda
    ay = pg.evaluate("""() => { const d = document.querySelector('#c_coord_pegar ~ .como-ubicar, .vias .como-ubicar');
      if(!d) return null; const t = d.innerText;
      return {abierta: d.open, resumen: d.querySelector('summary').textContent, t: d.textContent}; }""")
    afirma(ay is not None and ay['abierta'] is False, 'bajo el campo hay una ayuda plegada')
    afirma(ay and 'Cómo copio' in ay['resumen'], 'que se anuncia como «%s»' % (ay or {}).get('resumen'))
    afirma(ay and 'Mantén el dedo' in ay['t'] and 'clic derecho' in ay['t'], 'explica el camino en teléfono y en computadora')
    afirma(ay and all(x in ay['t'] for x in ['19.4326, -99.1332', '°', 'google.com/maps', '+GJ', 'maps.app.goo.gl']),
           'y enumera los formatos que reconoce, y el que todavía no')

    # ---- guía visual (DEC-125) ----
    gv = pg.evaluate("""() => { const d = document.querySelector('.como-ubicar'); d.open = true;
      const tabs = [...d.querySelectorAll('.guia-tabs .btn-sn')].map(b => b.textContent);
      const vis = () => [...d.querySelectorAll('.guia-panel')].filter(p => !p.hidden).map(p => p.dataset.guia);
      const antes = vis(); const mapa = document.getElementById('mapa'); if(mapa) mapa.dataset.testigo = 'mismo';
      d.querySelectorAll('.guia-tabs .btn-sn')[2].click(); const despues = vis();
      const svgs = [...d.querySelectorAll('.guia-panel svg')];
      return {tabs, antes, despues, mismoMapa: !mapa || document.getElementById('mapa').dataset.testigo === 'mismo',
              nsvg: svgs.length, sinAria: svgs.filter(s => !s.getAttribute('aria-label')).length,
              pasos: d.querySelectorAll('.guia-panel .guia-paso').length,
              compartir: d.querySelector('.guia-panel[data-guia="compartir"]').innerText}; }""")
    afirma(gv['tabs'] == ['En el teléfono', 'En la computadora', 'Desde «Compartir»'], 'la guía se elige por dónde se usa Google Maps: %s' % gv['tabs'])
    afirma(gv['antes'] == ['tel'] and gv['despues'] == ['compartir'], 'se ve una guía a la vez, y cambiar de guía no rehace la pantalla')
    afirma(gv['mismoMapa'], 'ni reinicia el mapa')
    afirma(gv['nsvg'] == 9 and gv['sinAria'] == 0 and gv['pasos'] == 9, 'tres pasos ilustrados por guía, cada dibujo con su descripción (%d)' % gv['nsvg'])
    afirma('números de arriba' in gv['compartir'], 'la guía de «Compartir» dice copiar los números y no el enlace')
    pc = pg.evaluate("t => leeCoordenadas(t)", '6R5P+GJ Ciudad de México')
    afirma(pc and abs(pc['lat'] - 19.2088) < 0.0005 and abs(pc['lon'] + 99.1635) < 0.0005,
           'el código plus del ejemplo cae en el lugar de la ficha (%s)' % pc)
    pg.set_viewport_size({'width':390,'height':800})
    anch = pg.evaluate("() => ({doc: document.documentElement.scrollWidth, vw: window.innerWidth})")
    afirma(anch['doc'] <= anch['vw'], 'en teléfono la guía no desborda la pantalla (%s)' % anch)
    ph = pg.get_attribute('#f_coord_pegar', 'placeholder')
    afirma(ph and '19.4326' in ph, 'el campo muestra un ejemplo: %r' % ph)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
