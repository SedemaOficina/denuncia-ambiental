# -*- coding: utf-8 -*-
"""El acuse en PDF (DEC-139).

   Sin envio de correos, la persona se lleva su acuse al terminar. Se
   comprueba que el PDF se arme sin bibliotecas externas, que sea un PDF
   valido, que lleve el folio, la fecha, el logotipo y todo lo que la
   persona reviso, con los acentos bien, y que avise que es un prototipo."""
import os, pathlib, sys, subprocess, tempfile
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
SALIDA = pathlib.Path(os.environ.get('ACUSE_PDF', tempfile.gettempdir())) 

def pdf_de(pg, escenario):
    datos = pg.evaluate("""(e) => { cargaEscenario(e); guarda('verificacion','si'); irA(6); enviar();
      return construyeAcusePdf().then(u => Array.from(u)); }""", escenario)
    ruta = SALIDA / ('acuse-%s.pdf' % escenario)
    ruta.write_bytes(bytes(datos))
    return ruta

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}, accept_downloads=True).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. El acuse ofrece la descarga ----
    ac = pg.evaluate("""() => { cargaEscenario('urbano'); guarda('verificacion','si'); irA(6); enviar();
      const b = [...document.querySelectorAll('#app button')].find(x => x.textContent.includes('Descargar acuse'));
      return {boton: !!b, texto: document.getElementById('app').innerText}; }""")
    afirma(ac['boton'], 'la pantalla final ofrece «Descargar acuse (PDF)»')
    afirma('no se envían por correo' in ac['texto'], 'y dice que el folio y el acuse no se envían por correo')
    with pg.expect_download() as d:
        pg.click('text=Descargar acuse (PDF)')
    dl = d.value
    afirma(dl.suggested_filename.startswith('acuse-SEDEMA-') and dl.suggested_filename.endswith('.pdf'),
           'se descarga con el folio en el nombre: %s' % dl.suggested_filename)

    # ---- 2. El PDF es valido y dice lo que tiene que decir ----
    for esc in ('urbano', 'conservacion', 'sin_calle'):
        ruta = pdf_de(pg, esc)
        chk = subprocess.run(['qpdf', '--check', str(ruta)], capture_output=True, text=True)
        afirma(chk.returncode == 0, '%s: el PDF es válido (qpdf)' % esc)
        txt = subprocess.run(['pdftotext', '-layout', str(ruta), '-'], capture_output=True, text=True).stdout
        folio = pg.evaluate("() => val('folio')")
        afirma(folio in txt, '%s: lleva el folio %s' % (esc, folio))
        clave = pg.evaluate("() => val('clave_consulta')")
        afirma(clave and clave in txt and 'Clave de consulta' in txt and 'No puede reponerse' in txt,
               '%s: lleva la clave de consulta %s (DEC-151)' % (esc, clave))
        afirma('ACUSE DE RECEPCIÓN' in txt and 'Recibida el' in txt, '%s: título y fecha de recepción' % esc)
        afirma('SECRETARÍA DEL MEDIO AMBIENTE' in txt, '%s: membrete con acentos correctos' % esc)
        afirma('Página 1 de' in txt, '%s: numeración de páginas' % esc)
        afirma('Prototipo de validación interna' in txt and 'no tiene validez oficial' in txt, '%s: advierte que es un prototipo' % esc)
        bloques = pg.evaluate("() => datosDelAcuse().map(b => b.titulo)")
        faltan = [b for b in bloques if b.upper() not in txt]
        afirma(bloques and not faltan, '%s: trae los bloques de la revisión %s (faltan %s)' % (esc, bloques, faltan))
        afirma('Editar' not in txt, '%s: sin los botones de la pantalla' % esc)
        img = subprocess.run(['pdfimages', '-list', str(ruta)], capture_output=True, text=True).stdout
        afirma('jpeg' in img, '%s: incrusta el logotipo institucional' % esc)
        if esc == 'urbano':
            afirma('Estado de México' in txt and 'Nezahualcóyotl' in txt, 'urbano: el domicilio fuera de la Ciudad sale completo')
        if esc == 'conservacion':
            afirma('Denuncia anónima' in txt and 'escribirá al correo' in txt, 'conservación: la anónima lo dice, y qué sigue')

    # ---- 3. Un texto largo se reparte en varias paginas ----
    largo = pg.evaluate("""() => { cargaEscenario('urbano'); guarda('hechos', ('Humo denso y olor a solvente durante toda la tarde. ').repeat(90));
      guarda('verificacion','si'); irA(6); enviar(); return construyeAcusePdf().then(u => Array.from(u)); }""")
    ruta = SALIDA / 'acuse-largo.pdf'; ruta.write_bytes(bytes(largo))
    info = subprocess.run(['pdfinfo', str(ruta)], capture_output=True, text=True).stdout
    pags = int([l for l in info.splitlines() if l.startswith('Pages:')][0].split()[-1])
    txt = subprocess.run(['pdftotext', str(ruta), '-'], capture_output=True, text=True).stdout
    afirma(pags >= 2 and ('Página %d de %d' % (pags, pags)) in txt, 'una descripción larga pasa a otra página y numera «de %d»' % pags)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
