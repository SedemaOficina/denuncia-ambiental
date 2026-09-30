# -*- coding: utf-8 -*-
"""Bloque D: las dos rutas de identificacion (DEC-130: se retira Llave CDMX)."""
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

    pg.evaluate("cfg.validar=true; irA(5)"); pg.wait_for_timeout(400)

    # 1. Dos opciones, y ninguna elegida de entrada
    o = pg.evaluate("""() => {
      const b=[...document.querySelectorAll('.opcion')];
      return {n:b.length, nombres:b.map(x=>x.querySelector('.nombre').textContent.trim()),
              elegida:b.filter(x=>x.getAttribute('aria-pressed')==='true').length,
              campos:document.querySelectorAll('#app .campo input[type=text], #app .campo input[type=email]').length};
    }""")
    afirma(o['n']==2 and o['nombres']==['Escribo mis datos','Denuncia anónima'], 'se ofrecen dos rutas: datos o anónima (%s)' % o['nombres'])
    afirma(o['elegida']==0, 'ninguna viene elegida de entrada: la decisión es de la persona')
    afirma(o['campos']==0, 'mientras no se elige ruta no se pide ningún dato (%d campos)' % o['campos'])

    # 2. La eleccion es obligatoria
    afirma(pg.evaluate("()=>valida(5)") is False, 'sin elegir ruta, el paso no avanza')
    afirma(pg.evaluate("()=>esObligatorio('identificacion')") is True, 'la elección está declarada obligatoria en OBLIG')

    # 3. Ruta de datos escritos
    pg.evaluate("guarda('identificacion','nombre'); render()"); pg.wait_for_timeout(300)
    afirma(pg.locator('#f_nombre').count()==1, 'ruta «escribo mis datos»: aparecen los campos')
    afirma(pg.evaluate("()=>valida(5)") is False, 'y con los campos vacíos no avanza')

    # 4. La cuenta Llave CDMX ya no existe (DEC-130)
    ll = pg.evaluate("""() => ({fn: ['conLlave','haySesion','entraConLlave','salirDeLlave'].filter(f => typeof window[f] === 'function'),
      derivado: typeof DERIVADOS !== 'undefined' && 'sesion_llave' in DERIVADOS,
      texto: document.getElementById('app').innerText.includes('Llave')})""")
    afirma(ll['fn'] == [] and not ll['derivado'] and not ll['texto'], 'no queda rastro de la cuenta Llave CDMX: %s' % ll)
    pg.evaluate("guarda('identificacion','llave'); render()"); pg.wait_for_timeout(300)
    mig = pg.evaluate("() => ({ident: val('identificacion'), campos: document.querySelectorAll('#f_nombre').length})")
    afirma(mig['ident']=='nombre' and mig['campos']==1, 'un borrador con la ruta retirada se abre como «Escribo mis datos» (%s)' % mig)

    # 5. Ruta anonima
    pg.evaluate("guarda('identificacion','anonima'); render()"); pg.wait_for_timeout(300)
    #    La anónima no pide nombre, pero sí un correo de contacto (DEC-119,
    #    DEC-120); el teléfono es opcional.
    an = pg.evaluate("""() => ({campos: document.querySelectorAll('#f_nombre').length,
      contacto: !!document.getElementById('f_correo') && !!document.getElementById('f_telefono'),
      sinCorreo: (guarda('privacidad','si'), guarda('correo',''), guarda('telefono',''), valida(5)),
      conCorreo: (guarda('correo','avisos@correo.mx'), valida(5))})""")
    afirma(an['campos']==0, 'ruta anónima: no se pide el nombre')
    afirma(an['contacto'], 'pero sí correo, y teléfono como opcional')
    afirma(an['sinCorreo'] is False, 'sin correo la anónima no avanza')
    afirma(an['conCorreo'] is True, 'con correo, y sin teléfono, se puede enviar')

    # 6. La denuncia anónima no depende de ninguna configuración (DEC-97)
    #    La variante C —identificación obligatoria— se retiró: quedó decidido
    #    que la denuncia puede ser anónima o identificada, y la bandera que
    #    permitía ocultar la ruta anónima desapareció con ella. Esta
    #    comprobación cuida que no vuelva por la puerta de atrás.
    c = pg.evaluate("""() => {
      guarda('identificacion',''); render();
      const b=[...document.querySelectorAll('.opcion')];
      return {n:b.length, nombres:b.map(x=>x.querySelector('.nombre').textContent.trim()),
              cfg: Object.keys(cfg)};
    }"""); pg.wait_for_timeout(300)
    afirma(c['n']==2 and any('anónima' in x.lower() for x in c['nombres']),
           'las dos rutas se ofrecen siempre, sin configuración que las cambie (%s)' % c['nombres'])
    afirma('ident' not in c['cfg'],
           'el panel ya no lleva la variante de identificación: %s' % c['cfg'])

    # 7. El resumen dice quién denuncia, sin hablar de acreditación (DEC-130)
    pg.evaluate("""() => { guarda('identificacion','nombre');
        guarda('nombre','Maria'); guarda('apellido_paterno','Ramirez'); irA(6); }""")
    pg.wait_for_timeout(350)
    t = pg.locator('#app').inner_text()
    afirma('Maria Ramirez' in t and 'acredit' not in t.lower(), 'el resumen dice el nombre y no habla de acreditación')

    # 8. Los escenarios de prueba
    esc = pg.evaluate("""() => ESCENARIOS.map(e => ({n: e.nom || '', ident: (e.e||{}).identificacion}))""")
    afirma(any(x['ident']=='anonima' for x in esc) and any(x['ident']=='nombre' for x in esc) and not any(x['ident']=='llave' for x in esc),
           'hay un escenario de prueba por cada ruta, y ninguno con la retirada (%s)' % [x['ident'] for x in esc])

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
