---
objetivo: "Documentar el video vertical para TikTok de la investigación 06 (v2 vigente, v1 archivada), sus cifras con fuente y su regeneración."
uso: "Publicar video/wata_tiktok_v2.mp4 con portada_v2.png; reproducir el generador si cambian los textos o los datos."
---

# Difusión: video vertical (TikTok)

## Versión vigente: v2

**Archivo:** `video/wata_tiktok_v2.mp4` — 33,4 s, 1080×1920 (9:16), 30 fps, H.264 (High, yuv420p, `faststart`), ~2 MB, sin audio.
**Portada:** `portada_v2.png` (fotograma del gancho con todos los elementos).
**Generador:** `generar_video_v2.py` (Pillow + imageio-ffmpeg). Los gráficos se dibujan desde los CSV de `04_resultados/` y desde `wata`; el propio script comprueba con `assert` cada cifra de pantalla al arrancar. `frames_control_v2/` guarda el primer y el último fotograma de cada escena y dos hojas de contacto (`hoja_*_mascara.png` marca las zonas que tapa la interfaz de TikTok).

### Escenas

| # | Inicio | Contenido |
|---|---|---|
| 1 | 0:00 | «¿Antes o después de 1438?»: la misma muestra de ejemplo (450 ± 25 AP) con SHCal20, mixta e IntCal20; medianas 1473, 1453 y 1444, probabilidad de «antes de 1438» (<1 %, 5 % y 25 %) y 29 años entre las medianas |
| 2 | 0:05 | Presentación: *wata* («año» en quechua), calibración radiocarbónica en español |
| 3 | 0:08 | Terminal con las salidas reales de `calibrar 450 25` y `--curva intcal20 calibrar 450 25` |
| 4 | 0:13 | Validación: 20/21 rangos con los mismos tramos frente a OxCal; 616 rangos frente a IOSACal (diferencias por decisiones de IOSACal, no de wata) |
| 5 | 0:17 | Aplicación al Cusco: 50 fechados calibrados; distribución calibrada (SHCal20) de los 16 de los siglos XI–XVI |
| 6 | 0:21 | 1438: probabilidad de «antes de 1438»; una muestra de 1430 aún deja un cuarto de probabilidad de salir después |
| 7 | 0:25 | Alcance de un fechado: 43–53 años entre 1400 y 1449; 134–149 desde 1450 |
| 8 | 0:29 | Cierre: «Declara la curva con cada fecha», repositorio público y licencias |

### Cifras y fuentes

| Cifra en pantalla | Fuente |
|---|---|
| 1473, 1453, 1444 (medianas de 450 ± 25 AP), 29 años | salida de `python -m wata [--curva …] calibrar 450 25` (wata 0.1.0); resta 1473 − 1444 |
| 95.4 %: 1442–1503 (82.6 %) y 1423–1461 (91.7 %) | misma salida de `wata` |
| «antes de 1438»: <1 %, 5 %, 25 % (SHCal20, mixta, IntCal20) | `prob_entre(-100000, 1437)` de cada calibración de 450 ± 25 AP (años ≤ 1437, criterio de `antes_1438.csv`) |
| 20/21 con los mismos tramos; diferencia máxima 2 años; 11 fechados de Machu Picchu, Chachabamba y Choqesuysuy | `04_resultados/02_validacion.md` (Ziółkowski et al., 2021, tabla 3) |
| 616 rangos, 508 con los mismos tramos, diferencia máxima 11 años | `04_resultados/02_validacion.md` (IOSACal 0.7.0; el informe atribuye las diferencias a tres decisiones de IOSACal, no de wata) |
| 50 fechados calibrados; 16 de los siglos XI–XVI | `04_resultados/fechados_cusco/calibrados.csv` (50 filas; 16 con mediana SHCal20 ≥ 1000) y `04_fechados_cusco.md` |
| 1438 «fecha documental del ascenso de Pachacuti» | `03_simulacion_cusco.md` (las fuentes escritas lo asocian al ascenso; Burger et al., 2021) |
| Curvas de «antes de 1438»; 1430 → 0,74 → «un cuarto» | `04_resultados/simulacion/antes_1438.csv` (fechado único ± 20 AP) |
| 43–53 y 134–149 años | `04_resultados/simulacion/recuperacion.csv` (± 25 AP; medianas por tramo y curva; coinciden con la tabla 1 de `03_simulacion_cusco.md`) |
| «Declara la curva con cada fecha» | `03_simulacion_cusco.md`, apartado 3: la curva usada debe declararse junto con cada fecha |

Ninguna escena sugiere cuál es la curva correcta para el Cusco: las tres se muestran con el mismo peso y el mensaje final pide declararla.

### Diseño

- Todo lo esencial cae en la zona segura de TikTok: x 70–930 e y 170–1500 (arriba la barra de pestañas, abajo la descripción, a la derecha los iconos).
- El primer fotograma ya muestra la pregunta; los cortes son fundidos de 0,15 s (sin caídas a negro).
- Texto secundario de 36 px o más; gráficos con marcas de 32 px, sin etiquetas verticales de eje.

### Publicación sugerida

Descripción: «Una misma edad radiocarbónica de ejemplo (450 ± 25 AP), tres curvas, 29 años
entre medianas. Calibré fechados con wata, una herramienta abierta en español: SHCal20, IntCal20
y curva mixta. Código, datos y figuras en
github.com/yova03/wata-calibracion-radiocarbono». Etiquetas sugeridas:
`#arqueología #Cusco #carbono14 #radiocarbono #Perú #cienciaabierta #tesis`.
El MP4 no lleva audio: la música se añade dentro de TikTok al publicarlo.

### Regenerar

```bash
python generar_video_v2.py            # video completo (~1 min)
python generar_video_v2.py --prueba --mascara   # solo controles con zonas seguras
```

Requiere `04_resultados/`, el paquete `wata` (`01_codigo/`) y las fuentes del
sistema (Arial Black, Segoe UI, Consolas).

## Versión archivada: v1 (no publicar)

`video/wata_tiktok_v1.mp4` (42 s) y `generar_video.py` se conservan por historial, con `frames_control/`.
La v1 contiene afirmaciones que la v2 corrige:

- «20/21 rangos idénticos a OxCal»: la fuente dice que 20 de 21 tienen el mismo número de tramos, con diferencia máxima de 2 años.
- «50 calibraciones de 94 registros»: los 94 registros incluyen las 16 filas de Earle (2025) que se excluyeron por decisión del investigador.
- «IntCal20 ≈ 30 años más antigua que SHCal20»: lo que sale más antiguo es la fecha calibrada, no la curva.
- «11 fechados de Machu Picchu»: son de Machu Picchu, Chachabamba y Choqesuysuy.
- Pies de texto dentro de la franja inferior que tapa TikTok, y un primer fotograma negro.
