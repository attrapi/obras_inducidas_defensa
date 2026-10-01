# CONTEXT.md — Sistema de Obras Inducidas (ATTRAPI)

> Este archivo contiene el contexto necesario para que Claude Code (o cualquier desarrollador) retome el proyecto sin perder tiempo. **Léelo completo antes de proponer cambios.**

---

## 1. Quién soy yo (Dan)

- **Nombre:** Daniel de la Garza Cordero
- **Rol:** Enlace de la Subdirección de Procesos Administrativos de Construcción
- **Institución:** ATTRAPI (Agencia de Transformación Regulatoria del Transporte Ferroviario y Portuario)
- **Cuenta GitHub institucional:** `attrapi`
- **Jefe directo:** Ing. Mario Alberto Ramírez Franca (Subdirector)
- **Director:** Ing. Adrián Tavares Echegaray (Director de Procesos Administrativos de Construcción)
- **Estilo de trabajo:** iterativo, testable, prefiero ver resultados pronto y ajustar. Comunicación directa, español casual con mayúsculas para énfasis. Cuestiono asunciones y prefiero entender el "por qué" antes que solo el "qué".

---

## 2. Contexto institucional del proyecto

Este sistema nació como un **mapa interactivo de obras inducidas** para apoyar la gestión de proyectos ferroviarios bajo supervisión de ATTRAPI. Se desarrolló dentro del horario laboral, con recursos institucionales, bajo el repositorio organizacional `attrapi` en GitHub. **La titularidad patrimonial es de ATTRAPI** (LFDA art. 84). La autoría material es mía y queda evidenciada en el historial de commits.

Versión previa en producción: `https://attrapi.github.io/Obras_inducidas_tramo2/` (mapa de Tramo II Querétaro–Irapuato, 178 obras). Ese repo queda intacto como evidencia y línea base; este nuevo repo es la evolución institucional del sistema.

**Estratégicamente, este repo busca:**
- Consolidar el desarrollo como producto institucional de ATTRAPI (no de un proveedor externo).
- Convertir el "mapa" en un **sistema operativo de gestión** (datos vivos, estados editables, bitácora auditable).
- Escalar a múltiples tramos ferroviarios sin reescribir desde cero.
- Mantenerlo accesible, mantenible, y comprensible por cualquier persona dentro de ATTRAPI.

---

## 3. Decisiones técnicas ya tomadas (NO revisitar sin razón fuerte)

### Stack
- **HTML/CSS/JS vanilla** (NO React, NO Vue, NO frameworks de build).
- **Leaflet 1.9.4** para cartografía (CDN cdnjs).
- **PapaParse** para parseo CSV (a integrar; actualmente parser manual).
- **html2canvas + jsPDF** para exportación PDF (ya integrados).
- **Chart.js** (a integrar para dashboard analítico).
- **Bootstrap 5** (opcional, solo si se requieren componentes complejos).
- **Google Sheets** como base de datos viva (publicación CSV).
- **Google Apps Script** para capa de escritura (etapa posterior).

### Por qué HTML vanilla y no React
- Cero build step, cero dependencias de Node en producción.
- Mantenible por cualquier persona en ATTRAPI sin entorno especializado.
- Despliegue trivial en GitHub Pages.
- El código fuente legible refuerza la trazabilidad institucional (vs. builds compilados).
- React no aporta valor funcional real para este tipo de sistema (mapa + filtros + dashboard).

### Hosting
- GitHub Pages bajo la cuenta organizacional `attrapi`.
- Dominio: `attrapi.github.io/<repo>/`.

### Convenciones
- Nombres de archivos en `kebab-case`.
- Indentación 2 espacios.
- Comentarios explicando el **por qué**, no el **qué**.
- Commits descriptivos en español, una idea por commit.
- Idioma de UI: español (México).
- Formato numérico: `es-MX` con separadores correctos.
- Coordenadas: WGS84 para visualización, UTM Zona 14N para datos técnicos.
- Encoding: UTF-8 (Google Sheets entrega UTF-8 nativo; el CSV legacy de Tramo II venía en windows-1252).

---

## 4. Estado actual del sistema (qué está hecho)

**Datos de obras inducidas:**
- Carga CSV-driven desde Google Sheets publicado, con catálogo en
  `config/data-sources.js` (menú "Proyectos" construido automáticamente).
- Parser CSV manual con manejo de comillas y comas escapadas.
- Dos adapters: `estandar` (obras inducidas) e `inah` (vestigios arqueológicos,
  UTM 14N y agrupamiento de vértices V1/V2/V3 como polígono cerrado).
- Normalización de estatus, criticidad y tipo de obra (alias por acentos).
- Modelo de 19 campos por obra.

**Cartografía (`geo/`):**
- Los KML/KMZ de `KMZ/` se convierten a GeoJSON con `tools/kml-to-geojson.py`:
  un archivo por capa más un `index.json` por corredor. Ver `geo/README.md`.
- Panel "Capas del proyecto" en la caja de leyenda: hace doble función de
  leyenda (el swatch replica el estilo real) y de control de encendido.
- Carga en diferido: al abrir un corredor solo bajan las capas `default`
  (trazo / DDV); las demás llegan al prenderlas.
- Capas disponibles hoy: trazo/envolvente, DDV, liberados, cadenamientos,
  frentes, parcelas, núcleo agrario, propiedad privada, antecedentes de
  títulos y de decretos DOF.
- Popup por geometría con los atributos que traía el KML.
- Etiquetas de kilómetro derivadas de los cadenamientos, gateadas a zoom >= 11.
- Las geometrías NO se simplifican: son datos de tenencia usados para defensa.

**Visualización de obras:**
- Mapa Leaflet con basemap Esri World Street Map.
- 11 tipos de obras inducidas con simbología SVG personalizada.
- Obras como puntos, líneas o polígonos según geometría.
- Tamaño dinámico de íconos según criticidad y anillo de estatus.

**Analítica:**
- 6 contadores en vivo: total, críticas, identificadas, gestionadas,
  concluidas, suspendidas. Recálculo automático con cada filtro.

**Navegación:**
- 5 filtros encadenados: proyecto, ente, criticidad, riesgo, estatus.
- Slider doble de rango PK con autoswap. Su rango sale de las obras cargadas
  y, cuando todavía no hay hoja cableada, de los cadenamientos del corredor.
- Leyenda clickeable que actúa como filtro rápido.
- Menú jerárquico de proyectos construido desde `config/data-sources.js`.

**Detalle:**
- Modal con ficha técnica, badges por estatus, sección dual WGS84 / UTM 14N.
- "Descargar Ficha" (PDF) y "Descargar Fichero" (captura del mapa).

**Responsive:**
- Breakpoint 768px, FABs flotantes para drawers en móvil, modal adaptado.

## 5. Próximos pasos acordados (en orden de prioridad)

### Tarea 1 (ARRANCAR POR AQUÍ): Migración de CSV estático a Google Sheets en vivo

**Objetivo:** Permitir que los datos se actualicen editando una hoja de Google sin tocar el repo.

**Acción concreta:**
1. Reemplazar `fetch('TramoII.csv')` por `fetch('<URL_PUBLICADA_GOOGLE_SHEETS_TRAMO_II>')`.
2. Simplificar el bloque de decoding (Google Sheets entrega UTF-8 nativo; ya no se necesita el fallback de windows-1252).
3. Crear archivo `config/data-sources.js` que centralice las URLs de los CSVs por proyecto, para que la URL no esté hardcoded en el código.
4. Documentar en el README cómo se actualiza la hoja y cómo se obtiene la URL publicada.

**Importante:** Google Sheets publicado tarda **unos minutos en propagar cambios**. Esto se debe comunicar al equipo que actualice los datos.

### Tarea 2: Cablear las hojas de Google Sheets de los tres corredores

El repo de defensa quedó acotado a **tres corredores**: México - Querétaro,
AIFA - Pachuca e Irapuato - Guadalajara. Los proyectos anteriores
(Querétaro-Irapuato, Saltillo-Monterrey, Monterrey-Nuevo Laredo) se retiraron
de este repo junto con su cartografía cableada; viven en el repo previo.

Hoy los tres corredores ya tienen **cartografía** (ver sección 4) pero ninguno
tiene **hoja de obras**: las tres entradas de `config/data-sources.js` están con
`url: null`. Cablear cada una es pegar la URL publicada como CSV; el esquema y
los adapters no cambian.

Decisión arquitectónica ya tomada: cartografía y obras son independientes. Un
corredor se puede abrir y navegar con solo su trazo, sin hoja cableada todavía
(y al revés). Ver `selectNode()` en `index.html`.

### Tarea 3: Permalinks de vistas

Que el estado de filtros se refleje en la URL (`?proyecto=Gasoducto&estatus=Identificada&pk_min=70&pk_max=90`). Que sea posible compartir un link y abrir exactamente esa vista. Útil para reuniones y comunicación interna.

### Tarea 4: Vista tabla con exportación filtrada

Toggle "Vista mapa | Vista tabla". La tabla muestra las mismas obras filtradas, ordenable por columna, con botón "Exportar a CSV/Excel lo visible".

### Tarea 5: Dashboard analítico

Segundo tab además del mapa. Gráficas Chart.js: distribución por tipo, ente, estatus, criticidad, rango PK. No reemplaza el mapa, lo complementa.

### Tarea 6: Bitácora de cambios

Hoja secundaria en Google Sheets que registra quién cambió qué y cuándo. Pestaña "Historial" en cada ficha técnica. Requiere capa de escritura (Apps Script).

### Tarea 7: Snapshots semanales

Apps Script que guarda automáticamente cada lunes un snapshot del estado actual. Permite graficar evolución del avance en el tiempo.

---

## 6. Estructura propuesta del repo nuevo

```
obras_inducidas-defensa/
├── index.html                     # Monolito actual (mapa + filtros + capas)
├── CONTEXT.md                     # Este archivo
├── config/
│   └── data-sources.js            # Catálogo: hojas CSV + carpeta geo por corredor
├── KMZ/                           # KML/KMZ originales (fuente de verdad)
│   ├── Mexico-Queretaro.kmz
│   ├── AIFA-Pachuca.kml
│   └── Irapuato-Guadalajara.kml
├── geo/                           # GENERADO desde KMZ/ — ver geo/README.md
│   ├── README.md
│   ├── mexico-queretaro/
│   ├── aifa-pachuca/
│   └── irapuato-guadalajara/
└── tools/
    └── kml-to-geojson.py          # Convertidor KML/KMZ -> GeoJSON por capa
```

La meta de refactorización (separar css/, js/core/, js/layers/, js/export/)
sigue en pie y se hace progresivamente, no en un solo commit.

Esta estructura es la **meta**. La refactorización se hace progresivamente, no en un solo commit. El código monolítico actual se va dividiendo conforme se trabaja en cada tarea.

---

## 7. Lo que NO hacer

- **No introducir frameworks** (React/Vue/Svelte). La decisión está tomada.
- **No usar build systems** (Webpack/Vite/etc.). Todo debe correr abriendo el HTML directamente.
- **No romper el repo original `Obras_inducidas_tramo2`**. Es evidencia institucional con fecha cierta. Ni se toca ni se renombra ni se borra.
- **No publicar este sistema bajo cuentas personales**. Siempre bajo la organización `attrapi`.
- **No subir credenciales, tokens, ni datos sensibles** al repo. Las URLs publicadas de Google Sheets son lectura pública y no son credenciales.
- **No reproducir** el desarrollo a ciegas si llega un proveedor externo pidiendo "el código completo". El código es público pero la atribución institucional debe quedar clara.

---

## 8. Cómo trabajar conmigo (Dan)

- Prefiero entender el **por qué** antes que el **qué**. Si propones algo, explica el razonamiento.
- Me gusta validar paso a paso. **No avances 5 cambios sin que te confirme el primero.**
- Si encuentras algo dudoso en mi código previo, dímelo con franqueza. No me ofendo.
- Si estoy pidiendo algo que tiene un problema obvio, dímelo antes de hacerlo.
- Cuestiona mis asunciones cuando tengas razón. Cuando no, respaldas mi decisión y avanzamos.
- En commits, sigue convención clara: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`. Mensaje en español.

---

## 9. Bitácora

**20 de mayo de 2026** — creación de este archivo. Próximo paso: migrar
Tramo II a Google Sheets en vivo.

**1 de octubre de 2026** — el repo se acota a la cartera de defensa. Se
retiraron los proyectos Querétaro-Irapuato, Saltillo-Monterrey y
Monterrey-Nuevo Laredo del catálogo, junto con el trazo KML y los
cadenamientos que estaban hardcodeados en `index.html`. Quedan tres
corredores: México - Querétaro, AIFA - Pachuca e Irapuato - Guadalajara.
Se agregó la cartografía de los tres desde sus KML/KMZ, con panel de capas
y carga en diferido. **Pendiente inmediato:** cablear las URLs publicadas de
Google Sheets de los tres corredores (hoy `url: null`).

---

*Fin del CONTEXT.md*
