# -*- coding: utf-8 -*-
"""Corre todas las pruebas del formulario sobre el artefacto ya construido.

    python3 construccion/construir.py
    python3 construccion/pruebas.py

Cada archivo de construccion/pruebas/ corresponde a un cierre de trabajo y se
conserva aunque su asunto ya este cerrado: una prueba vieja que sigue en verde
es lo que avisa cuando un cambio nuevo rompe algo viejo. Si una falla porque
el formulario cambio a proposito, se actualiza la prueba y se anota por que;
nunca se borra para que deje de molestar.

Variables de entorno: ARTEFACTO (ruta del archivo a probar) y CHROMIUM (sin
ella se usa el Chromium que instala Playwright).
"""
import os, sys, glob, subprocess, pathlib

AQUI = pathlib.Path(os.path.abspath(__file__)).parent
ARTE = pathlib.Path(os.environ.get('ARTEFACTO', AQUI / 'artefacto.html'))
if not ARTE.exists():
    sys.exit('No existe %s. Corre antes construccion/construir.py' % ARTE)

archivos = sorted(glob.glob(str(AQUI / 'pruebas' / '[0-9]*.py')))
if not archivos:
    sys.exit('No se encontró ninguna prueba en construccion/pruebas/')

# La copia de la version publicada que no sale a internet (DEC-240): la usan
# la bateria 42 y la segunda vuelta de abajo.
PUBLICADA = AQUI / 'publicada-pruebas.html'
r = subprocess.run([sys.executable, str(AQUI / 'publicada_de_prueba.py')], capture_output=True, text=True, encoding='utf-8')
print((r.stdout or '').strip() or (r.stderr or '').strip())
if r.returncode != 0:
    sys.exit('No se pudo armar la copia de pruebas de la versión publicada.')

total, fallidos = 0, []
def corre(f, destino, extra, etiqueta=''):
    global total
    nombre = os.path.basename(f)
    # En Windows Python lee y escribe por omision en cp1252; las baterias y lo
    # que leen de pdftotext van en UTF-8, y sin esto se pierden acentos.
    r = subprocess.run([sys.executable, f], capture_output=True, text=True, encoding='utf-8',
                       env=dict(os.environ, ARTEFACTO=str(destino), PYTHONUTF8='1', **extra))
    salida = (r.stdout or '') + (r.stderr or '')
    verdes = salida.count('\nOK ') + (1 if salida.startswith('OK ') else 0)
    total += verdes
    print('%-34s %3d comprobaciones  %s' % (nombre, verdes, 'en verde' if r.returncode == 0 else 'CON FALLOS'))
    if r.returncode != 0:
        fallidos.append(etiqueta + nombre)
        for linea in salida.splitlines():
            if linea.startswith('FALLA'):
                print('      ' + linea)
    return verdes

for f in archivos:
    corre(f, ARTE, {})

# Segunda vuelta: las baterias del paso 2 sobre la version publicada, que usa
# Leaflet y busca la direccion donde el artefacto usa el mapa vectorial
# (auditoria del 20 de octubre, A1-01).
PASO2 = ['01-datos-del-lugar-y-ubicacion.py', '02-lugar-sin-calle.py', '07-codigo-plus.py', '18-colonia-cp-y-uga.py',
         '21-como-pegar-la-ubicacion.py', '22-punto-opcional-con-direccion.py', '31-manzana-y-lote-obligatoria.py',
         '32-campos-anidados-y-cp.py']
print('\nVersión publicada (docs/index.html, con Leaflet local):')
publicada = sum(corre(str(AQUI / 'pruebas' / n), PUBLICADA, {'PUBLICADA': '1'}, 'publicada: ') for n in PASO2)

print()
if fallidos:
    print('FALLARON: %s' % ', '.join(fallidos))
    sys.exit(1)
print('TODO EN VERDE · %d comprobaciones en %d archivos; de ellas, %d sobre la versión publicada (%d baterías)'
      % (total, len(archivos), publicada, len(PASO2)))
