# -*- coding: utf-8 -*-
"""Campos que abre una respuesta, sangrados bajo su pregunta; código postal
   opcional; sin «Número de obra» (DEC-200, DEC-201). Se mide en pantalla."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina32.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
CASOS = [  # (paso, preparación, campo que debe ir dentro de .anidado, pregunta que lo abre)
  (2, "guarda('tiene_direccion','si'); guarda('tiene_mz_lote','si')", 'f_manzana', 'c_tiene_mz_lote'),
  (3, "guarda('es_estab','si')", 'f_nombre_estab', 'c_es_estab'),
  (3, "guarda('tipo_denunciado','gobierno')", 'f_resp_area', 'c_tipo_denunciado'),
  (3, "guarda('tipo_denunciado','nose')", 'f_resp_senas', 'c_tipo_denunciado'),
  (3, "guarda('reporto_antes','si')", 'f_gestiones', 'c_reporto_antes'),
  (5, "guarda('identificacion','nombre'); guarda('dom_tiene_mz_lote','si')", 'f_dom_manzana', 'c_dom_tiene_mz_lote'),
]
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho in (1100, 390):
        pg = nav.new_context(viewport={'width': ancho, 'height': 900}).new_page()
        err = []
        pg.on('pageerror', lambda e: err.append(str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
        for paso, prep, campo, preg in CASOS:
            r = pg.evaluate("""([paso, prep, campo, preg]) => { estado = {}; cfg.validar = true; guarda('materia','rsu'); eval(prep); irA(paso);
              const c = document.getElementById(campo), q = document.getElementById(preg);
              if (!c || !q) return null;
              const a = c.closest('.anidado'); if (!a) return {dentro: false};
              const cs = getComputedStyle(a), ra = a.getBoundingClientRect(), rq = q.getBoundingClientRect();
              return {dentro: true, filete: parseFloat(cs.borderLeftWidth) >= 2, sangria: ra.left > rq.left,
                      despues: ra.top >= rq.bottom - 1, ancho: document.documentElement.scrollWidth <= innerWidth + 1}; }""", [paso, prep, campo, preg])
            ok = r and r['dentro'] and r['filete'] and r['sangria'] and r['despues'] and r['ancho']
            afirma(ok, '%d px · %s va sangrado, con filete, debajo de su pregunta y sin desbordar: %s' % (ancho, campo, r))
        nada = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2);
          return document.querySelectorAll('.anidado').length; }""")
        afirma(nada == 0, '%d px: sin respuesta no hay bloque sangrado vacío (%d)' % (ancho, nada))
        afirma(not err, '%d px: sin errores en consola %s' % (ancho, err[:2]))
        pg.close()
    pg = nav.new_context(viewport={'width': 1100, 'height': 900}).new_page()
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    cp = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2);
      const l = document.querySelector('label[for="f_cp"]');
      const r = {oblig: esObligatorio('cp'), domOblig: esObligatorio('dom_cp'), opc: l ? l.innerText.includes('(opcional)') : null};
      guarda('cp','99999'); r.malo = formatoMal('cp'); guarda('cp',''); r.vacio = formatoMal('cp'); return r; }""")
    afirma(cp['oblig'] is False and cp['domOblig'] is False and cp['opc'], 'el código postal es opcional en el lugar y en el domicilio, y lo dice: %s' % cp)
    afirma(cp['malo'] and not cp['vacio'], 'si se escribe, se sigue revisando; vacío, no estorba')
    obra = pg.evaluate("""() => { estado = {}; guarda('materia','rsu'); guarda('tipo_denunciado','gobierno'); irA(3);
      return {campo: !!document.getElementById('f_resp_obra'), oblig: 'resp_obra' in OBLIG, texto: document.getElementById('app').innerText.includes('Número de obra')}; }""")
    afirma(not obra['campo'] and not obra['oblig'] and not obra['texto'], 'ya no se pregunta «Número de obra, contrato o permiso»')
    nav.close()
try: TMP.unlink()
except OSError: pass
for n in notas + fallos: print(n)
sys.exit(1 if fallos else 0)
