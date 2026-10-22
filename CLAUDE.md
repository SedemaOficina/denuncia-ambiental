# Denuncias Ambientales · instrucciones para Claude Code

Formulario web de denuncia ambiental ciudadana de la Secretaría del Medio Ambiente de la Ciudad de México (SEDEMA), para la Dirección General de Inspección y Vigilancia Ambiental (DGIVA). Lo dirige Liber Saltijeral, asesor en la Oficina de la Secretaría (Sistema de Información Ambiental, SIA). **Liber no programa:** todo el código se hace con Claude. Explícale lo que hiciste en lenguaje llano, sin jerga, en español institucional mexicano.

Este archivo existe porque la memoria del entorno anterior (Claude en la app de escritorio) no viaja. Todo lo que haya que saber está aquí o en `documentacion/`.

## Dónde está el proyecto

- **Fase 1, maqueta del formulario: en cierre** (DEC-229). El acta de validación de la DGIVA se firmó sobre la «Versión 30 · Validación DGIVA» (DEC-230). Para cerrar la fase faltan tres puntos, y los tres dependen de otras áreas, no de código:
  1. Criterio 1: el fundamento de «Plásticos de un solo uso», hoy hueco visible `[Art. __, fracc. __]`.
  2. Criterio 6: P-02, tres datos del aviso de privacidad (Unidad de Transparencia).
  3. Criterio 7: la respuesta de la DGIVA a OBS-0024.
- **Fase 2, contrato de datos y servicios:** se puede adelantar lo que no dependa de esos puntos (diccionario de datos, catálogos).
- **Plan de corrección de la auditoría, terminado:** `documentacion/AUDITORIA-2026-10-20.md`, apartado 11. Los siete bloques están hechos: el 2 salió como «Versión 31» (DEC-232); el 4, como «Versión 32» y «Versión 33» (DEC-233 a DEC-235); el 3, sólo documentos (DEC-236); el 5, como «Versión 34» (DEC-237); el 6, limpieza, sin cambio de versión (DEC-239). Aparte, la «Versión 35» corrigió la empresa propuesta en el responsable (DEC-238) y la «Versión 36» hizo que «Atrás» del navegador regrese al paso anterior (DEC-241). La «Versión 37» agrega el modo captura por personal (DEC-248). De «Para decidir» quedan abiertos los puntos 2 (presupuesto de peso), 6 (trato del aviso de privacidad) y 7 (P-04). El 7 cerró el plan el 21 de octubre: las baterías del paso 2 corren también sobre la versión publicada, con Leaflet guardado en `construccion/terceros/` (DEC-240). Lo anotado «de paso» queda en la bitácora del documento 11.
- **Maqueta del módulo de administración:** bosquejo al día (documento 22, versión 0.11); hechos el bloque A, cascarón y cuarenta denuncias de prueba (DEC-242), el B, bandeja con vistas, filtros y búsqueda (DEC-243), el C, expediente (DEC-244), el D, Inicio, tablero y mapa operativo (DEC-245 a DEC-247), el E, captura por personal, que es el «modo captura» del propio formulario (DEC-248, «Versión 37»), y el F, búsqueda, exportación y administración (DEC-249). **La maqueta está completa**; después, el tablero pasó a llevarse por año (DEC-251) y cada coordinación da de alta y de baja a su personal (DEC-252). Lo que sigue es la sesión con la DGIVA y la DGCORENADR (documento 22, §9, paso 4).
- **Todo cambio visible en el formulario sale como «Versión 31» o posterior** y se informa a la DGIVA con la relación de cambios respecto de la versión firmada (DEC-230).

## Documentos que mandan

| Documento | Para qué |
|---|---|
| `documentacion/05-decisiones-y-pendientes.md` | **El de referencia.** Toda decisión, con clave `DEC-n`, fecha, razón y estado; preguntas abiertas `P-n` y su registro de respuestas |
| `documentacion/11-ruta-de-trabajo.md` | Fases y criterios de salida, convenciones de código (§3), regla contra el código zombi (§4), procedimiento de cambios (§7) y bitácora |
| `documentacion/01-ficha-del-proyecto.md` | Estado del proyecto en una página |
| `documentacion/20-que-resuelve-el-servidor-del-sia.md` | Lo que el servidor del SIA debe resolver al montar el formulario (SIA-n) |
| `construccion/LEEME.md` | Cadena de construcción y pruebas |

Los documentos 09 y 10 **se generan** del prototipo; no se editan a mano sus apartados generados.

## Cómo se trabaja

1. **Un solo archivo fuente:** `prototipo/prototipo-denuncia-ambiental-sedema.html`. `construccion/artefacto.html` y `docs/index.html` se generan; nunca se editan. La maqueta del módulo de administración tiene su propio archivo, `prototipo/administracion/maqueta-administracion.html`; lo que comparte con el formulario lo mete `construccion/generar_admin.py` entre marcas y no se edita a mano (DEC-242).
2. **Antes de añadir, busca.** Si lo que se pide ya existe, se corrige ahí; no se escribe una regla nueva encima de la anterior.
3. **Después de cada cambio**, en este orden:
   ```
   python construccion/generar_doc09.py     # documento 09 y versión declarada en el prototipo
   python construccion/generar_doc10.py     # documento 10
   python construccion/construir.py         # artefacto
   python construccion/generar_admin.py     # lo que la maqueta de administración toma del formulario
   python construccion/publicar_pages.py    # docs/index.html para GitHub Pages
   python construccion/pruebas.py           # todas las baterías; deben quedar en verde
   ```
   Si una batería falla, no se hace commit. Hoy: 1 872 comprobaciones en 53 baterías, de ellas 285 sobre la versión publicada.
4. **Registra cada decisión** como renglón nuevo `DEC-n` en la tabla del documento 05, con sus cinco celdas (Clave, Decisión, Fecha, Razón, Estado). Si la nueva decisión modifica otra, escribe «Modifica DEC-x» en la razón y cambia el estado de DEC-x a «Modificada por DEC-n». La batería 36 revisa que la numeración no tenga huecos y que toda decisión citada exista.
5. **Anota en la bitácora** del documento 11 qué cambió y por qué.
6. **Versión en pantalla.** El formulario muestra siempre su versión («Versión N · Validación DGIVA», en `VERSION_FORMULARIO`). Sube N cuando cambia algo visible.
7. **Commit y push.** Haz el commit y el push tú mismo. Dale a Liber el nombre del commit. Termina el mensaje con la línea de coautoría de Claude.
8. **Trabajo por bloques cerrados** (documento 11, §7.4): un propósito por bloque. Lo que llegue «de paso» se anota para el bloque siguiente.

## Reglas que no se negocian

- **Nunca borres archivos.** Lo que sobre se mueve a `_to_delete/` (ignorada por git) y se le avisa a Liber para que él lo borre.
- **Nunca inventes un número de artículo, fracción o numeral.** Si no está verificado contra el texto vigente, el hueco queda visible: `[Art. __, fracc. __]`, y se advierte.
- **Advierte cuando una petición contradiga una decisión anterior**, en lugar de ejecutarla sin más.
- **Sin código zombi:** ninguna función, variable, clase o estilo sin uso; nada de código comentado (documento 11, §4). La batería 35 lo revisa.
- **Hojas de estilo** (documento 11, §3.6): un selector, una declaración (excepciones comentadas: `textarea`, `select`, `input[type=date]`); sin `!important` salvo en el bloque de `prefers-reduced-motion`; colores sólo desde variables de `:root`; estilo por clase, nunca por `#id`; estilos en línea repetidos se vuelven clase; cada regla nueva en su bloque, no al final del archivo.
- **Una sola fuente de verdad por concepto:** `OBLIG`, `FORMATO`, `MATERIAS`, `DERIVA`, `LIMITES`, `BIFURCACIONES`, `ESCENARIOS`. Un valor que ya vive en una de ellas no se repite.
- **Comentarios que explican por qué**, en español; identificadores en español sin acentos.
- **Lo que `construccion/mapa_svg.js` redefine** (`iniciaMapa`, `ponMarcador`, `vaA`, `ubicaPorDireccion`) se revisa también ahí cuando se toca en el prototipo.
- **Datos y promesas al ciudadano:** hoy no hay servicio de correo (lo dará el SIA, SIA-29); el formulario no promete acuses por correo y el correo no es vía de presentación. Con datos, se notifica en el domicilio. La denuncia anónima se admite, se atiende y se le notifica el resultado en el correo que deja, que es obligatorio (DEC-233). El género se trata con el consentimiento general del aviso de privacidad, sin casilla propia (DEC-234).
- **Claves:** `prototipo/configuracion-local.js` tiene la clave del mapa base y no se versiona. No la copies a ningún otro archivo.

## Entorno en esta computadora (Windows)

Preparado en la primera sesión (DEC-231): Playwright con su Chromium, Pillow, numpy, Node.js, `qpdf` y Poppler (`pdftotext`, `pdfinfo`). Sin la variable `CHROMIUM`, las baterías usan el Chromium de Playwright.

- **Corre la cadena desde PowerShell, no desde Bash.** La terminal Bash de Git trae un `pdftotext` antiguo (Xpdf 4.00) que tapa al de Poppler y hace fallar la batería 25.
- Si `qpdf` o `pdftotext` no aparecen, la terminal se abrió antes de instalarlos: refresca el PATH (`$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')`).

## Lo que vive fuera del repositorio

- **Proyecto «Denuncias Ambientales» en claude.ai:** copia de los documentos para consultarlos desde el chat. La fuente es este repositorio. Si Liber trabaja también desde el chat, recuérdale que los documentos del proyecto pueden quedar atrás.
- **Seguimiento de la fase 1** (criterios, acciones, preguntas y observaciones): https://claude.ai/artifact/NvZi6katDj6ZisQPs641fx. Se actualiza desde el chat de claude.ai.
- **Hoja de observaciones de la DGIVA:** Apps Script en `revision/`; la copia de control está en `revision/control-observaciones-2026-10-19.tsv`.
- **Repositorio:** https://github.com/SedemaOficina/denuncia-ambiental. GitHub Pages publica `docs/`: el formulario en la raíz y la maqueta del módulo de administración en `/administracion/` (DEC-250).
