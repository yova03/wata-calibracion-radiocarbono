"""Pruebas automáticas: python -m pytest pruebas"""

import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "01_codigo"))
sys.path.insert(0, str(RAIZ / "pruebas"))

from casos_oxcal import CASOS  # noqa: E402
from validar_oxcal import validar  # noqa: E402

from wata import calibrar, cargar, formato_anio, mezclar, sumar  # noqa: E402
from wata.simular import recuperar  # noqa: E402


def test_formato_de_anios_sin_anio_cero():
    assert formato_anio(1438) == "1438 d. C."
    assert formato_anio(1) == "1 d. C."
    assert formato_anio(0) == "1 a. C."
    assert formato_anio(-499) == "500 a. C."


def test_densidad_normalizada_y_hpd_contiene_el_nivel():
    cal = calibrar(450, 25, "shcal20")
    assert cal.densidad.sum() == pytest.approx(1.0)
    for nivel in (0.683, 0.954):
        assert sum(r.prob for r in cal.hpd(nivel)) >= nivel - 1e-9


def test_mezcla_en_los_extremos_reproduce_cada_curva():
    sur, norte = cargar("shcal20"), cargar("intcal20")
    m1, m0 = mezclar(sur, norte, 1.0), mezclar(sur, norte, 0.0)
    anios = np.arange(0, 5000)
    assert np.allclose(m1.en(anios)[0], sur.en(anios)[0], atol=1e-6)
    assert np.allclose(m0.en(anios)[1], norte.en(anios)[1], atol=1e-6)


def test_shcal20_da_fechas_mas_recientes_que_intcal20():
    # el desfase interhemisférico hace más «joven» la calibración austral
    assert calibrar(450, 25, "shcal20").media() > calibrar(450, 25, "intcal20").media()


def test_reproduce_oxcal_en_machu_picchu():
    filas = validar()
    comparables = [f for f in filas if f["dif_max_anios"] is not None]
    assert len(comparables) >= 20
    assert max(f["dif_max_anios"] for f in comparables) <= 3
    assert len(CASOS) == 11


def test_suma_de_probabilidades():
    s = sumar([calibrar(450, 25), calibrar(520, 30)])
    assert s.densidad.sum() == pytest.approx(1.0)


def test_simulacion_cobertura_razonable():
    r = recuperar(1450, 25, "shcal20", n=200)
    assert 0.9 <= r.cobertura_95 <= 1.0
