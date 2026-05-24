"""Export graph to PNG."""

from __future__ import annotations

from pathlib import Path

from matplotlib.figure import Figure


def export_figure_png(figure: Figure, path: str | Path, dpi: int = 150) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        path,
        dpi=dpi,
        facecolor=figure.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
