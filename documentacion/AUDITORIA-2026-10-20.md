# Formulario web de Denuncia Ambiental · Auditoría de cierre de etapa

**Fecha:** 20 de octubre de 2026
**Objeto auditado:** copia del proyecto sin historial de Git (`prototipo/`, `construccion/`, `docs/`, `documentacion/`, `revision/`, `capas/`), con el formulario en «Versión 30 · Validación DGIVA» (`VERSION_FORMULARIO`, DEC-228). Sin commit identificable: la copia no trae `.git`.
**Perfil:** cierre de etapa (fase 1 cerrada; fase 2 por congelar el prototipo como especificación).
**Alcance:** auditorías de cada cambio (A1 a A6), de cada versión (B1 a B9), de cierre de etapa (D1 a D5, B4 con lector de pantalla), las de interfaz que corresponden tras los cambios grandes del 20 de octubre (C2, C4, C5 y E3) y las de «siempre que aparezca» (G1, G2).
**Modo:** solo lectura. El único archivo escrito en el proyecto es este informe. Los guiones, salidas, PDF generados y huellas están fuera del proyecto, en la carpeta de trabajo de la auditoría (apartado 15).

---

## 1. Veredicto

| Etapa | Veredicto |
|---|---|
| **Cierre de la fase 1 y congelamiento como especificación** | **No lista.** Cuatro hallazgos Altos abiertos: el cierre se declaró con los criterios 5, 6 y 7 incumplidos según su propio texto y sin identificar la versión que firmó la DGIVA; la resolución de P-01 no llegó al acuse; el marco jurídico (documento 03) contradice las citas que el formulario muestra, y el documento 09 afirma cosas falsas sobre los datos personales que se recaban. Hay además 16 contradicciones o huecos de especificación de gravedad Media y no existe presupuesto de peso. |
| En cada cambio (A1 a A6) | **Lista con reservas.** 1 160 comprobaciones en 35 baterías, todas en verde, dos veces. Reservas: ninguna batería ejerce la versión publicada con su mapa real (A1-01) y la batería 35 no detecta obligatoriedades escritas a mano ni variables locales sin uso (A5-01, F1-02). |
| En cada versión (B1 a B9) | **Lista con reservas.** Sin hallazgos Altos en B. Reservas: foco perdido en la ventana del aviso de privacidad (B4-01); acuse en PDF que dice algo distinto de la pantalla en dos rutas (B3-01); sin lector de pantalla, sin axe-core y sin Firefox ni WebKit en este entorno. |
| Antes de usar datos reales o publicar | **No lista**, y no era objeto de esta auditoría: P-02 sigue abierta y E1 no se ha corrido. |

---

## 2. Resumen ejecutivo

El prototipo está en buen estado como pieza de software: se construye de forma reproducible (dos construcciones idénticas entre sí y a lo publicado), sus 1 160 comprobaciones pasan, el texto capturado se escapa bien en pantalla y en el PDF, no hay desborde horizontal en siete anchos y 140 pantallas medidas, los catálogos incrustados cuadran con sus fuentes y el cruce espacial del navegador coincide con las capas más detalladas en el área que atiende en 2 077 de 2 077 puntos.

Lo que impide congelarlo como especificación no está en el código sino en **lo que el proyecto afirma de sí mismo**. El mismo 20 de octubre se registraron cinco versiones (26 a 30), se resolvieron P-01, P-05, P-22 y P-12, se recibió el acta y se cerró la fase; varias de esas resoluciones no se propagaron a los documentos ni a todas las pantallas:

1. **El cierre de la fase 1 no cumple su propio criterio de salida.** El documento 11 exige acta «sobre una versión identificada», P-01 y P-02 resueltas y ninguna observación sin «Atendida» o «Descartada». Hoy la versión del acta es un pendiente, P-02 está «en parte» y OBS-0024 está «Para discusión». Entre la versión que se firmó, que no consta, y la versión 30 cambió al menos la regla de turnado en las Áreas Naturales Protegidas federales (DEC-226).
2. **P-01 se dio por resuelta y el acuse sigue diciendo lo contrario.** El PDF que se entrega a la persona dice «Ley Ambiental de la Ciudad de México, [Art. __, fracc. __]. Por confirmar: depende de la naturaleza jurídica del canal de recepción», y no informa la vía de la Procuraduría ni el plazo, que es lo que la opción A obliga a cuidar. El hueco no figura entre los pendientes de DEC-228.
3. **El documento 03, marco jurídico, quedó atrás de DEC-104** y sostiene como verificados artículos que DEC-104 declaró equivocados, en seis materias.
4. **La parte redactada a mano del documento 09** —el que sustenta la minimización ante la Unidad de Transparencia— afirma que la denuncia anónima no pide datos de contacto y que el domicilio se omite cuando se acepta notificación por correo. Las dos cosas son falsas desde DEC-120 y DEC-134. Es la misma clase de defecto que el documento 16 dio por corregida el 20 de septiembre.

A eso se suman huecos que la fase 2 encontraría al escribir el diccionario de datos: 24 campos de texto sin longitud máxima, una clave de turnado (`FEDERAL`) que ya no corresponde a la regla resuelta, una decisión aceptada (P-20, opción A) que pide un consentimiento separado que no existe, y una tabla de ramas que omite seis bifurcaciones. Ninguno exige rediseñar pantallas; casi todos se corrigen en documentos y en catálogos.

**Recomendación:** no congelar la versión 30 todavía. Ejecutar los bloques 1 a 4 del plan (apartado 11), que no requieren código de servidor y son de esfuerzo S o M, y volver a correr D1 sobre el resultado.

---

## 3. Cobertura

Escala de calificación: 5 = completa y sin Críticos ni Altos; 1 = no se pudo hacer.

| Código | Auditoría | Estado | Cómo se hizo | Hallazgos (C/A/M/B/I) | Calif. | Qué faltó |
|---|---|---|---|---|---|---|
| A1 | Pruebas y regresión | En parte | `pruebas.py` sobre copia, dos corridas (línea base y final); revisión de qué archivo ejercita cada batería | 0/0/1/0/1 | 4 | Sin Git no se pudo correr cada prueba contra la versión anterior; no hay integración continua visible en la copia |
| A2 | Integridad de datos | Hecha | Conteos de catálogos y capas contra documentos y archivos de origen | 0/0/0/0/0 | 5 | Sin sumas de control registradas en el proyecto con las cuales comparar |
| A3 | Construcción reproducible | Hecha | `construir.py` dos veces en carpeta temporal; `publicar_pages.py`, `generar_doc09.py` y `generar_doc10.py` en copia; comparación byte a byte | 0/0/0/1/0 | 4 | — |
| A4 | Calidad estática | Hecha | `node --check` y ESLint 10.1 sobre los cinco bloques de código del prototipo juntos | 0/0/0/1/0 | 4 | Sin revisión de tipos (no aplica a JavaScript sin tipos) |
| A5 | Consistencia automática | Hecha | Identificadores repetidos, secretos en lo publicado, términos retirados, decisiones citadas contra registro | 0/0/1/0/0 | 4 | — |
| A6 | Estilos y contraste | Hecha | Contraste de cada nodo de texto visible sobre su fondo compuesto, 140 pantallas; batería 35 | 0/0/0/0/0 | 5 | Contraste de capas sobre mapa base: no medible sin el mapa base (sin red) |
| B1 | Barrido de pantallas | Hecha | Guion propio: 7 anchos (360, 390, 430, 844×390, 768, 1440, 640×400 como zoom 200 %) × 20 pantallas y variantes | 0/0/0/0/0 | 5 | Mapa Leaflet de la versión publicada (sin red) |
| B2 | Coherencia de cifras | No aplica | No muestra cifras ni indicadores | — | — | — |
| B3 | Archivos que genera | Hecha | Acuse PDF de tres escenarios, dos veces; metadatos, acentos, paginación y contenido contra pantalla | 0/0/1/0/0 | 3 | — |
| B4 | Accesibilidad | En parte | Nombres accesibles, identificadores, referencias ARIA, letra mínima, contraste, recorrido con teclado en 6 pantallas y 2 anchos, foco de ventanas | 0/0/1/0/0 | 3 | axe-core no está instalado; sin lector de pantalla; sin simulación de daltonismo |
| B5 | Robustez | Hecha | Borrador dañado (paso inexistente, estado de otro tipo), marcado inyectado, sin bibliotecas externas | 0/0/0/1/0 | 4 | Servidor lento o caído: no hay servidor |
| B6 | Teléfono y sin conexión | En parte | Horizontal 844×390; arranque con todo recurso externo bloqueado | 0/0/0/0/0 | 4 | No hay modo sin conexión que probar (no hay caché ni envíos) |
| B7 | Privacidad técnica | Hecha | Bloqueo de todo dominio externo y conteo | 0/0/0/0/1 | 4 | — |
| B8 | Navegadores y fechas | En parte | Chromium; reloj fijado al 31 de diciembre 23:30 en dos zonas horarias (resultado en D2-03) | 0/0/0/0/0 | 2 | Firefox y WebKit no están instalados |
| B9 | Seguridad del despliegue | No aplica | Sin servidor propio; GitHub Pages no admite cabeceras | — | — | Revisar en fase 4 |
| C2 | UX heurística | En parte | Sólo lo que surgió de las pruebas (registrado en C4-01 y B3-01) | 0/0/0/0/0 | 2 | Revisión heurística completa (la última es el documento 07, 18 sep) |
| C4 | Matriz de estados | En parte | «Atrás», adelante, recarga, doble clic al enviar | 0/0/1/0/0 | 3 | Dos pestañas, enlace compartido |
| C5 | Textos | Hecha | Inventario de 31 973 palabras en 87 pantallas y variantes; trato, términos retirados, siglas | 0/0/0/1/0 | 4 | Revisión ortográfica completa |
| D1 | Coherencia documental | Hecha | Cruce de documentos 01 a 22, decisiones, respuestas, código y pruebas | 0/3/8/2/0 | 1 | — |
| D2 | Modelo de datos | Hecha | `OBLIG`, `DERIVADOS`, `INTERNOS`, `LIMITES`, `FORMATO` contra documentos 04 y 09 | 0/0/2/1/0 | 2 | No hay base de datos todavía: se auditó el contrato implícito |
| D3 | Datos de terceros | Hecha | Conteos de capas y catálogos; 2 077 puntos cruzados contra capas más detalladas | 0/0/0/0/1 | 5 | `validar_catalogos.py` requiere `shapely`, no instalado |
| D4 | Peso y velocidad | En parte | Peso total y comprimido; carga y cambio de paso con procesador 1×, 4× y 6× más lento | 0/0/1/0/0 | 2 | Red 3G simulada no aplicable a archivo local; no hay presupuesto |
| D5 | Validación del método | No aplica | No calcula índices ni puntajes | — | — | — |
| E3 | Intentar romperlo | En parte | Datos raros, longitudes, relleno, inyección, doble envío, «Atrás», recarga, reloj (resultados registrados en D2-01, D1-12, C4-01, B5-01 y D2-03) | 0/0/0/0/0 | 4 | Sin servidor: peticiones simultáneas y sesiones no aplican |
| G1 | Cotejo normativo | En parte | Coherencia interna de cada cita entre formulario y documentos | 0/1/0/0/0 | 1 | **No verificable en esta auditoría** contra el texto oficial: sin salida a internet y sin la carpeta `insumos/normativa` en la copia |
| G2 | Componentes compartidos | Hecha | Leaflet, OpenStreetMap, Nominatim, Google Fonts, Apps Script | 0/0/0/0/0 | 5 | Sin fallas atribuibles a terceros |
| E1, E2, F1 a F6, H1 a H7 | — | No corresponden a esta etapa | Se anotan las observaciones que surgieron (F1-01, F1-02, E1-01) | — | — | — |

**Totales: 0 Críticos · 4 Altos · 16 Medios · 10 Bajos · 3 Informativos = 33 hallazgos.**

### 3.1 Auditorías anteriores

| Código | Auditoría | ¿Se hizo? | Fecha o versión | Informe o evidencia | Hallazgos y estado hoy | Qué faltó |
|---|---|---|---|---|---|---|
| A1 | Pruebas y regresión | Sí | Continuo; 35 baterías al 20 oct | `construccion/pruebas/`, bitácora del doc 11 | En verde | Prueba contra la versión anterior; cobertura de la versión publicada (A1-01) |
| A3 | Construcción | Sí | DEC-146 (30 sep) | `construir.py` aborta si una sustitución no encuentra su texto | Se mantiene | `publicar_pages.py` no comprueba dos de sus sustituciones (`robots`, título); hoy funcionan |
| A4, A5, A6 | Código muerto, estilos, contraste | Sí | DEC-227, 20 oct; doc 06, 18 sep | Batería 35; doc 06 | Cerrados | Variables locales (A4-01); obligatoriedad literal (A5-01) |
| B1, B4 | Barrido y accesibilidad | En parte | Diagnóstico con el estándar del SIA (doc 11:1060) | Doc 11 | Sin violaciones de axe a 390 y 1280 px | Lector de pantalla; foco de ventanas (B4-01) |
| C2 | Heurística | Sí | 18 sep | Doc 07 | Nota de vigencia | No repetida tras los cambios del 19 y 20 oct |
| C3 | Carga de la interfaz | Sí | 19 sep | Doc 13 y bitácora del doc 11 | Medido en pantallas por paso | No repetida tras DEC-200 a DEC-220 |
| D1, G1 | Coherencia y cotejo | Sí | 20 sep | Doc 16; DEC-104 (21 sep) | **Tres regresiones**: conteo de preguntas (D1-05), cola del doc 09 (D1-03), decisión revertida sin marca (D1-04) | El doc 03 no se revisó entonces (D1-02) |
| E3 | Abuso | Sí | 20 sep | Doc 15 | Controles 1 y 2 adoptados (P-21) | Controles 3 a 6, de servidor |
| — | Auditoría de cierre | Sí | 30 sep | DEC-146 | — | — |

---

## 4. Las 10 de mayor prioridad

| # | Clave | Gravedad | Esfuerzo | Qué |
|---|---|---|---|---|
| 1 | D1-01 | Alta | S | Cierre de fase 1 con criterios 5, 6 y 7 incumplidos; acta sin versión ni constancia; cambios posteriores sin ratificar |
| 2 | G1-01 | Alta | S | P-01 resuelta y el acuse sigue con el hueco «depende de la naturaleza jurídica del canal»; faltan vía de la Procuraduría y plazo |
| 3 | D1-03 | Alta | M | Documento 09: afirmaciones falsas sobre datos personales en la parte redactada a mano |
| 4 | D1-02 | Alta | M | Documento 03 cita seis materias con artículos que DEC-104 declaró equivocados |
| 5 | D2-01 | Media | S | 24 de 32 campos de texto sin longitud máxima: el diccionario no puede escribirse desde el prototipo |
| 6 | D1-04 | Media | S | P-22 resuelta, y cinco documentos siguen diciendo «PROFEPA, provisionalmente» |
| 7 | B3-01 | Media | S | El acuse en PDF promete visita de inspección en las rutas federal y de autoridad |
| 8 | D2-02 | Media | S | `dg = 'FEDERAL'` ya no es una unidad que reciba |
| 9 | D1-09 | Media | S | P-20 aceptada con una condición —consentimiento separado— que no existe |
| 10 | D1-07 | Media | S | DEC-90 a DEC-93 se citan en código y documentos y no están en el registro |

---

## 5. Hallazgos completos

### 5.1 Altos

#### D1-01 · El cierre de la fase 1 no cumple el criterio de salida escrito, y la versión firmada no está identificada
- **Gravedad:** Alta · **Prioridad:** 1 · **Esfuerzo:** S
- **Auditoría y etapa:** D1, cierre de etapa.
- **Dónde:** `documentacion/11-ruta-de-trabajo.md`:24, 30-36, 1197, 1207; `documentacion/05-decisiones-y-pendientes.md`:236 (DEC-228), 779 (P-02); `revision/control-observaciones-2026-10-19.tsv`, renglón 24.
- **Qué pasa.** Se esperaba que «criterios 2 a 7 cumplidos» (doc 11:24 y DEC-228) fuera cierto. Se observa:
  - Criterio 5 exige el acta «sobre una versión identificada del prototipo» (11:34); DEC-228 deja como pendiente «registrar sobre qué versión se firmó el acta».
  - Criterio 6 exige P-01 **y P-02** resueltas (11:35); P-02 está «En parte» (05:779). El 11:1197 lo redefine («no impiden cerrar la fase») sin modificar el criterio.
  - Criterio 7 exige que ninguna observación quede fuera de «Atendida» o «Descartada» (11:36); OBS-0024 está «Para discusión» (TSV renglón 24) y DEC-228 la traslada como pendiente.
  - El acta no está en el repositorio ni referida por un archivo; DEC-226 dice que se entregó «firmada, en físico».
  - El mismo día, después de las versiones 26 a 28, la versión 29 (DEC-226) cambió el turnado en las Áreas Naturales Protegidas federales (de «PROFEPA» a «DGCORENADR recibe y remite»), y la 30 (DEC-227) cambió código. La especificación que se va a congelar es la 30.
- **Consecuencia.** La fase 2 traduciría a contrato una versión que no consta que la DGIVA haya validado, y el registro dice que se cumplieron criterios que no se cumplieron.
- **Cómo se reproduce.** Leer los cuatro lugares citados.
- **Evidencia.** Citas textuales arriba; `grep -n "Para discusión"` en el TSV devuelve un renglón.
- **Reproducido:** 2 de 2 (lectura y búsqueda independientes).
- **Causa probable.** Cierre registrado en la misma jornada que las respuestas, sin repasar el criterio.
- **Corrección propuesta.** Registrar la versión y la fecha del acta; anexar una relación de cambios entre esa versión y la 30, y obtener la conformidad de la DGIVA sobre ella, o declarar formalmente qué criterios se dispensan y por qué (decisión nueva que modifique el criterio). Guardar en el repositorio una referencia al acta (número de oficio o digitalización sin datos personales).
- **Listo cuando:** DEC-228 y el doc 11 nombran la versión firmada; hay una decisión que acepta o ratifica cada cambio posterior; el texto de los criterios 5 a 7 coincide con su estado. Prueba automática: un guion de coherencia (apartado 12) que falle si el doc 11 dice «cumplidos» y existe una observación en estado distinto de «Atendida» o «Descartada».
- **Estado:** Abierto · Decide el dueño (ver «Para decidir», 1).

#### G1-01 · P-01 se resolvió sin llegar al acuse ni a la lista de pendientes
- **Gravedad:** Alta · **Prioridad:** 2 · **Esfuerzo:** S
- **Auditoría y etapa:** G1 y D1, cierre de etapa.
- **Dónde:** `prototipo/prototipo-denuncia-ambiental-sedema.html`:5256-5259 (acuse PDF), 3497-3502 (acuse en pantalla); `documentacion/05-decisiones-y-pendientes.md`:246-266 (P-01), 778 (respuesta).
- **Qué pasa.** P-01 está resuelta con la opción A: la Secretaría recibe como denuncia ciudadana con fundamento en el Reglamento Interior. La propia pregunta dice qué obliga esa opción: «El acuse. Debe decir que la Secretaría atiende la denuncia, en qué plazo informa del trámite, y que quien quiera la respuesta fundada y motivada en treinta días hábiles del artículo 332 puede acudir además a la Procuraduría». Observado en el PDF de tres escenarios: «Fundamento jurídico: Ley Ambiental de la Ciudad de México, [Art. __, fracc. __]. Por confirmar: depende de la naturaleza jurídica del canal de recepción.» Ni la pantalla ni el PDF mencionan la vía de la Procuraduría. El comentario del código (5256) sigue diciendo que P-01 «no está resuelta». DEC-228 sólo traslada como huecos el fundamento de plásticos y los tres datos del aviso.
- **Consecuencia.** El documento que la persona conserva dice que el fundamento depende de una decisión ya tomada, y nombra la ley que no es (la opción A se funda en el Reglamento Interior). Al congelar, el hueco pasaría al contrato sin estar registrado como pendiente.
- **Cómo se reproduce.** Panel de validación → escenario «Suelo urbano» → enviar → «Descargar acuse (PDF)» → apartado «Fundamento».
- **Evidencia.** `pdftotext acuse-urbano.pdf` (también `anp_federal` y `gobierno`): renglón 154, texto citado.
- **Reproducido:** 2 de 2 corridas, en 3 de 3 escenarios.
- **Causa probable.** La resolución de P-01 cambió el estado de la pregunta y no los textos que de ella dependían («Bloquea: P-02, P-05, P-07 y todos los textos del formulario»).
- **Corrección propuesta.** Registrar el hueco como pendiente con su clave; redactar el fundamento del acuse conforme a la opción A una vez verificado por la unidad jurídica (los artículos citados en P-01 **no pudieron verificarse en esta auditoría**); añadir al acuse la vía de la Procuraduría y el plazo (P-07, hoy «en parte»).
- **Listo cuando:** el PDF y la pantalla de cada escenario contienen el mismo fundamento y la mención de la Procuraduría; una batería compara ambos textos.
- **Estado:** Abierto · Decide el dueño con la unidad jurídica.

#### D1-02 · El marco jurídico (documento 03) contradice las citas del formulario y las presenta como verificadas
- **Gravedad:** Alta · **Prioridad:** 4 · **Esfuerzo:** M
- **Auditoría y etapa:** D1 y G1, cierre de etapa.
- **Dónde:** `documentacion/03-marco-juridico.md`:3, 17-27, 108-120, 190; `documentacion/05-decisiones-y-pendientes.md`:112 (DEC-104); prototipo, catálogo `MATERIAS` (1099-1159).
- **Qué pasa.** Versión 1.0 del 18 de septiembre, sin nota de vigencia. Su §3 da como fundamento:

  | Materia | Documento 03 | Formulario (tras DEC-104, 21 sep) |
  |---|---|---|
  | Arbolado urbano | Art. 106 | Arts. 108, 109 y 112 |
  | Impacto ambiental | Arts. 23 y 53 | Arts. 25 y 50 |
  | Descargas | Arts. 223 y 230 | Arts. 223, 226 y 227 |
  | Áreas verdes | Arts. 104 a 106 | Arts. 105 y 113 |
  | Suelo de conservación | Art. 92 | Arts. 98, 123 y 138 (se retiró el 92) |
  | Áreas Naturales Protegidas | Art. 126 | Arts. 98, 123 y 138 |

  DEC-104 declara expresamente que el 106, el 53, el 230 y el 92 «eran de otra materia». El §7 del mismo documento dice que «los artículos citados fueron verificados contra el texto vigente». Su §2 afirma que «la Ley no prevé a la Secretaría como receptora de la denuncia ciudadana» y recomienda la «Vía A — reporte ciudadano», cuando P-01 se reformuló el 25 de septiembre y se resolvió en sentido contrario (denuncia ciudadana).
- **Consecuencia.** Quien redacte el contrato o el acuse con el documento 03 como referencia jurídica reintroduce las cuatro citas que el proyecto ya corrigió.
- **Evidencia.** Líneas citadas; DEC-104 textual.
- **Reproducido:** 2 de 2.
- **Causa probable.** El documento no se actualizó tras DEC-104 ni tras la reformulación de P-01; el documento 16 revisó la vigencia de 02, 04 y 12, no la del 03.
- **Corrección propuesta.** Actualizar §2, §3 y §7 contra DEC-104 y P-01, o ponerle nota de vigencia que remita a DEC-104 y al catálogo `MATERIAS`. **Que cuál de las dos citas es la vigente no pudo verificarse aquí**: el cotejo contra el texto oficial queda para la unidad jurídica.
- **Listo cuando:** cada materia cita en el doc 03 lo mismo que `MATERIAS`; prueba automática que extraiga los artículos de ambos y los compare.
- **Estado:** Abierto.

#### D1-03 · El documento 09 afirma cosas falsas sobre los datos personales que se recaban (regresión)
- **Gravedad:** Alta · **Prioridad:** 3 · **Esfuerzo:** M
- **Auditoría y etapa:** D1, cierre de etapa.
- **Dónde:** `documentacion/09-mapeo-campos-obligatorios.md`:189-216 (parte redactada a mano, que el generador conserva).
- **Qué pasa.** El encabezado generado dice 57 campos, 22 datos personales. La parte redactada a mano dice:
  - «Los cincuenta y tres tienen una finalidad verificable» (189): son 57.
  - H-01: «En los dos esquemas el teléfono aparece como obligatorio… Propuesta: volverlo opcional» (191-193): el segundo esquema se retiró con DEC-97 y P-17 se resolvió (sigue obligatorio, DEC-222).
  - H-02: «Seis campos contienen datos personales de terceros… nombre, señas, domicilio y persona encargada del presunto responsable» (195-196): tras DEC-193 sólo quedan dos con dato personal (`resp_senas`, `resp_area`).
  - H-04: «Se conserva en el bloque de persona física» (202-203): ese bloque se retiró (DEC-193).
  - §4: «Los siete campos de domicilio se omiten cuando la persona acepta la notificación por correo electrónico (DEC-48)» (212): **falso**; el domicilio es siempre obligatorio y no hay notificación por correo (DEC-134).
  - §4: «La denuncia anónima no pide ningún dato de contacto» (214): **falso**; exige correo (DEC-120, `EXIGIDO_ANONIMO`).
- **Consecuencia.** El documento que el `LEEME` de construcción describe como «el que sustenta la minimización ante la Unidad de Transparencia», y cuyo mapeo validó la DGIVA, contradice el aviso de privacidad y el formulario en qué datos personales se piden.
- **Evidencia.** Líneas citadas; `generar_doc09.py` regenera un documento idéntico (la cola no se toca).
- **Reproducido:** 2 de 2.
- **Causa probable.** Es la misma clase de defecto que el documento 16 (§3.3) dio por corregida el 20 de septiembre: texto escrito a mano dentro de un documento generado.
- **Corrección propuesta.** Reescribir §3 y §4 contra `OBLIG`, o generarlos (número de campos y de datos personales de terceros desde `OBLIG`).
- **Listo cuando:** ninguna cifra de la cola difiere de la tabla generada; prueba que compare cada número escrito en letra con el calculado.
- **Estado:** Abierto · regresión de un hallazgo dado por cerrado.

### 5.2 Medios

#### D1-04 · P-22 resuelta, y cinco lugares siguen con el criterio provisional
- **Dónde:** `01-ficha-del-proyecto.md`:40; `10-variantes-del-formulario.md`:62 (tabla escrita a mano dentro del documento generado: «PROFEPA, provisionalmente… Criterio a consulta de las áreas (P-22)»); `19-nomenclatura-de-folios.md`:32; `22-bosquejo-modulo-de-administracion.md`:62; DEC-89 (05:102) sin marca de sustituida por DEC-226.
- **Qué pasa.** El formulario y el doc 02 aplican «la DGCORENADR recibe y remite»; esos cinco lugares dicen lo anterior. Es la tercera vez que una decisión revertida queda sin marca (doc 16 §3.3 lo señaló con DEC-07).
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Corrección:** actualizar los cinco y añadir columna de estado a la tabla de decisiones. **Listo cuando:** búsqueda de «provisional» junto a P-22 devuelve cero fuera del historial.

#### D1-05 · El encabezado del documento 05 cuenta mal las preguntas (regresión)
- **Dónde:** `05-decisiones-y-pendientes.md`:5 contra el registro de respuestas (776-799).
- **Qué pasa.** Dice «trece todavía sin respuesta, cuatro respondidas en parte y una retirada». El registro da: 3 sin respuesta (P-04, P-06, P-14), 7 en parte, 2 retiradas (P-12, P-15), 1 consolidada (P-19) y 9 resueltas. El documento va dirigido a la DGIVA. Doc 16 §3.3 había corregido el mismo conteo.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Listo cuando:** el conteo se genera o se comprueba con un guion.

#### D1-06 · La tabla de ramas (`BIFURCACIONES`, documento 10 y panel) está desactualizada
- **Dónde:** prototipo:1558-1577; `10-variantes-del-formulario.md`:14.
- **Qué pasa.** Dice «6 supuestos de otra autoridad»: son 7 desde DEC-222 (`DERIVA.length` = 7). «Desde cuándo ocurre… cambia el texto de la fecha que se pide»: desde DEC-206 la fecha depende de «¿Conoces la fecha?» y su rótulo es fijo. Faltan seis ramas que cambian la forma del formulario: `conoce_fecha`, `tiene_mz_lote` y `dom_tiene_mz_lote`, `reporto_antes`, `veh_servicio` (vehículo), `ruido_medicion` (ruido con datos) y el ámbito «No lo sé». El criterio 2 de la fase 1 («bifurcaciones documentadas y simulables una por una») se dio por cumplido.
- **Consecuencia.** El contrato que «reproduce exactamente el comportamiento» partiría de una tabla incompleta.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Listo cuando:** prueba que exija que toda condición de `OBLIG` que dependa de una respuesta tenga su renglón en `BIFURCACIONES`, y que los conteos se calculen de los catálogos.

#### D1-07 · DEC-90 a DEC-93 se citan y no existen en el registro
- **Dónde:** registro de decisiones salta de DEC-89 a DEC-95 (223 filas). DEC-90 se cita en el prototipo (entre calles en un solo campo), en 05:109 (con otro sentido: pegar un enlace), en 11 y 17; DEC-91 (tabla `FORMATO`, base de la validación) en el prototipo y en 05:109 y 05:232; DEC-92 y DEC-93 en el prototipo y en la batería 01.
- **Consecuencia.** La tabla de formatos —regla de validación de cada campo del futuro diccionario— se apoya en una decisión no registrada; la regla 7.5 del doc 11 exige que toda decisión quede escrita.
- **Reproducido:** 2 de 2 (búsqueda de citas contra claves registradas). **Esfuerzo:** S.

#### D1-08 · P-12 «retirada» sin motivo ni sustituto, y sigue citada como respuesta
- **Dónde:** DEC-226 (05:234) «(5) P-12: se retira»; 05:635-636 (dos riesgos con mitigación «P-12»), 05:644 (secuencia), `11-ruta-de-trabajo.md`:77 (producto de la fase 3), `12-conformidad-con-la-norma.md`:98, 117.
- **Qué pasa.** No se dice por qué se retira ni qué la sustituye (posiblemente SIA-05 y SIA-06 del doc 20, sin que nada lo enlace).
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Corrección:** motivo y remisión a SIA-05/SIA-06 en DEC-226 y en los lugares citados.

#### D1-09 · P-20 aceptada con una condición que el formulario no cumple
- **Dónde:** 05:584 (opción A: «Conservarlas como están, **con consentimiento expreso separado del resto**»), 05:797 (respuesta A); prototipo:3283-3286 (una sola casilla); aviso de privacidad: «El género es un dato personal sensible, por lo que sólo se tratará con su consentimiento expreso».
- **Qué pasa.** Hay una sola casilla que junta consentimiento general y protesta de decir verdad; no hay consentimiento separado para el género. La recomendación también condiciona la opción A a que el SIA asuma la publicación de la desagregación; no consta.
- **Consecuencia.** El diccionario de datos necesitaría un campo de consentimiento que el prototipo no tiene.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Estado:** Decide el dueño (ver «Para decidir», 5).

#### D1-10 · Reglas contradictorias sobre la denuncia anónima
- **Dónde:** `02-reglas-de-negocio.md`:97 (RN-17: correo obligatorio «para que la Secretaría pueda pedir lo que falte») y 105 (RN-21: «sin posibilidad de requerimiento… se atiende, pero no se notifica»); acuse anónimo: «Si la Secretaría necesita algo más, te escribirá al correo que dejaste».
- **Consecuencia.** El contrato debe decir para qué sirve el correo de la anónima; según la respuesta cambia si es obligatorio, qué finalidad declara el aviso y si existe el estado «requerimiento» en el expediente.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Estado:** Decide el dueño (ver «Para decidir», 4).

#### D1-11 · El documento 04, modelo de datos, contradice al formulario
- **Dónde:** `04-modelo-de-datos.md`:25 («calle, número exterior, alcaldía, colonia y código postal son obligatorios»), 65 («El Histórico Coyoacán, que el formulario remite a la PROFEPA»).
- **Qué pasa.** El código postal es opcional desde DEC-200; El Histórico Coyoacán lo recibe la DGCORENADR y lo remite (DEC-226). El documento conserva fecha 30 de septiembre.
- **Reproducido:** 2 de 2. **Esfuerzo:** S.

#### D2-01 · 24 de 32 campos de texto sin longitud máxima
- **Dónde:** `LIMITES` (prototipo:1861) sólo fija tope para `hechos`, `gestiones`, `referencias`, `otras_pruebas` y `resp_senas`; sólo `cp`, `dom_cp` y `telefono` llevan `maxlength`.
- **Qué pasa.** Recorriendo pasos 2 a 5 y sus ramas, 24 de los 32 campos de texto no tienen tope: `nombre`, `apellido_paterno`, `apellido_materno`, `correo`, `calle`, `num_ext`, `entre_calles`, `colonia`, `manzana`, `lote`, `nombre_lugar`, `coord_pegar`, `tipo_estab_otro`, `nombre_estab`, `autoridad_denunciada`, `resp_area` y los ocho del domicilio (`dom_calle`, `dom_num_ext`, `dom_num_int`, `dom_manzana`, `dom_lote`, `dom_entre_calles`, `dom_colonia`, `dom_municipio`). Con 20 000 caracteres en «Nombre(s)» y en «Calle», `valida(5)` y `valida(2)` devuelven verdadero.
- **Consecuencia.** El producto 1 de la fase 2 (diccionario: «nombre, tipo, **longitud**…») no puede derivarse del prototipo, y el doc 11 manda corregir el prototipo antes que el contrato.
- **Cómo se reproduce:** guiones `romperlo.py` (caso «sin_tope_de_longitud») y `topes.py`. **Reproducido:** 2 de 2. **Esfuerzo:** S. **Listo cuando:** todo campo de texto de `OBLIG` tiene `max` en `LIMITES` y una prueba lo exige.

#### D2-02 · La clave de turnado `FEDERAL` ya no corresponde a quien recibe
- **Dónde:** prototipo:1466 (`dg`: «DGIVA, DGCORENADR o FEDERAL: enruta la denuncia en el módulo interno»), 2749 (`r.dg = 'FEDERAL'`), 3509-3514.
- **Qué pasa.** Tras DEC-226 la denuncia en ANP federal la recibe la DGCORENADR y la remite; el dato que «enruta en el módulo interno» sigue valiendo `FEDERAL`, que no es una bandeja.
- **Consecuencia.** El catálogo «área que atiende» del diccionario mezclaría unidades receptoras con un destino de remisión.
- **Corrección propuesta:** separar `dg` (DGIVA o DGCORENADR) de una marca de remisión (`remite_a`: PROFEPA). **Reproducido:** 2 de 2. **Esfuerzo:** S.

#### B3-01 · El acuse en PDF dice algo distinto de la pantalla en las rutas federal y de autoridad
- **Dónde:** prototipo:5240-5245 (pasos del PDF) frente a 3497-3514 (pantalla).
- **Qué pasa.** En «ANP federal», la pantalla agrega «Una vez remitida, el seguimiento del asunto corre por cuenta de la PROFEPA»; en «Autoridad», agrega que se emitirán recomendaciones «en lugar de instaurar un procedimiento de inspección» (art. 331). El PDF de ambas rutas dice sólo «Personal de inspección visita el lugar y levanta un acta» y «Se te notifica el resultado en el domicilio que registraste», sin las dos aclaraciones. El comentario del PDF afirma que «dice lo mismo que la pantalla».
- **Consecuencia.** El documento que la persona conserva promete una visita de la Secretaría que, en esas rutas, no ocurrirá.
- **Reproducido:** 2 de 2 (`acuse_pdf.py`, escenarios `anp_federal` y `gobierno`). **Esfuerzo:** S. **Listo cuando:** pantalla y PDF salen de una sola lista de pasos por ruta, y una prueba los compara.

#### B4-01 · La ventana del aviso de privacidad no recibe el foco y lo pierde al cerrarse
- **Dónde:** prototipo:2079-2084 (`abrePrivacidad`), 5632-5637 (Escape).
- **Qué pasa.** Con teclado, al abrir «Aviso de privacidad» desde el pie el foco se queda en el botón de fondo; tras tres Tab entra a la ventana; con Escape la ventana se cierra y el foco cae en el cuerpo del documento, no en el botón que la abrió. La ventana declara `aria-modal="true"` sin contener el foco. WCAG 2.4.3 (orden del foco).
- **Reproducido:** 2 de 2 (`modal_foco.py`, 1280 px). **Esfuerzo:** S.

#### C4-01 · «Atrás» del navegador sale del formulario
- **Dónde:** no hay `pushState` ni `popstate` en el código.
- **Qué pasa.** En el paso 3, «Atrás» lleva a la página anterior al formulario; al volver se ve la portada con la franja «Tienes una denuncia sin terminar» y un clic recupera lo capturado. La recarga hace lo mismo. En teléfono, el gesto de regreso produce este efecto.
- **Reproducido:** 2 de 2 (`atras_y_doble.py`). **Esfuerzo:** M. **Estado:** Decide el dueño (ver «Para decidir», 3).

#### A1-01 · Ninguna batería ejerce la versión que se publica y que validó la DGIVA
- **Dónde:** `construccion/pruebas/*.py`; sólo 28, 33 y 35 leen el prototipo, y sólo como texto.
- **Qué pasa.** Las 35 baterías corren sobre `artefacto.html`, donde `mapa_svg.js` sustituye `iniciaMapa`, `ponMarcador`, `vaA`, `ubicaPorDireccion` y `quitaPunto`. La versión publicada (`docs/index.html`, con Leaflet y geocodificación) no tiene ninguna prueba de comportamiento; el `LEEME` de construcción reconoce que esas funciones ya se desfasaron una vez.
- **Reproducido:** 2 de 2 (búsqueda en las 35). **Esfuerzo:** M. **Listo cuando:** al menos las baterías del paso 2 corren también sobre `docs/index.html` con Leaflet servido desde una copia local fijada.

#### A5-01 · Nueve constructores fijan la obligatoriedad a mano
- **Dónde:** prototipo:2519 (`entre_calles`), 2548 (`coord_pegar`), 2910 (`gestiones`), 3102 (`resp_senas`), 3119 (`otras_pruebas`), 3201 (`telefono` en la anónima, intencional), 3209 (`apellido_materno`), 3231 (`dom_num_int`), 3236 (`dom_entre_calles`).
- **Qué pasa.** Pasan `false` en lugar de `esObligatorio(k)`. Hoy coincide con `OBLIG`; si la DGIVA vuelve obligatorio uno de ellos, la validación lo exigiría y la pantalla lo seguiría mostrando como opcional. El mismo defecto se corrigió dos veces (DEC-198, DEC-202) y la batería 35 no lo detecta.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Listo cuando:** una prueba falla si un constructor recibe un literal en la posición de obligatoriedad (salvo la excepción anotada de la anónima).

#### D4-01 · No hay presupuesto de peso y la cifra documentada está atrasada
- **Qué pasa.** `docs/index.html` pesa 1 016 KB (365 KB comprimido con gzip); el artefacto, 1 025 KB. El doc 12:109 dice «cerca de 730 KB». Con el procesador 6 veces más lento la carga tarda 550 ms (mediana de 3) y el paso más lento se dibuja en 112 ms; el peso de red no pudo medirse con red simulada. El criterio de cierre de etapa pide estar «dentro del presupuesto de peso», que no existe.
- **Reproducido:** 2 de 2. **Esfuerzo:** S. **Estado:** Decide el dueño (ver «Para decidir», 2).

### 5.3 Bajos

| Clave | Dónde | Qué pasa | Reproducido |
|---|---|---|---|
| C5-01 | prototipo:3236 (marcador «Entre calle 1 y calle 2»), 3379 y 3428 (formateo) | La revisión y el acuse dicen «entre Entre la calle Sur 20 y la calle Sur 24»: el marcador invita a escribir «Entre…» y el formateo antepone «entre». Ocurre en los escenarios cuyo dato empieza con «Entre» (siete del domicilio, dos del lugar), en la revisión y en el PDF | 2 de 2 |
| D1-12 | DEC-224 (05:232) | El título dice «Ningún campo de texto libre acepta letras al azar»; calle, entre calles, nombre del establecimiento, nombre, apellido y calle del domicilio aceptan «ASFSAFASFDSFQWRTZX» (la regla cubre siete campos) | 2 de 2 |
| D1-13 | Encabezados de 01 («los diecinueve documentos»: son 20 más la cédula), 02 (v1.3, 30 sep, con contenido del 20 oct), 04, 11 (v1.6, 30 sep), 12; tabla de decisiones | Versiones y fechas que no dicen la vigencia real; 17 filas (DEC-212 a DEC-228) con cinco columnas bajo un encabezado de cuatro | 2 de 2 |
| A3-01 | `construir.py`, paso 1 | El artefacto pierde las metaetiquetas `viewport` y `format-detection` (la corrección de DEC-213 para iPhone) y el idioma `es-MX`; depende de que la plataforma de artefactos las reponga (no verificable aquí) | 2 de 2 |
| A4-01 | prototipo:2600 | ESLint: variable local `dg` asignada y no usada en `cajaCapas()`; 23 bloques `catch` vacíos sin comentario | 2 de 2 |
| F1-01 | `_v.html` en la raíz | Archivo de 1 MB con la «Versión 16», fuera de la documentación del proyecto; si está versionado, publica una versión antigua en un repositorio público | 2 de 2 |
| F1-02 | prototipo:5256 (P-01 «no resuelta»), 3279 («el resto queda por desarrollar (DEC-138)»), 1520 («sin él la Secretaría no puede enviar el folio»: no hay envío de correos, DEC-134), 3434 (`nd:'Prefiere no decirlo'`, opción retirada por DEC-218) | Comentarios y restos que describen un estado anterior | 2 de 2 |
| B5-01 | prototipo:5541-5544 | Un borrador con un paso fuera de 1 a 6 deja la pantalla en blanco, sin mensaje ni salida | 2 de 2 |
| D2-03 | prototipo:4965-4970 | `fecha_acuse` se guarda como texto en español con el reloj y la zona del equipo: con reloj al 31 dic 2026 23:30 (hora de la Ciudad) un equipo en zona de Tokio registra «1 de enero de 2027, 14:30 horas» y folio de 2027. El doc 19 ya fija la hora del servidor para el folio; falta para la fecha de recepción y su tipo de dato | 2 de 2 |
| E1-01 | `sedemaoficina.github.io` | El borrador (con nombre, teléfono, correo y domicilio) se guarda en `localStorage` del origen `sedemaoficina.github.io`, compartido por todas las páginas de proyecto de esa cuenta en GitHub Pages. Riesgo bajo mientras sea versión de prueba con datos ficticios | Lectura de código |

### 5.4 Informativos

| Clave | Qué |
|---|---|
| D3-01 | Cruce del navegador contra la capa original de alcaldías (`capas/originales/alcaldias_cdmx.json`): alcaldía distinta en 17 de 2 077 puntos (2 de 1 500 al azar; 15 de 577 a menos de 150 m de un límite). Área que atiende distinta contra `capas/geometrias.geojson` y `suelo_conservacion.geojson`: 0 de 2 077. Insumo para el conjunto de 50 puntos del criterio de la fase 3 |
| B7-01 | La versión publicada pide recursos a cuatro terceros (Google Fonts, cdnjs, mosaicos de OpenStreetMap y Nominatim) y, en modo revisión, a Apps Script. Está documentado (doc 12:94-98, doc 20 SIA-06) y queda para la fase 4 |
| A1-02 | Las baterías escriben `construccion/pruebas/_pagina.html` dentro del proyecto; no pudo verificarse si `.gitignore` lo excluye (la copia no lo trae) |

### 5.5 Totales

| Gravedad | Número |
|---|---|
| Crítica | 0 |
| Alta | 4 |
| Media | 16 |
| Baja | 10 |
| Informativa | 3 |
| **Total** | **33** |

Por auditoría: D1 13 · D2 3 · A1 2 · F1 2 · G1 1 · A3 1 · A4 1 · A5 1 · B3 1 · B4 1 · B5 1 · B7 1 · C4 1 · C5 1 · D3 1 · D4 1 · E1 1.

---

## 6. Verificado sin hallazgos

- **Pruebas:** 1 160 comprobaciones en 35 baterías, en verde en la línea base (196 s) y en la corrida final.
- **Construcción:** `construir.py` dos veces → archivos idénticos entre sí y al `artefacto.html` del proyecto (SHA-256 `3a79e3a3…`). `publicar_pages.py` → idéntico a `docs/index.html`. `generar_doc09.py` y `generar_doc10.py` → idénticos a los documentos 09 y 10 y al prototipo. La versión publicada lleva `noindex` y la franja de versión de prueba, y no contiene la clave del mapa base.
- **Versión en pantalla:** «Versión 30 · Validación DGIVA» en el pie, tomada de `VERSION_FORMULARIO`.
- **Sintaxis y análisis estático:** sin errores; sin variables globales sin definir.
- **Barrido (B1):** 280 pantallas medidas (140 en la versión publicada, 140 en el artefacto) en siete anchos: 0 desbordes horizontales en la publicada, 0 controles sin nombre accesible, 0 identificadores repetidos, 0 referencias ARIA rotas, 0 textos bajo 4.5:1, idioma declarado. Los botones «Editar» de la revisión miden 41 × 19 px y cumplen WCAG 2.5.8 por separación (35.5 px al objetivo más cercano). *Nota de método:* el barrido del artefacto con emulación de teléfono marcó 68 y 34 px de desborde; se debe a que el artefacto, abierto fuera de su plataforma, no trae `viewport` (A3-01), no a un defecto de diseño.
- **Teclado:** 58 a 60 paradas por pantalla en seis pantallas y dos anchos, todas con foco visible y ninguna tapada por la barra fija. (Una primera lectura marcó el campo de fecha sin foco: era la transición de 0.3 s; repetida con espera, el foco es visible.)
- **Escape de texto:** marcado inyectado en once campos por medio del borrador se muestra como texto en la revisión y en el PDF; 0 ejecuciones.
- **Doble clic en «Enviar denuncia»:** un solo número de registro (2 de 2).
- **Sin recursos externos:** la versión publicada arranca y recorre los pasos sin errores propios con todo dominio externo bloqueado.
- **Velocidad de dibujo:** carga en 94 / 368 / 550 ms y cambio de paso en 15 / 64 / 112 ms con procesador 1×, 4× y 6× más lento.
- **PDF del acuse:** título, autor, número de páginas, «Página X de Y», acentos y «ñ» correctos; nombre del archivo con el número de registro.
- **Catálogos (A2, D3):** 19 materias, 5 grupos, 7 casos de otra autoridad, 18 giros más «Otro», 1 837 colonias, 16 alcaldías, 1 624 celdas UGA (versión `sia-2026-09-22`), 31 entidades, 66 polígonos de AVA y ANP (13/26/18/9), 7 de suelo de conservación, 8 ANP coadministradas, todas presentes en la capa. Coinciden con los documentos 01 y 04.
- **Huecos deliberados:** el fundamento de «Plásticos de un solo uso» (`[Art. __, fracc. __]`, PB-09) y los tres datos del aviso de privacidad están registrados igual en DEC-228, doc 11, doc 02, P-02 y el código.
- **Apps Script del modo revisión:** palabra de acceso fuera del código, bloqueo concurrente, protección contra fórmulas (`= + - @`), límite diario, deduplicación por identificador.
- **Trato:** todo el formulario en «tú»; «usted» sólo en el aviso de privacidad (ver «Para decidir», 6). Sin «En persona», «tala», «folio», «olores» ni «antro» en pantalla.

---

## 7. Contradicciones entre documentos y datos atrasados

| # | Fuente A | Fuente B | Contradicción |
|---|---|---|---|
| 1 | 11:24 y 05:236 «criterios 2 a 7 cumplidos» | 11:34-36; 05:779; TSV renglón 24 | Criterios 5, 6 y 7 (D1-01) |
| 2 | 05:778 P-01 resuelta | prototipo:5259 acuse «depende de la naturaleza jurídica del canal» | G1-01 |
| 3 | 03:108-120 y 190 | 05:112 DEC-104; `MATERIAS` | Seis materias (D1-02) |
| 4 | 03:21-27 «la Ley no prevé a la Secretaría como receptora» | 05:246-266 P-01 opción A | D1-02 |
| 5 | 09:189-216 | `OBLIG`; DEC-120, DEC-134, DEC-193, DEC-222 | D1-03 |
| 6 | 01:40; 10:62; 19:32; 22:62; DEC-89 | DEC-226; 02:55 | D1-04 |
| 7 | 05:5 | 05:776-799 | D1-05 |
| 8 | 10:14 y prototipo:1558 «6 supuestos» | `DERIVA` (7); 11:1175 «quedan siete casos» | D1-06 |
| 9 | Prototipo y 05:109, 232 (DEC-90 a 93) | Registro de decisiones | D1-07 |
| 10 | 05:789 P-12 retirada | 05:635-644; 11:77; 12:98, 117 | D1-08 |
| 11 | 05:797 P-20 opción A | prototipo:3285 una sola casilla | D1-09 |
| 12 | 02:97 RN-17 | 02:105 RN-21 | D1-10 |
| 13 | 04:25, 65 | DEC-200, DEC-226 | D1-11 |
| 14 | 12:109 «cerca de 730 KB» | `docs/index.html` 1 016 KB | D4-01 |
| 15 | 01:49 «cierra con… la resolución de P-01 y P-02» | 05:779 P-02 en parte | D1-01 |
| 16 | 11:212 y 302 «los doce escenarios» | `ESCENARIOS` (11) | Baja, incluida en D1-13 |
| 17 | Proyecto de Claude con los documentos 21 y 23 (aviso de privacidad) | La carpeta `documentacion/` no los tiene | El doc 01:69 dice que las dos copias «se actualizan a la vez»; no se pudo comparar su contenido |

---

## 8. Para decidir (dueño)

1. **¿Cómo se acredita la versión que se congela?**
   - A. Registrar la versión firmada y enviar a la DGIVA la relación de cambios hasta la 30 para su conformidad. Costo: un oficio; S. **Recomendada.**
   - B. Declarar en una decisión nueva que los criterios 5 a 7 se dan por cumplidos con reservas, enumerándolas. Costo: S; deja la especificación sin validación formal de la regla federal (DEC-226).
2. **Presupuesto de peso y tiempo.** Propuesta: primera carga ≤ 400 KB comprimidos y ≤ 3 s hasta poder escribir en 4G lenta en un teléfono de gama baja; hoy 365 KB sin contar Leaflet, fuentes ni mosaicos. Alternativa: fijarlo hasta la fase 4, cuando las capas salgan del archivo. **Recomendación:** fijarlo ahora como criterio de la fase 4.
3. **«Atrás» del navegador.** A. Un paso por entrada del historial (M). B. Aviso antes de salir con captura en curso (S). C. Dejarlo así, apoyado en el borrador (0). **Recomendación:** A en la fase 4, por ser el gesto habitual en teléfono.
4. **Denuncia anónima: ¿para qué sirve el correo?** A. Para requerir información: corregir RN-21 y declararlo en el aviso. B. Sólo para avisos sin efecto procesal: entonces volverlo opcional, como el teléfono. **Recomendación:** A, porque la pantalla ya promete escribir al correo.
5. **Género (P-20).** A. Casilla de consentimiento expreso propia para el género y compromiso escrito del SIA de publicar la desagregación. B. Opción B de P-20: sólo rango de edad. **Recomendación:** A si el SIA asume la publicación; si no, B.
6. **Trato del aviso de privacidad.** A. Conservar «usted» por tratarse de texto legal. B. Pedir a la Unidad de Transparencia la versión en «tú». **Recomendación:** A, con la decisión registrada.
7. **P-04, concurrencia de decretos federal y local.** El código ya aplica una regla (gana el federal, con nota de concurrencia). **Recomendación:** resolver P-04 antes de escribir el catálogo de turnado de la fase 2, o registrar la regla actual como provisional en el contrato.

---

## 9. Fallas de componentes compartidos

Ninguna atribuible a un componente de otro equipo. Leaflet 1.9.4, OpenStreetMap, Nominatim, Google Fonts y Apps Script se usan como está documentado; sus límites de uso ya están registrados (doc 12, doc 20).

---

## 10. No verificable desde aquí, hipótesis, no confirmado y no aplica

**No verificable desde aquí**

| Qué | Motivo | Cómo verificarlo |
|---|---|---|
| Citas de leyes, reglamentos y normas (G1) | Sin salida a internet y sin `insumos/normativa` en la copia | Unidad jurídica, contra el texto vigente publicado en la Gaceta Oficial; prioridad: las seis materias de D1-02, los artículos de P-01 y los del aviso de privacidad |
| Comportamiento del mapa Leaflet y de la geocodificación en la versión publicada | Sin red (cdnjs, mosaicos y Nominatim bloqueados) | Prueba con red, o Leaflet servido localmente en las baterías (A1-01) |
| Lector de pantalla, axe-core, simulación de daltonismo | No instalados | NVDA o VoiceOver en los seis pasos; axe-core en las baterías |
| Firefox y WebKit | No instalados | Instalar los motores de Playwright o probar en equipos reales (H1) |
| Que la plataforma de artefactos reponga `viewport` y `format-detection` | Fuera del entorno | Abrir el artefacto publicado en iPhone |
| `.gitignore`, historial, integración continua | La copia no trae `.git` ni `.gitignore` | `git check-ignore -v _v.html construccion/pruebas/_pagina.html insumos/` |
| `validar_catalogos.py` | Requiere `shapely`, no instalado | Instalarlo en el equipo de trabajo y correrlo |
| Contenido de los documentos 21 y 23 del proyecto de Claude | No están en la copia | Comparar con la carpeta |

**Hipótesis**
- El correo de la Unidad de Transparencia que da el aviso (`smaoip@gmail.com`) es un dominio de correo gratuito; conviene confirmar que es el oficial publicado por la Secretaría antes de publicar.
- La carpeta `insumos/` (normativa y texto fuente del aviso, DEC-210) no está en el repositorio; si sólo vive en la carpeta sincronizada, el respaldo de la verificación jurídica depende de esa carpeta (riesgo de continuidad ya señalado en el doc 16 §4.3).

**No confirmado:** ninguno.

**No aplica:** B2 y D5 (sin cifras ni modelos); B9 y E2 (sin servidor ni base); F1 a F6 y H1 a H7 (otra etapa).

---

## 11. Plan de corrección en bloques cerrados

Cada bloque se abre, se cierra con su prueba y sale como versión numerada. Ninguno toca pantallas salvo los marcados.

| Bloque | Contenido | Prueba que lo cierra | Versión |
|---|---|---|---|
| **1. Cierre formal de la fase 1** (sin código) | D1-01 (versión del acta, relación de cambios, conformidad), D1-05, D1-07, D1-08, estado de DEC-89, columna de estado en la tabla de decisiones | Guion de coherencia nuevo: conteo de preguntas, secuencia de decisiones sin saltos, toda decisión citada existe, criterios contra estados de la hoja | Documentos; versión del formulario sin cambio |
| **2. Fundamento y acuse** | G1-01, B3-01, C5-01 | Batería nueva: por escenario, los pasos, el fundamento y la mención de la Procuraduría coinciden entre pantalla y PDF; ningún «entre Entre» | Versión 31 |
| **3. Documentos jurídicos y de datos** | D1-02 (con la unidad jurídica), D1-03, D1-04, D1-11, D1-13 | Guion que compare los artículos del doc 03 con `MATERIAS`, las cifras del doc 09 con `OBLIG` y que busque «provisional» junto a P-22 | Documentos |
| **4. Especificación de datos** | D2-01, D2-02, D2-03, D1-06, D1-09 y D1-10 (según «Para decidir» 4 y 5) | Pruebas: todo texto con tope en `LIMITES`; `dg` sólo con unidades receptoras; toda rama de `OBLIG` en `BIFURCACIONES`; fecha de recepción en formato ISO con zona de la Ciudad | Versión 32 (cambia pantalla si se decide la casilla de género: antes y después en apartado 11.1) |
| **5. Accesibilidad y robustez** | B4-01, B5-01, A5-01, D1-12 | Pruebas: foco dentro de la ventana al abrir y devuelto al cerrar; borrador inválido lleva a la portada con aviso; ningún constructor con obligatoriedad literal; relleno rechazado en los campos que se decidan | Versión 33 |
| **6. Limpieza** | F1-01 (mover `_v.html` a `_to_delete/` y avisar; no borrar), F1-02, A4-01, A3-01 | Batería 35 ampliada a variables locales y a comentarios con claves P- resueltas | Versión 34 |
| **7. Cobertura de la versión publicada** | A1-01, A1-02 | Baterías del paso 2 corridas también sobre `docs/index.html` con Leaflet local | Sin cambio de versión |

### 11.1 Propuestas que cambian pantalla

| Clave | Antes | Después |
|---|---|---|
| G1-01 | Acuse: «Ley Ambiental de la Ciudad de México, [Art. __, fracc. __]. Por confirmar: depende de la naturaleza jurídica del canal de recepción.» | Acuse: fundamento conforme a P-01 verificado por jurídico, más un renglón: «Si deseas una respuesta fundada y motivada en treinta días hábiles, puedes presentar además tu denuncia ante la Procuraduría Ambiental y del Ordenamiento Territorial.» (redacción a validar) |
| B3-01 | PDF, en ANP federal y en autoridad: «Personal de inspección visita el lugar…» | PDF igual a la pantalla: en ANP federal, remisión y seguimiento por la PROFEPA; en autoridad, recomendaciones del art. 331 |
| C5-01 | «entre Entre la calle Sur 20 y la calle Sur 24» | Marcador «Ej. Sur 20 y Sur 24», y el formateo no antepone «entre» si el texto ya empieza así |
| D1-09 (si se elige A) | Una casilla: consentimiento general y protesta | Segunda casilla, sólo si se contesta el género: «Consiento expresamente el tratamiento de mi género con fines estadísticos» |
| B4-01 | El foco queda detrás de la ventana | El foco va al título de la ventana y regresa al botón al cerrarla |

---

## 12. Pruebas nuevas que deben quedar permanentes

| Prueba | Serie |
|---|---|
| Coherencia documental: conteo de preguntas, secuencia y existencia de decisiones citadas, criterios contra la hoja de observaciones, «provisional» con P-22 | Cada cambio |
| Acuse: pantalla y PDF dicen lo mismo por escenario | Cada cambio |
| Longitud máxima de todo campo de texto | Cada cambio |
| Ramas de `OBLIG` presentes en `BIFURCACIONES`; conteos calculados | Cada cambio |
| Constructores sin obligatoriedad literal | Cada cambio |
| Foco de ventanas | Cada versión |
| Borrador inválido | Cada versión |
| Baterías del paso 2 sobre la versión publicada | Cada versión |
| Guiones de esta auditoría (`barrido.py`, `teclado.py`, `romperlo.py`, `cruce_vs_completas.py`, `velocidad.py`) | Antes de entregar |

---

## 13. Criterios de salida

| Momento | Criterio | Resultado |
|---|---|---|
| En cada cambio | 0 fallas | **Cumple:** 1 160 de 1 160, dos veces |
| En cada versión | 0 Críticos y 0 Altos abiertos en A y B | **Cumple** en A y B; los Altos están en D1 y G1 |
| Tras cambios grandes de interfaz | Sin Altos en C1 ni en C5 | **Cumple** en C5; C1 no se corrió |
| Antes de cerrar una etapa | Sin contradicciones abiertas; dentro del presupuesto de peso | **No cumple:** 17 contradicciones (apartado 7); no hay presupuesto |
| En documentos que van a firma | 0 citas equivocadas | **No verificable** contra el texto oficial; hay una contradicción abierta entre el doc 03 y el formulario (D1-02) |
| Antes de usar datos reales | 0 Críticos y Altos; plazo de conservación; aviso aprobado | **No cumple** (fuera de alcance): P-02 abierta, E1 sin correr |

---

## 14. Calendario

| Auditoría | Cuándo |
|---|---|
| A1 a A6 | En cada bloque de cambios (ya automatizadas en su mayoría) |
| B1, B3, B4, E3 | En cada versión numerada, con los guiones de esta auditoría |
| D1 | Al cerrar los bloques 1 a 4 y antes de entregar el contrato de la fase 2 |
| G1 | Cuando la unidad jurídica entregue el cotejo; de nuevo antes de publicar |
| D3 | Al recibir las capas completas (fase 3) |
| B8 y B4 con lector de pantalla | Antes de la prueba con personas usuarias (fase 4) |

---

## 15. Método

- **Revisores:** uno, sin revisores en paralelo (no disponibles en este entorno). Se hizo una segunda pasada propia dedicada a lo que pudo escaparse (regla 11): de ella salieron A5-01, B3-01, D1-07, D1-09 y D1-10.
- **Herramientas:** Python 3.13, Playwright con Chromium 1194 (sin interfaz), Node.js 22.22, ESLint 10.1, `pdftotext`/`pdfinfo`. Sin axe-core, lector de pantalla, Firefox, WebKit, `shapely` ni salida a internet.
- **Pantallas y anchos:** 20 pantallas y variantes (portada, pasos 1 a 7, seis escenarios, derivación, fuera de la Ciudad, formulario vacío) en 360, 390, 430, 844×390, 768, 1440 y 640×400 px (zoom 200 %): 140 mediciones por versión, sobre la publicada y sobre el artefacto. Textos: 87 pantallas. Teclado: 6 pantallas × 2 anchos. Cruce espacial: 2 077 puntos.
- **Huellas:** 84 archivos con huella SHA-256 al inicio y al final, excluyendo este informe. Resultado de la comparación: **«Sin cambios: 84 archivos idénticos»**. La auditoría no modificó ningún archivo del proyecto.
- **Línea base contra resultado final:** 1 160 comprobaciones en 35 archivos en ambas corridas, idénticas batería por batería (196 s y 195 s).
- **Evidencia y guiones:** en la carpeta de trabajo de la sesión, subcarpeta `auditoria/` (`guiones/`, `barrido-publicada.json`, `barrido-artefacto.json`, `textos-visibles.json`, `pdf/`, `pdf2/`, `linea-base-pruebas.txt`, `final-pruebas.txt`, `huellas-antes.json`, `huellas-despues.json`). Por la regla de esta auditoría no se escribieron en el proyecto; conviene copiarlos a `documentacion/evidencia-2026-10-20/` cuando se apruebe.
- **Información sensible:** el archivo `prototipo/configuracion-local.js` contiene la clave del proveedor de mapa base; no se reproduce aquí. No aparece en `docs/index.html`, en el artefacto ni en `_v.html`.

---

## 16. Qué sigue

No congelar la versión 30 como especificación todavía. Ejecutar los bloques 1 a 4 —documentos, acuse y catálogos, ninguno con código de servidor— y obtener de la DGIVA la conformidad sobre los cambios posteriores al acta. Con eso, repetir D1 y G1 (esta última con la unidad jurídica) y congelar. Los bloques 5 a 7 pueden correr en paralelo con el inicio del diccionario de datos.

---

## 17. Seguimiento de la corrección

| Bloque | Estado | Fecha | Qué se hizo |
|---|---|---|---|
| 1. Cierre formal de la fase 1 | **Hecho** | 20 oct 2026 | DEC-229: la fase 1 vuelve a «en cierre» (documentos 01 y 11). Documento 05 versión 3.1: columna «Estado» en las 229 decisiones (DEC-89 sustituida por DEC-226; DEC-228 modificada por DEC-229), DEC-90 a DEC-93 registradas y DEC-94 declarada sin asignar, DEC-101 corregida, encabezado con el conteo del registro (D1-05, D1-07). P-12 retirada con su razón y sus citas cambiadas a SIA-05 y SIA-06 del documento 20 (D1-08). Textos de P-22 alineados en los documentos 01, 02, 10, 17, 19 y 22 (D1-04). Batería 36, coherencia documental: 15 comprobaciones; total 1 175 en 36 archivos, en verde. **D1-01:** el acta se firmó sobre la Versión 30, la vigente; sin cambios posteriores que relacionar (DEC-230). Quedan abiertos los criterios 1, 6 y 7, que dependen de otras áreas |
| 2. Fundamento y acuse | **Hecho** | 20 oct 2026 | DEC-232, «Versión 31 · Validación DGIVA». **G1-01:** el acuse cita el Reglamento Interior, art. 191, fracc. XXX (DGIVA) o art. 188, fracc. XXXVIII (DGCORENADR), cotejados contra el texto vigente en `insumos/normativa/`, y en la ruta de autoridad el art. 331 de la Ley Ambiental; el fundamento está también en la pantalla; apartado «Otras vías» con la Procuraduría y la Fiscalía, salvo en la ruta federal, sin el plazo de treinta días que se proponía: DEC-138 dispone que el formulario no menciona plazos. El plazo para informar del trámite sigue abierto en P-07. Queda por confirmar con la unidad jurídica la aplicación de los artículos a cada ruta, sobre todo la federal. **B3-01:** pantalla y PDF leen una sola lista de pasos por ruta; sin visita en la ruta federal ni ante una autoridad. **C5-01:** marcador «Ej. Sur 20 y Sur 24» y una sola regla para anteponer «entre». Batería 37 nueva |
| 4. Especificación de datos | **En parte** | 20 oct 2026 | Decididos y aplicados los puntos 4 y 5 de «Para decidir»: **D1-10**, la anónima se notifica en el correo, que sigue obligatorio, y la Secretaría puede usarlo para aclarar algo sin efecto procesal (DEC-233, «Versión 32»); **D1-09**, el género se trata con la casilla general de consentimiento, sin casilla propia (DEC-234). Faltan D2-01, D2-02, D2-03 y D1-06 |
| 4. Especificación de datos | **Hecho** | 20 oct 2026 | DEC-235, «Versión 33». **D2-01:** los 32 campos de texto tienen tope en `LIMITES`, como `maxlength` y en la validación. **D2-02:** `dg` sólo DGIVA o DGCORENADR; la remisión a la PROFEPA en `remite_a`. **D2-03:** fecha de recepción en ISO 8601 con hora y zona de la Ciudad; el año del folio sale de ella. **D1-06:** 17 ramas, cada una con sus campos, y conteos calculados de los catálogos. D1-09 y D1-10, en DEC-233 y DEC-234 (renglón anterior). Batería 38 nueva |
| 3. Documentos jurídicos y de datos | **Hecho** | 20 oct 2026 | DEC-236, sin cambio de versión. **D1-02:** el documento 03 (versión 2.0) cita por materia lo mismo que `MATERIAS`, da P-01 por resuelta y dice qué se cotejó el 20 de octubre contra los textos vigentes; queda la confirmación de la unidad jurídica. **D1-03:** la parte a mano del documento 09, sin cifras ni afirmaciones viejas; la cabecera cuenta los datos de terceros. **D1-11:** documento 04 al día. **D1-13:** encabezados y conteos en 01, 02, 11, 12 y 20; P-01 deja de aparecer abierta en 12, 13, 17 y 20. Batería 39 nueva |
| 5. Accesibilidad y robustez | **Hecho** | 20 oct 2026 | DEC-237, «Versión 34». **B4-01:** foco al título de la ventana, retenido con Tab y devuelto al cerrar, en las tres ventanas. **B5-01:** un borrador dañado se descarta con aviso en la portada. **A5-01:** once constructores leen la obligatoriedad de `OBLIG` (los nueve señalados, más género y rango de edad); la batería lo prueba cambiando `OBLIG` campo por campo. **D1-12:** letras al azar rechazadas en calles, entre calles y nombre del establecimiento, sin falsos rechazos en las colonias del catálogo; los nombres de persona, fuera a propósito. Batería 40 nueva |
| 6. Limpieza | **Hecho** | 20 oct 2026 | DEC-239, sin cambio de versión. **F1-01:** `_v.html` ya no estaba en el proyecto. **F1-02:** comentarios y restos al día (correo de la anónima, aviso de privacidad, «Prefiere no decirlo», P-12, domicilio de la DGCORENADR) y lo anotado de paso en los bloques 2 y 4. **A4-01:** sin la variable `dg` sobrante; siete `catch` vacíos con su razón. **A3-01:** el artefacto conserva viewport, format-detection y nointentdetection y fija `es-MX`. Batería 35 ampliada; la 26 ya no depende de un tiempo fijo |
| 7. Cobertura de la versión publicada | **Hecho** | 21 oct 2026 | DEC-240, sin cambio de versión. **A1-01:** Leaflet 1.9.4 fijado en el proyecto, con huellas cotejadas contra cdnjs; `publicada_de_prueba.py` arma una copia de `docs/index.html` sin red, y `pruebas.py` corre sobre ella las ocho baterías del paso 2 y la 42, que exige que el mapa de Leaflet funcione y que nada salga a internet. **A1-02:** ya resuelto en DEC-231; la batería 42 lo comprueba. **Con este bloque se cierra el plan de corrección.** |
