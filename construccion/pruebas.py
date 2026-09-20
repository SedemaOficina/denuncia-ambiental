# -*- coding: utf-8 -*-
"""Corre todas las pruebas del formulario sobre el artefacto ya construido.

    python3 construccion/construir.py
    python3 construccion/pruebas.py

Cada archivo de construccion/pruebas/ corresponde a un cierre de trabajo y se
conserva aunque su asunto ya este cerrado: una prueba vieja que sigue en verde
es lo que avisa cuando un cambio nuevo rompe algo viejo. Si una falla porque
el formulario cambio a proposito, se actualiza la prueba y se anota por que;
nunca se borra para que deje de molestar.

Variables de entorno: ARTEFACTO (ruta del archivo a probar) y CHROMIUM.
"""
import os, sys, glob, subprocess, pathlib

AQUI = pathlib.Path(os.path.abspath(__file__)).parent
ARTE = pathlib.Path(os.environ.get('ARTEFACTO', AQUI / 'artefacto.html'))
if not ARTE.exists():
    sys.exit('No existe %s. Corre antes construccion/construir.py' % ARTE)

archivos = sorted(glob.glob(str(AQUI / 'pruebas' / '[0-9]*.py')))
if not archivos:
    sys.exit('No se encontró ninguna prueba en construccion/pruebas/')

total, fallidos = 0, []
for f in archivos:
    nombre = os.path.basename(f)
    r = subprocess.run([sys.executable, f], capture_output=True, text=True,
                       env=dict(os.environ, ARTEFACTO=str(ARTE)))
    salida = (r.stdout or '') + (r.stderr or '')
    verdes = salida.count('\nOK ') + (1 if salida.startswith('OK ') else 0)
    total += verdes
    print('%-34s %3d comprobaciones  %s' % (nombre, verdes, 'en verde' if r.returncode == 0 else 'CON FALLOS'))
    if r.returncode != 0:
        fallidos.append(nombre)
        for linea in salida.splitlines():
            if linea.startswith('FALLA'):
                print('      ' + linea)

print()
if fallidos:
    print('FALLARON: %s' % ', '.join(fallidos))
    sys.exit(1)
print('TODO EN VERDE · %d comprobaciones en %d archivos' % (total, len(archivos)))
