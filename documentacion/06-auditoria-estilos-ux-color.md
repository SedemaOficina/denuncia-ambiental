# Formulario web de Denuncia Ambiental · Auditoría de estilos, experiencia de uso y color

> **Nota de vigencia · 20 de septiembre de 2026.** Este documento es una **auditoría fechada**: describe el prototipo en la fecha de su encabezado y **no se actualiza**. Sus mediciones, conteos, citas de pantalla y listas de controles describen la versión auditada, no la vigente; donde dice «hoy» debe leerse «en la fecha de esta auditoría». Las correcciones que derivaron de ella están registradas como decisiones en `05-decisiones-y-pendientes.md` y en la bitácora de `11-ruta-de-trabajo.md`, que son las fuentes del estado actual, junto con el prototipo. **Un hallazgo de este documento sólo se tiene por cerrado cuando una decisión lo declara cerrado y una comprobación automática lo sujeta.**
>
> *Qué la dejó atrás:* DEC-61 —se marca lo obligatorio y no lo opcional, al revés de lo que aquí se recomienda—, DEC-62 —retiro de siete ayudas y del ejemplo por supuesto—, DEC-64 —escala de jerarquía de seis niveles—, DEC-71 —retroceder pasa a enlace sin borde—, DEC-76 y DEC-77 —portada rehecha—, DEC-78 y DEC-79 —estadística y aviso de privacidad en el paso 5— y DEC-85 y DEC-86 —paso 6—. Los conteos de materias y tarjetas corresponden al catálogo de entonces.

**Versión:** 1.0 · 18 de septiembre de 2026
**Objeto auditado:** prototipo del formulario, versión del 18 de septiembre.
**Método:** revisión del código de estilos, medición de contraste conforme a WCAG 2.1 AA y recorrido del flujo en pantalla de escritorio (1100 px) y de teléfono (390 px).

---

## Parte I. Auditoría de estilos

### 1. El guinda hace demasiados trabajos

El color institucional aparece en **treinta y tres reglas distintas**, cumpliendo funciones que deberían estar separadas:

| Función que hoy cumple el guinda | Ejemplos |
|---|---|
| Identidad institucional | Barra superior, filete, encabezados de tabla |
| Jerarquía tipográfica | Títulos de página, de tarjeta y de sección |
| Acción primaria | Botón «Continuar» |
| Selección | Tarjeta de materia elegida |
| Obligatoriedad | Asterisco de campo requerido |
| Error | Texto de error y borde del campo inválido |
| Foco | Anillo de foco del campo activo |

Cuando un mismo color significa *marca*, *haz esto* y *algo salió mal*, ninguno de los tres se lee con claridad. Es el hallazgo de fondo de esta auditoría y del que se derivan las recomendaciones de la Parte III.

**Efecto secundario:** el estado de reposo de una tarjeta usa dorado en el paso del cursor y guinda al seleccionarse. Son dos lenguajes cromáticos para el mismo componente.

### 2. No existe escala tipográfica

El prototipo emplea **dieciocho tamaños de letra distintos** —11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 17, 18, 19, 20, 21, 23 y 26 px—, muchos separados por medio punto. Diferencias de 0.5 px no se perciben como jerarquía: se perciben como descuido.

**Recomendación.** Reducir a una escala de siete pasos: 12 · 13 · 14 · 16 · 20 · 24 · 30. Cuerpo en 16, ayudas en 13, títulos de tarjeta en 20, título de página en 30.

### 3. No existe escala de radios

Hay **once valores de `border-radius`** conviviendo: 3, 4, 6, 7, 8, 10, 12, 24 px, 50 %, un valor compuesto y el token `--radio`.

**Recomendación.** Tres valores: 6 px para controles, 10 px para contenedores y 999 px para píldoras. El token `--radio` ya existe; basta usarlo.

### 4. Contraste: cinco pares no cumplen

Medición conforme a WCAG 2.1, criterios 1.4.3 (texto, 4.5:1) y 1.4.11 (componentes no textuales, 3:1).

| Elemento | Par | Ratio | Estado |
|---|---|---|---|
| Ayudas de campo y etiqueta «opcional» | #8A8D8F sobre blanco | 3.34 | **Falla** |
| Ayudas sobre el fondo de página | #8A8D8F sobre #F4F5F6 | 3.06 | **Falla** |
| Acentos en dorado | #B28E5C sobre blanco | 3.04 | **Falla** |
| Texto de aviso ámbar | #B26A00 sobre #FDF6E8 | 3.94 | **Falla** |
| Borde de los campos de captura | #DCDEE0 sobre blanco | 1.35 | **Falla** |
| Cuerpo del formulario | #2B2D2E sobre blanco | 13.84 | Cumple |
| Texto secundario | #55585A sobre blanco | 7.17 | Cumple |
| Botón primario | blanco sobre #9D2148 | 7.65 | Cumple |

El borde de campo en 1.35 es el más grave: en una pantalla con reflejo o en un teléfono a plena luz, los campos dejan de percibirse como campos. Para un trámite de gobierno, sujeto a obligaciones de accesibilidad, ninguno de los cinco es admisible.

**Valores corregidos, ya verificados:**

| Uso | Valor actual | Valor propuesto | Ratio corregido |
|---|---|---|---|
| Ayudas de campo | #8A8D8F | **#6B6E70** | 5.14 sobre blanco · 4.70 sobre el fondo |
| Dorado tipográfico | #B28E5C | **#8C6C3E** | 4.85 *(el dorado original se conserva en filetes, que no son texto)* |
| Texto de advertencia | #B26A00 | **#8A5200** | 5.94 sobre su fondo |
| Borde de campo | #DCDEE0 | **#8E9295** | 3.14 |
| Éxito | #1F7A4D | **#1B6B43** | 6.03 sobre su fondo |

### 5. Sin estados de foco ni respeto a la reducción de movimiento

No hay `:focus-visible` en ninguna regla, de modo que el foco de teclado queda en el estilo por defecto del navegador, que desaparece sobre fondos claros. Tampoco hay `prefers-reduced-motion`, pese a que la barra de progreso y las transiciones animan.

---

## Parte II. Auditoría de experiencia de uso

### 6. Accesibilidad: el formulario no es operable con teclado

Es el hallazgo más serio y tiene consecuencia jurídica, no sólo de diseño.

| Hallazgo | Medición | Consecuencia |
|---|---|---|
| Tarjetas de materia y de derivación construidas como `<div>` con `onclick` | **12 elementos** | No reciben foco, no responden a Enter ni a barra espaciadora y un lector de pantalla no las anuncia como opciones. Una persona que navega con teclado **no puede elegir la materia**, es decir, no puede denunciar |
| Etiquetas sin asociación | **0 de 11 `<label>` tienen `for`** | El lector de pantalla no relaciona la etiqueta con su campo; tocar la etiqueta no enfoca el campo |
| Atributos de accesibilidad | **1 `aria-*`, 0 `role`** | Los estados —seleccionado, inválido, bloqueado— no se comunican por vía no visual |
| Zona de carga de archivos | `<div>` con `onclick` | Mismo problema |

**Corrección.** Convertir las tarjetas y la zona de carga en `<button type="button">` con `aria-pressed`, asociar cada `<label>` por `for`/`id`, marcar los campos inválidos con `aria-invalid` y anunciar los avisos de bloqueo con `role="alert"`. Es trabajo mecánico, de unas horas, y sin él el formulario no es publicable por una dependencia.

### 7. La primera pantalla pide demasiado

Con catorce materias, el primer paso mide **5,409 px de alto en un teléfono**: más de seis pantallas de desplazamiento antes de poder continuar. El ciudadano que denuncia suele estar molesto y con prisa; es el peor momento para pedirle que lea catorce opciones con su fundamento legal.

**Recomendaciones, por orden de efecto:**

1. **Campo de búsqueda al inicio del paso.** «Describe en pocas palabras qué ocurre» filtrando las tarjetas conforme se escribe. Quien sabe qué denuncia llega en dos segundos; quien no, sigue viendo la lista.
2. **Ocultar el fundamento legal tras un enlace «ver fundamento».** Hoy cada tarjeta muestra sus artículos. Es información valiosa para la Dirección General y ruido para el ciudadano.
3. **Colapsar los bloques en teléfono**, mostrando sólo los cuatro títulos y desplegando el elegido.

### 8. Objetivos táctiles por debajo del mínimo

| Elemento | Alto medido | Mínimo recomendado |
|---|---|---|
| Botones de navegación | **41 px** | 44 px |
| Botón del panel de validación | **37 px** | 44 px |
| Botón de quitar archivo adjunto | **≈ 17 px** | 44 px |
| Tarjetas de materia | 93 px | Cumple |

### 9. La barra de progreso se apaga en teléfono

En pantallas angostas los rótulos de las etapas se reducen a tamaño cero y sólo queda visible la activa. El usuario pierde la referencia de cuánto falta, que es justo lo que sostiene la motivación en un formulario largo.

**Recomendación.** Sustituir por un indicador textual: «Paso 2 de 6 · Dónde ocurre».

### 10. El avance no se conserva

Si el ciudadano cierra la pestaña o se le agota la batería, pierde todo lo capturado. En un formulario de seis pasos con carga de fotografías, es una causa previsible de abandono.

**Recomendación.** Guardar un borrador en el navegador tras cada paso y ofrecer retomarlo al volver, advirtiendo que el borrador es local y no constituye denuncia presentada.

### 11. Detalles menores con efecto acumulado

| Hallazgo | Recomendación |
|---|---|
| Contador de caracteres siempre visible bajo cada área de texto | Mostrarlo sólo cuando falte para el mínimo |
| El folio del acuse no se puede copiar de un toque | Botón «Copiar folio» |
| El panel de validación flota sobre el botón «Continuar» | Desplazarlo o replegarlo al hacer clic fuera |
| Se marcan a la vez los campos obligatorios y los opcionales | Marcar sólo lo opcional: reduce a la mitad las marcas en pantalla |
| El aviso de privacidad se abre en una ventana del navegador | Mostrarlo en el mismo modal que el comparativo |

### 12. Lo que está bien resuelto y conviene no tocar

El orden del recorrido es correcto: pide la ubicación —lo más laborioso— cuando la motivación está alta, y los datos personales al final, cuando el ciudadano ya invirtió esfuerzo y es menos probable que abandone por desconfianza. El filtro de competencia antes de cualquier captura evita que alguien llene seis pasos para recibir una improcedencia. La ficha que explica **por qué** se turna a un área concreta convierte una decisión opaca en una decisión motivada. Y el aviso de que los datos personales no se comunican al denunciado aparece exactamente donde se necesita: junto a los campos que lo preocupan.

---

## Parte III. Color aplicado a las acciones

### 13. Principio

En un trámite de gobierno el color no decora: informa sobre el riesgo de lo que se va a hacer. Un sistema de acción funciona cuando el ciudadano distingue, sin leer, entre *avanzar*, *retroceder*, *corregir* y *no puedes continuar*. Hoy los cuatro comparten el guinda.

### 14. Sistema propuesto

| Función | Color | Dónde se usa | Razón |
|---|---|---|---|
| **Identidad** | Guinda #9D2148 | Barra, filetes, títulos, encabezados de tabla | Es la marca; conserva la continuidad institucional |
| **Acción primaria** | Guinda #9D2148 sólido | «Continuar», «Enviar denuncia» | En trámites de gobierno la coincidencia entre la marca y la acción principal refuerza la percepción de legitimidad. Se conserva, pero a condición de retirar el guinda de los tres usos siguientes |
| **Acción secundaria** | Blanco con borde #8E9295 y texto #55585A | «Regresar», «Corregir» | Retroceder nunca debe competir visualmente con avanzar |
| **Selección** | Borde guinda, fondo #F7F1F3 **y marca de verificación** | Tarjeta de materia elegida | El color deja de ser el único portador del estado |
| **Error y bloqueo** | Rojo #B3261E | Texto de error, campo inválido, bloqueo fuera de la Ciudad | Un rojo distinto del guinda separa *marca* de *problema* |
| **Advertencia** | Ámbar #8A5200 sobre #FDF6E8 | Plazo de un año, denuncia anónima, límites de archivo | Señala una consecuencia, no un impedimento |
| **Confirmación** | Verde #1B6B43 | Acuse, aviso de protección de datos | Aparece sólo dos veces en todo el recorrido, y por eso pesa |

### 15. Tres decisiones que conviene sostener

**El verde no debe usarse para «avanzar».** En una dependencia ambiental el verde ya significa *tema ecológico*. Emplearlo además como color de acción produce ambigüedad: el usuario no sabe si el botón verde continúa el trámite o se refiere al contenido ambiental. Reservarlo para la confirmación.

**El rojo se reserva para lo que impide continuar, no para lo que falta.** Si cada campo pendiente se pinta de rojo, el formulario se percibe como hostil y el abandono aumenta. Un campo por llenar es una advertencia; un punto fuera de la Ciudad es un bloqueo. Sólo el segundo es rojo.

**El color nunca es el único portador.** Cada estado lleva además icono y texto: la tarjeta seleccionada muestra una marca de verificación, el campo inválido enuncia qué falta, el bloqueo territorial explica a dónde acudir. Es requisito de accesibilidad y, además, es lo que hace que el mensaje sobreviva a una impresión en blanco y negro o a una pantalla mal calibrada.

### 16. Retirar el guinda de tres lugares

Es la corrección de mayor efecto y la de menor costo:

1. **Asterisco de obligatoriedad** → gris #55585A, o mejor, marcar únicamente lo opcional y suprimir el asterisco.
2. **Texto de error y borde del campo inválido** → rojo #B3261E.
3. **Anillo de foco** → azul #1A73C7 o el guinda con trazo discontinuo, para que el foco de teclado no se confunda con el estado de error.

---

## Parte IV. Correcciones aplicadas

Todas las recomendaciones de prioridad 1 a 7 quedaron implementadas en la versión del 18 de septiembre.

| § | Corrección | Estado |
|---|---|---|
| 6 | Las 21 tarjetas de materia y derivación, la zona de carga, las opciones de temporalidad y de identificación y los resultados de búsqueda pasaron de `div` a `button` con `aria-pressed`; el estado seleccionado añade una marca de verificación | Aplicado |
| 6 | Las once etiquetas quedaron asociadas por `for`/`id`; las ayudas se enlazan con `aria-describedby`; los campos inválidos marcan `aria-invalid`; los avisos de bloqueo se anuncian con `role="alert"` | Aplicado |
| 4 | Ayudas a #6B6E70, borde de campo a #8E9295, advertencia a #8A5200, confirmación a #1B6B43 y dorado tipográfico a #8C6C3E | Aplicado |
| 5 | `:focus-visible` con anillo azul de 3 px y bloque `prefers-reduced-motion` | Aplicado |
| 16 | El guinda se retiró de la obligatoriedad, del error y del foco. El error usa #B3261E y el foco #1A73C7 | Aplicado |
| 11 | Se suprimió el asterisco de obligatoriedad: sólo se marca lo opcional | Aplicado |
| 7 | Campo de búsqueda al inicio del paso 1, con coincidencia indiferente a acentos y **palabras clave de lenguaje ciudadano** en los 21 supuestos: «perro» lleva a maltrato animal, «talaron» a arbolado, «humo negro» a vehículo contaminante, «peste» a emisiones, «chinampa» a Área de Valor Ambiental | Aplicado |
| 7 | El fundamento legal se oculta tras «Ver el fundamento legal de cada supuesto» | Aplicado |
| 8 | Botones a 48 px de alto, panel a 44 px, botón de quitar archivo a 44 × 44 px | Aplicado |
| 9 | Indicador textual «Paso N de 6 · Etapa», visible en teléfono en lugar de los rótulos comprimidos | Aplicado |
| 10 | Borrador local tras cada paso, con aviso para retomarlo, caducidad de catorce días y advertencia de que no constituye denuncia presentada | Aplicado |
| 11 | Botón «Copiar» junto al folio; contador de caracteres sólo cuando falta para el mínimo; el panel se cierra al hacer clic fuera o con Escape | Aplicado |
| 2, 3 | Escala tipográfica de siete pasos y tres radios, en tokens | Aplicado |

**Efecto medido en la primera pantalla.** El paso 1 pasó de 5,409 px a 4,645 px de alto en teléfono al ocultar el fundamento legal; con el buscador en uso —por ejemplo «ruido»— baja a 1,615 px, esto es, **menos de dos pantallas frente a las seis y media originales**.

## Parte V. Orden de atención sugerido

| Prioridad | Trabajo | Razón |
|---|---|---|
| 1 | Accesibilidad de teclado y lector de pantalla (§6) | Sin esto el formulario no es publicable por una dependencia |
| 2 | Contraste: los cinco pares que fallan (§4) | Misma obligación, corrección de minutos |
| 3 | Separar el guinda de error, obligatoriedad y foco (§16) | Alto efecto, bajo costo |
| 4 | Reducir la carga de la primera pantalla (§7) | Es donde se pierde al ciudadano |
| 5 | Objetivos táctiles e indicador textual de paso (§8, §9) | Uso real en teléfono |
| 6 | Escalas de tipografía y de radios (§2, §3) | Consistencia; no bloquea |
| 7 | Borrador local del avance (§10) | Reduce abandono en formularios largos |
