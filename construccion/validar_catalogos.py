# -*- coding: utf-8 -*-
"""Comprueba el catalogo de colonias contra las capas completas (DEC-117).
Requiere shapely; no forma parte de la construccion, se corre al cambiar un
origen. El punto interior de cada unidad territorial cae en la alcaldia que
el IECM le asigna, segun la capa de alcaldias del prototipo. El cotejo de las
celdas UGA se retiro con el catalogo (DEC-257).
"""
import json, os, re
from shapely.geometry import shape
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI)
O=os.path.join(RAIZ,'capas','originales')
alc=json.load(open(os.path.join(RAIZ,'capas','alcaldias.geojson'),encoding='utf-8'))
AL=[(f['properties']['nombre'],shape(f['geometry'])) for f in alc['features']]
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
