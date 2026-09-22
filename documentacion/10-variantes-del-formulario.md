# Formulario web de Denuncia Ambiental · Variantes del formulario

**Versión:** 2.0 · 22 de septiembre de 2026
**Generado automáticamente** de las estructuras `BIFURCACIONES` y `ESCENARIOS` del prototipo, que son las mismas que gobiernan el panel de validación. Documento y comportamiento no pueden discrepar.

El formulario no es un camino único: hay **doce puntos donde cambia de forma** según lo que se responde. Este documento los enumera y describe los doce escenarios que el panel de validación carga con un toque, para recorrer cada rama sin capturar todo a mano.

---

## 1. Puntos de bifurcación

| Paso | Qué se responde | Opciones | Cómo cambia el formulario |
|---|---|---|---|
| 1 | **Qué se denuncia** | 19 materias · 7 supuestos de otra autoridad | Elegir una materia avanza al paso 2. Elegir un supuesto de otra autoridad detiene el flujo y muestra a dónde acudir. |
| 2 | **Dónde cae el punto (cruce espacial)** | Suelo urbano · AVA · ANP local · ANP federal con convenio · ANP federal sin convenio · Suelo de conservación · Fuera de la Ciudad | Determina el área que atiende y el contenido de la ficha. Fuera de la Ciudad bloquea el avance. |
| 3 | **¿Los hechos ocurren dentro de un establecimiento?** | Sí · No | «Sí» muestra tipo de establecimiento y nombre comercial, y preselecciona «Una empresa o negocio» en la pregunta siguiente, donde se puede cambiar. |
| 3 | **Tipo de establecimiento** | 19 giros · Otro | «Otro» abre un campo de texto para especificarlo. |
| 3 | **¿Quién es responsable de los hechos?** | Persona · Empresa · Autoridad · No lo sé | Cambia por completo el bloque de responsables. «Autoridad» además advierte la ruta del artículo 331 y la refleja en el acuse. |
| 3 | **Desde cuándo ocurre y fecha** | Único · Recurrente · Permanente, con fecha anterior o posterior a un año | Más de un año muestra un aviso distinto según si los hechos continúan o fueron un hecho único. |
| 5 | **¿Con qué identidad se presenta?** | Cuenta Llave CDMX · Escribir los datos · Denuncia anónima | Llave CDMX llena los datos y liga el folio a la cuenta. La anónima oculta todos los datos de identificación y cambia el acuse: sin notificación. |
| 5 | **¿Notificación por correo?** | Sí · No | «No» despliega los siete campos del domicilio. «Sí» los suprime. |
| 5 | **¿Datos confidenciales?** | Sí · No | Se registra en el resumen; no cambia los campos. |
| Todos | **Obligatoriedad** | Desactivada · Activa | Activa, cada paso exige sus campos obligatorios antes de continuar y los demás se marcan como opcionales. |
| Todos | **Filtro de competencia** | Activo · Inactivo | Inactivo retira del paso 1 los supuestos de otra autoridad. |
| Portada | **Borrador guardado** | Existe · No existe | Si existe, la portada ofrece retomarlo o descartarlo. |

### Cuántas combinaciones son

Multiplicadas, las ramas dan varios miles de recorridos distintos. No tiene sentido probarlos todos: los que importan son aquellos en los que **cambia el área que atiende, cambia el conjunto de campos, o cambia lo que el acuse promete**. Ésos son los doce del apartado siguiente.

---

## 2. Escenarios cargables desde el panel

Cada botón limpia el formulario, carga un caso completo —incluida la coordenada, que dispara el cruce espacial— y abre el paso donde se aprecia el cambio.

| Escenario | Qué muestra | Abre en |
|---|---|---|
| **Sitio sin domicilio, con cuenta Llave CDMX** | Tala en el Bosque de Tlalpan · sin calle ni colonia · identidad acreditada · DGCORENADR | Paso 6 |
| **Comercio en suelo urbano** | Emisiones de un taller · identificado · notificación por correo · DGIVA | Paso 6 |
| **Tala en suelo de conservación, anónima** | Tala · anónima · responsable desconocido · DGCORENADR | Paso 6 |
| **Obra de una alcaldía** | Se señala a una autoridad · ruta del artículo 331 · notificación por domicilio | Paso 6 |
| **Afectación en Área de Valor Ambiental** | Bosque urbano · DGIVA · persona física señalada | Paso 2 |
| **ANP federal con coadministración** | Desierto de los Leones · con convenio, pero la inspección es federal (P-22) | Paso 2 |
| **ANP federal sin convenio** | El Histórico Coyoacán · se deriva a la PROFEPA | Paso 2 |
| **Punto fuera de la Ciudad** | Naucalpan · el formulario impide continuar | Paso 2 |
| **Caso de otra autoridad** | Ruido de vecinos · se detiene el flujo y se orienta | Paso 1 |
| **Hechos de hace más de un año** | Permanente · aviso del plazo del artículo 22 BIS 2 | Paso 3 |
| **Establecimiento de giro no listado** | «Otro» abre el campo de texto | Paso 3 |
| **Formulario vacío con validación activa** | Muestra qué exige cada paso antes de dejar continuar | Paso 2 |

> El área que atiende cada caso no se documenta aquí: la resuelve el cruce espacial al cargar el escenario, y repetirla a mano es exactamente la forma en que este documento se separó del formulario. El apartado 3 explica la regla; el prototipo muestra el resultado.

---
## 3. Las rutas de competencia

Es la bifurcación con más consecuencia, porque decide quién atiende y qué procedimiento sigue.

| El punto cae en | Atiende | Procedimiento |
|---|---|---|
| Suelo urbano | DGIVA | Inspección y, en su caso, sanción |
| Área de Valor Ambiental | DGIVA | Inspección y, en su caso, sanción |
| Área Natural Protegida local | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas | Inspección y, en su caso, sanción |
| Suelo de conservación | DGCORENADR · Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas | Inspección y, en su caso, sanción |
| Área Natural Protegida federal, **con convenio o sin él** | PROFEPA, provisionalmente | La Secretaría la recibe y la remite. Con convenio queda enterada por su papel en la administración del parque. **Criterio a consulta de las áreas (P-22)** |
| Fuera de la Ciudad de México | Ninguna | Se impide continuar |

A esto se superpone una ruta que no depende del territorio sino de a quién se señala: **si se denuncia a una autoridad**, el artículo 331 de la Ley Ambiental manda emitir recomendaciones en lugar de sancionar, y el acuse lo advierte.

---

## 4. Cómo usarlo en la sesión de revisión

1. Abrir el **panel de validación**, esquina inferior derecha. No forma parte del formulario y no se publica: es una herramienta de trabajo de la Secretaría.
2. En **Escenarios de prueba**, tocar el que corresponda: el formulario se carga completo y abre en el paso pertinente.
3. **Ver las ramas del formulario** abre la tabla del apartado 1 dentro del propio prototipo; **Ver el mapeo de campos**, la de obligatoriedad y uso declarado de cada campo.
4. Para revisar la obligatoriedad, encender *Exigir los campos obligatorios*. Hay una sola lista de campos obligatorios (DEC-97) y el escenario «Formulario vacío con validación activa» ya viene así.

**Recomendación de orden.** Empezar por los tres escenarios que representan el grueso del volumen real —comercio en suelo urbano, tala en suelo de conservación y obra de una alcaldía— y sólo después revisar los casos de borde. Son los tres que muestran las tres rutas de competencia local y las tres formas del bloque de responsables.
