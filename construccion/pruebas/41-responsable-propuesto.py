# -*- coding: utf-8 -*-
"""El responsable que propone el formulario se retira si ya no aplica (DEC-238).

   Con «Sí» en «¿Los hechos ocurren dentro de un establecimiento?», el
   formulario propone «Una empresa o negocio» en «¿Quién es responsable de los
   hechos?» (DEC-26). Liber Saltijeral marcó «Sí», luego «No», y la empresa
   siguió elegida sin que nadie la hubiera elegido. Se comprueba, con clics
   como los de una persona, que la propuesta se retira al cambiar a «No» y que
   lo que la persona eligió ella misma no se toca."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina41.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    def nuevo():
        pg.evaluate("() => { estado = {}; responsableHeredado = false; guarda('materia','emisiones'); guarda('tiene_direccion','si'); irA(3); }")
        pg.wait_for_timeout(100)
    def estab(r):
        pg.locator('#c_es_estab button', has_text=r).first.click(); pg.wait_for_timeout(100)
    def elige(v):
        pg.select_option('#f_tipo_denunciado', v); pg.wait_for_timeout(100)
    lista = lambda: pg.evaluate("() => ({dato: val('tipo_denunciado'), lista: document.getElementById('f_tipo_denunciado').value})")

    nuevo()
    afirma(lista()['dato'] == '', 'al empezar no hay responsable elegido')
    estab('Sí')
    afirma(lista() == {'dato': 'empresa', 'lista': 'empresa'}, 'con «Sí» se propone «Una empresa o negocio» (DEC-26)')
    estab('No')
    afirma(lista() == {'dato': '', 'lista': ''}, 'con «Sí» y luego «No», la propuesta se retira: %s' % lista())
    estab('Sí')
    afirma(lista()['dato'] == 'empresa', 'y vuelve a proponerse si se regresa a «Sí»')

    nuevo(); estab('Sí'); elige('empresa'); estab('No')
    afirma(lista()['dato'] == 'empresa', 'si la persona confirma «Una empresa o negocio» en la lista, «No» no se la quita')
    nuevo(); estab('Sí'); elige('particular'); estab('No')
    afirma(lista()['dato'] == 'particular', 'si la cambia por «Una persona», «No» tampoco la toca')
    nuevo(); estab('No'); elige('empresa'); estab('Sí'); estab('No')
    afirma(lista()['dato'] == 'empresa', 'lo elegido antes de responder «Sí» se conserva')

    pg.evaluate("() => { cargaEscenario('urbano'); irA(3); }"); pg.wait_for_timeout(150)
    estab('No')
    afirma(lista()['dato'] == 'empresa', 'en un escenario que ya trae la empresa elegida, «No» no la quita')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
