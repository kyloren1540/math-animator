"""Graph rendering and animation."""

from graph.renderer import GraphRenderer

__all__ = ["DrawAnimator", "MplCanvas", "GraphRenderer", "create_toolbar"]


def __getattr__(name: str):
    """Carga componentes Qt solo bajo demanda (app de escritorio)."""
    if name == "DrawAnimator":
        from graph.animator import DrawAnimator

        return DrawAnimator
    if name == "MplCanvas":
        from graph.canvas import MplCanvas

        return MplCanvas
    if name == "create_toolbar":
        from graph.canvas import create_toolbar

        return create_toolbar
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
