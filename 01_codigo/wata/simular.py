"""Simulación de fechados: ¿cuánto recupera la calibración un año conocido?

Para un año calendario verdadero se toma la edad de la curva en ese año,
se añade la dispersión de la curva y el error del laboratorio, se calibra
y se mide si el año verdadero cae dentro del rango y cuán ancho es. Es el
equivalente de R_Simulate de OxCal repetido muchas veces.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .calibrar import calibrar
from .curvas import Curva, cargar


def edad_simulada(anio: int, sigma: float, curva: Curva, rng: np.random.Generator) -> float:
    """Edad 14C que un laboratorio podría medir para una muestra del año dado."""
    mu, s = curva.en(1950 - anio)
    return float(np.round(rng.normal(mu, np.sqrt(s**2 + sigma**2))))


@dataclass
class Recuperacion:
    anio: int
    sigma: float
    curva: str
    n: int
    cobertura_95: float  # fracción de simulaciones cuyo rango 95.4 % contiene el año
    ancho_95_mediana: float  # años cubiertos por el rango 95.4 % (mediana)
    n_intervalos_mediana: float
    error_mediana: float  # |mediana calibrada − año verdadero|, mediana
    sesgo_mediana: float  # mediana calibrada − año verdadero, mediana (con signo)


def recuperar(
    anio: int,
    sigma: float = 25,
    curva: str | Curva = "shcal20",
    n: int = 500,
    semilla: int = 14,
    curva_real: str | Curva | None = None,
) -> Recuperacion:
    """Simula con ``curva_real`` (por defecto la misma) y calibra con ``curva``.

    Usar dos curvas distintas mide el error de elegir mal: por ejemplo, una
    atmósfera mixta calibrada solo con SHCal20.
    """
    c = cargar(curva) if isinstance(curva, str) else curva
    real = c if curva_real is None else (cargar(curva_real) if isinstance(curva_real, str) else curva_real)
    rng = np.random.default_rng(semilla + anio)
    dentro = 0
    anchos_l, tramos_l, errores_l = [], [], []
    for _ in range(n):
        cal = calibrar(edad_simulada(anio, sigma, real, rng), sigma, c)
        rangos = cal.hpd(0.954)
        dentro += any(r.desde <= anio <= r.hasta for r in rangos)
        anchos_l.append(sum(r.hasta - r.desde + 1 for r in rangos))
        tramos_l.append(len(rangos))
        errores_l.append(cal.mediana() - anio)
    return Recuperacion(
        anio=anio,
        sigma=sigma,
        curva=c.nombre,
        n=n,
        cobertura_95=dentro / n,
        ancho_95_mediana=float(np.median(anchos_l)),
        n_intervalos_mediana=float(np.median(tramos_l)),
        error_mediana=float(np.median(np.abs(errores_l))),
        sesgo_mediana=float(np.median(errores_l)),
    )


def distinguir(
    anio_a: int,
    anio_b: int,
    sigma: float = 25,
    curva: str | Curva = "shcal20",
    n: int = 500,
    semilla: int = 14,
) -> float:
    """Probabilidad media de que un fechado del año A se asigne antes del año B.

    Sirve para preguntar, por ejemplo, si un fechado único puede decir si
    una construcción es anterior o posterior a 1438.
    """
    c = cargar(curva) if isinstance(curva, str) else curva
    rng = np.random.default_rng(semilla + anio_a)
    probs = []
    for _ in range(n):
        cal = calibrar(edad_simulada(anio_a, sigma, c, rng), sigma, c)
        probs.append(cal.prob_entre(-100000, anio_b - 1))
    return float(np.mean(probs))
