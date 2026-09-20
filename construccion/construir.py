# -*- coding: utf-8 -*-
"""Genera la versión de artefacto a partir del archivo local.
   El artefacto no admite recursos externos, de modo que se retira Leaflet
   y se sustituye el mapa por una implementación en SVG."""
import re, sys, os

AQUI    = os.path.dirname(os.path.abspath(__file__))
RAIZ    = os.path.dirname(AQUI)
ORIGEN  = os.environ.get('ORIGEN',  os.path.join(RAIZ, 'prototipo', 'prototipo-denuncia-ambiental-sedema.html'))
DESTINO = os.environ.get('DESTINO', os.path.join(AQUI, 'artefacto.html'))
MAPA    = os.path.join(AQUI, 'mapa_svg.js')

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
#mapa{position:relative;background:#EDEFF1;overflow:hidden;touch-action:none;height:440px}
#svgmapa{width:100%;height:100%;display:block;cursor:crosshair}
#contorno{fill:#FFFFFF;stroke:#9D2148}
#alcaldias .alc{fill:transparent;stroke:#B9BDC0}
#etiquetas text{fill:#9AA0A4;font-family:'Roboto',Arial,sans-serif;pointer-events:none;letter-spacing:.0002px}
#zona path{pointer-events:none}
#punto .pin{cursor:grab}
.traza{stroke-linejoin:round}
.mapa-ctrl{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px}
.mapa-ctrl button{background:#fff;border:1px solid var(--linea);border-radius:6px;padding:5px 9px;font-size:14px;font-family:'Cabin',sans-serif;font-weight:600;color:var(--guinda);cursor:pointer;line-height:1.2}
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
 """  '<div class="aviso" style="margin-bottom:14px">Esta versión en línea dibuja la Ciudad con las capas del Sistema de Información Ambiental, sin mapa de calles de fondo y sin el servicio que ubica la dirección a partir del texto. Da un clic para colocar el punto, arrástralo para ajustarlo y usa los controles del mapa para acercar. La versión completa está en el archivo del proyecto.</div>'+
  '<div id="resBusqueda"></div>'+""")

# 5 bis. En el artefacto no hay servicio de geocodificación: se retira el botón
#        que ubica por dirección. El de «estoy en el lugar» sí funciona —sólo
#        necesita el navegador— y se conserva.
_antes = s
s = re.sub(
    r"\s*'<button type=\"button\" class=\"btn btn-primario\" style=\"padding:11px 20px;font-size:14px\" onclick=\"ubicaPorDireccion\(\)\">'\+"
    r"\s*svgIcono\('pin',16\)\+' Ubicar en el mapa</button>'\+",
    '', s, count=1)
if s == _antes:
    sys.exit('ERROR: no se retiró el botón «Ubicar en el mapa»; revisa el marcado.')

# 5 ter. El estado vacío no puede nombrar un botón que aquí no existe.
_antes = s
s = s.replace(
 'Captura la dirección y pulsa <strong>Ubicar en el mapa</strong>, o coloca el punto directamente sobre el mapa.',
 'Coloca el punto directamente sobre el mapa.')
if s == _antes:
    sys.exit('ERROR: el estado vacío sigue nombrando un botón inexistente; revisa el texto.')

# 6. Sustituir la implementación del mapa
mapa = open(MAPA, encoding='utf-8').read()
s = s.replace('\nrender();\n</script>', '\n' + mapa + '\nrender();\n</script>')

open(DESTINO, 'w', encoding='utf-8').write(s)
print('artefacto:', round(len(s)/1024,1), 'KB')
