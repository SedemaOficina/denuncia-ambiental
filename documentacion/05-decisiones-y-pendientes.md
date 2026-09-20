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
| DEC-30 | Nombrar como autoridad competente a la **dirección general** y no a la coordinación, con fundamento verificado en el Reglamento Interior del Poder Ejecutivo | 18 sep 2026 | El art. 191, fracc. III, acota a la DGIVA a suelo urbano y Áreas de Valor Ambiental, y el art. 188, fracc. XXXIX a XLI, faculta a la DGCORENADR en suelo de conservación y Áreas Naturales Protegidas, donde además la fracc. XXXVIII le atribuye recibir denuncias ciudadanas. La Coordinación de Inspección y Vigilancia no figura en el Reglamento Interior: mientras su atribución no se verifique en el Manual Administrativo, el acto de turnado debe dirigirse a la unidad que sí tiene facultad reglamentaria |
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

*Por qué importa.* La capa entregada contiene nueve Áreas Naturales Protegidas federales y el catálogo de convenios enumera ocho. La diferencia es El Histórico Coyoacán, y es el único sitio de la Ciudad que el formulario deriva hoy a la PROFEPA.

*Opciones.* A. Confirmar que efectivamente no está cubierta. B. Incorporarla al catálogo si la omisión fue involuntaria.

*Bloquea:* regla RN-05.

---

**P-04. ¿Cómo se turna una denuncia cuando concurren decreto federal y local sobre la misma superficie?**

*Por qué importa.* Cerro de la Estrella y Sierra de Guadalupe tienen decreto federal y local traslapados. El prototipo da precedencia al federal y advierte la concurrencia, pero no es una regla adoptada.

*Opciones.* A. Precedencia federal con vista al área local. B. Precedencia local por tratarse de superficie coadministrada. C. Turnado simultáneo a ambas.

*Recomendación.* Opción B para las ocho coadministradas, por ser superficie sobre la que la Secretaría ya ejerce atribuciones.

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

*Bloquea:* regla RN-29 y los textos del acuse.

---

**P-08. ¿Cuáles son los datos de contacto de las instancias receptoras por derivación?**

*Detalle.* Se requieren teléfono y liga vigentes de: Secretaría de Obras y Servicios, Secretaría de Seguridad Ciudadana, PAOT, PROFEPA, INVEA, Agencia de Atención Animal y las dieciséis alcaldías. Hoy aparecen marcados como pendientes en el prototipo.

*Bloquea:* las pantallas de derivación.

---

**P-09. ¿Cuáles son los domicilios vigentes de las dos unidades que atienden y el de recepción de denuncias?**

*Por qué importa.* Hoy conviven dos domicilios contradictorios en los canales oficiales: el formato en PDF señala **Tlaxcoaque No. 8** y el portal remite al **Bosque de San Juan de Aragón**. A eso se suma que, desde que el turnado se decide por el tipo de suelo, **la unidad que atiende ya no siempre es la misma**: una denuncia en suelo urbano la sigue la Dirección General de Inspección y Vigilancia Ambiental, y una en suelo de conservación o Área Natural Protegida la sigue la Coordinación de Inspección y Vigilancia de la DGCORENADR. Si sus domicilios son distintos, el formulario y el acuse deben decirle a cada persona a dónde acudir, y no a una dirección genérica.

*Lo que hay que validar, con domicilio completo, horario y teléfono:*

| Unidad | Dato por confirmar |
|---|---|
| **Recepción de denuncias** | Domicilio y horario de la Oficialía de Partes que recibe. Si es única para ambas direcciones generales, basta uno; si cada una recibe por su cuenta, son dos |
| **Dirección General de Inspección y Vigilancia Ambiental** | Domicilio de atención al público, horario y teléfono |
| **Coordinación de Inspección y Vigilancia · DGCORENADR** | Domicilio de atención al público, horario y teléfono. Conviene precisar si atiende en la sede de la dirección general o en oficinas en suelo de conservación |

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

---

**P-11. ¿Quién normaliza las categorías de `geometrias.geojson`?**

*Estado.* El prototipo ya normaliza la acentuación para el despliegue, pero la corrección de fondo corresponde a la capa de origen.

*Detalle.* Existen inconsistencias de acentuación —"Zona Ecologica y Cultural" frente a "Zona Ecológica y Cultural"; "Zona Sujeta a Conservacion Ecologica" frente a su forma acentuada— y la Sierra de Santa Catarina aparece duplicada como Zona de Conservación Ecológica y como Zona Sujeta a Conservación Ecológica. Impide agrupar por categoría sin limpieza previa.

---

**P-12. ¿Con qué servicio se resolverán la geocodificación y el cruce espacial en la versión funcional?**

*Por qué importa.* El prototipo usa un servicio externo para proponer colonia, código postal y calle, y resuelve el cruce en el navegador con geometrías simplificadas. Ninguna de las dos cosas es admisible en producción: el cruce debe resolverse en servidor contra las capas completas y la geocodificación debe apoyarse en un servicio propio.

*Severidad elevada el 18 de septiembre de 2026.* Con la dirección capturada primero y el punto propuesto a partir de ella (DEC-37), la geocodificación dejó de ser una mejora y **sostiene el flujo**: sin ella la persona debe colocar el punto a mano en todos los casos. El formulario lo permite y lo dice —ningún servicio externo puede dejar la pantalla inservible—, pero es una degradación notable de la experiencia.

*Se relaciona con:* **P-16**, catálogo oficial de colonias y códigos postales.

*Bloquea:* la fase 2 y la calidad del paso 2 desde ahora.

---

**P-13. ¿Cuál es la estructura definitiva del folio y cómo se administra el consecutivo?**

*Supuesto del prototipo.* `SEDEMA/DGIVA/DEN/AAAA/NNNNNN`. Debe confirmarse si el consecutivo es único o se segmenta por área competente, dado que una parte de las denuncias se turna a la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural.

*Bloquea:* la fase 2.

---

**P-14. ¿Qué estados del expediente pueden mostrarse a quien denunció, con qué redacción, y hasta cuándo permanece disponible la consulta?**

*Por qué importa.* El seguimiento ciudadano (AD-02) no puede mostrar el estado interno tal cual: hay etapas cuya difusión compromete la diligencia de la visita de inspección o expone datos del presunto responsable. Se requiere una equivalencia autorizada entre los estados operativos y los estados públicos.

*A quién corresponde.* Dirección General de Inspección y Vigilancia Ambiental y Coordinación de Inspección y Vigilancia de la Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural, con opinión de la Unidad de Transparencia.

*Bloquea:* el desarrollo de AD-02.

---

**P-15. ¿Cómo se integra el formulario con Llave CDMX y qué ocurre con la denuncia anónima?**

*Por qué importa.* Son dos cuestiones distintas y ambas condicionan el diseño.

1. *Técnica.* Debe confirmarse con la Agencia Digital de Innovación Pública el mecanismo de integración, los datos que la cuenta entrega a la dependencia —nombre, CURP, correo, domicilio— y si el acceso del personal servidor público se resuelve por la misma vía o por una distinta. Debe confirmarse también la relación con la identidad digital nacional «Llave MX» y cuál de las dos, o ambas, se acepta.
2. *De diseño.* Exigir cuenta para denunciar es incompatible con la denuncia anónima, que el formulario ofrece hoy. La ruta propuesta conserva las dos: denuncia **identificada** con Llave CDMX —prellena los datos, vincula el folio a la cuenta y habilita el seguimiento y la notificación— y denuncia **anónima** sin cuenta, con folio y clave en pantalla, sin notificación y sin recuperación. Si la Dirección General decide que la cuenta sea obligatoria, la denuncia anónima desaparece del canal y debe resolverse P-05 en ese sentido.

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
| P-03 | | | |
| P-04 | | | |
| P-05 | | | |
| P-06 | | | |
| P-07 | | | |
| P-08 | | | |
| P-09 | | | |
| P-10 | | | |
| P-11 | | | |
| P-12 | | | |
| P-13 | | | |
| P-14 | | | |
| P-15 | | | |
| P-16 | | | |
| P-17 | | | |
