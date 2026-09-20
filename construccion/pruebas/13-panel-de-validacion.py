# -*- coding: utf-8 -*-
"""El panel de validación, después de simplificarlo (DEC-97).

   El panel había crecido hasta guardar decisiones que ya estaban tomadas:
   una variante de identificación obligatoria descartada hace tiempo y un
   conmutador entre el «esquema DGIVA» y el «formato vigente», de cuando el
   formulario se presentaba a una sola Dirección General. Hoy el formulario
   es de la Secretaría y tiene un solo conjunto de campos obligatorios.

   Esta batería cuida tres cosas: que el panel no reintroduzca aquellas
   variantes; que la obligatoriedad la gobierne **una sola bandera** del
   catálogo, sin rastro de la del formato de 2016 (DEC-99); y que **todo
   campo obligatorio lleve su marca en pantalla**, en cualquiera de los
   constructores de campo."""
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
      const restos   = k.filter(x => 'dgiva' in OBLIG[x] || 'vigente' in OBLIG[x]);
      cfg.validar = false;
      const apagado = k.filter(esObligatorio).length;
      cfg.validar = true;
      const encendido = k.filter(esObligatorio);
      return {n:k.length, sinOblig, restos, apagado,
              encendido: encendido.length,
              coincide: encendido.every(x => OBLIG[x].oblig)};
    }""")
    afirma(b['restos'] == [], 'ningún campo conserva una bandera vieja —dgiva o vigente—: %s' % b['restos'])
    afirma(b['sinOblig'] == [], 'los %d campos declaran su obligatoriedad: %s' % (b['n'], b['sinOblig']))
    afirma(b['apagado'] == 0, 'con la validación apagada no se exige nada (%d)' % b['apagado'])
    afirma(b['encendido'] > 0 and b['coincide'],
           'encendida, se exige lo que declara «oblig» y nada más (%d campos)' % b['encendido'])

    # ---- 4. Forzar una bandera que ya no existe no cambia nada ----
    v = pg.evaluate("""() => {
      const k = Object.keys(OBLIG);
      const antes = k.filter(esObligatorio).join(',');
      cfg.esquema = 'vigente';                 /* la bandera que ya no existe */
      const despues = k.filter(esObligatorio).join(',');
      delete cfg.esquema;
      return antes === despues;
    }""")
    afirma(v, 'forzar el esquema retirado no cambia lo que el formulario exige')
    m2016 = pg.evaluate("""() => { abreMapeo();
      const c = document.getElementById('modalMapeo');
      const th = [...c.querySelectorAll('thead th')].map(x => x.textContent.trim());
      const cols = c.querySelector('tbody tr:not([style]) td') ? 0 : 0;
      const filas = [...c.querySelectorAll('tbody tr')].map(r => r.children.length);
      const txt = c.innerText;
      c.classList.remove('abierto');
      return {th, filas: [...new Set(filas)], hay2016: /2016|vigente/i.test(txt)}; }""")
    afirma(not m2016['hay2016'],
           'el mapeo no menciona el formato de 2016 en ninguna parte')
    afirma('Formato de 2016' not in m2016['th'] and len(m2016['th']) == 4,
           'y su tabla quedó en cuatro columnas: %s' % m2016['th'])
    afirma(m2016['filas'] == [4] or m2016['filas'] == [1, 4] or m2016['filas'] == [4, 1],
           'todos los renglones tienen el mismo número de celdas: %s' % m2016['filas'])

    # ---- 5. La leyenda de pantalla ya no habla de esquemas ----
    leyenda = pg.evaluate("""() => { cfg.validar = true; guarda('materia','rsu');
      guarda('tiene_direccion','si'); irA(2);
      const l = document.querySelector('.leyenda-oblig');
      return l ? l.innerText : ''; }""")
    pg.wait_for_timeout(250)
    afirma('obligatorios' in leyenda and 'esquema' not in leyenda,
           'la leyenda dice sólo que son obligatorios: %r' % leyenda)

    # ---- 6. Todo campo obligatorio lleva su marca en pantalla ----
    #    El asterisco lo ponía cada constructor por su cuenta, y los dos que no
    #    son <input> —las preguntas de sí o no y la hora— se quedaron sin él:
    #    «¿El lugar tiene calle y número?» es obligatoria y no lo decía. Esto
    #    recorre los cinco pasos con la validación encendida y exige, para cada
    #    campo que en ese momento sea obligatorio, la marca y su texto para
    #    lector de pantalla (DEC-99).
    sinMarca, sinError = [], []
    for n in (1, 2, 3, 4, 5):
        d = pg.evaluate("""(n) => {
          cfg.validar = true;
          guarda('materia','tala'); guarda('tiene_direccion','si');
          guarda('tipo_denunciado','empresa'); guarda('identificacion','nombre');
          guarda('notif_correo','no');
          irA(n);
          const out = {marca: [], err: []};
          Object.keys(OBLIG).forEach(k => {
            if(OBLIG[k].p !== n || !esObligatorio(k)) return;
            const c = document.getElementById('c_' + k);
            if(!c) return;                       /* no se rinde en esta ruta */
            const req = c.querySelector('.req');
            const lec = c.querySelector('.solo-lector');
            if(!req || !lec || lec.textContent.indexOf('obligatorio') < 0) out.marca.push(k);
            if(!c.querySelector('.err')) out.err.push(k);
          });
          return out;
        }""", n)
        pg.wait_for_timeout(120)
        sinMarca += d['marca']; sinError += d['err']
    afirma(sinMarca == [], 'todo campo obligatorio lleva asterisco y su «(obligatorio)» para lector: %s' % sinMarca)
    afirma(sinError == [], 'y todo campo obligatorio tiene dónde mostrar su error: %s' % sinError)

    # Y lo contrario: la marca no aparece donde no toca.
    demas = pg.evaluate("""() => {
      cfg.validar = true; irA(3);
      return Object.keys(OBLIG).filter(k => {
        if(OBLIG[k].p !== 3 || esObligatorio(k)) return false;
        const c = document.getElementById('c_' + k);
        return c && c.querySelector('.req');
      });
    }"""); pg.wait_for_timeout(120)
    afirma(demas == [], 'y ningún campo opcional la lleva: %s' % demas)

    # ---- 6 bis. El resumen de errores nombra el campo como la pantalla ----
    r = pg.evaluate("""() => {
      cfg.validar = true; estado = {}; archivos = [];
      guarda('materia','tala'); guarda('tiene_direccion','si');
      irA(2); valida(2);
      const c = document.getElementById('resumenErrores');
      if(!c) return null;
      const ren = [...c.querySelectorAll('li a')].map(a => a.textContent.trim());
      const punto = [...c.querySelectorAll('li a')].find(a => /punto/i.test(a.textContent));
      if(punto) punto.click();
      return {ren, mapa: !!document.getElementById('mapa'),
              foco: document.activeElement ? document.activeElement.id : ''};
    }"""); pg.wait_for_timeout(300)
    afirma(r is not None, 'el resumen de errores aparece')
    if r:
        sucios = [x for x in r['ren'] if '*' in x or 'obligatorio' in x.lower()]
        afirma(sucios == [], 'ningún renglón arrastra «* (obligatorio)»: %s' % sucios)
        afirma(any('unto' in x for x in r['ren']), 'el punto del mapa se lista: %s' % r['ren'])
        afirma(r['foco'] == 'mapa', 'y su renglón lleva al mapa, no a un ancla inexistente: %r' % r['foco'])

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
