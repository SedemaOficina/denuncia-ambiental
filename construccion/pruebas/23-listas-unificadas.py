# -*- coding: utf-8 -*-
"""Una sola lista desplegable en todo el formulario (DEC-126).

   Había tres aspectos: el <select> nativo, el <datalist> de la autoridad, que
   Chrome pinta en negro, y la lista propia de la colonia. Se vigila que:
   1. No quede ningún <datalist>.
   2. La autoridad use la misma lista que la colonia, con teclado y texto libre.
   3. Donde el navegador lo permite, el <select> dibuje su lista con el mismo
      fondo, borde, renglón y color de selección que la lista propia."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina23.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
FUENTE = RUTA.read_text(encoding='utf-8')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' + FUENTE + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

afirma("'<datalist" not in FUENTE and 'list="cat_' not in FUENTE, 'no queda ningún <datalist> en el formulario')

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1000,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- autoridad ----
    pg.evaluate("() => { estado={}; guarda('materia','rsu'); guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','alcaldia'); irA(3); }")
    pg.wait_for_timeout(300)
    a = pg.evaluate("""() => { const i = document.getElementById('f_autoridad_denunciada');
      return {rol: i.getAttribute('role'), list: i.getAttribute('list'), ctrl: i.getAttribute('aria-controls')}; }""")
    afirma(a['rol'] == 'combobox' and not a['list'] and a['ctrl'] == 'lista_autoridad_denunciada', 'la autoridad usa la lista del formulario, no un datalist')
    pg.click('#f_autoridad_denunciada'); pg.wait_for_timeout(150)
    n = pg.evaluate("() => document.querySelectorAll('#lista_autoridad_denunciada li[role=option]').length")
    afirma(n == 16, 'al entrar muestra las 16 alcaldías, como un desplegable (%d)' % n)
    pg.keyboard.type('coyo'); pg.wait_for_timeout(120)
    f = pg.evaluate("() => [...document.querySelectorAll('#lista_autoridad_denunciada .op-nom')].map(x=>x.textContent)")
    afirma(f == ['Coyoacán'], 'al escribir filtra sin importar acentos: %s' % f)
    pg.keyboard.press('ArrowDown'); pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
    afirma(pg.evaluate("() => val('autoridad_denunciada')") == 'Coyoacán', 'con flecha y Enter se elige')
    pg.fill('#f_autoridad_denunciada', 'Dirección de obras de la alcaldía'); pg.evaluate("() => document.getElementById('f_autoridad_denunciada').blur()")
    afirma(pg.evaluate("() => val('autoridad_denunciada')") == 'Dirección de obras de la alcaldía', 'y se puede escribir lo que no está en la lista')

    # ---- catálogos con nombre y sigla (DEC-160) ----
    cat = pg.evaluate("() => AUTORIDADES.cdmx.concat(AUTORIDADES.federal)")
    malos = [x for x in cat if ' — ' in x or (x[0].isupper() and x.split(' ')[0].isupper() and len(x.split(' ')[0]) > 1)]
    afirma(not malos, 'todas las dependencias se nombran «Nombre (SIGLA)», con el nombre primero: %s' % malos[:3])
    pg.evaluate("() => { estado={}; guarda('materia','rsu'); guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','federal'); irA(3); }")
    pg.wait_for_timeout(200)
    pg.click('#f_autoridad_denunciada'); pg.keyboard.type('conagua'); pg.wait_for_timeout(120)
    f = pg.evaluate("() => [...document.querySelectorAll('#lista_autoridad_denunciada .op-nom')].map(x=>x.textContent)")
    afirma(f == ['Comisión Nacional del Agua (CONAGUA)'], 'la sigla sigue encontrando la dependencia: %s' % f)
    pg.fill('#f_autoridad_denunciada', 'Instituto Nacional de Migración'); pg.wait_for_timeout(120)
    nota = pg.evaluate("() => { const u = document.getElementById('lista_autoridad_denunciada'); return u.hidden ? '' : u.innerText; }")
    afirma('No está en la lista: se guarda como lo escribiste' in nota, 'si no está, la lista lo dice en vez de desaparecer')
    pg.evaluate("() => document.getElementById('f_autoridad_denunciada').blur()")
    afirma(pg.evaluate("() => val('autoridad_denunciada')") == 'Instituto Nacional de Migración', 'y lo escrito se conserva')

    # ---- mismo aspecto ----
    pg.evaluate("() => { const i=document.getElementById('f_autoridad_denunciada'); i.value=''; guarda('autoridad_denunciada',''); i.focus(); pintaLista('autoridad_denunciada'); }")
    li = pg.evaluate("""() => { const l = document.querySelector('#lista_autoridad_denunciada li'); const c = getComputedStyle(l), u = getComputedStyle(l.parentElement);
      return {pad: c.padding, fondo: u.backgroundColor, borde: u.borderTopColor}; }""")
    soporta = pg.evaluate("() => CSS.supports('appearance','base-select')")
    if soporta:
        pg.evaluate("() => { estado={}; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2); }"); pg.wait_for_timeout(300)
        op = pg.evaluate("""() => { const s = document.getElementById('f_alcaldia_dir'); const o = s.options[1]; const c = getComputedStyle(o);
          return {ap: getComputedStyle(s).appearance, pad: c.padding}; }""")
        afirma(op['ap'] == 'base-select', 'el <select> se dibuja con la lista del formulario (%s)' % op['ap'])
        afirma(op['pad'] == li['pad'], 'sus renglones miden lo mismo que los de la lista propia (%s / %s)' % (op['pad'], li['pad']))
    else:
        notas.append('OK  (este navegador no dibuja el <select> a medida: queda el nativo, en claro)')
    raiz = pg.evaluate("() => getComputedStyle(document.documentElement).colorScheme")
    afirma('light' in raiz, 'la página se declara en claro, para que ninguna lista nativa salga en negro (%s)' % raiz)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
