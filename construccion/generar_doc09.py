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
            'vigente': val('vigente') == 'true',
            'dp': val('dp') == 'true',
            'etq': txt('etq'),
            'fin': txt('fin'),
            'uso': ' '.join(txt('uso').split()),
            'cond_txt': ' '.join(txt('cond_txt').split()),
        })
    if not campos:
        sys.exit('ERROR: no se leyó ningún campo de OBLIG; revisa el formato del catálogo.')
    if len(campos) != declaradas:
        sys.exit('ERROR: el catálogo declara %d campos y el lector reconoció %d. '
                 'Alguna entrada no coincide con el patrón y el documento saldría incompleto.'
                 % (declaradas, len(campos)))
    return campos

def marca(obligatorio, cond):
    if not obligatorio:
        return 'Opcional'
    return 'Obligatorio' if not cond else 'Obligatorio *(condicionado)*'

html = io.open(ORIGEN, encoding='utf-8').read()
campos = lee_oblig(html)

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
nvig   = sum(1 for c in campos if c['vigente'])
ncond  = sum(1 for c in campos if c['cond_txt'])
sin_uso= [c['clave'] for c in campos if not c['uso']]
hoy    = datetime.date.today()
MESES  = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
          'septiembre','octubre','noviembre','diciembre']

o = []
o.append('# Formulario web de Denuncia Ambiental · Mapeo de campos, obligatoriedad y uso declarado\n')
o.append('**Versión:** 3.0 · %d de %s de %d' % (hoy.day, MESES[hoy.month-1], hoy.year))
o.append('**Generado automáticamente** del catálogo `OBLIG` del prototipo, que es la única fuente de verdad: '
         'gobierna la marca de opcionalidad en pantalla, la validación y este documento. '
         'Si algo aquí no coincide con el formulario, el error está en el generador, no en los datos.\n')
o.append('**Para qué sirve.** Declara, campo por campo, **quién usa el dato y para qué**. Responde a la '
         'exigencia de minimización —no se recaba un dato para el que no exista un uso declarado— y es el '
         'insumo con el que la Unidad de Transparencia redacta el aviso de privacidad.\n')
o.append('| | |\n|---|---|')
o.append('| Campos del formulario | **%d** |' % n)
o.append('| Datos personales | **%d** (%d %%) |' % (ndp, round(100.0*ndp/n)))
o.append('| Obligatorios en este formulario | %d de %d |' % (ndg, n))
o.append('| Obligatorios en el formato de 2016 | %d de %d · referencia documental |' % (nvig, n))
o.append('| Campos con obligatoriedad condicionada | %d |' % ncond)
o.append('| Campos sin uso declarado | **%d** |' % len(sin_uso))
o.append('\n---\n')
o.append('## 1. Finalidades\n')
o.append('Todo dato recabado sirve a una de estas finalidades. Ninguna otra.\n')
o.append('| Finalidad | Para qué | Campos |\n|---|---|---|')
for nom, para in FINALIDADES:
    k = sum(1 for c in campos if c['fin'] == nom)
    if k:
        o.append('| **%s** | %s | %d |' % (nom, para, k))
huerfanas = sorted({c['fin'] for c in campos} - {f[0] for f in FINALIDADES})
if huerfanas:
    sys.exit('ERROR: finalidades no declaradas en el generador: %s' % huerfanas)
o.append('\n---\n')
o.append('## 2. Campos, por paso\n')
o.append('**Dato personal** marca los datos de una persona física identificada o identificable, '
         'sea la persona denunciante o un tercero señalado. '
         '**Obligatorio *(condicionado)*** significa que el campo sólo se exige en la situación '
         'que indica la última columna; fuera de ella no se pide ni se marca.\n')
for p in sorted(PASOS):
    delPaso = [c for c in campos if c['p'] == p]
    if not delPaso:
        continue
    o.append('### Paso %d · %s\n' % (p, PASOS[p]))
    o.append('| Campo | Obligatorio | Formato 2016 | Dato personal | Se pide | Uso declarado |\n|---|---|---|---|---|---|')
    for c in delPaso:
        o.append('| %s | %s | %s | %s | %s | %s |' % (
            c['etq'], marca(c['oblig'], c['cond_txt']), marca(c['vigente'], c['cond_txt']),
            '**Sí**' if c['dp'] else 'No',
            c['cond_txt'] or 'Siempre', c['uso']))
    o.append('')
o.append('---\n')

io.open(DESTINO, 'w', encoding='utf-8').write('\n'.join(o) + cola)
print('documento 09: %d campos, %d datos personales, %d condicionados, %d sin uso declarado'
      % (n, ndp, ncond, len(sin_uso)))
if sin_uso:
    print('AVISO: campos sin uso declarado:', sin_uso)
