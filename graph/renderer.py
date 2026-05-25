"""Matplotlib rendering for multiple functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

if TYPE_CHECKING:
    from functions.base import MathFunction

# Minimal dark theme (applied per-axes, not via global rcParams)
BG_FIGURE = "#0f1419"
BG_AXES = "#151b23"
GRID_COLOR = "#2a3140"
SPINE_COLOR = "#3d4654"
TEXT_MUTED = "#8b949e"
TEXT_MAIN = "#e6edf3"
ORIGIN_COLOR = "#484f58"


class GraphRenderer:
    """Draws functions on a matplotlib Axes with optional soft glow."""

    LINE_WIDTH = 2.0
    GLOW_WIDTH = 5.0
    GLOW_ALPHA = 0.18
    MARKER_SIZE = 28
    HEAD_MARKER_SIZE = 90
    MAX_CURVE_MARKERS = 24

    def __init__(self, figure: Figure, axes: Axes, glow: bool = False):
        self.figure = figure
        self.ax = axes
        self.glow = glow
        self.show_curve_points = True
        self._lines: dict[int, Line2D] = {}
        self._glow_lines: dict[int, Line2D] = {}
        self._point_artists: list = []
        self._curve_scatters: dict[int, PathCollection] = {}
        self._head_markers: dict[int, Line2D] = {}
        self._origin_lines: list[Line2D] = []
        self.x_min = -10.0
        self.x_max = 10.0
        self._apply_style()

    def _apply_style(self) -> None:
        self.figure.patch.set_facecolor(BG_FIGURE)
        self.ax.set_facecolor(BG_AXES)
        self.ax.set_xlabel("x", color=TEXT_MUTED, fontsize=10, labelpad=6)
        self.ax.set_ylabel("f(x)", color=TEXT_MUTED, fontsize=10, labelpad=6)
        self.ax.tick_params(
            colors=TEXT_MUTED, labelsize=9, length=4, width=0.8, pad=4
        )
        self.ax.grid(
            True,
            linestyle="-",
            linewidth=0.6,
            alpha=0.45,
            color=GRID_COLOR,
            zorder=0,
        )
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xlim(self.x_min, self.x_max)

    def _draw_origin_axes(self) -> None:
        # After ax.clear(), old references are invalid; only remove live artists.
        for line in self._origin_lines:
            if line.axes is not None:
                line.remove()
        self._origin_lines.clear()
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        if xlim[0] <= 0 <= xlim[1]:
            self._origin_lines.append(
                self.ax.axvline(
                    0,
                    color=ORIGIN_COLOR,
                    linewidth=0.9,
                    zorder=0.5,
                    linestyle="-",
                )
            )
        if ylim[0] <= 0 <= ylim[1]:
            self._origin_lines.append(
                self.ax.axhline(
                    0,
                    color=ORIGIN_COLOR,
                    linewidth=0.9,
                    zorder=0.5,
                    linestyle="-",
                )
            )

    def _update_axis_labels(self, functions: list[MathFunction]) -> None:
        if not functions:
            self.ax.set_xlabel("x", color=TEXT_MUTED)
            self.ax.set_ylabel("f(x)", color=TEXT_MUTED)
            return
        iv = functions[0].independent_var
        for fn in functions[1:]:
            if fn.independent_var != iv:
                iv = f"{functions[0].independent_var}…"
                break
        iv_label = functions[0].independent_var if "…" not in iv else "x"
        self.ax.set_xlabel(iv_label, color=TEXT_MUTED, fontsize=10, labelpad=6)
        self.ax.set_ylabel(f"f({iv_label})", color=TEXT_MUTED, fontsize=10, labelpad=6)

    def set_xlim(self, x_min: float, x_max: float) -> None:
        self.x_min, self.x_max = x_min, x_max
        self.ax.set_xlim(x_min, x_max)

    def clear(self) -> None:
        self._clear_curve_markers()
        self.ax.clear()
        self._apply_style()
        self._lines.clear()
        self._glow_lines.clear()
        self._point_artists.clear()
        self._curve_scatters.clear()
        self._head_markers.clear()

    @staticmethod
    def _safe_remove_artist(artist) -> None:
        try:
            if artist.axes is not None:
                artist.remove()
        except (NotImplementedError, ValueError):
            pass

    def _remove_curve_markers_for(self, index: int) -> None:
        if index in self._curve_scatters:
            self._safe_remove_artist(self._curve_scatters[index])
            del self._curve_scatters[index]
        if index in self._head_markers:
            self._safe_remove_artist(self._head_markers[index])
            del self._head_markers[index]

    def _clear_curve_markers(self) -> None:
        for index in list(self._curve_scatters.keys()):
            self._remove_curve_markers_for(index)

    def _x_array(self, n: int = 2000) -> np.ndarray:
        return np.linspace(self.x_min, self.x_max, n)

    @staticmethod
    def _mask_discontinuities(y: np.ndarray) -> np.ndarray:
        """Break line segments at asymptotes and vertical jumps."""
        y = np.asarray(y, dtype=float).copy()
        if y.size < 2:
            return y
        finite = y[np.isfinite(y)]
        if finite.size == 0:
            return y
        scale = float(np.nanpercentile(np.abs(finite), 90))
        threshold = max(25.0, scale * 4.0)
        dy = np.abs(np.diff(y))
        for i in np.where((dy > threshold) | ~np.isfinite(dy))[0]:
            y[i + 1] = np.nan
        return y

    def _plot_curve(
        self, x: np.ndarray, y: np.ndarray, color: str, label: str, index: int
    ) -> None:
        y = self._mask_discontinuities(y)
        if self.glow:
            glow_line, = self.ax.plot(
                x,
                y,
                color=color,
                alpha=self.GLOW_ALPHA,
                linewidth=self.GLOW_WIDTH,
                solid_capstyle="round",
                zorder=1,
            )
            self._glow_lines[index] = glow_line
        line, = self.ax.plot(
            x,
            y,
            color=color,
            linewidth=self.LINE_WIDTH,
            label=label,
            solid_capstyle="round",
            zorder=2,
        )
        self._lines[index] = line

    def _style_legend(self) -> None:
        if not self.ax.get_legend_handles_labels()[1]:
            return
        leg = self.ax.legend(
            loc="upper right",
            fontsize=9,
            frameon=True,
            framealpha=0.85,
            facecolor=BG_AXES,
            edgecolor=SPINE_COLOR,
            labelcolor=TEXT_MAIN,
        )
        leg.get_frame().set_linewidth(0.6)

    def _mark_curve_points(
        self,
        x: np.ndarray,
        y: np.ndarray,
        color: str,
        index: int,
        *,
        highlight_head: bool = False,
    ) -> None:
        """Dots along the drawn line; optional head marks animation tip."""
        self._remove_curve_markers_for(index)

        y = np.asarray(y, dtype=float)
        mask = np.isfinite(y)
        xi, yi = x[mask], y[mask]
        if xi.size < 1:
            return

        step = max(1, int(np.ceil(xi.size / self.MAX_CURVE_MARKERS)))
        scatter = self.ax.scatter(
            xi[::step],
            yi[::step],
            c=color,
            s=self.MARKER_SIZE,
            alpha=0.85,
            edgecolors=BG_AXES,
            linewidths=0.8,
            zorder=3,
        )
        self._curve_scatters[index] = scatter

        if highlight_head and xi.size > 0:
            head = self.ax.plot(
                xi[-1],
                yi[-1],
                "o",
                color=color,
                markersize=9,
                markeredgecolor="#ffffff",
                markeredgewidth=1.5,
                zorder=5,
            )[0]
            self._head_markers[index] = head

    def _mark_special_points(self, fn: MathFunction, color: str) -> None:
        for px, py, lbl in fn.special_points():
            pt = self.ax.plot(
                px,
                py,
                "o",
                color=color,
                markersize=5,
                markeredgecolor=BG_AXES,
                markeredgewidth=1.2,
                zorder=4,
            )[0]
            self._point_artists.append(pt)
            self.ax.annotate(
                lbl,
                (px, py),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=8,
                color=TEXT_MUTED,
                bbox=dict(
                    boxstyle="round,pad=0.25",
                    facecolor=BG_AXES,
                    edgecolor=SPINE_COLOR,
                    alpha=0.9,
                    linewidth=0.5,
                ),
            )

    def draw_full(
        self,
        functions: list[MathFunction],
        show_legend: bool = True,
        show_points: bool = True,
    ) -> None:
        self.clear()
        x = self._x_array()
        for i, fn in enumerate(functions):
            if not fn.meta.visible:
                continue
            y = fn.y_values(x)
            self._plot_curve(x, y, fn.meta.color, fn.formula_text(), i)
            if self.show_curve_points:
                self._mark_curve_points(x, y, fn.meta.color, i)
            if show_points:
                self._mark_special_points(fn, fn.meta.color)

        if show_legend and functions:
            self._style_legend()
        self._autoscale_y(functions, x)
        self._update_axis_labels(functions)
        self._draw_origin_axes()
        self.figure.subplots_adjust(left=0.09, right=0.97, top=0.97, bottom=0.11)

    def draw_partial(
        self,
        functions: list[MathFunction],
        progress: float,
        show_legend: bool = True,
    ) -> None:
        """Draw curves up to `progress` in [0, 1] left-to-right."""
        progress = max(0.0, min(1.0, progress))
        x_full = self._x_array()
        n_visible = max(2, int(len(x_full) * progress))
        x = x_full[:n_visible]

        active = {i for i, fn in enumerate(functions) if fn.meta.visible}
        self._prune_stale_lines(active)

        if not self._lines and progress > 0:
            self.clear()

        for i, fn in enumerate(functions):
            if not fn.meta.visible:
                continue
            y = fn.y_values(x_full)[:n_visible]
            y = self._mask_discontinuities(y)
            color = fn.meta.color
            label = fn.formula_text()
            if i in self._lines:
                self._lines[i].set_data(x, y)
                if i in self._glow_lines:
                    self._glow_lines[i].set_data(x, y)
            else:
                self._plot_curve(x, y, color, label, i)

            if self.show_curve_points:
                self._mark_curve_points(
                    x, y, color, i, highlight_head=progress < 1.0
                )

        if show_legend and functions:
            handles, labels = self.ax.get_legend_handles_labels()
            if labels:
                self._style_legend()

        self._autoscale_y(functions, x_full)
        self._update_axis_labels(functions)
        self._draw_origin_axes()

    def _prune_stale_lines(self, active: set[int]) -> None:
        for i in list(self._lines.keys()):
            if i not in active:
                self._lines[i].remove()
                del self._lines[i]
                if i in self._glow_lines:
                    self._glow_lines[i].remove()
                    del self._glow_lines[i]
                self._remove_curve_markers_for(i)

    def _autoscale_y(
        self, functions: list[MathFunction], x: np.ndarray
    ) -> None:
        ys = []
        for fn in functions:
            if fn.meta.visible:
                y = fn.y_values(x)
                valid = y[np.isfinite(y)]
                if valid.size:
                    ys.append(valid)
        if not ys:
            self.ax.set_ylim(-10, 10)
            return
        all_y = np.concatenate(ys)
        lo, hi = np.percentile(all_y, [2, 98])
        margin = max(0.5, (hi - lo) * 0.12)
        if hi - lo < 1e-6:
            lo, hi = -5, 5
        self.ax.set_ylim(lo - margin, hi + margin)

    @staticmethod
    def compute_intersections(
        f1: MathFunction,
        f2: MathFunction,
        x_min: float,
        x_max: float,
        n: int = 500,
    ) -> list[tuple[float, float]]:
        x = np.linspace(x_min, x_max, n)
        y1 = f1.y_values(x)
        y2 = f2.y_values(x)
        diff = y1 - y2
        points: list[tuple[float, float]] = []
        for i in range(len(x) - 1):
            if not (np.isfinite(diff[i]) and np.isfinite(diff[i + 1])):
                continue
            if diff[i] * diff[i + 1] <= 0 and abs(diff[i + 1] - diff[i]) > 1e-12:
                t = -diff[i] / (diff[i + 1] - diff[i])
                xi = x[i] + t * (x[i + 1] - x[i])
                yi = float(f1.evaluate(np.array([xi]))[0])
                if np.isfinite(yi):
                    points.append((float(xi), yi))
        return points
