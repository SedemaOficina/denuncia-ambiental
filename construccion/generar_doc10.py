# -*- coding: utf-8 -*-
"""Genera el documento 10 a partir del prototipo.

El documento decia «Generado desde el prototipo» y no lo estaba: sus tablas
se mantenian a mano y se separaron del formulario en cuanto este cambio —la
variante C de identificacion y el conmutador de esquemas siguieron
documentados meses despues de retirarse. Es el mismo defecto que ya habia
mordido al documento 09, y se cierra igual: generandolo.

Los apartados 1 y 2 salen de BIFURCACIONES y ESCENARIOS, que son las mismas
estructuras que gobiernan el panel de validacion. Del apartado 3 en adelante
el texto es redactado a mano y este guion lo CONSERVA: lo busca por su
encabezado y lo vuelve a pegar. Si no lo encuentra, se detiene en vez de
publicar un documento mutilado.
"""
import io, re, os, sys, datetime

AQUI    = os.path.dirname(os.path.abspath(__file__))
RAIZ    = os.path.dirname(AQUI)
ORIGEN  = os.environ.get('ORIGEN',  os.path.join(RAIZ, 'prototipo', 'prototipo-denuncia-ambiental-sedema.html'))
DESTINO = os.environ.get('DESTINO', os.path.join(RAIZ, 'documentacion', '10-variantes-del-formulario.md'))
CORTE   = '## 3. Las rutas de competencia'

NUM = {1:'una',2:'dos',3:'tres',4:'cuatro',5:'cinco',6:'seis',7:'siete',8:'ocho',
       9:'nueve',10:'diez',11:'once',12:'doce',13:'trece',14:'catorce',15:'quince',
       16:'dieciséis',17:'diecisiete',18:'dieciocho',19:'diecinueve',20:'veinte'}

def bloque(texto, arranque):
    """Devuelve el literal del arreglo que empieza en `arranque`, contando
       corchetes. Se detiene si no encuentra el cierre: un arreglo truncado
       produciria un documento incompleto sin avisar."""
    i = texto.find(arranque)
    if i < 0:
        sys.exit('ERROR: no se encontró %r en el prototipo.' % arranque)
    j = texto.index('[', i)
    prof, k, en_cadena, escapa = 0, j, None, False
    while k < len(texto):
        c = texto[k]
        if en_cadena:
            if escapa:            escapa = False
            elif c == '\\':       escapa = True
            elif c == en_cadena:  en_cadena = None
        elif c in '\'"':          en_cadena = c
        elif c == '[':            prof += 1
        elif c == ']':
            prof -= 1
            if prof == 0:         return texto[j:k+1]
        k += 1
    sys.exit('ERROR: el arreglo de %r no cierra.' % arranque)

def campos(entrada):
    """Lee los pares clave:'valor' de una entrada, sin evaluar codigo."""
    d = {}
    for m in re.finditer(r"(\w+)\s*:\s*'((?:[^'\\]|\\.)*)'", entrada):
        d[m.group(1)] = m.group(2).replace("\\'", "'").replace('\\"', '"')
    for m in re.finditer(r'(\w+)\s*:\s*(\d+)\s*[,}]', entrada):
        d.setdefault(m.group(1), m.group(2))
    return d

def entradas(lit):
    """Parte el literal del arreglo en sus objetos de primer nivel."""
    out, prof, ini, en_cadena, escapa = [], 0, None, None, False
    for k, c in enumerate(lit):
        if en_cadena:
            if escapa:            escapa = False
            elif c == '\\':       escapa = True
            elif c == en_cadena:  en_cadena = None
            continue
        if c in '\'"':            en_cadena = c
        elif c == '{':
            if prof == 0:         ini = k
            prof += 1
        elif c == '}':
            prof -= 1
            if prof == 0:         out.append(lit[ini:k+1])
    return out

html = io.open(ORIGEN, encoding='utf-8').read()
BIF = [campos(e) for e in entradas(bloque(html, 'var BIFURCACIONES'))]
ESC = [campos(e) for e in entradas(bloque(html, 'var ESCENARIOS'))]
if not BIF or not ESC:
    sys.exit('ERROR: el lector no reconoció ninguna rama o ningún escenario.')
for b in BIF:
    if not all(x in b for x in ('paso','pregunta','opciones','efecto')):
        sys.exit('ERROR: rama incompleta: %s' % b)
for e in ESC:
    if not all(x in e for x in ('id','nom','d','paso')):
        sys.exit('ERROR: escenario incompleto: %s' % e)

previo = io.open(DESTINO, encoding='utf-8').read() if os.path.exists(DESTINO) else ''
if previo and CORTE not in previo:
    sys.exit('ERROR: no se encontró %r en el documento. Se aborta para no '
             'perder la parte redactada a mano.' % CORTE)
cola = previo[previo.index(CORTE):] if previo else ''
if previo and not cola.strip():
    sys.exit('ERROR: la cola redactada a mano quedó vacía; se aborta.')

hoy   = datetime.date.today()
MESES = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto',
         'septiembre','octubre','noviembre','diciembre']

o = []
o.append('# Formulario web de Denuncia Ambiental · Variantes del formulario\n')
o.append('**Versión:** 2.0 · %d de %s de %d' % (hoy.day, MESES[hoy.month-1], hoy.year))
o.append('**Generado automáticamente** de las estructuras `BIFURCACIONES` y `ESCENARIOS` del '
         'prototipo, que son las mismas que gobiernan el panel de validación. Documento y '
         'comportamiento no pueden discrepar.\n')
o.append('El formulario no es un camino único: hay **%s puntos donde cambia de forma** según lo '
         'que se responde. Este documento los enumera y describe los %s escenarios que el panel '
         'de validación carga con un toque, para recorrer cada rama sin capturar todo a mano.\n'
         % (NUM.get(len(BIF), str(len(BIF))), NUM.get(len(ESC), str(len(ESC)))))
o.append('---\n')
o.append('## 1. Puntos de bifurcación\n')
o.append('| Paso | Qué se responde | Opciones | Cómo cambia el formulario |\n|---|---|---|---|')
for b in BIF:
    o.append('| %s | **%s** | %s | %s |' % (b['paso'], b['pregunta'], b['opciones'], b['efecto']))
o.append('\n### Cuántas combinaciones son\n')
o.append('Multiplicadas, las ramas dan varios miles de recorridos distintos. No tiene sentido '
         'probarlos todos: los que importan son aquellos en los que **cambia el área que atiende, '
         'cambia el conjunto de campos, o cambia lo que el acuse promete**. Ésos son los %s del '
         'apartado siguiente.\n' % NUM.get(len(ESC), str(len(ESC))))
o.append('---\n')
o.append('## 2. Escenarios cargables desde el panel\n')
o.append('Cada botón limpia el formulario, carga un caso completo —incluida la coordenada, que '
         'dispara el cruce espacial— y abre el paso donde se aprecia el cambio.\n')
o.append('| Escenario | Qué muestra | Abre en |\n|---|---|---|')
for e in ESC:
    o.append('| **%s** | %s | Paso %s |' % (e['nom'], e['d'], e['paso']))
o.append('')
o.append('> El área que atiende cada caso no se documenta aquí: la resuelve el cruce espacial '
         'al cargar el escenario, y repetirla a mano es exactamente la forma en que este '
         'documento se separó del formulario. El apartado 3 explica la regla; el prototipo '
         'muestra el resultado.\n')
o.append('---\n')

io.open(DESTINO, 'w', encoding='utf-8').write('\n'.join(o) + cola)
print('documento 10: %d ramas, %d escenarios' % (len(BIF), len(ESC)))
