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

> **Antes de abrir esta fase: cambiar el entorno de trabajo a Claude Code.**
> Hasta aquí el trabajo ha sido un archivo y unos documentos, y la app de escritorio basta.
> De la fase 2 en adelante hay muchos archivos que correr y probar, migraciones, y trabajo
> continuo con el repositorio: eso pertenece a una herramienta que vive en la máquina, con
> la red y las credenciales de git de quien dirige el proyecto.
>
> **Qué se gana:** el `push` deja de depender de otra aplicación; se puede verificar
> cualquier servicio externo contra la red real; se prueba el archivo en su lugar, sin
> subirlo y bajarlo; y desaparecen los permisos de borrado que git necesita para operar.
>
> **Qué hay que prever:** se instala con una sola línea en PowerShell y no requiere
> Node.js, pero es una ventana de comandos. Las skills guardadas en la cuenta de claude.ai
> siguen funcionando ahí; la memoria del entorno actual no viaja, y por eso todo lo que
> importa vive en estos documentos y en el repositorio.
>
> **Qué se queda aquí:** el artefacto de validación con su historial de versiones, los
> documentos visibles desde el navegador y el teléfono, y la tarea programada de revisión
> de la Gaceta Oficial. No es una mudanza: es trabajar el código allá y la validación aquí,
> sobre el mismo repositorio.

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


### 18 de septiembre de 2026 · bloque «titularidad, repositorio y minimización»

| Cambio | Naturaleza | Motivo |
|---|---|---|
| `LEEME.md` → `README.md` | Renombrado | Es el archivo que muestra la plataforma al abrir el repositorio; mantener los dos habría duplicado el mismo contenido |
| `.gitignore` | Añadido | Excluye la normativa de referencia (26 MB públicos y re-descargables), `prototipo/historial/` —la historia la lleva git— y `_to_delete/`. Cada exclusión razonada en el propio archivo |
| `OBLIG` | Ampliado | Cada campo declara `uso`, `dp` y `fin`. No se eliminó nada |
| `abreMapeo()` | Ampliado | Dos columnas nuevas en el comparativo: dato personal y uso declarado |
| `table.comp td.uso-campo` | Clase nueva | Columna de texto largo y secundario; declarada en el bloque de componentes, no al final del archivo |

**Verificación de cierre.** Sintaxis correcta. Cero funciones duplicadas, cero funciones sin uso, cero claves de estado sin lectura, cero clases de estilo huérfanas, cero `!important` indebidos. Un selector declarado dos veces: `textarea`, que es la excepción deliberada al alto mínimo, anotada como tal. Seis pasos y doce escenarios recorridos sin error en consola. Prueba específica: el comparativo muestra 47 campos con su uso, 20 marcados como dato personal, y totales 19 / 25 / 20, coincidentes con el documento 09. Auditoría de repositorio corrida antes del primer registro: sin secretos.

### 18 de septiembre de 2026 · bloque «dirección primero en el paso 2»

| Cambio | Naturaleza | Motivo |
|---|---|---|
| Orden del paso 2 | Reordenado | La dirección va primero —calle, número, alcaldía, colonia, código postal— y el mapa debajo. Es como la gente piensa el lugar. **Invierte la dependencia declarada antes**, pero no la regla: el cruce que determina la competencia se sigue resolviendo sobre la coordenada (DEC-04) |
| `buscaDireccion()` → `ubicaPorDireccion()` | Sustituida | El buscador de texto libre desapareció: los campos de dirección **son** la búsqueda. La consulta se arma con calle, número, colonia y alcaldía |
| `.buscador` | Clase retirada | Quedó sin uso al retirar el buscador libre |
| `geocodificaInverso()` | Acotada | Sólo rellena campos vacíos: mover el punto ya no sobrescribe la dirección que la persona escribió |
| `alcaldia_difiere` | Clave nueva | El punto manda sobre la alcaldía —de ella depende el turnado— y cuando difiere de la elegida **se avisa en vez de cambiarla en silencio** |
| `resp_domicilio` en el bloque de empresa | Retirado | La razón social más el lugar de los hechos bastan para el emplazamiento, y es un dato que quien denuncia rara vez conoce. Se conserva en el bloque de persona física, donde puede ser el único modo de ubicarla |
| `sabe_permisos`, `reporto_antes` | Preguntas filtro nuevas | Dos campos de texto largos que la mayoría dejaba vacíos quedaron tras una pregunta de sí o no. La respuesta misma informa: saber que alguien ya reportó ante otra autoridad distingue el caso |
| Construcción del artefacto | Ajustada | El artefacto no tiene servicio de búsqueda: se retira el botón de ubicar y se corrige el texto del estado vacío, que nombraba un botón inexistente |

**Verificación de cierre.** Sintaxis correcta. Cero funciones duplicadas o sin uso, cero claves de estado sin lectura, cero clases de estilo huérfanas, cero `!important` indebidos; el único selector declarado dos veces es `textarea`, la excepción anotada. Orden del paso 2 comprobado por lectura del DOM: calle → número → alcaldía → colonia → código postal. Las dos preguntas filtro muestran y ocultan su campo según la respuesta. El bloque de empresa ya no pide domicilio; el de persona sí. El aviso de alcaldía discrepante persiste y desaparece cuando el punto llega a la alcaldía indicada. Seis pasos y doce escenarios sin error en consola.

**Nota sobre el método.** Durante la verificación se dio por defectuoso el aviso de alcaldía con base en una prueba cuyo patrón de búsqueda estaba mal escrito y nunca podía coincidir. El código estaba bien. Es el caso de «el método de verificación también se verifica»: la corrección aplicada —comparar contra la alcaldía que eligió la persona y no contra la última calculada— se conserva porque es más robusta, pero **no corrigó un defecto que estuviera ocurriendo**.

### 19 de septiembre de 2026 · bloque «un solo sentido y barra navegable»

| Cambio | Naturaleza | Motivo |
|---|---|---|
| Variante A de identificación | Retirada | Criterio ya descartado que reabría la discusión en cada sesión (DEC-40) |
| `geocodificaInverso()` | Eliminada | El punto deja de escribir en la dirección. Una llamada menos a un servicio externo (DEC-41) |
| `alcaldia_difiere` → `alcaldia_punto` | Clave sustituida | Ya no marca una discrepancia resuelta: guarda la alcaldía que arroja la capa, sin tocar la capturada |
| `usaAlcaldiaDelPunto()` | Función nueva | Única vía por la que el mapa escribe en la dirección, y sólo a petición expresa |
| Etapas de la barra de progreso | `div` → `button` | Navegación entre pasos, con `aria-current` en el actual |
| `vaAlPaso(n)` | Función nueva | Reutiliza `valida()`: no se crea una segunda puerta con criterios propios |
| 79 secuencias `\uXXXX` | Convertidas a caracteres reales | **Defecto propio.** En las cadenas funcionaban, pero en los comentarios quedaban como basura ilegible. Se verificó que el texto renderizado de los seis pasos es idéntico antes y después |

**Verificación de cierre.** Sintaxis correcta. Cero funciones duplicadas o sin uso, cero claves de estado sin lectura, cero clases huérfanas, cero escapes literales; el único selector declarado dos veces es `textarea`, la excepción anotada. Comprobado que al colocar el punto en otra alcaldía **ninguno de los cinco campos de dirección cambia**, que la ficha muestra la alcaldía del punto y que la corrección sólo ocurre al pulsar el botón. En la barra: retroceder con un clic funciona; avanzar en modo de prueba funciona; con obligatoriedad activada y campos vacíos **no avanza y muestra el resumen de errores**; y con el punto fuera de la Ciudad **no avanza ni siquiera en modo de prueba**. Seis pasos y doce escenarios sin error en consola.

### 19 de septiembre de 2026 · bloque «barra fija»

| Cambio | Naturaleza | Motivo |
|---|---|---|
| `.barra-fija` | Contenedor nuevo | Agrupa la barra de avance y el recordatorio de materia, y los fija arriba (DEC-43) |
| `chipMateria()` | Reubicado | Deja de pintarse dentro del contenido, que se reconstruye en cada paso, y se pinta una sola vez en la barra |
| `html{scroll-padding-top}` | Declaración nueva | Con la barra fija, todo desplazamiento automático debe detenerse por debajo de ella |

**Corrección durante el propio cierre.** La primera versión repartía `scroll-margin-top` entre `.campo`, `.tarjeta h2`, `.sub-seccion` y `.resumen-errores`, **cuatro selectores que ya estaban declarados en otro sitio**. La auditoría de hojas de estilo lo detectó: es exactamente la regla «un selector, una declaración». Se sustituyó por una sola declaración de `scroll-padding-top` en el contenedor de desplazamiento, que además cubre cualquier elemento y no sólo esos cuatro.

**Verificación de cierre.** Sintaxis correcta. Cero funciones duplicadas o sin uso, cero claves de estado sin lectura, cero clases huérfanas; el único selector declarado dos veces vuelve a ser `textarea`, la excepción anotada. Comprobado por medición que el recordatorio sigue visible tras desplazar 1 200 y 3 000 px, en pantalla de 1 100 y de 390 px; que no queda duplicado dentro del contenido; que no aparece en el paso 1 ni en el acuse; y que la barra ocupa 110 px en un teléfono de 760 px de alto. Seis pasos y doce escenarios sin error en consola.

### 19 de septiembre de 2026 · bloque «mejoras desde la ciudadanía» (segunda parte: estructura)

Segunda mitad de lo aprobado en el documento 13. La primera —contenido y redacción: anonimato y qué pasa después en la pantalla de inicio, ejemplo por supuesto, etiquetas en lenguaje común— cerró en el commit anterior.

| Cambio | Naturaleza | Motivo |
|---|---|---|
| `.bloque-opcional` / `.enc-opcional` / `.cuerpo-opcional` | Componente nuevo | Plegable de campos accesorios. Se usa en el paso 2 sobre referencias adicionales e identificación del establecimiento (DEC-44, M-03) |
| `mas_lugar` | Clave de estado nueva | Sólo abre y cierra el bloque. **No entra en `OBLIG`**: no es un dato de la denuncia y no aparece en el acuse ni en el documento generado |
| `.cuerpo-opcional .opc{display:none}` | Regla nueva | Dentro del bloque no se repite «opcional»: lo dice el encabezado una vez (DEC-46, M-07) |
| `estoyEnElLugar()` | Función nueva | La ubicación del dispositivo, con el encuadre de DEC-45. Propone el punto; no toca la dirección (M-04) |
| Red de seguridad en `valida()` | Guarda nueva | Si un campo obligatorio quedara dentro del bloque plegado, el resumen de errores enlazaría a algo que no está en la pantalla. La lista `ENVUELTOS_LUGAR` despliega el bloque antes de mostrar el error |

**Tres defectos propios corregidos durante el cierre, los tres en la cadena de construcción del artefacto.** Ninguno era visible en el archivo local; los tres habrían llegado a la versión en línea que se usa para validar con la Dirección General.

1. **`construir.py` retiraba el bloque de acciones por una expresión que ya no coincidía.** El marcado había ganado `flex-wrap:wrap` y la sustitución fallaba **en silencio**, dejando en el artefacto un botón que allí no funciona. Se acotó la expresión al botón que de verdad sobra —el que necesita servicio de geocodificación— y, sobre todo, **se hizo que el guion se detenga con error cuando una sustitución no encuentra su objetivo**. Una transformación que no encuentra qué transformar no puede seguir adelante como si nada.
2. **La nota del artefacto sustituía al contenedor `resBusqueda` en lugar de precederlo.** Como `estoyEnElLugar()` escribe ahí sus mensajes y empieza con `if(!cont) return;`, en el artefacto la opción **no habría hecho absolutamente nada, sin aviso alguno**. La nota ahora va antes y el contenedor se conserva.
3. **`quitaPunto()` del módulo de mapa vectorial se había desfasado del prototipo.** Al cargarse después, lo sobrescribe: en el artefacto no limpiaba `alcaldia_punto` —de modo que un aviso de alcaldía podía sobrevivir a quitar el punto— y sí limpiaba cinco claves que ya no existen. Se igualaron las listas. También se retiraron de ese módulo `geocodificaInverso()` y `buscaDireccion()`, ya sin llamador, y se añadió el encuadre del punto que el mapa vectorial no tenía.

**Verificación de cierre.** Treinta y seis comprobaciones automatizadas sobre el artefacto construido, todas en verde. Sintaxis correcta en las dos piezas. Cero funciones sin uso; el único selector declarado dos veces sigue siendo `textarea`, la excepción anotada. Comprobado: el bloque nace plegado y sus campos **no están en el árbol del documento**, de modo que no los recorre el teclado ni el lector de pantalla; abre y cierra; lo capturado dentro sobrevive al plegado; ningún campo plegado es hoy obligatorio, y forzando que uno lo fuera, `valida()` frena y despliega el bloque; sin permiso de ubicación se muestra un mensaje y no un vacío; con permiso, el punto queda donde el navegador lo indica, el mapa se acerca, **la alcaldía capturada no cambia** y la del punto sí se registra. Siete pantallas sin error propio en consola.

**Medición, contra la línea base del documento 13** (mismo método: alto del contenedor del formulario, teléfono de 390 × 760 px).

| Paso | Antes | Ahora | |
|---|---|---|---|
| 1 · Qué denuncias | 2 251 px | 2 251 px | sin cambio |
| 2 · Dónde ocurre | 3 609 px | **2 163 px** | −1 446 px · de 4.7 a 2.8 pantallas · de 513 a 282 palabras |
| 3 · Qué ocurre | 2 969 px | **2 013 px** | −956 px, por las preguntas filtro de permisos y gestiones |
| 4 · Pruebas | 838 px | 880 px | +42 px, por las etiquetas en lenguaje común |
| 5 · Tus datos | 1 993 px | 1 884 px | −109 px |
| 6 · Revisión | 2 273 px | 2 321 px | +48 px |
| **Total** | **13 933 px · 18.3 pantallas** | **11 512 px · 15.1 pantallas** | **−17 %** |

La palabra «opcional» pasa de veintiocho a dieciocho apariciones. La pantalla más larga es ahora **la revisión final, con 3.1** — que es justo lo que propone plegar M-10, pendiente junto con M-06.

**Corrección de la propia medición.** La primera cifra que se anotó en este cierre —23.8 pantallas— medía el alto de todo el documento, con encabezado de gobierno, pie y ventanas modales incluidos, mientras que la línea base del documento 13 mide sólo el contenedor del formulario. Comparadas así, las dos versiones decían que el formulario había crecido cuando en realidad se había acortado un 17 %. **Una medición sólo sirve si repite el método de aquella contra la que se compara**; se rehízo con el método original y son las cifras de arriba las que valen.

**Nota sobre el método.** Una de las treinta y seis comprobaciones falló en su primera ejecución por culpa de la prueba, no del código: forzaba la obligatoriedad de un campo marcando sólo la bandera del esquema vigente, cuando el panel estaba en el esquema de la propuesta de la Dirección General. Se corrigió la prueba para marcar ambas y no depender del esquema seleccionado. Es la segunda vez que el método de verificación resulta ser lo defectuoso; conviene anotarlo cada vez.

### 19 de septiembre de 2026 · reconstrucción del repositorio remoto

Al intentar sincronizar, GitHub Desktop devolvió **«Unable to merge unrelated histories»**. No era un fallo de la herramienta: al retirar de la historia el documento de trabajo de la Dirección General, `filter-branch` no editó los commits sino que **creó commits nuevos con raíz nueva**, de modo que la historia local (`b28e8b5`) y la publicada (`fef6652`) no compartían ningún ancestro.

**Antes de decidir nada se comprobó qué había de cada lado.** Los cuatro commits del remoto eran los cuatro primeros del local, con los mismos mensajes, en su versión previa a la limpieza; la única diferencia de contenido era el documento. El remoto no tenía nada propio. Se auditó además toda la historia local: 32 archivos, el documento en cero commits, y **ni la llave de CARTO ni los PDF de normativa ni `configuracion-local.js` en ninguno**.

Se descartó resolverlo con `--allow-unrelated-histories`, que habría injertado de vuelta la historia con el documento, deshaciendo la limpieza. Entre las dos vías reales —forzar el envío sobre el repositorio existente, o borrarlo y crearlo de nuevo— se eligió **la segunda**: el envío forzado deja los objetos sueltos accesibles por su identificador durante un tiempo indeterminado, mientras que borrar el repositorio los elimina con él.

**Verificación posterior al envío.** Punta remota y local coinciden en `ee48daf`; dieciséis commits arriba; ninguna diferencia de contenido; el documento aparece cero veces en la historia remota; la raíz remota es `b28e8b5`, la limpia.

**Lo que esto no arregla, y conviene no olvidar.** El documento **estuvo publicado**. Quien lo haya clonado o descargado en esos días lo conserva. La lección operativa es anterior a todo esto: **el `.gitignore` se escribe antes del primer commit, no después del primer push.** Hoy ya excluye ese documento, los PDF de normativa, el historial del prototipo y el archivo de configuración con la llave de CARTO.

**Nota de herramienta.** La primera escritura de estos dos archivos se hizo desde el entorno de trabajo y la herramienta reportó «éxito» habiendo dejado en disco una versión anterior. Se detectó al comprobar el contenido en disco, no al leer la respuesta de la herramienta. **Vale para cualquier escritura: lo que confirma que un archivo quedó bien es leerlo, no que la herramienta diga que sí.**

### 19 de septiembre de 2026 · bloque «el lugar sin domicilio y las tres rutas de identificación»

Dos asuntos que parecían de la misma clase y no lo eran: el primero es un **defecto**, el segundo una decisión de diseño.

#### El defecto

El formulario exigía calle, colonia y código postal. En un bosque, un área natural protegida, una barranca, un camino o un canal esos datos no existen. Comprobado antes de tocar nada, poniendo un punto dentro del Bosque de Tlalpan: **el sistema identificaba correctamente el área natural protegida, la alcaldía y que la denuncia correspondía a la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural —y acto seguido no dejaba continuar**, porque pedía un domicilio inexistente. El formulario servía bien a la mitad urbana de lo que la Secretaría atiende.

| Cambio | Naturaleza | Motivo |
|---|---|---|
| `tiene_direccion` | Pregunta nueva, obligatoria | Encamina el paso. Obligatoria porque, sin respuesta, el formulario elegía una rama en silencio (DEC-47) |
| `nombre_lugar` | Campo nuevo | Sustituye al domicilio donde no lo hay. **Se propone desde la capa oficial que contiene el punto**: si el punto cae en el Bosque de Tlalpan, el nombre aparece solo |
| `usaNombreDelPunto()` | Función nueva | Gemela de `usaAlcaldiaDelPunto()`. El sistema propone; corrige quien denuncia (DEC-41) |
| Orden del paso | Bifurcado | Con domicilio, la dirección primero y el punto después. Sin domicilio, el punto primero —es el único localizador— y la identificación del sitio después, porque el nombre se propone desde la capa |

#### La obligatoriedad, a donde pertenece

Las condiciones —qué campo se pide y cuándo— vivían sueltas en `valida()`. El documento 09 se genera de `OBLIG`, de modo que **afirmaba que el domicilio de notificación era obligatorio siempre**, cuando sólo se pide a quien rechaza la notificación electrónica. El documento con el que se sustenta la minimización ante la Unidad de Transparencia no puede decir algo distinto de lo que el formulario hace. Diecisiete campos declaran hoy su condición en `OBLIG`, con un texto legible que el documento 09 publica en una columna propia, y `valida()` quedó reducida a comprobar presencia (DEC-48).

#### Dos observaciones del propio usuario, ambas correctas

**«Color o características del sitio» y «Otras referencias» eran la misma pregunta hecha dos veces.** Dos cajas vacías donde bastaba una, y el efecto habitual: quien no sabe en cuál escribir, no escribe en ninguna. Peor aún, este mismo bloque estaba a punto de añadir una tercera —«cómo se llega»— para la ruta sin domicilio. Las tres son ahora una sola: **«Cómo se reconoce y cómo se llega al sitio»**, obligatoria sólo donde no hay domicilio, porque ahí es lo único que permite al personal de inspección llegar a una coordenada.

**La pregunta del establecimiento estaba en el paso equivocado, y el código lo estaba diciendo.** Existía `avisoHeredado()`, una función cuyo único trabajo era explicar en el paso 3 lo contestado en el paso 2: «En el paso anterior señalaste que...». **Cuando hace falta un puente así, la pregunta está mal colocada.** No es un detalle del lugar: es la primera pregunta sobre quién responde, y propone la respuesta a la siguiente. Movida al paso 3, el aviso puente se eliminó entero y con él la redundancia con «¿a quién denuncias?» que estaba anotada desde la revisión heurística (DEC-49).

#### Las tres rutas de identificación

Anónima, datos escritos y cuenta Llave CDMX. **La tercera no es un adorno de la segunda:** escribir el nombre a mano identifica para contacto pero no acredita a nadie, y la reserva de identidad frente a la persona denunciada sólo tiene sentido si hay identidad. La elección se pide **en el paso 5 y no en la primera pantalla**, por tres razones que constan en DEC-50; la tercera es de calendario: así el formulario puede salir sin la integración y esperarla, en vez de depender de ella. La cuenta se simula y **la pantalla dice que se simula**, porque P-15 sigue abierto.

#### Lo que se recuperó

El generador del documento 09 **no estaba en ninguna parte**: se había escrito en una sesión anterior y se perdió con ella, de modo que el documento sólo podía mantenerse a mano —justo lo que no debe pasar con un documento generado—. Se reescribió y quedó en `construccion/`, y se detiene con error si no encuentra la parte redactada a mano, en vez de publicar un documento mutilado. Las tres baterías de pruebas se reunieron en `construccion/pruebas/` con un solo corredor.

**Verificación de cierre.** **101 comprobaciones automatizadas, todas en verde**, incluidas las dos baterías anteriores, que se conservan: una prueba vieja en verde es lo que avisa cuando un cambio nuevo rompe algo viejo. Sintaxis correcta. Cero funciones sin uso, cero duplicadas, cero claves de estado escritas y nunca leídas, cero clases de estilo huérfanas; los cuatro `!important` están todos dentro de `prefers-reduced-motion`, que es su uso legítimo, y el único selector declarado dos veces sigue siendo `textarea`, la excepción anotada. Documento 09 regenerado: **50 campos, 20 datos personales, 17 con obligatoriedad condicionada, ninguno sin uso declarado**. Comprobado que la denuncia en el Bosque de Tlalpan ya puede presentarse, que sin domicilio no se piden calle ni colonia ni código postal y sí el nombre y el acceso, que con domicilio todo sigue igual que ayer, que las tres rutas de identificación piden lo suyo y sólo lo suyo, y que el resumen final distingue la identidad acreditada de la que no lo está.

**Nota sobre el método.** Dos de las comprobaciones antiguas fallaron al correrlas de nuevo. Ninguna era una regresión: una nombraba un campo que hoy está fundido en otro, y la otra forzaba la obligatoriedad de un campo que ahora tiene condición propia, de modo que medía la condición y no la red que pretendía probar. Se corrigieron las pruebas, no el código —y se anota, porque es la tercera vez en el proyecto que lo defectuoso resulta ser el método de verificación, y la única defensa contra eso es comprobar siempre qué falló antes de tocar nada.

### 19 de septiembre de 2026 · los datos accesorios del lugar, arriba del mapa y sin plegar

Cambio pedido por el usuario, con una razón que no se había visto al plegarlos: **el mapa partía en dos el bloque de dirección**. Calle, número, alcaldía, colonia y código postal arriba; el mapa y el panel de capas en medio; y luego, abajo, entre calles y cómo se reconoce el sitio —que son dirección también—. Puestos donde corresponden, el paso se lee de corrido: la dirección completa, y después el mapa que la confirma.

Sobre el plegado, **lo que cambió es el tamaño del bloque**. Cuando se plegó (DEC-44) tenía siete campos; hoy tiene tres, porque el propio usuario detectó que dos de ellos preguntaban lo mismo (DEC-47). A tres campos, esconderlos cuesta más de lo que ahorra: quien tiene el dato no encuentra dónde ponerlo.

| Cambio | Naturaleza | Motivo |
|---|---|---|
| Posición del bloque | Movido | De debajo del panel de capas a justo después del código postal, cerrando la dirección (DEC-51) |
| `.enc-opcional` | `button` → `h3` | Ya no despliega nada; es el encabezado de una sección |
| `mas_lugar` | Clave retirada | Sin plegado no hay estado de plegado que guardar |
| `ENVUELTOS_LUGAR` en `valida()` | Red retirada | Existía para desplegar el bloque antes de mostrar un error dentro. Sin nada plegado sería código muerto |

**Lo que se conserva de DEC-44** es lo que sigue valiendo: «opcional» se dice **una vez, en el encabezado**, y no campo por campo. La regla `.cuerpo-opcional .opc{display:none}` sigue en pie y el paso mantiene seis apariciones de la palabra en lugar de las nueve que tendría.

**Medición.** El paso 2 pasa de 2 163 a 2 864 px: de 2.8 a 3.8 pantallas de teléfono. **Cuesta una pantalla**, y conviene decirlo sin adornos. Sigue por debajo de los 3 609 px con que empezó el día anterior, y la contrapartida es que ya no hay tres campos escondidos tras un clic que la mayoría no daba.

**Verificación de cierre.** 94 comprobaciones en verde. Sintaxis correcta. Cero funciones sin uso, cero claves escritas y nunca leídas, cero clases de estilo huérfanas. Comprobado por medición del árbol que el bloque queda **después del código postal y antes del mapa**, que no queda ningún plegable, que los tres campos se ven de entrada, que lo capturado sobrevive a salir y volver al paso, y que dentro del bloque no se repite la palabra «opcional».

**Nota sobre las pruebas.** La batería que comprobaba el plegado se reescribió para comprobar lo contrario, y se renombró: se llamaba `01-plegado-y-ubicacion.py` y describía un comportamiento que ya no existe. **No se borró.** Su encabezado ahora cuenta las dos decisiones —por qué se plegó y por qué se dejó de plegar—, que es justo lo que alguien necesita saber dentro de seis meses antes de proponer plegarlo otra vez.

### 20 de septiembre de 2026 · la pantalla de inicio

Observación del usuario: «mucho texto y poco atractiva». Medida antes de tocar nada, le sobraba razón: **232 palabras repartidas en cuatro cajas de aviso visualmente idénticas**, donde nada distinguía lo importante de lo accesorio, y el botón de empezar a **1 268 px** —casi dos pantallas de teléfono de desplazamiento antes de poder hacer nada—.

| Cambio | Naturaleza | Motivo |
|---|---|---|
| Título y bajada de la tarjeta | **Eliminados** | Repetían casi literalmente el encabezado institucional que está justo arriba. Era la mitad de la sensación de exceso: lo mismo dicho dos veces seguidas |
| Tres datos de entrada | Bloque nuevo | Sin tu nombre · 10 minutos · Con folio. Es lo que alguien necesita saber antes de decidir si empieza |
| Botón de iniciar | Subido | De después de 232 palabras a inmediatamente después de los tres datos |
| «Qué pasa después» | Cuatro frases → cuatro pasos | Numerados, con título corto y una línea de detalle. Se lee de un vistazo en vez de leerse |
| «Ten a la mano» | Cuatro viñetas → tres etiquetas | «Dónde ocurre», «Qué ocurre y desde cuándo», «Fotos o videos, si tienes» |
| Cajas `.aviso` en la portada | De cuatro a cero | Lo que las justificaba era la advertencia, no la enumeración |

**Medición.** De **232 a 123 palabras**, de **1 162 a 880 px** de alto, y el botón de iniciar de **1 268 a 411 px**: visible sin desplazar tanto en teléfono como en escritorio.

**Un defecto propio, encontrado al mirar la captura y no al medir.** La primera versión ponía el título y el detalle de cada paso como dos celdas sueltas de la misma rejilla, de modo que el detalle caía en la columna de 28 píxeles del número y **se partía una palabra por renglón**. Ninguna comprobación automática lo habría visto: el texto estaba, era correcto y no había error en consola. **Hay una clase de defecto que sólo aparece mirando**, y por eso el cierre incluye siempre una captura. Se corrigió envolviendo cada paso en su propia celda, y la prueba nueva mide el ancho del texto para que no vuelva a pasar inadvertido.

**Verificación de cierre.** 112 comprobaciones en verde, incluidas dieciocho nuevas sobre la portada, en teléfono y en escritorio: tope de palabras, botón visible sin desplazar, cero cajas apiladas, que la tarjeta no repita el título ni la bajada del encabezado, que el texto de los pasos no se parta, y sin desbordamiento horizontal. Cero funciones sin uso y cero clases de estilo huérfanas.

### 20 de septiembre de 2026 · barra de pasos, paleta y datos del lugar

Tres cambios pedidos por el usuario en la misma sesión, todos de forma más que de fondo.

**El aviso de denuncia sin terminar (DEC-54).** Se pidió borrar la parte que nombraba el supuesto y decía que el borrador se guardó en el navegador. Se acortó, pero **se conservó una frase que no se había pedido conservar**: que la denuncia aún no se ha presentado. Sin ella alguien puede cerrar el navegador creyendo que ya denunció. De 36 a 22 palabras, y una prueba automatizada fija que esa frase no se pierda en una limpieza futura.

**La barra de pasos y la paleta (DEC-55).** La barra era un filete de avance con seis etiquetas debajo. Ahora es un círculo por paso: palomita verde en los recorridos, círculo oscuro relleno con el número en el actual, número gris en los pendientes, unidos por una línea que se pinta de verde conforme se avanza. **El estado no se confía al color** —la palomita y el número lo dicen igual—, de modo que sirve también a quien no distingue verde de gris. En pantalla estrecha se ocultan las seis etiquetas y queda el renglón que nombra el paso actual: los círculos caben, seis etiquetas no.

Sobre la paleta, la observación fue «está saturadísimo todo de guinda». Medido: **cincuenta reglas de estilo lo usaban**. El efecto de eso es que nada destaca, porque todo destaca. Quedan diecinueve.

| Uso | Color | Por qué |
|---|---|---|
| Barra de gobierno, encabezado, pie | **Guinda** | Identidad institucional. No se toca, por indicación expresa |
| Título de cada paso y botón de acción principal | **Guinda** | Uno por pantalla: eso es lo que la hace reconocible sin saturarla |
| Lo que se toca y lo que quedó elegido | **Azul `#1A56A8`** | Opciones, enlaces, tarjetas seleccionadas, zonas de carga. Es donde más se repetía |
| Avance | **Verde `#1B6B43`** | Ya estaba declarado como color de «hecho»; la barra de pasos lo usa |
| Estructura y jerarquía | **Neutros** | Subtítulos, encabezados de resumen, etiquetas: se resuelven con tipografía, no repitiendo el color de la institución |

El recordatorio de materia, que va fijo en todas las pantallas, pierde el fondo guinda y conserva un **filete dorado** —que es el uso para el que ese color está declarado en la paleta: «sólo filetes y rellenos, nunca texto»—.

**Los datos accesorios del lugar (DEC-56).** Se pidió eliminar el encabezado «Más datos del lugar — todo esto es opcional» y la línea que lo explicaba, dejando los campos como parte de la dirección. Hecho: los tres siguen a la colonia y el código postal sin caja que los envuelva. **Con eso, «opcional» vuelve a marcarse campo por campo, y es correcto**: entre campos visibles de un mismo bloque la palabra sí distingue —la calle se pide, las entre calles no—, que es exactamente el caso que DEC-46 reservaba para ella. Las tres clases de estilo del bloque se retiraron al quedar sin uso.

**Verificación de cierre.** 118 comprobaciones en verde. Sintaxis correcta. Cero funciones sin uso, cero claves de estado escritas y nunca leídas, cero clases de estilo huérfanas. Revisión visual en capturas a 900 y a 390 px: la barra de pasos se lee en ambas, las etiquetas se ocultan en la estrecha y queda el renglón del paso actual, y no hay desbordamiento.

**Nota sobre las pruebas.** Dos comprobaciones fallaron al correrlas de nuevo y ninguna era regresión. Una fijaba la existencia del bloque plegable, que acaba de disolverse; se reescribió para comprobar lo contrario. La otra miraba la marca de «opcional» **sin activar la obligatoriedad**, de modo que en modo de prueba veía todos los campos marcados y daba por defectuoso lo que era correcto. Es el mismo error de método de la vez anterior: la prueba medía una cosa creyendo medir otra.

### 20 de septiembre de 2026 · la portada, segunda pasada

El usuario revisó la portada rehecha y señaló dos cosas: falta un texto de presentación, y el aviso de denuncia sin terminar «casi tiene el mismo peso que iniciar».

**Las dos observaciones son correctas, y la primera corrige algo que yo hice.** Al recortar las 232 palabras se fue con ellas lo que presentaba el trámite. Quedaron tres tarjetas y un botón, sin una línea que dijera para qué sirve nada de eso: eficiente y abrupta. La lección es que **recortar no es lo mismo que jerarquizar**: lo que sobraba era la repetición y las cuatro cajas iguales, no la presentación.

| Cambio | Naturaleza | Motivo |
|---|---|---|
| Párrafo de presentación | Recuperado | Dos frases: qué puede hacer la Secretaría y qué necesita para hacerlo. No repite el encabezado, que dice qué es el sitio, no para qué sirve |
| Orden | Ajustado | Presentación → los tres datos → botón. La información antes de pedir la acción, que es lo que se pidió |
| Aviso de denuncia sin terminar | Caja → tira | Era una caja con relleno y un botón guinda, es decir, un segundo botón principal compitiendo con el primero. Ahora es una tira con filete dorado, botón secundario y un enlace para descartar |

**Medición.** 172 palabras —frente a las 232 de origen y las 123 de la versión anterior—, y el botón de iniciar a **573 px en teléfono y 472 en escritorio**: visible sin desplazar en ambos, que era la condición que no había que perder. El aviso de borrador ocupa el **19 %** del área del botón principal en escritorio.

**Un defecto de alineación.** El párrafo nacía centrado como bloque, con un ancho máximo menor que el de las tarjetas, de modo que su borde izquierdo no coincidía con el de nada. Se alineó a la izquierda de la tarjeta y la prueba lo mide: los dos bordes deben coincidir dentro de dos píxeles. En teléfono, además, a 20 px ocupaba siete renglones y empujaba el botón al filo de la pantalla; al tamaño de cuerpo ocupa cinco.

**Verificación de cierre.** 124 comprobaciones en verde. Cero funciones sin uso y cero clases de estilo huérfanas. Revisión visual en capturas de 1 300 y 390 px.

**Nota sobre las pruebas.** Una comprobación falló porque buscaba el aviso de borrador por su clase anterior, que acababa de cambiar. Es el tipo de fallo que conviene que ocurra: la prueba estaba atada a lo que el aviso *era*, no a lo que hace, y al cambiar avisó. Se actualizó el selector y se añadió una comprobación de lo que sí importa —que el botón de continuar no tenga relleno, para que no compita con el de empezar—.

### 20 de septiembre de 2026 · cuatro ajustes de forma pedidos en revisión

**«Qué pasa después», en horizontal (DEC-58).** Cuatro frases apiladas se leen como una lista; cuatro columnas unidas por una línea se leen como una secuencia. Usa la misma gramática visual que la barra de pasos —círculo numerado y línea—, de modo que el formulario dice «esto son pasos» de una sola manera. En pantalla estrecha van dos por renglón y sin línea. La nota de plazos por confirmar salió de la columna, donde no cabía, y va debajo.

**El aviso de borrador, fuera del formulario (DEC-59).** Se preguntó si podía ser una ventana nativa del navegador. **Se descartó, y conviene dejar escrito por qué**: `confirm()` bloquea la página hasta que se responde, así que no se puede mirar nada para decidir; aparece encabezada con «La página en … dice», que es el formato que la gente cierra por reflejo sin leer; no admite formato, de modo que no lleva identidad institucional; y algunos navegadores suprimen esos diálogos al cargar, en cuyo caso **el borrador quedaría irrecuperable y sin aviso**. Lo que sí resuelve la intención —sacarlo del formulario— es una franja de sistema entre el encabezado y la tarjeta, a todo lo ancho, sólo en la pantalla de inicio.

**El paso 2 no muestra nada hasta contestar (DEC-60).** La pregunta del domicilio decide la forma de todo lo demás. Mostrada junto con el resto se contesta de paso sin leerla, y la persona puede acabar en la ruta equivocada, que es el defecto que DEC-47 vino a corregir. Sola en pantalla se lee. Mientras no se contesta tampoco hay Continuar.

**Asterisco en lo obligatorio, en vez de rótulo en lo opcional (DEC-61).** La palabra llegó a aparecer veintiocho veces en el recorrido; cuando casi todo es opcional deja de significar algo y el formulario **parece más largo de lo que es**. Invertida la marca, lo que lleva señal es lo poco que se exige. El asterisco por sí solo no es accesible, así que lo acompaña la palabra «obligatorio» en texto visible sólo para lectores de pantalla, y la leyenda del panel lo explica. Medido en el paso 2: **de nueve apariciones de «opcional» a cero**, con cinco asteriscos.

**Texto corregido desde un comentario en el artefacto.** La ayuda de la pregunta del domicilio nombraba los sitios sin domicilio en lenguaje coloquial. Pasa a los términos que usa la Secretaría: área natural protegida, barranca, bosque urbano, terreno forestal o de cultivo, camino o canal.

**Verificación de cierre.** **132 comprobaciones en verde**, ocho de ellas nuevas. Sintaxis correcta. Cero funciones sin uso, cero claves escritas y nunca leídas, cero clases de estilo huérfanas. Documento 09 regenerado. Comprobado por medición: el paso 2 sin contestar muestra un solo campo y sólo el botón de Regresar, y al contestar muestra nueve campos y los dos botones; la franja de borrador **no está dentro del formulario**, va encima de la tarjeta y desaparece al entrar al cuestionario; los cuatro momentos van en una fila en pantalla ancha y en dos en la estrecha.

**Nota sobre las pruebas.** Cuatro comprobaciones fallaron al correrlas de nuevo y ninguna era regresión: dos miraban el aviso de borrador por la clase y el contenedor anteriores, una fijaba un ancho mínimo que dejó de tener sentido al pasar a columnas, y otra leía la marca de obligatoriedad por la palabra «opcional», que acababa de desaparecer. **Es el patrón de toda la sesión**: cuando una prueba se ata a cómo se ve algo y no a lo que garantiza, cambia el diseño y la prueba se rompe sin que haya nada roto. Las cuatro se reescribieron contra la garantía —que el aviso quede fuera del formulario, que el texto no caiga en la columna del número, que lo obligatorio lleve marca— y no contra la apariencia.

### 20 de septiembre de 2026 · limpieza de textos de ayuda

Revisión en pantalla, señalando uno por uno los textos que estorban. Todos eran de la misma clase: **explicar con palabras lo que el propio control enseña al usarlo**.

| Texto retirado | Dónde | Por qué sobraba |
|---|---|---|
| «Por ejemplo: Avenida Río Churubusco» | Calle | Nadie necesita un ejemplo de cómo es una calle |
| «Si el punto del mapa cae en otra, el formulario te lo advierte» | Alcaldía | Sigue siendo cierto —el aviso existe—, pero anunciarlo antes de que ocurra no ayuda: cuando ocurre, el aviso se explica solo |
| «No hace falta que suene formal» | Descripción | La caja vacía ya invita a escribir; decirlo no cambia lo que la persona escribe |
| «Por ejemplo: "De la chimenea de la fábrica…"» | Descripción | Ejemplo por supuesto, de M-05 |
| «Si es así, lo habitual es que el establecimiento sea el responsable, y el formulario lo propone» | Establecimiento | Describe lo que la persona va a ver ocurrir un segundo después |
| «Elige el que más se parezca» | Tipo de establecimiento | Es lo que cualquiera hace ante una lista |

**Dos cambios de fondo, no de recorte.**

El título de la descripción **daba por hecho que los hechos siguen ocurriendo**: «Describe lo que está ocurriendo». Una denuncia puede ser de ayer o de hace dos meses, y el campo de temporalidad que viene después contempla las tres cosas. Pasa a **«Cuenta qué pasó o qué está pasando»**.

Lo que de verdad orienta —qué se hace, quién lo hace, en qué horario, con qué frecuencia y qué efecto produce— estaba en una caja de aviso debajo del campo. **Pasa a ser el marcador dentro del propio campo**: se lee en el momento en que hace falta, desaparece al empezar a escribir y no ocupa espacio permanente. `campoArea()` ganó un parámetro para ello.

**Esto revierte M-05**, que añadió un ejemplo de descripción por cada supuesto. Se retiran la función y los dieciocho textos: dejarlos sin llamador sería exactamente el código zombi que la norma prohíbe. Quedan en el historial si se quisieran recuperar.

**Los subtítulos de sección vuelven al guinda.** En la reducción de saturación habían pasado a neutro, pero un h2 grande en guinda para el paso y un h3 menor en guinda para la sección son jerarquía de tipografía **y** color a la vez, no repetición. Fue una corrección pedida al verlo en pantalla, y es correcta.

**Corrección desde un comentario en el artefacto.** La ayuda de la pregunta del domicilio pasa a los términos con que la Secretaría nombra esos sitios: área natural protegida, barranca, bosque urbano, terreno forestal o de cultivo, camino o canal.

**Verificación de cierre.** 132 comprobaciones en verde. Sintaxis correcta, cero funciones sin uso, cero clases de estilo huérfanas. Comprobado por lectura del árbol que la calle y la alcaldía ya no llevan ayuda, que el número exterior dice «escribe S/N», y que el campo de descripción tiene el marcador dentro y ninguna ayuda ni ejemplo alrededor.

### 20 de septiembre de 2026 · jerarquía visual de los seis niveles

Petición: que se distingan bien el paso, el título de sección, la subsección, las preguntas y las respuestas. **Medido antes de tocar nada, había dos defectos, no una impresión:**

1. **El título del paso y el de sección eran idénticos**: 20 px, Cabin 600, guinda los dos. Lo único que los separaba era el círculo con el número.
2. **La respuesta se veía más grande que la pregunta**: el control a 16 px y su etiqueta a 14. La jerarquía al revés, en todos los campos del formulario.

| Nivel | Antes | Ahora |
|---|---|---|
| **Paso** | 20 px Cabin 600 guinda | **24 px Cabin 700 guinda**, con el número en círculo |
| **Sección** | 20 px Cabin 600 guinda | 20 px Cabin 600 guinda, **con filete dorado encima** |
| **Subsección** | 14 px | **13 px en mayúsculas espaciadas, gris, con filete inferior** |
| **Pregunta** | 14 px Roboto 500 | **16 px Roboto 600** |
| **Respuesta** | 16 px Roboto 400 | igual, dentro de un control con borde |
| **Ayuda** | 13 px gris | igual |

De paso, el encabezado «¿Desde cuándo ocurre?» dejó de ser un estilo escrito en línea que repetía a mano el tamaño del título de sección, y pasa a usar la clase.

**Lo que se comprueba es la regla, no la tabla.** La batería nueva mide los seis niveles y exige dos cosas: que cada nivel se separe del contiguo por **al menos dos rasgos** —tamaño, peso, familia, color, mayúsculas o el hecho de ir dentro de un control con borde— y que **ninguna respuesta se vea mayor que su pregunta**. Fijar la tabla de tamaños congelaría el diseño; fijar la regla deja rediseñar sin volver a caer en lo mismo. Pregunta y respuesta comparten tamaño, y se separan por peso y por el borde del control: dos rasgos, que es el mínimo exigido.

**Nombres de establecimiento (DEC-63).** «Como aparece en el anuncio o la fachada» **supone que el sitio tiene anuncio**, y muchos no lo tienen —una escuela, una bodega, un predio en obra—. Y «nombre comercial» excluye a lo que no es comercio. Pasa a «Nombre del establecimiento», con ejemplos que cubren los dos casos.

**Verificación de cierre.** **147 comprobaciones en verde**, quince de ellas nuevas. Sintaxis correcta, cero funciones sin uso, cero clases de estilo huérfanas. Documento 09 regenerado. Revisión visual en captura a 1 000 px.

### 20 de septiembre de 2026 · ubicación sin geolocalización, y confirmación del punto

Bloque largo de revisión en pantalla. Lo sustantivo son tres cosas.

**Se retira la detección de ubicación del dispositivo (DEC-67).** Revierte DEC-45, que se había implementado el día anterior. El formulario deja de pedir ese permiso al navegador y **no queda una sola mención a la API de geolocalización en el código**. El argumento es el que no se tuvo al añadirla: un permiso de ubicación en un formulario de denuncia es, para quien denuncia, justo la clase de petición que da motivo a desconfiar, y ahorrar un clic no lo compensa.

**Lo sustituye algo mejor (DEC-69):** pegar las coordenadas o el enlace de Google Maps. La persona pega lo que ya tiene —el pin que dejó en el mapa— y el punto se coloca. **El enlace se lee en el navegador, con una expresión regular sobre el texto**; el sistema no lo abre ni consulta nada fuera, y una prueba vigila que la operación no genere ninguna petición de red. Se reconocen las tres formas en que ese servicio escribe la coordenada en la dirección web: `@lat,lon`, `q=lat,lon` y `!3dlat!4dlon`. Los enlaces cortos no la llevan dentro, de modo que no hay nada que leer: **se pide el enlace completo en vez de resolverlo por fuera**, que es exactamente lo que se quiso evitar.

**El punto debe confirmarse (DEC-70).** El punto se arrastra, y un roce basta para moverlo unas calles; de esa coordenada dependen el área que atiende y el tipo de suelo que se invoca. Aparece una casilla bajo el resultado del cruce —debajo de lo que ese punto acaba de determinar— y **cualquier colocación o arrastre posterior la borra**. Ésa es la única parte que la hace útil: una confirmación que sobrevive al movimiento no confirma nada.

**Una regla que hubo que escribir dos veces, y esta vez a tiempo.** El mapa vectorial del artefacto sobrescribe `ponMarcador`, así que la limpieza de la confirmación tuvo que repetirse en `mapa_svg.js`. Es la segunda regla del LEEME de la carpeta de construcción, anotada el día anterior después de que un desfase parecido llegara al artefacto sin que nadie lo viera. Esta vez se aplicó **antes** de que fallara.

**Un defecto propio, encontrado al probar.** La casilla se colocó primero fuera del panel de capas, que es lo único que se vuelve a dibujar al mover el punto: aparecía sólo tras un render completo, de modo que quien pegaba unas coordenadas no la veía. Se movió dentro del panel, que además es su sitio natural.

| Otros cambios | |
|---|---|
| Tarjetas de la portada | Retiradas (DEC-65). **Con ellas se va de la primera pantalla el aviso de que se puede denunciar sin dar el nombre**, que era M-01: la opción sigue existiendo, pero ya no se anuncia antes de empezar |
| «Ten a la mano» | Tenía borde redondeado y fondo blanco, es decir, el aspecto de un control: pasa a lista con viñeta dorada |
| Pie de página | Las dos vías de presentación juntas, con el correo primero, y las dos áreas que atienden. **Nombrando a la dirección general y no a la coordinación**, conforme a DEC-30 |
| Botones de sí y no | 40 px con ratón, 48 con el dedo: la regla del blanco táctil se condiciona al tipo de puntero, que es lo que mide, y no al ancho de pantalla (DEC-68) |

**Verificación de cierre.** **166 comprobaciones en verde.** Sintaxis correcta en las dos piezas, cero funciones sin uso, cero claves escritas y nunca leídas, cero clases huérfanas. Documento 09 regenerado: 52 campos, 18 con obligatoriedad condicionada. Comprobado que sin punto no se pide confirmarlo, que al colocarlo aparece sin marcar, que sin confirmar el paso no avanza, y que **mover el punto borra la confirmación, destilda la casilla y vuelve a frenar el paso**.

### 20 de septiembre de 2026 · el peso de las tres acciones

«Regresar» tenía borde y pesaba lo mismo que los botones de sí y no, justo en la pantalla donde lo único que hay que hacer es leer una pregunta y contestarla. **Retroceder es navegación, no una respuesta**, y no debía parecerlo. Pasa a «‹ Regresar», sin borde ni relleno, en los siete lugares donde aparece.

| Acción | Cómo se ve |
|---|---|
| Avanzar | Relleno guinda. **Una por pantalla** |
| Responder | Borde y fondo neutro |
| Retroceder | Ni borde ni relleno: flecha y texto |

El blanco táctil de 44 px se conserva por relleno interior y no por caja visible, que es lo que la norma pide: superficie para el dedo, no un recuadro dibujado.

**Lo que se comprueba es la regla.** La batería de jerarquía gana cuatro comprobaciones: que retroceder no lleve borde ni relleno, que responder lleve borde y fondo neutro, que avanzar sea lo único con relleno de color, y que retroceder conserve los 44 px.

**Una prueba mal escrita, corregida.** La primera versión daba por «relleno» cualquier fondo no transparente, de modo que consideraba rellenos los botones de sí y no, que son blancos sobre blanco. Blanco sobre blanco no distingue nada: lo que la regla quiere decir es **relleno de color**, y así se escribió.

**Pregunta abierta que quedó registrada como P-18.** Si el sistema debe resolver los enlaces cortos de Google Maps para sacar la coordenada. No se puede hacer desde el navegador —la política de origen cruzado lo impide—, así que exige servidor; y aceptar que el servidor pida una dirección web escrita por el público es una vulnerabilidad conocida, admisible sólo con lista blanca estricta. La recomendación es hacerlo en la versión funcional, con esas condiciones, porque el beneficio recae en el caso más difícil: el sitio sin domicilio, donde el pin del mapa es lo único que la persona tiene.

**Verificación de cierre.** 171 comprobaciones en verde. Cero clases de estilo huérfanas.

### 20 de septiembre de 2026 · reseño del paso 2, a partir de la auditoría

Quien construye el formulario se declaró confundido sobre cómo debía funcionar el paso del lugar. **Esa confusión se tomó como el hallazgo y no como el punto de partida:** si quien conoce cada decisión no sabe explicar el paso, nadie que llegue de la calle podrá recorrerlo. Se auditó y el resultado está en el documento 14.

#### El defecto que la auditoría encontró

**La alcaldía existía dos veces**: la escrita y la que calcula el cruce espacial. El turnado usaba la del punto; el acuse mostraba la escrita; **el formulario no exigía que coincidieran**. Comprobado capturando una dirección en Coyoacán y el punto dentro del Bosque de Tlalpan: la denuncia se enviaba diciendo, en el mismo resumen, que ocurre en «Av. México 10, Del Carmen, C.P. 04100, Coyoacán» y que ocurre en «Área Natural Protegida local — Bosque de Tlalpan», turnada a la DGCORENADR. **Un expediente que nace contradiciéndose.**

Se resolvió de raíz y no administrando el conflicto: **la alcaldía deja de preguntarse y la determina el punto** (DEC-72), que es el mismo dato con el que se resuelve el turnado. Reconoce además algo cierto: los límites de alcaldía no se conocen con precisión, así que se pedía un dato que el sistema determina mejor.

#### Lo demás

| Cambio | Motivo |
|---|---|
| Dos bloques rotulados | «La dirección del lugar» —para que el personal llegue— y «El punto en el mapa» —decide qué área atiende—. Dicho una vez arriba y una vez en cada bloque (DEC-73) |
| Las tres vías, juntas | Buscar la dirección escrita, pegar coordenadas o enlace, o dar clic en el mapa: en una lista, con el mismo peso. Antes estaban repartidas y el subtítulo describía sólo una (DEC-74) |
| «Ubicar en el mapa» a secundario | Había dos acciones con relleno compitiendo por ser el siguiente paso |
| Sin «Quitar el punto» | El punto es obligatorio: su único destino era un error (DEC-74) |
| La confirmación, junto a los botones | Y diciendo qué se confirma: alcaldía y área identificada, al día con el punto (DEC-75) |

#### Código que quedó sin dueño y se retiró

`alcaldia_punto`, `usaAlcaldiaDelPunto()`, el aviso de discrepancia, `quitaPunto()` y el catálogo `ALCALDIAS` completo, que existía sólo para llenar el selector.

#### Dos defectos propios, los dos encontrados al probar

**La casilla quedó duplicada.** Se añadió la nueva encima de los botones sin retirar la que estaba dentro de la ficha del cruce: **dos elementos con el mismo identificador**. Se retiró la vieja y la que queda tiene contenedor propio, refrescado junto con la ficha, porque el punto cambia sin rehacer la pantalla —rehacerla reiniciaría el mapa y perdería el encuadre—.

**El guion de construcción se detuvo con error**, como se le pidió que hiciera: la vía que requiere geocodificación cambió de marcado y de texto. Se actualizó. **Es la primera vez que esa salvaguarda avisa en lugar de dejar pasar el fallo en silencio**, que era exactamente para lo que se puso.

**Verificación de cierre.** **177 comprobaciones en verde.** Sintaxis correcta, cero funciones sin uso, cero claves escritas y nunca leídas, cero clases huérfanas. Documento 09 regenerado. Comprobado que la alcaldía ya no se pregunta, que la determina el punto, y que **el resumen del paso 6 usa la misma alcaldía con la que se turna**, que es el defecto que abrió todo esto.

---

## Bloque: la portada, la estadística, el aviso de privacidad y el relleno

**20 de septiembre de 2026.** Cinco encargos que llegaron seguidos y que resultaron ser el mismo tema: qué dice el formulario de sí mismo, y a quién se lo dice.

### La portada ya no describe un trámite

La versión anterior abría diciendo lo que la Secretaría puede hacer. Era correcta y era fría, y sobre todo era **breve donde tenía que informar**: quien nunca ha denunciado llega con tres preguntas y la pantalla no contestaba ninguna.

La nueva abre con el derecho —*Denunciar el daño ambiental es tu derecho*— y las contesta en orden: **qué me reconoce la ley**, cuatro enunciados con palomita; **por qué importa**, un párrafo que dice lo que ninguna otra pantalla decía —que la Ciudad no tiene personal en cada calle y que buena parte del daño sólo se conoce porque alguien lo reportó—; y **qué pasa después**, que ya estaba. El tope de palabras sube de 180 a 340 y **sigue habiendo tope**, comprobado a 390 px: el botón de empezar tiene que verse sin desplazar (DEC-76).

Con los cuatro enunciados **vuelve a la primera pantalla la promesa de denunciar sin dar el nombre** (M-01), que se había perdido sin que nadie lo notara al retirar las tarjetas de datos (DEC-77).

### Dos preguntas para la estadística

Género y rango de edad, al final del paso 5 y fuera del bloque de contacto. Se piden **también en la ruta anónima**, que es donde se perdería la mitad del universo, porque un género y un rango de edad no identifican a nadie ni entran al expediente. En desplegable y no en botones, para que se lean como lo que son. Ambas admiten «Prefiero no decirlo», que no es cortesía: **la identidad de género es dato sensible** y sólo puede tratarse con consentimiento expreso (DEC-78, P-20).

### El aviso de privacidad salió de la ventana del navegador

La PAOT pone su aviso simplificado en la pantalla, antes de enviar. Aquí estaba detrás de un enlace que abría una alerta con un texto provisional. Ahora es un bloque de seis rótulos —quién trata tus datos, para qué, con qué fundamento, cuánto se conservan, a quién se transfieren, cómo ejerces tus derechos—, colocado inmediatamente antes de la casilla con la que se consiente.

**Cuatro de los seis están incompletos y así se ven.** El nombre del sistema de datos personales, el ciclo de vida, el catálogo de transferencias y los datos de la Unidad de Transparencia quedan como huecos a la vista, con el mismo tratamiento que el resto de los pendientes. Ninguno se rellenó con una aproximación: estas pantallas van a nombre de la Secretaría (DEC-79, P-19).

### El relleno de teclado

Se probó el formulario de la PAOT llenando todos los campos con letras al azar: **se envió**. El formulario mide ahora tres señales del relato —cuántas palabras tiene, qué proporción de vocales y si hay caracteres repetidos— y no deja avanzar cuando ninguna se cumple, con un mensaje que dice cuál es el problema en lugar de «este dato es necesario».

El criterio de diseño fue **no castigar a quien escribe mal**: un relato con faltas de ortografía, sin acentos y sin puntuación pasa, y así está comprobado en la batería 06. Lo que no pasa es una cadena sin vocales o una tecla repetida.

**Y se dejó escrito lo que esto no resuelve.** Una validación en el navegador ayuda a quien escribe de buena fe; a quien quiere hacer daño no lo detiene, porque el navegador es suyo y puede saltárselo. Las defensas que sirven —prueba de humanidad, límite por origen, verificación del correo, detección de duplicados, umbral de ráfaga y puntaje de completitud— viven en el servidor y son decisiones, no código. El documento 15 las desarrolla con su costo y su efecto, y P-21 las pone a decisión (DEC-80).

### El acuse toma dos cosas del de la PAOT

Que el correo puede caer en la carpeta de no deseados, que es un aviso práctico. Y **la ratificación**: ante la Procuraduría, la denuncia electrónica debe ratificarse en tres días hábiles o se tiene por no presentada. Quien ha denunciado antes lo espera, y su ausencia se lee como omisión. El acuse lo dice, lo contrasta con esta vía —que no lo exige— y ofrece la remisión a la Procuraduría para quien quiera la denuncia formal con respuesta obligada (DEC-81).

**Verificación de cierre.** **208 comprobaciones en verde** en seis baterías, incluida la nueva 06 sobre estadística, aviso y relleno. Documento 09 regenerado: 54 campos, 22 datos personales, 19 condicionados, cero sin uso declarado.

### Añadido: el enlace corto de Google Maps

**20 de septiembre de 2026.** El enlace que la aplicación de mapas comparte —`maps.app.goo.gl/…`— **no lleva la coordenada dentro**. Es un identificador que alguien tiene que canjear, y el navegador no puede hacerlo: la política de origen cruzado se lo impide. No es una limitación del prototipo.

La salida no fue resolverlo, fue **dejar de necesitarlo**. El código plus —el que Google Maps muestra en la ficha de cualquier lugar, `WQGR+9V`— sí lleva la coordenada dentro: es la coordenada escrita en veinte caracteres, y se decodifica con aritmética, sin red y sin depender de ningún servicio. En el teléfono se copia con un toque, que es justo donde el enlace corto deja a la persona atorada.

Se implementó el decodificador completo y la recuperación del código corto respecto de la Ciudad. **Comprobado contra los ejemplos publicados de la especificación** —`8FVC2222+22` y `796RWF8Q+WF`— y en los cuatro rumbos de la Ciudad, incluido el sureste de Milpa Alta, que cae en otro bloque de un grado que el centro y es donde una recuperación ingenua se equivoca por un grado entero.

Y quien pegue un enlace corto ya no recibe un reproche: recibe el propio enlace para abrirlo en otra pestaña y la instrucción de qué copiar de vuelta, en dos pasos.

**P-18 —que el servidor resuelva el enlace corto— sigue abierto, pero bajó de prioridad**: ya no es la diferencia entre poder denunciar y no poder, sino entre dos toques y uno.

**Verificación.** **232 comprobaciones en verde** en siete baterías. La batería 01 tenía una comprobación que buscaba la palabra «cortos» en el aviso; se verificó que no era regresión —el aviso ahora dice más, no menos— y se actualizó para fijar lo que no puede perderse: que el enlace no trae la coordenada y qué hay que copiar en su lugar (DEC-82).

### Corrección el mismo día: el código plus no era la respuesta

La observación fue exacta: **nadie sabe qué es un código plus**. Quien no sabe sacar una coordenada tampoco va a ir a buscar un código de ocho caracteres en la ficha de un lugar. Lo que la gente sí sabe hacer es **compartir la ubicación desde Google Maps**, y ese gesto produce justamente el enlace que el navegador no puede leer.

De modo que el código plus quedó donde le corresponde —como alternativa que funciona, no como instrucción— y el campo se reordenó en torno al gesto real: *«Pegar la ubicación de Google Maps o las coordenadas»*. El aviso dejó de explicar una imposibilidad y ahora dice **quién lo va a resolver y cuándo**, con su marca de pendiente. Se añadió un «Ver cómo funcionará» que coloca un punto de demostración **sólo a petición y advirtiéndolo con todas sus letras**, igual que la cuenta simulada de Llave CDMX: sin esa advertencia, alguien probaría el prototipo con un enlace suyo y daría por buena una coordenada inventada.

**Y P-18 cambió de naturaleza.** Deja de ser una mejora opcional y pasa a ser **requisito de la versión funcional**: no es la diferencia entre dos toques y uno, es la diferencia entre que la persona marque el sitio o abandone, y pesa más justo donde el formulario es más necesario —el lugar sin domicilio—. Para que no quede como un problema abierto, el pendiente lleva ahora la especificación completa del servicio: lista blanca de tres dominios, petición que no sigue la redirección, lectura sólo del encabezado, tiempo de espera de tres segundos y salida limitada a la coordenada. Son las condiciones que evitan la falsificación de petición del lado del servidor.

Tiene además un efecto favorable que conviene decir en voz alta: resolviéndolo en el servidor, **el navegador de la persona nunca habla con Google**, de modo que Google no sabe que alguien está presentando una denuncia (DEC-83).

**Verificación.** **237 comprobaciones en verde** en siete baterías. Dos comprobaciones de la batería 01 y 07 buscaban el texto anterior del aviso; se verificó que no eran regresiones y se actualizaron para fijar lo que no puede perderse: que el enlace no trae la coordenada, que se dice quién lo resolverá, y que la demostración se advierte.

---

## Bloque: el Manual Administrativo entra como fuente

**20 de septiembre de 2026.** El Manual Administrativo de la Secretaría se incorporó a `insumos/normativa`. Resuelve tres cosas que estaban abiertas desde el principio, y corrige una que teníamos mal.

### Lo que teníamos mal

La unidad de la DGCORENADR **no se llama** «Coordinación de Inspección y Vigilancia Ambiental». Se llama **Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas**. Y la de la DGIVA es **Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano**, con el complemento que la distingue. Ambos nombres estaban mal en el turnado y en el pie de página; quedaron corregidos.

### El reparto de competencias deja de ser interpretación

Las dos atribuciones están redactadas en paralelo y la única diferencia es el tipo de suelo: la DGIVA recibe las denuncias «relacionadas con suelo urbano y áreas de valor ambiental» (fracción XXX) y la DGCORENADR las de «suelo de conservación y áreas naturales protegidas» (fracción XXXVIII). **Es exactamente la regla que el formulario aplica al cruzar el punto con las capas.** Hasta hoy se sostenía en la lectura de la Ley; ahora la sostiene también el Manual.

### Los plazos dejan de estar por confirmar

| | Suelo urbano (DGIVA) | Suelo de conservación (DGCORENADR) |
|---|---|---|
| Recibir y turnar | 3 días hábiles | 3 días hábiles |
| Analizar el caso | 10 días hábiles | 10 días hábiles |
| **Procedimiento completo** | **93 días hábiles** | **90 días hábiles** |

Los tres avisos de «plazo por confirmar» —portada, revisión y acuse— se sustituyeron por estas cifras, con la advertencia del propio Manual: son días hábiles y pueden variar si otra dependencia tarda en responder o si la persona denunciada interpone un medio de defensa.

### Dos hallazgos que conviene que la Secretaría vea

**La DGIVA tiene una Jefatura de Unidad Departamental de Seguimiento a Denuncias** cuya función expresa es atender a las personas denunciantes que preguntan por el avance y elaborarles informes. Es la unidad que faltaba nombrar en el acuse, y ya aparece ahí.

**La DGSANPAVA no recibe denuncias.** El Manual no le asigna ninguna función de recepción, trámite o seguimiento. Pero el artículo 190, fracción XXII, del Reglamento Interior **sí le atribuye operar el sistema de inspección y vigilancia en Áreas Naturales Protegidas y Áreas de Valor Ambiental**. Es una incongruencia entre el Reglamento y el Manual, no del formulario. Hasta que se aclare, el formulario no la nombra como área que atiende, y así queda registrado en P-10.

**Verificación.** 237 comprobaciones en verde. La portada creció diez palabras al sustituir el aviso por las cifras, de modo que el tope subió de 340 a 350 —es dato, no relleno— y sigue comprobándose que el botón de empezar se ve sin desplazar a 390 px (DEC-84).
