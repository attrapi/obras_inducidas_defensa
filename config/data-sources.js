// Catálogo jerárquico de fuentes de datos del sistema.
//
// El menú "Proyectos" del header se construye automáticamente a partir de
// este objeto. Para agregar una nueva fuente solo hay que pegar su URL
// publicada de Google Sheets en el campo `url`. Las entradas con `url: null`
// aparecen deshabilitadas en gris hasta que se cablee la URL real.
//
// Adapters disponibles (definidos en index.html):
//   - 'estandar': esquema de obras inducidas.
//   - 'inah'   : esquema arqueológico (UTM 14N + agrupamiento V1/V2/V3
//                como polígono cerrado).
//
// `geo` apunta a la carpeta de cartografía del corredor en geo/, generada
// desde los KML/KMZ de KMZ/ con `python tools/kml-to-geojson.py`. Cada carpeta
// trae un index.json que lista sus capas; el panel de capas se construye de
// ahí. La cartografía se dibuja al seleccionar el proyecto, independiente de
// que la hoja de obras ya esté cableada o no.
//
// Importante: las hojas publicadas de Google Sheets tardan unos minutos en
// propagar cambios. Quien actualice los datos debe saberlo.

window.DATA_SOURCES = {
  'mexico-queretaro': {
    label: 'México - Querétaro',
    geo: 'geo/mexico-queretaro/',
    adapter: 'estandar',
    url: null
  },
  'aifa-pachuca': {
    label: 'AIFA - Pachuca',
    geo: 'geo/aifa-pachuca/',
    adapter: 'estandar',
    url: null
  },
  'irapuato-guadalajara': {
    label: 'Irapuato - Guadalajara',
    geo: 'geo/irapuato-guadalajara/',
    adapter: 'estandar',
    url: null
  }
};
