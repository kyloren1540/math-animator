"""Logarithmic function f(x) = log(x) natural log."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class LogarithmicFunction(MathFunction):
    TYPE_ID = "logarithmic"
    DISPLAY_NAME = "Logarítmica"
    PARAM_SPECS: list[tuple[str, str, float]] = []

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        y = np.zeros_like(x, dtype=float)
        mask = x > 0
        y[~mask] = np.nan
        y[mask] = np.log(x[mask])
        return y

    def formula_text(self) -> str:
        return "f(x) = ln(x)"

    def formula_latex(self) -> str:
        return r"f(x) = \ln(x)"

    def domain_description(self) -> str:
        return "(0, +∞)"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        return "ℝ"
