# -*- coding: utf-8 -*-
"""Genera la versión de artefacto a partir del archivo local.
   El artefacto no admite recursos externos, de modo que se retira Leaflet
   y se sustituye el mapa por una implementación en SVG."""
import re, sys, os, pathlib

# Las rutas se resuelven contra la raiz del repositorio, como en los otros dos
# guiones. Estaban escritas fijas y apuntaban a carpetas de la maquina donde se
# escribio el guion, de modo que el comando que documenta el LEEME no corria
# desde el repositorio (DEC-111). Admiten sustitucion por variable de entorno.
RAIZ    = pathlib.Path(os.path.abspath(__file__)).parent.parent
ORIGEN  = os.environ.get('ORIGEN',  str(RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'))
DESTINO = os.environ.get('DESTINO', str(RAIZ / 'construccion' / 'artefacto.html'))
MAPA    = os.environ.get('MAPA',    str(RAIZ / 'construccion' / 'mapa_svg.js'))

s = open(ORIGEN, encoding='utf-8').read()

def cambia(antes, despues, que):
    """Toda sustitucion se comprueba: una regla que ya no encuentra su texto
    es codigo muerto y detiene la construccion (DEC-146)."""
    global s
    if s.count(antes) != 1:
        sys.exit('ERROR: la regla «%s» no encontró su texto en el prototipo.' % que)
    s = s.replace(antes, despues)

# 1. Quitar el esqueleto: el artefacto lo añade al publicar
s = re.sub(r'^.*?<title>', '<title>', s, flags=re.S)
cambia('</head>\n<body>\n', '', 'esqueleto')
s = re.sub(r'\n</body>\s*</html>\s*$', '\n', s)

# 2. Quitar Leaflet (script y hoja de estilos) — bloqueados o innecesarios
s = re.sub(r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet[^>]*>\n?', '', s)
s = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet[^>]*></script>\n?', '', s)
# La configuracion local no existe en el artefacto: el mapa vectorial no usa mosaicos.
s = re.sub(r'<!-- Configuraci\u00f3n local.*?-->\n?', '', s, flags=re.S)
s = re.sub(r'<script src="configuracion-local\.js"></script>\n?', '', s)

# 3. Título propio del artefacto
cambia('<title>Denuncia Ambiental en línea — Prototipo SEDEMA</title>',
       '<title>Denuncia Ambiental CDMX</title>', 'título')

# 4. Estilos del mapa vectorial
estilos = """
/* ---- Mapa vectorial (artefacto) ---- */
#mapa{position:relative;background:var(--mapa-bg);overflow:hidden;touch-action:none;height:440px}
#svgmapa{width:100%;height:100%;display:block;cursor:crosshair}
#contorno{fill:var(--blanco);stroke:var(--guinda)}
#alcaldias .alc{fill:transparent;stroke:var(--linea)}
#etiquetas text{fill:var(--gris-cl);font-family:'Roboto',Arial,sans-serif;pointer-events:none;letter-spacing:.0002px}
#zona path{pointer-events:none}
#punto .pin{cursor:grab}
.traza{stroke-linejoin:round}
.mapa-ctrl{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px}
.mapa-ctrl button{background:var(--blanco);border:1px solid var(--linea);border-radius:6px;padding:5px 9px;font-size:14px;font-family:'Cabin',sans-serif;font-weight:600;color:var(--guinda);cursor:pointer;line-height:1.2}
.mapa-ctrl button:hover{background:var(--guinda-cl)}
.mapa-ctrl button:last-child{font-size:11px;padding:5px 8px}
"""
cambia('.mapa-sin{display:none;', estilos + '.mapa-sin{display:none;', 'estilos del mapa')

# 4 bis y 4 ter se retiraron en DEC-146: el logotipo ya va incrustado y
#        «color-scheme: light» ya esta en el origen; no sustituian nada.

# 5. Nota sobre el alcance de esta versión. El contenedor de resultados se
#    conserva: «Los hechos ocurren donde estoy ahora» sigue escribiendo ahí.
cambia(
 """  '<div id="resBusqueda"></div>'+""",
 """  '<p class="nota-gris" style="margin:0 0 12px"><span class="pendiente">Versión en línea: dibuja la Ciudad con las capas del Sistema de Información Ambiental, sin mapa de calles de fondo y sin el servicio que ubica la dirección a partir del texto</span></p>'+
  '<div id="resBusqueda"></div>'+""", 'nota de alcance')

# 5 bis. En el artefacto no hay servicio de geocodificación: se retira el botón
#        que ubica por dirección. El de «estoy en el lugar» sí funciona —sólo
#        necesita el navegador— y se conserva.
# 5 bis. La via que requiere el servicio de geocodificacion ya no es un boton:
#        la direccion coloca el punto sola al salir del campo (DEC-101). Aqui
#        no hay servicio, de modo que se deja la funcion en su lugar —el
#        sustituto de mapa_svg.js la atiende— y solo se corrige la promesa que
#        el texto hace, porque en esta version no se cumple.
cambia(
 '<span class="solo-local">Al terminar de escribir la dirección, el punto se coloca solo; si quedó fuera de lugar, arrástralo.</span>',
 '<span class="solo-local">Esta versión de prueba no ubica la dirección sola: márcalo tú o continúa sin punto.</span>',
 'promesa de ubicar la dirección')

# 5 ter. (Retirado en DEC-123: el estado vacío ya no nombra el botón «Ubicar en
#        el mapa» en el origen, que era lo que esta regla corregía aquí.)

# 6. Sustituir la implementación del mapa
mapa = open(MAPA, encoding='utf-8').read()
cambia('\nrender();\niniciaRevision();\n</script>', '\n' + mapa + '\nrender();\niniciaRevision();\n</script>', 'mapa vectorial')

open(DESTINO, 'w', encoding='utf-8').write(s)
print('artefacto:', round(len(s)/1024,1), 'KB')
