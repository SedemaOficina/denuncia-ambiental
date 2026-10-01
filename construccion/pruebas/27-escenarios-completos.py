# -*- coding: utf-8 -*-
"""Los escenarios de prueba llenan todos los campos (DEC-177).

   Con la obligatoriedad encendida (DEC-161), un escenario que trae pasos a
   medias no deja avanzar ni enviar, y el panel deja de servir para recorrer
   casos. Se comprueba que cada escenario completo pasa los cinco pasos, que
   en pantalla no queda ningún campo vacío, que llega al acuse sin capturar
   nada y que las tres excepciones siguen siendo lo que son."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina27.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

EXCEPCIONES = {'derivado', 'vacio', 'fuera'}
VACIOS_PERMITIDOS = {'f_filtro'}   # el buscador de materias del paso 1

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    ids = pg.evaluate("() => ESCENARIOS.map(e => e.id)")
    afirma(len(ids) == 11, 'el panel ofrece los once escenarios: %s' % ids)
    afirma(pg.evaluate("() => cfg.validar === true"), 'la obligatoriedad está encendida, como en operación')

    for e in ids:
        if e in EXCEPCIONES: continue
        pasos = pg.evaluate("""(e) => { cargaEscenario(e); const r = [];
          for(let n = 1; n <= 5; n++) r.push(valida(n)); return r; }""", e)
        afirma(all(pasos), '%s: los cinco pasos pasan la validación %s' % (e, pasos))
        vacios = []
        for n in range(1, 6):
            v = pg.evaluate("""([e, n]) => { cargaEscenario(e); irA(n);
              return [...document.querySelectorAll('#app input:not([type=checkbox]):not([type=radio]):not([type=file]), #app textarea, #app select')]
                .filter(x => x.offsetParent && !x.value).map(x => x.id); }""", [e, n])
            vacios += [x for x in v if x not in VACIOS_PERMITIDOS]
        afirma(not vacios, '%s: ningún campo visible queda vacío, tampoco los opcionales (vacíos: %s)' % (e, vacios))
        fin = pg.evaluate("""(e) => { cargaEscenario(e); guarda('verificacion','si'); irA(6); enviar();
          return {folio: val('folio'), acuse: !!document.querySelector('.datos-acuse'), arch: archivos.length}; }""", e)
        afirma(fin['folio'] and fin['acuse'], '%s: llega al acuse sin capturar nada (%s)' % (e, fin['folio']))
        afirma(fin['arch'] == 2, '%s: trae dos pruebas simuladas' % e)

    # La colonia se reconoce en el catálogo, como si se eligiera de la lista
    cves = pg.evaluate("""() => ['urbano','ava','anp_federal','otro_giro'].map(e => { cargaEscenario(e); return val('colonia_cve'); })""")
    afirma(all(cves), 'la colonia de los escenarios con dirección lleva su clave del IECM: %s' % cves)

    # Datos que existen en los catálogos
    tipos = pg.evaluate("""() => ESCENARIOS.map(e => e.e.tipo_denunciado).filter(Boolean)
      .filter(t => !TIPOS_DENUNCIADO.some(x => x.v === t))""")
    afirma(tipos == [], 'todo «tipo_denunciado» es un valor del catálogo (fuera de catálogo: %s)' % tipos)
    gob = pg.evaluate("""() => { cargaEscenario('gobierno'); irA(3); const f = document.getElementById('f_autoridad_denunciada');
      return f && f.offsetParent ? f.value : null; }""")
    afirma(gob == 'Iztapalapa', '«Obra de una alcaldía» muestra la autoridad señalada: %s' % gob)

    # Las tres excepciones
    afirma(pg.evaluate("() => { cargaEscenario('vacio'); return !valida(2); }"), '«Formulario vacío» sigue vacío: el paso 2 exige sus datos')
    afirma(pg.evaluate("() => { cargaEscenario('derivado'); return !!val('deriva') && !val('materia'); }"), '«Caso de otra autoridad» se detiene en el paso 1 y orienta')
    afirma(pg.evaluate("() => { cargaEscenario('fuera'); return !valida(2) && valida(3) && valida(5); }"),
           '«Punto fuera de la Ciudad»: el paso 2 lo detiene la competencia; los demás pasos vienen llenos')

    # Desde el panel, con un clic
    pg.evaluate("() => { estado = {}; irA(0); document.getElementById('panel').classList.add('abierto'); }")
    pg.click('#listaEscenarios button:has-text("Afectación en Área de Valor Ambiental")')
    pg.wait_for_timeout(300)
    vis = pg.evaluate("() => [...document.querySelectorAll('#app input, #app textarea')].filter(x => x.offsetParent && x.id === 'f_calle').map(x => x.value)")
    afirma(vis == ['Avenida San Fernando'], 'al pulsar el escenario en el panel, los campos aparecen llenos en pantalla: %s' % vis)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
