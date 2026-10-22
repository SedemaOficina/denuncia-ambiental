# Formulario web de Denuncia Ambiental · Modelo de datos

**Versión:** 2.1 · 20 de octubre de 2026 · al día con DEC-200, DEC-226, DEC-233 y DEC-235
**Para qué sirve este documento.** Describe de dónde sale cada dato, los catálogos contra los que se valida y las capas que deciden la competencia. **La lista de campos no se escribe aquí**: vive en el documento 09, que se genera del código (`OBLIG` y `DERIVADOS`) cada vez que el formulario cambia, y así no puede quedarse atrás. La versión 1.0 de este documento enumeraba los campos a mano y se desactualizó en días (DEC-146).

---

## 1. Origen de los datos

Cada dato del expediente tiene uno de cuatro orígenes. El documento 09 los separa en «campos que llena la persona» y «campos que viajan a la base y no se ven en pantalla».

| Origen | Qué es | Ejemplos |
|---|---|---|
| **Captura** | Lo escribe o elige la persona | Materia, dirección, relato, datos de contacto |
| **Cruce espacial** | Lo determina el punto contra las capas del SIA | Alcaldía del punto, tipo de suelo, área que atiende |
| **Catálogo** | Sale de una lista cerrada al elegir | Clave de la colonia (IECM 2022), alcaldía de la dirección |
| **Sistema** | Lo pone el formulario o el servidor | Folio, fecha y hora de recepción, origen de la ubicación, huella de las fotos |

En el prototipo el cruce espacial y el folio los resuelve el navegador; en operación los resuelve el servidor del SIA (documento 20, «Qué resuelve el servidor del SIA»).

**Longitud de cada campo.** Todo campo de texto tiene su máximo en `LIMITES`, que el formulario aplica al capturar y al validar (DEC-235); de ahí la toma el diccionario de datos.

## 2. Rutas que cambian el esquema

| Ruta | Qué cambia |
|---|---|
| Lugar con dirección · sin dirección | Con dirección, calle, número exterior, alcaldía y colonia son obligatorios; el código postal (DEC-200) y el punto (DEC-123) son opcionales. Sin dirección, el punto es obligatorio y se piden nombre del lugar y referencias |
| Denuncia con datos · anónima | Con datos: nombre, teléfono, correo y domicilio para notificaciones. Anónima: sólo un correo, obligatorio, donde se le notifica el resultado, y el teléfono opcional (DEC-120, DEC-233) |
| Domicilio en la Ciudad · fuera de ella | En la Ciudad: alcaldía en lista, colonia del catálogo y código postal del 01000 al 16999. Fuera: entidad en lista, municipio y colonia escritos (DEC-135, DEC-136) |
| Establecimiento · otro giro | «Otro» abre el campo para especificarlo |
| Quién responde | Persona, empresa, autoridad o «no lo sé» cambian el bloque de datos del responsable |

La tabla completa de las ramas, con las respuestas que gobiernan cada una, está en el documento 10, que se genera de `BIFURCACIONES`.

## 3. Catálogos

| Catálogo | Valores | Fuente | Dónde se declara |
|---|---|---|---|
| Materias | 19, en cinco grupos | Ley Ambiental y base histórica (documento 17) | `MATERIAS`, `GRUPOS_MATERIA` |
| Casos de otra autoridad | 7 | Formato vigente y base histórica | `DERIVA` |
| Giros de establecimiento | 18 más «Otro» | Provisional, a la espera del catálogo de la Dirección General | `TIPOS_ESTAB` |
| Alcaldías | 16 | Capa de alcaldías del SIA | `CATALOGO_COLONIAS.alcaldias` |
| Colonias | 1 837 unidades territoriales | IECM 2022 | `CATALOGO_COLONIAS` |
| Entidades federativas | 31, sin la Ciudad | — | `ENTIDADES_FUERA` |
| Formatos de archivo | JPG, JPEG, PNG, MP4, MOV, Word, PDF y Excel; 10 archivos de hasta 25 MB | DEC-120 | `ARCHIVOS` |

## 4. Folio y acuse

- **Folio.** `SEDEMA/DEN/AAAA/NNNNNN-V`: año de recepción en la hora de la Ciudad, consecutivo único de seis dígitos y carácter verificador. No lleva el área: la que recibe es el dato `dg` del expediente, DGIVA o DGCORENADR, y la remisión a la PROFEPA, el dato `remite_a` (DEC-151, DEC-235, documento 19).
- **Fecha de recepción** (`fecha_acuse`). En ISO 8601 con la hora y la zona de la Ciudad de México, por ejemplo `2026-12-31T23:30:00-06:00`, sea cual sea la zona del equipo; la pantalla y el acuse la dicen en palabras (DEC-235).
- **Clave de consulta** (`clave_consulta`). Ocho caracteres aleatorios, `XXXX-XXXX`, sin 0, O, 1, I ni L. Con el folio, abre la consulta ciudadana (AD-02). El servidor guarda sólo su huella; no puede reponerse.
- **Acuse.** PDF que la persona descarga al terminar: no se envía por correo (DEC-134, DEC-139). Lleva el folio, la clave de consulta, la fecha de recepción, todo lo revisado y las huellas de las fotografías.

## 5. Capas geográficas

| Capa | Archivo | Rasgos | Uso |
|---|---|---|---|
| Alcaldías | `alcaldias.geojson` | 16 | Alcaldía del punto |
| Áreas de Valor Ambiental y Áreas Naturales Protegidas | `geometrias.geojson` | 66: 13 bosques urbanos, 26 barrancas, 18 ANP locales, 9 ANP federales | AVA y ANP |
| Suelo de conservación | `suelo_conservacion.geojson` | 7 | Suelo de conservación |
| Colonias | `capas/originales/colonias_iecm2022.geojson` | 1 837 | Catálogo de colonias |

En el prototipo las geometrías se simplificaron a una tolerancia aproximada de ocho metros para reducir el peso del archivo. **En operación el cruce se resuelve en el servidor contra las capas completas.**

### Brechas detectadas en las capas

1. El artículo 116 de la Ley reconoce cuatro categorías de Área de Valor Ambiental: bosques urbanos, cinturones verdes, barrancas y cuerpos de agua de competencia de la Ciudad. La capa contiene bosques urbanos y barrancas, las únicas categorías con declaratoria a la fecha.
2. La capa contiene nueve Áreas Naturales Protegidas federales y el convenio de coadministración enumera ocho. La diferencia es **El Histórico Coyoacán** (P-03). Como en las otras ocho, la denuncia la recibe la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural y la remite a la PROFEPA (DEC-226).
3. Hay traslapes entre decretos federales y locales sobre la misma superficie: Cerro de la Estrella y Sierra de Guadalupe.
4. Las categorías de la capa de origen se normalizaron al ingresarla (P-11, resuelto en el proyecto).
