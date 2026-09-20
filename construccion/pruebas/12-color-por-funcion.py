# -*- coding: utf-8 -*-
"""Un color, un trabajo (DEC-95).

   El formulario llegó a tener treinta y dos valores de color en siete
   familias, once de ellos escritos sueltos fuera de la paleta. Peor que la
   cantidad era el reparto: el mismo ámbar servía para advertir a la persona
   y para marcar un pendiente de la Secretaría, que no se parecen en nada; el
   verde estaba en la barra de pasos, en los avisos de confirmación y en el
   acuse; y una familia entera —el morado— existía para una sola pantalla.

   Estas comprobaciones fijan el reparto, no el gusto: cada familia hace un
   solo trabajo y ninguna vive fuera de la paleta."""
import os, pathlib, sys, re, collections
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina12.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

FUENTE = RUTA.read_text(encoding='utf-8')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' + FUENTE + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# ---- 1. Ningún color vive fuera de la paleta ----
css = FUENTE[FUENTE.index('<style>'):FUENTE.index('</style>')]
ini = css.index(':root{'); fin = css.index('}', ini)
raiz, resto = css[ini:fin], css[:ini] + css[fin:]
sueltos = collections.Counter(re.findall(r'#[0-9A-Fa-f]{3,6}\b', resto))
afirma(not sueltos, 'ningún color escrito fuera de la paleta: %s' % dict(sueltos))

declarados = dict(re.findall(r'--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,6})', raiz))
afirma(len(declarados) <= 30, 'la paleta cabe en treinta valores (%d)' % len(declarados))
for v in ['error','pend','ok','azul','guinda','dorado']:
    afirma(v in declarados, 'la familia «%s» está declarada' % v)

# ---- 2. El morado desapareció ----
afirma('capas-federal' not in css, 'el morado del panel federal ya no existe')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    V = lambda n: pg.evaluate("(n)=>getComputedStyle(document.documentElement).getPropertyValue('--'+n).trim()", n)
    OK, PEND, ERROR, AZUL = V('ok'), V('pend'), V('error'), V('azul')

    def rgb(h):
        h = h.lstrip('#')
        return 'rgb(%d, %d, %d)' % tuple(int(h[i:i+2],16) for i in (0,2,4))

    # ---- 3. El verde sólo en el acuse ----
    r = pg.evaluate("""() => {
      cfg.validar = false;
      guarda('materia','rsu'); guarda('tiene_direccion','si');
      const verde = [];
      for(const n of [0,1,2,3,4,5,6]){
        irA(n);
        [...document.querySelectorAll('#app *')].forEach(e => {
          const c = getComputedStyle(e);
          [c.color, c.backgroundColor, c.borderLeftColor, c.borderTopColor].forEach(v => {
            if(v === 'rgb(27, 107, 67)') verde.push(n + ':' + e.className);
          });
        });
      }
      return [...new Set(verde)];
    }""")
    afirma(r == [], 'el verde no aparece en ninguno de los siete pasos: %s' % r[:4])

    ac = pg.evaluate("""() => {
      guarda('folio','X'); guarda('identificacion','nombre'); guarda('correo','a@b.mx'); irA(7);
      return [...document.querySelectorAll('#app *')].some(e => {
        const c = getComputedStyle(e);
        return [c.color, c.backgroundColor].includes('rgb(27, 107, 67)');
      });
    }""")
    afirma(ac, 'y sí aparece en el acuse, que es la pantalla que dice «recibida»')

    # ---- 4. El ámbar sólo marca pendientes ----
    am = pg.evaluate("""(pend) => {
      const fuera = [];
      for(const n of [0,1,2,3,4,5,6,7]){
        irA(n);
        [...document.querySelectorAll('#app *')].forEach(e => {
          const c = getComputedStyle(e);
          const usa = [c.color, c.backgroundColor, c.borderLeftColor, c.borderTopColor]
                        .some(v => v === pend);
          if(usa && !e.classList.contains('pendiente')) fuera.push(n + ':' + (e.className||e.tagName));
        });
      }
      return [...new Set(fuera)];
    }""", rgb(PEND))
    afirma(am == [], 'el ámbar sólo lo usa la marca de pendiente: %s' % am[:4])

    # ---- 5. La barra de pasos ya no usa color para decir «hecho» ----
    barra = pg.evaluate("""() => {
      guarda('materia','rsu'); irA(3);
      const h = document.querySelector('.progreso .etapa.hecha');
      if(!h) return null;
      const b = h.querySelector('.bolita');
      return {color: getComputedStyle(b).borderTopColor,
              palomita: b.textContent.trim(),
              etq: getComputedStyle(h.querySelector('.etq')).color};
    }""")
    afirma(barra is not None, 'hay pasos ya recorridos en la barra')
    if barra:
        afirma(barra['color'] != 'rgb(27, 107, 67)', 'el paso hecho no se marca en verde (%s)' % barra['color'])
        afirma(barra['palomita'] == '✓', 'lo dice la palomita, que no depende del color')

    # ---- 6. El azul sigue siendo lo elegido ----
    az = pg.evaluate("""(azul) => {
      cfg.validar = false; guarda('verificacion','si'); irA(6);
      const h = document.querySelector('.humano.listo');
      return h ? getComputedStyle(h).borderTopColor === azul : null;
    }""", rgb(AZUL))
    afirma(az is True, 'la prueba de humanidad marcada usa el azul de «elegido», no el verde')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
