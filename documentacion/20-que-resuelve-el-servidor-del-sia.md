# Formulario web de Denuncia Ambiental · Qué resuelve el servidor del SIA

**Versión:** 1.0 · 1 de octubre de 2026
**Para qué sirve este documento.** Es la lista de lo que el Sistema de Información Ambiental tiene que construir cuando monte el formulario en su servidor: todo lo que el prototipo **simula, deja en el navegador o pospone «para la versión funcional»**, reunido en un solo lugar con su origen y con la condición para darlo por hecho. Lo citan los documentos 01 y 04.
**Cómo se mantiene.** Cuando una decisión nueva deje algo para el servidor, se agrega aquí, con su clave `SIA-NN`, en la misma sesión en que se registra en el documento 05. Una tarea terminada no se borra: se marca con la fecha y el commit que la cerró.

---

## 1. La regla que gobierna todo

El prototipo valida para **ayudar**; el servidor valida para **defender**. Lo que el servidor no revise no está revisado, porque la computadora de quien denuncia es suya y puede saltarse cualquier control de la página (documento 15, §2).

De ahí tres consecuencias que valen para cada tarea de esta lista:

1. **Toda validación del navegador se repite en el servidor**: obligatoriedad, formatos, intervalos y punto dentro de la Ciudad.
2. **Todo lo que decide competencia o identidad lo pone el servidor**: el cruce espacial, el folio, la clave de consulta y la hora de recepción.
3. **Ningún servicio externo puede impedir que se reciba una denuncia.** Si la geocodificación o la prueba de humanidad no responden, la denuncia se recibe y se marca para revisión.

---

## 2. Tareas, por fase

Las fases son las del documento 11. La etapa 3 de la Oficina de la Secretaría, «implementación en el SIA», reúne las fases 2, 3, 4 y 6.

### Fase 2 · Contrato de datos y servicios

| Clave | Tarea | Se da por hecha cuando | Origen |
|---|---|---|---|
| **SIA-01** | **Contrato de la interfaz**: qué recibe y qué devuelve cada operación —alta de denuncia, carga de evidencia, cruce espacial, geocodificación, resolución de enlace corto y consulta por folio— | El contrato reproduce el comportamiento del prototipo validado; si aparece un caso que el prototipo no resuelve, se corrige primero el prototipo | Documento 11, fase 2 |
| **SIA-02** | **Diccionario de datos y modelo entidad-relación**, a partir del documento 09 —que se genera del código— y de los catálogos del documento 04 convertidos en tablas | Cada campo del documento 09 tiene tipo, longitud, obligatoriedad, catálogo y regla de validación | Documento 11, fase 2 |
| **SIA-03** | **Campos de canal y origen** para la captura por personal: canal, origen, fecha de recepción original, folio de origen, quién recibió, quién capturó y soporte | Están en el modelo aunque el módulo se construya en la fase 5 | AD-03, DEC-154 |

### Fase 3 · Servicios de territorio

| Clave | Tarea | Se da por hecha cuando | Origen |
|---|---|---|---|
| **SIA-04** | **Capas completas, documentadas y válidas.** Declarar dónde viven las capas completas de alcaldías, AVA y ANP y suelo de conservación —el prototipo sólo tiene las simplificadas a unos 8 m—; declarar la proyección de `alcaldias.geojson`; normalizar los atributos crudos de `suelo_conservacion.geojson` y darle una clave estable; verificar la validez topológica de las tres | Auditoría 6 corrida sin hallazgos abiertos | Documento 12, §4; P-12 |
| **SIA-05** | **Servicio de cruce espacial en el servidor**, contra las capas completas (PostGIS o el mismo algoritmo de punto en polígono). Devuelve alcaldía, tipo de zona, AVA o ANP, concurrencia federal-local y área que atiende, y vuelve a derivar la celda UGA con la versión vigente de la malla | El mismo punto da el mismo resultado en el prototipo y en el servicio sobre al menos cincuenta puntos de prueba que cubran las seis situaciones de la jerarquía de turnado, bordes y traslapes | Documento 11, fase 3; P-12; DEC-117 |
| **SIA-06** | **Geocodificación propia**, sólo como comodidad: propone el punto a partir de la dirección y nunca lo fija. **No puede publicarse apuntando al servicio público de Nominatim**, que lo prohíbe. Ruta recomendada: buscador propio con el catálogo de colonias y la capa de vialidades de la Ciudad; Photon autoalojado como respaldo | La dirección de quien denuncia no sale de la Secretaría, y si el servicio cae el formulario sigue sirviendo | P-12, B-10 |
| **SIA-07** | **Catálogo oficial de colonias y códigos postales**, con su mecanismo de actualización, para validar la dirección y la estadística por colonia. Hoy el prototipo usa el IECM 2022 con su clave CVEUT | Catálogo cargado como tabla y versión registrada | P-16 |
| **SIA-08** | **Resolución de enlaces cortos de Google Maps** (`maps.app.goo.gl`). Servicio de una sola función: lista blanca de `maps.app.goo.gl`, `goo.gl` y `g.co`; se lee el encabezado `Location` sin seguir la redirección ni leer el cuerpo; tres segundos de espera, máximo dos redirecciones, sólo hacia `google.com/maps`; devuelve la coordenada o un error | Cumple las seis condiciones de la ficha de P-18 y tiene límite de peticiones por origen | P-18, DEC-88, RN-15 |
| **SIA-09** | **Ubicar al recibir las denuncias que llegan sin punto.** Con dirección y sin punto, el servidor geocodifica al guardar y aplica el cruce; lo que no resuelva va a la bandeja «por ubicar» con `ubicacion_origen` = «direccion» | El plazo para turnar no se consume esperando a que alguien ubique a mano lo que el servidor podía ubicar | DEC-123 |

### Fase 4 · Versión funcional del formulario

| Clave | Tarea | Se da por hecha cuando | Origen |
|---|---|---|---|
| **SIA-10** | **Alta y guardado de la denuncia**, con la validación completa repetida en el servidor: obligatoriedad por ruta, formatos, código postal del lugar entre 01000 y 16999, relato mínimo y prueba de texto legible, y punto dentro de la Ciudad verificado contra las capas | Una petición que se salta el navegador recibe el mismo rechazo, con el mismo motivo, que la pantalla | Documento 15, §3; RN-30 |
| **SIA-11** | **Folio y clave de consulta**, conforme al documento 19: `SEDEMA/DEN/AAAA/NNNNNN-V`, consecutivo de una secuencia de la base por año, carácter verificador Luhn sobre año y consecutivo, año del reloj del servidor en hora de la Ciudad. **Sólo se emite después de guardar**; un número perdido no se rellena ni se reasigna. Clave aleatoria de ocho caracteres sin 0, O, 1, I ni L, de la que **se guarda sólo la huella** | El navegador ya no genera folios; los casos particulares del documento 19, §6, se comportan como dice la tabla | Documento 19; DEC-151; RN-27 |
| **SIA-12** | **Evidencias.** Almacenamiento de hasta 10 archivos de hasta 25 MB (supuesto de P-06, por confirmar), con verificación del tipo real del archivo y no sólo de su extensión. Se conservan la huella SHA-256 del original y la fecha y el lugar de captura que el navegador extrajo antes de optimizar la foto. **Video y PDF escaneados pesados se optimizan en el servidor**, no en el teléfono | La huella guardada coincide con la que muestra el acuse, y una foto optimizada conserva su fecha y su lugar en el expediente | DEC-121; P-06 |
| **SIA-13** | **Acuse con los datos del servidor.** El PDF lleva el folio, la clave y la hora que emite el servidor; se apaga la marca «PROTOTIPO» y su leyenda (`ACUSE_PROTOTIPO`); el apartado «Fundamento» se llena cuando se resuelva P-01 —hoy es un hueco visible—. Conviene que el servidor guarde una copia del acuse en el expediente | El acuse descargado y el registro de la base dicen lo mismo | DEC-139, DEC-175; P-01 |
| **SIA-14** | **Croquis del acuse con calles.** El croquis actual se dibuja con las capas simplificadas y no trae calles. Con el servidor: mapa base con calles y nombres de vialidades, límite de la colonia y capas completas; dos vías, mosaicos del SIA con acceso entre dominios o acuse generado en el servidor | El recuadro del entorno muestra calles en zona urbana | AD-04 |
| **SIA-15** | **Prueba de humanidad**, siempre, también en la ruta anónima. El token se verifica **en el servidor**; si el servicio no responde, la denuncia se acepta y se marca para revisión. Recomendación: prueba de trabajo autoalojada; si se prefiere un servicio gestionado, la variante no intrusiva y declarada en el aviso de privacidad; nunca acertijos visuales | Tecnología elegida con la Unidad de Transparencia y verificación en servidor probada | Documento 15, control 1; DEC-86 |
| **SIA-16** | **Límite por origen y ventana de tiempo**, deslizante, con las cifras propuestas del documento 15 a confirmar con la DGIVA: 5 por red en una hora y 3 por navegador en una hora endurecen la prueba; 20 por red en un día muestran la pantalla de límite; 50 por red en un día cortan y avisan al área. **Las cifras no se publican** | La pantalla de límite que ya trae el prototipo responde al límite real y no emite folio | Documento 15, control 2; DEC-86 |
| **SIA-17** | **Configuración fuera del código.** La clave del mapa base pasa de `configuracion-local.js` a variable de entorno; se alojan en la Secretaría la biblioteca del mapa y las tipografías, hoy servidas por `cdnjs.cloudflare.com` y `fonts.googleapis.com`; el dominio y los correos institucionales salen del código | Cambiar de dominio o de proveedor no obliga a tocar el código | B-09, B-10, DEC-36 |
| **SIA-18** | **Retirar del sitio público lo que sólo sirve para validar**: el panel de validación con sus escenarios de prueba, el modo revisión con su liga a la hoja de Google, el folio y la clave simulados, y la geocodificación de prueba. El cruce en el navegador puede quedarse como vista previa, pero **el que decide es el del servidor** | Ninguna de esas piezas carga en la versión publicada | DEC-153; documento 11, §6 |
| **SIA-19** | **Separar el archivo único** en estructura, estilos, catálogos servidos por la interfaz y módulos, para que el área sustantiva actualice una materia o un giro sin tocar el código | La estructura del documento 11, §5, está en el repositorio | Documento 11, §5 |

### Antes del primer dato real

| Clave | Tarea | Se da por hecha cuando | Origen |
|---|---|---|---|
| **SIA-20** | **Auditoría de datos personales** (auditoría 16): control de acceso por perfil, bitácora de consultas y de cambios, cifrado en tránsito y en reposo, política de conservación y supresión, y tratamiento de los datos de terceros señalados como responsables | Auditoría corrida y política aprobada con la Unidad de Transparencia | Documento 12, §4; documento 09; AD-01 |
| **SIA-21** | **Auditoría de rendimiento** (auditoría 12), medida con red limitada | Tiempo de carga medido en teléfono con red lenta | Documento 12, §4 |
| **SIA-22** | **Prueba controlada** con un grupo reducido de personas usuarias y con personal de la DGIVA antes de la publicación abierta | Criterio de salida de la fase 4 cumplido | Documento 11, fase 4 |

### Fases 5 y 6 · Módulo interno y seguimiento ciudadano

| Clave | Tarea | Se da por hecha cuando | Origen |
|---|---|---|---|
| **SIA-23** | **Cuentas institucionales nominales** del personal, administradas por el SIA, con perfiles de captura, consulta, atención y administración; el de atención sólo ve las denuncias de su área | Bitácora de accesos operando | AD-01, AD-03 |
| **SIA-24** | **Captura por personal** de lo que llega por Oficialía de Partes, teléfono, correo o comparecencia, en la misma serie de folios, con aviso de denuncias cercanas en lugar y fecha | Una semana de operación con todo lo recibido, por cualquier canal, en el sistema | AD-03; documento 11, fase 5 |
| **SIA-25** | **Bandeja, detalle, tablero y exportación** del módulo interno, con los indicadores del documento 15, §6: denuncias concluidas sin materia, expedientes acumulados por duplicado y tiempo hasta la primera valoración | El tablero distingue por canal | AD-01; documento 15, §6 |
| **SIA-26** | **Controles contra el abuso que siguen abiertos**: detección de duplicados por materia, punto y ventana de días, que acumula en lugar de abrir otro expediente; umbral de ráfaga que marca sin rechazar; y puntaje de completitud que ordena la cola. La verificación del correo no aplica mientras no haya servicio de envío | Decididos con la DGIVA y operando en el servidor | P-21, controles 3 a 6 |
| **SIA-27** | **Consulta ciudadana por folio y clave**: rechaza de inmediato un folio con carácter verificador inválido, compara la clave contra su huella y muestra sólo los estados visibles que defina P-14, sin datos personales en pantalla | Opera sobre estados que el módulo interno registra efectivamente | AD-02; P-14; documento 19, §4 |
| **SIA-28** | **Migración de la base histórica** al modelo nuevo, en lugar de recapturarla | Serie histórica comparable con la del formulario | AD-03, CP-5 (recomendación) |

---

## 3. Lo que el SIA necesita de otros para cerrar su parte

| Lo que falta | Quién lo da | Detiene |
|---|---|---|
| Naturaleza jurídica del canal (P-01): define estados, plazos y el fundamento del acuse | Oficina de la Secretaría, área jurídica | SIA-13, SIA-25, SIA-27 |
| Aviso de privacidad reexpedido y sus seis datos (P-02, P-19) | Unidad de Transparencia | La publicación; SIA-15 si se elige servicio gestionado |
| Catálogo de colonias, códigos postales y vialidades (P-16) | Agencia Digital de Innovación Pública | SIA-06, SIA-07 |
| Cifras definitivas de los límites y criterio de acumulación de duplicados | Dirección General de Inspección y Vigilancia Ambiental | SIA-16, SIA-26 |
| Número y peso de archivos admitidos (P-06) | Dirección General de Inspección y Vigilancia Ambiental | SIA-12 |
| Catálogo de giros o padrón de fuentes fijas | Dirección General de Inspección y Vigilancia Ambiental | SIA-02 |
| Catálogo de estados del expediente y estados visibles (P-14) | Área sustantiva | SIA-25, SIA-27 |
| Acta de validación del formulario | Dirección General de Inspección y Vigilancia Ambiental | Toda la fase 2 |

---

## 4. Registro de avance

| Clave | Fecha | Cómo se cerró |
|---|---|---|
| — | — | Ninguna tarea cerrada todavía |
