# -*- coding: utf-8 -*-
"""Documentos jurídicos y de datos (DEC-236; bloque 3 de la auditoría del 20
   de octubre de 2026).

   La auditoría encontró documentos que contradecían al formulario porque se
   escribieron a mano y nadie los volvió a mirar cuando una decisión los dejó
   atrás. Esta batería los cruza con el código:
   1. D1-02: el apartado 3 del documento 03 repite, materia por materia, el
      fundamento de MATERIAS, y el apartado 2 da P-01 por resuelta.
   2. D1-03: la parte del documento 09 redactada a mano no lleva cifras de
      campos ni repite lo que el formulario ya no hace; la cabecera cuenta los
      datos personales de terceros igual que OBLIG.
   3. D1-11: el documento 04 dice lo que hace el formulario.
   4. D1-13: el documento 01 cuenta los documentos que hay, y los criterios
      del 11 no fijan a mano cuántos escenarios existen.
   5. Ninguna pregunta resuelta se presenta como abierta fuera de los
      documentos históricos. Lo «provisional» junto a una pregunta resuelta lo
      revisa la batería 36."""
import os, pathlib, re, sys
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent
DOC  = RAIZ.parent / 'documentacion'
RUTA = pathlib.Path(os.environ.get('ARTEFACTO', RAIZ / 'artefacto.html'))
TMP  = AQUI / '_pagina39.html'
CHROMIUM = os.environ.get('CHROMIUM')  # sin la variable, Playwright usa el Chromium que él mismo instala
from playwright.sync_api import sync_playwright
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
lee = lambda n: (DOC / n).read_text(encoding='utf-8')
def tramo(t, desde, hasta):
    i = t.index(desde); return t[i:t.index(hasta, i)]

TMP.write_text('<!doctype html><html lang="es"><head><meta charset="utf-8">' +
               RUTA.read_text(encoding='utf-8') + '</body></html>', encoding='utf-8')
with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=CHROMIUM)
    pg = nav.new_page(); pg.goto(TMP.as_uri()); pg.wait_for_timeout(600)
    cod = pg.evaluate("""() => ({
      materias: MATERIAS.map(m => [m.id, m.formal || m.nom, m.norma]),
      terceros: Object.values(OBLIG).filter(c => c.dp && c.fin === 'Responsable').length })""")
    nav.close()
TMP.unlink(missing_ok=True)

NUMS = (r'(?:\d+|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|'
        r'dieciséis|diecisiete|dieciocho|diecinueve|veinte|veinti\w+|(?:treinta|cuarenta|cincuenta|sesenta)(?: y \w+)?)')

# ---- 1. Documento 03 (D1-02) ----
d03 = lee('03-marco-juridico.md')
tabla = tramo(d03, '## 3. Fundamento por materia', '## 4. ')
filas = {m.group(2): (m.group(1), m.group(3)) for m in re.finditer(r'^\| (.+?) \| `([a-z_]+)` \| (.+) \|$', tabla, re.M)}
codigo = {i: (n, f) for i, n, f in cod['materias']}
afirma(set(filas) == set(codigo), 'el apartado 3 del documento 03 tiene las %d materias del formulario: sobran %s, faltan %s'
       % (len(codigo), sorted(set(filas) - set(codigo)), sorted(set(codigo) - set(filas))))
distintas = sorted(k for k in codigo if k in filas and filas[k][1] != codigo[k][1])
afirma(not distintas, 'y cada una cita exactamente lo mismo que `MATERIAS`: %s' % distintas)
afirma(all(filas[k][0] == codigo[k][0] for k in codigo if k in filas), 'con el mismo nombre de materia')
dos = tramo(d03, '## 2. ', '## 2 bis.')
afirma('Resuelto (P-01' in dos and 'artículo 191, fracción XXX' in dos and 'artículo 188, fracción XXXVIII' in dos,
       'el apartado 2 da P-01 por resuelta y cita el Reglamento Interior')
afirma('Adoptar la Vía A' not in d03, 'y ya no recomienda el «reporte ciudadano»')

# ---- 2. Documento 09 (D1-03) ----
d09 = lee('09-mapeo-campos-obligatorios.md')
cola = tramo(d09, '## 3. Hallazgos de la revisión de minimización', '## 5. ')
cifras = re.findall(r'\b' + NUMS + r'\s+(?:campos|datos|controles)\b', cola, re.I)
afirma(not cifras, 'la parte redactada a mano del documento 09 no cuenta campos: %s' % cifras)
viejas = [f for f in ('cincuenta y tres', 'dos esquemas', 'bloque de persona física', '(DEC-48)',
                      'no pide ningún dato de contacto', 'Seis campos') if f in cola]
afirma(not viejas, 'ni repite lo que el formulario ya no hace: %s' % viejas)
m = re.search(r'^\| De ellos, de terceros[^|]*\| (\d+) \|$', d09, re.M)
afirma(m and int(m.group(1)) == cod['terceros'], 'la cabecera cuenta %s datos de terceros, como OBLIG (%d)' % (m and m.group(1), cod['terceros']))

# ---- 3. Documento 04 (D1-11) ----
d04 = lee('04-modelo-de-datos.md')
afirma(all(f not in d04 for f in ('código postal son obligatorios', 'que el formulario remite a la PROFEPA', 'correo de contacto')),
       'el documento 04 ya no dice que el código postal es obligatorio ni que el formulario remite El Histórico Coyoacán')
afirma('`remite_a`' in d04 and 'ISO 8601' in d04 and '`LIMITES`' in d04,
       'y describe la remisión aparte, la fecha en ISO y los topes de longitud (DEC-235)')

# ---- 4. Encabezados y conteos (D1-13) ----
NUM = {19:'diecinueve', 20:'veinte', 21:'veintiún', 22:'veintidós', 23:'veintitrés', 24:'veinticuatro', 25:'veinticinco'}
n = len(list(DOC.glob('[0-9][0-9]-*.md')))
afirma(('Los %s documentos de este proyecto' % NUM.get(n, str(n))) in lee('01-ficha-del-proyecto.md'),
       'el documento 01 cuenta los %d documentos que hay' % n)
d11 = lee('11-ruta-de-trabajo.md')
vigente11 = d11[:d11.index('## 8. Bitácora de limpieza')]
afirma(not re.search(r'\b' + NUMS + r' escenarios\b', vigente11, re.I), 'los criterios del documento 11 no fijan a mano cuántos escenarios hay')
for nombre, viejo in (('02-reglas-de-negocio.md', '1.3 · 30 de septiembre'), ('04-modelo-de-datos.md', '2.0 · 30 de septiembre'),
                      ('11-ruta-de-trabajo.md', '1.6 · 30 de septiembre'), ('12-conformidad-con-la-norma.md', '1.2 · 18 de septiembre')):
    afirma(viejo not in lee(nombre)[:400], '%s ya no declara la versión %s' % (nombre, viejo))

# ---- 5. Ninguna pregunta resuelta se presenta como abierta ----
d05 = lee('05-decisiones-y-pendientes.md').split('\n')
reg = {}
for l in d05[d05.index('### Registro de respuestas'):]:
    if re.match(r'\| P-\d+ \|', l):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        reg[c[0]] = c[1]
resueltas = [p for p, t in reg.items() if t.strip() and not re.match(r'\*\*(Retirada|Consolidada|En parte)', t)]
HISTORICOS = {'05-decisiones-y-pendientes.md', '06-auditoria-estilos-ux-color.md', '07-auditoria-heuristica.md',
              '14-auditoria-paso-2.md', '16-auditoria-general.md'}
ABIERTA = ('sin resolver', 'cuando se resuelva', 'siguen abiertas', 'sigue abierta', 'pendiente de resolver')
abiertas = []
for f in sorted(DOC.glob('*.md')):
    if f.name in HISTORICOS or f.name.startswith('AUDITORIA'): continue
    t = f.read_text(encoding='utf-8')
    if f.name == '11-ruta-de-trabajo.md': t = vigente11
    for k, l in enumerate(t.split('\n'), 1):
        for p in resueltas:
            if re.search(re.escape(p) + r'(?!\d)', l) and (any(a in l for a in ABIERTA) or ('Depende de ' + p) in l):
                abiertas.append('%s:%d %s' % (f.name, k, p))
afirma(not abiertas, 'ninguna de las %d preguntas resueltas se presenta como abierta: %s' % (len(resueltas), abiertas[:6]))

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
