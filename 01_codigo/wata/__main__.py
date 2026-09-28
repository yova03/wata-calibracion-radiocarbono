"""Línea de comandos.

    python -m wata calibrar 450 25 --curva shcal20 --figura fig.png
    python -m wata lote fechados.csv --curva mixta:0.5 --salida tabla.csv
    python -m wata simular 1438 --sigma 25
    python -m wata curvas
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from . import __version__
from .calibrar import calibrar, formato_anio
from .curvas import descargar
from .graficos import figura_calibracion
from .simular import recuperar


def _imprimir(cal, era: str) -> None:
    print(f"{cal.nombre}: {cal.edad:g} ± {cal.sigma:g} AP · curva {cal.curva}")
    for nivel in (0.683, 0.954):
        print(f"  {nivel * 100:.1f} %: " + "; ".join(r.texto(era) for r in cal.hpd(nivel)))
    print(f"  mediana: {formato_anio(cal.mediana(), era)}")
    for aviso in cal.avisos:
        print(f"  aviso: {aviso}")


def cmd_calibrar(a) -> None:
    cal = calibrar(a.edad, a.sigma, a.curva, nombre=a.nombre)
    _imprimir(cal, a.era)
    if a.figura:
        print(f"  figura: {figura_calibracion(cal, Path(a.figura), a.era)}")


def cmd_lote(a) -> None:
    """CSV con columnas nombre (o codigo_lab), edad_ap, sigma."""
    filas = list(csv.DictReader(open(a.csv, encoding="utf-8-sig")))
    salida = []
    for f in filas:
        try:
            edad, sigma = float(f["edad_ap"]), float(f["sigma"])
        except (KeyError, ValueError):
            continue
        nombre = f.get("nombre") or f.get("codigo_lab") or f.get("id") or ""
        cal = calibrar(edad, sigma, a.curva, nombre=nombre)
        salida.append(cal.resumen(a.era))
        if not a.salida:
            _imprimir(cal, a.era)
    if a.salida and salida:
        with open(a.salida, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(salida[0]))
            w.writeheader()
            w.writerows(salida)
        print(f"{len(salida)} fechados calibrados -> {a.salida}")


def cmd_simular(a) -> None:
    r = recuperar(a.anio, a.sigma, a.curva, n=a.n)
    print(f"Año verdadero {formato_anio(a.anio)} · ±{a.sigma:g} · {r.curva} · {r.n} simulaciones")
    print(f"  el rango 95.4 % contiene el año verdadero en el {r.cobertura_95 * 100:.1f} % de los casos")
    print(f"  ancho mediano del rango 95.4 %: {r.ancho_95_mediana:.0f} años "
          f"en {r.n_intervalos_mediana:.0f} tramo(s)")
    print(f"  error mediano de la mediana calibrada: {r.error_mediana:.0f} años")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="wata", description="Calibración de fechados radiocarbónicos")
    p.add_argument("--version", action="version", version=f"wata {__version__}")
    p.add_argument("--curva", default="shcal20", help="shcal20 | intcal20 | mixta:P (P = fracción SHCal20)")
    p.add_argument("--era", default="d. C.", help="sufijo de era: «d. C.» (RAE) o «d.C.»")
    sub = p.add_subparsers(dest="orden", required=True)

    c = sub.add_parser("calibrar", help="calibra una edad")
    c.add_argument("edad", type=float)
    c.add_argument("sigma", type=float)
    c.add_argument("--nombre", default="")
    c.add_argument("--figura", help="ruta PNG de la figura")
    c.set_defaults(func=cmd_calibrar)

    l_ = sub.add_parser("lote", help="calibra un CSV (edad_ap, sigma)")
    l_.add_argument("csv")
    l_.add_argument("--salida", help="CSV de resultados")
    l_.add_argument("--curva", dest="curva_lote")
    l_.set_defaults(func=cmd_lote)

    s = sub.add_parser("simular", help="¿cuánto recupera la calibración un año conocido?")
    s.add_argument("anio", type=int, help="año d. C. (negativo para a. C., astronómico)")
    s.add_argument("--sigma", type=float, default=25)
    s.add_argument("-n", type=int, default=500)
    s.set_defaults(func=cmd_simular)

    d = sub.add_parser("curvas", help="descarga las curvas de intcal.org si faltan")
    d.set_defaults(func=lambda a: descargar())

    a = p.parse_args(argv)
    if getattr(a, "curva_lote", None):
        a.curva = a.curva_lote
    a.func(a)


if __name__ == "__main__":
    sys.exit(main())
