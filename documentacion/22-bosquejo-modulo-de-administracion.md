# Formulario web de Denuncia Ambiental · Bosquejo del módulo de administración y seguimiento

**Versión:** 0.14 · 21 de octubre de 2026 · al día con las decisiones hasta DEC-255
**Estado:** bosquejo para discusión. **No abre la construcción del módulo.**
**Para qué sirve este documento.** Reúne en un solo lugar lo que tendría que tener el módulo interno de la Secretaría —captura por personal (AD-03), bandeja, expediente, tablero y administración (AD-01)—, para llegar a la fase 5 con el módulo ya pensado y acordado con las áreas. Desarrolla lo que el documento 05 dejó enunciado en la Parte V y lo que el documento 20 lista como SIA-23 a SIA-29.

**Regla que este bosquejo respeta.** DEC-19 y DEC-32 pedían no abrir ningún módulo antes del acta de validación del formulario; el acta se firmó sobre la «Versión 30» (DEC-230), y esa condición ya se cumplió. Sigue vigente la ruta de trabajo (documento 11): el módulo se **construye** en la fase 5, sobre el contrato de datos de la fase 2, y **no se programa nada que guarde datos mientras el diccionario de datos no esté cerrado** (documento 11, §6). Bosquejar y hacer una maqueta navegable con datos ficticios, que no guarda nada, no contradicen esa regla. Lo que dependa del catálogo de estados (P-14) o del diccionario se da como propuesta hasta que se acuerden.

---

## Qué cambió en esta versión

**De la 0.13 a la 0.14** (el pase de diseño, DEC-255): el apartado 9 suma el paso 5, el pase de diseño de la maqueta, después de la sesión con las áreas; la construcción pasa a ser el paso 6.

**De la 0.12 a la 0.13** (la evidencia sin datos del sistema, DEC-254): el apartado 3.3 deja sólo el nombre y el tipo de cada archivo.

**De la 0.11 a la 0.12** (la evidencia, fácil de revisar, DEC-253): el apartado 3.3 dice cómo se ve la evidencia en el expediente.

**De la 0.10 a la 0.11** (cada coordinación da de alta a su personal, DEC-252): el apartado 2 dice quién da de alta a quién, y el 3.9, nuevo, describe la pantalla «Personal».

**De la 0.9 a la 0.10** (el tablero se lleva por año, DEC-251): el apartado 5 filtra por año y mes, separa suelo de conservación, Áreas Naturales Protegidas y Áreas de Valor Ambiental, y ya no lleva los sitios con denuncia reiterada; el 3.5 dice que el mapa también se filtra por año.

**De la 0.8 a la 0.9** (búsqueda, exportación y administración, DEC-249): los apartados 3.7 y 3.8 dicen lo que propone la maqueta, y el paso 2 del apartado 9 está hecho.

**De la 0.7 a la 0.8** (captura por personal, DEC-248): el apartado 3.4 dice cómo quedó el modo captura del formulario, y el paso 3 del apartado 9 está hecho.

**De la 0.6 a la 0.7** (mapa de la maqueta, DEC-247): el apartado 3.5 dice cómo dibuja la maqueta el mapa operativo.

**De la 0.5 a la 0.6** (tablero de la maqueta, DEC-246): el apartado 5 dice cómo cuenta la maqueta cada indicador.

**De la 0.4 a la 0.5** (Inicio de la maqueta, DEC-245): el apartado 3.1 dice qué listas ve cada perfil.

**De la 0.3 a la 0.4** (expediente de la maqueta, DEC-244): el apartado 3.3 dice lo que la maqueta propone para el expediente.

**De la 0.2 a la 0.3** (bandeja de la maqueta, DEC-243): el apartado 3.2 dice lo que la maqueta propone para la bandeja y el 10 suma MA-13. La tabla que sigue es el cambio de la 0.1 a la 0.2.

| Apartado | Antes (versión 0.1, 5 de octubre) | Ahora |
|---|---|---|
| Regla | No se bosquejaba más allá del acta, que no existía | El acta está firmada (DEC-230); la construcción sigue en la fase 5 y la persistencia espera al diccionario |
| 3.2 Bandeja | «Área que atiende» con un valor «federal» | Área que **recibe** —DGIVA o DGCORENADR— y, aparte, la **remisión** a la PROFEPA (DEC-235) |
| 3.2 y 3.3 | La anónima, «con correo de contacto» | La anónima **se notifica en su correo** (DEC-233); el expediente registra la notificación |
| 3.3 Expediente | — | Muestra el fundamento que citó el acuse (DEC-232) y la fecha de recepción en hora de la Ciudad (DEC-235) |
| 4 Ciclo | Sin estado de notificación | Estado **Notificada**, por domicilio o por correo |
| 5 Tablero | Género y edad «condicionado a P-20» | P-20 resuelta (DEC-225, DEC-234); indicador de notificaciones por correo |
| 6 Datos | — | Notificación, área y remisión, y la longitud de cada campo desde `LIMITES` (DEC-235) |
| 7 Protección de datos | — | Género como dato sensible (DEC-234) y correo de la anónima como única vía de contacto |
| 8 Qué no entra | «Avisos por correo: no hay servicio de envío» | **Sí entra** la notificación por correo de la anónima (DEC-233, SIA-29); siguen fuera los avisos automáticos a quien da sus datos |
| 9 Orden | Maqueta «con la reserva de que los campos pueden cambiar tras la revisión» | Maqueta posible ya, sin guardar datos; los campos son los de la versión validada y sus cambios posteriores (DEC-232 a DEC-241) |

---

## 1. Qué problema resuelve

El formulario termina en el acuse. Lo que ocurre después hoy vive en una hoja de cálculo que, según el análisis de la base histórica (documento 17), **no registra fecha de recepción, folio, estatus, fecha de visita ni sentido de la resolución**. De ahí cuatro carencias que el módulo debe cerrar:

| Carencia observada | Evidencia | Qué debe hacer el módulo |
|---|---|---|
| No puede medirse el tiempo de atención ni el cumplimiento de plazos | La base no tiene fechas (documento 17, apartado 10) | Fechar cada cambio de estado y contar los plazos del Manual Administrativo |
| La marca de incompetencia mezcla dos fenómenos | 17.8 % en 2026, sin distinguir salida de la Secretaría y turnado interno (PB-01) | Registrar por separado «remitida a otra autoridad» y «returnada a otra dirección general» |
| El volumen histórico no llega por un solo canal | 27.7 % de los registros parece turnado por servidores públicos (PB-04) | Captura por personal con canal y origen, antes que el tablero (DEC-154) |
| La mitad del territorio no aparece | 4.3 % de las denuncias en las tres alcaldías de suelo de conservación; la DGCORENADR no ha participado | Bandeja propia para la DGCORENADR e indicador de captación en suelo de conservación (D-18) |

---

## 2. Quién lo usa

Cinco perfiles. Los cuatro primeros estaban previstos en AD-01 y SIA-23; **el de coordinación es una propuesta de este bosquejo**, porque alguien tiene que asignar y returnar.

| Perfil | Quién | Ve | Hace | Datos personales de quien denuncia |
|---|---|---|---|---|
| **Captura** | Oficialía de Partes o la unidad que se designe (CP-2) | Lo que capturó y el aviso de denuncias cercanas | Registra denuncias recibidas por escrito, teléfono, correo o comparecencia | Sólo los de lo que captura |
| **Atención** | Personal de la coordinación que sustancia, en cada dirección general | Las denuncias de su área | Analiza competencia, cambia estado, registra actuaciones y notificaciones | Sí, de su área |
| **Coordinación** | Titular de cada coordinación o quien designe | Las de su área, con carga por persona | Asigna, reasigna, returna, remite, autoriza acumulación y conclusión; da de alta y de baja a su personal de captura, atención y coordinación | Sí, de su área |
| **Consulta** | Oficina de la Secretaría, direcciones generales | Tablero, mapa y bandeja de toda la Secretaría | Filtra y exporta | **No**: ve el expediente sin nombre, contacto ni domicilio |
| **Administración** | Sistema de Información Ambiental | Usuarios, catálogos, parámetros y bitácora | Da de alta las cuentas de consulta, administración y la primera coordinación de cada dirección general; actualiza catálogos | No, salvo por requerimiento registrado |

Reglas comunes: cuenta institucional nominal, nunca compartida; toda consulta de un expediente y todo cambio quedan en bitácora; el perfil y el área los asigna la coordinación de cada dirección general a su personal, y el SIA a los demás (DEC-252).

---

## 3. Qué pantallas tiene

Nueve pantallas. Las tres primeras son el trabajo diario; las demás se usan por semana o por mes.

### 3.1 Inicio

Lo que cada persona debe atender hoy, según su perfil: denuncias nuevas de su área, las asignadas a ella, las que vencen en los próximos días, las que ya vencieron y las resueltas que falta notificar. Sin gráficas: es una lista de trabajo.

**Lo que la maqueta propone, por acordar (DEC-245).** Las listas no son estados: juntan denuncias de varios estados. Atención ve las nuevas de su área y, en lo demás, sólo lo que tiene a su cargo. Coordinación ve toda su área y, en lugar de «Asignadas», «Por asignar»: lo turnado sin persona. Captura ve lo que capturó y lo que parece duplicado. «Por vencer» es lo que vence dentro de dos días hábiles, cifra de prueba.

### 3.2 Bandeja

Listado con folio, fecha de recepción, canal, materia, alcaldía, tipo de zona, área que recibe, remisión si la hay, estado, persona asignada y días hábiles transcurridos. Filtros combinables y búsqueda por folio, nombre del establecimiento, calle y texto de los hechos.

**El área y la remisión son dos columnas.** El formulario guarda el área que recibe —DGIVA o DGCORENADR— y, aparte, si la denuncia se remite a la PROFEPA (`dg` y `remite_a`, DEC-235). En un Área Natural Protegida federal la recibe la DGCORENADR y la remite (DEC-226): aparece en su bandeja con la marca de remisión, no en una bandeja «federal» que nadie atiende.

**Vistas predefinidas**, que salen de reglas que el formulario ya fijó:

| Vista | Qué reúne | Origen |
|---|---|---|
| Por turnar | Recibidas sin turnar, con el plazo de tres días hábiles corriendo | Manual Administrativo, DEC-84 |
| Por ubicar | Llegaron con dirección y sin punto, y el servidor no pudo ubicarlas | DEC-123, SIA-09 |
| En análisis de competencia | Turnadas, dentro de los diez días hábiles | Manual Administrativo |
| Por remitir a la PROFEPA | Áreas Naturales Protegidas federales: la DGCORENADR las recibe y las remite | DEC-226, DEC-235 |
| Posible duplicado | Misma materia, punto cercano y fechas próximas | P-21, control 4; D-12 |
| Marcadas para revisión | Prueba de humanidad sin verificar, ráfaga o baja completitud | Documento 15; SIA-15, SIA-26 |
| Alcaldía que no coincide | La alcaldía de la dirección difiere de la del punto | DEC-118 |
| Autoridad señalada como responsable | Siguen la vía de recomendación del artículo 331 de la Ley Ambiental | RN-24 bis; DEC-232 |
| Anónimas | Sin nombre ni domicilio; el resultado se notifica en su correo | RN-17, RN-21, DEC-233 |
| Por notificar | Resueltas cuyo resultado no se ha notificado en el domicilio o en el correo | Propuesta de esta versión |

Los plazos de esta bandeja son internos: el formulario no los menciona a la persona (DEC-138).

**Lo que la maqueta propone, por acordar (DEC-243).** Una denuncia sin punto todavía no es de ningún área: la ven las dos direcciones generales hasta que alguien la ubica (MA-13). «Posible duplicado» usa cifras de prueba —50 metros y 15 días— que fija la DGIVA (SIA-26), y sólo compara denuncias abiertas. Los días hábiles se cuentan desde la recepción original hasta hoy o hasta el cierre, sin sábados ni domingos, mientras falte el calendario de días inhábiles (MA-11). Cierran el trámite, y dejan de contar días, la remisión a otra autoridad, la conclusión, la acumulación, la conclusión sin materia y la recomendación. «Marcadas para revisión» reúne las marcas que pondría el servidor al recibir: prueba de humanidad sin verificar, ráfaga y baja completitud (documento 15; las dos últimas esperan los controles 5 y 6 de P-21).

### 3.3 Expediente

Una sola pantalla por denuncia. Encabezado fijo con folio, estado, área que recibe, remisión si la hay, persona asignada y plazo vigente. Debajo, seis secciones:

1. **Denuncia.** Todo lo capturado, en el mismo orden del acuse, con la fecha y hora de recepción en hora de la Ciudad (DEC-235) y el fundamento que citó el acuse —el artículo del Reglamento Interior del área que recibe, y el 331 de la Ley Ambiental si se señaló a una autoridad— (DEC-232). La materia declarada y, aparte, la **materia confirmada** por quien analiza (D-20).
2. **Ubicación.** Mapa con el punto y el polígono de la zona, resultado del cruce con su motivación, celda UGA, origen de la ubicación y la marca de discrepancia de alcaldía. Denuncias cercanas en un radio.
3. **Evidencia.** Galería de miniaturas —fotos, videos, PDF, Word y Excel— que se abren con un clic, con el nombre y el tipo de cada archivo y, en las fotografías, la fecha y el lugar de captura dichos en palabras —el lugar, contra el de la denuncia— (DEC-253, DEC-254). Peso, huella y coordenadas son datos del sistema: se guardan (DEC-121), pero no se muestran. En captura por personal, el escrito o la nota de soporte.
4. **Actuaciones.** Línea de tiempo: cada cambio de estado, turnado, asignación y nota, con fecha, hora y persona. No se edita ni se borra.
5. **Contacto y notificación.** Registro de cada comunicación con quien denuncia y de la información adicional recibida, y de la **notificación del resultado**: en el domicilio que registró o, en la anónima, en su correo (DEC-233). El correo lo envía el servidor y el envío y su resultado quedan aquí (SIA-29). Una aclaración pedida a la persona anónima que no conteste no detiene el trámite (RN-21). Sólo perfiles de atención y coordinación.
6. **Vínculos.** Expedientes acumulados, número del expediente administrativo si se abre, y oficio de remisión cuando sale de la Secretaría.

**Acciones**, según perfil: cambiar estado, asignar, returnar a la otra dirección general, remitir a otra autoridad, acumular, corregir el punto —con la ubicación original conservada—, registrar la notificación, agregar nota o documento, descargar ficha en PDF.

**Lo que la maqueta propone, por acordar (DEC-244).** El plazo vigente del encabezado es el del estado en que va la denuncia, contado desde la recepción original; el del procedimiento completo se lee del área que recibe —93 días hábiles en la DGIVA y 90 en la DGCORENADR—, porque el reparto de competencias sigue el tipo de suelo (DEC-84). El género y la edad no se muestran por denuncia, y consulta tampoco ve el lugar donde se tomó cada foto. Las denuncias cercanas usan un radio de prueba de 500 metros. Las acciones se reparten así: coordinación, todas; atención, cambiar estado, corregir el punto —lo propone y coordinación lo autoriza (MA-10)—, registrar la notificación, agregar nota y descargar la ficha; captura, agregar nota y descargar; consulta, descargar.

### 3.4 Captura por personal

El mismo formulario, con las diferencias ya descritas en AD-03: primer paso con canal, fecha y hora de recepción original, folio de origen y quién recibió; soporte obligatorio según el canal; datos de contacto que pueden marcarse «no proporcionado»; sin prueba de humanidad ni límite de envíos; aviso de denuncias cercanas al guardar; misma serie de folios (documento 19). Hereda del formulario sus reglas de captura: obligatoriedad desde `OBLIG` (DEC-237), longitudes desde `LIMITES` y rechazo de letras al azar (DEC-224, DEC-235, DEC-237).

**Cómo quedó (DEC-248).** Es el «modo captura» del propio formulario, con su interruptor en el panel de validación («Versión 37»); la pantalla de la maqueta lo abre y lista lo capturado. «No proporcionado» no es una casilla: el correo y el domicilio simplemente dejan de ser obligatorios en este modo y, si faltan, el formulario lo anota al guardar. Quedan por decidir cómo consta el aviso de privacidad de quien denunció por escrito o por teléfono y si el teléfono también puede no venir.

### 3.5 Mapa operativo

Las denuncias sobre las capas del Sistema de Información Ambiental, filtrables por materia, estado, área y periodo —año y mes—; agregación por alcaldía, colonia y celda UGA. Es el insumo para programar operativos: sitios con denuncia reiterada y zonas con concentración.

**Lo que la maqueta propone (DEC-247).** El mapa se dibuja con las capas del mapa vectorial del formulario, sin calles de fondo ni servicios externos. Abiertas y cerradas se distinguen por la forma, no sólo por el color, y junto al mapa van las mismas cuentas en tablas, porque el mapa no puede ser el único camino. En el expediente, el mapa enseña la zona protegida completa si el punto cae en una y, si no, la alcaldía.

### 3.6 Tablero

Ver apartado 5.

### 3.7 Búsqueda y exportación

Descarga en hoja de cálculo de la bandeja filtrada y de los indicadores. **La exportación con datos personales queda limitada a coordinación y se registra en bitácora**; la del perfil de consulta sale sin ellos.

**Lo que la maqueta propone (DEC-249).** Además de descargar, se abre un expediente por folio, consecutivo o folio de origen. La descarga con datos personales pide un motivo, que queda en la bitácora con quién y cuántas; atención y consulta descargan sin ellos. Género y edad no salen por denuncia en ninguna descarga.

### 3.8 Administración

Cuentas y perfiles; catálogos que el área puede actualizar sin tocar código —materias, giros (pendiente de OBS-0024), supuestos de otra autoridad, estados—; calendario de días inhábiles, sin el cual ningún plazo se cuenta bien; plazos y umbrales de los controles contra el abuso; plantilla del correo de notificación de la anónima; bitácora de accesos y cambios.

**Lo que la maqueta propone (DEC-249).** Todo se consulta y nada se cambia. Los plazos y umbrales se leen de donde los usa la maqueta, con quién fija cada uno y cuáles son cifras de prueba. La bitácora registra también las consultas al expediente, con datos personales o sin ellos, y no sólo los cambios.

### 3.9 Personal

Alta y baja del personal de cada dirección general, a cargo de su coordinación (DEC-252): nombre completo, área de la que depende, cargo, correo institucional y perfil —captura, atención o coordinación—. Consulta, administración y la primera coordinación de cada dirección general las da de alta el SIA.

**Lo que la maqueta propone (DEC-252).** Todo dato es obligatorio y dos personas activas no comparten correo, porque la cuenta es nominal. La baja no borra: la persona queda inactiva, ya no entra ni recibe asignaciones, y su nombre se conserva en lo que firmó y en la bitácora. Al dar de baja se avisa cuántas denuncias abiertas tenía asignadas, para reasignarlas, y una dirección general no puede quedarse sin coordinación activa. Administración ve al personal de las dos direcciones generales, sin cambiarlo.

---

## 4. Ciclo de la denuncia

**Propuesta para discutir con las áreas.** AD-01 dejó el catálogo de estados «pendiente de definir con el área sustantiva» y P-14 la equivalencia con lo que ve la ciudadanía. Se propone partir de esto:

| # | Estado interno | Qué significa | Plazo que corre | Lo que vería la ciudadanía (P-14) |
|---|---|---|---|---|
| 1 | Recibida | Guardada, con folio | 3 días hábiles para turnar | Recibida |
| 2 | Por ubicar | Sin punto; falta determinar el área | El mismo de turnado | Recibida |
| 3 | Turnada | Asignada a la coordinación de una dirección general | 10 días hábiles para analizar | En revisión |
| 4 | En análisis de competencia | Con persona asignada | — | En revisión |
| 5a | Returnada | Corresponde a la otra dirección general; **conserva el folio** | 5 días hábiles | En revisión |
| 5b | Remitida a otra autoridad | No es competencia de la Secretaría; sale con oficio. En un Área Natural Protegida federal es el camino normal: llega marcada para la PROFEPA (DEC-226, DEC-235) | 5 días hábiles | Remitida a (autoridad) |
| 6 | Admitida | Expediente integrado | 93 o 90 días hábiles, según el tipo de suelo | En atención |
| 7 | Visita programada | Con fecha interna | — | En atención |
| 8 | Visita practicada | Acta levantada | — | En atención |
| 9 | En procedimiento | Emplazamiento, pruebas, alegatos | — | En atención |
| 10 | Resuelta | Resolución emitida | — | Concluida, con el sentido que autorice la Unidad de Transparencia |
| 11 | Notificada | Resultado notificado en el domicilio o, en la anónima, en el correo (DEC-233) | — | Concluida |
| 12 | Concluida | Cierre del expediente | — | Concluida |

Estados laterales: **Acumulada** a otro expediente; **Concluida sin materia**, cuando los hechos no se acreditan o la información no basta; **Recomendación emitida**, para la vía del artículo 331.

Cinco reglas del ciclo:

1. Ningún cambio de estado sin fecha, persona y nota. De ahí salen todos los indicadores de tiempo.
2. La fecha de la visita programada **no sale del módulo**: difundirla compromete la diligencia.
3. Returnar y remitir son actos distintos y se cuentan por separado. Es lo que la base histórica no permite distinguir.
4. Los plazos se cuentan en días hábiles desde la **fecha de recepción original**, no desde la captura (CP-1, recomendación). En las denuncias en línea es la que guarda el formulario, en hora de la Ciudad (DEC-235).
5. El artículo 332 de la Ley Ambiental obliga a informar a quien denuncia del trámite que recaiga a su denuncia; el plazo en que se le informa sigue abierto (P-07), y el módulo debe poder medirlo en cuanto se fije.

---

## 5. Tablero de indicadores

Cinco grupos. Todos se filtran por año, mes, área, canal, materia y alcaldía. Los años salen de las denuncias registradas y no de una lista fija: el tablero se lleva año con año sin tocar el código (DEC-251).

| Grupo | Indicador | Para qué sirve |
|---|---|---|
| **Operación** | Recibidas, en trámite y concluidas, por año y por mes | Carga de trabajo; comparar un año con otro |
| | Recibidas por canal y por origen | Comparar con la serie histórica (D-19) |
| | Carga por persona asignada | Repartir trabajo; sólo coordinación |
| **Plazos** | Días hábiles hasta el turnado, contra el plazo de 3 | Cumplimiento del Manual |
| | Días hábiles hasta la primera valoración, contra el plazo de 10 | Cumplimiento del Manual; documento 15, §6 |
| | Expedientes dentro y fuera del plazo de 93 o 90 días | Rezago |
| | Tiempo que una denuncia pasa «por ubicar» | Medir el costo de DEC-123 |
| | Días entre la resolución y la notificación | Medir lo que P-07 deje fijado |
| **Resultado** | Proporción con visita practicada, por materia | Línea base: 76.7 % en plásticos de un solo uso |
| | Remitidas a otra autoridad y returnadas, por separado | Responde PB-01 con dato propio |
| | Concluidas sin materia y acumuladas por duplicado | Calidad de lo que entra; documento 15, §6 |
| | Materia declarada frente a materia confirmada | Mide si el paso 1 se entiende; alimenta D-2 |
| **Territorio** | Denuncias por alcaldía, colonia, tipo de zona y celda UGA | Programación de operativos |
| | Proporción en suelo de conservación, en Áreas Naturales Protegidas y en Áreas de Valor Ambiental, cada una por separado | Línea base de las dos primeras, juntas: 4.3 %; 0.2 % en Milpa Alta (D-18) |
| **Canal** | Denuncias anónimas y con datos | Seguimiento de DEC-03 |
| | Notificaciones por correo enviadas y fallidas, en anónimas | Seguimiento de DEC-233 y SIA-29 |
| | Con punto y sin punto; con evidencia y sin ella | Calidad de la captura |
| | Género y rango de edad, sólo en agregado | P-20 resuelta (DEC-225, DEC-234); falta que el SIA asuma publicar la desagregación |

**Lo que la maqueta propone, por acordar (DEC-246).** El turnado y la primera valoración se cuentan en días hábiles desde la recepción original; la primera valoración es la primera vez que la denuncia se admite, returna, remite, recomienda o concluye. El género y la edad sólo van en agregado, y una cifra menor que 3 se muestra como «menos de 3», porque con los filtros podría señalar a una persona; la cifra la fija la Unidad de Transparencia.

**Lo que cambió (DEC-251).** Por instrucción de Liber Saltijeral, el tablero ya no reporta las celdas UGA con denuncia reiterada; el mapa operativo conserva su cuenta por celda UGA. Suelo de conservación, Áreas Naturales Protegidas y Áreas de Valor Ambiental se cuentan por separado, cada denuncia en la zona que dio el cruce del formulario. Y el tablero y el mapa se filtran por año, con un cuadro de recibidas, en trámite y cerradas por año: los años salen de las denuncias, de modo que el que llegue aparece solo.

---

## 6. Datos que el módulo agrega al modelo

El formulario captura la denuncia; el módulo agrega su trámite. Deben entrar al contrato de datos de la fase 2 (SIA-02, SIA-03) aunque se construyan después:

- **Trámite:** estado, fecha y hora de cada cambio, persona que lo hizo, nota.
- **Turnado:** área actual e historial de áreas, fecha de turnado, constancia (D-13). El área inicial y la remisión ya vienen del formulario (`dg`, `remite_a`, DEC-235).
- **Análisis:** materia confirmada, persona asignada, motivo de returnado o remisión, autoridad de destino, oficio.
- **Resultado:** fecha de visita, sentido de la resolución, tipo de conclusión, número de expediente administrativo.
- **Notificación:** medio —domicilio o correo—, fecha, y en el correo el resultado del envío (DEC-233, SIA-29).
- **Vínculos:** expediente principal cuando hay acumulación.
- **Canal y origen:** los de AD-03 —canal, origen, fecha de recepción original, folio de origen, quién recibió, quién capturó, fecha de captura y soporte—.
- **Corrección de ubicación:** punto original y punto corregido, con quién y cuándo.

Las fechas van en ISO 8601 con la zona de la Ciudad, como la de recepción (DEC-235), y la longitud de cada campo de texto sale de `LIMITES`.

---

## 7. Protección de datos

El módulo concentra datos personales de quien denuncia y señalamientos sobre terceros. Siete condiciones de diseño, a confirmar con la Unidad de Transparencia (SIA-20):

1. Acceso por perfil y por área; el perfil de consulta nunca ve datos personales.
2. Bitácora de consultas, no sólo de cambios.
3. La identidad de quien denuncia no aparece en ningún documento que el módulo genere para la persona denunciada (RN-19).
4. Exportación con datos personales restringida y registrada.
5. Política de conservación y supresión definida antes del primer dato real.
6. El correo de la denuncia anónima es su única vía de contacto y el medio de notificación (DEC-233): el mensaje no lleva datos de la persona denunciada ni de terceros (SIA-29).
7. El género es dato sensible; se trata con el consentimiento general del aviso de privacidad (DEC-234), que la Unidad de Transparencia debe confirmar frente al artículo 14 de la Ley de datos personales (P-02). En el módulo sólo aparece en agregado.

---

## 8. Qué no entra en la primera versión

| No entra | Por qué |
|---|---|
| Sustanciación del procedimiento: órdenes de visita, actas, acuerdos | Fuera del alcance del proyecto (documento 01). El módulo registra hitos, no genera actos |
| Avisos automáticos por correo a quien denuncia con datos | No hay servicio de envío para eso y en esa ruta se notifica en el domicilio (DEC-134). **Sí entra** la notificación por correo de la anónima (DEC-233, SIA-29) |
| Consulta ciudadana por folio | Es AD-02 y va después, sobre estados que el módulo ya registre |
| Interoperabilidad con la PAOT o el INVEA | Etapa 3 |
| Migración de la base histórica | SIA-28; se decide con CP-5 |

---

## 9. Orden de trabajo propuesto

Mismo método que el formulario: primero maqueta, después servidor.

| Paso | Qué se hace | Cuándo puede empezar |
|---|---|---|
| 1 | Acordar este bosquejo y resolver las preguntas del apartado 10 que dependen de la Oficina de la Secretaría | Ahora |
| 2 | Maqueta navegable del módulo con datos ficticios —los escenarios del panel de validación convertidos en unas cuarenta denuncias de prueba—: bandeja, expediente y tablero. No guarda nada. **Hecha (DEC-242 a DEC-249)** y publicada en https://sedemaoficina.github.io/denuncia-ambiental/administracion/ (DEC-250): bloques A, cascarón y datos de prueba (DEC-242), B, bandeja (DEC-243), C, expediente (DEC-244), D, Inicio, tablero y mapa (DEC-245 a DEC-247), E, captura por personal (DEC-248), y F, búsqueda, exportación y administración (DEC-249) | Ahora: el acta ya se firmó (DEC-230) y una maqueta sin persistencia no choca con el documento 11, §6. Los estados son los de la propuesta del apartado 4 hasta que se resuelva P-14 |
| 3 | Variante «modo captura» del prototipo del formulario (AD-03) | **Hecho:** «Versión 37» (DEC-248) |
| 4 | Sesión con la DGIVA y con la DGCORENADR sobre estados, perfiles y vistas, con la maqueta a la vista | En cuanto exista la maqueta |
| 5 | Pase de diseño de la maqueta, pantalla por pantalla —jerarquía, espacios, gráficas, que cada pantalla se entienda a primera vista—, con capturas de antes y después para que Liber Saltijeral decida. La identidad gráfica no cambia: viene del formulario | Después del paso 4, con el contenido acordado (DEC-255) |
| 6 | Construcción: captura por personal, después bandeja y expediente, después tablero y mapa | Fase 5 (documento 11), sobre el contrato de la fase 2 |

---

## 10. Preguntas que abre

Clave `MA-NN`. Las seis primeras puede resolverlas la Oficina de la Secretaría; las demás son de las áreas. Ninguna se ha respondido todavía.

| Clave | Pregunta | Recomendación |
|---|---|---|
| **MA-01** | ¿El módulo va en la misma dirección web que el formulario o en otra? | **Otra**, dentro del SIA y con el mismo control de acceso del tablero del SIA. Separa lo público de lo interno y evita exponer la entrada del personal en el sitio ciudadano |
| **MA-02** | ¿Dónde vive la versión funcional de la etapa 2: en el servidor del SIA o en una solución provisional con hojas de cálculo? | **Servidor del SIA.** Una hoja de cálculo no da acceso por perfil ni bitácora de consultas, y son datos personales. La maqueta no depende de esta decisión |
| **MA-03** | ¿Hasta dónde llega el registro: hasta el turnado y la visita, o hasta la resolución? | Hasta la resolución y su notificación, **como hitos con fecha**, sin gestionar los documentos del procedimiento |
| **MA-04** | ¿La Oficina de la Secretaría consulta con o sin datos personales? | Sin ellos, salvo requerimiento registrado |
| **MA-05** | ¿Se agrega el perfil de coordinación? | Sí: sin quien asigne, la bandeja no reparte trabajo |
| **MA-06** | ¿El tablero tendrá una versión pública? | No en esta etapa; decidirlo junto con PB-20 |
| **MA-07** | ¿Qué estados reconoce cada dirección general, y cuáles puede ver la ciudadanía? | Partir de la tabla del apartado 4 (P-14, PB-15) |
| **MA-08** | ¿La DGCORENADR opera su bandeja en este módulo? | Sí, y debe verlo antes de construirse (PB-14, CP-4); también remite desde ahí las de Áreas Naturales Protegidas federales |
| **MA-09** | ¿Quién captura lo que llega por otros canales? | CP-2, abierta |
| **MA-10** | ¿Quién puede corregir el punto del mapa y returnar? | Atención propone, coordinación autoriza |
| **MA-11** | ¿Qué calendario de días inhábiles se usa? | El que publique la Secretaría para cada año, cargado por el SIA |
| **MA-12** | ¿Quién redacta y firma el correo con que se notifica el resultado a la persona anónima, y desde qué cuenta sale? | La dirección general que recibe, con plantilla acordada con la Unidad de Transparencia y una cuenta institucional del SIA (SIA-29). *Pregunta de la versión 0.2* |
| **MA-13** | ¿Quién ubica las denuncias que llegan sin punto y que el servidor no pudo ubicar (SIA-09)? Mientras no tienen punto no son de ningún área | Que las vean las dos direcciones generales en «Por ubicar» y que la turne la que la ubique, como hace la maqueta (DEC-243). La alternativa es que las ubique quien capture (MA-09). *Pregunta nueva de esta versión* |

---

## 11. Relación con otros documentos

| Documento | Qué aporta a este módulo |
|---|---|
| 03 · Marco jurídico | Fundamento con que recibe cada dirección general (artículos 188 y 191 del Reglamento Interior) y el artículo 332 de la Ley Ambiental |
| 05 · Decisiones | AD-01, AD-02, AD-03; P-07, P-14, P-21; CP-1 a CP-5; DEC-226, DEC-232, DEC-233 y DEC-235 |
| 09 · Mapeo de campos | Lo que se muestra en la sección «Denuncia» del expediente; se genera del código |
| 10 · Variantes | Las ramas del formulario, que son las combinaciones que la bandeja tiene que poder filtrar |
| 15 · Resistencia al abuso | Marcas de revisión, duplicados e indicadores de calidad |
| 17 · Base histórica | Líneas base y preguntas PB-01 a PB-20 |
| 19 · Folios | Serie única; el área es dato del expediente |
| 20 · Servidor del SIA | SIA-23 a SIA-29 |
