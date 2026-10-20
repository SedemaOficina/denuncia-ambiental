# -*- coding: utf-8 -*-
"""Medios de presentación de PROFEPA, PAOT e INVEA en las derivaciones (DEC-197).
   Se comprueba en pantalla: cada supuesto que deriva a una de las tres muestra
   sus medios y sus ligas, ya no la marca «por confirmar», y los datos salen de
   una sola fuente (CONTACTOS)."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina30.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
ESPERA = {
  'd_silvestre':      {'profepa': ['haz_tu_denuncia.html', 'denuncia-ante-la-profepa', 'tel:8007763372', 'denuncias@profepa.gob.mx', 'Félix Cuevas 6', '3 días hábiles']},
  'd_peligrosos':     {'profepa': ['haz_tu_denuncia.html']},
  'd_ruido_comercio': {'invea':   ['tel:+525547377700', 'atencion.invea@cdmx.gob.mx', 'Carolina 132', 'invea.cdmx.gob.mx', 'viernes de 9:00 a 15:00']},
  'd_uso_suelo':      {'invea':   ['Carolina 132'], 'paot': ['inicia-tu-denuncia.php', 'tel:+525552650780', 'Medellín 202', '15430']},
  'd_olores':         {'paot':    ['inicia-tu-denuncia.php', 'Disponible las 24 horas']},
  'd_visual':         {'paot':    ['inicia-tu-denuncia.php']},
  'd_mascotas':       {'paot':    ['Medellín 202']},
}
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho in (1200, 390):
        pg = nav.new_context(viewport={'width': ancho, 'height': 900}).new_page()
        err = []
        pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
        for did, refs in ESPERA.items():
            r = pg.evaluate("""(id) => { estado = {}; guarda('deriva', id); irA(1);
              const red = document.querySelector('.redir');
              const ancho = document.documentElement.scrollWidth <= window.innerWidth + 1;
              return red ? {html: red.innerHTML, texto: red.innerText, ancho,
                ext: [...red.querySelectorAll('a[href^="http"]')].every(a => a.target === '_blank' && /noopener/.test(a.rel))} : null; }""", did)
            afirma(r is not None, '%s · %d px: aparece la pantalla de derivación' % (did, ancho))
            if not r: continue
            for ref, cosas in refs.items():
                faltan = [c for c in cosas if c not in r['html']]
                afirma(not faltan, '%s · %d px: muestra los medios de %s%s' % (did, ancho, ref.upper(), (' — faltan %s' % faltan) if faltan else ''))
            afirma(r['ext'], '%s · %d px: las ligas externas abren en otra pestaña' % (did, ancho))
            afirma(r['ancho'], '%s · %d px: nada desborda a lo ancho' % (did, ancho))
        sinpend = pg.evaluate("""() => DERIVA.filter(d => d.inst.some(i => i.ref)).every(d => { estado = {}; guarda('deriva', d.id); irA(1);
              const red = document.querySelector('.redir'); return [...red.querySelectorAll('.inst')].every(x => !/PROFEPA|PAOT|INVEA/.test(x.querySelector('.nom').textContent) || !x.querySelector('.pendiente')); })""")
        afirma(sinpend, '%d px: PROFEPA, PAOT e INVEA ya no llevan «Teléfono y liga por confirmar»' % ancho)
        afirma(not err, '%d px: sin errores en consola %s' % (ancho, err[:2]))
        pg.close()
    pg = nav.new_context(viewport={'width': 1200, 'height': 900}).new_page()
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    fuente = pg.evaluate("""() => { const t = document.documentElement.outerHTML;
      return ['haz_tu_denuncia.html', 'Carolina 132', 'Medellín 202'].map(x => t.split(x).length - 1); }""")
    afirma(fuente == [1, 1, 1], 'cada dato vive una sola vez en el código (CONTACTOS): %s' % fuente)
    anp = pg.evaluate("""() => typeof CONTACTOS === 'object' && Object.keys(CONTACTOS).sort().join()""")
    afirma(anp == 'invea,paot,profepa', 'CONTACTOS declara las tres autoridades')
    nav.close()
try: TMP.unlink()
except OSError: pass
for n in notas + fallos: print(n)
sys.exit(1 if fallos else 0)
