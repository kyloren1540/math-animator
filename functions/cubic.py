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
        v = self.v
        return f"f({v}) = {a:g}{v}³ + {b:g}{v}² + {c:g}{v} + {d:g}"

    def formula_latex(self) -> str:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        v = self.v_latex
        return rf"f({v}) = {a:g}{v}^3 + {b:g}{v}^2 + {c:g}{v} + {d:g}"

    def roots(self) -> list[float]:
        a, b, c, d = (
            self._params["a"],
            self._params["b"],
            self._params["c"],
            self._params["d"],
        )
        sym = sp.Symbol(self.v)
        sols = sp.solve(a * sym**3 + b * sym**2 + c * sym + d, sym)
        return [float(sp.re(s)) for s in sols if s.is_real]
