# Formulario web de Denuncia Ambiental · Documento de decisiones

**Versión:** 1.1 · 18 de septiembre de 2026
**Destinatario:** Dirección General de Inspección y Vigilancia Ambiental

Este documento concentra las decisiones ya tomadas y **las quince preguntas abiertas** que deben resolverse para pasar del prototipo a la versión funcional. Cada pregunta incluye opciones y una recomendación, de modo que pueda resolverse en sesión y quede constancia de la respuesta.

---

## Parte I. Decisiones tomadas

| Clave | Decisión | Fecha | Razón |
|---|---|---|---|
| DEC-01 | Construir primero un prototipo HTML navegable, sin servidor | 18 sep 2026 | Validar flujo, campos y reglas antes de programar |
| DEC-02 | Incorporar un filtro previo de competencia | 18 sep 2026 | Reducir la recepción de denuncias improcedentes |
| DEC-03 | Admitir la denuncia anónima con aviso de efectos | 18 sep 2026 | Maximizar la captación |
| DEC-04 | Determinar el área competente por ubicación y no por la materia declarada | 18 sep 2026 | La competencia depende del tipo de suelo, no de la calificación que haga el ciudadano |
| DEC-05 | Suprimir la pregunta sobre Área de Valor Ambiental | 18 sep 2026 | Se resuelve por cruce espacial |
| DEC-06 | Suprimir el campo de liga de Google Maps | 18 sep 2026 | Redundante con la coordenada |
| DEC-07 | Atender localmente las ocho ANP federales con convenio de coadministración | 18 sep 2026 | Instrucción del área sustantiva |
| DEC-08 | Desagregar apellidos y domicilio en campos independientes | 18 sep 2026 | Explotación estadística y precisión en la notificación |
| DEC-09 | Desactivar la obligatoriedad de campos durante la validación | 18 sep 2026 | Permitir recorrer el formulario sin fricción en las sesiones de revisión |
| DEC-10 | Incorporar el ruido de establecimientos como materia propia | 18 sep 2026 | El art. 215 de la Ley lo asigna a la Secretaría; el portal lo derivaba indebidamente |
| DEC-11 | Adoptar la identidad gráfica institucional 2024-2030 y su set de iconos | 18 sep 2026 | Cumplimiento del Manual de Identidad Gráfica |
| DEC-12 | Dar por completa la capa de Áreas de Valor Ambiental con bosques urbanos y barrancas | 18 sep 2026 | No existen declaratorias de cinturones verdes ni de cuerpos de agua; la estructura del cruce ya admite ambas categorías cuando se expidan |
| DEC-13 | Suprimir el botón de geolocalización del mapa | 18 sep 2026 | El lugar de los hechos rara vez coincide con la ubicación de quien denuncia; la búsqueda por dirección es la vía adecuada |
| DEC-14 | Sustituir el marcador por uno propio en guinda | 18 sep 2026 | El marcador de la biblioteca depende de imágenes externas que no cargan; sin marcador visible el punto no puede moverse |
| DEC-15 | Excluir el decreto y la superficie de la ficha bajo el mapa | 18 sep 2026 | Información innecesaria para quien denuncia |
| DEC-16 | No desplegar las zonas sobre el mapa; dibujar únicamente el polígono en el que cae el punto | 18 sep 2026 | Mantener el mapa legible y dirigir la atención al resultado del cruce |
| DEC-17 | Recortar el mapa base al contorno de la Ciudad de México y acotar el desplazamiento | 18 sep 2026 | Evitar que el punto se coloque fuera del ámbito de competencia y centrar la atención en el territorio de la Ciudad |
| DEC-18 | Suprimir la leyenda del mapa y expresar el resultado del cruce en la ficha, desagregado en tipo de zona y categoría | 18 sep 2026 | La ficha es el lugar donde se lee el resultado; la leyenda duplicaba información sin nombrar la categoría |
| DEC-19 | Diferir el módulo de administración y seguimiento hasta que el formulario de denuncia esté validado | 18 sep 2026 | El modelo de datos del formulario determina la bandeja, las consultas y los indicadores; construirlo antes obligaría a rehacerlo |
| DEC-20 | Impedir el envío cuando el punto cae fuera de los límites de la Ciudad de México | 18 sep 2026 | La Secretaría carece de competencia sobre hechos ocurridos fuera de la Ciudad; admitir el envío generaría expediente improcedente y expectativa de atención |
| DEC-21 | Ampliar el catálogo de materias de diez a catorce y agruparlas en cuatro bloques temáticos | 18 sep 2026 | La revisión contra la Ley Ambiental vigente mostró cuatro supuestos de competencia local que el canal actual no ofrece: quema a cielo abierto, vehículo ostensiblemente contaminante, irregularidades en verificentros y daño a áreas verdes |
| DEC-22 | Rediseñar la primera pantalla: elegir el supuesto avanza al paso siguiente, sin botón de continuar | 18 sep 2026 | Con veintiún opciones y el botón al final, la pantalla obligaba a recorrerla entera para poder avanzar; es la causa previsible de abandono |
| DEC-23 | Abrir un bloque propio de zonas de protección con seis supuestos | 18 sep 2026 | Las conductas características del suelo de conservación —asentamiento irregular, tala, afectación de cuerpos de agua, agroquímicos— no tenían dónde entrar; el catálogo sólo las cubría de forma indirecta |
| DEC-24 | Reconstruir la obligatoriedad sobre una sola tabla, con dos esquemas conmutables desde el panel | 18 sep 2026 | La obligatoriedad estaba repartida en veinte lugares del código; ahora una tabla gobierna la pantalla, la validación y el documento de mapeo |
| DEC-25 | Preguntar a quién se denuncia: persona, empresa, autoridad de gobierno o desconocido | 18 sep 2026 | Tomado del formulario de la EPA. Cuando se señala a una autoridad, el art. 331 de la Ley Ambiental manda emitir recomendaciones en lugar de sancionar, de modo que el dato cambia la ruta del expediente y lo que el acuse promete |
| DEC-26 | Conservar las dos preguntas —establecimiento y responsable— diferenciando su enunciado y heredando la respuesta del paso 2 al paso 3 | 18 sep 2026 | Leídas en secuencia, «¿Ocurre en un establecimiento?» y «¿A quién denuncias? · Una empresa o negocio» parecían la misma pregunta. No lo son: la primera ubica el sitio para la visita de inspección, la segunda identifica al sujeto y define la vía del procedimiento; divergen en los casos frecuentes de obra pública y de hechos en vía pública atribuibles a una empresa. Suprimir una de las dos perdería información operativa; la duplicación percibida se corrigió reencuadrando ambos enunciados y eliminando la doble captura |
| DEC-27 | Resolver el acceso al sistema con **Llave CDMX**, tanto para la ciudadanía como para el personal que atiende las denuncias: con la misma cuenta se presenta la denuncia y se consulta el estatus del trámite | 18 sep 2026 | Es la identidad digital con la que la Ciudad opera sus trámites en línea: evita construir un padrón propio de usuarios, prellena los datos de identificación, da certeza sobre quién presenta la denuncia y vincula el folio a una cuenta, que es lo que hace posible el seguimiento sin claves adicionales. En el caso del personal sustituye las cuentas nominales previstas en AD-01 |
| DEC-28 | Ante un hecho iniciado hace más de un año, advertir y pedir que se indique desde cuándo se tuvo conocimiento, sin impedir el envío | 18 sep 2026 | El art. 22 BIS 2 de la Ley Orgánica de la Procuraduría computa el plazo desde el inicio de los hechos o desde su conocimiento; en hechos continuos o permanentes —la mayoría de las denuncias ambientales— corre desde el conocimiento. El prototipo muestra el aviso según la temporalidad declarada |
| DEC-29 | Incorporar el campo de gestiones previas ante otras autoridades, con carácter opcional, en el paso de hechos | 18 sep 2026 | Lo pide el art. 22 BIS 1, fracc. II, de la Ley Orgánica de la Procuraduría y tiene valor operativo: distingue a quien ya acudió a la alcaldía sin obtener respuesta, lo que suele indicar reincidencia o mayor gravedad |
| DEC-30 | Nombrar como autoridad competente a la **dirección general** y no a la coordinación, con fundamento verificado en el Reglamento Interior del Poder Ejecutivo | 18 sep 2026 | El art. 191, fracc. III, acota a la DGIVA a suelo urbano y Áreas de Valor Ambiental, y el art. 188, fracc. XXXIX a XLI, faculta a la DGCORENADR en suelo de conservación y Áreas Naturales Protegidas, donde además la fracc. XXXVIII le atribuye recibir denuncias ciudadanas. La coordinación que la atiende no figura en el Reglamento Interior —sus atribuciones constan en el Manual Administrativo, ya integrado, y su nombre es Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas (DEC-84)—: mientras su atribución no se verifique en el Manual Administrativo, el acto de turnado debe dirigirse a la unidad que sí tiene facultad reglamentaria |
| DEC-31 | Fijar convenciones de código y regla contra el código zombi desde la maqueta, documentadas en `11-ruta-de-trabajo.md` | 18 sep 2026 | La maqueta no es un borrador desechable: es la especificación ejecutable del sistema y su código se hereda. Una sola fuente de verdad por concepto, nada declarado dos veces, y auditoría de código muerto al cerrar cada bloque de cambios, con bitácora de lo eliminado |
| DEC-32 | No abrir ningún módulo complementario antes del acta de validación del formulario ciudadano por la Dirección General | 18 sep 2026 | Un cambio de campo después de programar base de datos, bandeja e indicadores cuesta entre diez y veinte veces lo que cuesta en la maqueta. El orden de fases y sus criterios de salida quedan en `11-ruta-de-trabajo.md` |
| DEC-33 | Titularidad del desarrollo: **Sistema de Información Ambiental de la Secretaría del Medio Ambiente de la Ciudad de México** | 18 sep 2026 | Resuelve la brecha B-02 de la norma de construcción. Define de quién es el código y en qué área vive el proyecto, condición previa para decidir la cuenta institucional del repositorio y de la infraestructura |
| DEC-34 | Poner el proyecto bajo control de versiones con git, en la propia carpeta del proyecto | 18 sep 2026 | Resuelve la brecha B-01. Antes no había historia comparable ni respaldo fuera del equipo, y la auditoría de repositorio no podía correrse. Se versiona el trabajo propio —documentación, prototipo, capas e insumos fundacionales— y se excluyen la normativa de referencia (26 MB de documentos públicos re-descargables), las copias de `prototipo/historial/` —porque la historia ahora la lleva git— y las carpetas `_to_delete/`. Cada exclusión queda razonada en el propio `.gitignore` |
| DEC-35 | Declarar en el catálogo de campos, para cada uno, su **uso**, si es **dato personal** y a qué **finalidad** sirve | 18 sep 2026 | Resuelve la brecha B-05. La obligatoriedad y el uso son cosas distintas y sólo estaba declarada la primera. El uso vive en la misma estructura `OBLIG` que gobierna pantalla y validación, de modo que no puede quedar desactualizado, y es el insumo con el que la Unidad de Transparencia redacta el aviso de privacidad (P-02). Resultado: 47 campos, 20 datos personales, seis finalidades, **cero campos sin uso** |
| DEC-36 | Adoptar el mapa base de **CARTO** con clave propia, y sacar del código la dirección del proveedor y la clave hacia un archivo de configuración local no versionado | 18 sep 2026 | Resuelve la mitad de B-10: el prototipo consumía los mosaicos de OpenStreetMap directamente, cuyo servicio no está abierto al uso institucional de producción. La capa gratuita de CARTO admite cinco millones de peticiones de mosaico al mes y obliga a acreditar a CARTO y a OpenStreetMap en cada mapa. La clave **no puede vivir en el código**: el repositorio es público y una credencial escrita ahí queda indexada en horas. Queda en `prototipo/configuracion-local.js`, excluido del repositorio, y el prototipo cae al proveedor sin clave si el archivo no existe. Es la regla de cero valores fijos, y el mismo mecanismo que en la versión funcional será una variable de entorno |
| DEC-37 | Capturar primero la dirección —calle, número, alcaldía, colonia, código postal— y proponer el punto en el mapa a partir de ella, dejando que la persona lo mueva | 18 sep 2026 | Es como la gente piensa el lugar de los hechos. **Invierte la dependencia** que se había fijado —alcaldía, colonia y código postal derivados del mapa— pero no la regla de fondo: el cruce que determina la competencia se resuelve sobre la coordenada (DEC-04). Cuando la alcaldía del punto difiere de la elegida, manda la del punto y se avisa, en lugar de cambiarla en silencio. La geocodificación inversa deja de sobrescribir lo que la persona escribió: sólo rellena lo vacío |
| DEC-38 | Retirar el domicilio de la empresa denunciada, y anteponer una pregunta de sí o no a los campos de permisos y de gestiones previas | 18 sep 2026 | Aplicación del criterio de minimización (DEC-35): el domicilio fiscal rara vez lo conoce quien denuncia y la razón social más el sitio bastan para el emplazamiento. Los dos campos de texto largo quedan tras una pregunta filtro: sólo los ve quien tiene algo que aportar, y la respuesta de sí o no ya informa por sí misma |
| DEC-39 | Cambiar el entorno de trabajo a **Claude Code** al iniciar la fase 2, conservando aquí la validación y los documentos | 19 sep 2026 | La app de escritorio es la herramienta correcta mientras el proyecto es un archivo y unos documentos: se revisan capturas, se leen leyes en PDF, se publica el artefacto de validación y se comparte todo sin instalar nada. De la fase 2 en adelante el trabajo es código en muchos archivos, migraciones y uso continuo del repositorio, y esta sesión ya topó con los tres límites que eso implica: no puede hacer `push` —no hay credenciales de git—, no alcanza servicios externos para verificarlos, y cada prueba exige subir y bajar el archivo. El repositorio creado el 18 de septiembre es el punto de encuentro entre los dos entornos. **Recordatorio anotado al inicio de la fase 2 en `11-ruta-de-trabajo.md`** |
| DEC-40 | Retirar definitivamente la variante **A — identificación obligatoria** del panel de validación | 19 sep 2026 | La denuncia anónima quedó admitida desde DEC-03 y el artículo 280 de la Ley Ambiental permite a la Secretaría instaurar el procedimiento de inspección con la información recabada, sin ratificación. Mantener como variante viva un criterio ya descartado abre de nuevo una discusión cerrada en cada sesión de validación |
| DEC-41 | El punto del mapa **no escribe en la dirección**: el flujo va en un solo sentido | 19 sep 2026 | La dirección la captura la persona y es su dato; el punto se propone a partir de ella. Que el marcador reescribiera lo capturado al moverse es la fuente de confusión que este diseño evita. Se retiró la geocodificación inversa, que además era una llamada más a un servicio externo. La alcaldía que arroja la capa oficial se guarda aparte, se muestra en la ficha como **Alcaldía del punto** y, cuando difiere de la capturada, se ofrece corregirla con un botón: **quien decide es la persona, no el sistema** |
| DEC-42 | Barra de progreso navegable: cada etapa es un botón | 19 sep 2026 | Permite volver a un paso anterior sin recorrer todos y revisar lo capturado durante la sesión de validación. Usa **las mismas reglas que el botón Continuar**, no una segunda puerta con criterios propios: retroceder es libre, avanzar valida cada paso intermedio y se detiene en el primero que falle mostrando ahí sus errores, y la regla de competencia territorial se aplica siempre, también en modo de prueba |
| DEC-43 | Fijar arriba la barra de avance y el recordatorio de qué se está denunciando | 19 sep 2026 | El formulario es largo y ambos quedaban fuera de la vista al primer desplazamiento: la persona perdía de vista en qué paso va y qué supuesto eligió, que es justo lo que da sentido a lo que se le pregunta. En pantalla estrecha el recordatorio se reduce a una línea para no comerse la pantalla: ocupa el 14 % en un teléfono de 760 px de alto |
| DEC-44 | Plegar los datos accesorios del lugar tras «Añadir más datos del lugar» | 19 sep 2026 | El paso 2 contenía cuatro cosas distintas —dirección, mapa, referencias adicionales e identificación del establecimiento— y ocupaba casi cinco pantallas de teléfono para responder «¿dónde?». Sólo la dirección y el mapa quedan a la vista; lo demás se abre a petición. Medido contra la línea base del documento 13, en teléfono de 390 × 760 px: **el paso baja de 3 609 a 2 163 px —de 4.7 a 2.8 pantallas—, de 513 a 282 palabras y de diez a cinco campos a la vista**, sin retirar un solo dato del esquema. Ningún campo obligatorio puede quedar escondido: si alguno de los plegados llegara a serlo y faltara, `valida()` despliega el bloque antes de mostrar el error (M-03) |
| DEC-45 | Ofrecer la ubicación del dispositivo con el encuadre «Los hechos ocurren donde estoy ahora» | 19 sep 2026 | **Reabre DEC-13 sin contradecirla.** Aquella retiró el botón de «ubicarme» porque el lugar de los hechos rara vez coincide con dónde está quien denuncia; sigue siendo cierto. Pero hay un caso muy frecuente en que sí coincide: la persona parada frente al problema. Se ofrece con ese encuadre exacto, como opción secundaria, **nunca automática**, y sólo propone el punto: la dirección capturada no se toca, conforme a DEC-41 (M-04) |
| DEC-46 | La palabra «opcional» se retira de los campos que viven dentro de un bloque plegado | 19 sep 2026 | Aparecía veintiocho veces en el recorrido. Cuando casi todo es opcional la palabra deja de significar algo y el formulario **parece más largo de lo que es**. El encabezado del bloque lo dice una sola vez —«todo esto es opcional»— y dentro no se repite campo por campo. Así la palabra conserva su valor donde sí distingue: entre campos visibles de un mismo bloque (M-07) |
| DEC-47 | El lugar de los hechos se captura por una de dos rutas, según tenga domicilio o no | 19 sep 2026 | **Corrige un defecto, no añade una mejora.** El formulario exigía calle, colonia y código postal, datos que no existen en bosques, áreas naturales protegidas, barrancas, caminos, canales ni suelo de conservación. Comprobado: una denuncia por tala dentro del Bosque de Tlalpan **no podía presentarse** —el sistema identificaba correctamente el ANP, la alcaldía y que correspondía a la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural, y acto seguido bloqueaba el paso—. El formulario servía bien a la mitad urbana de lo que la Secretaría atiende. Una pregunta de sí o no encamina el paso: con domicilio, la dirección va primero y propone el punto; sin domicilio, el punto va primero y **el nombre del sitio se propone desde la capa oficial que lo contiene**, igual que la alcaldía, y se ofrece —no se impone— conforme a DEC-41 |
| DEC-48 | La obligatoriedad condicional se declara en `OBLIG`, no en `valida()` | 19 sep 2026 | Un campo puede ser obligatorio en una ruta y no aplicar en otra. Esas condiciones vivían sueltas en la función de validación, de modo que el documento 09 —que se genera de `OBLIG`— afirmaba que el domicilio de notificación era obligatorio siempre, cuando sólo se pide a quien rechaza la notificación electrónica. **El documento que sustenta la minimización ante la Unidad de Transparencia no puede decir algo distinto de lo que el formulario hace.** Diecisiete campos declaran hoy su condición, con un texto legible que el documento 09 publica en una columna propia. `valida()` quedó reducida a comprobar presencia, que es su único asunto |
| DEC-49 | La pregunta del establecimiento se hace en el paso 3, junto a quién responde | 19 sep 2026 | Vivía al final del paso 2, entre los datos del lugar, y obligaba a mantener una función —`avisoHeredado()`— cuyo único trabajo era explicar en el paso 3 lo que se había contestado en el 2. **Cuando hace falta un puente así, la pregunta está en el lugar equivocado.** No es un detalle del lugar: es la primera pregunta sobre quién responde por los hechos, y propone la respuesta a la siguiente. Preguntada donde se usa, el aviso puente desapareció y con él la redundancia con «¿a quién denuncias?» que estaba anotada desde la revisión heurística |
| DEC-50 | Tres rutas de identificación, y la elección al final del formulario | 19 sep 2026 | **Anónima**, **datos escritos** y **cuenta Llave CDMX**. La tercera no es un adorno de la segunda: escribir el nombre a mano identifica a efectos de contacto pero no acredita a nadie, y **la reserva de identidad frente a la persona denunciada sólo tiene sentido si hay identidad**. La elección se pide en el paso 5 y no en la primera pantalla: antes de saber qué se le va a preguntar nadie decide con criterio cuánto quiere exponerse, y un muro de autenticación en la primera pantalla pierde la denuncia entera, porque todavía no hay nada capturado. Al final, si la cuenta falla o la persona no la tiene, la denuncia ya existe. Además, así el formulario puede operar sin la integración y esperarla, en vez de depender de ella para salir (P-15) |
| DEC-51 | Los datos accesorios del lugar van **arriba del mapa y sin plegar** | 19 sep 2026 | **Modifica DEC-44 en parte y conserva DEC-46.** Son datos de la dirección: dejarlos debajo del mapa partía en dos el bloque de dirección, con el mapa en medio, y obligaba a volver atrás mentalmente. Sobre el plegado, lo que cambió es el tamaño: al fundirse los dos campos de referencias en uno (DEC-47), el bloque bajó de siete campos a tres, y a ese tamaño esconderlos cuesta más de lo que ahorra —quien tiene el dato no encuentra dónde ponerlo—. Se conserva lo que sigue valiendo de DEC-44: la palabra «opcional» se dice **una vez en el encabezado del bloque** y no campo por campo. Medido: el paso pasa de 2 163 a 2 864 px, de 2.8 a 3.8 pantallas, todavía por debajo de los 3 609 px de partida. Desaparece la clave `mas_lugar` y la red de `valida()` que desplegaba el bloque, que sin nada plegado sería código muerto |
| DEC-52 | El envío al repositorio remoto se hace a mano; los commits, no | 20 sep 2026 | Los commits se generan de forma automática al cerrar cada bloque de trabajo, con su mensaje y su verificación. El **envío** queda a cargo de la persona, desde GitHub Desktop. Automatizarlo exigiría guardar un token de GitHub en texto plano **dentro de una carpeta sincronizada a OneDrive**, en el mismo árbol donde cada commit ejecuta `git add -A`: es la misma vía por la que un documento de trabajo acabó publicado y obligó a borrar y rehacer el repositorio. El beneficio —ahorrar un clic dos o tres veces por sesión— no compensa. **Se revisa si se programa alguna tarea automática que deba actualizar el repositorio sin nadie presente**; en ese caso, token de alcance fino, limitado a ese repositorio, con permiso de contenido y fecha de caducidad |
| DEC-53 | Rehacer la pantalla de inicio: la promesa arriba, el botón enseguida, la explicación debajo | 20 sep 2026 | Tenía **232 palabras en cuatro cajas de aviso idénticas**, sin jerarquía entre lo importante y lo accesorio, y el botón de empezar quedaba a **1 268 px: casi dos pantallas de desplazamiento antes de poder hacer nada**. Además repetía el título y la bajada que ya están en el encabezado institucional de la página, que es la mitad de la sensación de exceso de texto: lo mismo dicho dos veces seguidas. Ahora abre con tres datos —sin tu nombre, diez minutos, con folio—, el botón enseguida, y debajo qué pasa después en cuatro pasos numerados y qué tener a la mano en tres etiquetas. Medido: **de 232 a 123 palabras, de 1 162 a 880 px, y el botón de 1 268 a 411 px**, visible sin desplazar en teléfono y en escritorio |
| DEC-54 | El aviso de denuncia sin terminar se acorta, pero conserva que **aún no se ha presentado** | 20 sep 2026 | Decía el supuesto elegido y que se había guardado en el navegador: ruido para quien sólo quiere seguir o descartar. De todo eso se conserva una frase, y no por brevedad sino porque sin ella **alguien puede cerrar el navegador creyendo que ya denunció**. De 36 a 22 palabras. Una prueba automatizada fija que esa frase no pueda perderse en una limpieza futura |
| DEC-55 | Barra de pasos con círculos enlazados, y el guinda acotado a la identidad y a la acción principal | 20 sep 2026 | **Dos cosas.** La primera: la barra era un filete de avance con seis etiquetas; ahora es un círculo por paso —palomita en los hechos, círculo relleno en el actual, número en los pendientes— unidos por una línea que se pinta conforme se avanza. **El estado no se confía al color**: la palomita y el número lo dicen igual, de modo que sirve también a quien no distingue verde de gris. La segunda: **cincuenta reglas de estilo usaban guinda**, y el resultado era que nada destacaba porque todo destacaba. Quedan diecinueve. El guinda se reserva a la identidad —barra de gobierno, encabezado, pie—, al título de cada paso y al botón de acción principal: **uno por pantalla**. Lo que se toca y lo que quedó elegido pasa a azul `#1A56A8`; el avance, a verde; la estructura, a tipografía y neutros. El recordatorio de materia, que va fijo en todas las pantallas, pierde el fondo guinda y conserva un filete dorado, que es el uso para el que ese color está declarado |
| DEC-56 | Los datos accesorios del lugar dejan de ser un bloque aparte | 20 sep 2026 | Son el final de la dirección, no una sección con encabezado propio. Se retiran el título «Más datos del lugar» y la línea que lo explicaba, y los tres campos siguen a la colonia y el código postal sin caja que los envuelva. **Aquí «opcional» vuelve a marcarse campo por campo, y es correcto**: entre campos visibles de un mismo bloque la palabra sí distingue —la calle se pide, las entre calles no—, que es justo el caso que DEC-46 reservaba para ella. Desaparecen las tres clases de estilo del bloque, que quedarían sin uso |
| DEC-57 | La portada recupera un texto de presentación, y el aviso de borrador baja de jerarquía | 20 sep 2026 | **Corrige DEC-53 en parte.** Al quitar las 232 palabras se fue también lo que presentaba el trámite, y la pantalla quedó abrupta: tres tarjetas y un botón, sin decir para qué sirve nada de eso. Vuelve un párrafo de dos frases —qué puede hacer la Secretaría y qué necesita para hacerlo— antes de los tres datos, y el botón conserva su peso inmediatamente después. Sigue habiendo tope: 172 palabras frente a las 232 de origen, y el botón queda a 573 px en teléfono y 472 en escritorio, visible sin desplazar en ambos. Aparte, el aviso de denuncia sin terminar **pesaba casi lo mismo que el botón de empezar**: era una caja con relleno y un botón guinda. Pasa a una tira con filete dorado, botón secundario y un enlace para descartar; medido, ocupa el 19 % del área del botón principal en escritorio |
| DEC-58 | «Qué pasa después» se dibuja en horizontal, como una secuencia | 20 sep 2026 | Cuatro frases apiladas se leen como una lista; cuatro columnas unidas por una línea se leen como lo que son, una secuencia en el tiempo. Usa **la misma gramática visual que la barra de pasos** —círculo numerado y línea— de modo que el formulario dice «esto son pasos» de una sola manera. En pantalla estrecha van dos por renglón y sin línea, que no tendría a dónde ir. La nota de plazos por confirmar sale de la columna y va debajo, donde cabe |
| DEC-59 | El aviso de denuncia sin terminar sale del formulario y pasa a una franja de sistema | 20 sep 2026 | Es información sobre el sitio —hay algo guardado en este navegador—, no una pregunta del cuestionario, y dentro de la tarjeta tomaba un peso que no le toca. Va entre el encabezado y la tarjeta, a todo lo ancho, y **sólo en la pantalla de inicio**: dentro del formulario el borrador ya está cargado y el aviso no diría nada. **Se descartó la ventana nativa del navegador** que se propuso: `confirm()` bloquea la página hasta que se responde, de modo que no se puede mirar nada para decidir; aparece encabezada con «La página en … dice», que es el formato que la gente cierra por reflejo; no admite formato, así que no lleva identidad institucional; y algunos navegadores suprimen esos diálogos al cargar, en cuyo caso **el borrador quedaría irrecuperable sin aviso alguno** |
| DEC-60 | En el paso 2, nada aparece hasta contestar si el lugar tiene domicilio | 20 sep 2026 | Esa pregunta decide la forma de todo lo demás. Si se muestra junto con el resto, se contesta de paso sin leerla y la persona puede acabar en la ruta equivocada —que es justamente el defecto que DEC-47 vino a corregir—. Sola en pantalla se lee. Mientras no se contesta tampoco hay botón de Continuar: no habría nada que continuar |
| DEC-61 | Se marca lo obligatorio con asterisco, en vez de rotular lo opcional | 20 sep 2026 | La palabra aparecía hasta veintiocho veces en el recorrido, y como casi todo era opcional dejaba de significar algo y **hacía el formulario más largo de lo que es**. Invertida la marca, lo que lleva señal es lo poco que se exige. **El asterisco por sí solo no es accesible**, así que lo acompaña la palabra «obligatorio» en texto visible sólo para lectores de pantalla, y la leyenda del panel lo explica. Medido en el paso 2: de nueve apariciones de «opcional» a **cero**, con cinco asteriscos |
| DEC-62 | Limpieza de textos de ayuda, y el marcador dentro del campo en vez de instrucciones alrededor | 20 sep 2026 | Se retiran siete ayudas que no aportaban: un ejemplo de calle, un aviso sobre algo que el formulario ya dice cuando ocurre, dos frases que explicaban lo que el propio campo enseña al usarlo. **El título de la descripción daba por hecho que los hechos siguen ocurriendo** —«Describe lo que está ocurriendo»— cuando una denuncia puede ser de ayer o de hace dos meses: pasa a «Cuenta qué pasó o qué está pasando». Lo que de verdad orienta —qué se hace, quién, en qué horario, con qué frecuencia y con qué efecto— **deja de ser una caja de aviso debajo y pasa a ser el marcador dentro del propio campo**, donde se lee justo cuando hace falta y desaparece al escribir. **Revierte M-05**: el ejemplo por supuesto se retira, y con él la función y los dieciocho textos, que si no quedarían sin uso. Los subtítulos de sección vuelven al guinda: h2 grande para el paso y h3 menor para la sección es jerarquía de tipografía y color a la vez, no repetición |
| DEC-63 | Los nombres de establecimiento se piden con ejemplos, no por dónde aparecen | 20 sep 2026 | «Como aparece en el anuncio o la fachada» **supone que el sitio tiene anuncio**, y muchos no lo tienen: una escuela, una bodega, un predio en obra. Y «nombre comercial» excluye a lo que no es comercio. Pasa a **«Nombre del establecimiento»**, con ejemplos que abarcan los dos casos: Taller Automotriz Hernández, Escuela Primaria Benito Juárez, Bodega La Central. El campo equivalente del bloque de responsable recibe el mismo trato |
| DEC-64 | Escala de jerarquía visual: cada nivel se distingue del contiguo por al menos dos rasgos | 20 sep 2026 | **Corrige dos defectos medidos, no una impresión.** El título del paso y el de sección eran tipográficamente **idénticos** —20 px, Cabin 600, guinda—, distinguibles sólo por el círculo del número. Y **la respuesta se veía más grande que la pregunta**: 16 px el control contra 14 px la etiqueta, que es la jerarquía al revés. La escala queda: paso 24 px Cabin 700 guinda con número en círculo; sección 20 px Cabin 600 guinda con filete dorado encima; subsección 13 px en mayúsculas espaciadas, gris, con filete inferior; pregunta 16 px Roboto 600; respuesta 16 px Roboto 400 dentro de un control con borde; ayuda 13 px gris. **La regla, y no la tabla, es lo que se comprueba**: una prueba mide los seis niveles y exige dos rasgos de diferencia entre contiguos y que ninguna respuesta se vea mayor que su pregunta |
| DEC-65 | La portada pierde las tres tarjetas de datos, y las cosas que tener a la mano dejan de parecer botones | 20 sep 2026 | Las tarjetas —sin tu nombre, diez minutos, con folio— se retiran a petición expresa. **Con ellas se va de la primera pantalla el aviso de que se puede denunciar sin dar el nombre**, que era M-01: la opción sigue existiendo, pero ya no se anuncia antes de empezar. Las etiquetas de «Ten a la mano» tenían borde redondeado y fondo blanco, es decir, el aspecto de los controles del formulario: pasan a lista con viñeta dorada, que es lo que son |
| DEC-66 | El pie nombra las dos formas de presentar la denuncia y las dos áreas que la atienden | 20 sep 2026 | Decía «presentar la denuncia en persona» y dejaba el correo en un bloque aparte llamado «contacto», como si sólo hubiera una vía. Ahora las dos aparecen juntas, con el correo primero. Y se nombran las dos áreas que atienden según el tipo de suelo. **Conforme a DEC-30 se nombra a la dirección general y no a la coordinación**: la Coordinación de Inspección y Vigilancia Ambiental no figura en el Reglamento Interior y su atribución sigue por verificar en el Manual Administrativo (P-10), de modo que aparece como el área a través de la cual atiende su dirección general, no como autoridad por sí misma |
| DEC-67 | Se retira por completo la detección de ubicación del dispositivo | 20 sep 2026 | **Revierte DEC-45.** El formulario deja de pedir ese permiso al navegador y de tocar esa interfaz: cero menciones a la API de geolocalización en el código. Un permiso de ubicación en un formulario de denuncia es, para quien denuncia, exactamente la clase de petición que da motivo a desconfiar, y el beneficio —ahorrar un clic a quien está parado frente al problema— no lo compensa. Lo sustituye DEC-69 |
| DEC-68 | El tamaño de los botones de sí y no depende del tipo de puntero, no del ancho de pantalla | 20 sep 2026 | Medían 48 px de alto en todas partes porque ésa es la regla del **blanco táctil**: un pulgar necesita esa superficie, un ratón no. Aplicada por ancho de pantalla, la regla agrandaba los controles en escritorio sin motivo. Se condiciona a `pointer: coarse`, que es lo que la regla mide de verdad: 40 px con ratón, 48 con el dedo |
| DEC-69 | Se admiten coordenadas y enlaces de Google Maps, leídos en el navegador | 20 sep 2026 | Sustituye a la detección de ubicación. La persona pega lo que ya tiene —las coordenadas, o el enlace del mapa donde dejó el pin— y el punto se coloca. **El enlace se lee aquí, con una expresión regular sobre el texto: el sistema no lo abre ni consulta nada fuera**, comprobado por prueba que vigila que no se genere ninguna petición de red. Se reconocen las tres formas en que ese servicio escribe la coordenada en la dirección web. Los enlaces cortos no la llevan dentro, así que no hay nada que leer: se pide el enlace completo en vez de resolverlo por fuera, que es justo lo que se quiso evitar |
| DEC-70 | El punto del mapa debe confirmarse, y cualquier movimiento borra la confirmación | 20 sep 2026 | El punto se arrastra, y **un roce basta para moverlo unas calles**; de esa coordenada depende el área que atiende la denuncia y el tipo de suelo que se invoca. Se pide confirmarlo con una casilla que aparece bajo el resultado del cruce —justo debajo de lo que ese punto determinó— y **cualquier colocación o arrastre posterior la borra**: si sobreviviera al movimiento, pedirla no serviría de nada. La regla hubo que escribirla **dos veces**, porque el mapa vectorial del artefacto sobrescribe `ponMarcador`; es la segunda regla del LEEME de la carpeta de construcción, y esta vez se aplicó antes de que fallara |
| DEC-71 | Retroceder deja de ser un botón con borde y pasa a enlace con flecha | 20 sep 2026 | **Retroceder es navegación, no una respuesta.** Con borde pesaba lo mismo que los botones de sí y no, y competía con ellos por la atención justo donde había que leer una pregunta. Pasa a «‹ Regresar», sin borde ni relleno. Queda así una sola acción con relleno de color por pantalla —continuar—, una con borde —responder— y una sin nada —retroceder—. El blanco táctil de 44 px se conserva por relleno interior, no por caja visible. Se comprueba la regla: una prueba mide que retroceder no lleve borde ni relleno, que responder lleve borde y fondo neutro, y que avanzar sea lo único con color |
| DEC-72 | **La alcaldía deja de preguntarse: la determina el punto** | 20 sep 2026 | **Corrige un defecto que llegaba al expediente.** La alcaldía existía dos veces —la escrita y la calculada por el cruce—, el turnado usaba la del punto, el acuse mostraba la escrita, **y el formulario no exigía que coincidieran**. Comprobado: capturando una dirección en Coyoacán y el punto dentro del Bosque de Tlalpan, la denuncia se enviaba diciendo «Av. México 10, Del Carmen, C.P. 04100, Coyoacán» y, en el mismo resumen, «Área Natural Protegida local — Bosque de Tlalpan», turnada a la DGCORENADR. Ahora hay una sola alcaldía y la pone el punto: **el mismo dato con el que se resuelve el turnado**, de modo que acuse y expediente no pueden contradecirse. Además reconoce algo cierto: los límites de alcaldía no se conocen con precisión —Coyoacán con Benito Juárez, Tlalpan con Xochimilco—, así que se estaba pidiendo un dato que el sistema determina mejor. Desaparecen el selector, la clave `alcaldia_punto`, la función `usaAlcaldiaDelPunto()`, el aviso de discrepancia y el catálogo `ALCALDIAS`, que quedó sin quien lo usara |
| DEC-73 | Cada bloque del paso 2 declara para qué sirve | 20 sep 2026 | El paso pedía dos trabajos distintos —describir el lugar con palabras y señalarlo en un mapa— sin decir cuál servía para qué, de modo que mover el punto parecía corregir la dirección y escribirla parecía mover el punto. Ahora lo dice una vez arriba y una vez en cada bloque: **la dirección es para que el personal de inspección llegue; el punto decide qué área atiende la denuncia** |
| DEC-74 | Las tres vías de marcar el sitio van juntas, y «Quitar el punto» desaparece | 20 sep 2026 | Había cuatro maneras de colocar el punto repartidas por la pantalla, y el subtítulo describía sólo una. Las tres que dependen de la persona —buscar la dirección escrita, pegar coordenadas o un enlace, o dar clic en el mapa— se enuncian juntas y con el mismo peso, en una lista. «Ubicar en el mapa» pasa a secundario: **una sola acción con relleno de color por pantalla** (DEC-71). Y se retira «Quitar el punto»: el punto es obligatorio, de modo que **su único destino era un mensaje de error**; para moverlo se arrastra o se da otro clic |
| DEC-75 | La confirmación del punto vive en su propio contenedor, junto a los botones | 20 sep 2026 | Estaba dentro de la ficha del cruce, arriba: si un arrastre la borraba —que es justo el descuido que previene—, se destildaba fuera del campo de visión y el error aparecía al pulsar Continuar, abajo. Ahora va inmediatamente antes de los botones y **dice qué se está confirmando** —alcaldía y área identificada—, que se actualiza al mover el punto. Tiene contenedor propio porque el punto cambia sin rehacer la pantalla: rehacerla reiniciaría el mapa y perdería el encuadre. **Defecto propio detectado al probar:** la primera versión dejó dos casillas con el mismo identificador, la vieja dentro de la ficha y la nueva arriba de los botones |
| DEC-76 | La portada enuncia un derecho, no un trámite | 20 sep 2026 | Decía, en tres renglones, lo que la Secretaría puede hacer. Ahora empieza por lo que **la persona** puede hacer, y responde en orden las tres preguntas de quien nunca ha denunciado: qué me reconoce la ley, para qué sirve denunciar, qué pasa después. Cuatro enunciados con palomita sustituyen a las cuatro cajas idénticas que se retiraron en DEC-53, y el párrafo de «por qué importa» dice lo que ninguna otra pantalla dice: que la Ciudad no tiene personal en cada calle y que buena parte del daño ambiental sólo se conoce porque alguien lo reportó. El tope de palabras sube de 180 a 340 y **sigue habiendo tope**: el botón de empezar tiene que verse sin desplazar, y se comprueba a 390 px |
| DEC-77 | Vuelve a la portada la promesa de denunciar sin dar el nombre (M-01) | 20 sep 2026 | Al retirar las tarjetas de datos en DEC-53 se fue con ellas la única mención del anonimato en la primera pantalla, que era justo el motivo de la mejora aprobada. Regresa como uno de los cuatro enunciados de lo que la ley reconoce, con su consecuencia dicha en la misma línea: sin datos no hay aviso del resultado ni aclaración posible |
| DEC-78 | Se preguntan género y rango de edad, con fines estadísticos y en las dos rutas | 20 sep 2026 | Van al final del paso 5, fuera del bloque de contacto, porque **no identifican a nadie y no entran al expediente**: por eso se piden también en la ruta anónima, que es donde se perdería la mitad del universo. En desplegable y no en botones, para que se lean como lo que son. Ambas admiten «Prefiero no decirlo», que no es cortesía: **la identidad de género es dato sensible** y sólo puede tratarse con consentimiento expreso. Quedan declaradas en OBLIG con finalidad «Estadística», de modo que el documento 09 dice qué se pide, para qué y con qué carácter |
| DEC-79 | El aviso de privacidad se lee en pantalla antes de enviar | 20 sep 2026 | Estaba detrás de un enlace que abría una ventana del navegador con un texto provisional. Ahora es un bloque de seis rótulos —quién trata tus datos, para qué, con qué fundamento, cuánto se conservan, a quién se transfieren, cómo ejerces tus derechos— colocado inmediatamente antes de la casilla con la que se consiente, como lo hace la PAOT en su formulario. **Lo que no está verificado queda a la vista como hueco**: el nombre del sistema de datos personales, el ciclo de vida, el catálogo de transferencias y los datos de la Unidad de Transparencia (P-19) |
| DEC-80 | El relato tiene que parecer un texto escrito por una persona | 20 sep 2026 | En el formulario de la PAOT se puede enviar una denuncia con todos los campos llenos de letras al azar; se comprobó. El formulario mide tres señales del relato —cuántas palabras tiene, qué proporción de vocales y si hay caracteres repetidos— y no deja avanzar cuando ninguna se cumple. **No juzga el contenido ni castiga a quien escribe mal**: un relato con faltas de ortografía pasa, y así está probado. El mensaje deja de ser «este dato es necesario» y dice cuál es el problema. Esto ayuda a quien escribe de buena fe; **a quien no la tiene lo detiene el servidor, no el navegador** (documento 15) |
| DEC-81 | El acuse explica la ratificación que aquí no hace falta | 20 sep 2026 | Ante la Procuraduría, la denuncia electrónica debe ratificarse en tres días hábiles o se tiene por no presentada. Quien ha denunciado antes lo espera, y su ausencia se lee como omisión. El acuse lo dice y lo contrasta con esta vía, que no lo exige, y ofrece la remisión a la Procuraduría para quien quiera la denuncia formal con respuesta obligada. Se toma también del acuse de la PAOT el aviso de revisar la carpeta de correo no deseado |
| DEC-82 | El formulario acepta códigos plus, y el enlace corto deja de ser un callejón | 20 sep 2026 | Un enlace `maps.app.goo.gl` **no lleva la coordenada dentro** y el navegador no puede canjearlo (P-18): no es una limitación del prototipo, es la política de origen cruzado. La salida no era resolverlo, era **dejar de necesitarlo**: el código plus sí lleva la coordenada dentro, se decodifica con aritmética —sin red y sin depender de nadie— y Google Maps lo muestra en la ficha de cualquier lugar, donde se copia con un toque. Se implementó el decodificador y la recuperación del código corto respecto de la Ciudad, comprobados contra los ejemplos publicados de la especificación y en los cuatro rumbos, **incluido el sureste de Milpa Alta, que cae en otro bloque de un grado** y es donde falla una recuperación ingenua. Además, quien pegue un enlace corto ya no recibe un reproche: recibe el propio enlace para abrirlo y la instrucción de qué copiar de vuelta |
| DEC-83 | El enlace de compartir es la vía principal, y el formulario lo dice así | 20 sep 2026 | El código plus resuelve el problema técnico pero **no el humano: nadie sabe qué es**, y quien no sabe sacar una coordenada tampoco va a buscar un código de ocho caracteres. Lo que la gente sí sabe hacer es **compartir la ubicación desde Google Maps**, y eso produce el enlace corto. El campo se reordenó en torno a ese gesto —«Pegar la ubicación de Google Maps o las coordenadas»—, el aviso dejó de explicar una imposibilidad y ahora dice **quién lo va a resolver y cuándo**, y se añadió un «Ver cómo funcionará» que coloca un punto de demostración **sólo a petición y advirtiéndolo**, como la cuenta simulada de Llave CDMX. El código plus y las coordenadas siguen aceptándose, pero como alternativas, no como la instrucción |
| DEC-84 | El Manual Administrativo entra como fuente: nombres correctos y plazos reales | 20 sep 2026 | El Manual resuelve tres cosas que estaban abiertas. **Los nombres**: la unidad de la DGCORENADR no se llama «Coordinación de Inspección y Vigilancia» sino **Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas**, y la de la DGIVA es **Coordinación de Inspección y Vigilancia Ambiental en Suelo Urbano**; ambas quedan corregidas en el turnado y en el pie. **El reparto de competencias**: las fracciones XXX de la DGIVA y XXXVIII de la DGCORENADR dicen exactamente lo que el formulario ya hacía —suelo urbano y Áreas de Valor Ambiental a una, suelo de conservación y Áreas Naturales Protegidas a la otra—, de modo que la regla de turnado deja de sostenerse sólo en la Ley. **Los plazos**: tres días hábiles para turnar, diez para analizar el caso, y noventa y tres días hábiles el procedimiento completo en suelo urbano —noventa en suelo de conservación—. Los avisos de «plazo por confirmar» de la portada, la revisión y el acuse se sustituyen por esas cifras |
| DEC-85 | En la revisión, todos los renglones se corrigen, y el botón aterriza en el campo | 20 sep 2026 | De veinticuatro renglones sólo siete tenían «Editar», sin regla visible: lo que la persona lee ahí es que **el resto no se puede cambiar**, y lo que hace es enviar algo que sabe incorrecto o abandonar. Ahora cada renglón lleva su botón, y **corregir aterriza en el campo**, no al principio del paso —el paso 3 es largo y llegar arriba obliga a buscar—; el foco queda puesto en el control. Los dos únicos renglones sin botón son los que **calcula el punto** —tipo de suelo y área que atiende—, y en vez de callar lo dicen: «Lo determina el punto del mapa». La comprobación que lo fija no cuenta botones: exige que **ningún renglón se quede sin decir cómo se corrige** |
| DEC-86 | Se adoptan los dos primeros controles contra el envío masivo | 20 sep 2026 | **Prueba de humanidad** junto al botón de enviar, exigida siempre —también en la ruta anónima, que es la que no tiene ninguna otra barrera, y también con la validación de campos apagada— y **límite por origen y ventana de tiempo**, con su pantalla. En el prototipo lo que existe es **el lugar y el texto**, que es lo que el servidor no puede inventar; la comprobación y el conteo se construyen del lado del servidor. Dos reglas de diseño que quedan fijadas: **el límite no rechaza, endurece** —el primer umbral sube el costo, sólo el último corta—, y si el servicio de verificación no responde **el envío no se bloquea**: se acepta y se marca, porque perder una denuncia real es peor que recibir una falsa. Se descarta el acertijo visual: excluye a personas con baja visión y es el que más denuncias legítimas pierde. Especificación completa y cifras propuestas en el documento 15 |
| DEC-87 | Las categorías de las capas se normalizan en el dato, no en la pantalla | 20 sep 2026 | El origen trae la misma categoría escrita de dos formas —«Zona Ecologica y Cultural» y «Zona Ecológica y Cultural»—: **catorce categorías distintas que en realidad son diez**, de modo que agrupar por ese texto cuenta dos veces lo mismo. La pantalla lo tapaba con una tabla de equivalencias al vuelo, que arregla lo que se ve y no lo que se agrupa —y obliga a mantener dos catálogos—. Ahora la normalización ocurre **al ingresar la capa**: se añaden `categoria` —el nombre correcto— y `categoria_clave` —la clave estable con la que se agrupa—, y `categoria_origen` **queda intacta** como rastro de auditoría frente al decreto. Se normalizaron también las alcaldías, que estaban peor: sin acentos, con formas cortas, con listas en distinto orden y con una errata («Cujimalpa»). El guion **se detiene** ante un valor no catalogado, para que una errata nueva se vea en vez de colarse como categoría propia. Se retiró la tabla de equivalencias y su función, que quedaron sin uso |
| DEC-88 | El enlace de Google Maps lo resuelve el servidor (P-18, opción B) | 20 sep 2026 | Decidido: el servidor sigue la redirección del enlace corto y devuelve **sólo la coordenada**. Para la persona es un paso menos justo en el caso más difícil —el sitio sin domicilio, donde el punto del mapa es lo único que tiene—. Tiene además un efecto que conviene decir en voz alta: **el navegador de quien denuncia nunca habla con Google**; quien consulta es el servidor, de modo que Google no obtiene su dirección de red ni sabe que alguien está presentando una denuncia. Se construye con las condiciones ya escritas en P-18 —lista blanca de tres dominios, petición que no sigue la redirección, lectura sólo del encabezado, tres segundos de espera y salida limitada a la coordenada—, que son las que evitan la falsificación de petición del lado del servidor. El prototipo no cambia de comportamiento —no hay servidor—, pero sus textos dejan de decir «pendiente» y dicen «por construir» |
| DEC-89 | **Provisional, a consulta de las áreas.** Mientras se resuelve, toda Área Natural Protegida federal se turna a la PROFEPA | 20 sep 2026 | **Lo que se leyó.** La cláusula SEGUNDA del Convenio Marco de Coordinación CONANP-CDMX —firmado el 10 de marzo de 2025 y vigente hasta el 30 de septiembre de 2030— define la coadyuvancia en la administración *«sin perjuicio de las facultades que en materia de inspección y vigilancia otorga el Título Sexto de la Ley General del Equilibrio Ecológico»*, cuyo artículo 161 atribuye esos actos a la autoridad federal. Leído así, el convenio reparte administración y manejo, no inspección. **Lo que no se decide aquí.** Interpretar un convenio frente al Reglamento Interior y al Manual Administrativo **corresponde a las áreas y a la unidad jurídica**, no al prototipo. Por eso la decisión es provisional y queda a consulta en **P-22**. **Qué hace el formulario mientras tanto.** Asume la competencia federal, que es la lectura que **no produce un acto viciado** si resulta la correcta, y lo advierte en pantalla con su marca de pendiente. Si las áreas resuelven lo contrario, el cambio es de una línea. **Lo que sí queda firme**, porque no depende de interpretación: las ocho áreas coadministradas que enumera la cláusula PRIMERA, y la corrección de tres datos del catálogo contra el convenio —fecha de decreto de Cumbres del Ajusco, superficies de Cerro de la Estrella y de Insurgente Miguel Hidalgo y Costilla— |
| DEC-95 | Un color, un trabajo: de siete familias a cinco, y ninguna fuera de la paleta | 20 sep 2026 | Había **treinta y dos valores de color en siete familias, once escritos sueltos** fuera de la paleta. Peor que la cantidad era el reparto. **El ámbar hacía dos trabajos** —advertir a la persona y marcar un pendiente de la Secretaría— y con valores distintos, de modo que se parecían sin serlo: ahora el aviso al ciudadano va en neutro con filete y el ámbar queda sólo para lo pendiente. **El verde estaba en la barra de pasos, en los avisos y en el acuse**: sale de la barra —que un paso esté hecho lo dicen la palomita y el número, y la barra está en todas las pantallas— y queda reservado a una sola: la que dice que la denuncia se recibió. **El morado existía para una pantalla**, la del área federal: la ficha del cruce pasa a un solo panel neutro, porque quién atiende ya lo dice con letras; el rojo se queda sólo donde el punto cae fuera de la Ciudad, que es lo único que impide continuar. **La prueba de humanidad marcada pasa a azul**, que es el color de lo elegido en todo el formulario. Los once valores sueltos entraron a la paleta, que ahora declara en un comentario qué trabajo hace cada familia. La batería 12 no comprueba el gusto, comprueba el reparto: que ningún color viva fuera de la paleta, que el verde no aparezca en ninguno de los siete pasos y sí en el acuse, y que el ámbar sólo lo use la marca de pendiente |
| DEC-96 | «Qué pasa después» va en horizontal en pantalla ancha y **en columna en el teléfono** | 20 sep 2026 | La secuencia horizontal se pidió y estaba bien pedida, pero en el teléfono se resolvía como **dos por renglón**: cuatro cajas centradas en tiras de unos 150 px, con el título partido en dos y el detalle apretado debajo. Dejaba de leerse 1-2-3-4 y se leían cuatro tarjetas sueltas, que es lo contrario de lo que la secuencia quiere decir. En el teléfono pasa a **columna**, con el número a la izquierda, el título y el detalle apilados a su derecha y la línea uniendo los círculos en vertical: ocupa el ancho completo y sigue siendo una secuencia. Desde 620 px vuelve a ser horizontal. La comprobación fija las dos formas: una fila en pantalla ancha, cuatro en el teléfono, y el texto alineado a la izquierda y sangrado a la derecha del número |

---

## Parte II. Preguntas abiertas

### Bloque A · Jurídicas — deben resolverse primero

---

**P-01. ¿Qué es jurídicamente este formulario: un reporte ciudadano o una denuncia ciudadana?**

*Por qué importa.* El artículo 329 de la Ley Ambiental de la Ciudad de México dispone que la denuncia ciudadana se presenta **ante la Procuraduría**, no ante la Secretaría, y el artículo 332 exige su ratificación y obliga a contestar en treinta días hábiles. La Ley no prevé a la Secretaría como receptora. La respuesta determina el nombre del instrumento, los textos del acuse, el aviso de privacidad y los compromisos de plazo que la Secretaría adquiere.

*Opciones.*
- **A. Reporte ciudadano.** El formulario capta información que, conforme al artículo 280 de la Ley Ambiental, la Secretaría valora para instaurar por sí misma el procedimiento de inspección. No requiere ratificación, es compatible con el anonimato y no obliga a plazo de respuesta.
- **B. Denuncia ciudadana en sentido estricto.** El formulario opera como ventanilla que remite a la Procuraduría, con la ratificación en tres días hábiles y el plazo de respuesta de treinta días hábiles que fija su Ley Orgánica.
- **C. Mixta con remisión automática.** Se capta como reporte y, además, se remite a la Procuraduría.
- **D. Mixta con orientación.** Se capta como reporte y se informa a la persona denunciante que puede presentar además su denuncia ante la Procuraduría, sin remitirla de oficio.

*Recomendación fundada.* **Opción D.** La revisión de la Ley Orgánica de la Procuraduría la sustenta en tres puntos:

1. **La Procuraduría no inspecciona.** Su artículo 25, fracción IV, la faculta para requerir a las autoridades competentes la realización de las visitas de verificación e inspección. En materia ambiental local esa autoridad es la Secretaría, de modo que la denuncia presentada allá regresa como requerimiento, con la carga añadida de rendir informe en diez días hábiles (arts. 20 y 25 BIS) bajo apercibimiento de responsabilidad administrativa. Recibir directamente es más rápido para el ciudadano y menos oneroso para la Secretaría.
2. **La remisión automática convierte cada denuncia en un requerimiento.** La opción C generaría de manera artificial la obligación de informar en diez días hábiles por cada caso, sin beneficio para la persona denunciante.
3. **La actuación de oficio no exige ratificación.** El artículo 280 de la Ley Ambiental basta para que la Secretaría instaure el procedimiento de inspección con la información recabada.

*Bloquea:* P-02, P-05, P-07 y todos los textos del formulario.

---

**P-02. ¿Quién y cuándo reexpide el aviso de privacidad?**

*Por qué importa.* El aviso del formato vigente se funda en la Ley de Protección de Datos Personales para el Distrito Federal y remite al InfoDF, ambos superados por la Ley de Protección de Datos Personales en Posesión de Sujetos Obligados de la Ciudad de México y el INFO CDMX. No es publicable un formulario que recabe datos con ese aviso.

*Recomendación.* Solicitarlo a la Unidad de Transparencia una vez resuelta P-01, indicando expresamente la finalidad, las transferencias y el responsable del sistema de datos personales.

*Bloquea:* la publicación.

---

**P-03. ¿El Histórico Coyoacán queda fuera del convenio de coadministración?**

*Por qué importa.* La capa entregada contiene nueve Áreas Naturales Protegidas federales y el catálogo de convenios enumera ocho. La diferencia es El Histórico Coyoacán. **Desde DEC-89 los nueve polígonos federales se derivan a la PROFEPA**: lo que el convenio cambia no es quién inspecciona, sino que la Secretaría coadyuva en la administración y queda enterada.

*Opciones.* A. Confirmar que efectivamente no está cubierta. B. Incorporarla al catálogo si la omisión fue involuntaria.

**Respondido el 20 de septiembre de 2026 · Opción A.** El Histórico Coyoacán **no forma parte del convenio de coadministración**: al no estar en el convenio, la totalidad del polígono es competencia federal. El formulario ya se comportaba así —se verificó colocando un punto dentro del polígono—, de modo que en su momento no hubo cambio de código. **Horas después, el examen del convenio mostró que tampoco en las ocho coadministradas hay facultad local de inspección, y la regla se generalizó a las nueve (DEC-89).**

*Sobre el polígono, que también se preguntó.* **Sí existe.** Viene de la CONANP, se enlazó por alias («El Historico de Coyoacan»), está clasificado como Parque Nacional en Coyoacán y ocupa aproximadamente un kilómetro por seiscientos metros al sur del centro de la alcaldía. **Dos reservas que conviene anotar:** tiene sólo veintitrés vértices, que es un trazo grueso para un parque —suficiente para decidir competencia, insuficiente para un plano—; y la superficie decretada llega en cero, es decir, el origen no la trajo. Ninguna de las dos impide operar; las dos deberían corregirse cuando se actualice la capa federal.

*Bloquea:* nada. Regla RN-05 confirmada.

---

**P-04. ¿Cómo se turna una denuncia cuando concurren decreto federal y local sobre la misma superficie?**

*Por qué importa.* Cerro de la Estrella y Sierra de Guadalupe tienen decreto federal y local traslapados. El prototipo da precedencia al federal y advierte la concurrencia, pero no es una regla adoptada.

*Opciones.* A. Precedencia federal con vista al área local. B. Precedencia local por tratarse de superficie coadministrada. C. Turnado simultáneo a ambas.

*Recomendación original, **invalidada el 20 de septiembre de 2026 por DEC-89**.* Decía: «Opción B para las ocho coadministradas, por ser superficie sobre la que la Secretaría ya ejerce atribuciones». **Esa premisa es falsa:** la Secretaría no ejerce atribuciones de inspección en las Áreas Naturales Protegidas federales, tampoco en las coadministradas. La recomendación pasa a ser la **opción A** —precedencia federal, con vista al área local—, **sujeta a lo que se resuelva en P-22**: cuando el punto cae además en un área local, la Secretaría puede intervenir por el decreto local, nunca por el convenio.

*Bloquea:* regla RN-07.

---

### Bloque B · Operativas

---

**P-05. ¿Cuál es el criterio de procedencia de la denuncia anónima?**

*Por qué importa.* Sin datos de contacto no es posible requerir información faltante ni notificar el resultado.

*Lo que aclara la Ley Orgánica de la Procuraduría.* El anonimato no impide la actuación de la autoridad; sólo cambia la vía. El artículo 22 dispone que la denuncia no ratificada *se tendrá por no presentada*, pero el mismo artículo permite investigar si el asunto lo amerita, y el artículo 23, fracción II, enumera expresamente las denuncias no ratificadas como supuesto de **investigación de oficio**. El equivalente para la Secretaría es el artículo 280 de la Ley Ambiental.

*Recomendación.* Admitirla siempre, tratarla como insumo de actuación de oficio y condicionar la práctica de la inspección a que la descripción y la ubicación resulten suficientes por sí mismas. El formulario debe decirlo con esas palabras: la denuncia anónima se atiende, pero no se notifica.

*Bloquea:* regla RN-21.

---

**P-06. ¿Cuántos archivos y de qué peso máximo se admiten?**

*Supuesto del prototipo.* Diez archivos de hasta 25 MB cada uno.

*Bloquea:* regla RN-25.

---

**P-07. ¿Qué plazo de atención se comunica al ciudadano y por qué medio se informa el resultado?**

*Por qué importa.* El acuse afirma que se informará el resultado. Si no existe plazo comprometido, el texto debe redactarse sin generar expectativa incumplible.

**Respondido en parte el 20 de septiembre de 2026, con el Manual Administrativo.** Los plazos existen y están escritos:

| | Suelo urbano y AVA (DGIVA) | Suelo de conservación y ANP (DGCORENADR) |
|---|---|---|
| Recibir la denuncia y turnarla | 3 días hábiles | 3 días hábiles |
| Analizar el caso | 10 días hábiles | 10 días hábiles |
| Si no es competencia, turnar o rechazar | 5 días hábiles | 5 días hábiles |
| **Procedimiento completo, hasta la resolución notificada** | **93 días hábiles** | **90 días hábiles (aproximado)** |

Son días hábiles, y el propio Manual advierte que pueden variar si otra dependencia tarda en responder o si la persona inspeccionada interpone un medio de defensa. Los tres avisos de «plazo por confirmar» —portada, revisión y acuse— ya se sustituyeron por estas cifras (DEC-84).

**Lo que sigue abierto:** el Manual fija el plazo del **procedimiento**, no el de **informar a la persona denunciante**. La Jefatura de Unidad Departamental de Seguimiento a Denuncias tiene la función de elaborar esos informes, pero sin plazo escrito. Falta que la DGIVA diga en cuántos días se responde a quien pregunta por su folio, que es lo que el acuse promete.

*Bloquea:* la parte de RN-29 relativa al aviso de resultado.

---

**P-08. ¿Cuáles son los datos de contacto de las instancias receptoras por derivación?**

*Detalle.* Se requieren teléfono y liga vigentes de: Secretaría de Obras y Servicios, Secretaría de Seguridad Ciudadana, PAOT, PROFEPA, INVEA, Agencia de Atención Animal y las dieciséis alcaldías. Hoy aparecen marcados como pendientes en el prototipo.

*Bloquea:* las pantallas de derivación.

---

**P-09. ¿Cuáles son los domicilios vigentes de las dos unidades que atienden y el de recepción de denuncias?**

*Por qué importa.* Hoy conviven dos domicilios contradictorios en los canales oficiales: el formato en PDF señala **Tlaxcoaque No. 8** y el portal remite al **Bosque de San Juan de Aragón**. A eso se suma que, desde que el turnado se decide por el tipo de suelo, **la unidad que atiende ya no siempre es la misma**: una denuncia en suelo urbano la sigue la Dirección General de Inspección y Vigilancia Ambiental, y una en suelo de conservación o Área Natural Protegida la sigue la Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas de la DGCORENADR. Si sus domicilios son distintos, el formulario y el acuse deben decirle a cada persona a dónde acudir, y no a una dirección genérica.

*Lo que hay que validar, con domicilio completo, horario y teléfono:*

| Unidad | Dato por confirmar |
|---|---|
| **Recepción de denuncias** | Domicilio y horario de la Oficialía de Partes que recibe. Si es única para ambas direcciones generales, basta uno; si cada una recibe por su cuenta, son dos |
| **Dirección General de Inspección y Vigilancia Ambiental** | Domicilio de atención al público, horario y teléfono |
| **Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas · DGCORENADR** | Domicilio de atención al público, horario y teléfono. Conviene precisar si atiende en la sede de la dirección general o en oficinas en suelo de conservación |

*Cómo validarlo.* Contrastar el directorio institucional publicado con lo que señalan el portal y el formato en PDF, y confirmarlo con cada dirección general. Un domicilio publicado en un canal oficial y desmentido en otro es, en sí mismo, un problema de certeza jurídica para quien presenta una denuncia por escrito.

*Efecto en el instrumento.* El pie del formulario y el apartado «Qué sigue» del acuse deben mostrar el domicilio de la unidad que efectivamente atenderá el caso, que el propio cruce espacial ya determinó. Mientras no se confirme, ambos muestran únicamente la Oficialía de Partes con la advertencia correspondiente.

*Se relaciona con:* **P-08**, datos de contacto de las instancias receptoras por derivación, y **P-10**, fundamento del reparto de atribuciones.

*Bloquea:* los textos del pie y del acuse, y la corrección del portal institucional.

---

### Bloque C · Técnicas y de información

---

**P-10. ¿Qué falta por verificar en el reparto de atribuciones entre unidades administrativas?**

*Estado.* **Resuelto en lo esencial.** El Reglamento Interior del Poder Ejecutivo y de la Administración Pública de la Ciudad de México, texto vigente al 27 de marzo de 2026, sustenta el reparto que aplica el formulario: artículo 191, fracción III, para suelo urbano y Áreas de Valor Ambiental; artículo 188, fracciones XXXIX a XLI, para suelo de conservación y Áreas Naturales Protegidas, más la fracción XXXVIII, que atribuye a esa dirección general recibir y atender denuncias ciudadanas en esos ámbitos. El desarrollo consta en el documento de marco jurídico, apartado 6 bis.

*Lo que subsiste.*

1. **Coordinación de Inspección y Vigilancia.** No aparece en el Reglamento Interior, que sólo adscribe a la DGCORENADR la Dirección Ejecutiva de la Zona Patrimonio Mundial. Debe verificarse en el **Manual Administrativo** si puede ordenar visitas y sustanciar el procedimiento por sí misma o sólo ejecutar lo que ordene su dirección general. Determina quién firma la orden de visita y cómo se nombra a la autoridad en el acuse.
2. **Traslape con la DGSANPAVA.** El artículo 190, fracción XXII, le atribuye establecer y operar el sistema de inspección, seguridad y vigilancia de las Áreas Naturales Protegidas, Áreas de Valor Ambiental y áreas verdes urbanas. No desplaza la facultad sancionadora, pero debe definirse si recibe copia de las denuncias que caen en esos polígonos.
3. **Áreas Naturales Protegidas federales con convenio.** Si el fundamento de la actuación local deriva del propio convenio o requiere además previsión reglamentaria.

*Responsable.* Dirección General de Inspección y Vigilancia Ambiental, con apoyo de la unidad jurídica.

*Bloquea:* la firma de la orden de visita, los perfiles de usuario de AD-01 y la copia a terceras unidades.


*Respondido el 20 de septiembre, con el Manual Administrativo a la vista.*

**La Coordinación existe, tiene nombre distinto del que usábamos y sí sustancía.** Se llama **Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas**, y el procedimiento del Manual le asigna recibir la denuncia, analizar la competencia, preparar los documentos, aprobar el acuerdo de emplazamiento y turnar la resolución. La orden y la resolución las **autoriza y firma la dirección general**, de modo que DEC-30 sigue siendo correcta: el formulario nombra a la dirección general, y ahora puede añadir la coordinación como unidad que atiende, que es lo que hace.

**La DGSANPAVA no recibe denuncias.** El Manual no le asigna ninguna función de recepción, trámite o seguimiento: su única mención al tema es «coordinar con las instancias correspondientes en la atención de la denuncia ciudadana en materia de delitos ambientales», y está en una subdirección de proyectos, no en una unidad de inspección. **Queda una tensión que conviene registrar**: el artículo 190, fracción XXII, del Reglamento Interior le atribuye operar el sistema de inspección y vigilancia en Áreas Naturales Protegidas y Áreas de Valor Ambiental, y el Manual no le da procedimiento para ello. Es una incongruencia entre el Reglamento y el Manual, no del formulario; hasta que se aclare, la DGSANPAVA **no se nombra** como área que atiende.

**Trasladado a P-22 el 20 de septiembre de 2026.** Lo que quedaba abierto era el fundamento de la actuación en Áreas Naturales Protegidas federales con convenio. La lectura del convenio sugiere que **no hay fundamento porque no hay actuación**: el convenio reparte administración y manejo, y su cláusula SEGUNDA deja a salvo las facultades federales de inspección. La denuncia se turna, provisionalmente, a la PROFEPA. **La interpretación queda a consulta de las áreas en P-22.**
---

**P-11. ¿Quién normaliza las categorías de `geometrias.geojson`?**

*Estado.* El prototipo ya normaliza la acentuación para el despliegue, pero la corrección de fondo corresponde a la capa de origen.

*Detalle.* Existen inconsistencias de acentuación —"Zona Ecologica y Cultural" frente a "Zona Ecológica y Cultural"; "Zona Sujeta a Conservacion Ecologica" frente a su forma acentuada— y la Sierra de Santa Catarina aparece duplicada como Zona de Conservación Ecológica y como Zona Sujeta a Conservación Ecológica. Impide agrupar por categoría sin limpieza previa.

**Respondido el 20 de septiembre de 2026. Lo hizo el proyecto, no hacía falta esperar a nadie.**

*La normalización.* Se hace **al ingresar la capa**, con un guion propio —`construccion/normalizar_capas.py`— y no en la pantalla: `categoria` es el nombre correcto, `categoria_clave` la clave estable con la que se agrupa, y `categoria_origen` queda intacta como rastro de auditoría frente al decreto. Catorce categorías del origen resultaron ser diez. Se normalizaron también las alcaldías, que estaban peor —sin acentos, con formas cortas, con listas en distinto orden y con la errata «Cujimalpa»—. El guion **se detiene ante un valor no catalogado**, de modo que una errata nueva se ve en lugar de colarse como categoría propia, y la batería 10 comprueba que ninguna categoría se repita con otra acentuación (DEC-87).

*El supuesto duplicado no lo era.* La Sierra de Santa Catarina aparece dos veces porque **son dos áreas distintas y colindantes**, no una capturada dos veces: la Zona de Conservación Ecológica, de 528 ha, y la Zona Sujeta a Conservación Ecológica, de 220.55 ha. Se comprobó con una rejilla de 180 × 180 puntos sobre la envolvente común de los dos polígonos: **12 603 puntos caen dentro de alguno de los dos y ninguno dentro de los dos a la vez**. No se traslapan ni un metro, de modo que el cruce espacial nunca queda ambiguo y no hay precedencia que resolver.

*Lo único que queda, y es del área.* Confirmar contra los decretos que efectivamente son dos figuras jurídicas distintas sobre la misma sierra —y no un desdoblamiento administrativo antiguo—, y si los nombres deben conservar las siglas «(ZCE)» y «(ZSCE)» o llevar el nombre completo de cada declaratoria. Ninguna de las dos cosas impide operar.

*A quién corresponde.* Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural, para la confirmación documental.

---

**P-12. ¿Con qué servicio se resolverán la geocodificación y el cruce espacial en la versión funcional?**

*Por qué importa.* El prototipo usa un servicio externo para proponer colonia, código postal y calle, y resuelve el cruce en el navegador con geometrías simplificadas. Ninguna de las dos cosas es admisible en producción: el cruce debe resolverse en servidor contra las capas completas y la geocodificación debe apoyarse en un servicio propio.

*Severidad elevada el 18 de septiembre de 2026.* Con la dirección capturada primero y el punto propuesto a partir de ella (DEC-37), la geocodificación dejó de ser una mejora y **sostiene el flujo**: sin ella la persona debe colocar el punto a mano en todos los casos. El formulario lo permite y lo dice —ningún servicio externo puede dejar la pantalla inservible—, pero es una degradación notable de la experiencia.

*Se relaciona con:* **P-16**, catálogo oficial de colonias y códigos postales.

*Bloquea:* la fase 2 y la calidad del paso 2 desde ahora.


**Respondido el 20 de septiembre de 2026, con una distinción que cambia la pregunta.**

*El cruce espacial no necesita servicio.* Es lo primero, y lo que más ahorra: el cruce corre contra **nuestras propias capas**, no contra las de nadie. Hoy lo hace el navegador con la geometría incrustada; en la versión funcional lo hará el servidor, con PostGIS o con el mismo algoritmo de punto en polígono. **Cero costo, cero dependencia y cero terceros.** Y así debe ser, porque de ese cruce depende a qué autoridad se turna un expediente: una regla de competencia no puede quedar sujeta a que un servicio externo responda.

*Sólo la geocodificación necesita servicio*, y **sólo como comodidad**: convierte la dirección escrita en un punto, pero el punto puede colocarse siempre con un clic en el mapa o pegando la ubicación. Si el servicio no responde, el formulario sigue sirviendo —así está previsto ya, y así debe quedar—.

*Lo que no sirve.* El **servicio público de Nominatim** no es una opción para producción, y conviene decirlo antes de que alguien lo proponga: su política de uso permite **una petición por segundo**, **prohíbe el autocompletado**, prohíbe las consultas sistemáticas, exige identificar la aplicación, y establece que las aplicaciones cuya función principal sea geocodificar **deben operar su propia instancia**. Un formulario público de gobierno lo incumpliría el primer día de operación.

*Opciones reales.*

| Opción | Qué implica | A favor | En contra |
|---|---|---|---|
| **A. Nominatim propio**, con un extracto de la Ciudad de México | Un servidor con la base de OpenStreetMap del área metropolitana | Sin límites ni costo por consulta; **la dirección de quien denuncia no sale de la Secretaría** | Hay que alojarlo y actualizarlo |
| **B. Photon propio** | Igual, pero pensado para buscar mientras se escribe | Responde a cada tecla, que es lo que la gente espera; ligero | Menos preciso en direcciones exactas que Nominatim |
| **C. Pelias propio** | Motor que **mezcla OpenStreetMap con catálogos locales** de direcciones | Puede ingerir el padrón de direcciones de la Ciudad y mejorar lo que OSM no tiene | El más complejo de operar de los tres |
| **D. Servicio del propio Gobierno de la Ciudad** | Usar lo que exponga el Sistema Abierto de Información Geográfica de la Ciudad de México, operado por la Agencia Digital de Innovación Pública | Es dato oficial, sin terceros y sin costo | **Falta verificar si expone geocodificación y con qué condiciones** |
| **E. Proveedor comercial** (Google, Mapbox y similares) | Consumo por consulta | Cero operación | Costo recurrente, y **la dirección del domicilio de quien denuncia viaja a un tercero extranjero**, con lo que eso implica en el aviso de privacidad |

*Recomendación.* **Preguntar primero por la opción D** —si la Ciudad ya opera un geocodificador, usarlo es más barato, más defendible y más congruente que montar otro— y, si no lo hay o no está disponible, **la opción B para buscar mientras se escribe, respaldada por A para la resolución exacta**, las dos autoalojadas. La opción E se descarta salvo que las anteriores resulten inviables, y en ese caso debe declararse la transferencia en el aviso de privacidad.

*Condición que vale para cualquiera.* El geocodificador **propone** el punto; nunca lo fija por su cuenta. La persona lo ve en el mapa antes de continuar, y el cruce que decide la competencia se hace contra nuestras capas, sobre el punto que quedó.

*A quién corresponde.* Sistema de Información Ambiental, con la Agencia Digital de Innovación Pública para la opción D.
---

**P-13. ¿Cuál es la estructura definitiva del folio y cómo se administra el consecutivo?**

*Supuesto del prototipo.* `SEDEMA/DGIVA/DEN/AAAA/NNNNNN`. Debe confirmarse si el consecutivo es único o se segmenta por área competente, dado que una parte de las denuncias se turna a la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural.

*Bloquea:* la fase 2.

---

**P-14. ¿Qué estados del expediente pueden mostrarse a quien denunció, con qué redacción, y hasta cuándo permanece disponible la consulta?**

*Por qué importa.* El seguimiento ciudadano (AD-02) no puede mostrar el estado interno tal cual: hay etapas cuya difusión compromete la diligencia de la visita de inspección o expone datos del presunto responsable. Se requiere una equivalencia autorizada entre los estados operativos y los estados públicos.

*A quién corresponde.* Dirección General de Inspección y Vigilancia Ambiental y Coordinación de Inspección Ambiental en Suelo de Conservación y Áreas Naturales Protegidas de la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural, con opinión de la Unidad de Transparencia.

*Bloquea:* el desarrollo de AD-02.

---

**P-15. ¿Cómo se integra el formulario con Llave CDMX y qué ocurre con la denuncia anónima?**

*Por qué importa.* Son dos cuestiones distintas y ambas condicionan el diseño.

1. *Técnica.* Debe confirmarse con la Agencia Digital de Innovación Pública el mecanismo de integración, los datos que la cuenta entrega a la dependencia —nombre, CURP, correo, domicilio— y si el acceso del personal servidor público se resuelve por la misma vía o por una distinta. Debe confirmarse también la relación con la identidad digital nacional «Llave MX» y cuál de las dos, o ambas, se acepta.
2. *De diseño.* **Resuelto por DEC-50:** el formulario ya opera con las tres rutas y la cuenta se simula, rotulada como simulada, para poder mostrar el recorrido completo en la sesión de validación. Lo que sigue dependiendo de la Agencia es la integración técnica, no el diseño. Exigir cuenta para denunciar es incompatible con la denuncia anónima. La ruta propuesta conserva las dos: denuncia **identificada** con Llave CDMX —prellena los datos, vincula el folio a la cuenta y habilita el seguimiento y la notificación— y denuncia **anónima** sin cuenta, con folio y clave en pantalla, sin notificación y sin recuperación. Si la Dirección General decide que la cuenta sea obligatoria, la denuncia anónima desaparece del canal y debe resolverse P-05 en ese sentido.

*Consideración de protección de datos.* La autenticación con identidad digital traslada a la cuenta datos personales que hoy se capturan a mano. El aviso de privacidad (P-02) debe redactarse ya con ese supuesto.

*A quién corresponde.* Agencia Digital de Innovación Pública en lo técnico; Dirección General de Inspección y Vigilancia Ambiental y Unidad de Transparencia en lo relativo al anonimato y al tratamiento de datos.

*Bloquea:* la versión funcional del formulario, AD-01 y AD-02.

---

**P-16. ¿Con qué catálogo oficial de colonias y códigos postales se valida la dirección?**

*Por qué importa.* El prototipo propone colonia y código postal a partir de un servicio externo de geocodificación y los deja como texto libre. Eso tiene tres consecuencias: la misma colonia se escribe de formas distintas y la explotación estadística por colonia deja de ser posible; el código postal puede no corresponder a la colonia capturada, con el riesgo de que la notificación por domicilio no llegue; y la denuncia no puede cruzarse con los padrones y sistemas del Gobierno de la Ciudad, que operan sobre el catálogo oficial.

*Qué se solicita.* A la **Agencia Digital de Innovación Pública**, el catálogo vigente de **colonias, códigos postales y alcaldías** de la Ciudad de México, preferentemente con su geometría, con la clave de cada colonia y con el mecanismo de actualización. Interesa saber si se entrega como capa descargable, como servicio de consulta, o ambos: de eso depende si el formulario valida contra una tabla local o consulta en línea.

*Efecto en el formulario.* Con el catálogo, la colonia deja de ser texto libre y pasa a ser una selección acotada por la alcaldía que arroja el punto en el mapa, y el código postal se deriva de ella en lugar de capturarse. Reduce errores de captura y vuelve explotable el dato.

*A quién corresponde.* Agencia Digital de Innovación Pública. **Se solicita en el mismo oficio que P-15**, por dirigirse a la misma instancia.

*Se relaciona con:* **P-12**, servicio de geocodificación propio, del que este catálogo es el insumo base.

*Bloquea:* la validación de domicilio en la versión funcional y la estadística por colonia.

---

**P-17. ¿El teléfono debe seguir siendo obligatorio?**

*Por qué importa.* En los dos esquemas el teléfono es obligatorio, pero **no es vía de notificación**: la notificación se practica por correo electrónico o por domicilio. Su uso real es operativo —aclarar un dato, coordinar el acceso al sitio durante la visita—. La revisión de minimización (DEC-35) lo hizo visible: un dato personal que no sostiene ninguna actuación formal está condicionando la presentación de la denuncia.

*Opciones.* A. Dejarlo obligatorio. B. Volverlo opcional, con la ayuda «agiliza la visita si el personal necesita confirmar algo contigo».

*Recomendación.* **Opción B.** Quien quiera darlo lo dará; exigirlo sólo aparta a quien no quiere dejar su teléfono, y esa persona hoy no tiene alternativa salvo la denuncia anónima, que renuncia al seguimiento.

*A quién corresponde.* Dirección General de Inspección y Vigilancia Ambiental.

*Bloquea:* el cierre del esquema de obligatoriedad.

---

**P-18. ¿Debe el sistema resolver los enlaces cortos de Google Maps para extraer la coordenada?**

*Por qué importa.* Cuando alguien comparte un lugar desde la aplicación de mapas, lo que obtiene es un enlace corto —`maps.app.goo.gl/…`— que **no lleva la coordenada dentro**: es sólo un identificador que hay que canjear. El formulario lee los enlaces largos con una expresión regular, en el navegador y sin salir a la red (DEC-69), pero con los cortos no hay nada que leer, y hoy pide el enlace completo.

*Lo que no se puede.* Resolverlo desde el navegador es **imposible**, no difícil: la política de origen cruzado impide leer la redirección. Cualquier solución exige que lo haga el servidor.

*Opciones.*
- **A. Dejarlo como está.** El formulario explica cómo obtener el enlace completo. Cero dependencias, cero superficie de ataque.
- **B. Resolverlo en el servidor.** El servidor sigue la redirección y devuelve sólo la coordenada. Para la persona es un paso menos, y **su navegador no habla con Google**: quien consulta es el servidor, de modo que Google no obtiene su dirección de red.

*Condiciones si se elige B.* Aceptar que el servidor pida una dirección web que escribe el público es una vulnerabilidad conocida —falsificación de petición del lado del servidor— y sólo es admisible con: **lista blanca estricta** de los dominios de enlaces cortos, ninguna redirección fuera de ellos, tiempo de espera corto, y uso exclusivo del encabezado de redirección sin leer el contenido de la respuesta. Añade además una dependencia de un servicio externo en un trámite de gobierno, con su modo de fallo.

**Respondido el 20 de septiembre de 2026 · Opción B** (DEC-88). Queda decidido: lo resuelve el servidor, con las condiciones de esta ficha. Falta construirlo, no decidirlo.

*Recomendación original, que la decisión confirma.* **Opción B, en la versión funcional y con esas condiciones**, porque el beneficio recae justo en el caso más difícil —el sitio sin domicilio, donde el pin del mapa es lo único que la persona tiene—. En el prototipo no cabe: no hay servidor.

*Lo que cambió el 20 de septiembre, y por qué P-18 subió de prioridad.* Primero se añadió el código plus, que sí lleva la coordenada dentro y se lee sin red (DEC-82). Después quedó claro que eso resuelve el problema técnico y no el humano: **nadie sabe qué es un código plus**, y quien no sabe sacar una coordenada menos va a buscar un código. El gesto que la gente conoce es compartir la ubicación, y ese gesto produce exactamente el enlace que no podemos leer.

**P-18 deja de ser una mejora y pasa a ser requisito de la versión funcional.** No es la diferencia entre dos toques y uno: es la diferencia entre que la persona marque el sitio o abandone, y pesa más justo donde el formulario es más necesario —el lugar sin domicilio, donde el punto es lo único que hay—.

*Cómo se implementa, para que no quede como un problema abierto.* Es un servicio de una sola función, y estas son sus condiciones:

| | |
|---|---|
| **Entrada** | La dirección web que la persona pegó, nada más |
| **Lista blanca** | `maps.app.goo.gl`, `goo.gl`, `g.co`. Cualquier otra, se rechaza sin consultarla |
| **Consulta** | Petición que **no sigue** la redirección: se lee el encabezado `Location` y se descarta el cuerpo de la respuesta |
| **Límites** | Tiempo de espera de tres segundos, máximo dos redirecciones, y sólo si la redirección apunta a `google.com/maps` |
| **Salida** | La coordenada extraída del destino con las mismas expresiones que ya usa el navegador, o un error. **Nunca el contenido de la respuesta** |
| **Abuso** | Límite de peticiones por origen, como el resto del formulario (P-21) |

Esas condiciones son las que evitan la falsificación de petición del lado del servidor, que es el riesgo de aceptar una dirección web escrita por el público. Con ellas, la superficie de ataque se reduce a tres dominios y a un encabezado.

*Efecto colateral favorable.* El navegador de la persona **nunca habla con Google**: quien consulta es el servidor, de modo que Google no obtiene su dirección de red ni sabe que alguien está presentando una denuncia.

*A quién corresponde.* Sistema de Información Ambiental, junto con P-12.

*Bloquea:* nada. Es una mejora de la versión funcional.

---

**P-19. Los seis datos que el aviso de privacidad simplificado necesita para poder publicarse**

*Por qué importa.* El aviso ya se lee en pantalla antes de enviar (DEC-79), que es como debe ser. Pero cuatro de sus seis rótulos están incompletos, y ninguno puede inventarse: **el nombre del sistema de datos personales** en que se protegen los datos de la denuncia, y su inscripción; **el ciclo de vida del dato**, conforme al catálogo de disposición documental de la Secretaría; **el catálogo de transferencias** y su fundamento; y el **domicilio, teléfono y correo de la Unidad de Transparencia**. Falta además el artículo del Reglamento Interior que atribuye la función a la unidad responsable.

*Qué se hizo mientras tanto.* Los huecos quedan visibles en la propia pantalla, con el mismo tratamiento que el resto de los pendientes del prototipo. Ninguno se rellenó con una aproximación.

*A quién corresponde.* Unidad de Transparencia de la Secretaría, junto con la Dirección General de Inspección y Vigilancia Ambiental.

*Bloquea:* la publicación del formulario. Va junto con P-02.

---

**P-20. ¿Se preguntan género y edad, y con qué respaldo?**

*Por qué importa.* El formulario ya las pregunta, opcionales y en las dos rutas (DEC-78). Dos cosas faltan por resolver antes de operar: **el género es dato sensible** —la identidad de género lo es, conforme al criterio del órgano garante—, de modo que su tratamiento exige consentimiento expreso y no puede ampararse en el ejercicio de atribuciones, como sí ocurre con los datos de la denuncia; y **el uso real del dato**, porque un dato que nadie explota no se pide: si no hay quien produzca la estadística y la publique, la pregunta es carga sin beneficio.

*Opciones.* A. Conservarlas como están, con consentimiento expreso separado del resto. B. Conservarlas sin el género y sólo con el rango de edad, que no es dato sensible. C. Retirarlas.

*Recomendación.* **Opción A**, con dos condiciones: que el aviso de privacidad diga expresamente que son opcionales y para qué se usan —ya lo dice—, y que el Sistema de Información Ambiental asuma la publicación periódica de la desagregación. Sin lo segundo, la opción B.

*A quién corresponde.* Unidad de Transparencia y Sistema de Información Ambiental.

*Bloquea:* nada en el prototipo; sí la operación.

---

**P-21. Qué controles del lado del servidor se adoptan contra el envío masivo o de mala fe**

*Por qué importa.* Se comprobó en el formulario de la PAOT que puede enviarse una denuncia con todos los campos llenos de letras al azar, sin validación alguna. El formulario ya no lo permite del lado del navegador (DEC-80), pero **eso no detiene a nadie que quiera hacer daño**: cualquiera puede saltarse el navegador. Las defensas que sirven viven en el servidor y son decisiones, no código: prueba de humanidad en el envío, límite de denuncias por origen y por ventana de tiempo, verificación del correo antes de emitir el folio, detección de duplicados por punto y materia, y umbral de ráfaga que marca una campaña para revisión. El documento 15 las desarrolla con su costo y su efecto.

*Lo que no debe hacerse.* Rechazar denuncias por sospecha. La autoridad no puede negarse a recibir; **lo que sí puede es ordenar la cola**. La defensa correcta no es el rechazo, es la priorización y la acumulación.

*Respondido en parte el 20 de septiembre.* Los controles **1 y 2 quedan adoptados** (DEC-86), con su especificación y sus cifras propuestas en el documento 15; el prototipo ya trae el lugar y el texto de ambos. Siguen abiertos los controles 3 a 6 —verificación del correo, detección de duplicados, umbral de ráfaga y puntaje de completitud— y falta elegir la tecnología de la prueba de humanidad entre las tres familias del documento 15.

*A quién corresponde.* Sistema de Información Ambiental, con la Dirección General de Inspección y Vigilancia Ambiental para el criterio de acumulación, y con la Unidad de Transparencia si se elige un servicio gestionado de terceros.

*Bloquea:* la puesta en operación, no el prototipo.

---

**P-22. ¿Quién atiende una denuncia dentro de un Área Natural Protegida federal coadministrada?**

*Por qué importa.* Es la pregunta de competencia con más consecuencias del formulario. Si la Secretaría inspecciona donde no puede, el acto nace viciado y la persona denunciada lo tumba; si deriva a la PROFEPA lo que sí podía atender, el canal pierde su razón de ser en ocho de los sitios de mayor valor ambiental de la Ciudad —el Desierto de los Leones, Cumbres del Ajusco, el Tepeyac, Lomas de Padierna, Fuentes Brotantes, Cerro de la Estrella, Insurgentes Miguel Hidalgo y Costilla y Tláhuac-Xico—.

*Lo que dice el convenio.* Su cláusula SEGUNDA define la administración como la ejecución de actividades de conservación mediante manejo, gestión y uso de recursos, **«sin perjuicio de las facultades que en materia de inspección y vigilancia otorga el Título Sexto de la Ley General del Equilibrio Ecológico y la Protección al Ambiente»**. El artículo 161 de esa ley atribuye los actos de inspección y vigilancia a la autoridad federal, y el 160 fija que ese título rige los asuntos de competencia federal.

*Lo que no resuelve el convenio.* Si la salvedad significa que la Secretaría **no puede** inspeccionar en esas áreas, o que **puede hacerlo por otra vía** —el decreto local cuando hay concurrencia, un convenio específico de los que prevé la cláusula QUINTA, o la coadyuvancia en vigilancia que menciona la cláusula CUARTA, inciso d)—. Tampoco si la Secretaría, al recibir una denuncia federal, debe remitirla, y por qué vía: el artículo 189 admite que la denuncia federal se presente ante otras autoridades, pero el trámite de remisión no está convenido.

*Opciones.*
- **A. Competencia federal en las nueve.** La denuncia se recibe y se remite a la PROFEPA. Es lo que el formulario hace hoy, de forma provisional.
- **B. Competencia local en las ocho coadministradas.** Requiere el fundamento que el convenio no da: habría que exhibirlo.
- **C. Competencia federal, con convenio específico de remisión y de vigilancia.** Se conviene con la CONANP el cauce —que su cláusula TERCERA, inciso p), contempla al enumerar la denuncia ciudadana entre las materias de los proyectos conjuntos— y la Secretaría coadyuva en vigilancia sin ordenar inspecciones.

*Recomendación.* **Opción A mientras no haya respuesta, y opción C como destino.** La opción A no compromete nada y evita el acto viciado; la C aprovecha el convenio para algo más que enterarse.

*A quién corresponde.* Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural y Dirección General de Inspección y Vigilancia Ambiental, con la unidad jurídica de la Secretaría. Conviene consultarlo también con la Dirección Regional Centro y Eje Neovolcánico de la CONANP, que es la responsable designada en la cláusula SÉPTIMA.

*Bloquea:* la regla RN-04 y RN-05 en su parte federal, y P-04, cuya recomendación depende de esta respuesta.

---

## Parte III. Riesgos

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Publicar con el aviso de privacidad vigente | Tratamiento de datos personales sin fundamento actualizado | P-02 antes de cualquier publicación |
| Difundir fundamentos de la ley abrogada | Actos viciados y pérdida de certeza jurídica | Sustitución de citas conforme al documento de marco jurídico |
| Resolver el cruce espacial en el navegador | Manipulación del resultado y dependencia de geometrías simplificadas | P-12 |
| Dependencia de un servicio externo de geocodificación | Indisponibilidad y consideraciones de protección de datos | P-12 |
| Ofrecer respuesta sin plazo sustentado | Incumplimiento frente al ciudadano | P-01 y P-07 |

## Parte IV. Secuencia sugerida

1. Resolver P-01, por condicionar la redacción de todos los textos.
2. Resolver en la misma sesión el Bloque B, que no requiere consulta jurídica.
3. Solicitar el aviso de privacidad (P-02) con la decisión de P-01 ya tomada.
4. Encargar al Sistema de Información Ambiental P-11 y P-12.
5. Solicitar a la Agencia Digital de Innovación Pública, en un solo oficio, la integración con Llave CDMX (P-15) y el catálogo de colonias y códigos postales (P-16).
6. Construir la versión funcional y el tablero de seguimiento.
7. Prueba controlada con un grupo reducido antes de la publicación abierta.
8. Desarrollar el módulo de administración y seguimiento interno (AD-01) y, sobre él, el seguimiento ciudadano por folio (AD-02).


---

## Parte V. Alcance diferido

### AD-01. Módulo de administración y seguimiento

**Estado: pendiente. No se construye hasta que el formulario de denuncia esté validado por la Dirección General de Inspección y Vigilancia Ambiental.**

Es la herramienta interna con la que el equipo que atiende las denuncias las recibe, consulta y da seguimiento. Se difiere porque su bandeja, sus filtros y sus indicadores se construyen sobre el modelo de datos del formulario: cualquier cambio en los campos obligaría a rehacerla.

**Alcance previsto**

*Acceso y usuarios.* Acceso del personal mediante **Llave CDMX** (DEC-27), con perfiles diferenciados dentro del sistema: consulta, atención y administración. La identidad la provee la cuenta; el perfil y el área los asigna la Secretaría. El perfil de atención opera únicamente sobre las denuncias del área a la que pertenece —Dirección General de Inspección y Vigilancia Ambiental o Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural—, conforme al enrutamiento automático. Bitácora de accesos y de cambios de estado, por tratarse de un sistema con datos personales.

*Bandeja de denuncias.* Listado con folio, fecha de recepción, materia, alcaldía, tipo de zona, área que atiende, estado y días transcurridos. Ordenamiento y filtros combinables por cada uno de esos campos, más búsqueda por folio, por nombre del establecimiento y por texto de los hechos.

*Detalle de la denuncia.* Ficha completa en una sola pantalla: datos capturados, ubicación en mapa con el polígono de la zona, galería de evidencia, resultado del cruce espacial con su motivación, y bitácora de actuaciones. Desde ahí se registra el cambio de estado, se asigna a personal inspector, se turna a otra área y se generan los acuses y notificaciones.

*Estados de la denuncia.* Recepción, revisión de procedencia, integración de expediente, programación de visita, visita practicada, resolución y conclusión; más los estados de improcedencia y de turnado a otra autoridad. **Pendiente de definir con el área sustantiva.**

*Consultas y tableros.* Indicadores de operación —denuncias recibidas, atendidas y pendientes, tiempo promedio de atención, proporción de improcedentes— y de incidencia —distribución por materia, por alcaldía, por tipo de zona y por área que atiende, serie mensual, y mapa de calor de puntos denunciados—. La georreferenciación permite además cruzar la incidencia con las capas del Sistema de Información Ambiental, insumo directo para la programación de operativos.

*Exportación.* Descarga en hoja de cálculo de la bandeja filtrada y de los indicadores, para informes y respuestas a solicitudes de información.

**Condiciones previas**

1. Validación del formulario de denuncia por la Dirección General de Inspección y Vigilancia Ambiental.
2. Resolución de P-01, porque la naturaleza jurídica del canal determina los estados y los plazos que el sistema controla.
3. Definición del catálogo de estados y de los perfiles de usuario con el área sustantiva.
4. Confirmación de la estructura del folio (P-13).

**Consideración de protección de datos.** El módulo concentra datos personales de personas denunciantes y señalamientos sobre presuntos responsables. Su diseño debe contemplar control de acceso por perfil, bitácora de consultas y criterios de conservación y supresión, en los términos que determine la Unidad de Transparencia.

---

### AD-02. Seguimiento de la denuncia por la persona denunciante

**Estado: pendiente. Depende de AD-01 y no se construye antes que él: el seguimiento ciudadano sólo puede mostrar estados que el área sustantiva registre efectivamente en el módulo interno.**

AD-01 resuelve el seguimiento **interno** —la bandeja con la que el personal atiende y actualiza cada expediente—. AD-02 resuelve el seguimiento **externo**: el medio por el que la persona que denunció conoce en qué va su denuncia sin tener que llamar, escribir o acudir. Hoy el canal termina en el acuse: se entrega un folio y no existe forma de consultarlo. Es la principal causa previsible de reincidencia de la misma denuncia y de solicitudes de información sobre casos propios.

**Alcance previsto**

*Consulta con Llave CDMX.* Quien presentó la denuncia identificada entra con su cuenta (DEC-27) y ve el listado de sus folios con el estado actual, la fecha de cada cambio y el área que atiende. No requiere recordar el folio ni clave alguna: el vínculo entre cuenta y expediente lo resuelve el sistema.

*Consulta por folio sin cuenta.* Ruta alterna para la denuncia anónima: se captura el folio y la clave entregada en el acuse. Devuelve la misma información, sin dato personal alguno en pantalla.

*Estados visibles.* Subconjunto de los estados de AD-01, redactados en lenguaje ciudadano y sin exponer información reservada ni datos del presunto responsable. La equivalencia entre estados internos y estados visibles se define con el área sustantiva. **Pendiente: P-14.**

*Notificación de avance.* Cuando la persona aceptó la notificación por correo electrónico, aviso automático en cada cambio de estado relevante y al concluir. Sin ese consentimiento, la información queda disponible únicamente en la pantalla de consulta.

*Aportación posterior de información.* Desde la consulta, posibilidad de adjuntar evidencia o datos adicionales sobre el mismo folio, que ingresan al expediente como anexo fechado. Es la promesa que el propio formulario ya hace en el paso de notificación.

*Denuncia anónima.* Sin correo electrónico no hay notificación ni recuperación de folio. El acuse debe advertirlo de manera expresa y ofrecer la clave de consulta en pantalla, con la indicación de conservarla: no puede reponerse.

*Resultado final.* Al concluir, la consulta muestra el sentido de la conclusión en los términos que autorice la Unidad de Transparencia, y la vía para solicitar el expediente si la persona lo requiere.

**Condiciones previas**

1. AD-01 en operación, con catálogo de estados definido y efectivamente capturado.
2. Resolución de P-01 y P-07: sin naturaleza jurídica ni plazo de atención definidos, la pantalla de consulta no puede informar cuándo debe esperarse una respuesta.
3. Confirmación de la estructura del folio (P-13), que es la llave de consulta en la ruta sin cuenta.
4. Integración con Llave CDMX resuelta (P-15).
5. Criterio de la Unidad de Transparencia sobre qué información del expediente puede mostrarse a la persona denunciante y por cuánto tiempo se conserva la consulta.

**Riesgo si no se desarrolla.** Un canal que recibe denuncias y no informa su curso genera desconfianza, duplica expedientes y traslada la carga de seguimiento a la atención telefónica y a la Unidad de Transparencia. El formulario ya ofrece «seguir aportando información y documentos»: sin AD-02 esa oferta no puede cumplirse.

---

### Registro de respuestas

| Clave | Respuesta | Quién decidió | Fecha |
|---|---|---|---|
| P-01 | | | |
| P-02 | | | |
| P-03 | **A** · El Histórico Coyoacán no está en el convenio: todo el polígono es federal | Liber Saltijeral | 20 sep 2026 |
| P-04 | | | |
| P-05 | | | |
| P-06 | | | |
| P-07 | **En parte** · plazos del procedimiento, del Manual Administrativo; falta el plazo para informar a quien pregunta por su folio | Manual Administrativo | 20 sep 2026 |
| P-08 | | | |
| P-09 | | | |
| P-10 | **En parte** · nombres y atribuciones de las dos coordinaciones; la DGSANPAVA no recibe denuncias. Falta el fundamento en ANP federales con coadministración | Manual Administrativo | 20 sep 2026 |
| P-11 | **Resuelto en el proyecto** · normalización al ingresar la capa; el duplicado de Santa Catarina no lo era | Sistema de Información Ambiental | 20 sep 2026 |
| P-12 | | | |
| P-13 | | | |
| P-14 | | | |
| P-15 | | | |
| P-16 | | | |
| P-17 | | | |
| P-18 | **B** · lo resuelve el servidor, con lista blanca y sin seguir la redirección | Liber Saltijeral | 20 sep 2026 |
| P-19 | | | |
| P-20 | | | |
| P-21 | **En parte** · adoptados los controles 1 y 2: prueba de humanidad y límite por origen. Faltan los controles 3 a 6 | Liber Saltijeral | 20 sep 2026 |
| P-22 | | | |
