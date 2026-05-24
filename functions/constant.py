"""Constant function f(x) = c."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class ConstantFunction(MathFunction):
    TYPE_ID = "constant"
    DISPLAY_NAME = "Constante"
    PARAM_SPECS = [("c", "Valor c", 1.0)]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return np.full_like(x, self._params["c"], dtype=float)

    def formula_text(self) -> str:
        return f"f(x) = {self._params['c']:g}"

    def formula_latex(self) -> str:
        return rf"f(x) = {self._params['c']:g}"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        return f"{{ {self._params['c']:g} }}"

    def roots(self) -> list[float]:
        if abs(self._params["c"]) < 1e-12:
            return [0.0]  # every x is root visually — mark origin
        return []
