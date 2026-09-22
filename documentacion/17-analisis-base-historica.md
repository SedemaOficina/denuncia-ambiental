# Formulario web de Denuncia Ambiental · Análisis de la base histórica de denuncias

**Versión:** 2.0 · 22 de septiembre de 2026
**Fuente:** `BASE_DE_DENUNCIAS_CIVASU_2024_2025_Y_2026` (corte al 21 de septiembre de 2026), tres hojas anuales, **2,175 registros** con asunto capturado: 689 (2024), 850 (2025), 636 (2026 al corte).

**Para qué sirve.** Es el primer insumo empírico del proyecto: hasta ahora el catálogo de materias, el de giros y el filtro de competencia se construyeron desde la norma y desde el formato vigente. Esta base dice **qué se denuncia de verdad**, en qué proporción, dónde, con qué calidad de domicilio y qué termina en incompetencia. Cada apartado cierra con la decisión de diseño que se deriva, y el documento termina con la **batería de preguntas que debe resolver la Dirección General** para que el dato sea utilizable.

**Límites del dato.** Tres, y los tres condicionan la lectura.

1. **No hay variables de tiempo ni de resultado.** La base no tiene fecha de recepción, folio, fecha de los hechos, estatus ni resolución: sólo denunciante, domicilio, asunto en texto libre, materia y tres marcas de trámite —incompetencia, reconocimiento de hechos y visita—.
2. **Las clasificaciones de este documento son aproximadas.** Las categorías por conducta y por giro se obtuvieron por coincidencia de palabras sobre el campo de asunto, no por captura estructurada; son órdenes de magnitud confiables, no cifras oficiales.
3. **Es la base de una dirección general, no de la Secretaría.** Proviene de la Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano, de la DGIVA. Las denuncias de suelo de conservación y de Áreas Naturales Protegidas corresponden a la DGCORENADR y no están aquí, o están sólo mientras se turnaban. **El apartado 8 desarrolla esta advertencia, que es la más importante del documento.**

---

## 1. Distribución por materia

| Materia (catálogo DGIVA en la base) | 2024 | 2025 | 2026 | Total | % |
|---|---:|---:|---:|---:|---:|
| Impacto ambiental | 198 | 259 | 163 | 620 | 28.5 |
| Emisiones a la atmósfera | 93 | 121 | 142 | 356 | 16.4 |
| AVA | 62 | 163 | 82 | 307 | 14.1 |
| Arbolado | 113 | 106 | 81 | 300 | 13.8 |
| Plásticos de un solo uso | 89 | 47 | 66 | 202 | 9.3 |
| Residuos sólidos | 32 | 52 | 41 | 125 | 5.7 |
| Emisiones sonoras | 62 | 33 | 25 | 120 | 5.5 |
| Aguas residuales | 23 | 46 | 28 | 97 | 4.5 |
| MAUCDMX | 17 | 23 | 8 | 48 | 2.2 |

**Cuatro materias concentran el 72.8 %** de la demanda. La base opera con nueve categorías; el formulario ofrece dieciocho. Mayor granularidad es correcta para el expediente, pero obliga a ordenar el paso 1 por volumen y no por bloque normativo.

**D-1.** Reordenar las tarjetas del paso 1 por frecuencia observada y no por bloque temático. Las cinco primeras —impacto ambiental por obra, emisiones a la atmósfera, daño a arbolado urbano, afectación a zona protegida y plásticos de un solo uso— cubren cuatro de cada cinco denuncias y deben verse sin desplazar la pantalla. Refuerza la recomendación 7 de la auditoría de UX, donde el paso 1 medía 5,409 px en teléfono.

---

## 2. El hallazgo principal: la persona denunciante no puede elegir la materia

431 denuncias mencionan derribo, tala, poda o afectación de arbolado. La DGIVA las clasificó así:

| | Arbolado | Impacto ambiental | AVA |
|---|---:|---:|---:|
| Derribo **con** obra o construcción de por medio (209) | 26 | **176** | 7 |
| Derribo **sin** obra (222) | **179** | 23 | 15 |
| Derribo dentro de barranca o zona protegida (24) | 3 | 2 | **19** |

El mismo hecho visible —un árbol derribado— se clasifica en tres materias distintas según dos circunstancias que la persona sí conoce —¿hay obra?, ¿dónde ocurre?— pero cuyo efecto jurídico no tiene por qué conocer. Pedirle que elija la materia traslada al ciudadano una decisión de competencia y garantiza una proporción alta de clasificación errónea en origen.

**D-2.** El paso 1 debe preguntar **conducta observable**, no materia. La materia se deriva de tres datos que el formulario ya captura: la conducta, el cruce espacial del punto del paso 2 y la respuesta a «¿los hechos ocurren dentro de una obra o establecimiento?». La materia derivada se muestra en el paso 6 como resultado, con la posibilidad de que la DGIVA la corrija al recibir. Es el cambio de mayor efecto sobre la calidad del turnado y no exige campos nuevos: sólo reordenar los que ya existen. Es además coherente con DEC-04, que ya fijó que la competencia la determina la ubicación y no la calificación del ciudadano.

**D-3.** Admitir **más de una conducta por denuncia**. El 12.6 % de los asuntos describe dos o más conductas —ruido, emisiones y descarga, en el mismo taller—. Hoy la captura obliga a elegir una y se pierde el resto. El formulario debe permitir marcar varias y designar una como principal, que es la que determina el turnado.

---

## 3. Incompetencia: el costo que el formulario puede evitar

| Año | Denuncias | % declaradas incompetencia |
|---|---:|---:|
| 2024 | 689 | 1.9 |
| 2025 | 850 | 10.1 |
| 2026 (al corte) | 636 | **17.8** |

Por materia, en 2026: arbolado 40.7 %, emisiones sonoras 40.0 %, residuos sólidos 26.8 %, aguas residuales 17.9 %, impacto ambiental 15.3 %, AVA 12.2 %. Plásticos de un solo uso: **0 % en los tres años**.

El aumento admite al menos tres lecturas que la base no permite distinguir: un cambio en la composición de la demanda, un criterio de registro más estricto, o que la marca esté absorbiendo también el turnado interno a la DGCORENADR. **Es la primera pregunta de la batería del apartado 12 (PB-01)**, porque de la respuesta depende todo lo que sigue. En cualquiera de las tres lecturas, una de cada seis denuncias de 2026 consumió trámite para concluir que no correspondía a esta dirección general.

Los supuestos recurrentes en las 212 incompetencias son identificables y coinciden sólo en parte con los siete supuestos de derivación del filtro vigente:

| Supuesto observado | Ejemplo textual de la base | Autoridad que corresponde | Filtro |
|---|---|---|---|
| Ruido entre particulares o vecinos | «RUIDO ENTRE VECINOS» | Juez Cívico · SSC (art. 215, fr. IV) | **Cubierto** |
| Poda o daño a arbolado en unidad habitacional | «PODA DE ÁRBOLES EN UNIDAD HABITACIONAL» | Alcaldía · régimen condominal | No cubierto |
| Arbolado y área verde en vía pública | «AFECTACIÓN DE ÁREA VERDE Y OMISIÓN DE LA ALCALDÍA» | Alcaldía | No cubierto |
| Acumulación de basura en vía pública | «ACUMULACIÓN DE BASURA EN VÍA PÚBLICA» | Alcaldía · servicios urbanos | No cubierto |
| Grasas y aceites al drenaje desde un establecimiento | «RESTAURANTE QUE TIRA LAS GRASAS AL DRENAJE» | SACMEX · INVEA | No cubierto |
| Residuos orgánicos de comercio en vía pública | «LOCALES DE VENTA DE POLLO… VÍSCERAS Y SANGRE EN LA VÍA PÚBLICA» | Alcaldía | No cubierto |
| Obra irregular sin componente ambiental acreditado | «OBRAS CONSTRUCTIVAS POR AFECTACIÓN DE ARBOLADO» | Alcaldía · INVEA | Parcial |
| Trámite que no es denuncia | «SOLICITA CAMBIO DE USO DE SUELO DEL PREDIO LA ANGOSTURA» | Ventanilla de trámites | No cubierto |

**D-4.** Ampliar los supuestos de otra autoridad del paso 1 con los seis no cubiertos y —donde el deslinde depende de una circunstancia y no de la materia— resolverlo con una pregunta de una sola línea en lugar de bloquear la tarjeta completa: «¿el árbol está dentro de una unidad habitacional o en la vía pública?», «¿la basura está en la vía pública o dentro de un predio o establecimiento?». La orientación debe ofrecer la vía concreta, no sólo el nombre de la autoridad, lo que exige resolver P-08.

**D-5.** Ningún supuesto de derivación debe impedir presentar la denuncia. El aviso orienta; si la persona insiste, la denuncia se recibe y se turna. La incompetencia se resuelve en la dirección general, no en la pantalla.

---

## 4. Plásticos de un solo uso: la materia ausente del catálogo

202 denuncias —9.3 %, cuarto lugar en volumen—, **0 % de incompetencia** y **76.7 % de visita practicada**, la tasa de conversión más alta de todas las materias. El patrón es homogéneo: comercialización o distribución de globos metalizados y bolsas de plástico en sucursales de cadena. Menciones: Walmart 15, Bodega Aurrera 13, Soriana 12, Chedraui 10.

Esta materia **no aparece** entre las dieciocho del catálogo RN-01 del formulario.

**D-6.** Incorporarla como materia propia del paso 1, con fundamento en la Ley de Residuos Sólidos de la Ciudad de México y la norma ambiental aplicable —texto por verificar, conforme al criterio de no citar disposiciones sin confirmar—, y con dos campos obligatorios para ella: **razón social o nombre de la cadena** y **sucursal**, que es lo único que la dirección general necesita para practicar la visita. Es la materia con mejor relación entre esfuerzo de captura y acto de inspección efectivo; dejarla fuera pierde una de cada diez denuncias.

---

## 5. Tipo de fuente: catálogo empírico de giros

El catálogo de diecinueve giros del paso 2 es provisional, y su sustitución está registrada como pendiente en `08-normativa-por-integrar`. La base permite fundarlo:

| Tipo de fuente mencionado en el asunto | n | % del total | % incompetencia |
|---|---:|---:|---:|
| Obra o construcción | 507 | 23.3 | 7.5 |
| Barranca, ANP, AVA o área verde | 355 | 16.3 | 7.3 |
| Fábrica o industria —incluye imprenta, carpintería, herrería, textil | 152 | 7.0 | 5.9 |
| Predio baldío, invasión o asentamiento | 134 | 6.2 | 14.2 |
| Comercio, sucursal o cadena | 125 | 5.7 | 4.0 |
| Restaurante, bar o comercio de alimentos | 101 | 4.6 | 9.9 |
| Taller mecánico, hojalatería y pintura, vulcanizadora, verificentro | 100 | 4.6 | 10.0 |
| Evento, fiesta o actividad en vía pública | 70 | 3.2 | 28.6 |
| Vivienda, unidad habitacional o vecino | 45 | 2.1 | **35.6** |
| Centro de reciclaje, acopio o chatarrera | 22 | 1.0 | 13.6 |

**D-7.** Sustituir el catálogo provisional por estos diez giros más «otro», ordenados por frecuencia. «Taller de hojalatería y pintura» debe ser una opción propia y no quedar dentro de «taller mecánico»: aparece asociada de manera sistemática a emisiones y a descargas, y define qué se inspecciona. La sustitución definitiva sigue condicionada al padrón de fuentes fijas (PB-08).

**D-8.** Los dos giros con mayor tasa de incompetencia —vivienda o unidad habitacional, 35.6 %, y evento en vía pública, 28.6 %— deben disparar la orientación de competencia en el momento de elegirlos, no al final del recorrido.

---

## 6. Calidad del domicilio: el punto en el mapa queda validado

| Situación en el campo de domicilio | n | % |
|---|---:|---:|
| Domicilio alterno —«y/o», dos direcciones posibles | 197 | 9.1 |
| Sólo calle, sin número | 178 | 8.2 |
| Colonia vacía | 142 | 6.5 |
| Referencia vaga —«frente a», «esquina», «entre», «a la altura» | 135 | 6.2 |
| Manzana y lote en vez de calle y número | 127 | 5.8 |
| Coordenadas geográficas incluidas | 66 | 3.0 |

Casi tres de cada diez domicilios no permiten llegar al sitio por sí solos, y sólo el 3 % trae coordenada. Es el respaldo empírico de construir la ubicación desde el punto en el mapa —con apoyo del artículo 282, segundo párrafo, de la Ley Ambiental— y de la ruta «el lugar no tiene calle ni número» adoptada en DEC-47, que atiende al 16.3 % de los casos que ocurren en barrancas, áreas verdes y predios sin domicilio.

**D-9.** Añadir **manzana y lote** como par de campos opcionales en el paso 2: el 5.8 % de los sitios se identifica así y hoy se captura dentro del campo de calle, lo que rompe la dirección en el expediente.

**D-10.** Mantener «entre calle 1» y «entre calle 2» como campos opcionales permanentes —el 6.2 % de los domicilios se describe con referencias— y no sólo en la ruta sin domicilio.

---

## 7. Territorio y sitios recurrentes

Seis alcaldías concentran el 63.2 % de las denuncias: Cuauhtémoc 14.3 %, Álvaro Obregón 12.8 %, Benito Juárez 11.2 %, Coyoacán 9.4 %, Miguel Hidalgo 8.2 %, Iztapalapa 7.3 %.

Las barrancas con denuncia reiterada son identificables por nombre: Cerro Zacatepetl 52 menciones, Tarango 28, Jalalpa 23, Anzaldo 18, Santa Rita 16, Echanove 15, Texcalatlaco 12, Mixcoac 10, El Moral 8, Guadalupe 7.

**D-11.** La propuesta de «nombre del lugar» desde la capa oficial debe priorizar estas barrancas y las AVA declaradas: son el 16 % de la demanda y hoy se capturan como texto libre con grafías inconsistentes.

**D-12.** Detección de duplicados por proximidad. Con texto libre sólo el 4.4 % de las denuncias cae en un domicilio ya denunciado, cifra subestimada por las variantes de escritura. Con coordenada, el sistema puede advertir al recibir —«ya existe una denuncia a menos de 50 m en esta materia»— y ofrecer sumarse al expediente existente en vez de abrir uno nuevo. Alimenta el control 4 del documento 15 y la parte abierta de P-21.

---

## 8. Suelo de conservación y Áreas Naturales Protegidas: la competencia de la DGCORENADR

Es el apartado con mayor consecuencia sobre cómo debe leerse todo lo anterior, y responde a una pregunta directa: **qué pasa con las denuncias que llegan y no son de esta dirección general porque los hechos ocurren en suelo de conservación o en un Área Natural Protegida.**

### 8.1 El reparto, que ya está resuelto en la norma

No es una zona gris. El Reglamento Interior lo reparte y el Manual Administrativo lo confirma, como quedó asentado en DEC-30 y DEC-84:

| Ámbito territorial | Unidad competente | Fundamento |
|---|---|---|
| Suelo urbano y Áreas de Valor Ambiental | DGIVA · Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano | Art. 191, fr. III y XVI, del Reglamento Interior |
| Suelo de conservación y Áreas Naturales Protegidas locales | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas | Art. 188, fr. XXXVIII a XLI |
| Áreas Naturales Protegidas federales, con y sin convenio | PROFEPA, de manera provisional | DEC-89, a consulta en P-22 |

La consecuencia práctica: **una barranca es AVA y por tanto es DGIVA; un ANP local o el suelo de conservación no lo son**. Esa distinción —que el ciudadano no puede hacer y el mapa sí— es la que el formulario ya resuelve por cruce espacial desde DEC-04, y la que DEC-72 blindó al suprimir la alcaldía capturada en favor de la del punto.

### 8.2 Lo que la base revela: esas denuncias casi no existen aquí

La base confirma el reparto por la vía de la ausencia. Las conductas características del suelo de conservación **no tienen volumen en ella**:

| Conducta propia del suelo de conservación | Menciones en 2,175 registros |
|---|---:|
| Terráceos, despalme o remoción de cubierta vegetal | **0** |
| Uso de agroquímicos prohibidos | **0** |
| Chinampa, ejido o parcela | **1** |
| Asentamiento irregular | 13 |
| Invasión de predio | 28 |
| Tala o desmonte | 49 |
| Mención expresa de «suelo de conservación» | 17 |

Y las tres alcaldías cuyo territorio es mayoritaria o íntegramente suelo de conservación aportan 94 denuncias de 2,175 —el 4.3 %—:

| Alcaldía | 2024 | 2025 | 2026 | Total | % del total | Incompetencia |
|---|---:|---:|---:|---:|---:|---:|
| Xochimilco | 17 | 12 | 30 | 59 | 2.7 | 16.9 % |
| Tláhuac | 5 | 15 | 10 | 30 | 1.4 | 23.3 % |
| Milpa Alta | 5 | 0 | 0 | **5** | **0.2** | 0 % |

**Milpa Alta, que es la alcaldía con mayor proporción de suelo de conservación de la Ciudad, aporta cinco denuncias en tres años y ninguna desde 2024.** No es que no haya afectación ambiental en Milpa Alta: es que esta base no la ve.

En cambio, la AVA —que sí es competencia de la DGIVA— aparece con 307 registros, 14.1 % del total, concentrada en Álvaro Obregón (129), Cuajimalpa (55), Coyoacán (52) y Magdalena Contreras (36), y con la **tasa de incompetencia más baja de todas las materias: 4.4 % entre las que mencionan barranca**. El reparto funciona: lo que es AVA se queda y se atiende.

Lo que sí llega y no se queda son los casos de ANP. Los 64 registros que mencionan un ANP por su nombre —Desierto de los Leones, Sierra de Guadalupe, Cerro de la Estrella, Bosque de Tlalpan, Ajusco— tienen una tasa de incompetencia del **20.3 %, más del doble de la general**, y creciente: 0 % en 2024, 21.1 % en 2025, 35.7 % en 2026.

### 8.3 La pregunta que esto abre, y que no puede responderse desde el dato

El campo «INCOMPETENCIA» de la base no distingue entre dos cosas jurídicamente distintas:

1. **Incompetencia de la Secretaría**: los hechos corresponden a la alcaldía, al SACMEX, al INVEA o a la PROFEPA. La denuncia sale de la Secretaría.
2. **Turnado interno a la DGCORENADR**: los hechos son ambientales y son de la Secretaría; sólo los atiende otra dirección general. La denuncia **no sale**, se mueve.

Si la marca absorbe ambos fenómenos, el 17.8 % de 2026 mezcla un problema real de captación con un simple movimiento interno, y la lectura del apartado 3 cambia de sentido. **Es PB-01 de la batería, y la primera que debe contestarse.**

Hay evidencia textual de que el segundo caso ocurre y se descubre tarde. Un asunto de la base lo dice con todas sus letras: *«SOLICITA VISITA A CONSTRUCCIÓN POR DERRIBO DE ARBOLADO, PERO SE ENCUENTRA EN SUELO DE CONSERVACIÓN»*. La condición territorial se advirtió **después** de capturar la denuncia, que es exactamente lo que el cruce espacial del formulario evita al colocar el punto antes de preguntar nada más.

### 8.4 Lo que el formulario ya resuelve, y lo que le falta

**Ya resuelto.** El formulario determina la unidad competente por cruce espacial (DEC-04), la nombra al nivel de dirección general con fundamento reglamentario (DEC-30), muestra el resultado en la ficha bajo el mapa (DEC-18), lo refleja en el acuse, y admite la captura de sitios sin domicilio, que es la situación normal en suelo de conservación (DEC-47). El escenario «Tala en suelo de conservación, anónima» ya recorre esa rama completa. En esto el prototipo está por delante de la práctica que la base documenta.

**Lo que falta, y que la base hace visible:**

**D-13 · Constancia del turnado, con su plazo.** El Manual Administrativo fija **tres días hábiles para recibir y turnar**. El sistema debe registrar la fecha y hora del turnado a la DGCORENADR, generar la constancia y contar ese plazo. Hoy el turnado es una etiqueta en el acuse, no un acto con fecha y acuse de recibo. Sin eso, la denuncia que cambia de dirección general pierde trazabilidad justo en el punto donde más fácil se extravía.

**D-14 · El acuse debe decir a dónde acudir, no sólo quién atiende.** Cuando la denuncia se turna a la DGCORENADR, el acuse y el pie deben mostrar el domicilio, horario y teléfono de esa unidad, no la dirección genérica de la Secretaría. Depende de P-09, hoy abierta y con dos domicilios institucionales contradictorios.

**D-15 · Regla para hechos que abarcan dos tipos de suelo.** El caso es frecuente: una obra en suelo urbano que descarga o deposita en la barranca colindante; un predio a caballo sobre el límite. El punto manda, conforme a DEC-72, pero debe existir una regla expresa: **se turna a la unidad del punto y se da vista a la otra**, dejando constancia de la colindancia en el expediente. Sin regla escrita, el caso se resuelve por criterio de quien captura, que es la situación que la base refleja.

**D-16 · Conservar en el catálogo las conductas de suelo de conservación aunque no tengan volumen aquí.** Terráceos, remoción de cubierta vegetal, agroquímicos y afectación a cuerpo de agua tienen cero o casi cero menciones en esta base. **Esa ausencia no mide la realidad, mide el canal.** El bloque de zonas de protección abierto en DEC-23 debe conservarse íntegro: retirarlo por falta de volumen sería confundir lo que no llega con lo que no ocurre.

**D-17 · Folio único con segmento de área.** Alimenta P-13. El consecutivo debe ser único para la Secretaría, con un segmento que identifique la unidad que atiende, de modo que una denuncia turnada conserve su folio y la persona pueda seguirla con el mismo número aunque cambie de dirección general. Un consecutivo segmentado por área obligaría a reexpedir folio al turnar, que es la forma más segura de perder el seguimiento ciudadano prometido en AD-02.

**D-18 · Medir la captación en suelo de conservación como indicador propio.** Con línea base en esta serie: 4.3 % de las denuncias en las tres alcaldías de suelo de conservación, 0.2 % en Milpa Alta. Si el formulario funciona, esa proporción debe subir. Es el indicador que mide si el canal alcanzó a la mitad del territorio que hoy no lo usa.

### 8.5 Lo que debe convenirse con la DGCORENADR antes de publicar

El formulario recibe por las dos direcciones generales, pero **la DGCORENADR no ha participado en su diseño** y su procedimiento tiene plazos propios —noventa días hábiles, frente a noventa y tres en suelo urbano, según DEC-84—. Tres cosas deben quedar convenidas: que acepta recibir por este canal y no por uno propio, quién opera su bandeja en AD-01, y qué estados registra para que AD-02 pueda mostrarlos. Están recogidas como PB-09 a PB-11.

---

## 9. Quién denuncia

| Tipo de denunciante | 2024 | 2025 | 2026 | Total |
|---|---:|---:|---:|---:|
| Con título profesional en el nombre | 426 | 169 | 225 | 820 |
| Nombre simple, sin cargo ni título | 165 | 406 | 246 | 817 |
| «No aplica» o sin denunciante | 58 | 214 | 101 | 373 |
| Persona servidora pública con cargo explícito | 40 | 61 | 64 | 165 |

Cinco nombres concentran 602 registros —el 27.7 % del total—, todos con título o cargo. La lectura más probable es que no sean denunciantes finales sino **servidores públicos que turnan** denuncias captadas por otra vía; la base no permite confirmarlo y debe verificarse antes de afirmarlo en ningún documento institucional (PB-04).

Si se confirma, tiene dos consecuencias de diseño. La primera: el volumen que hoy registra la base no proviene de captación ciudadana directa, de modo que el formulario web no sustituye un canal saturado sino que abre uno nuevo, y su meta debe medirse como denuncia ciudadana incorporada, no como sustitución. La segunda: hace falta una **vía de captura institucional** —misma estructura de datos, con campo de dependencia que turna y de folio de origen— para que el turno no se capture como si fuera una denuncia ciudadana anónima.

**D-19.** Incorporar el campo **origen de la denuncia** —ciudadana directa, turno de otra autoridad, oficio, medio de comunicación— al modelo de datos. Sin él, la estadística del nuevo canal no es comparable con la serie histórica.

---

## 10. Lo que la base no registra y el sistema debe registrar

La base carece de fecha de recepción, fecha de los hechos, folio, estatus, fecha de visita y sentido de la resolución. Sin esos campos no puede medirse tiempo de atención, no puede verificarse el cumplimiento de los plazos del Manual Administrativo ni computarse el del artículo 22 BIS 2, y no puede evaluarse el desempeño del canal.

**D-20.** El modelo de datos del formulario debe devolver a las dos direcciones generales, además de lo que hoy captura: folio, fecha y hora de recepción, fecha de los hechos, materia derivada y materia confirmada, unidad que atiende por cruce espacial, fecha de turnado, estatus, fecha de visita y sentido de la resolución. Es la condición para que la base de 2027 sí permita el análisis que ésta no permitió.

---

## 11. Resumen de decisiones derivadas, y qué se hizo con cada una

**Estado al 22 de septiembre de 2026.** «Aplicada» significa que está en el prototipo y sujeta por una comprobación automática; «ya estaba» que el prototipo la resolvía antes de este análisis y la verificación lo confirmó; «variante» que se construye en el panel de validación para que la Dirección General decida viéndola; «espera» que depende de una respuesta de la batería del apartado 12.

| Clave | Decisión | Paso | Estado |
|---|---|---|---|
| D-1 | Ordenar las materias por frecuencia observada | 1 | **Aplicada** · DEC-108. El supuesto más denunciado pasa de 2,363 px a 672 px en teléfono |
| D-2 | Preguntar conducta, derivar materia | 1–2 | Variante · es el cambio de mayor efecto y el más difícil de explicar por escrito |
| D-3 | Admitir varias conductas con una principal | 1 | Variante · cambia el modelo de datos, depende de PB-10 |
| D-4 | Ampliar los supuestos de derivación con seis casos observados | 1 | Espera · los seis exigen verificación jurídica y los datos de contacto de P-08. **Lo que sí puede hacerse ya** son las dos preguntas que discriminan la circunstancia, que no derivan a nadie |
| D-5 | La derivación orienta, no bloquea | 1 | Variante · contradice cómo opera hoy RN-02 y aumenta el volumen de incompetencia: lo decide quien lo atiende |
| D-6 | Incorporar plásticos de un solo uso como materia | 1 | **Aplicada** · DEC-109, con el fundamento como hueco visible |
| D-7 | Catálogo de giros fundado en la base | 2 | Espera · el catálogo provisional puede reordenarse por frecuencia desde ya; la sustitución definitiva depende de PB-08 |
| D-8 | Orientación temprana en los dos giros de mayor incompetencia | 2 | Variante · va con D-5 |
| D-9 | Campos de manzana y lote | 2 | **Aplicada** · DEC-110 |
| D-10 | Entre calles como campo permanente | 2 | **Ya estaba**, y mejor resuelto: DEC-90 fundió los dos campos del formato de papel en uno solo, porque nadie dice «entre calle 1» |
| D-11 | Priorizar barrancas y AVA en el nombre del lugar | 2 | **Ya estaba**: `consultaCapas()` tiene la precedencia declarada y el nombre se propone desde la capa que contiene el punto |
| D-12 | Aviso de denuncia previa por proximidad | 2 | Espera · es servidor, fase 2 |
| D-13 | Constancia de turnado con fecha y plazo de tres días | Modelo | Espera · PB-11 y PB-13 |
| D-14 | El acuse muestra el domicilio de la unidad que atiende | Acuse | Espera · P-09 |
| D-15 | Regla escrita para hechos en dos tipos de suelo | Turnado | Espera · PB-16 |
| D-16 | Conservar las conductas de suelo de conservación en el catálogo | 1 | **Aplicada** como acuerdo de no retirarlas: anotada en el código junto a la estructura que las ordena, y sujeta por una comprobación |
| D-17 | Folio único con segmento de área | Modelo | Espera · P-13 y PB-18 |
| D-18 | Indicador de captación en suelo de conservación | Tablero | Espera · fase 5 |
| D-19 | Campo de origen de la denuncia | Modelo | Espera · PB-04 |
| D-20 | Devolver folio, fechas, unidad, estatus y resolución | Modelo | Espera · PB-03 |

---

## 12. Batería de preguntas para la Dirección General

Veinte preguntas en cuatro bloques. Cada una indica **por qué importa**, **qué muestra la base**, el **formato de respuesta** esperado —cerrado siempre que es posible, para que se resuelva en sesión— y **a qué alimenta** del expediente del proyecto. Las que se responden con un documento o un archivo lo señalan.

Las preguntas del documento 05 —P-01 a P-22— siguen abiertas y son de otra naturaleza: resuelven el diseño jurídico del instrumento. Éstas resuelven el uso del dato histórico y la relación con la DGCORENADR. Donde una alimenta a otra, se indica.

### Bloque A · Para poder leer la base

**PB-01. ¿La marca «INCOMPETENCIA» incluye el turnado interno a la DGCORENADR, o sólo la incompetencia de la Secretaría frente a otras autoridades?**
*Por qué importa.* Son dos fenómenos distintos —uno saca la denuncia de la Secretaría, el otro sólo la mueve de dirección general— y hoy comparten una sola marca. De la respuesta depende si el 17.8 % de 2026 mide un problema de captación o un movimiento interno normal.
*Qué muestra la base.* Los registros que mencionan un ANP por su nombre tienen 20.3 % de incompetencia frente al 9.7 % general, y suben de 0 % en 2024 a 35.7 % en 2026.
*Formato.* A · sólo incompetencia externa. B · incluye el turnado interno. C · depende de quién captura.
*Alimenta.* La lectura completa del apartado 3 y de D-13.

**PB-02. ¿A qué se debe el aumento de la incompetencia de 1.9 % a 17.8 % en tres años?**
*Formato.* A · cambio de criterio de registro, con la fecha en que cambió. B · cambio real en la composición de la demanda. C · efecto de PB-01. D · se desconoce.
*Alimenta.* D-4 y la línea base de cualquier meta de reducción.

**PB-03. ¿Es posible obtener la misma base con fecha de recepción, folio y sentido de la resolución?**
*Por qué importa.* Sin fecha no hay estacionalidad, no hay tiempo de atención y no hay evaluación del canal. Sin resolución no se sabe qué pasó con la denuncia.
*Formato.* Archivo, con indicación de qué campos existen en el sistema de origen aunque no se hayan entregado.
*Alimenta.* D-20 y el tablero de AD-01.

**PB-04. ¿Quiénes son los cinco denunciantes que concentran el 27.7 % de los registros?**
*Por qué importa.* Si son servidores públicos que turnan y no denunciantes finales, el volumen histórico no mide captación ciudadana y la meta del formulario debe plantearse de otro modo.
*Formato.* A · denunciantes ciudadanos recurrentes. B · servidores públicos que turnan, indicando de qué instancia. C · personal de la propia Coordinación que captura.
*Alimenta.* D-19 y el apartado 9.

**PB-05. ¿Existe una base equivalente de la DGCORENADR para suelo de conservación y Áreas Naturales Protegidas?**
*Por qué importa.* Esta base cubre la mitad urbana de lo que la Secretaría atiende. Sin la otra mitad no hay diagnóstico de la denuncia ambiental en la Ciudad, y el catálogo del paso 1 se estaría dimensionando sobre medio universo.
*Formato.* Archivo, o la indicación de a quién solicitarlo.
*Alimenta.* Los apartados 1, 5 y 8, y D-16.

### Bloque B · Clasificación y catálogo

**PB-06. ¿Cuál es el catálogo vigente de materias con el que se captura, y por qué la base opera con nueve categorías y el formato vigente con otras?**
*Formato.* Documento o pantalla del sistema de captura.
*Alimenta.* RN-01 y el reordenamiento de D-1.

**PB-07. ¿Con qué criterio se distingue «arbolado» de «impacto ambiental» cuando el derribo ocurre dentro de una obra?**
*Por qué importa.* Es el hallazgo del apartado 2: la base muestra que el criterio existe y es consistente —con obra, impacto ambiental en 176 de 209 casos; sin obra, arbolado en 179 de 222—, pero no está escrito. Escribirlo permite que lo aplique el sistema y no la persona que captura.
*Formato.* Regla redactada en una frase, con el supuesto de excepción si lo hay.
*Alimenta.* D-2, que es el cambio de mayor efecto del documento.

**PB-08. ¿Existe padrón de fuentes fijas o catálogo oficial de giros?**
*Por qué importa.* El catálogo de diecinueve giros del paso 2 es provisional. La base permite fundarlo con evidencia, pero un padrón oficial permite además cruzar la denuncia con las licencias y las autorizaciones existentes.
*Formato.* Archivo o sistema de consulta.
*Alimenta.* D-7 y el pendiente registrado en el documento 08.

**PB-09. ¿Se incorpora «plásticos de un solo uso» como materia del formulario, y con qué fundamento vigente?**
*Por qué importa.* Es el 9.3 % de la demanda, con 0 % de incompetencia y la mejor tasa de visita, y no está en las dieciocho materias del catálogo.
*Formato.* A · sí, con el artículo y la norma que deben citarse. B · no, indicando por qué se captura entonces en la base.
*Alimenta.* D-6.

**PB-10. ¿Se admite que una denuncia declare más de una conducta?**
*Formato.* A · sí, con una principal que determina el turnado. B · no, se conserva una sola materia.
*Alimenta.* D-3 y el modelo de datos.

### Bloque C · Denuncias de suelo de conservación y Áreas Naturales Protegidas

**PB-11. ¿Qué hace hoy la Coordinación cuando recibe una denuncia cuyos hechos ocurren en suelo de conservación o en un ANP local?**
*Por qué importa.* Es la pregunta de proceso de la que dependen D-13 a D-15. La norma dice quién es competente; falta saber qué ocurre en la práctica.
*Formato.* Describir la secuencia real: quién advierte la condición territorial, en qué momento, con qué documento se turna, quién acusa recibo y qué se le informa a la persona denunciante.
*Alimenta.* D-13 y D-15.

**PB-12. ¿En qué momento del trámite se advierte que el sitio está en suelo de conservación o en un ANP?**
*Por qué importa.* La base contiene un asunto que lo dice expresamente —«solicita visita a construcción por derribo de arbolado, pero se encuentra en suelo de conservación»—: la condición se advirtió después de capturar. El formulario la resuelve antes de preguntar nada más, pero sólo si el punto se coloca con precisión.
*Formato.* A · al capturar, por conocimiento del personal. B · al analizar la competencia, dentro de los diez días hábiles. C · al llegar al sitio.
*Alimenta.* D-15 y el diseño del paso 2.

**PB-13. ¿Cuántas denuncias se turnaron a la DGCORENADR en 2024, 2025 y 2026?**
*Por qué importa.* Es la cifra que esta base no permite obtener y que da la magnitud real del flujo entre direcciones generales.
*Formato.* Cifra anual, y si es posible el listado.
*Alimenta.* D-13 y D-18.

**PB-14. ¿La DGCORENADR acepta recibir denuncias por este formulario, o mantiene un canal propio?**
*Por qué importa.* Si mantiene canal propio, el formulario crea una doble entrada para el mismo hecho y el ciudadano no sabrá cuál usar. Si acepta, debe participar en la validación antes de publicar, porque sus plazos y su procedimiento son distintos.
*Formato.* A · recibe por este canal. B · mantiene canal propio. C · ambos, con criterio de reparto.
*Alimenta.* La condición de publicación del formulario y el alcance de AD-01.

**PB-15. ¿Quién opera la bandeja de la DGCORENADR en el módulo de administración, y qué estados registra?**
*Por qué importa.* AD-02 sólo puede mostrar a la ciudadanía estados que alguien registre efectivamente. Si la unidad que atiende la mitad del territorio no captura, el seguimiento ciudadano falla justo ahí.
*Formato.* Unidad responsable, perfil y catálogo de estados.
*Alimenta.* AD-01, AD-02 y P-14.

**PB-16. ¿Cuál es la regla cuando los hechos abarcan suelo urbano y suelo de conservación a la vez?**
*Por qué importa.* Una obra en suelo urbano que deposita en la barranca colindante, o un predio sobre el límite. El punto manda conforme a DEC-72, pero la vista a la otra unidad no está escrita.
*Formato.* A · turna la unidad del punto, con vista a la otra. B · conocen ambas, con expedientes separados. C · se resuelve caso por caso.
*Alimenta.* D-15 y RN-04.

### Bloque D · Operación y destino del dato

**PB-17. ¿En cuántos días se responde a quien pregunta por su folio?**
*Por qué importa.* El Manual Administrativo fija los plazos del procedimiento, no el de informar a la persona denunciante, y el acuse promete informar. Es la parte que quedó abierta de P-07.
*Formato.* Número de días hábiles, o la decisión de no comprometer plazo y redactar el acuse sin generar expectativa.
*Alimenta.* P-07, el acuse y AD-02.

**PB-18. ¿El folio es único para la Secretaría o se segmenta por dirección general?**
*Por qué importa.* Si se segmenta, la denuncia turnada cambia de folio y el seguimiento ciudadano se rompe en el peor momento.
*Formato.* A · único con segmento de área. B · consecutivo por dirección general. C · por definir.
*Alimenta.* P-13 y D-17.

**PB-19. ¿Se conserva el teléfono como dato obligatorio?**
*Por qué importa.* Es P-17, aún sin responder, y condiciona el cierre del esquema de obligatoriedad. La base no aporta evidencia sobre este punto: se incluye porque bloquea.
*Formato.* A · obligatorio. B · opcional.
*Alimenta.* P-17 y el documento 09.

**PB-20. ¿Quién publica la estadística de denuncias y con qué periodicidad?**
*Por qué importa.* Un dato que nadie explota no se pide. Aplica tanto a las variables de operación como a las de género y rango de edad, cuya conservación en el formulario quedó condicionada en P-20 a que exista quien publique la desagregación.
*Formato.* Unidad responsable y periodicidad, o la decisión de no publicar.
*Alimenta.* P-20 y el tablero de AD-01.

---

### Cómo conviene resolverlas

Las del **bloque A** son las primeras: sin PB-01 no se sabe qué mide la cifra de incompetencia, y sin PB-03 y PB-05 el diagnóstico sigue incompleto. Pueden resolverse en una sola sesión con la Coordinación, salvo las que requieren archivo.

Las del **bloque C** exigen una reunión con la DGCORENADR, no con la DGIVA. Conviene convocarla antes de cerrar el catálogo del paso 1: si esa dirección general va a recibir por este canal, tiene que haber visto el formulario antes de que se publique, y no después.

Las del **bloque B** y **D** pueden resolverse por escrito, salvo PB-07, que conviene trabajar en sesión porque lo que se pide no es un dato sino la redacción de una regla que hoy existe sólo en la práctica de quien captura.
