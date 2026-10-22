# -*- coding: utf-8 -*-
"""Maqueta del módulo de administración: la cuenta, arriba a la derecha
   (DEC-260).

   1. Cada perfil tiene una cuenta activa de prueba, y el botón de la esquina
      de arriba a la derecha la muestra con su foto —las iniciales, en la
      maqueta— y su nombre para el lector de pantalla; al cambiar de perfil,
      cambia.
   2. El botón abre un panel con los datos de la cuenta: nombre, correo,
      perfil, dirección general, área de la que depende y cargo, los mismos
      del personal registrado.
   3. Se cierra con el botón, con Escape —y el foco vuelve al botón— o con un
      clic fuera; el botón dice si está abierto.
   4. En teléfono el panel cabe en la pantalla y nada se desplaza a lo ancho;
      sin errores en consola."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
# Lo único que la maqueta pide a internet son las tipografías; si no cargan, no
# es un error de la maqueta. Chrome no pone la dirección en el texto del aviso:
# se lee de su ubicación.
TIPOGRAFIAS = ('https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')

LEE = """() => { const b = document.querySelector('.usuario-boton'), p = document.getElementById('usuario-panel');
  return {avatar: b.querySelector('.avatar').textContent, nombre: b.title, etiqueta: b.getAttribute('aria-label'),
    expandido: b.getAttribute('aria-expanded'), abierto: !p.hidden, titulo: p.querySelector('.usuario-titulo').textContent,
    correo: p.querySelector('.dato-sec').textContent,
    pares: Object.fromEntries([...p.querySelectorAll('.ficha > div')].map(x => [x.querySelector('dt').textContent, x.querySelector('dd').textContent]))}; }"""

def iniciales(nombre):
    return ''.join(w[0] for w in nombre.split() if w[0].isupper())[:2]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1280,'height':900}).new_page()
    err = []
    pg.on('console', lambda x: err.append(x.text) if x.type == 'error' and not (x.location or {}).get('url', '').startswith(TIPOGRAFIAS) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(MAQUETA.as_uri()); pg.wait_for_timeout(500)
    perfiles = pg.evaluate("() => PERFILES.map(p => ({id: p.id, nom: p.nom, rol: p.rol, area: p.area || ''}))")
    personal = pg.evaluate("() => PERSONAL")

    # ---- 1 y 2. Cada perfil, su cuenta y sus datos ----
    malos = []
    for p in perfiles:
        pg.evaluate("(id) => { document.getElementById('perfil').value = id; cambiaPerfil(id); }", p['id']); pg.wait_for_timeout(60)
        c = next((x for x in personal if x['perfil'] == p['rol'] and x['dg'] == p['area'] and x['activa']), None)
        pg.click('.usuario-boton'); pg.wait_for_timeout(40)
        v = pg.evaluate(LEE)
        esperado = c and {'avatar': iniciales(c['nombre']), 'nombre': c['nombre'], 'etiqueta': 'Cuenta: ' + c['nombre'], 'expandido': 'true', 'abierto': True,
                          'titulo': c['nombre'], 'correo': c['correo'],
                          'pares': {'Perfil': p['nom'], 'Dirección general': c['dg'] or 'Toda la Secretaría', 'Área de la que depende': c['area'], 'Cargo': c['cargo']}}
        if v != esperado: malos.append((p['id'], v, esperado))
        pg.click('.usuario-boton'); pg.wait_for_timeout(40)
    afirma(not malos, 'cada perfil tiene su cuenta: el botón muestra las iniciales y lleva el nombre, y el panel sus datos —perfil, dirección general, área, cargo y correo—: %s' % malos[:1])
    esquina = pg.evaluate("() => { const b = document.querySelector('.usuario-boton').getBoundingClientRect(), h = document.querySelector('header.titulo').getBoundingClientRect(), t = document.querySelector('.titulo-txt').getBoundingClientRect(); return [b.top - h.top < 40, h.right - b.right < 140, b.left >= t.right || b.bottom <= t.top]; }")
    afirma(all(esquina), 'el botón está en la esquina de arriba a la derecha, sin encimarse al título: %s' % esquina)
    afirma(len({iniciales(x['nombre']) for x in personal}) > 1 and all(iniciales(x['nombre']) for x in personal), 'cada cuenta de prueba tiene sus iniciales en lugar de foto')

    # ---- 3. Cerrar ----
    pg.click('.usuario-boton'); pg.wait_for_timeout(40)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(40)
    r = pg.evaluate("() => [document.getElementById('usuario-panel').hidden, document.activeElement.classList.contains('usuario-boton'), document.querySelector('.usuario-boton').getAttribute('aria-expanded')]")
    afirma(r == [True, True, 'false'], 'Escape la cierra y el foco vuelve al botón: %s' % r)
    pg.click('.usuario-boton'); pg.wait_for_timeout(40)
    pg.click('#pantalla h2'); pg.wait_for_timeout(40)
    afirma(pg.evaluate("() => document.getElementById('usuario-panel').hidden"), 'un clic fuera la cierra')
    afirma(err == [], 'sin errores en consola: %s' % err[:2])

    # ---- 4. Teléfono ----
    tel = nav.new_context(viewport={'width':360,'height':760}).new_page()
    tel.goto(MAQUETA.as_uri()); tel.wait_for_timeout(400)
    tel.click('.usuario-boton'); tel.wait_for_timeout(80)
    r = tel.evaluate("() => { const c = document.getElementById('usuario-panel').getBoundingClientRect(); return [c.left >= 0, c.right <= innerWidth, document.documentElement.scrollWidth - innerWidth]; }")
    afirma(r[0] and r[1] and r[2] <= 0, 'a 360 px el panel cabe en la pantalla y nada se desplaza a lo ancho: %s' % r)
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
