import pytest

from assistant.tools import simulate_loan


def test_cuota_metodo_frances():
    sim = simulate_loan(10_000, 30, 12)
    assert sim.cuota == pytest.approx(957.86, abs=0.01)
    assert sim.total_pagado == pytest.approx(sim.cuota * 12, abs=0.05)


def test_tea_cero_divide_en_partes_iguales():
    assert simulate_loan(1_200, 0, 12).cuota == 100


@pytest.mark.parametrize("monto,tea,plazo", [(0, 30, 12), (1000, -1, 12), (1000, 30, 0)])
def test_parametros_invalidos(monto, tea, plazo):
    with pytest.raises(ValueError):
        simulate_loan(monto, tea, plazo)


from assistant.tools import validate_loan_params  # noqa: E402


@pytest.mark.parametrize("params", [
    {"monto": "S/ 10,000", "tea": "30%", "plazo_meses": "12"},
    {"monto": 10000, "tea": 30.0, "plazo_meses": 12.0},
])
def test_validacion_acepta_formatos_validos(params):
    values, problems = validate_loan_params(params)
    assert problems == [] and values == {"monto": 10000.0, "tea": 30.0, "plazo_meses": 12}


@pytest.mark.parametrize("params,fragment", [
    ({"monto": 10000, "tea": 30, "plazo_meses": 0}, "plazo"),
    ({"monto": 10000, "tea": 30, "plazo_meses": -6}, "plazo"),
    ({"monto": 10000, "tea": 30, "plazo_meses": 12.5}, "entero"),
    ({"monto": -500, "tea": 30, "plazo_meses": 12}, "monto"),
    ({"monto": 10000, "tea": 0, "plazo_meses": 12}, "TEA"),
    ({"monto": 10000, "tea": 999, "plazo_meses": 12}, "TEA"),
    ({"monto": "doce mil", "tea": 30, "plazo_meses": 12}, "monto"),
    ({"monto": None, "tea": None, "plazo_meses": None}, "necesito"),
    ({"monto": True, "tea": 30, "plazo_meses": 12}, "monto"),
])
def test_validacion_rechaza_valores_invalidos(params, fragment):
    values, problems = validate_loan_params(params)
    assert values is None and fragment in " ".join(problems)
