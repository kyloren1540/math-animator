"""Linear function f(x) = mx + b."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class LinearFunction(MathFunction):
    TYPE_ID = "linear"
    DISPLAY_NAME = "Lineal"
    PARAM_SPECS = [
        ("m", "Pendiente (m)", 1.0),
        ("b", "Ordenada (b)", 0.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        m, b = self._params["m"], self._params["b"]
        return m * x + b

    def formula_text(self) -> str:
        m, b = self._params["m"], self._params["b"]
        v = self.v
        return f"f({v}) = {m:g}{v} + {b:g}"

    def formula_latex(self) -> str:
        m, b = self._params["m"], self._params["b"]
        v = self.v_latex
        sign = "+" if b >= 0 else ""
        return rf"f({v}) = {m:g}{v} {sign}{b:g}"

    def roots(self) -> list[float]:
        m = self._params["m"]
        if abs(m) < 1e-12:
            return []
        return [float(-self._params["b"] / m)]

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        m = self._params["m"]
        if abs(m) < 1e-12:
            return f"{{ {self._params['b']:g} }}"
        return "ℝ"
