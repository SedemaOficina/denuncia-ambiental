# -*- coding: utf-8 -*-
"""Quién atiende una denuncia dentro de un parque federal (DEC-89, P-22).

   El prototipo turnaba a la DGCORENADR las Áreas Naturales Protegidas
   federales con convenio, como si el convenio le diera a la Secretaría
   facultades de inspección. La cláusula SEGUNDA del Convenio Marco
   CONANP-CDMX deja a salvo, con todas sus letras, las facultades del Título
   Sexto de la Ley General del Equilibrio Ecológico, que es el que atribuye
   la inspección a la autoridad federal.

   **Es un criterio provisional.** Interpretar el convenio frente al
   Reglamento Interior y al Manual corresponde a las áreas y a la unidad
   jurídica, no al prototipo, y la pregunta está abierta en P-22. Mientras se
   resuelve, el formulario asume la competencia federal —la lectura que no
   produce un acto viciado si resulta la correcta— y lo advierte en pantalla.

   Esta batería comprueba ese comportamiento provisional: **ningún punto
   dentro de un parque federal se turna a la Secretaría**, tenga convenio o
   no, y **la pantalla dice que el criterio está a consulta**. Si P-22 se
   resuelve en otro sentido, esta batería cambia con la regla."""
import os, pathlib, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina11.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

# Busca un punto dentro de cada rasgo: primero el centro de la envolvente y,
# si cae fuera —los poligonos concavos lo hacen—, una rejilla dentro de ella.
DENTRO = """(nombre) => {
  const f = CAPAS_GEOM.find(x => x.p.nombre === nombre);
  if(!f) return null;
  const pts = [];
  (function rec(x){
    if(Array.isArray(x) && x.length === 2 && typeof x[0] === 'number') pts.push(x);
    else if(Array.isArray(x)) x.forEach(rec);
  })(f.g.coordinates);
  const lons = pts.map(p => p[0]), lats = pts.map(p => p[1]);
  const x0 = Math.min(...lons), x1 = Math.max(...lons);
  const y0 = Math.min(...lats), y1 = Math.max(...lats);
  for(let i = 1; i < 12; i++) for(let j = 1; j < 12; j++){
    const lo = x0 + (x1 - x0) * i / 12, la = y0 + (y1 - y0) * j / 12;
    const hit = buscaEn(CAPAS_GEOM, la, lo, p => p.nombre === nombre);
    if(hit) return {lat: la, lon: lo};
  }
  return null;
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1100,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---- 1. El catálogo coincide con la cláusula PRIMERA del convenio ----
    d = pg.evaluate("""() => ({
      convenio: Object.keys(ANP_COADMIN),
      federales: CAPAS_GEOM.filter(f => f.p.grupo === 'ANP · Federal').map(f => f.p.nombre),
      firma: CONVENIO_CONANP.firma, vigencia: CONVENIO_CONANP.vigencia,
      ajusco: ANP_COADMIN['Cumbres del Ajusco'],
      estrella: ANP_COADMIN['Cerro de la Estrella (federal)'],
      insurgente: ANP_COADMIN['Insurgente Miguel Hidalgo y Costilla']
    })""")
    afirma(len(d['convenio']) == 8, 'el convenio ampara ocho parques (%d)' % len(d['convenio']))
    fuera = [n for n in d['federales'] if n not in d['convenio']]
    afirma(fuera == ['El Histórico Coyoacán'],
           'el único parque federal fuera del convenio es El Histórico Coyoacán: %s' % fuera)
    afirma(d['firma'] == '10 de marzo de 2025' and d['vigencia'] == '30 de septiembre de 2030',
           'el convenio lleva su fecha de firma y su vigencia')
    # Los tres datos que el convenio corrigió.
    afirma(d['ajusco']['decreto'] == '23 de septiembre de 1936',
           'Cumbres del Ajusco lleva la fecha de decreto del convenio')
    afirma(abs(d['estrella']['ha'] - 1183.33) < 0.01, 'Cerro de la Estrella, 1 183.33 ha')
    afirma(abs(d['insurgente']['ha'] - 1889.96) < 0.01, 'Insurgente Miguel Hidalgo y Costilla, 1 889.96 ha')

    # ---- 2. La invariante: ningún parque federal se turna a la Secretaría ----
    turnados = []
    for nombre in d['federales']:
        pt = pg.evaluate(DENTRO, nombre)
        if not pt:
            notas.append('OK  (sin punto interior de muestra para %s)' % nombre)
            continue
        r = pg.evaluate("""([a,b]) => { ponMarcador(a,b);
          return {dg: val('dg_nombre'), razon: val('dg_razon'), tipo: val('capa_tipo'), nombre: val('capa_nombre')}; }""",
          [pt['lat'], pt['lon']])
        turnados.append((nombre, r))
    locales = [n for n, r in turnados if 'PROFEPA' not in (r['dg'] or '')]
    afirma(locales == [],
           'ninguno de los %d parques federales se turna a la Secretaría: %s' % (len(turnados), locales))

    # ---- 3. Con convenio y sin convenio se explican distinto ----
    for nombre, conConvenio in [('Desierto de los Leones', True), ('El Histórico Coyoacán', False)]:
        pt = pg.evaluate(DENTRO, nombre)
        afirma(pt is not None, 'hay un punto de muestra dentro de %s' % nombre)
        if not pt: continue
        r = pg.evaluate("""([a,b]) => { ponMarcador(a,b);
          return {dg: val('dg_nombre'), razon: val('dg_razon'), tipo: val('capa_tipo')}; }""",
          [pt['lat'], pt['lon']])
        afirma('PROFEPA' in r['dg'], '%s se turna a la PROFEPA' % nombre)
        if conConvenio:
            afirma('coadyuva' in r['razon'] and 'inspección y vigilancia' in r['razon'],
                   '%s: se dice que la Secretaría coadyuva y que el convenio deja a salvo la inspección' % nombre)
            afirma('2030' in r['razon'], 'y se cita la vigencia del convenio')
            afirma('coadyuva' in r['tipo'], 'el tipo de suelo lo refleja: %r' % r['tipo'])
        else:
            afirma('no participa' in r['razon'],
                   '%s: se dice que la Secretaría ni siquiera participa en la administración' % nombre)
        afirma('recibe y la remite' in r['razon'],
               '%s: la Secretaría recibe la denuncia y la remite, no la devuelve' % nombre)
        # El aviso vive en la ficha del cruce, que sólo existe dentro del paso 2.
        aviso = pg.evaluate("""([a,b]) => {
          cfg.validar = true; guarda('materia','rsu'); guarda('tiene_direccion','no');
          irA(2); ponMarcador(a,b);
          const c = document.getElementById('panelCapas');
          return c ? c.innerText : '';
        }""", [pt['lat'], pt['lon']])
        afirma('a consulta de las áreas' in aviso,
               '%s: la pantalla advierte que el criterio está a consulta (P-22)' % nombre)

    # ---- 4. Lo local sigue siendo local ----
    pt = pg.evaluate(DENTRO, 'Bosque de Tlalpan')
    if pt:
        r = pg.evaluate("""([a,b]) => { ponMarcador(a,b); return val('dg_nombre'); }""", [pt['lat'], pt['lon']])
        afirma('Recursos Naturales' in r, 'un Área Natural Protegida local sigue siendo de la Secretaría')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
