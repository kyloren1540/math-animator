"""Trigonometric functions with amplitude and frequency."""

from __future__ import annotations

import numpy as np

from functions.base import MathFunction


class SineFunction(MathFunction):
    TYPE_ID = "sine"
    DISPLAY_NAME = "Seno"
    PARAM_SPECS = [
        ("amplitude", "Amplitud (A)", 1.0),
        ("frequency", "Frecuencia (ω)", 1.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a = self._params["amplitude"]
        w = self._params["frequency"]
        return a * np.sin(w * x)

    def formula_text(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return f"f(x) = {a:g}·sin({w:g}x)"

    def formula_latex(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return rf"f(x) = {a:g}\sin({w:g}x)"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        a = abs(self._params["amplitude"])
        return f"[-{a:g}, {a:g}]"


class CosineFunction(MathFunction):
    TYPE_ID = "cosine"
    DISPLAY_NAME = "Coseno"
    PARAM_SPECS = [
        ("amplitude", "Amplitud (A)", 1.0),
        ("frequency", "Frecuencia (ω)", 1.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a = self._params["amplitude"]
        w = self._params["frequency"]
        return a * np.cos(w * x)

    def formula_text(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return f"f(x) = {a:g}·cos({w:g}x)"

    def formula_latex(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return rf"f(x) = {a:g}\cos({w:g}x)"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        a = abs(self._params["amplitude"])
        return f"[-{a:g}, {a:g}]"


class TangentFunction(MathFunction):
    TYPE_ID = "tangent"
    DISPLAY_NAME = "Tangente"
    PARAM_SPECS = [
        ("amplitude", "Amplitud (A)", 1.0),
        ("frequency", "Frecuencia (ω)", 1.0),
    ]

    def evaluate(self, x: np.ndarray) -> np.ndarray:
        a = self._params["amplitude"]
        w = self._params["frequency"]
        return a * np.tan(w * x)

    def formula_text(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return f"f(x) = {a:g}·tan({w:g}x)"

    def formula_latex(self) -> str:
        a, w = self._params["amplitude"], self._params["frequency"]
        return rf"f(x) = {a:g}\tan({w:g}x)"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        return "ℝ (asíntotas verticales)"
