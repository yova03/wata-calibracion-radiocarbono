---
objetivo: "Evaluar si es viable una herramienta abierta y en español para calibrar fechados radiocarbónicos, frente al software existente a setiembre de 2026."
uso: "Leer para justificar el proyecto: qué existe, qué falta y qué aporta wata. Cada dato lleva su fuente."
---

# Viabilidad de una herramienta abierta de calibración en español

**Veredicto: viable.** La matemática de la calibración simple es pública y
estable; las curvas oficiales se descargan libremente; la primera versión
reproduce los rangos publicados con OxCal con una diferencia de uno o dos
años (ver [validación](02_validacion.md)). Lo difícil no es calcular, sino
ganar credibilidad: por eso cada resultado queda contrastado con OxCal e
IOSACal.

## Estado del software a setiembre de 2026

| Programa | Última versión | Fecha | Código abierto | Forma | Consultado |
|---|---|---|---|---|---|
| OxCal | 4.4.4 | 15/04/2021 | No declara licencia abierta | Web y escritorio | [historial oficial](https://c14.arch.ox.ac.uk/oxcalhelp/hlp_develop.html) |
| CALIB | 8.2 | sin confirmar (calib.org no respondió) | No | Web y escritorio | — |
| ChronoModel | 4.0.0 | 24/09/2026 | Sí, CeCILL 2.1 | Escritorio (C++/Qt) | [GitHub](https://github.com/Chronomodel/chronomodel/releases) |
| IOSACal | 0.7.0 | 14/02/2026 | Sí, GPL-3 | Paquete Python | [Zenodo](https://zenodo.org/records/18651152) |
| rcarbon | 1.5.2 | 28/07/2025 | Sí | Paquete R | [CRAN](https://cran.r-project.org/web/packages/rcarbon/index.html) |
| rintcal, rice, clam, rbacon | activos | 2025–2026 | Sí | Paquetes R | CRAN |

El historial de OxCal, programa de referencia de la disciplina, no registra
versiones posteriores a la 4.4.4. Al 28 de setiembre de 2026 suma cinco años
y cinco meses sin actualizarse: la afirmación inicial del proyecto («hace
cuatro años») se queda corta. En ninguna de las páginas consultadas aparece
una interfaz en español.

## El vacío que cubre wata

Existen alternativas abiertas, pero ninguna reúne estas condiciones para
quien investiga en el Cusco:

1. **Español de principio a fin**: órdenes, mensajes, tablas y figuras, con
   años en «d. C.» y «a. C.» sin año cero.
2. **Elección de curva explícita para los Andes tropicales**: SHCal20,
   IntCal20 o una mezcla con su proporción e incertidumbre, que es el debate
   abierto por Marsh et al. (2018).
3. **Salidas listas para una tesis**: rangos 68.3 % y 95.4 % en texto, CSV
   y figura a 300 ppp.
4. **Sin conexión y sin instalar R**: Python con numpy y matplotlib; las
   curvas quedan en la carpeta del proyecto.
5. **Trazabilidad**: curvas con SHA-256, pruebas automáticas contra valores
   publicados.

## Curva para el Cusco: una decisión, no un valor por defecto

- Hogg et al. (2020) publican SHCal20, estiman que el hemisferio sur da
  edades 36 ± 27 años 14C más antiguas que el norte y sugieren dónde sería
  más apropiada una mezcla a partes iguales de ambas curvas.
- Marsh et al. (2018) advierten que el monzón sudamericano lleva aire del
  hemisferio norte sobre buena parte del continente y proponen, mientras no
  haya anillos de árboles locales, «a mixed calibration curve … as a third
  calibration option».
- En la práctica andina conviven las tres opciones: Ziółkowski et al.
  (2021) calibran Machu Picchu con una mezcla 50 % ± 10 % de SHCal13 e
  IntCal13; Burger et al. (2021) usan SHCal20.

wata usa SHCal20 por defecto y obliga a declarar la curva en cada resultado.
El [estudio de simulación](03_simulacion_cusco.md) mide cuánto cambia la
fecha según la curva elegida.

## Riesgos

| Riesgo | Tratamiento |
|---|---|
| Errores numéricos que pasen inadvertidos | Pruebas contra OxCal (Ziółkowski et al., 2021) e IOSACal en cada cambio |
| Condiciones de uso de las curvas | Cita obligatoria; descarga desde intcal.org ([origen](../02_datos/curvas/ORIGEN.md)) |
| Una nueva IntCal/SHCal | El cargador acepta cualquier `.14c`; basta añadir el archivo |
| Uso de la suma de probabilidades como demografía | Se ofrece solo como descripción; las advertencias van en el informe |
| Modelos bayesianos (fases, límites) | Fuera de la versión 0.1; segunda etapa |

## Referencias

Burger, R. L., Salazar, L. C., Nesbitt, J., Washburn, E. y Fehren-Schmitz, L.
(2021). New AMS dates for Machu Picchu: Results and implications.
*Antiquity, 95*(383), 1265–1279. https://doi.org/10.15184/aqy.2021.99

Hogg, A. G., Heaton, T. J., Hua, Q., Palmer, J. G., Turney, C. S. M.,
Southon, J., Bayliss, A., Blackwell, P. G., Boswijk, G., Bronk Ramsey, C.,
Pearson, C., Petchey, F., Reimer, P., Reimer, R. y Wacker, L. (2020).
SHCal20 Southern Hemisphere calibration, 0–55,000 years cal BP.
*Radiocarbon, 62*(4), 759–778. https://doi.org/10.1017/RDC.2020.59

Marsh, E. J., Bruno, M. C., Fritz, S. C., Baker, P., Capriles, J. M. y
Hastorf, C. A. (2018). IntCal, SHCal, or a mixed curve? Choosing a 14C
calibration curve for archaeological and paleoenvironmental records from
tropical South America. *Radiocarbon, 60*(3), 925–940.
https://doi.org/10.1017/RDC.2018.16

Ziółkowski, M., Bastante Abuhadba, J. M., Hogg, A., Sieczkowska, D.,
Rakowski, A., Pawlyta, J. y Manning, S. W. (2021). When did the Incas build
Machu Picchu and its satellite sites? New approches [*sic*] based on
radiocarbon dating. *Radiocarbon, 63*(4), 1133–1148.
https://doi.org/10.1017/RDC.2020.79
