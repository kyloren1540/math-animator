"""Qt-embedded matplotlib canvas with navigation."""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from graph.renderer import GraphRenderer


class MplCanvas(FigureCanvasQTAgg):
    """Interactive plot canvas with zoom/pan toolbar support."""

    def __init__(self, parent=None, glow: bool = False):
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.figure.patch.set_facecolor("#0f1419")
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.graph_renderer = GraphRenderer(self.figure, self.ax, glow=glow)
        self.setStyleSheet("background-color: #0f1419;")


def create_toolbar(canvas: MplCanvas, parent) -> NavigationToolbar2QT:
    toolbar = NavigationToolbar2QT(canvas, parent)
    toolbar.setStyleSheet(
        """
        QToolBar { background: #161b22; border: none; spacing: 4px; }
        QToolButton { color: #c9d1d9; background: #21262d; border-radius: 4px; padding: 4px; }
        QToolButton:hover { background: #30363d; }
        """
    )
    return toolbar
