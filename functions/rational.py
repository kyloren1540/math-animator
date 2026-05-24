"""Rational function f(x) = p(x) / q(x) with simple polynomials."""

from __future__ import annotations

import numpy as np
import sympy as sp

from functions.base import MathFunction


class RationalFunction(MathFunction):
    TYPE_ID = "rational"
    DISPLAY_NAME = "Racional"
    PARAM_SPECS = [
        ("p0", "Num. constante", 1.0),
        ("p1", "Num. x", 0.0),
        ("q0", "Den. constante", 1.0),
        ("q1", "Den. x", 1.0),
    ]

    def _numerator(self, x: np.ndarray) -> np.ndarray:
        p0, p1 = self._params["p0"], self._params["p1"]
        return p0 + p1 * x

    def _denominator(self, x: np.ndarray) -> np.ndarray:
        q0, q1 = self._params["q0"], self._params["q1"]
        return q0 + q1 * x

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        num = self._numerator(x)
        den = self._denominator(x)
        with np.errstate(divide="ignore", invalid="ignore"):
            y = num / den
        y[np.abs(den) < 1e-10] = np.nan
        return y

    def formula_text(self) -> str:
        p0, p1 = self._params["p0"], self._params["p1"]
        q0, q1 = self._params["q0"], self._params["q1"]
        num = f"{p0:g}" if abs(p1) < 1e-12 else f"{p0:g} + {p1:g}x"
        den = f"{q0:g}" if abs(q1) < 1e-12 else f"{q0:g} + {q1:g}x"
        return f"f(x) = ({num}) / ({den})"

    def formula_latex(self) -> str:
        p0, p1 = self._params["p0"], self._params["p1"]
        q0, q1 = self._params["q0"], self._params["q1"]
        return rf"f(x) = \frac{{{p0:g} + {p1:g}x}}{{{q0:g} + {q1:g}x}}"

    def domain_description(self) -> str:
        q0, q1 = self._params["q0"], self._params["q1"]
        if abs(q1) < 1e-12:
            if abs(q0) < 1e-12:
                return "— (denominador nulo)"
            return "ℝ"
        pole = -q0 / q1
        return f"ℝ \\ {{ {pole:g} }}"

    def roots(self) -> list[float]:
        p0, p1 = self._params["p0"], self._params["p1"]
        if abs(p1) < 1e-12:
            return []
        return [float(-p0 / p1)]
