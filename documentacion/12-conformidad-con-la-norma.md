# Formulario web de Denuncia Ambiental · Conformidad con la norma de construcción

**Versión:** 1.2 · 18 de septiembre de 2026
**Para qué sirve este documento.** Sitúa el proyecto frente a la norma de construcción de sistemas: qué cumple, qué falta y qué hay que decidir antes de avanzar de etapa. No sustituye a `11-ruta-de-trabajo.md`, que es el documento del proyecto y manda; éste lo contrasta con la norma general y anota las brechas.

---

## Etapa actual

**Etapa 1 · El cascarón público, avanzada.** Prototipo navegable con identidad gráfica, publicado y abierto desde el teléfono, sin base, sin servidor y sin autenticación. Es donde la norma dice que debe estar.

**No se ha entrado a la etapa 2.** El módulo de administración está diferido de manera expresa (DEC-19, AD-01) y no se abre antes del acta de validación (DEC-32).

---

## 1. Lo que ya cumple

Verificado contra el prototipo y los documentos del proyecto:

| Norma | Estado |
|---|---|
| §2 · Orden de etapas | Se respeta. Cascarón público primero, administración diferida por decisión expresa |
| §2 · Criterio de salida | Declarado en `11-ruta-de-trabajo.md`, con seis requisitos verificables |
| §6.2 · Coordenadas | Las tres capas en grados decimales, orden longitud–latitud, rangos correctos para la Ciudad |
| §6.2 · Precisión | Cinco y seis decimales. Conforme: no hay precisión falsa |
| §6.6 · Precedencia de traslapes | Declarada como RN-04 y RN-06, no dejada al orden de evaluación |
| §6.9 · Qué se dibuja | Sólo el polígono que resultó del cruce (DEC-16), y el resultado se enuncia en texto (DEC-18) |
| §6.8 · Ámbito acotado | Mapa base recortado a la Ciudad (DEC-17) y envío impedido fuera de ella (DEC-20) |
| §6.10 · El mapa no es el único camino | Hay búsqueda por dirección y captura manual |
| §8.3 · Hojas de estilo | Auditadas y consolidadas: un selector, una declaración |
| §8.4 · Color | Auditado y medido sobre cada fondo real |
| §9 · Comentarios | Explican el porqué y citan el fundamento normativo |
| §10 · Fuente única de verdad | `OBLIG`, `MATERIAS`, `LIMITES`, `BIFURCACIONES` gobiernan pantalla, validación y documentación |
| §10.4 · Código muerto | Auditado: cero funciones sin uso, cero claves de estado sin lectura, cero duplicados |
| §12.10 · Bloques cerrados | En operación, con bitácora |
| §14 · Citas normativas | Ninguna sin verificar contra texto vigente; los huecos quedan visibles |

**Nota favorable sobre la capa principal.** `geometrias.geojson` **sí cumple §6.1**: declara fuente, proyección, versión, fecha de consolidación y notas sobre duplicidades conocidas. Es el modelo a replicar en las otras dos.

---

## 2. Brechas que impiden cerrar la etapa 1

Eran cinco. **Tres quedaron resueltas el 18 de septiembre.** Las dos restantes —el acta de validación y los pendientes jurídicos P-01 y P-02— no dependen de nosotros.

**B-01 · Repositorio — RESUELTA el 18 de septiembre de 2026** *(§1.7, §12.8, auditoría 2)*
El proyecto quedó bajo control de versiones con git en su propia carpeta (DEC-34). Primer registro: 21 archivos, 690 KiB empaquetados.
**Qué se versiona:** documentación, prototipo, capas del Sistema de Información Ambiental e insumos fundacionales —formato público vigente y propuesta de la Dirección General—.
**Qué se excluye, y por qué** —razonado en el propio `.gitignore`—: la normativa de referencia, 26 MB de documentos públicos re-descargables que cargarían cada copia; `prototipo/historial/`, porque a partir de ahora la historia la lleva git y mantener dos a mano es peor que una sola (§9.7); y las carpetas `_to_delete/`.
**Auditoría 2 corrida en el mismo acto:** sin secretos —las coincidencias de «token» son referencias a *tokens de color*, y las de «contrase» son la palabra «contraste»—, sin archivos sueltos y sin nada versionado que no deba estarlo.
**Lo que sigue:** decidir la cuenta institucional donde vivirá el repositorio remoto y publicarlo ahí. Mientras tanto, la historia existe pero **sólo en el equipo**, de modo que el respaldo sigue dependiendo de la sincronización de la carpeta.

**B-02 · Titularidad — RESUELTA el 18 de septiembre de 2026** *(§1.7)*
El desarrollo es del **Sistema de Información Ambiental de la Secretaría del Medio Ambiente de la Ciudad de México** (DEC-33). Queda asentado en la ficha del proyecto.
**Lo que sigue:** con la titularidad definida, corresponde resolver en qué **cuentas institucionales** viven el repositorio remoto y, en su momento, la infraestructura, el dominio y el correo del sistema. Es lo que la norma exige en la entrega (§13) y lo que tarda en gestionarse.

**B-03 · Acta de validación de la DGIVA** *(§2, criterio de salida)*
Sigue siendo el requisito 5 del criterio de salida y no depende de nosotros.

**B-04 · P-01 y P-02 sin resolver** *(criterio de salida)*
Naturaleza jurídica del canal y aviso de privacidad. Sin ellos no hay publicación posible.

**B-05 · Minimización — RESUELTA el 18 de septiembre de 2026** *(§1.8)*
Cada uno de los 47 campos declara ahora su **uso**, si es **dato personal** y a qué **finalidad** sirve, dentro del mismo catálogo `OBLIG` que gobierna la pantalla y la validación (DEC-35). El documento 09 se genera de ahí y el comparativo del panel de validación lo muestra en pantalla.

**Resultado:** 20 datos personales de 47 campos, seis finalidades y **cero campos sin uso declarado**. No hubo campos que retirar.

**Tres hallazgos que sí salieron:**

1. **El teléfono es obligatorio y no es vía de notificación** —abierto como P-17, con recomendación de volverlo opcional—.
2. **Seis campos contienen datos personales de terceros**, sobre los que se formula un señalamiento no acreditado y que no dieron su consentimiento. El aviso de privacidad debe mencionarlos expresamente y no se publican nunca.
3. **La coordenada del sitio es dato personal** cuando los hechos ocurren en un domicilio.

**Lo que destraba:** es el insumo que la Unidad de Transparencia necesita para reexpedir el aviso de privacidad, de modo que reduce el trabajo de P-02 —que sigue siendo B-04—.

---

## 3. Brechas que hay que cerrar antes de la etapa 2

**B-06 · Falta el tercer identificador** *(§1.2, relacionado con P-13)*
El proyecto contempla el folio interno y el folio público. **No contempla el folio del sistema de origen:** las denuncias que sigan llegando por Oficialía de Partes o por correo traen su propio número, y sin una columna donde guardarlo, el sistema nuevo y el expediente en papel no se podrán empatar. *En otro proyecto, no tener dónde guardar ese tercer identificador hizo fallar la ficha pública en 68 de 70 registros.*
**Acción:** decidir los tres identificadores antes de definir el modelo de datos.

**B-07 · Catálogos no cerrados** *(§1.4)*
`TIPOS_ESTAB` está declarado como provisional en el propio código, a la espera del catálogo de giros de la Dirección General. Los valores admitidos deben quedar fijos **antes** de que existan datos reales.
**Acción:** solicitar el catálogo de giros o padrón de fuentes fijas; ya está listado en `08-normativa-por-integrar.md`.

**B-08 · Datos ficticios sin conjunto formal** *(§3)*
Existen doce escenarios de prueba, que sirven para recorrer variantes, pero **no** un conjunto de 25 a 40 registros con todos los valores de cada catálogo representados, ni campo `es_ficticio`. Verificado: la marca no existe en el prototipo.
Y hay un problema de fondo en los que sí existen: nombres como «Hojalatería El Volante» o «Servicios Automotrices del Centro S.A. de C.V.» **parecen negocios reales**. La norma lo prohíbe: un nombre creíble en una base de pruebas termina en una captura de pantalla o en un oficio, y ya no se distingue.
**Acción:** al construir el conjunto formal, usar denominaciones inequívocamente falsas y legibles, y marcarlas.

**B-09 · Valores fijos en el código — parcialmente resuelta** *(§1.6, auditoría 3)*
El proveedor de mosaicos y su clave salieron del código a `prototipo/configuracion-local.js`, no versionado (DEC-36). **Siguen escritos en el archivo:** `cdnjs.cloudflare.com` (biblioteca del mapa), `fonts.googleapis.com` (tipografías), `nominatim.openstreetmap.org` (geocodificación) y el correo `denuncias@sedema.cdmx.gob.mx`. En una maqueta es aceptable; en la versión funcional no. **La prueba de la norma:** si al cambiar de dominio o de proveedor hay que tocar el código, el diseño está mal.

**B-10 · Proveedores externos — mitad resuelta** *(§6.8)*
**Mapa base: resuelto.** Se adoptó CARTO con clave propia (DEC-36). Su capa gratuita admite cinco millones de peticiones de mosaico al mes, lo que sí cubre el uso de un portal público, y la atribución a CARTO y a OpenStreetMap —obligatoria por licencia— quedó en el mapa.
**Geocodificación: sigue abierta.** El prototipo consulta `nominatim.openstreetmap.org`, cuyo servicio no está abierto al uso sistemático de producción. La salida es P-12 y P-16 —servicio propio y catálogo de colonias de la ADIP—.
**Pendiente de verificación:** el formato del parámetro de la clave no pudo comprobarse desde el entorno de trabajo, porque la política de salida de red no alcanza al proveedor. Si el mapa aparece con la marca de agua «API key required», hay que sustituir la dirección por la que CARTO entregó al emitir la clave.

## 4. Auditorías del catálogo que nunca se han corrido

| # | Auditoría | Por qué falta |
|---|---|---|
| 2 | Repositorio | **Corrida el 18 sep 2026**, en el acto de crear el repositorio. Sin hallazgos |
| 3 | Portabilidad | Nunca corrida; sus hallazgos están anticipados en B-09 |
| 6 | Capas geoespaciales | **Nunca corrida.** Ver abajo |
| 7 | Cruce espacial | Se probó con puntos representativos, pero no de forma sistemática por capa, traslape y borde, ni contra una capa completa |
| 12 | Rendimiento | Nunca corrida. El prototipo pesa cerca de 660 KB con las capas y el logotipo incrustados; la norma exige medirlo con red limitada |
| 16 | Datos personales | Nunca corrida. Debe correrse **antes del primer dato real** |

**Lo que ya se ve sin correr la auditoría 6**, sólo con leer las capas:

1. `alcaldias.geojson` **no declara proyección**. Las coordenadas son correctas, pero el archivo no lo dice: la norma pide que no se adivine.
2. `suelo_conservacion.geojson` **conserva los atributos crudos del shapefile de origen** —`OBJECTID`, `AREA`, `PERIMETER`, `DESCRIP`, `SUECON0009`—, con los nombres truncados a diez caracteres que impone ese formato. No están normalizados y **no hay clave estable declarada** para la unión.
3. **Ninguna de las tres tiene verificada la validez topológica.** Es la comprobación que más importa, porque una geometría inválida no falla: responde mal en silencio, y de este cruce depende a qué dirección general se turna el expediente.
4. **Sólo existe la capa simplificada.** No está documentado dónde vive la capa completa contra la que deberá resolverse el cruce en la versión funcional *(§6.4, P-12)*.
5. `geometrias.geojson` **sí** trae fuente, proyección, versión y fecha de consolidación. Las otras dos deben igualarlo.

---

## 5. Orden propuesto

1. ~~**B-01 y B-02** — repositorio y titularidad~~ **hechas el 18 sep 2026.** Queda la gestión de la cuenta institucional para el repositorio remoto.
2. ~~**B-05** — uso declarado por campo~~ **hecha el 18 sep 2026.**
3. **Auditoría 6** sobre las tres capas, y normalización de `suelo_conservacion`.
4. **B-06 y B-07** —identificadores y catálogos— antes de tocar el modelo de datos.
5. **Auditorías 12 y 16** —rendimiento y datos personales— antes de publicar.
6. **B-08** —conjunto formal de datos ficticios— al abrir la etapa 2.
7. **B-09 y B-10** —configuración y proveedores— al construir la versión funcional.

**B-03 y B-04 no dependen de nosotros** y son los que cierran la etapa 1.
