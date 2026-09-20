# -*- coding: utf-8 -*-
"""Bloque C: obligatoriedad condicional en OBLIG, ruta del lugar sin calle,
   fusion de los dos campos de referencias y mudanza del establecimiento."""
import os, pathlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
import sys, json

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')

fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width':390,'height':844})
    pg = ctx.new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---------- 1. El defecto original ----------
    r = pg.evaluate("""() => {
      cfg.validar = true;
      guarda('materia','tala'); guarda('resp_tipo','desconocido');
      guarda('tiene_direccion','no');
      irA(2); ponMarcador(19.2938, -99.1930);
      return {capa: val('capa_nombre'), dg: val('dg'), alc_punto: val('alcaldia_punto'),
              nombre: val('nombre_lugar'), alc: val('alcaldia')};
    }""")
    afirma(r['capa'] == 'Bosque de Tlalpan', 'el punto se identifica como Bosque de Tlalpan')
    afirma(r['nombre'] == 'Bosque de Tlalpan', 'el nombre del sitio se PROPONE desde la capa (%s)' % r['nombre'])
    afirma(r['alc'] == 'Tlalpan', 'la alcaldia se propone desde el punto (%s)' % r['alc'])

    pg.wait_for_timeout(300)
    res = pg.evaluate("""() => {
      guarda('referencias','Se entra por la puerta 3, a 200 m del estacionamiento.');
      const pasa = valida(2);
      const faltan = [...document.querySelectorAll('.campo.invalido label, .campo.invalido .etq')].map(e=>e.textContent.trim());
      return {pasa, faltan};
    }""")
    afirma(res['pasa'] is True, 'UNA DENUNCIA EN EL BOSQUE DE TLALPAN YA PUEDE PRESENTARSE (faltan: %s)' % res['faltan'])

    # ---------- 2. Sin el campo de acceso no avanza ----------
    r2 = pg.evaluate("""() => { guarda('referencias',''); const pasa = valida(2);
        return {pasa, esOblig: esObligatorio('referencias')}; }""")
    afirma(r2['pasa'] is False and r2['esOblig'] is True,
           'sin dirección, «cómo se llega» es obligatorio y frena el paso')
    pg.evaluate("guarda('referencias','Se entra por la puerta 3.')")

    # ---------- 3. La condicion vive en OBLIG ----------
    c = pg.evaluate("""() => {
      const antes = {calle: esObligatorio('calle'), colonia: esObligatorio('colonia'), cp: esObligatorio('cp'),
                     nombre: esObligatorio('nombre_lugar'), refs: esObligatorio('referencias')};
      guarda('tiene_direccion','si');
      const despues = {calle: esObligatorio('calle'), colonia: esObligatorio('colonia'), cp: esObligatorio('cp'),
                       nombre: esObligatorio('nombre_lugar'), refs: esObligatorio('referencias')};
      guarda('tiene_direccion','no');
      return {antes, despues};
    }""")
    afirma(c['antes']['calle'] is False and c['antes']['colonia'] is False and c['antes']['cp'] is False,
           'sin dirección: calle, colonia y CP NO son obligatorios')
    afirma(c['despues']['calle'] is True and c['despues']['colonia'] is True and c['despues']['cp'] is True,
           'con dirección: calle, colonia y CP vuelven a ser obligatorios')
    afirma(c['antes']['nombre'] is True and c['despues']['nombre'] is False,
           'el nombre del lugar sólo es obligatorio en la ruta sin dirección')
    afirma(c['antes']['refs'] is True and c['despues']['refs'] is False,
           'el campo de acceso sólo es obligatorio en la ruta sin dirección')

    cond = pg.evaluate("""() => {
      const con = Object.keys(OBLIG).filter(k => OBLIG[k].cond);
      const sinTxt = con.filter(k => !OBLIG[k].cond_txt);
      return {n: con.length, claves: con, sinTxt};
    }""")
    afirma(cond['n'] >= 17, 'hay %d campos con condición declarada en OBLIG' % cond['n'])
    afirma(cond['sinTxt'] == [], 'toda condición tiene texto legible para el documento 09 (%s)' % cond['sinTxt'])

    sueltas = pg.evaluate("""() => {
      const t = valida.toString();
      return ['sabe_permisos','reporto_antes','tipo_denunciado','notif_correo'].filter(x => t.indexOf(x) >= 0);
    }""")
    afirma(sueltas == [], 'valida() ya no lleva condiciones propias (quedan: %s)' % sueltas)

    # ---------- 4. La ruta con direccion sigue intacta ----------
    d = pg.evaluate("""() => {
      guarda('tiene_direccion','si'); ['calle','colonia','cp'].forEach(k=>guarda(k,''));
      const vacio = valida(2);
      guarda('calle','Av. Rio Churubusco'); guarda('colonia','Del Carmen'); guarda('cp','04100');
      const lleno = valida(2);
      return {vacio, lleno};
    }""")
    afirma(d['vacio'] is False and d['lleno'] is True, 'con dirección: frena vacía y avanza llena')

    # ---------- 5. La pantalla cambia de forma ----------
    pg.evaluate("guarda('tiene_direccion','si'); irA(2)"); pg.wait_for_timeout(350)
    conDir = pg.evaluate("""() => ({calle: !!document.getElementById('f_calle'),
        nombre: !!document.getElementById('f_nombre_lugar'),
        plegable: document.querySelectorAll('.enc-opcional').length,
        ubicar: [...document.querySelectorAll('button')].some(b=>b.textContent.includes('Ubicar en el mapa'))})""")
    pg.evaluate("guarda('tiene_direccion','no'); render()"); pg.wait_for_timeout(350)
    sinDir = pg.evaluate("""() => ({calle: !!document.getElementById('f_calle'),
        nombre: !!document.getElementById('f_nombre_lugar'),
        refs: !!document.getElementById('f_referencias'),
        plegable: document.querySelectorAll('.enc-opcional').length})""")
    afirma(conDir['calle'] and not conDir['nombre'], 'con dirección se ve la calle y no el nombre del lugar')
    afirma(sinDir['nombre'] and not sinDir['calle'], 'sin dirección se ve el nombre del lugar y no la calle')
    afirma(sinDir['refs'], 'sin dirección, el campo de acceso está a la vista (no plegado)')
    # El bloque plegable se disolvio (DEC-56): los campos accesorios son parte
    # de la direccion, y por eso no existen en la ruta sin domicilio.
    afirma(conDir['plegable'] == 0 and sinDir['plegable'] == 0,
           'no queda ningun bloque plegable en ninguna ruta (%s / %s)' % (conDir['plegable'], sinDir['plegable']))
    afirma(pg.evaluate("() => !!document.getElementById('f_entre_calle1')") is False,
           'sin direccion no se piden entre-calles')

    # ---------- 6. Fusion de los dos campos ----------
    f = pg.evaluate("""() => ({fachada: typeof OBLIG.fachada, comoLlegar: typeof OBLIG.como_llegar,
        refsEtq: OBLIG.referencias.etq, enLimites: typeof LIMITES.fachada})""")
    afirma(f['fachada'] == 'undefined' and f['comoLlegar'] == 'undefined',
           'no quedan campos duplicados: fachada y como_llegar desaparecieron de OBLIG')
    afirma(f['enLimites'] == 'undefined', 'fachada tampoco quedó en la tabla de límites')
    afirma('reconoce' in f['refsEtq'] and 'llega' in f['refsEtq'], 'el campo fundido nombra las dos cosas: «%s»' % f['refsEtq'])

    # ---------- 7. El establecimiento, en el paso 3 ----------
    e = pg.evaluate("""() => ({paso: OBLIG.es_estab.p, tipo: OBLIG.tipo_estab.p, nom: OBLIG.nombre_estab.p,
        aviso: typeof avisoHeredado})""")
    afirma(e['paso'] == 3 and e['tipo'] == 3 and e['nom'] == 3, 'es_estab, tipo_estab y nombre_estab declaran paso 3')
    afirma(e['aviso'] == 'undefined', 'avisoHeredado() se eliminó: ya no hay distancia que salvar')

    pg.evaluate("irA(3)"); pg.wait_for_timeout(350)
    p3 = pg.evaluate("""() => {
      const t = document.getElementById('app').innerText;
      return {tieneEstab: t.includes('dentro de un establecimiento'),
              antesQueResponsable: t.indexOf('dentro de un establecimiento') < t.indexOf('responsable de los hechos'),
              yaNoDiceElLugar: !t.includes('el lugar ya lo señalaste')};
    }""")
    afirma(p3['tieneEstab'], 'la pregunta del establecimiento se hace en el paso 3')
    afirma(p3['antesQueResponsable'], 'y va ANTES de «¿quién es responsable?», que es lo que propone')
    afirma(p3['yaNoDiceElLugar'], 'desapareció la aclaración que existía sólo por la distancia entre pasos')

    herencia = pg.evaluate("""() => {
      guarda('tipo_denunciado',''); guarda('es_estab','si'); heredaEstablecimiento();
      return val('tipo_denunciado');
    }""")
    afirma(herencia == 'empresa', 'la herencia sigue funcionando desde su nueva posición')

    # ---------- 8. Recorrido completo ----------
    for n in range(0, 8):
        pg.evaluate("irA(%d)" % n); pg.wait_for_timeout(230)
        afirma(pg.locator('#app').inner_html().strip() != '', 'el paso %d renderiza' % n)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:3])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
