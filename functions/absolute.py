"""Absolute value function f(x) = |x|."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class AbsoluteFunction(MathFunction):
    TYPE_ID = "absolute"
    DISPLAY_NAME = "Valor absoluto"
    PARAM_SPECS: list[tuple[str, str, float]] = []

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        return np.abs(x)

    def formula_text(self) -> str:
        return "f(x) = |x|"

    def formula_latex(self) -> str:
        return r"f(x) = |x|"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        return "[0, +∞)"

    def roots(self) -> list[float]:
        return [0.0]
