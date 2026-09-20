# Formulario web de Denuncia Ambiental · Resistencia al abuso

**Versión:** 1.0 · 20 de septiembre de 2026
**Origen:** prueba del formulario en operación de la Procuraduría Ambiental y del Ordenamiento Territorial, en la que se envió una denuncia con todos los campos llenos de caracteres al azar sin que el sistema lo impidiera.

---

## 1. El hallazgo

Un formulario público de denuncia admite hoy, en la Ciudad, el envío de un expediente sin contenido. No hay validación de forma ni de fondo: basta pulsar enviar. La consecuencia no es una pantalla fea; es que **una sola persona con un guion puede abrir mil expedientes en una hora**, y cada uno de ellos, una vez recibido, es un asunto que la autoridad tiene que registrar, valorar y concluir.

El riesgo tiene dos caras distintas, que conviene no confundir:

| | Quién | Qué produce | Cómo se contiene |
|---|---|---|---|
| **Descuido** | Persona de buena fe con prisa, o que no sabe qué escribir | Denuncias pobres: relatos de una línea, direcciones sin colonia, puntos mal puestos | Se contiene **en el navegador**, ayudando a escribir mejor |
| **Mala fe** | Quien quiere saturar, desacreditar el canal o dirigir inspecciones contra un tercero | Denuncias masivas, duplicadas o dirigidas | Se contiene **en el servidor**. El navegador no participa |

Toda la discusión que sigue depende de esa separación.

## 2. Por qué el navegador no defiende

Las validaciones que corren en la página —longitud mínima, formato del correo, campos obligatorios— se ejecutan en la computadora de quien denuncia, y esa computadora es suya. Puede abrir las herramientas del navegador y borrarlas, o ignorar la página por completo y enviar la petición directamente al servidor. **Cualquier control que viva sólo en el navegador es una sugerencia.**

De ahí la regla que gobierna este documento: el formulario valida para **ayudar**, el servidor valida para **defender**, y lo que el servidor no revise no está revisado. Ninguna de las medidas de la sección 4 tiene sentido si el servidor no repite por su cuenta la validación que la pantalla ya hizo.

## 3. Lo que ya quedó hecho en el prototipo

| Control | Qué detiene | Dónde vive |
|---|---|---|
| Relato mínimo de 40 caracteres | El campo vacío o de una palabra | Navegador |
| **Prueba de texto legible** (DEC-80) | El relleno de teclado: mide palabras, proporción de vocales y caracteres repetidos | Navegador |
| Mensaje de error que dice el motivo | Que la persona reintente a ciegas | Navegador |
| Punto obligatorio dentro de la Ciudad, verificado contra las capas | La denuncia sin lugar, o fuera de competencia territorial | Navegador; **debe repetirse en el servidor** |
| Formato de código postal, correo y teléfono | Datos de contacto inservibles | Navegador |
| Protesta de decir verdad, expresa | Nada por sí sola; sostiene la consecuencia jurídica | Navegador |

La prueba de texto legible se diseñó con un criterio explícito: **no castigar a quien escribe mal**. Un relato con faltas de ortografía, sin acentos y sin puntuación pasa; lo que no pasa es una cadena sin vocales o una tecla repetida. Está comprobado con ambos casos en la batería 06.

## 4. Lo que debe decidirse antes de operar (P-21)

Seis controles, ordenados por relación entre lo que cuestan y lo que evitan.

**1. Prueba de humanidad en el envío.** Un desafío al pulsar «Enviar denuncia». Detiene el envío automatizado, que es el único modo de producir miles de denuncias. Costo para la persona: un segundo. Conviene la variante que no exige resolver acertijos visuales, por accesibilidad. *Es el control de mayor efecto por unidad de molestia.*

**2. Límite por origen y por ventana de tiempo.** Un número máximo de denuncias por dirección de red y por sesión en una hora y en un día. No impide la denuncia legítima —nadie presenta veinte denuncias distintas en una hora— y convierte el ataque masivo en un ataque lento. Debe contemplar la excepción de la red compartida: una oficina o un café con muchos usuarios salen por la misma dirección.

**3. Verificación del correo antes de emitir el folio.** En la ruta identificada, el folio se entrega cuando la persona confirma el correo. Encarece el envío masivo porque exige un buzón real por denuncia. **No aplica a la ruta anónima**, y ahí está el límite del control: el anonimato es un valor del canal y no puede sacrificarse a la comodidad de la defensa.

**4. Detección de duplicados.** Misma materia, mismo punto dentro de un radio corto, misma ventana de días: en lugar de abrir un expediente nuevo, se acumula al existente y se registra como denuncia adicional. **Es el control que más trabajo ahorra**, y además mejora el expediente legítimo: diez vecinos denunciando el mismo taller valen más juntos que separados.

**5. Umbral de ráfaga.** Cuando el número de denuncias sobre un mismo punto o un mismo establecimiento supera lo ordinario en poco tiempo, el sistema no rechaza: **marca**. Una campaña organizada contra un negocio y una verdadera indignación vecinal se ven igual en los datos, y sólo una persona puede distinguirlas.

**6. Puntaje de completitud.** Cada denuncia recibe un valor según lo que trae: relato sustantivo, fotografías, punto confiable, datos del responsable, persona identificada. **No sirve para rechazar, sirve para ordenar la cola.** Es lo que permite que la denuncia bien hecha se atienda antes, que es el incentivo correcto.

## 5. Lo que no debe hacerse

**No rechazar por sospecha.** La autoridad no puede negarse a recibir. Una denuncia mal escrita, anónima o poco creíble sigue siendo información, y el artículo 280 de la Ley Ambiental le permite a la Secretaría actuar con la información que reúna, venga de donde venga. La defensa legítima no es cerrar la puerta: es **ordenar la fila y acumular lo repetido**.

**No exigir identificación para denunciar.** Sería la defensa más eficaz y la más costosa: cerraría el canal a quien denuncia a su patrón, a su casero o a su vecino, que es exactamente quien más lo necesita.

**No confiar en el navegador.** Ver la sección 2.

**No publicar el umbral.** Los números de los controles 2 y 5 no van en el aviso ni en la ayuda del formulario: quien conoce el umbral lo bordea.

## 6. Cómo se sabe si funciona

Tres indicadores, que el Sistema de Información Ambiental puede producir desde el primer mes:

1. **Proporción de denuncias concluidas sin materia** sobre el total recibido. Es la medida directa del ruido que llega.
2. **Expedientes acumulados por duplicado** sobre expedientes abiertos. Mide lo que el control 4 ahorra.
3. **Tiempo entre la recepción y la primera valoración**, comparado entre denuncias de puntaje alto y bajo. Si no hay diferencia, el control 6 no está operando.

## 7. Qué pasa si aun así ocurre

Conviene tener escrito de antemano qué se hace el día que lleguen diez mil denuncias en una noche, porque ese día no hay tiempo de decidirlo:

1. Se activa el umbral de ráfaga y las denuncias del episodio quedan en una cola aparte, **sin dejar de recibirse ni de acusarse**.
2. Se revisa una muestra. Si el episodio es real —una fuga, un incendio, una tala masiva—, la cola aparte se vuelve una prioridad, no un descarte.
3. Si es una campaña, los expedientes se acumulan en uno solo y se documenta el episodio. El canal no se cierra.
4. Se informa a la Titular con el número, el punto y el sentido del episodio, antes de que lo haga otro.

---

*Este documento responde a P-21 y se actualiza con la decisión que se tome sobre cada uno de los seis controles.*
