"""Herramienta determinista: simulador de cuota con el método francés (cuota fija).

Los cálculos financieros NUNCA se delegan al LLM: el modelo solo extrae los parámetros y el
cálculo se hace en Python, que es exacto y auditable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class LoanSimulation:
    monto: float
    tea: float
    plazo_meses: int
    tem: float
    cuota: float
    total_pagado: float
    total_intereses: float


def simulate_loan(monto: float, tea: float, plazo_meses: int) -> LoanSimulation:
    """tea en porcentaje (30 = 30%). Convierte TEA a TEM: (1 + TEA)^(1/12) - 1."""
    if monto <= 0 or plazo_meses <= 0 or tea < 0:
        raise ValueError("monto y plazo deben ser positivos y la TEA no negativa")
    tem = (1 + tea / 100) ** (1 / 12) - 1
    cuota = monto / plazo_meses if tem == 0 else monto * tem / (1 - (1 + tem) ** -plazo_meses)
    total = cuota * plazo_meses
    return LoanSimulation(
        monto=monto, tea=tea, plazo_meses=plazo_meses, tem=tem,
        cuota=round(cuota, 2), total_pagado=round(total, 2), total_intereses=round(total - monto, 2),
    )


def format_simulation(sim: LoanSimulation) -> str:
    return (
        f"Para un préstamo de S/ {sim.monto:,.2f} a {sim.plazo_meses} meses con una TEA de {sim.tea:g}% "
        f"(TEM {sim.tem * 100:.2f}%), tu cuota mensual aproximada sería S/ {sim.cuota:,.2f}. "
        f"Pagarías en total S/ {sim.total_pagado:,.2f}, de los cuales S/ {sim.total_intereses:,.2f} son intereses. "
        "Es una simulación referencial: no incluye seguros ni comisiones, y la tasa final depende de tu evaluación."
    )


# Límites de negocio del simulador (referenciales para el banco demo).
LIMITS = {
    "monto": (100.0, 1_000_000.0),
    "tea": (0.01, 200.0),
    "plazo_meses": (1, 360),
}
LABELS = {"monto": "el monto en soles", "tea": "la TEA (%)", "plazo_meses": "el plazo en meses"}


def _to_number(value) -> float | None:
    """Convierte 10000, "10,000", "S/ 10 000", "30%" a float. None si no es interpretable."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = re.sub(r"[^\d.,-]", "", str(value)).replace(",", "")
    try:
        return float(text) if text not in {"", "-", "."} else None
    except ValueError:
        return None


def validate_loan_params(params: dict) -> tuple[dict | None, list[str]]:
    """Devuelve (parámetros limpios, []) o (None, mensajes de error claros para el cliente)."""
    values, missing, errors = {}, [], []
    for key, (low, high) in LIMITS.items():
        number = _to_number(params.get(key))
        if number is None:
            missing.append(LABELS[key])
            continue
        if key == "plazo_meses":
            if number != int(number):
                errors.append("el plazo debe ser un número entero de meses")
                continue
            number = int(number)
        if not low <= number <= high:
            errors.append(f"{LABELS[key]} debe estar entre {low:g} y {high:,g}")
            continue
        values[key] = number
    messages = []
    if missing:
        messages.append("Para simular tu cuota necesito " + ", ".join(missing) + ".")
    if errors:
        messages.append("Revisa estos datos: " + "; ".join(errors) + ".")
    return (values, []) if not messages else (None, messages)
