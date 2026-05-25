"""Quadratic function f(x) = ax² + bx + c."""

from __future__ import annotations

import numpy as np
import sympy as sp

from functions.base import MathFunction


class QuadraticFunction(MathFunction):
    TYPE_ID = "quadratic"
    DISPLAY_NAME = "Cuadrática"
    PARAM_SPECS = [
        ("a", "Coef. a", 1.0),
        ("b", "Coef. b", 0.0),
        ("c", "Coef. c", 0.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a, b, c = self._params["a"], self._params["b"], self._params["c"]
        return a * x**2 + b * x + c

    def formula_text(self) -> str:
        a, b, c = self._params["a"], self._params["b"], self._params["c"]
        v = self.v
        return f"f({v}) = {a:g}{v}² + {b:g}{v} + {c:g}"

    def formula_latex(self) -> str:
        a, b, c = self._params["a"], self._params["b"], self._params["c"]
        v = self.v_latex
        return rf"f({v}) = {a:g}{v}^2 + {b:g}{v} + {c:g}"

    def vertex(self) -> tuple[float, float] | None:
        a = self._params["a"]
        if abs(a) < 1e-12:
            return None
        b, c = self._params["b"], self._params["c"]
        xv = -b / (2 * a)
        yv = self.evaluate(np.array([xv]))[0]
        return float(xv), float(yv)

    def roots(self) -> list[float]:
        a, b, c = self._params["a"], self._params["b"], self._params["c"]
        if abs(a) < 1e-12:
            return []
        sym = sp.Symbol(self.v)
        sols = sp.solve(a * sym**2 + b * sym + c, sym)
        return [float(sp.re(s)) for s in sols if s.is_real]

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        a = self._params["a"]
        v = self.vertex()
        if v is None or abs(a) < 1e-12:
            return super().range_description(x_min, x_max)
        yv = v[1]
        if a > 0:
            return f"[{yv:g}, +∞) (mínimo en vértice)"
        return f"(-∞, {yv:g}] (máximo en vértice)"
