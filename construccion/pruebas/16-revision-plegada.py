# -*- coding: utf-8 -*-
"""La revisión final, plegada por bloques (M-10).

   Eran tres pantallas repitiendo todo lo capturado. Desde que el recorrido se
   acortó un 17 %, era la pantalla más larga del formulario, justo donde la
   persona ya quiere terminar. Ahora cada bloque muestra una línea con lo que
   importa y guarda el detalle a un clic.

   Lo que esta batería exige, y que es donde plegar puede salir mal:
   1. Que la línea visible diga algo: un bloque cuyo resumen esté vacío obliga
      a abrirlo, y entonces plegar no ahorró nada.
   2. Que ningún renglón se vuelva mudo al esconderse (DEC-85 sigue vigente).
   3. Que exista la salida para leerlo todo.
   4. Que la pantalla haya bajado de alto de verdad, medido en teléfono."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina16.html'
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
  guarda('hechos','Todos los dias sacan escombro y lo tiran en la esquina desde hace tres semanas, y nadie lo recoge; el monton ya invade la banqueta y la gente tiene que bajarse a la calle.');
  guarda('es_estab','si'); guarda('temporalidad','recurrente');
  guarda('tipo_denunciado','empresa'); guarda('establecimiento','Constructora del Sur');
  guarda('identificacion','nombre'); guarda('nombre','Ana'); guarda('apellido_paterno','Ruiz');
  guarda('telefono','5512345678'); guarda('correo','ana@ejemplo.mx');
  guarda('notif_correo','no'); guarda('reserva','si');
  guarda('dom_calle','Miguel Angel de Quevedo'); guarda('dom_num_ext','22');
  guarda('dom_colonia','Chimalistac'); guarda('dom_cp','01070');
  guarda('sexo_genero','mujer'); guarda('edad_rango','30-44');
  irA(6);
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width':390,'height':760})
    pg = ctx.new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    pg.evaluate(PREPARA); pg.wait_for_timeout(500)

    b = pg.evaluate("""() => {
      const ds = [...document.querySelectorAll('details.rev-bloque')];
      return {
        n: ds.length,
        abiertos: ds.filter(d => d.open).length,
        titulos: ds.map(d => (d.querySelector('.rb-tit')||{}).textContent),
        resumenes: ds.map(d => ((d.querySelector('.rb-res')||{}).textContent||'').trim()),
        conDl: ds.filter(d => d.querySelector('dl')).length,
        haySumario: ds.every(d => !!d.querySelector('summary'))
      };
    }""")
    afirma(b['n'] == 5, 'la revisión se reparte en %d bloques' % b['n'])
    afirma(b['abiertos'] == 0, 'y llegan todos plegados (%d abiertos)' % b['abiertos'])
    afirma(b['haySumario'], 'cada bloque es un <details> con su <summary>: teclado y lectores de pantalla sin JS propio')
    afirma(all(t and t.strip() for t in b['titulos']), 'cada bloque se nombra: %s' % b['titulos'])
    vacios = [b['titulos'][i] for i,x in enumerate(b['resumenes']) if not x or x == 'Sin dato']
    afirma(vacios == [], 'ningún bloque obliga a abrirlo para saber qué trae: %s' % vacios)
    afirma(b['conDl'] == 5, 'los cinco conservan su detalle dentro')

    # El resumen visible lleva el dato que importa, no una etiqueta generica.
    res = ' | '.join(b['resumenes'])
    afirma('Churubusco' in res, 'el bloque del lugar enseña la dirección sin abrirlo')
    afirma('escombro' in res, 'el bloque de hechos enseña el relato sin abrirlo')
    afirma('Ana' in res, 'el bloque de identificación enseña quién denuncia sin abrirlo')

    # DEC-85 sigue en pie: plegar no vuelve mudo a ningun renglon.
    r = pg.evaluate("""() => {
      const dts = [...document.querySelectorAll('.resumen dt')];
      return {total: dts.length,
              mudos: dts.filter(d => !d.querySelector('button.editar') && !d.querySelector('.derivado')).map(d => d.textContent.trim()),
              conBoton: dts.filter(d => d.querySelector('button.editar')).length};
    }""")
    afirma(r['total'] >= 20, 'el detalle sigue resumiendo %d renglones: no se perdió nada' % r['total'])
    afirma(r['mudos'] == [], 'y ninguno se quedó sin decir cómo se corrige: %s' % r['mudos'])
    afirma(r['conBoton'] >= 18, 'con %d botones de corregir dentro de los bloques' % r['conBoton'])

    # La salida para leerlo todo.
    t0 = pg.evaluate("() => (document.getElementById('btnRevTodo')||{}).textContent")
    afirma(t0 and 'Ver todo' in t0, 'hay una salida para leerlo entero: «%s»' % t0)
    pg.evaluate("() => alternaDetalleRevision()"); pg.wait_for_timeout(250)
    ab = pg.evaluate("() => [...document.querySelectorAll('details.rev-bloque')].filter(d=>d.open).length")
    t1 = pg.evaluate("() => (document.getElementById('btnRevTodo')||{}).textContent")
    afirma(ab == 5, 'que abre los cinco de una vez (%d abiertos)' % ab)
    afirma(t1 and 'Ocultar' in t1, 'y el botón dice entonces lo contrario: «%s»' % t1)
    pg.evaluate("() => alternaDetalleRevision()"); pg.wait_for_timeout(250)
    ce = pg.evaluate("() => [...document.querySelectorAll('details.rev-bloque')].filter(d=>d.open).length")
    afirma(ce == 0, 'y vuelve a cerrarlos')

    # Corregir desde un bloque cerrado sigue aterrizando en el campo.
    pg.evaluate(PREPARA); pg.wait_for_timeout(350)
    ok = pg.evaluate("""() => {
      const dt = [...document.querySelectorAll('.resumen dt')].find(x => x.textContent.indexOf('Hechos denunciados') === 0);
      if(!dt) return false;
      const b = dt.querySelector('button.editar');
      if(!b) return false;
      b.click(); return true;
    }""")
    afirma(ok is True, 'desde un bloque cerrado se puede corregir un renglón')
    pg.wait_for_timeout(450)
    foco = pg.evaluate("""() => {
      const e = document.getElementById('f_hechos');
      return {paso: paso, existe: !!e, enfocado: !!e && document.activeElement === e};
    }""")
    afirma(foco['paso'] == 3 and foco['existe'] and foco['enfocado'],
           'y el cursor queda en el campo, no al principio de la pantalla')

    # Cuanto bajo la pantalla, en telefono.
    pg.evaluate(PREPARA); pg.wait_for_timeout(400)
    alto = pg.evaluate("() => Math.round(document.querySelector('.tarjeta').getBoundingClientRect().height)")
    pg.evaluate("() => alternaDetalleRevision()"); pg.wait_for_timeout(300)
    altoAbierto = pg.evaluate("() => Math.round(document.querySelector('.tarjeta').getBoundingClientRect().height)")
    afirma(alto < altoAbierto * 0.55,
           'plegada mide %d px contra %d px desplegada: %.0f %% menos, de %.1f a %.1f pantallas de teléfono'
           % (alto, altoAbierto, (1-alto/altoAbierto)*100, altoAbierto/760.0, alto/760.0))
    afirma(alto <= 1600, 'y cabe en %.1f pantallas de 760 px (%d px)' % (alto/760.0, alto))

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
