# -*- coding: utf-8 -*-
"""El mapeo de campos dice todo lo que viaja a la base, y no puede quedarse atrás (DEC-128).

   1. Ninguna clave viaja sin declararse: toda clave que el código guarda está
      en OBLIG (lo que la persona llena), en DERIVADOS (lo que el formulario
      calcula) o en INTERNOS (estado de pantalla que no viaja). Lo mismo para
      lo que se guarda de cada foto.
   2. El mapeo se arma de esos catálogos al abrirse: sus cifras coinciden con
      ellos, y muestra la versión del formulario.
   3. Tiene su sección «Campos que viajan a la base y no se ven en pantalla»,
      con lo que de verdad no se ve, y aparte lo calculado que sí se muestra.
   4. Todo dato tiene uso declarado."""
import os, pathlib, sys, re, tempfile
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina24.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
FUENTE = RUTA.read_text(encoding='utf-8')
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' + FUENTE + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# claves que el código guarda con literal, en las dos formas de comillas
guardadas = set(re.findall(r"guarda\('([a-z_0-9]+)'", FUENTE)) | set(re.findall(r"guarda\(\\\\?'([a-z_0-9]+)", FUENTE))
# lo que se escribe en cada foto
foto = set(re.findall(r"\ba\.([a-z_0-9]+)\s*=", FUENTE[FUENTE.index('function procesaFoto'):FUENTE.index('function procesaFoto') + 4000]))
foto |= set(re.findall(r"\ba\.([a-z_0-9]+)\s*=", FUENTE[FUENTE.index('function agregaArchivos'):FUENTE.index('function agregaArchivos') + 2500]))

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    cat = pg.evaluate("() => ({oblig: Object.keys(OBLIG), der: Object.keys(DERIVADOS), intr: Object.keys(INTERNOS), fotoDer: Object.keys(DERIVADOS).filter(k => DERIVADOS[k].por === 'foto'), ver: VERSION_FORMULARIO})")
    declaradas = set(cat['oblig']) | set(cat['der']) | set(cat['intr'])
    sueltas = sorted(guardadas - declaradas)
    afirma(len(guardadas) > 30 and sueltas == [], 'toda clave que el código guarda está declarada (%d revisadas): %s' % (len(guardadas), sueltas))
    base_foto = {'estado', 'blob', 'size', 'name'}
    foto_sueltas = sorted(foto - set(cat['fotoDer']) - base_foto)
    afirma(foto_sueltas == [], 'todo lo que se guarda de cada foto está declarado: %s' % foto_sueltas)
    doble = sorted(set(cat['oblig']) & set(cat['der']))
    afirma(doble == [], 'ningún dato está declarado dos veces: %s' % doble)
    afirma(re.match(r'^DEC-\d+$', cat['ver']['dec']) and cat['ver']['fecha'], 'el formulario declara su versión: %s' % cat['ver'])

    # ---- el mapeo ----
    m = pg.evaluate("""() => { abreMapeo(); const t = document.getElementById('tablaMapeo');
      const d = mapeoDatos();
      const filas = id => { const h = document.getElementById(id); let n = h.nextElementSibling; while(n && n.tagName !== 'TABLE') n = n.nextElementSibling;
        return n ? [...n.querySelectorAll('tbody tr')].filter(r => r.children.length === 4).length : -1; };
      return {abierto: document.getElementById('modalMapeo').classList.contains('abierto'),
              titulos: [...t.querySelectorAll('h4')].map(h => h.textContent),
              version: (t.querySelector('.mapeo-version')||{}).textContent || '',
              nLlena: d.llena.length, nOcu: d.ocultos.length, nVis: d.visibles.length,
              fLlena: filas('mapeoLlena'), fOcu: filas('mapeoOcultos'), fVis: filas('mapeoVisibles'),
              ocultos: d.ocultos.map(x => x.k), visibles: d.visibles.map(x => x.k),
              sinUso: d.ocultos.concat(d.visibles).filter(x => !x.uso).map(x => x.k)
                      .concat(d.llena.filter(k => !OBLIG[k].uso)),
              texto: t.innerText}; }""")
    afirma(m['abierto'], 'el mapeo se abre desde el panel')
    afirma(any('viajan a la base y no se ven en pantalla' in x for x in m['titulos']), 'tiene la sección «Campos que viajan a la base y no se ven en pantalla»')
    afirma(any('se muestran como información' in x for x in m['titulos']), 'y aparte lo calculado que sí se muestra')
    afirma(cat['ver']['dec'] in m['version'], 'muestra la versión del formulario: %r' % m['version'][:60])
    afirma(m['fLlena'] == m['nLlena'] and m['fOcu'] == m['nOcu'] and m['fVis'] == m['nVis'],
           'cada sección lista exactamente lo que dicen los catálogos (%d/%d, %d/%d, %d/%d)' % (m['fLlena'], m['nLlena'], m['fOcu'], m['nOcu'], m['fVis'], m['nVis']))
    for k in ['uga', 'colonia_cve', 'ubicacion_origen', 'dg', 'sha256_original', 'fecha_captura', 'lat_captura']:
        afirma(k in m['ocultos'], '«%s» está entre lo que viaja sin verse' % k)
    for k in ['alcaldia', 'dg_nombre', 'folio']:
        afirma(k in m['visibles'] and k not in m['ocultos'], '«%s» está entre lo calculado que se muestra' % k)
    afirma(m['sinUso'] == [], 'ningún dato sin uso declarado: %s' % m['sinUso'])
    afirma('Hora aproximada' not in m['texto'] and 'Confidencialidad de los datos' not in m['texto'],
           'no quedan campos retirados (hora, confidencialidad)')
    afirma('¿El predio se identifica por manzana y lote?' in m['texto'], 'y sí los más recientes (manzana y lote)')

    # ---- de verdad no se ven ----
    pg.evaluate("() => { document.getElementById('modalMapeo').classList.remove('abierto'); estado={}; guarda('materia','rsu'); guarda('tiene_direccion','si'); guarda('alcaldia_dir','Coyoacán'); guarda('colonia','Del Carmen'); guarda('colonia_cve','03-021'); irA(2); ponMarcador(19.35,-99.162); }")
    pg.wait_for_timeout(300)
    vis = pg.evaluate("() => { irA(6); alternaDetalleRevision(); const t = document.body.innerText; return {uga: val('uga') && t.indexOf(val('uga')) >= 0, cve: t.indexOf('03-021') >= 0}; }")
    afirma(not vis['uga'] and not vis['cve'], 'lo que el mapeo dice que no se ve, no se ve en la revisión')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
