# Cartografía (`geo/`)

Esta carpeta es **generada**. No se edita a mano.

## De dónde sale

Los archivos fuente son los KML/KMZ de `KMZ/`, tal como los entregó el área
técnica. Esos son la fuente de verdad y se quedan en el repo como evidencia.
El convertidor los pasa a GeoJSON:

```
python tools/kml-to-geojson.py
```

Se corre cada vez que cambie un KML/KMZ. El resultado se commitea junto con el
archivo fuente que lo originó.

## Por qué GeoJSON y no leer el KML en el navegador

`Mexico-Queretaro.kmz` son 10.8 MB de XML con 13 699 placemarks y coordenadas a
13 decimales. Convertirlo una vez, redondeando a 6 decimales (~11 cm) y tirando
la altitud, baja el peso ~6x y deja al navegador solo pintar en vez de parsear
XML en cada carga.

**Las geometrías no se simplifican.** Son datos de tenencia de la tierra que se
usan para defensa jurídica: la única pérdida aceptable es ese redondeo.

## Estructura

Una carpeta por corredor, un archivo por capa, más un `index.json`:

```
geo/
├── mexico-queretaro/
│   ├── index.json                   # catálogo de capas del corredor
│   ├── trazo.geojson                # (default) 2 363 líneas
│   ├── liberados.geojson            #     180 polígonos
│   ├── cadenamientos.geojson        #  11 320 puntos (cada 20 m)
│   ├── frentes.geojson              #      13 puntos
│   ├── parcelas.geojson             #     778 polígonos
│   ├── nucleo-agrario.geojson       #      75 polígonos
│   ├── propiedad-privada.geojson    #     508 polígonos
│   ├── antecedentes-titulos.geojson #     550 polígonos
│   └── antecedentes-decretos.geojson#      24 polígonos
├── aifa-pachuca/
│   ├── index.json
│   └── ddv.geojson                  # (default) derecho de vía, 258.3 ha
└── irapuato-guadalajara/
    ├── index.json
    └── trazo.geojson                # (default) 2 líneas
```

El split por capa existe para cargar en diferido: al abrir un corredor solo
bajan las capas marcadas `default` (trazo / DDV); las demás llegan la primera
vez que alguien las prende en el panel "Capas del proyecto". Un solo archivo
de 3.5 MB obligaría a bajar los 11 320 cadenamientos aunque nadie los vea.

`index.json` es lo que lee el panel:

```json
{
  "label": "México - Querétaro",
  "fuente": "Mexico-Queretaro.kmz",
  "capas": [
    {"key":"trazo","label":"Trazo / envolvente de afectación",
     "file":"trazo.geojson","count":2363,"default":true}
  ]
}
```

## Agregar un corredor

1. Deja el KML/KMZ en `KMZ/`.
2. Agrégalo a `SOURCES` en `tools/kml-to-geojson.py` (archivo, carpeta de
   salida, etiqueta, y la capa por default para los KML cuya carpeta raíz no
   diga de qué capa se trata).
3. Corre el convertidor.
4. Apunta el proyecto a su carpeta con el campo `geo` en
   `config/data-sources.js`.

Si el KMZ trae una carpeta que no cae en ninguna regla de `CAPA_RULES`, el
convertidor truena nombrándola: hay que darle su regla y su etiqueta en
`CAPA_META`. Es a propósito — una capa sin etiqueta se perdería en silencio.
