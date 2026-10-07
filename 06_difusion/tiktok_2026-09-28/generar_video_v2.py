# -*- coding: utf-8 -*-
"""Genera la versión 2 del video vertical (TikTok) de la investigación 06: wata.

Salida: video/wata_tiktok_v2.mp4 (1080x1920, 30 fps, sin audio) y portada_v2.png.
Todas las cifras de pantalla salen de wata o de los CSV de 04_resultados y se
verifican con «assert» al preparar los datos; nada se escribe a mano salvo los
rótulos.  Regenerar con:  python generar_video_v2.py
Comprobación visual:      python generar_video_v2.py --prueba [--mascara]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
RESULTADOS = RAIZ / "04_resultados"
sys.path.insert(0, str(RAIZ / "01_codigo"))
from wata import calibrar  # noqa: E402

ANCHO, ALTO, FPS = 1080, 1920, 30
SS = 2  # sobremuestreo de los gráficos (antialiasing)

# zona segura de TikTok: arriba la barra de pestañas, abajo la descripción,
# a la derecha la columna de iconos
X0, X1 = 70, 930
Y0, Y1 = 170, 1500
CX = (X0 + X1) // 2

FONDO = (10, 13, 19)
BLANCO = (244, 246, 250)
GRIS = (170, 180, 196)
GRIS_OSC = (44, 52, 68)
AMARILLO = (255, 209, 102)
C_SH = (92, 170, 255)   # SHCal20
C_MIX = (255, 145, 84)  # mixta 50:50
C_INT = (64, 216, 160)  # IntCal20
CURVAS = (("shcal20", "SHCal20", C_SH), ("mixta:0.5:0.1", "Mixta 50:50", C_MIX), ("intcal20", "IntCal20", C_INT))

FUENTES = {
    "negro": r"C:\Windows\Fonts\ariblk.ttf",
    "negrita": r"C:\Windows\Fonts\segoeuib.ttf",
    "normal": r"C:\Windows\Fonts\segoeui.ttf",
    "mono": r"C:\Windows\Fonts\consolab.ttf",
}
_fuentes: dict = {}


def fnt(nombre: str, tam: int) -> ImageFont.FreeTypeFont:
    clave = (nombre, tam)
    if clave not in _fuentes:
        _fuentes[clave] = ImageFont.truetype(FUENTES[nombre], tam)
    return _fuentes[clave]


def ajustar(txt: str, nombre: str, tam: int, ancho_max: int = X1 - X0) -> ImageFont.FreeTypeFont:
    """Mayor tamaño (≤ tam) con que el texto cabe en el ancho seguro."""
    while tam > 24 and fnt(nombre, tam).getlength(txt) > ancho_max:
        tam -= 2
    return fnt(nombre, tam)


# --------------------------------------------------------------------------
# animación y texto
# --------------------------------------------------------------------------

def suave(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def entre(t: float, a: float, b: float) -> float:
    return suave((t - a) / max(b - a, 1e-6))


def salida(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


_txt: dict = {}


def _img_texto(txt: str, fuente, color):
    clave = (txt, id(fuente), color)
    if clave not in _txt:
        b = fuente.getbbox(txt, anchor="ls")
        im = Image.new("RGBA", (b[2] - b[0] + 8, b[3] - b[1] + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - b[0], 4 - b[1]), txt, font=fuente, fill=color + (255,), anchor="ls")
        _txt[clave] = im
    return _txt[clave]


def _alfa(im: Image.Image, a: float) -> Image.Image:
    if a >= 0.999:
        return im
    r, g, b, al = im.split()
    return Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))


def poner(cuadro, txt, cx, cy, fuente, color, a=1.0, dy=0.0, alin="c") -> None:
    """Texto con su caja de tinta centrada en cy; alin: c (cx centro), l (cx borde izq.), r (cx borde der.)."""
    if a <= 0.004:
        return
    im = _alfa(_img_texto(txt, fuente, color), a)
    x = {"c": cx - im.width / 2, "l": cx - 4, "r": cx - im.width + 4}[alin]
    cuadro.alpha_composite(im, (int(x), int(cy - im.height / 2 + dy)))


def ent(t: float, t0: float, dur: float = 0.40, desp: float = 30.0):
    """(alfa, desplazamiento vertical) de una entrada que sube y aparece."""
    p = salida((t - t0) / dur)
    return p, (1 - p) * desp


def texto(cuadro, txt, cx, cy, fuente, color, t, t0, dur=0.40, desp=30.0, alin="c") -> None:
    a, dy = ent(t, t0, dur, desp)
    poner(cuadro, txt, cx, cy, fuente, color, a, dy, alin)


def texto_mixto(cuadro, trozos, cx, cy, fuente, a=1.0, dy=0.0) -> None:
    """Una línea centrada con trozos de distinto color y una misma línea base."""
    if a <= 0.004:
        return
    ancho = sum(fuente.getlength(s) for s, _ in trozos)
    b = fuente.getbbox("Hg", anchor="ls")
    capa = Image.new("RGBA", (int(ancho) + 16, b[3] - b[1] + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x = 8
    for s, color in trozos:
        d.text((x, 8 - b[1]), s, font=fuente, fill=color + (255,), anchor="ls")
        x += fuente.getlength(s)
    cuadro.alpha_composite(_alfa(capa, a), (int(cx - capa.width / 2), int(cy - capa.height / 2 + dy)))


# --------------------------------------------------------------------------
# lienzo con antialiasing para los gráficos
# --------------------------------------------------------------------------

class Lienzo:
    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def _p(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def linea(self, pts, color, ancho) -> None:
        if len(pts) >= 2:
            self.d.line(self._p(pts), fill=color, width=int(ancho * SS), joint="curve")
            r = ancho * SS / 2  # extremos redondeados
            for x, y in (pts[0], pts[-1]):
                self.d.ellipse((x * SS - r, y * SS - r, x * SS + r, y * SS + r), fill=color)

    def discontinua(self, x0, y0, x1, y1, color, ancho, trazo=14, hueco=10) -> None:
        largo = float(np.hypot(x1 - x0, y1 - y0))
        n = max(1, int(largo // (trazo + hueco)))
        for i in range(n + 1):
            a = i * (trazo + hueco) / largo
            b = min(1.0, (i * (trazo + hueco) + trazo) / largo)
            if a < 1.0:
                self.d.line(self._p([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)]),
                            fill=color, width=int(ancho * SS))

    def poligono(self, pts, relleno) -> None:
        p = self._p(pts)
        xs, ys = [q[0] for q in p], [q[1] for q in p]
        bx0, by0 = int(max(0, min(xs) - 2)), int(max(0, min(ys) - 2))
        bx1, by1 = int(min(self.w * SS, max(xs) + 3)), int(min(self.h * SS, max(ys) + 3))
        if bx1 <= bx0 or by1 <= by0:
            return
        capa = Image.new("RGBA", (bx1 - bx0, by1 - by0), (0, 0, 0, 0))
        ImageDraw.Draw(capa).polygon([(x - bx0, y - by0) for x, y in p], fill=relleno)
        self.img.alpha_composite(capa, (bx0, by0))

    def texto(self, x, y, txt, nombre, tam, color, anclaje="ms") -> None:
        self.d.text((x * SS, y * SS), txt, font=fnt(nombre, tam * SS), fill=color, anchor=anclaje)

    def triangulo(self, cx, y_punta, ancho, alto, color) -> None:
        self.d.polygon(self._p([(cx, y_punta), (cx - ancho / 2, y_punta + alto), (cx + ancho / 2, y_punta + alto)]), fill=color)

    def punto(self, x, y, r, color) -> None:
        self.d.ellipse(((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS), fill=color)

    def anillo(self, x, y, r, color, ancho) -> None:
        self.d.ellipse(((x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS), outline=color, width=int(ancho * SS))

    def listo(self) -> Image.Image:
        return self.img.resize((self.w, self.h), Image.Resampling.LANCZOS)


class Ejes:
    def __init__(self, x0, y0, x1, y1, xmin, xmax, ymin, ymax):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def px(self, x):
        return self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * (self.x1 - self.x0)

    def py(self, y):
        return self.y1 - (y - self.ymin) / (self.ymax - self.ymin) * (self.y1 - self.y0)


def marco(L: Lienzo, ej: Ejes, xticks, yticks=(), yfmt=str, tam=32) -> None:
    """Cuadrícula horizontal tenue, eje inferior y marcas con números grandes."""
    for v in yticks:
        y = ej.py(v)
        L.linea([(ej.x0, y), (ej.x1, y)], GRIS_OSC + (255,), 2)
        L.texto(ej.x0 - 14, y + tam * 0.35, yfmt(v), "normal", tam, GRIS + (255,), "rs")
    L.linea([(ej.x0, ej.y1), (ej.x1, ej.y1)], (120, 130, 148, 255), 3)
    for v in xticks:
        x = ej.px(v)
        L.linea([(x, ej.y1), (x, ej.y1 + 10)], (120, 130, 148, 255), 3)
        L.texto(x, ej.y1 + 12 + tam, str(v), "normal", tam, GRIS + (255,), "ms")


def recorte_x(xs, ys, x_max):
    """Puntos con x ≤ x_max, con el último interpolado (dibujo progresivo)."""
    px, py = [], []
    for i, (x, y) in enumerate(zip(xs, ys)):
        if x <= x_max:
            px.append(x)
            py.append(y)
        else:
            if i > 0 and xs[i - 1] < x_max:
                f = (x_max - xs[i - 1]) / (x - xs[i - 1])
                px.append(x_max)
                py.append(ys[i - 1] + f * (y - ys[i - 1]))
            break
    return px, py


# --------------------------------------------------------------------------
# datos (todo verificado contra las fuentes)
# --------------------------------------------------------------------------

D: dict = {}


def leer(ruta: Path) -> list[dict]:
    with open(ruta, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def preparar() -> None:
    ys = np.linspace(0, 1, ALTO)[:, None]
    color = np.array([17, 21, 31], float)[None, :] * (1 - ys) + np.array([7, 9, 13], float)[None, :] * ys
    D["fondo"] = Image.fromarray(np.repeat(color[:, None, :], ANCHO, axis=1).astype(np.uint8), "RGB").convert("RGBA")

    # gancho: la misma muestra de ejemplo (450 ± 25 AP) con las tres curvas
    D["gancho"] = {}
    for clave, _, _ in CURVAS:
        cal = calibrar(450, 25, clave)
        orden = np.argsort(cal.anios)
        D["gancho"][clave] = (cal.anios[orden].astype(float), cal.densidad[orden], cal.mediana(), cal)
    assert D["gancho"]["shcal20"][2] == 1473 and D["gancho"]["intcal20"][2] == 1444 and D["gancho"]["mixta:0.5:0.1"][2] == 1453
    D["p_antes"] = {c: D["gancho"][c][3].prob_entre(-100000, 1437) for c in D["gancho"]}
    assert D["p_antes"]["shcal20"] < 0.01 and 0.04 < D["p_antes"]["mixta:0.5:0.1"] < 0.07 and 0.24 < D["p_antes"]["intcal20"] < 0.27
    D["dif_gancho"] = D["gancho"]["shcal20"][2] - D["gancho"]["intcal20"][2]
    assert D["dif_gancho"] == 29
    rango = {c: [i.texto() for i in D["gancho"][c][3].hpd(0.954)] for c in ("shcal20", "intcal20")}
    assert rango["shcal20"][0].startswith("1442–1503 d. C. (82.6") and rango["intcal20"][0].startswith("1423–1461 d. C. (91.7")

    # fechados del Cusco: los 16 con mediana SHCal20 ≥ 1000 (mismo criterio que la figura del informe)
    filas = leer(RESULTADOS / "fechados_cusco" / "calibrados.csv")
    assert len(filas) == 50
    cals = []
    for f in filas:
        cal = calibrar(float(f["edad_ap"]), float(f["sigma"]), "shcal20")
        if cal.mediana() >= 1000:
            cals.append(cal)
    assert len(cals) == 16
    cals.sort(key=lambda c: -c.mediana())
    D["ridges"] = []
    for cal in cals:
        orden = np.argsort(cal.anios)
        D["ridges"].append((cal.anios[orden].astype(float), cal.densidad[orden]))

    # ¿antes o después de 1438? (fechado único ± 20 AP)
    D["antes"] = {}
    for f in leer(RESULTADOS / "simulacion" / "antes_1438.csv"):
        if float(f["sigma"]) == 20:
            D["antes"].setdefault(f["curva"], []).append((float(f["anio"]), float(f["prob_antes_1438"])))
    p1430 = dict(D["antes"]["shcal20"])[1430.0]
    assert abs(p1430 - 0.74) < 0.005
    D["p1430"] = p1430

    # ancho del rango 95.4 % (fechado único ± 25 AP)
    D["ancho"] = {}
    for f in leer(RESULTADOS / "simulacion" / "recuperacion.csv"):
        if float(f["sigma"]) == 25:
            D["ancho"].setdefault(f["curva"], []).append((float(f["anio"]), float(f["ancho_95_mediana"])))
    med = {}
    for clave, _, _ in CURVAS:
        pares = D["ancho"][clave]
        for nombre, a, b in (("1400", 1400, 1449), ("1450", 1450, 1539), ("1540", 1540, 1599)):
            med[(clave, nombre)] = float(np.median([w for y, w in pares if a <= y <= b]))
    D["ancho_1400"] = (min(round(med[(c, "1400")]) for c, _, _ in CURVAS), max(round(med[(c, "1400")]) for c, _, _ in CURVAS))
    D["ancho_1450"] = (min(round(med[(c, n)]) for c, _, _ in CURVAS for n in ("1450", "1540")),
                       max(round(med[(c, n)]) for c, _, _ in CURVAS for n in ("1450", "1540")))
    assert D["ancho_1400"] == (43, 53) and D["ancho_1450"] == (134, 149), (D["ancho_1400"], D["ancho_1450"])


# --------------------------------------------------------------------------
# elementos comunes
# --------------------------------------------------------------------------

def nuevo() -> Image.Image:
    return D["fondo"].copy()


def fila_curva(cuadro, cy, color, etiqueta, valor, a, dy=0.0, extra=None) -> None:
    if a <= 0.004:
        return
    capa = Image.new("RGBA", (ANCHO, 120), (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle((X0 + 60, 60 - 12, X0 + 60 + 24, 60 + 12), 6, fill=color + (255,))
    cuadro.alpha_composite(_alfa(capa, a), (0, int(cy - 60 + dy)))
    poner(cuadro, etiqueta, X0 + 110, cy, fnt("negrita", 46), BLANCO, a, dy, "l")
    if extra is None:
        poner(cuadro, valor, X1 - 60, cy, fnt("negro", 54), color, a, dy, "r")
    else:
        poner(cuadro, valor, X1 - 300, cy, fnt("negro", 54), color, a, dy, "r")
        poner(cuadro, extra, X1 - 60, cy, fnt("negro", 54), AMARILLO, a, dy, "r")


# --------------------------------------------------------------------------
# escenas (t = segundos desde el inicio de cada escena)
# --------------------------------------------------------------------------

def esc_gancho(t: float) -> Image.Image:
    """El gancho está completo desde el primer fotograma: pregunta, eje y línea de 1438."""
    c = nuevo()
    poner(c, "¿Antes o después", CX, 262, ajustar("¿Antes o después", "negro", 96), BLANCO)
    poner(c, "de 1438?", CX, 386, fnt("negro", 156), AMARILLO)
    texto(c, "fecha documental del ascenso de Pachacuti", CX, 492, fnt("normal", 40), GRIS, t, 0.05, 0.35, 12)
    texto(c, "Muestra de ejemplo: 450 ± 25 AP", CX, 566, fnt("negrita", 42), BLANCO, t, 0.10, 0.35, 12)

    W, H = X1 - X0, 470
    L = Lienzo(W, H)
    ej = Ejes(44, 56, W - 44, H - 66, 1400, 1620, 0, 1)
    ymax = max(d[1].max() for d in D["gancho"].values())
    ej.ymax = ymax * 1.04
    marco(L, ej, (1400, 1500, 1600))
    x38 = ej.px(1438)
    L.discontinua(x38, 44, x38, ej.y1, AMARILLO + (255,), 4)
    L.texto(x38, 34, "1438", "negrita", 36, AMARILLO + (255,), "ms")
    for k, (clave, _, color) in enumerate(CURVAS):
        anios, dens, med, _ = D["gancho"][clave]
        g = entre(t, 0.15 + 0.22 * k, 1.25 + 0.22 * k)
        m = (anios >= 1400) & (anios <= 1620)
        pts = [(ej.px(a), ej.py(v * g)) for a, v in zip(anios[m], dens[m])]
        L.poligono([(pts[0][0], ej.py(0))] + pts + [(pts[-1][0], ej.py(0))], color + (70,))
        if g > 0.02:
            L.linea(pts, color + (255,), 6)
        if t > 1.5 + 0.35 * k:
            a_med = entre(t, 1.5 + 0.35 * k, 1.8 + 0.35 * k)
            L.triangulo(ej.px(med), ej.y1 - 26, 30, 24, color + (int(255 * a_med),))
    c.alpha_composite(L.listo(), (X0, 600))

    a, dy = ent(t, 1.45, 0.35, 14)
    poner(c, "mediana", X1 - 300, 1112, fnt("normal", 32), GRIS, a, dy, "r")
    poner(c, "antes de 1438", X1 - 60, 1112, fnt("normal", 32), AMARILLO, a, dy, "r")
    for k, (clave, nombre, color) in enumerate(CURVAS):
        a, dy = ent(t, 1.55 + 0.35 * k, 0.35, 20)
        p = D["p_antes"][clave]
        fila_curva(c, 1172 + 66 * k, color, nombre, str(D["gancho"][clave][2]), a, dy,
                   extra="<1 %" if p < 0.01 else f"{round(100 * p)} %")
    a, dy = ent(t, 3.15, 0.45, 26)
    poner(c, "29 años entre las medianas", CX, 1404, ajustar("29 años entre las medianas", "negro", 58), AMARILLO, a, dy)
    return c


def esc_wata(t: float) -> Image.Image:
    c = nuevo()
    a = entre(t, 0.05, 0.50)
    esc = 0.90 + 0.10 * entre(t, 0.05, 0.70)
    im = _alfa(_img_texto("wata", fnt("negro", 260), BLANCO), a)
    im = im.resize((int(im.width * esc), int(im.height * esc)), Image.Resampling.LANCZOS)
    c.alpha_composite(im, (int(CX - im.width / 2), int(600 - im.height / 2)))
    largo = int(430 * entre(t, 0.40, 0.90))
    if largo > 0:
        ImageDraw.Draw(c).rounded_rectangle((CX - largo // 2, 760, CX + largo // 2, 774), 7, fill=AMARILLO + (255,))
    texto(c, "«año» en quechua", CX, 850, fnt("normal", 46), GRIS, t, 0.55, 0.35, 14)
    texto(c, "calibración radiocarbónica", CX, 990, fnt("negrita", 62), BLANCO, t, 0.75, 0.35, 18)
    texto(c, "en español", CX, 1066, fnt("negrita", 62), BLANCO, t, 0.85, 0.35, 18)
    texto(c, "SHCal20 · IntCal20 · curva mixta", CX, 1200, fnt("normal", 44), GRIS, t, 1.10, 0.35, 14)
    texto(c, "Python · código abierto", CX, 1270, fnt("normal", 44), GRIS, t, 1.25, 0.35, 14)
    return c


def esc_terminal(t: float) -> Image.Image:
    c = nuevo()
    texto(c, "Un comando por curva", CX, 400, fnt("negrita", 68), BLANCO, t, 0.02, 0.30, 14)
    bx0, by0, bw, bh = X0, 470, X1 - X0, 720
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), 24, fill=(24, 26, 32, 255), outline=(64, 70, 84, 255), width=2)
    for i, col in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((bx0 + 34 + i * 46, by0 + 30, bx0 + 62 + i * 46, by0 + 58), fill=col + (255,))
    mono = fnt("mono", 40)
    paso = mono.getlength("0")
    xt = bx0 + 40
    y = by0 + 120
    blanco, ama = (240, 240, 240, 255), (250, 214, 120, 255)

    def escribir(lineas, y_ini, t_ini, t_fin):
        """Tecleo por caracteres a lo largo de varias líneas; devuelve (y, x) del cursor."""
        total = sum(len(s) for s in lineas)
        n = int(total * entre(t, t_ini, t_fin))
        cur = (y_ini, xt)
        for i, s in enumerate(lineas):
            k = max(0, min(len(s), n))
            n -= len(s)
            yy = y_ini + i * 62
            d.text((xt, yy), s[:k], font=mono, fill=blanco)
            if k > 0 or i == 0:
                cur = (yy, xt + paso * k)
            if k < len(s):
                break
        return cur

    cmd1 = ["$ python -m wata calibrar 450 25"]
    cmd2 = ["$ python -m wata --curva intcal20 \\", "      calibrar 450 25"]
    escribir(cmd1, y, 0.15, 0.85)
    salidas = [
        (y + 72, "  95.4 %: 1442–1503 d. C. (82.6 %)", blanco, 1.00),
        (y + 136, "  mediana: 1473 d. C.", ama, 1.25),
        (y + 262, None, None, None),
        (y + 394, "  95.4 %: 1423–1461 d. C. (91.7 %)", blanco, 2.70),
        (y + 458, "  mediana: 1444 d. C.", ama, 2.95),
    ]
    cur = None
    if t < 1.5:
        cur = (y, xt + paso * int(len(cmd1[0]) * entre(t, 0.15, 0.85)))
    elif t >= 1.5:
        cur = escribir(cmd2, y + 262, 1.55, 2.45)
    for yy, s, col, t0 in salidas:
        if s is None:
            continue
        a = entre(t, t0, t0 + 0.30)
        if a > 0:
            d.text((xt, yy), s, font=mono, fill=tuple(int(v * a + 24 * (1 - a)) for v in col[:3]) + (255,))
    if cur is not None and t < 3.2 and int(t * 3) % 2 == 0:
        d.rectangle((cur[1] + 3, cur[0] + 2, cur[1] + 23, cur[0] + 48), fill=blanco)
    texto(c, "misma muestra, dos curvas", CX, 1290, fnt("negrita", 46), BLANCO, t, 3.25, 0.35, 14)
    texto(c, "salida real de wata 0.1.0 · se muestra el tramo principal", CX, 1355, ajustar("salida real de wata 0.1.0 · se muestra el tramo principal", "normal", 36), GRIS, t, 3.40, 0.35, 14)
    return c


def esc_validacion(t: float) -> Image.Image:
    c = nuevo()
    texto(c, "Contrastado con OxCal", CX, 330, fnt("negrita", 68), BLANCO, t, 0.02, 0.30, 14)
    n = int(round(20 * entre(t, 0.10, 0.95)))
    g = fnt("negro", 290)
    ancho = g.getlength("20/21")
    xi = CX - ancho / 2
    a, dy = ent(t, 0.05, 0.30, 16)
    poner(c, "/21", xi + g.getlength("20"), 610, g, AMARILLO, a, dy, "l")
    poner(c, str(n), xi + g.getlength("20"), 610, g, AMARILLO, a, dy, "r")
    texto(c, "rangos con los mismos tramos", CX, 830, ajustar("rangos con los mismos tramos", "negrita", 58), BLANCO, t, 0.95, 0.35, 16)
    texto(c, "diferencia máxima entre extremos: 2 años", CX, 912, ajustar("diferencia máxima entre extremos: 2 años", "normal", 44), GRIS, t, 1.15, 0.35, 14)
    a = entre(t, 1.45, 1.75)
    if a > 0:
        ImageDraw.Draw(c).line((CX - 220, 1000, CX + 220, 1000), fill=(64, 72, 90, int(255 * a)), width=3)
    texto(c, "IOSACal: 616 rangos cotejados", CX, 1078, ajustar("IOSACal: 616 rangos cotejados", "negrita", 50), BLANCO, t, 1.55, 0.35, 14)
    texto(c, "508 con los mismos tramos", CX, 1148, fnt("normal", 42), GRIS, t, 1.75, 0.35, 12)
    texto(c, "máximo 11 años, por decisiones de IOSACal", CX, 1204, ajustar("máximo 11 años, por decisiones de IOSACal", "normal", 42), GRIS, t, 1.85, 0.35, 12)
    texto(c, "OxCal: 11 fechados de Machu Picchu, Chachabamba", CX, 1338, ajustar("OxCal: 11 fechados de Machu Picchu, Chachabamba", "normal", 36), GRIS, t, 2.15, 0.35, 10)
    texto(c, "y Choqesuysuy (Ziółkowski et al., 2021)", CX, 1388, fnt("normal", 36), GRIS, t, 2.25, 0.35, 10)
    return c


def esc_cusco(t: float) -> Image.Image:
    c = nuevo()
    poner(c, "50 fechados del Cusco", CX, 290, ajustar("50 fechados del Cusco", "negro", 78), BLANCO)
    texto(c, "calibrados con wata", CX, 384, fnt("negrita", 46), AMARILLO, t, 0.05, 0.35, 14)
    W, H = X1 - X0, 800
    L = Lienzo(W, H)
    ej = Ejes(44, 100, W - 44, H - 70, 900, 1750, 0, 1)
    marco(L, ej, (1000, 1250, 1500, 1750))
    n = len(D["ridges"])
    paso = (ej.y1 - ej.y0 - 20) / n
    alto = paso * 2.6
    for i, (anios, dens) in enumerate(D["ridges"]):
        base = ej.y0 + 20 + paso * (i + 1)
        g = entre(t, 0.30 + 0.05 * i, 0.85 + 0.05 * i)
        m = (anios >= 900) & (anios <= 1750)
        xs, ys = anios[m], dens[m] / dens[m].max()
        pts = [(ej.px(a), base - alto * v * g) for a, v in zip(xs, ys)]
        L.poligono([(pts[0][0], base)] + pts + [(pts[-1][0], base)], C_SH + (170,))
        if g > 0.02:
            L.linea(pts, (168, 214, 255, 255), 3)
    x38 = ej.px(1438)
    L.discontinua(x38, 46, x38, ej.y1, AMARILLO + (255,), 4)
    L.texto(x38, 36, "1438", "negrita", 34, AMARILLO + (255,), "ms")
    c.alpha_composite(L.listo(), (X0, 450))
    texto(c, "los 16 de los siglos XI–XVI · distribución calibrada con SHCal20", CX, 1330, ajustar("los 16 de los siglos XI–XVI · distribución calibrada con SHCal20", "normal", 40), GRIS, t, 1.20, 0.35, 12)
    return c


def esc_1438(t: float) -> Image.Image:
    c = nuevo()
    poner(c, "1438", CX, 320, fnt("negro", 220), AMARILLO)
    texto(c, "fecha documental del ascenso de Pachacuti", CX, 462, ajustar("fecha documental del ascenso de Pachacuti", "normal", 38), GRIS, t, 0.05, 0.35, 12)
    texto(c, "Probabilidad de «antes de 1438» tras calibrar", CX, 545, ajustar("Probabilidad de «antes de 1438» tras calibrar", "negrita", 40), BLANCO, t, 0.15, 0.35, 12)
    W, H = X1 - X0, 560
    L = Lienzo(W, H)
    ej = Ejes(112, 24, W - 44, H - 66, 1400, 1480, 0, 1)
    marco(L, ej, (1400, 1420, 1440, 1460, 1480), (0, 0.5, 1.0), lambda v: f"{int(v * 100)} %")
    x38 = ej.px(1438)
    L.discontinua(x38, ej.y0, x38, ej.y1, AMARILLO + (255,), 4)
    p = entre(t, 0.35, 2.10)
    for clave, _, color in CURVAS:
        xs = [ej.px(a) for a, _ in D["antes"][clave]]
        ys = [ej.py(v) for _, v in D["antes"][clave]]
        px, py = recorte_x(xs, ys, ej.x0 + p * (ej.x1 - ej.x0))
        L.linea(list(zip(px, py)), color + (255,), 7)
    for k, (clave, nombre, color) in enumerate(CURVAS):
        yy = ej.y0 + 30 + 42 * k
        L.d.rounded_rectangle(((ej.x1 - 250) * SS, (yy - 10) * SS, (ej.x1 - 226) * SS, (yy + 10) * SS), 5 * SS, fill=color + (255,))
        L.texto(ej.x1 - 210, yy + 11, nombre, "normal", 32, BLANCO + (255,), "ls")
    a = entre(t, 2.25, 2.60)
    if a > 0:
        xd, yd = ej.px(1430), ej.py(D["p1430"])
        pulso = 0.5 + 0.5 * np.sin(max(0.0, t - 2.25) * 5.0)
        L.anillo(xd, yd, 16 + 6 * pulso, AMARILLO + (int(255 * a),), 4)
        L.punto(xd, yd, 9, AMARILLO + (int(255 * a),))
    c.alpha_composite(L.listo(), (X0, 610))
    a, dy = ent(t, 2.45, 0.40, 22)
    texto_mixto(c, [("Una muestra de 1430 aún deja", BLANCO)], CX, 1236, fnt("negrita", 48), a, dy)
    texto_mixto(c, [("un cuarto", AMARILLO), (" de probabilidad", BLANCO)], CX, 1300, fnt("negrita", 54), a, dy)
    texto_mixto(c, [("de salir después de 1438", BLANCO)], CX, 1364, fnt("negrita", 48), a, dy)
    texto(c, "simulación · fechado único ± 20 AP", CX, 1440, fnt("normal", 36), GRIS, t, 2.80, 0.35, 10)
    return c


def esc_precision(t: float) -> Image.Image:
    c = nuevo()
    poner(c, "¿Cuánto abarca un fechado?", CX, 290, ajustar("¿Cuánto abarca un fechado?", "negro", 60), BLANCO)
    texto(c, "rango de 95.4 % · fechado único ± 25 AP", CX, 370, ajustar("rango de 95.4 % · fechado único ± 25 AP", "normal", 38), GRIS, t, 0.05, 0.35, 12)
    W, H = X1 - X0, 660
    L = Lienzo(W, H)
    ej = Ejes(84, 46, W - 44, H - 70, 1000, 1600, 30, 160)
    marco(L, ej, (1000, 1200, 1400, 1600), (50, 100, 150))
    L.texto(ej.x0 + 4, 26, "años que abarca el rango", "normal", 32, GRIS + (255,), "ls")
    ba = entre(t, 1.80, 2.30)
    if ba > 0:
        L.poligono([(ej.px(1400), ej.y0), (ej.px(1450), ej.y0), (ej.px(1450), ej.y1), (ej.px(1400), ej.y1)], AMARILLO + (int(70 * ba),))
    p = entre(t, 0.30, 1.90)
    for clave, _, color in CURVAS:
        xs = [ej.px(a) for a, _ in D["ancho"][clave]]
        ys = [ej.py(v) for _, v in D["ancho"][clave]]
        px, py = recorte_x(xs, ys, ej.x0 + p * (ej.x1 - ej.x0))
        L.linea(list(zip(px, py)), color + (255,), 6)
    c.alpha_composite(L.listo(), (X0, 440))
    a1, a2 = D["ancho_1400"], D["ancho_1450"]
    a, dy = ent(t, 1.95, 0.40, 20)
    texto_mixto(c, [("1400–1449: ", AMARILLO), (f"de {a1[0]} a {a1[1]} años", AMARILLO)], CX, 1190, fnt("negro", 50), a, dy)
    a, dy = ent(t, 2.20, 0.40, 20)
    texto_mixto(c, [(f"desde 1450: de {a2[0]} a {a2[1]} años", BLANCO)], CX, 1262, fnt("negro", 50), a, dy)
    texto(c, "separar lo inka tardío de lo colonial temprano", CX, 1360, ajustar("separar lo inka tardío de lo colonial temprano", "normal", 40), GRIS, t, 2.55, 0.35, 10)
    texto(c, "exige secuencias y modelos bayesianos", CX, 1410, fnt("normal", 40), GRIS, t, 2.65, 0.35, 10)
    return c


def esc_cierre(t: float) -> Image.Image:
    c = nuevo()
    poner(c, "Declara la curva", CX, 300, ajustar("Declara la curva", "negro", 84), BLANCO)
    poner(c, "con cada fecha", CX, 400, ajustar("con cada fecha", "negro", 84), AMARILLO)
    texto(c, "wata 0.1.0", CX, 640, fnt("negro", 150), BLANCO, t, 0.15, 0.40, 20)
    texto(c, "código, datos y figuras abiertos", CX, 780, ajustar("código, datos y figuras abiertos", "negrita", 52), AMARILLO, t, 0.45, 0.35, 14)
    a, dy = ent(t, 0.75, 0.40, 22)
    if a > 0:
        caja = Image.new("RGBA", (X1 - X0, 240), (0, 0, 0, 0))
        dc = ImageDraw.Draw(caja)
        dc.rounded_rectangle((0, 0, caja.width - 1, 239), 24, fill=(22, 26, 36, 235), outline=AMARILLO + (220,), width=3)
        mono = fnt("mono", 44)
        for i, linea in enumerate(("github.com/yova03/", "wata-calibracion-radiocarbono")):
            dc.text((caja.width / 2, 78 + i * 72), linea, font=mono, fill=(238, 240, 246, 255), anchor="mm")
        c.alpha_composite(_alfa(caja, a), (X0, int(880 + dy)))
    texto(c, "Python · MIT (código) + CC BY 4.0 (contenido)", CX, 1190, ajustar("Python · MIT (código) + CC BY 4.0 (contenido)", "normal", 40), GRIS, t, 1.15, 0.35, 10)
    return c


# (nombre, duración, función); cada escena se prolonga TR s bajo la siguiente (fundido corto)
ESCENAS = [
    ("01_gancho", 4.8, esc_gancho),
    ("02_wata", 3.0, esc_wata),
    ("03_terminal", 4.8, esc_terminal),
    ("04_validacion", 4.2, esc_validacion),
    ("05_cusco", 4.0, esc_cusco),
    ("06_1438", 4.4, esc_1438),
    ("07_precision", 4.0, esc_precision),
    ("08_cierre", 4.2, esc_cierre),
]
TR = 0.15
INICIOS = np.cumsum([0.0] + [d for _, d, _ in ESCENAS])
TOTAL = float(INICIOS[-1])


def cuadro_global(T: float) -> Image.Image:
    k = max(0, min(len(ESCENAS) - 1, int(np.searchsorted(INICIOS, T, side="right")) - 1))
    c = ESCENAS[k][2](T - INICIOS[k])
    if k > 0 and T - INICIOS[k] < TR:  # fundido corto desde la escena anterior
        previa = ESCENAS[k - 1][2](T - INICIOS[k - 1])
        c = Image.blend(previa, c, (T - INICIOS[k]) / TR)
    return c


def barra_progreso(c: Image.Image, T: float) -> None:
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((X0, 152, X1, 158), 3, fill=(36, 42, 56, 255))
    largo = int((X1 - X0) * min(1.0, T / TOTAL))
    if largo > 6:
        d.rounded_rectangle((X0, 152, X0 + largo, 158), 3, fill=AMARILLO + (255,))


def mascara_segura(c: Image.Image) -> Image.Image:
    capa = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    rojo = (255, 40, 40, 90)
    d.rectangle((0, 0, ANCHO, 150), fill=rojo)
    d.rectangle((0, 1500, ANCHO, ALTO), fill=rojo)
    d.rectangle((940, 900, ANCHO, 1650), fill=rojo)
    d.rectangle((0, 0, 60, ALTO), fill=rojo)
    return Image.alpha_composite(c, capa)


def fotograma(T: float) -> Image.Image:
    c = cuadro_global(T)
    barra_progreso(c, T)
    return c


def controles(con_mascara: bool) -> None:
    carpeta = AQUI / "frames_control_v2"
    carpeta.mkdir(exist_ok=True)
    hojas = {"inicio": [], "final": []}
    for k, (nombre, dur, _) in enumerate(ESCENAS):
        for etiqueta, T in (("inicio", INICIOS[k] + 0.02), ("final", INICIOS[k] + dur - 0.05)):
            c = fotograma(float(T))
            c.convert("RGB").save(carpeta / f"control_{nombre}_{etiqueta}.png", "PNG")
            v = mascara_segura(c) if con_mascara else c
            hojas[etiqueta].append(v.convert("RGB").resize((360, 640), Image.Resampling.LANCZOS))
    for etiqueta, ims in hojas.items():
        hoja = Image.new("RGB", (360 * 4 + 30, 640 * 2 + 10), (60, 60, 60))
        for i, im in enumerate(ims):
            hoja.paste(im, ((i % 4) * 370, (i // 4) * 650))
        hoja.save(carpeta / f"hoja_{etiqueta}{'_mascara' if con_mascara else ''}.png", "PNG")
    fotograma(float(INICIOS[0] + 3.9)).convert("RGB").save(AQUI / "portada_v2.png", "PNG")
    print("controles y portada guardados")


def main() -> None:
    preparar()
    print("duración total: %.1f s · %d fotogramas" % (TOTAL, int(round(TOTAL * FPS))))
    if "--prueba" in sys.argv:
        controles("--mascara" in sys.argv)
        return
    import imageio.v2 as imageio

    carpeta = AQUI / "video"
    carpeta.mkdir(exist_ok=True)
    ruta = carpeta / "wata_tiktok_v2.mp4"
    editor = imageio.get_writer(
        str(ruta), fps=FPS, codec="libx264", quality=None, pixelformat="yuv420p", macro_block_size=None,
        ffmpeg_log_level="error",
        output_params=["-crf", "17", "-preset", "slow", "-profile:v", "high", "-movflags", "+faststart"],
    )
    n = int(round(TOTAL * FPS))
    for i in range(n):
        editor.append_data(np.asarray(fotograma(i / FPS).convert("RGB")))
        if i % 150 == 0:
            print("fotograma %d/%d" % (i, n), flush=True)
    editor.close()
    controles(False)
    print("video:", ruta)


if __name__ == "__main__":
    main()
