# Formulario web de Denuncia Ambiental · Modelo de datos

**Versión:** 1.0 · 18 de septiembre de 2026
Origen: **C** captura directa · **D** derivado del cruce espacial · **G** propuesto por geocodificación, editable · **S** generado por el sistema

---

## 1. Clasificación

| Clave | Etiqueta | Tipo | Origen | Obligatorio | Notas |
|---|---|---|---|---|---|
| `materia` | Materia de la denuncia | Catálogo (10) | C | Sí | Determina el área sustantiva, no el turnado |
| `deriva` | Supuesto de derivación | Catálogo (7) | C | No | Excluyente con `materia`; impide la captura |

## 2. Lugar de los hechos

| Clave | Etiqueta | Tipo | Origen | Obligatorio | Notas |
|---|---|---|---|---|---|
| `lat` / `lon` | Coordenadas | Decimal, 6 posiciones | C | Sí | Dato rector; valor procesal conforme al art. 282 |
| `alcaldia` | Alcaldía | Catálogo (16) | D | Sí | Cruce con `alcaldias.geojson` |
| `colonia` | Colonia | Texto | G | Sí | |
| `cp` | Código postal | Texto, 5 dígitos | G | Sí | |
| `calle` | Calle y número | Texto | G | Sí | |
| `entre_calle1` · `entre_calle2` | Entre calles | Texto | C | No | |
| `fachada` | Color o características de la fachada | Texto | C | No | |
| `redes` | Redes sociales o nombre comercial | Texto | C | No | Insumo para identificar al presunto responsable |
| `referencias` | Otras referencias | Texto largo | C | No | |
| `capa_tipo` | Tipo de suelo | Derivado | D | — | Suelo urbano, AVA, ANP local, ANP federal o suelo de conservación |
| `capa_nombre` | Área identificada | Derivado | D | — | Nombre del polígono |
| `dg` · `dg_nombre` · `dg_razon` | Área que atiende y motivación | Derivado | D | — | Conforme a RN-04 |
| `coadmin` · `decreto` · `superficie` | Coadministración, decreto y superficie | Derivado | D | — | Sólo en ANP federales del catálogo |
| `concurrencia` | Concurrencia de competencias | Derivado | D | — | Traslape federal y local |
| `fuera` | Punto fuera de la Ciudad | Booleano | D | — | |

## 3. Hechos

| Clave | Etiqueta | Tipo | Origen | Obligatorio | Notas |
|---|---|---|---|---|---|
| `hechos` | Descripción de los hechos | Texto largo | C | Sí | Extensión mínima sugerida de 40 caracteres |
| `temporalidad` | Temporalidad | Catálogo (único, recurrente, permanente) | C | No | |
| `fecha_hecho` | Fecha en que ocurrió o inició | Fecha | C | No | |
| `horario` | Horario en que se presenta | Texto | C | No | |
| `establecimiento` | Nombre o razón social | Texto | C | No | |
| `responsables` | Personas señaladas como responsables | Texto largo | C | No | |
| `permisos` | Permisos o autorizaciones conocidos | Texto largo | C | No | |

## 4. Elementos probatorios

| Clave | Etiqueta | Tipo | Origen | Obligatorio | Notas |
|---|---|---|---|---|---|
| `archivos[]` | Archivos adjuntos | Fotografía, video o documento | C | No | Máximo sujeto a confirmación: 10 archivos de 25 MB |
| `otras_pruebas` | Pruebas que no pueden adjuntarse | Texto largo | C | No | |

## 5. Persona denunciante

| Clave | Etiqueta | Tipo | Origen | Obligatorio | Notas |
|---|---|---|---|---|---|
| `anonima` | Denuncia anónima | Booleano | C | — | Si es afirmativa, se omite todo el bloque |
| `nombre` | Nombre | Texto | C | Sí | |
| `apellido_paterno` | Apellido paterno | Texto | C | Sí | |
| `apellido_materno` | Apellido materno | Texto | C | No | |
| `telefono` | Teléfono | Texto, 10 dígitos | C | Sí | |
| `correo` | Correo electrónico | Correo | C | Sí | Destino del acuse |
| `dom_calle` · `dom_num_ext` · `dom_num_int` | Domicilio, vialidad y números | Texto | C | Sí salvo interior | |
| `dom_colonia` · `dom_cp` | Colonia y código postal | Texto | C | Sí | |
| `dom_alcaldia` · `dom_entidad` | Alcaldía o municipio y entidad | Texto | C | Sí | Admite domicilios fuera de la Ciudad |
| `privacidad` | Protesta de decir verdad y consentimiento | Booleano | C | Sí | |

## 6. Acuse

| Clave | Etiqueta | Tipo | Origen | Notas |
|---|---|---|---|---|
| `folio` | Folio | Texto | S | `SEDEMA/DGIVA/DEN/AAAA/NNNNNN` |
| `fecha_acuse` | Fecha y hora de recepción | Fecha y hora | S | |

## 7. Capas geográficas

| Capa | Archivo | Rasgos | Uso |
|---|---|---|---|
| Alcaldías | `alcaldias.geojson` | 16 | Determinación de alcaldía |
| Áreas de Valor Ambiental y Áreas Naturales Protegidas | `geometrias.geojson` | 66: 13 bosques urbanos, 26 barrancas, 18 ANP locales, 9 ANP federales | Determinación de AVA y ANP |
| Suelo de conservación | `suelo_conservacion.geojson` | 7 | Determinación de suelo de conservación |

En el prototipo las geometrías se simplificaron a una tolerancia aproximada de ocho metros para reducir el peso del archivo. **En la versión funcional el cruce debe resolverse en servidor contra las capas completas.**

### Brechas detectadas en las capas

1. El artículo 116 de la Ley reconoce cuatro categorías de Área de Valor Ambiental: bosques urbanos, cinturones verdes, barrancas y cuerpos de agua de competencia de la Ciudad. La capa contiene bosques urbanos y barrancas, que son las únicas categorías con declaratoria a la fecha; **no existen todavía cinturones verdes ni cuerpos de agua declarados**, por lo que la cobertura es completa. La estructura del cruce ya admite ambas categorías cuando se expidan sus decretos.
2. La capa contiene nueve Áreas Naturales Protegidas federales, mientras que el catálogo de convenios de coadministración enumera ocho. La diferencia es **El Histórico Coyoacán**, único caso que el formulario deriva a la PROFEPA.
3. Existen traslapes entre decretos federales y locales sobre la misma superficie: Cerro de la Estrella y Sierra de Guadalupe. La Sierra de Santa Catarina aparece duplicada como Zona de Conservación Ecológica y como Zona Sujeta a Conservación Ecológica.
4. Los nombres de categoría presentan inconsistencias de acentuación —"Zona Ecologica y Cultural" frente a "Zona Ecológica y Cultural", "Zona Sujeta a Conservacion Ecologica" frente a su forma acentuada—, lo que impide agrupar por categoría sin normalización previa.
