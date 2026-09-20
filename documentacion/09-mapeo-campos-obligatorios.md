# Formulario web de Denuncia Ambiental · Mapeo de campos, obligatoriedad y uso declarado

**Versión:** 3.0 · 20 de septiembre de 2026
**Generado automáticamente** del catálogo `OBLIG` del prototipo, que es la única fuente de verdad: gobierna la marca de opcionalidad en pantalla, la validación y este documento. Si algo aquí no coincide con el formulario, el error está en el generador, no en los datos.

**Para qué sirve.** Declara, campo por campo, **quién usa el dato y para qué**. Responde a la exigencia de minimización —no se recaba un dato para el que no exista un uso declarado— y es el insumo con el que la Unidad de Transparencia redacta el aviso de privacidad.

| | |
|---|---|
| Campos del formulario | **52** |
| Datos personales | **20** (38 %) |
| Obligatorios · esquema DGIVA | 23 de 52 |
| Obligatorios · formato vigente | 29 de 52 |
| Campos con obligatoriedad condicionada | 19 |
| Campos sin uso declarado | **0** |

---

## 1. Finalidades

Todo dato recabado sirve a una de estas finalidades. Ninguna otra.

| Finalidad | Para qué | Campos |
|---|---|---|
| **Competencia** | Determinar la competencia y turnar al área que atiende | 4 |
| **Localización** | Localizar y caracterizar el sitio para la visita de inspección | 13 |
| **Expediente** | Integrar el expediente y motivar el acto de inspección | 10 |
| **Responsable** | Identificar y emplazar al probable infractor | 10 |
| **Identificación** | Determinar cómo se identifica quien denuncia y qué seguimiento admite | 1 |
| **Contacto** | Identificar, notificar y dar seguimiento con la persona denunciante | 12 |
| **Cumplimiento** | Dejar constancia del consentimiento y de la vía elegida | 2 |

---

## 2. Campos, por paso

**Dato personal** marca los datos de una persona física identificada o identificable, sea la persona denunciante o un tercero señalado. **Obligatorio *(condicionado)*** significa que el campo sólo se exige en la situación que indica la última columna; fuera de ella no se pide ni se marca.

### Paso 1 · Qué denuncias

| Campo | DGIVA | Vigente | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|---|
| Materia de la denuncia | Obligatorio | Obligatorio | No | Siempre | Determina la competencia de la Secretaría y el fundamento que se invoca; alimenta la estadística por materia. |

### Paso 2 · Dónde ocurre

| Campo | DGIVA | Vigente | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|---|
| ¿El lugar tiene calle y número? | Obligatorio | Obligatorio | No | Siempre | Pregunta de encaminamiento, no un dato del expediente: decide cómo se captura el lugar y por eso debe responderse. Una parte de las denuncias ocurre en bosques, áreas naturales, barrancas, caminos o canales, donde no existe domicilio y exigirlo impide presentar la denuncia. |
| Coordenadas o enlace de mapa pegados | Opcional | Opcional | No | Siempre | Vía de captura, no dato del expediente: de lo pegado se extrae la coordenada y lo que se conserva es el punto. Sustituye a la detección de ubicación del dispositivo, que se retiró. |
| Confirmación del punto | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Sólo cuando ya hay un punto colocado | El punto se arrastra, y un roce basta para moverlo. Como de esa coordenada depende el área que atiende la denuncia, se pide confirmarla; cualquier movimiento posterior borra la confirmación. |
| Punto en el mapa | Obligatorio | Obligatorio | **Sí** | Siempre | Resuelve por cruce espacial el área que atiende y permite al personal inspector llegar al sitio. El art. 282 de la Ley Ambiental admite identificar el lugar por coordenadas. |
| Alcaldía | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | No se pregunta: la determina el punto del mapa | Turnado, programación de operativos y estadística territorial. **No se captura**: la determina el cruce del punto contra la capa de alcaldías, que es el mismo dato con el que se resuelve el turnado, de modo que el acuse y el expediente no pueden contradecirse. |
| Colonia | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Localización del sitio y estadística territorial. |
| Código postal | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Localización del sitio; verifica la congruencia de la dirección capturada. |
| Calle o vialidad | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Sólo cuando el lugar tiene calle y número | Domicilio del lugar de los hechos en la orden de visita (art. 281). |
| Número exterior | Opcional | Opcional | No | Siempre | Precisa el predio en la orden de visita. |
| Entre calle 1 | Opcional | Opcional | No | Siempre | Permite ubicar el predio cuando no hay número visible. |
| Entre calle 2 | Opcional | Opcional | No | Siempre | Permite ubicar el predio cuando no hay número visible. |
| Nombre del lugar | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Sólo cuando el lugar no tiene calle ni número | Sustituye al domicilio en la orden de visita cuando el sitio no lo tiene. Se propone desde la capa oficial que contiene el punto. |
| Cómo se reconoce y cómo se llega al sitio | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | No | Obligatorio sólo cuando el lugar no tiene calle ni número; en los demás casos se pide como dato opcional | Reúne en un solo campo lo que antes se preguntaba dos veces —cómo se ve el sitio y cómo se accede a él—. Sin domicilio es lo único que permite al personal de inspección llegar, y por eso ahí se exige. |

### Paso 3 · Qué ocurre

| Campo | DGIVA | Vigente | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|---|
| ¿Los hechos ocurren dentro de un establecimiento? | Opcional | Opcional | No | Siempre | Caracteriza el sitio como fuente fija y propone al establecimiento como responsable. Se pregunta junto a la identificación del responsable, que es lo que determina. |
| Tipo de establecimiento | Opcional | Opcional | No | Sólo cuando los hechos ocurren dentro de un establecimiento | Prepara la visita —qué se va a inspeccionar— y alimenta la estadística por tipo de fuente. |
| Nombre del establecimiento | Opcional | Opcional | No | Sólo cuando los hechos ocurren dentro de un establecimiento | Identifica el establecimiento en campo y permite cruzarlo con el padrón de fuentes fijas. |
| Descripción de lo que ocurre | Obligatorio | Obligatorio | No | Siempre | Objeto y alcance de la visita de inspección; es la base de la motivación del acto. |
| Desde cuándo ocurre | Opcional | Obligatorio | No | Siempre | Determina si la conducta es continua o aislada, lo que define la urgencia y el cómputo del plazo. |
| Fecha en que ocurrió o inició | Opcional | Obligatorio | No | Siempre | Cómputo del plazo de presentación y ubicación temporal de los hechos en el expediente. |
| Hora aproximada | Opcional | Opcional | No | Siempre | Programar la visita en el horario en que la conducta ocurre; sin este dato la visita puede no encontrar nada. |
| ¿Quién es responsable de los hechos? | Opcional | Opcional | No | Siempre | Define la vía del procedimiento: señalar a una autoridad activa el art. 331, que manda recomendar y no sancionar. |
| Dependencia, alcaldía u organismo señalado | Opcional | Opcional | No | Siempre | Destinataria de la recomendación del art. 331. |
| Nombre de la persona o del negocio | Opcional | Opcional | **Sí** | Siempre | Emplazamiento del probable infractor (art. 289). |
| Cómo se identifica al responsable | Opcional | Opcional | **Sí** | Siempre | Identificación del responsable en campo cuando no se conoce su nombre. |
| Dónde se localiza al responsable | Opcional | Opcional | **Sí** | Siempre | Domicilio para el emplazamiento cuando es distinto del lugar de los hechos. |
| Persona encargada o representante | Opcional | Opcional | **Sí** | Siempre | Persona con quien se entiende la diligencia (art. 283). |
| Área o persona servidora pública | Opcional | Opcional | **Sí** | Siempre | Precisa el área a la que se dirige la recomendación. |
| Número de obra, contrato o permiso | Opcional | Opcional | No | Siempre | Permite requerir el expediente de la obra pública señalada. |
| Razón social del establecimiento | Opcional | Obligatorio *(condicionado)* | No | Sólo cuando se denuncia a una empresa o establecimiento | Razón social del probable infractor para el emplazamiento y el cruce con licencias. |
| Personas señaladas como responsables | Opcional | Obligatorio | **Sí** | Siempre | Personas señaladas como responsables, en el esquema del formato vigente. |
| ¿Sabes algo sobre los permisos? | Opcional | Opcional | No | Siempre | Filtra la pregunta larga: sólo se pide el detalle a quien tiene algo que aportar. |
| Permisos o autorizaciones | Opcional | Obligatorio *(condicionado)* | No | Sólo cuando la persona dice saber algo sobre los permisos | Orienta la verificación documental: si existe autorización y si la obra se ajusta a sus términos. |
| ¿Ya reportaste ante otra autoridad? | Opcional | Opcional | No | Siempre | Detecta reincidencia y evita duplicar expedientes con otra autoridad; filtra la pregunta larga. |
| Gestiones previas | Opcional | Opcional | No | Sólo cuando la persona dice haberlo reportado antes | Evita duplicar expedientes con otras autoridades y gradúa la gravedad por reincidencia. |

### Paso 4 · Pruebas

| Campo | DGIVA | Vigente | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|---|
| Fotos, videos o documentos | Opcional | Obligatorio | **Sí** | Siempre | Elementos probatorios que sustentan la presunción fundada del art. 280. |
| Otras pruebas que puedas ofrecer | Opcional | Opcional | No | Siempre | Describe pruebas que la persona no puede adjuntar pero puede ofrecer. |

### Paso 5 · Tus datos

| Campo | DGIVA | Vigente | Dato personal | Se pide | Uso declarado |
|---|---|---|---|---|---|
| Cómo se presenta la denuncia | Obligatorio | Obligatorio | No | Siempre | Determina qué datos se piden y qué seguimiento es posible. Con cuenta Llave CDMX la identidad queda acreditada, que es lo que da sentido a la reserva de identidad frente a la persona denunciada; con datos escritos hay contacto pero no acreditación; anónima no admite notificación ni aclaraciones. |
| Nombre(s) | Obligatorio | Obligatorio | **Sí** | Siempre | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido paterno | Obligatorio | Obligatorio | **Sí** | Siempre | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido materno | Opcional | Opcional | **Sí** | Siempre | Completa la identificación en el registro administrativo. |
| Teléfono | Obligatorio | Obligatorio | **Sí** | Siempre | Contacto para aclarar datos o coordinar el acceso al sitio durante la visita. No es vía de notificación. |
| Correo electrónico | Obligatorio | Obligatorio | **Sí** | Siempre | Envío del acuse, notificación del avance y consulta del estatus. |
| Domicilio · calle | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · número exterior | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · número interior | Opcional | Opcional | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · colonia | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · código postal | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · alcaldía o municipio | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · entidad federativa | Obligatorio *(condicionado)* | Obligatorio *(condicionado)* | **Sí** | Sólo cuando la persona no acepta la notificación electrónica | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Consentimiento de notificación por correo | Obligatorio | Obligatorio | No | Siempre | Registra la vía de notificación elegida; de ella depende que se pida o no el domicilio. |
| Confidencialidad de los datos | Opcional | Opcional | No | Siempre | Registra si la persona solicita que sus datos no se hagan del conocimiento del denunciado. |

---
## 3. Hallazgos de la revisión de minimización

**Ningún campo carece de uso.** Los cuarenta y siete tienen una finalidad verificable. No hay campos «por si acaso» que retirar. Lo que sí hay son tres ajustes.

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

**El domicilio de notificación sólo se pide cuando hace falta.** Los ocho campos de domicilio son obligatorios en ambos esquemas, pero la validación los omite cuando la persona acepta la notificación por correo electrónico. Verificado en el código. Es minimización efectiva: en la ruta ordinaria, el paso 5 pide seis datos en lugar de diecinueve.

**La denuncia anónima no pide ningún dato de contacto.** Los campos del paso 5 quedan fuera de la validación cuando se elige esa vía.

---

## 5. Interruptor de obligatoriedad

Mientras el formulario está en validación, **ningún campo es obligatorio**: se puede recorrer completo y enviarlo vacío. La obligatoriedad se activa desde el panel de validación, y permite alternar entre el esquema de la Dirección General y el del formato vigente para comparar la carga que impone cada uno. **Debe quedar activa antes de la publicación.**
