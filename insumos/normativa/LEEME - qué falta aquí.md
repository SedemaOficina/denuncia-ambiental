# Formulario web de Denuncia Ambiental · Normativa por integrar

**Versión:** 1.0 · 18 de septiembre de 2026
**Para qué sirve este documento.** Enumera los ordenamientos que hacen falta en la carpeta `insumos/normativa/` del proyecto, qué pendiente resuelve cada uno y qué se cita hoy sin haberlo verificado. Mientras un documento no esté aquí, lo que el formulario afirma sobre esa materia es criterio, no fundamento.

Lo ya integrado: **Ley Ambiental de la Ciudad de México** (18 jul 2024) y **Ley Orgánica de la PAOT** (última reforma 24 dic 2025).

---

## 1. Indispensables · desbloquean un pendiente abierto

| Ordenamiento | Qué resuelve | Pendiente |
|---|---|---|
| **Reglamento Interior del Poder Ejecutivo y de la Administración Pública de la Ciudad de México** | Los artículos que reparten la inspección y vigilancia entre la Dirección General de Inspección y Vigilancia Ambiental y la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural. La Ley Ambiental sólo atribuye a *la Secretaría*, de forma genérica | **P-17** |
| **Manual Administrativo de la SEDEMA**, con su dictamen de estructura vigente | Ubicación, adscripción y atribuciones de la **Coordinación de Inspección y Vigilancia** de la DGCORENADR; si puede ordenar visitas y sustanciar el procedimiento o sólo ejecutarlas | **P-17**, y perfiles de usuario de **AD-01** |
| **Ley de Residuos Sólidos de la Ciudad de México y su Reglamento** | Dos de las dieciocho materias se fundan en ella y hoy se citan sin artículo: residuos sólidos urbanos de establecimientos y residuos de la construcción | Citas del catálogo |
| **Ley de Protección de Datos Personales en Posesión de Sujetos Obligados de la Ciudad de México** y sus lineamientos | Reexpedición del aviso de privacidad, que hoy se funda en normativa abrogada | **P-02** |
| **Reglamento de la Ley Orgánica de la PAOT** | Trámite de la denuncia, ratificación y reconocimiento de hechos. La Ley Orgánica remite a él en los artículos 21 y 25 | **P-01** |
| **Convenios de coadministración** de las ocho Áreas Naturales Protegidas federales | Fundamento de que la Secretaría atienda en ellas, y si El Histórico Coyoacán quedó fuera deliberadamente | **P-03**, **P-04** |
| **Norma Ambiental NADF-001-RNAT-2015** | Qué constituye poda, derribo o trasplante indebido; hoy se cita la norma sin poder precisar la conducta | Materia de arbolado |

## 2. Necesarios · sostienen citas que ya están en el prototipo

| Ordenamiento | Para qué |
|---|---|
| **Reglamento de la Ley Ambiental** y **Reglamento de Impacto Ambiental y Riesgo** | El transitorio SEXTO de la Ley Ambiental los mantiene vigentes en lo que no se opongan. Precisan el procedimiento de evaluación de impacto ambiental y las obras que lo requieren |
| **Ley Orgánica del Poder Ejecutivo y de la Administración Pública de la Ciudad de México** | El artículo 7 de la Ley Ambiental remite a ella para las facultades de la Secretaría |
| **Ley de Procedimiento Administrativo de la Ciudad de México** | Supletoria del procedimiento de inspección conforme al artículo 276 |
| **Código Penal para la Ciudad de México**, artículo 344 Bis | Se cita en tres materias —terráceos, cascajo y tala—; falta verificar el texto vigente |
| **Ley de Cultura Cívica de la Ciudad de México** | Sustenta la derivación del ruido entre particulares a la Secretaría de Seguridad Ciudadana, conforme al artículo 215, fracción IV, de la Ley Ambiental |
| **Ley del Instituto de Verificación Administrativa de la Ciudad de México** | Sustenta la vía del artículo 215, fracción I, inciso h): la Secretaría solicita al INVEA la visita en establecimientos mercantiles |
| **Programa General de Ordenamiento Territorial** | El artículo 92 define el suelo de conservación por remisión a este programa |

## 3. Útiles · mejoran el instrumento sin bloquearlo

| Documento | Para qué |
|---|---|
| **Decretos de las Áreas de Valor Ambiental y de las Áreas Naturales Protegidas locales** | Verificar nombres, superficies y categorías contra la capa `geometrias.geojson`, y resolver las inconsistencias de acentuación y los traslapes |
| **Normas ambientales locales de ruido, emisiones y descargas** | Enunciar en el formulario los límites permisibles, de modo que la persona sepa si lo que percibe es probablemente una infracción |
| **Catálogo de giros o padrón de fuentes fijas de la Secretaría** | Sustituir el catálogo provisional de tipos de establecimiento y permitir cruzar la denuncia contra el padrón desde el primer momento |
| **Formatos y machotes vigentes** de orden de visita, acta de inspección y acuerdo de improcedencia | Alinear los campos capturados con lo que el acta necesita, para que el inspector no tenga que volver a pedir datos |
| **Lineamientos de accesibilidad web** del Gobierno de la Ciudad, si existen | Verificar el formulario contra el criterio propio de la administración, además de las WCAG |

## 4. Cómo integrarlos

Colocar los archivos en `insumos/normativa/` con el nombre del ordenamiento y la fecha de la última reforma, por ejemplo `Reglamento Interior PEAP CDMX - ref 00 mmm 2026.pdf`. Al incorporar cada uno se actualiza la columna correspondiente de este documento y, cuando proceda, la cita en el catálogo de materias y en el documento de marco jurídico.

**Criterio que se mantiene:** no se escribe en el prototipo ningún número de artículo, fracción o numeral que no se haya verificado contra el texto vigente. Donde falta, se deja el hueco visible.
