"""Predefined function sets for quick demos."""

from __future__ import annotations

from dataclasses import dataclass

from functions.base import MathFunction
from functions.factory import create_function

COLOR_BLUE = "#6cb6ff"
COLOR_GREEN = "#56d364"
COLOR_GOLD = "#e3b341"
COLOR_PINK = "#f778ba"
COLOR_PURPLE = "#bc8cff"
COLOR_CORAL = "#ff9b8a"


@dataclass(frozen=True)
class FunctionSpec:
    type_id: str
    params: dict[str, float] | None = None
    color: str | None = None
    independent_var: str | None = None


@dataclass(frozen=True)
class ExamplePreset:
    id: str
    title: str
    description: str
    functions: tuple[FunctionSpec, ...]
    default_independent_var: str = "x"


EXAMPLES: tuple[ExamplePreset, ...] = (
    ExamplePreset(
        id="parabola",
        title="Parábola clásica",
        description="y = x² − 4: vértice en (0, −4) y dos raíces reales.",
        functions=(
            FunctionSpec("quadratic", {"a": 1, "b": 0, "c": -4}, COLOR_BLUE),
        ),
    ),
    ExamplePreset(
        id="seno_coseno",
        title="Seno y coseno",
        description="Compara f(x) = sin(x) y g(x) = cos(x) en la misma ventana.",
        functions=(
            FunctionSpec("sine", {"amplitude": 1, "frequency": 1}, COLOR_BLUE),
            FunctionSpec("cosine", {"amplitude": 1, "frequency": 1}, COLOR_GREEN),
        ),
    ),
    ExamplePreset(
        id="recta_parabola",
        title="Recta y parábola",
        description="Intersecciones entre y = 0.5x + 1 y y = x² − 2.",
        functions=(
            FunctionSpec("linear", {"m": 0.5, "b": 1}, COLOR_BLUE),
            FunctionSpec("quadratic", {"a": 1, "b": 0, "c": -2}, COLOR_GOLD),
        ),
    ),
    ExamplePreset(
        id="exponencial_log",
        title="Exponencial y logaritmo",
        description="2ˣ y ln(x): funciones inversas (reflexión sobre y = x).",
        functions=(
            FunctionSpec("exponential", {"a": 2}, COLOR_BLUE),
            FunctionSpec("logarithmic", {}, COLOR_GREEN),
        ),
    ),
    ExamplePreset(
        id="valor_absoluto",
        title="Valor absoluto",
        description="f(x) = |x|: forma en V con vértice en el origen.",
        functions=(FunctionSpec("absolute", {}, COLOR_BLUE),),
    ),
    ExamplePreset(
        id="ondas",
        title="Ondas de distinta frecuencia",
        description="sin(2x) y sin(x): distinta periodicidad en el mismo gráfico.",
        functions=(
            FunctionSpec("sine", {"amplitude": 1, "frequency": 2}, COLOR_BLUE),
            FunctionSpec("sine", {"amplitude": 1, "frequency": 1}, COLOR_PINK),
        ),
    ),
    ExamplePreset(
        id="racional",
        title="Función racional",
        description="(1 + x) / (1 − x): asíntota vertical en x = 1.",
        functions=(
            FunctionSpec(
                "rational",
                {"p0": 1, "p1": 1, "q0": 1, "q1": -1},
                COLOR_CORAL,
            ),
        ),
    ),
    ExamplePreset(
        id="cubica",
        title="Cúbica con inflexión",
        description="0.25x³ − 1.5x: curva con punto de inflexión en el origen.",
        functions=(
            FunctionSpec(
                "cubic",
                {"a": 0.25, "b": 0, "c": -1.5, "d": 0},
                COLOR_PURPLE,
            ),
        ),
    ),
    ExamplePreset(
        id="tangente",
        title="Tangente",
        description="tan(x): período π y asíntotas verticales.",
        functions=(
            FunctionSpec("tangent", {"amplitude": 1, "frequency": 1}, COLOR_BLUE),
        ),
    ),
    ExamplePreset(
        id="piso_techo",
        title="Constante y seno",
        description="Compara una recta horizontal con una onda sinusoidal.",
        functions=(
            FunctionSpec("constant", {"c": 2}, COLOR_GOLD),
            FunctionSpec("sine", {"amplitude": 1.5, "frequency": 1}, COLOR_BLUE),
        ),
    ),
    ExamplePreset(
        id="tiempo",
        title="Seno en el tiempo",
        description="f(t) = sin(t): variable independiente t (tiempo).",
        default_independent_var="t",
        functions=(
            FunctionSpec("sine", {"amplitude": 1, "frequency": 1}, COLOR_BLUE),
        ),
    ),
)

_EXAMPLES_BY_ID = {ex.id: ex for ex in EXAMPLES}


def example_choices() -> list[tuple[str, str]]:
    """Return (id, title) pairs for UI lists."""
    return [(ex.id, ex.title) for ex in EXAMPLES]


def get_example(example_id: str) -> ExamplePreset | None:
    return _EXAMPLES_BY_ID.get(example_id)


def create_functions_from_example(example_id: str) -> list[MathFunction]:
    preset = get_example(example_id)
    if preset is None:
        raise ValueError(f"Ejemplo desconocido: {example_id}")
    return [
        create_function(
            spec.type_id,
            spec.params,
            spec.color,
            spec.independent_var or preset.default_independent_var,
        )
        for spec in preset.functions
    ]
