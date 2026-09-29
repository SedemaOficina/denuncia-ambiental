# -*- coding: utf-8 -*-
"""El servicio del vehículo, y que la foto del paso 2 no vuelva (DEC-120).

   M-06. La invitación a tomar la foto en el paso 2 (DEC-114) se retiró por
   instrucción (DEC-120): se vigila que no vuelva y que la evidencia siga
   entrando por el paso 4.

   Vehículo contaminante. La tarjeta dice sólo lo que se ve (DEC-107); el dato
   de si la unidad presta un servicio se pregunta en el paso 3. Se vigila que
   aparezca sólo para esa materia, que se exija, que «No lo sé» baste, y que la
   ayuda no prometa un turnado que todavía no está convenido."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina17.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# Un archivo falso que agregaArchivos acepta: tiene nombre, extension y peso.
FALSO = "({name:'basura-esquina.jpg', size:1200000})"

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---------------- Foto en el paso 2: retirada (DEC-120) ----------------
    #    La invitación a tomar la foto frente al lugar (M-06, DEC-114) se
    #    retiró por instrucción. Se vigila que no vuelva y que la evidencia
    #    siga entrando por el paso 4.
    pg.evaluate("() => { archivos.length = 0; guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2); }")
    pg.wait_for_timeout(300)
    pg.evaluate("() => ponMarcador(19.3500, -99.1620)"); pg.wait_for_timeout(400)
    r = pg.evaluate("""() => ({bloque: !!document.querySelector('#fotoAhora, .foto-ahora, #inputFoto'),
      texto: /frente al lugar|Tomar o elegir una foto/.test(document.getElementById('app').innerText)})""")
    afirma(not r['bloque'] and not r['texto'], 'con el punto colocado, el paso 2 ya no ofrece tomar la foto')
    p4 = pg.evaluate("() => { irA(4); return !!document.querySelector('.lista-arch') && !!document.querySelector('input[type=file]'); }")
    afirma(p4, 'la evidencia sigue entrando por el paso 4')

    # ---------------- Vehiculo ----------------
    PREP = """(m) => { archivos.length = 0; cfg.validar = true; guarda('materia', m); guarda('veh_servicio','');
      guarda('hechos','Un microbus de la ruta pasa todas las mananas echando humo negro por la avenida principal.');
      guarda('temporalidad','recurrente'); guarda('tipo_denunciado','nose'); guarda('es_estab','no');
      guarda('sabe_permisos','no'); guarda('reporto_antes','no'); irA(3); }"""
    pg.evaluate(PREP, 'vehiculo'); pg.wait_for_timeout(350)
    v = pg.evaluate("""() => {
      const c = document.getElementById('c_veh_servicio');
      return {existe: !!c, ops: c ? [...c.querySelectorAll('button.btn-sn')].map(b => b.textContent) : [],
              marca: c ? !!c.querySelector('.req') : false,
              ayuda: c ? (c.querySelector('.ayuda')||{}).textContent : ''};
    }""")
    afirma(v['existe'], 'con «Vehículo contaminante» el paso 3 pregunta si es transporte público o de carga')
    afirma(len(v['ops']) == 4 and any('pasajeros' in o for o in v['ops']) and any('carga' in o for o in v['ops']),
           'con cuatro respuestas, pasajeros y carga separados: %s' % v['ops'])
    afirma(any('No lo s' in o for o in v['ops']), 'e incluye «No lo sé»: no saber la placa no impide denunciar')
    afirma(v['marca'], 'lleva la marca de obligatorio')
    afirma('turna' not in v['ayuda'].lower(),
           'la ayuda no promete un turnado que todavía no está convenido: «%s»' % v['ayuda'])

    sin = pg.evaluate("() => valida(3)")
    afirma(sin is False, 'sin responderla no se avanza')
    pg.evaluate("() => { guarda('veh_servicio','nose'); render(); }"); pg.wait_for_timeout(250)
    con = pg.evaluate("() => valida(3)")
    afirma(con is True, 'con «No lo sé» sí se avanza')

    pg.evaluate("() => { guarda('veh_servicio','pasajeros'); irA(6); }"); pg.wait_for_timeout(400)
    rv = pg.evaluate("""() => {
      const dt = [...document.querySelectorAll('.resumen dt')].find(x => x.textContent.indexOf('Tipo de servicio') === 0);
      return {existe: !!dt, boton: !!(dt && dt.querySelector('button.editar')),
              valor: dt ? dt.nextElementSibling.textContent : ''};
    }""")
    afirma(rv['existe'] and 'pasajeros' in rv['valor'], 'la revisión lo resume: «%s»' % rv['valor'])
    afirma(rv['boton'], 'y se puede corregir desde ahí')

    pg.evaluate(PREP, 'rsu'); pg.wait_for_timeout(350)
    otra = pg.evaluate("() => !!document.getElementById('c_veh_servicio')")
    afirma(not otra, 'con cualquier otra materia la pregunta no aparece')
    pg.evaluate("() => irA(6)"); pg.wait_for_timeout(350)
    otraRev = pg.evaluate("() => [...document.querySelectorAll('.resumen dt')].some(x => x.textContent.indexOf('Tipo de servicio') === 0)")
    afirma(not otraRev, 'ni en la revisión')
    oblig = pg.evaluate("() => esObligatorio('veh_servicio')")
    afirma(oblig is False, 'y fuera de su materia no se exige')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
