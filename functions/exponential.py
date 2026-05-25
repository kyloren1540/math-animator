"""Exponential function f(x) = a^x."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class ExponentialFunction(MathFunction):
    TYPE_ID = "exponential"
    DISPLAY_NAME = "Exponencial"
    PARAM_SPECS = [("a", "Base (a)", 2.0)]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a = self._params["a"]
        if a <= 0:
            return np.full_like(x, np.nan, dtype=float)
        return np.power(a, x)

    def formula_text(self) -> str:
        v = self.v
        return f"f({v}) = {self._params['a']:g}^{v}"

    def formula_latex(self) -> str:
        v = self.v_latex
        return rf"f({v}) = {self._params['a']:g}^{{{v}}}"

    def domain_description(self) -> str:
        return "ℝ"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        a = self._params["a"]
        if a <= 0:
            return "—"
        if a > 1:
            return "(0, +∞)"
        if abs(a - 1) < 1e-12:
            return "{1}"
        return "(0, +∞)"
