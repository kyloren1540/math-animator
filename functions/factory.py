"""Factory and registry for function types."""

from __future__ import annotations

from typing import Type

from functions.absolute import AbsoluteFunction
from functions.base import MathFunction
from functions.constant import ConstantFunction
from functions.cubic import CubicFunction
from functions.exponential import ExponentialFunction
from functions.linear import LinearFunction
from functions.logarithmic import LogarithmicFunction
from functions.quadratic import QuadraticFunction
from functions.rational import RationalFunction
from functions.trigonometric import CosineFunction, SineFunction, TangentFunction

COLOR_PALETTE = [
    "#6cb6ff",
    "#56d364",
    "#e3b341",
    "#f778ba",
    "#bc8cff",
    "#ff9b8a",
    "#79d4ff",
    "#7ee787",
]

_color_counter = 0


def _color_index() -> int:
    global _color_counter
    idx = _color_counter
    _color_counter += 1
    return idx


FUNCTION_REGISTRY: dict[str, Type[MathFunction]] = {
    LinearFunction.TYPE_ID: LinearFunction,
    QuadraticFunction.TYPE_ID: QuadraticFunction,
    CubicFunction.TYPE_ID: CubicFunction,
    ExponentialFunction.TYPE_ID: ExponentialFunction,
    LogarithmicFunction.TYPE_ID: LogarithmicFunction,
    SineFunction.TYPE_ID: SineFunction,
    CosineFunction.TYPE_ID: CosineFunction,
    TangentFunction.TYPE_ID: TangentFunction,
    RationalFunction.TYPE_ID: RationalFunction,
    AbsoluteFunction.TYPE_ID: AbsoluteFunction,
    ConstantFunction.TYPE_ID: ConstantFunction,
}


def function_choices() -> list[tuple[str, str]]:
    return [(cls.TYPE_ID, cls.DISPLAY_NAME) for cls in FUNCTION_REGISTRY.values()]


def create_function(
    type_id: str,
    params: dict[str, float] | None = None,
    color: str | None = None,
    independent_var: str | None = None,
) -> MathFunction:
    cls = FUNCTION_REGISTRY.get(type_id)
    if cls is None:
        raise ValueError(f"Tipo de función desconocido: {type_id}")
    return cls(params=params, color=color, independent_var=independent_var)
