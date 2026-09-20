# Formulario web de Denuncia Ambiental · Auditoría del paso «¿Dónde ocurre?»

**Versión:** 1.0 · 20 de septiembre de 2026
**Qué es este documento.** Auditoría heurística y lógica del paso 2, hecha porque quien lo construye se declaró confundido sobre cómo debe funcionar. **Esa confusión es el hallazgo, no el punto de partida:** si quien conoce cada decisión no sabe explicar el paso, nadie que llegue de la calle podrá recorrerlo.

---

## 1. Lo que el paso hace hoy

Medido sobre la versión 33, ruta con dirección: **diez campos y diecisiete controles** en una sola pantalla.

**Hay cuatro maneras distintas de colocar el punto**, más una de quitarlo:

| | Acción | Dónde está |
|---|---|---|
| 1 | Pulsar «Ubicar en el mapa» tras escribir la dirección | Botón, bajo la dirección |
| 2 | Pegar coordenadas o un enlace de mapa y pulsar «Colocar el punto» | Campo y botón, sobre el mapa |
| 3 | Dar un clic sobre el mapa | El mapa mismo |
| 4 | Arrastrar el punto ya colocado | El mapa mismo |
| — | «Quitar el punto» | Barra sobre el mapa |

Y el subtítulo del paso describe **una sola** de las cuatro: «Escribe la dirección del lugar de los hechos y colócala en el mapa».

---

## 2. El defecto de fondo

> **La alcaldía existe dos veces en el formulario, el sistema usa una para turnar y la otra para el acuse, y no exige que coincidan.**

`alcaldia` la escribe la persona. `alcaldia_punto` la calcula el cruce espacial. El **turnado** se decide por el punto (DEC-04). El **resumen y el acuse** muestran la escrita.

**Comprobado**, capturando una dirección en Coyoacán y colocando el punto dentro del Bosque de Tlalpan:

| Lo que dice el resumen | |
|---|---|
| Lugar de los hechos | Av. México 10, Del Carmen, C.P. 04100, **Coyoacán** |
| Tipo de suelo | Área Natural Protegida local — **Bosque de Tlalpan** |
| Área que atiende | **Dirección General de la Comisión de Recursos Naturales y Desarrollo Rural** |

**El formulario deja enviar esa denuncia.** El expediente nacería diciendo que los hechos ocurren en una calle de Coyoacán y, al mismo tiempo, que ocurren dentro de un Área Natural Protegida de Tlalpan, con una orden de visita dirigida a un domicilio que no está en el polígono que motivó el turnado.

Hoy el formulario **avisa** de la discrepancia y ofrece corregir la alcaldía con un botón, pero el aviso dice «revisa cuál es la correcta» y **no impide continuar**. Le pide a la persona que resuelva una contradicción que el sistema creó, sin decirle cuál de los dos datos usa para qué.

---

## 3. Los demás hallazgos

**H-1. La dirección y el punto no declaran para qué sirve cada uno.** Son dos trabajos distintos —describir el lugar con palabras y señalarlo en un mapa— presentados como si fueran el mismo. La dirección sirve para que el personal llegue y para el domicilio de la orden de visita; el punto decide qué área atiende. Mientras eso no se diga, mover el punto parece corregir la dirección, y escribir la dirección parece mover el punto.

**H-2. Dos acciones con relleno de color en la misma pantalla.** «Ubicar en el mapa» y «Continuar» compiten por ser el siguiente paso. Contradice la regla de DEC-71: una acción principal por pantalla. *(En el artefacto no se nota, porque la construcción retira ese botón; en el archivo local sí está.)*

**H-3. «Quitar el punto» sólo conduce a un error.** El punto es obligatorio. Quien lo quita queda en un estado que el formulario rechazará; para moverlo basta arrastrarlo o dar otro clic. Es una acción cuyo único destino es un mensaje de error.

**H-4. La confirmación del punto está lejos de donde se decide.** Vive dentro de la ficha del cruce, arriba. Si la persona arrastra el punto después de confirmarlo —que es justo el descuido que la confirmación previene— la casilla se destilda **fuera de su campo de visión**, y el error aparece al pulsar Continuar, abajo.

**H-5. El estado vacío no menciona la tercera vía.** Dice «captura la dirección y pulsa Ubicar, o coloca el punto sobre el mapa», y omite pegar coordenadas, que se añadió después.

---

## 4. Propuesta

### 4.1 El principio que ordena todo lo demás

Decirlo, una vez, arriba del paso:

> **La dirección sirve para que el personal de inspección llegue. El punto del mapa decide qué área de la Secretaría atiende la denuncia.**

Con eso, cada control tiene un porqué y el paso se puede explicar en una frase.

### 4.2 La alcaldía: dos salidas honestas

**Opción A — la alcaldía deja de escribirse y se deriva del punto.** Desaparece el selector. La persona escribe calle, colonia y código postal; la alcaldía la determina el punto y se muestra como resultado, no como pregunta.

*A favor:* elimina la contradicción de raíz, no la administra. Quita un campo obligatorio. Y reconoce algo cierto: **los límites de alcaldía no se conocen con precisión** —Coyoacán con Benito Juárez, Tlalpan con Xochimilco—, de modo que se está pidiendo un dato que el sistema conoce mejor que quien lo escribe.
*En contra:* si el mapa no carga, no hay alcaldía. Lo cubre el aviso que ya existe: la Secretaría georreferencia el sitio al recibirla.

**Opción B — se conserva escrita, y al continuar el formulario obliga a resolver.** Si difieren, no se avanza hasta elegir cuál vale, y se guarda una sola.

*A favor:* conserva el dato tal como lo da el formato vigente.
*En contra:* mantiene dos fuentes para lo mismo y añade una puerta más al recorrido.

**Recomendación: A.**

### 4.3 El resto

| | Cambio |
|---|---|
| **Dos bloques rotulados** | «La dirección del lugar» y «El punto en el mapa», cada uno con su propósito escrito |
| **Una sola acción principal** | «Ubicar en el mapa» pasa a secundario; «Continuar» queda como única con relleno |
| **Las tres vías, juntas** | Buscar por dirección, pegar coordenadas o enlace, o dar clic en el mapa: enunciadas en el mismo sitio y con el mismo peso |
| **Sin «Quitar el punto»** | Para moverlo se arrastra o se da otro clic |
| **La confirmación, junto a Continuar** | Se lee inmediatamente antes de actuar, y el error aparece donde la persona está mirando |

---

## 5. Lo que esta auditoría no resuelve

La geocodificación depende de un servicio externo y sigue sin decidirse (P-12). Mientras no se resuelva, **la vía más fiable para colocar el punto es el clic en el mapa**, que no depende de nadie, y el diseño debería tratarla como tal y no como el último recurso.
