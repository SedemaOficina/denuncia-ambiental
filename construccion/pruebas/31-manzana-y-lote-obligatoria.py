# -*- coding: utf-8 -*-
"""La pregunta de manzana y lote es obligatoria, en el lugar y en el domicilio (DEC-198).
   Sin respuesta no se avanza; con «Sí» se exige al menos la manzana y el lote
   es opcional (DEC-199); con «No», ninguno.
   Se comprueba en pantalla (marca y error) y en la validación del paso."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina31.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho in (1200, 390):
        pg = nav.new_context(viewport={'width': ancho, 'height': 900}).new_page()
        err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
        for pre, paso, esc in (('', 2, 'urbano'), ('dom_', 5, 'urbano')):
            k = pre + 'tiene_mz_lote'
            r = pg.evaluate("""([k, pre, paso, esc]) => {
              cargaEscenario(esc); cfg.validar = true; irA(paso);
              const c = document.getElementById('c_' + k);
              const marca = c ? c.querySelector('.req') !== null && !c.innerText.includes('(opcional)') : null;
              guarda(k, ''); render();
              const sinResp = valida(paso);
              const conError = (document.getElementById('c_' + k) || {}).className || '';
              guarda(k, 'si'); guarda(pre + 'manzana', ''); guarda(pre + 'lote', ''); render();
              const mzMarca = ['manzana', 'lote'].map(x => { const e = document.getElementById('c_' + pre + x); return !!e && !!e.querySelector('.req'); });
              const siVacio = valida(paso);
              guarda(pre + 'manzana', '118'); render();
              const siLleno = valida(paso);   /* sin lote: opcional desde DEC-199 */
              guarda(k, 'no'); actualizaMzLote(pre); render();
              const no = valida(paso);
              return {marca, sinResp, conError, mzMarca, siVacio, siLleno, no, sueltos: [val(pre + 'manzana'), val(pre + 'lote')]};
            }""", [k, pre, paso, esc])
            lugar = 'lugar' if not pre else 'domicilio'
            afirma(r['marca'], '%d px · %s: la pregunta lleva asterisco y no dice «(opcional)»' % (ancho, lugar))
            afirma(r['sinResp'] is False and 'invalido' in r['conError'], '%d px · %s: sin respuesta no se avanza y el campo marca el error (%s)' % (ancho, lugar, r['conError']))
            afirma(r['mzMarca'] == [True, False], '%d px · %s: con «Sí», la manzana lleva asterisco y el lote no (DEC-199)' % (ancho, lugar))
            afirma(r['siVacio'] is False and r['siLleno'] is True, '%d px · %s: con «Sí» se exige la manzana; el lote no' % (ancho, lugar))
            afirma(r['no'] is True and r['sueltos'] == ['', ''], '%d px · %s: con «No» se avanza y manzana y lote se sueltan' % (ancho, lugar))
        sin = pg.evaluate("""() => { cargaEscenario('sin_calle'); cfg.validar = true; irA(2); return {pide: !!document.getElementById('c_tiene_mz_lote'), pasa: valida(2)}; }""")
        afirma(not sin['pide'] and sin['pasa'], '%d px: sin domicilio la pregunta no aparece ni se exige' % ancho)
        afirma(not err, '%d px: sin errores en consola %s' % (ancho, err[:2]))
        pg.close()
    nav.close()
try: TMP.unlink()
except OSError: pass
for n in notas + fallos: print(n)
sys.exit(1 if fallos else 0)
