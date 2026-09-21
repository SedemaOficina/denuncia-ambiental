# -*- coding: utf-8 -*-
"""Genera la versión de artefacto a partir del archivo local.
   El artefacto no admite recursos externos, de modo que se retira Leaflet
   y se sustituye el mapa por una implementación en SVG."""
import re, sys

ORIGEN  = '/mnt/user-data/outputs/prototipo-denuncia-ambiental-sedema.html'
DESTINO = '/home/claude/build/artefacto.html'
MAPA    = '/home/claude/build/mapa_svg.js'

s = open(ORIGEN, encoding='utf-8').read()

# 1. Quitar el esqueleto: el artefacto lo añade al publicar
s = re.sub(r'^.*?<title>', '<title>', s, flags=re.S)
s = s.replace('</head>\n<body>\n', '')
s = re.sub(r'\n</body>\s*</html>\s*$', '\n', s)

# 2. Quitar Leaflet (script y hoja de estilos) — bloqueados o innecesarios
s = re.sub(r'<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet[^>]*>\n?', '', s)
s = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/leaflet[^>]*></script>\n?', '', s)
# La configuracion local no existe en el artefacto: el mapa vectorial no usa mosaicos.
s = re.sub(r'<!-- Configuraci\u00f3n local.*?-->\n?', '', s, flags=re.S)
s = re.sub(r'<script src="configuracion-local\.js"></script>\n?', '', s)

# 3. Título propio del artefacto
s = s.replace('<title>Denuncia Ambiental en línea — Prototipo SEDEMA</title>',
              '<title>Denuncia Ambiental CDMX</title>')

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
s = s.replace('.mapa-sin{display:none;', estilos + '.mapa-sin{display:none;')

# 4 bis. El logotipo va incrustado como data URI, así que funciona también
#        en el artefacto; no hay nada que sustituir.
s = s.replace(
 """    <img src="https://raw.githubusercontent.com/SedemaOficina/activos-sedema/main/Logotipo_SEDEMA_rgb%20(1).png"
         alt="Gobierno de la Ciudad de México · Secretaría del Medio Ambiente"
         onerror="this.style.display='none';document.getElementById('logoAlt').style.display='block'">
    <div class="fallback" id="logoAlt" style="display:none">GOBIERNO DE LA CIUDAD DE MÉXICO<br>SECRETARÍA DEL MEDIO AMBIENTE</div>""",
 """    <div class="fallback" id="logoAlt">GOBIERNO DE LA CIUDAD DE MÉXICO<br>SECRETARÍA DEL MEDIO AMBIENTE</div>""")

# 4 ter. La página compromete una sola apariencia; se declara para que los
#        controles de formulario no se pinten en oscuro.
s = s.replace(':root{\n  --guinda:#9D2148;', ':root{\n  color-scheme: light;\n  --guinda:#9D2148;')

# 5. Nota sobre el alcance de esta versión. El contenedor de resultados se
#    conserva: «Los hechos ocurren donde estoy ahora» sigue escribiendo ahí.
s = s.replace(
 """  '<div id="resBusqueda"></div>'+""",
 """  '<p class="nota-gris" style="margin:0 0 12px"><span class="pendiente">Versión en línea: dibuja la Ciudad con las capas del Sistema de Información Ambiental, sin mapa de calles de fondo y sin el servicio que ubica la dirección a partir del texto</span></p>'+
  '<div id="resBusqueda"></div>'+""")

# 5 bis. En el artefacto no hay servicio de geocodificación: se retira el botón
#        que ubica por dirección. El de «estoy en el lugar» sí funciona —sólo
#        necesita el navegador— y se conserva.
# 5 bis. La via que requiere el servicio de geocodificacion ya no es un boton:
#        la direccion coloca el punto sola al salir del campo (DEC-101). Aqui
#        no hay servicio, de modo que se deja la funcion en su lugar —el
#        sustituto de mapa_svg.js la atiende— y solo se corrige la promesa que
#        el texto hace, porque en esta version no se cumple.
_antes = s
s = s.replace(
 '<strong>Al terminar de escribir la dirección, el punto se coloca solo.</strong> Si quedó fuera de lugar, arrástralo o da un clic donde corresponda. También puedes:',
 'Esta versión en línea no ubica la dirección por ti. Marca el punto directamente:')
if s == _antes:
    sys.exit('ERROR: no se corrigió la promesa de que la dirección coloca el punto; revisa el texto.')

# 5 ter. El estado vacío no puede nombrar un botón que aquí no existe.
_antes = s
s = s.replace(
 'Captura la dirección y pulsa <strong>Ubicar en el mapa</strong>, o coloca el punto directamente sobre el mapa.',
 'Pega las coordenadas o da un clic directamente sobre el mapa.')
if s == _antes:
    sys.exit('ERROR: el estado vacío sigue nombrando una vía que aquí no existe; revisa el texto.')

# 6. Sustituir la implementación del mapa
mapa = open(MAPA, encoding='utf-8').read()
s = s.replace('\nrender();\n</script>', '\n' + mapa + '\nrender();\n</script>')

open(DESTINO, 'w', encoding='utf-8').write(s)
print('artefacto:', round(len(s)/1024,1), 'KB')
