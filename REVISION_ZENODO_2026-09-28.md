---
objetivo: "Documentar la revisión previa a publicar la investigación 06 en Zenodo y asignarle un DOI."
uso: "Revisar el alcance, las verificaciones y las limitaciones antes de publicar el registro."
---

# Revisión previa al depósito en Zenodo — 28 de setiembre de 2026

## Dictamen

**El depósito técnico está preparado para revisión; no es un artículo revisado
por pares. Aún no se reservó ni registró un DOI.** El software `wata` tiene
una base funcional verificable. El autor eligió depositar la investigación
completa bajo su autoría única. El nombre, ORCID y licencias están identificados.
La tabla analítica apartó siete registros de calidad insuficiente. El catálogo
de fuentes y un ZIP para depósito están preparados; tres fuentes siguen sin
enlace público comprobado, una de ellas con 13 fechas de Batán Urqu.

Un DOI de Zenodo identifica el objeto depositado; no equivale a revisión por
pares ni convierte estos informes en un artículo aceptado. Zenodo permite
reservar un DOI en un borrador, pero solo lo registra al publicar:
[guía oficial](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/).

## Verificaciones completadas

| Comprobación | Resultado |
|---|---|
| Pruebas existentes | `python -m pytest pruebas -q`: 7 aprobadas el 28/09/2026 |
| Curvas `.14c` | Los cuatro SHA-256 coinciden con [`ORIGEN.md`](02_datos/curvas/ORIGEN.md) |
| Conteos de archivos | 94 filas originales, 23 exclusiones documentadas, 50 filas en `calibrados.csv` |
| Referencias locales | Las 94 rutas `fuente_archivo` existen en `_BIBLIOTECA_MD` del equipo |
| Validación OxCal | 20 de 21 rangos comparables tienen igual número de tramos; uno difiere; un rango adicional no tiene referencia legible |

El contraste con OxCal usa curvas de 2013 y rangos publicados, no una
comparación directa con OxCal para todas las curvas y casos de 2020. Las
dependencias en [`requirements.txt`](requirements.txt) tienen límites mínimos;
las versiones efectivas de la revisión constan en
[`ENTORNO_EJECUCION.md`](ENTORNO_EJECUCION.md).

## Hallazgos corregidos y pendientes

1. **Cinco fechas rechazadas por la fuente estaban en los resultados.**
   Shadik et al. identifican cinco valores atípicos de la laguna Acopia en
   la tabla 1: `F063` a `F067`. El CSV original ya anota que fueron
   rechazados. Se añadieron a
   [`excluidos.csv`](02_datos/fechados/excluidos.csv) y se regeneró
   [`calibrados.csv`](04_resultados/fechados_cusco/calibrados.csv).
   Permanecen en el inventario bruto. Los 16 fechados de los siglos XI a XVI
   no cambiaron.
2. **Un código de laboratorio tiene dos edades.** `AA 39783` aparece como
   `F035 = 1527 ± 40 AP` y `F086 = 1422 ± 51 AP`. Ambas filas quedaron
   excluidas provisionalmente de la tabla analítica y siguen en el inventario.
   Antes de reincorporar alguna hay que cotejar las publicaciones originales
   de Bauer. El conflicto figura en
   [`extraccion_informe.md`](02_datos/fechados/extraccion_informe.md).
3. **Proveniencia pública parcialmente resuelta.** `fuente_archivo` apunta a
   `_BIBLIOTECA_MD`, que no forma parte del proyecto. El ZIP de depósito
   añade enlaces públicos a 77 de las 94 filas; el
   [catálogo](02_datos/fechados/fuentes_publicas.csv) documenta los 23
   archivos fuente y una [nota](02_datos/fechados/FUENTES_SIN_ENLACE.md)
   identifica los tres sin enlace institucional comprobado. Trece filas
   proceden de un informe local de Batán Urqu sin acceso público verificado;
   las 13 están entre las 50 calibraciones. Por ello, el subconjunto de
   Batán Urqu requiere cotejo independiente antes de sustentar conclusiones
   cronológicas decisivas.
   Las citas del CSV local son en varios casos texto normalizado o
   reconstruido del OCR: el ZIP público omite la columna `cita_textual`.
4. **Licencias resueltas para material propio.** El autor autorizó MIT para
   código y CC BY 4.0 para textos, tablas y figuras propios. Se añadieron
   [`LICENSE_CODE.txt`](LICENSE_CODE.txt) y
   [`LICENSE_CONTENT.md`](LICENSE_CONTENT.md). Las curvas `.14c` de IntCal
   quedan fuera del ZIP, pues [`ORIGEN.md`](02_datos/curvas/ORIGEN.md) no
   documenta permiso de redistribución. La
   [política de Zenodo](https://about.zenodo.org/policies/) exige derechos
   adecuados para lo que se sube.
5. **Autoría única resuelta.** El usuario indicó ser el único autor y pidió
   cotejar su grafía en el disco D. Sus documentos académicos registran
   «Daril Yovani Cabrera Huaycochea», nombre incorporado al proyecto y al
   [`CITATION.cff`](CITATION.cff). El ORCID
   `0009-0007-9912-8010` consta en un borrador académico del disco D.

Los cuatro fechados lacustres aceptados por Shadik et al. también deben
identificarse expresamente como datos paleoambientales; su modelo de edad
no equivale a la calibración aislada hecha aquí. Si el depósito se presenta
como arqueológico, conviene dejar esa serie fuera del análisis principal.

## Depósito preparado

- **Objeto elegido:** un registro de la investigación completa, con código,
  datos y resultados. Título: «Calibración radiocarbónica abierta
  y cronología del Cusco: wata, datos y simulaciones (v0.1.0)». Se propone
  el tipo Software como contenido predominante; Zenodo permite elegirlo para
  materiales mixtos:
  [tipos de recurso](https://help.zenodo.org/docs/deposit/describe-records/resource-type/).
- **Autoría:** Daril Yovani Cabrera Huaycochea,
  [ORCID 0009-0007-9912-8010](https://orcid.org/0009-0007-9912-8010).
- **Licencias:** MIT para código propio y CC BY 4.0 para textos, tablas y
  figuras propios. La ficha de Zenodo debe expresar el alcance por archivo;
  [Zenodo permite describir las licencias](https://help.zenodo.org/docs/deposit/describe-records/licenses/).

El [script de depósito](05_deposito_zenodo/preparar_archivo.py) forma un ZIP
con lista explícita de archivos y manifiesto de hashes. Excluye `.git`,
cachés, `_RETIRADOS`, las curvas ajenas y los extractos textuales del CSV.
Antes de publicar, revisar en Zenodo el archivo subido, sus metadatos y las
advertencias sobre las fuentes sin enlace. La publicación registrará el DOI.
