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
  (3, "guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','cdmx')", 'f_resp_area', 'c_tipo_denunciado'),
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

    # ---- DEC-202: obligatorias del paso 3 y la referencia del sitio; «No lo sé» en el ámbito ----
    ob = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','si');
      guarda('es_estab','si'); guarda('tipo_estab','Otro'); guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','cdmx');
      return ['referencias','temporalidad','es_estab','tipo_estab','tipo_estab_otro','tipo_denunciado','autoridad_nivel','reporto_antes']  /* «¿Cuál?» es opcional desde DEC-209 */
        .filter(k => !esObligatorio(k)); }""")
    afirma(ob == [], 'las preguntas del paso 3 y la referencia del sitio son obligatorias (DEC-202); opcionales todavía: %s' % ob)
    op = pg.evaluate("""() => ({fecha: esObligatorio('fecha_hecho'), nombre: esObligatorio('nombre_estab'), area: esObligatorio('resp_area'), gest: (guarda('reporto_antes','si'), esObligatorio('gestiones'))})""")
    afirma(not any(op.values()), 'siguen opcionales la fecha, el nombre del establecimiento, el área y el detalle de gestiones: %s' % op)
    ns = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); guarda('tipo_denunciado','gobierno'); irA(3);
      const tiene = NIVELES_AUTORIDAD.some(n => n.v === 'nose' && n.t === 'No lo sé');
      guarda('autoridad_nivel','nose'); render();
      return {tiene, cual: !!document.getElementById('c_autoridad_denunciada'), oblig: esObligatorio('autoridad_denunciada')}; }""")
    afirma(ns['tiene'] and not ns['cual'] and not ns['oblig'], 'el ámbito ofrece «No lo sé» y con él no se pregunta «¿Cuál?»: %s' % ns)
    tp = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); irA(3);
      const c = document.getElementById('c_tipo_denunciado'); const sel = document.getElementById('f_tipo_denunciado');
      const r = {select: !!sel && sel.tagName === 'SELECT', botones: c ? c.querySelectorAll('.btn-sn').length : -1, opciones: sel ? sel.options.length : 0, err: !!document.getElementById('e_tipo_denunciado')};
      if (sel) { sel.value = 'nose'; sel.dispatchEvent(new Event('change')); }
      r.abre = !!document.getElementById('f_resp_senas'); return r; }""")
    afirma(tp['select'] and tp['botones'] == 0 and tp['opciones'] == 5 and tp['err'] and tp['abre'],
           '«¿Quién es responsable?» es lista desplegable con sus cuatro respuestas y al elegir abre lo suyo (DEC-203): %s' % tp)
    t3 = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); irA(3); valida(3);
      return !!document.querySelector('#c_temporalidad.invalido') && !!document.getElementById('e_temporalidad'); }""")
    afirma(t3, 'sin contestar, la temporalidad marca su error en su propio renglón')
    # ---- DEC-204: nada aparece arriba de la pregunta del domicilio al contestarla ----
    pp = pg.evaluate("""() => ['si','no'].map(v => { estado = {}; guarda('materia','rsu'); guarda('tiene_direccion', v); irA(2);
      const t = document.querySelector('#app .tarjeta'); const h2 = t.querySelector('h2'); const q = document.getElementById('c_tiene_direccion');
      return {sinParrafo: !t.innerText.includes('Este paso pide'), seguida: h2.nextElementSibling === q}; })""")
    afirma(all(x['sinParrafo'] and x['seguida'] for x in pp), 'al contestar si tiene calle y número, nada aparece entre el título y la pregunta (DEC-204): %s' % pp)
    # ---- DEC-209: autoridad — «¿Cuál?» opcional; con «No lo sé», ni «¿Cuál?» ni área ----
    au = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','rsu'); guarda('tipo_denunciado','gobierno'); guarda('autoridad_nivel','cdmx'); irA(3);
      const r = {cualOpc: !esObligatorio('autoridad_denunciada') && !!document.getElementById('c_autoridad_denunciada'), area: !!document.getElementById('f_resp_area')};
      guarda('resp_area','Dirección de obras'); const s = document.getElementById('f_autoridad_nivel'); s.value = 'nose'; s.dispatchEvent(new Event('change'));
      r.nose = {cual: !!document.getElementById('c_autoridad_denunciada'), area: !!document.getElementById('f_resp_area'), suelta: !val('resp_area')};
      return r; }""")
    afirma(au['cualOpc'] and au['area'], 'con ámbito conocido, «¿Cuál?» aparece y es opcional, y se ofrece el área: %s' % au)
    afirma(not au['nose']['cual'] and not au['nose']['area'] and au['nose']['suelta'], 'con «No lo sé», no se pregunta cuál ni el área, y se suelta lo escrito: %s' % au['nose'])
    # ---- DEC-210: aviso de privacidad con su texto ----
    av = pg.evaluate("""() => { estado = {}; guarda('materia','rsu'); guarda('identificacion','nombre'); irA(5);
      const pl = document.querySelector('.priv-plegable'); if(pl) pl.open = true; const p = document.querySelector('.priv'); return p ? {t: p.innerText, huecos: [...p.querySelectorAll('.pendiente')].map(x => x.textContent)} : null; }""")
    afirma(av and 'Ley de Protección de Datos Personales en Posesión de Sujetos Obligados de la Ciudad de México' in av['t'] and 'ARCOP' in av['t'] and 'Por desarrollar' not in av['t'],
           'el aviso del paso 5 tiene su texto y ya no dice «Por desarrollar»')
    afirma(av and av['huecos'] == ['[nombre del sistema registrado]', '[fundamento de esta transferencia por confirmar]', '[dirección electrónica]'],
           'los tres huecos quedan marcados como pendientes: %s' % (av and av['huecos']))
    nav.close()
try: TMP.unlink()
except OSError: pass
for n in notas + fallos: print(n)
sys.exit(1 if fallos else 0)
