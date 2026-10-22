# -*- coding: utf-8 -*-
"""El modo captura le habla a quien captura (DEC-261, «Versión 38»).

   1. En modo captura, ningún paso le habla a quien denuncia: ni «tú» ni
      «tus», ni «mi denuncia», ni el consentimiento en primera persona; los
      pasos se llaman «Qué se denuncia» y «Quien denuncia».
   2. El aviso de privacidad no se muestra: quien captura marca que se le
      informó a la persona y que aceptó, y que manifestó bajo protesta de decir
      verdad que los hechos son ciertos.
   3. Se pregunta «¿Por qué medio llegó?»; la hora se escribe en horas y
      minutos, de 00:00 a 23:59, y la revisión la dice en palabras.
   4. El soporte se sube como la evidencia: se elige o se arrastra.
   5. En línea, nada cambia: el formulario le sigue hablando a quien
      denuncia."""
import os, pathlib, re, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina56.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED', 'net::ERR_', 'Failed to load resource')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
# Lo que delata que se le habla a quien denuncia.
A_QUIEN_DENUNCIA = re.compile(r'\b(tu|tus|Tu|Tus|contigo|te notifica|mi denuncia|mis datos|Escribo mis datos|consiento|denuncio|Vivo fuera)\b')

# Recorre los pasos 1 a 6 con un escenario, en un modo o en el otro, abriendo lo
# plegado, y junta lo que se lee. Cargar un escenario apaga la captura: se
# vuelve a poner.
LEE_PASOS = """([esc, captura]) => { cargaEscenario(esc); cfg.captura = captura; const out = {};
  for (let n = 1; n <= 6; n++) { irA(n); document.querySelectorAll('#app details').forEach(d => d.open = true);
    out[n] = document.getElementById('app').innerText + '\\n' + document.getElementById('progreso').getAttribute('aria-label'); }
  return out; }"""

try:
  with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(TMP.as_uri() + '?modo=captura'); pg.wait_for_timeout(700)

    # ---- 1. Ningún paso le habla a quien denuncia ----
    vistos = {}
    for esc in ('captura', 'urbano', 'gobierno', 'anp_federal'):
        pasos = pg.evaluate(LEE_PASOS, [esc, True])
        for n, texto in pasos.items():
            for m in A_QUIEN_DENUNCIA.finditer(texto):
                linea = next(l for l in texto.splitlines() if m.group(0) in l)
                vistos.setdefault((n, linea.strip()[:110]), esc)
    afirma(not vistos, 'en modo captura ningún paso le habla a quien denuncia: %s' % list(vistos)[:4])
    pg.evaluate("() => { cargaEscenario('captura'); irA(5); }"); pg.wait_for_timeout(100)
    afirma(pg.evaluate("() => etapas()[0] === 'Qué se denuncia' && etapas()[4] === 'Quien denuncia' && document.querySelector('#app h2').textContent.indexOf('Datos de quien denuncia') >= 0"),
           'los pasos se llaman «Qué se denuncia» y «Quien denuncia», y el 5 «Datos de quien denuncia»')

    # ---- 2. Aviso de privacidad ----
    priv = pg.evaluate("() => ({aviso: !!document.querySelector('#app .priv-plegable'), casilla: document.querySelector('label[for=chkPriv]').innerText})")
    afirma(not priv['aviso'] and priv['casilla'].startswith('Se informó a la persona del aviso de privacidad y aceptó')
           and 'bajo protesta de decir verdad' in priv['casilla'], 'sin el texto del aviso: quien captura marca que se le informó y aceptó, y la protesta: %s' % priv['casilla'][:70])

    # ---- 3. Medio y hora ----
    pg.evaluate("() => irA(0)"); pg.wait_for_timeout(100)
    afirma('¿Por qué medio llegó?' in pg.inner_text('#app') and 'canal' not in pg.inner_text('#app').lower(), 'se pregunta «¿Por qué medio llegó?» y no se dice «canal»')
    tipo = pg.evaluate("() => document.getElementById('f_recepcion_hora').type")
    def hora(v):
        pg.fill('#f_recepcion_hora', v); pg.evaluate("() => { guarda('recepcion_hora', document.getElementById('f_recepcion_hora').value); avisaFormato('recepcion_hora'); }")
        return pg.evaluate("() => formatoMal('recepcion_hora')")
    malas = {v: hora(v) for v in ('09:30', '23:59', '00:00', '9:30', '24:00', '12:60', '0930')}
    pg.fill('#f_recepcion_hora', '11:20 a. m.'); corta = pg.evaluate("() => document.getElementById('f_recepcion_hora').value")
    afirma(tipo == 'text' and corta == '11:20' and malas == {'09:30': False, '23:59': False, '00:00': False, '9:30': True, '24:00': True, '12:60': True, '0930': True},
           'la hora es de horas y minutos, de 00:00 a 23:59, sin «a. m.» ni «p. m.»: %s' % malas)
    afirma('cuatro cifras' in pg.evaluate("() => msgFormato('recepcion_hora')"), 'si no, dice cómo escribirla')
    pg.evaluate("() => { cargaEscenario('captura'); irA(6); }"); pg.wait_for_timeout(150)
    filas = {f[0]: f[1] for b in pg.evaluate("() => datosDelAcuse()") for f in b['filas']}
    afirma(filas.get('Medio') == 'Oficialía de Partes' and filas.get('Recepción original') == '19 de octubre de 2026, 11:20 horas',
           'la revisión dice el medio y la recepción en palabras, en horas y minutos: %s' % {k: filas.get(k) for k in ('Medio', 'Recepción original')})

    # ---- 4. El soporte, como la evidencia ----
    pg.evaluate("() => { guarda('soporte', ''); irA(4); }"); pg.wait_for_timeout(100)
    sop = pg.evaluate("() => { const c = document.getElementById('c_soporte'); return {zona: !!c.querySelector('button.zona-carga'), oculto: getComputedStyle(document.getElementById('f_soporte')).display, texto: c.innerText}; }")
    pg.set_input_files('#f_soporte', {'name': 'escrito-con-sello.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 prueba'}); pg.wait_for_timeout(150)
    afirma(sop['zona'] and sop['oculto'] == 'none' and 'Selecciona o arrastra el soporte' in sop['texto']
           and pg.evaluate("() => val('soporte')") == 'escrito-con-sello.pdf' and 'Adjunto: escrito-con-sello.pdf' in pg.inner_text('#c_soporte'),
           'el soporte se elige o se arrastra en una zona como la de la evidencia, y dice qué se adjuntó')
    afirma(not pg.locator('#c_soporte .lista-arch').count(), 'y no se mezcla con la lista de la evidencia')

    # ---- 5. En línea, nada cambia ----
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    pasos = pg.evaluate(LEE_PASOS, ['urbano', False])
    afirma('Tus datos' in pasos['5'] and 'Revisar mi denuncia' in pasos['5'] and 'He leído el aviso de privacidad' in pasos['5']
           and pg.evaluate("() => !!document.querySelector('#app .priv-plegable') || (irA(5), !!document.querySelector('#app .priv-plegable'))")
           and '¿Qué quieres denunciar?' in pasos['1'] and pg.evaluate("() => etapas()[4]") == 'Tus datos',
           'en línea el formulario le sigue hablando a quien denuncia, con su aviso de privacidad')
    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()
finally:
    TMP.unlink(missing_ok=True)

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
