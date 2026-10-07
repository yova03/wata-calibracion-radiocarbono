---
objetivo: "Reunir los campos del depósito manual en Zenodo listos para copiar y pegar."
uso: "Abrir junto al formulario de Zenodo; copiar cada campo en su casilla y publicar."
---

# Texto para el depósito manual en Zenodo

**Archivo:** `borrador/investigacion_cusco_wata_v0.1.0_DEPOSITO.zip` — 1 578 402 bytes
**SHA-256:** `a6c2e484fc16614e369d60fdfbe7854b090b149979be13ba3a868b1aab34e381` (45 archivos, con `MANIFIESTO.json`)

## Pasos

1. En Zenodo, pulsa **New upload** y arrastra el ZIP de arriba.
2. Pulsa **Reserve DOI** (Get a DOI now!) y anota el DOI reservado.
3. Copia los campos de abajo en sus casillas.
4. Revisa el archivo, el título y las relaciones; luego **Publish**.
5. Copia el DOI final: con él se actualizan el README y `CITATION.cff`.

Antes de subir: en **Settings → GitHub**, pon el interruptor del repositorio en
**OFF** para que un release futuro no genere un registro automático duplicado.

## Campos

| Campo | Valor |
|---|---|
| Resource type | Software |
| Title | Calibración radiocarbónica abierta y cronología del Cusco: wata, datos y simulaciones (v0.1.0) |
| Creator | Cabrera Huaycochea, Daril Yovani — ORCID `0009-0007-9912-8010` |
| License | MIT (el alcance por archivo se explica en la descripción) |
| Version | 0.1.0 |
| Language | Spanish / Español (spa) |
| Keywords | radiocarbono; calibración radiocarbónica; Cusco; arqueología andina; SHCal20; IntCal20; simulación; software científico; cronología inka |
| Publication date | La fecha real de publicación |

### Description (pegar tal cual)

<p><code>wata</code> es una herramienta en Python para calibrar edades radiocarbónicas convencionales con SHCal20, IntCal20 o una curva mixta, con resultados en español. Este depósito reúne la versión 0.1.0 del código, los datos derivados de fuentes publicadas sobre Cusco, las reglas de exclusión, los resultados de calibración, simulaciones y figuras. Las edades originales proceden de un inventario de 94 registros; el análisis calibra 50 tras excluir 16 filas por decisión del investigador, cinco fechas rechazadas por la fuente y dos lecturas incompatibles del mismo código de laboratorio.</p><p>La implementación de calibración simple se comparó con rangos publicados obtenidos con OxCal y con IOSACal; las siete pruebas incluidas pasan. Los resultados sobre los siglos XI a XVI se basan en 16 fechados del inventario y simulaciones con semillas fijas. El material lacustre aceptado se identifica como paleoambiental y queda fuera de las figuras arqueológicas. El software no incluye modelos bayesianos de fases o secuencias y el escenario de atmósfera mixta no afirma que la proporción real del Cusco sea 50:50.</p><p>Las curvas de calibración son de IntCal y no se incluyen en el archivo depositado; el programa las descarga desde el sitio oficial y registra sus SHA-256. El catálogo ofrece enlaces públicos para 77 de las 94 filas del inventario. Las 13 fechas de Batán Urqu provienen de un informe local sin enlace público verificado; se identifican como tales y requieren cotejo independiente antes de sustentar una conclusión cronológica decisiva.</p>

## Related works (una por una, relación «References»)

| Identificador | Esquema |
|---|---|
| 10.1017/RDC.2020.59 | DOI (SHCal20) |
| 10.1017/RDC.2020.41 | DOI (IntCal20) |
| 10.18800/boletindearqueologiapucp.202401.003 | DOI (Machuqolqa) |
| 20.500.12918/7753 | Handle (Pukara Pantillijlla) |
| 10.3390/plants13071019 | DOI (Acopia) |

## Licencias

MIT para el código propio; CC BY 4.0 para textos, tablas y figuras propios
(la descripción ya lo declara). Las curvas IntCal/SHCal y las mediciones
citadas conservan la atribución a sus fuentes y no viajan en el ZIP.
