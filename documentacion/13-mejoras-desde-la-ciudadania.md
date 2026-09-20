# Formulario web de Denuncia Ambiental · Mejoras desde la mirada de quien denuncia

**Versión:** 1.0 · 19 de septiembre de 2026
**Qué es este documento.** Propuestas, no decisiones. Ninguna está implementada. Cada una indica qué pasa hoy, qué se propone, qué cuesta y a quién corresponde resolverla.

**Desde dónde está escrito.** La persona típica no está en un escritorio: está **en la calle, frente al problema, con el teléfono en una mano**, probablemente molesta y a veces con miedo de que la vean. Tiene tres minutos. Ése es el usuario contra el que hay que medir cada pantalla.

---

## Lo que mide el formulario hoy

Medido sobre la versión 24, en pantalla de teléfono de 390 × 760 px.

| Paso | Alto | En pantallas de teléfono | Entradas | Palabras |
|---|---|---|---|---|
| 1 · Qué denuncias | 2 251 px | 3.0 | 21 botones | 272 |
| 2 · Dónde ocurre | **3 609 px** | **4.7** | 11 | 513 |
| 3 · Qué ocurre | 2 969 px | 3.9 | 8 | 462 |
| 4 · Pruebas | 838 px | 1.1 | 2 | 93 |
| 5 · Tus datos | 1 993 px | 2.6 | 6 | 220 |
| 6 · Revisión | 2 273 px | 3.0 | — | 161 |
| **Total** | **13 933 px** | **18.3** | | **1 721** |

**Tres lecturas de esta tabla.**

1. **El recorrido completo son más de dieciocho pantallas de teléfono.** No es escandaloso para un trámite, pero sí es el presupuesto que hay que administrar: cada pantalla que se ahorre se nota.
2. **El paso 2 es el cuello de botella**: casi cinco pantallas y 513 palabras para responder «¿dónde?». Es, además, el paso donde la persona está de pie en la calle.
3. **Las pruebas son el paso más corto**, 1.1 pantallas, y llegan al final. Es exactamente al revés de lo que valen: una fotografía sostiene la presunción fundada del artículo 280 mejor que tres párrafos de descripción.

La ruta mínima —anónima, sin establecimiento, responsable desconocido— baja el paso 5 a 957 px, pero **el paso 2 sigue pesando 3 346 px**: el problema no es lo que se pregunta de más, es la estructura del paso.

---

## Las propuestas, por cuánta gente pierden

### M-01 · Decir en la primera pantalla que se puede denunciar sin dar el nombre
**Coste: una línea de texto. Es la propuesta con mejor relación entre esfuerzo y efecto.**

Quien teme a su vecino, al dueño del taller de la esquina o a quien ordenó la obra, **abandona antes de empezar**. Hoy la posibilidad de denunciar de forma anónima aparece hasta el paso 5, después de dieciséis pantallas de inversión. Quien tenía miedo nunca llegó ahí.

*Se propone* una línea en la pantalla de inicio: «Puedes presentar tu denuncia sin dar tu nombre.» Y, junto a ella, la otra mitad del mensaje: que identificarse permite dar seguimiento.

---

### M-02 · Dejar de pedirle a la ciudadanía que clasifique como abogada
**Coste: revisión del catálogo con el área sustantiva. Decisión de la Dirección General.**

La primera pantalla ofrece dieciocho supuestos más siete derivaciones: **veinticinco cosas que leer** antes de poder avanzar. Y algunas parejas sólo se distinguen por un dato que la persona no tiene: «Tala o desmonte de vegetación» frente a «Daño a arbolado urbano» se separan por el tipo de suelo —y **el tipo de suelo lo resuelve el mapa en el paso siguiente**—.

Es pedirle a quien denuncia que haga el trabajo que el sistema ya sabe hacer.

*Se propone*, en orden de ambición:

1. **Fundir las parejas que sólo difieren por la zona** y dejar que el cruce espacial las separe después. Reduce el catálogo sin perder información.
2. **Ordenar por frecuencia real** de denuncia, no por materia jurídica, y dejar el resto bajo «Ver todos los supuestos».
3. **Permitir describir con palabras propias** y proponer el supuesto a partir de esa descripción, con la opción de corregirlo.

---

### M-03 · Partir el paso 2 y esconder lo accesorio
**Coste: bajo. Es reorganización, no funcionalidad nueva.**

Casi cinco pantallas para responder «¿dónde?». El paso contiene cuatro cosas distintas: la dirección, el mapa, las referencias adicionales y la identificación del establecimiento.

*Se propone* dejar a la vista **sólo la dirección y el mapa**, y plegar «Referencias adicionales» y «Identificación del sitio» tras un «Añadir más datos del lugar», como ya se hizo con permisos y gestiones previas. Quien tenga algo que aportar lo abre; quien no, avanza.

---

### M-04 · Ofrecer «los hechos ocurren donde estoy ahora»
**Coste: bajo. Reabre una decisión anterior, con distinto encuadre.**

El botón de geolocalización se retiró deliberadamente (DEC-13) por una razón correcta: el lugar de los hechos rara vez coincide con dónde está quien denuncia. Pero hay un caso muy frecuente en el que sí coincide: **la persona está parada frente al problema**.

*Se propone* una opción secundaria, explícita y nunca automática, con ese encuadre exacto: «Los hechos ocurren donde estoy ahora». No sustituye a la dirección; propone el punto y la persona confirma.

---

### M-05 · Sustituir la caja en blanco por preguntas pequeñas
**Coste: medio. Cambia el modelo de datos de un campo.**

«Descripción de los hechos», con mínimo de cuarenta caracteres, es el campo más difícil del formulario: una caja vacía y la obligación de llenarla. Quien no sabe cuánto escribir, escribe poco; quien escribe poco, recibe un expediente débil.

*Se propone* una de dos:

1. **Dos o tres preguntas pequeñas** que se compongan en la descripción: qué está pasando, cómo se nota, a quién afecta.
2. **Un ejemplo propio de cada supuesto**, aprovechando que cada materia ya tiene su descripción en el catálogo: para tala, «Están cortando un árbol grande en la banqueta, sin lona ni aviso visible».

La segunda cuesta casi nada y resuelve la mayor parte del problema.

---

### M-06 · Pedir la fotografía cuando la persona está frente al hecho
**Coste: medio. Mueve un paso de lugar.**

La evidencia llega en el paso 4, después de lo difícil. Para entonces la persona puede estar ya en su casa, en el metro, o haber perdido el impulso. **La fotografía se toma cuando se ve el problema, no diez minutos después.**

*Se propone* ofrecer la cámara **en el paso 3, justo después de describir**, conservando el paso 4 para quien quiera añadir más. El dato más valioso del expediente no debería estar detrás de la parte más pesada del formulario.

---

### M-07 · Quitar la palabra «opcional» de casi todas partes
**Coste: bajo, pero toca muchas pantallas.**

La palabra «opcional» aparece **veintiocho veces** en el recorrido completo. Cuando casi todo es opcional, la palabra deja de significar algo y el formulario **parece más largo de lo que es**.

*Se propone* invertir la lógica: mostrar lo necesario, y poner lo demás tras «Añadir más detalles». Así **nada a la vista necesita marcarse**, porque todo lo visible o hace falta o la persona eligió abrirlo.

---

### M-08 · Decir qué pasa después
**Coste: una redacción. Depende de P-01 y P-08.**

La pregunta que toda persona se hace antes de invertir diez minutos es **«¿me van a hacer caso?»**. Hoy el formulario no la responde en ningún momento.

*Se propone* una secuencia breve en la pantalla de inicio y en el acuse: se revisa, se programa la visita, se te informa. Aunque el plazo siga pendiente de confirmar, **describir el camino ya cambia la disposición de quien denuncia** — y es una promesa institucional, así que debe revisarla el área sustantiva.

---

### M-09 · Pasar todas las etiquetas por la prueba de la conversación
**Coste: bajo. Sólo redacción.**

Quedan términos de oficio: «presuntos responsables», «temporalidad», «gestiones previas», «elementos probatorios», «materia». Algunos ya se suavizaron; el resto no.

*La prueba:* leer la etiqueta en voz alta a alguien que no trabaja en gobierno. Si hay que explicarla, se cambia. «Presuntos responsables» → «¿Quién lo está haciendo?». «Elementos probatorios» → «Fotos o videos».

---

### M-10 · Plegar la revisión final
**Coste: bajo.**

Tres pantallas repitiendo todo lo capturado. Sirve para dar confianza, pero es mucho para leer al final.

*Se propone* plegarla por bloques, con el resumen de una línea visible y el detalle a un clic, y un enlace para corregir cada bloque sin salir de la pantalla.

---

## Lo que ya está bien y conviene no tocar

- **Elegir el supuesto avanza solo**, sin botón al final (DEC-22).
- **Las preguntas filtro** de permisos y gestiones previas: sólo ve el campo largo quien tiene algo que aportar.
- **La ruta anónima es de verdad corta**: el paso 5 baja de 1 993 a 957 px.
- **El punto no reescribe la dirección** (DEC-41): una sola dirección de flujo, sin sorpresas.
- **El recordatorio fijo** de qué se está denunciando (DEC-43).
- **La regla de competencia bloquea siempre**, incluso en pruebas.

---

## Orden sugerido

| Primero, cuesta poco y rinde mucho | M-01, M-07, M-09, M-03 |
| Después, con el área sustantiva | M-02, M-08 |
| Cuando haya decisión de diseño | M-04, M-05, M-06, M-10 |

**M-01 debería hacerse hoy**: es una línea de texto y es lo único de esta lista que recupera a alguien que hoy se va antes de empezar.
