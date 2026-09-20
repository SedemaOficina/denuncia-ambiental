# -*- coding: utf-8 -*-
"""La pantalla de revisión: ningún renglón se queda callado (DEC-85).

   Tenía veinticuatro renglones y sólo siete con botón de corregir, sin regla
   visible: lo que parecía es que el resto no se podía cambiar. Ahora cada
   renglón o lleva su botón —que aterriza en el campo, no al principio del
   paso— o dice por qué no se corrige ahí."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina08.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

PREPARA = """() => {
  cfg.validar = true;
  guarda('materia','rsu'); guarda('tiene_direccion','si');
  guarda('calle','Avenida Rio Churubusco'); guarda('num_ext','100');
  guarda('colonia','Del Carmen'); guarda('cp','04100');
  ponMarcador(19.3500, -99.1620);
  guarda('hechos','Todos los dias sacan escombro y lo tiran en la esquina desde hace tres semanas, y nadie lo recoge.');
  guarda('es_estab','si'); guarda('temporalidad','recurrente');
  guarda('identificacion','nombre'); guarda('nombre','Ana'); guarda('apellido_paterno','Ruiz');
  guarda('telefono','5512345678'); guarda('correo','ana@ejemplo.mx');
  guarda('notif_correo','no'); guarda('reserva','si');
  guarda('sexo_genero','mujer'); guarda('edad_rango','30-44');
  irA(6);
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    pg.evaluate(PREPARA); pg.wait_for_timeout(500)

    r = pg.evaluate("""() => {
      const dts = [...document.querySelectorAll('.resumen dt')];
      const mudos = dts.filter(d => !d.querySelector('button.editar') && !d.querySelector('.derivado'))
                       .map(d => d.textContent.trim());
      return {total: dts.length, mudos: mudos,
              conBoton: dts.filter(d => d.querySelector('button.editar')).length,
              derivados: dts.filter(d => d.querySelector('.derivado')).map(d => d.textContent.replace(/\\s+/g,' ').trim())};
    }""")
    afirma(r['total'] >= 20, 'la revisión resume %d renglones' % r['total'])
    afirma(r['mudos'] == [], 'ningún renglón se queda sin decir cómo se corrige: %s' % r['mudos'])
    afirma(r['conBoton'] >= 18, 'y la mayoría se corrige desde ahí (%d con botón)' % r['conBoton'])
    afirma(len(r['derivados']) == 2,
           'sólo los dos datos que calcula el punto se explican en vez de editarse: %s' % r['derivados'])

    # Corregir aterriza en el campo, no al principio del paso.
    for etiqueta, paso, campo in [('Hechos denunciados', 3, 'f_hechos'),
                                  ('Contacto', 5, 'f_telefono'),
                                  ('Datos estadísticos', 5, 'f_sexo_genero')]:
        pg.evaluate(PREPARA); pg.wait_for_timeout(350)
        d = pg.evaluate("""(etq) => {
          const dt = [...document.querySelectorAll('.resumen dt')].find(x => x.textContent.indexOf(etq) === 0);
          if(!dt) return null;
          const b = dt.querySelector('button.editar');
          if(!b) return null;
          b.click();
          return true;
        }""", etiqueta)
        afirma(d is True, '«%s» tiene botón de corregir' % etiqueta)
        pg.wait_for_timeout(450)
        estado = pg.evaluate("""(id) => {
          const e = document.getElementById(id);
          return {paso: paso, existe: !!e, enfocado: !!e && document.activeElement === e};
        }""", campo)
        afirma(estado['paso'] == paso, '«%s» lleva al paso %d' % (etiqueta, paso))
        afirma(estado['existe'] and estado['enfocado'],
               'y deja el cursor en el campo, no al principio de la pantalla')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
