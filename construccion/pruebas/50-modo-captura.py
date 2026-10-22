# -*- coding: utf-8 -*-
"""Modo captura por personal en el formulario (AD-03, DEC-248).

   1. Apagado de origen: la ciudadanía no ve nada distinto. Lo encienden el
      panel de validación o la dirección «?modo=captura».
   2. El primer paso pide canal, fecha y hora de recepción original y quién
      recibió; el folio de origen es opcional.
   3. El paso 4 exige el soporte, y lo nombra según el canal.
   4. El correo y el domicilio pueden no venir; quedan anotados como no
      proporcionados y el acuse no promete notificar por esa vía.
   5. Sin prueba de humanidad ni límite de envíos; misma serie de folios.
   6. La revisión y el acuse dicen cómo llegó; el acuse dice cómo se entrega
      y deja a la vista el aviso de denuncias cercanas.
   7. Al apagarlo, todo vuelve a ser como en línea."""
import os, pathlib, re, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina50.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED', 'net::ERR_', 'Failed to load resource')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
OPCIONALES = {'correo', 'dom_calle', 'dom_num_ext', 'dom_tiene_mz_lote', 'dom_manzana', 'dom_colonia', 'dom_alcaldia', 'dom_entidad', 'dom_municipio'}

try:
  with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    def h2(): return pg.evaluate("() => document.querySelector('#app h2') ? document.querySelector('#app h2').textContent : document.querySelector('h2').textContent")

    # ---- 1. Apagado de origen ----
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    afirma(pg.evaluate("() => cfg.captura === false && !document.getElementById('cfgCaptura').checked") and 'Denunciar el daño ambiental' in pg.inner_text('body'),
           'apagado de origen: la portada es la de la ciudadanía')
    pg.goto(TMP.as_uri() + '?modo=captura'); pg.wait_for_timeout(700)
    afirma(pg.evaluate("() => cfg.captura === true && document.getElementById('cfgCaptura').checked") and 'Captura de una denuncia recibida por otro medio' in pg.inner_text('body'),
           '«?modo=captura» lo enciende y el panel lo muestra encendido')
    afirma(pg.evaluate("() => /Versión 38/.test(VERSION_FORMULARIO.nombre)"), 'el formulario dice «Versión 38»')

    # ---- 2. Primer paso ----
    pg.click('text=Iniciar la captura'); pg.wait_for_timeout(200)
    faltan = pg.evaluate("() => [...document.querySelectorAll('.campo.invalido')].map(e => e.id.replace(/^c_/, ''))")
    afirma(pg.evaluate("() => paso") == 0 and {'canal', 'recepcion_fecha', 'recepcion_hora', 'recibio'} <= set(faltan) and 'folio_origen' not in faltan,
           'sin canal, fecha, hora y quién recibió no se inicia; el folio de origen es opcional: %s' % sorted(set(faltan)))
    pg.select_option('#f_canal', 'telefono')
    pg.fill('#f_recepcion_fecha', '2026-10-20'); pg.fill('#f_recepcion_hora', '09:15'); pg.fill('#f_recibio', 'Persona de prueba')
    pg.evaluate("() => { ['recepcion_fecha','recepcion_hora','recibio'].forEach(k => guarda(k, document.getElementById('f_' + k).value)); }")
    pg.click('text=Iniciar la captura'); pg.wait_for_timeout(200)
    afirma(pg.evaluate("() => paso") == 1, 'con lo obligatorio, la captura sigue al paso 1')

    # ---- 3. Soporte ----
    sop = pg.evaluate("""() => CANALES_CAPTURA.map(c => { guarda('canal', c.id); irA(4);
        return [c.id, document.getElementById('a_soporte').textContent.indexOf(c.soporte) === 0, esObligatorio('soporte')]; })""")
    afirma(len(sop) == 4 and all(s[1] and s[2] for s in sop), 'el paso 4 exige el soporte y lo nombra según cada uno de los cuatro canales')
    afirma(not pg.evaluate("() => valida(4)") and pg.evaluate("() => document.getElementById('c_soporte').classList.contains('invalido')"),
           'sin soporte no se pasa del paso 4')

    # ---- 4. Correo y domicilio pueden no venir ----
    opc = pg.evaluate("() => Object.keys(OBLIG).filter(k => OBLIG[k].captura_opcional)")
    afirma(set(opc) == OPCIONALES, 'pueden no venir el correo y los datos obligatorios del domicilio, y nada más: %s' % sorted(set(opc) ^ OPCIONALES))
    pg.evaluate("() => cargaEscenario('captura')"); pg.wait_for_timeout(300)
    afirma(pg.evaluate("() => [0,1,2,3,4,5].every(n => valida(n))"), 'el escenario «Captura por personal» pasa los seis pasos, del 0 al 5')
    pg.evaluate("() => { ['correo','dom_calle','dom_num_ext','dom_colonia','dom_alcaldia','dom_cp','dom_entre_calles','dom_num_int'].forEach(k => guarda(k, '')); irA(5); }")
    marcas = pg.evaluate("() => ['correo','dom_calle'].map(k => (document.querySelector('label[for=f_' + k + ']') || {}).textContent || '')")
    afirma(pg.evaluate("() => valida(5)") and all('(opcional)' in m for m in marcas), 'sin correo ni domicilio el paso 5 pasa, y los dos se ven como opcionales: %s' % marcas)
    pg.evaluate("() => irA(6)"); pg.wait_for_timeout(150)
    rev = pg.evaluate("() => datosDelAcuse()")
    filas = {f[0]: f[1] for b in rev for f in b['filas']}
    afirma(rev[0]['titulo'] == 'Cómo llegó' and filas.get('Medio') == 'Oficialía de Partes' and filas.get('Recepción original') == '19 de octubre de 2026, 11:20 horas'
           and filas.get('Folio de origen') == 'OP-2026-0517' and filas.get('Soporte') == 'escrito-con-sello.pdf',
           'la revisión empieza por «Cómo llegó»: medio, recepción, folio de origen, quién recibió y soporte')
    afirma('Correo no proporcionado' in filas.get('Contacto', '') and filas.get('Domicilio para notificaciones') == 'No proporcionado',
           'la revisión dice qué no se proporcionó')

    # ---- 5. Sin prueba de humanidad ni límite; misma serie ----
    afirma(not pg.locator('#chkHumano').count() and 'Guardar la captura' in pg.inner_text('#app'), 'sin prueba de humanidad, y el botón dice «Guardar la captura»')
    pg.evaluate("() => { cfg.limite = true; guarda('verificacion', ''); enviar(); }"); pg.wait_for_timeout(300)
    d = pg.evaluate("() => ({paso, folio: val('folio'), orig: val('fecha_recepcion_original'), np: val('no_proporcionado'), acuse: val('fecha_acuse')})")
    afirma(d['paso'] == 7 and re.fullmatch(r'SEDEMA/DEN/\d{4}/\d{6}-\d', d['folio']),
           'se guarda sin prueba de humanidad y aunque el límite esté encendido, con un folio de la misma serie: %s' % d['folio'])
    afirma(d['orig'] == '2026-10-19T11:20:00' + d['acuse'][-6:] and d['np'] == 'correo, domicilio',
           'guarda la recepción original en hora de la Ciudad y lo que no venía: %s · %s' % (d['orig'], d['np']))

    # ---- 6. Acuse ----
    a = pg.inner_text('#app')
    afirma('Denuncia capturada' in a and 'CP-3' in a and 'Denuncias cercanas' in a and 'P-21, control 4' in a,
           'el acuse dice cómo se entrega (CP-3) y deja a la vista el aviso de denuncias cercanas')
    afirma('Recibida por Oficialía de Partes el 19 de octubre de 2026, 11:20 horas' in a and 'capturada el' in a,
           'dice cuándo y por dónde llegó, y cuándo se capturó')
    afirma('No dejó domicilio' in a and 'domicilio que registró' not in a, 'sin domicilio, el acuse no promete notificar en él')

    # ---- 7. Al apagarlo ----
    pg.evaluate("() => { document.getElementById('panel').classList.add('abierto'); }")
    pg.uncheck('#cfgCaptura'); pg.wait_for_timeout(300)
    afirma(pg.evaluate("() => cfg.captura === false && paso === 0") and 'Denunciar el daño ambiental' in pg.inner_text('body'), 'apagarlo regresa a la portada de la ciudadanía')
    pg.evaluate("() => cargaEscenario('conservacion')"); pg.wait_for_timeout(300)
    ok = pg.evaluate("""() => { const c = val('correo'); guarda('correo', ''); const sin = valida(5); guarda('correo', c);
        return {sin, humano: !!document.querySelector('#chkHumano'), bloques: datosDelAcuse().map(b => b.titulo), correo: esObligatorio('correo')}; }""")
    afirma(ok['sin'] is False and ok['correo'] and ok['humano'] and 'Cómo llegó' not in ok['bloques'],
           'en línea la anónima vuelve a exigir el correo, hay prueba de humanidad y la revisión no trae «Cómo llegó»')
    pg.evaluate("() => cargaEscenario('captura')"); pg.wait_for_timeout(200)
    pg.evaluate("() => cargaEscenario('urbano')"); pg.wait_for_timeout(200)
    afirma(pg.evaluate("() => cfg.captura === false && !document.getElementById('cfgCaptura').checked"),
           'un escenario de la ciudadanía apaga el modo captura que dejó encendido el anterior')
    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()
finally:
  TMP.unlink(missing_ok=True)

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
