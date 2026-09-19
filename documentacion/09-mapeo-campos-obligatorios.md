# Formulario web de Denuncia Ambiental · Mapeo de campos, obligatoriedad y uso declarado

**Versión:** 2.0 · 18 de septiembre de 2026
**Generado automáticamente** del catálogo `OBLIG` del prototipo, que es la única fuente de verdad: gobierna la marca de opcionalidad en pantalla, la validación y este documento. Si algo aquí no coincide con el formulario, el error está en el generador, no en los datos.

**Para qué sirve.** Declara, campo por campo, **quién usa el dato y para qué**. Responde a la exigencia de minimización —no se recaba un dato para el que no exista un uso declarado— y es el insumo con el que la Unidad de Transparencia redacta el aviso de privacidad.

| | |
|---|---|
| Campos del formulario | **47** |
| Datos personales | **20** (43 %) |
| Obligatorios · esquema DGIVA | 19 de 47 |
| Obligatorios · formato vigente | 25 de 47 |
| Campos sin uso declarado | **0** |

---

## 1. Finalidades

Todo dato recabado sirve a una de estas seis finalidades. Ninguna otra.

| Finalidad | Para qué | Campos |
|---|---|---|
| **Competencia** | Determinar la competencia y turnar al área que atiende | 3 |
| **Localización** | Localizar y caracterizar el sitio para la visita de inspección | 11 |
| **Expediente** | Integrar el expediente y motivar el acto de inspección | 8 |
| **Responsable** | Identificar y emplazar al probable infractor | 10 |
| **Contacto** | Identificar, notificar y dar seguimiento con la persona denunciante | 12 |
| **Cumplimiento** | Dejar constancia del consentimiento y de la vía elegida | 3 |

---

## 2. Campos, por paso

**Dato personal** marca los datos de una persona física identificada o identificable, sea la persona denunciante o un tercero señalado.

### Paso 1 · Qué denuncias

| Campo | DGIVA | Vigente | Dato personal | Uso declarado |
|---|---|---|---|---|
| Materia de la denuncia | Obligatorio | Obligatorio | No | Determina la competencia de la Secretaría y el fundamento que se invoca; alimenta la estadística por materia. |

### Paso 2 · Dónde ocurre

| Campo | DGIVA | Vigente | Dato personal | Uso declarado |
|---|---|---|---|---|
| Punto en el mapa | Obligatorio | Obligatorio | **Sí** | Resuelve por cruce espacial el área que atiende y permite al personal inspector llegar al sitio. El art. 282 de la Ley Ambiental admite identificar el lugar por coordenadas. |
| Alcaldía | Obligatorio | Obligatorio | No | Turnado, programación de operativos y estadística territorial. |
| Colonia | Obligatorio | Obligatorio | No | Localización del sitio y estadística territorial. |
| Código postal | Obligatorio | Obligatorio | No | Localización del sitio; verifica la congruencia de la dirección capturada. |
| Calle o vialidad | Obligatorio | Obligatorio | No | Domicilio del lugar de los hechos en la orden de visita (art. 281). |
| Número exterior | Opcional | Opcional | No | Precisa el predio en la orden de visita. |
| Entre calle 1 | Opcional | Opcional | No | Permite ubicar el predio cuando no hay número visible. |
| Entre calle 2 | Opcional | Opcional | No | Permite ubicar el predio cuando no hay número visible. |
| Color o características del sitio | Opcional | Opcional | No | Reconocer el sitio en campo cuando la numeración es ambigua o inexistente. |
| ¿Los hechos ocurren dentro de un establecimiento? | Opcional | Opcional | No | Caracteriza el sitio como fuente fija y determina qué datos de identificación se piden. |
| Tipo de establecimiento | Opcional | Opcional | No | Prepara la visita —qué se va a inspeccionar— y alimenta la estadística por tipo de fuente. |
| Nombre comercial | Opcional | Opcional | No | Identifica el establecimiento en campo y permite cruzarlo con el padrón de fuentes fijas. |
| Otras referencias | Opcional | Opcional | No | Acceso al sitio cuando es de difícil localización. |

### Paso 3 · Qué ocurre

| Campo | DGIVA | Vigente | Dato personal | Uso declarado |
|---|---|---|---|---|
| Descripción de los hechos | Obligatorio | Obligatorio | No | Objeto y alcance de la visita de inspección; es la base de la motivación del acto. |
| Desde cuándo ocurre | Opcional | Obligatorio | No | Determina si la conducta es continua o aislada, lo que define la urgencia y el cómputo del plazo. |
| Fecha en que ocurrió o inició | Opcional | Obligatorio | No | Cómputo del plazo de presentación y ubicación temporal de los hechos en el expediente. |
| Hora aproximada | Opcional | Opcional | No | Programar la visita en el horario en que la conducta ocurre; sin este dato la visita puede no encontrar nada. |
| ¿Quién es responsable de los hechos? | Opcional | Opcional | No | Define la vía del procedimiento: señalar a una autoridad activa el art. 331, que manda recomendar y no sancionar. |
| Dependencia, alcaldía u organismo señalado | Opcional | Opcional | No | Destinataria de la recomendación del art. 331. |
| Nombre de la persona o del negocio | Opcional | Opcional | **Sí** | Emplazamiento del probable infractor (art. 289). |
| Cómo se identifica al responsable | Opcional | Opcional | **Sí** | Identificación del responsable en campo cuando no se conoce su nombre. |
| Dónde se localiza al responsable | Opcional | Opcional | **Sí** | Domicilio para el emplazamiento cuando es distinto del lugar de los hechos. |
| Persona encargada o representante | Opcional | Opcional | **Sí** | Persona con quien se entiende la diligencia (art. 283). |
| Área o persona servidora pública | Opcional | Opcional | **Sí** | Precisa el área a la que se dirige la recomendación. |
| Número de obra, contrato o permiso | Opcional | Opcional | No | Permite requerir el expediente de la obra pública señalada. |
| Razón social del establecimiento | Opcional | Obligatorio | No | Razón social del probable infractor para el emplazamiento y el cruce con licencias. |
| Personas señaladas como responsables | Opcional | Obligatorio | **Sí** | Personas señaladas como responsables, en el esquema del formato vigente. |
| Permisos o autorizaciones | Opcional | Obligatorio | No | Orienta la verificación documental: si existe autorización y si la obra se ajusta a sus términos. |
| Gestiones previas | Opcional | Opcional | No | Evita duplicar expedientes con otras autoridades y gradúa la gravedad por reincidencia. |

### Paso 4 · Pruebas

| Campo | DGIVA | Vigente | Dato personal | Uso declarado |
|---|---|---|---|---|
| Elementos probatorios | Opcional | Obligatorio | **Sí** | Elementos probatorios que sustentan la presunción fundada del art. 280. |
| Otras pruebas | Opcional | Opcional | No | Describe pruebas que la persona no puede adjuntar pero puede ofrecer. |

### Paso 5 · Tus datos

| Campo | DGIVA | Vigente | Dato personal | Uso declarado |
|---|---|---|---|---|
| Nombre(s) | Obligatorio | Obligatorio | **Sí** | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido paterno | Obligatorio | Obligatorio | **Sí** | Identificación de la persona denunciante en el expediente y en el acuse. |
| Apellido materno | Opcional | Opcional | **Sí** | Completa la identificación en el registro administrativo. |
| Teléfono | Obligatorio | Obligatorio | **Sí** | Contacto para aclarar datos o coordinar el acceso al sitio durante la visita. No es vía de notificación. |
| Correo electrónico | Obligatorio | Obligatorio | **Sí** | Envío del acuse, notificación del avance y consulta del estatus. |
| Domicilio · calle | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · número exterior | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · número interior | Opcional | Opcional | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · colonia | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · código postal | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · alcaldía o municipio | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Domicilio · entidad federativa | Obligatorio | Obligatorio | **Sí** | Notificación por domicilio. Sólo se pide si la persona no acepta la notificación electrónica. |
| Consentimiento de notificación por correo | Obligatorio | Obligatorio | No | Registra la vía de notificación elegida; de ella depende que se pida o no el domicilio. |
| Confidencialidad de los datos | Opcional | Opcional | No | Registra si la persona solicita que sus datos no se hagan del conocimiento del denunciado. |
| Protesta de decir verdad y aviso de privacidad | Obligatorio | Obligatorio | No | Constancia del consentimiento informado y de la protesta de decir verdad. |

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

---

## 4. Lo que ya cumple

**El domicilio de notificación sólo se pide cuando hace falta.** Los ocho campos de domicilio son obligatorios en ambos esquemas, pero la validación los omite cuando la persona acepta la notificación por correo electrónico. Verificado en el código. Es minimización efectiva: en la ruta ordinaria, el paso 5 pide seis datos en lugar de diecinueve.

**La denuncia anónima no pide ningún dato de contacto.** Los campos del paso 5 quedan fuera de la validación cuando se elige esa vía.

---

## 5. Interruptor de obligatoriedad

Mientras el formulario está en validación, **ningún campo es obligatorio**: se puede recorrer completo y enviarlo vacío. La obligatoriedad se activa desde el panel de validación, y permite alternar entre el esquema de la Dirección General y el del formato vigente para comparar la carga que impone cada uno. **Debe quedar activa antes de la publicación.**
