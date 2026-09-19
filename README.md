# Denuncias Ambientales · Carpeta del proyecto

Formulario web de denuncia ambiental de la Secretaría del Medio Ambiente de la Ciudad de México, para la Dirección General de Inspección y Vigilancia Ambiental.

Esta carpeta está vinculada al proyecto **Denuncias Ambientales** en Claude: los entregables se escriben aquí directamente, sin descargas.

## Estructura

| Carpeta | Contenido |
|---|---|
| `prototipo/` | Prototipo navegable del formulario. Es un archivo HTML autocontenido: se abre con doble clic en el navegador. Requiere conexión a internet para el mapa base y la búsqueda por dirección. |
| `documentacion/` | Ficha del proyecto, reglas de negocio, marco jurídico, modelo de datos y documento de decisiones y pendientes. Los mismos documentos están en el proyecto de Claude. |
| `capas/` | Capas del Sistema de Información Ambiental usadas por el formulario: alcaldías, Áreas de Valor Ambiental y Áreas Naturales Protegidas, y suelo de conservación. |
| `insumos/` | Formato público vigente, propuesta de la Dirección General de Inspección y Vigilancia Ambiental y Ley Ambiental de la Ciudad de México. |

## Cómo usar el prototipo en una sesión de validación

1. Abre `prototipo/prototipo-denuncia-ambiental-sedema.html`.
2. El botón **Panel de validación**, en la esquina inferior derecha, permite comparar las variantes de identificación, activar la obligatoridad de campos, abrir el comparativo de campos y cargar un caso de ejemplo.
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
