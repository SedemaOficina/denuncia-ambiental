# -*- coding: utf-8 -*-
"""Arma, para las pruebas, una copia de la version publicada que no sale a
internet (bloque 7 de la auditoria, A1-01; DEC-240).

docs/index.html es lo que la DGIVA ve en GitHub Pages: usa Leaflet para el
mapa y Nominatim para ubicar la direccion, donde el artefacto usa el mapa
vectorial de mapa_svg.js. Las baterias corrian solo sobre el artefacto, y las
funciones que mapa_svg.js sustituye ya se habian desfasado una vez. Esta copia
deja correr las del paso 2 tambien sobre la publicada, sin depender de la red:

1. Leaflet sale de construccion/terceros/leaflet-1.9.4/, la misma version que
   pide la pagina; se comprueba su huella antes de usarlo. Si la pagina pide
   otra version, se detiene: la copia fijada ya no seria la que se publica.
2. Los mosaicos del mapa base se sustituyen por una imagen vacia, y la busqueda
   de direcciones devuelve lo que la prueba ponga en RESPUESTA_DIRECCIONES
   (vacio si no pone nada).
3. Las tipografias de Google no se piden.

No toca docs/index.html: la copia vive en construccion/publicada-pruebas.html
y git la ignora, como al artefacto. pruebas.py la arma antes de correr.
"""
import hashlib, os, pathlib, sys

RAIZ    = pathlib.Path(os.path.abspath(__file__)).parent.parent
ORIGEN  = RAIZ / 'docs' / 'index.html'
DESTINO = RAIZ / 'construccion' / 'publicada-pruebas.html'
LEAFLET = RAIZ / 'construccion' / 'terceros' / 'leaflet-1.9.4'
CDN     = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/'
# Huellas SHA-256 de la copia fijada. Al descargarla se comprobó que su SHA-512
# es el que cdnjs publica para la 1.9.4 (terceros/leaflet-1.9.4/LEEME.md).
HUELLAS = {'leaflet.min.js':  '5c9aecfc30e4564519dbdcddcc53a418227dcc7568e619e9762ddcec7609ed47',
           'leaflet.min.css': 'b570abbda963c60b4de4b4ff4b26f9326f53fb2ccf1461fdf0955ca094fb2539'}

s = ORIGEN.read_text(encoding='utf-8')
copia = {}
for nombre, huella in HUELLAS.items():
    datos = (LEAFLET / nombre).read_bytes()
    if hashlib.sha256(datos).hexdigest() != huella:
        sys.exit('ERROR: %s no es la copia fijada de Leaflet 1.9.4 (la huella no coincide).' % nombre)
    copia[nombre] = datos.decode('utf-8')

def cambia(antes, despues, que):
    global s
    if s.count(antes) != 1:
        sys.exit('ERROR: la regla «%s» no encontró su texto en docs/index.html.' % que)
    s = s.replace(antes, despues)

# 1. Leaflet de la copia fijada, en linea
cambia('<link rel="stylesheet" href="%sleaflet.min.css">' % CDN,
       '<style>\n%s\n</style>' % copia['leaflet.min.css'], 'hoja de estilos de Leaflet')
SIN_RED = """<script>
/* Solo en la copia de pruebas (publicada_de_prueba.py): sin red. Los mosaicos
   son una imagen vacia y la busqueda de direcciones contesta lo que ponga la
   prueba. */
L.TileLayer.prototype.getTileUrl = function(){ return 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'; };
window.RESPUESTA_DIRECCIONES = [];
(function(fetchOriginal){
  window.fetch = function(url){
    if(String(url).indexOf('https://nominatim.openstreetmap.org/') === 0){
      return Promise.resolve(new Response(JSON.stringify(window.RESPUESTA_DIRECCIONES), {headers: {'Content-Type': 'application/json'}}));
    }
    return fetchOriginal.apply(this, arguments);
  };
})(window.fetch);
</script>"""
# Marcado como ajeno: las baterias que revisan el codigo del formulario lo
# dejan fuera (Leaflet trae, por ejemplo, su propia funcion de ubicacion).
cambia('<script src="%sleaflet.min.js"></script>' % CDN,
       '<script data-tercero="leaflet-1.9.4">\n%s\n</script>\n%s' % (copia['leaflet.min.js'], SIN_RED), 'código de Leaflet')
# 2. Sin tipografias de Google
inicio = s.find('<link href="https://fonts.googleapis.com/')
if inicio < 0 or s.count('<link href="https://fonts.googleapis.com/') != 1:
    sys.exit('ERROR: no se encontró, una sola vez, la carga de las tipografías.')
s = s[:inicio] + s[s.index('>', inicio) + 1:]
if 'cdnjs.cloudflare.com' in s:
    sys.exit('ERROR: la copia de pruebas todavía pide algo a cdnjs.')

DESTINO.write_text(s, encoding='utf-8', newline='\n')
print('publicada-pruebas.html: %.1f KB, con Leaflet 1.9.4 local y sin red' % (len(s.encode('utf-8')) / 1024))
