# Revisión del formulario con la DGIVA · hoja de observaciones

**Qué es.** Una liga del formulario publicado abre el **modo revisión**: un botón guinda «✎ Observar» abajo a la izquierda. **Es una sola liga para todas las personas que revisan**: la primera vez, cada quien escribe su nombre (y, si quiere, su área) y el navegador lo recuerda. Después señala un texto o una parte de la pantalla, elige el tipo (corregir redacción, quitar, agregar, error o falla, duda u otro), escribe su observación y, si quiere, cómo debería decir. Cada observación llega a una **hoja de Google** de la Oficina de la Secretaría, con el nombre de quien la hizo, la pantalla, la sección y el texto exacto que se señaló. En la hoja se contesta; en el panel, «Observaciones» muestra las de todo el equipo, con su estado y su respuesta, y la casilla «Sólo las mías» filtra las propias.

Sin la liga de revisión, el formulario se ve igual que siempre. Decisiones: DEC-153 y DEC-155.

---

## Instalación

> **Si ya habías instalado la versión anterior** (la de una clave por persona): sustituye todo el código por el nuevo `Codigo.gs`, guarda, ejecuta `prepararHoja` y publica una **versión nueva** de la misma implementación (paso 5). La URL `/exec` no cambia. Puedes borrar la hoja «Revisores»: ya no se usa.

1. **Crea la hoja.** En Google Drive: Nuevo → Hojas de cálculo de Google. Nómbrala «Revisión · Formulario de Denuncia Ambiental».
2. **Pega el código.** En la hoja: Extensiones → Apps Script. Borra lo que aparece, pega todo `Codigo.gs` y guarda (ícono de disco).
3. **Prepara la hoja.** Arriba, elige la función `prepararHoja` y pulsa Ejecutar. La primera vez Google pide autorización: Revisar permisos → tu cuenta → Configuración avanzada → Ir a «…» (no seguro) → Permitir. Es tu propio código; el aviso es normal. Se crea la hoja **Observaciones** y se genera la liga de revisión.
4. **Publícalo como aplicación web.** Implementar → Nueva implementación → ícono de engrane → Aplicación web. Ejecutar como: **Yo**. Quién tiene acceso: **Cualquier persona**. Implementar y copia la URL que termina en `/exec`.
5. **Si cambias el código después:** Implementar → Administrar implementaciones → lápiz → Versión: **Nueva versión** → Implementar. Así la URL `/exec` no cambia.
6. **La URL `/exec` va en el formulario** (`REVISION.endpoint`); ya está puesta.
7. **Envía la liga.** Recarga la hoja: aparece el menú **Revisión → Ver liga de revisión**. Es algo como `https://sedemaoficina.github.io/denuncia-ambiental/?revision=k7pmq4xz2abc`. Mándala a todas las personas de la DGIVA que revisan.

> La palabra al final de la liga la genera la hoja y **no está en el código**, que es público: sin ella nadie puede escribir en la hoja. Si la liga circula donde no debe, **Revisión → Generar liga de revisión** crea una nueva y la anterior deja de funcionar.

## Cómo se atiende

| Columna | Quién la llena | Uso |
|---|---|---|
| ID … Dispositivo | El formulario | Quién, dónde y qué se observó; no se editan |
| **Estado** | Oficina de la Secretaría | Pendiente · En revisión · Para discusión · Atendida · Descartada |
| **Respuesta** | Oficina de la Secretaría | Lo que ve el equipo revisor en «Observaciones» |
| **Atendida en** | Oficina de la Secretaría | La decisión del documento 05 que la resolvió (p. ej. DEC-160) |

Para que Claude las retome: pídele «lee las observaciones de la hoja de revisión». Con el conector de Google Drive la lee directamente; si no, descárgala en CSV y adjúntala.

## Qué guarda y qué no

- Guarda: el nombre y el área que escribió quien revisa, la observación, la pantalla y el texto señalado, la versión del formulario, la materia elegida y el tamaño de pantalla con el navegador.
- No guarda lo que se haya capturado en el formulario: ni hechos, ni direcciones, ni datos personales. El formulario de prueba no envía denuncias.
- El nombre no se verifica: es la palabra de quien revisa. La liga es lo que protege la hoja.
- Límite: 1000 observaciones al día. Un envío repetido (por reintento) no se duplica.
