---
objetivo: "Presentar la investigación 06: una herramienta abierta en español para calibrar fechados radiocarbónicos (wata) y su aplicación a la cronología del Cusco con fechados publicados y simulados."
uso: "Punto de entrada. Viabilidad, validación y simulación están en 04_resultados; la herramienta, en 01_codigo/wata; su manual, en README.md."
---

# Calibración radiocarbónica abierta y cronología del Cusco

**Investigación n.º 06 · 28 de setiembre de 2026**
**Herramienta:** `01_codigo/wata` (versión 0.1.0) · **Manual:** [`README.md`](README.md)

## Resumen

OxCal, el programa con el que la arqueología calibra sus fechados de carbono
14, no publica una versión nueva desde el 15 de abril de 2021. Las
alternativas abiertas existen, pero ninguna trabaja en español ni plantea la
elección de curva que exigen los Andes tropicales. Esta investigación
construyó **wata**, una herramienta en Python que calibra con SHCal20,
IntCal20 o una mezcla de ambas, y la validó contra rangos publicados con
OxCal: 20 de 21 coinciden con una diferencia máxima de dos años. Con ella se
simularon fechados de la cronología del Cusco entre 1000 y 1600 d. C., y se
calibraron los fechados publicados que reúne la biblioteca del proyecto.

## Enunciado (Supo)

| Elemento | Valor |
|---|---|
| Propósito | Evaluación |
| Línea de investigación | Resolución cronológica de la calibración radiocarbónica según la curva |
| Población | Fechados radiocarbónicos publicados y simulados |
| Lugar | Ciudad, valle y región del Cusco |
| Tiempo | Siglos XI a XVI (periodos Killke e Inka y contacto español) |

**Enunciado:** Evaluación de la resolución cronológica de la calibración
radiocarbónica en los fechados publicados y simulados del Cusco, siglos XI
a XVI.

**Pregunta:** ¿Qué resolución cronológica ofrece la calibración
radiocarbónica, según la curva empleada, para los fechados publicados y
simulados del Cusco entre los siglos XI y XVI?

**Objetivo general:** Evaluar la resolución cronológica de la calibración
radiocarbónica, según la curva empleada, en los fechados publicados y
simulados del Cusco entre los siglos XI y XVI.

Estudio observacional, retrospectivo para los fechados publicados,
transversal y descriptivo. No lleva hipótesis: compara el comportamiento de
tres curvas sin afirmar de antemano una diferencia que deba contrastarse.

## Método

1. **Herramienta** (`01_codigo/wata`): calibración simple año por año con la
   fórmula clásica (verosimilitud normal con la sigma del laboratorio y la de
   la curva sumadas en cuadratura, prior uniforme); rangos de máxima
   densidad; curva mixta con la fórmula de Mix_Curves de OxCal, en
   concentración de radiocarbono.
2. **Curvas**: SHCal20 e IntCal20 de intcal.org, con SHA-256
   ([origen](02_datos/curvas/ORIGEN.md)).
3. **Validación**: contra los 11 fechados de Machu Picchu calibrados con
   OxCal 4.3.2 por Ziółkowski et al. (2021) y contra IOSACal 0.7.0 en 616
   rangos ([validación](04_resultados/02_validacion.md)).
4. **Simulación** (`01_codigo/estudio_cusco.py`): 200 fechados simulados por
   año verdadero, de 1000 a 1600 d. C., con las tres curvas, y un escenario
   de atmósfera mixta calibrada con una sola curva
   ([simulación](04_resultados/03_simulacion_cusco.md)).
5. **Fechados publicados**: extracción desde `_BIBLIOTECA_MD` con cita textual
   y línea de origen, y calibración con las tres curvas
   ([fechados](04_resultados/04_fechados_cusco.md)).

## Resultados principales

- **Viabilidad**: sí. La matemática es pública y estable; lo que da
  credibilidad es la validación continua ([viabilidad](04_resultados/01_viabilidad.md)).
- **Precisión por siglo**: un fechado único ± 25 AP queda acotado a unos 45
  años entre 1400 y 1450 d. C., pero a 130–150 años entre 1450 y 1600.
- **1438**: un fechado aislado no decide si una muestra de 1430 o 1440 es
  anterior o posterior al ascenso de Pachacuti; hacen falta varios fechados
  y un modelo.
- **Curva**: para edades de época inka, IntCal20 da fechas unos 30 años más
  antiguas que SHCal20 (hasta 70 en las mesetas); la mezcla 50:50 queda en
  medio. Si la atmósfera del Cusco fuera mixta, calibrar solo con SHCal20
  rejuvenecería las fechas de 1460–1500 entre 40 y 70 años y el rango 95.4 %
  fallaría hasta en uno de cada cinco fechados.
- **Fechados publicados**: la biblioteca reúne 94 fechados del Cusco; sin
  Earle (2025), excluido por decisión del investigador, quedan 78, de los
  que 57 traen edad y sigma. La ciudad aporta uno solo utilizable
  (Sacsayhuaman, 770 ± 140 AP). De los 16 fechados de los siglos XI a XVI,
  los seis de Machuqolqa son anteriores a 1438 y tres de Pukara Pantillijlla
  quedan indecisos.

## Limitaciones

- La versión 0.1 hace calibración simple; los modelos bayesianos (fases,
  límites, secuencias) son la siguiente etapa.
- No corrige efecto reservorio ni fraccionamiento: recibe edades
  convencionales.
- La validación contra OxCal usa las curvas de 2013, que son las del caso
  andino publicado con tabla abierta. Falta un caso de referencia con
  SHCal20.
- Los fechados de la biblioteca dependen del OCR de las tesis; cada fila
  conserva la cita textual para revisarla.

## Estructura

| Carpeta | Contenido |
|---|---|
| `01_codigo/wata/` | paquete: curvas, calibración, simulación, figuras, línea de órdenes |
| `01_codigo/` | `estudio_cusco.py` y `calibrar_fechados_cusco.py` |
| `02_datos/curvas/` | curvas `.14c` y `ORIGEN.md` |
| `02_datos/fechados/` | fechados del Cusco con fuente, línea y cita textual |
| `04_resultados/` | informes 01–04, CSV y figuras |
| `pruebas/` | `pytest`, validación contra OxCal y contraste con IOSACal |
