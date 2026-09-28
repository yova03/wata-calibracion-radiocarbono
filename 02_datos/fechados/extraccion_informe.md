---
objetivo: "Informe de la extracción de fechados radiocarbónicos del Cusco desde la biblioteca Markdown."
uso: "Leer antes de usar fechados_biblioteca.csv: cobertura, criterios y dudas."
---

# Extracción de fechados C14 del Cusco — biblioteca `_BIBLIOTECA_MD`

## Método

1. Se localizaron con `grep` (ripgrep) 413 archivos `.md` de la biblioteca que contienen patrones de radiocarbono (`radiocarb`, `C-14`, `C14`, `14C`, códigos de laboratorio, `±`, `AP`/`BP`), excluyendo `_RETIRADOS`.
2. Se filtraron a 235 archivos (83 carpetas/documentos únicos, considerando duplicados `_parte_`, `_sub`, `-dup` como un solo documento) que además mencionan Cusco o algún sitio del valle/región.
3. Cinco agentes en paralelo revisaron esas 83 carpetas completas: cada dato se verificó leyendo el archivo original con la herramienta de lectura (no solo el resultado de grep), copiando la cita textual exacta y el número de línea.
4. Solo se registraron fechados con cifra numérica real (edad AP con o sin sigma, o rango calendárico explícito). Se descartaron menciones genéricas ("se hicieron fechados radiocarbónicos") sin cifra, y todo fechado de sitios fuera del departamento de Cusco (Titicaca/Puno, Bolivia, Apurímac, Ayacucho, Tacna, Argentina, etc.), aunque el documento mencionara Cusco de forma tangencial.
5. Los hallazgos se consolidaron y depuraron manualmente: mismo código de laboratorio + mismo valor en varias fuentes → una sola fila, con las fuentes repetidas anotadas en `notas`.

## Cobertura

83 documentos únicos revisados íntegramente. De ellos, **20 documentos** aportaron al menos un fechado de Cusco utilizable; el resto no tenía fechados de Cusco (o no tenía fechados C14 en absoluto, o trataban de sitios fuera del departamento).

## Resultado numérico

- **Total de filas en el CSV: 94** (fechados o registros calendáricos de sitios del departamento de Cusco).
- Por `ambito`:
  - `region_cusco`: 58
  - `valle_cusco`: 25
  - `ciudad_cusco`: 11
  - `fuera_cusco`: 0 (no se incluyó ninguno; el encargo pedía inventario de Cusco, así que los fechados de fuera del departamento se descartaron en origen y no llegaron al CSV)
- Con edad AP **y** sigma numéricos utilizables (edad convencional real, no solo rango calendárico): **73** de 94.
- Solo con rango calibrado/calendárico textual (`solo_calibrada = si`, sin AP/sigma): **21** de 94.

## Las 5 fuentes que más fechados aportan

1. `05-articulos/_recientes_2024-2026/earle2025tombs.md` — 16 filas (tumbas del Valle Sagrado del Cusco; 9 propias + 7 citadas de Chatfield 2007 y Bengtsson 1998; incluye 3 de Minaspata vía Hardy 2019).
2. `05-articulos/migraciones-altiplanicas-batan_orqo-julihno-z/..._sub26.md` — 13 filas (Batán Urqu, valle del Cusco, laboratorio de Heidelberg, informe original de 1994-1995).
3. `05-articulos/_recientes_2024-2026/shadik2024acopia.md` — 9 filas (núcleo de sedimento de la laguna de Acopia, Acomayo; fechado **paleoambiental**, no arqueológico).
4. `03-tesis/TESIS_UNSAAC_2026_13210_..._manos_de_moler.../parte_010_pp_045_050.md` — 8 filas (Yuthu, Anta; tabla de Davis y Delgado 2009).
5. `05-articulos/ravines-ceramica_documento/..._parte_009.md` — 8 filas (Chanapata/Carmenca, ciudad del Cusco; fechas dadas solo como año calendárico con código de laboratorio, sin AP/sigma explícitos).

(Cerca en 6.º lugar: `TESIS_2023_estratigrafico-arquitectura-pukara-pantillijlla` con 7 filas, y `delgado2024machuqolqa.md` con 6.)

## Duplicados resueltos

- **Q 3091** (1580±60 AP, Huillca Racay, cal. 340-620 d.C.): citado igual en `TESIS_UNSAAC_2019_5248` y en `publicacion-minaspata-ddc_cusco-of`. Una sola fila.
- **BETA-149193** (520±60, madera): citado como "Illarakay" en `TESIS_2023_planeamiento-arquitectura-illarakay` y como "Aqnapampa" en `earle2025tombs.md` (vía Chatfield 2007:218). Misma cifra, mismo laboratorio; se dejó una fila, con la discrepancia de nombre de sitio anotada.
- **Yuthu, códigos AA84430–AA84437** (8 muestras de Davis y Delgado 2009): aparecen tanto en `TESIS_2018_analisis-bioarqueologico-bandojan-yuthu` como en `TESIS_UNSAAC_2026_13210`. Se usó la tabla de 13210 (más completa, sin ambigüedad de columnas) como fuente principal; se anotó la repetición en la otra tesis.
- **AA 39783** (Peqokaypata): **NO se fusionó** — aparece con **1527±40 AP** (cal. 430-620 d.C., vía Bauer 2008) en `TESIS_UNSAAC_2019_5248`, y con **1422±51 AP** (cal. 530-700 d.C., vía Bauer 2011 p.158) en `publicacion-minaspata-ddc_cusco-of`. Mismo código, mismo sitio, **valores distintos**: se dejaron ambas filas por separado y se marcó el conflicto en `notas` de las dos, en vez de inventar cuál es correcta.
- **Sacsayhuaman (Dwyer, vía Bauer)**: `TESIS_2019_arqueologia-pachatusan-qosqo-ayllu` da 770±140 BP (cal. 1129-1351 d.C., Fairbanks); `TESIS_2019_evidencias-artefactuales-calle-mantas` da 1180±140 d.C. sin AP. Probablemente el mismo dato original mal transcrito en una de las dos tesis; se dejaron ambas filas por no compartir edad AP explícita, con nota cruzada.
- **Bandojan**: Beta-477535 (2220±30 AP, cal. 360-145 a.C.) en `TESIS_2018_...bandojan-yuthu` es cronológicamente compatible con la cita sin código de laboratorio "360 a.C.-145 d.C." de `TESIS_UNSAAC_2025_10945` (Delgado 2019); no se fusionaron por falta de código/AP compartido, solo se anotó la posible relación.

## Dudas y advertencias de calidad de dato (OCR / cifras ambiguas)

- **F038** (Lucre, "1000 a.C. ± 1432 d.C.", tesis de Succlli 2018 citada en TESIS_UNSAAC_2025_11507): es el **título** de una tesis, no se confirma que sea un fechado C14 real con código de laboratorio; el símbolo "±" entre dos fechas calendáricas no tiene sentido matemático, probablemente un guion mal reconocido por el OCR. Reportado con reserva explícita.
- Tabla de Yuthu en `TESIS_2018_analisis-bioarqueologico-bandojan-yuthu_parte_007.md`: el salto entre archivos `parte_006`/`parte_007` rompe el orden de la tabla justo donde debería ir el código de laboratorio de la muestra AA84433 (2369±36); se infirió el código por adyacencia y por comparación con la tabla completa de `TESIS_UNSAAC_2026_13210`, que sí lo trae explícito.
- Varias tablas (Batán Urqu, Machuqolqa, earle2025tombs, shadik2024acopia, Pukara Pantillijlla) muestran columnas reordenadas por el OCR del PDF original; se reconstruyeron fila por fila y se preservaron literalmente los valores, incluyendo posibles inversiones de rango calibrado (p. ej. AA84437/Yuthu RC-255: "83-118 AC" con el menor antes del mayor, tal cual aparece en dos fuentes distintas).
- **AA 39783** (Peqokaypata): valores en conflicto entre dos fuentes secundarias (Bauer 2008 vs. Bauer 2011); ver sección de duplicados. Requiere verificación contra la publicación original de Bauer antes de usarse en un análisis de calibración formal.
- El archivo `05-articulos/ENSAYO_SA_habermas-poder-religion-esfera-publica/ENSAYO_SA_habermas-poder-religion-esfera-publica.md` tiene contenido que no corresponde a su título/frontmatter (el cuerpo es una copia del artículo sobre Pukara); no se modificó, solo se deja constancia para quien administre la biblioteca.
- El fechado de la laguna de Acopia (`shadik2024acopia.md`) es un registro **paleoambiental** (núcleo de sedimento lacustre, Holoceno), no arqueológico; se incluyó porque cumple los criterios de un fechado C14 verificable de la región de Cusco, pero no tiene `periodo_asignado` cultural.
- Illarakay/Aqnapampa (BETA-149193): no queda resuelto si el laboratorio corresponde a una muestra propia del proyecto Illarakay o si ambas tesis/artículos citan la misma muestra de Chatfield 2007 bajo dos nombres de sitio distintos.

## Documentos revisados sin fechados de Cusco (constancia de que sí se revisaron)

Entre otros: `TESIS_2018_bioarqueologico-craneos-chancas-quichuas` (fechados existen pero son de Andahuaylas, Apurímac), `TESIS_2022_iconografia-monolitos-pukara` (Puno), `TESIS_2018_distribucion-espacial-arquitectura-inca-chuncal`, `TESIS_2021_litopatologias-paramentos-calle-conquista`, `TESIS_2022_alfareria-temprana-chimpahuaylla` (declara explícitamente que no tiene fechados), `TESIS_2022_trama-urbana-wari-pikillacta` (cita "fechados de McEwan 2005" sin cifra), `TESIS_2023_almacenamiento-depositos-machuqolqa`, `TESIS_2023_arquitectura-mujuncancha-huaro`, `TESIS_2023_arquitectura-naupallaqta`, `TESIS_2023_atributos-huaca-cauadcalla-huanoquite`, `TESIS_2023_estructuras-urbanas-funerarias-toqra-chamaca`, `TESIS_2023_microscopia-ceramica-inka-sillkinchani`, varias tesis UNSAAC 2024-2026 (8779, 9481, 11687, 12229, 12542 — declara explícitamente que no hizo C14, 12704, 13197, 13212), y varios libros/artículos centrados en la cuenca del Titicaca, Bolivia o Ayacucho que solo mencionan Cusco de forma tangencial (`advances-in-titicaca_basin-archaeology-i-1`, `definicion_e-identidificacion-de-yayamama`, `LIBRO_1975_estela-taraco-escultura-chavez`, `arqueologia-de-la_cuenca-del-titicaca-pe`, `ARTICULO_1998_escultura-precolombina-boliviana-portugal`, `secuencia-mas-temprana...pukara`, `ideologia_y-realidad-en-las-primeras-sociedades`, `susan_2012_e-bergh-wari-lords-of-the-ancient-andes`, `tiwanaku_y-el-impacto...`, `trade-and-early_state-formation-in-the-n`).

## Nota honesta sobre la ciudad del Cusco

Del total de 94 filas, solo **11** corresponden estrictamente a `ciudad_cusco` (Marcavalle: 1 fila sin AP; Chanapata/Carmenca: 8 fechas de Ravines sin AP/sigma explícito; Sacsayhuaman: 2 filas, con discrepancia entre sí). Es decir, dentro del casco urbano actual hay muy pocos fechados C14 con edad convencional AP y sigma propiamente dichos en esta biblioteca — la mayoría de lo disponible con AP/sigma robusto proviene del valle (Yuthu, Bandojan, Qotakalli, Machuqolqa, Batán Urqu, tumbas del Valle Sagrado) y de la región más amplia (Pukara Pantillijlla, Illarakay, Sicuani, K'anamarka). Esto es un resultado válido y debe tenerse en cuenta al diseñar la investigación de calibración: si se necesita específicamente radiocarbono de la ciudad, la biblioteca actual ofrece muy poco material verificable con cifra AP+sigma.

## Notas posteriores (2026-09-28)

- Las 16 filas tomadas de `earle2025tombs.md` quedan excluidas por decisión del investigador ([`excluidos.csv`](excluidos.csv)). Siguen en el CSV como registro de la extracción. Sin ellas, el CSV conserva 78 filas, de las que 57 tienen edad AP y sigma.
- Sacsayhuaman: «1180 ± 140 d. C.» (F016) es la misma edad «770 ± 140 AP» (F015) expresada sin calibrar (1950 − 770 = 1180). Las dos filas no se contradicen: son un solo dato, de Dwyer, citado a través de Bauer.
