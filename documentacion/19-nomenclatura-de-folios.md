# Formulario web de Denuncia Ambiental · Nomenclatura de folios

**Versión:** 1.1 · 30 de septiembre de 2026 · **Aprobada (DEC-151): resuelve P-13**
**Para qué sirve este documento.** Fija cómo se forma, quién emite y cómo se usa el folio de una denuncia, y qué se entrega a la persona para consultarla. Hasta hoy sólo existía el supuesto del prototipo (RN-27) y la pregunta abierta P-13.

---

## 1. Recomendación

**Folio sin área, consecutivo único por año y con carácter verificador:**

```
SEDEMA/DEN/2026/000123-3
```

| Segmento | Qué es | Regla |
|---|---|---|
| `SEDEMA` | Dependencia | Fijo |
| `DEN` | Tipo de expediente: denuncia ambiental | Fijo. Distingue la serie de otras de la Secretaría, como los oficios `SEDEMA/OS/…` |
| `2026` | Año de recepción | Año del reloj del servidor, en hora de la Ciudad de México |
| `000123` | Consecutivo | Seis dígitos, único para toda la Secretaría, reinicia el 1 de enero |
| `-3` | Carácter verificador | Calculado del consecutivo y el año; detecta un dígito mal escrito al consultar |

El área que atiende **no va en el folio**: va en el expediente, como dato propio.

## 2. Por qué no llevar el área en el folio

Hasta DEC-151 el prototipo ponía el área en el folio (`SEDEMA/DGIVA/DEN/2026/…`, `SEDEMA/DGCORENADR/…`, `SEDEMA/REM/…`). Tenía tres problemas:

1. **El turnado puede cambiar y el folio no.** Una denuncia sin punto se ubica después (DEC-123); una en ANP federal coadministrada está a consulta (P-22); cualquier área puede devolver un asunto que no es suyo. Un folio que nombra al área equivocada contradice al expediente para siempre.
2. **Obliga a decidir el área antes de guardar.** Sin punto, el prototipo emite un folio sin segmento de área: dos formatos para el mismo documento.
3. **No aporta nada que no diga el expediente.** Quien atiende ve el área en la bandeja (AD-01); quien denuncia la ve en el acuse.

## 3. Quién lo emite y cuándo

- **Sólo el servidor del SIA**, al terminar de guardar la denuncia. Si el guardado falla, no hay folio.
- El consecutivo sale de una secuencia de la base de datos por año. Puede quedar un número sin usar si una operación se interrumpe: **es aceptable y no se rellena**, porque un folio nunca se reasigna.
- El navegador no genera folios. El del prototipo es simulado y así lo dice el acuse («PROTOTIPO»).

## 4. Carácter verificador

Un dígito calculado con el algoritmo de Luhn sobre `año + consecutivo` (`2026000123` → `3`). Sirve para que la consulta por folio rechace de inmediato un folio con un dígito cambiado, sin buscarlo en la base. No es seguridad: la seguridad la da la clave de consulta.

## 5. Clave de consulta

El folio es **consecutivo y predecible**: quien tiene el 000123 puede adivinar el 000124. Por eso la consulta ciudadana (AD-02) pide **folio más clave**.

| Regla | Valor |
|---|---|
| Longitud | 8 caracteres, en dos grupos: `K7PM-4XQ2` |
| Alfabeto | Letras mayúsculas y dígitos, sin los que se confunden (0, O, 1, I, L) |
| Generación | Aleatoria, en el servidor, al emitir el folio |
| Guardado | Sólo su huella, nunca la clave en claro |
| Entrega | En pantalla y en el acuse en PDF, junto al folio. No puede reponerse |

El prototipo la muestra desde DEC-151 en la pantalla final y en el acuse en PDF, con la advertencia de que no puede reponerse. La genera el navegador sólo como simulación.

## 6. Casos particulares

| Caso | Folio |
|---|---|
| Denuncia en línea | Serie normal |
| Denuncia presentada en persona y capturada por el personal | **La misma serie**, con el canal como dato del expediente. Una sola numeración permite contar el total y detectar duplicados |
| Remitida a una autoridad federal (ANP sin convenio) | Serie normal; el estado del expediente dice «remitida». Desaparece el segmento `REM` |
| Caso de otra autoridad elegido en el paso 1 | **Sin folio**: no se presenta denuncia, sólo se orienta |
| Denuncia acumulada por duplicado (P-21, control 4) | Conserva su folio propio y se liga al expediente principal |
| Envío detenido por el límite de envíos | Sin folio: no se presentó |

## 7. Volumen

La base histórica registra **689 denuncias en 2024, 850 en 2025 y 636 en 2026** al 21 de septiembre (documento 17). Seis dígitos admiten 999 999 por año: margen de sobra aun si el canal en línea multiplica el volumen.

## 8. Qué cambió en el prototipo (DEC-151)

1. `enviar()` dejó de poner el área en el folio y añade el carácter verificador (`digitoLuhn`).
2. La pantalla final y el acuse en PDF muestran la clave de consulta (`claveConsulta`, dato `clave_consulta`).
3. RN-27, el documento 04 y el mapeo de campos se ajustaron; P-13 quedó resuelta.
4. Las pruebas 14, 22 y 25 comprueban el formato, el carácter verificador y la clave.

## 9. Decisión

**Aprobada la opción A** por Liber Saltijeral el 30 de septiembre de 2026 (DEC-151). Se conserva la comparación:

| Opción | Folio de ejemplo | Recomendación |
|---|---|---|
| **A. Sin área, consecutivo único** (este documento) | `SEDEMA/DEN/2026/000123-3` | **Recomendada** |
| B. Con área, consecutivo único | `SEDEMA/DGIVA/DEN/2026/000123` | Conserva el problema del turnado que cambia |
| C. Con área, consecutivo por área | `SEDEMA/DGCORENADR/DEN/2026/000045` | Además, dos denuncias pueden compartir número |

*A quién corresponde.* Dirección General de Inspección y Vigilancia Ambiental, con el Sistema de Información Ambiental, que emite el folio.
