"""Figuras de calibración listas para una tesis (PNG a 300 ppp)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np

from .calibrar import Calibracion, formato_anio
from .curvas import cargar

TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
REJILLA = "#e4e3df"
SERIE = ["#2a78d6", "#eb6834", "#1baf7a"]  # paleta categórica validada, en orden

_INSTALADAS = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
_FUENTE = next((f for f in ("Arial Narrow", "Arial", "Liberation Sans") if f in _INSTALADAS), "DejaVu Sans")

plt.rcParams.update(
    {
        "font.family": _FUENTE,
        "font.size": 9,
        "axes.edgecolor": TINTA_2,
        "axes.labelcolor": TINTA,
        "xtick.color": TINTA_2,
        "ytick.color": TINTA_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def _eje_anios(ax, era: str, nbins: int = 8) -> None:
    """Marcas en años históricos redondos (900 a. C., no 901 a. C.).

    Se llama después de fijar los límites. La escala interna es astronómica
    (1 a. C. = 0), así que un año histórico redondo t ≤ 0 va en t + 1.
    """
    x0, x1 = ax.get_xlim()
    redondos = matplotlib.ticker.MaxNLocator(nbins=nbins, steps=[1, 2, 2.5, 5, 10]).tick_values(x0, x1)
    marcas = [t if t > 0 else t + 1 for t in redondos]
    marcas = [m for m in marcas if x0 <= m <= x1]
    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(marcas))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: str(int(round(v))) if v >= 1 else formato_anio(int(round(v)), era)))
    ax.set_xlabel(f"Años calendario calibrados ({era}, salvo indicación)")


def figura_calibracion(cal: Calibracion, salida: Path, era: str = "d. C.") -> Path:
    """Curva, edad del laboratorio y distribución calibrada con rangos HPD."""
    curva = cargar(cal.curva)
    anios = cal.anios
    visible = anios[cal.densidad > 1e-3 * cal.densidad.max()]
    margen = max(60, int(0.35 * (visible.max() - visible.min())))
    x0, x1 = visible.min() - margen, visible.max() + margen
    sel = (1950 - curva.cal_bp >= x0) & (1950 - curva.cal_bp <= x1)
    xa = 1950 - curva.cal_bp[sel]

    fig, ax = plt.subplots(figsize=(6.3, 4.4), dpi=300)
    ax.grid(color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    # curva de calibración (banda 1σ)
    ax.fill_between(xa, curva.edad[sel] - curva.sigma[sel], curva.edad[sel] + curva.sigma[sel],
                    color=TINTA_2, alpha=0.25, linewidth=0, label=f"Curva {curva.nombre.upper()} (1σ)")
    ax.plot(xa, curva.edad[sel], color=TINTA_2, linewidth=0.8)
    ymin = min(cal.edad - 4 * cal.sigma, (curva.edad[sel] - curva.sigma[sel]).min())
    ymax = max(cal.edad + 4 * cal.sigma, (curva.edad[sel] + curva.sigma[sel]).max())
    span = ymax - ymin
    # franja inferior reservada: rangos HPD y distribución calibrada
    fondo = ymin - 0.55 * span
    ax.set_xlim(x0, x1)
    ax.set_ylim(fondo, ymax + 0.05 * span)
    # edad del laboratorio: normal sobre el eje y
    ys = np.linspace(cal.edad - 4 * cal.sigma, cal.edad + 4 * cal.sigma, 200)
    gy = np.exp(-0.5 * ((ys - cal.edad) / cal.sigma) ** 2)
    ax.fill_betweenx(ys, x0, x0 + gy * 0.15 * (x1 - x0), color=SERIE[1], alpha=0.6, linewidth=0,
                     label=f"Edad medida {cal.edad:g} ± {cal.sigma:g} AP")
    # distribución calibrada sobre el eje x
    base = fondo + 0.14 * span
    d = cal.densidad / cal.densidad.max() * 0.36 * span
    ax.fill_between(anios, base, base + d, color=SERIE[0], alpha=0.8, linewidth=0,
                    label="Distribución calibrada")
    for nivel, alto in ((0.954, 0.04), (0.683, 0.09)):
        yb = fondo + alto * span
        rangos = cal.hpd(nivel)
        for r in rangos:
            ax.plot([r.desde, r.hasta + 1], [yb, yb], color=TINTA, linewidth=2, solid_capstyle="butt")
        ax.text(rangos[0].desde - 0.01 * (x1 - x0), yb, f"{nivel * 100:.1f} %", va="center",
                ha="right", fontsize=6.5, color=TINTA_2)
    ax.set_ylabel("Edad radiocarbónica (años AP)")
    _eje_anios(ax, era)
    rangos = "\n".join(r.texto(era) for r in cal.hpd(0.954))
    ax.text(0.99, 0.98, f"{cal.nombre}\n95.4 %:\n{rangos}", transform=ax.transAxes,
            ha="right", va="top", fontsize=7.5, color=TINTA,
            bbox=dict(facecolor="white", edgecolor=REJILLA, boxstyle="round,pad=0.4"))
    fig.legend(loc="lower center", ncol=3, fontsize=7, frameon=False)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida)
    plt.close(fig)
    return salida


def figura_multiple(cals: list[Calibracion], salida: Path, titulo: str = "",
                    era: str = "d. C.", referencias: dict[str, int] | None = None) -> Path:
    """Una fila por fechado, con sus rangos 95.4 % (al estilo de un multiplot)."""
    n = len(cals)
    fig, ax = plt.subplots(figsize=(6.3, 0.9 + 0.32 * n), dpi=300)
    for i, cal in enumerate(cals):
        y = n - 1 - i
        d = cal.densidad / cal.densidad.max() * 0.8
        ax.fill_between(cal.anios, y, y + d, color=SERIE[0], alpha=0.7, linewidth=0)
        for r in cal.hpd(0.954):
            ax.plot([r.desde, r.hasta], [y - 0.08, y - 0.08], color=TINTA, linewidth=1.5)
    visibles = [c.anios[c.densidad > 1e-3 * c.densidad.max()] for c in cals]
    lo, hi = min(v.min() for v in visibles), max(v.max() for v in visibles)
    margen = max(20, 0.04 * (hi - lo))
    ax.set_xlim(lo - margen, hi + margen)
    ax.set_yticks(range(n))
    ax.set_yticklabels([c.nombre for c in reversed(cals)], fontsize=7)
    ax.grid(axis="x", color=REJILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    for etiqueta, anio in (referencias or {}).items():
        ax.axvline(anio, color=SERIE[1], linewidth=1, linestyle="--")
        ax.text(anio, n - 0.1, f" {etiqueta}", color=TINTA, fontsize=7, va="bottom")
    _eje_anios(ax, era, nbins=5)
    if titulo:
        ax.set_title(titulo, fontsize=9, color=TINTA, loc="left")
    fig.tight_layout()
    salida.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida)
    plt.close(fig)
    return salida
