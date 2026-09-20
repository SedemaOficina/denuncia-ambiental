# Formulario web de Denuncia Ambiental · Variantes del formulario

**Versión:** 1.0 · 18 de septiembre de 2026
**Generado desde el prototipo.** Las tablas de abajo salen de las mismas estructuras que gobiernan el formulario, de modo que documento y comportamiento no pueden discrepar.

El formulario no es un camino único: hay **trece puntos donde cambia de forma** según lo que se responde. Este documento los enumera y describe los trece escenarios que el panel de validación carga con un toque, para recorrer cada rama sin tener que capturar todo a mano.

---

## 1. Puntos de bifurcación

| Paso | Qué se responde | Opciones | Cómo cambia el formulario |
|---|---|---|---|
| 1 | **Qué se denuncia** | 18 materias · 7 supuestos de otra autoridad | Elegir una materia avanza al paso 2. Elegir un supuesto de otra autoridad detiene el flujo y muestra a dónde acudir. |
| 2 | **Dónde cae el punto (cruce espacial)** | Suelo urbano · AVA · ANP local · ANP federal con convenio · ANP federal sin convenio · Suelo de conservación · Fuera de la Ciudad | Determina el área que atiende y el contenido de la ficha. Fuera de la Ciudad bloquea el avance. |
| 2 | **¿Los hechos ocurren dentro de un establecimiento?** | Sí · No | «Sí» muestra tipo de establecimiento y nombre comercial, y preselecciona «Una empresa o negocio» en el paso 3, donde puede cambiarse. |
| 2 | **Tipo de establecimiento** | 19 giros · Otro | «Otro» abre un campo de texto para especificarlo. |
| 3 | **¿Quién es responsable de los hechos?** | Persona · Empresa · Autoridad · No lo sé | Cambia por completo el bloque de responsables. «Autoridad» además advierte la ruta del artículo 331 y la refleja en el acuse. |
| 3 | **Desde cuándo ocurre y fecha** | Único · Recurrente · Permanente, con fecha anterior o posterior a un año | Más de un año muestra un aviso distinto según si los hechos continúan o fueron un hecho único. |
| 5 | **Variante de identificación** | B admite anónima *(decidida)* · C obligatoria sin anonimato | La opción A —identificación obligatoria según la propuesta de la Dirección General— se retiró el 19 de septiembre de 2026 (DEC-40). B agrega la elección entre identificarse y denunciar anónimamente. |
| 5 | **¿Denuncia anónima?** | Sí · No | «Sí» oculta todos los datos de identificación y cambia el acuse: sin notificación. |
| 5 | **¿Notificación por correo?** | Sí · No | «No» despliega los siete campos del domicilio. «Sí» los suprime. |
| 5 | **¿Datos confidenciales?** | Sí · No | Se registra en el resumen; no cambia los campos. |
| Todos | **Obligatoriedad** | Desactivada · Esquema DGIVA · Formato vigente | Cambia qué campos se marcan como opcionales y qué exige cada paso al continuar. |
| Todos | **Filtro de competencia** | Activo · Inactivo | Inactivo retira del paso 1 los supuestos de otra autoridad. |
| Portada | **Borrador guardado** | Existe · No existe | Si existe, la portada ofrece retomarlo o descartarlo. |

### Cuántas combinaciones son

Multiplicadas, las ramas dan varios miles de recorridos distintos. No tiene sentido probarlos todos: los que importan son aquellos en los que **cambia el área que atiende, cambia el conjunto de campos, o cambia lo que el acuse promete**. Esos son los doce del apartado siguiente.

---

## 2. Escenarios cargables desde el panel

Cada botón limpia el formulario, carga una combinación completa de respuestas —incluida la coordenada, que dispara el cruce espacial— y abre el paso donde se aprecia el cambio.

| Escenario | Qué muestra | Abre en | Área que atiende |
|---|---|---|---|
| **Comercio en suelo urbano** | Emisiones de un taller · identificado · notificación por correo · DGIVA | Paso 6 | DGIVA |
| **Tala en suelo de conservación, anónima** | Tala · anónima · responsable desconocido · DGCORENADR | Paso 6 | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas |
| **Obra de una alcaldía** | Se señala a una autoridad · ruta del artículo 331 · notificación por domicilio | Paso 6 | DGIVA |
| **Afectación en Área de Valor Ambiental** | Bosque urbano · DGIVA · persona física señalada | Paso 2 | DGIVA |
| **ANP federal coadministrada** | Desierto de los Leones · la Secretaría coadyuva en la administración; la denuncia se turna a la PROFEPA mientras las áreas resuelven (P-22) | Paso 2 | PROFEPA |
| **ANP federal sin convenio** | El Histórico Coyoacán · se deriva a la PROFEPA | Paso 2 | PROFEPA |
| **Punto fuera de la Ciudad** | Naucalpan · el formulario impide continuar | Paso 2 | Bloqueado: fuera de la Ciudad |
| **Caso de otra autoridad** | Ruido de vecinos · se detiene el flujo y se orienta | Paso 1 | — |
| **Hechos de hace más de un año** | Permanente · aviso del plazo del artículo 22 BIS 2 | Paso 3 | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas |
| **Establecimiento de giro no listado** | «Otro» abre el campo de texto | Paso 2 | DGIVA |
| **Formato vigente con validación activa** | Formulario vacío · muestra todo lo que el esquema ampliado exige | Paso 3 | — |
| **Esquema DGIVA con validación activa** | Formulario vacío · muestra el mínimo exigible | Paso 2 | — |

### Qué cubre cada uno

| Escenario | Zona | A quién se denuncia | Identificación | Notificación |
|---|---|---|---|---|
| Comercio en suelo urbano | Suelo urbano | Empresa | Identificada | Correo |
| Tala en suelo de conservación, anónima | Suelo de conservación | Desconocido | Anónima | — |
| Obra de una alcaldía | Suelo urbano | Autoridad | Identificada | Domicilio |
| Afectación en Área de Valor Ambiental | Área de Valor Ambiental · Bosque urbano | Persona | — | — |
| ANP federal coadministrada | Área Natural Protegida federal · la Secretaría coadyuva en su administración | PROFEPA | — | — |
| ANP federal sin convenio | Área Natural Protegida de competencia federal | — | — | — |
| Punto fuera de la Ciudad | Fuera de la Ciudad | — | — | — |
| Caso de otra autoridad | — | — | — | — |
| Hechos de hace más de un año | Suelo de conservación | Desconocido | — | — |
| Establecimiento de giro no listado | Suelo urbano | — | — | — |
| Formato vigente con validación activa | — | — | — | — |
| Esquema DGIVA con validación activa | — | — | — | — |

---

## 3. Las cinco rutas de competencia

Es la bifurcación con más consecuencia, porque decide quién atiende y qué procedimiento sigue.

| El punto cae en | Atiende | Procedimiento |
|---|---|---|
| Suelo urbano | DGIVA | Inspección y, en su caso, sanción |
| Área de Valor Ambiental | DGIVA | Inspección y, en su caso, sanción |
| Área Natural Protegida local | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas | Inspección y, en su caso, sanción |
| Suelo de conservación | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas | Inspección y, en su caso, sanción |
| Área Natural Protegida federal, **con convenio o sin él** | PROFEPA, provisionalmente | La Secretaría la recibe y la remite. Con convenio queda enterada por su papel en la administración del parque. **Criterio a consulta de las áreas (P-22)** |
| Fuera de la Ciudad de México | Ninguna | Se impide continuar |

A esto se superpone una séptima ruta que no depende del territorio sino de a quién se señala: **si se denuncia a una autoridad**, el artículo 331 de la Ley Ambiental manda emitir recomendaciones en lugar de sancionar, y el acuse lo advierte.

---

## 4. Cómo usarlo en la sesión de validación

1. Abrir el **panel de validación**, esquina inferior derecha.
2. En **Escenarios de prueba**, tocar el que corresponda: el formulario se carga completo y abre en el paso pertinente.
3. **Ver todas las variantes del formulario** abre la tabla del apartado 1 dentro del propio prototipo.
4. Para revisar obligatoriedad, encender *Exigir los campos obligatorios* y alternar entre los dos esquemas; los escenarios «con validación activa» ya vienen configurados así.

**Recomendación de orden.** Empezar por los tres escenarios que representan el grueso del volumen real —comercio en suelo urbano, tala en suelo de conservación y obra de una alcaldía— y sólo después revisar los casos de borde. Son los tres que muestran las tres rutas de competencia y las tres formas del bloque de responsables.
