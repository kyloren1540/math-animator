"""Base class for mathematical functions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from functions.variables import independent_var_to_latex, normalize_independent_var


@dataclass
class FunctionMeta:
    """Metadata shown in UI and exports."""

    name: str
    type_id: str
    color: str = "#58a6ff"
    params: dict[str, float] = field(default_factory=dict)
    visible: bool = True
    independent_var: str = "x"


class MathFunction(ABC):
    """Abstract mathematical function with analysis helpers."""

    TYPE_ID: str = "base"
    DISPLAY_NAME: str = "Función"
    PARAM_SPECS: list[tuple[str, str, float]] = []  # (key, label, default)

    def __init__(
        self,
        params: dict[str, float] | None = None,
        color: str | None = None,
        independent_var: str | None = None,
    ):
        self._params = self._default_params()
        if params:
            self._params.update(params)
        self.independent_var = normalize_independent_var(independent_var or "x")
        self.meta = FunctionMeta(
            name=self.formula_text(),
            type_id=self.TYPE_ID,
            color=color or self._next_color(),
            params=dict(self._params),
            independent_var=self.independent_var,
        )

    @classmethod
    def _default_params(cls) -> dict[str, float]:
        return {key: default for key, _, default in cls.PARAM_SPECS}

    @staticmethod
    def _next_color() -> str:
        from functions.factory import COLOR_PALETTE, _color_index

        return COLOR_PALETTE[_color_index() % len(COLOR_PALETTE)]

    @property
    def params(self) -> dict[str, float]:
        return self._params

    @property
    def v(self) -> str:
        """Symbol of the independent variable (e.g. x, t)."""
        return self.independent_var

    @property
    def v_latex(self) -> str:
        return independent_var_to_latex(self.independent_var)

    def set_independent_var(self, var: str) -> None:
        self.independent_var = normalize_independent_var(var)
        self.meta.independent_var = self.independent_var
        self.meta.name = self.formula_text()

    def set_param(self, key: str, value: float) -> None:
        self._params[key] = float(value)
        self.meta.params = dict(self._params)
        self.meta.name = self.formula_text()

    def update_params(self, params: dict[str, float]) -> None:
        for k, v in params.items():
            if k in self._params:
                self.set_param(k, v)

    @abstractmethod
    def evaluate(self, x: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def formula_text(self) -> str:
        pass

    @abstractmethod
    def formula_latex(self) -> str:
        pass

    def x_domain(self, x_min: float = -10.0, x_max: float = 10.0, n: int = 2000) -> np.ndarray:
        return np.linspace(x_min, x_max, n)

    def y_values(self, x: np.ndarray) -> np.ndarray:
        y = self.evaluate(x)
        y = np.asarray(y, dtype=float)
        y[~np.isfinite(y)] = np.nan
        return y

    def domain_description(self) -> str:
        return "ℝ (reales)"

    def range_description(self, x_min: float = -10.0, x_max: float = 10.0) -> str:
        x = self.x_domain(x_min, x_max)
        y = self.y_values(x)
        valid = y[np.isfinite(y)]
        if valid.size == 0:
            return "—"
        return f"[{valid.min():.3g}, {valid.max():.3g}] (aprox. en ventana)"

    def roots(self) -> list[float]:
        return []

    def vertex(self) -> tuple[float, float] | None:
        return None

    def special_points(self) -> list[tuple[float, float, str]]:
        """Annotated points: (indep, dep, label)."""
        points: list[tuple[float, float, str]] = []
        iv = self.v
        for r in self.roots():
            if np.isfinite(r):
                y = float(self.evaluate(np.array([r]))[0])
                if np.isfinite(y):
                    points.append((r, y, f"raíz ({iv}={r:.3g}, {y:.3g})"))
        vtx = self.vertex()
        if vtx is not None:
            points.append((vtx[0], vtx[1], f"vértice ({iv}={vtx[0]:.3g}, {y:.3g})"))
        return points

    def to_dict(self) -> dict[str, Any]:
        return {
            "type_id": self.TYPE_ID,
            "params": self._params,
            "color": self.meta.color,
            "visible": self.meta.visible,
            "independent_var": self.independent_var,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MathFunction:
        from functions.factory import create_function

        return create_function(
            data["type_id"],
            data.get("params"),
            data.get("color"),
            data.get("independent_var"),
        )
