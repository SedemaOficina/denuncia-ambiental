# Formulario web de Denuncia Ambiental · Ficha del proyecto

**Área responsable:** Secretaría del Medio Ambiente de la Ciudad de México · Dirección General de Inspección y Vigilancia Ambiental
**Titularidad del desarrollo:** Sistema de Información Ambiental, Secretaría del Medio Ambiente de la Ciudad de México
**Control de versiones:** repositorio git en la carpeta del proyecto, desde el 18 de septiembre de 2026, publicado en `SedemaOficina/denuncia-ambiental`
**Nota sobre el historial:** el historial se reescribió el 19 de septiembre de 2026 para retirar de él un documento de trabajo de la Dirección General de Inspección y Vigilancia Ambiental que no debía publicarse. La reescritura creó commits nuevos con **raíz nueva** (`b28e8b5`), sin ancestro común con la publicada antes (`fef6652`). El repositorio en GitHub se borró y se creó de nuevo para que ningún objeto de la historia anterior quedara almacenado ahí. Los cuatro primeros commits conservan sus mensajes originales y su contenido, sin ese documento; **no hay nada perdido**. Quien encuentre referencias a identificadores anteriores a `b28e8b5` está mirando la historia previa a la limpieza
**Estado:** prototipo navegable en validación interna
**Última actualización:** 20 de septiembre de 2026

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
| Georreferenciación y determinación automática del área competente | Notificación electrónica de actos administrativos |
| Carga de elementos probatorios | Consulta pública del estado del expediente (fase 4) |
| Folio y acuse automáticos | Módulo de administración y seguimiento (fase 3, diferida) |
| | Interoperabilidad con la PAOT o el INVEA (fase 4) |

## 4. Actores

- **Dirección General de Inspección y Vigilancia Ambiental.** Autoridad sustantiva; define reglas de procedencia y recibe las denuncias en suelo urbano y Áreas de Valor Ambiental, por conducto de su Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano.
- **Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural.** Recibe las denuncias en suelo de conservación y Áreas Naturales Protegidas **locales**, por conducto de su Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas. Las Áreas Naturales Protegidas **federales**, con convenio o sin él, se turnan hoy a la PROFEPA, porque el convenio reparte administración y manejo y deja a salvo las facultades federales de inspección. **Es un criterio provisional, a consulta de las áreas (P-22).**
- **Oficina de la Secretaría.** Coordinación del proyecto y enlace entre áreas.
- **Sistema de Información Ambiental.** Provee las capas geográficas y, en la versión funcional, los servicios de geocodificación y cruce espacial.
- **Autoridades receptoras por derivación.** Secretaría de Obras y Servicios, Secretaría de Seguridad Ciudadana, PAOT, PROFEPA, INVEA, Agencia de Atención Animal y alcaldías.

## 5. Arquitectura por fases

**Fase 1 — Prototipo navegable (en curso).** Cierra con el acta de validación de la DGIVA y la resolución de P-01 y P-02. Archivo HTML autocontenido, sin servidor, con las capas del Sistema de Información Ambiental embebidas. Sirve para validar el flujo, los campos y las reglas de enrutamiento con la Dirección General de Inspección y Vigilancia Ambiental antes de programar nada.

**Fase 2 — Versión funcional.** Formulario en Google Apps Script con respaldo en Sheets, carga de archivos a Drive, folio consecutivo, acuse en PDF y tablero de seguimiento para el área sustantiva. Permite operar sin depender de tiempos de la Dirección General de Tecnologías de la Información.

**Fase 3 — Módulo de administración y seguimiento.** Herramienta interna para el equipo que atiende las denuncias: usuarios con perfiles diferenciados, bandeja con filtros, detalle de la denuncia con mapa y evidencia, control de estados, tableros de indicadores y exportación. **Diferida hasta que el formulario de denuncia esté validado**, porque se construye sobre su modelo de datos. El alcance previsto está descrito en el documento de decisiones, apartado AD-01.

**Fase 4 — Integración institucional.** Publicación en el portal de la Secretaría, servicios de cruce espacial y geocodificación resueltos en servidor contra las capas completas, y consulta ciudadana del estado de la denuncia por folio.

## 6. Ubicación de los archivos

El proyecto tiene una carpeta local vinculada a esta sesión de trabajo:

`…\SEDEMA\Sistema de Información Ambiental\Páginas web\Denuncias Ambientales`

| Carpeta | Contenido |
|---|---|
| `prototipo/` | Prototipo navegable del formulario, en un archivo HTML autocontenido |
| `documentacion/` | Los quince documentos de este proyecto |
| `capas/` | Capas del Sistema de Información Ambiental empleadas por el formulario |
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
