# Formulario web de Denuncia Ambiental · Ficha del proyecto

**Área responsable:** Secretaría del Medio Ambiente de la Ciudad de México · Dirección General de Inspección y Vigilancia Ambiental
**Titularidad del desarrollo:** Sistema de Información Ambiental, Secretaría del Medio Ambiente de la Ciudad de México
**Control de versiones:** repositorio git en la carpeta del proyecto, desde el 18 de septiembre de 2026, publicado en `SedemaOficina/denuncia-ambiental`
**Nota sobre el historial:** el historial se reescribió el 19 de septiembre de 2026 para retirar de él un documento de trabajo de la Dirección General de Inspección y Vigilancia Ambiental que no debía publicarse. La reescritura creó commits nuevos con **raíz nueva** (`b28e8b5`), sin ancestro común con la publicada antes (`fef6652`). El repositorio en GitHub se borró y se creó de nuevo para que ningún objeto de la historia anterior quedara almacenado ahí. Los cuatro primeros commits conservan sus mensajes originales y su contenido, sin ese documento; **no hay nada perdido**. Quien encuentre referencias a identificadores anteriores a `b28e8b5` está mirando la historia previa a la limpieza
**Estado:** prototipo navegable en validación, publicado como versión de prueba en GitHub Pages (DEC-127)
**Última actualización:** 30 de septiembre de 2026

---

## 1. Objeto

Sustituir el canal actual de recepción de denuncias ambientales —formato en PDF entregado en Oficialía de Partes o enviado por correo electrónico— por un formulario web que capture la denuncia de forma estructurada, la georreferencie y la turne automáticamente al área competente.

## 2. Diagnóstico

El canal vigente presenta cinco deficiencias que el formulario corrige:

1. **El formato público está desactualizado.** Fue elaborado en 2016, señala como domicilio de seguimiento Tlaxcoaque No. 8 —que ya no corresponde— y su aviso de privacidad se funda en la Ley de Protección de Datos Personales para el Distrito Federal y remite al InfoDF, ambos superados.
2. **El fundamento jurídico difundido está abrogado.** La página institucional cita la Ley Ambiental de Protección a la Tierra en la Ciudad de México, abrogada por la Ley Ambiental de la Ciudad de México publicada el 18 de julio de 2024.
3. **No existe filtro de competencia.** Una proporción relevante de las denuncias recibidas corresponde a otras autoridades, lo que consume capacidad de análisis sin producir actos de inspección.
4. **La ubicación se captura en texto libre.** Sin coordenada no es posible programar eficientemente la visita ni construir estadística territorial de incidencia.
5. **La denuncia no se clasifica en origen.** El turnado exige lectura previa de cada escrito.

## 3. Alcance

| Incluye | No incluye |
|---|---|
| Captura estructurada de la denuncia | Sustitución de la Oficialía de Partes; el canal presencial se conserva |
| Filtro previo de competencia y derivación | Sustanciación del procedimiento administrativo de inspección |
| Georreferenciación y determinación automática del área competente | Notificación electrónica: no hay servicio de envío de correos (DEC-134) |
| Carga de elementos probatorios | Consulta pública del estado del expediente (etapa 3) |
| Folio y acuse en PDF que la persona descarga | Módulo de administración y seguimiento (etapa 2, diferida) |
| | Interoperabilidad con la PAOT o el INVEA (etapa 3) |

## 4. Actores

- **Dirección General de Inspección y Vigilancia Ambiental.** Autoridad sustantiva; define reglas de procedencia y recibe las denuncias en suelo urbano y Áreas de Valor Ambiental, por conducto de su Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano.
- **Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural.** Recibe las denuncias en suelo de conservación y Áreas Naturales Protegidas **locales**, por conducto de su Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas. Las Áreas Naturales Protegidas **federales**, con convenio o sin él, se turnan hoy a la PROFEPA, porque el convenio reparte administración y manejo y deja a salvo las facultades federales de inspección. **Es un criterio provisional, a consulta de las áreas (P-22).**
- **Oficina de la Secretaría.** Coordinación del proyecto y enlace entre áreas.
- **Sistema de Información Ambiental.** Provee las capas geográficas y, en la versión funcional, los servicios de geocodificación y cruce espacial.
- **Autoridades receptoras por derivación.** Secretaría de Obras y Servicios, Secretaría de Seguridad Ciudadana, PAOT, PROFEPA, INVEA, Agencia de Atención Animal y alcaldías.

## 5. Arquitectura por etapas

Tres etapas, en el orden que fijó la Oficina de la Secretaría. El documento 11 las desglosa en fases con criterio de salida.

**Etapa 1 — Validar el formulario (en curso).** Prototipo navegable, sin servidor, con las capas del Sistema de Información Ambiental embebidas y una versión de prueba en GitHub Pages. Cierra con el acta de validación de la Dirección General de Inspección y Vigilancia Ambiental y la resolución de P-01 y P-02.

**Etapa 2 — Módulo de acceso de la Secretaría.** Entrada protegida para el personal, con cuentas institucionales, bandeja de denuncias y tablero de indicadores, sobre la misma base que el formulario (AD-01). Se construye sobre el modelo de datos validado en la etapa 1.

**Etapa 3 — Implementación en el SIA.** El servidor del Sistema de Información Ambiental recibe y guarda la denuncia, emite el folio, resuelve el cruce espacial contra las capas completas, la geocodificación y los controles contra el envío masivo, y sostiene la consulta ciudadana por folio (AD-02). El detalle está en el documento «Qué resuelve el servidor del SIA».

## 6. Ubicación de los archivos

El proyecto tiene una carpeta local vinculada a esta sesión de trabajo:

`…\SEDEMA\Sistema de Información Ambiental\Páginas web\Denuncias Ambientales`

| Carpeta | Contenido |
|---|---|
| `prototipo/` | Prototipo navegable del formulario, en un archivo HTML autocontenido |
| `documentacion/` | Los diecisiete documentos de este proyecto y la cédula de respuesta a la DGIVA |
| `capas/` | Capas del Sistema de Información Ambiental empleadas por el formulario |
| `construccion/` | Cadena que genera la versión en línea, la de GitHub Pages y los documentos 09 y 10, y las baterías de prueba |
| `insumos/` | Formato público vigente, propuesta de la Dirección General y Ley Ambiental |

Los entregables se escriben directamente en esa carpeta. La documentación se mantiene además en el proyecto de Claude, de modo que las dos copias se actualizan a la vez.

## 7. Insumos recibidos

| Insumo | Origen | Uso |
|---|---|---|
| Ficha de Denuncia, formato público | Portal de la Secretaría, versión 2016 | Línea base de campos |
| Información básica obligatoria para presentar una denuncia | Dirección General de Inspección y Vigilancia Ambiental | Propuesta de reestructura de campos |
| `alcaldias.geojson` (16 polígonos) | Sistema de Información Ambiental | Determinación de alcaldía |
| `geometrias.geojson` (66 polígonos: 13 bosques urbanos, 26 barrancas, 18 ANP locales, 9 ANP federales) | Sistema de Información Ambiental | Determinación de AVA y ANP |
| `suelo_conservacion.geojson` (7 polígonos) | Sistema de Información Ambiental | Determinación de suelo de conservación |
| Convenio Marco de Coordinación CONANP–CDMX (firma 10 mar 2025, vigencia 30 sep 2030) | Secretaría del Medio Ambiente | Catálogo de las ocho ANP coadministradas y regla de competencia |
| Manual Administrativo de la SEDEMA | Secretaría del Medio Ambiente | Nombres de las unidades que atienden y plazos del procedimiento |
| Manual de Identidad Gráfica Institucional 2024-2030 y set de iconos | Gobierno de la Ciudad de México | Identidad visual del formulario |
| Ley Ambiental de la Ciudad de México, Gaceta Oficial 18 de julio de 2024 | Congreso de la Ciudad de México | Fundamento jurídico |
| Colonias del IECM 2022 (1 837 unidades territoriales) | Sistema de Información Ambiental | Catálogo de colonias de la dirección y del domicilio |
| Malla UGA (1 624 celdas de ~1 km², versión del 22-09-2026) | Sistema de Información Ambiental | Celda del punto, para operativos y estadística |
