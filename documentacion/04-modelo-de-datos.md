# Formulario web de Denuncia Ambiental · Modelo de datos

**Versión:** 2.0 · 30 de septiembre de 2026
**Para qué sirve este documento.** Describe de dónde sale cada dato, los catálogos contra los que se valida y las capas que deciden la competencia. **La lista de campos no se escribe aquí**: vive en el documento 09, que se genera del código (`OBLIG` y `DERIVADOS`) cada vez que el formulario cambia, y así no puede quedarse atrás. La versión 1.0 de este documento enumeraba los campos a mano y se desactualizó en días (DEC-146).

---

## 1. Origen de los datos

Cada dato del expediente tiene uno de cuatro orígenes. El documento 09 los separa en «campos que llena la persona» y «campos que viajan a la base y no se ven en pantalla».

| Origen | Qué es | Ejemplos |
|---|---|---|
| **Captura** | Lo escribe o elige la persona | Materia, dirección, relato, datos de contacto |
| **Cruce espacial** | Lo determina el punto contra las capas del SIA | Alcaldía del punto, tipo de suelo, área que atiende, celda UGA |
| **Catálogo** | Sale de una lista cerrada al elegir | Clave de la colonia (IECM 2022), alcaldía de la dirección |
| **Sistema** | Lo pone el formulario o el servidor | Folio, fecha y hora de recepción, origen de la ubicación, huella de las fotos |

En el prototipo el cruce espacial y el folio los resuelve el navegador; en operación los resuelve el servidor del SIA (documento «Qué resuelve el servidor del SIA»).

## 2. Rutas que cambian el esquema

| Ruta | Qué cambia |
|---|---|
| Lugar con dirección · sin dirección | Con dirección, calle, número exterior, alcaldía, colonia y código postal son obligatorios y el punto es opcional (DEC-123). Sin dirección, el punto es obligatorio y se piden nombre del lugar y referencias |
| Denuncia con datos · anónima | Con datos: nombre, teléfono, correo y domicilio para notificaciones. Anónima: sólo un correo de contacto, obligatorio (DEC-120, DEC-134) |
| Domicilio en la Ciudad · fuera de ella | En la Ciudad: alcaldía en lista, colonia del catálogo y código postal del 01000 al 16999. Fuera: entidad en lista, municipio y colonia escritos (DEC-135, DEC-136) |
| Establecimiento · otro giro | «Otro» abre el campo para especificarlo |
| Quién responde | Persona, empresa, autoridad o «no lo sé» cambian el bloque de datos del responsable |

## 3. Catálogos

| Catálogo | Valores | Fuente | Dónde se declara |
|---|---|---|---|
| Materias | 19, en cinco grupos | Ley Ambiental y base histórica (documento 17) | `MATERIAS`, `GRUPOS_MATERIA` |
| Casos de otra autoridad | 7 | Formato vigente y base histórica | `DERIVA` |
| Giros de establecimiento | 18 más «Otro» | Provisional, a la espera del catálogo de la Dirección General | `TIPOS_ESTAB` |
| Alcaldías | 16 | Capa de alcaldías del SIA | `CATALOGO_COLONIAS.alcaldias` |
| Colonias | 1 837 unidades territoriales | IECM 2022 | `CATALOGO_COLONIAS` |
| Entidades federativas | 31, sin la Ciudad | — | `ENTIDADES_FUERA` |
| Celdas UGA | 1 624 hexágonos de ~1 km² | Malla del SIA, versión del 22-09-2026 | `CATALOGO_UGA` |
| Formatos de archivo | JPG, JPEG, PNG, MP4, MOV, Word, PDF y Excel; 10 archivos de hasta 25 MB | DEC-120 | `ARCHIVOS` |

## 4. Folio y acuse

- **Folio.** `SEDEMA/DEN/AAAA/NNNNNN-V`: año de recepción, consecutivo único de seis dígitos y carácter verificador. No lleva el área: la que atiende es el dato `dg` del expediente (DEC-151, documento 19).
- **Clave de consulta** (`clave_consulta`). Ocho caracteres aleatorios, `XXXX-XXXX`, sin 0, O, 1, I ni L. Con el folio, abre la consulta ciudadana (AD-02). El servidor guarda sólo su huella; no puede reponerse.
- **Acuse.** PDF que la persona descarga al terminar: no se envía por correo (DEC-134, DEC-139). Lleva el folio, la clave de consulta, la fecha de recepción, todo lo revisado y las huellas de las fotografías.

## 5. Capas geográficas

| Capa | Archivo | Rasgos | Uso |
|---|---|---|---|
| Alcaldías | `alcaldias.geojson` | 16 | Alcaldía del punto |
| Áreas de Valor Ambiental y Áreas Naturales Protegidas | `geometrias.geojson` | 66: 13 bosques urbanos, 26 barrancas, 18 ANP locales, 9 ANP federales | AVA y ANP |
| Suelo de conservación | `suelo_conservacion.geojson` | 7 | Suelo de conservación |
| Colonias | `capas/originales/colonias_iecm2022.geojson` | 1 837 | Catálogo de colonias |
| Malla UGA | `capas/originales/UGA_CDMX.geojson` | 1 624 | Celda UGA del punto |

En el prototipo las geometrías se simplificaron a una tolerancia aproximada de ocho metros para reducir el peso del archivo. **En operación el cruce se resuelve en el servidor contra las capas completas.**

### Brechas detectadas en las capas

1. El artículo 116 de la Ley reconoce cuatro categorías de Área de Valor Ambiental: bosques urbanos, cinturones verdes, barrancas y cuerpos de agua de competencia de la Ciudad. La capa contiene bosques urbanos y barrancas, las únicas categorías con declaratoria a la fecha.
2. La capa contiene nueve Áreas Naturales Protegidas federales y el convenio de coadministración enumera ocho. La diferencia es **El Histórico Coyoacán**, que el formulario remite a la PROFEPA (P-03).
3. Hay traslapes entre decretos federales y locales sobre la misma superficie: Cerro de la Estrella y Sierra de Guadalupe.
4. Las categorías de la capa de origen se normalizaron al ingresarla (P-11, resuelto en el proyecto).
