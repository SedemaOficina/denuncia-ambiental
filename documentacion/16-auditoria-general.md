# Formulario web de Denuncia Ambiental · Auditoría general del proyecto

**Versión:** 1.0 · 20 de septiembre de 2026
**Alcance:** los quince documentos, el prototipo completo, la cadena de construcción y las trece baterías de prueba vigentes ese día.
**Método:** tres revisiones independientes y simultáneas —documental, de código y jurídica—, cada una obligada a verificar sus hallazgos antes de afirmarlos. La revisión de código ejecutó el formulario en un navegador; la jurídica trabajó sin acceso a los PDF de la normativa y así lo declara en cada punto.

> **Qué es este documento.** No es una auditoría de estilo ni una lista de mejoras. Registra **lo que el proyecto afirmaba y no era cierto**, lo que se corrigió el mismo día y lo que queda abierto. Se escribe una vez y no se actualiza: es fotografía de una fecha. Lo que de aquí se decida vive en el documento 05; lo que se corrigió, en DEC-99 y DEC-100.

---

## 1. El juicio, en un párrafo

El proyecto está en mejor estado que la mayoría de los desarrollos de su tipo y su principal activo es una disciplina poco común: deja sus huecos a la vista en la propia pantalla, registra sus errores —incluido el incidente del repositorio— y genera del código los documentos que puede generar. **Pero no está listo para presentarse como un instrumento a punto de publicarse.** Tres de sus afirmaciones centrales descansaban en verificaciones incompletas, y el formulario decía al ciudadano, en la misma pantalla, dos cosas contrarias sobre quién atiende su denuncia. Todo eso convivía con 343 comprobaciones automáticas en verde. **Sí está listo para presentarse a las Direcciones Generales como lo que es**: un prototipo maduro que necesita decisiones que sólo ellas y la unidad jurídica pueden tomar.

---

## 2. La lección de método

Las 343 comprobaciones no eran pocas ni flojas. Fallaron por una razón que conviene nombrar, porque volverá a presentarse:

**Se comprobaba el estado y no la pantalla.** La batería del turnado federal verificaba que `dg_nombre` dijera PROFEPA —y lo decía— y que el aviso del criterio provisional apareciera —y aparecía—. Nunca leyó el resto del panel, donde un recuadro verde afirmaba lo contrario. La misma familia explica el resto: el botón de descartar el borrador *existía*, y nadie comprobó que hiciera algo; el renglón «Punto en el mapa» *se listaba*, y nadie comprobó que llevara a alguna parte; el límite de archivos *estaba escrito en la pantalla*, y nadie comprobó que se aplicara.

De ahí la batería 14, que mira lo que la persona ve y lo que la persona pulsa: recorre cada parque federal leyendo el panel completo, pulsa los veinte botones «Editar» y verifica dónde aterriza cada uno, pasa archivos inadmisibles y comprueba que se rechacen **y se diga**, y recorre las reglas de estilo buscando selectores que el documento ya no usa —el mismo barrido que habría cazado la variable `--error-txt` que se definía a sí misma—.

**Regla que queda:** una comprobación que sólo lee el estado no ha comprobado el formulario.

---

## 3. Lo que se corrigió el mismo día

### 3.1 Lo que el ciudadano habría visto

| # | Qué pasaba | Dónde |
|---|---|---|
| 1 | En las ocho ANP federales con convenio, la ficha turnaba a la PROFEPA, lo advertía, y debajo imprimía en verde «la denuncia se atiende en el ámbito local». Era lo último que se leía | `cajaCapas()` |
| 2 | La tala y el cascajo citaban un artículo penal que no les corresponde | catálogo `MATERIAS` |
| 3 | «Descartar» el borrador no hacía absolutamente nada | `pideBorrar()` |
| 4 | Los límites de archivos se anunciaban y no se aplicaban; los sobrantes se descartaban en silencio | `agregaArchivos()` |
| 5 | La zona de carga invitaba a arrastrar; soltar un archivo hacía que el navegador lo abriera y se perdiera la pantalla | paso 4 |
| 6 | El resumen de errores listaba «Punto en el mapa» con un enlace que no llevaba a ninguna parte | `muestraResumenErrores()` |
| 7 | Cinco de los veinte botones «Editar» llevaban a campos que esa ruta no rinde | `pRevision()` |
| 8 | El acuse prometía a nombre de la PROFEPA los plazos y la unidad de seguimiento de la Secretaría | `pAcuse()` |
| 9 | El folio decía DGIVA aunque el cruce turnara a la DGCORENADR | `enviar()` |
| 10 | Lo capturado en una rama de responsable sobrevivía al cambio a otra y reaparecía en la revisión | `bloqueDenunciado()` |
| 11 | El foco se perdía en cada cambio de paso: seis veces por recorrido, con teclado o lector de pantalla | `render()` |

### 3.2 Las tres citas penales

Verificadas contra el texto vigente del **Código Penal para el Distrito Federal** (archivo `10_CODIGO_PENAL_CDMX_20260723.pdf`, con las reformas publicadas en la Gaceta Oficial de la Ciudad de México del 24 de diciembre de 2025). El artículo 344 BIS se citaba en las tres materias:

| Materia | Decía | Dice | Por qué |
|---|---|---|---|
| Tala o desmonte | Art. 344 Bis | **Art. 345 BIS** | Es el que sanciona a quien «de forma ilegal o con dolo derribe, tale u ocasione la muerte de uno o más árboles» |
| Despalmes y terráceos | Art. 344 Bis | **Art. 344 BIS** | Correcto: extracción de suelo o cubierta vegetal, piedra o tierra natural, por dos metros cúbicos o más |
| Depósito de cascajo | Art. 344 Bis | **Art. 344** | Es el que sanciona descargar o depositar residuos sólidos de la industria de la construcción en lugar no autorizado |

*Fuente: `insumos/normativa/10_CODIGO_PENAL_CDMX_20260723.pdf`, artículos 344, 344 BIS y 345 BIS.*

**Por qué importa más de lo que parece.** El documento 08 registraba esta cita como «pendiente de verificar el texto vigente» mientras el documento 12 afirmaba, con la misma fecha, que ninguna cita del proyecto estaba sin verificar. Las dos cosas no podían ser ciertas a la vez, y la que estaba en la pantalla del ciudadano era una imputación penal equivocada en dos de las tres materias donde aparecía.

### 3.3 Cifras que el proyecto afirmaba y no eran ciertas

El documento 05 anunciaba quince preguntas abiertas y formulaba veintidós. El 12 decía 54 campos en un renglón y 56 dos renglones después. La cola redactada a mano del 09 —bajo un encabezado que promete exactitud— hablaba de cuarenta y siete campos y de ocho campos de domicilio, que son siete. El 12 contaba trece escenarios y son doce. El criterio de salida de la fase 1, en el documento 11, seguía exigiendo el mapeo «en los dos esquemas» después de que DEC-97 retirara el segundo: mientras estuviera así escrito, esa puerta no podía cruzarse. El documento 08 ligaba el Reglamento Interior a P-17, que es la pregunta del teléfono. Y DEC-07 seguía en la tabla de decisiones vigentes sin decir que DEC-89 la había revertido, precisamente la decisión que la Dirección General va a revisar.

Todo eso está corregido. **Dónde estaba el daño:** en lo que se escribe a mano dentro de un documento generado, y en los documentos que no llevan nota de vigencia pero describen estado actual —el 02, el 04 y el 12, detenidos en el 18 de septiembre mientras el prototipo avanzaba dos días—.

### 3.4 Dos hallazgos que resultaron falsos

Se dejan registrados porque el método importa: a dos de las tres revisiones se les entregó una copia parcial del proyecto, y ambas concluyeron —correctamente, para lo que veían— que faltaban veintiún archivos de normativa y que `construccion/normalizar_capas.py` no existía. Verificado contra la carpeta de trabajo: **los veintidós archivos están y llevan la nomenclatura correcta, y el guion existe.** Un auditor sólo puede responder por lo que se le entrega.

---

## 4. Lo que queda abierto

### 4.1 Nivel 1 · Bloquea todos los textos

**P-01, naturaleza jurídica del canal.** De ella dependen el nombre del instrumento, el acuse, el aviso de privacidad, los plazos y los compromisos. Hoy el prototipo se llama «denuncia», emite folio con el segmento `DEN` y promete plazos, mientras el documento 03 recomienda configurarlo como reporte ciudadano. Nada que se redacte antes de resolver esto es definitivo.

### 4.2 Nivel 2 · Bloquea la publicación

1. **El aviso de privacidad** (P-02, P-19). Faltan el nombre e inscripción del sistema de datos personales, el ciclo de vida del dato conforme al catálogo de disposición documental, el catálogo de transferencias, los datos de la Unidad de Transparencia y el artículo del Reglamento Interior que atribuye la función. **No es tarea del equipo que construye el formulario.**
2. **El cauce escrito de remisión** a la PROFEPA y a la Procuraduría. El formulario recibe, emite folio y anuncia que remitirá. Si el cauce no existe, la denuncia se queda en la Secretaría con constancia de la recepción y de la promesa. Es requisito de publicación, no mejora.
3. **Los fundamentos de las materias.** Doce de los diecisiete que el formulario muestra no tienen respaldo documental declarado. Las tres citas penales quedaron verificadas; las demás, no. El criterio de salida 1 de la fase 1 exige esa verificación, y **el acta de validación no debería firmarse antes**, porque convertiría en certificación institucional lo que hoy es una verificación incompleta.
4. **Domicilios y datos de contacto** de las dos unidades, de la Oficialía de Partes y de las siete instancias de derivación (P-08, P-09).
5. **Activar la obligatoriedad de campos** (RN-30). Hoy el formulario se puede recorrer y enviar vacío.

### 4.3 Riesgos que no estaban nombrados en ningún documento

Los recoge la revisión jurídica y ninguno tiene decisión tomada. Se enuncian sin resolverlos, que es lo que corresponde:

- **Metadatos de las fotografías.** El formulario pide expresamente no editarlas «para conservar la fecha y la ubicación con que fueron tomadas», y ningún documento trata esos metadatos como dato personal. En la ruta anónima, una fotografía tomada desde la ventana de quien denuncia lleva su domicilio dentro del archivo.
- **Datos de terceros señalados.** Se recaban nombre, señas, domicilio y área de alguien sobre quien se formula un señalamiento no acreditado. El aviso que el ciudadano lee no los menciona, y no está definido qué versión del expediente se entrega al emplazarlo.
- **El consentimiento y la protesta de decir verdad** van en una sola casilla. Son actos de naturaleza distinta y el consentimiento debe poder revocarse por separado.
- **El borrador** queda catorce días en el navegador, con todo lo capturado, sin declararlo. En un equipo compartido, cualquiera lo recupera —incluida la denuncia anónima—.
- **La dirección de red** que el control de abuso necesita registrar es un dato personal y no está en el catálogo ni en el aviso.
- **El rango «Menor de 18 años»** existe y no hay ninguna previsión sobre consentimiento ni interés superior.
- **La vista al Órgano Interno de Control** cuando se señala a una persona servidora pública. El formulario capta el señalamiento y la ruta prevista es la recomendación del artículo 331.
- **Registro del trámite y publicación** conforme al régimen que corresponda. Sustituir un formato público por un formulario en línea probablemente lo exige, y omitirlo obliga a retirar lo ya publicado.
- **Régimen archivístico** del expediente electrónico: sin él no puede contestarse cuánto se conservan los datos, que es justamente el rubro en blanco del aviso.
- **Continuidad del proyecto.** El repositorio vive en una cuenta cuya titularidad institucional está sin resolver y el respaldo depende de la sincronización de una carpeta. Hoy el proyecto no sobrevive a la salida de quien lo dirige.

### 4.4 Las nueve áreas que no han sido consultadas

Unidad de Transparencia · unidad jurídica de la Secretaría · DGCORENADR · Dirección Regional Centro y Eje Neovolcánico de la CONANP · Órgano Interno de Control · Agencia Digital de Innovación Pública · Procuraduría Ambiental y del Ordenamiento Territorial · PROFEPA · INVEA.

---

## 5. Recomendación para la sesión con las Direcciones Generales

Que la sesión se estructure alrededor de **tres resoluciones** y no del recorrido del formulario:

**Primero.** P-01, naturaleza jurídica del canal, con la unidad jurídica presente. Es el nudo del que cuelga todo lo demás.

**Segundo.** P-22 junto con P-04 y RN-07 como un solo punto: la competencia en las Áreas Naturales Protegidas federales y en las superficies con decreto federal y local concurrente.

**Tercero.** El cauce escrito de remisión a la PROFEPA y a la Procuraduría, sin el cual el canal promete lo que no puede cumplir.

**Cuarto.** Antes de esa sesión, completar la verificación de los doce fundamentos de materia que siguen sin respaldo declarado. El acta de validación no se firma mientras eso no esté hecho.

---

## 6. Estado de la verificación automática

| | |
|---|---|
| Baterías | 14 |
| Comprobaciones | 381 |
| Campos del catálogo | 53 |
| Datos personales | 21 (40 %) |
| Campos sin uso declarado | 0 |
| Documentos generados del prototipo | 09 y 10 |
