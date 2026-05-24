"""Cubic function f(x) = ax³ + bx² + cx + d."""

from __future__ import annotations

import numpy as np
import sympy as sp

from functions.base import MathFunction


class CubicFunction(MathFunction):
    TYPE_ID = "cubic"
    DISPLAY_NAME = "Cúbica"
    PARAM_SPECS = [
        ("a", "Coef. a", 1.0),
        ("b", "Coef. b", 0.0),
        ("c", "Coef. c", 0.0),
        ("d", "Coef. d", 0.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        return a * x**3 + b * x**2 + c * x + d

    def formula_text(self) -> str:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        return f"f(x) = {a:g}x³ + {b:g}x² + {c:g}x + {d:g}"

    def formula_latex(self) -> str:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        return rf"f(x) = {a:g}x^3 + {b:g}x^2 + {c:g}x + {d:g}"

    def roots(self) -> list[float]:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        x = sp.Symbol("x")
        sols = sp.solve(a * x**3 + b * x**2 + c * x + d, x)
        return [float(sp.re(s)) for s in sols if s.is_real]
