# Formulario web de Denuncia Ambiental · Auditoría heurística

**Versión:** 1.0 · 18 de septiembre de 2026
**Pregunta que guía la revisión:** ¿puede una persona cualquiera de la Ciudad de México presentar una denuncia ambiental sin ayuda, desde su teléfono, en una sola sesión?
**Método:** las diez heurísticas de Nielsen aplicadas al recorrido completo, más medición de reflujo a 320 px, atributos de asistencia al llenado, carga por paso y legibilidad de los textos por el índice Fernández-Huerta.

---

## Parte I. Las diez heurísticas

### 1. Visibilidad del estado del sistema · **Parcial**

El indicador «Paso 2 de 6 · Dónde ocurrió» y la barra de avance cumplen. Dos huecos:

- **El cambio de paso no se anuncia.** No existe ninguna región `aria-live`, de modo que quien navega con lector de pantalla no sabe que la pantalla cambió: sólo percibe que el contenido dejó de corresponder.
- **El borrador se guarda en silencio.** Cada paso lo escribe en el navegador, pero nada se lo dice a la persona. Si cierra la pestaña sin saberlo, da por perdido lo capturado y no vuelve.

### 2. Correspondencia con el mundo real · **Parcial**

El rediseño de la primera pantalla y las palabras clave de búsqueda resolvieron lo esencial: «perro», «talaron», «humo negro» o «chinampa» llevan al supuesto correcto. Queda vocabulario que sólo se entiende dentro de la Secretaría:

| Término en pantalla | Cómo lo diría un ciudadano |
|---|---|
| Terráceos y despalmes | Están removiendo tierra o vegetación |
| Fuentes fijas | Un negocio, una fábrica, un taller |
| Manifestación Ambiental Única | El permiso ambiental del negocio |
| Área de Valor Ambiental | Un bosque, una barranca |

«Terráceos» es el caso más claro: fuera de la Secretaría prácticamente nadie sabe qué significa, y es el nombre principal de una de las dieciocho opciones.

### 3. Control y libertad · **Parcial**

Todos los pasos tienen «Regresar» y el punto del mapa se puede mover o quitar. Falta lo más útil: **desde la pantalla de revisión no se puede saltar al dato que se quiere corregir**. El botón «Corregir» devuelve al paso 5, de modo que para arreglar la colonia hay que retroceder tres pantallas y volver a avanzarlas.

### 4. Consistencia y estándares · **Parcial**

La auditoría de estilos dejó tokens, escala y componentes consistentes. Persiste una inconsistencia de lenguaje: tres verbos distintos para acciones emparentadas —«Quitar el punto», «Limpiar», «Empezar de nuevo»—.

### 5. Prevención de errores · **Parcial**

Bien resueltos: el bloqueo cuando el punto cae fuera de la Ciudad, el tope de fecha en el día de hoy, el aviso del plazo de un año y la advertencia de efectos de la denuncia anónima.

Faltan tres:

- **«Empezar de nuevo» borra el borrador sin preguntar.** Un toque accidental destruye lo capturado y no hay manera de recuperarlo.
- **Ningún campo numérico abre el teclado numérico** en el teléfono: código postal y teléfono se capturan con el teclado de texto, que es donde se cometen los errores de dedo.
- **No hay límite de caracteres** en el código postal ni en el teléfono.

### 6. Reconocer antes que recordar · **Parcial**

La pantalla de revisión antes de enviar cumple. Pero **la materia elegida sólo se muestra en el paso 3**: en el paso de ubicación, en el de pruebas y en el de datos personales la persona ya no ve qué está denunciando. En un formulario que se llena en varias sesiones —lo que el borrador ahora permite— eso importa.

### 7. Flexibilidad y eficiencia · **Insuficiente**

El buscador de supuestos es un acierto. En contra: **ninguno de los diecinueve campos tiene `autocomplete`**. Quien ya llenó otro trámite en su teléfono tiene que volver a teclear nombre, teléfono, correo y domicilio completo, en lugar de aceptar lo que el navegador ya guardó. Es la diferencia entre treinta segundos y tres minutos, y es donde se abandona un formulario de gobierno.

### 8. Diseño estético y minimalista · **Parcial**

| Paso | Campos | Palabras |
|---|---|---|
| 1 · Qué denuncias | 7 | 302 |
| 2 · Dónde ocurrió | 16 | 253 |
| 3 · Qué ocurrió | 13 | 268 |
| 4 · Pruebas | 7 | 62 |
| **5 · Tus datos** | **19** | 186 |
| 6 · Revisión | 6 | 118 |

El paso 5 concentra diecinueve campos, casi todos del domicilio. Conviene evaluar si el domicilio completo es indispensable cuando ya se pidió correo y teléfono: la notificación electrónica lo vuelve prescindible en la mayoría de los casos.

### 9. Reconocer y recuperar errores · **Insuficiente**

Con la validación activa y el formulario vacío, el envío marca **once campos**, pero:

- **no aparece un resumen de errores al inicio** de la pantalla;
- **el foco no se mueve** al primer campo con problema, se queda en el botón;
- quien usa lector de pantalla **no recibe ningún aviso** de que el envío falló.

Es un incumplimiento del criterio 3.3.1 de las WCAG y, en la práctica, deja al usuario mirando una pantalla que no parece haber hecho nada.

### 10. Ayuda y documentación · **Ausente**

No existe ninguna vía de ayuda: ni teléfono, ni correo, ni preguntas frecuentes, ni un «¿Tienes dudas?». Si la persona se atora —y en un trámite ambiental se atora en la ubicación o en la descripción de los hechos— no tiene a dónde ir salvo cerrar la pestaña.

---

## Parte II. Accesibilidad pendiente

La auditoría anterior resolvió el teclado, las etiquetas y el contraste. Quedan cinco puntos:

| Hallazgo | Medición | Criterio |
|---|---|---|
| **Desbordamiento horizontal a 320 px** en la pantalla de supuestos y en el acuse | Filas de hasta 348 px y folio de 490 px en una ventana de 320 px | WCAG 1.4.10 Reflujo |
| **Sin atributos `autocomplete`** | 0 de 19 campos | WCAG 1.3.5 Identificar el propósito |
| **Encabezado con nombre accesible defectuoso** | El lector anuncia «5Tus datos» porque el número del paso se pega al título | WCAG 1.3.1 |
| **Sin enlace para saltar al contenido** ni regiones `aria-live` | 0 y 0 | WCAG 2.4.1 y 4.1.3 |
| **Los campos no están dentro de un `<form>`** | 0 elementos `form` | Semántica y envío con Enter |

---

## Parte III. Lenguaje

Índice Fernández-Huerta sobre los textos que la persona lee en pantalla. Por encima de 70 es fácil; entre 50 y 60, algo difícil.

| Texto | Índice | Palabras por frase | Lectura |
|---|---|---|---|
| Guía para describir los hechos | 72.8 | 9.7 | fácil |
| Nota de zonas de protección | 70.4 | 27.0 | fácil |
| Qué sigue, en el acuse | 64.9 | 15.0 | normal |
| Aviso de competencia | 59.3 | 11.0 | algo difícil |
| Protesta de decir verdad | 58.3 | 28.0 | algo difícil |
| Portada, qué es el formulario | 57.6 | 14.5 | algo difícil |
| **Motivación de la ficha de competencia** | **54.6** | **35.0** | **algo difícil** |

El patrón es claro: **los textos que redacté como consejo práctico son fáciles; los que trasladan lenguaje jurídico son difíciles**, y no por las palabras sino por la longitud de las frases. La motivación de la ficha —la que explica por qué se turna a una u otra dirección general— tiene treinta y cinco palabras por frase. Partirla en dos oraciones la llevaría a lectura normal sin perder precisión.

La protesta de decir verdad no se puede simplificar sin riesgo jurídico, pero sí acompañarse de una línea en lenguaje llano debajo.

---

## Parte IV. Correcciones aplicadas el mismo día

| § | Corrección | Estado |
|---|---|---|
| 9 | **Resumen de errores** al inicio de la pantalla, con `role="alert"`, la cuenta de datos faltantes, un enlace por cada campo y el foco puesto en el resumen. Tocar un enlace lleva el foco al campo | Aplicado |
| II | **Desbordamiento a 320 px corregido** en las siete pantallas: la lista de supuestos y el folio del acuse ya no fuerzan desplazamiento lateral | Aplicado |
| 7 y 5 | **`autocomplete` en doce campos** —nombre, apellidos, teléfono, correo y las seis partes del domicilio— e **`inputmode` numérico** con longitud máxima en código postal y teléfono | Aplicado |
| 5 y 1 | **«Descartar y empezar de nuevo» pide confirmación** antes de borrar el borrador, y cada guardado muestra «Avance guardado en este navegador» | Aplicado |
| 6 y 3 | **Recordatorio permanente de la materia elegida** a partir del paso 2, con enlace para cambiarla, y **enlaces «Editar»** en la pantalla de revisión que llevan al paso correspondiente | Aplicado |
| 10 | **Pie institucional** con el logotipo, la dependencia, el domicilio y el horario de Oficialía de Partes, el correo de denuncias y el aviso de privacidad | Aplicado |
| 1 | **Anuncio del cambio de paso** en una región `aria-live` y **enlace para saltar al formulario** | Aplicado |
| 2 | **«Terráceos» dejó de ser el nombre principal**: la opción se llama ahora «Remoción de tierra o vegetación» y el término técnico se conserva como denominación formal | Aplicado |
| II | El **logotipo institucional quedó incrustado** en el propio archivo, de modo que aparece aunque no haya red o el entorno bloquee recursos externos | Aplicado |

**Pendiente de decisión, no de trabajo:** el teléfono de atención ciudadana, que es la pieza que falta para cerrar la heurística 10, y la evaluación de si el domicilio completo es indispensable cuando ya se pidió correo y teléfono (heurística 8).

## Parte V. Prioridades

| Prioridad | Trabajo | Heurística |
|---|---|---|
| 1 | Resumen de errores con foco y anuncio al lector de pantalla | 9 |
| 2 | Corregir el desbordamiento a 320 px | Accesibilidad |
| 3 | `autocomplete` e `inputmode` en los diecinueve campos | 7 y 5 |
| 4 | Confirmar antes de borrar el borrador; avisar que se guardó | 5 y 1 |
| 5 | Mostrar siempre la materia elegida y permitir editar desde la revisión | 6 y 3 |
| 6 | Bloque de ayuda con teléfono y correo | 10 |
| 7 | Sustituir «Terráceos» y partir las frases largas | 2 |
| 8 | Evaluar si el domicilio completo es indispensable | 8 |
