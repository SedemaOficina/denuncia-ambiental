# Leaflet 1.9.4 · copia fijada para las pruebas

**Qué es.** La misma versión de Leaflet que carga la versión publicada (`docs/index.html`) desde cdnjs. La usa `construccion/publicada_de_prueba.py` para que las baterías corran sobre la versión publicada sin salir a internet (DEC-240). El formulario publicado no la usa: sigue pidiendo Leaflet a cdnjs.

**De dónde salió.** Descargada el 21 de octubre de 2026, con autorización de Liber Saltijeral, de:

- `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js`
- `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css`

**Huellas.** Coinciden con las que publica cdnjs para la versión 1.9.4 (`api.cdnjs.com/libraries/leaflet/1.9.4?fields=sri`):

| Archivo | SHA-512 (cdnjs) | SHA-256 (la que comprueba el armador) |
|---|---|---|
| `leaflet.min.js` | `puJW3E/qXDqYp9IfhAI54BJEaWIfloJ7JWs7OeD5i6ruC9JZL1gERT1wjtwXFlh7CjE7ZJ+/vcRZRkIYIb6p4g==` | `5c9aecfc30e4564519dbdcddcc53a418227dcc7568e619e9762ddcec7609ed47` |
| `leaflet.min.css` | `h9FcoyWjHcOcmEVkxOfTLnmZFWIH0iZhZT1H2TbOq55xssQGEJHEaIm+PgoUaZbRvQTNTluNOEfb1ZRy6D3BOw==` | `b570abbda963c60b4de4b4ff4b26f9326f53fb2ccf1461fdf0955ca094fb2539` |

**No se edita.** Si la versión publicada cambia de versión de Leaflet, el armador se detiene: hay que fijar la nueva versión en una carpeta propia, con sus huellas.

## Licencia

Leaflet se distribuye con la licencia BSD de dos cláusulas. El archivo minificado de cdnjs no trae el aviso; se reproduce aquí, como pide la licencia:

```
BSD 2-Clause License

Copyright (c) 2010-2023, Volodymyr Agafonkin
Copyright (c) 2010-2011, CloudMade
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
