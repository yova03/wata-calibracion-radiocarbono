"""wata — calibración abierta de fechados radiocarbónicos, en español.

«Wata» es «año» en quechua. Calibración simple con SHCal20, IntCal20 o una
curva mixta, rangos de máxima densidad, suma de probabilidades y
simulación de fechados.
"""

from .calibrar import Calibracion, Intervalo, calibrar, formato_anio, sumar
from .curvas import Curva, cargar, mezclar

__version__ = "0.1.0"
__all__ = ["Calibracion", "Curva", "Intervalo", "calibrar", "cargar", "formato_anio", "mezclar", "sumar"]
