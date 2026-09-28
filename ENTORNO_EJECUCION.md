---
objetivo: "Registrar el entorno con el que se generaron y revisaron los resultados del depósito."
uso: "Consultar junto con requirements.txt al reproducir la versión 0.1.0."
---

# Entorno de ejecución de wata 0.1.0

Los resultados incluidos en este depósito se generaron y revisaron el
28 de setiembre de 2026 en Windows con Python 3.12.10 (64 bits),
NumPy 1.26.4 y Matplotlib 3.10.8. Las siete pruebas existentes se ejecutaron
con pytest 8.4.2. [`requirements.txt`](requirements.txt) indica versiones
mínimas para una instalación nueva; este archivo registra las versiones
efectivamente usadas en la revisión.

Las curvas SHCal20, IntCal20, SHCal13 e IntCal13 se obtienen desde IntCal.
Sus hashes SHA-256 están en [`ORIGEN.md`](02_datos/curvas/ORIGEN.md).
El ZIP no contiene copias de esas curvas.
