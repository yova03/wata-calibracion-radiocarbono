# -*- coding: utf-8 -*-
"""Genera el video vertical (TikTok) de la investigación 06: wata.

Salida: video/wata_tiktok_v1.mp4 (1080x1920, 30 fps, sin audio).
Todas las cifras de pantalla provienen del README y de los informes 03 y 04.
Regenerar con:  python generar_video.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
AQUI = Path(__file__).resolve().parent
FIGURAS = RAIZ / "04_resultados"

ANCHO, ALTO, FPS = 1080, 1920, 30

FONDO = (10, 13, 19)
BLANCO = (244, 246, 250)
GRIS = (170, 180, 196)
AMARILLO = (255, 209, 102)
TERMINAL_FONDO = (24, 26, 32)
TERMINAL_BORDE = (64, 70, 84)

FUENTES = {
    "negro": r"C:\Windows\Fonts\ariblk.ttf",
    "negrita": r"C:\Windows\Fonts\segoeuib.ttf",
    "normal": r"C:\Windows\Fonts\segoeui.ttf",
    "mono": r"C:\Windows\Fonts\consolab.ttf",
}

_cache_fuentes: dict = {}


def fnt(nombre: str, tam: int) -> ImageFont.FreeTypeFont:
    clave = (nombre, tam)
    if clave not in _cache_fuentes:
        _cache_fuentes[clave] = ImageFont.truetype(FUENTES[nombre], tam)
    return _cache_fuentes[clave]


# --------------------------------------------------------------------------
# utilidades de dibujo
# --------------------------------------------------------------------------

def suave(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def entre(t: float, inicio: float, fin: float) -> float:
    return suave((t - inicio) / max(fin - inicio, 1e-6))


def capa() -> Image.Image:
    return Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))


def con_alfa(img: Image.Image, a: float) -> Image.Image:
    if a >= 0.999:
        return img
    r, g, b, al = img.split()
    al = al.point(lambda v: int(v * a))
    return Image.merge("RGBA", (r, g, b, al))


def lineas(dib: ImageDraw.ImageDraw, cy: float, textos, fuente, color, esp: int = 14) -> None:
    alturas = [dib.textbbox((0, 0), tx, font=fuente)[3] for tx in textos]
    total = sum(alturas) + esp * (len(textos) - 1)
    y = cy - total / 2
    for tx, h in zip(textos, alturas):
        w = dib.textlength(tx, font=fuente)
        dib.text(((ANCHO - w) / 2, y), tx, font=fuente, fill=color)
        y += h + esp


def texto_img(texto: str, fuente, color) -> Image.Image:
    medidor = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    b = medidor.textbbox((0, 0), texto, font=fuente)
    img = Image.new("RGBA", (b[2] + 8, b[3] + 8), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4 - b[0], 4 - b[1]), texto, font=fuente, fill=color)
    return img


def pegar_centrado(base: Image.Image, img: Image.Image, cy: float, escala: float = 1.0, dy: float = 0.0) -> None:
    if escala != 1.0:
        img = img.resize((max(1, int(img.width * escala)), max(1, int(img.height * escala))), Image.Resampling.LANCZOS)
    base.alpha_composite(img, (int((ANCHO - img.width) / 2), int(cy - img.height / 2 + dy)))


def bloque_texto(cy, textos, fuente, color, dy=0.0) -> Image.Image:
    su = capa()
    lineas(ImageDraw.Draw(su), cy - dy, textos, fuente, color)
    return su, dy


def cuadrado_fondo() -> Image.Image:
    ys = np.linspace(0, 1, ALTO)[:, None]
    arriba = np.array([17, 21, 31], dtype=float)
    abajo = np.array([7, 9, 13], dtype=float)
    color = arriba[None, :] * (1 - ys) + abajo[None, :] * ys
    rejilla = np.repeat(color[:, None, :], ANCHO, axis=1).astype(np.uint8)
    return Image.fromarray(rejilla, "RGB").convert("RGBA")


def recorte_zoom(imagen: Image.Image, z: float) -> Image.Image:
    w = int(ANCHO / z)
    h = int(ALTO / z)
    x = (imagen.width - w) // 2
    y = (imagen.height - h) // 2
    return imagen.crop((x, y, x + w, y + h)).resize((ANCHO, ALTO), Image.Resampling.LANCZOS)


def tarjeta_figura(figura: Image.Image, z: float, cy: float, ancho_caja: int = 940) -> None:
    proporcion = figura.height / figura.width
    caja_w = ancho_caja
    caja_h = int(ancho_caja * proporcion)
    w = int(caja_w * z)
    h = int(caja_h * z)
    grande = figura.resize((w, h), Image.Resampling.LANCZOS)
    x = (w - caja_w) // 2
    y = (h - caja_h) // 2
    recorte = grande.crop((x, y, x + caja_w, y + caja_h))
    mascara = Image.new("L", (caja_w, caja_h), 0)
    ImageDraw.Draw(mascara).rounded_rectangle((0, 0, caja_w - 1, caja_h - 1), 26, fill=255)
    recorte.putalpha(mascara)
    return recorte, caja_w, caja_h


def pegar_tarjeta(base: Image.Image, figura: Image.Image, z: float, cy: float) -> None:
    recorte, w, h = tarjeta_figura(figura, z, cy)
    x = (ANCHO - w) // 2
    y = int(cy - h / 2)
    sombra = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((30, 40, w + 30, h + 52), 26, fill=(0, 0, 0, 120))
    base.alpha_composite(sombra, (x - 30, y - 30))
    base.alpha_composite(recorte, (x, y))
    ImageDraw.Draw(base).rounded_rectangle((x, y, x + w - 1, y + h - 1), 26, outline=(96, 104, 122, 255), width=2)


# --------------------------------------------------------------------------
# piezas cargadas una vez
# --------------------------------------------------------------------------

FONDO_BASE = None
F_CALIB = F_SIGLOS = F_1438 = F_ANCHO = F_CURVA = None
F_CALIB_GRANDE = None


def preparar() -> None:
    global FONDO_BASE, F_CALIB, F_SIGLOS, F_1438, F_ANCHO, F_CURVA, F_CALIB_GRANDE
    FONDO_BASE = cuadrado_fondo()
    F_CALIB = Image.open(FIGURAS / "vista_previa/calibracion_450_25.png").convert("RGBA")
    F_SIGLOS = Image.open(FIGURAS / "fechados_cusco/fig_fechados_siglos_XI_XVI.png").convert("RGBA")
    F_1438 = Image.open(FIGURAS / "simulacion/fig_antes_1438.png").convert("RGBA")
    F_ANCHO = Image.open(FIGURAS / "simulacion/fig_ancho_rango.png").convert("RGBA")
    F_CURVA = Image.open(FIGURAS / "simulacion/fig_efecto_curva.png").convert("RGBA")
    escala = (ALTO * 1.20) / F_CALIB.height
    F_CALIB_GRANDE = F_CALIB.resize(
        (int(F_CALIB.width * escala), int(F_CALIB.height * escala)), Image.Resampling.LANCZOS
    )


# --------------------------------------------------------------------------
# escenas
# --------------------------------------------------------------------------

def escena_1(t: float) -> Image.Image:
    cuadro = recorte_zoom(F_CALIB_GRANDE, 1.04 + 0.10 * suave(t / 4.0))
    cuadro = Image.alpha_composite(cuadro, Image.new("RGBA", (ANCHO, ALTO), (5, 7, 11, 168)))
    for ap, cy, textos, fuente, color, dy in (
        (entre(t, 0.15, 0.85), 560, ["El Cusco inka"], fnt("negro", 104), BLANCO, 46),
        (entre(t, 1.05, 1.75), 800, ["se fecha con carbono 14"], fnt("negrita", 74), BLANCO, 46),
        (entre(t, 2.10, 2.80), 1030, ["¿y con qué curva?"], fnt("negro", 88), AMARILLO, 46),
    ):
        if ap > 0:
            su, _ = bloque_texto(cy, textos, fuente, color)
            cuadro.alpha_composite(con_alfa(su, ap), (0, int((1 - ap) * dy)))
    return cuadro


def escena_2(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    ap = entre(t, 0.10, 0.70)
    img = texto_img("wata", fnt("negro", 250), BLANCO)
    pegar_centrado(cuadro, con_alfa(img, ap), 700, escala=0.92 + 0.08 * entre(t, 0.10, 1.00))
    largo = int(430 * entre(t, 0.60, 1.30))
    if largo > 0:
        ImageDraw.Draw(cuadro).rounded_rectangle(
            ((ANCHO - largo) // 2, 862, (ANCHO + largo) // 2, 876), 7, fill=AMARILLO + (255,)
        )
    su, _ = bloque_texto(1010, ["calibración radiocarbónica en español"], fnt("negrita", 58), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.90, 1.60)))
    su, _ = bloque_texto(1130, ["Python · sin conexión · SHCal20 / IntCal20"], fnt("normal", 42), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.35, 2.05)))
    return cuadro


SALIDA_TERMINAL = [
    "450±25: 450 ± 25 AP · curva shcal20",
    "  68.3 %: 1448–1485 d. C. (65.2 %)",
    "  95.4 %: 1442–1503 d. C. (82.6 %)",
    "  mediana: 1473 d. C.",
]
COMANDO = "$ python -m wata calibrar 450 25"


def escena_3(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    su, _ = bloque_texto(470, ["Así se calibra"], fnt("negrita", 66), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.10, 0.70)))

    x0, y0, w, h = 70, 600, 940, 660
    d = ImageDraw.Draw(cuadro)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 24, fill=TERMINAL_FONDO + (255,), outline=TERMINAL_BORDE + (255,), width=2)
    for i, color in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((x0 + 34 + i * 46, y0 + 30, x0 + 62 + i * 46, y0 + 58), fill=color + (255,))
    mono = fnt("mono", 36)
    visible = int(len(COMANDO) * entre(t, 0.50, 2.00))
    d.text((x0 + 44, y0 + 110), COMANDO[:visible], font=mono, fill=(240, 240, 240, 255))
    if t > 2.00 and int(t * 2) % 2 == 0:
        cursor_x = x0 + 44 + d.textlength(COMANDO, font=mono) + 4
        d.rectangle((cursor_x, y0 + 110, cursor_x + 20, y0 + 150), fill=(240, 240, 240, 255))
    y = y0 + 190
    for i, linea in enumerate(SALIDA_TERMINAL):
        aparece = entre(t, 2.30 + i * 0.55, 2.75 + i * 0.55)
        if aparece > 0:
            color = (222, 226, 236, 255) if i == 0 else (250, 214, 120, 255)
            d.text((x0 + 44, y + i * 62), linea, font=mono, fill=tuple(int(c * aparece) for c in color[:3]) + (255,))
    su, _ = bloque_texto(1420, ["salida real de wata 0.1.0 · tramos principales"], fnt("normal", 38), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 3.20, 3.80)))
    return cuadro


def escena_4(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    su, _ = bloque_texto(620, ["Contrastado con OxCal"], fnt("negrita", 72), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.10, 0.70)))
    img = texto_img("20/21", fnt("negro", 300), AMARILLO)
    pegar_centrado(cuadro, con_alfa(img, entre(t, 0.70, 1.30)), 950, escala=0.82 + 0.22 * entre(t, 0.70, 1.50))
    su, _ = bloque_texto(1210, ["rangos idénticos"], fnt("negrita", 70), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.20, 1.80)))
    su, _ = bloque_texto(1400, ["11 fechados de Machu Picchu · OxCal 4.3.2"], fnt("normal", 44), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.55, 2.15)))
    su, _ = bloque_texto(1475, ["616 rangos cotejados con IOSACal"], fnt("normal", 44), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.80, 2.40)))
    return cuadro


def escena_5(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    su, _ = bloque_texto(400, ["Y se aplicó al Cusco"], fnt("negro", 84), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.10, 0.70)))
    pegar_tarjeta(cuadro, F_SIGLOS, 1.0 + 0.06 * suave(t / 4.6), 1080)
    su, _ = bloque_texto(1580, ["50 calibraciones de 94 registros revisados"], fnt("normal", 46), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.90, 1.60)))
    return cuadro


def escena_6(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    img = texto_img("1438", fnt("negro", 220), AMARILLO)
    pegar_centrado(cuadro, con_alfa(img, entre(t, 0.10, 0.70)), 430, escala=0.9 + 0.1 * entre(t, 0.10, 0.90))
    su, _ = bloque_texto(600, ["el ascenso de Pachacuti"], fnt("negrita", 58), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.50, 1.10)))
    pegar_tarjeta(cuadro, F_1438, 1.0 + 0.06 * suave(t / 4.8), 1180)
    su, _ = bloque_texto(1700, ["un fechado aislado no decide antes/después"], fnt("normal", 46), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.00, 1.70)))
    return cuadro


def escena_7(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    su, _ = bloque_texto(400, ["¿Cuánto abarca un fechado?"], fnt("negrita", 70), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.10, 0.70)))
    pegar_tarjeta(cuadro, F_ANCHO, 1.0 + 0.06 * suave(t / 4.8), 1035)
    su, _ = bloque_texto(1520, ["±25 AP: ~45 años entre 1400 y 1450", "130–150 años desde 1450"], fnt("normal", 46), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.90, 1.60)))
    return cuadro


def escena_8(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    su, _ = bloque_texto(400, ["La curva no es un detalle"], fnt("negrita", 70), BLANCO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.10, 0.70)))
    pegar_tarjeta(cuadro, F_CURVA, 1.0 + 0.06 * suave(t / 4.8), 1035)
    su, _ = bloque_texto(
        1520,
        ["IntCal20 ≈ 30 años más antigua que SHCal20", "en las fechas de época inka"],
        fnt("normal", 46),
        GRIS,
        0.0,
    )
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.90, 1.60)))
    return cuadro


def escena_9(t: float) -> Image.Image:
    cuadro = FONDO_BASE.copy()
    img = texto_img("wata 0.1.0", fnt("negro", 165), BLANCO)
    pegar_centrado(cuadro, con_alfa(img, entre(t, 0.10, 0.70)), 620)
    su, _ = bloque_texto(780, ["código, datos y figuras abiertos"], fnt("negrita", 54), AMARILLO, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 0.50, 1.10)))
    ap = entre(t, 0.90, 1.60)
    if ap > 0:
        caja = Image.new("RGBA", (900, 250), (0, 0, 0, 0))
        dc = ImageDraw.Draw(caja)
        dc.rounded_rectangle((0, 0, 899, 249), 24, fill=(22, 26, 36, 235), outline=AMARILLO + (220,), width=3)
        mono = fnt("mono", 46)
        for i, linea in enumerate(("github.com/yova03/", "wata-calibracion-radiocarbono")):
            w = dc.textlength(linea, font=mono)
            dc.text(((900 - w) / 2, 58 + i * 72), linea, font=mono, fill=(238, 240, 246, 255))
        cuadro.alpha_composite(con_alfa(caja, ap), ((ANCHO - 900) // 2, 930))
    su, _ = bloque_texto(1420, ["Python · MIT + CC BY 4.0"], fnt("normal", 42), GRIS, 0.0)
    cuadro.alpha_composite(con_alfa(su, entre(t, 1.40, 2.10)))
    return cuadro


ESCENAS = [
    ("01_hook", 4.0, escena_1),
    ("02_wata", 4.2, escena_2),
    ("03_terminal", 5.2, escena_3),
    ("04_validacion", 4.6, escena_4),
    ("05_cusco", 4.6, escena_5),
    ("06_1438", 4.8, escena_6),
    ("07_precision", 4.8, escena_7),
    ("08_curva", 4.8, escena_8),
    ("09_cta", 5.0, escena_9),
]


def main() -> None:
    import imageio.v2 as imageio

    preparar()
    total = sum(d for _, d, _ in ESCENAS)
    carpeta_video = AQUI / "video"
    carpeta_control = AQUI / "frames_control"
    carpeta_video.mkdir(exist_ok=True)
    carpeta_control.mkdir(exist_ok=True)
    ruta = carpeta_video / "wata_tiktok_v1.mp4"
    print("duración total: %.1f s · %d fotogramas" % (total, int(total * FPS)))

    editor = imageio.get_writer(
        str(ruta),
        fps=FPS,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p",
        macro_block_size=None,
        ffmpeg_log_level="error",
    )
    contador = 0
    for nombre, duracion, render in ESCENAS:
        fotogramas = int(round(duracion * FPS))
        cuadro_control = None
        for i in range(fotogramas):
            t = i / FPS
            cuadro = render(t)
            a = min(1.0, t / 0.30, max(0.001, (duracion - t) / 0.30))
            if a < 1.0:
                cuadro = Image.alpha_composite(cuadro, Image.new("RGBA", (ANCHO, ALTO), FONDO + (int(255 * (1 - a)),)))
            if i == int(fotogramas * 0.70):
                cuadro_control = cuadro
            editor.append_data(np.asarray(cuadro.convert("RGB")))
            contador += 1
        if cuadro_control is not None:
            cuadro_control.convert("RGB").save(carpeta_control / ("control_%s.png" % nombre), "PNG")
        print("escena %s lista" % nombre)
    editor.close()
    print("video: %s (%d fotogramas)" % (ruta, contador))


if __name__ == "__main__":
    main()
