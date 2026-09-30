# Formulario web de Denuncia Ambiental · Mapeo de campos, obligatoriedad y uso declarado

**Versión:** DEC-144 · 30 de septiembre de 2026
**Generado automáticamente** del catálogo `OBLIG` del prototipo, que es la única fuente de verdad: gobierna la marca de opcionalidad en pantalla, la validación y este documento. Si algo aquí no coincide con el formulario, el error está en el generador, no en los datos.

**Para qué sirve.** Declara, campo por campo, **quién usa el dato y para qué**. Responde a la exigencia de minimización —no se recaba un dato para el que no exista un uso declarado— y es el insumo con el que la Unidad de Transparencia redacta el aviso de privacidad.

| | |
|---|---|
| Campos que llena la persona | **61** |
| Datos que viajan a la base sin verse en pantalla | **13** |
| Datos que calcula el formulario y se muestran | 14 |
| Datos personales | **24** (39 %) |
| Obligatorios en este formulario | 26 de 61 |
| Campos con obligatoriedad condicionada | 25 |
| Datos sin uso declarado | **0** |

---

## 1. Finalidades

Todo dato recabado o calculado sirve a una de estas finalidades. Ninguna otra.

| Finalidad | Para qué | Datos |
|---|---|---|
| **Competencia** | Determinar la competencia y turnar al área que atiende | 17 |
| **Localización** | Localizar y caracterizar el sitio para la visita de inspección | 17 |
| **Expediente** | Integrar el expediente y motivar el acto de inspección | 19 |
| **Responsable** | Identificar y emplazar al probable infractor | 9 |
| **Identificación** | Determinar cómo se identifica quien denuncia y qué seguimiento admite | 1 |
| **Contacto** | Identificar, notificar y dar seguimiento con la persona denunciante | 18 |
| **Cumplimiento** | Dejar constancia del consentimiento y de la vía elegida | 2 |
| **Estadística** | Conocer quién denuncia, sin formar parte del expediente | 5 |

---

## 2. Campos que llena la persona, por paso

**Dato personal** marca los datos de una persona física identificada o identificable, sea la persona denunciante o un tercero señalado. **Obligatorio *(condicionado)*** significa que el campo sólo se exige en la situación que indica la última columna; fuera de ella no se pide ni se marca.

### Paso 1 · Qué denuncias

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| Materia de la denuncia | Obligatorio | No | Siempre | Determina la competencia de la Secretaría y el fundamento que se invoca; alimenta la estadística por materia. |

### Paso 2 · Dónde ocurre

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| ¿El lugar tiene calle y número? | Obligatorio | No | Siempre | Pregunta de encaminamiento, no un dato del expediente: decide cómo se captura el lugar y por eso debe responderse. Una parte de las denuncias ocurre en bosques, áreas naturales, barrancas, caminos o canales, donde no existe domicilio y exigirlo impide presentar la denuncia. |
| Ubicación pegada: enlace, coordenadas o código de lugar | Opcional | No | Siempre | Vía de captura, no dato del expediente: de lo pegado se extrae la coordenada y lo que se conserva es el punto. Sustituye a la detección de ubicación del dispositivo, que se retiró. |
| Punto en el mapa | Obligatorio *(condicionado)* | **Sí** | Obligatorio sólo cuando el lugar no tiene dirección; con dirección, si no se marca, la Secretaría ubica el lugar a partir de ella | Resuelve por cruce espacial el área que atiende y permite al personal inspector llegar al sitio. El art. 282 de la Ley Ambiental admite identificar el lugar por coordenadas. Con dirección es opcional: quien no sabe usar un mapa no puede quedarse sin denunciar; entonces la Secretaría ubica el lugar con la dirección y el turnado espera a ese paso (DEC-123). |
| Alcaldía de la dirección | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Parte del domicilio del lugar en la orden de visita y filtro del catálogo de colonias: sólo se ofrecen las de la alcaldía elegida. **No decide el turnado**: quién atiende lo sigue resolviendo la alcaldía del punto (DEC-72). Si no coinciden, el formulario lo avisa y el expediente lo marca (DEC-118). |
| Colonia | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Localización del sitio y estadística territorial. |
| Código postal | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Localización del sitio; verifica la congruencia de la dirección capturada. Se escribe a mano y se admite sólo en el intervalo de la Ciudad, del 01000 al 16999 (DEC-117). |
| Calle o vialidad | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Domicilio del lugar de los hechos en la orden de visita (art. 281). |
| Número exterior | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Precisa el predio en la orden de visita. Obligatorio cuando el lugar tiene dirección; si el predio no tiene número se escribe «S/N», que es una respuesta válida (DEC-120). |
| Entre qué calles | Opcional | No | Siempre | Permite ubicar el predio cuando no hay número visible. |
| ¿El predio se identifica por manzana y lote? | Opcional | No | Sólo cuando el lugar tiene calle y número | Pregunta de encaminamiento, no dato del expediente: muestra manzana y lote sólo a quien los tiene, en vez de enseñárselos a todos (DEC-124). |
| Manzana | Opcional | No | Sólo cuando el predio se identifica por manzana y lote | Identifica el predio en la orden de visita donde no hay número exterior y la referencia usual es manzana y lote. |
| Lote | Opcional | No | Sólo cuando el predio se identifica por manzana y lote | Identifica el predio en la orden de visita donde no hay número exterior y la referencia usual es manzana y lote. |
| Nombre del lugar | Obligatorio *(condicionado)* | No | Sólo cuando el lugar no tiene calle ni número | Sustituye al domicilio en la orden de visita cuando el sitio no lo tiene. Se propone desde la capa oficial que contiene el punto. |
| Cómo se reconoce y cómo se llega al sitio | Obligatorio *(condicionado)* | No | Obligatorio sólo cuando el lugar no tiene calle ni número; en los demás casos se pide como dato opcional | Reúne en un solo campo lo que antes se preguntaba dos veces —cómo se ve el sitio y cómo se accede a él—. Sin domicilio es lo único que permite al personal de inspección llegar, y por eso ahí se exige. |

### Paso 3 · Qué ocurre

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| ¿Es transporte público o de carga? | Obligatorio *(condicionado)* | No | Sólo cuando se denuncia un vehículo contaminante | Distingue el transporte concesionado de pasajeros y el de carga del vehículo particular. El cauce de atención de cada uno con la Secretaría de Movilidad está por definirse: el dato se recoge desde ahora para no tener que volver a pedirlo. |
| ¿Los hechos ocurren dentro de un establecimiento? | Opcional | No | Siempre | Caracteriza el sitio como fuente fija y propone al establecimiento como responsable. Se pregunta junto a la identificación del responsable, que es lo que determina. |
| Tipo de establecimiento | Opcional | No | Sólo cuando los hechos ocurren dentro de un establecimiento | Prepara la visita —qué se va a inspeccionar— y alimenta la estadística por tipo de fuente. |
| Tipo de establecimiento, si es otro | Opcional | No | Sólo cuando el giro elegido es «Otro» | Especifica el giro que no está en la lista (DEC-143: faltaba en el mapeo). |
| Nombre del establecimiento | Opcional | No | Sólo cuando los hechos ocurren dentro de un establecimiento | Identifica el establecimiento en campo y permite cruzarlo con el padrón de fuentes fijas. |
| Descripción de lo que ocurre | Obligatorio | No | Siempre | Objeto y alcance de la visita de inspección; es la base de la motivación del acto. |
| Desde cuándo ocurre | Opcional | No | Siempre | Determina si la conducta es continua o aislada, lo que define la urgencia de la atención. |
| Fecha en que ocurrió o inició | Opcional | No | Siempre | Ubicación temporal de los hechos en el expediente. |
| ¿Quién es responsable de los hechos? | Opcional | No | Siempre | Define la vía del procedimiento: señalar a una autoridad activa el art. 331, que manda recomendar y no sancionar. |
| Ámbito de la autoridad señalada | Opcional | No | Sólo cuando se señala a una autoridad | Encamina la recomendación del art. 331: de él depende si se dirige a una dependencia de la Ciudad, a una alcaldía o a la federación, y contra qué catálogo se propone el nombre. |
| Dependencia, alcaldía u organismo señalado | Opcional | No | Sólo cuando se señala a una autoridad y se eligió su ámbito | Destinataria de la recomendación del art. 331. Se propone sobre el catálogo del ámbito elegido, que acepta la sigla. |
| Nombre de la persona o del negocio | Opcional | **Sí** | Siempre | Emplazamiento del probable infractor (art. 289). |
| Cómo se identifica al responsable | Opcional | **Sí** | Siempre | Identificación del responsable en campo cuando no se conoce su nombre. |
| Persona encargada o representante | Opcional | **Sí** | Siempre | Persona con quien se entiende la diligencia (art. 283). |
| Área o persona servidora pública | Opcional | **Sí** | Siempre | Precisa el área a la que se dirige la recomendación. |
| Número de obra, contrato o permiso | Opcional | No | Siempre | Permite requerir el expediente de la obra pública señalada. |
| Razón social del establecimiento | Opcional | No | Sólo cuando se denuncia a una empresa o establecimiento | Razón social del probable infractor para el emplazamiento y el cruce con licencias. |
| ¿Sabes algo sobre los permisos? | Opcional | No | Siempre | Filtra la pregunta larga: sólo se pide el detalle a quien tiene algo que aportar. |
| Permisos o autorizaciones | Opcional | No | Sólo cuando la persona dice saber algo sobre los permisos | Orienta la verificación documental: si existe autorización y si la obra se ajusta a sus términos. |
| ¿Ya reportaste ante otra autoridad? | Opcional | No | Siempre | Detecta reincidencia y evita duplicar expedientes con otra autoridad; filtra la pregunta larga. |
| Gestiones previas | Opcional | No | Sólo cuando la persona dice haberlo reportado antes | Evita duplicar expedientes con otras autoridades y gradúa la gravedad por reincidencia. |

### Paso 4 · Pruebas

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| Fotos, videos o documentos | Opcional | **Sí** | Siempre | Elementos probatorios que sustentan la presunción fundada del art. 280. |
| Otras pruebas que puedas ofrecer | Opcional | No | Siempre | Describe pruebas que la persona no puede adjuntar pero puede ofrecer. |

### Paso 5 · Tus datos

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| Cómo se presenta la denuncia | Obligatorio | No | Siempre | Determina qué datos se piden y qué seguimiento es posible. Con datos escritos hay nombre y contacto; la anónima no lleva nombre y sólo admite avisos si la persona deja un correo (DEC-119). En las tres rutas los datos son confidenciales frente a la persona denunciada. |
| Nombre(s) | Obligatorio | **Sí** | Siempre | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido paterno | Obligatorio | **Sí** | Siempre | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido materno | Opcional | **Sí** | Siempre | Completa la identificación en el registro administrativo. |
| Teléfono | Obligatorio | **Sí** | Siempre | Contacto para aclarar datos o coordinar el acceso al sitio durante la visita. No es vía de notificación. En la denuncia anónima se ofrece como opcional (DEC-119). |
| Correo electrónico | Obligatorio | **Sí** | Siempre | Contacto por escrito: la Secretaría puede escribir para aclarar datos o informar el trámite. No hay envío automático de correos (DEC-134). En la denuncia anónima también es obligatorio: es la única forma de contactar a quien no da su nombre (DEC-119, DEC-120). |
| Vivo fuera de la Ciudad de México | Opcional | No | Siempre | Casilla de encaminamiento: cambia alcaldía y colonia del catálogo por entidad federativa, municipio y colonia escrita, y admite cualquier código postal (DEC-136). |
| Domicilio · calle | Obligatorio | **Sí** | Siempre | Notificación por domicilio: es la vía para notificar las actuaciones (DEC-134). |
| Domicilio · número exterior | Obligatorio | **Sí** | Siempre | Notificación por domicilio: es la vía para notificar las actuaciones (DEC-134). |
| Domicilio · número interior | Opcional | **Sí** | Siempre | Notificación por domicilio: es la vía para notificar las actuaciones (DEC-134). |
| ¿El domicilio se identifica por manzana y lote? | Opcional | No | Siempre | Pregunta de encaminamiento, no dato del expediente: muestra manzana y lote sólo a quien los tiene (DEC-135). |
| Domicilio · manzana | Opcional | **Sí** | Sólo cuando el domicilio se identifica por manzana y lote | Precisa el domicilio de notificación donde no hay número exterior (DEC-135). |
| Domicilio · lote | Opcional | **Sí** | Sólo cuando el domicilio se identifica por manzana y lote | Precisa el domicilio de notificación donde no hay número exterior (DEC-135). |
| Domicilio · entre qué calles | Opcional | **Sí** | Siempre | Ayuda a quien notifica a encontrar el domicilio (DEC-135). |
| Domicilio · colonia | Obligatorio | **Sí** | Siempre | Notificación por domicilio: es la vía para notificar las actuaciones (DEC-134). |
| Domicilio · código postal | Obligatorio | **Sí** | Siempre | Notificación por domicilio: es la vía para notificar las actuaciones (DEC-134). |
| Domicilio · alcaldía | Obligatorio *(condicionado)* | **Sí** | Sólo cuando el domicilio está en la Ciudad de México | Notificación por domicilio. Se elige de la lista de las dieciséis alcaldías y acota las colonias que se ofrecen (DEC-135). |
| Domicilio · entidad federativa | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona vive fuera de la Ciudad de México | Notificación por domicilio fuera de la Ciudad. Se elige de la lista de las otras treinta y una entidades (DEC-136). |
| Domicilio · municipio | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona vive fuera de la Ciudad de México | Notificación por domicilio fuera de la Ciudad (DEC-136). |
| Género | Opcional | **Sí** | Siempre | Desagregación estadística de quién denuncia en la Ciudad. Opcional; no condiciona el trámite ni se incorpora al expediente. La identidad de género es dato sensible: sólo puede tratarse con consentimiento expreso, y por eso la pregunta admite no responder. |
| Rango de edad | Opcional | **Sí** | Siempre | Desagregación estadística por edad. Opcional; no condiciona el trámite ni se incorpora al expediente. |
| Protesta de decir verdad y aviso de privacidad | Obligatorio | No | Siempre | Constancia del consentimiento informado y de la protesta de decir verdad. |

### Paso 6 · Revisión

| Campo | Obligatorio | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|
| Prueba de humanidad | Obligatorio | No | Siempre | Impide el envío automatizado masivo. La comprobación la resuelve el servidor; no identifica a la persona ni se incorpora al expediente. |

---

## 2 bis. Campos que viajan a la base y no se ven en pantalla

Los calcula el formulario: la persona no los escribe ni los ve, pero llegan al expediente. Se declaran en `OBLIG` (marcados `oculto`) o en `DERIVADOS`, y una prueba exige que toda clave que el código guarda esté declarada en alguno de los dos o en `INTERNOS` (DEC-128).

**Por denuncia**

| Dato | Clave | Quién lo pone | Dato personal | Para qué sirve |
|---|---|---|---|---|
| Origen de la ubicación | `ubicacion_origen` | Lo pone el formulario al enviar, «punto» si la persona lo marcó o «dirección» si la Secretaría debe ubicar el lugar | No | Separa las denuncias que llegan con punto de las que hay que ubicar con la dirección antes de turnarlas; alimenta la bandeja «por ubicar» del módulo interno (DEC-123). |
| Clave de la colonia (IECM) | `colonia_cve` | La pone el catálogo cuando la persona elige su colonia de la lista | No | Clave CVEUT de la unidad territorial del IECM 2022. Agrupa las denuncias por colonia sin depender de cómo se escribió el nombre. Queda vacía cuando la persona escribe una colonia que no está en el catálogo: el nombre se conserva igual (DEC-117). |
| Celda UGA | `uga` | La asigna el punto del mapa | No | Celda de la malla hexagonal del Sistema de Información Ambiental (~1 km²) en la que cae el punto. No se muestra a la persona: queda en el expediente para la programación de operativos y la estadística territorial. Es provisional: el servidor la vuelve a derivar con la capa completa y guarda la versión de la malla (DEC-117). |
| Clave del área que atiende | `dg` | Regla de turnado, a partir del tipo de zona | No | DGIVA, DGCORENADR o FEDERAL: enruta la denuncia en el módulo interno y arma el folio. |
| ANP federal coadministrada | `coadmin` | Catálogo del convenio CONANP-CDMX | No | Marca si la Secretaría coadministra el ANP federal del punto; cambia el texto del turnado. |
| Versión de la malla UGA | `uga_version` | Catálogo UGA incrustado | No | Con qué versión de la malla se asignó la celda; el servidor la vuelve a derivar con la más reciente. |

**Por cada foto adjunta**

| Dato | Clave | Quién lo pone | Dato personal | Para qué sirve |
|---|---|---|---|---|
| Huella SHA-256 del original | `sha256_original` | La foto, antes de optimizarla | No | Permite comprobar después que el original que presente la persona es el mismo (DEC-121). |
| Fecha de captura de la foto | `fecha_captura` | Metadatos de la foto (EXIF) | No | Cuándo se tomó la foto; es parte de la prueba y se pierde al optimizarla. |
| Latitud donde se tomó la foto | `lat_captura` | Metadatos de la foto (EXIF) | **Sí** | Dónde se tomó la foto; lo dice el aviso de privacidad (DEC-121). |
| Longitud donde se tomó la foto | `lon_captura` | Metadatos de la foto (EXIF) | **Sí** | Dónde se tomó la foto; lo dice el aviso de privacidad (DEC-121). |
| Dimensiones de la foto optimizada | `dimensiones` | La optimización | No | Ancho y alto en píxeles de lo que se guarda. |
| Foto optimizada | `optimizada` | La optimización | No | Si la foto se optimizó o entró el original. |
| Formato de la foto guardada | `tipo` | La optimización | No | Formato con el que se guarda la foto optimizada (JPG). |

### Datos que calcula el formulario y se muestran como información

Tampoco los escribe la persona: se le enseñan en la ficha del mapa, en la revisión o en el acuse.

**Por denuncia**

| Dato | Clave | Quién lo pone | Dato personal | Para qué sirve |
|---|---|---|---|---|
| Alcaldía | `alcaldia` | La determina el punto del mapa | No | Turnado, programación de operativos y estadística territorial. **No se captura**: la determina el cruce del punto contra la capa de alcaldías, que es el mismo dato con el que se resuelve el turnado, de modo que el acuse y el expediente no pueden contradecirse. La dirección lleva además su propia alcaldía (`alcaldia_dir`, DEC-118), que **no la sustituye**. |
| Alcaldía de la dirección distinta de la del punto | `alcaldia_discrepa` | La calcula el formulario al comparar las dos alcaldías | No | Marca para quien recibe la denuncia: la dirección y el punto no están en la misma alcaldía. No impide enviar, porque cerca del límite puede no haber error; sí obliga a mirar antes de programar la visita (DEC-118). |
| Longitud del punto | `lon` | El punto del mapa, junto con la latitud | **Sí** | Con la latitud, ubica el sitio para el cruce de capas y la visita. |
| Tipo de zona | `capa_clase` | Cruce del punto con las capas del SIA | No | Suelo urbano, suelo de conservación o Área Natural Protegida: decide qué área atiende. |
| Tipo de suelo | `capa_tipo` | Cruce del punto con las capas del SIA | No | Resumen del tipo de suelo que se muestra en la revisión y viaja al expediente. |
| Categoría de la zona | `capa_categoria` | Cruce del punto con las capas del SIA | No | Categoría del Área Natural Protegida o de Valor Ambiental en la que cae el punto. |
| Área identificada | `capa_nombre` | Cruce del punto con las capas del SIA | No | Nombre del área protegida en la que cae el punto; precisa el lugar en la orden de visita. |
| Área que atiende | `dg_nombre` | Regla de turnado | No | Nombre del área que atiende, como se dice en la ficha, la revisión y el acuse. |
| Razón del turnado | `dg_razon` | Regla de turnado | No | Explica por qué la atiende otra autoridad cuando el punto cae en un Área Natural Protegida federal. |
| Área protegida local concurrente | `concurrencia` | Cruce del punto con las capas del SIA | No | Cuando el punto cae a la vez en un ANP federal y en una local: abre la vía de intervención local. |
| Punto fuera de la Ciudad | `fuera` | Cruce del punto con el límite de la Ciudad | No | Detiene la denuncia: la Secretaría sólo atiende hechos dentro de la Ciudad. |
| Folio | `folio` | El sistema, al enviar | No | Identifica la denuncia en el acuse, en el módulo interno y en la consulta de seguimiento. |
| Fecha y hora de recepción | `fecha_acuse` | El sistema, al enviar | No | Fecha y hora en que la denuncia entra al expediente. |

**Por cada foto adjunta**

| Dato | Clave | Quién lo pone | Dato personal | Para qué sirve |
|---|---|---|---|---|
| Peso original de la foto | `size_original` | La foto, al adjuntarla | No | Se muestra junto al peso optimizado; deja constancia de la optimización. |

---
## 3. Hallazgos de la revisión de minimización

**Ningún campo carece de uso.** Los cincuenta y tres tienen una finalidad verificable. No hay campos «por si acaso» que retirar. Lo que sí hay son tres ajustes.

**H-01 · El teléfono es obligatorio y no es vía de notificación.**
En los dos esquemas el teléfono aparece como obligatorio. Su uso real —contacto para aclarar un dato o coordinar el acceso al sitio durante la visita— es operativo, no procesal: la notificación se practica por correo electrónico o por domicilio, nunca por teléfono. Un dato personal que no sostiene ninguna actuación formal no debería condicionar la presentación de la denuncia.
**Propuesta:** volverlo opcional, con la ayuda «agiliza la visita si el personal necesita confirmar algo contigo». **Decisión de la Dirección General.**

**H-02 · Seis campos contienen datos personales de terceros.**
Nombre, señas, domicilio y persona encargada del presunto responsable, el área o persona servidora pública señalada, y las personas señaladas como responsables en el esquema vigente. Son datos de personas que **no dieron su consentimiento** y sobre las que se formula un señalamiento aún no acreditado. Su tratamiento es legítimo —el emplazamiento del probable infractor lo exige el procedimiento de inspección—, pero es de otra naturaleza que el de la persona denunciante.
**Consecuencias que deben quedar escritas:** el aviso de privacidad tiene que mencionarlos expresamente; no se publican ni se entregan nunca en versión pública; y su conservación se rige por la vida del expediente, no por la del registro de contacto.

**H-03 · La coordenada del sitio es un dato personal cuando los hechos ocurren en un domicilio.**
Está marcada como tal en el catálogo. Obliga a definir —antes del primer dato real— quién ve la coordenada exacta y qué se publica: agregado por colonia, centroide, o nada. Un mapa público de puntos de denuncia puede identificar tanto a quien denuncia como a quien es denunciado.

**H-04 · Retirado: el domicilio de la empresa denunciada.**
Aplicando el criterio de esta misma revisión, se eliminó el campo de domicilio en el bloque de empresa: la razón social más el lugar de los hechos bastan para el emplazamiento, y es un dato que quien denuncia rara vez conoce. Se conserva en el bloque de persona física —«dónde se le localiza»—, donde sí aporta: ahí puede ser el único modo de ubicar al responsable.

**H-05 · Dos preguntas largas quedaron tras una pregunta filtro.**
Permisos y gestiones previas eran campos de texto abiertos que la mayoría de las personas deja vacíos, y que ocupaban espacio y atención en la pantalla. Ahora van precedidos de una pregunta de sí o no, y el campo sólo aparece a quien tiene algo que aportar. La respuesta misma es información: saber que alguien **ya reportó ante otra autoridad** distingue el caso, aunque no detalle cuál.

---

## 4. Lo que ya cumple

**El domicilio de notificación sólo se pide cuando hace falta.** Los siete campos de domicilio se omiten cuando la persona acepta la notificación por correo electrónico (DEC-48). Medido en el formulario: el paso 5 muestra siete controles cuando se acepta el correo y catorce cuando se rechaza. Es minimización efectiva, y la mitad de lo que el formulario pregunta en ese paso depende de una sola respuesta.

**La denuncia anónima no pide ningún dato de contacto.** Los campos del paso 5 quedan fuera de la validación cuando se elige esa vía.

---

## 5. Interruptor de obligatoriedad

Mientras el formulario está en revisión, **ningún campo es obligatorio**: se puede recorrer completo y enviarlo vacío. La obligatoriedad se activa desde el panel de validación. **Debe quedar activa antes de la publicación.**

Hay una sola lista de campos obligatorios, la de la columna «Obligatorio» (DEC-97). La columna «Formato 2016» registra qué pedía la Ficha de Denuncia en papel y no gobierna nada: se conserva para poder responder, ante quien lo pregunte, qué dato se dejó de exigir y cuál se agregó.
