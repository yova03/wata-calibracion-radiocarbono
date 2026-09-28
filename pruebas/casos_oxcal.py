"""Casos publicados calibrados con OxCal, para validar wata.

Ziółkowski, M., Bastante Abuhadba, J. M., Hogg, A., Sieczkowska, D.,
Rakowski, A., Pawlyta, J. y Manning, S. W. (2021). When did the Incas build
Machu Picchu and its satellite sites? New approaches based on radiocarbon
dating. Radiocarbon, 63(4), 1133–1148. https://doi.org/10.1017/RDC.2020.79
Tabla 3, p. 1141: OxCal 4.3.2, curva mixta 50 % ± 10 % SHCal13 + IntCal13,
calibración simple (sin modelo). Rangos transcritos de la tabla impresa.

Erratas del original que no se usan: el rango 1σ de Waikato 46934 aparece
invertido («1440–1415») y el 2σ de 46933 lleva «94.2.5 %».
"""

CURVA = "mixta13:0.5:0.1"

# código, sitio, edad AP, sigma, rangos 68.2 %, rangos 95.4 % (años d. C.)
CASOS = [
    ("Wk-48116", "Machu Picchu", 560, 20, [(1400, 1421)], [(1329, 1338), (1393, 1432)]),
    ("Wk-46935", "Machu Picchu", 490, 18, [(1430, 1445)], [(1420, 1450)]),
    ("Wk-46936", "Machu Picchu", 441, 17, [(1444, 1460)], [(1439, 1479)]),
    ("Wk-48113", "Chachabamba", 434, 19, [(1445, 1468)], [(1440, 1490)]),
    ("Wk-48114", "Chachabamba", 475, 19, [(1434, 1450)], [(1425, 1455)]),
    ("Wk-46938", "Chachabamba", 338, 18, [(1514, 1529), (1539, 1585), (1620, 1631)],
     [(1499, 1600), (1613, 1640)]),
    ("Wk-46939", "Chachabamba", 391, 15, [(1463, 1497), (1602, 1611)], [(1454, 1510), (1590, 1619)]),
    ("Wk-46940", "Chachabamba", 499, 15, [(1428, 1441)], [(1420, 1446)]),
    ("Wk-48115", "Choqesuysuy", 209, 20, [(1666, 1676), (1740, 1798)],
     [(1656, 1684), (1732, 1804), (1943, 1950)]),
    ("Wk-46933", "Choqesuysuy", 423, 16, [(1450, 1472)], [(1445, 1493), (1604, 1607)]),
    ("Wk-46934", "Choqesuysuy", 567, 16, None, [(1328, 1340), (1392, 1425)]),
]
