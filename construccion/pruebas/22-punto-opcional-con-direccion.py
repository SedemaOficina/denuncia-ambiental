# -*- coding: utf-8 -*-
"""Con dirección, el punto es opcional (DEC-123).

   Quien no sabe usar un mapa ni sacar una coordenada no puede quedarse sin
   denunciar: si escribió la dirección, basta. La Secretaría ubica el lugar
   con ella y turna después. Lo que se vigila es que eso se diga en cada
   pantalla y que nada afirme lo que todavía no se sabe:
   1. Con dirección completa y sin punto, el paso 2 continúa.
   2. Sin dirección, el punto sigue siendo obligatorio.
   3. El bloque del mapa ya no menciona la alcaldía (va arriba, en la
      dirección) y dice que basta la dirección.
   4. La revisión y el aviso de envío no nombran un área que nadie ha
      determinado; el folio nunca lleva área (DEC-151).
   5. El expediente dice de dónde salió la ubicación."""
import os, pathlib, sys, re
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina22.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

DIR = """() => { estado = {}; archivos = []; cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','si');
  guarda('calle','Calle 5'); guarda('num_ext','27'); guarda('alcaldia_dir','Iztacalco');
  guarda('colonia','Pantitlán I'); guarda('cp','08100'); irA(2); }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- con dirección y sin punto ----
    pg.evaluate(DIR); pg.wait_for_timeout(300)
    b = pg.evaluate("""() => { const c = document.getElementById('c_lat'); const h = c.querySelector('h3').innerText, a = c.querySelector('.ayuda').innerText;
      return {h, a, ast: !!c.querySelector('h3 .req'), oblig: esObligatorio('lat'), caja: document.getElementById('panelCapas').innerText, pasa: valida(2)}; }""")
    afirma(b['oblig'] is False and not b['ast'], 'con dirección, el punto no es obligatorio ni lleva asterisco')
    afirma('si puedes' in b['h'], 'el título lo dice: «%s»' % b['h'])
    afirma('basta la dirección' in b['a'], 'y la ayuda dice que basta la dirección')
    afirma('alcald' not in b['a'].lower(), 'sin volver a mencionar la alcaldía, que ya se escribió arriba')
    afirma('Ubicar en el mapa' not in b['caja'] and 'Puedes continuar' in b['caja'],
           'bajo el mapa, sin punto: «%s»' % b['caja'][:70])
    afirma(b['pasa'] is True, 'con la dirección completa y sin punto, el paso continúa')
    local = pg.evaluate("() => document.getElementById('c_lat').innerText")
    afirma('continúa sin punto' in local and 'la dirección, el punto se coloca solo' not in local,
           'en esta versión de prueba no se promete que la dirección coloque el punto')

    # ---- revisión, envío y folio ----
    pg.evaluate("() => { guarda('hechos','Tiran basura revuelta en la banqueta todas las noches desde hace un mes.'); guarda('identificacion','anonima'); guarda('correo','a@b.mx'); guarda('privacidad','si'); irA(6); alternaDetalleRevision(); }")
    pg.wait_for_timeout(300)
    rv = pg.evaluate("""() => { const v = t => { const dt=[...document.querySelectorAll('.resumen dt')].find(x=>x.textContent.indexOf(t)===0); return dt ? dt.nextElementSibling.textContent : null; };
      return {coord: v('Coordenadas'), alc: v('Alcaldía que atiende'), suelo: v('Tipo de suelo'),
              envio: (document.querySelector('.aviso-envio')||{}).innerText || ''}; }""")
    afirma(rv['coord'] and 'ubicará el lugar con la dirección' in rv['coord'], 'la revisión dice que el punto se ubicará con la dirección')
    afirma(rv['alc'] and 'Se determinará' in rv['alc'] and 'Se determinará' in (rv['suelo'] or ''), 'y que la alcaldía que atiende y el tipo de suelo se determinarán')
    afirma('ubicará el lugar' in rv['envio'] and 'Dirección General' not in rv['envio'] and ' a el ' not in rv['envio'],
           'el aviso de envío no nombra un área: «%s»' % rv['envio'][:90])
    pg.evaluate("() => { guarda('verificacion','si'); enviar(); }"); pg.wait_for_timeout(300)
    f = pg.evaluate("() => ({folio: val('folio'), origen: val('ubicacion_origen')})")
    afirma(re.match(r'^SEDEMA/DEN/\d{4}/\d{6}-\d$', f['folio'] or '') is not None, 'el folio no lleva área: %s' % f['folio'])
    afirma(f['origen'] == 'direccion', 'y el expediente registra que la ubicación sale de la dirección')

    # ---- con punto: como antes ----
    pg.evaluate(DIR); pg.evaluate("() => ponMarcador(19.4100, -99.0700)"); pg.wait_for_timeout(300)
    pg.evaluate("() => { guarda('hechos','Tiran basura revuelta en la banqueta todas las noches desde hace un mes.'); guarda('identificacion','anonima'); guarda('correo','a@b.mx'); guarda('privacidad','si'); guarda('verificacion','si'); enviar(); }")
    pg.wait_for_timeout(300)
    f2 = pg.evaluate("() => ({folio: val('folio'), origen: val('ubicacion_origen')})")
    afirma(re.match(r'^SEDEMA/DEN/\d{4}/\d{6}-\d$', f2['folio'] or '') is not None and f2['origen'] == 'punto',
           'con punto, el folio tampoco lleva área y el origen es «punto» (%s)' % f2['folio'])

    # ---- sin dirección: el punto sigue siendo obligatorio ----
    s = pg.evaluate("""() => { estado = {}; cfg.validar = true; guarda('materia','tala'); guarda('tiene_direccion','no'); irA(2);
      const c = document.getElementById('c_lat');
      return {oblig: esObligatorio('lat'), ast: !!c.querySelector('h3 .req'), h: c.querySelector('h3').innerText, pasa: (guarda('referencias','Entrando por el camino de terracería, pasando el puente.'), valida(2))}; }""")
    afirma(s['oblig'] and s['ast'], 'sin dirección, el punto es obligatorio y lo marca')
    afirma('si puedes' not in s['h'], 'y el título no lo presenta como opcional: «%s»' % s['h'])
    afirma(s['pasa'] is False, 'sin punto, el paso no continúa')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
