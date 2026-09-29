# -*- coding: utf-8 -*-
"""Comprueba los catalogos incrustados contra las capas completas (DEC-117).
Requiere shapely; no forma parte de la construccion, se corre al cambiar un
origen. Dos comprobaciones:
 1. UGA. Para 20 000 puntos al azar dentro de la Ciudad, la celda que da el
    metodo del centro mas cercano (el que usa el prototipo) es la misma que la
    del poligono que lo contiene.
 2. Colonias. El punto interior de cada unidad territorial cae en la alcaldia
    que el IECM le asigna, segun la capa de alcaldias del prototipo.
"""
import json, os, re, random, math, sys
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI)
O=os.path.join(RAIZ,'capas','originales')
s=open(os.path.join(RAIZ,'prototipo','prototipo-denuncia-ambiental-sedema.html'),encoding='utf-8').read()
kx=float(re.search(r'"kx": ?([\d.]+)',s).group(1)); ap=float(re.search(r'"apotema": ?([\d.]+)',s).group(1))
celdas=json.loads(re.search(r'var CATALOGO_UGA = \{.*?celdas:(\[.*?\])\};',s,re.S).group(1))
uga=json.load(open(os.path.join(O,'UGA_CDMX.geojson'),encoding='utf-8'))
polys=[shape(f['geometry']) for f in uga['features']]; claves=[f['properties']['clave'] for f in uga['features']]
arbol=STRtree(polys)
alc=json.load(open(os.path.join(RAIZ,'capas','alcaldias.geojson'),encoding='utf-8'))
AL=[(f['properties']['nombre'],shape(f['geometry'])) for f in alc['features']]
from shapely.ops import unary_union
cdmx=unary_union([g for _,g in AL])
def cercana(lo,la):
    best=None;dm=1e9
    for c,x,y in celdas:
        d=((lo-x)*kx)**2+(la-y)**2
        if d<dm: dm=d;best=c
    return best, math.sqrt(dm)
random.seed(1); minx,miny,maxx,maxy=cdmx.bounds
n=ok=fuera=0; malos=[]; sincelda=0
while n<20000:
    lo=random.uniform(minx,maxx); la=random.uniform(miny,maxy); pt=Point(lo,la)
    if not cdmx.contains(pt): continue
    n+=1
    idx=[i for i in arbol.query(pt) if polys[i].contains(pt)]
    real=claves[idx[0]] if idx else None
    if real is None: sincelda+=1
    c,d=cercana(lo,la)
    if d>ap*1.2: c=None
    if c==real: ok+=1
    else: malos.append((lo,la,real,c,polys[idx[0]].exterior.distance(pt)*111000 if idx else None))
print('UGA: %d/%d coinciden; puntos de la Ciudad sin celda: %d'%(ok,n,sincelda))
for m in malos[:10]: print('  discrepa',m)
if malos: print('  distancia maxima al borde de la celda en los que discrepan: %.1f m'%max((m[4] or 0) for m in malos))
col=json.load(open(os.path.join(O,'colonias_iecm2022.geojson'),encoding='utf-8'))
import unicodedata
def norm(x): x=unicodedata.normalize('NFD',x.lower()); return re.sub(r'[^a-z]+',' ',''.join(ch for ch in x if unicodedata.category(ch)!='Mn')).strip()
mal=0
for f in col['features']:
    g=shape(f['geometry']).buffer(0); p=g.representative_point()
    dentro=[a for a,ga in AL if ga.contains(p)]
    if not dentro or norm(dentro[0])!=norm(f['properties']['DEMARCACIO']):
        mal+=1
        if mal<=10: print('  colonia fuera de su alcaldia:',f['properties']['UT'],f['properties']['DEMARCACIO'],dentro)
print('Colonias: %d de %d con su punto interior fuera de la alcaldia que les asigna el IECM'%(mal,len(col['features'])))
