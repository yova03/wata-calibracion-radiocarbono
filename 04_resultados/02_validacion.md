---
objetivo: "Documentar que wata reproduce los rangos calibrados de OxCal y de IOSACal, con sus diferencias explicadas."
uso: "Citar al justificar el uso de wata en una tesis. Se regenera con pruebas/validar_oxcal.py y pruebas/comparar_iosacal.py."
---

# Validación de wata frente a OxCal e IOSACal

## Contra OxCal: fechados de Machu Picchu

Ziółkowski et al. (2021, tabla 3, p. 1141) publican 11 fechados de Machu
Picchu, Chachabamba y Choqesuysuy calibrados con OxCal 4.3.2, sin modelo
bayesiano, con una curva mixta 50 % ± 10 % de SHCal13 e IntCal13. wata los
recalculó con las mismas curvas y la fórmula de mezcla de OxCal
(`--curva mixta13:0.5:0.1`).

| Resultado | Valor |
|---|---|
| Rangos comparados (68.2 % y 95.4 %) | 21 |
| Con el mismo número de tramos | 20 |
| Diferencia máxima entre extremos | 2 años |
| Diferencia mediana | 1 año |

El único rango con distinto número de tramos es el 68.2 % de Wk-48115
(209 ± 20 AP): OxCal da 1740–1798 d. C. en un solo tramo y wata lo parte en
cuatro, separados por huecos de uno o dos años. Esa edad cae en una meseta de
la curva; la causa probable es que wata calcula año por año y OxCal con un
paso mayor, que no separa mínimos tan cortos.

Dos erratas del original quedaron fuera de la comparación: el rango 1σ de
Wk-46934 impreso como «1440–1415» y el porcentaje «94.2.5 %» de Wk-46933.
Para Wk-46934, wata obtiene 1400–1414 d. C., lo que sugiere que el impreso
debía decir 1400–1415.

Detalle por fechado: [`validacion_oxcal.csv`](validacion_oxcal.csv).

## Contra IOSACal 0.7.0

IOSACal es otra implementación abierta (Python, GPL-3) que trae los mismos
archivos SHCal20 e IntCal20, con idéntico SHA-256. Se compararon 616 rangos:
edades de 200 a 4000 AP cada 50 años, sigmas de 20 y 40, ambas curvas y ambos
niveles.

| Resultado | Valor |
|---|---|
| Mismo número de tramos | 508 de 616 |
| Extremos a un año o menos, entre esos 508 | 446 |
| Diferencia máxima | 11 años (2650 ± 20 AP, meseta de Hallstatt) |

Las diferencias vienen de tres decisiones de IOSACal, no de wata:

1. recorta la curva a la media del laboratorio ± 5σ sin sumar la sigma de la
   curva, y pierde probabilidad en las colas;
2. excluye el último punto del tramo recortado;
3. descarta los tramos de un solo año.

Al imitar esas tres decisiones dentro de wata, se reproducen exactamente los
rangos de IOSACal en los cinco casos revisados (200, 650, 800 y 2650 ± 20
en SHCal20; 2250 ± 20 en IntCal20, salvo un tramo de un año). wata solo
descarta los años situados a más de 8σ combinadas (laboratorio y curva),
donde la probabilidad es despreciable.

Detalle: [`contraste_iosacal.csv`](contraste_iosacal.csv).

## Pruebas automáticas

`python -m pytest pruebas` ejecuta siete pruebas: formato de años sin año
cero, normalización, rangos que contienen el nivel pedido, curva mixta en sus
extremos, desfase SHCal20/IntCal20, reproducción de OxCal (diferencia ≤ 3
años) y cobertura de la simulación. Resultado al 28/09/2026: 7 de 7 pasan.

## Referencia

Ziółkowski, M., Bastante Abuhadba, J. M., Hogg, A., Sieczkowska, D.,
Rakowski, A., Pawlyta, J. y Manning, S. W. (2021). When did the Incas build
Machu Picchu and its satellite sites? New approches [*sic*] based on
radiocarbon dating. *Radiocarbon, 63*(4), 1133–1148.
https://doi.org/10.1017/RDC.2020.79
