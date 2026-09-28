---
objetivo: "Preparar los campos de Zenodo para un único registro de la investigación completa."
uso: "Usar los campos al crear el borrador y revisar el archivo antes de publicar."
---

# Metadatos propuestos para Zenodo

| Campo | Propuesta |
|---|---|
| Tipo | Software, con datos y resultados complementarios en el mismo ZIP |
| Título | Calibración radiocarbónica abierta y cronología del Cusco: wata, datos y simulaciones (v0.1.0) |
| Autor único | Daril Yovani Cabrera Huaycochea — grafía cotejada en sus documentos académicos del disco D |
| ORCID | https://orcid.org/0009-0007-9912-8010 |
| Fecha de publicación | Fecha real de publicación del registro |
| Versión | 0.1.0 |
| Idioma | Español |
| Acceso | Abierto; el ZIP contiene código y materiales propios, datos derivados con atribución y sin copias de fuentes ni curvas de terceros |
| Licencia | MIT para código propio y CC BY 4.0 para materiales propios restantes, autorizadas por el autor |
| DOI | Se reserva en el borrador de Zenodo o se asigna al publicar; todavía no existe uno para este proyecto |

## Descripción propuesta

`wata` es una herramienta en Python para calibrar edades radiocarbónicas
convencionales con SHCal20, IntCal20 o una curva mixta, con resultados en
español. Este depósito reúne la versión 0.1.0 del código, los datos derivados
de fuentes publicadas sobre Cusco, las reglas de exclusión, los resultados
de calibración, simulaciones y figuras. Las edades originales proceden de un
inventario de 94 registros; el análisis calibra 50 tras excluir 16 filas por
decisión del investigador, cinco fechas rechazadas por la fuente y dos
lecturas incompatibles del mismo código de laboratorio.

La implementación de calibración simple se comparó con rangos publicados
obtenidos con OxCal y con IOSACal; las siete pruebas incluidas pasan. Los
resultados sobre los siglos XI a XVI se basan en 16 fechados del inventario y
simulaciones con semillas fijas. El material lacustre aceptado se identifica
como paleoambiental y queda fuera de las figuras arqueológicas. El software
no incluye modelos bayesianos de fases o secuencias y el escenario de atmósfera
mixta no afirma que la proporción real del Cusco sea 50:50.

Las curvas de calibración son de IntCal y no se incluyen en el ZIP de depósito;
el programa las descarga desde el sitio oficial y registra sus SHA-256.
El catálogo ofrece enlaces públicos para 77 de las 94 filas del inventario.
Las 13 fechas de Batán Urqu provienen de un informe local sin enlace público
verificado; se identifican como tales y requieren cotejo independiente antes
de sustentar una conclusión cronológica decisiva.

## Palabras clave propuestas

radiocarbono; calibración radiocarbónica; Cusco; arqueología andina;
SHCal20; IntCal20; simulación; software científico; cronología inka.

## Relaciones bibliográficas prioritarias

- Hogg et al. (2020), SHCal20: <https://doi.org/10.1017/RDC.2020.59>.
- Reimer et al. (2020), IntCal20: <https://doi.org/10.1017/RDC.2020.41>.
- Delgado González et al. (2024), Machuqolqa:
  <https://doi.org/10.18800/boletindearqueologiapucp.202401.003>.
- Guevara Flores y Acero Valencia (2023), Pukara Pantillijlla:
  <https://hdl.handle.net/20.500.12918/7753>.
- Shadik et al. (2024), Acopia: <https://doi.org/10.3390/plants13071019>.

Estas referencias no sustituyen el catálogo de todas las fuentes del CSV.
