# -*- coding: utf-8 -*-
"""Genera los dos catalogos que el prototipo lleva incrustados y que la
persona no dibuja en el mapa: el de colonias y el de celdas UGA (DEC-117).

Origenes, sin tocar, en capas/originales/:
  · colonias_iecm2022.geojson  IECM 2022, unidades territoriales (1 837):
                               colonias, pueblos, barrios y unidades
                               habitacionales, cada una con su demarcacion.
  · UGA_CDMX.geojson           Malla hexagonal del SIA (1 624 celdas de
                               ~1 km2), entregada el 22-09-2026.
  · alcaldias_cdmx.json        Marco geoestadistico, 16 alcaldias; es el
                               origen de capas/alcaldias.geojson.

Tres reglas, las mismas que en normalizar_capas.py:
1. El valor de origen no se toca. Cada colonia conserva su clave CVEUT y su
   nombre IECM tal como llegaron; el nombre legible se anade.
2. Nada pasa en silencio. Una demarcacion que no case con las 16 alcaldias
   del prototipo detiene el guion con su nombre a la vista.
3. Es idempotente: correrlo dos veces deja el mismo archivo.

Que se incrusta:
  · CATALOGO_COLONIAS  [nombre legible, indice de alcaldia, CVEUT, nombre IECM]
                       Sin geometria: la colonia la escribe la persona y el
                       catalogo solo sugiere. 1 837 poligonos pesarian 4 MB.
  · CATALOGO_UGA       [clave, longitud del centro, latitud del centro]
                       La malla es regular: todas las celdas son hexagonos
                       completos del mismo tamano, de modo que la celda que
                       contiene un punto es la de centro mas cercano, medida
                       con la longitud corregida por la escala de la malla.
                       validar_catalogos.py lo comprueba contra los poligonos.

Uso:  python construccion/generar_catalogos.py
"""
import json, os, re, sys, unicodedata

AQUI  = os.path.dirname(os.path.abspath(__file__))
RAIZ  = os.path.dirname(AQUI)
ORIG  = os.path.join(RAIZ, 'capas', 'originales')
PROTO = os.environ.get('ORIGEN', os.path.join(RAIZ, 'prototipo', 'prototipo-denuncia-ambiental-sedema.html'))

def norm(s):
    s = unicodedata.normalize('NFD', str(s or '').lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

# ------------------------------------------------------------ nombre legible
# El IECM escribe en mayusculas y sin acentos. Se restituyen solo acentos de
# palabras inequivocas; una palabra que no este aqui queda sin acento, que es
# un defecto menor que un acento inventado. La busqueda ignora acentos, asi
# que esto no afecta lo que se encuentra, solo como se lee.
ACENTOS = {
 'seccion':'Sección','ampliacion':'Ampliación','maria':'María','aragon':'Aragón',
 'culhuacan':'Culhuacán','jose':'José','juarez':'Juárez','nicolas':'Nicolás',
 'agricola':'Agrícola','ursula':'Úrsula','andres':'Andrés','anahuac':'Anáhuac',
 'lopez':'López','angel':'Ángel','heroes':'Héroes','jesus':'Jesús','millan':'Millán',
 'jardin':'Jardín','gomez':'Gómez','ticoman':'Ticomán','pantitlan':'Pantitlán',
 'paraiso':'Paraíso','angeles':'Ángeles','aleman':'Alemán','sanchez':'Sánchez',
 'tomatlan':'Tomatlán','belen':'Belén','batan':'Batán','rincon':'Rincón',
 'cuitlahuac':'Cuitláhuac','alvaro':'Álvaro','bernabe':'Bernabé',
 'dominguez':'Domínguez','simon':'Simón','hipodromo':'Hipódromo',
 'triangulo':'Triángulo','martir':'Mártir','martires':'Mártires',
 'gonzalez':'González','capulin':'Capulín','tizapan':'Tizapán','martin':'Martín',
 'barbara':'Bárbara','tomas':'Tomás','republica':'República','rio':'Río',
 'hernandez':'Hernández','pavon':'Pavón','purisima':'Purísima','obregon':'Obregón',
 'gavilan':'Gavilán','escandon':'Escandón','serdan':'Serdán','coyoacan':'Coyoacán',
 'iztaccihuatl':'Iztaccíhuatl','cuauhtemoc':'Cuauhtémoc','ejercito':'Ejército',
 'mexico':'México','aguilas':'Águilas','ramirez':'Ramírez','martinez':'Martínez',
 'rodriguez':'Rodríguez','perez':'Pérez','diaz':'Díaz','garcia':'García',
 'fernandez':'Fernández','ramon':'Ramón','joaquin':'Joaquín','agustin':'Agustín',
 'sebastian':'Sebastián','fabian':'Fabián','julian':'Julián','lazaro':'Lázaro',
 'cardenas':'Cárdenas','ines':'Inés','lucia':'Lucía','panteon':'Panteón',
 'leon':'León','alamos':'Álamos','arbol':'Árbol','union':'Unión','tlahuac':'Tláhuac',
 'jimenez':'Jiménez','gutierrez':'Gutiérrez','alvarez':'Álvarez','vazquez':'Vázquez',
 'nuñez':'Núñez','benitez':'Benítez','marquez':'Márquez','ortiz':'Ortiz',
 'ecologica':'Ecológica','ecologico':'Ecológico','politecnico':'Politécnico',
 'aeropuerto':'Aeropuerto','ferreria':'Ferrería','azcapotzalco':'Azcapotzalco',
 'hidalgo':'Hidalgo','zocalo':'Zócalo','tepeyac':'Tepeyac','olimpica':'Olímpica',
 'petrolera':'Petrolera','acatlan':'Acatlán','aztecas':'Aztecas','sotelo':'Sotelo',
 'tlatilco':'Tlatilco','cristobal':'Cristóbal','trabajadores':'Trabajadores',
 'bolivar':'Bolívar','america':'América','americas':'Américas','peñon':'Peñón',
 'huipulco':'Huipulco','ixtlahuacan':'Ixtlahuacán','xochimilco':'Xochimilco',
 'mixquic':'Mixquic','tecomitl':'Tecómitl','atlazolpa':'Atlazolpa',
 'tlaltenco':'Tlaltenco','zapotitlan':'Zapotitlán','ixtapalapa':'Ixtapalapa',
 'tepalcates':'Tepalcates','periodista':'Periodista','educacion':'Educación',
 'caracol':'Caracol','ermita':'Ermita','cantera':'Cantera','lomas':'Lomas',
 'valentin':'Valentín','ruben':'Rubén','german':'Germán','adrian':'Adrián',
 'efrain':'Efraín','raul':'Raúl','hector':'Héctor','oscar':'Óscar','ruiz':'Ruiz',
 'avila':'Ávila','camacho':'Camacho','teotihuacan':'Teotihuacán','matias':'Matías',
 'ejidos':'Ejidos','zacatenco':'Zacatenco','tequesquinahuac':'Tequesquináhuac',
 'papalotla':'Papalotla','huitzilihuitl':'Huitzilíhuitl','moctezuma':'Moctezuma',
 'axotla':'Axotla','tacuba':'Tacuba','tacubaya':'Tacubaya','mixcoac':'Mixcoac',
 'echeverria':'Echeverría','quetzalcoatl':'Quetzalcóatl','gamiz':'Gámiz',
 'abdias':'Abdías','alban':'Albán','guzman':'Guzmán','roman':'Román','albarran':'Albarrán','galvez':'Gálvez',
}
# Abreviaturas del IECM, entre parentesis o sueltas
ABREV = {
 'u hab':'Unidad Habitacional','u habs':'Unidades Habitacionales','pblo':'Pueblo',
 'barr':'Barrio','ampl':'Ampliación','fracc':'Fraccionamiento','rdcial':'Residencial',
 'conj hab':'Conjunto Habitacional','rcnda':'Rinconada','rncda':'Rinconada',
 'pje':'Paraje','ej':'Ejido','cond':'Condominio','secc':'Sección','sta':'Santa',
 'sto':'Santo','ma':'María','nte':'Norte','ejto':'Ejército','sn':'San',
}
SIGLAS = {'ctm','infonavit','fovissste','pemex','issste','imss','gdf','uam','ipn',
          'unam','issfam','croc','fstse','stunam','sct','sedena','stc','ddf','fonhapo',
          'fividesu','invi','isstecali','sahop','cfe','ferronales','sutgdf','sme','ctc','cnc'}
ROMANOS = re.compile(r'^(i{1,3}|iv|v|vi{1,3}|ix|x{1,3}i{0,3}|xiv|xv|xvi{1,3})$')
MENORES = {'de','del','la','las','los','el','y','en'}

def palabra(t, primera):
    n = norm(t)
    if not n:
        return t
    if ROMANOS.match(n):
        return n.upper()
    if n in SIGLAS:
        return n.upper()
    m = re.match(r'^(\d+)(a|er|ra|da|o|ro|do|ta|va)$', n)
    if m:
        return m.group(1) + m.group(2)
    if n in MENORES and not primera:
        return n
    if len(n) == 1 or re.search(r'\d', n):
        return t.upper()
    if n in ACENTOS:
        return ACENTOS[n]
    if n.endswith('cion') and len(n) > 5:
        return n[:-4].capitalize() + 'ción'
    if '-' in t:
        return '-'.join(palabra(x, True) for x in t.split('-'))
    low = t.lower()
    return low[:1].upper() + low[1:]

def legible(ut):
    s = re.sub(r'\s+', ' ', ut).strip()
    # abreviaturas entre parentesis, p. ej. «ALPES (AMPL)» -> «Alpes (Ampliación)»
    def par(m):
        dentro = norm(m.group(1))
        if dentro in ABREV:
            return '(' + ABREV[dentro] + ')'
        return '(' + ' '.join(palabra(w, i == 0) for i, w in enumerate(m.group(1).split())) + ')'
    partes = re.split(r'(\([^)]*\))', s)
    out = []
    primera = True
    for p in partes:
        if p.startswith('('):
            out.append(par(re.match(r'\(([^)]*)\)', p)))
            continue
        toks = p.split(' ')
        res = []
        i = 0
        while i < len(toks):
            t = toks[i]
            if not t:
                res.append(t); i += 1; continue
            dos = norm(' '.join(toks[i:i+2]))
            if dos in ('u hab', 'conj hab', 'u habs'):
                res.append(ABREV[dos]); i += 2; primera = False; continue
            n = norm(t)
            if n in ABREV and n not in ('ej', 'cond'):
                res.append(ABREV[n]); i += 1; primera = False; continue
            res.append(palabra(t, primera)); primera = False; i += 1
        out.append(' '.join(res))
    s = ''.join(out)
    s = re.sub(r'\s+', ' ', s).replace('( ', '(').replace(' )', ')').strip()
    s = re.sub(r'(\S)\(', r'\1 (', s)
    return s

# ------------------------------------------------------------------ alcaldias
alc_prot = json.load(open(os.path.join(RAIZ, 'capas', 'alcaldias.geojson'), encoding='utf-8'))
ALCALDIAS = sorted(f['properties']['nombre'] for f in alc_prot['features'])
POR_NORMA = {norm(a): a for a in ALCALDIAS}
if len(ALCALDIAS) != 16:
    sys.exit('capas/alcaldias.geojson no trae 16 alcaldias')

# ------------------------------------------------------------------ colonias
col = json.load(open(os.path.join(ORIG, 'colonias_iecm2022.geojson'), encoding='utf-8'))
filas, sin_alc = [], set()
for f in col['features']:
    p = f['properties']
    dem = POR_NORMA.get(norm(p['DEMARCACIO']))
    if not dem:
        sin_alc.add(p['DEMARCACIO']); continue
    ut = re.sub(r'\s+', ' ', p['UT']).strip()
    filas.append([legible(ut), ALCALDIAS.index(dem), p['CVEUT'], ut])
if sin_alc:
    sys.exit('Demarcaciones sin alcaldia en el prototipo: %s' % sorted(sin_alc))
filas.sort(key=lambda r: (norm(r[0]), r[1]))
claves = [r[2] for r in filas]
if len(set(claves)) != len(claves):
    sys.exit('CVEUT repetida en el origen')

# ------------------------------------------------------------------ UGA
uga = json.load(open(os.path.join(ORIG, 'UGA_CDMX.geojson'), encoding='utf-8'))
celdas, anchos, altos = [], [], []
for f in uga['features']:
    g = f['geometry']
    anillo = g['coordinates'][0] if g['type'] == 'Polygon' else g['coordinates'][0][0]
    pts = anillo[:-1] if anillo[0] == anillo[-1] else anillo
    if len(pts) != 6:
        sys.exit('La celda %s no es un hexagono completo: el metodo del centro mas cercano no aplica' % f['properties']['clave'])
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    anchos.append(max(xs) - min(xs)); altos.append(max(ys) - min(ys))
    celdas.append([f['properties']['clave'], round(sum(xs) / 6, 6), round(sum(ys) / 6, 6)])
celdas.sort(key=lambda c: c[0])
ancho = sum(anchos) / len(anchos); alto = sum(altos) / len(altos)
# En un hexagono regular de lados planos arriba y abajo, alto = ancho * raiz(3)/2.
# La malla se trazo en metros; en grados el hexagono llega achatado. KX es el
# factor que devuelve la longitud a la escala de la latitud.
KX = round(alto / (ancho * 3 ** 0.5 / 2), 5)
RADIO = round(alto / 2, 6)        # apotema: distancia del centro al lado

meta = {'colonias': {'origen': 'IECM 2022, unidades territoriales', 'n': len(filas)},
        'uga': {'origen': 'SIA, malla hexagonal entregada el 22-09-2026', 'version': 'sia-2026-09-22',
                'n': len(celdas), 'kx': KX, 'apotema': RADIO}}

bloque_col = ('var CATALOGO_COLONIAS = {meta:' + json.dumps(meta['colonias'], ensure_ascii=False) +
              ',\n  alcaldias:' + json.dumps(ALCALDIAS, ensure_ascii=False) +
              ',\n  filas:' + json.dumps(filas, ensure_ascii=False, separators=(',', ':')) + '};')
bloque_uga = ('var CATALOGO_UGA = {meta:' + json.dumps(meta['uga'], ensure_ascii=False) +
              ',\n  celdas:' + json.dumps(celdas, separators=(',', ':')) + '};')

s = open(PROTO, encoding='utf-8').read()
n0 = len(s)
for nombre, bloque in (('CATALOGO_COLONIAS', bloque_col), ('CATALOGO_UGA', bloque_uga)):
    patron = re.compile(r'^var ' + nombre + r' = \{.*?\};$', re.S | re.M)
    if patron.search(s):
        s = patron.sub(lambda m: bloque, s, count=1)
    else:
        marca = '\nvar CAPAS_SUELO='
        i = s.find(marca)
        j = s.find('\n', i + 1)
        if i < 0:
            sys.exit('No se encontro CAPAS_SUELO para insertar ' + nombre)
        s = s[:j + 1] + bloque + '\n' + s[j + 1:]
open(PROTO, 'w', encoding='utf-8', newline='\n').write(s)
print('colonias: %d (%d alcaldias) · UGA: %d celdas · KX=%s apotema=%s · prototipo %+d bytes'
      % (len(filas), len(ALCALDIAS), len(celdas), KX, RADIO, len(s) - n0))
