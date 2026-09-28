"""Contraste independiente: wata frente a IOSACal 0.7 (Costa et al., GPL-3).

IOSACal trae los mismos archivos SHCal20 e IntCal20 (idéntico SHA-256), así
que las diferencias solo pueden venir de la implementación. Compara los
extremos de los rangos 95.4 % y 68.3 % en una malla de edades.

    set IOSACAL_PATH=<carpeta donde se instaló iosacal>
    python pruebas/comparar_iosacal.py
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "01_codigo"))
if os.environ.get("IOSACAL_PATH"):
    sys.path.insert(0, os.environ["IOSACAL_PATH"])

from iosacal import R  # noqa: E402
from iosacal.hpd import hpd_interval  # noqa: E402

from wata import calibrar  # noqa: E402


def rangos_iosacal(edad, sigma, curva, nivel):
    cal = R(edad, sigma, "x").calibrate(curva)
    # IOSACal devuelve (desde, hasta, %) en cal BP
    tramos = hpd_interval(cal, 1 - nivel)
    return sorted((int(1950 - max(t[0], t[1])), int(1950 - min(t[0], t[1]))) for t in tramos)


def rangos_wata(edad, sigma, curva, nivel):
    return [(r.desde, r.hasta) for r in calibrar(edad, sigma, curva).hpd(nivel)]


def main() -> None:
    filas, peor = [], 0
    for curva in ("shcal20", "intcal20"):
        for sigma in (20, 40):
            for edad in range(200, 4001, 50):
                for nivel in (0.683, 0.954):
                    a = rangos_wata(edad, sigma, curva, nivel)
                    b = rangos_iosacal(edad, sigma, curva, nivel)
                    mismo_n = len(a) == len(b)
                    dif = max(abs(x - y) for p, q in zip(a, b) for x, y in zip(p, q)) if mismo_n else None
                    if dif is not None:
                        peor = max(peor, dif)
                    filas.append({"curva": curva, "edad": edad, "sigma": sigma, "nivel": nivel,
                                  "wata": a, "iosacal": b, "mismos_tramos": mismo_n, "dif_max": dif})
    salida = RAIZ / "04_resultados" / "contraste_iosacal.csv"
    with open(salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    iguales = sum(f["mismos_tramos"] for f in filas)
    difs = [f["dif_max"] for f in filas if f["dif_max"] is not None]
    exactos = sum(d <= 1 for d in difs)
    print(f"{len(filas)} comparaciones · mismo número de tramos en {iguales}")
    print(f"extremos a ≤1 año en {exactos} de {len(difs)} · diferencia máxima {peor} años")
    print(f"detalle → {salida}")


if __name__ == "__main__":
    main()
