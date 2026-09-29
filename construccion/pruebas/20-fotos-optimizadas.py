# -*- coding: utf-8 -*-
"""Las fotos se optimizan en el navegador antes de subir (DEC-121).

   Se vigila lo que puede salir mal al tocar una prueba:
   1. Que pese menos y conserve detalle: 2048 px por el lado largo, JPG.
   2. Que respete la orientación con que se tomó.
   3. Que guarde la huella SHA-256 del ORIGINAL, y que sea la correcta.
   4. Que conserve la fecha y el lugar de captura del original.
   5. Que video y documentos no se toquen.
   6. Que, si no se puede optimizar o no conviene, se quede el original.
   7. Que mientras se optimiza no se pueda continuar, y que la persona vea
      qué pasa y cuánto se ahorró.
   Las imágenes de prueba se generan aquí, en una carpeta temporal: no se
   versionan archivos pesados."""
import os, pathlib, sys, tempfile, hashlib
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina20.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# ---------------- imágenes de prueba ----------------
FX = pathlib.Path(tempfile.mkdtemp(prefix='fotos_'))
rng = np.random.default_rng(1)
def foto(w, h):
    x = np.linspace(0, 255, w)[None, :]; y = np.linspace(0, 255, h)[:, None]
    base = np.stack([x + 0*y, y + 0*x, (x + y)/2], -1)
    return Image.fromarray(np.clip(base + rng.normal(0, 18, (h, w, 3)), 0, 255).astype('uint8'))
im = foto(4000, 3000); ex = im.getexif()
ex.get_ifd(0x8769)[0x9003] = '2026:09:15 08:31:02'
g = ex.get_ifd(0x8825); g[1] = 'N'; g[2] = (19.0, 21.0, 0.0); g[3] = 'W'; g[4] = (99.0, 9.0, 43.2)
im.save(FX/'grande.jpg', quality=95, exif=ex)
r = foto(3000, 2000); e2 = r.getexif(); e2[0x0112] = 6; r.save(FX/'girada.jpg', quality=92, exif=e2)
foto(2500, 1500).save(FX/'captura.png')
foto(200, 100).save(FX/'chica.jpg', quality=40)
(FX/'documento.pdf').write_bytes(b'%PDF-1.4\n' + os.urandom(3000))
(FX/'video.mp4').write_bytes(os.urandom(50000))
H = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in FX.iterdir()}
PESO = {p.name: p.stat().st_size for p in FX.iterdir()}

ESPERA = """() => new Promise(ok => { const t0 = Date.now();
  (function mira(){ if(!archivos.some(a => a.estado === 'optimizando') || Date.now()-t0 > 20000) ok(); else setTimeout(mira, 100); })(); })"""
DIMS = """async (nombre) => { const a = archivos.find(x => x.name === nombre); if(!a || !a.blob) return null;
  const b = await createImageBitmap(a.blob); return {w: b.width, h: b.height, tipo: a.blob.type}; }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':390,'height':800}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)
    pg.evaluate("() => { estado = {}; archivos = []; cfg.validar = true; guarda('materia','rsu'); irA(4); }")
    pg.wait_for_timeout(300)

    # ---- mientras optimiza: se ve y no deja continuar ----
    pg.evaluate("""() => { window._optimizaReal = optimizaFoto; window._suelta = null;
      window.optimizaFoto = f => new Promise(ok => { window._suelta = () => ok(window._optimizaReal(f)); }); }""")
    pg.set_input_files('#inputArch', [str(FX/'grande.jpg')]); pg.wait_for_timeout(600)
    d = pg.evaluate("""() => ({pend: archivos.some(a => a.estado === 'optimizando'),
      txt: document.getElementById('listaArch').innerText, pasa: valida(4),
      err: (document.getElementById('e_archivos')||{}).textContent || ''})""")
    afirma(d['pend'] and 'Optimizando' in d['txt'], 'mientras se optimiza, la lista dice «Optimizando…»')
    afirma(d['pasa'] is False and 'optimizarse' in d['err'], 'y no deja continuar: «%s»' % d['err'])
    pg.evaluate("() => { window._suelta(); window.optimizaFoto = window._optimizaReal; }")
    pg.evaluate(ESPERA)

    # ---- la foto grande ----
    a = pg.evaluate("() => { const a = archivos.find(x => x.name === 'grande.jpg'); const c = Object.assign({}, a); delete c.blob; return c; }")
    dims = pg.evaluate(DIMS, 'grande.jpg')
    afirma(a.get('optimizada') and a['size'] < PESO['grande.jpg'] * 0.35,
           'una foto de %.1f MB queda en %.2f MB' % (PESO['grande.jpg']/1048576, a['size']/1048576))
    afirma(dims and max(dims['w'], dims['h']) == 2048 and dims['tipo'] == 'image/jpeg',
           'a 2048 px por el lado largo, en JPG (%s)' % dims)
    afirma(a.get('sha256_original') == H['grande.jpg'], 'la huella SHA-256 es la del ORIGINAL')
    afirma(a.get('fecha_captura') == '2026-09-15T08:31:02', 'conserva la fecha de captura (%s)' % a.get('fecha_captura'))
    afirma(abs(a.get('lat_captura', 0) - 19.35) < 1e-4 and abs(a.get('lon_captura', 0) + 99.162) < 1e-4,
           'y el lugar de captura (%s, %s)' % (a.get('lat_captura'), a.get('lon_captura')))
    txt = pg.evaluate("() => document.getElementById('listaArch').innerText")
    afirma('→' in txt and 'MB' in txt, 'la lista muestra el ahorro: %r' % txt.replace('\n', ' ')[:80])
    pg.evaluate("() => { valida(4); }")
    afirma(pg.evaluate("() => valida(4)") is True, 'terminada la optimización, el paso continúa')

    # ---- orientación, PNG, documentos, video, foto chica ----
    pg.set_input_files('#inputArch', [str(FX/n) for n in ('girada.jpg','captura.png','documento.pdf','video.mp4','chica.jpg')])
    pg.wait_for_timeout(300); pg.evaluate(ESPERA)
    gd = pg.evaluate(DIMS, 'girada.jpg')
    afirma(gd and gd['h'] == 2048 and gd['w'] < gd['h'], 'una foto tomada en vertical sigue en vertical (%s)' % gd)
    pn = pg.evaluate(DIMS, 'captura.png')
    pa = pg.evaluate("() => { const a = archivos.find(x => x.name === 'captura.png'); return {opt: a.optimizada, size: a.size}; }")
    afirma(pn and pn['tipo'] == 'image/jpeg' and pa['opt'] and pa['size'] < PESO['captura.png'] / 5,
           'una captura PNG de %.1f MB pasa a JPG de %.2f MB' % (PESO['captura.png']/1048576, pa['size']/1048576))
    otros = pg.evaluate("""() => ['documento.pdf','video.mp4'].map(n => { const a = archivos.find(x => x.name === n);
      return {n, size: a.size, blob: a.blob ? a.blob.size : -1, opt: !!a.optimizada, huella: 'sha256_original' in a}; })""")
    afirma(all(o['size'] == PESO[o['n']] and o['blob'] == PESO[o['n']] and not o['opt'] for o in otros),
           'el PDF y el video no se tocan')
    ch = pg.evaluate("() => { const a = archivos.find(x => x.name === 'chica.jpg'); return {opt: a.optimizada, size: a.size, blob: a.blob.size, h: a.sha256_original}; }")
    afirma(ch['opt'] is False and ch['size'] == PESO['chica.jpg'] and ch['blob'] == PESO['chica.jpg'],
           'si optimizar no ahorra, se queda el original')
    afirma(ch['h'] == H['chica.jpg'], 'y aun así lleva su huella')

    # ---- navegador sin soporte: se sube el original ----
    pg.evaluate("() => { archivos = []; window._cib = window.createImageBitmap; window.createImageBitmap = undefined; }")
    pg.set_input_files('#inputArch', [str(FX/'grande.jpg')]); pg.wait_for_timeout(300); pg.evaluate(ESPERA)
    sn = pg.evaluate("() => { const a = archivos[0]; return {n: archivos.length, opt: a.optimizada, blob: a.blob.size, h: a.sha256_original, f: a.fecha_captura}; }")
    pg.evaluate("() => { window.createImageBitmap = window._cib; }")
    afirma(sn['n'] == 1 and sn['opt'] is False and sn['blob'] == PESO['grande.jpg'],
           'si el navegador no puede optimizar, la foto entra igual, original')
    afirma(sn['h'] == H['grande.jpg'] and sn['f'], 'con su huella y su fecha de captura')

    # ---- quitarla mientras se optimiza no rompe nada ----
    pg.evaluate("""() => { archivos = []; window._optimizaReal = optimizaFoto;
      window.optimizaFoto = f => new Promise(ok => { window._suelta = () => ok(window._optimizaReal(f)); }); }""")
    pg.set_input_files('#inputArch', [str(FX/'grande.jpg')]); pg.wait_for_timeout(400)
    pg.evaluate("() => { quitaArchivo(0); window._suelta(); window.optimizaFoto = window._optimizaReal; }")
    pg.evaluate(ESPERA); pg.wait_for_timeout(300)
    afirma(pg.evaluate("() => archivos.length") == 0, 'si se quita mientras se optimiza, no reaparece')

    # ---- el aviso de privacidad lo dice ----
    pv = pg.evaluate("() => { irA(5); const p = document.querySelector('.priv'); return p ? p.innerText : ''; }")
    afirma('fecha y el lugar en que se tomaron' in pv, 'el aviso de privacidad dice que se conservan fecha y lugar de las fotos')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
