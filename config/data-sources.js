// Catálogo jerárquico de fuentes de datos del sistema.
//
// El menú "Proyectos" del header se construye automáticamente a partir de
// este objeto. Para agregar una nueva fuente solo hay que pegar su URL
// publicada de Google Sheets en el campo `url`. Las entradas con `url: null`
// aparecen deshabilitadas en gris hasta que se cablee la URL real.
//
// Adapters disponibles (definidos en index.html):
//   - 'estandar': esquema de obras inducidas (Tramo II legacy).
//   - 'inah'   : esquema arqueológico (UTM 14N + agrupamiento V1/V2/V3
//                como polígono cerrado).
//
// Importante: las hojas publicadas de Google Sheets tardan unos minutos en
// propagar cambios. Quien actualice los datos debe saberlo.

window.DATA_SOURCES = {
  'queretaro-irapuato': {
    label: 'Querétaro - Irapuato',
    children: {
      'inah': {
        label: 'INAH',
        children: {
          'tramo-i': {
            label: 'Tramo I',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRqfqQIjo_aM3wNqz-nmldSGpAvc7pJV8vkoqQlGx3xZA4HrP8VXAHpeNLE2HVCxw/pub?gid=1971587044&single=true&output=csv'
          },
          'tramo-ii': {
            label: 'Tramo II',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQhwnRP-DRPHYKwlPe02Oh90in0PfT7I3VOailAYFVhGVXCEPvsahIypOpljdc7gg/pub?gid=1567286198&single=true&output=csv'
          },
          'tramo-iii': {
            label: 'Tramo III',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRhlO7-OWXxKz4oatI5djSc9t2fHHsf1EMtPKLL-LVU5QQ9xEBODGSa-yHFyJxKQw/pub?gid=24093312&single=true&output=csv'
          },
          'tramo-iv': {
            label: 'Tramo IV',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQaE_bz537rfB1AmX7VB6SoW-kQxXUNg6re3JFE9yq0jjQM2hnGiWeLEqCjdIlwIg/pub?gid=1701037126&single=true&output=csv'
          }
        }
      },
      'tramo-i': {
        label: 'Tramo I',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ599M1WRyy0A29IEGvluqc14k0jcObel0BP3RQ-z3w8ryr5FjmzSM1YeCoGauHyA/pub?gid=1935831653&single=true&output=csv'
      },
      'tramo-ii':  {
        label: 'Tramo II',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vToUBW-L08hKrlZ-fsOXtQSK29vYgxGJui17azAADydkjCmXlP0v2k7GjP5Sf_2pw/pub?gid=2026999666&single=true&output=csv'
      },
      'tramo-iii': {
        label: 'Tramo III',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT4nPjWU5T9qxIkM29K-d1o_QWTra5GCeI6bVJqZD7Qe6OQUrW4ZGR9MuCTUHucUQ/pub?gid=1261822212&single=true&output=csv'
      }
    }
  },
  'saltillo-monterrey': {
    label: 'Saltillo - Monterrey',
    children: {
      'inah': {
        label: 'INAH',
        children: {
          'tramo-13-14': {
            label: 'Tramo 13-14',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSbks6OG9F4SH1Ue_9qt3-4mk2A9arGzQKEXRHFGw5lq0r3H4u8NlbfSOJIG1ZYXg/pub?gid=60031769&single=true&output=csv'
          },
          'tramo-15b': {
            label: 'Tramo 15B',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSuhlYtmT4G7Z9sokHn2n1tLmB5eJvB0j4O93KrDDIpHWEi1ZqTznfmgtImfSRF6w/pub?gid=1646263905&single=true&output=csv'
          }
        }
      },
      'segmentos-13-14': {
        label: 'Segmentos 13 y 14',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQCXuNre9SGM6RGnZ5aAco1ztzIpY03LURR32NpE2E6SlHjYtZHmIarlay5mFpkdQ/pub?gid=800038218&single=true&output=csv'
      }
    }
  },
  'monterrey-nuevo-laredo': {
    label: 'Monterrey - Nuevo Laredo',
    children: {
      'inah': {
        label: 'INAH',
        children: {
          'segmentos-16-17': {
            label: 'Segmentos 16 y 17',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSsIQF5xjyL3PRpyahpK4856Z7oKv1Sz-_-M4eITpFCEV5dzwZpxMj51tdYmVJu-A/pub?gid=1831898889&single=true&output=csv'
          },
          'segmentos-18-19-20': {
            label: 'Segmentos 18, 19 y 20',
            adapter: 'inah',
            url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTNBDAO8oOh3MNNMDXHJv498Un3Lk4r-LK6oKhdctXF8cysucZbm-TvbDdtVJVAWw/pub?gid=1117185999&single=true&output=csv'
          }
        }
      },
      'segmento-15b': {
        label: 'Segmento 15B',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQHw5mPXdUn_R9GWohksMqIK90BFOb4nU7RKyVz4diF48wJRhym23h_1ryaEqLqiw/pub?gid=345548758&single=true&output=csv'
      },
      'segmento-16-17': {
        label: 'Segmento 16 y 17',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSRFZbjZQQ-Jsp51pe5s0LxcB9i8IDd1MH2z-d6LlTEvlRoC1qT79PTpSFCAVZBgw/pub?gid=1837026324&single=true&output=csv'
      },
      'segmento-18-19-20': {
        label: 'Segmento 18, 19 y 20',
        adapter: 'estandar',
        url: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT-9iXEU5DBOSJhZMv9XHMjqvmQ4o-AVEsDWTAx1QoQ4yfO6ccd8D9Cq9vOPhW9wg/pub?gid=841779046&single=true&output=csv'
      }
    }
  }
};
