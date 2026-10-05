# Formulario web de Denuncia Ambiental · Bosquejo del módulo de administración y seguimiento

**Versión:** 0.1 · 5 de octubre de 2026
**Estado:** bosquejo para discusión. **No abre la construcción del módulo.**
**Para qué sirve este documento.** Reúne en un solo lugar lo que tendría que tener el módulo interno de la Secretaría —captura por personal (AD-03), bandeja, expediente, tablero y administración (AD-01)—, para llegar al acta de validación del formulario con el módulo ya pensado. Desarrolla lo que el documento 05 dejó enunciado en la Parte V y lo que el documento 20 lista como SIA-23 a SIA-26.

**Regla que este bosquejo respeta.** DEC-19 y DEC-32 siguen vigentes: no se programa ningún módulo antes del acta de validación de la Dirección General de Inspección y Vigilancia Ambiental. Bosquejar no las contradice, con una condición: **todo lo que aquí dependa de un campo del formulario se da por provisional** hasta que cierre la revisión en curso. Lo que no depende de los campos —perfiles, estados, plazos, indicadores— sí puede acordarse desde ahora.

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
| **Atención** | Personal de la coordinación que sustancia, en cada dirección general | Las denuncias de su área | Analiza competencia, cambia estado, registra actuaciones | Sí, de su área |
| **Coordinación** | Titular de cada coordinación o quien designe | Las de su área, con carga por persona | Asigna, reasigna, returna, autoriza acumulación y conclusión | Sí, de su área |
| **Consulta** | Oficina de la Secretaría, direcciones generales | Tablero, mapa y bandeja de toda la Secretaría | Filtra y exporta | **No**: ve el expediente sin nombre, contacto ni domicilio |
| **Administración** | Sistema de Información Ambiental | Usuarios, catálogos, parámetros y bitácora | Da de alta cuentas, actualiza catálogos | No, salvo por requerimiento registrado |

Reglas comunes: cuenta institucional nominal, nunca compartida; toda consulta de un expediente y todo cambio quedan en bitácora; el perfil y el área los asigna la Secretaría.

---

## 3. Qué pantallas tiene

Ocho pantallas. Las tres primeras son el trabajo diario; las demás se usan por semana o por mes.

### 3.1 Inicio

Lo que cada persona debe atender hoy, según su perfil: denuncias nuevas de su área, las asignadas a ella, las que vencen en los próximos días y las que ya vencieron. Sin gráficas: es una lista de trabajo.

### 3.2 Bandeja

Listado con folio, fecha de recepción, canal, materia, alcaldía, tipo de zona, área que atiende, estado, persona asignada y días hábiles transcurridos. Filtros combinables y búsqueda por folio, nombre del establecimiento, calle y texto de los hechos.

**Vistas predefinidas**, que salen de reglas que el formulario ya fijó:

| Vista | Qué reúne | Origen |
|---|---|---|
| Por turnar | Recibidas sin turnar, con el plazo de tres días hábiles corriendo | Manual Administrativo, DEC-84 |
| Por ubicar | Llegaron con dirección y sin punto, y el servidor no pudo ubicarlas | DEC-123, SIA-09 |
| En análisis de competencia | Turnadas, dentro de los diez días hábiles | Manual Administrativo |
| Posible duplicado | Misma materia, punto cercano y fechas próximas | P-21, control 4; D-12 |
| Marcadas para revisión | Prueba de humanidad sin verificar, ráfaga o baja completitud | Documento 15; SIA-15, SIA-26 |
| Alcaldía que no coincide | La alcaldía de la dirección difiere de la del punto | DEC-118 |
| Área Natural Protegida federal | Por remitir a la PROFEPA, criterio provisional | DEC-89, P-22 |
| Autoridad señalada como responsable | Siguen la vía de recomendación del artículo 331 de la Ley Ambiental | RN-24 bis |
| Anónimas | Sin nombre ni domicilio, con correo de contacto | RN-17 |

### 3.3 Expediente

Una sola pantalla por denuncia. Encabezado fijo con folio, estado, área, persona asignada y plazo vigente. Debajo, seis secciones:

1. **Denuncia.** Todo lo capturado, en el mismo orden del acuse. La materia declarada y, aparte, la **materia confirmada** por quien analiza (D-20).
2. **Ubicación.** Mapa con el punto y el polígono de la zona, resultado del cruce con su motivación, celda UGA, origen de la ubicación y la marca de discrepancia de alcaldía. Denuncias cercanas en un radio.
3. **Evidencia.** Galería con la huella SHA-256 del original y la fecha y el lugar de captura de cada fotografía (DEC-121). En captura por personal, el escrito o la nota de soporte.
4. **Actuaciones.** Línea de tiempo: cada cambio de estado, turnado, asignación y nota, con fecha, hora y persona. No se edita ni se borra.
5. **Contacto con quien denuncia.** Registro de cada comunicación y de la información adicional recibida. Sólo perfiles de atención y coordinación.
6. **Vínculos.** Expedientes acumulados, número del expediente administrativo si se abre, y oficio de remisión cuando sale de la Secretaría.

**Acciones**, según perfil: cambiar estado, asignar, returnar a la otra dirección general, remitir a otra autoridad, acumular, corregir el punto —con la ubicación original conservada—, agregar nota o documento, descargar ficha en PDF.

### 3.4 Captura por personal

El mismo formulario, con las diferencias ya descritas en AD-03: primer paso con canal, fecha y hora de recepción original, folio de origen y quién recibió; soporte obligatorio según el canal; datos de contacto que pueden marcarse «no proporcionado»; sin prueba de humanidad ni límite de envíos; aviso de denuncias cercanas al guardar; misma serie de folios (documento 19).

### 3.5 Mapa operativo

Las denuncias sobre las capas del Sistema de Información Ambiental, filtrables por materia, estado, área y periodo; agregación por alcaldía, colonia y celda UGA. Es el insumo para programar operativos: sitios con denuncia reiterada y zonas con concentración.

### 3.6 Tablero

Ver apartado 5.

### 3.7 Búsqueda y exportación

Descarga en hoja de cálculo de la bandeja filtrada y de los indicadores. **La exportación con datos personales queda limitada a coordinación y se registra en bitácora**; la del perfil de consulta sale sin ellos.

### 3.8 Administración

Cuentas y perfiles; catálogos que el área puede actualizar sin tocar código —materias, giros, supuestos de otra autoridad, estados—; calendario de días inhábiles, sin el cual ningún plazo se cuenta bien; plazos y umbrales de los controles contra el abuso; bitácora de accesos y cambios.

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
| 5b | Remitida a otra autoridad | No es competencia de la Secretaría; sale con oficio | 5 días hábiles | Remitida a (autoridad) |
| 6 | Admitida | Expediente integrado | 93 o 90 días hábiles, según el tipo de suelo | En atención |
| 7 | Visita programada | Con fecha interna | — | En atención |
| 8 | Visita practicada | Acta levantada | — | En atención |
| 9 | En procedimiento | Emplazamiento, pruebas, alegatos | — | En atención |
| 10 | Resuelta | Resolución emitida | — | Concluida, con el sentido que autorice la Unidad de Transparencia |
| 11 | Concluida | Cierre del expediente | — | Concluida |

Estados laterales: **Acumulada** a otro expediente; **Concluida sin materia**, cuando los hechos no se acreditan o la información no basta; **Recomendación emitida**, para la vía del artículo 331.

Cuatro reglas del ciclo:

1. Ningún cambio de estado sin fecha, persona y nota. De ahí salen todos los indicadores de tiempo.
2. La fecha de la visita programada **no sale del módulo**: difundirla compromete la diligencia.
3. Returnar y remitir son actos distintos y se cuentan por separado. Es lo que la base histórica no permite distinguir.
4. Los plazos se cuentan en días hábiles desde la **fecha de recepción original**, no desde la captura (CP-1, recomendación).

---

## 5. Tablero de indicadores

Cuatro grupos. Todos se filtran por periodo, área, canal, materia y alcaldía.

| Grupo | Indicador | Para qué sirve |
|---|---|---|
| **Operación** | Recibidas, en trámite y concluidas, por periodo | Carga de trabajo |
| | Recibidas por canal y por origen | Comparar con la serie histórica (D-19) |
| | Carga por persona asignada | Repartir trabajo; sólo coordinación |
| **Plazos** | Días hábiles hasta el turnado, contra el plazo de 3 | Cumplimiento del Manual |
| | Días hábiles hasta la primera valoración, contra el plazo de 10 | Cumplimiento del Manual; documento 15, §6 |
| | Expedientes dentro y fuera del plazo de 93 o 90 días | Rezago |
| | Tiempo que una denuncia pasa «por ubicar» | Medir el costo de DEC-123 |
| **Resultado** | Proporción con visita practicada, por materia | Línea base: 76.7 % en plásticos de un solo uso |
| | Remitidas a otra autoridad y returnadas, por separado | Responde PB-01 con dato propio |
| | Concluidas sin materia y acumuladas por duplicado | Calidad de lo que entra; documento 15, §6 |
| | Materia declarada frente a materia confirmada | Mide si el paso 1 se entiende; alimenta D-2 |
| **Territorio** | Denuncias por alcaldía, colonia, tipo de zona y celda UGA | Programación de operativos |
| | Sitios con denuncia reiterada | Barrancas y predios recurrentes (documento 17, apartado 7) |
| | Proporción en suelo de conservación y Áreas Naturales Protegidas | Línea base: 4.3 %; 0.2 % en Milpa Alta (D-18) |
| **Canal** | Denuncias anónimas y con datos | Seguimiento de DEC-03 |
| | Con punto y sin punto; con evidencia y sin ella | Calidad de la captura |
| | Género y rango de edad, sólo en agregado | Condicionado a P-20 |

---

## 6. Datos que el módulo agrega al modelo

El formulario captura la denuncia; el módulo agrega su trámite. Deben entrar al contrato de datos de la fase 2 (SIA-02, SIA-03) aunque se construyan después:

- **Trámite:** estado, fecha y hora de cada cambio, persona que lo hizo, nota.
- **Turnado:** área actual, historial de áreas, fecha de turnado, constancia (D-13).
- **Análisis:** materia confirmada, persona asignada, motivo de returnado o remisión, autoridad de destino, oficio.
- **Resultado:** fecha de visita, sentido de la resolución, tipo de conclusión, número de expediente administrativo.
- **Vínculos:** expediente principal cuando hay acumulación.
- **Canal y origen:** los de AD-03 —canal, origen, fecha de recepción original, folio de origen, quién recibió, quién capturó, fecha de captura y soporte—.
- **Corrección de ubicación:** punto original y punto corregido, con quién y cuándo.

---

## 7. Protección de datos

El módulo concentra datos personales de quien denuncia y señalamientos sobre terceros. Cinco condiciones de diseño, a confirmar con la Unidad de Transparencia (SIA-20):

1. Acceso por perfil y por área; el perfil de consulta nunca ve datos personales.
2. Bitácora de consultas, no sólo de cambios.
3. La identidad de quien denuncia no aparece en ningún documento que el módulo genere para la persona denunciada (RN-19).
4. Exportación con datos personales restringida y registrada.
5. Política de conservación y supresión definida antes del primer dato real.

---

## 8. Qué no entra en la primera versión

| No entra | Por qué |
|---|---|
| Sustanciación del procedimiento: órdenes de visita, actas, acuerdos | Fuera del alcance del proyecto (documento 01). El módulo registra hitos, no genera actos |
| Avisos por correo | No hay servicio de envío (DEC-134) |
| Consulta ciudadana por folio | Es AD-02 y va después, sobre estados que el módulo ya registre |
| Interoperabilidad con la PAOT o el INVEA | Etapa 3 |
| Migración de la base histórica | SIA-28; se decide con CP-5 |

---

## 9. Orden de trabajo propuesto

Mismo método que el formulario: primero maqueta, después servidor.

| Paso | Qué se hace | Cuándo puede empezar |
|---|---|---|
| 1 | Acordar este bosquejo y resolver las preguntas del apartado 10 que dependen de la Oficina de la Secretaría | Ahora |
| 2 | Maqueta navegable del módulo con datos ficticios —los escenarios del panel de validación convertidos en unas cuarenta denuncias de prueba—: bandeja, expediente y tablero | Ahora, con la reserva de que los campos pueden cambiar tras la revisión de la DGIVA |
| 3 | Variante «modo captura» del prototipo del formulario | Tras el acta de validación (AD-03) |
| 4 | Sesión con la DGIVA y con la DGCORENADR sobre estados, perfiles y vistas | Tras el acta de validación |
| 5 | Construcción: captura por personal, después bandeja y expediente, después tablero y mapa | Fase 5 (documento 11), sobre el contrato de la fase 2 |

---

## 10. Preguntas que abre

Clave `MA-NN`. Las seis primeras puede resolverlas la Oficina de la Secretaría; las demás son de las áreas.

| Clave | Pregunta | Recomendación |
|---|---|---|
| **MA-01** | ¿El módulo va en la misma dirección web que el formulario o en otra? | **Otra**, dentro del SIA y con el mismo control de acceso del tablero del SIA. Separa lo público de lo interno y evita exponer la entrada del personal en el sitio ciudadano |
| **MA-02** | ¿Dónde vive la versión funcional de la etapa 2: en el servidor del SIA o en una solución provisional con hojas de cálculo? | **Servidor del SIA.** Una hoja de cálculo no da acceso por perfil ni bitácora de consultas, y son datos personales. La maqueta no depende de esta decisión |
| **MA-03** | ¿Hasta dónde llega el registro: hasta el turnado y la visita, o hasta la resolución? | Hasta la resolución, **como hitos con fecha**, sin gestionar los documentos del procedimiento |
| **MA-04** | ¿La Oficina de la Secretaría consulta con o sin datos personales? | Sin ellos, salvo requerimiento registrado |
| **MA-05** | ¿Se agrega el perfil de coordinación? | Sí: sin quien asigne, la bandeja no reparte trabajo |
| **MA-06** | ¿El tablero tendrá una versión pública? | No en esta etapa; decidirlo junto con PB-20 |
| **MA-07** | ¿Qué estados reconoce cada dirección general, y cuáles puede ver la ciudadanía? | Partir de la tabla del apartado 4 (P-14, PB-15) |
| **MA-08** | ¿La DGCORENADR opera su bandeja en este módulo? | Sí, y debe verlo antes de construirse (PB-14, CP-4) |
| **MA-09** | ¿Quién captura lo que llega por otros canales? | CP-2, abierta |
| **MA-10** | ¿Quién puede corregir el punto del mapa y returnar? | Atención propone, coordinación autoriza |
| **MA-11** | ¿Qué calendario de días inhábiles se usa? | El que publique la Secretaría para cada año, cargado por el SIA |

---

## 11. Relación con otros documentos

| Documento | Qué aporta a este módulo |
|---|---|
| 05 · Decisiones | AD-01, AD-02, AD-03; P-07, P-14, P-21; CP-1 a CP-5 |
| 09 · Mapeo de campos | Lo que se muestra en la sección «Denuncia» del expediente; se genera del código |
| 15 · Resistencia al abuso | Marcas de revisión, duplicados e indicadores de calidad |
| 17 · Base histórica | Líneas base y preguntas PB-01 a PB-20 |
| 19 · Folios | Serie única; el área es dato del expediente |
| 20 · Servidor del SIA | SIA-23 a SIA-28 |
