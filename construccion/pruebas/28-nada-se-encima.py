# -*- coding: utf-8 -*-
"""Nada se encima (DEC-186).

   En la versión con mapa de calles, el mapa y sus botones pasaban por encima
   de la barra fija de pasos al desplazar la página: la biblioteca del mapa
   numera sus capas del 200 al 1000 y la barra vale 40. Ninguna batería lo vio
   porque todas corren sobre la versión en línea, que dibuja el mapa sin esa
   biblioteca. Aquí se simula una capa alta dentro del mapa y, además, se
   recorre cada paso buscando lo mismo en general: algo sobre la barra fija,
   desborde a lo ancho, controles tapados o fuera de pantalla, textos cortados
   y la lista de colonias debajo de lo que tiene detrás."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina28.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright
TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

CAPA = """async () => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  cargaEscenario('urbano'); irA(2); await espera(500);
  const m = document.getElementById('mapa'), barra = document.querySelector('.barra-fija');
  const capa = document.createElement('div');
  capa.id = 'capaAlta'; capa.style.cssText = 'position:absolute;inset:0;z-index:1000';
  m.appendChild(capa);
  const cs = getComputedStyle(m);
  let encima = 0, muestras = 0;
  const y0 = m.getBoundingClientRect().top + scrollY;
  for (let y = y0 - 40; y < y0 + m.offsetHeight; y += 30) {
    window.scrollTo(0, y); await espera(15);
    const r = barra.getBoundingClientRect();
    for (let fx = 0.1; fx < 1; fx += 0.1) { muestras++;
      const el = document.elementFromPoint(r.left + r.width * fx, r.top + r.height * 0.5);
      if (el && el.closest('#mapa')) encima++; }
  }
  capa.remove(); window.scrollTo(0, 0);
  return {encima: encima, muestras: muestras, iso: cs.isolation, z: cs.zIndex, pos: cs.position}; }"""

RECORRIDO = """async () => {
  const out = [];
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const nombre = el => (el.id ? '#' + el.id : '') + '.' + String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className).split(' ')[0] + '<' + el.tagName.toLowerCase() + '>';
  const plegado = el => { const d = el.closest('details:not([open])'); return !!d && el.tagName !== 'SUMMARY' && !(el.closest('summary') && el.closest('summary').parentElement === d); };
  const pasos = [['urbano',0],['urbano',1],['urbano',2],['sin_calle',2],['urbano',3],['gobierno',3],['urbano',4],['urbano',5],['conservacion',5],['urbano',6],['urbano',7],['derivado',1],['fuera',2]];
  for (const [e, p] of pasos) {
    if (p === 0) { estado = {}; irA(0); }
    else { cargaEscenario(e); if (p === 7) { guarda('verificacion','si'); irA(6); enviar(); } else irA(p); }
    await espera(p === 2 ? 500 : 150);
    const barra = document.querySelector('.barra-fija'), H = document.documentElement.scrollHeight;
    if (barra && barra.offsetParent) for (let y = 0; y < H; y += 160) {
      window.scrollTo(0, y); await espera(10);
      const r = barra.getBoundingClientRect();
      for (let fx = 0.05; fx < 1; fx += 0.1) {
        const el = document.elementFromPoint(r.left + r.width * fx, r.top + r.height * 0.5);
        if (el && !barra.contains(el) && !el.contains(barra) && !el.closest('#panel') && !el.closest('#revision')) out.push([e, p, 'sobre la barra fija', nombre(el)]);
      }
    }
    if (document.documentElement.scrollWidth > innerWidth + 1) out.push([e, p, 'desborde a lo ancho', document.documentElement.scrollWidth + ' > ' + innerWidth]);
    const ctrls = [...document.querySelectorAll('#app button, #app a, #app input, #app select, #app textarea, #app summary, #franjaBorrador button')]
      .filter(x => x.offsetParent && x.type !== 'file' && x.type !== 'hidden' && !plegado(x));
    for (const c of ctrls) {
      c.scrollIntoView({block: 'center'}); await espera(5);
      const r = c.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
      if (r.left < -1 || r.right > innerWidth + 1) out.push([e, p, 'fuera de pantalla', nombre(c)]);
      const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      if (!el || el === c || c.contains(el) || el.contains(c)) continue;
      if (el.closest('label') && el.closest('label').contains(c)) continue;
      if ((c.type === 'radio' || c.type === 'checkbox') && c.parentElement && c.parentElement.contains(el)) continue;
      if (el.closest('#panel') || el.closest('#revision')) continue;
      out.push([e, p, 'tapado', nombre(c) + ' por ' + nombre(el)]);
    }
    for (const c of document.querySelectorAll('#app .btn, #app .opcion, #app .pendiente, #app .medio-etq, #app h2, #app h3')) {
      if (c.offsetParent && !plegado(c) && c.scrollWidth > c.clientWidth + 2) out.push([e, p, 'texto cortado', nombre(c) + ' «' + c.innerText.slice(0, 30) + '»']);
    }
    if (p === 2 && e === 'urbano') {
      const f = document.getElementById('f_colonia');
      f.scrollIntoView({block: 'center'}); f.focus(); f.click(); await espera(250);
      const ops = [...document.querySelectorAll('.combo-lista li')].filter(x => x.offsetParent);
      let tap = 0; for (const o of ops.slice(0, 8)) { const r = o.getBoundingClientRect(); if (r.bottom > innerHeight) continue;
        const el = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); if (!(el === o || o.contains(el))) tap++; }
      if (!ops.length) out.push([e, p, 'lista de colonias', 'no se abrió']);
      if (tap) out.push([e, p, 'lista de colonias', tap + ' opciones tapadas']);
      f.blur(); await espera(80);
    }
  }
  window.scrollTo(0, 0);
  return out; }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    for ancho, alto, nom in [(390, 760, 'teléfono'), (1280, 800, 'escritorio')]:
        pg = nav.new_context(viewport={'width':ancho,'height':alto}).new_page()
        err = []
        pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
        pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
        pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

        c = pg.evaluate(CAPA)
        afirma(c['iso'] == 'isolate' and c['z'] == '0' and c['pos'] == 'relative',
               '%s: el mapa vive en su propia capa (isolation %s, z-index %s)' % (nom, c['iso'], c['z']))
        afirma(c['muestras'] > 20 and c['encima'] == 0,
               '%s: una capa alta dentro del mapa no pasa por encima de la barra fija (%d de %d muestras)' % (nom, c['encima'], c['muestras']))

        r = pg.evaluate(RECORRIDO)
        for clase in ['sobre la barra fija', 'desborde a lo ancho', 'fuera de pantalla', 'tapado', 'texto cortado', 'lista de colonias']:
            h = sorted(set('paso %s (%s): %s' % (x[1], x[0], x[3]) for x in r if x[2] == clase))
            afirma(not h, '%s: en los trece estados recorridos, nada %s %s' % (nom,
                   {'sobre la barra fija':'pasa sobre la barra fija', 'desborde a lo ancho':'desborda a lo ancho', 'fuera de pantalla':'queda fuera de pantalla',
                    'tapado':'queda tapado por otro elemento', 'texto cortado':'tiene el texto cortado', 'lista de colonias':'tapa la lista de colonias'}[clase], h[:4]))
        afirma(err == [], '%s: sin errores propios en consola: %s' % (nom, err[:2]))
    nav.close()

# La regla está en la fuente, que es la que lleva la biblioteca del mapa.
fuente = (RAIZ.parent / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html')
if fuente.exists():
    t = fuente.read_text(encoding='utf-8')
    i = t.find('#mapa{height:330px')
    afirma(i > 0 and 'isolation:isolate' in t[i:i+400] and 'z-index:0' in t[i:i+400],
           'la versión con mapa de calles declara el mapa en su propia capa')

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
