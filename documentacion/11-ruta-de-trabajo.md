# Formulario web de Denuncia Ambiental · Ruta de trabajo y convenciones de código

**Versión:** 1.2 · 18 de septiembre de 2026
**Para qué sirve este documento.** Fija el orden en que se construye el sistema, el criterio para dar por terminada cada fase y las reglas de código que se aplican desde la maqueta. Es el documento que se consulta antes de abrir cualquier módulo nuevo.

---

## 1. Principio rector

**Primero se congela el comportamiento, después se construye la infraestructura.** La maqueta no es un borrador desechable: es la especificación ejecutable del sistema. Cada campo, cada bifurcación y cada regla que queda validada en el prototipo se convierte, sin traducción, en el contrato de datos del servidor.

De ahí se sigue el orden: mientras el formulario ciudadano no esté validado por el área sustantiva, **no se abre ningún módulo complementario**. Un cambio de campo después de programar la base de datos, la bandeja y los tableros cuesta entre diez y veinte veces lo que cuesta hoy.

---

## 2. Fases, en orden, con criterio de salida

Ninguna fase inicia sin que la anterior cumpla su criterio de salida. El criterio es verificable: no es una opinión sobre el avance.

### Fase 1 · Maqueta del formulario ciudadano *(en curso)*

Prototipo navegable, sin servidor, con los datos y las capas embebidos.

**Criterio de salida**

1. Las dieciocho materias y sus fundamentos verificados contra el texto vigente.
2. Las bifurcaciones documentadas y simulables una por una desde el panel de pruebas.
3. El mapeo de campos obligatorios acordado con la Dirección General, en los dos esquemas.
4. Auditorías de estilo, heurística y accesibilidad aplicadas y sin hallazgos abiertos de severidad alta.
5. **Acta de validación de la Dirección General de Inspección y Vigilancia Ambiental**, sobre una versión identificada del prototipo.
6. Pendientes jurídicos P-01 y P-02 resueltos: sin naturaleza del canal ni aviso de privacidad no hay publicación posible.

### Fase 2 · Contrato de datos y servicios

Se congela lo validado y se traduce a especificación técnica, **antes de escribir código de servidor**.

**Productos**

- Diccionario de datos: nombre, tipo, longitud, obligatoriedad por esquema, catálogo de valores y regla de validación de cada campo.
- Catálogos como tablas: materias, tipos de establecimiento, tipos de denunciado, supuestos de derivación, estados del expediente.
- Contrato de la interfaz: qué recibe y qué devuelve cada operación —alta de denuncia, consulta de estatus, carga de evidencia, cruce espacial, geocodificación—.
- Modelo entidad-relación y política de conservación y supresión de datos personales.

**Criterio de salida.** El contrato reproduce exactamente el comportamiento del prototipo validado. Si al escribirlo aparece un caso que el prototipo no resuelve, se corrige el prototipo primero y se vuelve a validar esa parte, nunca al revés.

### Fase 3 · Servicios de territorio

El cruce espacial deja el navegador y las geometrías simplificadas.

- Servicio propio de cruce contra las capas completas, en servidor (P-12).
- Catálogo oficial de colonias y códigos postales (P-16).
- Normalización de las categorías de la capa de origen (P-11).

**Criterio de salida.** El mismo punto arroja el mismo resultado en el prototipo y en el servicio, sobre un conjunto de al menos cincuenta puntos de prueba que cubra las seis situaciones de la jerarquía de turnado, incluidos los bordes y los traslapes.

### Fase 4 · Versión funcional del formulario

Persistencia, folio con consecutivo administrado, carga real de archivos, acuse en PDF, correo de notificación y acceso con Llave CDMX (P-15).

**Criterio de salida.** Prueba controlada con un grupo reducido de personas usuarias reales y con personal de la Dirección General, antes de la publicación abierta.

### Fase 5 · Módulo de administración y seguimiento interno (AD-01)

Bandeja, detalle, estados, asignación, indicadores y exportación.

### Fase 6 · Seguimiento ciudadano (AD-02)

Consulta de estatus, notificación de avance y aportación posterior de información.

**Regla de precedencia.** AD-02 no se construye antes que AD-01: sólo puede mostrar estados que el área sustantiva registre efectivamente.

---

## 3. Convenciones de código

Se aplican desde la maqueta, no a partir del servidor.

### 3.1 Una sola fuente de verdad por concepto

Todo dato que gobierna el comportamiento se declara **una vez**, en una estructura con nombre, y todo lo demás se deriva de ella. El prototipo ya opera así y la regla se conserva:

| Estructura | Gobierna |
|---|---|
| `OBLIG` | Marca de opcionalidad en pantalla, validación y documento de mapeo de campos |
| `MATERIAS` y `GRUPOS_MATERIA` | Catálogo de supuestos, buscador, fundamento y texto del acuse |
| `DERIVA` | Supuestos de otras autoridades y sus pantallas |
| `ANP_COADMIN` | Las ocho Áreas Naturales Protegidas federales atendidas localmente |
| `LIMITES` y `ARCHIVOS` | Longitudes, tamaños y extensiones admitidas, en pantalla y en validación |
| `BIFURCACIONES` y `ESCENARIOS` | Tabla de variantes y escenarios de prueba cargables |

**Prohibido** repetir un valor que ya vive en una de estas estructuras. Si un número o una etiqueta aparece dos veces en el código, una de las dos está por quedar desactualizada.

### 3.2 Declarar en lugar de improvisar

Un valor que se usa más de una vez se declara. Una regla que se aplica en más de un lugar se convierte en función con nombre. Un estilo que se repite se convierte en clase. No se admiten literales sueltos ni estilos en línea repetidos.

### 3.3 Nomenclatura

- Identificadores y comentarios en **español**, sin acentos en los identificadores.
- Funciones: verbo en infinitivo o tercera persona —`consultaCapas`, `esObligatorio`, `bloqueDenunciado`—.
- Catálogos y constantes: mayúsculas —`MATERIAS`, `LIMITES`—.
- Campos del formulario: el nombre del campo es el mismo en `OBLIG`, en el `id` del control, en el `estado` y en el contrato de datos. Un campo, un nombre, en toda la cadena.

### 3.4 Comentarios

El comentario explica **por qué**, no qué. El código ya dice qué hace. Se comenta:

- La regla de negocio o la disposición normativa que sustenta una decisión, con su artículo.
- Toda solución no evidente, con el problema que resuelve.
- Todo supuesto provisional, marcado de modo que pueda localizarse —el prototipo usa `[pendiente]`—.

No se comenta lo obvio ni se deja código comentado: para eso está el control de versiones.

### 3.5 Accesibilidad y estilo

Las decisiones de las auditorías de estilo, heurística y accesibilidad son parte de las convenciones, no una revisión posterior: paleta y tipografía institucionales, contraste mínimo AA, foco visible,controles reales en lugar de divs con `onclick`, y etiqueta asociada a cada control.

---

### 3.6 Organización de las hojas de estilo

Es donde más fácil se encima el trabajo, porque **el navegador no avisa**: si un selector se declara dos veces, no hay error; gana la última declaración y el resultado se ve raro sin que nada indique dónde. Las reglas siguientes existen para que eso no pueda ocurrir.

**Regla 1 · Un selector, una declaración.** Cada selector se declara **una sola vez** en el archivo. Si hace falta una excepción —un control que necesita otro alto mínimo—, se declara inmediatamente después de la regla base y **con un comentario que diga que es una excepción deliberada**. Una excepción anotada es mantenible; una repetición silenciosa, no.

**Regla 2 · Orden fijo de bloques.** La cascada resuelve sola los conflictos si el archivo respeta siempre este orden, de lo general a lo particular:

1. **Variables** de la identidad gráfica en `:root` —color, tipografía, tamaños, radios, espacios—.
2. **Reinicio y base de elementos** —`*`, `body`, `h1`–`h4`, `input`, `select`, `textarea`—.
3. **Estructura** —encabezado, contenedor, pie, renglones de campos, rejillas—.
4. **Componentes** —campo, botón, aviso, tarjeta, tabla, mapa, panel—.
5. **Estados** —`.campo.invalido`, `[aria-pressed="true"]`, `:focus-visible`, `:hover`—.
6. **Utilidades** —`.sub-seccion`, `.nota-gris`, `.oculto`—.
7. **Adaptaciones** —`@media` y `@supports`—, al final del componente al que pertenecen.

Una regla nueva se coloca en su bloque, **no al final del archivo**. Añadir al final es exactamente lo que produce el encimado.

**Regla 3 · Especificidad plana.** Se estiliza por **clase**. No se usan identificadores —`#algo`— para dar estilo, ni cadenas de descendencia de más de dos niveles. A igual especificidad, el orden manda y el orden está fijado por la Regla 2; en cuanto hay especificidades desiguales, la única forma de vencer una regla es escribir otra más específica, y ahí empieza la escalada que termina en `!important`.

**Regla 4 · Nada de `!important`.** La única excepción admitida es el bloque de `prefers-reduced-motion`, donde se anulan animaciones que el usuario pidió no ver. Cualquier otro `!important` es señal de que una regla anterior está mal colocada: se corrige la colocación, no se fuerza el resultado.

**Regla 5 · Una propiedad, un dueño.** Color, tipografía, tamaño, radio y espaciado provienen **siempre** de las variables de `:root`. No se escribe un valor de color fuera de ese bloque. Si un color hace falta y no existe como variable, se declara la variable.

**Regla 6 · Componente y modificador, sobre el mismo elemento.** El componente lleva su clase y la variante se añade como modificador en el mismo elemento —`.fila-op` y `.fila-op.otra`, `.btn` y `.btn-primario`, `.campo` y `.campo.invalido`—. No se crea una clase global nueva para una variante: se modifica la que ya existe.

**Regla 7 · El estado se lee del atributo, no de una clase paralela.** El resaltado de una opción elegida cuelga de `[aria-pressed="true"]`, no de una clase `.activa` que haya que sincronizar aparte. Así el estado visible y el estado que anuncia el lector de pantalla **no pueden divergir**, que es el defecto clásico de mantener ambos a mano.

**Regla 8 · `@media` y `@supports` sólo redeclaran lo que cambia.** Dentro de una adaptación se escribe únicamente la propiedad que varía en ese contexto. Repetir ahí la declaración completa del componente es duplicarlo, y a partir de ese momento hay dos lugares que mantener.

**Regla 9 · Sin estilos en línea repetidos.** Un estilo en línea se admite sólo para una geometría irrepetible —el ancho de una columna concreta de una tabla—. En cuanto aparece dos veces, se convierte en clase con nombre.

**Verificación, en cada cierre de bloque de cambios**

1. Ningún selector declarado dos veces fuera de `@media` y `@supports`; las excepciones deliberadas, comentadas.
2. Ninguna propiedad declarada dos veces para el mismo selector.
3. Ningún `!important` fuera del bloque de movimiento reducido.
4. Ninguna clase declarada y no usada, considerando también las que se construyen por concatenación en el código.
5. Ningún valor de color fuera de `:root`.
6. Recuento de estilos en línea: los repetidos, convertidos en clase.

---

## 4. Regla contra el código zombi

**Código zombi** es todo aquello que permanece en el archivo sin ejecutarse: funciones que nadie llama, variables que se escriben y nunca se leen, clases de estilo sin uso, declaraciones duplicadas donde la segunda anula a la primera, y restos de versiones anteriores.

Importa por tres razones: induce a error a quien lea el código después, oculta defectos reales —una función duplicada puede estar ejecutando la versión equivocada—, y crece con cada iteración hasta volver el archivo inmanejable.

**Procedimiento, al cerrar cada bloque de cambios:**

1. Verificación de sintaxis del archivo completo.
2. Listado de funciones declaradas contra sus llamadas: cero funciones sin uso.
3. Listado de claves del estado escritas contra leídas: cero claves escritas y nunca leídas.
4. Listado de clases de estilo declaradas contra usadas, incluidas las que se construyen por concatenación.
5. Detección de declaraciones duplicadas.
6. Recuento de estilos en línea: los repetidos se convierten en clase.
7. Recorrido automatizado de los seis pasos y de los doce escenarios, sin errores en consola.

Lo que se elimina se anota en la bitácora de este documento, con el motivo. **Nada se borra en silencio.**

---

## 5. Cuándo dejar el archivo único

El prototipo vive en un solo archivo por una razón: se abre con doble clic, se envía por correo y se revisa sin instalar nada. Esa ventaja se pierde en cuanto haya servidor.

**Punto de corte: al iniciar la Fase 4.** La separación queda así:

```
/publico
  index.html              estructura y accesibilidad
  /estilos
    identidad.css         variables de la identidad gráfica
    componentes.css       campos, botones, avisos, tablas
    pantallas.css         cada paso
  /datos
    materias.json         catálogos, servidos por la interfaz
    obligatoriedad.json
  /app
    estado.js             estado del formulario y persistencia
    campos.js             constructores de campo
    pasos.js              armado de cada pantalla
    validacion.js         reglas de obligatoriedad y formato
    mapa.js               mapa y cruce espacial
    envio.js              envío, folio y acuse
/servidor
  ...
```

Los catálogos dejan de ser literales en el código y pasan a servirse desde la interfaz: es lo que permite que el área sustantiva actualice una materia o un giro sin tocar el código.

---

## 6. Qué no se hace todavía

- No se abre el módulo de administración antes del acta de validación.
- No se programa persistencia mientras el diccionario de datos no esté cerrado.
- No se sustituye el cruce en navegador antes de tener el servicio de territorio probado contra el prototipo.
- No se incorpora ninguna cita normativa sin verificarla contra el texto vigente; donde falte, el hueco queda visible.

---

---

## 7. Cómo se piden y se cierran los cambios

Este apartado no es sobre el código: es sobre el **procedimiento de trabajo**. La persona que dirige el proyecto no programa, y no tiene por qué hacerlo: lo que necesita es un método que impida que los cambios se encimen.

### 7.1 Por qué se encima el trabajo

Tres causas, todas de procedimiento y ninguna de conocimiento técnico:

1. **Se pide el resultado, no el lugar.** «Quita eso» o «muévelo» sobre un archivo de cientos de páginas: si no se busca primero dónde ya está escrita esa regla, se escribe una nueva **encima** de la anterior. Las dos quedan; gana la última; nada avisa.
2. **Se pide a goteo.** Un ajuste suelto cada pocos minutos no deja momento para verificar. Los restos se acumulan entre petición y petición.
3. **No hay cierre.** Sin un punto donde se revisa y se anota lo hecho, nunca se sabe qué quedó vivo y qué quedó muerto.

### 7.2 Las tres defensas

**Primera · La regla se aplica sola.** Las convenciones de este documento están además guardadas como regla operativa, de modo que se apliquen en toda sesión de trabajo sobre el prototipo sin que haya que recordarlas ni repetirlas. Antes de añadir cualquier cosa se busca si ya existe; si existe, **se modifica lo que existe**; si se sustituye, lo viejo se elimina en el mismo movimiento.

**Segunda · Historial.** Antes de abrir un bloque de cambios se conserva la versión anterior en `prototipo/historial/` con la fecha y un nombre corto de lo que se va a hacer. Permite comparar y volver atrás sin depender de la memoria. El artefacto de prueba conserva además sus versiones numeradas.

**Tercera · Trabajo por bloques cerrados.** Un bloque es un conjunto de cambios con un mismo propósito —«ajustes de la pantalla de ubicación», «correcciones de la auditoría de accesibilidad»—. Se abre, se ejecuta completo, se verifica y se cierra. **No se abre un bloque nuevo con otro abierto.**

### 7.3 Cómo pedir un cambio

Cuatro datos. Con ellos, el cambio se hace en el lugar correcto y no se duplica:

| Dato | Ejemplo |
|---|---|
| **Dónde** | «En el paso 2, en el bloque de identificación del sitio» |
| **Qué debe lograr** | «Que el nombre comercial no se pida dos veces» |
| **Corrección o añadido** | «Es corrección: ya existe y está mal» / «Es añadido: no existe» |
| **Por qué**, si lo hay | «Porque el área lo pidió así» / «Porque la ley lo exige» |

El dato que más ahorra es el tercero. **«Es corrección» obliga a buscar lo que ya existe y modificarlo; «es añadido» autoriza a crear.** Decirlo evita la mayor parte de los solapamientos.

Lo que conviene evitar: pedir «y de paso…» con un bloque abierto. Se anota y entra en el bloque siguiente.

### 7.4 Cómo cerrar un bloque

Basta con decir **«cierra el bloque»**. Eso obliga a entregar, siempre lo mismo:

1. Verificación de sintaxis del archivo completo.
2. Auditoría de código muerto —las siete comprobaciones del apartado 4—.
3. Auditoría de hojas de estilo —las seis del apartado 3.6—.
4. Recorrido automatizado de los seis pasos y los doce escenarios, sin error en consola.
5. Prueba específica de lo que se acaba de cambiar.
6. Anotación en la bitácora de este documento: qué se eliminó y por qué.
7. Versión publicada del artefacto, con etiqueta de lo que contiene.

Si algo de eso no se entrega, el bloque no está cerrado.

### 7.5 Qué exigir siempre, sin pedirlo

- Que ningún número de artículo, fracción o numeral se escriba sin estar verificado contra el texto vigente; donde falte, el hueco queda visible.
- Que toda decisión quede en el documento de decisiones, con su motivo.
- Que nada se borre en silencio: lo eliminado se anota.
- Que se advierta cuando una petición contradiga una decisión anterior, en vez de ejecutarla sin más.

## 8. Bitácora de limpieza

### 18 de septiembre de 2026 · primera auditoría de código muerto

| Elemento | Naturaleza | Motivo de la eliminación |
|---|---|---|
| `function marca(k)` | Declaración duplicada | Declarada dos veces con cuerpo idéntico; la segunda anulaba a la primera. Se conservó una |
| `function aFC(capa,filtro)` | Función sin uso | Auxiliar de filtrado de capas de una versión anterior del cruce espacial; ninguna llamada |
| `function cargarEjemplo()` | Función sin uso | Cargador de datos de demostración, sustituido por `ESCENARIOS` y `cargaEscenario(id)` |
| `estado.decreto`, `estado.superficie` | Claves escritas y nunca leídas | Alimentaban la ficha bajo el mapa, suprimida por DEC-15. La fecha de decreto y la superficie permanecen en el catálogo `ANP_COADMIN` como dato documental |
| `estado.capa_grupo` | Clave escrita y nunca leída | El grupo de la capa se consume directamente del resultado del cruce |
| `.fallback`, `.req` | Clases de estilo sin uso | Restos de versiones anteriores de la barra de gobierno y del marcado de campos obligatorios |
| `.tipo-titulo` | Selector sin uso | Retirado de la lista de selectores de encabezado |
| Seis estilos en línea idénticos | Repetición | Convertidos en la clase `.sub-seccion`; cinco más, en `.nota-gris`. De 74 estilos en línea se pasó a 61 |

**Verificación posterior:** sintaxis correcta, doce escenarios cargados sin error, recorrido de los seis pasos sin error en consola, clases nuevas aplicadas en las pantallas correspondientes.

**Estado al cierre:** cero funciones sin uso, cero claves de estado sin lectura, cero clases de estilo huérfanas, cero declaraciones duplicadas.

### 18 de septiembre de 2026 · auditoría de hojas de estilo

| Elemento | Naturaleza | Efecto real |
|---|---|---|
| `.fila`, `.fila-3`, `.fila-2-1` | Selector declarado **cuatro veces**, con `display` y `grid-template-rows` en conflicto | Dentro de `@supports` se fijaba `grid-template-rows:subgrid` en el **renglón**, que no tiene rejilla padre de la cual heredar, y dos líneas después otra regla del mismo selector lo corregía a `auto auto auto auto`. Funcionaba por accidente: la segunda regla anulaba a la primera. Consolidado en una declaración por selector, con el comentario que explica por qué el renglón no lleva `subgrid` |
| `input[type=date]{min-height:46px}` | Regla redundante | Repetía el valor que ya fija la regla base de todos los controles |
| `textarea{min-height:130px}` | Excepción legítima | Se conserva y queda **anotada como excepción deliberada** a la regla base |
| Estilos en línea | Repetición | Ver la auditoría anterior: seis y cinco ocurrencias convertidas en `.sub-seccion` y `.nota-gris` |

**Verificación posterior:** cero selectores duplicados fuera de `@media` y `@supports` salvo la excepción anotada de `textarea`; `!important` únicamente en el bloque de movimiento reducido; alineación por subgrid comprobada por medición —los controles de un mismo renglón comparten el mismo borde superior al píxel—; seis pasos y doce escenarios sin error en consola.

