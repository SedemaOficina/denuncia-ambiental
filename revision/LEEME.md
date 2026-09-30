# Revisión del formulario con la DGIVA · hoja de observaciones

**Qué es.** Una liga del formulario publicado con `?revision=CLAVE` abre el **modo revisión**: un botón guinda «✎ Observar» abajo a la izquierda. Quien revisa señala un texto o una parte de la pantalla, elige el tipo (corregir redacción, quitar, agregar, error o falla, duda u otro), escribe su observación y, si quiere, cómo debería decir. Cada observación llega a una **hoja de Google** de la Oficina de la Secretaría, con la pantalla, la sección y el texto exacto que se señaló. En la hoja se contesta; quien revisa ve el estado y la respuesta en «Mis observaciones».

Sin la clave en la liga, el formulario se ve igual que siempre. Decisión: DEC-153.

---

## Instalación (una sola vez, unos 10 minutos)

1. **Crea la hoja.** En Google Drive: Nuevo → Hojas de cálculo de Google. Nómbrala «Revisión · Formulario de Denuncia Ambiental».
2. **Pega el código.** En la hoja: Extensiones → Apps Script. Borra lo que aparece, pega todo `Codigo.gs` y guarda (ícono de disco).
3. **Prepara la hoja.** Arriba, elige la función `prepararHoja` y pulsa Ejecutar. La primera vez Google pide autorización: Revisar permisos → tu cuenta → Configuración avanzada → Ir a «…» (no seguro) → Permitir. Es tu propio código; el aviso es normal. Se crean las hojas **Observaciones** y **Revisores**.
4. **Publícalo como aplicación web.** Implementar → Nueva implementación → ícono de engrane → Aplicación web.
   - Descripción: «Revisión DGIVA».
   - Ejecutar como: **Yo**.
   - Quién tiene acceso: **Cualquier persona**.
   - Implementar y copia la URL que termina en `/exec`.
5. **Pásale la URL a Claude.** Se pone en el formulario (`REVISION.endpoint`), se publica en Pages y queda conectado. Hasta entonces, el modo revisión guarda en el navegador y permite descargar en CSV.
6. **Da de alta a cada persona.** Vuelve a la hoja y recárgala: aparece el menú **Revisión → Agregar revisor**. Escribe nombre y área; la hoja genera su clave (`K7PM-4XQ2`) y su liga. Envía a cada quien **su** liga: la clave dice quién hizo cada observación.

> «Cualquier persona» significa que la URL `/exec` responde sin iniciar sesión, pero **sólo guarda y muestra observaciones de claves activas** en la hoja Revisores. Para retirar a alguien, cambia «Activa» a «No».

## Cómo se atiende

| Columna | Quién la llena | Uso |
|---|---|---|
| ID … Dispositivo | El formulario | Dónde y qué se observó; no se editan |
| **Estado** | Oficina de la Secretaría | Pendiente · En revisión · Para discusión · Atendida · Descartada |
| **Respuesta** | Oficina de la Secretaría | Lo que ve quien revisó, en «Mis observaciones» |
| **Atendida en** | Oficina de la Secretaría | La decisión del documento 05 que la resolvió (p. ej. DEC-160) |

Para que Claude las retome: pídele «lee las observaciones de la hoja de revisión». Con el conector de Google Drive la lee directamente; si no, descárgala en CSV y adjúntala.

## Cambios posteriores al código

Si se modifica `Codigo.gs`: Implementar → Administrar implementaciones → lápiz → Versión: **Nueva versión** → Implementar. Así la URL `/exec` no cambia y las ligas siguen sirviendo.

## Qué guarda y qué no

- Guarda: nombre y área de quien revisa (los que tú escribiste en Revisores), la observación, la pantalla y el texto señalado, la versión del formulario, la materia elegida y el tamaño de pantalla con el navegador.
- No guarda lo que se haya capturado en el formulario: ni hechos, ni direcciones, ni datos personales. El formulario de prueba no envía denuncias.
- Límite: 300 observaciones por clave al día. Un envío repetido (por reintento) no se duplica.
