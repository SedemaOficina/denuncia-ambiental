# Cadena de construcción del artefacto

El archivo del que todo depende es **uno solo**: `prototipo/prototipo-denuncia-ambiental-sedema.html`. Se abre con doble clic, no necesita servidor y es la única versión que se edita.

De ahí sale una **segunda versión, la que se publica en línea** para que la Dirección General pueda abrirla desde un enlace sin instalar nada. Esa versión no se edita a mano nunca: se genera. Lo que hay en esta carpeta es lo que la genera y lo que la comprueba.

## Por qué hacen falta dos versiones

El entorno donde se publica el artefacto **bloquea todo recurso externo**. El prototipo local usa Leaflet para el mapa y un servicio de geocodificación para ubicar la dirección; ninguno de los dos llega ahí. La versión publicada sustituye el mapa por un dibujo vectorial hecho con las capas del propio Sistema de Información Ambiental —contorno de la Ciudad, límites de alcaldía, polígonos de zona— y retira el botón que necesita el servicio de geocodificación.

**Lo que no cambia entre las dos versiones son las preguntas, las reglas ni la validación.** Si cambiaran, el artefacto dejaría de servir para validar el formulario.

## Qué hay aquí

| Archivo | Qué hace |
|---|---|
| `construir.py` | Transforma el archivo local en la versión publicable |
| `mapa_svg.js` | El mapa vectorial que sustituye a Leaflet. Se inyecta al final, de modo que **sus definiciones sobrescriben a las del prototipo** |
| `generar_doc09.py` | Regenera `documentacion/09-mapeo-campos-obligatorios.md` desde el catálogo `OBLIG` |
| `pruebas.py` | Corre todas las pruebas y suma el resultado |
| `pruebas/` | Una batería por cierre de trabajo. **No se borran cuando su asunto se cierra**: una prueba vieja en verde es lo que avisa cuando un cambio nuevo rompe algo viejo |

## Cómo se usa

```
python3 construccion/construir.py          # genera construccion/artefacto.html
python3 construccion/pruebas.py            # lo comprueba
python3 construccion/generar_doc09.py      # rehace el documento 09 desde OBLIG
```

Las pruebas necesitan Playwright y un Chromium; la ruta al navegador se pasa en la variable `CHROMIUM` si no es la predeterminada.

## Dos reglas que costaron caro aprender

**Primera: una sustitución que no encuentra su objetivo detiene el guion.** El 19 de septiembre una expresión regular dejó de coincidir porque el marcado había ganado un `flex-wrap:wrap`. La sustitución falló **en silencio** y el artefacto se publicó con un botón que allí no funciona. Desde entonces cada sustitución frágil comprueba que cambió algo y aborta si no. Un guion de construcción que sigue adelante sin haber hecho su trabajo es peor que uno que se rompe.

**Segunda: lo que `mapa_svg.js` sobrescribe hay que mantenerlo al día a mano.** Como se carga después, sus versiones de `quitaPunto`, `ponMarcador` e `iniciaMapa` ganan. El mismo día se descubrió que `quitaPunto` se había quedado atrás: no limpiaba una clave nueva y sí limpiaba cinco que ya no existen. **Al tocar en el prototipo cualquiera de las funciones que este archivo redefine, hay que revisar si aquí también.**

## Lo que las pruebas cubren

Que el bloque plegable nace cerrado y sus campos no están en el árbol del documento; que abre, cierra y conserva lo capturado; que ningún campo obligatorio queda escondido —y que, forzando que uno lo estuviera, la validación lo despliega—; que la ubicación del dispositivo avisa cuando no hay permiso y coloca el punto cuando lo hay; que **el punto no escribe en la dirección**; y que las siete pantallas se dibujan sin error propio en consola.

No cubren la apariencia. Eso se revisa mirando.

## El documento 09 se genera, no se escribe

`OBLIG` es la única fuente de verdad: de él salen la marca de «opcional» en pantalla, la validación y el documento 09. Mantener las tres cosas a mano es garantizarse que se separen, y cuando se separan **el documento que sustenta la minimización ante la Unidad de Transparencia empieza a decir algo distinto de lo que el formulario hace**. Por eso el documento se regenera.

El generador conserva la parte redactada a mano —del apartado 3 en adelante—, la busca por su encabezado y la vuelve a pegar. Si no la encuentra, **se detiene con error en vez de publicar un documento mutilado**. Ya ocurrió una vez que un generador anterior se llevó por delante esa cola.

Ese generador anterior, además, **no estaba en ninguna parte**: se escribió en una sesión de trabajo y se perdió con ella. Es la misma lección que el resto de esta carpeta: lo que produce un entregable vale tanto como el entregable, y va al repositorio.
