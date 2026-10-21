# -*- coding: utf-8 -*-
"""Prepara la version de prueba que se publica en GitHub Pages (DEC-127).

GitHub Pages sirve la carpeta docs/ de la rama main. Este guion copia ahi el
prototipo con tres cambios, y se detiene si algo no cuadra:

1. Quita la carga de configuracion-local.js. Ese archivo no viaja al
   repositorio (lleva la clave del mapa base); en Pages daria un error en
   consola, y sin el el mapa usa el proveedor abierto, que es lo correcto
   para una pagina publica.
2. Pide a los buscadores que no la indexen: una version de prueba de un
   formulario de denuncia no debe aparecer en Google como si fuera el canal
   oficial.
3. Anuncia arriba de todo que es una version de prueba y que no envia
   denuncias: quien llegue por el enlace no puede confundirla con el tramite.

Ademas publica la maqueta del modulo de administracion en docs/administracion/
(DEC-250), con su liga al modo captura apuntando al formulario publicado.

Uso:  python construccion/publicar_pages.py
Despues: commit de docs/ y push. Las paginas quedan en
https://sedemaoficina.github.io/denuncia-ambiental/ y
https://sedemaoficina.github.io/denuncia-ambiental/administracion/
"""
import os, re, sys, pathlib

RAIZ   = pathlib.Path(os.path.abspath(__file__)).parent.parent
ORIGEN = RAIZ / 'prototipo' / 'prototipo-denuncia-ambiental-sedema.html'
DOCS   = RAIZ / 'docs'

s = ORIGEN.read_text(encoding='utf-8')
n0 = len(s)

# 1. Sin configuracion local
s, n = re.subn(r'<!-- Configuración local.*?-->\s*<script src="configuracion-local\.js"></script>\n?', '', s, flags=re.S)
if n != 1:
    sys.exit('ERROR: no se encontro la carga de configuracion-local.js; revisa el prototipo.')

# 2. Que no se indexe
s = s.replace('<meta charset="UTF-8">',
              '<meta charset="UTF-8">\n<meta name="robots" content="noindex, nofollow">', 1)

# 3. Aviso de version de prueba
# Franja gris con rayas diagonales, texto blanco y una sola linea: se lee
# como marca de entorno de prueba, no como un aviso mas del formulario
# (DEC-137). Sus colores viven aqui y no en la paleta del prototipo, porque
# solo existe en la version publicada.
AVISO = ('<style>.franja-prueba{background:repeating-linear-gradient(135deg,#4A4F55 0 14px,#565B61 14px 28px);'
         'color:#FFFFFF;font-size:15px;line-height:1.4;padding:11px 20px}'
         '.franja-prueba p{max-width:980px;margin:0 auto}</style>'
         '<div class="franja-prueba" role="note"><p>Versión de prueba con datos ficticios. '
         'No envía denuncias ni guarda datos en la Secretaría.</p></div>\n')
if s.count('<body>\n') != 1:
    sys.exit('ERROR: no se encontro <body> para poner el aviso de version de prueba.')
s = s.replace('<body>\n', '<body>\n' + AVISO, 1)
s = s.replace('<title>Denuncia Ambiental en línea — Prototipo SEDEMA</title>',
              '<title>Denuncia Ambiental · versión de prueba — SEDEMA</title>', 1)

# Ninguna clave puede salir publicada
for prohibido in ('api_key', 'apikey', 'CFG_LOCAL = {', 'configuracion-local.js"'):
    if prohibido in s:
        sys.exit('ERROR: la version publica contiene «%s»; no se escribe nada.' % prohibido)

DOCS.mkdir(exist_ok=True)
(DOCS / 'index.html').write_text(s, encoding='utf-8', newline='\n')
(DOCS / '.nojekyll').write_text('', encoding='utf-8')
print('docs/index.html: %.1f KB (prototipo %+d bytes)' % (len(s.encode('utf-8'))/1024, len(s) - n0))

# 4. La maqueta del modulo de administracion, en /administracion/ (DEC-250).
# Ya trae su franja de maqueta con datos ficticios y pide no indexarse; lo
# unico que cambia es su liga al modo captura, que en Pages lleva al
# formulario publicado y no al prototipo, que no se publica.
MAQUETA = RAIZ / 'prototipo' / 'administracion' / 'maqueta-administracion.html'
m = MAQUETA.read_text(encoding='utf-8')
LIGA = "var FORMULARIO_CAPTURA = '../prototipo-denuncia-ambiental-sedema.html?modo=captura';"
if m.count(LIGA) != 1 or 'name="robots" content="noindex, nofollow"' not in m or 'franja-maqueta' not in m:
    sys.exit('ERROR: la maqueta no trae su liga al modo captura, su franja o su «noindex»; no se publica.')
m = m.replace(LIGA, "var FORMULARIO_CAPTURA = '../index.html?modo=captura';")
for prohibido in ('api_key', 'apikey', 'CFG_LOCAL = {', 'configuracion-local.js'):
    if prohibido in m:
        sys.exit('ERROR: la maqueta publicada contiene «%s»; no se escribe nada.' % prohibido)
(DOCS / 'administracion').mkdir(exist_ok=True)
(DOCS / 'administracion' / 'index.html').write_text(m, encoding='utf-8', newline='\n')
print('docs/administracion/index.html: %.1f KB' % (len(m.encode('utf-8'))/1024))
