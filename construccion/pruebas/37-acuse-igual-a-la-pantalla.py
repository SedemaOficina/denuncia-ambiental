# -*- coding: utf-8 -*-
"""El acuse dice lo mismo en la pantalla y en el PDF (DEC-232; bloque 2 de la
   auditoría del 20 de octubre de 2026).

   La auditoría encontró que el PDF que la persona conserva prometía una
   visita de inspección en las rutas federal y de autoridad, donde la pantalla
   decía otra cosa (B3-01); que el fundamento seguía «por confirmar: depende
   de la naturaleza jurídica del canal» con P-01 ya resuelta, y que ni la
   pantalla ni el PDF mencionaban a la Procuraduría (G1-01); y que la revisión
   y el acuse decían «entre Entre la calle Sur 20» (C5-01).

   Por cada escenario que llega al acuse se comprueba:
   1. Los pasos de «¿Qué sigue?» están en el PDF, en el mismo orden que en la
      pantalla, y sólo la ruta de inspección promete una visita.
   2. El fundamento es el mismo en los dos y cita el Reglamento Interior con
      el artículo del área que atiende; no queda el hueco ni la duda de P-01.
   3. La Procuraduría y la Fiscalía se mencionan en los dos, salvo en la ruta
      federal, que remite a la PROFEPA.
   4. Ni la revisión ni el PDF dicen «entre entre».
   Y además, que el marcador de «¿Entre qué calles?» ya no invita a escribir
   «Entre» y que la regla que lo antepone no lo duplica."""
import os, pathlib, re, subprocess, sys, tempfile
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina37.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
EXTERNO = ('ERR_TUNNEL_CONNECTION_FAILED','net::ERR_','Failed to load resource')
SALIDA = pathlib.Path(os.environ.get('ACUSE_PDF', tempfile.gettempdir()))
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
plano = lambda t: re.sub(r'\s+', ' ', t or '').strip()

# Escenarios que llegan al acuse y el área que debe atenderlos.
AREA = {'sin_calle': 'DGCORENADR', 'urbano': 'DGIVA', 'conservacion': 'DGCORENADR', 'gobierno': 'DGIVA',
        'ava': 'DGIVA', 'anp_coadmin': 'FEDERAL', 'anp_federal': 'FEDERAL', 'otro_giro': 'DGIVA'}
ARTICULO = {'DGIVA': 'artículo 191, fracción XXX', 'DGCORENADR': 'artículo 188, fracción XXXVIII',
            'FEDERAL': 'artículo 188, fracción XXXVIII'}

LEE = """(e) => { cargaEscenario(e); guarda('verificacion','si'); irA(6);
  const rev = document.getElementById('app').textContent;
  enviar();
  const sig = document.querySelector('.pasos-sig');
  const tras = t => { const h = [...sig.querySelectorAll('h3')].find(x => x.textContent.trim() === t);
                      return h ? h.nextElementSibling.textContent : null; };
  const pasos = [...sig.querySelectorAll('ol li')].map(li => { const c = li.cloneNode(true);
    c.querySelectorAll('.pendiente').forEach(x => x.remove()); return c.textContent.trim(); });
  return construyeAcusePdf().then(u => ({rev, pasos, fund: tras('Fundamento'), vias: tras('Otras vías'),
    dg: val('dg'), pdf: Array.from(u)})); }"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_context(viewport={'width':1200,'height':900}).new_page()
    err = []
    pg.on('console', lambda m: err.append(m.text) if m.type=='error' and not any(x in m.text for x in EXTERNO) else None)
    pg.on('pageerror', lambda e: err.append('pageerror: '+str(e)))
    pg.goto(TMP.as_uri()); pg.wait_for_timeout(700)

    for esc, area in AREA.items():
        r = pg.evaluate(LEE, esc)
        ruta = SALIDA / ('acuse37-%s.pdf' % esc)
        ruta.write_bytes(bytes(r['pdf']))
        pdf = plano(subprocess.run(['pdftotext', '-enc', 'UTF-8', str(ruta), '-'], capture_output=True, text=True, encoding='utf-8').stdout)
        pasos = [plano(p) for p in r['pasos']]
        afirma(r['dg'] == area, '%s: lo atiende %s (%s)' % (esc, area, r['dg']))

        # 1. Los pasos, iguales y en orden
        pos = [pdf.find(p) for p in pasos]
        afirma(pasos and -1 not in pos and pos == sorted(pos),
               '%s: los %d pasos de «¿Qué sigue?» están en el PDF, en el orden de la pantalla (%s)' % (esc, len(pasos), pos))
        todos = ' '.join(pasos)
        if area == 'FEDERAL':
            afirma('visita' not in todos and 'remite a la PROFEPA' in todos and 'por cuenta de la PROFEPA' in todos,
                   '%s: no promete visita; dice que se remite y que el seguimiento es de la PROFEPA' % esc)
        elif esc == 'gobierno':
            afirma('artículo 331' in todos and 'recomendaciones' in todos and 'Personal de inspección' not in todos,
                   '%s: ante una autoridad, recomendaciones del artículo 331 y no visita' % esc)
        else:
            afirma('Personal de inspección visita el lugar' in todos, '%s: la ruta de inspección dice la visita' % esc)

        # 2. El fundamento
        fund = plano(r['fund'])
        afirma(fund and fund in pdf, '%s: el fundamento de la pantalla es el del PDF' % esc)
        afirma('Reglamento Interior del Poder Ejecutivo y de la Administración Pública de la Ciudad de México' in fund
               and ARTICULO[area] in fund, '%s: cita el Reglamento Interior, %s' % (esc, ARTICULO[area]))
        afirma(('artículo 331' in fund) == (esc == 'gobierno'), '%s: suma el artículo 331 sólo ante una autoridad' % esc)
        afirma('[Art. __' not in pdf and 'naturaleza jurídica' not in pdf and 'Por confirmar' not in pdf,
               '%s: el PDF ya no dice que el fundamento depende de P-01' % esc)
        a, b = pdf.find('FUNDAMENTO'), pdf.find('Fundamento jurídico')
        afirma(-1 < a < b and 'Página' not in pdf[a:b], '%s: la barra «Fundamento» no queda sola al pie de una página' % esc)

        # 3. Las otras vías
        vias = plano(r['vias'])
        if area == 'FEDERAL':
            afirma(not vias and 'Ordenamiento Territorial' not in pdf, '%s: sin otras vías; la PROFEPA ya la ofrece la ficha' % esc)
        else:
            afirma('Procuraduría Ambiental y del Ordenamiento Territorial' in vias and 'fundada y motivada' in vias
                   and 'Fiscalía General de Justicia' in vias, '%s: menciona la Procuraduría y la Fiscalía' % esc)
            afirma('días hábiles' not in vias and 'ratific' not in vias,
                   '%s: sin plazos ni ratificación de la Procuraduría (DEC-138, DEC-162)' % esc)
            afirma(vias in pdf, '%s: y el PDF lo dice igual' % esc)

        # 4. Sin «entre entre»
        afirma(not re.search(r'entre\s+entre', r['rev'], re.I) and not re.search(r'entre\s+entre', pdf, re.I),
               '%s: ni la revisión ni el PDF dicen «entre entre»' % esc)

    # Sin punto todavía no se sabe qué área atiende: se citan las dos.
    sin = pg.evaluate("""() => { cargaEscenario('urbano'); guarda('lat',''); guarda('lon',''); return fundamentoAcuse(); }""")
    afirma('artículos 188, fracción XXXVIII, y 191, fracción XXX' in sin, 'sin punto, el fundamento cita los dos artículos')

    # El domicilio del escenario de autoridad lleva un solo «entre»
    dom = pg.evaluate("""() => { cargaEscenario('gobierno'); irA(6); return document.getElementById('app').textContent; }""")
    afirma(dom.count('entre la calle Sur 20 y la calle Sur 24') == 1, 'el domicilio dice «entre la calle Sur 20 y la calle Sur 24», una vez')
    afirma('Entre 5 de Mayo y 16 de Septiembre' in dom, 'y el lugar, escrito como el marcador, recibe su «Entre»')

    # La regla que antepone «entre»
    for v, may, esperado in (('Sur 20 y Sur 24', True, 'Entre Sur 20 y Sur 24'),
                             ('Sur 20 y Sur 24', False, 'entre Sur 20 y Sur 24'),
                             ('Entre la calle Sur 20 y la calle Sur 24', False, 'entre la calle Sur 20 y la calle Sur 24'),
                             ('ENTRE  Morelos y Juárez', True, 'Entre Morelos y Juárez'),
                             ('Entretenimiento y Sur 24', True, 'Entre Entretenimiento y Sur 24'),
                             ('', True, '')):
        obt = pg.evaluate("([v, m]) => entreCalles(v, m)", [v, may])
        afirma(obt == esperado, 'entreCalles(%r) da %r' % (v, obt))

    # El marcador ya no invita a escribir «Entre»
    mk = pg.evaluate("""() => { cargaEscenario('urbano'); irA(2); const a = document.getElementById('f_entre_calles').placeholder;
      irA(5); return [a, document.getElementById('f_dom_entre_calles').placeholder]; }""")
    afirma(mk == ['Ej. Sur 20 y Sur 24', 'Ej. Sur 20 y Sur 24'], 'el marcador de los dos «¿Entre qué calles?» es «Ej. Sur 20 y Sur 24»: %s' % mk)

    afirma(err == [], 'sin errores propios en consola: %s' % err[:2])
    nav.close()

TMP.unlink(missing_ok=True)
print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
