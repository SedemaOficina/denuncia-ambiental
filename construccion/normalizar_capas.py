# -*- coding: utf-8 -*-
"""Normaliza los atributos de las capas y los deja listos para agrupar.

Las capas institucionales llegan con la misma categoria escrita de dos formas
—«Zona Ecologica y Cultural» y «Zona Ecológica y Cultural»—, con alcaldias sin
acentos, con una errata («Cujimalpa») y con listas en distinto orden. Agrupar
por esos textos produce categorias fantasma: una misma categoria contada dos
veces, y ninguna suma correcta.

Tres reglas gobiernan este guion:

1. **El valor de origen no se toca.** `categoria_origen` y `alcaldia_origen`
   quedan como llegaron: son el rastro de auditoria frente al decreto.
2. **Lo normalizado se anade, no sustituye.** `categoria` es el nombre correcto
   y `categoria_clave` la clave estable con la que se agrupa. El nombre cambia
   de acentuacion entre versiones; la clave no.
3. **Nada pasa en silencio.** Un valor que no este en el catalogo detiene el
   guion con su nombre a la vista. Una errata nueva tiene que verse, no
   colarse como categoria propia.

Es idempotente: correrlo dos veces da el mismo resultado.
"""
import json, os, sys, unicodedata, collections

AQUI  = os.path.dirname(os.path.abspath(__file__))
RAIZ  = os.path.dirname(AQUI)
CAPAS = os.path.join(RAIZ, 'capas')
PROTO = os.path.join(RAIZ, 'prototipo', 'prototipo-denuncia-ambiental-sedema.html')

# ---------------------------------------------------------------- catalogos
# nombre de origen -> (nombre correcto, clave estable)
CATEGORIAS = {
 'Bosque urbano'                              : ('Bosque urbano', 'bosque_urbano'),
 'Barranca'                                   : ('Barranca', 'barranca'),
 'Zona Sujeta a Conservacion Ecologica'       : ('Zona Sujeta a Conservación Ecológica', 'zona_sujeta_conservacion_ecologica'),
 'Zona Sujeta a Conservación Ecológica'       : ('Zona Sujeta a Conservación Ecológica', 'zona_sujeta_conservacion_ecologica'),
 'Zona Ecologica y Cultural'                  : ('Zona Ecológica y Cultural', 'zona_ecologica_cultural'),
 'Zona Ecológica y Cultural'                  : ('Zona Ecológica y Cultural', 'zona_ecologica_cultural'),
 'Zona de Conservacion Ecologica'             : ('Zona de Conservación Ecológica', 'zona_conservacion_ecologica'),
 'Zona de Conservación Ecológica'             : ('Zona de Conservación Ecológica', 'zona_conservacion_ecologica'),
 'Zona de Proteccion Hidrologica y Ecologica' : ('Zona de Protección Hidrológica y Ecológica', 'zona_proteccion_hidrologica_ecologica'),
 'Zona de Protección Hidrológica y Ecológica' : ('Zona de Protección Hidrológica y Ecológica', 'zona_proteccion_hidrologica_ecologica'),
 'Reserva Ecologica Comunitaria'              : ('Reserva Ecológica Comunitaria', 'reserva_ecologica_comunitaria'),
 'Reserva Ecológica Comunitaria'              : ('Reserva Ecológica Comunitaria', 'reserva_ecologica_comunitaria'),
 'Zona de Proteccion Especial'                : ('Zona de Protección Especial', 'zona_proteccion_especial'),
 'Zona de Protección Especial'                : ('Zona de Protección Especial', 'zona_proteccion_especial'),
 'Parque Nacional'                            : ('Parque Nacional', 'parque_nacional'),
 # No es un acento: es una sigla donde el resto va desarrollado. Se desarrolla
 # conforme a la categoria federal, y queda advertido en el informe.
 'APRN'                                       : ('Área de Protección de Recursos Naturales', 'area_proteccion_recursos_naturales'),
}
DESARROLLADAS = {'APRN'}

# Erratas y formas cortas de alcaldia que no se resuelven quitando acentos.
ALIAS_ALCALDIA = {
 'cujimalpa'           : 'Cuajimalpa de Morelos',   # errata en el origen
 'cuajimalpa'          : 'Cuajimalpa de Morelos',
 'magdalena contreras' : 'La Magdalena Contreras',
}

def plano(s):
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode()
    return ' '.join(s.lower().split())

def carga(nombre):
    with open(os.path.join(CAPAS, nombre), encoding='utf-8') as f:
        return json.load(f)

def guarda(nombre, datos):
    with open(os.path.join(CAPAS, nombre), 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, separators=(',', ':'))

# ---------------------------------------------------------------- alcaldias
alc = carga('alcaldias.geojson')
CANON, CVE = {}, {}
for ft in alc['features']:
    n, c = ft['properties']['nombre'], ft['properties']['cvegeo']
    CANON[plano(n)] = n
    CVE[n] = c
for k, v in ALIAS_ALCALDIA.items():
    CANON[k] = v

def normaliza_alcaldias(texto):
    """Devuelve (nombres correctos ordenados, claves ordenadas). El orden
       alfabetico importa: «Tláhuac, Iztapalapa» y «Iztapalapa, Tláhuac» son
       el mismo conjunto y tienen que poder compararse."""
    if not str(texto or '').strip():
        return [], []
    nombres = []
    for parte in str(texto).split(','):
        p = plano(parte)
        if not p:
            continue
        if p not in CANON:
            sys.exit('ERROR: alcaldía no reconocida en el origen: %r' % parte.strip())
        nombres.append(CANON[p])
    nombres = sorted(set(nombres))
    return nombres, [CVE[n] for n in nombres]

# ---------------------------------------------------------------- geometrias
geo = carga('geometrias.geojson')
informe_cat = collections.Counter()
acentuadas, desarrolladas = set(), set()
for ft in geo['features']:
    p = ft['properties']
    origen = p.get('categoria_origen', '')
    if origen not in CATEGORIAS:
        sys.exit('ERROR: categoría no catalogada: %r' % origen)
    nombre, clave = CATEGORIAS[origen]
    if origen != nombre:
        (desarrolladas if origen in DESARROLLADAS else acentuadas).add((origen, nombre))
    p['categoria'], p['categoria_clave'] = nombre, clave
    informe_cat[clave] += 1
    p['alcaldias'], p['alcaldias_cve'] = normaliza_alcaldias(p.get('alcaldia_origen', ''))
guarda('geometrias.geojson', geo)

# ---------------------------------------------------------------- suelo
suelo = carga('suelo_conservacion.geojson')
vacias = 0
for ft in suelo['features']:
    p = ft['properties']
    d = p.get('DESCRIP')
    # El origen trae la cadena «None», que no es un valor: es un vacío escrito.
    d = '' if d in (None, 'None', '') else str(d).strip()
    if not d:
        vacias += 1
    p['descripcion'] = d
guarda('suelo_conservacion.geojson', suelo)

# ---------------------------------------------------------------- prototipo
# La capa va incrustada en el prototipo en forma compacta. Se le añaden las
# dos claves normalizadas para que la pantalla lea el dato ya normalizado y no
# lo normalice al vuelo, que es lo que obliga a mantener dos catálogos.
with open(PROTO, encoding='utf-8') as f:
    html = f.read()
i = html.index('var CAPAS_GEOM=')
j = html.index('];', i) + 1
rasgos = json.loads(html[i + len('var CAPAS_GEOM='):j])
if len(rasgos) != len(geo['features']):
    sys.exit('ERROR: el prototipo trae %d rasgos y la capa %d' % (len(rasgos), len(geo['features'])))
porNombre = {ft['properties']['nombre']: ft['properties'] for ft in geo['features']}
for r in rasgos:
    fuente = porNombre.get(r['p'].get('nombre'))
    if not fuente:
        sys.exit('ERROR: el rasgo %r del prototipo no está en la capa' % r['p'].get('nombre'))
    r['p']['categoria'] = fuente['categoria']
    r['p']['categoria_clave'] = fuente['categoria_clave']
html = html[:i] + 'var CAPAS_GEOM=' + json.dumps(rasgos, ensure_ascii=False, separators=(',', ':')) + html[j:]
with open(PROTO, 'w', encoding='utf-8') as f:
    f.write(html)

# ---------------------------------------------------------------- informe
print('capas normalizadas')
print('  categorías distintas en el origen : %d' % len({ft['properties']['categoria_origen'] for ft in geo['features']}))
print('  categorías reales tras normalizar : %d' % len(informe_cat))
print('  variantes de acentuación unidas   : %d' % len(acentuadas))
for a, b in sorted(acentuadas):
    print('      %-45s -> %s' % (a, b))
for a, b in sorted(desarrolladas):
    print('      %-45s -> %s   [sigla desarrollada, no es acento]' % (a, b))
print('  alcaldías normalizadas en %d rasgos (incluye la errata «Cujimalpa»)' % len(geo['features']))
print('  suelo de conservación: %d descripciones vacías declaradas como vacías' % vacias)
