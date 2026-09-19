# Formulario web de Denuncia Ambiental · Mapeo de campos obligatorios

**Versión:** 1.0 · 18 de septiembre de 2026
**Generado desde el propio formulario.** La tabla `OBLIG` del prototipo gobierna tres cosas a la vez: la marca «opcional» en pantalla, la validación al continuar y este documento. Cambiar la tabla cambia el formulario completo, de modo que aquí y allá no pueden discrepar.

## Los dos esquemas

| Esquema | Origen | Criterio |
|---|---|---|
| **DGIVA** | Documento «Información básica obligatoria para presentar una denuncia» de la Dirección General | Mínimo: quién denuncia, dónde ocurre y qué ocurre. Lo demás se pide pero no se exige |
| **Formato vigente** | Ficha de Denuncia publicada en el portal | Ampliado: añade momento de los hechos, presuntos responsables, permisos y elementos probatorios |

Cómo probarlos: en el **panel de validación**, esquina inferior derecha del prototipo, se enciende «Exigir los campos obligatorios» y se alterna entre ambos esquemas. El cambio es inmediato, sin recargar. Con la casilla apagada —que es como está entregado— el formulario se recorre y se envía vacío.

---

## Mapeo por paso


### Paso 1 · Qué denuncias

| Campo | Clave | Esquema DGIVA | Formato vigente |
|---|---|---|---|
| Materia de la denuncia | `materia` | **Obligatorio** | **Obligatorio** |

### Paso 2 · Dónde ocurrió

| Campo | Clave | Esquema DGIVA | Formato vigente |
|---|---|---|---|
| Punto en el mapa | `lat` | **Obligatorio** | **Obligatorio** |
| Alcaldía | `alcaldia` | **Obligatorio** | **Obligatorio** |
| Colonia | `colonia` | **Obligatorio** | **Obligatorio** |
| Código postal | `cp` | **Obligatorio** | **Obligatorio** |
| Calle o vialidad | `calle` | **Obligatorio** | **Obligatorio** |
| Número exterior | `num_ext` | Opcional | Opcional |
| Entre calle 1 | `entre_calle1` | Opcional | Opcional |
| Entre calle 2 | `entre_calle2` | Opcional | Opcional |
| Color o características del sitio | `fachada` | Opcional | Opcional |
| ¿Ocurre en un establecimiento? | `es_estab` | Opcional | Opcional |
| Tipo de establecimiento | `tipo_estab` | Opcional | Opcional |
| Nombre comercial | `nombre_estab` | Opcional | Opcional |
| Otras referencias | `referencias` | Opcional | Opcional |

### Paso 3 · Qué ocurrió

| Campo | Clave | Esquema DGIVA | Formato vigente |
|---|---|---|---|
| Descripción de los hechos | `hechos` | **Obligatorio** | **Obligatorio** |
| Desde cuándo ocurre | `temporalidad` | Opcional | **Obligatorio** |
| Fecha en que ocurrió o inició | `fecha_hecho` | Opcional | **Obligatorio** |
| Hora aproximada | `hora_h` | Opcional | Opcional |
| Razón social del establecimiento | `establecimiento` | Opcional | **Obligatorio** |
| Personas señaladas como responsables | `responsables` | Opcional | **Obligatorio** |
| Permisos o autorizaciones | `permisos` | Opcional | **Obligatorio** |
| Gestiones previas | `gestiones` | Opcional | Opcional |

### Paso 4 · Pruebas

| Campo | Clave | Esquema DGIVA | Formato vigente |
|---|---|---|---|
| Elementos probatorios | `archivos` | Opcional | **Obligatorio** |
| Otras pruebas | `otras_pruebas` | Opcional | Opcional |

### Paso 5 · Tus datos

| Campo | Clave | Esquema DGIVA | Formato vigente |
|---|---|---|---|
| Nombre(s) | `nombre` | **Obligatorio** | **Obligatorio** |
| Apellido paterno | `apellido_paterno` | **Obligatorio** | **Obligatorio** |
| Apellido materno | `apellido_materno` | Opcional | Opcional |
| Teléfono | `telefono` | **Obligatorio** | **Obligatorio** |
| Correo electrónico | `correo` | **Obligatorio** | **Obligatorio** |
| Domicilio · calle | `dom_calle` | **Obligatorio** | **Obligatorio** |
| Domicilio · número exterior | `dom_num_ext` | **Obligatorio** | **Obligatorio** |
| Domicilio · número interior | `dom_num_int` | Opcional | Opcional |
| Domicilio · colonia | `dom_colonia` | **Obligatorio** | **Obligatorio** |
| Domicilio · código postal | `dom_cp` | **Obligatorio** | **Obligatorio** |
| Domicilio · alcaldía o municipio | `dom_alcaldia` | **Obligatorio** | **Obligatorio** |
| Domicilio · entidad federativa | `dom_entidad` | **Obligatorio** | **Obligatorio** |
| Protesta de decir verdad y aviso de privacidad | `privacidad` | **Obligatorio** | **Obligatorio** |

---

## Totales

| | Campos obligatorios | De un total de 37 |
|---|---|---|
| Esquema DGIVA | **18** | 49 % |
| Formato vigente | **24** | 65 % |

## Reglas que modifican la obligatoriedad

**Denuncia anónima.** Cuando la persona elige no identificarse, ninguno de los datos de identificación se exige, cualquiera que sea el esquema: `apellido_materno`, `apellido_paterno`, `correo`, `dom_alcaldia`, `dom_calle`, `dom_colonia`, `dom_cp`, `dom_entidad`, `dom_num_ext`, `dom_num_int`, `nombre`, `telefono`. La protesta de decir verdad y el consentimiento de datos sí se exigen siempre, porque no dependen de la identidad.

**Establecimiento.** Los campos de tipo, nombre comercial y razón social sólo se piden —y sólo se validan— cuando se respondió que los hechos ocurren en un establecimiento.

**Regla de competencia.** Es independiente de la obligatoriedad y se aplica siempre, también con la validación apagada: si el punto cae fuera de la Ciudad de México, no se puede continuar.

**Validaciones de formato**, además de la presencia del dato:

| Campo | Regla |
|---|---|
| Código postal, propio y del domicilio | Exactamente cinco dígitos |
| Correo electrónico | Estructura de dirección válida |
| Teléfono | Al menos diez dígitos |
| Descripción de los hechos | Mínimo de 40 caracteres |
| Fecha de los hechos | No posterior al día de hoy |

## Cómo se comporta el formulario

Sólo se marca lo **opcional**. Un campo sin marca es obligatorio en el esquema activo. Es la decisión que tomó la auditoría de estilos: marcar a la vez lo obligatorio y lo opcional duplica las señales en pantalla sin añadir información.

Cuando la validación está encendida, cada paso muestra al inicio una línea que recuerda qué esquema está aplicando. Si falta algo, aparece un resumen al principio de la pantalla con la cuenta de datos faltantes y un enlace por cada uno; el foco se coloca en el resumen y, al tocar un enlace, en el campo.

## Pendiente

El esquema definitivo lo decide la Dirección General de Inspección y Vigilancia Ambiental. Los dos aquí descritos son las dos posiciones documentadas hasta hoy; el prototipo permite recorrer el formulario con uno y con otro para tomar la decisión con el instrumento a la vista y no sobre el papel.

Conviene medir, en la sesión de validación, cuántos campos se quedan vacíos de manera natural con cada esquema: un campo obligatorio que la mayoría no sabe llenar no protege el expediente, sólo interrumpe la denuncia.
