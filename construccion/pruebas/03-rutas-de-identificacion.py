# -*- coding: utf-8 -*-
"""Bloque D: las tres rutas de identificacion."""
import os, pathlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
import sys
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':844}).new_page()
    err=[]
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    pg.evaluate("cfg.validar=true; cfg.ident='B'; irA(5)"); pg.wait_for_timeout(400)

    # 1. Tres opciones, y ninguna elegida de entrada
    o = pg.evaluate("""() => {
      const b=[...document.querySelectorAll('.opcion')];
      return {n:b.length, nombres:b.map(x=>x.querySelector('.nombre').textContent.trim()),
              elegida:b.filter(x=>x.getAttribute('aria-pressed')==='true').length,
              campos:document.querySelectorAll('#app .campo input[type=text], #app .campo input[type=email]').length};
    }""")
    afirma(o['n']==3, 'la variante B ofrece tres rutas (%s)' % o['nombres'])
    afirma(o['elegida']==0, 'ninguna viene elegida de entrada: la decisión es de la persona')
    afirma(o['campos']==0, 'mientras no se elige ruta no se pide ningún dato (%d campos)' % o['campos'])

    # 2. La eleccion es obligatoria
    afirma(pg.evaluate("()=>valida(5)") is False, 'sin elegir ruta, el paso no avanza')
    afirma(pg.evaluate("()=>esObligatorio('identificacion')") is True, 'la elección está declarada obligatoria en OBLIG')

    # 3. Ruta de datos escritos
    pg.evaluate("guarda('identificacion','nombre'); render()"); pg.wait_for_timeout(300)
    afirma(pg.locator('#f_nombre').count()==1, 'ruta «escribo mis datos»: aparecen los campos')
    afirma(pg.evaluate("()=>valida(5)") is False, 'y con los campos vacíos no avanza')

    # 4. Ruta de cuenta
    pg.evaluate("guarda('identificacion','llave'); ['nombre','apellido_paterno','correo','telefono'].forEach(k=>guarda(k,'')); render()")
    pg.wait_for_timeout(300)
    antes = pg.evaluate("""() => ({campos: document.querySelectorAll('#f_nombre').length,
      boton: [...document.querySelectorAll('button')].some(b=>b.textContent.includes('Entrar con Llave CDMX')),
      simulada: document.getElementById('app').innerText.includes('Cuenta simulada'),
      chip: [...document.querySelectorAll('#app .pendiente')].some(e=>e.textContent.includes('Llave CDMX'))})""")
    afirma(antes['campos']==0, 'ruta de cuenta: antes de entrar no se piden datos')
    afirma(antes['boton'], 'se ofrece el botón de entrar con Llave CDMX')
    afirma(antes['simulada'], 'la pantalla advierte que la cuenta es simulada')
    afirma(antes['chip'], 'y lo dice con la marca de pendiente, como el resto de lo que falta (DEC-94)')

    pg.locator('button', has_text='Entrar con Llave CDMX').click(); pg.wait_for_timeout(400)
    dsp = pg.evaluate("""() => ({sesion: val('sesion_llave'), nombre: val('nombre'), correo: val('correo'),
      campos: document.querySelectorAll('#f_nombre').length,
      salir: [...document.querySelectorAll('button')].some(b=>b.textContent.includes('Salir de la cuenta'))})""")
    afirma(dsp['sesion']=='si' and dsp['nombre']!='', 'al entrar, los datos se llenan solos (%s)' % dsp['nombre'])
    afirma(dsp['campos']==1, 'y quedan visibles y corregibles, no ocultos')
    afirma(dsp['salir'], 'se puede salir de la cuenta')

    r = pg.evaluate("""() => { guarda('notif_correo','si'); guarda('reserva','si'); guarda('privacidad','si');
        return {pasa: valida(5)}; }""")
    afirma(r['pasa'] is True, 'con la cuenta, el paso 5 se completa sin escribir nada a mano')

    pg.locator('button', has_text='Salir de la cuenta').click(); pg.wait_for_timeout(350)
    afirma(pg.evaluate("()=>val('nombre')")=='' and pg.evaluate("()=>val('sesion_llave')")=='',
           'al salir, los datos de la cuenta no se quedan pegados')

    # 5. Ruta anonima
    pg.evaluate("guarda('identificacion','anonima'); render()"); pg.wait_for_timeout(300)
    an = pg.evaluate("""() => ({campos: document.querySelectorAll('#f_nombre').length,
      aviso: document.getElementById('app').innerText.includes('sin datos de contacto'),
      pasa: (guarda('privacidad','si'), valida(5))})""")
    afirma(an['campos']==0, 'ruta anónima: no se pide ningún dato')
    afirma(an['aviso'], 'y se advierte qué se pierde')
    afirma(an['pasa'] is True, 'la denuncia anónima puede enviarse')

    # 6. Variante C: sin anonimato, pero con las dos formas de identificarse
    pg.evaluate("cfg.ident='C'; guarda('identificacion',''); render()"); pg.wait_for_timeout(300)
    c = pg.evaluate("""() => {
      const b=[...document.querySelectorAll('.opcion')];
      return {n:b.length, nombres:b.map(x=>x.querySelector('.nombre').textContent.trim())};
    }""")
    afirma(c['n']==2 and not any('anónima' in x.lower() for x in c['nombres']),
           'variante C: quedan las dos rutas identificadas y desaparece la anónima (%s)' % c['nombres'])
    pg.evaluate("cfg.ident='B'")

    # 7. El resumen dice si la identidad esta acreditada
    pg.evaluate("""() => { guarda('identificacion','llave'); guarda('sesion_llave','si');
        guarda('nombre','Maria'); guarda('apellido_paterno','Ramirez'); irA(6); }""")
    pg.wait_for_timeout(350)
    t = pg.locator('#app').inner_text()
    afirma('Acreditada con cuenta Llave CDMX' in t, 'el resumen distingue la identidad acreditada')
    pg.evaluate("guarda('identificacion','nombre'); guarda('sesion_llave',''); render()"); pg.wait_for_timeout(300)
    afirma('sin acreditación' in pg.locator('#app').inner_text(), 'y distingue la que no lo está')

    # 8. Los tres escenarios de prueba
    esc = pg.evaluate("""() => ESCENARIOS.map(e => ({n: e.nom || '', ident: (e.e||{}).identificacion}))""")
    afirma(any(x['ident']=='llave' for x in esc) and any(x['ident']=='anonima' for x in esc) and any(x['ident']=='nombre' for x in esc),
           'hay un escenario de prueba por cada ruta (%s)' % [x['ident'] for x in esc])

    # 9. Recorrido completo
    for n in range(0,8):
        pg.evaluate("irA(%d)" % n); pg.wait_for_timeout(220)
        afirma(pg.locator('#app').inner_html().strip()!='', 'el paso %d renderiza' % n)
    afirma(err==[], 'sin errores propios en consola: %s' % err[:3])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
