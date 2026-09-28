"""Compara wata con los rangos publicados por OxCal (ver casos_oxcal.py).

    python pruebas/validar_oxcal.py

Escribe 04_resultados/validacion_oxcal.csv y resume la diferencia en años
entre los extremos de cada rango.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "01_codigo"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from casos_oxcal import CASOS, CURVA  # noqa: E402

from wata import calibrar  # noqa: E402


def comparar(publicado, calculado):
    """Diferencia máxima entre extremos, si hay el mismo número de tramos."""
    if publicado is None:
        return None, None
    if len(publicado) != len(calculado):
        return False, None
    return True, max(max(abs(a - c), abs(b - d)) for (a, b), (c, d) in zip(publicado, calculado))


def validar() -> list[dict]:
    filas = []
    for codigo, sitio, edad, sigma, r68, r95 in CASOS:
        cal = calibrar(edad, sigma, CURVA, nombre=codigo)
        for nivel, pub in ((0.683, r68), (0.954, r95)):
            calc = [(r.desde, r.hasta) for r in cal.hpd(nivel)]
            mismo, dif = comparar(pub, calc)
            filas.append({"codigo": codigo, "sitio": sitio, "edad": edad, "sigma": sigma,
                          "nivel": nivel, "oxcal": pub, "wata": calc,
                          "mismos_tramos": mismo, "dif_max_anios": dif})
    return filas


def main() -> None:
    filas = validar()
    salida = RAIZ / "04_resultados" / "validacion_oxcal.csv"
    with open(salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    for f in filas:
        marca = "--" if f["mismos_tramos"] is None else ("OK" if f["mismos_tramos"] else "!=")
        print(f"{marca} {f['codigo']} {f['edad']}±{f['sigma']} {f['nivel']:.3f}  "
              f"OxCal {f['oxcal']}  wata {f['wata']}  Δ={f['dif_max_anios']}")
    difs = [f["dif_max_anios"] for f in filas if f["dif_max_anios"] is not None]
    print(f"\n{len(difs)} rangos comparables · Δ máx {max(difs)} años · Δ mediana "
          f"{sorted(difs)[len(difs) // 2]} años -> {salida}")


if __name__ == "__main__":
    main()
