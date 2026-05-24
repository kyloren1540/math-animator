"""Main application window."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from functions.base import MathFunction
from functions.examples import create_functions_from_example
from functions.factory import create_function
from graph.animator import DrawAnimator
from graph.canvas import MplCanvas, create_toolbar
from ui.side_panel import SidePanel
from ui.styles import DARK_THEME
from utils.export import export_figure_png
from utils.json_io import export_functions, import_functions
from utils.math_helpers import format_roots, intersections_text

# Matplotlib LaTeX formula widget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FormulaCanvas
from matplotlib.figure import Figure


class FormulaWidget(QWidget):
    """Small matplotlib canvas for LaTeX formula."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 0.6), dpi=100)
        self.figure.patch.set_facecolor("#151b23")
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")
        self.canvas = FormulaCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def set_latex(self, latex: str) -> None:
        self.ax.clear()
        self.ax.axis("off")
        if latex:
            self.ax.text(
                0.5,
                0.5,
                f"${latex}$",
                ha="center",
                va="center",
                fontsize=14,
                color="#79c0ff",
                transform=self.ax.transAxes,
            )
        self.canvas.draw_idle()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Animator — Visualizador de Funciones")
        self.resize(1280, 800)
        self._functions: list[MathFunction] = []
        self._draft: MathFunction | None = None
        self._selected_index = -1
        self._live_timer = QTimer(self)
        self._live_timer.setSingleShot(True)
        self._live_timer.setInterval(80)
        self._live_timer.timeout.connect(self._plot)
        self._build_ui()
        self._connect_signals()
        self._refresh_draft()
        if self.side.live_check.isChecked():
            self._plot()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.side = SidePanel()
        splitter.addWidget(self.side)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(10)

        self.formula_widget = FormulaWidget()
        self.formula_widget.setObjectName("formulaLabel")

        info_frame = QFrame()
        info_frame.setStyleSheet(
            "QFrame { background: #151b23; border-radius: 8px; border: 1px solid #2a3140; }"
        )
        info_layout = QVBoxLayout(info_frame)
        self.info_domain = QLabel("Dominio: —")
        self.info_range = QLabel("Rango: —")
        self.info_roots = QLabel("Raíces: —")
        self.info_vertex = QLabel("Vértice: —")
        self.info_intersections = QLabel("Intersecciones: —")
        for lbl in (
            self.info_domain,
            self.info_range,
            self.info_roots,
            self.info_vertex,
            self.info_intersections,
        ):
            lbl.setObjectName("infoLabel")
            lbl.setWordWrap(True)
            info_layout.addWidget(lbl)

        self.canvas = MplCanvas(glow=False)
        self.toolbar = create_toolbar(self.canvas, self)
        self.progress_label = QLabel("Progreso animación: 0%")
        self.progress_label.setObjectName("infoLabel")

        right_layout.addWidget(self.formula_widget)
        right_layout.addWidget(info_frame)
        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.canvas, stretch=1)
        right_layout.addWidget(self.progress_label)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter)

        self.animator = DrawAnimator(
            self.canvas,
            self.canvas.graph_renderer,
            self._active_functions,
            on_frame=self._on_anim_frame,
        )

    def _connect_signals(self) -> None:
        self.side.function_type_changed.connect(self._on_type_changed)
        self.side.param_changed.connect(self._on_param_changed)
        self.side.plot_clicked.connect(self._plot)
        self.side.animate_clicked.connect(self._start_animate)
        self.side.stop_clicked.connect(self._stop_animate)
        self.side.pause_clicked.connect(self._toggle_pause)
        self.side.restart_clicked.connect(self.animator.restart)
        self.side.add_clicked.connect(self._add_function)
        self.side.remove_clicked.connect(self._remove_function)
        self.side.export_png_clicked.connect(self._export_png)
        self.side.export_json_clicked.connect(self._export_json)
        self.side.import_json_clicked.connect(self._import_json)
        self.side.history_selected.connect(self._select_history)
        self.side.glow_toggled.connect(self._toggle_glow)
        self.side.speed_changed.connect(self.animator.set_speed)
        self.side.live_update_toggled.connect(self._on_live_toggle)
        self.side.example_load_clicked.connect(self._load_example)

    def _active_functions(self) -> list[MathFunction]:
        """Functions on the graph; preview draft when the list is empty."""
        if self._functions:
            return self._functions
        return [self._draft] if self._draft else []

    def _refresh_draft(self) -> None:
        type_id = self.side.current_type_id()
        params = self.side.get_params()
        self._draft = create_function(type_id, params)
        self._update_info(self._draft)

    def _on_type_changed(self, _type_id: str) -> None:
        self._refresh_draft()

    def _on_param_changed(self, key: str, value: float) -> None:
        if self._draft:
            self._draft.set_param(key, value)
        if self._selected_index >= 0 and self._selected_index < len(self._functions):
            self._functions[self._selected_index].set_param(key, value)
            self._update_history_list()
        self._update_info(self._draft)
        if self.side.live_check.isChecked():
            self._live_timer.start()

    def _on_live_toggle(self, enabled: bool) -> None:
        if enabled and self._active_functions():
            self._plot()

    def _load_example(self, example_id: str) -> None:
        self.animator.stop()
        try:
            self._functions = create_functions_from_example(example_id)
        except ValueError as e:
            QMessageBox.warning(self, "Ejemplo", str(e))
            return
        self._selected_index = 0 if self._functions else -1
        self._update_history_list(select=self._selected_index)
        if self._functions:
            fn = self._functions[0]
            for i in range(self.side.type_combo.count()):
                if self.side.type_combo.itemData(i) == fn.TYPE_ID:
                    self.side.type_combo.blockSignals(True)
                    self.side.type_combo.setCurrentIndex(i)
                    self.side.type_combo.blockSignals(False)
                    break
            self.side.param_panel.load_from_function(fn)
            self._draft = create_function(fn.TYPE_ID, dict(fn.params), fn.meta.color)
        else:
            self._refresh_draft()
        self._plot()

    def _add_function(self) -> None:
        self._refresh_draft()
        if self._draft:
            self._functions.append(self._draft)
            self._draft = create_function(
                self.side.current_type_id(), self.side.get_params()
            )
            self._selected_index = len(self._functions) - 1
            self._update_history_list(select=self._selected_index)
            self._plot()

    def _remove_function(self) -> None:
        idx = self.side.history_list.currentRow()
        if 0 <= idx < len(self._functions):
            self._functions.pop(idx)
            self._selected_index = min(idx, len(self._functions) - 1)
            self._update_history_list()
            self._plot()

    def _select_history(self, index: int) -> None:
        if 0 <= index < len(self._functions):
            self._selected_index = index
            fn = self._functions[index]
            # Sync combo and params
            for i in range(self.side.type_combo.count()):
                if self.side.type_combo.itemData(i) == fn.TYPE_ID:
                    self.side.type_combo.blockSignals(True)
                    self.side.type_combo.setCurrentIndex(i)
                    self.side.type_combo.blockSignals(False)
                    break
            self.side.param_panel.load_from_function(fn)
            self._update_info(fn)

    def _update_history_list(self, select: int = -1) -> None:
        items = [
            f"{i + 1}. {fn.formula_text()}" for i, fn in enumerate(self._functions)
        ]
        self.side.update_history(items, select=select)

    def _update_info(self, fn: MathFunction | None) -> None:
        if fn is None:
            return
        self.formula_widget.set_latex(fn.formula_latex())
        self.info_domain.setText(f"Dominio: {fn.domain_description()}")
        self.info_range.setText(f"Rango: {fn.range_description()}")
        self.info_roots.setText(f"Raíces: {format_roots(fn.roots())}")
        v = fn.vertex()
        self.info_vertex.setText(
            f"Vértice: ({v[0]:.4g}, {v[1]:.4g})" if v else "Vértice: —"
        )
        if len(self._functions) >= 2:
            self.info_intersections.setText(
                "Intersecciones:\n"
                + intersections_text(
                    self._functions,
                    self.canvas.graph_renderer.x_min,
                    self.canvas.graph_renderer.x_max,
                )
            )
        else:
            self.info_intersections.setText("Intersecciones: —")

    def _plot(self) -> None:
        self.animator.stop()
        funcs = self._active_functions()
        self.canvas.graph_renderer.glow = self.side.glow_check.isChecked()
        self.canvas.graph_renderer.draw_full(funcs)
        self.canvas.draw_idle()
        if self._functions:
            idx = self._selected_index if 0 <= self._selected_index < len(self._functions) else -1
            self._update_info(self._functions[idx])
        elif self._draft:
            self._update_info(self._draft)
        self.progress_label.setText("Progreso animación: —")

    def _start_animate(self) -> None:
        if not self._functions:
            QMessageBox.information(
                self, "Animar", "Añade al menos una función antes de animar."
            )
            return
        self.animator.loop = True
        self.animator.start()

    def _stop_animate(self) -> None:
        self.animator.stop()
        self._plot()

    def _toggle_pause(self) -> None:
        paused = self.animator.toggle_pause()
        self.side.pause_btn.setText("▶" if paused else "⏸")

    def _on_anim_frame(self, progress: float) -> None:
        self.progress_label.setText(
            f"Progreso animación: {int(progress * 100)}%"
        )

    def _toggle_glow(self, enabled: bool) -> None:
        self.canvas.graph_renderer.glow = enabled
        self._plot()

    def _export_png(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar PNG", "grafica.png", "PNG (*.png)"
        )
        if path:
            export_figure_png(self.canvas.figure, path)
            QMessageBox.information(self, "Exportar", f"Guardado en:\n{path}")

    def _export_json(self) -> None:
        if not self._functions:
            QMessageBox.warning(self, "Exportar", "No hay funciones para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar JSON", "funciones.json", "JSON (*.json)"
        )
        if path:
            export_functions(self._functions, path)
            QMessageBox.information(self, "Exportar", f"Guardado en:\n{path}")

    def _import_json(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Importar JSON", "", "JSON (*.json)"
        )
        if path:
            try:
                self._functions = import_functions(path)
                self._selected_index = len(self._functions) - 1 if self._functions else -1
                self._update_history_list(select=self._selected_index)
                self._plot()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo importar:\n{e}")


def run_app() -> int:
    # High DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_THEME)
    win = MainWindow()
    win.show()
    return app.exec()
