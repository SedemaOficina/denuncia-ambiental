# -*- coding: utf-8 -*-
"""Coherencia documental (DEC-229).

   La auditoría del 20 de octubre de 2026 encontró que DEC-228 había cerrado
   la fase 1 con tres criterios de salida sin cumplir, que el encabezado del
   documento 05 contaba mal las preguntas, que cuatro decisiones se citaban
   en el código sin estar registradas y que varios documentos seguían
   llamando «provisional» a un criterio ya resuelto. Ninguna batería lo veía,
   porque todas leían el formulario y ninguna los documentos.

   Esta batería lee los documentos y los cruza entre sí:
   1. La tabla de decisiones: numeración sin huecos ni duplicados, cinco
      celdas por renglón, un estado válido y que remite a una decisión que existe.
   2. Toda decisión citada en documentos, prototipo o pruebas existe.
   3. El encabezado del documento 05 cuenta lo mismo que el registro de respuestas.
   4. Una pregunta retirada o consolidada no se cita como vigente fuera del 05.
   5. La fase 1 sólo puede decirse «cerrada» si sus criterios lo están, y los
      documentos 01 y 11 dicen lo mismo de ella."""
import os, pathlib, re, io, sys, collections
AQUI = pathlib.Path(os.path.abspath(__file__)).parent
RAIZ = AQUI.parent.parent
DOC = RAIZ / 'documentacion'
PROTO = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
TSV = RAIZ / 'revision' / 'control-observaciones-2026-10-19.tsv'
fallos, notas = [], []
def afirma(c, m): (notas if c else fallos).append(('OK  ' if c else 'FALLA ') + m)
lee = lambda p: p.read_text(encoding='utf-8')

d05 = lee(DOC / '05-decisiones-y-pendientes.md')
L = d05.split('\n')

# 1. Tabla de decisiones
i0 = L.index('| Clave | Decisión | Fecha | Razón | Estado |') if '| Clave | Decisión | Fecha | Razón | Estado |' in L else -1
afirma(i0 >= 0, 'la tabla de decisiones tiene columna «Estado»')
filas = [l for l in L if re.match(r'\| DEC-\d+ \|', l)]
nums = [int(re.match(r'\| DEC-(\d+)', l).group(1)) for l in filas]
dups = [n for n, c in collections.Counter(nums).items() if c > 1]
huecos = sorted(set(range(1, max(nums) + 1)) - set(nums))
afirma(not dups and not huecos, 'numeración de DEC-01 a DEC-%d sin huecos ni duplicados (huecos %s, duplicadas %s)' % (max(nums), huecos, dups))
mal_celdas = [n for n, l in zip(nums, filas) if l.rstrip().count('|') != 6]
afirma(not mal_celdas, 'cada decisión tiene cinco celdas: %s' % mal_celdas[:8])
ESTADO = re.compile(r'^(Vigente|No asignada|(Modificada|Revocada|Revertida|Sustituida|Superada) por (DEC-\d+)(, DEC-\d+)*)$')
existentes = set('DEC-%02d' % n if n < 10 else 'DEC-%d' % n for n in nums)
malos, colgados = [], []
for n, l in zip(nums, filas):
    e = l.rstrip().rstrip('|').split('|')[-1].strip()
    if not ESTADO.match(e): malos.append((n, e[:40]))
    for d in re.findall(r'DEC-\d+', e):
        if d not in existentes or int(d[4:]) <= n: colgados.append((n, d))
afirma(not malos, 'cada estado es válido: %s' % malos[:5])
afirma(not colgados, 'cada estado remite a una decisión posterior que existe: %s' % colgados[:5])

# 2. Toda decisión citada existe
fuentes = list(DOC.glob('*.md')) + [PROTO] + list((RAIZ / 'construccion' / 'pruebas').glob('*.py'))
sin_registro = collections.defaultdict(set)
for f in fuentes:
    for d in re.findall(r'DEC-(\d+)', lee(f)):
        k = 'DEC-%02d' % int(d) if int(d) < 10 else 'DEC-%d' % int(d)
        if k not in existentes: sin_registro[k].add(f.name)
afirma(not sin_registro, 'toda decisión citada está registrada en el 05: %s' % dict(list(sin_registro.items())[:4]))
proto = lee(PROTO)
m = re.search(r"VERSION_FORMULARIO\s*=\s*\{dec:'(DEC-\d+)'", proto)
afirma(m and int(m.group(1)[4:]) == max(nums), 'el prototipo declara la última decisión: %s / DEC-%d' % (m and m.group(1), max(nums)))

# 3. Encabezado contra registro de respuestas
reg = {}
for l in L[L.index('### Registro de respuestas'):]:
    if re.match(r'\| P-\d+ \|', l):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        reg[c[0]] = c[1]
def clase(t):
    if not t.strip(): return 'sin'
    if t.startswith('**Retirada'): return 'retirada'
    if t.startswith('**Consolidada'): return 'consolidada'
    if t.startswith('**En parte'): return 'parte'
    return 'resuelta'
cuenta = collections.Counter(clase(t) for t in reg.values())
NUM = {1:'una',2:'dos',3:'tres',4:'cuatro',5:'cinco',6:'seis',7:'siete',8:'ocho',9:'nueve',10:'diez',11:'once',12:'doce',13:'trece',
       14:'catorce',15:'quince',16:'dieciséis',17:'diecisiete',18:'dieciocho',19:'diecinueve',20:'veinte',21:'veintiuna',22:'veintidós',23:'veintitrés',24:'veinticuatro'}
cab = '\n'.join(L[:8])
esperado = {'resuelta': '%s resueltas', 'parte': '%s respondidas en parte', 'sin': '%s todavía sin respuesta',
            'retirada': '%s retiradas', 'consolidada': '%s consolidada'}
falta = [esperado[k] % NUM[v] for k, v in cuenta.items() if (esperado[k] % NUM[v]) not in cab
         and (esperado[k].replace('%s ', '') if v == 1 else '') not in cab]
afirma(('las %s preguntas' % NUM[len(reg)]) in cab, 'el encabezado cuenta %d preguntas' % len(reg))
afirma(not falta, 'el encabezado coincide con el registro %s: falta %s' % (dict(cuenta), falta))
sin_resp = sorted(p for p, t in reg.items() if clase(t) == 'sin')
afirma(all(p in cab for p in sin_resp), 'el encabezado nombra las preguntas sin respuesta: %s' % sin_resp)

# 4. Preguntas retiradas o consolidadas fuera del 05
HISTORICOS = {'05-decisiones-y-pendientes.md', '06-auditoria-estilos-ux-color.md', '07-auditoria-heuristica.md',
              '14-auditoria-paso-2.md', '16-auditoria-general.md'}
# La bitácora del documento 11 es historia: cuenta lo que se pensaba entonces.
BITACORA = lee(DOC / '11-ruta-de-trabajo.md').split('\n').index('## 8. Bitácora de limpieza') + 1
cerradas = [p for p, t in reg.items() if clase(t) in ('retirada', 'consolidada')]
vivas = []
for f in DOC.glob('*.md'):
    if f.name in HISTORICOS or f.name.startswith('AUDITORIA'): continue
    for n, l in enumerate(lee(f).split('\n'), 1):
        if f.name == '11-ruta-de-trabajo.md' and n >= BITACORA: continue
        for p in cerradas:
            if re.search(re.escape(p) + r'(?!\d)', l) and not re.search(r'antes ' + re.escape(p) + r'|absorbió ' + re.escape(p) + r'|' + re.escape(p) + r' (retirada|consolidada)', l):
                vivas.append('%s:%d %s' % (f.name, n, p))
afirma(not vivas, 'ninguna pregunta retirada o consolidada se cita como vigente: %s' % vivas[:6])
resueltas = [p for p, t in reg.items() if clase(t) == 'resuelta']
provis = []
for f in DOC.glob('*.md'):
    if f.name in HISTORICOS or f.name.startswith('AUDITORIA'): continue
    for n, l in enumerate(lee(f).split('\n'), 1):
        if f.name == '11-ruta-de-trabajo.md' and n >= BITACORA: continue
        for p in resueltas:
            if re.search(re.escape(p) + r'(?!\d)', l) and re.search(r'\ba consulta\b|provisional', l):
                provis.append('%s:%d %s' % (f.name, n, p))
afirma(not provis, 'ninguna pregunta resuelta se presenta como «provisional» o «a consulta»: %s' % provis[:6])

# 5. Estado de la fase 1
d11 = lee(DOC / '11-ruta-de-trabajo.md'); d01 = lee(DOC / '01-ficha-del-proyecto.md')
h = re.search(r'### Fase 1 · [^\n]*', d11).group(0)
cerrada11 = 'cerrada' in h
cerrada01 = bool(re.search(r'fase 1 cerrada|Etapa 1[^\n]*\(cerrada', d01))
afirma(cerrada11 == cerrada01, 'los documentos 01 y 11 dicen lo mismo de la fase 1 (11: %s; 01: %s)' % (h[-40:], 'cerrada' if cerrada01 else 'no cerrada'))
pendientes = []
if '[Art. __' in proto and 'plasticos' in proto: pendientes.append('criterio 1: fundamento de plásticos')
if clase(reg.get('P-02', '')) != 'resuelta': pendientes.append('criterio 6: P-02')
if 'Para discusión' in lee(TSV): pendientes.append('criterio 7: observación para discusión')
afirma(not cerrada11 or not pendientes, 'la fase 1 sólo se dice cerrada con sus criterios cumplidos: %s' % pendientes)
afirma(cerrada11 or '«en cierre»' in h or 'en cierre' in h, 'la fase 1 está «cerrada» o «en cierre», nunca sin estado')

print('\n'.join(notas)); print()
if fallos:
    print('\n'.join(fallos)); sys.exit(1)
print('TODAS LAS PRUEBAS PASAN (%d)' % len(notas))
