# -*- coding: utf-8 -*-
"""Convierte los KML/KMZ de KMZ/ a GeoJSON en geo/.

Se corre a mano cuando cambian los archivos fuente:

    python tools/kml-to-geojson.py

Por qué un script y no parsear el KML en el navegador: los archivos originales
pesan hasta 10 MB de XML (Mexico-Queretaro.kmz trae 13 699 placemarks con
coordenadas a 13 decimales). Convertirlos una vez a GeoJSON con coordenadas
redondeadas a 6 decimales (~11 cm, de sobra para cartografía de trazo) baja el
peso ~6x y deja al navegador solo pintar. El KMZ queda en el repo como fuente
de verdad.

Salida: una carpeta por proyecto con un GeoJSON por capa más un `index.json`
que lista las capas con su etiqueta, conteo y si va prendida por default. El
split es a propósito: el panel de capas carga en diferido: al abrir un proyecto
solo baja las capas default (trazo/DDV) y las demás llegan la primera vez que
alguien las prende. Un solo archivo de 3.8 MB obligaría a bajar los 11 320
cadenamientos aunque nadie los vea.

Las geometrías NO se simplifican. Son datos de tenencia de la tierra usados
para defensa jurídica: la única pérdida aceptable es el redondeo a 6 decimales
(~11 cm) y la altitud, que ninguna capa usa.
"""
import io
import json
import os
import re
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

KML_NS = '{http://www.opengis.net/kml/2.2}'
SRC_DIR = 'KMZ'
OUT_DIR = 'geo'
PRECISION = 6

# Mapea el nombre de carpeta del KML a la llave de capa de la aplicación.
# Se compara contra el nombre normalizado (sin acentos, minúsculas); el
# primer patrón que haga match gana, así que el orden importa.
# Etiqueta visible en el panel y si la capa arranca prendida. El orden de este
# dict es el orden del panel.
CAPA_META = [
    ('trazo',                 'Trazo / envolvente de afectación', True),
    ('ddv',                   'Derecho de vía (DDV)',             True),
    ('liberados',             'Liberados',                        False),
    ('cadenamientos',         'Cadenamientos PK',                 False),
    ('frentes',               'Frentes',                          False),
    ('parcelas',              'Parcelas',                         False),
    ('nucleo-agrario',        'Núcleo agrario',                   False),
    ('propiedad-privada',     'Propiedad privada',                False),
    ('antecedentes-titulos',  'Antecedentes: títulos',            False),
    ('antecedentes-decretos', 'Antecedentes: decretos DOF',       False),
    ('otros',                 'Otros',                            False),
]

CAPA_RULES = [
    (r'trazo|envolvente', 'trazo'),
    (r'^ddv$|derecho de via', 'ddv'),
    (r'cadenamiento', 'cadenamientos'),
    (r'liberado', 'liberados'),
    (r'parcela', 'parcelas'),
    (r'nucleo agrario|nuccleo agrario', 'nucleo-agrario'),
    (r'propiedad privada|^pp f', 'propiedad-privada'),
    (r'antecedentes.*titulo', 'antecedentes-titulos'),
    (r'antecedentes.*decreto', 'antecedentes-decretos'),
    (r'frentes', 'frentes'),
]


def deaccent(s):
    """Quita acentos para que las reglas de capa no dependan del encoding.

    Los nombres de carpeta del KMZ vienen con mojibake ("NÚCLEO" llega como
    "N\ufffdCCLEO"), por eso el match se hace laxo y con fallback.
    """
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def capa_for(path, fallback):
    """Resuelve la capa recorriendo el path de carpetas de la más específica
    a la más general, para que 'TRAZO-MQ / TRAZO / F1_Envolvente' gane sobre
    cualquier ancestro. `fallback` cubre los KML cuya carpeta raíz no dice de
    qué capa se trata (ej. 'IRO - GDL_V16_100426', que es el trazo)."""
    for name in reversed(path):
        n = deaccent(name)
        for pattern, capa in CAPA_RULES:
            if re.search(pattern, n):
                return capa
    return fallback


def read_kml(path):
    if path.lower().endswith('.kmz'):
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.lower().endswith('.kml'))
            return z.read(name).decode('utf-8', 'replace')
    with io.open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def parse_coords(text):
    """KML entrega 'lon,lat[,alt] lon,lat[,alt] ...'. GeoJSON quiere [lon,lat].
    La altitud se descarta: ninguna capa la usa y duplicaría el peso."""
    out = []
    for token in text.split():
        parts = token.split(',')
        if len(parts) < 2:
            continue
        try:
            lon, lat = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        out.append([round(lon, PRECISION), round(lat, PRECISION)])
    return out


def text_of(el, tag):
    child = el.find(KML_NS + tag)
    return (child.text or '').strip() if child is not None and child.text else ''


def geometries(el):
    """Extrae geometrías GeoJSON de un Placemark (aplana MultiGeometry)."""
    geoms = []
    for node in el.iter():
        tag = node.tag.replace(KML_NS, '')
        if tag == 'Point':
            coords = parse_coords(text_of(node, 'coordinates'))
            if coords:
                geoms.append({'type': 'Point', 'coordinates': coords[0]})
        elif tag == 'LineString':
            coords = parse_coords(text_of(node, 'coordinates'))
            if len(coords) >= 2:
                geoms.append({'type': 'LineString', 'coordinates': coords})
        elif tag == 'Polygon':
            rings = []
            for boundary in ('outerBoundaryIs', 'innerBoundaryIs'):
                for b in node.findall(KML_NS + boundary):
                    ring_el = b.find(KML_NS + 'LinearRing')
                    if ring_el is None:
                        continue
                    ring = parse_coords(text_of(ring_el, 'coordinates'))
                    if len(ring) < 4:
                        continue
                    if ring[0] != ring[-1]:
                        ring.append(ring[0])
                    rings.append(ring)
            if rings:
                geoms.append({'type': 'Polygon', 'coordinates': rings})
    return geoms


def extended_data(el):
    """Rescata los SimpleData/Data del KML como propiedades del feature: son
    los que alimentan el popup (número de parcela, superficie, núcleo agrario…)."""
    props = {}
    for sd in el.iter(KML_NS + 'SimpleData'):
        name = sd.get('name')
        if name and sd.text:
            props[name] = sd.text.strip()
    for data in el.iter(KML_NS + 'Data'):
        name = data.get('name')
        value = text_of(data, 'value')
        if name and value:
            props[name] = value
    return props


def walk(el, path, features, fallback):
    for child in el:
        tag = child.tag.replace(KML_NS, '')
        if tag in ('Document', 'Folder'):
            walk(child, path + [text_of(child, 'name')], features, fallback)
        elif tag == 'Placemark':
            capa = capa_for(path, fallback)
            name = text_of(child, 'name')
            props = extended_data(child)
            if name:
                props['nombre'] = name
            for geom in geometries(child):
                features.append((capa, {'type': 'Feature', 'properties': props,
                                        'geometry': geom}))


def convert(src, out_dir, label, fallback):
    root = ET.fromstring(read_kml(src).encode('utf-8'))
    features = []
    walk(root, [], features, fallback)

    by_capa = {}
    for capa, feature in features:
        by_capa.setdefault(capa, []).append(feature)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    capas = []
    total_kb = 0.0
    for capa, capa_label, on_by_default in CAPA_META:
        feats = by_capa.pop(capa, None)
        if not feats:
            continue
        filename = capa + '.geojson'
        path = os.path.join(out_dir, filename)
        with io.open(path, 'w', encoding='utf-8') as fh:
            # separators sin espacios: ahorra ~15% sobre el default de json.dump
            fh.write(json.dumps({'type': 'FeatureCollection', 'features': feats},
                                ensure_ascii=False, separators=(',', ':')))
        size_kb = os.path.getsize(path) / 1024.0
        total_kb += size_kb
        capas.append({'key': capa, 'label': capa_label, 'file': filename,
                      'count': len(feats), 'default': on_by_default})
        print('    %-24s %-6d %7.0f KB%s' % (capa, len(feats), size_kb,
                                             '  (default)' if on_by_default else ''))
    if by_capa:
        # Si aparece una capa nueva en el KMZ, mejor que truene ruidoso aquí
        # que silenciarla: hay que darle etiqueta en CAPA_META.
        raise SystemExit('Capas sin etiqueta en CAPA_META: %s' % sorted(by_capa))

    with io.open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
        json.dump({'label': label, 'fuente': os.path.basename(src), 'capas': capas},
                  fh, ensure_ascii=False, indent=2)
    print('  total %.0f KB' % total_kb)


# archivo fuente -> (carpeta de salida, etiqueta del proyecto, capa por default)
SOURCES = [
    ('Mexico-Queretaro.kmz',      'mexico-queretaro',      'México - Querétaro',      'otros'),
    ('AIFA-Pachuca.kml',          'aifa-pachuca',          'AIFA - Pachuca',          'ddv'),
    ('Irapuato-Guadalajara.kml',  'irapuato-guadalajara',  'Irapuato - Guadalajara',  'trazo'),
]

if __name__ == '__main__':
    for src_name, out_name, label, fallback in SOURCES:
        print('%s -> %s/' % (src_name, os.path.join(OUT_DIR, out_name)))
        convert(os.path.join(SRC_DIR, src_name), os.path.join(OUT_DIR, out_name),
                label, fallback)
