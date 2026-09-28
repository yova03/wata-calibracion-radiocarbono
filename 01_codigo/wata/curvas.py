"""Carga de curvas de calibración y curvas mixtas.

Las curvas vienen de intcal.org en formato .14c (cal BP, edad 14C, sigma,
Δ14C, sigma). Se interpolan a una rejilla de un año calendario para que
todas las operaciones trabajen sobre el mismo eje.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

CARPETA_CURVAS = Path(__file__).resolve().parents[2] / "02_datos" / "curvas"
URL_CURVAS = "https://intcal.org/curves/"

CURVAS_OFICIALES = {
    "shcal20": "shcal20.14c",
    "intcal20": "intcal20.14c",
    # versiones de 2013: solo para reproducir cálculos publicados con ellas
    "shcal13": "shcal13.14c",
    "intcal13": "intcal13.14c",
}


@dataclass(frozen=True)
class Curva:
    """Curva sobre una rejilla anual en cal BP (0 = 1950 d. C.)."""

    nombre: str
    cal_bp: np.ndarray  # años cal BP, enteros ascendentes
    edad: np.ndarray  # edad radiocarbónica media (años 14C BP)
    sigma: np.ndarray  # incertidumbre 1σ de la curva

    def en(self, cal_bp: float | np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Edad 14C y sigma de la curva en uno o varios años cal BP."""
        return (
            np.interp(cal_bp, self.cal_bp, self.edad),
            np.interp(cal_bp, self.cal_bp, self.sigma),
        )


def leer_14c(ruta: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Lee un archivo .14c y devuelve (cal BP, edad, sigma) en orden ascendente."""
    filas = []
    for linea in ruta.read_text(encoding="utf-8", errors="replace").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        campos = linea.replace("\t", ",").split(",")
        filas.append([float(c) for c in campos[:3]])
    datos = np.array(filas)
    datos = datos[np.argsort(datos[:, 0])]
    return datos[:, 0], datos[:, 1], datos[:, 2]


def _a_rejilla_anual(nombre: str, cal: np.ndarray, edad: np.ndarray, sig: np.ndarray) -> Curva:
    rejilla = np.arange(int(np.ceil(cal.min())), int(np.floor(cal.max())) + 1)
    return Curva(
        nombre=nombre,
        cal_bp=rejilla,
        edad=np.interp(rejilla, cal, edad),
        sigma=np.interp(rejilla, cal, sig),
    )


def descargar(carpeta: Path | None = None) -> list[Path]:
    """Descarga las curvas oficiales de intcal.org y muestra su SHA-256."""
    import hashlib
    import urllib.request

    destino = carpeta or CARPETA_CURVAS
    destino.mkdir(parents=True, exist_ok=True)
    rutas = []
    for archivo in CURVAS_OFICIALES.values():
        ruta = destino / archivo
        if not ruta.exists():
            urllib.request.urlretrieve(URL_CURVAS + archivo, ruta)
        print(f"{archivo}  sha256 {hashlib.sha256(ruta.read_bytes()).hexdigest()}")
        rutas.append(ruta)
    return rutas


_CACHE: dict[str, Curva] = {}


def cargar(nombre: str = "shcal20", carpeta: Path | None = None) -> Curva:
    """Devuelve una curva oficial (shcal20, intcal20) o una mixta.

    Mixta: ``mixta:P`` donde P es la proporción de SHCal20 (0–1), p. ej.
    ``mixta:0.5``. Opcionalmente ``mixta:P:D`` con D la incertidumbre (1σ)
    de esa proporción, y ``mixta13:P:D`` para mezclar las curvas de 2013.
    """
    clave = nombre.lower().strip()
    if clave in _CACHE:
        return _CACHE[clave]
    if clave.startswith("mixta"):
        partes = clave.split(":")
        if len(partes) < 2:
            raise ValueError("Use mixta:P, con P = proporción de SHCal20 entre 0 y 1")
        p = float(partes[1])
        dp = float(partes[2]) if len(partes) > 2 else 0.0
        serie = "13" if clave.startswith("mixta13") else "20"
        curva = mezclar(cargar("shcal" + serie, carpeta), cargar("intcal" + serie, carpeta), p, dp)
        curva = Curva(nombre=clave, cal_bp=curva.cal_bp, edad=curva.edad, sigma=curva.sigma)
    else:
        if clave not in CURVAS_OFICIALES:
            raise ValueError(f"Curva desconocida: {nombre}. Opciones: shcal20, intcal20, mixta:P, shcal13, intcal13")
        ruta = (carpeta or CARPETA_CURVAS) / CURVAS_OFICIALES[clave]
        if not ruta.exists():
            raise FileNotFoundError(f"No está {ruta}; ejecute: python -m wata curvas")
        curva = _a_rejilla_anual(clave, *leer_14c(ruta))
    _CACHE[clave] = curva
    return curva


LIBBY = 8033.0  # vida media de Libby / ln 2, define la edad convencional


def mezclar(sur: Curva, norte: Curva, p_sur: float, dp: float = 0.0) -> Curva:
    """Curva mixta con la proporción ``p_sur`` de SHCal20 (± ``dp``).

    Sigue la fórmula de Mix_Curves de OxCal, que mezcla en concentración de
    radiocarbono (F14C) y no en edad:

        R = (1 − P)·R_norte + P·R_sur
        E = √[((1 − P)·E_norte)² + (P·E_sur)² + (D·(R_sur − R_norte))²]

    Fuente: https://c14.arch.ox.ac.uk/oxcal3/math_ca.htm (Mixed calibration curves).
    """
    if not 0.0 <= p_sur <= 1.0:
        raise ValueError("La proporción de SHCal20 debe estar entre 0 y 1")
    lo = max(sur.cal_bp[0], norte.cal_bp[0])
    hi = min(sur.cal_bp[-1], norte.cal_bp[-1])
    rejilla = np.arange(lo, hi + 1)

    def a_f14c(curva: Curva):
        edad, sig = curva.en(rejilla)
        f = np.exp(-edad / LIBBY)
        return f, f * sig / LIBBY

    fs, es = a_f14c(sur)
    fn, en_ = a_f14c(norte)
    f = (1 - p_sur) * fn + p_sur * fs
    ef = np.sqrt(((1 - p_sur) * en_) ** 2 + (p_sur * es) ** 2 + (dp * (fs - fn)) ** 2)
    nombre = f"mixta:{p_sur:g}" + (f":{dp:g}" if dp else "")
    return Curva(nombre=nombre, cal_bp=rejilla, edad=-LIBBY * np.log(f), sigma=LIBBY * ef / f)
