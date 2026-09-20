# -*- coding: utf-8 -*-
"""El panel de validación, después de simplificarlo (DEC-97).

   El panel había crecido hasta guardar decisiones que ya estaban tomadas:
   una variante de identificación obligatoria descartada hace tiempo y un
   conmutador entre el «esquema DGIVA» y el «formato vigente», de cuando el
   formulario se presentaba a una sola Dirección General. Hoy el formulario
   es de la Secretaría y tiene un solo conjunto de campos obligatorios.

   Esta batería cuida tres cosas: que el panel no reintroduzca aquellas
   variantes; que la obligatoriedad la gobierne **una sola bandera** del
   catálogo; y que lo que pedía el formato de 2016 siga registrado como dato
   documental, sin cambiar el comportamiento de nada."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina13.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. Qué quedó en el panel ----
    pg.locator('#panel .toggle').click(); pg.wait_for_timeout(250)
    d = pg.evaluate("""() => {
      const c = document.querySelector('#panel .cuerpo');
      return {
        texto: c.innerText,
        controles: [...c.querySelectorAll('input')].map(x => x.id || x.name),
        botones: [...c.querySelectorAll('button')].map(x => x.textContent.trim()),
        cabeza: (c.querySelector('.nota-cabeza') || {}).innerText || '',
        primero: c.firstElementChild.className,
        claves: Object.keys(cfg)
      };
    }""")
    afirma('vIdent' not in d['controles'],
           'la variante de identificación obligatoria ya no está: %s' % d['controles'])
    afirma('cfgEsq' not in d['controles'],
           'el conmutador de esquemas ya no está: %s' % d['controles'])
    afirma(sorted(d['controles']) == ['cfgLimite','cfgTriage','cfgVal'],
           'quedan tres interruptores, uno por comportamiento: %s' % sorted(d['controles']))
    afirma(sorted(d['claves']) == ['limite','triage','validar'],
           'y la configuración lleva exactamente esas tres claves: %s' % sorted(d['claves']))
    # «DGIVA» sigue apareciendo en la descripción de dos escenarios, y ahí es
    # correcto: nombra al área que atiende el caso, no un esquema de campos.
    afirma('Esquema DGIVA' not in d['texto'] and 'esquema' not in d['texto'].lower(),
           'ya no se habla de esquemas de campos en el panel')
    afirma('Identificación obligatoria' not in d['texto'] and 'Formato vigente' not in d['texto'],
           'ni de las dos variantes retiradas')

    # ---- 2. La nota explicativa, al principio y a nombre de la Secretaría ----
    afirma(d['primero'] == 'nota-cabeza', 'la nota abre el panel, no lo cierra: %r' % d['primero'])
    afirma('Secretaría' in d['cabeza'], 'la nota es de la Secretaría: %r' % d['cabeza'][:60])
    afirma('no forma parte del formulario' in d['cabeza'] and 'no se publica' in d['cabeza'],
           'y dice lo que importa: que no es parte del formulario ni se publica')

    # ---- 3. Una sola bandera gobierna la obligatoriedad ----
    b = pg.evaluate("""() => {
      const k = Object.keys(OBLIG);
      const sinOblig = k.filter(x => typeof OBLIG[x].oblig !== 'boolean');
      const sinVig   = k.filter(x => typeof OBLIG[x].vigente !== 'boolean');
      const restos   = k.filter(x => 'dgiva' in OBLIG[x]);
      cfg.validar = false;
      const apagado = k.filter(esObligatorio).length;
      cfg.validar = true;
      const encendido = k.filter(esObligatorio);
      return {n:k.length, sinOblig, sinVig, restos, apagado,
              encendido: encendido.length,
              coincide: encendido.every(x => OBLIG[x].oblig)};
    }""")
    afirma(b['restos'] == [], 'ningún campo conserva la bandera vieja: %s' % b['restos'])
    afirma(b['sinOblig'] == [], 'los %d campos declaran su obligatoriedad: %s' % (b['n'], b['sinOblig']))
    afirma(b['apagado'] == 0, 'con la validación apagada no se exige nada (%d)' % b['apagado'])
    afirma(b['encendido'] > 0 and b['coincide'],
           'encendida, se exige lo que declara «oblig» y nada más (%d campos)' % b['encendido'])

    # ---- 4. El formato de 2016 se conserva, pero no manda ----
    afirma(b['sinVig'] == [],
           'cada campo sigue registrando qué pedía el formato de 2016: %s' % b['sinVig'])
    v = pg.evaluate("""() => {
      const k = Object.keys(OBLIG);
      const antes = k.filter(esObligatorio).join(',');
      cfg.esquema = 'vigente';                 /* la bandera que ya no existe */
      const despues = k.filter(esObligatorio).join(',');
      delete cfg.esquema;
      return antes === despues;
    }""")
    afirma(v, 'y ese dato no cambia lo que el formulario exige, aunque se intente forzarlo')

    # ---- 5. La leyenda de pantalla ya no habla de esquemas ----
    leyenda = pg.evaluate("""() => { cfg.validar = true; guarda('materia','rsu');
      guarda('tiene_direccion','si'); irA(2);
      const l = document.querySelector('.leyenda-oblig');
      return l ? l.innerText : ''; }""")
    pg.wait_for_timeout(250)
    afirma('obligatorios' in leyenda and 'esquema' not in leyenda,
           'la leyenda dice sólo que son obligatorios: %r' % leyenda)

    # ---- 6. El mapeo distingue lo vigente de lo documental ----
    m = pg.evaluate("""() => { abreMapeo();
      const c = document.getElementById('modalMapeo');
      const th = [...c.querySelectorAll('thead th')].map(x => x.textContent.trim());
      return {th, nota: c.querySelector('.nota-gris').innerText, abierto: c.classList.contains('abierto')}; }""")
    afirma(m['abierto'], 'el mapeo sigue abriéndose desde el panel')
    afirma('En este formulario' in m['th'] and 'Formato de 2016' in m['th'],
           'y sus columnas separan lo que se exige de lo que se guarda como referencia: %s' % m['th'])
    afirma('no cambia el comportamiento' in m['nota'],
           'la nota lo dice con todas sus letras')

    # ---- 7. Los escenarios siguen cargando ----
    esc = pg.evaluate("""() => {
      document.getElementById('modalMapeo').classList.remove('abierto');
      return ESCENARIOS.map(e => e.id); }""")
    afirma('vigente_vacio' not in esc and 'dgiva_vacio' not in esc,
           'se fueron los dos escenarios que sólo servían para comparar esquemas: %s' % esc)
    afirma('vacio' in esc, 'y queda uno solo que muestra qué exige cada paso')
    rotos = []
    for i in esc:
        r = pg.evaluate("""(id) => { try { cargaEscenario(id);
          return document.getElementById('app').innerText.length > 40; }
          catch(e){ return String(e); } }""", i)
        if r is not True: rotos.append((i, r))
    afirma(rotos == [], 'los %d escenarios cargan sin romperse: %s' % (len(esc), rotos))

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
