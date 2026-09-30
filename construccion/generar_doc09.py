# -*- coding: utf-8 -*-
"""Genera el documento 09 a partir del catalogo OBLIG del prototipo.

OBLIG es la unica fuente de verdad: gobierna la marca de opcionalidad en
pantalla, la validacion y este documento. Generarlo evita que las tres cosas
se separen, que es lo que pasa en cuanto se mantienen a mano.

El documento tiene una cabecera y dos apartados generados, y una cola
redactada a mano (apartados 3 en adelante) que este guion CONSERVA: la busca
por su encabezado y la vuelve a pegar. Si no la encuentra, se detiene en vez
de publicar un documento mutilado.
"""
import io, re, os, sys, datetime

AQUI    = os.path.dirname(os.path.abspath(__file__))
RAIZ    = os.path.dirname(AQUI)
ORIGEN  = os.environ.get('ORIGEN',  os.path.join(RAIZ, 'prototipo', 'prototipo-denuncia-ambiental-sedema.html'))
DESTINO = os.environ.get('DESTINO', os.path.join(RAIZ, 'documentacion', '09-mapeo-campos-obligatorios.md'))
CORTE   = '## 3. Hallazgos de la revisión de minimización'
DEC05   = os.environ.get('DEC05', os.path.join(RAIZ, 'documentacion', '05-decisiones-y-pendientes.md'))

PASOS = {1:'Qué denuncias', 2:'Dónde ocurre', 3:'Qué ocurre',
         4:'Pruebas', 5:'Tus datos', 6:'Revisión'}
FINALIDADES = [
 ('Competencia', 'Determinar la competencia y turnar al área que atiende'),
 ('Localización','Localizar y caracterizar el sitio para la visita de inspección'),
 ('Expediente',  'Integrar el expediente y motivar el acto de inspección'),
 ('Responsable', 'Identificar y emplazar al probable infractor'),
 ('Identificación','Determinar cómo se identifica quien denuncia y qué seguimiento admite'),
 ('Contacto',    'Identificar, notificar y dar seguimiento con la persona denunciante'),
 ('Cumplimiento','Dejar constancia del consentimiento y de la vía elegida'),
 ('Estadística','Conocer quién denuncia, sin formar parte del expediente'),
]

def lee_oblig(html):
    """Lee el literal OBLIG sin ejecutar JavaScript: cada entrada por separado.

       La coma final es opcional en la expresion: la ultima entrada del catalogo
       no la lleva, y exigirla hacia que el documento perdiera justo ese campo
       —el de la protesta de decir verdad y el aviso de privacidad— sin avisar,
       y que todas las cifras salieran una unidad cortas. Por eso el guion
       compara ahora cuantas entradas leyo contra cuantas hay."""
    i = html.index('var OBLIG = {')
    j = html.index('\n};', i)
    frag = html[i:j]
    campos = []
    declaradas = len(re.findall(r'\n  [a-z_0-9]+:\s*\{', frag))
    for m in re.finditer(r"\n  ([a-z_0-9]+):\s*\{(.*?)\},?(?=\n|$)", frag, re.S):
        clave, cuerpo = m.group(1), m.group(2)
        def val(k, patron=r"([^,}]*)"):
            mm = re.search(k + r":\s*" + patron, cuerpo)
            return mm.group(1).strip() if mm else None
        def txt(k):
            mm = re.search(k + r":'((?:[^'\\]|\\.)*)'", cuerpo, re.S)
            return mm.group(1).replace("\\'", "'") if mm else ''
        campos.append({
            'clave': clave,
            'p': int(val('p')),
            'oblig': val('oblig') == 'true',
            'dp': val('dp') == 'true',
            'etq': txt('etq'),
            'fin': txt('fin'),
            'uso': ' '.join(txt('uso').split()),
            'cond_txt': ' '.join(txt('cond_txt').split()),
            'oculto': val('oculto') == 'true',
        })
    if not campos:
        sys.exit('ERROR: no se leyó ningún campo de OBLIG; revisa el formato del catálogo.')
    if len(campos) != declaradas:
        sys.exit('ERROR: el catálogo declara %d campos y el lector reconoció %d. '
                 'Alguna entrada no coincide con el patrón y el documento saldría incompleto.'
                 % (declaradas, len(campos)))
    return campos

def lee_derivados(html):
    """Lee DERIVADOS (DEC-128): lo que el formulario calcula y viaja a la base."""
    i = html.index('var DERIVADOS = {')
    j = html.index('\n};', i)
    frag = html[i:j]
    out = []
    for m in re.finditer(r"\n  ([a-z_0-9]+):\s*\{(.*?)\}(?=,?\n|$)", frag, re.S):
        cuerpo = m.group(2)
        def txt(k):
            mm = re.search(k + r":'((?:[^'\\]|\\.)*)'", cuerpo, re.S)
            return ' '.join(mm.group(1).replace("\\'", "'").split()) if mm else ''
        def b(k):
            mm = re.search(k + r":\s*(true|false)", cuerpo)
            return bool(mm and mm.group(1) == 'true')
        out.append({'clave': m.group(1), 'etq': txt('etq'), 'origen': txt('origen'), 'fin': txt('fin'),
                    'dp': b('dp'), 'se_ve': b('se_ve'), 'por': txt('por'), 'uso': txt('uso')})
    declaradas = len(re.findall(r'\n  [a-z_0-9]+:\s*\{', frag))
    if len(out) != declaradas:
        sys.exit('ERROR: DERIVADOS declara %d datos y el lector reconoció %d.' % (declaradas, len(out)))
    return out

def ultima_decision(ruta):
    """La última decisión del documento 05: su número y su fecha."""
    t = io.open(ruta, encoding='utf-8').read()
    filas = re.findall(r'^\| DEC-(\d+) \|.*?\| (\d{1,2} \w{3,10} \d{4}) \|', t, re.M)
    if not filas:
        sys.exit('ERROR: no se encontró ninguna decisión en el documento 05.')
    n, f = max(filas, key=lambda x: int(x[0]))
    MES = {'ene':'enero','feb':'febrero','mar':'marzo','abr':'abril','may':'mayo','jun':'junio','jul':'julio',
           'ago':'agosto','sep':'septiembre','oct':'octubre','nov':'noviembre','dic':'diciembre'}
    d, m, a = f.split()
    return 'DEC-%s' % n, '%s de %s de %s' % (d, MES.get(m[:3].lower(), m), a)

def marca(obligatorio, cond):
    if not obligatorio:
        return 'Opcional'
    return 'Obligatorio' if not cond else 'Obligatorio *(condicionado)*'

html = io.open(ORIGEN, encoding='utf-8').read()

# La version que muestra el mapeo del prototipo se toma de la ultima
# decision registrada: asi no depende de acordarse de cambiarla (DEC-128).
DEC, FECHA = ultima_decision(DEC05)
nuevo = re.sub(r"var VERSION_FORMULARIO = \{dec:'[^']*', fecha:'[^']*'\};",
               "var VERSION_FORMULARIO = {dec:'%s', fecha:'%s'};" % (DEC, FECHA), html, count=1)
if nuevo == html and ("dec:'%s'" % DEC) not in html:
    sys.exit('ERROR: no se encontró VERSION_FORMULARIO en el prototipo.')
if nuevo != html:
    io.open(ORIGEN, 'w', encoding='utf-8', newline='\n').write(nuevo)
    html = nuevo

campos_todos = lee_oblig(html)
derivados = lee_derivados(html)
def calculado(c): return c['cond_txt'].startswith('No se pregunta')
campos = [c for c in campos_todos if not calculado(c)]
def mayus(t): return t[:1].upper() + t[1:]
calc = [{'clave': c['clave'], 'etq': c['etq'], 'origen': mayus(re.sub(r'^No se pregunta( ni se muestra)?:\s*', '', c['cond_txt'])),
         'fin': c['fin'], 'dp': c['dp'], 'se_ve': not c['oculto'], 'por': 'denuncia', 'uso': c['uso']}
        for c in campos_todos if calculado(c)] + derivados

previo = io.open(DESTINO, encoding='utf-8').read() if os.path.exists(DESTINO) else ''
if previo and CORTE not in previo:
    sys.exit('ERROR: no se encontró «%s» en el documento anterior. Se aborta para no '
             'perder la parte redactada a mano.' % CORTE)
cola = previo[previo.index(CORTE):] if previo else ''
if previo and not cola.strip():
    sys.exit('ERROR: la cola redactada a mano quedó vacía; se aborta.')

n      = len(campos)
ndp    = sum(1 for c in campos if c['dp'])
ndg    = sum(1 for c in campos if c['oblig'])
ncond  = sum(1 for c in campos if c['cond_txt'])
sin_uso= [c['clave'] for c in campos + calc if not c['uso']]
ocultos = [x for x in calc if not x['se_ve']]
visibles= [x for x in calc if x['se_ve']]
hoy    = datetime.date.today()
MESES  = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
          'septiembre','octubre','noviembre','diciembre']

o = []
o.append('# Formulario web de Denuncia Ambiental · Mapeo de campos, obligatoriedad y uso declarado\n')
o.append('**Versión:** %s · %s' % (DEC, FECHA))
o.append('**Generado automáticamente** del catálogo `OBLIG` del prototipo, que es la única fuente de verdad: '
         'gobierna la marca de opcionalidad en pantalla, la validación y este documento. '
         'Si algo aquí no coincide con el formulario, el error está en el generador, no en los datos.\n')
o.append('**Para qué sirve.** Declara, campo por campo, **quién usa el dato y para qué**. Responde a la '
         'exigencia de minimización —no se recaba un dato para el que no exista un uso declarado— y es el '
         'insumo con el que la Unidad de Transparencia redacta el aviso de privacidad.\n')
o.append('| | |\n|---|---|')
o.append('| Campos que llena la persona | **%d** |' % n)
o.append('| Datos que viajan a la base sin verse en pantalla | **%d** |' % len(ocultos))
o.append('| Datos que calcula el formulario y se muestran | %d |' % len(visibles))
o.append('| Datos personales | **%d** (%d %%) |' % (ndp, round(100.0*ndp/n)))
o.append('| Obligatorios en este formulario | %d de %d |' % (ndg, n))
o.append('| Campos con obligatoriedad condicionada | %d |' % ncond)
o.append('| Datos sin uso declarado | **%d** |' % len(sin_uso))
o.append('\n---\n')
o.append('## 1. Finalidades\n')
o.append('Todo dato recabado o calculado sirve a una de estas finalidades. Ninguna otra.\n')
o.append('| Finalidad | Para qué | Datos |\n|---|---|---|')
for nom, para in FINALIDADES:
    k = sum(1 for c in campos + calc if c['fin'] == nom)
    if k:
        o.append('| **%s** | %s | %d |' % (nom, para, k))
huerfanas = sorted({c['fin'] for c in campos + calc} - {f[0] for f in FINALIDADES})
if huerfanas:
    sys.exit('ERROR: finalidades no declaradas en el generador: %s' % huerfanas)
o.append('\n---\n')
o.append('## 2. Campos que llena la persona, por paso\n')
o.append('**Dato personal** marca los datos de una persona física identificada o identificable, '
         'sea la persona denunciante o un tercero señalado. '
         '**Obligatorio *(condicionado)*** significa que el campo sólo se exige en la situación '
         'que indica la última columna; fuera de ella no se pide ni se marca.\n')
for p in sorted(PASOS):
    delPaso = [c for c in campos if c['p'] == p]
    if not delPaso:
        continue
    o.append('### Paso %d · %s\n' % (p, PASOS[p]))
    o.append('| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |\n|---|---|---|---|---|')
    for c in delPaso:
        o.append('| %s | %s | %s | %s | %s |' % (
            c['etq'], marca(c['oblig'], c['cond_txt']),
            '**Sí**' if c['dp'] else 'No',
            c['cond_txt'] or 'Siempre', c['uso']))
    o.append('')
o.append('---\n')

def tabla_calc(lista):
    for por, rot in (('denuncia', 'Por denuncia'), ('foto', 'Por cada foto adjunta')):
        xs = [x for x in lista if x['por'] == por]
        if not xs:
            continue
        o.append('**%s**\n' % rot)
        o.append('| Dato | Clave | Quién lo pone | Dato personal | Para qué sirve |\n|---|---|---|---|---|')
        for x in xs:
            o.append('| %s | `%s` | %s | %s | %s |' % (x['etq'], x['clave'], x['origen'],
                     '**Sí**' if x['dp'] else 'No', x['uso']))
        o.append('')

o.append('## 2 bis. Campos que viajan a la base y no se ven en pantalla\n')
o.append('Los calcula el formulario: la persona no los escribe ni los ve, pero llegan al expediente. '
         'Se declaran en `OBLIG` (marcados `oculto`) o en `DERIVADOS`, y una prueba exige que toda clave '
         'que el código guarda esté declarada en alguno de los dos o en `INTERNOS` (DEC-128).\n')
tabla_calc(ocultos)
o.append('### Datos que calcula el formulario y se muestran como información\n')
o.append('Tampoco los escribe la persona: se le enseñan en la ficha del mapa, en la revisión o en el acuse.\n')
tabla_calc(visibles)
o.append('---\n')

io.open(DESTINO, 'w', encoding='utf-8').write('\n'.join(o) + cola)
print('documento 09 (%s): %d campos que llena la persona, %d que viajan sin verse, %d calculados visibles, %d sin uso declarado'
      % (DEC, n, len(ocultos), len(visibles), len(sin_uso)))
if sin_uso:
    print('AVISO: campos sin uso declarado:', sin_uso)
