# -*- coding: utf-8 -*-
"""El orden del paso 1, los plásticos de un solo uso y manzana y lote.

   Bloque del 22 de septiembre de 2026, derivado del análisis de la base
   histórica de la CIVASU —2,175 denuncias de 2024 a 2026— (documento 17).

   Lo que aquí se sujeta no es una lista de tarjetas, que va a cambiar, sino
   las tres reglas que hacen que ese orden signifique algo:

   · El grupo se referencia por CLAVE y no por índice de arreglo (DEC-108).
     Con índices, reordenar los bloques desalinea en silencio las materias que
     los apuntan, y nada avisa.
   · El cajón de sastre va al final de su bloque aunque sea el supuesto con más
     registros en la base: arriba se lleva las denuncias que tienen supuesto
     propio.
   · Las conductas de suelo de conservación se conservan aunque no tengan un
     solo registro: esa ausencia mide el canal y no la realidad (D-16).

   Y que ningún fundamento se escriba sin verificar: la materia de plásticos
   nace con el hueco a la vista (DEC-109)."""
import os, pathlib, sys, re
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina15.html'
CHROMIUM = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED', 'net::ERR_', 'Failed to load resource')
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    ctx = nav.new_context(viewport={'width': 1100, 'height': 900})
    pg = ctx.new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type == 'error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: ' + str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    # ---------- El catálogo ----------
    d = pg.evaluate("""() => ({
      grupos: GRUPOS_MATERIA.map(g => g.id),
      nomGrupos: GRUPOS_MATERIA.map(g => g.nom),
      total: MATERIAS.length,
      gs: MATERIAS.map(m => m.g),
      ids: MATERIAS.map(m => m.id),
      notas: Object.keys(NOTAS_GRUPO),
      porGrupo: GRUPOS_MATERIA.map(g => MATERIAS.filter(m => m.g === g.id).map(m => m.id)),
      normaPlasticos: (MATERIAS.filter(m => m.id === 'plasticos')[0] || {}).norma || '',
      sinIcono: MATERIAS.filter(m => !ICONOS[m.ico]).map(m => m.id)
    })""")

    afirma(d['total'] == 19, 'el catálogo tiene 19 materias: %d' % d['total'])
    afirma(all(isinstance(g, str) for g in d['gs']),
           'toda materia apunta a su grupo por clave de texto, no por índice')
    huerfanas = [i for i, g in zip(d['ids'], d['gs']) if g not in d['grupos']]
    afirma(huerfanas == [], 'ninguna materia apunta a un grupo inexistente: %s' % huerfanas)
    vacios = [g for g, l in zip(d['grupos'], d['porGrupo']) if not l]
    afirma(vacios == [], 'ningún bloque queda vacío: %s' % vacios)
    afirma(all(k in d['grupos'] for k in d['notas']),
           'las notas de bloque cuelgan de una clave viva: %s' % d['notas'])
    afirma(d['sinIcono'] == [], 'toda materia tiene icono: %s' % d['sinIcono'])

    # El cajón de sastre, al final de su bloque.
    bloqueZonas = d['porGrupo'][d['grupos'].index('zonas')]
    afirma(bloqueZonas[-1] == 'ava',
           'el cajón de sastre va al final de su bloque: %s' % bloqueZonas[-1])

    # D-16: lo que no tiene volumen en la base se conserva.
    afirma(set(['terraceos', 'agroquimicos', 'tala', 'asentamiento', 'agua_zona']).issubset(set(d['ids'])),
           'las conductas de suelo de conservación siguen en el catálogo')

    # Ningún fundamento inventado: el hueco queda a la vista.
    n = d['normaPlasticos']
    afirma('[Art. __' in n, 'la materia de plásticos declara su fundamento como hueco: %r' % n[:60])
    afirma(re.search(r'[Aa]rt\.\s*\d', n) is None,
           'no se escribió ningún número de artículo sin verificar: %r' % n[:60])

    # ---------- Lo que se ve en pantalla ----------
    pg.evaluate("irA(1)"); pg.wait_for_timeout(250)

    v = pg.evaluate("""() => {
      const bl = [...document.querySelectorAll('#listaMaterias h3.grupo-materia')].map(h => h.textContent.trim());
      const tar = [...document.querySelectorAll('#listaMaterias .lista-op .fila-op')];
      const nom = tar.map(b => b.querySelector('.fo-nom').textContent.trim());
      const y = {}; tar.forEach(b => { y[b.querySelector('.fo-nom').textContent.trim()] = Math.round(b.getBoundingClientRect().top + window.scrollY); });
      return {bloques: bl, nombres: nom, y: y, alto: Math.round(document.querySelector('.tarjeta').getBoundingClientRect().height)};
    }""")

    afirma(v['bloques'] == d['nomGrupos'],
           'los bloques se pintan en el orden declarado: %s' % ' · '.join(v['bloques']))
    afirma(v['bloques'][0].startswith('Obras'),
           'el primer bloque es el de mayor volumen en la base: %r' % v['bloques'][0])
    afirma(v['nombres'][0] == 'Impacto ambiental de una obra',
           'la primera tarjeta es el supuesto más denunciado: %r' % v['nombres'][0])
    afirma(len(v['nombres']) == 19, 'se pintan las 19 tarjetas: %d' % len(v['nombres']))
    afirma('Plásticos de un solo uso' in v['nombres'], 'la materia de plásticos aparece en la lista')

    # Lo que se comprueba es la regla, no la tabla: fijar aquí los nombres de
    # las cinco primeras tarjetas congelaría el orden y haría fallar la prueba
    # cada vez que el orden cambie a propósito. Lo que no puede cambiar es que
    # la pantalla pinte el orden del catálogo, que es su única fuente.
    esperado = pg.evaluate("""() => GRUPOS_MATERIA.reduce((a,g) =>
      a.concat(MATERIAS.filter(m => m.g === g.id).map(m => m.nom)), [])""")
    afirma(v['nombres'] == esperado,
           'la pantalla pinta exactamente el orden del catálogo (%d tarjetas)' % len(esperado))
    print('ORDEN de las cinco primeras: %s' % ' · '.join(v['nombres'][:5]))

    # El buscador encuentra la materia nueva por una palabra de la calle.
    pg.evaluate("guarda('filtro','globos'); renderMaterias()"); pg.wait_for_timeout(200)
    f = pg.evaluate("""() => [...document.querySelectorAll('#listaMaterias .fo-nom')].map(x => x.textContent.trim())""")
    afirma(f == ['Plásticos de un solo uso'],
           'buscar «globos» lleva a la materia de plásticos: %s' % f)
    pg.evaluate("guarda('filtro',''); render()"); pg.wait_for_timeout(200)

    # ---------- Elegir plásticos avanza y se conserva ----------
    pg.evaluate("eligeMateria('plasticos')"); pg.wait_for_timeout(300)
    est = pg.evaluate("() => ({paso: paso, materia: val('materia')})")
    afirma(est['paso'] == 2 and est['materia'] == 'plasticos',
           'elegir plásticos avanza al paso 2 y queda guardada: %s' % est)

    # ---------- Manzana y lote ----------
    pg.evaluate("guarda('tiene_direccion','si'); render()"); pg.wait_for_timeout(300)
    m = pg.evaluate("""() => {
      const ids = [...document.querySelectorAll('#c_lat, .campo')].map(c => (c.querySelector('input,select,textarea')||{}).name).filter(Boolean);
      const mz = document.getElementsByName('manzana')[0], lt = document.getElementsByName('lote')[0];
      const req = c => !!(c && c.closest('.campo') && c.closest('.campo').querySelector('.req'));
      return {orden: ids, hayMz: !!mz, hayLt: !!lt, mzReq: req(mz), ltReq: req(lt)};
    }""")
    afirma(m['hayMz'] and m['hayLt'], 'manzana y lote se piden cuando el lugar tiene domicilio')
    afirma(not m['mzReq'] and not m['ltReq'], 'ninguno de los dos es obligatorio')
    o = m['orden']
    afirma(o.index('manzana') > o.index('num_ext') and o.index('manzana') < o.index('colonia'),
           'van después del número exterior y antes de la colonia: %s' % ' → '.join(o[:8]))

    # Lo capturado sobrevive a salir y volver al paso.
    pg.evaluate("guarda('manzana','118'); guarda('lote','1'); irA(3); irA(2)"); pg.wait_for_timeout(300)
    g = pg.evaluate("() => [ (document.getElementsByName('manzana')[0]||{}).value, (document.getElementsByName('lote')[0]||{}).value ]")
    afirma(g == ['118', '1'], 'lo capturado en manzana y lote se conserva: %s' % g)

    # Sin domicilio no se piden: ahí no hay manzana que valga.
    pg.evaluate("guarda('tiene_direccion','no'); render()"); pg.wait_for_timeout(300)
    s = pg.evaluate("() => !!document.getElementsByName('manzana')[0] || !!document.getElementsByName('lote')[0]")
    afirma(not s, 'sin domicilio no se piden manzana ni lote')

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])

    # ---------- Medición en teléfono ----------
    pg2 = nav.new_context(viewport={'width': 390, 'height': 760}).new_page()
    pg2.goto(TMP.as_uri()); pg2.wait_for_timeout(600)
    pg2.evaluate("irA(1)"); pg2.wait_for_timeout(250)
    med = pg2.evaluate("""() => {
      const tar = [...document.querySelectorAll('#listaMaterias .lista-op .fila-op')];
      const y = t => Math.round(t.getBoundingClientRect().top + window.scrollY);
      return {impacto: y(tar[0]), ultima: y(tar[tar.length-1]),
              alto: Math.round(document.querySelector('.tarjeta').getBoundingClientRect().height)};
    }""")
    print('MEDICIÓN en teléfono de 390 px: primera tarjeta a %d px · última a %d px · paso 1 de %d px (%.1f pantallas)'
          % (med['impacto'], med['ultima'], med['alto'], med['alto'] / 760.0))
    afirma(med['impacto'] < 760,
           'el supuesto más denunciado se ve sin desplazar en teléfono: %d px' % med['impacto'])
    pg2.close(); pg.close(); nav.close()

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
