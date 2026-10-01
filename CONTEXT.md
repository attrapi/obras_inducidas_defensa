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

El sistema Tramo II ya tiene implementado:

**Datos:**
- Carga CSV-driven con `fetch` (actualmente archivo estático `TramoII.csv`).
- Parser CSV manual con manejo de comillas y comas escapadas.
- Detección de encoding (windows-1252 con fallback iso-8859-1).
- Normalización de estatus (`GESTIÓN / EJECUCIÓN` → `Gestión / Ejecución`, etc.).
- Modelo de 19 campos por obra: id, proyecto, tramo, pk_ini, pk_fin, estado, municipio, lat_ini, lon_ini, lat_fin, lon_fin, ente, tipo_activo, tipo_obra, descripcion, criticidad, riesgo, responsable, estatus, utm_ie, utm_in.

**Visualización:**
- Mapa Leaflet con basemap CartoDB Voyager.
- KML del trazo ferroviario (polilínea con ~480 vértices).
- Marcadores PK cada 10 km con labels.
- 11 tipos de obras inducidas con simbología SVG personalizada (Media Tensión, Telecomunicaciones, Gasoducto, Alta Tensión, Servicios Municipales, Drenaje, Servicios Privados, Hidrocarburo, Agua Potable, Baja Tensión, INAH).
- Obras como puntos o líneas según geometría (lat_ini ≠ lat_fin).
- Tamaño dinámico de íconos según criticidad.
- Anillo animado tipo radar (`@keyframes ripple`) cuando se filtra por proyecto.
- Toggle KML on/off.

**Analítica:**
- 6 contadores en vivo: total, críticas, identificadas, gestionadas, concluidas, suspendidas.
- Recálculo automático con cada filtro.

**Navegación:**
- 5 filtros encadenados: proyecto, ente, criticidad, riesgo, estatus.
- Slider doble de rango PK con tracking visual y autoswap.
- Leyenda clickeable que actúa como filtro rápido.
- Selector de "pildora" multi-proyecto (Tramo I, Tramo II, Segmento 16-17, Segmento 15b).

**Detalle:**
- Modal con 11 campos de ficha técnica.
- Badges con código de color por estatus.
- Sección dual WGS84 / UTM Zona 14N.
- Botón "Descargar Ficha" (PDF impreso por nueva ventana).
- Botón "Descargar Fichero" (captura completa del mapa con html2canvas + jsPDF).

**Responsive:**
- Breakpoint 768px.
- FABs flotantes para abrir/cerrar drawers en móvil.
- Scroll horizontal de stats sin scrollbar visible.
- Modal adaptado a viewports pequeños.
- Cierre por click en mapa.

---

## 5. Próximos pasos acordados (en orden de prioridad)

### Tarea 1 (ARRANCAR POR AQUÍ): Migración de CSV estático a Google Sheets en vivo

**Objetivo:** Permitir que los datos se actualicen editando una hoja de Google sin tocar el repo.

**Acción concreta:**
1. Reemplazar `fetch('TramoII.csv')` por `fetch('<URL_PUBLICADA_GOOGLE_SHEETS_TRAMO_II>')`.
2. Simplificar el bloque de decoding (Google Sheets entrega UTF-8 nativo; ya no se necesita el fallback de windows-1252).
3. Crear archivo `config/data-sources.js` que centralice las URLs de los CSVs por proyecto, para que la URL no esté hardcoded en el código.
4. Documentar en el README cómo se actualiza la hoja y cómo se obtiene la URL publicada.

**Importante:** Google Sheets publicado tarda **unos minutos en propagar cambios**. Esto se debe comunicar al equipo que actualice los datos.

### Tarea 2: Integración de proyecto Saltillo-Monterrey

Tres CSVs publicados que conviven en el mismo tramo geográfico:
- **Seg 13-14:** obras inducidas estándar (mismo esquema que Tramo II, presumiblemente).
- **INAH dataset 1:** hallazgos arqueológicos (esquema posiblemente distinto).
- **INAH dataset 2:** otro conjunto de hallazgos INAH (esquema posiblemente distinto).

**Decisión arquitectónica pendiente:** confirmar si los CSVs del INAH comparten esquema con el de obras inducidas, o si requieren un modelo paralelo. Hipótesis fuerte: los CSVs del INAH tienen estructura distinta (campos arqueológicos: época, tipo de vestigio, número de inventario, etc.), por lo que conviene tratarlos como **capa separada con render unificado** — se ven juntos en el mapa pero internamente son entidades distintas con fichas técnicas distintas.

URLs publicadas (confirmar al integrar):
- Seg 13-14: `https://docs.google.com/spreadsheets/d/e/2PACX-1vQCXuNre9SGM6RGnZ5aAco1ztzIpY03LURR32NpE2E6SlHjYtZHmIarlay5mFpkdQ/pub?gid=800038218&single=true&output=csv`
- INAH 1: `https://docs.google.com/spreadsheets/d/e/2PACX-1vSbks6OG9F4SH1Ue_9qt3-4mk2A9arGzQKEXRHFGw5lq0r3H4u8NlbfSOJIG1ZYXg/pub?gid=60031769&single=true&output=csv`
- INAH 2: `https://docs.google.com/spreadsheets/d/e/2PACX-1vSuhlYtmT4G7Z9sokHn2n1tLmB5eJvB0j4O93KrDDIpHWEi1ZqTznfmgtImfSRF6w/pub?gid=1646263905&single=true&output=csv`

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
sistema-obras-inducidas/
├── index.html                     # Punto de entrada (refactor del actual)
├── README.md                      # Documentación de uso, actualización de datos
├── CONTEXT.md                     # Este archivo
├── config/
│   └── data-sources.js            # URLs CSV por proyecto/tramo
├── css/
│   └── styles.css                 # CSS extraído del HTML monolítico
├── js/
│   ├── core/
│   │   ├── data-loader.js         # Carga y parseo de CSVs (PapaParse)
│   │   ├── map.js                 # Inicialización Leaflet + KML + PK
│   │   ├── filters.js             # Lógica de filtros y permalinks
│   │   └── modal.js               # Modal de ficha técnica
│   ├── layers/
│   │   ├── obras-inducidas.js     # Render de obras estándar
│   │   └── inah.js                # Render de hallazgos arqueológicos
│   ├── analytics/
│   │   ├── counters.js            # Contadores en vivo
│   │   └── dashboard.js           # Gráficas Chart.js (Tarea 5)
│   └── export/
│       ├── pdf.js                 # Exportación PDF (ya existente)
│       └── table.js               # Vista tabla y exportación CSV (Tarea 4)
└── assets/
    ├── kml/
    │   ├── tramo-ii.kml
    │   └── saltillo-monterrey.kml
    └── favicon.svg
```

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

## 9. Estado al momento de creación de este archivo

**Fecha:** 20 de mayo de 2026
**Próximo paso inmediato:** Tarea 1 — migrar Tramo II a Google Sheets en vivo.
**Hoja de Tramo II en Google Sheets:** PENDIENTE — Dan debe subir el `TramoII.csv` actual a una hoja de Google y publicarla como CSV. La URL resultante reemplaza al archivo estático.

---

*Fin del CONTEXT.md*
