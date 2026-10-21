# -*- coding: utf-8 -*-
"""Accesibilidad y robustez (DEC-237; bloque 5 de la auditoría del 20 de
   octubre de 2026).

   1. B4-01: las tres ventanas —aviso de privacidad, mapeo y ramas— llevan el
      foco a su título al abrirse, no lo dejan salir con Tab ni con Mayús+Tab
      y lo devuelven a quien las abrió al cerrarse, con Escape o con «×».
   2. B5-01: un borrador que no puede retomarse se descarta y la portada lo
      dice; antes dejaba la pantalla en blanco. Uno válido se sigue retomando.
   3. A5-01: ningún constructor fija la obligatoriedad a mano. Se comprueba
      por su efecto: si OBLIG vuelve obligatorio un campo opcional, la pantalla
      le pone el asterisco; en la anónima manda EXIGIDO_ANONIMO.
   4. D1-12: calles, entre calles y nombre del establecimiento rechazan
      letras al azar, sin rechazar ninguna colonia del catálogo; los nombres de
      persona quedan fuera a propósito."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina40.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

DONDE = "() => { const a = document.activeElement; const m = a && a.closest('.modal'); return {id: m ? m.id : null, tag: a ? a.tagName : null, txt: a ? (a.textContent || '').trim().slice(0, 30) : ''}; }"

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. Foco de las ventanas (B4-01) ----
    pg.evaluate("() => { estado = {}; paso = 0; render(); }")
    pie = pg.locator('button.enlace', has_text='Aviso de privacidad').first
    pie.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    d = pg.evaluate(DONDE)
    afirma(d['id'] == 'modalPriv' and d['tag'] == 'H3', 'al abrir el aviso de privacidad desde el pie, el foco va al título de la ventana: %s' % d)
    dentro = []
    for tecla in ['Tab'] * 4 + ['Shift+Tab'] * 4:
        pg.keyboard.press(tecla); dentro.append(pg.evaluate(DONDE)['id'])
    afirma(all(x == 'modalPriv' for x in dentro), 'Tab y Mayús+Tab no sacan el foco de la ventana: %s' % dentro)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
    r = pg.evaluate("() => ({abierta: document.getElementById('modalPriv').classList.contains('abierto'), txt: (document.activeElement.textContent || '').trim()})")
    afirma(not r['abierta'] and r['txt'] == 'Aviso de privacidad', 'Escape la cierra y el foco vuelve al botón que la abrió: %s' % r)
    for abre, ventana in (('abreMapeo', 'modalMapeo'), ('abreVariantes', 'modalVariantes')):
        r = pg.evaluate("""([abre, ventana]) => { const b = document.querySelector('#app button, #app a[href]'); b.focus();
          window[abre](); const m = document.activeElement.closest('.modal');
          const enTitulo = !!m && m.id === ventana && document.activeElement.tagName === 'H3';
          document.querySelector('#' + ventana + ' .cerrar').click();
          return {enTitulo, vuelve: document.activeElement === b, cerrada: !document.getElementById(ventana).classList.contains('abierto')}; }""", [abre, ventana])
        afirma(r['enTitulo'] and r['vuelve'] and r['cerrada'], '%s: el foco entra al título y, al cerrar con «×», vuelve a donde estaba: %s' % (ventana, r))

    # ---- 2. Borrador que no puede retomarse (B5-01) ----
    for nombre, valor in (('con un paso que no existe', '{"estado":{"materia":"ruido"},"paso":99,"t":%d}'),
                          ('que no es JSON', '{esto no es json'),
                          ('sin estado', '{"paso":3,"t":%d}')):
        pg.evaluate("(v) => localStorage.setItem(CLAVE_BORRADOR, v.replace('%d', Date.now()))", valor)
        pg.reload(); pg.wait_for_timeout(600)
        r = pg.evaluate("""() => ({franja: document.getElementById('franjaBorrador').innerText, guardado: localStorage.getItem(CLAVE_BORRADOR),
                                   portada: paso === 0 && document.getElementById('app').innerText.trim().length > 200})""")
        afirma('No se pudo recuperar el avance guardado' in r['franja'] and r['guardado'] is None and r['portada'],
               'un borrador %s se descarta y la portada lo dice: %r' % (nombre, r['franja'][:60]))
    pg.evaluate("() => localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado: {materia: 'ruido', tiene_direccion: 'si'}, paso: 3, t: Date.now()}))")
    pg.reload(); pg.wait_for_timeout(600)
    r = pg.evaluate("() => document.getElementById('franjaBorrador').innerText")
    afirma('Tienes una denuncia sin terminar' in r, 'uno válido se sigue ofreciendo')
    pg.click('text=Continuar donde me quedé'); pg.wait_for_timeout(300)
    r = pg.evaluate("() => ({paso: paso, h2: (document.querySelector('#app h2') || {}).textContent || ''})")
    afirma(r['paso'] == 3 and r['h2'], 'y se retoma en su paso: %s' % r)
    pg.evaluate("() => borraBorrador()")

    # ---- 3. La obligatoriedad sale de OBLIG (A5-01) ----
    #    En los dos sentidos: un opcional que se vuelve obligatorio gana el
    #    asterisco, y un obligatorio que se vuelve opcional lo pierde. Las
    #    casillas no se marcan (dejarlas sin marcar es una respuesta), y el de
    #    los archivos va en el título del paso, no en el campo.
    ob = pg.evaluate("""() => { const malos = [], probados = new Set();
      const rec = [['otro_giro', {tiene_mz_lote:'si', reporto_antes:'si', tipo_denunciado:'nose'}], ['gobierno', {autoridad_nivel:'cdmx', dom_tiene_mz_lote:'si'}],
                   ['urbano', {}], ['sin_calle', {}]];
      const marca = k => !!document.querySelector(k === 'archivos' ? '#app h2 .req' : '#c_' + k + ' .req');
      for (const [e, extra] of rec) for (let n = 2; n <= 5; n++) {
        cargaEscenario(e); Object.entries(extra).forEach(([k, v]) => guarda(k, v)); cfg.validar = true; irA(n);
        const ks = [...document.querySelectorAll('#app [id^="c_"]')].map(x => x.id.slice(2))
          .filter(k => OBLIG[k] && (!OBLIG[k].cond || OBLIG[k].cond()) && !document.querySelector('#c_' + k + ' input[type=checkbox]'));
        for (const k of ks) { const era = !!OBLIG[k].oblig; OBLIG[k].oblig = !era; render(); probados.add(k);
          if (marca(k) === era) malos.push(k + ' (paso ' + n + ', ' + (era ? 'no lo pierde' : 'no lo gana') + ')');
          OBLIG[k].oblig = era; }
        render(); }
      cargaEscenario('conservacion'); cfg.validar = true; irA(5);
      const antes = !!document.querySelector('#c_telefono .req');
      EXIGIDO_ANONIMO.push('telefono'); render(); const despues = !!document.querySelector('#c_telefono .req');
      EXIGIDO_ANONIMO.splice(EXIGIDO_ANONIMO.indexOf('telefono'), 1); render();
      return {malos, probados: [...probados], antes, despues}; }""")
    afirma(not ob['malos'], 'si OBLIG cambia la obligatoriedad de un campo, la pantalla pone o quita el asterisco: fallan %s' % ob['malos'])
    a_mano = ['entre_calles', 'gestiones', 'resp_senas', 'otras_pruebas', 'apellido_materno', 'dom_num_int', 'dom_entre_calles',
              'sexo_genero', 'edad_rango']
    afirma(all(k in ob['probados'] for k in a_mano), 'entre ellos los que tenían la obligatoriedad escrita a mano (%d campos probados)' % len(ob['probados']))
    afirma(not ob['antes'] and ob['despues'], 'en la anónima el teléfono sigue opcional, y lo decide EXIGIDO_ANONIMO, no un literal')

    # ---- 4. Letras al azar (D1-12) ----
    rl = pg.evaluate("""() => { const ks = ['calle', 'entre_calles', 'nombre_estab', 'dom_calle', 'dom_entre_calles'];
      cargaEscenario('urbano');
      const rechaza = ks.filter(k => { guarda(k, 'ASFSAFASFDSFQWRTZX'); const r = formatoMal(k) && msgFormato(k) === NO_SE_ENTIENDE; return !r; });
      const cols = [...new Set(CATALOGO_COLONIAS.filas.map(f => f[0]))];
      cargaEscenario('urbano'); cfg.validar = true; guarda('nombre', 'Asdrúbal'); guarda('apellido_paterno', 'Mkrtchyan'); irA(5);
      return {noRechaza: rechaza, colonias: cols.length, falsos: cols.filter(c => pareceRelleno(c)),
              nombres: ['nombre', 'apellido_paterno', 'apellido_materno'].filter(k => FORMATO[k]), pasa5: valida(5)}; }""")
    afirma(not rl['noRechaza'], 'calles, entre calles y nombre del establecimiento rechazan «ASFSAFASFDSFQWRTZX»: no lo rechazan %s' % rl['noRechaza'])
    afirma(not rl['falsos'], 'sin rechazar ninguna de las %d colonias del catálogo: %s' % (rl['colonias'], rl['falsos'][:5]))
    afirma(not rl['nombres'] and rl['pasa5'] is True, 'los nombres de persona quedan fuera: «Asdrúbal Mkrtchyan» pasa el paso 5')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
