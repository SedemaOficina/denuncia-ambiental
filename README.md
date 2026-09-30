# Denuncias Ambientales · Carpeta del proyecto

Formulario web de denuncia ambiental de la Secretaría del Medio Ambiente de la Ciudad de México, para la Dirección General de Inspección y Vigilancia Ambiental.

Esta carpeta está vinculada al proyecto **Denuncias Ambientales** en Claude: los entregables se escriben aquí directamente, sin descargas.

## Estructura

| Carpeta | Contenido |
|---|---|
| `prototipo/` | Prototipo navegable del formulario. Es un archivo HTML autocontenido: se abre con doble clic en el navegador. Requiere conexión a internet para el mapa base y la búsqueda por dirección. |
| `documentacion/` | Dieciocho documentos: ficha, reglas de negocio, marco jurídico, modelo de datos, decisiones y pendientes (el de referencia), mapeo de campos y ramas —generados del código—, ruta de trabajo, auditorías fechadas, análisis de la base histórica y nomenclatura de folios. Los mismos documentos están en el proyecto de Claude. |
| `capas/` | Capas del Sistema de Información Ambiental usadas por el formulario: alcaldías, Áreas de Valor Ambiental y Áreas Naturales Protegidas, suelo de conservación y, en `originales/`, colonias del IECM 2022 y la malla UGA. |
| `construccion/` | Lo que genera la versión en línea, la de GitHub Pages y los documentos 09 y 10, y las baterías de prueba. Ver su `LEEME.md`. |
| `docs/` | La versión de prueba que publica GitHub Pages. Se genera; no se edita a mano. |
| `revision/` | Apps Script de la hoja de observaciones del modo revisión (`?revision=CLAVE`) y su instalación paso a paso (DEC-153). |
| `insumos/` | Formato público vigente, propuesta de la Dirección General de Inspección y Vigilancia Ambiental y Ley Ambiental de la Ciudad de México. |

## Cómo usar el prototipo en una sesión de validación

1. Abre `prototipo/prototipo-denuncia-ambiental-sedema.html`.
2. El botón **Panel de validación**, en la esquina inferior derecha, permite exigir los campos obligatorios, simular el límite de envíos, cargar uno de los once escenarios de prueba y abrir el mapeo de campos y las ramas del formulario.
3. Mientras el formulario está en prueba, **ningún campo es obligatorio**: se puede recorrer completo sin llenar nada. La única regla que sí bloquea es la de competencia territorial.

## Configuración local

El prototipo lee la dirección del proveedor de mapa base y su clave de
`prototipo/configuracion-local.js`, que **no forma parte del repositorio**: una
clave escrita en un repositorio público queda indexada en horas.

Quien clone este repositorio no tendrá ese archivo y el mapa funcionará con el
proveedor por omisión, sin clave. Para usar el proveedor con clave, se crea el
archivo con esta forma y se pide la clave a quien administra el proyecto:

```js
var CFG_LOCAL = {
  mapa: {
    url: '<dirección de los mosaicos, con la clave>',
    atribucion: '&copy; CARTO, &copy; OpenStreetMap'
  }
};
```

La atribución al proveedor y a OpenStreetMap es **obligación de la licencia**,
no cortesía: debe quedar visible en el mapa.

## Documento de referencia

`documentacion/05-decisiones-y-pendientes.md` concentra las decisiones tomadas, las preguntas abiertas con sus opciones y recomendaciones, y el alcance diferido del módulo de administración. Es el documento que conviene llevar a la sesión con la Dirección General.
