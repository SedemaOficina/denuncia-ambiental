# -*- coding: utf-8 -*-
"""Textos libres sin letras al azar (DEC-224).

   «Cuenta qué pasó» ya pedía un relato que pareciera texto (pareceTexto).
   Los demás campos de texto libre —cómo se reconoce el sitio, nombre del
   lugar, tipo de establecimiento «Otro», señas de quien lo hace, gestiones
   previas y otras pruebas— admitían cualquier cosa. Ahora rechazan letras al
   azar, sin exigir extensión: «Portón negro» o «Mz. 3, Lt. 12» siguen
   valiendo. Un campo opcional en blanco no se revisa."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina34.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

BASURA = ['ASFSAFASFDSFSDVDVFEDFVEVERRV EVWEVEVERVEW  EVECWEDCWECWEC3ECWE', 'asdasd asdasd', 'qwerty',
          'sdfghjk', 'jjjjjj', 'xcvbnm', 'hola hola hola', 'kdkdkd lslsls']
BUENOS = ['Portón negro', 'Mz. 3, Lt. 12', 'Frente al OXXO', 'Junto a la CFE', 'IMSS ISSSTE',
          'Instrucciones del transformador', 'Llamé al 911 y no vinieron', 'Camioneta Nissan NP300 blanca',
          'Casa 10000 metros adelante', 'Hay un letrero de SCHWARZKOPF', 'Sí', 'Paraje Tlaxcaltenco']

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)

    r = pg.evaluate("""([b, g]) => {
      const reales = []; ESCENARIOS.forEach(e => ['referencias','nombre_lugar','tipo_estab_otro','resp_senas','gestiones','otras_pruebas','hechos']
        .forEach(k => { if(e.e[k]) reales.push(e.e[k]); }));
      return {noDetectados: b.filter(t => !pareceRelleno(t)), falsos: g.concat(reales).filter(t => pareceRelleno(t)), n: reales.length}; }""",
      [BASURA, BUENOS])
    afirma(r['noDetectados'] == [], 'las letras al azar se detectan: %s' % r['noDetectados'])
    afirma(r['falsos'] == [], 'los textos reales —cortos o de los %d de los escenarios— pasan: %s' % (r['n'], r['falsos']))

    # Obligatorio: «¿Cómo se reconoce el sitio?» con relleno no deja avanzar.
    v = pg.evaluate("""(t) => { cargaEscenario('urbano'); cfg.validar = true; guarda('referencias', t); irA(2);
      const ok = valida(2), e = document.getElementById('e_referencias');
      return {ok, msg: e ? e.textContent : '', marcado: document.getElementById('c_referencias').classList.contains('invalido')}; }""", BASURA[0])
    afirma(v['ok'] is False and v['marcado'], 'con letras al azar en «¿Cómo se reconoce el sitio?», el paso 2 no avanza')
    afirma('No se entiende' in v['msg'], 'y el mensaje dice cuál es el problema: %r' % v['msg'])
    v2 = pg.evaluate("""() => { cargaEscenario('urbano'); cfg.validar = true; guarda('referencias', 'Portón negro'); irA(2); return valida(2); }""")
    afirma(v2 is True, 'una respuesta corta y real («Portón negro») sí avanza')

    # Opcional: en blanco pasa; con relleno, no.
    o = pg.evaluate("""(t) => { cargaEscenario('urbano'); cfg.validar = true; guarda('reporto_antes','si'); guarda('gestiones',''); irA(3);
      const vacio = valida(3); guarda('gestiones', t); irA(3); const relleno = valida(3);
      return {vacio, relleno}; }""", 'asdasd asdasd')
    afirma(o['vacio'] is True, 'un campo opcional en blanco no se revisa')
    afirma(o['relleno'] is False, 'pero con relleno tampoco deja avanzar')

    # Al salir del campo se avisa, sin esperar a «Continuar».
    pg.evaluate("() => { cargaEscenario('urbano'); cfg.validar = true; guarda('referencias',''); irA(2); }")
    pg.fill('#f_referencias', 'qwerty qwerty'); pg.locator('#f_calle').focus(); pg.wait_for_timeout(150)
    b = pg.evaluate("() => ({marcado: document.getElementById('c_referencias').classList.contains('invalido'), msg: document.getElementById('e_referencias').textContent})")
    afirma(b['marcado'] and 'No se entiende' in b['msg'], 'al salir del campo ya avisa que no se entiende')

    # «Cuenta qué pasó»: además de parecer relato, sin relleno.
    h = pg.evaluate("""() => { cargaEscenario('urbano'); cfg.validar = true;
      guarda('hechos', 'Todos los dias sale humo negro del taller de la esquina asdasd asdasd asdasd y huele a solvente'); irA(3);
      return valida(3); }""")
    afirma(h is False, '«Cuenta qué pasó» con relleno metido entre palabras reales tampoco avanza')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
