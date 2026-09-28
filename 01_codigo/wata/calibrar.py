"""Calibración simple de una edad radiocarbónica.

Método clásico (el mismo principio de OxCal y CALIB): para cada año
calendario t la verosimilitud es

    L(t) ∝ exp(−(R − μ(t))² / 2(σ² + s(t)²)) / √(σ² + s(t)²)

con R ± σ la edad del laboratorio y μ(t) ± s(t) la curva. Con una prior
uniforme en el tiempo, la distribución calibrada es L normalizada.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .curvas import Curva, cargar

NIVELES = (0.683, 0.954)


def bp_a_anio(cal_bp: float) -> int:
    """Año cal BP → año astronómico (1 d. C. = 1, 1 a. C. = 0)."""
    return int(round(1950 - cal_bp))


def formato_anio(anio_astronomico: int, era: str = "d. C.") -> str:
    """Año astronómico → texto «1438 d. C.» o «250 a. C.» (sin año cero)."""
    if anio_astronomico >= 1:
        return f"{anio_astronomico} {era}"
    antes = era.replace("d.", "a.").replace("D.", "A.")
    return f"{1 - anio_astronomico} {antes}"


@dataclass
class Intervalo:
    desde: int  # año astronómico inicial
    hasta: int  # año astronómico final
    prob: float  # probabilidad contenida

    def texto(self, era: str = "d. C.") -> str:
        a, b = formato_anio(self.desde, era), formato_anio(self.hasta, era)
        if self.desde == self.hasta:
            return f"{b} ({self.prob * 100:.1f} %)"
        if self.desde >= 1 and self.hasta >= 1:
            a = str(self.desde)
        elif self.desde < 1 and self.hasta < 1:
            a = str(1 - self.desde)
        return f"{a}–{b} ({self.prob * 100:.1f} %)"


@dataclass
class Calibracion:
    nombre: str
    edad: float
    sigma: float
    curva: str
    cal_bp: np.ndarray
    densidad: np.ndarray  # suma 1 sobre la rejilla anual
    avisos: list[str] = field(default_factory=list)

    @property
    def anios(self) -> np.ndarray:
        return 1950 - self.cal_bp

    def hpd(self, nivel: float = 0.954) -> list[Intervalo]:
        """Intervalos de máxima densidad (pueden ser varios, disjuntos)."""
        orden = np.argsort(self.densidad)[::-1]
        acumulada = np.cumsum(self.densidad[orden])
        n = int(np.searchsorted(acumulada, nivel)) + 1
        dentro = np.zeros(self.densidad.size, dtype=bool)
        dentro[orden[:n]] = True
        intervalos = []
        i = 0
        while i < dentro.size:
            if not dentro[i]:
                i += 1
                continue
            j = i
            while j + 1 < dentro.size and dentro[j + 1]:
                j += 1
            prob = float(self.densidad[i : j + 1].sum())
            # cal_bp asciende: el año más reciente es el de menor cal BP
            intervalos.append(Intervalo(bp_a_anio(self.cal_bp[j]), bp_a_anio(self.cal_bp[i]), prob))
            i = j + 1
        return sorted(intervalos, key=lambda x: x.desde)

    def mediana(self) -> int:
        acumulada = np.cumsum(self.densidad)
        return bp_a_anio(self.cal_bp[int(np.searchsorted(acumulada, 0.5))])

    def media(self) -> float:
        return float(np.sum(self.anios * self.densidad))

    def prob_entre(self, desde: int, hasta: int) -> float:
        """Probabilidad de que el evento caiga entre dos años astronómicos."""
        a = self.anios
        return float(self.densidad[(a >= desde) & (a <= hasta)].sum())

    def resumen(self, era: str = "d. C.") -> dict:
        return {
            "nombre": self.nombre,
            "edad_ap": self.edad,
            "sigma": self.sigma,
            "curva": self.curva,
            "rango_68": "; ".join(i.texto(era) for i in self.hpd(0.683)),
            "rango_95": "; ".join(i.texto(era) for i in self.hpd(0.954)),
            "mediana": formato_anio(self.mediana(), era),
            "avisos": " | ".join(self.avisos),
        }


def calibrar(
    edad: float,
    sigma: float,
    curva: str | Curva = "shcal20",
    nombre: str = "",
    margen_sigmas: float = 8.0,
) -> Calibracion:
    """Calibra una edad convencional ``edad ± sigma`` (años 14C BP)."""
    if sigma <= 0:
        raise ValueError("La sigma del laboratorio debe ser positiva")
    c = cargar(curva) if isinstance(curva, str) else curva
    var = sigma**2 + c.sigma**2
    z2 = (edad - c.edad) ** 2 / var
    # recorte a la zona con verosimilitud apreciable, por velocidad
    util = z2 < margen_sigmas**2
    if not util.any():
        raise ValueError(f"{edad} ± {sigma} BP queda fuera de la curva {c.nombre}")
    idx = np.flatnonzero(util)
    lo, hi = max(idx[0] - 1, 0), min(idx[-1] + 1, c.cal_bp.size - 1)
    tramo = slice(lo, hi + 1)
    dens = np.exp(-0.5 * z2[tramo]) / np.sqrt(var[tramo])
    dens /= dens.sum()
    avisos = []
    if dens[0] > 1e-4 * dens.max() and lo == 0:
        avisos.append("la distribución toca el extremo reciente de la curva (1950)")
    if dens[-1] > 1e-4 * dens.max() and hi == c.cal_bp.size - 1:
        avisos.append("la distribución toca el extremo antiguo de la curva")
    return Calibracion(
        nombre=nombre or f"{edad:g}±{sigma:g}",
        edad=edad,
        sigma=sigma,
        curva=c.nombre,
        cal_bp=c.cal_bp[tramo],
        densidad=dens,
        avisos=avisos,
    )


def sumar(calibraciones: list[Calibracion]) -> Calibracion:
    """Suma de probabilidades (SPD) normalizada. Solo descriptiva."""
    lo = min(int(c.cal_bp[0]) for c in calibraciones)
    hi = max(int(c.cal_bp[-1]) for c in calibraciones)
    eje = np.arange(lo, hi + 1)
    total = np.zeros(eje.size)
    for c in calibraciones:
        total[int(c.cal_bp[0]) - lo : int(c.cal_bp[-1]) - lo + 1] += c.densidad
    total /= total.sum()
    return Calibracion(
        nombre=f"Suma de {len(calibraciones)} fechados",
        edad=float("nan"),
        sigma=float("nan"),
        curva=calibraciones[0].curva,
        cal_bp=eje,
        densidad=total,
    )
