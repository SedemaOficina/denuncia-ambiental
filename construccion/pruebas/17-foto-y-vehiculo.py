# -*- coding: utf-8 -*-
"""La fotografía donde se ve el problema (M-06) y el servicio del vehículo.

   M-06. La evidencia llegaba en el paso 4, después de lo difícil; para
   entonces la persona puede estar ya en su casa o en el metro. Ahora el paso
   2 ofrece tomar la foto en cuanto el punto cae dentro de la Ciudad. Lo que
   esta batería vigila es lo que puede salir mal al adelantarla:
   1. Que aparezca sin rehacer la pantalla, porque rehacerla reinicia el mapa.
   2. Que los archivos vayan al MISMO arreglo: lo tomado en el paso 2 tiene que
      estar en el 4 y en la revisión, no en una lista paralela.
   3. Que no compita con Continuar: una sola acción con color por pantalla.
   4. Que en teléfono abra la cámara, no el selector de archivos.

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

    # ---------------- M-06 ----------------
    pg.evaluate("() => { archivos.length = 0; guarda('lat',''); guarda('lon',''); guarda('materia','rsu'); guarda('tiene_direccion','si'); irA(2); }")
    pg.wait_for_timeout(400)
    antes = pg.evaluate("() => { const f = document.getElementById('fotoAhora'); return {existe: !!f, lleno: !!(f && f.innerHTML.trim())}; }")
    afirma(antes['existe'] and not antes['lleno'], 'sin punto todavía, el paso 2 no ofrece la foto')

    # Marcamos el mapa para saber si se reinicia al aparecer el bloque.
    pg.evaluate("() => { const m = document.getElementById('mapa'); if(m) m.dataset.testigo = 'mismo'; }")
    pg.evaluate("() => ponMarcador(19.3500, -99.1620)"); pg.wait_for_timeout(400)
    d = pg.evaluate("""() => {
      const f = document.getElementById('fotoAhora');
      const inp = document.getElementById('inputFoto');
      const b = f && f.querySelector('button');
      const m = document.getElementById('mapa');
      return {
        lleno: !!(f && f.innerHTML.trim()),
        texto: f ? f.textContent : '',
        capture: inp ? inp.getAttribute('capture') : null,
        accept: inp ? inp.getAttribute('accept') : null,
        multiple: inp ? inp.hasAttribute('multiple') : false,
        primario: b ? b.classList.contains('btn-primario') : null,
        mapaIntacto: !!(m && m.dataset.testigo === 'mismo'),
        coloreados: [...document.querySelectorAll('.btn-primario')].filter(x => x.offsetParent !== null).length
      };
    }""")
    afirma(d['lleno'], 'al caer el punto dentro de la Ciudad aparece la invitación a tomar la foto')
    afirma(d['mapaIntacto'], 'y aparece sin rehacer la pantalla: el mapa no se reinició')
    afirma('frente al lugar' in d['texto'], 'la invitación se dirige a quien está ahí: «%s…»' % d['texto'].strip()[:40])
    afirma(d['capture'] == 'environment', 'en teléfono abre la cámara trasera, no el selector de archivos')
    afirma(d['accept'] and 'image/' in d['accept'] and 'video/' in d['accept'], 'acepta foto y video')
    afirma(d['multiple'], 'y admite varias de una vez')
    afirma(d['primario'] is False, 'el botón no es de acción principal: no compite con Continuar')
    afirma(d['coloreados'] == 1, 'sigue habiendo una sola acción con color en la pantalla (%d)' % d['coloreados'])

    # Un solo arreglo: lo tomado en el paso 2 se ve ahi, en el 4 y en la revision.
    pg.evaluate("() => agregaArchivos([%s])" % FALSO); pg.wait_for_timeout(250)
    en2 = pg.evaluate("() => (document.getElementById('listaArchTemprano')||{}).textContent || ''")
    afirma('basura-esquina.jpg' in en2, 'lo que se toma en el paso 2 se lista ahí mismo')
    pg.evaluate("() => irA(4)"); pg.wait_for_timeout(350)
    en4 = pg.evaluate("() => (document.getElementById('listaArch')||{}).textContent || ''")
    afirma('basura-esquina.jpg' in en4, 'y aparece en el paso 4: es el mismo arreglo, no una lista paralela')
    pg.evaluate("() => irA(2)"); pg.wait_for_timeout(400)
    vuelta = pg.evaluate("() => (document.getElementById('listaArchTemprano')||{}).textContent || ''")
    afirma('basura-esquina.jpg' in vuelta, 'al regresar al paso 2 la lista sigue ahí')
    n = pg.evaluate("() => archivos.length")
    afirma(n == 1, 'y no se duplicó al ir y volver (%d archivo)' % n)

    # Fuera de la Ciudad no se ofrece: no hay denuncia que documentar.
    pg.evaluate("() => ponMarcador(19.6000, -98.9000)"); pg.wait_for_timeout(400)
    fuera = pg.evaluate("() => ({f: val('fuera'), lleno: !!document.getElementById('fotoAhora').innerHTML.trim()})")
    afirma(fuera['f'] == 'si' and not fuera['lleno'], 'con el punto fuera de la Ciudad la invitación se retira')

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
