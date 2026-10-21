# -*- coding: utf-8 -*-
"""Especificación de datos (DEC-235; bloque 4 de la auditoría del 20 de
   octubre de 2026).

   El diccionario de datos de la fase 2 se deriva del prototipo, y la
   auditoría encontró cuatro cosas que no podían derivarse bien:
   1. D2-01: 24 de 32 campos de texto no tenían longitud máxima. Ahora todo
      campo de texto que se rinde tiene su tope en LIMITES, el control lo
      lleva como maxlength y la validación detiene un texto más largo.
   2. D2-02: la clave del área que atiende valía «FEDERAL», que no es una
      unidad que reciba. Ahora `dg` es DGIVA o DGCORENADR, y la remisión a la
      PROFEPA es otro dato, `remite_a`; un borrador viejo se convierte.
   3. D2-03: la fecha de recepción se guardaba en palabras, con el reloj y la
      zona del equipo. Ahora va en ISO 8601 con la hora y la zona de la Ciudad
      de México, y el año del folio sale de esa misma hora.
   4. D1-06: la tabla de ramas estaba incompleta y con conteos escritos a
      mano. Ahora toda respuesta de la que dependa una condición de OBLIG
      tiene su renglón, y los conteos salen de los catálogos."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
DOC10 = RAIZ.parent / 'documentacion' / '10-variantes-del-formulario.md'
TMP  = AQUI / '_pagina38.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# Recorridos que, juntos, rinden todos los campos de texto de los pasos 2 a 5.
RECORRIDOS = [
  ['otro_giro', {'tiene_mz_lote':'si', 'reporto_antes':'si', 'tipo_denunciado':'nose'}],
  ['gobierno',  {'autoridad_nivel':'cdmx', 'dom_tiene_mz_lote':'si'}],
  ['urbano',    {}],
  ['sin_calle', {}],
  ['conservacion', {}]
]
CAMPOS = """(rec) => { const vistos = {};
  for (const [e, extra] of rec) {
    cargaEscenario(e); Object.entries(extra).forEach(([k, v]) => guarda(k, v));
    for (let n = 2; n <= 5; n++) { irA(n);
      document.querySelectorAll('#app input[type=text], #app input[type=email], #app input[type=tel], #app textarea').forEach(el => {
        if (!el.id.startsWith('f_') || el.closest('.panel-validacion')) return;
        const k = el.id.slice(2); vistos[k] = {max: el.getAttribute('maxlength'), lim: maxDe(k) || null, oblig: k in OBLIG};
      }); } }
  return vistos; }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. Todo campo de texto tiene tope (D2-01) ----
    vistos = pg.evaluate(CAMPOS, RECORRIDOS)
    afirma(len(vistos) >= 32, 'los recorridos rinden %d campos de texto (la auditoría contó 32)' % len(vistos))
    sin_tope = sorted(k for k, v in vistos.items() if not v['lim'])
    afirma(not sin_tope, 'todo campo de texto tiene su tope en LIMITES: %s' % sin_tope)
    distinto = sorted(k for k, v in vistos.items() if v['lim'] and str(v['lim']) != v['max'])
    afirma(not distinto, 'y el control lo lleva como maxlength, el mismo número: %s' % distinto)
    afirma(all(v['oblig'] for v in vistos.values()), 'todos son datos declarados en OBLIG: %s' % [k for k, v in vistos.items() if not v['oblig']])
    sobra = pg.evaluate("() => Object.keys(LIMITES).filter(k => !(k in OBLIG))")
    afirma(not sobra, 'LIMITES no tiene topes para datos que no existen: %s' % sobra)
    largo = pg.evaluate("""() => { cfg.validar = true; const r = {};
      cargaEscenario('urbano'); guarda('nombre', 'a'.repeat(20000)); irA(5); r.p5 = valida(5); r.msg5 = MOTIVO.nombre || '';
      cargaEscenario('urbano'); guarda('calle', 'Calle '.repeat(4000)); irA(2); r.p2 = valida(2); r.msg2 = MOTIVO.calle || '';
      cargaEscenario('urbano'); guarda('calle', 'x'.repeat(maxDe('calle'))); irA(2); r.justo = valida(2);
      return r; }""")
    afirma(largo['p5'] is False and 'admite hasta 80' in largo['msg5'], 'un nombre de 20 000 caracteres ya no pasa el paso 5: %r' % largo['msg5'])
    afirma(largo['p2'] is False and 'admite hasta 120' in largo['msg2'], 'ni una calle de 24 000 en el paso 2: %r' % largo['msg2'])
    afirma(largo['justo'] is True, 'una calle justo en su tope sí pasa')

    # ---- 2. El área es la que recibe; la remisión es otro dato (D2-02) ----
    areas = pg.evaluate("""() => ESCENARIOS.filter(e => e.e.lat).map(e => { cargaEscenario(e.id);
      return [e.id, val('dg'), val('remite_a')]; })""")
    afirma(areas and all(a[1] in ('DGIVA', 'DGCORENADR') for a in areas), 'en todo escenario con punto el área es DGIVA o DGCORENADR: %s' % areas)
    federales = [a for a in areas if a[0] in ('anp_coadmin', 'anp_federal')]
    afirma(len(federales) == 2 and all(a[1] == 'DGCORENADR' and a[2] == 'PROFEPA' for a in federales),
           'en las ANP federales la recibe la DGCORENADR y se remite a la PROFEPA: %s' % federales)
    afirma(all(a[2] == '' for a in areas if a[0] not in ('anp_coadmin', 'anp_federal')), 'en lo demás no hay remisión')
    viejo = pg.evaluate("""() => { localStorage.setItem(CLAVE_BORRADOR, JSON.stringify({estado: {materia:'ava', dg:'FEDERAL'}, paso: 2, t: Date.now()}));
      retomaBorrador(); const r = [val('dg'), val('remite_a')]; borraBorrador(); return r; }""")
    afirma(viejo == ['DGCORENADR', 'PROFEPA'], 'un borrador con «FEDERAL» se convierte al retomarlo: %s' % viejo)
    dic = pg.evaluate("() => [DERIVADOS.dg.uso, !!DERIVADOS.remite_a]")
    afirma('FEDERAL' not in dic[0] and dic[1], 'el diccionario declara `dg` sin «FEDERAL» y declara `remite_a`')

    # ---- 4. Toda rama de OBLIG tiene su renglón; los conteos salen de los catálogos (D1-06) ----
    ramas = pg.evaluate("""() => {
      const lee = (src, vistos) => {
        const k = new Set([...src.matchAll(/val\\('([a-z_]+)'\\)/g)].map(m => m[1]));
        for (const m of src.matchAll(/\\b([a-zA-Z]+)\\(\\)/g)) {
          const f = m[1];
          if (vistos.has(f) || typeof window[f] !== 'function' || f === 'val') continue;
          vistos.add(f); lee(window[f].toString(), vistos).forEach(x => k.add(x));
        }
        return k; };
      const calculado = k => OBLIG[k] && OBLIG[k].cond_txt && OBLIG[k].cond_txt.indexOf('No se pregunta') === 0;
      const gobiernan = new Set();
      Object.values(OBLIG).forEach(d => { if (d.cond) lee(d.cond.toString(), new Set()).forEach(k => { if (!calculado(k)) gobiernan.add(k); }); });
      const cubiertos = new Set(BIFURCACIONES.flatMap(b => b.campos || []));
      abreVariantes(); const tabla = document.getElementById('tablaVariantes').innerText;
      document.getElementById('modalVariantes').classList.remove('abierto');
      return {faltan: [...gobiernan].filter(k => !cubiertos.has(k)), gobiernan: gobiernan.size,
              ajenos: [...cubiertos].filter(k => !(k in OBLIG)), sinCampos: BIFURCACIONES.filter(b => !Array.isArray(b.campos)).map(b => b.pregunta),
              tabla, materias: MATERIAS.length, deriva: DERIVA.length, giros: TIPOS_ESTAB.length - 1}; }""")
    afirma(not ramas['faltan'], 'las %d respuestas que gobiernan condiciones de OBLIG tienen su renglón: faltan %s' % (ramas['gobiernan'], ramas['faltan']))
    afirma(not ramas['ajenos'] and not ramas['sinCampos'], 'cada renglón declara sus campos y todos existen: %s %s' % (ramas['ajenos'], ramas['sinCampos']))
    conteos = '%d materias · %d supuestos de otra autoridad' % (ramas['materias'], ramas['deriva'])
    afirma(conteos in ramas['tabla'] and ('%d giros' % ramas['giros']) in ramas['tabla'] and '{' not in ramas['tabla'],
           'el panel dice «%s» y «%d giros», calculados de los catálogos' % (conteos, ramas['giros']))
    d10 = DOC10.read_text(encoding='utf-8')
    afirma(conteos in d10 and ('%d giros' % ramas['giros']) in d10 and '{materias}' not in d10,
           'y el documento 10 dice lo mismo')
    afirma('Desde cuándo ocurre' not in d10.split('## 3.')[0], 'la temporalidad ya no aparece como rama: no cambia el formulario')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])

    # ---- 3. La fecha de recepción, con la hora de la Ciudad (D2-03) ----
    #    31 de diciembre de 2026 a las 23:30 en la Ciudad (UTC-6) son las 05:30
    #    del 1 de enero en UTC; se prueba con el equipo en Tokio y en Los Ángeles.
    for zona in ('Asia/Tokyo', 'America/Los_Angeles'):
        cx = nav.new_context(viewport={'width':1200,'height':900}, timezone_id=zona)
        pz = cx.new_page(); pz.clock.set_fixed_time('2027-01-01T05:30:00Z')
        pz.goto(TMP.as_uri()); pz.wait_for_timeout(600)
        f = pz.evaluate("""() => { cargaEscenario('urbano'); guarda('verificacion','si'); irA(6); enviar();
          return {iso: val('fecha_acuse'), folio: val('folio'), txt: document.getElementById('app').innerText,
                  equipo: new Date().getFullYear()}; }""")
        afirma(f['iso'] == '2026-12-31T23:30:00-06:00', '%s: la recepción se guarda en ISO con la hora y la zona de la Ciudad: %s' % (zona, f['iso']))
        afirma(f['folio'].startswith('SEDEMA/DEN/2026/'), '%s: el folio es de 2026, aunque el equipo diga %d: %s' % (zona, f['equipo'], f['folio']))
        afirma('Recibida el 31 de diciembre de 2026, 23:30 horas' in f['txt'], '%s: la pantalla lo dice en palabras' % zona)
        cx.close()
    nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
