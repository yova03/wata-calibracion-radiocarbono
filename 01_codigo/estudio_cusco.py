"""Simulaciones para la cronología del Cusco (siglos XI–XVI).

Tres preguntas, cada una con su tabla y su figura en 04_resultados/simulacion:

1. ¿Qué tan ancho sale el rango 95.4 % de un fechado único según el año
   verdadero? (la forma de la curva manda: pendientes y mesetas)
2. ¿Puede un fechado único decir si algo ocurrió antes o después de 1438,
   el año que las fuentes escritas dan al ascenso de Pachacuti?
3. ¿Cuánto mueve el resultado la elección de curva (SHCal20, IntCal20 o
   mixta 50:50) para edades de 250 a 1200 AP?
4. Si la atmósfera del Cusco fuera una mezcla 50:50 y se calibrara solo con
   SHCal20, ¿cuánto se equivocaría la fecha y cuántas veces el rango 95.4 %
   dejaría fuera el año verdadero?

    python 01_codigo/estudio_cusco.py [-n 200]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wata import calibrar  # noqa: E402
from wata.graficos import REJILLA, SERIE, TINTA, TINTA_2, plt  # noqa: E402
from wata.simular import distinguir, recuperar  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "04_resultados" / "simulacion"
CURVAS = [("shcal20", "SHCal20"), ("mixta:0.5:0.1", "Mixta 50:50 ± 10 %"), ("intcal20", "IntCal20")]
PACHACUTI = 1438


def _guardar(nombre: str, filas: list[dict]) -> None:
    with open(SALIDA / nombre, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def _figura(ancho=6.3, alto=3.4):
    fig, ax = plt.subplots(figsize=(ancho, alto), dpi=300)
    ax.grid(color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    return fig, ax


def _cerrar(fig, ax, nombre: str) -> None:
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(SALIDA / nombre)
    plt.close(fig)


def estudio_recuperacion(n: int, sigma: float = 25) -> None:
    anios = list(range(1000, 1601, 10))
    filas = []
    fig, ax = _figura()
    for k, (curva, rotulo) in enumerate(CURVAS):
        anchos = []
        for a in anios:
            r = recuperar(a, sigma, curva, n=n)
            anchos.append(r.ancho_95_mediana)
            filas.append({"curva": curva, "anio": a, "sigma": sigma, "n": n,
                          "cobertura_95": round(r.cobertura_95, 3),
                          "ancho_95_mediana": r.ancho_95_mediana,
                          "tramos_mediana": r.n_intervalos_mediana,
                          "error_mediana": r.error_mediana, "sesgo_mediana": r.sesgo_mediana})
        ax.plot(anios, anchos, color=SERIE[k], linewidth=2, label=rotulo)
    ax.axvline(PACHACUTI, color=TINTA_2, linewidth=0.8, linestyle="--")
    ax.text(PACHACUTI, ax.get_ylim()[1], " 1438", fontsize=7, color=TINTA, va="top")
    ax.set_xlabel("Año verdadero de la muestra (d. C.)")
    ax.set_ylabel(f"Años cubiertos por el rango 95.4 %\n(fechado único ± {sigma:g} AP, mediana)")
    _guardar("recuperacion.csv", filas)
    _cerrar(fig, ax, "fig_ancho_rango.png")


def estudio_1438(n: int, sigma: float = 20) -> None:
    anios = list(range(1400, 1481, 5))
    filas = []
    fig, ax = _figura()
    for k, (curva, rotulo) in enumerate(CURVAS):
        probs = [distinguir(a, PACHACUTI, sigma, curva, n=n) for a in anios]
        filas += [{"curva": curva, "anio": a, "sigma": sigma, "n": n, "prob_antes_1438": round(p, 3)}
                  for a, p in zip(anios, probs)]
        ax.plot(anios, probs, color=SERIE[k], linewidth=2, marker="o", markersize=3, label=rotulo)
    ax.axvline(PACHACUTI, color=TINTA_2, linewidth=0.8, linestyle="--")
    ax.axhline(0.5, color=TINTA_2, linewidth=0.6)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Año verdadero de la muestra (d. C.)")
    ax.set_ylabel(f"Probabilidad calibrada de «antes de 1438»\n(fechado único ± {sigma:g} AP, media)")
    _guardar("antes_1438.csv", filas)
    _cerrar(fig, ax, "fig_antes_1438.png")


def estudio_efecto_curva(sigma: float = 25) -> None:
    edades = list(range(250, 1201, 5))
    filas = []
    fig, ax = _figura()
    base = {e: calibrar(e, sigma, "shcal20") for e in edades}
    for k, (curva, rotulo) in enumerate(CURVAS[1:], start=1):
        difs = []
        for e in edades:
            otra = calibrar(e, sigma, curva)
            d = otra.mediana() - base[e].mediana()
            difs.append(d)
            filas.append({"edad_ap": e, "sigma": sigma, "curva": curva,
                          "mediana_shcal20": base[e].mediana(), "mediana_curva": otra.mediana(),
                          "diferencia_anios": d,
                          "rango95_shcal20": "; ".join(r.texto() for r in base[e].hpd()),
                          "rango95_curva": "; ".join(r.texto() for r in otra.hpd())})
        ax.plot(edades, difs, color=SERIE[k], linewidth=2, label=f"{rotulo} − SHCal20")
    ax.axhline(0, color=TINTA_2, linewidth=0.8)
    ax.set_xlabel(f"Edad radiocarbónica medida (años AP, ± {sigma:g})")
    ax.set_ylabel("Diferencia de la mediana calibrada\nrespecto de SHCal20 (años)")
    _guardar("efecto_curva.csv", filas)
    _cerrar(fig, ax, "fig_efecto_curva.png")


def estudio_curva_equivocada(n: int, sigma: float = 25) -> None:
    anios = list(range(1000, 1601, 10))
    casos = [("mixta:0.5:0.1", "Calibrada con la mezcla (curva correcta)"),
             ("shcal20", "Calibrada con SHCal20"), ("intcal20", "Calibrada con IntCal20")]
    filas = []
    fig, ax = _figura()
    for k, (curva, rotulo) in enumerate(casos):
        sesgos = []
        for a in anios:
            r = recuperar(a, sigma, curva, n=n, curva_real="mixta:0.5:0.1")
            sesgos.append(r.sesgo_mediana)
            filas.append({"curva_real": "mixta:0.5:0.1", "curva_calibracion": curva, "anio": a,
                          "sigma": sigma, "n": n, "cobertura_95": round(r.cobertura_95, 3),
                          "sesgo_mediana": r.sesgo_mediana, "error_mediana": r.error_mediana})
        ax.plot(anios, sesgos, color=SERIE[[1, 0, 2][k]], linewidth=2, label=rotulo)
    ax.axhline(0, color=TINTA_2, linewidth=0.8)
    ax.set_xlabel("Año verdadero de la muestra (d. C.), atmósfera mixta 50:50")
    ax.set_ylabel("Sesgo de la mediana calibrada (años)\n(positivo: fecha más reciente)")
    _guardar("curva_equivocada.csv", filas)
    _cerrar(fig, ax, "fig_curva_equivocada.png")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("-n", type=int, default=200, help="simulaciones por año")
    a = p.parse_args()
    SALIDA.mkdir(parents=True, exist_ok=True)
    estudio_efecto_curva()
    estudio_1438(a.n)
    estudio_recuperacion(a.n)
    estudio_curva_equivocada(a.n)
    print(f"Resultados en {SALIDA}")


if __name__ == "__main__":
    main()
