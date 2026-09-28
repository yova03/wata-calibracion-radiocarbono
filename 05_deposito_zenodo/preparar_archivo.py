"""Prepara un ZIP reproducible del depósito completo en Zenodo.

Uso: python 05_deposito_zenodo/preparar_archivo.py
No publica el depósito ni reserva un DOI.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = Path(__file__).resolve().parent / "borrador"
ARCHIVO = SALIDA / "investigacion_cusco_wata_v0.1.0_DEPOSITO.zip"
INCLUIR_RAIZ = ("00_LEEME.md", "README.md", "requirements.txt",
                "LICENSE_CODE.txt", "LICENSE_CONTENT.md", "CITATION.cff",
                "ENTORNO_EJECUCION.md", "REVISION_ZENODO_2026-09-28.md")
INCLUIR_CARPETAS = ("01_codigo", "02_datos", "04_resultados", "pruebas")
EXCLUIR_DIR = {".git", "__pycache__", ".pytest_cache", "_RETIRADOS"}
EXCLUIR_EXT = {".pyc", ".14c"}
CSV_BRUTO = "02_datos/fechados/fechados_biblioteca.csv"
ENLACES_FUENTE = {
    "burger-mcewan_2006": "https://bibliovault.org/BV.book.epl?ISBN=9780816529360",
    "TESIS_2018_analisis-bioarqueologico-bandojan-yuthu": "https://hdl.handle.net/20.500.12918/3566",
    "TESIS_UNSAAC_2026_13210": "https://hdl.handle.net/20.500.12918/13210",
    "TESIS_2019_arqueologia-pachatusan-qosqo-ayllu": "https://hdl.handle.net/20.500.12918/4163",
    "TESIS_2019_evidencias-artefactuales-calle-mantas": "https://hdl.handle.net/20.500.12918/3838",
    "TESIS_2023_arquitectura-laura-pampakuchu-paruro": "https://hdl.handle.net/20.500.12918/7976",
    "TESIS_2023_estratigrafico-arquitectura-pukara-pantillijlla": "https://hdl.handle.net/20.500.12918/7753",
    "TESIS_2023_planeamiento-arquitectura-illarakay": "https://hdl.handle.net/20.500.12918/7819",
    "TESIS_2024_arquitectura-pukara-sicuani": "https://hdl.handle.net/20.500.12918/8404",
    "TESIS_UNSAAC_2019_5248": "https://hdl.handle.net/20.500.12918/5248",
    "TESIS_UNSAAC_2025_10880": "https://hdl.handle.net/20.500.12918/10880",
    "TESIS_UNSAAC_2025_10945": "https://hdl.handle.net/20.500.12918/10945",
    "TESIS_UNSAAC_2025_11507": "https://hdl.handle.net/20.500.12918/11507",
    "delgado2024machuqolqa": "https://doi.org/10.18800/boletindearqueologiapucp.202401.003",
    "earle2025tombs": "https://doi.org/10.1017/laq.2024.28",
    "shadik2024acopia": "https://doi.org/10.3390/plants13071019",
    "ravines-ceramica_documento": "https://boletindelima.com/163-166/5.pdf",
}


def fuente_url(fuente_archivo: str) -> str:
    enlaces = [url for clave, url in ENLACES_FUENTE.items() if clave in fuente_archivo]
    if len(enlaces) > 1:
        raise ValueError(f"Fuente con más de un enlace: {fuente_archivo}")
    return enlaces[0] if enlaces else ""


def catalogar_fuentes() -> None:
    origen = RAIZ / CSV_BRUTO
    fuentes: dict[str, dict[str, str | int]] = {}
    with origen.open(encoding="utf-8-sig", newline="") as fh:
        for fila in csv.DictReader(fh):
            archivo = fila["fuente_archivo"]
            if archivo not in fuentes:
                fuentes[archivo] = {"fuente_archivo": archivo, "filas": 0,
                                    "fuente_primaria_indicada": fila["fuente_primaria"],
                                    "url_publica": fuente_url(archivo)}
            fuentes[archivo]["filas"] = int(fuentes[archivo]["filas"]) + 1
    destino = RAIZ / "02_datos" / "fechados" / "fuentes_publicas.csv"
    with destino.open("w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=["fuente_archivo", "filas",
                                                  "fuente_primaria_indicada", "url_publica"])
        escritor.writeheader()
        escritor.writerows(fuentes.values())


def archivos() -> list[Path]:
    rutas = [RAIZ / nombre for nombre in INCLUIR_RAIZ]
    for carpeta in INCLUIR_CARPETAS:
        rutas.extend(r for r in (RAIZ / carpeta).rglob("*") if r.is_file())
    return sorted(
        r for r in rutas
        if not (set(r.relative_to(RAIZ).parts) & EXCLUIR_DIR)
        and r.suffix.lower() not in EXCLUIR_EXT
    )


def contenido(ruta: Path) -> bytes:
    if ruta.relative_to(RAIZ).as_posix() != CSV_BRUTO:
        return ruta.read_bytes()
    with ruta.open(encoding="utf-8-sig", newline="") as origen:
        lector = csv.DictReader(origen)
        columnas = [c for c in lector.fieldnames or [] if c != "cita_textual"] + ["fuente_url"]
        salida = io.StringIO(newline="")
        escritor = csv.DictWriter(salida, fieldnames=columnas, lineterminator="\n")
        escritor.writeheader()
        for fila in lector:
            limpia = {c: fila[c] for c in columnas if c != "fuente_url"}
            limpia["fuente_url"] = fuente_url(fila["fuente_archivo"])
            escritor.writerow(limpia)
        return salida.getvalue().encode("utf-8")


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    catalogar_fuentes()
    manifiesto = []
    with ZipFile(ARCHIVO, "w", compression=ZIP_DEFLATED, compresslevel=9) as zipf:
        for ruta in archivos():
            nombre = ruta.relative_to(RAIZ).as_posix()
            datos = contenido(ruta)
            ficha = ZipInfo(nombre, date_time=(2026, 9, 28, 0, 0, 0))
            ficha.compress_type = ZIP_DEFLATED
            zipf.writestr(ficha, datos, compress_type=ZIP_DEFLATED, compresslevel=9)
            manifiesto.append({"ruta": nombre, "bytes": len(datos),
                               "sha256": hashlib.sha256(datos).hexdigest()})
        datos = json.dumps({"estado": "PREPARADO_PARA_DEPOSITO", "archivos": manifiesto},
                           ensure_ascii=False, indent=2).encode("utf-8")
        ficha = ZipInfo("MANIFIESTO.json", date_time=(2026, 9, 28, 0, 0, 0))
        ficha.compress_type = ZIP_DEFLATED
        zipf.writestr(ficha, datos, compress_type=ZIP_DEFLATED, compresslevel=9)
    print(f"ZIP de deposito: {ARCHIVO} ({len(manifiesto)} archivos)")


if __name__ == "__main__":
    main()
