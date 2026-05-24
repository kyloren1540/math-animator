"""Math analysis helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from functions.base import MathFunction


def format_roots(roots: list[float]) -> str:
    if not roots:
        return "Ninguna (real) en ventana"
    return ", ".join(f"x = {r:.4g}" for r in roots)


def intersections_text(
    functions: list[MathFunction], x_min: float, x_max: float
) -> str:
    from graph.renderer import GraphRenderer

    if len(functions) < 2:
        return "— (añade al menos 2 funciones)"

    lines: list[str] = []
    for i in range(len(functions)):
        for j in range(i + 1, len(functions)):
            pts = GraphRenderer.compute_intersections(
                functions[i], functions[j], x_min, x_max
            )
            if pts:
                pts_str = "; ".join(f"({x:.3g}, {y:.3g})" for x, y in pts[:5])
                lines.append(
                    f"{functions[i].formula_text()} ∩ {functions[j].formula_text()}: {pts_str}"
                )
    return "\n".join(lines) if lines else "Sin intersecciones detectadas"
