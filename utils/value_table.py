"""Build numeric value tables for plotted functions."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


def _format_cell(value: float) -> str:
    if not np.isfinite(value):
        return "—"
    return f"{value:.4g}"


def build_value_table(
    functions: list[MathFunction],
    x_min: float = -10.0,
    x_max: float = 10.0,
    steps: int = 11,
) -> tuple[list[str], list[list[str]]]:
    """
    Return (headers, rows) for a value table.

    First column is the independent variable; following columns are f(indep)
    for each function on the same sample points.
    """
    if not functions:
        return [], []

    steps = max(5, min(51, int(steps)))
    xs = np.linspace(x_min, x_max, steps)

    iv = functions[0].independent_var
    headers = [iv]
    for i, fn in enumerate(functions):
        label = fn.formula_text()
        if len(label) > 32:
            label = f"f{i + 1}({fn.independent_var})"
        headers.append(label)

    rows: list[list[str]] = []
    for xi in xs:
        row = [_format_cell(float(xi))]
        for fn in functions:
            y = float(fn.evaluate(np.array([xi]))[0])
            row.append(_format_cell(y))
        rows.append(row)

    return headers, rows


def table_to_csv(headers: list[str], rows: list[list[str]]) -> str:
    """CSV text for export."""
    lines = [",".join(headers)]
    lines.extend(",".join(row) for row in rows)
    return "\n".join(lines)
