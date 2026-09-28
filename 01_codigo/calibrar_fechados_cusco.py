"""Calibra los fechados del Cusco extraídos de la biblioteca con las tres curvas.

Lee 02_datos/fechados/fechados_biblioteca.csv (solo filas con edad AP y
sigma) y escribe en 04_resultados/fechados_cusco/:

- calibrados.csv: rangos 95.4 % y medianas con SHCal20, mixta e IntCal20;
- fig_fechados_siglos_XI_XVI.png y fig_fechados_anteriores.png (SHCal20).

    python 01_codigo/calibrar_fechados_cusco.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wata import calibrar  # noqa: E402
from wata.graficos import figura_multiple  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "02_datos" / "fechados" / "fechados_biblioteca.csv"
EXCLUIDOS = RAIZ / "02_datos" / "fechados" / "excluidos.csv"
SALIDA = RAIZ / "04_resultados" / "fechados_cusco"
CURVAS = {"shcal20": "SHCal20", "mixta:0.5:0.1": "mixta", "intcal20": "IntCal20"}


def _numero(texto: str) -> float | None:
    """Primer número del campo («+/-50», «±140» → 50, 140); None si no hay."""
    m = re.search(r"\d+(?:[.,]\d+)?", str(texto or ""))
    return float(m.group(0).replace(",", ".")) if m else None


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = list(csv.DictReader(open(ENTRADA, encoding="utf-8-sig")))
    excluidos = {r["id"] for r in csv.DictReader(open(EXCLUIDOS, encoding="utf-8"))} if EXCLUIDOS.exists() else set()
    utiles, tabla = [], []
    for f in filas:
        if f["id"] in excluidos:
            continue
        edad, sigma = _numero(f.get("edad_ap", "")), _numero(f.get("sigma", ""))
        if not edad or not sigma or f.get("ambito") == "fuera_cusco":
            continue
        rotulo = f.get("codigo_lab") or f["id"]
        rotulo = f"{rotulo} · {f.get('sitio', '').split('(')[0].strip()}"[:48]
        fila = {"id": f["id"], "codigo_lab": f.get("codigo_lab", ""), "sitio": f.get("sitio", ""),
                "ambito": f.get("ambito", ""), "periodo_asignado": f.get("periodo_asignado", ""),
                "edad_ap": edad, "sigma": sigma, "fuente_archivo": f.get("fuente_archivo", "")}
        cals = {}
        for curva, corto in CURVAS.items():
            try:
                cal = calibrar(edad, sigma, curva, nombre=rotulo)
            except ValueError as e:
                fila[f"rango95_{corto}"] = f"error: {e}"
                continue
            cals[curva] = cal
            fila[f"rango95_{corto}"] = "; ".join(r.texto() for r in cal.hpd(0.954))
            fila[f"mediana_{corto}"] = cal.mediana()
        if "shcal20" in cals and "intcal20" in cals:
            fila["intcal_menos_shcal"] = cals["intcal20"].mediana() - cals["shcal20"].mediana()
        tabla.append(fila)
        if "shcal20" in cals:
            utiles.append((f.get("ambito", ""), cals["shcal20"]))

    campos = list(dict.fromkeys(k for fila in tabla for k in fila))
    with open(SALIDA / "calibrados.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(tabla)

    # Dos figuras por bloque cronológico: el marco del estudio (siglos XI–XVI)
    # y lo anterior, fuera de las lagunas (sedimento, sin contexto arqueológico).
    tardios = sorted((c for _, c in utiles if c.mediana() >= 1000), key=lambda c: -c.mediana())
    tempranos = sorted((c for _, c in utiles if 0 <= c.mediana() < 1000 or
                        (c.mediana() < 0 and "Laguna" not in c.nombre)), key=lambda c: -c.mediana())
    if tardios:
        figura_multiple(tardios, SALIDA / "fig_fechados_siglos_XI_XVI.png",
                        titulo="Fechados del Cusco, siglos XI–XVI, calibrados con SHCal20 (95.4 %)",
                        referencias={"1438": 1438})
    if tempranos:
        figura_multiple(tempranos, SALIDA / "fig_fechados_anteriores.png",
                        titulo="Fechados del Cusco anteriores al siglo XI, SHCal20 (95.4 %)")
    print(f"{len(tabla)} fechados calibrados de {len(filas)} filas ({len(excluidos)} excluidas) -> {SALIDA}")


if __name__ == "__main__":
    main()
